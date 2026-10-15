"""Private stock-model assembly. No stock geometry is shipped in the source kit.

Reads classic W3D rigid/skinned HLODs, selects mesh/bone branches and retains
original vertex/material/UV data. Unsupported assets fail before writing a BIG.
"""
import hashlib
import math
import re
import struct
from pathlib import Path


def unpack(data, depth=0):
    if depth > 24:
        raise ValueError('W3D nesting limit exceeded')
    result = []
    pos = 0
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError('Truncated W3D chunk')
        cid, packed = struct.unpack_from('<II', data, pos)
        size = packed & 0x7fffffff
        end = pos + 8 + size
        if end > len(data):
            raise ValueError('W3D chunk exceeds parent')
        payload = data[pos+8:end]
        result.append((cid, unpack(payload, depth+1) if packed >> 31 else payload))
        pos = end
    return result


def pack(items):
    result = bytearray()
    for cid, payload in items:
        nested = isinstance(payload, list)
        raw = pack(payload) if nested else payload
        result += struct.pack('<II', cid, len(raw) | (0x80000000 if nested else 0)) + raw
    return bytes(result)


def one(items, cid):
    values = [value for key, value in items if key == cid]
    if len(values) != 1:
        raise ValueError(f'W3D requires one chunk 0x{cid:x}; found {len(values)}')
    return values[0]


def name(raw):
    return raw.split(b'\0', 1)[0].decode('ascii')


def encoded(value, size=16):
    raw = value.encode('ascii')
    if not raw or len(raw) >= size or not re.fullmatch(rb'[A-Za-z0-9_.-]+', raw):
        raise ValueError('Invalid W3D identifier: '+value)
    return raw.ljust(size, b'\0')


class Resources:
    def __init__(self, source):
        from .project import GameSource
        from .stock_art import shared_roots
        self.roots = [source.game_dir] + shared_roots(source.game_dir)
        self.sources = [source] + [GameSource(root) for root in self.roots[1:]
                                  if any(p.suffix.lower() == '.big' for p in root.iterdir())]
        self.records = []
        self.cache = {}

    def read(self, virtual):
        from .project import _inside
        if not re.fullmatch(r'Art\\W3D\\[A-Za-z0-9_.-]+\.w3d', virtual, re.I):
            raise ValueError('Unsafe stock model path')
        key = virtual.lower()
        if key in self.cache:
            return self.cache[key]
        found = None
        # Same precedence as the stock texture reader, including shared Generals.
        for root in self.roots:
            path = root
            for part in virtual.split('\\'):
                matches = [p for p in path.iterdir() if p.name.lower() == part.lower()] if path.is_dir() else []
                if len(matches) != 1:
                    break
                path = matches[0]
            else:
                if path.is_file() and not path.is_symlink() and _inside(path, root):
                    if path.stat().st_size > 32*1024*1024:
                        raise ValueError('Stock model exceeds size limit')
                    found = (path.read_bytes(), root, 'loose')
            if found:
                break
        if not found:
            for source in self.sources:
                if key in source.entries:
                    found = (source.read(virtual), source.game_dir, 'archive')
                    break
        if not found:
            raise ValueError('Required stock model unavailable in Zero Hour or nearby Generals: '+virtual)
        raw, root, kind = found
        self.records.append({'virtual_path': virtual, 'root': str(root), 'kind': kind,
                             'sha256': hashlib.sha256(raw).hexdigest()})
        self.cache[key] = raw
        return raw


def verify_dependencies(source, records):
    resources = Resources(source)
    for record in records:
        resources.read(record['virtual_path'])
    if resources.records != records:
        raise ValueError('Original stock models changed or are masked since build; rebuild')


