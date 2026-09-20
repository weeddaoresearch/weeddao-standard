# WeedDAO Laboratory Measurement Assurance Roadmap

**Status:** evidence-driven companion analysis  
**Branch:** `registry-rfc`  
**Reviewed:** 2026-09-20  
**Schema impact:** none; this document does not modify v0.2-draft

## Purpose

WeedDAO currently preserves the meaning of reported laboratory results better than a flat COA transcription model.

The next technical risk is different:

> A result can be represented correctly while the evidence supporting that result is still missing.

A laboratory-quality interoperability layer should eventually be able to preserve not only **what was reported**, but enough context to evaluate **how the measurement was produced, whether it was fit for purpose, and how a pass/fail decision was reached**.

This is the measurement-assurance layer.

## External measurement-science anchors

The roadmap should remain compatible with the principles used by:

- NIST metrological-traceability policy;
- NIST cannabis laboratory quality-assurance work (CannaQAP);
- NIST cannabis/hemp reference-material work, including RM 8210 Hemp Plant;
- ISO/IEC 17025 laboratory-competence concepts as reflected in ILAC guidance;
- ILAC G17 measurement uncertainty in testing;
- ILAC G8 decision rules and statements of conformity;
- ILAC P9 proficiency testing / interlaboratory comparison;
- ILAC P10 metrological traceability;
- ASTM D37 laboratory standards and work items;
- AOAC cannabis Standard Method Performance Requirements where applicable.

No affiliation, accreditation, endorsement, or NIST traceability is implied.

## Critical distinction

WeedDAO must not equate:

```text
traceable instrument
=
traceable measurement result
```

Metrological traceability is a property of a **measurement result** supported by a documented chain of calibrations/reference standards and associated uncertainties.

Likewise:

```text
measured value
!=
statement of conformity
```

A PASS/FAIL decision may depend on:

- the specification or regulatory limit;
- the measured value;
- measurement uncertainty;
- the decision rule / guard band;
- rounding conventions;
- jurisdiction-specific requirements.

These must not be silently collapsed.

---

# Measurement-assurance vantage points

## 1. Measurement uncertainty

### Question

Can WeedDAO represent uncertainty attached to a quantitative result?

Potential source concepts include:

- standard uncertainty;
- combined standard uncertainty;
- expanded uncertainty;
- coverage factor `k`;
- coverage probability / confidence level;
- uncertainty unit;
- relative uncertainty;
- uncertainty basis or model.

### Current WeedDAO state

No dedicated uncertainty object is present in v0.2-draft.

### Risk

A value such as:

```text
9.8 ± 0.8 mg/g
```

is materially different from:

```text
9.8 mg/g
```

when the regulatory limit is near 10 mg/g.

### Priority

**HIGH**

Do not add schema fields until real laboratory/export evidence is collected.

---

## 2. Decision rules / guard bands

### Question

How was a PASS or FAIL conclusion derived?

Potential attributes:

- specification source;
- limit;
- decision rule identifier;
- uncertainty considered: yes/no;
- guard band;
- rounding rule;
- inclusive/exclusive comparator;
- decision outcome.

### Current WeedDAO state

WeedDAO correctly separates `assessment` from `result_state`, but does not encode the decision rule that produced the assessment.

### Risk

Two competent laboratories can report the same numerical result yet reach different conformity statements if different decision rules are used.

### Priority

**HIGH**

This should be tested before expanding PASS/FAIL interoperability.

---

## 3. Metrological traceability

### Question

What reference chain supports the measurement result?

Potential evidence:

- certified/reference material identifier;
- producer;
- certificate identifier;
- lot/batch;
- certified value;
- uncertainty;
- expiration/use-by;
- calibration standard;
- calibration date;
- traceability claim/source;
- SI or other specified reference.

### Current WeedDAO state

General provenance exists, but no measurement-traceability chain.

### Guardrail

Never label a result “NIST traceable” merely because:

- an instrument was calibrated;
- a NIST reference material was used;
- a vendor certificate mentions NIST.

The provider of the measurement result remains responsible for supporting the traceability claim.

### Priority

**HIGH**

---

## 4. Reference materials and controls

### Question

Which materials were used to establish or check analytical performance?

Potential categories:

- CRM / certified reference material;
- RM / reference material;
- matrix reference material;
- calibration standard;
- internal standard;
- blank;
- matrix blank;
- spike;
- duplicate;
- laboratory control sample;
- continuing calibration verification.

### Cannabis-specific importance

NIST developed RM 8210 Hemp Plant for cannabinoids and toxic elements and describes natural-matrix RMs as tools for quality control and method validation/development.

### Priority

**HIGH**

