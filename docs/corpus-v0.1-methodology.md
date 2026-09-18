# Corpus v0.1 Methodology

## Objective
Build a 50-case public COA corpus testing WeedDAO Cultivation Record **v0.1-alpha** interoperability without modifying the frozen schema.

## Authoritative inputs
1. `corpus/v0.1/inputs/weeddao_verified_manifest_v0.1.json` — official verified case list (`verified_total_cases=50`).
2. `corpus/v0.1/inputs/weeddao_extracted_coa_data_v0.1.jsonl` — interoperability metadata.
3. Seed mappings in `review-data/coa-00{1,2,3}-weeddao-record.json`.

`replacement_case_ids` in the verified manifest are historical (already applied); this build does not re-replace sources.

## Freeze rules
- Do not modify the v0.1-alpha schema
- Expected SHA256: `31b0bdab4585954bebb9af1b06ac8b2d5a7b513ad1ca9694070836f1c723b5ee`
- Do not move git tag `v0.1-alpha`
- Do not design v0.2 schema here

## Fetch policy
- Fetch **only** the exact `source_url` from the verified manifest
- User-Agent: `WeedDAOCorpusBot/0.1 (+research)`
- Timeout ~35s
- OpenCOA: cookie `age_verified=1`
- TagLeaf: HTML scrape
- PDF hosts: download → `pdftotext -layout` → parse; **do not commit PDF binaries**
- On failure: `SOURCE_UNAVAILABLE` and continue (no replacement search)

## Mapping rules
- Required: `schema_version`, `record_id`, `cultivation_batch_id`, `created_at`
- `cultivation_batch_id`: batch_observed OR sample_observed OR deterministic `corpus-coa-NNN-unknown-batch`
- Detected numeric cannabinoids → CannabinoidMeasurement with unit ∈ {%, mg/g, mg/ml, mg/serving}; prefer `%` when multi-unit; alts in `extensions.weeddao_corpus`
- ND cannabinoids/terpenes: **omit**; gap (issue #3)
- `<LOQ`/`<LOD`/`<n`: **omit**; gap (issue #1)
- Panel PASS/FAIL/NOT_TESTED → `lab_results.safety.*.status`
- Mycotoxins panel status is first-class; moisture / water activity / foreign material → extensions + gaps
- `mapping_result`: FULL only if no important semantics dropped; else PARTIAL; FAILED if no valid record

## Limitations
- Best-effort parsers; some PDFs are layout-noisy
- Seed labs remain redacted (`external-lab-00x`)
- Corpus is WeedDAO-authored mappings, not external software adoption

## Pipeline
`corpus/v0.1/scripts/build_corpus.py`
