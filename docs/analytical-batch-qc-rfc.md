# WeedDAO Analytical Batch QC RFC

**Status:** experimental companion RFC  
**Branch:** `registry-rfc`  
**Schema:** `schemas/weeddao-analytical-batch-qc-0.1-draft.schema.json`  
**Reviewed:** 2026-09-20  
**Relationship to v0.2:** sidecar only; no change to `weeddao-record-v0.2-draft.schema.json`

## Why this exists

A COA can contain a valid-looking result even when the analytical run that produced it had quality-control problems.

WeedDAO therefore needs to preserve evidence about whether an analytical batch was in control.

This is distinct from:

- the reported result itself;
- method validation;
- sampling representativeness;
- measurement uncertainty;
- calibration/traceability evidence.

The analytical-batch QC layer answers:

> What controls were run with this batch, what were their acceptance criteria, did they pass, and what happened when they did not?

## Evidence basis

This layer is consistent with laboratory quality systems and cannabis analytical practice.

NIST cannabis laboratory-quality work focuses on comparability and measurement assurance across laboratories.

ASTM D37.03 and AOAC cannabis method-performance frameworks rely on laboratory controls, performance criteria, and continuing assurance of analytical validity.

ISO/IEC 17025 quality-system practice also requires monitoring the validity of results and handling nonconforming work.

## Architecture

The sidecar has four major concepts:

1. **Analytical batch**
2. **QC observations**
3. **Nonconforming work**
4. **Batch disposition**

### Analytical batch

A batch groups the results and controls produced under one analytical run or sequence.

It can preserve:

- batch identifier;
- method IDs;
- instrument/system IDs;
- start/end timestamps;
- result paths;
- controls;
- nonconforming events;
- final disposition.

### QC observations

Supported control types include:

- reagent blank;
- method blank;
- calibration blank;
- matrix blank;
- negative control;
- positive control;
- laboratory control sample;
- matrix spike;
- matrix spike duplicate;
- sample duplicate;
- surrogate;
- internal standard;
- initial calibration verification;
- continuing calibration verification;
- continuing calibration blank;
- reference-material control.

The model supports source-reported values and acceptance criteria without forcing one universal QC formula.

## Acceptance criteria

A QC observation may carry:

- minimum;
- maximum;
- range;
- target ± tolerance;
- qualitative criterion;
- source-reported criterion.

Do not infer a criterion from a generic industry norm.

The acceptance criterion should come from:

- the laboratory SOP;
- validated method;
- regulatory requirement;
- standard method;
- source record.

## QC outcomes

A control may be:

- pass;
- fail;
- warning;
- not evaluated;
- unknown.

A failed control does not automatically mean every result is invalid.

The next question is what the laboratory did about it.

## Nonconforming work

When a control fails, the sidecar can preserve:

- triggering control IDs;
- description;
- impact assessment;
- affected result paths;
- immediate action;
- corrective action;
- whether reanalysis was performed;
- authorized disposition.

This distinction matters.

A competent laboratory may:

- identify a failing control;
- demonstrate the issue was isolated;
- repeat a subset of analyses;
- invalidate affected results;
- rerun the entire batch.

WeedDAO should preserve that evidence rather than making an independent validity judgment.

## Batch disposition

Supported batch dispositions:

- accepted;
- accepted with qualification;
- rejected;
- reprocessed;
- retested;
- pending;
- unknown.

The disposition represents the source laboratory's documented decision when available.

It is not a WeedDAO certification.

## Internal standards and surrogates

These are related but not interchangeable.

An internal standard may be used for quantitation or correction.

A surrogate may be used to monitor recovery or process performance.

Do not normalize either one into a generic `control=true` field.

## Matrix spike vs laboratory control sample

These also serve different purposes.

A laboratory control sample tests method/system performance in a controlled matrix.

A matrix spike evaluates analyte recovery in the actual sample matrix.

WeedDAO keeps them separate because matrix effects are a major analytical issue in cannabis products.

## Duplicates

Duplicate evidence may include:

- sample duplicate;
- matrix spike duplicate;
- replicate preparation;
- replicate analysis.

A reported relative percent difference or another precision metric should be preserved with its source acceptance criterion.

## Continuing calibration verification

Calibration establishment and calibration verification are different.

The traceability sidecar captures the calibration evidence.

This QC sidecar captures whether ongoing analytical performance remained acceptable during the batch.

A calibration curve created at the beginning of a run does not prove the system remained in control throughout the sequence.

## Public COA limitations

Most public COAs do not expose complete analytical-batch QC.

That is expected.

This sidecar is likely to become most useful for:

- laboratory integrations;
- audit packages;
- validation packages;
- regulatory investigations;
- customer migration projects;
- dispute resolution;
- private data-quality audits.

Missing QC data must not be interpreted as evidence that controls were absent.

## Non-goals

This RFC does not:

- decide whether a result is scientifically valid;
- calculate recovery or RPD unless explicitly requested by another workflow;
- replace the laboratory QMS;
- score laboratories;
- certify ISO/IEC 17025 compliance;
- infer corrective action;
- automatically invalidate batches;
- modify WeedDAO v0.2-draft.

## First validation set

Collect examples containing:

1. passing method blanks;
2. failed blanks;
3. matrix spikes and recoveries;
4. duplicate/RPD criteria;
5. surrogate recovery;
6. continuing calibration verification;
7. batch rejection;
8. partial reanalysis;
9. qualified acceptance;
10. corrective action.

For each example ask:

- Can the control be represented without losing its type?
- Can its acceptance criterion be preserved?
- Can its outcome remain separate from sample results?
- Can failed controls be linked to only the affected results?
- Can the laboratory's disposition be preserved without WeedDAO making a new judgment?

## Schema decision

The evidence supports an analytical-batch QC companion model.

It does **not** justify changing the v0.2 core.

**V0.2 SCHEMA CHANGE = NOT JUSTIFIED**

## Next step: architecture consolidation

WeedDAO now has multiple evidence sidecars.

The next task should not be another isolated sidecar.

The next task is to define the **WeedDAO Laboratory Assurance Architecture** so the layers share common linkage patterns and do not drift into overlapping schemas.

No affiliation, accreditation, certification, or endorsement is implied.
