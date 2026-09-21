# CONFIDENT-01 — Confident LIMS GET Sample × WeedDAO v0.2-draft
**Status:** evidence crosswalk only. **No WeedDAO schema changes.**
**Retrieved:** 2026-09-21T19:51:34Z
## Sources
- `official_docs_base`: https://api.confidentcannabis.com/v0/docs/
- `clients_get_sample`: https://api.confidentcannabis.com/v0/docs/clients/get-sample-details.md
- `labs_get_sample`: https://api.confidentcannabis.com/v0/docs/labs/get-sample-details.md
- `post_test_results`: https://api.confidentcannabis.com/v0/docs/labs/post-sample-test-results.md
- `compounds`: https://api.confidentcannabis.com/v0/docs/get-compound.md
- `order_lifecycle`: https://api.confidentcannabis.com/v0/docs/order-lifecycle.md
- `api_version_note`: v0 API under active development; docs indexed as v0.16.0 via llms.txt
- `weeddao_schema`: schemas/weeddao-record-v0.2-draft.schema.json
- `weeddao_branch_ref`: v0.2-draft @ ff294e7 (schema not modified by this task)

## Endpoint focus
Primary: `GET /v0/clients/sample/{sample_id}` (client/third-party authorized retrieval; matches Confident’s recommendation to WeedDAO).
Supporting: `POST /v0/labs/sample/{sample_id}/test_results` (defines compound object + status enum), `GET /v0/compounds`, order lifecycle (draft vs published).

## Classification counts
- Fields/concepts reviewed: **42**
- EXACT: **14**
- PARTIAL: **19**
- NOT_REPRESENTABLE: **4**
- NOT_APPLICABLE: **5**

