# WeedDAO ↔ OpenTHC Result-Semantics Crosswalk

**Status:** experimental RFC companion  
**Reviewed:** 2026-09-19  
**Branch:** `registry-rfc`

## Why this exists

Identifier interoperability and semantic interoperability are different problems.

WeedDAO can map an analyte identifier cleanly to WCIA/OpenTHC and still lose meaning when translating the corresponding laboratory result.

The result layer therefore needs its own crosswalk.

The core rule is:

> Preserve distinctions that the source establishes, and do not manufacture equivalence merely because two systems use similar labels.

## WeedDAO result model

WeedDAO v0.2-draft separates:

- `result_state`
- `measurements[]`
- `limits[]`
- `assessment`
- `reported_as`

That separation is intentional.

A numeric result can coexist with an independent regulatory assessment. A source literal such as `ND` or `<LOQ` can be retained even when the normalized state is known. Multiple originally reported units can coexist without choosing a preferred representation.

## Reviewed OpenTHC result model

The reviewed OpenTHC `Lab_Result_Metric` model exposes:

- `qom` — Quantity of Measure
- `uom` — Unit of Measure
- `lod`
- `loq`
- `limit`
- `status`

The published status enum includes:

- `fail`
- `na`
- `nd`
- `nr`
- `nt`
- `pass`

OpenTHC also publishes special quantity concepts including:

- `N/A` — Not Applicable
- `N/T` — Not Tested
- `LT-LOD` — Less Than Level of Detection
- `GT-LOD / LT-LOQ` — trace amount between LOD and LOQ lower bound
- `LOQ-LB`
- `LOQ-UB`
- `GT-LOQ`

These are useful interoperability targets, but they are not interchangeable with every WeedDAO state.

## Important mappings

### ND

WeedDAO:

`result_state=not_detected`

OpenTHC:

`status=nd`

This is compatible for the normalized state.

However, WeedDAO may also retain:

`reported_as="ND"`

The reviewed OpenTHC result schema does not expose an equivalent raw-source-literal field.

Therefore a strict round trip can lose the literal even when the normalized state maps cleanly.

**Never convert ND to numeric zero.**

## Below reporting threshold

WeedDAO deliberately has a broad normalized state:

`result_state=below_reporting_limit`

with `limits[]` and/or `reported_as` preserving source detail.

OpenTHC publishes more specific concepts:

- below LOD
- greater than LOD but below LOQ

Those concepts are narrower.

A source value reported only as:

`<LOQ`

does **not** by itself prove whether it is:

- below LOD; or
- detected between LOD and LOQ.

Therefore WeedDAO must not automatically translate generic `<LOQ` into either OpenTHC special state.

That requires additional source context.

## NOT_TESTED vs NOT_PERFORMED

OpenTHC explicitly exposes Not Tested through `nt` / `N/T`.

WeedDAO distinguishes:

- `not_tested`
- `not_performed`

No distinct Not Performed concept was identified in the reviewed OpenTHC result model.

Therefore:

`WeedDAO not_tested → OpenTHC nt`

is compatible.

But:

`WeedDAO not_performed → OpenTHC nt`

is **not** safe by default.

Doing that would collapse two distinct source meanings.

## NOT_REPORTED

OpenTHC's published status enum includes `nr`, but the reviewed result schema does not expand its meaning.

It is therefore treated as a **requires-context** candidate for WeedDAO `not_reported`, not a proven unconditional equivalence.

## Measurements and units

A WeedDAO result may preserve multiple concurrent measurements, for example:

- %
- mg/g
- mg/serving
- mg/package

The reviewed OpenTHC core result metric exposes one `qom` / `uom` pair per metric.

That means a direct one-record transformation cannot necessarily preserve every originally reported representation.

Do not silently choose one unit and discard the others for archival conversion.

## Limits

Two mappings are straightforward:

- WeedDAO `LOD` → OpenTHC `lod`
- WeedDAO `LOQ` → OpenTHC `loq`

WeedDAO also distinguishes:

- reporting limit
- action limit
- regulatory limit
- other

OpenTHC exposes a more generic `limit` described as an upper limit below which the sample passes.

Mapping multiple WeedDAO limit types into that single field is therefore context-dependent and potentially lossy.

## Assessment

WeedDAO keeps result state separate from assessment.

Example:

```text
result_state = detected
assessment = fail
```

OpenTHC can represent the fail signal with `status=fail`, but the compact status no longer independently expresses that the analyte was also numerically detected.

This distinction matters in real COAs.

## Corpus checks

Representative WeedDAO corpus cases were reviewed:

- **COA-002** — ND values map to OpenTHC `nd`, but the source literal may not round-trip.
- **COA-001** — `<LOQ` cannot safely be coerced into either OpenTHC LT-LOD or GT-LOD/LT-LOQ without more context.
- **COA-001** — NOT_PERFORMED has no exact reviewed OpenTHC core equivalent.
- **COA-029** — concurrent % and mg/g values exceed a simple one-qom/one-uom target representation.
- **COA-046** — a detected Total THC result with FAIL assessment and four concurrent units shows why analytical state, assessment, and measurements must remain separable.

## Result

The first result-semantics crosswalk confirms that WeedDAO preserves information that can be lost in a naïve translation to the reviewed OpenTHC core result model.

That is not a reason to replace OpenTHC.

It is a reason to provide a safe bridge.

The intended pattern remains:

**WCIA/OpenTHC identifiers ↔ WeedDAO semantics ↔ TestSpecs ↔ customer dependencies**

## Machine-readable file

See:

`compatibility/wcia-openthc-result-semantics-0.1-draft.json`

## Schema decision

No new WeedDAO schema gap was revealed by this exercise.

The current v0.2-draft model already represents the tested distinctions.

**SCHEMA CHANGE = NOT JUSTIFIED**

## Next evidence needed

Before building a transformation engine, validate this crosswalk against at least one:

1. real OpenTHC/WCIA implementation;
2. software-vendor export;
3. laboratory integration;
4. paid customer dataset.

Any future mapping rule should be driven by observed source behavior rather than inferred from names alone.

## Sources reviewed

- `openthc/api/openapi/components/schema/Lab_Result_Metric.yaml`
- `openthc/api/etc/lab-metric-qom.yaml`
- `openthc/api/json-example/openthc/lab-result.json`
- WeedDAO `schemas/weeddao-record-v0.2-draft.schema.json`
- WeedDAO v0.2-draft corpus mappings

No affiliation or endorsement is implied.
