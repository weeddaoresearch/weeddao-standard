# Cannlytics → WeedDAO evidence triage

**Branch:** `cannlytics-compat` @ `57b6a2b`  
**Target schema:** WeedDAO Cannabis Data Record `0.2-draft` (**unchanged** by this triage)  
**Authority:** Existing completed real-data + semantic audit only — no re-fetch, no PDF download, no schema edit, no merge, no tag/release.  
**Machine companion:** [evidence-triage.json](evidence-triage.json)

This document classifies Cannlytics compatibility **evidence for post-review decisions**. It does not redesign the bridge and does not alter historical totals in [REAL_DATA_AUDIT.json](REAL_DATA_AUDIT.json).

---

## 1. Locked audit totals (authoritative)

| Metric | Value |
|--------|------:|
| RECORDS_AUDITED | 2000 |
| VALID (STRUCTURALLY_VALID_OUTPUTS) | 1250 |
| UNMAPPABLE (STRUCTURALLY_UNMAPPABLE) | 750 |
| LOSSLESS_FOR_AVAILABLE_SEMANTICS | 35 (2.8% of mappable) |
| SEMANTICALLY_PARTIAL | 1215 |
| SUBJECT_TYPE_DETERMINATE / AMBIGUOUS | 642 / 608 |
| ND_EXPLICIT / ND_UNRECOVERABLE | 34421 / 999 |
| BELOW_LIMIT_EXPLICIT / STATE_AMBIGUOUS | 5165 / 0 |
| NT_AMBIGUOUS / PANEL_NT_AMBIGUOUS | 2 / 0 |
| MULTI_UNIT source / preserved | 129 / 129 |
| LOD_PRESENT / LOD_PRESERVED | 42370 / 554 |
| LOQ_PRESENT / LOQ_PRESERVED | 47375 / 425 |
| GENERIC_LIMIT_PRESENT / LIMIT_TYPE_AMBIGUOUS | 0 / 272 |
| TRACEABILITY present / core-mapped | 197 / 197 |
| EXTENSION_USAGE_RECORDS | 1250 |
| States | CA, FL, HI, MA, MD, MI, NV, NY (8) |
| Schema validation failures | 0 |

Denominator for `percent_of_mappable_records` below: **1250**, unless a finding is about the unmappable set (then of 2000).

---

## 2. LOD / LOQ metrics reconciliation (docs only)

**Do not treat `LOD_PRESERVED / LOD_PRESENT` (or the LOQ pair) as a preservation rate.** The numerators and denominators measure different things.

| Metric | What it counts |
|--------|----------------|
| `LOD_PRESENT` = 42370 | Source **analyte / cell-level** LOD occurrences in nested Cannlytics `results[]` across the audited corpus |
| `LOD_PRESERVED` = 554 | WeedDAO **`limits[]` Limit objects** with `type: LOD` emitted into **valid** bridge outputs |
| `LOQ_PRESENT` = 47375 | Same as LOD_PRESENT, for LOQ |
| `LOQ_PRESERVED` = 425 | WeedDAO `limits[]` Limit objects with `type: LOQ` |

**Interpretation best-supported by bridge code** (`bridges/cannlytics_to_weeddao.py`): for each mapped `ResultDetail`, if `lod` / `loq` parse as floats, the bridge **appends** `{"type":"LOD"|"LOQ", ...}` onto that analyte’s `limits` array. Therefore:

> **PRESERVED ≈ count of LOD/LOQ Limit objects emitted into valid outputs**  
> (not “records that had any LOD”, and not a fraction of PRESENT).

PRESENT aggregates source cells (including details that may not become WeedDAO analytes, and including rows in the broader audit pass). Units differ by design. **REAL_DATA_AUDIT.json numbers are left unchanged**; this section is the reconciliation note only.

---

## 3. The 750 structurally unmappable records

**UNMAPPABLE_PRIMARY_REASON = `SOURCE_IDENTITY_INSUFFICIENT`**

The bridge’s **only** structural failure gate is:

```text
subject_id = batch_number OR sample_id OR id
if none → STRUCTURALLY_UNMAPPABLE
```

All three candidates missing → no WeedDAO record. Exact sub-counts (“missing batch only”, “has sample_id but …”, etc.) are **UNAVAILABLE without re-fetch**. Do **not** weaken identity requirements to inflate the valid count.

---

## 4. Loss attribution (partials vs lossless)

- **35 / 1250 = 2.8%** `LOSSLESS_FOR_AVAILABLE_SEMANTICS` — every semantic distinction **present in the Cannlytics normalized record** was represented **without guessing** (not “original COA PDF was lossless”).
- **1215 / 1250** `SEMANTICALLY_PARTIAL` — mapped with documented ambiguity flags.

