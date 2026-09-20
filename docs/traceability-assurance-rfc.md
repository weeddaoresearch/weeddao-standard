# WeedDAO Traceability Assurance RFC

**Status:** experimental companion RFC  
**Branch:** `registry-rfc`  
**Schema:** `schemas/weeddao-traceability-assurance-0.1-draft.schema.json`  
**Reviewed:** 2026-09-20  
**Relationship to v0.2:** sidecar only; no change to `weeddao-record-v0.2-draft.schema.json`

## Why this exists

WeedDAO now has companion models for:

- reported result semantics;
- measurement uncertainty and decision rules;
- sampling assurance;
- analytical method assurance.

The next question is whether a measurement result can be connected to the references and calibration evidence that support a claim of metrological traceability.

NIST is explicit that metrological traceability is a property of a **measurement result**, not an instrument, certificate, laboratory, or reference material. It requires a documented unbroken calibration chain, with each link contributing to measurement uncertainty.

Therefore WeedDAO must not reduce traceability to a boolean.

## Evidence basis

NIST states that:

- traceability belongs to the measurement result;
- merely having an instrument calibrated by NIST is insufficient;
- merely purchasing or using an SRM is insufficient;
- each link in the calibration chain must be documented;
- uncertainty must accompany the measurement result;
- providers are responsible for supporting their own traceability claims.

NIST also distinguishes Certified Reference Materials from other reference materials and ties certified values to uncertainty and traceability statements.

NIST RM 8210 Hemp Plant demonstrates a cannabis-relevant reference material with assigned values and documented uncertainty for cannabinoids and toxic elements.

## Architecture

The sidecar has three evidence layers:

1. **Reference materials**
2. **Calibration events**
3. **Result-specific traceability claims**

### Reference materials

A material record may preserve:

- material type: CRM, RM, SRM, calibration standard, control material;
- producer;
- catalog number;
- lot/batch;
- certificate identifier/revision;
- validity/expiration;
- intended use;
- assigned value(s);
- uncertainty;
- coverage factor/confidence;
- traceability statement;
- storage conditions;
- source reference.

Do not assume every NIST material is an SRM. RM 8210, for example, is a NIST Reference Material, not automatically a Certified Reference Material or SRM.

### Calibration events

Calibration evidence may preserve:

- instrument/system identity;
- calibration date;
- provider;
- certificate;
- reference standard identifiers;
- measurands;
- reported uncertainty;
- validity interval.

A calibration record does not by itself prove the downstream analytical result is traceable.

## Result-specific claim

Every claim attaches to a result path.

Example:

```json
{
  "result_path": "/lab_results/cannabinoids/total_thc"
}
```

The claim status can be:

- `source_claimed`
- `evidence_partial`
- `evidence_complete`
- `not_demonstrated`
- `unknown`

These are evidence states, not WeedDAO certification labels.

### Important guardrail

`evidence_complete` means the attached dataset contains the evidence elements the integration expects for the claim.

It does **not** mean WeedDAO independently certifies that a regulator, accreditation body, NIST, or another authority would accept the claim.

## Traceability chain evidence

A robust traceability claim may need:

- identified measurand;
- measurement result;
- associated measurement uncertainty;
- calibrated measurement system/working standard;
- reference standard identity;
- uncertainty for each calibration link;
- relevant dates;
- measurement-assurance controls.

This is consistent with NIST's published traceability guidance.

## Reference-material guardrails

Do not write:

```text
used NIST RM → NIST traceable
```

or:

```text
instrument calibrated by NIST → result is NIST traceable
```

Those are specifically unsafe inferences.

Instead preserve:

- which material was used;
- what assigned value/certificate applied;
- how it was used;
- which calibration event relied on it;
- which analytical result the evidence supports;
- whether the source claims traceability.

## RM 8210 relevance

NIST RM 8210 Hemp Plant is directly relevant to cannabis/hemp laboratory comparability.

It provides assigned values for cannabinoids and toxic elements in a dried, ground hemp matrix and includes uncertainty characterization.

It is useful to WeedDAO as an example of how to model a matrix reference material without overstating certification status.

## Public COAs

Most public COAs will not expose enough information to support a complete traceability chain.

That is expected.

A public COA may reveal:

- method;
- standard name;
- certificate or lot;
- perhaps a calibration statement.

WeedDAO should preserve only what is visible.

More complete chains will likely come from:

- laboratory integrations;
- validation packages;
- calibration certificates;
- audit files;
- accreditation evidence;
- customer-supplied private records.

## Non-goals

This RFC does not:

- establish or certify metrological traceability;
- validate calibration certificates;
- endorse a calibration provider;
- imply NIST endorsement;
- infer traceability from a brand or certificate name;
- calculate calibration uncertainty;
- replace ISO/IEC 17025 assessment;
- turn WeedDAO into calibration-management software;
- modify v0.2-draft.

## First validation set

Collect real examples containing:

1. NIST RM/SRM use;
2. commercial CRM use;
3. calibration certificates;
4. in-house calibration standards;
5. analytical calibration curves tied to standard lots;
6. expired/replaced reference-material lots;
7. results with explicit traceability statements;
8. cases where traceability is only partially documented.

For each example ask:

- Is the reference material uniquely identified?
- Is the assigned value preserved?
- Is its uncertainty preserved?
- Is the calibration event linked?
- Is the measurement result linked?
- Does the source claim more than the evidence demonstrates?
- Can WeedDAO preserve the chain without asserting validity?

## Schema decision

The evidence supports a companion traceability-assurance model.

It does **not** justify modifying WeedDAO v0.2 core.

**V0.2 SCHEMA CHANGE = NOT JUSTIFIED**

## Next laboratory layer

After traceability examples are validated, the next highest-value companion RFC should be:

**analytical batch QC + control evidence**

including:

- blanks;
- spikes;
- duplicates;
- surrogates/internal standards;
- control samples;
- continuing calibration verification;
- acceptance criteria;
- corrective action / batch invalidation.

## Reference anchors

- NIST Policy on Metrological Traceability
- NIST Metrological Traceability FAQ
- NIST RM 8210 Hemp Plant documentation
- ILAC P10 metrological traceability policy

No affiliation, accreditation, certification, endorsement, or traceability claim is implied.
