#!/usr/bin/env python3
"""Report private stock part-selection metadata, without exporting model geometry."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import sys

from uwmod.project import GameSource, _inside
from uwmod.archive import read_big
from uwmod.cementaur import normal_draw
from uwmod.ini import parse_ini
from uwmod.kitbash import Resources, load_model, branch, one, name, world_positions, select_mesh


def strings(items, target):
    result=[]
    for cid,payload in items:
        if isinstance(payload,list):
            result.extend(strings(payload,target))
        elif cid==target:
            result.append(name(payload))
    return result


def channel_info(items,target,stride):
    result=[]
    for cid,payload in items:
        if isinstance(payload,list):
            result.extend(channel_info(payload,target,stride))
        elif cid==target:
            result.append({'entries':len(payload)//stride,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()})
    return result


def inspect_vehicle(resources, raw, role):
    draw,state=normal_draw(raw)
    model,=[f.value for f in state.find_fields('Model')]
    turret,=[f.value for f in state.find_fields('Turret')]
    pivots,meshes=load_model(resources,model)
    pivot,selected=branch(pivots,turret)
    keep=set(range(len(pivots))) if role=='assembled' else (selected if role=='turret' else set(range(len(pivots)))-selected)
    worlds=world_positions(pivots)
    def field_info(block):
        return [{'key':f.key,'value':f.value} for f in block.fields
                if f.key.lower() in {'model','animation','animationmode','hidesubobject','showsubobject','turret','turretpitch',
                                     'weaponlaunchbone','weaponfirefxbone','weaponrecoilbone','weaponmuzzleflash'}]
    parts=[]
    for index,(bone,mesh) in enumerate(meshes):
        header=one(mesh,0x1f)
        flags=struct.unpack_from('<I',header,4)[0]
        nt,nv=struct.unpack_from('<II',header,40)
        influences=[p for cid,p in mesh if cid==0xe]
        weights=Counter()
        face_groups=Counter()
        if influences:
            raw_links,=influences
            if len(raw_links)!=nv*8:
                raise ValueError('Invalid vertex influence count')
            links=[struct.unpack_from('<H',raw_links,i*8)[0] for i in range(nv)]
            weights.update(links)
            triangles=one(mesh,0x20)
            for a,b,c,*_ in struct.iter_unpack('<4I4f',triangles):
                face_groups.update([','.join(str(x) for x in sorted({links[a],links[b],links[c]}))])
        try:
            filtered=select_mesh(mesh,bone,keep,{i:i for i in range(len(pivots))},'UWCEMENTAUR',f'M{index:03d}')
            kept=struct.unpack_from('<I',one(filtered,0x1f),40)[0] if filtered else 0
            error=None
        except ValueError as exc:
            kept=None;error=str(exc)
        parts.append({'mesh':name(header[24:40])+'.'+name(header[8:24]),'binding_bone':bone,
                      'binding_name':name(pivots[bone][0]),'flags_hex':hex(flags),'geometry_type_hex':hex(flags&0xff0000),
                      'triangles':nt,'vertices':nv,'selected_triangles':kept,'selection_error':error,
                      'influence_vertices_by_bone':{str(k):v for k,v in sorted(weights.items())},
                      'triangle_bone_groups':dict(sorted(face_groups.items())),
                      'textures':strings(mesh,0x32),'materials':strings(mesh,0x2c),
                      'vertices_sha256':hashlib.sha256(one(mesh,2)).hexdigest(),
                      'mesh_bounds':list(struct.unpack_from('<6f',header,76)),
                      'uv_channels':channel_info(mesh,0x4a,8),
                      'texture_id_channels':channel_info(mesh,0x49,4),
                      'shader_id_channels':channel_info(mesh,0x3a,4)})
    return {'role':role,'model':model,'draw_type':draw.value.split()[0],'turret_bone':turret,
            'normal_state':field_info(state),'states':[{'kind':s.kind,'condition':s.value,'fields':field_info(s)} for s in draw.children],
            'bones':[{'index':i,'name':name(p[0]),'parent':p[1],'world_position':list(worlds[i]),'selected':i in keep}
                     for i,p in enumerate(pivots)],'meshes':parts}


def diagnose(game_dir, archive_path=None):
    source=GameSource(game_dir)
    resources=Resources(source)
    vehicles=[]
    for object_id,role in (('ChinaVehicleNukeLauncher','chassis'),('ChinaTankOverlord','turret')):
        raw,path=source.find_object(object_id)
        data=inspect_vehicle(resources,raw,role)
        data.update(object=object_id,object_virtual_path=path)
        vehicles.append(data)
    assembled=None
    if archive_path is not None:
        archive=read_big(archive_path)
        entries={e.name.lower():e.name for e in archive.entries}
        class ArchiveResources:
            def read(self,virtual):
                return archive.read(entries[virtual.lower()])
        key='data\\ini\\object\\chinatankuwcementaur.ini'
        assembled=inspect_vehicle(ArchiveResources(),archive.read(entries[key]),'assembled')
    return {'tool_version':'1.0','purpose':'Cementaur part-selection metadata; no vertex/UV arrays or model files exported',
            'native_render_tested':False,'vehicles':vehicles,'assembled_model':assembled,
            'model_sources':[{'virtual_path':r['virtual_path'],'kind':r['kind'],'sha256':r['sha256']} for r in resources.records]}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-dir',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--archive',type=Path)
    args=parser.parse_args(argv)
    try:
        source=GameSource(args.game_dir)
        resources=Resources(source)
        path=args.report.resolve()
        if any(_inside(path,root) for root in resources.roots):
            raise ValueError('Diagnostic report must stay outside all game installations')
        if path.exists() or path.is_symlink():
            raise ValueError('Report already exists; choose a new --report path')
        result=diagnose(args.game_dir,args.archive)
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('x',encoding='utf-8') as handle:
            json.dump(result,handle,ensure_ascii=False,indent=2)
            handle.write('\n')
        print('Diagnostic report: '+str(path))
        print('Only part-selection metadata was saved. Game and mod archive unchanged.')
        return 0
    except (ValueError,OSError,KeyError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
