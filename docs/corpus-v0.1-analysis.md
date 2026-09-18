# Corpus v0.1 Analysis

Evidence-only analysis against frozen v0.1-alpha.

## Summary counts

- **TOTAL_CASES** = 50
- **SEED_CASES** = 3
- **NEW_PUBLIC_CASES** = 47
- **PRIMARY_SOURCE_CASES** = 37
- **SECONDARY_SOURCE_CASES** = 10
- **FULL_MAPPINGS** = 0
- **PARTIAL_MAPPINGS** = 50
- **FAILED_MAPPINGS** = 0
- **SOURCE_UNAVAILABLE** = 3

### Jurisdictions

- Connecticut
- Louisiana brand
- Louisiana brand / California lab
- Massachusetts
- Missouri
- New Mexico
- New York
- Texas
- Texas retail / Oregon laboratory

### Laboratories

- ACT Laboratories (NY)
- ChemHistory
- Green Precision Analytics
- Kaycha Labs
- external-lab-001
- external-lab-002

### Producers / brands / clients

- 8th Avenue
- 8th Avenue / ChemHistory
- BakPak
- Desert Green Farm
- Grams Brooklyn
- Grams Brooklyn / ACT Laboratories
- OpenCOA
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

- **ND**: 48 / 50
- **below_limit**: 32 / 50
- **NOT_TESTED_OR_NOT_PERFORMED**: 20 / 50
- **NOT_REPORTED**: 14 / 50
- **multi_unit**: 40 / 50
- **sample_lifecycle**: 24 / 50
- **regulatory_tracking**: 28 / 50
- **water_activity**: 11 / 50
- **moisture**: 19 / 50
- **foreign_material**: 19 / 50
- **FAIL**: 0 / 50

## Gap statistics

| gap_key | cases | % | labs | jurisdictions | product_types | severity | existing_issue | evidence_class |
|---------|------:|--:|-----:|--------------:|--------------:|----------|----------------|----------------|
| `nd_not_representable` | 48 | 96.0 | 5 | 8 | 12 | CRITICAL_INTEROPERABILITY | 3 | CROSS_JURISDICTION |
| `multi_unit_cannabinoid` | 40 | 80.0 | 6 | 7 | 11 | CRITICAL_INTEROPERABILITY | 4 | CROSS_JURISDICTION |
| `below_reporting_limit_qualifier` | 32 | 64.0 | 6 | 6 | 8 | CRITICAL_INTEROPERABILITY | 1 | CROSS_JURISDICTION |
| `regulatory_tracking` | 27 | 54.0 | 4 | 3 | 8 | JURISDICTION_SPECIFIC | None | CROSS_JURISDICTION |
| `sample_lifecycle_metadata` | 24 | 48.0 | 4 | 4 | 7 | IMPORTANT | None | CROSS_JURISDICTION |
| `analyte_level_not_performed` | 20 | 40.0 | 3 | 4 | 8 | CRITICAL_INTEROPERABILITY | 2 | CROSS_JURISDICTION |
| `foreign_material` | 20 | 40.0 | 5 | 4 | 6 | IMPORTANT | None | CROSS_JURISDICTION |
| `moisture_not_in_core` | 19 | 38.0 | 4 | 3 | 6 | OPTIONAL | None | CROSS_JURISDICTION |
| `not_reported` | 14 | 28.0 | 2 | 2 | 5 | IMPORTANT | None | CROSS_JURISDICTION |
| `water_activity_not_in_core` | 12 | 24.0 | 2 | 2 | 5 | OPTIONAL | None | CROSS_JURISDICTION |
| `batch_id_missing_placeholder` | 8 | 16.0 | 0 | 3 | 6 | IMPORTANT | None | CROSS_JURISDICTION |
| `analyte_tables_unparsed` | 5 | 10.0 | 0 | 3 | 5 | IMPORTANT | None | CROSS_JURISDICTION |
| `source_unavailable_or_unparsed` | 3 | 6.0 | 0 | 2 | 2 | IMPORTANT | None | CROSS_JURISDICTION |
| `extended_cannabinoid_vocabulary` | 1 | 2.0 | 1 | 1 | 1 | IMPORTANT | None | SINGLE_CASE |
| `best_by_date` | 1 | 2.0 | 1 | 1 | 1 | OPTIONAL | None | SINGLE_CASE |
| `literal_batch_id_zero` | 1 | 2.0 | 1 | 1 | 1 | IMPORTANT | None | SINGLE_CASE |

## Existing issues #1–#4 confirmation

- **Issue #1** (`below_reporting_limit_qualifier`): 32 cases (64.0%), labs=6, jurisdictions=6, evidence=CROSS_JURISDICTION
- **Issue #2** (`analyte_level_not_performed`): 20 cases (40.0%), labs=3, jurisdictions=4, evidence=CROSS_JURISDICTION
- **Issue #3** (`nd_not_representable`): 48 cases (96.0%), labs=5, jurisdictions=8, evidence=CROSS_JURISDICTION
- **Issue #4** (`multi_unit_cannabinoid`): 40 cases (80.0%), labs=6, jurisdictions=7, evidence=CROSS_JURISDICTION

## FAIL / numeric contaminant PASS / missing panels

- Actual FAIL overall_status rows: 0
- Numeric contaminant detections that still PASS: not systematically quantified; `<` analyte rows never coerced to 0.
- Missing panels: omission or `not_tested` when source says NOT PERFORMED/NOT TESTED; never PASS.