---

## 5. Quality-control evidence

### Question

Did the analytical batch meet the laboratory's QC acceptance criteria?

Potential observations:

- blank result;
- spike recovery;
- duplicate precision;
- surrogate/internal-standard recovery;
- calibration verification;
- control-chart status;
- QC acceptance limits;
- QC pass/fail.

### Current WeedDAO state

COA outcome is represented, but analytical-batch QC evidence is not.

### Priority

**HIGH for lab integrations; LOW for ordinary public COA ingestion**

Keep private/customer QC data separate from public COA corpus unless explicitly released.

---

## 6. Method identity and version

### Question

Exactly which analytical method produced the result?

A free-text method name is not enough for high-assurance interoperability.

Potential attributes:

- method identifier;
- method title;
- revision/version;
- internal SOP identifier;
- standard method reference;
- modification/deviation;
- effective date;
- validation/verification status;
- intended matrix/analyte scope.

### External relevance

ASTM D37 maintains cannabis laboratory methods and a laboratory method validation/development practice. AOAC SMPRs define minimum performance characteristics for several cannabis analytical uses.

### Current WeedDAO state

`method` exists primarily as a free-text result field.

### Priority

**HIGH**

---

## 7. Method performance characteristics

Potential characteristics:

- accuracy / bias;
- precision;
- repeatability;
- reproducibility;
- recovery;
- selectivity/specificity;
- linearity;
- working range;
- LOD;
- LOQ;
- robustness;
- measurement uncertainty;
- matrix applicability.

### Key rule

Do not treat a reported LOD/LOQ as proof that the entire method is validated for the tested matrix.

### Priority

**MEDIUM-HIGH**

---

## 8. Sampling uncertainty and representativeness

### Question

Does the laboratory result represent the batch/product it is claimed to represent?

Potential context:

- sampling plan;
- sampling procedure;
- sampling party;
- number of increments;
- sample mass;
- batch mass;
- sampling locations;
- randomization strategy;
- composite vs grab sample;
- sample reduction/subsampling;
- representativeness statement.

### Cannabis-specific importance

Cannabis material can be heterogeneous. ASTM D37 separately addresses post-harvest batch sampling and sample preparation.

### Current WeedDAO state

The sample lifecycle and collection party are represented, but the sampling plan itself is not.

### Priority

**VERY HIGH**

A perfectly modeled analytical result is not enough if the sample was not representative.

---

## 9. Sample preparation / homogenization

Potential context:

- grinding/milling;
- particle size;
- homogenization procedure;
- drying;
- extraction;
- digestion;
- dilution;
- subsampling;
- sample mass;
- extraction volume;
- preparation timestamps.

### Why it matters

NIST's RM 8210 documentation explicitly describes controlled grinding, sieving, packaging and storage. NIST's CannaQAP moisture work also showed large interlaboratory variability associated with different drying methods.

### Priority

**VERY HIGH for comparability research**

---

## 10. Moisture and dry-weight basis

### Question

Is a concentration:

- as received;
- wet weight;
- dry weight;
- moisture corrected;
- normalized by another basis?

### Current WeedDAO state

Measurement `basis` is available, which is a strong start.

### Next test

Determine whether WeedDAO can preserve:

- measured moisture value;
- moisture method;
- dry-weight conversion formula;
- original vs converted concentration;
- rounding.

### Priority

**VERY HIGH**

Never silently compare dry-weight and as-received results.

---

## 11. Rounding and significant figures

### Question

Was the value used for the conformity decision:

- the unrounded instrument result;
- the rounded report value;
- a truncated value?

Potential fields:

- reported precision;
- source decimals;
- rounding rule;
- decision-value precision.

### Priority

**MEDIUM-HIGH**

This becomes high priority near legal thresholds.

---

## 12. Calibration model

Potential context:

- calibration model type;
- calibration range;
- levels;
- weighting;
- internal standard;
- calibration acceptance;
- verification frequency;
- recalibration event.

### Guardrail

Do not attempt to turn WeedDAO into a LIMS.

Only model this if customer workflows show that calibration provenance must survive system migration or audit.

### Priority

**MEDIUM**

---

## 13. Proficiency testing / interlaboratory comparison

### Question

Can a lab demonstrate that its measurement performance is comparable to peers or assigned values?

Potential metadata:

- PT/ILC provider;
- scheme/exercise;
- analyte/matrix;
- participation date;
- performance statistic;
- satisfactory/unsatisfactory;
- corrective action status.

### External relevance

NIST CannaQAP was designed to improve comparability and competence through interlaboratory exercises. ILAC P9 governs the role of PT/ILC in accreditation.

### Priority

