# WeedDAO Cannabis Data Record v0.2 Draft

**Status:** **EXTERNAL REVIEW CANDIDATE** — experimental working draft on branch `v0.2-draft`

This branch publishes WeedDAO Cannabis Data Record **`v0.2-draft`** for **independent external review**.

It is **not** a release, **not** an industry standard, **not** a regulatory specification, and makes **no claim of industry adoption**.

| Item | Value |
|------|--------|
| Active review draft | `0.2-draft` (`schemas/weeddao-record-v0.2-draft.schema.json`) |
| Published frozen baseline | `v0.1-alpha` (unchanged; still validated by `scripts/validate.py`) |
| Branch | [`v0.2-draft`](https://github.com/weeddaoresearch/weeddao-standard/tree/v0.2-draft) |
| License | [Apache-2.0](LICENSE) |
| Review brief | [docs/v0.2-external-review-brief.md](docs/v0.2-external-review-brief.md) |
| Quickstart | [docs/v0.2-quickstart.md](docs/v0.2-quickstart.md) |
| RFC | [docs/v0.2-request-for-comments.md](docs/v0.2-request-for-comments.md) |
| Evidence log | [docs/v0.2-review-evidence.md](docs/v0.2-review-evidence.md) (empty until real external evidence) |
| Conceptual board | [STATUS.md](STATUS.md) |

**WeedDAO = Weed Data Alliance Organization.** The name refers to an alliance around open cannabis data interoperability; WeedDAO is not a decentralized autonomous organization and has no token.

> **Different platforms. Different organizations. One shared data language.**

This is a **coordination / data layer**. It does not replace growers, labs, researchers, dispensaries, or software products.

## Relationship to v0.1-alpha

- **`v0.1-alpha`** is the **published frozen baseline** (tag `v0.1-alpha`). Schema and tag must not be modified on this review track.
- **`v0.2-draft`** is the **evidence-driven successor** based on a public COA corpus:
  - **50 COAs / 8 jurisdictions / 7 labs / 40 primary / 7 secondary**
  - Critical interoperability gaps addressed in core: below-limit (#1, 35), not-performed (#2, 22), ND (#3, 48), multi-unit (#4, 43)
- Historical v0.1 docs under `docs/` remain preserved (specification, field reference, v0.1 review brief, etc.).

## Design highlights (v0.2-draft)

- **Subject model** — required `subject` (`subject_type`, `subject_id`); finished products use `product_batch` instead of forcing `cultivation_batch_id`
- **Sample lifecycle** — optional `lab_results.sample` with distinct `collected_at` / `received_at` / `reported_at` (never silently substituted for `tested_at`)
- **External identifiers** — open `scheme` + `value` (track-and-trace, lab sample, producer lot, …)
- **`result_state` vs `assessment`** — measurement state (detected / ND / below-limit / not-performed / …) is separate from pass/fail assessment; no sentinel `0` for ND or visual-only passes

See [docs/v0.2-design.md](docs/v0.2-design.md) and [docs/v0.1-to-v0.2-migration.md](docs/v0.1-to-v0.2-migration.md).

## What this is not

- Not an official or “industry-leading” standard
- Not a v0.2 release or tagged version
- Not a replacement for laboratory methods, agronomy practice, or business software
- Not a compliance or certification scheme
- Not related to tokens, blockchains, NFTs, or crypto assets of any kind

## Quick start (v0.2-draft)

Full path: [docs/v0.2-quickstart.md](docs/v0.2-quickstart.md) (includes **INDEPENDENT IMPLEMENTATION CHALLENGE**).

```bash
git checkout v0.2-draft
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_v0.2.py
python scripts/validate_v0.2.py examples/v0.2-draft/01-minimal-subject.json
```

Minimal record:

```json
{
  "schema_version": "0.2-draft",
  "record_id": "v02-ex-001-minimal",
  "created_at": "2026-09-18T12:00:00Z",
  "subject": {
    "subject_type": "sample",
    "subject_id": "sample-minimal-001"
  }
}
```

## Repository layout (review-relevant)

```
weeddao-standard/
├── README.md                          # this file (v0.2-draft branch)
├── STATUS.md
├── schemas/
│   ├── weeddao-cultivation-record-v0.1-alpha.schema.json   # frozen baseline
│   └── weeddao-record-v0.2-draft.schema.json               # active review draft
├── examples/
│   ├── minimal-record.json / complete-record.json          # v0.1
│   └── v0.2-draft/                                         # v0.2 examples
├── docs/
│   ├── v0.2-external-review-brief.md
│   ├── v0.2-quickstart.md
│   ├── v0.2-request-for-comments.md
│   ├── v0.2-outreach-copy.md
│   ├── v0.2-review-evidence.md
│   ├── v0.2-design.md
│   ├── v0.1-to-v0.2-migration.md
│   ├── v0.2-corpus-validation.md
│   └── … (historical v0.1 docs preserved)
├── scripts/
│   ├── validate.py            # v0.1-alpha
│   └── validate_v0.2.py       # v0.2-draft (+ --shadow)
└── .github/ISSUE_TEMPLATE/
    ├── v0.2-implementation-feedback.md
    └── … (v0.1 templates kept)
```

## Documentation

| Document | Purpose |
|----------|---------|
| [STATUS.md](STATUS.md) | Published baseline vs active review draft |
| [v0.2-external-review-brief.md](docs/v0.2-external-review-brief.md) | ~2–3 min reviewer brief |
| [v0.2-quickstart.md](docs/v0.2-quickstart.md) | Validate + independent challenge |
| [v0.2-request-for-comments.md](docs/v0.2-request-for-comments.md) | Concise RFC |
| [v0.2-outreach-copy.md](docs/v0.2-outreach-copy.md) | Short review-request messages |
| [v0.2-review-evidence.md](docs/v0.2-review-evidence.md) | External evidence log (empty) |
| [v0.2-design.md](docs/v0.2-design.md) | Design rationale |
| [v0.1-to-v0.2-migration.md](docs/v0.1-to-v0.2-migration.md) | Migration notes |
| [v0.2-corpus-validation.md](docs/v0.2-corpus-validation.md) | Shadow corpus results |
| [specification-v0.1-alpha.md](docs/specification-v0.1-alpha.md) | Historical v0.1 normative overview (preserved) |
| [RELEASE-v0.1-alpha.md](RELEASE-v0.1-alpha.md) | v0.1-alpha release notes (preserved) |

## License

Copyright 2026 WeedDAO Contributors. Licensed under the [Apache License 2.0](LICENSE).
