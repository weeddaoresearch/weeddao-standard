# Corpus v0.1 Methodology

## Objective
Build a 50-case public COA corpus testing WeedDAO Cultivation Record **v0.1-alpha** interoperability without modifying the frozen schema.

## Authoritative inputs
1. `corpus/v0.1/inputs/weeddao_verified_manifest_v0.1.json` — official verified case list (`verified_total_cases=50`).
2. `corpus/v0.1/inputs/weeddao_extracted_coa_data_v0.1.jsonl` — interoperability metadata.
3. Seed mappings in `review-data/coa-00{1,2,3}-weeddao-record.json`.
4. `corpus/v0.1/inputs/qa_replacements_v0.1.json` — QA replacements for COA-043/044/046.

## Freeze rules
- Do not modify the v0.1-alpha schema
- Expected SHA256: `31b0bdab4585954bebb9af1b06ac8b2d5a7b513ad1ca9694070836f1c723b5ee`
- Do not move git tag `v0.1-alpha`
- Do not design v0.2 schema here

## Fetch policy
- Fetch **only** the exact `source_url` (or QA-authorized replacement URLs)
- PDF hosts: download → `pdftotext -layout` → parse; **do not commit PDF binaries** (cache gitignored)
- On OpenCOA 429: QA replaced three slots with authorized primary PDFs (Grams/ACT ×2, Grön/Lightscale FAIL)

## Mapping rules
- Required: `schema_version`, `record_id`, `cultivation_batch_id`, `created_at`
- Detected numeric cannabinoids → CannabinoidMeasurement with unit ∈ {%, mg/g, mg/ml, mg/serving}; prefer `%` when multi-unit; alts + labeled targets in `extensions.weeddao_corpus`
- ND cannabinoids/terpenes: **omit**; gap (issue #3)
- `<LOQ`/`<LOD`/`<n`: **omit**; gap (issue #1)
- Panel PASS/FAIL/NOT_TESTED → `lab_results.safety.*.status` when native; never invent PASS
- Potency-spec / homogeneity FAIL: **not** mapped as contaminant safety FAIL; document in extensions + review gaps
- Taxonomy: `producer_or_brand` is never OpenCOA/lab composite; `jurisdiction` is never a cross-state composite string

## Gap classes used in analysis
- **INTEROPERABILITY_GAPS** — semantics v0.1-alpha cannot represent (issues #1–#4 and related)
- **OPTIONAL_METADATA_GAPS** — moisture, water activity, foreign material, etc.
- **JURISDICTION_SPECIFIC_FIELDS** — METRC / regulatory tracking
- **PIPELINE_LIMITATIONS** — fetch/parse/QA limits (`analyte_tables_unparsed`, `source_unavailable_or_unparsed`, unverified `batch_id_missing_placeholder`)

## Canonical counts
All summary numbers are emitted by `corpus/v0.1/scripts/recompute_stats.py` → `build_stats.json`. Docs must not hand-copy conflicting figures.
