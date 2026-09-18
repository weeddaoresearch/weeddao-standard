# Review evidence log — v0.1-alpha

This file records **independent external** review and implementation evidence for the WeedDAO Open Cannabis Data Standard `v0.1-alpha`.

No fabricated reviewers. Empty categories remain until real evidence is submitted and verified by maintainers.

---

## GROWER_REVIEW

- **status:** NOT YET RECORDED
- **date:** 
- **identity:** 
- **summary:** 
- **issues:** 
- **changes:** 

---

## LAB_REVIEW

- **status:** NOT YET RECORDED
- **date:** 
- **identity:** 
- **summary:** 
- **issues:** 
- **changes:** 

---

## RESEARCH_REVIEW

- **status:** NOT YET RECORDED
- **date:** 
- **identity:** 
- **summary:** 
- **issues:** 
- **changes:** 

---

## SOFTWARE_REVIEW

- **status:** NOT YET RECORDED
- **date:** 
- **identity:** 
- **summary:** 
- **issues:** 
- **changes:** 

---

## FIRST_EXTERNAL_VALID_RECORD

- **status:** NOT YET RECORDED
- **date:** 
- **identity:** 
- **summary:** 
- **issues:** 
- **changes:** 

---

## FIRST_REAL_WORLD_COA_MAPPING

- **status:** COMPLETED
- **date:** 2026-09-18
- **case_id:** COA-001
- **case_type:** REAL_WORLD_COA_MAPPING
- **source:** GROWER_SUPPLIED (Desert Green Farm; permission confirmed for WeedDAO development/review)
- **permission:** CONFIRMED
- **original_image_public:** NO
- **schema_version_tested:** 0.1-alpha
- **mapping_result:** PARTIAL
- **identity:** Grower disclosed with permission; laboratory branded identity redacted as `external-lab-001`
- **summary:** First real-world COA mapped into v0.1-alpha. Validated redacted record produced. Critical gaps: below-limit (`<`) qualifiers; analyte-level NOT_PERFORMED. WeedDAO performed the mapping (not an external implementation). Portfolio now includes COA-002 and COA-003 (see below); TOTAL_REAL_WORLD_COA_MAPPINGS=3.
- **issues:** GitHub issues titled `COA-001: Support …` (below-limit qualifier; analyte NOT_PERFORMED)
- **changes:** Documentation/evidence only — **schema unchanged**; v0.1-alpha tag untouched
- **links:** [coa-001.md](review-cases/coa-001.md), [coa-001-gaps.md](review-cases/coa-001-gaps.md), [mapped JSON](../review-data/coa-001-weeddao-record.json)

---


---

## REAL_WORLD_COA_MAPPING — COA-002

- **status:** COMPLETED
- **date:** 2026-09-18
- **case_id:** COA-002
- **case_type:** REAL_WORLD_COA_MAPPING
- **source:** PRODUCER_SUPPLIED (Texas Original; 0:1 SLH Medical Vaporization Oil 0.5g)
- **permission:** CONFIRMED
- **original_image_public:** NO
- **schema_version_tested:** 0.1-alpha
- **mapping_result:** PARTIAL
- **identity:** Producer/license disclosed; laboratory branded identity redacted as `external-lab-002`
- **summary:** Second real-world COA mapped into v0.1-alpha. Critical gaps confirmed/new: HM below-limit `<0.008` (confirms #1); explicit cannabinoid/terpene ND; concurrent %/mg/g/mg/unit medical dosing. NOT_PERFORMED (#2) not exercised. WeedDAO performed the mapping (not an external implementation).
- **issues:** #1 confirmed by evidence in case docs (PAT could not comment on existing issues); created #3 (ND), #4 (multi-unit)
- **changes:** Documentation/evidence only — **schema unchanged**; v0.1-alpha tag untouched
- **links:** [coa-002.md](review-cases/coa-002.md), [coa-002-gaps.md](review-cases/coa-002-gaps.md), [mapped JSON](../review-data/coa-002-weeddao-record.json)

---

## REAL_WORLD_COA_MAPPING — COA-003

- **status:** COMPLETED
- **date:** 2026-09-18
- **case_id:** COA-003
- **case_type:** REAL_WORLD_COA_MAPPING
- **source:** PRODUCER_SUPPLIED (Texas Original; 0:1 OGK Distillate Syringe 0.5g)
- **permission:** CONFIRMED
- **original_image_public:** NO
- **schema_version_tested:** 0.1-alpha
- **mapping_result:** PARTIAL
- **identity:** Producer/license disclosed; laboratory branded identity redacted as `external-lab-002`; batch ID literal `"0"` preserved as string
- **summary:** Third real-world COA mapped into v0.1-alpha. Repeats ND, `<0.008` HM, and multi-unit gaps; documents ambiguous batch token `"0"`. WeedDAO performed the mapping (not an external implementation).
- **issues:** Same disposition as COA-002 (#3 ND, #4 multi-unit); batch `"0"` documented in gaps only
- **changes:** Documentation/evidence only — **schema unchanged**; v0.1-alpha tag untouched
- **links:** [coa-003.md](review-cases/coa-003.md), [coa-003-gaps.md](review-cases/coa-003-gaps.md), [mapped JSON](../review-data/coa-003-weeddao-record.json)

---

## CROSS_CASE_ANALYSIS — COA-001..003

- **status:** COMPLETED
- **date:** 2026-09-18
- **path:** [cross-case-analysis-001-003.md](review-cases/cross-case-analysis-001-003.md)
- **TOTAL_REAL_WORLD_COA_MAPPINGS:** 3
- **FIRST_EXTERNAL_IMPLEMENTATION:** NO

## FIRST_EXTERNAL_IMPLEMENTATION

- **status:** NOT YET RECORDED
- **date:** 
- **identity:** 
- **summary:** 
- **issues:** 
- **changes:** 

---

Machine-readable mirror: [../review-tracker.json](../review-tracker.json).

## Public COA Corpus v0.1 (QA baseline)
- Path: `corpus/v0.1/`
- TOTAL_CASES=50; SOURCE_UNAVAILABLE=0; ACTUAL_FAIL_CASES=1 (['COA-046'])
- Schema SHA256 `31b0bdab4585954bebb9af1b06ac8b2d5a7b513ad1ca9694070836f1c723b5ee`; tag `v0.1-alpha` unchanged.
- Stats: `corpus/v0.1/build_stats.json` (canonical).
