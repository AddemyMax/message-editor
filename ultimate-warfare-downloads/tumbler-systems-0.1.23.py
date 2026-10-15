"""Private additive Tumbler minigun, innate stealth and manual smoke weapon."""
from .ini import parse_ini, patch_command_set


def install(source, spec, project, clone, output, files):
    from .project import _append, _rename, _fields, _edit, _scalar, _newline, BuildError
    body, = parse_ini(clone).blocks
    weapon_sets = [c for c in body.children if c.kind.lower() == 'weaponset']
    occupied = {f.value.split()[0].upper() for ws in weapon_sets for f in ws.find_fields('Weapon')
                if f.value.split()[-1].upper() != 'NONE'}
    free = [slot for slot in ('SECONDARY', 'TERTIARY') if slot not in occupied]
    if not free:
        layout = '; '.join(('/'.join(f.value for f in ws.find_fields('Conditions')) or 'NONE') + ': ' + ', '.join(f.value for f in ws.find_fields('Weapon')) for ws in weapon_sets)
        raise BuildError('Reference tank occupies all three weapon slots across its weapon sets; original weapons were preserved. Layout: ' + layout)
    minigun_slot = free[0]
    # Clone the local ordinary Humvee's normal machine gun, leaving it untouched.
    donor_raw, _ = source.find_object('AmericaVehicleHumvee')
    donor, = parse_ini(donor_raw).blocks
    candidates = [c for c in donor.children if c.kind.lower() == 'weaponset'
                  and (not c.find_fields('Conditions') or c.find_fields('Conditions')[0].value.upper() == 'NONE')]
    primary = [f.value.split()[1] for c in candidates for f in c.find_fields('Weapon')
               if f.value.split()[0].upper() == 'PRIMARY']
    if len(set(primary)) != 1:
        raise BuildError('Ordinary Humvee must have one normal primary weapon for the roof minigun')
    gun_name = 'UWTumblerMinigun'
    gun = _rename(parse_ini(output['Weapon']).extract_block('Weapon', primary[0]), 'Weapon', gun_name)
    output['Weapon'] = _append(output['Weapon'], [gun])
    systems = parse_ini((project / 'content/effects/tumbler.ini').read_bytes())
    original_ocl = source.read('Data\\INI\\ObjectCreationList.ini')
    ocls = []
    for block in systems.blocks:
        raw = systems.source(block)
        if block.kind.lower() == 'weapon' and block.name.lower() == 'uwtumblersmokelauncher':
            # Its cooldown belongs to SpecialPower, not to a disposable weapon.
            raw = _fields(raw, parse_ini(raw).blocks[0], {'ClipSize': '0', 'ClipReloadTime': '0'})
        if block.kind.lower() == 'object':
            if block.name.lower() in source.object_names:
                raise BuildError('New support object already exists: ' + block.name)
            path = f'Data\\INI\\Object\\{block.name}.ini'
            if path.lower() in source.entries:
                raise BuildError('New support object path already exists: ' + path)
            files[path] = raw
        elif block.kind.lower() == 'objectcreationlist':
            ocls.append(raw)
        elif block.kind.lower() in ('weapon', 'particlesystem'):
            target = 'Weapon' if block.kind.lower() == 'weapon' else 'ParticleSystem'
            output[target] = _append(output[target], [raw])
        else:
            raise BuildError('Unsupported Tumbler system block: ' + block.kind)
    # Smoke is a separate per-vehicle power. FireWeaponNugget allocates a
    # temporary weapon, so it never replaces any of the tank's three slots.
    ocls.append(b'''ObjectCreationList OCL_UWTumblerLaunchSmoke
  FireWeapon
    Weapon = UWTumblerSmokeLauncher
  End
End
''')
    files['Data\\INI\\ObjectCreationList.ini'] = _append(original_ocl, ocls)
    original_powers = source.read('Data\\INI\\SpecialPower.ini')
    files['Data\\INI\\SpecialPower.ini'] = _append(original_powers, [b'''SpecialPower SpecialAbilityUWTumblerSmoke
  Enum = SPECIAL_AMBUSH
  ReloadTime = 30000
  PublicTimer = No
  SharedSyncedTimer = No
  ShortcutPower = No
  ViewObjectRange = 0
  ViewObjectDuration = 0
End
'''])
    body, = parse_ini(clone).blocks
    edits = []
    for ws in (c for c in body.children if c.kind.lower() == 'weaponset'):
        # Occupied source slots, their preferences and auto-choice rules stay
        # intact. Only the selected free slot is populated on the NEW object.
        additions = (f'    Weapon = {minigun_slot} UWTumblerMinigun\n'
                     f'    AutoChooseSources = {minigun_slot} FROM_PLAYER FROM_SCRIPT FROM_AI\n'
                     f'    PreferredAgainst = {minigun_slot} INFANTRY\n').encode('ascii').replace(b'\n', _newline(clone))
        for key in ('Weapon', 'AutoChooseSources', 'PreferredAgainst'):
            for field in ws.find_fields(key):
                if field.value.split()[0].upper() == minigun_slot:
                    edits.append((field.start, field.end, b''))
        edits.append((ws.end_start, ws.end_start, additions))
    clone = _edit(clone, edits)
    body, = parse_ini(clone).blocks
    ai = next(c for c in body.children if c.kind.lower() == 'behavior' and 'aiupdate' in c.value.split()[0].lower())
    turret = f'''    Turret
      TurretTurnRate = 180
      TurretPitchRate = 120
      AllowsPitch = Yes
      ControlledWeaponSlots = {minigun_slot}
    End
'''.encode('ascii').replace(b'\n', _newline(clone))
    clone = _edit(clone, [(ai.end_start, ai.end_start, turret)])
    body, = parse_ini(clone).blocks
    # Adapt Draw bindings after the common reference-vehicle compiler so the
    # same one-file hotfix also applies to the already unpacked 0.1.21 kit.
    draw = next(c for c in body.children if c.kind.lower() == 'draw')
    state = next(c for c in draw.children if c.kind.lower() == 'defaultconditionstate')
    bindings = []
    for slot in ('PRIMARY', 'SECONDARY', 'TERTIARY'):
        if slot in occupied or slot == minigun_slot:
            bone = 'MG_MUZZLE' if slot == minigun_slot else 'MUZZLE'
            bindings += [f'      WeaponFireFXBone = {slot} {bone}\n', f'      WeaponLaunchBone = {slot} {bone}\n']
    edits = [(f.start, f.end, b'') for f in state.fields if f.key.lower() in ('weaponfirefxbone', 'weaponlaunchbone')]
    edits.append((state.end_start, state.end_start, ''.join(bindings).encode('ascii').replace(b'\n', _newline(clone))))
    clone = _edit(clone, edits)
    body, = parse_ini(clone).blocks
    modules = b'''  Behavior = OCLSpecialPower UWTumblerSmokePower
    SpecialPowerTemplate = SpecialAbilityUWTumblerSmoke
    OCL = OCL_UWTumblerLaunchSmoke
    CreateLocation = USE_OWNER_OBJECT
    StartsPaused = No
  End
  Behavior = StealthUpdate UWTumblerStealth
    StealthDelay = 3000
    StealthForbiddenConditions = FIRING_PRIMARY FIRING_SECONDARY FIRING_TERTIARY TAKING_DAMAGE
    FriendlyOpacityMin = 35%
    FriendlyOpacityMax = 60%
    PulseFrequency = 1000
    InnateStealth = Yes
  End
'''.replace(b'\n', _newline(clone))
    if any(c.kind.lower() == 'behavior' and c.value.split()[0].lower() == 'stealthupdate' for c in body.children):
        raise BuildError('Reference tank already has a stealth module')
    clone = _edit(clone, [(body.end_start, body.end_start, modules)])
    # The independent special-power timer is local to each vehicle.
    button = b'''CommandButton Command_UWTumblerSmoke
  Command = SPECIAL_POWER
  SpecialPower = SpecialAbilityUWTumblerSmoke
  Options = NEED_TARGET_POS CONTEXTMODE_COMMAND
  TextLabel = CONTROLBAR:UWTumblerSmoke
  ButtonImage = UWTumblerSmokeCameo
  ButtonBorderType = ACTION
  DescriptLabel = CONTROLBAR:TooltipUWTumblerSmoke
  CursorName = Attack
  InvalidCursorName = GenericInvalid
End
'''
    output['CommandButton'] = _append(output['CommandButton'], [button])
    patch = patch_command_set(output['CommandSet'], spec['command_set'], 'Command_UWTumblerSmoke')
    output['CommandSet'] = patch.data
    image_path = 'Data\\INI\\MappedImages\\HandCreated\\UWTumblerSmoke.ini'
    if image_path.lower() in source.entries:
        raise BuildError('New smoke mapped-image file already exists')
    for key in source.entries:
        if key.startswith('data\\ini\\mappedimages\\') and key.endswith('.ini'):
            if any(b.kind.lower() == 'mappedimage' and b.name.lower() == 'uwtumblersmokecameo'
                   for b in parse_ini(source.read(key)).blocks):
                raise BuildError('New smoke image name already exists')
    files[image_path] = b'''MappedImage UWTumblerSmokeCameo
  Texture = uwsmkbtn.tga
  TextureWidth = 128
  TextureHeight = 128
  Coords = Left:0 Top:0 Right:128 Bottom:128
  Status = NONE
End
'''
    return clone, {'minigun_source': primary[0], 'minigun_slot': minigun_slot, 'smoke_uses_weapon_slot': False, 'smoke_button_slot': patch.slot,
                   'stealth_delay_ms': 3000, 'smoke_radius': 60, 'smoke_lifetime_ms': 8000,
                   'smoke_reload_ms': 30000, 'smoke_effect': 'enemy NO_ATTACK status, 1200 ms renewed every 500 ms; armor STATUS resistance applies'}


