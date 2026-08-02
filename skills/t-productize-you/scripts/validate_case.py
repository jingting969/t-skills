#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from case_library import iter_case_paths, parse_case, render_index, validate_record


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate product case files and case index freshness.")
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--cases-dir", type=Path, default=SKILL_DIR / "references" / "cases")
    parser.add_argument("--index", type=Path, default=SKILL_DIR / "references" / "case-index.md")
    args = parser.parse_args()
    paths = [args.path] if args.path else list(iter_case_paths(args.cases_dir))
    failed = False
    records: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for path in paths:
        try:
            record = parse_case(path)
        except (OSError, ValueError) as error:
            print(f"ERROR {path}: {error}")
            failed = True
            continue
        records.append(record)
        for issue in validate_record(record):
            print(f"ERROR {path} [{issue.field}]: {issue.message}")
            failed = True
        identifier = str(record.get("id", ""))
        if identifier in seen_ids:
            print(f"ERROR {path} [id]: duplicate id {identifier}")
            failed = True
        seen_ids.add(identifier)
    if args.path is None:
        expected_index = render_index(records)
        actual_index = args.index.read_text(encoding="utf-8") if args.index.exists() else ""
        if actual_index != expected_index:
            print(f"ERROR {args.index}: index is stale; run scripts/add_case.py or rebuild_index")
            failed = True
    if failed:
        return 1
    print(f"Validated {len(paths)} case file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
