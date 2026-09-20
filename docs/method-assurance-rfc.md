# WeedDAO Method Assurance RFC

**Status:** experimental companion RFC  
**Branch:** `registry-rfc`  
**Schema:** `schemas/weeddao-method-assurance-0.1-draft.schema.json`  
**Reviewed:** 2026-09-20  
**Relationship to v0.2:** sidecar only; no change to `weeddao-record-v0.2-draft.schema.json`

## Why this exists

A COA field such as:

```text
Method: LC-MS/MS
```

does not establish that the exact analytical procedure was validated for:

- the reported analyte;
- the tested matrix;
- the reported concentration range;
- the laboratory/site performing the work;
- the current procedure revision.

WeedDAO therefore needs to distinguish **method identity** from **method qualification evidence**.

## Evidence basis

This layer is evidence-backed.

- ASTM D8282-26 states that fitness for intended purpose is demonstrated through method characterization and validation, and separately addresses method transfer.
- AOAC SMPRs define minimum performance characteristics and may be used in on-site verification, single-laboratory validation, and multi-site collaborative studies.
- NIST CannaQAP asks participants to report sample-preparation and analytical methods specifically so potential method-related bias can be examined.
- NIST's 2025 moisture work showed materially different results across laboratories using different drying methods, underscoring that method identity and procedure details can affect comparability.

## Critical distinctions

### Technique is not method

`LC-MS/MS`, `LC-UV`, `GC-FID`, or `ICP-MS` describe analytical techniques.

They do not uniquely identify the method.

A defensible method identity may also require:

- standard or official-method identifier;
- laboratory SOP identifier;
- revision/version;
- effective date;
- source reference;
- laboratory modification status.

### Validation is not verification

A method may have been validated elsewhere and then verified by a user laboratory for local use.

WeedDAO keeps separate event types for:

- characterization;
- validation;
- verification;
- method transfer;
- revalidation.

Do not rewrite all of these as `validated=true`.

### Method validity is scope-dependent

A method can be fit for:

- flower;

but not automatically:

- gummies;
- beverages;
- vape oil;
- topicals.

Likewise, validation for one analyte or concentration range does not prove fitness for every analyte or range.

The sidecar therefore makes scope explicit:

- analytes;
- matrices;
- product types;
- quantitative/qualitative use;
- working range;
- limitations.

### Standard method does not mean automatically fit for local use

Referencing ASTM, AOAC, USP, FDA, EPA, or another published method does not by itself prove:

- the lab implemented it correctly;
- the exact matrix is in scope;
- modifications were validated;
- local verification was completed;
- the current revision was used.

## Architecture

The sidecar has three main concepts:

1. **Method identity**
2. **Qualification events**
3. **Result-to-method linkage**

### Method identity

A method can preserve:

- WeedDAO-local `method_id`;
- title;
- type;
- external standard reference;
- internal SOP ID;
- revision;
- effective date;
- analytical technique;
- optional platform;
- literal source representation.

### Qualification events

Each event can represent:

- characterization;
- validation;
- verification;
- transfer;
- revalidation.

The event may carry:

- study design;
- status;
- performer;
- acceptance framework;
- validated/verified scope;
- performance characteristics;
- evidence reference.

### Performance characteristics

The sidecar supports source-reported evidence for characteristics such as:

- accuracy;
- bias;
- precision;
- repeatability;
- intermediate precision;
- reproducibility;
- recovery;
- selectivity/specificity;
- linearity;
- working range;
- LOD;
- LOQ;
- robustness;
- measurement uncertainty;
- probability of detection.

These are evidence slots, not requirements that every method must contain every characteristic.

Different method types require different demonstrations.

## AOAC compatibility

AOAC SMPRs are particularly useful as external acceptance frameworks because they define minimum performance expectations for specified analytes and matrices.

For example, AOAC SMPR 2022.001 applies to quantitative cannabinoid methods in beverage matrices and explicitly frames method evaluation as verification, single-laboratory validation, or multi-site collaborative study.

WeedDAO should preserve a reference such as:

```text
acceptance_framework = "AOAC SMPR 2022.001"
```

without copying copyrighted standards text into the registry.

## ASTM compatibility

ASTM D8282-26 is useful as a method-assurance framework because it distinguishes:

