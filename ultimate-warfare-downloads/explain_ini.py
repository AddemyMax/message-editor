#!/usr/bin/env python3
"""Explain one INI parser failure without uploading an original game file.

Unlike the ordinary metadata-only doctor, this opt-in diagnostic includes one
clipped, escaped source line and its bytes. It never executes or changes it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from uwmod.diagnostics import diagnose, _ini_details
from uwmod.ini import IniError, parse_ini
from uwmod.project import PROJECT, MONOLITHIC, GameSource, _atomic_write, _inside, _scalar


def _production_layout(game_dir: Path, project: Path) -> list[dict]:
    """Expose factory/menu identifiers, never whole configuration files."""
    source = GameSource(game_dir)
    catalog = json.loads((project / "content/catalog.json").read_text(encoding="utf-8"))
    menu_path = "Data\\INI\\CommandSet.ini"
    menus = parse_ini(source.read(menu_path))
    result = []
    for relative in catalog["units"]:
        manifest = (project / "content" / relative).resolve()
        if not _inside(manifest, project / "content"):
            raise ValueError("Unit manifest escapes content directory")
        spec = json.loads(manifest.read_text(encoding="utf-8"))
        factory, factory_path = source.find_object(spec["production_object"])
        factory_block, = parse_ini(factory).blocks
        name = _scalar(factory_block, "CommandSet")
        block = menus.find_block("CommandSet", name)
        slots = [{"slot": int(field.key), "command_button": field.value}
                 for field in block.fields if field.key.isascii() and field.key.isdecimal()]
        result.append({"factory_object": spec["production_object"],
                       "factory_source_path": factory_path,
                       "command_set": name, "command_set_archive": source.entries[menu_path.lower()].archive_path.name,
                       "slots": slots,
                       "free_production_slots": [slot for slot in range(1, 13)
                                                 if slot not in {item["slot"] for item in slots}]})
    return result


def _structure_context(raw_lines: list[bytes], line_number: int) -> dict:
    """List nearby keys/module types without copying scalar field values.

    This is a lexical trace, not a guessed repair or alternate INI parser.
    """
    from uwmod.ini import _TOP_TYPES
    records = []
    modules = []
    scope = None
    for number, raw in enumerate(raw_lines[:line_number], start=1):
        content = raw.rstrip(b"\r\n").split(b";", 1)[0].strip(b" \t")
        if not content:
            continue
        match = re.match(rb"([A-Za-z0-9_%]+)(.*)", content)
        if match is None:
            records.append({"line": number, "keyword": "<unrecognized>"})
            continue
        key = match[1].decode("ascii")
        tail = match[2].strip(b" \t")
        assigned = tail.startswith(b"=")
        if assigned:
            tail = tail[1:].strip(b" \t")
        tokens = tail.split()
        if key.lower() in _TOP_TYPES and not assigned and tokens:
            scope = {"line": number, "keyword": key}
            if re.fullmatch(rb"[A-Za-z0-9_]{1,128}", tokens[0]):
                scope["identifier"] = tokens[0].decode("ascii")
            records = []
            modules = []
        if key.lower() in ("behavior", "draw", "body", "clientupdate") and tokens:
            module = {"line": number, "keyword": key}
            if re.fullmatch(rb"[A-Za-z0-9_]{1,128}", tokens[0]):
                module["module_type"] = tokens[0].decode("ascii")
            modules.append(module)
        records.append({"line": number, "keyword": key, "has_equals": assigned,
                        "value_token_count": len(tokens)})
    return {"scope_header": scope, "module_headers": modules[-16:],
            "previous_keywords": records[-60:], "trace_kind": "lexical_metadata_not_repaired_structure"}


def explain(game_dir: Path, *, project: Path = PROJECT) -> dict:
    report = diagnose(game_dir, project=project)
    report["detail_kind"] = "one_clipped_ini_error_line"
    report["detail_tool_version"] = "1.2"
    if any("no free production slot" in check.get("message", "").lower()
           for check in report.get("checks", [])):
        report["detail_kind"] = "factory_command_identifiers"
        report["production_layout"] = _production_layout(game_dir, project)
        report["line_detail_status"] = "Factory slots inspected; no source lines included."
        return report
    details = report.get("ini_error", {})
    line_number = details.get("line")
    if not isinstance(line_number, int) or line_number < 1:
        report["line_detail_status"] = "No source line number is available for this failure."
        return report
    source = GameSource(game_dir)
    virtual = details.get("source_virtual_path")
    if virtual:
        candidates = [virtual]
    else:
        # A monolithic source error may not yet carry explicit provenance.
        # Match its structural line/keyword against independently parsed
        # source files; identify multiple matches as candidates, not certainty.
        candidates = []
        names = [f"Data\\INI\\{name}.ini" for name in MONOLITHIC]
        names += [entry.name for key, entry in sorted(source.entries.items())
                  if key.startswith("data\\ini\\object\\") and key.endswith(".ini")]
        for name in names:
            if name.lower() not in source.entries:
                continue
            try:
                parse_ini(source.read(name))
            except IniError as exc:
                candidate = _ini_details(exc)
                if candidate.get("line") == line_number and candidate.get("keyword") == details.get("keyword"):
                    candidates.append(name)
            if len(candidates) >= 5:
                break
    lines = []
    for name in candidates:
        raw_lines = source.read(name).splitlines(keepends=True)
        if line_number > len(raw_lines):
            continue
        raw = raw_lines[line_number - 1]
        clipped = raw[:512]
        lines.append({"source_virtual_path": name, "archive_name": source.entries[name.lower()].archive_path.name,
                      "line": line_number, "ascii_escaped": clipped.decode("ascii", errors="backslashreplace"),
                      "hex": clipped.hex(), "original_line_bytes": len(raw), "truncated": len(raw) > 512,
                      "structure_before_error": _structure_context(raw_lines, line_number)})
    report["error_line_candidates"] = lines
    report["line_detail_status"] = (
        "Exact source provenance" if virtual and lines else
        "Candidate source lines; provenance is not uniquely established" if lines else
        "No matching original source line found; the error may occur in generated content"
    )
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    try:
        report = explain(args.game_dir)
        data = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        print(data.decode("utf-8"), end="")
        if args.report is not None:
            if _inside(args.report, args.game_dir):
                raise ValueError("Diagnostic report must stay outside the game installation")
            _atomic_write(args.report, data)
            print("Diagnostic report: " + str(args.report.resolve()), file=sys.stderr)
        return 0 if report["status"] == "passed" else 1
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
