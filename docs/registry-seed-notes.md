# Registry seed notes

## Purpose

This seed is intentionally small. It proves the registry mechanics with evidence already available to WeedDAO rather than attempting comprehensive coverage.

## Analyte seed

The initial analyte bundle contains **19 provisional identifiers**.

Evidence comes from:

- WeedDAO public COA corpus cases COA-001, COA-002, COA-003, and COA-046;
- California DCC DCC-2025-03-R final pesticide regulation for Abamectin and Acephate identifiers / CAS values;
- Oregon OAR 333-007-0400 Exhibit A Table 3 for the same pesticide labels, action levels, and regulator-specific identifiers.

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

## Oregon testing-rule seed

The second jurisdiction seed models the active Oregon OAR 333-007-0400 Table 3 action levels for the same two targets:

- Abamectin — 0.5 ppm;
- Acephate — 0.4 ppm.

The Oregon seed is effective March 31, 2022 and is represented as active as of September 19, 2026.

Oregon OHA is also conducting 2026 cannabis-testing rulemaking. Those proposals are not encoded as active rules.

## Cross-jurisdiction identifier finding

California and Oregon both use the label **Abamectin**, but their official testing tables use different CAS identifiers. The analyte schema was therefore extended so external identifiers can carry source and context provenance.

This is not silently reconciled. `WDA-AN-000016` remains provisional and preserves both regulator-specific identifiers for review.

See [California vs Oregon cross-jurisdiction proof](cross-jurisdiction-ca-or.md).

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


## Texas TCUP seed

Texas was added as the third jurisdiction because its model differs from the numeric pesticide examples in California and Oregon.

The seed records:

- required processed-product testing categories under 37 TAC §12.7(b);
- package-label potency and contaminant-test reporting requirements under §12.7(p);
- the current statutory low-THC definition of no more than 10 mg tetrahydrocannabinols per dosage unit under Occupations Code §169.001(3).

The seed does not invent contaminant action limits where the cited Texas TCUP provision does not provide them.

Texas DPS also states that only licensed dispensing organizations may test low-THC products; this structural difference is documented in `docs/texas-regulatory-model.md`.

An apparent mismatch remains between the current statute and older administrative-rule text in §12.7(q). WeedDAO preserves this as a review issue instead of silently resolving it.

Consumable-hemp rules under 25 TAC Chapter 300 are not imported into the TCUP seed.


## Massachusetts seed

Massachusetts is the fourth jurisdiction and adds a lab-centric regulatory model.

The seed records:

- Independent Testing Laboratory / market-release requirements;
- required testing categories and the statutory 72-hour contamination-reporting rule;
- ISO/IEC 17025-based laboratory qualification;
- +/-10% single-serving potency variance;
- heavy-metal upper limits for All Uses and Ingestion Only;
- the ingestion-only warning-label requirement;
- Administrative Order No. 4's single-ITL full-panel sample-package rule.

Massachusetts is actively reviewing testing protocols in 2026. Proposed recommendations are not treated as active requirements.

The Commission also publishes machine-readable testing datasets, making Massachusetts a strong candidate for future large-scale WeedDAO registry and validation testing.


## New York seed

New York is the fifth jurisdiction and adds a revision-heavy OCM testing model.

The seed records:

- ISO/IEC 17025 laboratory accreditation and proficiency-testing requirements;
- Abamectin and Acephate pesticide limits;
- route-specific heavy-metal limits;
- Total THC reporting and potency/homogeneity requirements;
- a regulator-defined TIC reporting state for certain pesticide results;
- report-results-only microbial testing for specified adult-use unextracted products.

The current source is the OCM Cannabis Testing Limits revision dated February 9, 2026. New York's revision history makes it a strong candidate for future automated rule-change monitoring.


## Query layer

A first public query CLI now exists at `scripts/query_registry.py`.

It can filter by jurisdiction, analyte ID, requirement type, test category, and effective date, and can emit JSON. This is a proof-of-utility layer, not a hosted regulatory-compliance service.
