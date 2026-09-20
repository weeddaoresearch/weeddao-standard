# Registry utility proof — effective-date change monitoring

**Status:** experimental proof, not a compliance service

The five-jurisdiction seed can now do more than answer point-in-time queries. The registry includes an effective-date diff tool:

```bash
python scripts/diff_registry.py --from-date YYYY-MM-DD --to-date YYYY-MM-DD
```

The purpose is to prove the shape of a future regulatory-intelligence product without building a hosted monitoring platform before customer demand exists.

## Proof 1 — California rule activation

California's Phase I pesticide records begin on **2026-10-01**.

Compare the day before and the effective date:

```bash
python scripts/diff_registry.py \
  --jurisdiction US-CA \
  --from-date 2026-09-30 \
  --to-date 2026-10-01
```

The diff should expose the Phase I requirements as newly applicable.

A point-in-time query on 2026-09-19 correctly excludes those future records, while the same query after the effective date includes them.

## Proof 2 — California Phase I to Phase II

```bash
python scripts/diff_registry.py \
  --jurisdiction US-CA \
  --from-date 2028-03-31 \
  --to-date 2028-04-01
```

The tool distinguishes:

- **MODIFIED** requirements when semantics or thresholds change;
- **SOURCE_TRANSITION** when a new rule record takes over but the normalized requirement semantics stay the same.

This matters because a regulatory update can require customer review even when a particular analyte limit does not change.

## Proof 3 — one analyte across states

```bash
python scripts/query_registry.py \
  --analyte WDA-AN-000016 \
  --as-of 2026-10-01
```

The same stable analyte ID can retrieve Abamectin requirements from multiple jurisdictions while preserving each regulator's:

- source-native units;
- product scope;
- effective dates;
- source provenance;
- regulator-specific identifiers.

## Proof 4 — not everything is a scalar threshold

The same registry also contains:

- Texas required-test and package-reporting rules;
- Massachusetts laboratory qualification, contamination reporting, and full-panel workflow;
- New York report-results-only microbial semantics and TIC pesticide reporting.

The query/diff layer must therefore preserve requirement type instead of flattening every rule into a single "limit" table.

## What the commercial product could add

The public proof does **not** monitor the web or decide applicability for a customer.

A paid WeedDAO regulatory-intelligence layer could later add:

- monitored authoritative sources;
- regulator-document fingerprints;
- revision detection;
- human-reviewed structured diffs;
- customer-specific impact mapping;
- method / LOQ / data-field impact analysis;
- alerts and scheduled summaries;
- hosted API access;
- audit history;
- links to conformance re-validation when a rule change affects an implementation.

## Guardrail

Do not market this RFC branch as complete compliance coverage.

The useful commercial promise would eventually be closer to:

> WeedDAO tracks structured cannabis-testing rule changes and shows what changed, where it came from, and which customer mappings may be affected.

That promise should only be made after source monitoring, review workflow, and coverage standards are operational.
