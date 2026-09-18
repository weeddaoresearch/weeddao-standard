# COA-002 — Evidence-backed schema gaps (v0.1-alpha)

**Schema:** WeedDAO Cultivation Record **0.1-alpha** (FROZEN — not modified by this review)  
**Case:** Real-world Texas Original medical vaporization oil COA mapping  
**Principle:** Document only gaps demonstrated by this COA. Do not invent a v0.2 design here.

## CRITICAL_INTEROPERABILITY

### 1. Explicit ND (Not Detected) for cannabinoids / terpenes — CORE_INTEROPERABILITY

**Observed:** Cannabinoid panel reports CBDV/CBDA/CBGA/CBD/THCV/CBN/CBC/THCA as **ND** (Not Detected), and Total CBD = ND. Many terpenes listed as ND. COA states ND ≠ zero.

**v0.1-alpha limitation:** `CannabinoidMeasurement` / `TerpeneEntry` allow `value: number|null` and gap `status` ∈ {`not_measured`,`not_applicable`,`withheld`} only. There is **no ND / not_detected** state for quantitative analyte panels. Coercing ND → `0` is scientifically wrong; coercing to `null` + `not_measured` is also wrong (tests *were* performed).

**Contrast with safety:** `SafetyAnalyteResult` includes `not_detected`, which is acceptable for microbial organisms on this COA — but that enum is **not** available on cannabinoid/terpene measurements.

**Interoperability consequence:** Downstream systems cannot distinguish “tested, not detected” from “zero,” “absent,” or “not tested,” which breaks faithful COA exchange across labs/markets.

**Layer:** CORE_INTEROPERABILITY  
**vs existing issues:** Distinct from #1 (`<` qualifier) and #2 (NOT_PERFORMED). New critical gap.

### 2. Below-reporting-limit heavy metals (`<0.008` ppm) — CORE_INTEROPERABILITY

**Observed:** As/Cd/Pb/Hg each `<0.008` ppm with panel Passed.

**v0.1-alpha limitation:** Same as COA-001 / issue #1 — no qualifier / below_limit construct. Must not encode as `0`.

**Evidence:** Confirms GitHub issue #1; do not duplicate the issue.

**Layer:** CORE_INTEROPERABILITY

### 3. Concurrent multi-unit quantitative representations (% + mg/g + mg/unit) — CORE_INTEROPERABILITY (medical dosing)

**Observed:** Same cannabinoids reported as %wt, mg/g, and mg/unit for a **0.5g medical** vaporization oil (e.g. THC 87.13% / 871.30 mg/g / 435.65 mg/unit).

**v0.1-alpha limitation:** Each `CannabinoidMeasurement` carries a single `unit` enum value. Concurrent equivalent measurements cannot live in core without picking one unit and stuffing others into extensions.

**Interoperability consequence:** Losing mg/unit dosing information for medical products is a **material** interchange failure for clinical/dispensary consumers of the record — not merely presentation.

**Layer:** CORE_INTEROPERABILITY (dose-bearing medical products) — often misread as PRESENTATION_ONLY; this case shows material dosing loss.

## IMPORTANT

### 4. Best-by / expiry date — OPTIONAL_METADATA

**Observed:** Best by 2027-07-31.

**v0.1-alpha limitation:** No first-class `best_by` / product expiry on the cultivation record.

**Layer:** OPTIONAL_METADATA

### 5. Visual inspection / foreign material — OPTIONAL_METADATA

**Observed:** Visual Inspection Passed.

**v0.1-alpha limitation:** No foreign-material / visual-inspection structure (same family as COA-001 gap).

**Layer:** OPTIONAL_METADATA

### 6. Finished product display name / SKU — OPTIONAL_METADATA / JURISDICTION_SPECIFIC

**Observed:** Display name and product code (DISVAPE…) distinct from cultivar code SLH.

**v0.1-alpha limitation:** Cultivar `reported_name` is the closest field; finished-goods SKU semantics live in extensions.

**Layer:** OPTIONAL_METADATA (SKU) / PRESENTATION_ONLY (display packaging copy)

## NICE_TO_HAVE

### 7. Explicit COA certificate ID distinct from redacted placeholder

Public record uses `redacted-coa-002` by design.

## OUT_OF_SCOPE

- Republishing original COA artwork, lab brand name, signatures
- WeedDAO independently verifying analytical accuracy
- Changing frozen v0.1-alpha schema

## Explicit non-gaps (handled)

| Construct | How represented |
|-----------|-----------------|
| Detected numeric cannabinoids/terpenes (%wt) | Standard measurement objects, unit `%` |
| Microbial ND for organisms | `SafetyAnalyteResult` `not_detected` |
| Residual solvents PASS + 5000 ppm limit | `result=pass` with limit/unit |
| Pesticide / HM **panel** PASS | `status=pass` |
| TX license 0005 | `producer.license_id` |
| Batch ID | `cultivation_batch_id` |

## Mapping result

**PARTIAL** — validated v0.1-alpha record produced, but ND states, `<` heavy-metal qualifiers, and concurrent multi-unit dosing cannot be represented faithfully without schema evolution / extension bags.
