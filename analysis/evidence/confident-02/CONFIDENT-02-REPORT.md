# CONFIDENT-02 — Confident LIMS → WeedDAO v0.2-draft Mapping Artifact

**Status:** COMPLETE. Evidence/mapping only. **No schema changes. No connector.**

**Baseline:** CONFIDENT-01 @ `f8bfa71` on `cannlytics-compat`. Schema: `schemas/weeddao-record-v0.2-draft.schema.json` unchanged.

## Counts

- **MAPPING_RECORDS** = 42
- **EXACT** = 18
- **PARTIAL** = 15
- **UNRESOLVED** = 5
- **NOT_APPLICABLE** = 4

## Classification note

CONFIDENT-01 `NOT_REPRESENTABLE` for ND / below-limit / multi-unit / not-run are recorded here as **UNRESOLVED** (no invented behavior). Size quantities and LIMS workflow fields remain **NOT_APPLICABLE** to core.

## Mapping records

See `confident-02-mapping.json` for full machine-readable records (M001–M042).

| ID | Concept | Classification | WeedDAO destination |
|---|---|---|---|
| M001 | sample.id | **PARTIAL** | `lab_results.sample.sample_id AND/OR external_identifiers[scheme=confident.sample_id]` |
| M002 | path sample_id aliases (public_key / lab_internal_id) | **EXACT** | `subject.external_identifiers[] / extensions` |
| M003 | regulator_sample_id | **EXACT** | `subject.external_identifiers[scheme=metrc.tag|biotrack.sample|other]` |
| M004 | regulator_batch_id | **EXACT** | `subject.external_identifiers[scheme=metrc.source|metrc.package|other]` |
| M005 | harvest_id | **PARTIAL** | `subject.external_identifiers[scheme=regulator.harvest|other]; may inform subject_type=harvest_lot` |
| M006 | batch_id (client IMS) | **PARTIAL** | `subject.subject_id (preferred when subject_type in product_batch|harvest_lot|cultivation_batch) AND/OR external_identifiers[scheme=producer.batch]` |
| M007 | lot_id | **EXACT** | `subject.external_identifiers[scheme=producer.lot]` |
| M008 | regulator_lot_id | **EXACT** | `subject.external_identifiers[scheme=metrc.package|other]` |
| M009 | production_run_id | **EXACT** | `subject.external_identifiers[scheme=producer.production_run]` |
| M010 | manifest_id | **EXACT** | `subject.external_identifiers[scheme=regulator.manifest]` |
| M011 | regulator_sample_id2 / regulator_batch_id2 (Leaf) | **EXACT** | `subject.external_identifiers[scheme=leaf.pre_transfer_batch|leaf.pre_transfer_lot]` |
| M012 | sample_name | **EXACT** | `subject.name` |
| M013 | strain_name | **EXACT** | `cultivar.reported_name` |
| M014 | sample_type_name | **PARTIAL** | `subject.product_type AND/OR subject.matrix` |
| M015 | sample_category_name / industry / classification / production_method | **PARTIAL** | `extensions.confident.* OR subject.matrix notes` |
| M016 | batch_size / lot_size / production_run_size (+ units) | **NOT_APPLICABLE** | `(none in core) → extensions.confident.sizes` |
| M017 | lab.name | **EXACT** | `lab_results.lab_name` |
| M018 | lab.id | **EXACT** | `lab_results.lab_id` |
| M019 | order_id / order_status / client_id | **NOT_APPLICABLE** | `extensions.confident.order (optional)` |
| M020 | test_packages / test_types | **PARTIAL** | `extensions.confident.test_packages|test_types; panels may align to safety.*` |
| M021 | date_samples_collected | **EXACT** | `lab_results.sample.collected_at` |
| M022 | production_date | **EXACT** | `lab_results.sample.produced_at` |
| M023 | lab_data.date_reported | **EXACT** | `lab_results.sample.reported_at` |
| M024 | categories.*.info_fields.date_tested | **PARTIAL** | `lab_results.tested_at (primary) AND/OR notes/extensions for multi-assay` |
| M025 | date_published / last_modified / lab_data.date_created | **PARTIAL** | `extensions.confident.timestamps OR record created_at/updated_at only if appropriate` |
| M026 | received_at | **NOT_APPLICABLE** | `lab_results.sample.received_at` |
| M027 | compounds[].name | **PARTIAL** | `lab_results.cannabinoids.<key> | terpenes[].name | safety.*.analytes[].name | cannabinoids.other[].name` |
| M028 | compounds[].value + report/input units (detected numeric) | **PARTIAL** | `AnalyteResult.result_state=detected + measurements[{value,unit}]` |
| M029 | secondary_report_units | **UNRESOLVED** | `extensions.confident.secondary_report_units OR second Measurement IF and only if a second numeric exists (not documented)` |
| M030 | compounds[].lod | **EXACT** | `AnalyteResult.limits[{type:LOD,value,unit}]` |
| M031 | compounds[].loq | **EXACT** | `AnalyteResult.limits[{type:LOQ,value,unit}]` |
| M032 | compounds[].limit (fail threshold) | **PARTIAL** | `AnalyteResult.limits[{type:action_limit|other,value,unit}]` |
| M033 | ND / Not Detected | **UNRESOLVED** | `AnalyteResult.result_state=not_detected (TARGET if clarified)` |
| M034 | below-LOQ / below-LOD state | **UNRESOLVED** | `AnalyteResult.result_state=below_reporting_limit (TARGET if clarified)` |
| M035 | concurrent multi-unit numeric per compound | **UNRESOLVED** | `measurements[] (multi) — TARGET if clarified` |
| M036 | ordered/required analyte not run | **UNRESOLVED** | `result_state=not_tested|not_performed OR omit — TARGET if clarified` |
| M037 | category info_fields.status 1/2/3 | **PARTIAL** | `lab_results.safety.<panel>.status OR analyte assessment` |
| M038 | lab_data.status overall | **PARTIAL** | `extensions.confident.lab_data_status OR outcomes if later defined` |
| M039 | info_fields.method | **EXACT** | `AnalyteResult.method and/or SafetyPanel.method / lab_results.method` |
| M040 | thc_total / cbd_total / cannabinoid_total / terpene_total + calculations | **PARTIAL** | `cannabinoids.total_thc|total_cbd|total_cannabinoids; total_terpenes; notes for formula` |
| M041 | compounds[].qualifiers / regulatornotes / rsd/rpd/stdev/spike | **NOT_APPLICABLE** | `extensions.confident.compound_qc OR notes` |
| M042 | coa / public_url / images | **PARTIAL** | `extensions.confident.coa_url|public_url (provenance links)` |

