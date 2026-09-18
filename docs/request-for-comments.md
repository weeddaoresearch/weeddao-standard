# Request for Comments — WeedDAO Open Cannabis Data Standard v0.1-alpha

**Draft:** `0.1-alpha`  
**Date opened:** 2026-09-18  
**Status:** Open for comment  

This RFC invites technical and domain feedback on the experimental cultivation record schema and accompanying documents.

## Purpose of this RFC

We are proposing a **shared data language** for cultivation and related lab summaries so that different platforms and organizations can exchange information more consistently.

This is a **proposed, under-development** open standard. It is:

- Not regulatory
- Not a certification scheme
- Not finalized
- Not a claim of industry adoption

Positioning reminder: **Different platforms. Different organizations. One shared data language.** — as a coordination layer, not a replacement for growers, labs, researchers, or software.

## Artifacts under review

| Artifact | Path |
|----------|------|
| Schema | `schemas/weeddao-cultivation-record-v0.1-alpha.schema.json` |
| Specification | `docs/specification-v0.1-alpha.md` |
| Field reference | `docs/field-reference.md` |
| Interoperability | `docs/interoperability.md` |
| Privacy | `docs/privacy.md` |
| Examples | `examples/*.json` |
| Validator | `scripts/validate.py` |

## Questions we especially want feedback on

1. **Required set** — Are `schema_version`, `record_id`, `cultivation_batch_id`, and `created_at` the right minimal required fields?
2. **Environment units** — Are Celsius / % / kPa / ppm / µmol/m²/s / mol/m²/day the right defaults for a cross-jurisdiction exchange format?
3. **Cannabinoid shape** — Is `{value, unit}` per analyte preferable to a flat numeric map?
4. **Terpene extensibility** — Is an open array sufficient, or should `0.1-alpha` ship a recommended name vocabulary?
5. **Cultivar identity** — Is the `reported` vs `genetically_verified` split clear enough for seed-to-sale and research use?
6. **Provenance enum** — Missing methods? Overlap between `third_party_verified` and `laboratory_verified`?
7. **Missing-data semantics** — Does `null` + `not_measured` / `not_applicable` / `withheld` cover real export cases without magic numbers?
8. **Safety block** — Right level of detail for optional contaminant panels?
9. **Extensions** — Should top-level `additionalProperties` stay open, or should non-`extensions` extras be forbidden?
10. **Privacy** — Any field that accidentally encourages PII collection?

## How to comment

- Open an issue describing the problem, impact, and a concrete proposal when possible
- Reference field paths (e.g. `environment.average_vpd_kpa`)
- Include sample JSON when proposing shape changes
- Note your perspective (grower tooling, LIMS, research, regulator observer, etc.) without requiring personal contact details in the record examples themselves

See also [CONTRIBUTING.md](../CONTRIBUTING.md) and [GOVERNANCE.md](../GOVERNANCE.md).

## Out of scope for this RFC

- Blockchain, tokens, NFTs, or crypto asset designs
- Building a full market platform or certification body
- Replacing laboratory methods or agronomic standards of practice
- Declaring a post-alpha version number in this comment period

## Success criteria for the comment period

Useful outcomes include clarified field definitions, better enums, improved examples/tests, documented mappings from existing systems, and privacy hardening — not marketing claims or premature “final” branding.

Thank you for reviewing this experimental draft.
