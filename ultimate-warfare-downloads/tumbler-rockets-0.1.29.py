"""Private triple armor and an independent four-round Scorpion-style rear rack."""
import math

from .ini import parse_ini

# Preserve healing, scripts, crew/control/status mechanics when DEFAULT changes.
SPECIAL_DAMAGE = {'HEALING','UNRESISTABLE','WATER','DEPLOY','SURRENDER','HACK',
                  'KILLPILOT','PENALTY','DISARM','HAZARD_CLEANUP','KILL_GARRISONED',
                  'STATUS','SUBDUAL_UNRESISTABLE'}


def strengthen_armor(clone, output, factor):
    from .project import _rename, _append, _edit, _newline, BuildError
    if type(factor) not in (int,float) or not math.isfinite(factor) or not 1 <= factor <= 100:
        raise BuildError('Invalid Tumbler armor strength multiplier')
    body,=parse_ini(clone).blocks
    mapping={};replacements=[]
    for armor_set in (c for c in body.children if c.kind.lower()=='armorset'):
        for field in armor_set.find_fields('Armor'):
            old=field.value
            if old not in mapping:
                new=f'UWTumblerArmor{len(mapping)}'
                raw=_rename(parse_ini(output['Armor']).extract_block('Armor',old),'Armor',new)
                block,=parse_ini(raw).blocks
                # ArmorTemplate::clear initializes every coefficient to 100%.
                # DEFAULT is optional and resets all preceding overrides;
                # repeated damage kinds use the last value, as in the engine.
                values={};default=100.0;edits=[]
                for entry in block.find_fields('Armor'):
                    tokens=entry.value.split()
                    if len(tokens)!=2 or not tokens[1].endswith('%'):
                        raise BuildError('Unsupported stock armor percentage')
                    kind=tokens[0].upper();value=float(tokens[1][:-1])
                    if not math.isfinite(value) or value<0:
                        raise BuildError('Invalid stock armor coefficient')
                    if kind=='DEFAULT':
                        default=value;values.clear()
                    else:
                        values[kind]=value
                    edits.append((entry.start,entry.end,b''))
                coefficients=[('DEFAULT',default/factor)]
                for kind in sorted(values.keys() | SPECIAL_DAMAGE):
                    value=values.get(kind,default)
                    coefficients.append((kind,value if kind in SPECIAL_DAMAGE else value/factor))
                lines=''.join(f'  Armor = {kind} {value:.10g}%\n' for kind,value in coefficients)
                # Emit DEFAULT first so it cannot erase specific coefficients.
                edits.append((block.header_end,block.header_end,lines.encode('ascii').replace(b'\n',_newline(raw))))
                output['Armor']=_append(output['Armor'],[_edit(raw,edits)])
                mapping[old]=new
            replacements.append((field.start,field.end,f'    Armor = {mapping[old]}\n'.encode('ascii').replace(b'\n',_newline(clone))))
    if not mapping:
        raise BuildError('Tumbler has no armor to strengthen')
    return _edit(clone,replacements),mapping