## Information disposition

### Preserved
- Regulator and client batch/lot/sample identifiers (as ExternalIdentifier)
- sample_name → subject.name; strain_name → cultivar.reported_name
- lab name/id
- collected_at, produced_at, reported_at
- Detected numeric compound values + report units
- LOD and LOQ numeric limits
- Assay method strings
- Panel pass/fail (status 1/2) when mapped to PanelStatus

### Transformed
- Confident compound_key → WeedDAO cannabinoid keys / NamedAnalyteResult names
- Status integers 1/2/3 → pass/fail/not_applicable
- Numeric strings → JSON numbers
- Timestamps → ISO-8601
- Totals + calculation formulas (formula → notes/extensions)
- Fail threshold limit → action_limit or other

### Intentionally Omitted
- Order/client workflow fields (order_id, order_status, client_id)
- Batch/lot/run sizes (no core destination)
- QC fields (rsd, rpd, stdev, spike, purity) from core
- Signatory / CoA presentation fields from core
- Invented ND / below-LOQ / multi-unit / not_performed analyte rows

### Unresolved
- ND / Not Detected (M033)
- below-LOQ / below-LOD distinct state (M034)
- Concurrent multi-unit numeric results (M029/M035)
- Ordered/required analyte not run (M036)

## Synthetic examples

| Example | File | Demonstrates |
|---|---|---|
| A | `examples/A-detected-numeric.json` | Straightforward detected numeric |
| B | `examples/B-lod-loq.json` | LOD + LOQ with detected (no below-LOQ invention) |
| C | `examples/C-panel-pass-fail.json` | Panel status 1/2/3 → pass/fail/not_applicable |
| D | `examples/D-identifiers-lifecycle.json` | IDs + collected/produced/tested/reported |
| E | `examples/E-unresolved-semantics.json` | Explicit UNRESOLVED markers; no invented ND/multi-unit/not_performed |

## Pending clarification matrix (Steve / Confident)

### Q1: ND / Not Detected and below LOQ/LOD representation
How should ND / Not Detected and below-LOQ / below-LOD appear on GET /v0/clients/sample/{id} lab_data.categories.*.compounds — omitted row, value 0, empty string, qualifier, distinct token, or other? How do value, lod, loq, and qualifiers interact?

Blocks: M033, M034. Status: `PENDING_STEVE`.

### Q2: secondary_report_units vs second numeric
When secondary_report_units is set, does GET ever return a second numeric for the same compound, or only a display conversion / category-level unit hint?

Blocks: M029, M035. Status: `PENDING_STEVE`.

### Q3: ordered/required analyte not run
For an ordered/required panel analyte that was not run, is omission the only signal, or can status/qualifiers (or another field) mark not tested / not performed?

Blocks: M036. Status: `PENDING_STEVE`.

## Gates

- **SCHEMA_CHANGE_REQUIRED** = NO
- **IMPLEMENTATION_RECOMMENDED** = NO
- **NEXT_ACTION** = Send Q1–Q3 to Steve; wait before CONFIDENT-03 / bridge work.

## Validation

All 5 synthetic examples validated OK against v0.2-draft schema via `scripts/validate_v0.2.py`. Schema unmodified.