Attribute buckets below **may overlap**. Documented overlaps: `ND_UNRECOVERABLE` (999) and `SUBJECT_TYPE_AMBIGUOUS` (608) frequently co-occur on partials; `LIMIT_TYPE_AMBIGUOUS` (272) may co-occur with either. The **750** unmappable are **disjoint** from the 1250 mappable set. `flower→other` (608) is the **same population** as `SUBJECT_TYPE_AMBIGUOUS`.

### 4.1 LOSS_BY_SOURCE_NORMALIZATION

| Signal | records_affected (known) |
|--------|-------------------------:|
| ND_UNRECOVERABLE (null≠ND) | 999 |
| SUBJECT_TYPE_AMBIGUOUS | 608 |
| LIMIT_TYPE_AMBIGUOUS | 272 |
| NT_AMBIGUOUS | 2 |
| PANEL_NT_AMBIGUOUS | 0 |
| STRUCTURALLY_UNMAPPABLE (identity) | 750 (of 2000) |
| Status-only safety panels | ESTIMATED (exact UNAVAILABLE) |

These are **not** WeedDAO schema defects. Where WeedDAO can already say `other` / `sample` / `unknown` / `limits[type=other]` honestly, source insufficiency stays **SOURCE_LOSS**.

### 4.2 LOSS_BY_WEEDDAO_CORE (ESTIMATED)

Fields present in Cannlytics (see `WEEDDAO_GAPS_SAMPLE`) that land only in `extensions.cannlytics_source_fields` (or `NO_EQUIVALENT`) because v0.2-draft has no appropriate core slot — **exact per-field presence counts UNAVAILABLE without re-audit**:

| Field / block | Notes |
|---------------|-------|
| distributor / license / address | Commercial chain; OPTIONAL_METADATA |
| date_packaged | Lifecycle enrichment; do not assume CORE |
| serving_size / servings_per_package / product_size | Dosing-relevant **if** present; edible-skewed product types in audit tops; prevalence unproven → not auto-CORE |
| classification / indica% / sativa% | Analytics → OUT_OF_SCOPE |
| lab_license_number / lab_address | Facility enrichment |
| coa_url / coa_urls / coa_pdf / lab_results_url | SOURCE_METADATA |

### 4.3 LOSS_BY_BRIDGE_POLICY

| Policy | Effect |
|--------|--------|
| `date_expires` **not** mapped to `lab_results.best_by` | OMIT + extension stash (`equivalence_to_best_by_unsupported`) |
| Panel `nt` | Omit WeedDAO `safety.*.status`; preserve under `panel_nt_preserved` (0 hits in this sample) |
| Flowerish without lot metadata | `subject_type=other`, **never** auto `cultivation_batch` (608) |
| Null top-level floats | Omit; never `0` or ND (999) |
| Generic `ResultDetail.limit` | `limits[{type:other}]` (272) |

---

## 5. Finding evaluations (minimum set)

Categories: `CORE_CANDIDATE` | `OPTIONAL_METADATA` | `SOURCE_LOSS` | `BRIDGE_ONLY` | `OUT_OF_SCOPE`.

**CORE_CANDIDATE bar (strict):** multi-state meaningful occurrence **AND** losing it harms interop / traceability / safety / dosing / lifecycle **AND** extension-only materially reduces interchange usefulness.  
After scrutiny: **no finding cleared this bar for a pre-release schema patch.** Distributor, `date_packaged`, and serving/package were deliberately **not** assumed CORE.

### 5.1 Distributor block — OPTIONAL_METADATA · DEFER · MEDIUM

Present in gaps sample; extension-only. Commercial metadata, not METRC identity. Multi-state usefulness plausible but not required for v0.2 lab-result core. `schema_change_recommended_after_external_review=true`.

### 5.2 date_packaged — OPTIONAL_METADATA · DEFER · MEDIUM

Useful lifecycle enrichment; not proven necessary for release interchange. Do not assume CORE.

### 5.3 date_expires vs best_by — BRIDGE_ONLY · DEFER · MEDIUM

Bridge correctly refuses unsupported equivalence. Decide post-review whether WeedDAO needs a distinct expires concept — **do not silently alias**.

### 5.4 classification / indica% / sativa% — OUT_OF_SCOPE · NO_SCHEMA_ACTION · LOW

Analytics / marketing genetics proxies. Field-map `NO_EQUIVALENT`. Never used for `cultivar.*`.

