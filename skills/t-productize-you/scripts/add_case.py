#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from case_library import rebuild_index, write_case


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Add one product case and rebuild the case index.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--cases-dir", type=Path, default=SKILL_DIR / "references" / "cases")
    parser.add_argument("--index", type=Path, default=SKILL_DIR / "references" / "case-index.md")
    args = parser.parse_args()
    record = json.loads(args.input_json.read_text(encoding="utf-8"))
    destination = write_case(record, args.cases_dir)
    rebuild_index(args.cases_dir, args.index)
    print(f"Added {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
