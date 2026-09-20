# WeedDAO Sampling Assurance RFC

**Status:** experimental companion RFC  
**Branch:** `registry-rfc`  
**Schema:** `schemas/weeddao-sampling-assurance-0.1-draft.schema.json`  
**Reviewed:** 2026-09-20  
**Relationship to v0.2:** sidecar only; no change to `weeddao-record-v0.2-draft.schema.json`

## Why this exists

Laboratory interoperability fails upstream if the tested specimen does not adequately represent the claimed batch or lot.

A technically precise analytical result can still mischaracterize a population when:

- the sampling plan is weak or undocumented;
- too few increments are collected;
- collection locations are biased;
- a composite is formed inconsistently;
- the received sample is not fully homogenized;
- the test portion is reduced nonrepresentatively.

WeedDAO already models sample lifecycle metadata. This RFC addresses a different problem: **sampling assurance and representativeness**.

## Evidence basis

This layer is not speculative.

USDA hemp testing guidance treats the laboratory sample as a **composite sample representing a lot** and requires the laboratory to homogenize the sample prior to test-portion selection.

ASTM D8334 addresses collection of harvested cannabis/hemp samples for laboratory testing and explicitly exists because batches may be heterogeneous.

NIST cannabis/hemp quality-assurance work and reference-material preparation reinforce the importance of controlled sample preparation and homogenization for comparable measurements.

## Critical distinctions

### Sample identity is not representativeness

A valid sample ID only tells us which sample was tested.

It does not prove that the sample represents:

- the full harvest batch;
- the full product batch;
- all containers;
- all spatial locations;
- the declared lot.

### Collection is not preparation

These are separate events:

1. collection from the population;
2. combining increments into a composite;
3. laboratory receipt;
4. drying or conditioning;
5. grinding/homogenization;
6. test-specimen reduction;
7. analytical measurement.

Do not collapse them into a single generic `sampled_at` event.

### Analytical uncertainty is not sampling uncertainty

The existing measurement-assurance sidecar concerns the uncertainty of the analytical result.

Sampling variation can be much larger and is governed by different evidence.

WeedDAO must not add analytical and sampling uncertainty together unless a competent source explicitly supplies a combined uncertainty model.

## Architecture

The sampling sidecar links back to a WeedDAO record and may describe one or more sampling events.

Each event can preserve:

- population/lot identity;
- declared population size;
- sampling plan;
- selection method;
- collection party;
- collection time;
- increment count;
- increment locations;
- composite formation;
- sample mass;
- drying;
- grinding;
- homogenization;
- particle-size bounds;
- test-specimen mass;
- retained specimen;
- subsampling method;
- source claim of representativeness;
- known limitations.

## Population

The population is the material the sample is intended to represent.

Examples:

- field lot;
- harvest batch;
- product batch;
- container lot.

A sampling record should not imply batch representativeness if the source only establishes a grab sample.

## Sampling plan

The sidecar supports source-reported plan types such as:

- regulatory standard;
- consensus standard;
- performance-based;
- customer-specified;
- laboratory internal;
- research.

Selection method may be:

- random;
- systematic;
- stratified;
- judgmental;
- composite protocol;
- source-reported;
- unknown.

Do not infer a statistical design merely because multiple increments were collected.

## Composite samples

When a source reports a composite sample, WeedDAO can preserve:

- whether the sample is composite;
- number of increments;
- combined mass;
- formation method;
- individual increment details when available.

A composite claim should not be invented when the COA simply says “sample.”

## Test-specimen preparation

This section exists because the transition from received sample to analytical test portion can materially affect comparability.

Potential evidence includes:

- whether the whole received sample was processed;
- drying method and endpoint;
- grinding method;
- homogenization method;
- particle-size range;
- test-specimen mass;
- retained specimen;
- subsampling method.

### Guardrail

Do not claim homogenization merely because grinding occurred.

Grinding can be part of homogenization, but the source must support the representation.

## Representativeness

The model intentionally treats representativeness as a source claim plus evidence/limitations, not as a WeedDAO-generated verdict.

Possible claims include:

- representative;
- compliance sample;
- research sample;
- grab sample;
- unknown.

WeedDAO should preserve the statement:

```text
representative compliance sample
```

when the source supports it.

It should not transform that into:

```text
statistically representative
```

unless the sampling plan establishes the statistical basis.

## What public COAs usually omit

Many COAs will not expose:

- increment locations;
- exact randomization;
- sample mass;
- composite-formation method;
- particle size;
- subsampling procedure.

That absence must remain `unknown` or omitted.

It is not evidence of poor practice.

More complete sampling records are expected in:

- regulator datasets;
- laboratory integrations;
- sampling SOPs;
- compliance audits;
- litigation/forensic workflows;
- research studies;
- customer migration projects.

## Non-goals

This RFC does not:

- certify that a sample is representative;
- compute sampling uncertainty;
- generate a sampling plan;
- replace USDA/ASTM/state protocols;
- determine compliance;
- score laboratories or samplers;
- require every COA to expose internal SOP details;
- modify v0.2-draft.

## First validation targets

Collect 5–10 real examples spanning:

1. regulatory composite sampling;
2. independent laboratory sampling;
3. client-submitted samples;
4. grab samples;
5. homogeneous manufactured products;
6. heterogeneous flower/biomass;
7. amended/recollected samples.

For each example ask:

- What population was claimed?
- How many increments were collected?
- Were locations/randomization specified?
- Was the sample composite?
- Was the entire received sample homogenized?
- How was the test portion reduced?
- What representativeness claim appears?
- What information would be lost by a flat COA model?

## Schema decision

The evidence supports a companion sampling-assurance model.

It does **not** justify modifying the WeedDAO v0.2 record.

**V0.2 SCHEMA CHANGE = NOT JUSTIFIED**

## Highest-value next lab layer

After real sampling examples are validated, the next companion RFC should be:

**method identity + method validation/verification**

That layer should distinguish:

- standard method;
- laboratory-developed method;
- modified method;
- revision/version;
- matrix/analyte scope;
- validation vs verification;
- performance characteristics;
- deviations.

## Reference anchors

- USDA hemp sampling/testing guidance for representative composite samples and laboratory homogenization
- ASTM D8334 Standard Practice for Collection of a Representative Sample of Cannabis/Hemp Post-Harvest Batch for Laboratory Testing
- NIST Tools for Cannabis Laboratory Quality Assurance
- NIST cannabis/hemp reference-material preparation work

No affiliation, accreditation, endorsement, or representativeness claim is implied.
