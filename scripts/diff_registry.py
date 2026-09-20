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
    return date.fromisoformat(value)

def effective_on(rule, as_of):
    eff = rule.get("effective", {})
    start = date.fromisoformat(eff["start_date"]) if eff.get("start_date") else None
    end = date.fromisoformat(eff["end_date"]) if eff.get("end_date") else None
    if start and as_of < start:
        return False
    if end and as_of > end:
        return False
    return rule.get("status") != "withdrawn"

def analyte_index():
    bundle = load_json(ANALYTE_FILE)
    return {r["analyte_id"]: r for r in bundle.get("records", [])}

def all_rules():
    rows = []
    for path in sorted(RULE_DIR.glob("*seed-0.1-draft.json")):
        bundle = load_json(path)
        for rule in bundle.get("records", []):
            rows.append((path.name, rule))
    return rows

def scope_key(rule):
    scope = rule.get("scope", {})
    return (
        scope.get("program"),
        tuple(sorted(scope.get("product_types", []))),
        tuple(sorted(scope.get("matrices", []))),
    )

def requirement_key(rule, req):
    j = rule.get("jurisdiction", {})
    return (
        j.get("subdivision") or j.get("name"),
        scope_key(rule),
        req.get("requirement_id"),
    )

def semantic_payload(req):
    return {
        "requirement_type": req.get("requirement_type"),
        "test_category": req.get("test_category"),
        "analyte_id": req.get("analyte_id"),
        "comparator": req.get("comparator"),
        "threshold": req.get("threshold"),
        "summary": req.get("source_text_summary"),
        "notes": req.get("notes"),
    }

def record_for(rule, req, bundle, analytes):
    aid = req.get("analyte_id")
    return {
        "jurisdiction": rule.get("jurisdiction", {}).get("name"),
        "subdivision": rule.get("jurisdiction", {}).get("subdivision"),
        "authority": rule.get("authority"),
        "rule_id": rule.get("rule_id"),
        "scope": rule.get("scope"),
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
        "bundle": bundle,
    }

def snapshot(as_of, jurisdiction=None, analyte=None, requirement_type=None):
    analytes = analyte_index()
    out = {}
    for bundle, rule in all_rules():
        j = rule.get("jurisdiction", {})
        j_text = " ".join(str(j.get(k, "")) for k in ("name", "subdivision", "country")).lower()
        if jurisdiction and jurisdiction.lower() not in j_text:
            continue
        if not effective_on(rule, as_of):
            continue
        for req in rule.get("requirements", []):
            if analyte and req.get("analyte_id") != analyte:
                continue
            if requirement_type and req.get("requirement_type") != requirement_type:
                continue
            key = requirement_key(rule, req)
            row = record_for(rule, req, bundle, analytes)
            # Multiple simultaneously effective records with the same semantic key would
            # be ambiguous. Preserve them instead of silently overwriting.
            out.setdefault(key, []).append(row)
    return out

def single_or_list(rows):
    if rows is None:
        return None
    return rows[0] if len(rows) == 1 else rows

def main():
    ap = argparse.ArgumentParser(description="Compare WeedDAO testing-rule registry across two dates")
    ap.add_argument("--from-date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--to-date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--jurisdiction", help="Jurisdiction name or subdivision, e.g. California or US-CA")
    ap.add_argument("--analyte", help="WeedDAO analyte ID")
    ap.add_argument("--requirement-type", help="Filter requirement_type")
    ap.add_argument("--json", action="store_true", help="Emit JSON")
    args = ap.parse_args()

    from_date = parse_date(args.from_date)
    to_date = parse_date(args.to_date)
    if to_date < from_date:
        raise SystemExit("--to-date must be on or after --from-date")

    before = snapshot(from_date, args.jurisdiction, args.analyte, args.requirement_type)
    after = snapshot(to_date, args.jurisdiction, args.analyte, args.requirement_type)

    changes = []
    for key in sorted(set(before) | set(after), key=lambda x: str(x)):
        b_rows = before.get(key)
        a_rows = after.get(key)

        if b_rows is None:
            changes.append({
                "change_type": "ADDED",
                "before": None,
                "after": single_or_list(a_rows),
            })
            continue

        if a_rows is None:
            changes.append({
                "change_type": "REMOVED",
                "before": single_or_list(b_rows),
                "after": None,
            })
            continue

        # If either side has overlapping records, expose the ambiguity rather than
        # pretending there is one authoritative row.
        if len(b_rows) != 1 or len(a_rows) != 1:
            changes.append({
                "change_type": "OVERLAP_REVIEW",
                "before": single_or_list(b_rows),
                "after": single_or_list(a_rows),
            })
            continue

        b = b_rows[0]
        a = a_rows[0]
        b_sem = semantic_payload(b)
        a_sem = semantic_payload(a)
        source_transition = b.get("rule_id") != a.get("rule_id")

        if b_sem != a_sem:
            changed_fields = [
                field for field in b_sem
                if b_sem.get(field) != a_sem.get(field)
            ]
            changes.append({
                "change_type": "MODIFIED",
                "changed_fields": changed_fields,
                "source_transition": source_transition,
                "before": b,
                "after": a,
            })
        elif source_transition:
            changes.append({
                "change_type": "SOURCE_TRANSITION",
                "changed_fields": [],
                "source_transition": True,
                "before": b,
                "after": a,
            })

    result = {
        "from_date": args.from_date,
        "to_date": args.to_date,
        "jurisdiction": args.jurisdiction,
        "analyte": args.analyte,
        "requirement_type": args.requirement_type,
        "change_count": len(changes),
        "changes": changes,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(
        f"WEEDDAO_REGISTRY_DIFF from={args.from_date} to={args.to_date} "
        f"changes={len(changes)}"
    )
    for change in changes:
        row = change.get("after") or change.get("before")
        if isinstance(row, list):
            label = "overlapping records"
        else:
            aid = row.get("analyte_id") if row else None
            name = row.get("analyte_name") if row else None
            category = row.get("test_category") if row else None
            label = f"{aid or '-'} {name or category or '-'}"
        extra = ""
        if change.get("changed_fields"):
            extra = " fields=" + ",".join(change["changed_fields"])
        print(f"{change['change_type']} | {label}{extra}")

if __name__ == "__main__":
    main()
