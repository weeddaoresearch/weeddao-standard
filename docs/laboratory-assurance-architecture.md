# WeedDAO Laboratory Assurance Architecture

**Status:** experimental architecture map  
**Branch:** `registry-rfc`  
**Reviewed:** 2026-09-20

## Purpose

WeedDAO now contains multiple laboratory-assurance companion models. This document keeps them coherent.

The design goal is not to create one enormous laboratory schema.

The design goal is to preserve a chain of evidence around a cannabis laboratory result while allowing each layer to remain optional and independently adoptable.

## Core rule

The v0.2 record remains the source-facing interoperability core.

Assurance evidence stays in companion sidecars.

```text
WeedDAO v0.2 result
        |
        +-- result semantics
        +-- measurement assurance
        +-- sampling assurance
        +-- method assurance
        +-- traceability assurance
        +-- analytical batch QC
```

No sidecar should silently overwrite the core result.

## Evidence chain

A defensible result can be viewed as:

```text
population / batch
    ↓
sampling plan + collection
    ↓
composite / sample preparation
    ↓
qualified analytical method
    ↓
reference materials + calibration evidence
    ↓
analytical batch QC
    ↓
measurement result + uncertainty
    ↓
specification + decision rule
    ↓
assessment / conformity statement
```

Each layer answers a different question.

## 1. Core result semantics

**Question:** What did the source report?

Examples:

- detected;
- ND;
- <LOQ;
- not tested;
- not performed;
- measurements;
- units;
- limits;
- pass/fail;
- original literal.

Primary asset:

`schemas/weeddao-record-v0.2-draft.schema.json`

## 2. Measurement assurance

**Question:** What uncertainty and decision-rule evidence qualifies the result?

Primary assets:

- `schemas/weeddao-measurement-assurance-0.1-draft.schema.json`
- `docs/measurement-assurance-rfc.md`

## 3. Sampling assurance

**Question:** What population was sampled and how was the test specimen made representative?

Primary assets:

- `schemas/weeddao-sampling-assurance-0.1-draft.schema.json`
- `docs/sampling-assurance-rfc.md`

## 4. Method assurance

**Question:** What exact method/version produced the result and what evidence supports its fitness for the intended analyte × matrix × range?

Primary assets:

- `schemas/weeddao-method-assurance-0.1-draft.schema.json`
- `docs/method-assurance-rfc.md`

## 5. Traceability assurance

**Question:** What reference materials and calibration evidence support the result's traceability claim?

Primary assets:

- `schemas/weeddao-traceability-assurance-0.1-draft.schema.json`
- `docs/traceability-assurance-rfc.md`

## 6. Analytical batch QC

**Question:** Was the analytical run in control, and what happened when controls failed?

Primary assets:

- `schemas/weeddao-analytical-batch-qc-0.1-draft.schema.json`
- `docs/analytical-batch-qc-rfc.md`

## Shared linkage pattern

Result-specific sidecars should use JSON Pointer paths such as:

```text
/lab_results/cannabinoids/total_thc
```

This gives all companion evidence a common anchor without changing the v0.2 object.

Where evidence applies to a larger entity, use explicit identifiers:

- subject ID;
- sample ID;
- sampling event ID;
- method ID;
- analytical batch ID;
- calibration ID;
- reference material ID.

## Separation rules

### Sampling vs method

Sampling determines whether the specimen represents the population.

Method assurance determines whether the analytical procedure is fit for that specimen/analyte.

Do not combine them.

### Method vs QC

Method validation establishes capability.

Batch QC monitors continuing performance during a particular run.

A validated method can still have a failed analytical batch.

### Calibration vs QC

Calibration establishes the measurement relationship.

Continuing calibration verification monitors whether it remains acceptable during use.

The same evidence should not be duplicated across both sidecars unless the source itself provides both contexts.

### Uncertainty vs QC

Measurement uncertainty characterizes dispersion around the reported result.

QC observations indicate whether performance controls met acceptance criteria.

A passing QC batch does not imply zero or negligible uncertainty.

### Assessment vs batch disposition

A sample result may FAIL a regulatory specification while the analytical batch itself is valid and accepted.

Conversely, a sample may appear to PASS while the analytical batch is rejected.

These are different axes.

## Evidence status discipline

WeedDAO should preserve evidence states rather than generate certification claims.

Preferred concepts include:

- source reported;
- demonstrated by supplied evidence;
- partial evidence;
- unknown;
- not demonstrated.

Avoid claims such as:

- scientifically valid;
- fully traceable;
- compliant laboratory;
- representative sample;
- validated method;

unless those are explicitly source-attributed and supported.

## Public vs private boundary

### Public/open

Good candidates for public standardization:

- schemas;
- identifiers;
- relationship semantics;
- example records;
- validators;
- transformation warnings;
- documentation.

### Usually private/customer-specific

Likely private:

- complete QC batches;
- calibration certificates;
- proprietary SOP details;
- validation reports;
- uncertainty budgets;
- corrective-action records;
- internal audit findings;
- customer-specific mappings.

This keeps WeedDAO useful as an open standard without forcing laboratories to publish sensitive QMS records.

## Anti-monster rule

Before adding another laboratory sidecar, require all four:

1. distinct information problem not already represented;
2. real source evidence;
3. commercial/interoperability use case;
4. clear reason the concept cannot remain documentation-only.

If those conditions are not met, do not create another schema.

## Consolidation target

Once at least one real external dataset exercises each assurance layer, evaluate whether shared primitives should be factored into a common schema package:

- record/result references;
- quantities;
- evidence references;
- source literals;
- evidence status;
- timestamps.

Do **not** consolidate prematurely.

Real implementation evidence should reveal which abstractions are actually stable.

## Current architecture decision

The sidecars remain separate.

The v0.2 core remains unchanged.

**MONOLITHIC LAB SCHEMA = NOT JUSTIFIED**

**V0.2 SCHEMA CHANGE = NOT JUSTIFIED**

## Next validation milestone

The next major milestone should be an end-to-end laboratory evidence bundle in which one real result is connected through as many available layers as possible:

```text
batch
→ sampling
→ method
→ reference/calibration evidence
→ batch QC
→ result
→ uncertainty
→ decision rule
→ assessment
```

The goal is not completeness.

The goal is to discover where the current sidecars overlap, fail, or require unsupported inference before more schema growth.
