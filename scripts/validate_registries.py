#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ANALYTE_SCHEMA = ROOT / "schemas" / "weeddao-analyte-registry-0.1-draft.schema.json"
RULE_SCHEMA = ROOT / "schemas" / "weeddao-testing-rule-0.1-draft.schema.json"
ANALYTE_SEED = ROOT / "registry" / "analytes" / "seed-0.1-draft.json"
RULE_DIR = ROOT / "registry" / "rules"

def load(path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def validate_records(records, schema, label):
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for idx, record in enumerate(records):
        for err in sorted(validator.iter_errors(record), key=lambda e: list(e.path)):
            errors.append(f"{label}[{idx}] {list(err.path)}: {err.message}")
    return errors

def main():
    analyte_bundle = load(ANALYTE_SEED)
    rule_bundles = [(p, load(p)) for p in sorted(RULE_DIR.glob("*seed-0.1-draft.json"))]
    analyte_schema = load(ANALYTE_SCHEMA)
    rule_schema = load(RULE_SCHEMA)

    errors = []
    errors += validate_records(analyte_bundle["records"], analyte_schema, "analytes")
    all_rules = []
    for path, bundle in rule_bundles:
        errors += validate_records(bundle["records"], rule_schema, f"rules:{path.name}")
        all_rules.extend(bundle["records"])

    analyte_ids = [r["analyte_id"] for r in analyte_bundle["records"]]
    rule_ids = [r["rule_id"] for r in all_rules]

    if len(analyte_ids) != len(set(analyte_ids)):
        errors.append("duplicate analyte_id detected")
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate rule_id detected")

    known = set(analyte_ids)
    for rule in all_rules:
        for req in rule.get("requirements", []):
            aid = req.get("analyte_id")
            if aid is not None and aid not in known:
                errors.append(f"{rule['rule_id']} references unknown analyte_id {aid}")

    if errors:
        print("REGISTRY_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        raise SystemExit(1)

    print("REGISTRY_VALIDATION=PASS")
    print(f"ANALYTES={len(analyte_ids)}")
    print(f"RULE_BUNDLES={len(rule_bundles)}")
    print(f"RULE_RECORDS={len(rule_ids)}")
    print("RULE_ANALYTE_REFERENCES=RESOLVED")

if __name__ == "__main__":
    main()
