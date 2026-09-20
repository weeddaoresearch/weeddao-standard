# RFC — WeedDAO Canonical Analyte Registry

**Status:** experimental / request for comments  
**Registry draft:** `0.1-draft`

## Problem

Cannabis laboratory and software systems often refer to the same testing target using different labels, abbreviations, punctuation, casing, or vendor-specific names. A normalizer that relies only on free-text labels can become brittle, and a change in display name can break downstream mappings.

WeedDAO proposes a public registry of stable analyte / testing-target identifiers.

The registry is not intended to dictate how a laboratory must label a result in its own system. It provides a durable cross-system identity layer.

## Proposed identity model

Each target receives an immutable identifier such as:

`WDA-AN-000001`

The identifier remains stable even if:

- the preferred display name changes;
- new aliases are discovered;
- external reference identifiers are added;
- a source system changes punctuation or capitalization.

A registry record may include:

- `analyte_id` — immutable WeedDAO identifier;
- `canonical_name` — preferred neutral name;
- `target_type` — chemical, microbial, physical, derived metric, or other;
- `category` — cannabinoid, terpene, pesticide, heavy metal, residual solvent, microbial, mycotoxin, moisture, water activity, foreign material, etc.;
- `aliases[]` — source-native labels with provenance/context;
- `external_identifiers[]` — CAS, PubChem, InChIKey, regulator identifiers, vendor identifiers, or other schemes when applicable;
- `measurement_dimensions[]` — the kinds of measurement that may be reported, without forcing one unit;
- `status` — active, deprecated, or provisional;
- `replaced_by` — optional successor identifier;
- `references[]` — evidence supporting the identity or mapping.

## Why IDs must be separate from names

Names are presentation. IDs are identity.

A cannabis data standard should not require every participant to use one display string. Instead:

- laboratories can preserve their source-native label;
- WeedDAO can map that label to a stable identifier when evidence supports the mapping;
- downstream systems can compare records by ID;
- ambiguous labels can remain unmapped rather than guessed.

## Alias evidence

Aliases should carry context and provenance where possible.

Example:

```json
{
  "label": "D9 THC",
  "context": "source export label",
  "source": "example-lims"
}
```

The existence of an alias in one source does not automatically mean it is safe to apply globally.

## Measurement semantics

The registry should identify the target, not force one reporting unit.

A single analyte may appear as:

- percent by mass;
- mg/g;
- mg/unit;
- mg/package;
- concentration;
- presence/absence;
- count-based measurements.

Unit compatibility belongs in validation / measurement logic, not in the analyte identifier itself.

## Deprecation

Identifiers should not be recycled.

If an entry is later found to represent multiple distinct targets, the original record should be deprecated and point to replacement IDs. Historical records remain interpretable.

## Governance questions for review

1. Should IDs be sequential and opaque, or include semantic slugs?
2. Which external identifiers should be first-class?
3. Should microbial targets live in the same registry or a broader "testing target" registry?
4. How should stereoisomers and closely related chemical forms be represented?
5. What evidence threshold is required before an alias becomes globally accepted?
6. Should jurisdiction-specific regulator codes be aliases or external identifiers?
7. Which measurement dimensions should be normalized as controlled vocabulary?

## Non-goals

This registry does not:

- determine regulatory action limits;
- establish laboratory methods;
- certify laboratory accuracy;
- replace source-native labels;
- infer chemical equivalence from a string alone.
