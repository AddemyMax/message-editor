#!/usr/bin/env python3
"""Read effective Tumbler armor/health and weapon metadata from a private BIG."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

from uwmod.archive import read_big
from uwmod.ini import parse_ini
from uwmod.project import GameSource,_inside

COMBAT_TYPES=('EXPLOSION','CRUSH','ARMOR_PIERCING','SMALL_ARMS','GATTLING',
              'RADIATION','FLAME','LASER','SNIPER','POISON','MELEE','PARTICLE_BEAM',
              'INFANTRY_MISSILE','AURORA_BOMB','LAND_MINE','JET_MISSILES',
              'STEALTHJET_MISSILES','MOLOTOV_COCKTAIL','COMANCHE_VULCAN','MICROWAVE')
SPECIAL_TYPES=('HEALING','UNRESISTABLE','SUBDUAL_UNRESISTABLE','STATUS','KILL_PILOT')
WEAPON_FIELDS={'PrimaryDamage','SecondaryDamage','PrimaryDamageRadius','SecondaryDamageRadius','DamageType',
               'DeathType','AttackRange','MinimumAttackRange','DelayBetweenShots','ClipSize',
               'ClipReloadTime','ShotsPerBarrel','ProjectileObject','RadiusDamageAffects','DamageDealtAtSelfPosition'}


def scalars(block,keys):
    return {key:[f.value for f in block.find_fields(key)] for key in keys if block.find_fields(key)}


def scalar(block,key,default=None):
    fields=block.find_fields(key)
    if not fields:return default
    if len(fields)!=1:raise ValueError('Ambiguous diagnostic scalar '+key)
    return fields[0].value


def armor_values(block):
    default=100.0;overrides={}
    for field in block.find_fields('Armor'):
        kind,value=field.value.split();kind=kind.upper()
        if not value.endswith('%'):raise ValueError('Unsupported armor percentage')
        value=float(value[:-1])
        if not math.isfinite(value) or value<0:raise ValueError('Invalid armor coefficient')
        if kind=='DEFAULT':default=value;overrides.clear()
        else:overrides[kind]=value
    return default,overrides


def weapon_info(doc,ref,armor_sets,health):
    weapon=doc.find_block('Weapon',ref)
    result={'weapon':ref,'fields':scalars(weapon,sorted(WEAPON_FIELDS)),'damage_estimates':[]}
    damage_type=scalar(weapon,'DamageType','EXPLOSION').upper()
    value=scalar(weapon,'PrimaryDamage')
    if value is not None:
        hp_damage=damage_type not in {'HEALING','DEPLOY','SURRENDER','HACK','KILL_PILOT','DISARM','HAZARD_CLEANUP','KILL_GARRISONED','STATUS','SUBDUAL_MISSILE','SUBDUAL_VEHICLE','SUBDUAL_BUILDING','SUBDUAL_UNRESISTABLE'}
        raw=float(value)
        for armor in armor_sets:
            percent=armor['effective_percent'].get(damage_type,armor['default_percent'])
            bypass=damage_type in ('UNRESISTABLE','SUBDUAL_UNRESISTABLE')
            amount=raw if bypass else raw*percent/100
            result['damage_estimates'].append({'conditions':armor['conditions'],'armor':armor['armor'],
                'damage_type':damage_type,'raw_primary_damage':raw,'armor_bypassed':bypass,
                'affects_hp':hp_damage,'estimated_primary_hp_damage':amount if hp_damage else None,
                'estimated_hits_to_deplete_health':math.ceil(health/amount) if hp_damage and amount>0 else None,
                'limits':'Base primary damage only; excludes upgrades, veterancy, damage scalars, splash overlap, multiple barrels/attackers and crew/status mechanics.'})
    return result


def diagnose(game_dir,archive_path):
    archive=read_big(archive_path);names={e.name.lower():e.name for e in archive.entries}
    def read(key):return archive.read(names[key.lower()])
    path='Data\\INI\\Object\\AmericaVehicleUWTumbler.ini'
    body=parse_ini(read(path)).find_block('Object','AmericaVehicleUWTumbler')
    bodies=[c for c in body.children if c.kind.lower()=='body']
    if len(bodies)!=1:raise ValueError('Tumbler requires one Body')
    health=float(scalar(bodies[0],'MaxHealth'))
    armor_doc=parse_ini(read('Data\\INI\\Armor.ini'));weapon_doc=parse_ini(read('Data\\INI\\Weapon.ini'))
    armors=[]
    for state in (c for c in body.children if c.kind.lower()=='armorset'):
        name=scalar(state,'Armor');definition=armor_doc.find_block('Armor',name)
        default,values=armor_values(definition)
        armors.append({'conditions':scalar(state,'Conditions','NONE'),'armor':name,'default_percent':default,
                       'effective_percent':{k:values.get(k,default) for k in sorted(set(COMBAT_TYPES+SPECIAL_TYPES)|values.keys())}})
    modifiers=[{'module':c.value,'fields':scalars(c,('TriggeredBy','AddToHealth','ArmorSetFlag','DamageScalar','Multiplier','HealthMultiplier','MaxHealth','InitialHealth'))}
               for c in body.children if c.kind.lower()=='behavior' and any(k in c.value.lower() for k in ('armor','health','damag','battleplan'))]
    own_refs=sorted({f.value.split()[-1] for state in body.children if state.kind.lower()=='weaponset'
                     for f in state.find_fields('Weapon') if f.value.split()[-1].upper()!='NONE'})
    if any(b.name.lower()=='uwtumblerrearrocket' for b in weapon_doc.blocks):
        own_refs.append('UWTumblerRearRocket')
    source=GameSource(game_dir);attackers=[]
    for object_id in ('AmericaVehicleHumvee','ChinaTankGattling','ChinaTankBattleMaster','AmericaTankCrusader'):
        try:
            raw,_=source.find_object(object_id);obj,=parse_ini(raw).blocks
            refs=sorted({f.value.split()[-1] for state in obj.children if state.kind.lower()=='weaponset'
                         for f in state.find_fields('Weapon') if f.value.split()[-1].upper()!='NONE'})
            attackers.append({'object':object_id,'weapons':[weapon_info(weapon_doc,ref,armors,health) for ref in refs]})
        except ValueError as exc:
            attackers.append({'object':object_id,'unavailable':str(exc)})
    manifest_path=archive_path.with_suffix('.manifest.json');manifest={}
    if manifest_path.is_file():manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    unit=next((u for u in manifest.get('units',[]) if u.get('id')=='AmericaVehicleUWTumbler'),{})
    checksum=hashlib.sha256(archive_path.read_bytes()).hexdigest()
    return {'tool_version':'1.0','purpose':'Effective armor and weapon metadata only; no game art or full INI exported',
            'archive_file':archive_path.name,'archive_sha256':checksum,'build_version':manifest.get('version'),
            'matches_build_checksum':checksum==manifest.get('archive_sha256') if manifest else None,
            'native_loaded_archive_verified':False,
            'vehicle':{'id':body.name,'display_label':scalar(body,'DisplayName'),'body_type':bodies[0].value.split()[0],
                       'body':scalars(bodies[0],('MaxHealth','InitialHealth','SubdualDamageCap','SubdualDamageHealRate','SubdualDamageHealAmount')),
                       'armor_sets':armors,'invalid_damage_types':sorted({kind for a in armors for kind in a['effective_percent'] if kind not in COMBAT_TYPES+SPECIAL_TYPES+('FALLING','TOPPLING','DEPLOY','SURRENDER','HACK','PENALTY','DISARM','HAZARD_CLEANUP','KILL_GARRISONED','WATER','SUBDUAL_MISSILE','SUBDUAL_VEHICLE','SUBDUAL_BUILDING')}),'modifier_modules':modifiers,'build_armor_mapping':unit.get('armor'),
                       'build_armor_policy':(unit.get('rockets') or {}).get('armor_policy'),
                       'own_weapons':[weapon_info(weapon_doc,ref,armors,health) for ref in own_refs]},
            'test_attackers':attackers,
            'next_check':'Confirm Launch-Mod.ps1 used this exact archive; test a newly produced vehicle in a new Skirmish, not an existing save.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-dir',type=Path,required=True)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        target=args.report.resolve()
        from uwmod.stock_art import shared_roots
        if any(_inside(target,p) for p in [args.game_dir.resolve()]+shared_roots(args.game_dir.resolve())):
            raise ValueError('Report must stay outside all game installations')
        if target.exists() or target.is_symlink():raise ValueError('Report already exists; choose a new --report')
        result=diagnose(args.game_dir.resolve(),args.archive.resolve())
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('x',encoding='utf-8') as handle:
            json.dump(result,handle,ensure_ascii=False,indent=2);handle.write('\n')
        print('Diagnostic report: '+str(target))
        print('Game files and mod archive unchanged.')
        return 0
    except (ValueError,OSError,KeyError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
