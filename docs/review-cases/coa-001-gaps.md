# COA-001 — Evidence-backed schema gaps (v0.1-alpha)

**Schema:** WeedDAO Cultivation Record **0.1-alpha** (FROZEN — not modified by this review)  
**Case:** Real-world grower-supplied COA mapping  
**Principle:** Document only gaps demonstrated by this COA. Do not invent a v0.2 design here.

## CRITICAL_INTEROPERABILITY

### 1. Below-reporting-limit / quantitation qualifier (`<`)

**Observed:** Many cannabinoid and terpene results are reported as `<0.1` mg/g or `<0.01%`, not as zero and not as “not measured.”

**v0.1-alpha limitation:** `CannabinoidMeasurement` / `TerpeneEntry` allow `value: number|null` and gap `status` ∈ {`not_measured`,`not_applicable`,`withheld`} only. There is no `qualifier` / `below_limit` / `reporting_limit` construct. Coercing `<0.1` → `0` is scientifically wrong; coercing to `null` + `not_measured` is also wrong.

**Interoperability consequence:** Downstream systems cannot distinguish “measured below LOQ/LOR” from “absent,” “zero,” or “not tested,” which breaks faithful COA exchange.

**Design considerations (non-prescriptive):** optional qualifier enum; separate reporting_limit field; allow structured non-detect objects without magic zeros.

### 2. Analyte-level NOT_PERFORMED vs PASS/FAIL

**Observed:** Microbial panel includes organisms with PASS and **P. aeruginosa: Test Not Performed**, while overall text says Passed Microbial Analysis. Residual solvent panel is entirely Not Performed.

**v0.1-alpha limitation:** Safety analyte `result` enum is `pass|fail|not_detected|detected`. Panel `status` includes `not_tested` / `partial`, which helps at panel level, but analyte-level Not Performed cannot be expressed in the enum.

**Interoperability consequence:** Risk of collapsing “not performed” into pass, fail, or missing — each wrong.

## IMPORTANT

### 3. Fixed cannabinoid vocabulary vs extended COA analytes

**Observed:** COA reports Δ8-THC, Δ10-THC, Δ6a,10a-THC, Δ9-THCP, CBDV.

**v0.1-alpha limitation:** `cannabinoids` object has `additionalProperties: false` and a fixed key set (thc, thca, cbd, …). Extended analytes cannot be added without schema change.

**Interoperability consequence:** Modern COAs with expanded cannabinoid panels lose machine-readable fidelity.

### 4. Sample received date / collection party / material type

**Observed:** Date received, “Sample Collected by Client,” material “Cured Flower.”

**v0.1-alpha limitation:** LabResults exposes `tested_at` / `sample_id` but not received date, collector, or matrix/material as first-class fields.

**Interoperability consequence:** Chain-of-custody semantics required by labs/growers are lost or stuffed into free-text notes.

### 5. Foreign material inspection

**Observed:** Passed Visual Inspection.

**v0.1-alpha limitation:** No foreign-material / visual-inspection structure under LabSafety.

### 6. Dual reporting units for totals (mg/g table vs % summary)

**Observed:** Cannabinoid table total 248.2 mg/g alongside Total Cannabinoids 24.8%.

**v0.1-alpha limitation:** Totals are single `CannabinoidMeasurement` objects; dual unit presentations require extensions/notes.

### 7. Certificate validity period

**Observed:** Results valid for 90 days (COA-specific statement).

**v0.1-alpha limitation:** No certificate validity window field. Correctly should **not** become a universal WeedDAO rule — but COA metadata has nowhere first-class to live.

## NICE_TO_HAVE

### 8. Per-analyte method alongside panel method

HPLC is captured at lab_results level; pesticide/microbial methods differ (qPCR). Panel `method` exists for some safety blocks; richer per-analyte method linkage would help.

### 9. Explicit approval date distinct from tested_at

COA approval date mapped partially onto `tested_at`.

## Explicit non-gaps (handled)

| Construct | How represented |
|-----------|-----------------|
| Residual solvents Not Performed | `safety.residual_solvents.status = not_tested` |
| Pesticide panel PASS | `safety.pesticides.status = pass` |
| Detected numeric cannabinoids/terpenes | Standard measurement objects |
| PASS ≠ NOT_PERFORMED at panel level | `not_tested` / `partial` available |

## Mapping result

**PARTIAL** — validated v0.1-alpha record produced, but below-limit qualifiers and several COA analytes/panel semantics cannot be represented faithfully without schema evolution.