def load_model(resources, model):
    top = unpack(resources.read('Art\\W3D\\'+model+'.w3d'))
    hlod = one(top, 0x700)
    header = one(hlod, 0x701)
    if len(header) != 40:
        raise ValueError('Unsupported HLOD header')
    hierarchy_name = name(header[24:40])
    trees = [p for cid, p in top if cid == 0x100]
    if not trees:
        extra = unpack(resources.read('Art\\W3D\\'+hierarchy_name+'.w3d'))
        trees = [p for cid, p in extra if cid == 0x100]
    if len(trees) != 1:
        raise ValueError('Stock model requires one internal or external hierarchy: '+model)
    tree = trees[0]
    tree_header = one(tree, 0x101)
    if len(tree_header) != 36 or name(tree_header[4:20]).lower() != hierarchy_name.lower():
        raise ValueError('Stock model hierarchy name mismatch')
    raw = one(tree, 0x102)
    count = struct.unpack_from('<I', tree_header, 20)[0]
    if len(raw) != count*60 or not 0 < count <= 512:
        raise ValueError('Invalid stock pivot count')
    pivots = list(struct.iter_unpack('<16sI10f', raw))
    for i, p in enumerate(pivots):
        if (p[1] != 0xffffffff if i == 0 else p[1] >= i) or not all(math.isfinite(v) for v in p[2:]):
            raise ValueError('Invalid stock hierarchy parent/transform')
    lods = [p for cid, p in hlod if cid == 0x702]
    if not lods:
        raise ValueError('Stock HLOD has no LOD array')
    bindings = []
    meshes = [p for cid, p in top if cid == 0]
    for cid, payload in lods[0]:
        if cid != 0x704:
            continue
        if len(payload) != 36:
            raise ValueError('Invalid stock HLOD binding')
        bone, mesh_name = struct.unpack('<I32s', payload)
        mesh_name = name(mesh_name)
        if bone >= count:
            raise ValueError('HLOD bone out of range')
        def lookup():
            return [m for m in meshes if (name(one(m, 0x1f)[24:40])+'.'+name(one(m, 0x1f)[8:24])).lower() == mesh_name.lower()]
        matched = lookup()
        if not matched:
            namespace = mesh_name.split('.')[0]
            more = unpack(resources.read('Art\\W3D\\'+namespace+'.w3d'))
            meshes += [p for key, p in more if key == 0]
            matched = lookup()
        if len(matched) != 1:
            raise ValueError('Cannot resolve stock mesh: '+mesh_name)
        bindings.append((bone, matched[0]))
    if not bindings:
        raise ValueError('Stock model has no mesh bindings')
    return pivots, bindings


def branch(pivots, bone):
    matches = [i for i, p in enumerate(pivots) if name(p[0]).lower() == bone.lower()]
    if len(matches) != 1:
        raise ValueError('Cannot identify stock turret pivot: '+bone)
    root = matches[0]
    result = {root}
    for i, p in enumerate(pivots):
        if p[1] in result:
            result.add(i)
    return root, result


def chassis_selection(pivots, turret_bone, model):
    """Remove the complete stock weapon assembly, including travel variants.

    NVNukeCn's transport gun is split into sibling branches outside TURRET01.
    Native normal-state ShowSubObject selects TURRETFRONT/TURRETBACK. They
    must be removed as well when retaining only the carrier chassis.
    """
    root, removed = branch(pivots, turret_bone)
    extra_roots = []
    if model.casefold() == 'nvnukecn':
        available = {name(p[0]).casefold() for p in pivots}
        variants = ('TURRETFRONT', 'TURRETBACK')
        if any(value.casefold() in available for value in variants):
            for value in variants:
                _, members = branch(pivots, value)
                removed.update(members)
                extra_roots.append(value)
    return root, removed, extra_roots


def world_positions(pivots):
    # Quaternion transforms, including rotated chassis deployment pivots.
    positions, rotations = [], []
    def rotate(q, v):
        x,y,z,w = q
        tx,ty,tz = 2*(y*v[2]-z*v[1]),2*(z*v[0]-x*v[2]),2*(x*v[1]-y*v[0])
        return (v[0]+w*tx+y*tz-z*ty, v[1]+w*ty+z*tx-x*tz, v[2]+w*tz+x*ty-y*tx)
    def multiply(a,b):
        x,y,z,w=a; X,Y,Z,W=b
        return (w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z)
    for p in pivots:
        parent=p[1]; q=p[8:12]
        if abs(sum(v*v for v in q)-1) > .01:
            raise ValueError('Stock pivot quaternion is not normalized')
        pos=p[2:5]
        if parent != 0xffffffff:
            pos=tuple(a+b for a,b in zip(positions[parent],rotate(rotations[parent],pos)))
            q=multiply(rotations[parent],q)
        positions.append(pos);rotations.append(q)
    return positions


