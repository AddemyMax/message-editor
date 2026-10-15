"""Lossless structural parsing of stock SAGE INI blocks.

This is not ConfigParser: SAGE uses nested End blocks and context-dependent
keywords. In particular ConditionState.Turret and AliasConditionState are
scalars, whereas AIUpdate's Turret and Draw.ConditionState are blocks.
The parser preserves original bytes, comments, encoding and line endings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable


class IniError(ValueError):
    """Malformed, ambiguous, or unsupported SAGE INI input."""


_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z", re.ASCII)
# EA field tables include HealthRegen%PerSec, HoleHealthRegen%PerSecond and
# RepairWhenBelowHealth%. Percent belongs to the keyword, not only its value.
_LINE = re.compile(rb"([A-Za-z0-9_%]+)(?:[ \t]+|[ \t]*=[ \t]*|$)(.*)")
_TOP_TYPES = frozenset(word.lower() for word in """
AIData Animation Armor AudioEvent AudioSettings Bridge Campaign ChallengeGenerals
CommandButton CommandMap CommandSet ControlBarScheme ControlBarResizer CrateData
Credits WindowTransition DamageFX DialogEvent DrawGroupInfo EvaEvent FXList
GameData InGameUI Locomotor Language MapCache MapData MappedImage MiscAudio Mouse
MouseCursor MultiplayerColor MultiplayerStartingMoneyChoice OnlineChatColors
MultiplayerSettings MusicTrack Object ObjectCreationList ObjectReskin ParticleSystem
PlayerTemplate Road Science Rank SpecialPower ShellMenuScheme Terrain Upgrade Video
WaterSet WaterTransparency Weather Weapon WebpageURL HeaderTemplate StaticGameLOD
DynamicGameLOD LODPreset BenchProfile ReallyLowMHz ScriptAction ScriptCondition
""".split())
_OBJECT_BLOCKS = frozenset(word.lower() for word in """
Draw Body Behavior ClientUpdate WeaponSet ArmorSet Prerequisites UnitSpecificSounds
UnitSpecificFX AddModule ReplaceModule InheritableModule
""".split())
_STATE_BLOCKS = frozenset(word.lower() for word in """
DefaultConditionState ConditionState TransitionState
""".split())
_FX_BLOCKS = frozenset(word.lower() for word in """
Sound RayEffect Tracer LightPulse ViewShake TerrainScorch ParticleSystem
FXListAtBonePos
""".split())
_OCL_BLOCKS = frozenset(word.lower() for word in """
CreateObject CreateDebris ApplyRandomForce DeliverPayload FireWeapon Attack
""".split())
_BEHAVIOR_DECALS = frozenset(word.lower() for word in """
AttackAreaDecal TargetingReticleDecal DeliveryDecal GridDecalTemplate
""".split())


@dataclass(frozen=True)
class IniField:
    key: str
    value: str
    start: int
    end: int
    line: int


@dataclass(frozen=True)
class IniBlock:
    kind: str
    name: str
    value: str
    start: int
    header_end: int
    end_start: int
    end: int
    start_line: int
    end_line: int
    children: tuple[IniBlock, ...]
    fields: tuple[IniField, ...]

    def find_fields(self, key: str) -> tuple[IniField, ...]:
        return tuple(item for item in self.fields if item.key.lower() == key.lower())


@dataclass(frozen=True)
class IniDocument:
    data: bytes
    blocks: tuple[IniBlock, ...]

    def source(self, block: IniBlock) -> bytes:
        return self.data[block.start:block.end]

    def find_block(self, kind: str, name: str) -> IniBlock:
        matches = [block for block in self.blocks
                   if block.kind.lower() == kind.lower() and block.name.lower() == name.lower()]
        if len(matches) != 1:
            raise IniError(f"Expected one {kind} {name}; found {len(matches)}")
        return matches[0]

    def extract_block(self, kind: str, name: str) -> bytes:
        return self.source(self.find_block(kind, name))


@dataclass
class _OpenBlock:
    kind: str
    value: str
    start: int
    header_end: int
    start_line: int
    children: list[IniBlock] = field(default_factory=list)
    fields: list[IniField] = field(default_factory=list)


def _is_nested_block(parent: _OpenBlock, key: str) -> bool:
    kind = parent.kind.lower()
    key = key.lower()
    if kind in ("object", "objectreskin", "addmodule", "replacemodule", "inheritablemodule"):
        return key in _OBJECT_BLOCKS
    if kind == "draw":
        return key in _STATE_BLOCKS
    if kind == "behavior":
        # EA RadiusDecalTemplate::parseRadiusDecalTemplate consumes its own End
        # in Spectre, payload, neutron-missile and shroud-update modules.
        return key in ("turret", "altturret") or key in _BEHAVIOR_DECALS
    if kind == "fxlist":
        return key in _FX_BLOCKS
    if kind == "objectcreationlist":
        return key in _OCL_BLOCKS
    if kind in ("attack", "deliverpayload"):
        # DeliverPayloadNugget registers DeliverPayloadData's field table,
        # including a RadiusDecalTemplate that consumes a nested End.
        # Its FireWeapon field remains a scalar, unlike the OCL nugget.
        return key == "deliverydecal"
    return False


def parse_ini(data: bytes) -> IniDocument:
    """Parse immutable bytes and expose absolute byte spans of every block/field.

    Semicolon comments follow the actual engine, including inside quotations.
    Unsupported directives and unknown top-level blocks fail closed. Arbitrary
    8-bit localized comments pass through without decoding or normalization.
    """
    if not isinstance(data, bytes):
        raise TypeError("INI input must be bytes")
    if b"\x00" in data or data.startswith((b"\xff\xfe", b"\xfe\xff")):
        raise IniError("SAGE INI must be byte text, not NUL/UTF-16 input")
    if len(data) > 128 * 1024 * 1024:
        raise IniError("INI input is excessively large")
    blocks = []
    stack: list[_OpenBlock] = []
    offset = 0
    for line_number, line in enumerate(data.splitlines(keepends=True), start=1):
        line_start = offset
        offset += len(line)
        content = line.rstrip(b"\r\n").split(b";", 1)[0].strip(b" \t")
        if line_number == 1 and content.startswith(b"\xef\xbb\xbf"):
            content = content[3:]
        if not content:
            continue
        match = _LINE.fullmatch(content)
        if match is None:
            raise IniError(f"Malformed or unsupported INI syntax on line {line_number}")
        key = match[1].decode("ascii")
        value = match[2].strip(b" \t")
        # The first regex separator may consume spaces ahead of an equals sign.
        if value.startswith(b"="):
            value = value[1:].strip(b" \t")
        text_value = value.decode("latin-1")
        if key.lower() == "end":
            # INI::initFromINIMulti checks only the first token against END.
            # Native stock files can append annotations such as upgrade names;
            # preserve their bytes, but they do not change the closing scope.
            if not stack:
                raise IniError(f"Unexpected/malformed End on line {line_number}")
            opened = stack.pop()
            block = IniBlock(opened.kind, opened.value.split()[0] if opened.value else "",
                             opened.value, opened.start, opened.header_end, line_start,
                             offset, opened.start_line, line_number,
                             tuple(opened.children), tuple(opened.fields))
            if stack:
                stack[-1].children.append(block)
            else:
                blocks.append(block)
            continue
        if not stack:
            if key.lower() not in _TOP_TYPES:
                raise IniError(f"Unsupported top-level block {key} on line {line_number}")
            if b"=" in content:
                raise IniError(f"Top-level block headers do not use '=' on line {line_number}")
            stack.append(_OpenBlock(key, text_value, line_start, offset, line_number))
        elif _is_nested_block(stack[-1], key):
            stack.append(_OpenBlock(key, text_value, line_start, offset, line_number))
        else:
            if not value:
                raise IniError(f"Empty field or unsupported nested block {key} on line {line_number}")
            stack[-1].fields.append(IniField(key, text_value, line_start, offset, line_number))
    if stack:
        opened = stack[-1]
        raise IniError(f"Unclosed {opened.kind} block beginning on line {opened.start_line}")
    return IniDocument(data, tuple(blocks))


@dataclass(frozen=True)
class CommandSetPatch:
    data: bytes
    slot: int


def patch_command_set(data: bytes, command_set: str, command_button: str,
                      slots: Iterable[int] = range(1, 13)) -> CommandSetPatch:
    """Insert into a free production slot in the entire original local file.

    Slots 13/14 (normally rally/sell) are never modified. Slot 15 is allowed
    only when explicitly requested by a caller providing a matching UI. Every
    preexisting byte and every original command remains intact. No duplicate
    blocks are appended; the complete returned file replaces CommandSet.ini.
    """
    if not _IDENTIFIER.fullmatch(command_set) or not _IDENTIFIER.fullmatch(command_button):
        raise IniError("CommandSet and CommandButton names must be single safe identifiers")
    allowed = tuple(slots)
    if not allowed or len(set(allowed)) != len(allowed) or any(type(slot) is not int or slot not in (*range(1, 13), 15) for slot in allowed):
        raise IniError("Production slots must be unique integers from 1 through 12 or explicit slot 15")
    doc = parse_ini(data)
    block = doc.find_block("CommandSet", command_set)
    if block.value != block.name or not _IDENTIFIER.fullmatch(block.name) or block.children:
        raise IniError("Malformed target CommandSet header or nested content")
    occupied = {}
    for entry in block.fields:
        if not entry.key.isascii() or not entry.key.isdecimal():
            raise IniError(f"Unexpected field in target CommandSet: {entry.key}")
        slot = int(entry.key)
        if not 1 <= slot <= 18 or slot in occupied:
            raise IniError(f"Invalid or duplicate target CommandSet slot: {entry.key}")
        if not _IDENTIFIER.fullmatch(entry.value):
            raise IniError(f"Invalid target CommandSet button in slot {slot}")
        if entry.value.lower() == command_button.lower():
            raise IniError("CommandButton is already present in target CommandSet")
        occupied[slot] = entry
    free = next((slot for slot in sorted(allowed) if slot not in occupied), None)
    if free is None:
        raise IniError("No free production slot 1..12; original commands were preserved")
    header = data[block.start:block.header_end]
    newline = b"\r\n" if header.endswith(b"\r\n") else b"\n" if header.endswith(b"\n") else b"\r" if header.endswith(b"\r") else b"\n"
    indent = b"  "
    if block.fields:
        sample = data[block.fields[0].start:block.fields[0].end]
        indent = sample[:len(sample) - len(sample.lstrip(b" \t"))]
    insertion = indent + str(free).encode("ascii") + b" = " + command_button.encode("ascii") + newline
    patched = data[:block.end_start] + insertion + data[block.end_start:]
    # Validate the returned whole file, including the insertion's structural effect.
    parse_ini(patched).find_block("CommandSet", command_set)
    return CommandSetPatch(patched, free)