## Field-level crosswalk
| Confident concept | WeedDAO v0.2-draft | Class | Notes |
|---|---|---|---|
| `sample.id` | `record_id and/or lab_results.sample.sample_id / ExternalIdentifier` | **PARTIAL** | Confident sample ID is Confident-scoped; map as record_id or lab.sample identifier, not cultivation_batch_id. |
| `sample public key / path sample_id aliases` | `ExternalIdentifier (scheme open)` | **EXACT** | Can carry confident.public_key / lab_internal_id as identifiers. |
| `regulator_sample_id` | `subject.external_identifiers / lab_results identifiers (e.g. metrc.tag)` | **EXACT** | Open ExternalIdentifier schemes fit Metrc/BioTrack/Leaf IDs. |
| `regulator_batch_id` | `subject.external_identifiers (e.g. metrc.source/package)` | **EXACT** |  |
| `harvest_id` | `subject.external_identifiers; may inform subject_type=harvest_lot` | **PARTIAL** | ID maps; subject_type inference still requires product/matrix context. |
| `batch_id (client IMS)` | `subject.subject_id (when product_batch/harvest_lot)` | **PARTIAL** | Good subject_id candidate; not always cultivation batch. |
| `lot_id / regulator_lot_id / production_run_id / manifest_id` | `ExternalIdentifier extensions` | **EXACT** | Preserve as identifiers; core subject has one subject_id. |
| `regulator_sample_id2 / regulator_batch_id2 (Leaf pre-transfer)` | `ExternalIdentifier` | **EXACT** | Jurisdiction-specific; open scheme strings. |
| `sample_name` | `subject.name` | **EXACT** | Do not put into cultivar. |
| `strain_name` | `cultivar.reported_name` | **EXACT** | Genetics only when present. |
| `sample_type_name / category / industry / classification / production_method` | `subject.product_type / matrix; classification→OUT_OF_SCOPE or extension` | **PARTIAL** | Type/category/matrix map loosely; Hybrid classification is analytics/metadata, not core genetics verification. |
| `batch_size / lot_size / production_run_size (+ units)` | `no dedicated core quantity fields` | **NOT_REPRESENTABLE** | Optional extension only in v0.2-draft; not required for interop of results. |
| `units_per_serving / servings_per_container / unit_description / container_description` | `measurement.basis / basis_quantity; sample/category info_fields overlap` | **PARTIAL** | Serving/unit basis can be expressed on measurements; container marketing text is optional metadata. |
| `lab.id / lab.name` | `lab_results.lab_id / lab_name` | **EXACT** |  |
| `order_id / order_status_* / client_id` | `extensions / optional notes` | **NOT_APPLICABLE** | LIMS workflow state, not cannabis record core. |
| `test_packages / test_types` | `lab_results notes / extensions; panels via safety categories` | **PARTIAL** | Package catalog is Confident commercial; test_types align roughly to panel categories. |
| `has_coa / coa / coa_additions / images / public_url` | `extensions / provenance links` | **PARTIAL** | URLs expire for some file links; public_url is useful provenance, not core analyte semantics. |
| `date_samples_collected` | `lab_results.sample.collected_at` | **EXACT** |  |
| `production_date` | `lab_results.sample.produced_at` | **EXACT** |  |
| `lab_data.date_reported` | `lab_results.sample.reported_at` | **EXACT** | Confident: COA/data upload/report time. |
| `categories.*.info_fields.date_tested` | `lab_results.tested_at and/or per-panel notes` | **PARTIAL** | WeedDAO has one primary tested_at; multi-assay dates need notes/extensions or repeated panel metadata. |
| `date_published / last_modified / lab_data.date_created` | `created_at/updated_at or extensions` | **PARTIAL** | Platform timestamps ≠ sample lifecycle events; do not conflate with collected/tested/reported. |
| `received_at` | `lab_results.sample.received_at` | **NOT_APPLICABLE** | Not observed as a first-class field on clients GET Sample docs reviewed. |
| `compounds[].name (compound_key) + GET /compounds synonyms` | `cannabinoid keys / terpenes[].name / NamedAnalyteResult; alias via registry later` | **PARTIAL** | Stable Confident keys exist; not WeedDAO analyte IDs. Synonym list helps mapping. |
| `compounds[].value (string numeric) + category report/input units` | `AnalyteResult.result_state=detected + measurements[]` | **PARTIAL** | Numeric detected maps cleanly. Docs require name+value; ND representation not documented as a distinct non-numeric state on GET Sample. |
| `input_units / report_units / secondary_report_units / unit_weight / ml_weight` | `measurements[].unit + basis/basis_quantity` | **PARTIAL** | Category-level dual display units ≠ concurrent per-analyte multi-unit measurements. GET docs say most compound values converted to report unit. |
| `concurrent % and mg/g (or mg/serving) on same analyte in one payload` | `measurements[] multi-unit` | **NOT_REPRESENTABLE** | Public GET Sample shape exposes one compound value (in report units) plus category secondary_report_units—not a second numeric per compound in the documented GET schema. |
| `compounds[].lod` | `limits[{type:LOD}]` | **EXACT** | When present and numeric. |
| `compounds[].loq` | `limits[{type:LOQ}]` | **EXACT** |  |
| `compounds[].limit` | `limits[{type:action_limit|regulatory_limit|other}]` | **PARTIAL** | Confident: fail threshold. WeedDAO should prefer action_limit/regulatory_limit when known; else other + ambiguity flag—same pattern as Cannlytics generic limit. |
| `compounds[].max / limitrangelow / limitrangehigh` | `limits[] other / extensions` | **PARTIAL** | Range/ULOQ semantics not first-class named limit types in WeedDAO beyond other. |
| `compounds[].qualifiers` | `reported_as / notes` | **PARTIAL** | Free-text regulator qualifiers; may encode ND/<LOQ if used—needs Confident clarification. |
| `compounds[].rsd/rpd/stdev/spike/purity_percent/regulatornotes` | `extensions / notes` | **NOT_APPLICABLE** | QC/regulatory posting metadata; not core interchange for WeedDAO v0.2-draft. |
| `ND / not detected as distinct semantic` | `result_state=not_detected` | **NOT_REPRESENTABLE** | Official POST docs: never include compounds not tested; value required as numeric string. No documented ND token on compound.value in reviewed pages. Risk: ND collapsed to omission or zero in practice—ASK Confident. |
| `below LOQ / <LOQ as distinct semantic` | `result_state=below_reporting_limit + limits` | **NOT_REPRESENTABLE** | Not documented as a compound value mode in public GET/POST sample docs reviewed. loq field can exist alongside a numeric value without stating below-LOQ. |
| `not tested (omit compound)` | `result_state=not_tested OR omit analyte` | **PARTIAL** | Confident instructs omit untested compounds. WeedDAO can omit or use not_tested; omission loses explicit 'was in scope but not tested' vs 'not in panel'. |
| `not_performed as distinct from not_tested` | `result_state=not_performed` | **NOT_APPLICABLE** | Not present in Confident GET Sample docs reviewed. |
| `category info_fields.status 1/2/3` | `safety.*.status pass/fail; assessment; completed→not_applicable-ish` | **PARTIAL** | 1=passed,2=failed,3=completed (no pass/fail limits). Maps to panel status; completed≠not_tested. |
| `lab_data.status 1/2/3 overall` | `outcomes / extensions` | **PARTIAL** | Overall sample pass/fail/completed; WeedDAO should not invent panel fails from overall alone. |
| `thc_total / cbd_total / cannabinoid_total / terpene_total + *_calculation` | `total_thc / total_cbd / total_cannabinoids / total_terpenes + notes` | **PARTIAL** | Totals map; calculation formula strings are presentation/provenance—keep in notes/extensions. |
| `info_fields.method` | `AnalyteResult.method or panel notes` | **EXACT** | String method eg HPLC. |
| `signatory_name / title / footnotes / wet_weight / dry_weight` | `extensions / notes` | **NOT_APPLICABLE** | CoA presentation/QC aliquot metadata. |

