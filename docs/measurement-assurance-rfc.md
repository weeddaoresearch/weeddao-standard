# WeedDAO Measurement Assurance RFC — Uncertainty + Decision Rules

**Status:** experimental companion RFC  
**Branch:** `registry-rfc`  
**Schema:** `schemas/weeddao-measurement-assurance-0.1-draft.schema.json`  
**Reviewed:** 2026-09-20  
**Relationship to v0.2:** sidecar only; no change to `weeddao-record-v0.2-draft.schema.json`

## Why this exists

WeedDAO v0.2-draft can preserve the reported analytical result:

- state;
- measurements;
- units;
- limits;
- assessment;
- literal source representation.

That is necessary, but it is not always enough to explain a conformity decision.

A result near a regulatory or specification limit may depend on:

- measurement uncertainty;
- the specification itself;
- the decision rule;
- whether uncertainty was considered;
- guard bands;
- rounding conventions.

Therefore this RFC introduces a narrow **measurement-assurance sidecar** that links uncertainty and conformity-decision evidence to a specific WeedDAO result.

It does not redesign the core result model.

## Evidence basis

This is not speculative.

### USDA hemp testing

USDA hemp laboratory requirements explicitly call for measurement uncertainty to be estimated and reported with total delta-9 THC results.

That establishes cannabis/hemp regulatory relevance for uncertainty as a first-class result attribute.

### NIST

NIST's metrological-traceability policy treats traceability as a property of a **measurement result**, supported by a documented unbroken chain of calibrations and associated uncertainties.

NIST's cannabis quality-assurance work and reference-material programs reinforce the importance of comparable, fit-for-purpose measurements and documented uncertainty.

### ISO/IEC 17025 / ILAC

ILAC G17 addresses uncertainty in testing.

ILAC G8 addresses decision rules and statements of conformity under ISO/IEC 17025.

The important architectural consequence is that:

```text
measurement result
!=
conformity decision
```

and:

```text
uncertainty
!=
pass/fail
```

They are related evidence layers.

## Design goals

The sidecar must:

1. attach assurance evidence to a specific result;
2. preserve source-reported uncertainty without inventing missing parameters;
3. distinguish expanded, standard, relative and source-reported uncertainty;
4. preserve coverage factor and confidence/coverage information when known;
5. represent decision rules independently from analytical state;
6. preserve the specification/limit used in a decision;
7. record whether uncertainty was considered;
8. permit guard-band and rounding metadata;
9. avoid claiming traceability from uncertainty alone;
10. remain optional.

## Result linkage

Each sidecar entry uses a JSON Pointer:

```json
{
  "result_path": "/lab_results/cannabinoids/total_thc"
}
```

This intentionally keeps assurance evidence outside `AnalyteResult`.

The same analytical result can remain portable even when one system does not carry assurance metadata.

## Measurement uncertainty

Example:

```json
{
  "uncertainty": {
    "kind": "expanded",
    "value": 0.6,
    "unit": "mg/g",
    "coverage_factor": 2,
    "confidence_level_percent": 95,
    "reported_as": "±0.6 mg/g (k=2)"
  }
}
```

Do not infer:

- `k=2`;
- 95% confidence;
- GUM compliance;
- a particular calculation method;

unless the source establishes it.

A source that merely reports:

```text
MU = 8%
```

should be preserved as source-reported/relative uncertainty rather than normalized beyond the evidence.

## Decision rules

Example:

```json
{
  "decision_rule": {
    "rule_type": "guard_band",
    "uncertainty_considered": true,
    "specification": {
      "operator": "<=",
      "value": 10.0,
      "unit": "mg/g",
      "source": "example specification"
    },
    "guard_band": {
      "value": 0.5,
      "unit": "mg/g"
    },
    "assessment": "fail"
  }
}
```

The sidecar must not recompute or override the source COA assessment unless an explicit transformation/audit workflow is requested.

Its first purpose is preservation.

## Unknown decision rules

A COA may state PASS or FAIL without disclosing the laboratory's decision rule.

Represent that honestly:

```json
{
  "decision_rule": {
    "rule_type": "unknown",
    "uncertainty_considered": null,
    "assessment": "pass"
  }
}
```

Do not assume simple acceptance merely because no guard band is printed.

## Traceability guardrail

This RFC deliberately does **not** include a boolean such as:

```text
nist_traceable = true
```

That would be too easy to misuse.

Metrological traceability requires evidence linking the measurement result through calibrations/reference standards with stated uncertainties.

Reference-material and calibration-chain modeling should be a separate future RFC grounded in real laboratory exports.

## Public COAs vs private laboratory data

Most public COAs will not expose:

- full uncertainty budgets;
- calibration records;
- QC batch evidence;
- guard-band calculations.

That is acceptable.

The sidecar should remain sparse for public COAs and richer for:

- laboratory integrations;
- audit projects;
- migration projects;
- regulatory-impact analysis;
- customer-supplied private data.

Absence of assurance metadata must never be interpreted as poor laboratory performance.

## Non-goals

This RFC does not:

- calculate uncertainty;
- validate a laboratory's uncertainty budget;
- certify ISO/IEC 17025 compliance;
- establish NIST traceability;
- recalculate PASS/FAIL;
- rank laboratories;
- create a LIMS;
- replace an accreditation body;
- modify WeedDAO v0.2-draft.

## Next validation set

Before expanding the model, collect real examples containing:

- absolute uncertainty;
- relative uncertainty;
- expanded uncertainty;
- coverage factor;
- confidence/coverage statement;
- source decision-rule text;
- explicit guard bands;
- pass/fail results close to limits;
- uncertainty reported separately from COA values.

For each example test:

1. source → sidecar preservation;
2. sidecar → source reconstruction;
3. whether any source meaning is lost;
4. whether fields remain optional when the source is silent.

## Schema decision

The current evidence supports a companion assurance model.

It does **not** justify modifying `AnalyteResult`.

**V0.2 SCHEMA CHANGE = NOT JUSTIFIED**

## Next laboratory RFC after validation

If this sidecar survives real lab examples, the next high-value companion model should be:

**sampling representativeness + sampling plan**

because analytical uncertainty and sampling uncertainty are different, and a defensible laboratory result still may not represent the batch if sampling was poor.

## Reference anchors

- NIST Policy on Metrological Traceability
- NIST Tools for Cannabis Laboratory Quality Assurance
- NIST cannabis/hemp reference-material program
- ILAC G17 — measurement uncertainty in testing
- ILAC G8 — decision rules and statements of conformity
- USDA hemp testing laboratory requirements

No affiliation, accreditation, endorsement, or traceability claim is implied.
