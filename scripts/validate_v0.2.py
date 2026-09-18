#!/usr/bin/env python3
"""WeedDAO Cannabis Data Record v0.2-draft — record validator.

Usage:
  python scripts/validate_v0.2.py
  python scripts/validate_v0.2.py path/to/record.json ...
  python scripts/validate_v0.2.py --schema-only
  python scripts/validate_v0.2.py --shadow   # validate corpus/v0.2-draft/mappings
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema is required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "weeddao-record-v0.2-draft.schema.json"
EXPECTED_VERSION = "0.2-draft"
EXPECTED_TITLE = "WeedDAO Cannabis Data Record v0.2 Draft"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema_document(schema: dict) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("Schema $schema must be Draft 2020-12 URI")
    if schema.get("title") != EXPECTED_TITLE:
        errors.append(f"Schema title must be {EXPECTED_TITLE!r}")
    sv = schema.get("properties", {}).get("schema_version", {})
    if sv.get("const") != EXPECTED_VERSION:
        errors.append(f"schema_version must constrain to {EXPECTED_VERSION!r}")
    required = schema.get("required", [])
    for field in ("schema_version", "record_id", "created_at", "subject"):
        if field not in required:
            errors.append(f"Required field missing from schema.required: {field}")
    if "cultivation_batch_id" in required:
        errors.append("cultivation_batch_id must not be required in v0.2-draft")
    try:
        Draft202012Validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as e:
        errors.append(f"Schema failed Draft202012 check: {e.message}")
    return errors


def validate_record(schema: dict, data: dict, path: Path) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"{path}: {e.message} (at {list(e.path)})"
        for e in sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    ]


def discover_default_targets() -> tuple[list[Path], list[Path]]:
    valid = sorted((ROOT / "tests" / "v0.2-draft" / "valid").glob("*.json"))
    examples = sorted((ROOT / "examples" / "v0.2-draft").glob("*.json"))
    seen = {p.name for p in valid}
    for ex in examples:
        if ex.name not in seen:
            valid.append(ex)
    invalid = sorted((ROOT / "tests" / "v0.2-draft" / "invalid").glob("*.json"))
    return valid, invalid


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate WeedDAO records (v0.2-draft).")
    parser.add_argument("paths", nargs="*", type=Path, help="JSON record files to validate")
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--shadow", action="store_true", help="Validate corpus/v0.2-draft/mappings")
    parser.add_argument("--expect-fail", action="store_true")
    args = parser.parse_args(argv)

    if not SCHEMA_PATH.is_file():
        print(f"ERROR: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 2

    schema = load_json(SCHEMA_PATH)
    schema_errors = validate_schema_document(schema)
    if schema_errors:
        print("SCHEMA INVALID:")
        for e in schema_errors:
            print(f"  - {e}")
        return 1
    print(f"OK  schema {SCHEMA_PATH.relative_to(ROOT)}")

    if args.schema_only:
        return 0

    if args.shadow:
        paths = sorted((ROOT / "corpus" / "v0.2-draft" / "mappings").glob("*.json"))
        if not paths:
            print("ERROR: no shadow mappings found", file=sys.stderr)
            return 1
        any_error = False
        for path in paths:
            data = load_json(path)
            errs = validate_record(schema, data, path)
            if errs:
                any_error = True
                print(f"FAIL {path.relative_to(ROOT)}")
                for e in errs[:5]:
                    print(f"  - {e}")
            else:
                print(f"OK   {path.relative_to(ROOT)}")
        return 1 if any_error else 0

    if args.paths:
        targets = args.paths
        if args.expect_fail:
            unexpected_pass = 0
            for path in targets:
                data = load_json(path)
                errs = validate_record(schema, data, path)
                if errs:
                    print(f"FAIL (expected) {path}: {errs[0]}")
                else:
                    unexpected_pass += 1
                    print(f"UNEXPECTED PASS {path}")
            return 1 if unexpected_pass else 0

        any_error = False
        for path in targets:
            data = load_json(path)
            errs = validate_record(schema, data, path)
            if errs:
                any_error = True
                print(f"FAIL {path}")
                for e in errs:
                    print(f"  - {e}")
            else:
                print(f"OK   {path}")
        return 1 if any_error else 0

    valid_paths, invalid_paths = discover_default_targets()
    exit_code = 0

    print("\n--- valid records (must pass) ---")
    for path in valid_paths:
        data = load_json(path)
        errs = validate_record(schema, data, path)
        if errs:
            exit_code = 1
            print(f"FAIL {path.relative_to(ROOT)}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {path.relative_to(ROOT)}")

    print("\n--- invalid records (must fail) ---")
    for path in invalid_paths:
        data = load_json(path)
        errs = validate_record(schema, data, path)
        if errs:
            print(f"FAIL (expected) {path.relative_to(ROOT)}: {errs[0]}")
        else:
            exit_code = 1
            print(f"UNEXPECTED PASS {path.relative_to(ROOT)}")

    if exit_code == 0:
        print("\nAll v0.2-draft checks passed.")
    else:
        print("\nOne or more v0.2-draft checks failed.", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
