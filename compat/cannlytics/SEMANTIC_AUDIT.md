# Cannlytics → WeedDAO semantic audit

Upstream: `cannlytics/cannabis_results` @ `a4e05a9f7367ac0b1637bd84773875b3bd1453ec` (`config/results_schema.py`).

WeedDAO target: `schemas/weeddao-record-v0.2-draft.schema.json` (**unchanged** by this bridge).

Legend for each finding: **LOSSY** | **UNMAPPABLE** | **REQUIRES_EXTENSION** | **AMBIGUOUS** | **DEFECT (documented, not schema-changed)**.

---

## 1. Status / `nt` ambiguity — DEFECT

Cannlytics `normalize_status` collapses:

`not tested`, `n/t`, `not applicable`, `n/a`, `na`, `-`, `''` → **`nt`**

| Direction | Bridge behavior |
|-----------|-----------------|
| `nt` → WeedDAO `not_tested` | **FORBIDDEN** |
| Analyte `nt` (no raw “Not Tested” text) | `result_state=unknown`, `reported_as="nt"`, flag `AMBIGUOUS_NT` |
| Panel `*_status=nt` | **Omit** WeedDAO `safety.*.status`; preserve under `extensions.cannlytics_bridge.panel_nt_preserved`; flag `PANEL_NT_AMBIGUOUS` |
| Raw value/status `"Not Tested"` | May map to `not_tested` |
| Raw `"Not Applicable"` | May map to `not_applicable` |

**Classification:** LOSSY + AMBIGUOUS + DEFECT (documented in compat only; WeedDAO schema not altered).

---

## 2. Null cannabinoid / terpene floats — DEFECT

Top-level `Optional[float]` fields (`delta_9_thc`, `thca`, `cbd`, …) use `None` for three distinct realities in source COAs: missing, ND, not tested.

| Anti-pattern | Bridge |
|--------------|--------|
| null → `0` | **FORBIDDEN** |
| null → `not_detected` / ND | **FORBIDDEN** |
| null present in normalized record | Omit field; flag `ND_UNRECOVERABLE` |

**Classification:** LOSSY + AMBIGUOUS + DEFECT.

---

## 3. Subject model mismatches

| Cannlytics | WeedDAO | Notes |
|------------|---------|-------|
| `product_name` | `subject.name` | **Never** `cultivar.*` |
| `strain_name` | `cultivar.reported_name` | Only when present; `identity_status=reported` |
| `product_type` finished (vape/edible/…) | `subject_type=product_batch` | Determinate |
| `product_type` flower/bud/biomass | `other` (+ `SUBJECT_TYPE_AMBIGUOUS`) unless harvest/lot metadata → `harvest_lot` | **Never** auto `cultivation_batch` |
| sample-only identity | `subject_type=sample` | |
| no `batch_number`/`sample_id`/`id` | STRUCTURALLY_UNMAPPABLE | |

**Classification:** LOSSY (subject_type) when flowerish without lot metadata.

---

## 4. ResultDetail semantics

| Source | WeedDAO | Flags |
|--------|---------|-------|
| numeric `value` | `detected` + measurement | |
| `mg_g` + `value` | second measurement unit `mg/g` | `MULTI_UNIT_PRESERVED` |
| `lod` / `loq` | `limits` LOD / LOQ | |
| generic `limit` | `limits[{type:other}]` | `LIMIT_TYPE_AMBIGUOUS` |
| status pass/fail | `assessment` only | must **not** auto-set `result_state` |
| explicit `ND` | `not_detected` | |
| explicit `<LOQ` / `<LOD` | `below_reporting_limit` | |
| LOQ/LOD present, value null, no qualifier | `unknown` + limits | `BELOW_LIMIT_STATE_AMBIGUOUS` — do **not** infer below_limit |
| `nt` | `unknown` + `reported_as=nt` | `AMBIGUOUS_NT` |

**Classification:** AMBIGUOUS / LOSSY for nt, generic limit, LOQ-without-qualifier.

---

## 5. Panel status without analytes — LOSSY

Cannlytics often stores only `pesticides_status=pass` with empty `results[]` for that panel. WeedDAO can record `safety.pesticides.status=pass` with `analytes` omitted. This is **status-only** evidence — not analyte-level ResultDetail.

When `nt`, panel status is omitted entirely (see §1).

---

## 6. Multi-unit — preserved when source has both

If ResultDetail has both `value` (with units, typically `%`) and `mg_g`, both measurements are emitted → `MULTI_UNIT_PRESERVED`.

Top-level LabResult floats are **percent-only** in schema comments; mg/g requires `results[]`.

---

## 7. Traceability

| Field | Mapping |
|-------|---------|
| `metrc_lab_id` | `ExternalIdentifier` scheme `metrc.lab` |
| `metrc_source_id` | `metrc.source` |
| `metrc_ids[]` | `metrc.tag` |
| `traceability_ids` | extension + `TRACEABILITY_STRUCTURE_AMBIGUOUS` |

---

## 8. Dates / best_by

Lifecycle dates map 1:1 when present. **No** `reported_at` is manufactured. `date_expires` is **not** mapped to `lab_results.best_by` (equivalence unsupported) → OMIT + gap.

---

## 9. Fields REQUIRES_EXTENSION / UNMAPPABLE in core

Distributor block, COA URL/PDF paths, product_size/serving_size, classification/indica%/sativa%, lab street address — stored under `extensions.cannlytics_source_fields` (REQUIRES_EXTENSION / SOURCE_METADATA). Not forced into core.

---

## 10. Provenance

`extensions.cannlytics_bridge` = `{upstream_project, upstream_record_id, upstream_source, upstream_schema_commit, bridge_version, panel_nt_preserved, flags}`.

Analyte `provenance` is `derived` (bridge), **not** claimed `laboratory_verified` unless separately indicated.

---

## Explicit LOSSLESS definition

`LOSSLESS_FOR_AVAILABLE_SEMANTICS` means: every semantic distinction **present in the Cannlytics normalized record** was represented in WeedDAO **without guessing**.

It does **not** mean the original COA PDF was captured losslessly by Cannlytics.