def install(source,spec,clone,output,files,scale):
    from .project import _scalar,_rename,_fields,_append,_edit,_newline,BuildError
    factor=spec['armor_strength_multiplier']
    clone,armor_map=strengthen_armor(clone,output,factor)
    settings=spec['tumbler_rockets']
    attack_range=settings['attack_range'];reload_ms=settings['reload_ms'];delay=settings['delay_ms']
    for value in (attack_range,reload_ms,delay):
        if type(value) not in (int,float) or not math.isfinite(value) or value<=0:
            raise BuildError('Invalid Tumbler rocket settings')
    # Resolve the installed Scorpion's supplemental projectile weapon through
    # its WeaponSets, rather than assuming a localized or mod-specific weapon ID.
    donor_raw,donor_path=source.find_object('GLATankScorpion')
    donor,=parse_ini(donor_raw).blocks
    weapons=parse_ini(output['Weapon']);candidates=set()
    for ws in (c for c in donor.children if c.kind.lower()=='weaponset'):
        for field in ws.find_fields('Weapon'):
            slot,weapon=field.value.split()
            if slot.upper()=='SECONDARY' and weapon.upper()!='NONE':
                block=weapons.find_block('Weapon',weapon)
                if block.find_fields('ProjectileObject') and _scalar(block,'ProjectileObject').upper()!='NONE':
                    candidates.add(weapon)
    if not candidates:
        raise BuildError('Scorpion has no supplemental SECONDARY missile weapon')
    # Prefer the least-upgraded normal PLAYER_UPGRADE set. Different crate
    # levels may have stronger secondary weapons, but the base rocket is wanted.
    selected=[]
    for ws in (c for c in donor.children if c.kind.lower()=='weaponset'):
        conditions=' '.join(f.value.upper() for f in ws.find_fields('Conditions'))
        if 'CRATE' not in conditions and 'HERO' not in conditions:
            selected += [f.value.split()[1] for f in ws.find_fields('Weapon')
                         if f.value.split()[0].upper()=='SECONDARY' and f.value.split()[1] in candidates]
    if len(set(selected))!=1:
        if len(candidates)!=1:
            raise BuildError('Ambiguous base Scorpion missile weapon')
        selected=list(candidates)
    old=selected[0];weapon=weapons.find_block('Weapon',old)
    projectile=_scalar(weapon,'ProjectileObject');source.find_object(projectile)
    rocket_name='UWTumblerRearRocket'
    raw=_rename(weapons.source(weapon),'Weapon',rocket_name)
    block,=parse_ini(raw).blocks
    raw=_fields(raw,block,{'AttackRange':f'{attack_range:g}','MinimumAttackRange':'0',
                         'ClipSize':'4','AutoReloadsClip':'Yes','ClipReloadTime':f'{reload_ms:g}',
                         'DelayBetweenShots':f'{delay:g}','ShotsPerBarrel':'1',
                         'AntiAirborneVehicle':'No','AntiAirborneInfantry':'No','AntiGround':'Yes'})
    output['Weapon']=_append(output['Weapon'],[raw])
    rack_id='UWTumblerRocketRack';path='Data\\INI\\Object\\'+rack_id+'.ini'
    if rack_id.lower() in source.object_names or path.lower() in source.entries or path in files:
        raise BuildError('New Tumbler rocket rack already exists')
    files[path]=f'''Object {rack_id}
  Side = America
  RadarPriority = NOT_ON_RADAR
  Draw = W3DDependencyModelDraw UWTumblerRocketDraw
    AttachToBoneInContainer = FIREPOINT01
    OkToChangeModelColor = Yes
    ProjectileBoneFeedbackEnabledSlots = PRIMARY
    DefaultConditionState
      Model = UWTBRACK
      Turret = R_TURRET
      WeaponLaunchBone = PRIMARY ROCKET
      WeaponFireFXBone = PRIMARY ROCKET
    End
    ConditionState = RUBBLE
      Model = NONE
    End
  End
  WeaponSet
    Conditions = NONE
    Weapon = PRIMARY {rocket_name}
    AutoChooseSources = PRIMARY FROM_PLAYER FROM_SCRIPT FROM_AI
  End
  Body = ActiveBody UWTumblerRocketBody
    MaxHealth = 1000
    InitialHealth = 1000
  End
  Behavior = AIUpdateInterface UWTumblerRocketAI
    Turret
      TurretTurnRate = 180
      ControlledWeaponSlots = PRIMARY
    End
    AutoAcquireEnemiesWhenIdle = Yes
  End
  Behavior = DestroyDie UWTumblerRocketDestroy
  End
  TransportSlotCount = 1
  KindOf = CAN_ATTACK PORTABLE_STRUCTURE UNATTACKABLE CLICK_THROUGH
  Scale = {scale:g}
  Geometry = SPHERE
  GeometryMajorRadius = 0.5
  GeometryIsSmall = Yes
  Shadow = NONE
End
'''.encode('ascii')
    body,=parse_ini(clone).blocks
    if any(c.kind.lower()=='behavior' and 'contain' in c.value.split()[0].lower() for c in body.children):
        raise BuildError('Tumbler already has a container; rocket payload cannot safely be added')
    contain=f'''  Behavior = OverlordContain UWTumblerRearRackContain
    Slots = 1
    PayloadTemplateName = {rack_id}
    AllowInsideKindOf = PORTABLE_STRUCTURE
    PassengersAllowedToFire = Yes
    PassengersInTurret = No
    DamagePercentToUnits = 0%
    ExperienceSinkForRider = Yes
  End
'''.encode('ascii').replace(b'\n',_newline(clone))
    clone=_edit(clone,[(body.end_start,body.end_start,contain)])
    body,=parse_ini(clone).blocks
    draw=next(c for c in body.children if c.kind.lower()=='draw')
    clone=_edit(clone,[(draw.end_start,draw.end_start,b'    ExtraPublicBone = FIREPOINT01'+_newline(clone))])
    body,=parse_ini(clone).blocks
    stealth=next(c for c in body.children if c.kind.lower()=='behavior' and c.value.split()[0].lower()=='stealthupdate')
    forbidden=_scalar(stealth,'StealthForbiddenConditions')
    clone=_fields(clone,stealth,{'StealthForbiddenConditions':forbidden+' RIDERS_ATTACKING'})
    return clone,{'armor_strength_multiplier':factor,'armor':armor_map,'source_object':'GLATankScorpion',
                  'source_object_file':donor_path,'source_weapon':old,'projectile':projectile,
                  'weapon':rocket_name,'payload':rack_id,'attack_range':attack_range,'salvo':4,
                  'delay_ms':delay,'reload_ms':reload_ms,'uses_vehicle_weapon_slot':False,
                  'targeting':'independent automatic ground-target acquisition; parent movement still uses main-gun range'}


