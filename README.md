<p align="center"><img src="assets/weeddao-mark.svg" alt="WeedDAO" width="92"></p>

# WeedDAO Open Cannabis Data Standard

**Version:** `0.1-alpha` (experimental, proposed)

An open, proposed data standard for cannabis cultivation records. This project defines a shared JSON shape so growers, laboratories, researchers, and software systems can exchange cultivation and lab data without inventing incompatible formats.

**WeedDAO = Weed Data Alliance Organization.** The name refers to an alliance around open cannabis data interoperability; WeedDAO is not a decentralized autonomous organization and has no token.

> **Different platforms. Different organizations. One shared data language.**

This is a **coordination / data layer**. It does not replace growers, labs, researchers, or software products. It is **not** a regulatory standard, **not** a certification program, **not** finalized, and makes **no claim of industry adoption**.

## Status

| Item | Value |
|------|--------|
| Schema version | `0.1-alpha` |
| Status | **EXTERNAL REVIEW** — see [STATUS.md](STATUS.md) |
| Maturity | Experimental working draft — proposed / under development |
| License | [Apache-2.0](LICENSE) |
| Release notes | [RELEASE-v0.1-alpha.md](RELEASE-v0.1-alpha.md) |
| Spec | [docs/specification-v0.1-alpha.md](docs/specification-v0.1-alpha.md) |
| RFC | [docs/request-for-comments.md](docs/request-for-comments.md) |
| External review brief | [docs/external-review-brief.md](docs/external-review-brief.md) |

## What this is

- A JSON Schema (Draft 2020-12) for a **cultivation record**
- Optional sections for producer, cultivar, cultivation, environment, irrigation/nutrition, harvest, post-harvest, lab results, outcomes, and provenance
- Explicit units, clear missing-data semantics, and provenance labels
- Privacy-conscious: **no PII is required**

## What this is not

- Not an official or “industry-leading” standard
- Not a replacement for laboratory methods, agronomy practice, or business software
- Not a compliance or certification scheme
- Not related to tokens, blockchains, NFTs, or crypto assets of any kind

## Repository layout

```
weeddao-standard/
├── README.md
├── STATUS.md
├── RELEASE-v0.1-alpha.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── review-tracker.json
├── requirements.txt
├── schemas/
│   └── weeddao-cultivation-record-v0.1-alpha.schema.json
├── examples/
│   ├── minimal-record.json
│   └── complete-record.json
├── docs/
│   ├── external-review-brief.md
│   ├── quickstart.md
│   ├── specification-v0.1-alpha.md
│   ├── field-reference.md
│   ├── interoperability.md
│   ├── privacy.md
│   ├── request-for-comments.md
│   ├── review-evidence.md
│   └── outreach-copy.md
├── tests/
│   ├── valid/
│   └── invalid/
├── scripts/
│   └── validate.py
└── .github/ISSUE_TEMPLATE/
    ├── field-request.md
    ├── schema-problem.md
    └── implementation-feedback.md
```

## Quick start

Full path: [docs/quickstart.md](docs/quickstart.md) (~10 minutes).

### Minimal record

Only four fields are required:

```json
{
  "schema_version": "0.1-alpha",
  "record_id": "rec-001-minimal",
  "cultivation_batch_id": "batch-2026-001",
  "created_at": "2026-09-18T10:00:00Z"
}
```

See `examples/complete-record.json` for a fully populated illustration.

### Validate

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate.py
```

The validator checks:

1. The schema document itself (Draft 2020-12)
2. All `tests/valid/*.json` (and examples) — must pass
3. All `tests/invalid/*.json` — must fail for schema reasons

## Design highlights

- **`schema_version`** is fixed to `"0.1-alpha"` for this draft.
- **Environment** fields carry units in their names (e.g. `average_day_temp_c`, `average_vpd_kpa`, `ppfd_umol_m2_s`).
- **Cannabinoids** are objects `{ "value": number|null, "unit": "..." }` for `thc`, `thca`, `cbd`, `cbda`, `cbg`, `cbga`, `cbc`, `cbn`, `thcv`, plus totals.
- **Terpenes** are an extensible array of `{ name, value, unit }`.
- **Provenance** uses: `self_reported` | `sensor_measured` | `laboratory_verified` | `third_party_verified` | `derived`.
- **Missing data:** use `null`. Document why with `not_measured` / `not_applicable` / `withheld` — never magic numbers like `-1`, `999`, or `0` as sentinels.
- **Cultivar identity:** distinguish `reported` vs `genetically_verified` via `identity_status` and optional `genetic_verification`.

## Documentation

| Document | Purpose |
|----------|---------|
| [RELEASE-v0.1-alpha.md](RELEASE-v0.1-alpha.md) | External-review release notes |
| [STATUS.md](STATUS.md) | Conceptual status board |
| [external-review-brief.md](docs/external-review-brief.md) | ~2 min reviewer brief |
| [quickstart.md](docs/quickstart.md) | 10-minute developer path |
| [specification-v0.1-alpha.md](docs/specification-v0.1-alpha.md) | Normative overview of the draft |
| [field-reference.md](docs/field-reference.md) | Field-by-field reference |
| [interoperability.md](docs/interoperability.md) | How systems can map to/from this shape |
| [privacy.md](docs/privacy.md) | PII avoidance and sharing guidance |
| [request-for-comments.md](docs/request-for-comments.md) | Open questions and comment process |
| [review-evidence.md](docs/review-evidence.md) | External review evidence log (empty until real reviews) |
| [outreach-copy.md](docs/outreach-copy.md) | Short review-request messages |
| [GOVERNANCE.md](GOVERNANCE.md) | How decisions are made |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |

## License

Copyright 2026 WeedDAO Contributors. Licensed under the [Apache License 2.0](LICENSE).
