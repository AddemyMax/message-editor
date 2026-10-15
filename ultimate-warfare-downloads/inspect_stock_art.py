#!/usr/bin/env python3
"""Private visual references from the owner's game; never edit installed data.

Writes PNG previews and a metadata report outside the game. These images are
original game artwork and must not be bundled in the distributable source kit.
Python 3.10+ standard library only. No executables are launched.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import struct
import zlib

from uwmod.ini import parse_ini
from uwmod.project import GameSource, PROJECT, _inside, _atomic_write


def texture_names(data: bytes, depth=0) -> list[str]:
    if depth > 16:
        raise ValueError('Excessive W3D chunk depth')
    cursor = 0
    names = []
    while cursor < len(data):
        if cursor + 8 > len(data):
            raise ValueError('Truncated W3D chunk')
        kind, packed = struct.unpack_from('<II', data, cursor)
        size = packed & 0x7fffffff
        end = cursor + 8 + size
        if end > len(data):
            raise ValueError('W3D chunk exceeds container')
        payload = data[cursor+8:end]
        if packed & 0x80000000:
            names.extend(texture_names(payload, depth+1))
        elif kind == 0x32:
            name = payload.rstrip(b'\x00').decode('ascii')
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', name):
                raise ValueError('Unsupported texture filename')
            names.append(name)
        cursor = end
    return list(dict.fromkeys(names))


def _dimensions(w, h):
    if not 0 < w <= 2048 or not 0 < h <= 2048:
        raise ValueError('Reference image dimensions exceed supported limits')


def decode_tga(data: bytes):
    if len(data) < 18 or data[1] != 0 or data[2] not in (2, 10) or data[16] not in (24, 32):
        raise ValueError('Supported TGA formats: RGB/RGBA, raw or RLE')
    w, h = struct.unpack_from('<HH', data, 12)
    _dimensions(w, h)
    step = data[16]//8
    cursor = 18+data[0]
    pixels = []
    def take(n):
        nonlocal cursor
        if cursor+n > len(data):
            raise ValueError('Truncated TGA payload')
        result = data[cursor:cursor+n]
        cursor += n
        return result
    while len(pixels) < w*h:
        packet = take(1)[0] if data[2] == 10 else 0
        count = (packet & 127)+1
        if len(pixels)+count > w*h:
            raise ValueError('TGA packet exceeds image')
        if packet & 128:
            p = take(step)
            pixels.extend([bytes((p[2],p[1],p[0]))]*count)
        else:
            for _ in range(count):
                p = take(step)
                pixels.append(bytes((p[2],p[1],p[0])))
    rows = [pixels[y*w:(y+1)*w] for y in range(h)]
    if not data[17] & 32:
        rows.reverse()
    if data[17] & 16:
        rows = [list(reversed(row)) for row in rows]
    return w, h, b''.join(p for row in rows for p in row)


def decode_dds(data: bytes):
    if len(data) < 128 or data[:4] != b'DDS ' or struct.unpack_from('<I',data,4)[0] != 124:
        raise ValueError('Invalid DDS header')
    h,w = struct.unpack_from('<II',data,12)
    _dimensions(w,h)
    flags = struct.unpack_from('<I',data,80)[0]
    fourcc = data[84:88]
    output = bytearray(w*h*3)
    if flags & 4:
        if fourcc not in (b'DXT1',b'DXT3',b'DXT5'):
            raise ValueError('Supported compressed DDS formats: DXT1/3/5')
        step = 8 if fourcc == b'DXT1' else 16
        cursor = 128
        for by in range(0,h,4):
            for bx in range(0,w,4):
                if cursor+step > len(data):
                    raise ValueError('Truncated DDS blocks')
                color_at = cursor + (0 if step==8 else 8)
                a,b,indices = struct.unpack_from('<HHI',data,color_at)
                def rgb565(c):
                    return ((c>>11)*255//31,((c>>5)&63)*255//63,(c&31)*255//31)
                ca,cb = rgb565(a),rgb565(b)
                if a>b or fourcc != b'DXT1':
                    colors = [ca,cb,tuple((2*x+y)//3 for x,y in zip(ca,cb)),tuple((x+2*y)//3 for x,y in zip(ca,cb))]
                else:
                    colors = [ca,cb,tuple((x+y)//2 for x,y in zip(ca,cb)),(0,0,0)]
                for index in range(16):
                    x,y = bx+index%4,by+index//4
                    if x<w and y<h:
                        start = (y*w+x)*3
                        output[start:start+3] = bytes(colors[(indices>>(2*index))&3])
                cursor += step
    else:
        bits = struct.unpack_from('<I',data,88)[0]
        if not flags & 64 or bits not in (24,32):
            raise ValueError('Supported raw DDS: 24/32-bit RGB')
        masks = struct.unpack_from('<III',data,92)
        if any(not mask for mask in masks):
            raise ValueError('Invalid DDS color masks')
        has_pitch = struct.unpack_from('<I',data,8)[0] & 8
        pitch = max(w*(bits//8),struct.unpack_from('<I',data,20)[0]) if has_pitch else w*(bits//8)
        if pitch*h > len(data)-128:
            raise ValueError('Truncated raw DDS image')
        for y in range(h):
            for x in range(w):
                start = 128+y*pitch+x*(bits//8)
                value = int.from_bytes(data[start:start+bits//8],'little')
                output[(y*w+x)*3:(y*w+x)*3+3] = bytes(((value&mask)*255//mask) for mask in masks)
    return w,h,bytes(output)


def png(w,h,rgb):
    if len(rgb) != w*h*3:
        raise ValueError('RGB size mismatch')
    def chunk(name,data):
        return struct.pack('>I',len(data))+name+data+struct.pack('>I',zlib.crc32(name+data)&0xffffffff)
    scan = b''.join(b'\x00'+rgb[y*w*3:(y+1)*w*3] for y in range(h))
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))
            +chunk(b'IDAT',zlib.compress(scan))+chunk(b'IEND',b''))


def inspect(game_dir: Path, output: Path):
    source = GameSource(game_dir)
    if _inside(output, source.game_dir):
        raise ValueError('Output must stay outside the game installation')
    if output.exists() or output.is_symlink():
        raise ValueError('Output directory exists; choose a new path')
    report = {'purpose':'private original-game visual references, not distributable mod artwork',
              'objects':[], 'textures':[], 'errors':[]}
    images = []
    seen = set()
    for unit in ('ChinaTankBattleMaster','ChinaTankOverlord'):
        raw,virtual = source.find_object(unit)
        obj, = parse_ini(raw).blocks
        models = []
        for draw in obj.children:
            if draw.kind.lower() != 'draw':
                continue
            for state in draw.children:
                for field in state.find_fields('Model'):
                    model = field.value
                    if re.fullmatch(r'[A-Za-z0-9_]+',model) and model.upper() != 'NONE':
                        models.append(model)
        item = {'object':unit,'source_virtual_path':virtual,'models':list(dict.fromkeys(models))}
        report['objects'].append(item)
        for model in item['models'][:1]:
            model_path = 'Art\\W3D\\'+model+'.w3d'
            try:
                names = texture_names(source.read(model_path))
                item['texture_names'] = names
                for name in names:
                    stem = name.rsplit('.',1)[0]
                    candidates = ['Art\\Textures\\'+stem+'.dds','Art\\Textures\\'+name]
                    virtual_tex = next((path for path in candidates if path.lower() in source.entries),None)
                    if virtual_tex is None or virtual_tex.lower() in seen:
                        continue
                    seen.add(virtual_tex.lower())
                    payload = source.read(virtual_tex)
                    try:
                        w,h,rgb = decode_dds(payload) if payload[:4]==b'DDS ' else decode_tga(payload)
                    except ValueError as exc:
                        report['errors'].append({'texture':virtual_tex,'reason':str(exc)})
                        continue
                    index = len(images)
                    if index >= 6:
                        break
                    filename = f'reference-{index+1}.png'
                    images.append((filename,png(w,h,rgb)))
                    report['textures'].append({'object':unit,'model':model,'source_virtual_path':virtual_tex,
                                               'archive_name':source.entries[virtual_tex.lower()].archive_path.name,
                                               'width':w,'height':h,'preview':filename})
            except (ValueError,KeyError,OSError) as exc:
                report['errors'].append({'model':model,'reason':str(exc)})
    for name,image in images:
        _atomic_write(output/name,image)
    _atomic_write(output/'stock-visual-details.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=PROJECT/'dist/stock-visual-reference')
    args = parser.parse_args()
    try:
        report = inspect(args.game_dir,args.output)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        print('Private reference folder: '+str(args.output.resolve()))
        return 0 if report['textures'] else 1
    except (ValueError,OSError,KeyError) as exc:
        print('ERROR: '+str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