def validate(documents,objects,archive,names):
    """Check independent payload, attachment, ammunition and stealth contracts."""
    import struct
    from .project import _scalar,BuildError
    from assets.validate_w3d import chunks,one
    rack=objects.get('uwtumblerrocketrack')
    rocket=[b for b in documents['Weapon'].blocks if b.name.lower()=='uwtumblerrearrocket']
    if not rack and not rocket:
        return
    vehicle=objects.get('americavehicleuwtumbler')
    if rack is None or vehicle is None or len(rocket)!=1:
        raise BuildError('Rear rockets require their vehicle, rack and weapon')
    weapon=rocket[0]
    if any(_scalar(weapon,k)!=v for k,v in {'ClipSize':'4','AutoReloadsClip':'Yes','ShotsPerBarrel':'1'}.items()):
        raise BuildError('Rear rocket rack must reload a four-round salvo')
    if float(_scalar(weapon,'AttackRange'))<=0 or float(_scalar(weapon,'ClipReloadTime'))<=0:
        raise BuildError('Rear rocket range and reload must be positive')
    contains=[c for c in vehicle.children if c.kind.lower()=='behavior' and c.value.split()[0].lower()=='overlordcontain']
    if len(contains)!=1 or _scalar(contains[0],'PayloadTemplateName').lower()!=rack.name.lower():
        raise BuildError('Rear rocket rack lacks its contained payload')
    if _scalar(contains[0],'PassengersAllowedToFire').upper()!='YES':
        raise BuildError('Rear rocket payload cannot fire')
    stealth=next(c for c in vehicle.children if c.kind.lower()=='behavior' and c.value.split()[0].lower()=='stealthupdate')
    if 'RIDERS_ATTACKING' not in _scalar(stealth,'StealthForbiddenConditions').upper().split():
        raise BuildError('Rear rocket fire must reveal the stealth vehicle')
    draw=next(c for c in rack.children if c.kind.lower()=='draw')
    if draw.value.split()[0].lower()!='w3ddependencymodeldraw' or _scalar(draw,'AttachToBoneInContainer')!='FIREPOINT01':
        raise BuildError('Rear rocket visual and logical attachment must use FIREPOINT01')
    if _scalar(draw,'ProjectileBoneFeedbackEnabledSlots')!='PRIMARY':
        raise BuildError('Rear missiles require independent ammunition visibility')
    state=draw.children[0]
    if _scalar(state,'WeaponLaunchBone')!='PRIMARY ROCKET' or state.find_fields('WeaponHideShowBone'):
        raise BuildError('Rear missile visibility must use numbered launch subobjects')
    ws=next(c for c in rack.children if c.kind.lower()=='weaponset')
    if _scalar(ws,'Weapon')!='PRIMARY UWTumblerRearRocket':
        raise BuildError('Rear rocket payload has the wrong weapon')
    for key,expected in (('art\\w3d\\uwtumbler.w3d',{'FIREPOINT01'}),
                         ('art\\w3d\\uwtbrack.w3d',{'R_TURRET','ROCKET01','ROCKET02','ROCKET03','ROCKET04'})):
        if key not in names:
            raise BuildError('Rear rocket asset missing: '+key)
        top=chunks(archive.read(names[key]));pivots=one(one(top,0x100),0x102)
        bones={p[0].split(b'\0')[0].decode('ascii') for p in struct.iter_unpack('<16sI10f',pivots)}
        if not expected<=bones:
            raise BuildError('Rear rocket asset lacks attachment or launch bones')
        if 'uwtbrack' in key:
            meshes={one(m,0x1f)[8:24].split(b'\0')[0].decode('ascii') for cid,m in top if cid==0}
            if not {'ROCKET01','ROCKET02','ROCKET03','ROCKET04'}<=meshes:
                raise BuildError('Rear rocket mesh names must match ammunition feedback')
