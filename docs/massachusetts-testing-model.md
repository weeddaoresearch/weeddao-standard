# Massachusetts registry proof — lab-centric rules, product-specific limits, and machine-readable opportunity

**Status:** experimental registry evidence  
**As of:** 2026-09-19  
**Scope:** narrow Massachusetts testing seed. This is not a complete compliance ruleset.

Massachusetts adds a fourth regulatory model to the WeedDAO registry and exposes several capabilities that a durable testing-data layer should support.

## Independent testing laboratory model

Massachusetts law requires marijuana and marijuana products to be tested by an Independent Testing Laboratory before sale or marketing. The statutory definition requires Commission licensure, ISO/IEC 17025 accreditation by an accepted accrediting body or Commission approval, financial independence, and qualification to test cannabis.

This differs sharply from the Texas TCUP structure and confirms that WeedDAO should model the **testing actor / laboratory qualification model** separately from the analyte result itself.

## Product-use-specific metal limits

The Commission's current published Exhibit 4 applies different heavy-metal upper limits based on product use.

### All Uses

| WeedDAO ID | Metal | Upper limit |
|---|---|---:|
| `WDA-AN-000012` | Arsenic (inorganic) | 200 µg/kg |
| `WDA-AN-000013` | Cadmium | 200 µg/kg |
| `WDA-AN-000014` | Lead | 500 µg/kg |
| `WDA-AN-000015` | Mercury (total) | 100 µg/kg |

### Ingestion Only

| WeedDAO ID | Metal | Upper limit |
|---|---|---:|
| `WDA-AN-000012` | Arsenic (inorganic) | 1500 µg/kg |
| `WDA-AN-000013` | Cadmium | 500 µg/kg |
| `WDA-AN-000014` | Lead | 1000 µg/kg |
| `WDA-AN-000015` | Mercury (total) | 1500 µg/kg |

The protocol also requires an additional oral-consumption-only warning for products evaluated under the ingestion-only limits.

This is another reason a rule cannot be keyed only by analyte + jurisdiction. **Intended use / product scope matters.**

## Full-panel testing workflow

Administrative Order No. 4, effective April 1, 2025, requires one test sample package to be submitted to a single Independent Testing Laboratory for all required compliance testing.

That is a workflow rule rather than an analyte limit, so WeedDAO models it as a `sampling_rule`.

## Reporting and release controls

Massachusetts law requires an ITL to report contamination results to the Commission within 72 hours of identification. Current regulations also require tested products to meet Commission standards before market release and include a +/-10% potency-variance rule for single servings.

These are operational constraints that belong in a regulatory-intelligence layer even though they do not map to one analyte.

## Active 2026 review — do not encode proposals as active law

Massachusetts is actively reviewing cannabis testing regulations and protocols in 2026. The Commission solicited feedback in August 2026 and stated that the review would begin in September.

Earlier 2026 recommendations addressed microbial methods, reporting standardization, sampling/analysis, and pesticides. Those recommendations were explicitly described as non-final.

WeedDAO therefore records the currently effective rules and keeps the 2026 review as a monitoring signal rather than converting recommendations into active requirements.

## Open testing data creates a strong online opportunity

The Massachusetts Cannabis Control Commission publishes machine-readable testing data through its public data catalog, including CSV and JSON datasets. The catalog states that testing data is released with a six-month lag.

That creates a valuable WeedDAO proof path:

1. map public Massachusetts test-result fields to WeedDAO IDs;
2. compare source-native labels and units against the canonical registry;
3. test result-state normalization on a large public state dataset;
4. build jurisdiction-aware validation examples;
5. demonstrate change impact when the Commission revises its testing protocols.

This is useful evidence without requiring private customer data.

## Governance signal

As amended effective April 19, 2026, M.G.L. c.94G §15 requires the Commission to review testing regulations and protocols at least once every two years and post review reports online in machine-readable format.

That requirement aligns unusually well with the WeedDAO rules-registry model: **versioned requirements, effective dates, source provenance, and machine-readable change history.**

## Sources

- Massachusetts General Laws c.94G §§1 and 15.
- 935 CMR 500.160.
- CCC Exhibit 4 — metals limits, revised December 30, 2021.
- CCC Administrative Order No. 4, effective April 1, 2025.
- CCC testing-protocol review notices and recommendations issued in 2026.
- CCC public data catalog.
