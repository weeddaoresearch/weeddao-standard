# Changelog

All notable changes to the WeedDAO Open Cannabis Data Standard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to experimental pre-1.0 versioning.

## [0.1-alpha] — 2026-09-18

### Added

- Initial experimental cultivation record schema (`schemas/weeddao-cultivation-record-v0.1-alpha.schema.json`) targeting JSON Schema Draft 2020-12.
- Required fields: `schema_version`, `record_id`, `cultivation_batch_id`, `created_at`.
- Optional top-level sections: `producer`, `cultivar`, `cultivation`, `environment`, `irrigation_nutrition`, `harvest`, `post_harvest`, `lab_results`, `outcomes`, `provenance`.
- Explicit unit field naming for environment (Celsius, %, kPa, ppm, µmol/m²/s, mol/m²/day).
- Cannabinoid objects `{value, unit}` and extensible terpene arrays.
- Optional lab safety structures (pesticides, heavy metals, microbials, mycotoxins, residual solvents).
- Provenance methods: `self_reported`, `sensor_measured`, `laboratory_verified`, `third_party_verified`, `derived`.
- Missing-data semantics via `null` plus `not_measured` / `not_applicable` / `withheld` (no magic numbers).
- Distinction between reported and genetically verified cultivar identity.
- Minimal and complete example records; valid/invalid test fixtures; `scripts/validate.py`.
- Specification, field reference, interoperability, privacy, and RFC documents.


### Documentation (external review packaging)

- Added `RELEASE-v0.1-alpha.md`, `STATUS.md`, `docs/external-review-brief.md`, `docs/quickstart.md`, `docs/review-evidence.md`, `docs/outreach-copy.md`, `review-tracker.json`, and `.github/ISSUE_TEMPLATE/` for external review.
- Schema unchanged for this packaging step.

### Notes

- This release is **experimental and open for comment**. It is **not** a regulatory standard, certification scheme, or finalized specification.
