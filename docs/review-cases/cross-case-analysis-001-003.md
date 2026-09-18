# Cross-case analysis — COA-001, COA-002, COA-003

**Schema:** WeedDAO Cultivation Record **0.1-alpha** (FROZEN)  
**Cases:** REAL_WORLD_COA_MAPPING × 3  
**FIRST_EXTERNAL_IMPLEMENTATION:** NO (all mappings performed by WeedDAO)

## Case summary

| Case | Producer | Matrix / product | Mapping | Key stress tests |
|------|----------|------------------|---------|------------------|
| COA-001 | Desert Green Farm | Cured flower | PARTIAL | `<` LOQ, NOT_PERFORMED microbials, extended cannabinoids, dual %/mg/g totals |
| COA-002 | Texas Original | 0.5g medical vaporization oil (SLH) | PARTIAL | Explicit **ND**, HM `<0.008`, concurrent %/mg/g/**mg/unit**, residual solvent PASS+limits |
| COA-003 | Texas Original | 0.5g distillate syringe (OGK) | PARTIAL | Same ND/`<`/multi-unit as 002; literal batch ID **`"0"`**; CBN-dominant minor cannabinoid |

## REPEATED_GAPS

| Gap | Cases | Severity | Existing issue |
|-----|-------|----------|----------------|
| Below-reporting-limit / `<` qualifier on quantitative results | 001 (`<0.1` mg/g, `<0.01%`); 002+003 (HM `<0.008` ppm) | CRITICAL_INTEROPERABILITY | **#1** (confirmed by 002/003; do not duplicate) |
| No first-class visual / foreign-material inspection | 001, 002, 003 | IMPORTANT / OPTIONAL_METADATA | Documented; no dedicated issue required yet |
| Dual / multi unit presentations requiring extensions | 001 (mg/g table vs %); 002+003 (% + mg/g + **mg/unit**) | IMPORTANT→CRITICAL for medical dose (002/003) | New issue for concurrent multi-unit (002/003 evidence) |
| Finished material / product naming beyond cultivar | 001 (Cured Flower); 002/003 (SKU + display) | IMPORTANT / OPTIONAL_METADATA | Gaps docs only |

## NEW_GAPS (vs COA-001)

| Gap | Cases | Severity | Action |
|-----|-------|----------|--------|
| Explicit **ND / Not Detected** on cannabinoid & terpene panels (distinct from `<`, 0, not_measured, NOT_PERFORMED) | 002, 003 | CRITICAL_INTEROPERABILITY | **New GitHub issue** |
| Concurrent **mg/unit** dosing alongside % and mg/g on medical 0.5g products | 002, 003 | CRITICAL_INTEROPERABILITY (medical interchange) | **New GitHub issue** |
| Literal / ambiguous batch token `"0"` (preserve string; do not coerce null) | 003 | IMPORTANT (workflow) | Gaps only — schema already stores string |
| Best-by / expiry date | 002, 003 | OPTIONAL_METADATA | Gaps only |
| TX license on producer | 002, 003 | RESOLVED_BY_EXISTING_SCHEMA (`producer.license_id`) | — |
| Residual solvents **PASS + numeric limits** (performed panels) | 002, 003 | RESOLVED_BY_EXISTING_SCHEMA | Contrast COA-001 `not_tested` |
| Microbial organism **ND → `not_detected`** | 002, 003 | RESOLVED_BY_EXISTING_SCHEMA (safety enum) | Highlights asymmetry vs cannabinoid ND |

## RESOLVED_BY_EXISTING_SCHEMA

- Detected numeric cannabinoids with unit `%` or `mg/g` (001 used mg/g; 002/003 used %)
- Detected terpene arrays
- Panel-level pesticide / heavy-metal / microbial `status=pass`
- Residual solvents panel `status=pass` with analyte `result=pass` + `limit`/`unit` (additionalProperties-friendly)
- Microbial `not_detected` for Yeast/Mold, Salmonella, E.coli
- Producer organization name + jurisdiction
- `producer.license_id` for TX 0005
- `cultivation_batch_id` holding both long numeric strings (002) and literal `"0"` (003)
- Lab identity redaction via opaque `lab_id`
- Extension bag `extensions.weeddao_review` for non-core facts without schema change
- Residual solvents **Not Performed** (001) via `status=not_tested` — complementary to 002/003 PASS path

## FORMAT_DIFFERENCES

| Dimension | COA-001 | COA-002 / COA-003 |
|-----------|---------|-------------------|
| Primary cannabinoid unit on COA | mg/g table + % summaries | %wt primary + mg/g + mg/unit |
| Non-detect style | Mostly `<LOQ` qualifiers | Explicit **ND** token + HM `<` |
| Safety solvents | Entire panel Not Performed | Full PASS with 5000 ppm limits |
| Microbial detail | PASS + one Not Performed organism | All listed organisms ND / panel pass |
| Product form | Cured flower | Concentrates / medical oil & syringe |
| Jurisdiction signals | US-NM grower COA | US-TX license 0005 |
| Batch identifier | Synthetic review batch id | Real batch string / literal `"0"` |
| Minor cannabinoids detected | THCA, CBGA dominant flower pattern | CBG (002) or CBN (003) with high Δ9-THC distillate/oil |

## LAB/PRODUCER_WORKFLOW_DIFFERENCES

1. **Flower vs concentrate workflows:** COA-001 emphasizes acid forms (THCA) and moisture/foreign-material flower checks; 002/003 emphasize decarboxylated high-% THC oils with residual solvent panels (extraction workflow).
2. **Non-detect vocabulary:** One lab/report style uses `<` reporting limits; Texas Original style uses **ND** for organics panels and `<` for heavy metals — schema must support **both** without collapse.
3. **NOT_PERFORMED:** Only COA-001 exercises analyte-level Not Performed (issue #2). COA-002/003 do **not** exercise #2 — optional note only.
4. **Dose presentation:** Medical 0.5g unit products publish mg/unit; flower COA did not — multi-unit becomes critical when dose-per-package is the clinical quantity of record.
5. **Identity & compliance fields:** TX license and best-by appear on 002/003; BioTrack-style IDs withheld on 001 — different compliance surfaces, same need for optional public license fields (already present).

## Checklist evaluation (requested)

| Checklist item | Finding |
|----------------|---------|
| Does `<` / below-limit recur? | **YES** — HM `<0.008` on 002/003 confirms #1 |
| Does NOT_PERFORMED recur? | **NO** on 002/003 — #2 not newly evidenced |
| Is ND a distinct critical gap? | **YES** — new CRITICAL vs #1/#2 |
| Is multi-unit critical for medical products? | **YES** — mg/unit loss on 0.5g oil/syringe is material dosing interoperability |
| Batch `"0"` silent mis-merge risk? | **IMPORTANT** documentation; schema can store `"0"`; no CRITICAL issue filed |
| Best-by first-class? | OPTIONAL_METADATA only |
| External implementation? | **NO** — WeedDAO mapped all three |

## Issue disposition

| Action | Target |
|--------|--------|
| Comment with evidence | Issue **#1** (HM `<0.008` on COA-002/003) |
| No forced update | Issue **#2** (not exercised; optional clarifying comment) |
| Created | [#3](https://github.com/weeddaoresearch/weeddao-standard/issues/3) ND/Not Detected for quantitative cannabinoid/terpene panels (COA-002 + COA-003) |
| Created | [#4](https://github.com/weeddaoresearch/weeddao-standard/issues/4) Concurrent multi-unit quantitative representations / medical dose units (COA-002 + COA-003) |
| Attempted evidence append | #1 / #2 — PAT lacked `issues: write` on existing issues/comments; evidence recorded in case docs + #3/#4 bodies |
| Do not create | Batch `"0"` or best-by standalone CRITICAL issues |

## Mapping portfolio status

- **TOTAL_REAL_WORLD_COA_MAPPINGS:** 3  
- **All mapping results:** PARTIAL  
- **Schema changed:** NO  
- **v0.1-alpha tag changed:** NO  
- **FIRST_EXTERNAL_IMPLEMENTATION:** NO  
