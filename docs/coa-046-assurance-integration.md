# COA-046 Laboratory Assurance Integration Review

**Status:** experimental integration proof  
**Branch:** `registry-rfc`  
**Case:** COA-046 — Lightscale Labs / Grön Chocolate  
**Bundle:** `examples/assurance-bundles/coa-046-assurance-bundle.json`

## Purpose

This is the first end-to-end WeedDAO laboratory-assurance integration proof.

The goal is not to prove that every layer is populated.

The goal is to test whether the current architecture can describe:

1. what is known;
2. what is only partially supported;
3. what is absent from the available public evidence;
4. where one evidence layer must not be confused with another.

## Why COA-046

COA-046 is a strong stress case because it already exercises several difficult semantics in one real public result:

- multi-unit Total THC;
- potency-spec FAIL;
- homogeneity FAIL;
- <LOQ;
- ND vocabulary;
- regulatory tracking identifiers;
- sample lifecycle dates.

The v0.2 mapping is full for the previously identified core interoperability gaps.

That makes it a good case for testing the new assurance architecture.

## What the core gets right

### Result semantics

Total THC remains a detected quantitative result with concurrent units:

- 0.2531 %
- 2.531 mg/g
- 11.39 mg/serving
- 113.9 mg/package

The result can independently carry:

```text
assessment = fail
```

without rewriting the analytical state.

### Potency vs homogeneity

The potency-spec failure and homogeneity failure remain separate.

Homogeneity is represented as:

- Total THC RPD;
- 10.1%;
- action limit <=10%;
- FAIL.

This is not contaminant failure and is not analytical-batch QC failure.

### ND and <LOQ

Both remain explicit source semantics rather than being converted to numeric zero.

## Assurance-layer coverage

### Sampling — partial

Known:

- product batch;
- METRC package/source identifiers;
- sample ID;
- collection date.

Not established in current corpus evidence:

- sampling plan;
- selection/randomization;
- increment count;
- composite formation;
- collection party;
- sample mass;
- representativeness basis;
- homogenization/test-specimen reduction.

Conclusion:

> Sample identity is represented. Representativeness is not demonstrated.

### Method assurance — not demonstrated

The current corpus mapping does not establish:

- exact SOP/method;
- revision;
- technique;
- validated matrix/analyte scope;
- verification;
- deviations.

Conclusion:

> Do not infer method fitness merely because the result came from a laboratory COA.

### Traceability assurance — not demonstrated

The current corpus evidence does not establish:

- CRM/RM/standard identity;
- certificate/lot;
- assigned value;
- reference uncertainty;
- calibration event;
- calibration chain;
- result-specific traceability claim.

Conclusion:

> `provenance=laboratory_verified` must never be interpreted as metrological traceability.

### Analytical-batch QC — partial hint only

The v0.1 review captured ND vocabulary on QC blanks, which proves that QC semantics were visible in the source environment.

But the current structured corpus does not establish:

- batch ID;
- control identities;
- blank values;
- spike recovery;
- duplicate precision;
- calibration verification;
- QC acceptance criteria;
- final batch disposition.

Conclusion:

> Product/result FAIL must not be interpreted as analytical-batch failure.

### Measurement uncertainty — not demonstrated

No uncertainty value or uncertainty model is established in the current corpus evidence.

The following are **not substitutes**:

- homogeneity RPD;
- LOQ;
- LOD;
- number of decimal places;
- label deviation.

### Conformity decision — partial

The source evidence preserves the outcome and some relevant values:

- measured vs labeled Total THC;
- homogeneity RPD vs action limit.

But the current corpus does not establish:

- formal decision-rule identity;
- uncertainty treatment;
- guard band;
- rounding rule;
- full authoritative specification basis for the potency decision.

Conclusion:

> WeedDAO can preserve the observed decision without pretending it knows the complete decision procedure.

## Most important integration findings

### 1. No sidecar collision yet

The current sidecars answer distinct questions.

No evidence from COA-046 requires merging:

- sampling;
- method;
- traceability;
- QC;
- uncertainty/decision rules.

### 2. Public evidence is naturally sparse

This is not a defect.

A public COA is primarily a reporting artifact, not a full ISO/IEC 17025 quality-system export.

The sidecars should therefore remain optional and sparse until richer laboratory/customer data is available.

### 3. Missing evidence must not become a negative score

This integration proof reinforces a major product rule:

> Absence of public evidence is not evidence of poor laboratory practice.

Therefore assurance coverage should never automatically become a lab-quality score.

### 4. The current architecture survives a real failure case

COA-046 is especially useful because a FAIL result can easily tempt systems to collapse multiple meanings.

The architecture correctly keeps apart:

- product conformity failure;
- homogeneity failure;
- analytical batch validity;
- measurement uncertainty;
- sampling representativeness;
- metrological traceability.

## Architecture decision

The first integration proof does **not** support another schema.

It supports validation of the existing architecture with richer evidence.

**NEW SIDECAR = NOT JUSTIFIED**

**MONOLITHIC LAB SCHEMA = NOT JUSTIFIED**

**V0.2 SCHEMA CHANGE = NOT JUSTIFIED**

## Highest-value next evidence

The next target should be one real laboratory/customer export where the **same result** can be linked to several of:

- method/SOP and revision;
- validation/verification scope;
- QC batch controls;
- uncertainty;
- calibration/reference-material data;
- conformity decision.

That dataset will provide far more architectural information than creating another conceptual schema.

## Commercial significance

This integration pattern also sharpens the interoperability-audit product.

For a customer dataset WeedDAO can report, separately:

- result semantics preserved;
- method evidence available/missing;
- sampling evidence available/missing;
- QC evidence available/missing;
- uncertainty/decision evidence available/missing;
- traceability evidence available/missing;
- information loss introduced by target systems.

That is an evidence-gap map, not a laboratory rating.

It can be commercially useful even if the customer never adopts WeedDAO as its native schema.
