# Registry seed notes

## Purpose

This seed is intentionally small. It proves the registry mechanics with evidence already available to WeedDAO rather than attempting comprehensive coverage.

## Analyte seed

The initial analyte bundle contains **19 provisional identifiers**.

Evidence comes from:

- WeedDAO public COA corpus cases COA-001, COA-002, COA-003, and COA-046;
- California DCC DCC-2025-03-R final pesticide regulation for Abamectin and Acephate identifiers / CAS values.

The seed includes cannabinoids, aggregate cannabinoid metrics, four heavy metals, and two pesticide targets.

All entries remain **provisional** while registry governance is under review.

## California testing-rule seed

The first real rules seed models only a narrow slice of California residual pesticide rules:

- Abamectin;
- Acephate;
- inhalable vs non-inhalable product scope;
- Phase I beginning October 1, 2026 and ending March 31, 2028;
- Phase II beginning April 1, 2028.

It is **not a complete California ruleset** and must not be used as a stand-alone compliance source.

The authoritative source is the California Department of Cannabis Control final text for DCC-2025-03-R.

## Why this is useful

The seed demonstrates three long-term WeedDAO capabilities:

1. a stable analyte ID can survive changing display labels;
2. a regulatory rule can reference that ID instead of duplicating free-text names;
3. the same analyte can carry different thresholds by jurisdiction, product scope, and effective date without changing its identity.

## Validation

Run:

```bash
python scripts/validate_registries.py
```

The validator checks:

- each analyte record against the analyte registry schema;
- each rule record against the testing-rule schema;
- duplicate IDs;
- rule-to-analyte referential integrity.
