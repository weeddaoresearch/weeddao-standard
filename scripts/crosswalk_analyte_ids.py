#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "compatibility" / "wcia-analyte-crosswalk-0.1-draft.json"

def load():
    with CROSSWALK.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def main():
    ap = argparse.ArgumentParser(description="Translate experimental WeedDAO/WCIA analyte identifiers.")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--weeddao", help="WeedDAO analyte ID")
    group.add_argument("--wcia", help="WCIA analyte ULID")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    data = load()
    results = []
    for row in data.get("mappings", []):
        if args.weeddao and row.get("weeddao_id") == args.weeddao:
            results.append(row)
        elif args.wcia and args.wcia in row.get("wcia_ids", []):
            results.append(row)

    output = {"count": len(results), "results": results}
    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    if not results:
        print("NO_CROSSWALK_MATCH")
        raise SystemExit(1)

    for row in results:
        print(f"{row['weeddao_id']} | {row['weeddao_name']} | {row['relationship']}")
        if row.get("wcia_ids"):
            for wid, name in zip(row["wcia_ids"], row["wcia_names"]):
                print(f"  WCIA {wid} | {name}")
        else:
            print("  WCIA exact mapping: none identified")
        if row.get("note"):
            print(f"  NOTE: {row['note']}")

if __name__ == "__main__":
    main()
