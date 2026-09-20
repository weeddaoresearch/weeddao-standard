# WeedDAO Registry RFCs

**Status:** experimental companion RFCs  
**Branch:** `registry-rfc`  
**Relationship to v0.2:** these registries are **not part of the v0.2-draft schema** and do not change the v0.2 external-review candidate.

WeedDAO is exploring two companion registries that could make cannabis testing data easier to exchange across laboratories, software platforms, jurisdictions, and research systems:

1. **Canonical Analyte Registry** — stable identifiers for testing targets and their source-native aliases.
2. **Testing Rules Registry** — versioned, source-linked machine-readable testing requirements by jurisdiction and effective date.

The design goal is to create reusable identifiers and rules without forcing laboratories or regulators to replace their existing systems.

## Design principles

- **Stable IDs, mutable labels.** A registry identifier should remain stable even if preferred display names or aliases evolve.
- **Source meaning is preserved.** Registry mapping must not silently rewrite or infer source-native meaning.
- **Time matters.** Regulatory rules must carry effective dates and supersession history.
- **Evidence is required.** Regulatory entries must point to authoritative source material.
- **No legal interpretation by default.** The registry represents sourced requirements and structured metadata; it is not legal advice.
- **Open core.** Registry schemas and identifiers are intended to remain publicly implementable.
- **Commercial services may sit above the open registry.** Change monitoring, impact analysis, private mappings, hosted verification, and implementation support can remain commercial.
- **No change to v0.2 during review.** These companion RFCs are deliberately isolated on this branch.

## Files

- [Canonical Analyte Registry RFC](docs/analyte-registry-rfc.md)
- [Testing Rules Registry RFC](docs/testing-rules-registry-rfc.md)
- [Analyte Registry draft schema](schemas/weeddao-analyte-registry-0.1-draft.schema.json)
- [Testing Rule draft schema](schemas/weeddao-testing-rule-0.1-draft.schema.json)
- [Illustrative analyte record](examples/registries/analyte-example.json)
- [Illustrative testing rule](examples/registries/testing-rule-example.json)
- [Initial analyte seed](registry/analytes/seed-0.1-draft.json) — 19 provisional IDs grounded in existing COA evidence plus two DCC pesticide targets
- [California pesticide rule seed](registry/rules/us-ca-dcc-pesticides-seed-0.1-draft.json) — narrow Phase I/II example from authoritative DCC final text
- [Oregon pesticide rule seed](registry/rules/us-or-oha-pesticides-seed-0.1-draft.json) — active OHA/OAR Table 3 example
- [Texas TCUP rule seed](registry/rules/us-tx-dps-tcup-seed-0.1-draft.json) — required testing categories, reporting requirements, and current dosage-unit definition
- [Massachusetts CCC rule seed](registry/rules/us-ma-ccc-testing-seed-0.1-draft.json) — ITL requirements, metal limits, reporting, potency variance, and full-panel workflow
- [New York OCM rule seed](registry/rules/us-ny-ocm-testing-seed-0.1-draft.json) — lab qualification, pesticides, metals, potency/homogeneity, and report-only microbial semantics
- [California vs Oregon cross-jurisdiction proof](docs/cross-jurisdiction-ca-or.md)
- [Texas regulatory-model / drift finding](docs/texas-regulatory-model.md)
- [Five-jurisdiction testing-model comparison](docs/jurisdiction-model-comparison.md)
- [Massachusetts testing-model / open-data proof](docs/massachusetts-testing-model.md)
- [New York testing-model / change-monitoring proof](docs/new-york-testing-model.md)
- [Registry query quickstart](docs/registry-query-quickstart.md)
- [Cross-jurisdiction query CLI](scripts/query_registry.py)
- [Effective-date change diff CLI](scripts/diff_registry.py)
- [Change-monitoring utility proof](docs/registry-change-monitoring-proof.md)
- [Authoritative source watch index](registry/source-watch-0.1-draft.json) — manual index only; no automated-monitoring claim
- [Registry seed notes](docs/registry-seed-notes.md)
- [Registry validator](scripts/validate_registries.py)
- [WCIA / OpenTHC interoperability crosswalk](docs/wcia-openthc-crosswalk.md)
- [Machine-readable WCIA crosswalk](compatibility/wcia-analyte-crosswalk-0.1-draft.json)
- [Identifier crosswalk CLI](scripts/crosswalk_analyte_ids.py)
- [OpenTHC result-semantics interoperability crosswalk](docs/wcia-openthc-result-semantics.md)
- [Machine-readable result-semantics crosswalk](compatibility/wcia-openthc-result-semantics-0.1-draft.json)
- [Result-semantics crosswalk query CLI](scripts/crosswalk_result_semantics.py)
- [Laboratory measurement-assurance roadmap](docs/laboratory-measurement-assurance-roadmap.md)
- [Measurement assurance example](examples/registries/measurement-assurance-example.json)
- [Sampling assurance example](examples/registries/sampling-assurance-example.json)
- [Method assurance example](examples/registries/method-assurance-example.json)
- [Method assurance draft schema](schemas/weeddao-method-assurance-0.1-draft.schema.json)
- [Method assurance RFC](docs/method-assurance-rfc.md)
- [Sampling assurance draft schema](schemas/weeddao-sampling-assurance-0.1-draft.schema.json)
- [Sampling assurance RFC](docs/sampling-assurance-rfc.md)
- [Measurement assurance draft schema](schemas/weeddao-measurement-assurance-0.1-draft.schema.json)
- [Measurement assurance RFC](docs/measurement-assurance-rfc.md)

## Current scope

This branch now includes a **small evidence-grounded seed**, but it does **not** claim that WeedDAO maintains a complete analyte registry or complete regulatory rules database.

The current seed contains 19 provisional analyte IDs plus deliberately narrow California, Oregon, Texas, Massachusetts, and New York rule examples. Population remains evidence-driven, starting with analytes and requirements encountered in public COAs, authoritative regulatory sources, external implementations, and paid customer work.

## Validate

```bash
python scripts/validate_registries.py
```

The validator checks schema validity, duplicate identifiers, and rule-to-analyte references.
