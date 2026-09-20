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
- [Registry seed notes](docs/registry-seed-notes.md)
- [Registry validator](scripts/validate_registries.py)

## Current scope

This branch now includes a **small evidence-grounded seed**, but it does **not** claim that WeedDAO maintains a complete analyte registry or complete regulatory rules database.

The current seed contains 19 provisional analyte IDs and a deliberately narrow California pesticide rules example. Population remains evidence-driven, starting with analytes and requirements encountered in public COAs, authoritative regulatory sources, external implementations, and paid customer work.

## Validate

```bash
python scripts/validate_registries.py
```

The validator checks schema validity, duplicate identifiers, and rule-to-analyte references.
