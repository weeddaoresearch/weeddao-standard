# Cannlytics → WeedDAO v0.2-draft compatibility bridge

**Branch work:** `cannlytics-compat` (forked from `v0.2-draft` @ `ff294e7`)

Experimental, conservative bridge from Cannlytics `LabResult` / `ResultDetail` (pinned upstream) into WeedDAO Cannabis Data Record **`0.2-draft`**.

This compatibility layer:

- Does **not** modify WeedDAO schemas to fit Cannlytics
- Documents semantic defects (especially ambiguous `nt` and null floats) instead of guessing
- Is **not** a release, merge to main, or schema change

## Upstream pin

See [UPSTREAM.md](UPSTREAM.md).

- Repo: https://github.com/cannlytics/cannabis_results
- Commit: `a4e05a9f7367ac0b1637bd84773875b3bd1453ec`
- License: CC BY 4.0

## How to run

```bash
# from repo root
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# single record
python bridges/cannlytics_to_weeddao.py \
  compat/cannlytics/fixtures/01-numeric-flower.json \
  -o /tmp/out.json --report /tmp/report.json

# tests
python -m pytest tests/v0.2/test_cannlytics_bridge.py -q
python scripts/validate_v0.2.py examples/compat/weeddao-output.json
```

Library usage:

```python
from bridges.cannlytics_to_weeddao import convert_lab_result
record, report = convert_lab_result(lab_result_dict)
```

## Deliverables

| Path | Purpose |
|------|---------|
| [semantic-rules.json](semantic-rules.json) | 10 authoritative mapping rules |
| [field-map.json](field-map.json) | Machine-readable field classifications |
| [SEMANTIC_AUDIT.md](SEMANTIC_AUDIT.md) | Human semantic defect audit |
| [fixtures/](fixtures/) | Synthetic LabResult-shaped JSON (no fabricated COA numbers) |
| `bridges/cannlytics_to_weeddao.py` | CLI + library |
| `tests/v0.2/test_cannlytics_bridge.py` | Focused semantic tests |
| `examples/compat/` | Example input/output pair |

## Critical limitations (do not ignore)

1. **`nt` is ambiguous.** Cannlytics `normalize_status` maps `not tested`, `n/a`, `na`, `-`, `''` → `nt`. The bridge **never** maps `nt` → WeedDAO `not_tested`. Panel `nt` is omitted from WeedDAO panel status (`PANEL_NT_AMBIGUOUS`). Analyte `nt` → `result_state=unknown` + `reported_as="nt"`.
2. **Null cannabinoid floats are ambiguous.** `Optional[float] = None` cannot distinguish missing vs ND vs not tested. Nulls are omitted (never coerced to `0` or `ND`).
3. **Subject type is often indeterminate** for flower/bud/biomass without harvest/lot metadata → `subject_type=other` + `SUBJECT_TYPE_AMBIGUOUS` (never auto-`cultivation_batch`).
4. **Panel status alone ≠ analyte ResultDetail.** Pass/fail without analytes is status-only.
5. **`date_expires` is not auto-mapped to `best_by`** (equivalence unsupported).
6. **Never fabricate COA / certificate numbers.**

## Audit classes

- `LOSSLESS_FOR_AVAILABLE_SEMANTICS` — all semantics in the Cannlytics *normalized* record represented without guessing (**not** “original COA was lossless”)
- `SEMANTICALLY_PARTIAL` — mapped with documented ambiguity flags
- `STRUCTURALLY_UNMAPPABLE` — missing `subject_id` candidates (`batch_number` / `sample_id` / `id`)