## Semantic loss risks
- ND / not-detected may be invisible in GET Sample if Confident only stores numeric values and omits ND analytes—or stores 0—docs do not define an ND value token.
- Below-LOQ may be indistinguishable from a low detected value unless qualifiers encode it.
- Not-tested is omission-only; cannot distinguish 'panel not ordered' vs 'analyte not run' without test_packages/test_types context.
- Multi-unit: secondary_report_units is category-level; GET payload does not document dual numeric measurements per compound.
- Per-assay date_tested collapses awkwardly into a single lab_results.tested_at.
- Generic compound.limit fail-threshold type is under-specified relative to WeedDAO action vs regulatory vs reporting limits.

## Top gaps (meaningful, not manufactured)
- Undocumented ND / below-limit compound value semantics on public API
- No concurrent multi-measurement array per analyte on GET Sample
- Omission-based not-tested loses explicit analyte-level NOT_PERFORMED/NOT_TESTED distinction
- Batch/lot/run size quantities not in WeedDAO v0.2 core (optional—not blocking results interop)

## Questions for Steve (Confident LIMS)
1. How should ND / Not Detected appear on GET /v0/clients/sample/{id} lab_data.categories.*.compounds—omitted row, value 0, empty string, qualifier, or other?
2. How should below-LOQ / <LOQ / <LOD appear relative to compounds[].value, loq, lod, and qualifiers?
3. When secondary_report_units is set, does GET ever return a second numeric for the same compound, or only a display conversion client-side?
4. For a required panel analyte that was not run, is omission the only signal, or can status/qualifiers mark not tested / not performed?
5. Is compounds[].limit always an action/fail threshold, or can it mean reporting limit in some categories/states?
6. Are draft (unpublished) results ever visible to authorized third-party client API keys, or only published lab_data?

## Recommendation
Treat Confident GET Sample as a strong structured source for identity, Metrc IDs, lifecycle dates, panel pass/fail, LOD/LOQ numerics, and detected values. Do not change WeedDAO v0.2-draft yet—ask Steve the ND/below-limit/multi-unit questions first. Prefer mapping detected+limits+panel status with existing AnalyteResult; park sizes/signatories/Metrc-specific info_fields in extensions.

## Schema change recommended?
**NO** — pending answers on ND / below-limit / multi-unit representation in the live GET payload.
