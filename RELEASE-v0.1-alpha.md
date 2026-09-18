# Release: WeedDAO Open Cannabis Data Standard v0.1-alpha

**Release name:** WeedDAO Open Cannabis Data Standard `v0.1-alpha`  
**Status:** EXTERNAL REVIEW  
**Date:** 2026-09-18  

## Purpose

Publish an experimental, proposed cultivation-record data shape so growers, laboratories, researchers, and software developers can review and comment on a shared JSON exchange format before any later draft.

This release packages a frozen `0.1-alpha` schema, examples, a local validator, and supporting documentation for **independent external review**.

## Scope

In scope for this draft:

- One document type: **Cultivation Record** (JSON Schema Draft 2020-12)
- Required fields: `schema_version`, `record_id`, `cultivation_batch_id`, `created_at`
- Optional sections: producer, cultivar, cultivation, environment, irrigation/nutrition, harvest, post-harvest, lab results, outcomes, provenance, extensions, data gaps
- Explicit units, missing-data semantics, and provenance labels
- Minimal and complete examples; valid/invalid fixtures; `scripts/validate.py`

Out of scope:

- Regulatory compliance frameworks or official standards status
- Formal certification or grading programs
- Tokens, blockchains, NFTs, or crypto assets
- Claiming industry adoption or finalized maturity

## Limitations

- Experimental working draft — fields and enums **may change** after comment
- Not a laboratory method standard or agronomy practice guide
- Not legal advice; privacy notes are guidance only
- Compatibility is defined only for `schema_version: "0.1-alpha"`
- No claim that any jurisdiction, lab network, or vendor has adopted this draft

## Who should review

| Audience | Useful focus |
|----------|----------------|
| Growers / cultivation operators | Field practicality, batch IDs, environment and harvest coverage |
| Laboratories | Cannabinoid/terpene shapes, safety block, COA mapping |
| Researchers | Provenance, missing-data semantics, cultivar identity |
| Software developers | Schema clarity, validator usage, interoperability mapping |

## How to feedback

1. Read [docs/external-review-brief.md](docs/external-review-brief.md) (~2 minutes)
2. Optionally follow [docs/quickstart.md](docs/quickstart.md) to validate a record locally
3. Open an issue using templates under `.github/ISSUE_TEMPLATE/`, or comment via the process in [docs/request-for-comments.md](docs/request-for-comments.md)
4. Reference field paths (e.g. `environment.average_vpd_kpa`) and include sample JSON when proposing shape changes
5. Identity is **optional** — organizational or role context is enough

See also [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).

## Experimental — not regulatory

This draft is an **open cannabis data standard under development**. It is **not** a regulatory standard, **not** a certification scheme, and **not** finalized. Validation against the schema means structural conformance to this experimental draft only.

## Compatibility definition

A JSON document is compatible with this release if and only if:

1. It is valid JSON
2. It validates against `schemas/weeddao-cultivation-record-v0.1-alpha.schema.json` using a Draft 2020-12 capable validator
3. `schema_version` is exactly `"0.1-alpha"`
4. Required fields are present and satisfy schema constraints

Receivers should not assume compatibility with any future draft version number.

## Links

| Artifact | Path |
|----------|------|
| Schema | [schemas/weeddao-cultivation-record-v0.1-alpha.schema.json](schemas/weeddao-cultivation-record-v0.1-alpha.schema.json) |
| Examples | [examples/](examples/) |
| Field reference | [docs/field-reference.md](docs/field-reference.md) |
| Specification | [docs/specification-v0.1-alpha.md](docs/specification-v0.1-alpha.md) |
| RFC | [docs/request-for-comments.md](docs/request-for-comments.md) |
| Governance | [GOVERNANCE.md](GOVERNANCE.md) |
| External review brief | [docs/external-review-brief.md](docs/external-review-brief.md) |
| Quickstart | [docs/quickstart.md](docs/quickstart.md) |
| Status | [STATUS.md](STATUS.md) |
| Review evidence log | [docs/review-evidence.md](docs/review-evidence.md) |
| Review tracker | [review-tracker.json](review-tracker.json) |
| License | [LICENSE](LICENSE) (Apache-2.0) |