def select_mesh(mesh, bone, selected, remap, model, mesh_name):
    header=one(mesh,0x1f)
    if len(header)!=116:
        raise ValueError('Unsupported stock mesh header')
    nt,nv=struct.unpack_from('<II',header,40)
    influences=[p for cid,p in mesh if cid==0xe]
    triangles=one(mesh,0x20)
    if not nt or not nv or len(triangles)!=nt*32 or len(one(mesh,2))!=nv*12:
        raise ValueError('Invalid stock geometry count')
    for i in range(nt):
        if max(struct.unpack_from('<III',triangles,i*32))>=nv:
            raise ValueError('Invalid stock vertex index')
    if influences:
        raw,=influences
        if len(raw)!=nv*8:
            raise ValueError('Unsupported skin influences')
        bones=[struct.unpack_from('<H',raw,i*8)[0] for i in range(nv)]
        if any(b not in remap for b in bones):
            raise ValueError('Skin bone out of range')
        keep=[]
        for i in range(nt):
            indices=struct.unpack_from('<III',triangles,i*32)
            if max(indices)>=nv:
                raise ValueError('Invalid stock vertex index')
            sides={bones[v] in selected for v in indices}
            if len(sides)>1:
                raise ValueError('Cannot separate a stock triangle spanning chassis and turret')
            if True in sides:
                keep.append(i)
        skin=b''.join(struct.pack('<H',remap[bones[i]])+raw[i*8+2:i*8+8] for i in range(nv))
    else:
        keep=list(range(nt)) if bone in selected else []
        skin=None
    if not keep:
        return None
    # Preserve UVs/materials and vertex channels. Filter per-face channels and
    # discard the optional acceleration tree whose polygon indices changed.
    def edit(items):
        result=[]
        for cid,payload in items:
            if cid==0x90:
                continue
            if isinstance(payload,list):
                payload=edit(payload)
            elif cid==0x1f:
                payload=payload[:8]+encoded(mesh_name)+encoded(model)+struct.pack('<I',len(keep))+payload[44:]
            elif cid==0x20:
                payload=b''.join(payload[i*32:i*32+32] for i in keep)
            elif cid==0xe:
                payload=skin
            elif cid in (0x3a,0x49,0x4b):
                stride=12 if cid==0x4b else 4
                if len(payload)==nt*stride:
                    payload=b''.join(payload[i*stride:i*stride+stride] for i in keep)
                elif len(payload)!=stride or cid==0x4b:
                    raise ValueError('Unsupported per-face material channel')
            result.append((cid,payload))
        return result
    return edit(mesh)


def assemble(resources, chassis_model, turret_model, chassis_bone, turret_bone, model):
    cp,cm=load_model(resources,chassis_model)
    tp,tm=load_model(resources,turret_model)
    cr,removed,extra_roots=chassis_selection(cp,chassis_bone,chassis_model)
    tr,selected=branch(tp,turret_bone)
    target=world_positions(cp)[cr];old=world_positions(tp)[tr]
    delta=tuple(a-b for a,b in zip(target,old))
    pivots=[(encoded('ROOTTRANSFORM'),0xffffffff,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.)]
    c_map={i:i+1 for i in range(len(cp))}
    t_map={i:i+1+len(cp) for i in range(len(tp))}
    for i,p in enumerate(cp):
        pivots.append((encoded(f'C{i:03d}'),0 if p[1]==0xffffffff else c_map[p[1]],*p[2:]))
    used={name(p[0]).lower() for p in pivots}
    for i,p in enumerate(tp):
        new_name=name(p[0]) if i in selected else f'O{i:03d}'
        if new_name.lower() in used:
            raise ValueError('Duplicate composite bone name')
        used.add(new_name.lower())
        values=list(p[2:])
        if p[1]==0xffffffff:
            values[:3]=[a+b for a,b in zip(values[:3],delta)]
        pivots.append((encoded(new_name),0 if p[1]==0xffffffff else t_map[p[1]],*values))
    meshes=[];bindings=[];counts=[];mesh_names=set()
    for mesh_list,keep,remap in ((cm,set(range(len(cp)))-removed,c_map),(tm,selected,t_map)):
        before=len(meshes)
        for bone,mesh in mesh_list:
            original_name=name(one(mesh,0x1f)[8:24])
            mn=original_name
            if mn.lower() in mesh_names:
                mn=f'M{len(meshes):03d}'
            revised=select_mesh(mesh,bone,keep,remap,model,mn)
            if revised is not None:
                mesh_names.add(mn.lower())
                meshes.append((0,revised));bindings.append((0x704,struct.pack('<I32s',remap[bone],encoded(model+'.'+mn,32))))
        counts.append(len(meshes)-before)
    if not all(counts):
        raise ValueError('No separable chassis or turret geometry; stock model layout needs inspection')
    hierarchy=[(0x101,struct.pack('<I16sI3f',0x40001,encoded(model),len(pivots),0,0,0)),
               (0x102,b''.join(struct.pack('<16sI10f',*p) for p in pivots))]
    hlod=[(0x701,struct.pack('<II16s16s',0x10000,1,encoded(model),encoded(model))),
          (0x702,[(0x703,struct.pack('<If',len(bindings),3.402823466e38))]+bindings)]
    result=pack([(0x100,hierarchy)]+meshes+[(0x700,hlod)])
    return result,{'chassis_model':chassis_model,'turret_model':turret_model,'mesh_counts':counts,
                   'removed_chassis_weapon_roots':[chassis_bone]+extra_roots,
                   'turret_mount':list(target),'chassis_bones':{name(p[0]):f'C{i:03d}' for i,p in enumerate(cp)},'pose':'unanimated stock hierarchy bind pose',
                   'textures':'original mesh materials and UVs; resolved by installed game'}
