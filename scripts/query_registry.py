#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE_DIR = ROOT / "registry" / "rules"
ANALYTE_FILE = ROOT / "registry" / "analytes" / "seed-0.1-draft.json"

def load_json(path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def parse_date(value):
    return date.fromisoformat(value) if value else None

def effective_on(rule, as_of):
    eff = rule.get("effective", {})
    start = parse_date(eff.get("start_date"))
    end = parse_date(eff.get("end_date"))
    if start and as_of < start:
        return False
    if end and as_of > end:
        return False
    return rule.get("status") not in {"withdrawn"}

def analyzer_index():
    bundle = load_json(ANALYTE_FILE)
    return {r["analyte_id"]: r for r in bundle["records"]}

def all_rules():
    rows = []
    for path in sorted(RULE_DIR.glob("*seed-0.1-draft.json")):
        bundle = load_json(path)
        for rule in bundle.get("records", []):
            rows.append((path.name, rule))
    return rows

def main():
    ap = argparse.ArgumentParser(description="Query experimental WeedDAO testing-rule registry")
    ap.add_argument("--jurisdiction", help="Jurisdiction name or subdivision, e.g. New York or US-NY")
    ap.add_argument("--analyte", help="WeedDAO analyte ID, e.g. WDA-AN-000016")
    ap.add_argument("--requirement-type", help="Filter requirement_type")
    ap.add_argument("--test-category", help="Filter test_category")
    ap.add_argument("--as-of", default=str(date.today()), help="YYYY-MM-DD; default today")
    ap.add_argument("--include-out-of-period", action="store_true", help="Do not filter by effective dates")
    ap.add_argument("--json", action="store_true", help="Emit JSON")
    args = ap.parse_args()

    as_of = parse_date(args.as_of)
    analytes = analyzer_index()
    output = []

    for bundle_name, rule in all_rules():
        j = rule.get("jurisdiction", {})
        j_text = " ".join(str(j.get(k, "")) for k in ("name", "subdivision", "country")).lower()
        if args.jurisdiction and args.jurisdiction.lower() not in j_text:
            continue
        if not args.include_out_of_period and not effective_on(rule, as_of):
            continue

        for req in rule.get("requirements", []):
            if args.analyte and req.get("analyte_id") != args.analyte:
                continue
            if args.requirement_type and req.get("requirement_type") != args.requirement_type:
                continue
            if args.test_category and req.get("test_category") != args.test_category:
                continue

            aid = req.get("analyte_id")
            output.append({
                "jurisdiction": j.get("name"),
                "subdivision": j.get("subdivision"),
                "authority": rule.get("authority"),
                "rule_id": rule.get("rule_id"),
                "effective_start": rule.get("effective", {}).get("start_date"),
                "effective_end": rule.get("effective", {}).get("end_date"),
                "requirement_id": req.get("requirement_id"),
                "requirement_type": req.get("requirement_type"),
                "test_category": req.get("test_category"),
                "analyte_id": aid,
                "analyte_name": analytes.get(aid, {}).get("canonical_name") if aid else None,
                "comparator": req.get("comparator"),
                "threshold": req.get("threshold"),
                "summary": req.get("source_text_summary"),
                "notes": req.get("notes"),
                "sources": rule.get("sources", []),
                "bundle": bundle_name
            })

    if args.json:
        print(json.dumps({
            "as_of": args.as_of,
            "count": len(output),
            "results": output
        }, indent=2, ensure_ascii=False))
        return

    print(f"WEEDDAO_REGISTRY_QUERY as_of={args.as_of} results={len(output)}")
    for row in output:
        threshold = row["threshold"]
        if threshold:
            value = f"{row['comparator'] or ''}{threshold['value']} {threshold['unit']}"
        else:
            value = "-"
        analyte = row["analyte_id"] or "-"
        name = row["analyte_name"] or row["test_category"] or "-"
        print(
            f"{row['subdivision'] or row['jurisdiction']} | {analyte} | {name} | "
            f"{row['requirement_type']} | {value} | {row['rule_id']}"
        )

if __name__ == "__main__":
    main()
