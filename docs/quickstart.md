# Quickstart — validate a cultivation record in about 10 minutes

**Standard:** WeedDAO Open Cannabis Data Standard `v0.1-alpha` (experimental working draft)

## 1. Find the schema (1 min)

Path:

```text
schemas/weeddao-cultivation-record-v0.1-alpha.schema.json
```

Dialect: JSON Schema Draft 2020-12. Instance documents must set `"schema_version": "0.1-alpha"`.

## 2. Open the examples (2 min)

| File | Purpose |
|------|---------|
| [examples/minimal-record.json](../examples/minimal-record.json) | Smallest valid record |
| [examples/complete-record.json](../examples/complete-record.json) | Fully populated illustration |

Minimal record (all required fields):

```json
{
  "schema_version": "0.1-alpha",
  "record_id": "rec-001-minimal",
  "cultivation_batch_id": "batch-2026-001",
  "created_at": "2026-09-18T10:00:00Z"
}
```

## 3. Validate locally (4 min)

From the `weeddao-standard/` directory (using the existing project venv or a new one):

```bash
# Option A — shared WeedDAO venv (if present one level up)
source ../.venv/bin/activate

# Option B — local venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/validate.py
```

Expected: schema OK; all `tests/valid` (and examples) pass; all `tests/invalid` fail as expected.

Validate one file:

```bash
python scripts/validate.py examples/minimal-record.json
python scripts/validate.py path/to/your-record.json
```

## 4. Required fields checklist (1 min)

| Field | Constraint |
|-------|------------|
| `schema_version` | Exactly `"0.1-alpha"` |
| `record_id` | Non-empty string |
| `cultivation_batch_id` | Non-empty string |
| `created_at` | ISO 8601 date-time string |

Everything else is optional. Prefer `null` + gap reasons over sentinel numbers. See [field-reference.md](field-reference.md).

## 5. Produce your first valid record (2 min)

1. Copy `examples/minimal-record.json`
2. Replace `record_id` and `cultivation_batch_id` with your opaque IDs
3. Set `created_at` to a real UTC timestamp
4. Optionally add only the sections you can populate (e.g. `harvest`, `lab_results`)
5. Run `python scripts/validate.py your-record.json`

If it prints `OK`, you have a structurally valid `0.1-alpha` cultivation record.

## Next

- Domain questions: [external-review-brief.md](external-review-brief.md)
- Mapping tips: [interoperability.md](interoperability.md)
- Comment process: [request-for-comments.md](request-for-comments.md)
