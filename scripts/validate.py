#!/usr/bin/env python3
"""WeedDAO Open Cannabis Data Standard v0.1-alpha — record validator.

Validates cultivation records against the Draft 2020-12 JSON Schema.
Also performs a structural check that the schema document itself is loadable
and references Draft 2020-12.

Usage:
  python scripts/validate.py                          # schema + examples + tests
  python scripts/validate.py path/to/record.json ...  # specific files
  python scripts/validate.py --schema-only
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
SCHEMA_PATH = ROOT / "schemas" / "weeddao-cultivation-record-v0.1-alpha.schema.json"
EXPECTED_VERSION = "0.1-alpha"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema_document(schema: dict) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("Schema $schema must be Draft 2020-12 URI")
    if "schema_version" not in schema.get("properties", {}):
        errors.append("Schema missing schema_version property")
    else:
        sv = schema["properties"]["schema_version"]
        const = sv.get("const")
        enum = sv.get("enum")
        if const != EXPECTED_VERSION and not (enum and EXPECTED_VERSION in enum):
            errors.append(f"schema_version must constrain to {EXPECTED_VERSION!r}")
    required = schema.get("required", [])
    for field in ("schema_version", "record_id", "cultivation_batch_id", "created_at"):
        if field not in required:
            errors.append(f"Required field missing from schema.required: {field}")
    try:
        Draft202012Validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as e:
        errors.append(f"Schema failed Draft202012 check: {e.message}")
    return errors


def validate_record(schema: dict, data: dict, path: Path) -> list[str]:
    validator = Draft202012Validator(schema)
    return [f"{path}: {e.message} (at {list(e.path)})" for e in sorted(validator.iter_errors(data), key=lambda e: list(e.path))]


def discover_default_targets() -> tuple[list[Path], list[Path]]:
    valid = sorted((ROOT / "tests" / "valid").glob("*.json"))
    examples = sorted((ROOT / "examples").glob("*.json"))
    # Prefer tests/valid; include examples if not duplicated by name
    seen = {p.name for p in valid}
    for ex in examples:
        if ex.name not in seen:
            valid.append(ex)
    invalid = sorted((ROOT / "tests" / "invalid").glob("*.json"))
    return valid, invalid


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate WeedDAO cultivation records (v0.1-alpha).")
    parser.add_argument("paths", nargs="*", type=Path, help="JSON record files to validate")
    parser.add_argument("--schema-only", action="store_true", help="Only validate the schema document")
    parser.add_argument("--expect-fail", action="store_true", help="Exit 0 only if all given paths FAIL validation")
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

    if args.paths:
        targets = args.paths
        if args.expect_fail:
            failures = 0
            unexpected_pass = 0
            for path in targets:
                data = load_json(path)
                errs = validate_record(schema, data, path)
                if errs:
                    failures += 1
                    print(f"FAIL (expected) {path}: {errs[0]}")
                else:
                    unexpected_pass += 1
                    print(f"UNEXPECTED PASS {path}")
            if unexpected_pass:
                return 1
            return 0 if failures == len(targets) else 1

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

    # Default suite: valid must pass, invalid must fail
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
        print("\nAll checks passed.")
    else:
        print("\nOne or more checks failed.", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
