# Corpus v0.1 Analysis

Evidence-only analysis against frozen v0.1-alpha. Counts from `corpus/v0.1/build_stats.json`.

## Summary counts

- **TOTAL_CASES** = 50
- **SEED_CASES** = 3
- **NEW_PUBLIC_CASES** = 47
- **PRIMARY_SOURCE_CASES** = 40
- **SECONDARY_SOURCE_CASES** = 7
- **FULL_MAPPINGS** = 0
- **PARTIAL_MAPPINGS** = 50
- **FAILED_MAPPINGS** = 0
- **SOURCE_UNAVAILABLE** = 0
- **ACTUAL_FAIL_CASES** = 1
- **FAIL_CASE_IDS** = ['COA-046']

### Jurisdictions

- Connecticut
- Louisiana
- Massachusetts
- Missouri
- New Mexico
- New York
- Oregon
- Texas

### Laboratories

- ACT Laboratories (NY)
- ChemHistory
- Green Precision Analytics
- Kaycha Labs
- Lightscale Labs
- external-lab-001
- external-lab-002

### Producers / brands / clients

- 8th Avenue
- BakPak
- Desert Green Farm
- Grams Brooklyn
- Grön Chocolate
- Show-Me GP
- Texas Original

### Product types

- beverage
- concentrate
- concentrate/extract
- concentrate/vape
- edible
- flower
- flower/biomass
- infused pre-roll
- pre-roll
- tincture/liquid edible
- topical
- vape

## Occurrence counts

- **ND**: 46 / 50
- **below_limit**: 32 / 50
- **NOT_TESTED_OR_NOT_PERFORMED**: 21 / 50
- **NOT_REPORTED**: 16 / 50
- **multi_unit**: 43 / 50
- **sample_lifecycle**: 26 / 50
- **regulatory_tracking**: 30 / 50
- **water_activity**: 13 / 50
- **moisture**: 20 / 50
- **foreign_material**: 18 / 50
- **FAIL**: 1 / 50

## Gap statistics

| gap_key | cases | % | labs | jurisdictions | product_types | severity | existing_issue | evidence_class |
|---------|------:|--:|-----:|--------------:|--------------:|----------|----------------|----------------|
| `nd_not_representable` | 48 | 96.0 | 6 | 7 | 12 | CRITICAL_INTEROPERABILITY | 3 | CROSS_JURISDICTION |
| `multi_unit_cannabinoid` | 43 | 86.0 | 7 | 6 | 11 | CRITICAL_INTEROPERABILITY | 4 | CROSS_JURISDICTION |
| `below_reporting_limit_qualifier` | 35 | 70.0 | 7 | 6 | 8 | CRITICAL_INTEROPERABILITY | 1 | CROSS_JURISDICTION |
| `regulatory_tracking` | 30 | 60.0 | 5 | 3 | 8 | JURISDICTION_SPECIFIC | None | JURISDICTION_SPECIFIC |
| `sample_lifecycle_metadata` | 27 | 54.0 | 5 | 4 | 8 | IMPORTANT | None | CROSS_JURISDICTION |
| `analyte_level_not_performed` | 22 | 44.0 | 3 | 3 | 8 | CRITICAL_INTEROPERABILITY | 2 | CROSS_JURISDICTION |
| `foreign_material` | 22 | 44.0 | 5 | 4 | 6 | OPTIONAL | None | OPTIONAL_METADATA |
| `moisture_not_in_core` | 21 | 42.0 | 4 | 2 | 6 | OPTIONAL | None | OPTIONAL_METADATA |
| `not_reported` | 16 | 32.0 | 2 | 1 | 5 | IMPORTANT | None | CROSS_LAB |
| `water_activity_not_in_core` | 14 | 28.0 | 2 | 2 | 5 | OPTIONAL | None | OPTIONAL_METADATA |
| `batch_id_missing_placeholder` | 5 | 10.0 | 0 | 3 | 5 | PIPELINE_LIMITATION | None | PIPELINE_LIMITATIONS |
| `analyte_tables_unparsed` | 5 | 10.0 | 0 | 3 | 5 | PIPELINE_LIMITATION | None | PIPELINE_LIMITATIONS |
| `extended_cannabinoid_vocabulary` | 1 | 2.0 | 1 | 1 | 0 | IMPORTANT | None | SINGLE_CASE |
| `best_by_date` | 1 | 2.0 | 1 | 1 | 0 | OPTIONAL | None | OPTIONAL_METADATA |
| `literal_batch_id_zero` | 1 | 2.0 | 1 | 1 | 0 | IMPORTANT | None | SINGLE_CASE |
| `potency_spec_failure_not_native` | 1 | 2.0 | 1 | 1 | 1 | IMPORTANT | None | SINGLE_CASE |
| `homogeneity_not_in_core` | 1 | 2.0 | 1 | 1 | 1 | IMPORTANT | None | OPTIONAL_METADATA |
| `labeled_vs_measured_dosing` | 1 | 2.0 | 1 | 1 | 1 | IMPORTANT | None | SINGLE_CASE |

