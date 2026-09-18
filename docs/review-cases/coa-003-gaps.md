# COA-003 — Evidence-backed schema gaps (v0.1-alpha)

**Schema:** WeedDAO Cultivation Record **0.1-alpha** (FROZEN — not modified by this review)  
**Case:** Real-world Texas Original OGK distillate syringe COA mapping  
**Principle:** Document only gaps demonstrated by this COA. Do not invent a v0.2 design here.

## CRITICAL_INTEROPERABILITY

### 1. Explicit ND (Not Detected) for cannabinoids / terpenes — CORE_INTEROPERABILITY

**Observed:** CBDV/CBDA/CBGA/CBG/CBD/THCV/CBC/THCA = ND; Total CBD = ND; remaining terpene panel ND. Same semantic failure mode as COA-002.

**v0.1-alpha limitation:** No ND state on `CannabinoidMeasurement` / `TerpeneEntry`. Microbial `not_detected` does **not** transfer to quantitative cannabinoid panels.

**Layer:** CORE_INTEROPERABILITY  
**vs existing issues:** New vs #1 (`<`) and #2 (NOT_PERFORMED).

### 2. Below-reporting-limit heavy metals (`<0.008` ppm) — CORE_INTEROPERABILITY

**Observed:** Same As/Cd/Pb/Hg `<0.008` ppm pattern as COA-002.

**Evidence:** Confirms issue #1; do not duplicate.

**Layer:** CORE_INTEROPERABILITY

### 3. Concurrent multi-unit representations (% + mg/g + mg/unit) — CORE_INTEROPERABILITY (medical dosing)

**Observed:** CBN/THC/Total THC as %wt, mg/g, and mg/unit for 0.5g distillate syringe (e.g. THC 85.49% / 854.90 mg/g / 427.45 mg/unit).

**Interoperability consequence:** Medical dose/unit loss without extension bag is material for interchange.

**Layer:** CORE_INTEROPERABILITY

## IMPORTANT

### 4. Ambiguous batch token `"0"` — OPTIONAL_METADATA / IMPORTANT documentation

**Observed:** Certificate batch ID is literal `"0"`. Schema **can** store string `"0"` in `cultivation_batch_id` (mapped exactly). Risk is **operational**: consumers may treat `"0"` as empty/missing and silently mis-merge, or mappers may coerce to `null`.

**Recommendation:** Document + preserve string; no CRITICAL schema change required solely for this token. Optional guidance / advisory issue only if maintainers want explicit “do not coerce zero-like tokens” rule — **not filed as CRITICAL** here.

**Layer:** IMPORTANT (workflow) / OPTIONAL_METADATA

### 5. Best-by date — OPTIONAL_METADATA

**Observed:** Best by 2026-12-03.

**Layer:** OPTIONAL_METADATA

### 6. Visual inspection — OPTIONAL_METADATA

**Observed:** Passed Visual Inspection.

**Layer:** OPTIONAL_METADATA

### 7. Finished product display / SKU — OPTIONAL_METADATA / PRESENTATION_ONLY

**Observed:** DISSyr product code + display name vs cultivar OGK.

**Layer:** OPTIONAL_METADATA / PRESENTATION_ONLY

## NICE_TO_HAVE

### 8. Shared lab identity across COA-002/003

Both use `external-lab-002` redaction token for the same producer’s lab partner pattern.

## OUT_OF_SCOPE

- Original images / signatures / lab brand names
- Independent analytical verification
- Schema mutation of frozen v0.1-alpha

## Explicit non-gaps (handled)

| Construct | How represented |
|-----------|-----------------|
| Batch ID literal `"0"` | `cultivation_batch_id: "0"` (string preserved) |
| Detected CBN/THC/Total THC % | Core cannabinoid measurements |
| Detected terpenes | `terpenes[]` |
| Microbial ND | `not_detected` |
| Residual solvents PASS + limits | `pass` + limit |
| Panel-level pesticide/HM pass | `status=pass` |

## Mapping result

**PARTIAL** — validated record with literal batch `"0"` preserved; ND, `<` HM, and multi-unit dosing remain unrepresentable in core fields.
