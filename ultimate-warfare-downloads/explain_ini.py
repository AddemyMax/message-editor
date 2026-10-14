#!/usr/bin/env python3
"""Explain one INI parser failure without uploading an original game file.

Unlike the ordinary metadata-only doctor, this opt-in diagnostic includes one
clipped, escaped source line and its bytes. It never executes or changes it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from uwmod.diagnostics import diagnose, _ini_details
from uwmod.ini import IniError, parse_ini
from uwmod.project import PROJECT, MONOLITHIC, GameSource, _atomic_write, _inside


def explain(game_dir: Path, *, project: Path = PROJECT) -> dict:
    report = diagnose(game_dir, project=project)
    report["detail_kind"] = "one_clipped_ini_error_line"
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
                      "hex": clipped.hex(), "original_line_bytes": len(raw), "truncated": len(raw) > 512})
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
