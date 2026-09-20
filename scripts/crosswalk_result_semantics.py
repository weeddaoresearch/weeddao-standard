#!/usr/bin/env python3
"""Query the WeedDAO ↔ OpenTHC result-semantics crosswalk.

This tool is intentionally read-only. It reports documented relationships and
warnings; it does not transform laboratory data.
"""

import argparse
import json
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parents[1] / "compatibility" / "wcia-openthc-result-semantics-0.1-draft.json"


def load(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def matches(mapping, weeddao=None, openthc=None):
    if weeddao and weeddao.lower() not in str(mapping.get("weeddao_concept", "")).lower():
        return False
    if openthc and openthc.lower() not in str(mapping.get("openthc_concept", "")).lower():
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Query WeedDAO/OpenTHC result-semantic mappings")
    parser.add_argument("--weeddao", help="substring of a WeedDAO concept, e.g. not_performed")
    parser.add_argument("--openthc", help="substring of an OpenTHC concept, e.g. status=nd")
    parser.add_argument("--relationship", help="filter by relationship type")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit JSON")
    parser.add_argument("--crosswalk", type=Path, default=DEFAULT_PATH, help="path to crosswalk JSON")
    args = parser.parse_args()

    if not any([args.weeddao, args.openthc, args.relationship]):
        parser.error("provide --weeddao, --openthc, or --relationship")

    data = load(args.crosswalk)
    rows = []
    for mapping in data.get("mappings", []):
        if not matches(mapping, args.weeddao, args.openthc):
            continue
        if args.relationship and mapping.get("relationship") != args.relationship:
            continue
        rows.append(mapping)

    if args.as_json:
        print(json.dumps(rows, indent=2))
        return

    if not rows:
        print("No documented mapping found.")
        return

    for idx, row in enumerate(rows, 1):
        if idx > 1:
            print()
        print(f"WeedDAO: {row.get('weeddao_concept')}")
        print(f"OpenTHC: {row.get('openthc_concept')}")
        print(f"Relationship: {row.get('relationship')}")
        print(f"Lossy: {row.get('lossy')}")
        if row.get("direction_note"):
            print(f"Direction note: {row['direction_note']}")
        if row.get("guidance"):
            print(f"Guidance: {row['guidance']}")
        if row.get("evidence"):
            print(f"Evidence: {row['evidence']}")


if __name__ == "__main__":
    main()