def validate(documents, objects, archive, names):
    """Resolve the complete authored smoke chain in a built BIG, offline."""
    from .project import BuildError, _scalar
    weapons = documents['Weapon']
    launcher = [b for b in weapons.blocks if b.name.lower() == 'uwtumblersmokelauncher']
    if not launcher:
        return  # Older prototypes do not contain the support systems.
    launcher, = launcher
    projectile = _scalar(launcher, 'ProjectileObject').lower()
    if projectile not in objects:
        raise BuildError('Smoke projectile object is absent')
    ocl_path = 'data\\ini\\objectcreationlist.ini'
    if ocl_path not in names:
        raise BuildError('Smoke detonation lacks its full ObjectCreationList overlay')
    ocls = parse_ini(archive.read(names[ocl_path]))
    ocl = ocls.find_block('ObjectCreationList', _scalar(launcher, 'ProjectileDetonationOCL'))
    clouds = [f.value.lower() for c in ocl.children for f in c.find_fields('ObjectNames')]
    if len(clouds) != 1 or clouds[0] not in objects:
        raise BuildError('Smoke OCL references a missing cloud object')
    cloud = objects[clouds[0]]
    pulses = [c for c in cloud.children if c.kind.lower() == 'behavior' and c.value.split()[0].lower() == 'fireweaponupdate']
    if len(pulses) != 1:
        raise BuildError('Smoke cloud requires a periodic effect weapon')
    weapons.find_block('Weapon', _scalar(pulses[0], 'Weapon'))
    particles = [f.value.split()[-1] for c in cloud.children if c.kind.lower() == 'draw'
                 for state in c.children for f in state.find_fields('ParticleSysBone')]
    if not particles:
        raise BuildError('Smoke cloud has no particle effect')
    for particle in particles:
        documents['ParticleSystem'].find_block('ParticleSystem', particle)
    button = documents['CommandButton'].find_block('CommandButton', 'Command_UWTumblerSmoke')
    if _scalar(button, 'Command').upper() != 'SPECIAL_POWER':
        raise BuildError('Smoke button must use its independent special power')
    power_path = 'data\\ini\\specialpower.ini'
    if power_path not in names:
        raise BuildError('Smoke ability lacks its full SpecialPower overlay')
    power_name = _scalar(button, 'SpecialPower')
    parse_ini(archive.read(names[power_path])).find_block('SpecialPower', power_name)
    vehicle = objects.get('americavehicleuwtumbler')
    if vehicle is None:
        raise BuildError('Smoke systems lack their vehicle')
    modules = [c for c in vehicle.children if c.kind.lower() == 'behavior' and c.value.split()[0].lower() == 'oclspecialpower'
               and any(f.value.lower() == power_name.lower() for f in c.find_fields('SpecialPowerTemplate'))]
    if len(modules) != 1:
        raise BuildError('Smoke ability lacks its vehicle power module')
    launch = ocls.find_block('ObjectCreationList', _scalar(modules[0], 'OCL'))
    fire = [c for c in launch.children if c.kind.lower() == 'fireweapon']
    if len(fire) != 1 or _scalar(fire[0], 'Weapon').lower() != launcher.name.lower():
        raise BuildError('Smoke power must launch its temporary grenade weapon')
    command_set = documents['CommandSet'].find_block('CommandSet', _scalar(vehicle, 'CommandSet'))
    if not any(f.value.lower() == button.name.lower() and 1 <= int(f.key) <= 12 for f in command_set.fields):
        raise BuildError('Smoke ability has no visible unit command slot')
    for path in ('art\\w3d\\uwsmkgren.w3d', 'art\\textures\\uwsmoke.tga', 'art\\textures\\uwsmkbtn.tga'):
        if path not in names:
            raise BuildError('Smoke asset is absent: ' + path)