**MEDIUM-HIGH for laboratory profiles; not part of individual public COA core**

---

## 14. Accreditation scope

### Question

Is the exact test within the laboratory's accredited scope?

Potential dimensions:

- accreditation body;
- certificate number;
- standard;
- status;
- effective/expiry dates;
- analyte;
- matrix;
- method;
- technology;
- site/location.

### Important distinction

```text
laboratory is ISO/IEC 17025 accredited
```

does not automatically mean:

```text
every analyte × matrix × method on this COA is inside accredited scope
```

### Priority

**HIGH for trust/audit products**

---

## 15. Deviations, nonconformities and amended reports

Potential context:

- method deviation;
- sample exception;
- dilution exception;
- QC failure;
- authorized deviation;
- report amendment;
- superseded certificate;
- reason for revision.

### Priority

**HIGH for provenance**

A corrected COA should never silently replace the original without a revision relationship.

---

## 16. Data integrity / audit trail

Potential controls:

- original record identifier;
- source hash;
- version;
- amendment timestamp;
- signer/authorizer role;
- electronic signature status;
- originating system;
- transformation history.

### Priority

**VERY HIGH**

WeedDAO's commercial value increases if customers can prove what changed during normalization.

---

# Proposed architecture: keep the layers separate

Do not overload `AnalyteResult`.

A future model should conceptually separate:

1. **Reported result**
   - analyte
   - value/state
   - units
   - limits
   - assessment
   - literal source representation

2. **Measurement procedure**
   - method identity/version
   - matrix/scope
   - preparation
   - instrument/technique where necessary

3. **Measurement assurance**
   - uncertainty
   - reference materials
   - calibration/traceability evidence
   - QC
   - validation/verification

4. **Conformity decision**
   - specification
   - decision rule
   - uncertainty treatment
   - comparator
   - outcome

5. **Sampling**
   - plan
   - party
   - batch relationship
   - representativeness

6. **Laboratory competence**
   - accreditation scope
   - PT/ILC
   - relevant credentials

These layers may ultimately link to a result without all becoming mandatory fields.

# What not to build yet

Do not build:

- a full LIMS;
- instrument-control records;
- complete ISO/IEC 17025 quality-management software;
- universal calibration records;
- a claim that WeedDAO establishes NIST traceability;
- accreditation scoring;
- laboratory rankings;
- inferred uncertainty values;
- inferred method validation.

# Highest-value next experiment

## Experiment: uncertainty + conformity decision round-trip

Collect 5–10 real COAs or laboratory exports containing any of:

- explicit measurement uncertainty;
- `±` notation;
- confidence/coverage statements;
- decision-rule language;
- guard bands;
- results near specification limits;
- amended conformity statements.

Test whether WeedDAO can preserve all distinctions without changing the current v0.2 result object.

### Success

The evidence identifies a stable companion model for:

```text
measurement → uncertainty → specification → decision rule → assessment
```

### Failure

The examples are too inconsistent to justify a common model.

### Maximum engineering before evidence

Documentation and mapping examples only.

**Do not modify v0.2-draft before evidence.**

# Current recommendation

The next WeedDAO laboratory RFC should target:

**Measurement Uncertainty + Decision Rules**

This has higher information value than adding more analyte IDs because it tests whether WeedDAO can preserve the evidence behind a regulatory PASS/FAIL statement.

After that:

1. sampling / representativeness;
2. method identity + validation;
3. reference materials / traceability;
4. QC evidence;
5. accreditation scope + PT/ILC.

# Reference anchors

- NIST Policy on Metrological Traceability: https://www.nist.gov/calibrations/traceability
- NIST Tools for Cannabis Laboratory Quality Assurance: https://www.nist.gov/programs-projects/nist-tools-cannabis-laboratory-quality-assurance
- NIST RM 8210 Hemp Plant overview: https://www.nist.gov/news-events/news/2024/07/rm-measuring-cannabinoids-and-toxic-elements-hemp
- ILAC G17 guidance: https://ilac.org/latest_ilac_news/revised-ilac-g17-published/
- ILAC G8 decision-rule guidance: https://ilac.org/latest_ilac_news/revised-ilac-g8-published/
- ILAC P9 proficiency-testing policy: https://ilac.org/publications-and-resources/ilac-policy-series/
- ILAC P10 metrological-traceability policy: https://ilac.org/publications-and-resources/ilac-policy-series/
- ASTM D37.03 laboratory portfolio: https://www.astm.org/membership-participation/technical-committees/committee-d37/subcommittee-d37/jurisdiction-d3703
- AOAC cannabis resources: https://www.aoac.org/resources/?topic=Cannabis