### 5.5 Panel `nt` collapse — SOURCE_LOSS · NO_SCHEMA_ACTION · LOW

Cannlytics `normalize_status` collapse is upstream. WeedDAO can represent `not_tested` / `not_applicable` when source distinguishes them. **PANEL_NT_AMBIGUOUS=0** in this sample.

### 5.6 Analyte `nt` — SOURCE_LOSS · NO_SCHEMA_ACTION · LOW

**NT_AMBIGUOUS=2** (0.16% of mappable). `result_state=unknown` + `reported_as=nt`; never `not_tested`.

### 5.7 Null float ND ambiguity — SOURCE_LOSS · NO_SCHEMA_ACTION · HIGH (awareness)

**ND_UNRECOVERABLE=999** (79.92% of mappable). Null ≠ ND ≠ not tested. Priority is **data-quality awareness**, not a schema patch.

### 5.8 Generic ResultDetail.limit — SOURCE_LOSS · NO_SCHEMA_ACTION · MEDIUM

**LIMIT_TYPE_AMBIGUOUS=272** (21.76%). WeedDAO already has typed limits; source underspecifies.

### 5.9 Status-only safety panels — SOURCE_LOSS · NO_SCHEMA_ACTION · MEDIUM

Pass/fail without analyte ResultDetail is honest but incomplete. Exact status-only counts UNAVAILABLE; panels appear in gaps sample.

### 5.10 Subject type ambiguity — SOURCE_LOSS · NO_SCHEMA_ACTION · HIGH (awareness)

**608** (48.64%) flowerish → `other`. WeedDAO can represent `other`/`sample` honestly; guessing `cultivation_batch` would be a defect.

### 5.11 COA URL / source metadata — OPTIONAL_METADATA · DEFER · LOW

Provenance pointers; extension-sufficient for v0.2.

### 5.12 serving_size / servings_per_package / product_size — OPTIONAL_METADATA · DEFER · MEDIUM

Dosing-relevant **when present**, but edible-ish types are a small slice of the 2000-row tops and exact field presence is UNAVAILABLE. **Not** promoted to CORE_CANDIDATE without prevalence proof.

### 5.13 Lab license / address — OPTIONAL_METADATA · DEFER · LOW

Lab name/id core-mapped; facility license/address extension.

### 5.14 Traceability — BRIDGE_ONLY (freeform) / success (METRC) · NO_SCHEMA_ACTION · LOW

**197/197** structured METRC → core `ExternalIdentifier`. Freeform `traceability_ids` stay extension + structure-ambiguous when present. Do not invent schemes.

### Positive controls (no action)

- **MULTI_UNIT 129/129** preserved  
- **BELOW_LIMIT_EXPLICIT=5165**, **BELOW_LIMIT_STATE_AMBIGUOUS=0**  
- **EXTENSION_USAGE=1250** (expected bridge provenance)  
- **0** schema validation failures on valid outputs  

---

## 6. Final disposition buckets

### PATCH_BEFORE_V0_2_RELEASE

*(empty)*

No schema edit is justified from this evidence before v0.2 release. Conservatively empty by design.

### DEFER_TO_POST_V0_2

Pending independent external review (no CORE auto-promotion):

1. distributor block  
2. date_packaged  
3. date_expires vs distinct expires / best_by decision  
4. COA URL / source document metadata  
5. serving_size / servings_per_package / product_size  
6. lab license / address  

### NO_SCHEMA_ACTION

All **SOURCE_LOSS**, **OUT_OF_SCOPE**, success controls, METRC core success, LOD/LOQ metric reconciliation, identity gate, panel/analyte `nt` handling, null-float policy, generic limit typing, status-only panels, subject_type conservatism, universal extension provenance.

---

## 7. What this triage explicitly does *not* do

- Change v0.2 schema or `v0.2-draft` branch  
- Merge, tag, or release  
- Fetch more Cannlytics records or download PDFs  
- Redesign the bridge  
- Alter historical raw values in `REAL_DATA_AUDIT.json`  
- Weaken `subject_id` identity requirements  

---

## 8. Sources

- [REAL_DATA_AUDIT.json](REAL_DATA_AUDIT.json) / [REAL_DATA_AUDIT.md](REAL_DATA_AUDIT.md)  
- [SEMANTIC_AUDIT.md](SEMANTIC_AUDIT.md)  
- [field-map.json](field-map.json)  
- [semantic-rules.json](semantic-rules.json)  
- [README.md](README.md)  
- `bridges/cannlytics_to_weeddao.py` (subject_id gate; LOD/LOQ limits append; extension stash; date_expires omit)  