- characterization;
- validation;
- transfer.

Current ASTM D37.03 also maintains specific cannabis/hemp analytical methods for cannabinoids, pesticides, elements, sample preparation, and laboratory operations.

WeedDAO should preserve exact standard identifiers/revisions rather than a generic statement such as:

```text
ASTM method
```

## NIST relevance

NIST's cannabis program is focused on measurement comparability rather than merely instrument output.

CannaQAP participants were asked to report their normal analytical and preparation methods so NIST could examine potential method bias.

This supports a central WeedDAO principle:

> The method is part of the meaning of a measurement result.

## Result linkage

A single COA may use different methods for:

- cannabinoids;
- pesticides;
- heavy metals;
- microbiology;
- moisture.

The sidecar therefore links each method to specific result paths.

Example:

```json
{
  "result_path": "/lab_results/cannabinoids/total_thc",
  "method_id": "LAB-SOP-CAN-004-R7"
}
```

This is safer than storing one generic COA-level method string.

## Within-scope flag

`within_claimed_scope` is intentionally nullable.

Only set:

```json
"within_claimed_scope": true
```

when the available evidence establishes that the specific result's:

- analyte;
- matrix;
- intended use;
- range;

fall within the claimed qualification scope.

Do not infer it from laboratory reputation or accreditation alone.

## Deviations

A laboratory may depart from its method/SOP for legitimate reasons.

The sidecar can preserve:

- deviation identity;
- description;
- whether authorization was reported;
- whether impact was assessed;
- impact summary.

A deviation must not automatically mean the result is invalid.

Likewise, an authorized deviation must not automatically mean the result is unaffected.

WeedDAO records what the source establishes.

## What not to claim

Do not use this model to assert:

- “ISO 17025 compliant method” without evidence;
- “validated for all cannabis matrices” from a single-matrix study;
- “AOAC validated” merely because AOAC performance criteria were consulted;
- “ASTM validated” merely because an ASTM practice was followed;
- “NIST validated” because a NIST method or RM was used.

## Public COA behavior

Most public COAs expose only a method name, code, or technique.

That is still useful.

A sparse method record is valid.

Example:

```text
method_id = source-method-1
reported_as = "SOP-12 LC-UV"
qualification_events = unknown/omitted
```

Missing validation evidence should be treated as **not demonstrated in the available source**, not as evidence that validation did not occur.

## Non-goals

This RFC does not:

- approve methods;
- validate methods;
- certify laboratory competence;
- copy proprietary SOPs;
- reproduce copyrighted standards;
- infer performance characteristics;
- calculate validation statistics;
- replace a LIMS or QMS;
- modify WeedDAO v0.2-draft.

## First validation set

Collect real records from at least:

1. a public COA with only a method code;
2. a laboratory export with SOP revision;
3. a standard-method implementation;
4. a modified standard method;
5. a laboratory-developed method;
6. an AOAC/ASTM-scoped method;
7. a method with a documented deviation;
8. a method transferred or verified at a second site.

For each, test:

- Can the exact method identity survive normalization?
- Can validation and verification remain distinct?
- Can analyte × matrix × range scope be represented?
- Can a result be linked to the correct method?
- Can an unsupported “within scope” conclusion be avoided?

## Schema decision

The evidence supports a companion method-assurance model.

It does **not** justify modifying `AnalyteResult` or the v0.2 core record.

**V0.2 SCHEMA CHANGE = NOT JUSTIFIED**

## Next laboratory layer

After validating this sidecar with real method records, the next highest-value laboratory RFC should be:

**reference materials + calibration + metrological traceability**

That layer must connect a measurement result to:

- calibration/reference material identity;
- lot/certificate;
- assigned value;
- uncertainty;
- calibration chain;
- traceability claim evidence;

without reducing traceability to a misleading boolean.

## Reference anchors

- ASTM D8282-26 — Standard Practice for Laboratory Test Method Validation and Method Development
- ASTM D37.03 laboratory standards portfolio
- AOAC Standard Method Performance Requirements for cannabis analytical methods
- NIST Tools for Cannabis Laboratory Quality Assurance
- NIST CannaQAP reports

No affiliation, accreditation, validation, endorsement, or conformity claim is implied.
