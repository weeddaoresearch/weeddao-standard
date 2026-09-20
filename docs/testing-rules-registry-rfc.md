# RFC — WeedDAO Testing Rules Registry

**Status:** experimental / request for comments  
**Registry draft:** `0.1-draft`

## Problem

Cannabis testing requirements vary by jurisdiction and change over time. A static spreadsheet or hard-coded integration can become stale when required panels, analytes, limits, reporting rules, or effective dates change.

WeedDAO proposes a source-linked, versioned rules registry designed for machine-readable comparison and change tracking.

## Core model

A rule record identifies:

- the jurisdiction;
- issuing authority;
- regulatory or policy source;
- publication and effective dates;
- status;
- product / matrix scope;
- requirement type;
- relevant WeedDAO analyte ID or test category where applicable;
- comparator and threshold where applicable;
- source citation;
- supersession relationship.

## Requirement types

Initial draft vocabulary:

- `required_test`
- `action_limit`
- `reporting_requirement`
- `lod_loq_requirement`
- `method_requirement`
- `sampling_rule`
- `retest_rule`
- `other`

This vocabulary is intentionally extensible.

## Temporal versioning

Rules must be queryable by date.

A rule record should distinguish:

- publication date;
- effective start date;
- optional effective end date;
- active / future / superseded / withdrawn status;
- predecessor / successor rules.

The registry should make it possible to answer:

> What rules applied to this matrix in this jurisdiction on this date?

and:

> What changed between two effective dates?

## Source-of-truth requirement

A regulatory entry should not exist without authoritative source evidence.

Each entry should include one or more sources such as:

- regulation;
- statute;
- agency rulemaking;
- official guidance;
- official testing technical document.

Source metadata should include a stable citation and URL where possible. Future implementations may also store a cryptographic fingerprint of the source document used to build the record.

## Relationship to the Analyte Registry

When a rule applies to a specific target, it should reference a stable WeedDAO `analyte_id`.

Example:

```json
{
  "requirement_type": "action_limit",
  "analyte_id": "WDA-AN-000123"
}
```

This avoids duplicating unstable free-text names across every jurisdictional rule.

## Thresholds and units

Thresholds should preserve:

- comparator;
- numeric value;
- unit;
- unit notation / system;
- source-native expression;
- matrix or product scope.

The registry should not silently convert a regulatory threshold into another unit without retaining the original expression and transformation provenance.

## Change feed

A future hosted WeedDAO service could publish machine-readable diffs such as:

- new requirement;
- removed requirement;
- threshold changed;
- unit changed;
- method requirement changed;
- effective date changed;
- reporting requirement changed.

That service is a potential commercial layer above the open registry.

## Legal posture

The registry is structured regulatory data, not legal advice.

Every customer-facing implementation should:

- link back to authoritative sources;
- expose effective dates;
- distinguish sourced text from WeedDAO normalization;
- avoid claiming legal completeness unless a reviewed service explicitly provides it;
- provide a correction process.

## Governance questions for review

1. What is the minimum authoritative source required for a rule?
2. How should emergency rules and temporary guidance be represented?
3. Should one record represent one atomic requirement or a regulatory section?
4. How should jurisdictional product categories map across states?
5. How should rules with formula-based thresholds be modeled?
6. What review cadence is required before a jurisdiction can be called "monitored"?
7. What should be open versus commercial in the change-monitoring layer?

## Non-goals

This registry does not:

- provide legal advice;
- guarantee that a jurisdiction's rules are complete;
- replace regulator publications;
- certify laboratory compliance;
- decide whether a product may legally be sold.