## Gap class rollup


### CROSS_JURISDICTION

- `nd_not_representable` — 48 cases (96.0%)
- `multi_unit_cannabinoid` — 43 cases (86.0%)
- `below_reporting_limit_qualifier` — 35 cases (70.0%)
- `sample_lifecycle_metadata` — 27 cases (54.0%)
- `analyte_level_not_performed` — 22 cases (44.0%)

### CROSS_LAB

- `not_reported` — 16 cases (32.0%)

### SINGLE_CASE

- `extended_cannabinoid_vocabulary` — 1 cases (2.0%)
- `literal_batch_id_zero` — 1 cases (2.0%)
- `potency_spec_failure_not_native` — 1 cases (2.0%)
- `labeled_vs_measured_dosing` — 1 cases (2.0%)

### OPTIONAL_METADATA

- `foreign_material` — 22 cases (44.0%)
- `moisture_not_in_core` — 21 cases (42.0%)
- `water_activity_not_in_core` — 14 cases (28.0%)
- `best_by_date` — 1 cases (2.0%)
- `homogeneity_not_in_core` — 1 cases (2.0%)

### JURISDICTION_SPECIFIC

- `regulatory_tracking` — 30 cases (60.0%)

### PIPELINE_LIMITATIONS

- `batch_id_missing_placeholder` — 5 cases (10.0%)
- `analyte_tables_unparsed` — 5 cases (10.0%)

## Classification legend

- **INTEROPERABILITY_GAPS**: recurring critical/important gaps with CROSS_*/REPEATED evidence (issues #1–#4 confirmed).
- **OPTIONAL_METADATA_GAPS**: moisture / water activity / foreign material / homogeneity metadata.
- **JURISDICTION_SPECIFIC_FIELDS**: METRC / regulatory tracking.
- **PIPELINE_LIMITATIONS**: unparsed analyte tables, source unavailable, unverified batch-id placeholders.

## Existing issues #1–#4 confirmation

- **Issue #1** (`below_reporting_limit_qualifier`): 35 cases (70.0%), labs=7, jurisdictions=6, evidence=CROSS_JURISDICTION
- **Issue #2** (`analyte_level_not_performed`): 22 cases (44.0%), labs=3, jurisdictions=3, evidence=CROSS_JURISDICTION
- **Issue #3** (`nd_not_representable`): 48 cases (96.0%), labs=6, jurisdictions=7, evidence=CROSS_JURISDICTION
- **Issue #4** (`multi_unit_cannabinoid`): 43 cases (86.0%), labs=7, jurisdictions=6, evidence=CROSS_JURISDICTION

## FAIL analysis

- **ACTUAL_FAIL_CASES** = 1
- **FAIL_CASE_IDS** = ['COA-046']
- **Limitation**: Only **one** FAIL case is present in this 50-case corpus (COA-046 Grön / Lightscale). Do not over-generalize FAIL coverage; contaminant FAIL vs potency-spec FAIL vs homogeneity FAIL must remain distinct.
- **COA-046**: overall_batch_failure=True, types=['potency_spec', 'homogeneity'], potency_spec_fail=True, homogeneity_fail=True, contaminant_safety_fail=False
- Potency-spec FAIL is **not** labeled as contaminant FAIL. v0.1-alpha has no native potency-spec failure field; evidence is in extensions + review gaps.
- Numeric contaminant detections that still PASS: not systematically quantified in this pass; `<` analyte rows never coerced to 0.
- Missing panels: omission or `not_tested` when source says NOT TESTED; never PASS.

