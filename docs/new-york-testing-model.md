# New York registry proof — revision-heavy limits, report-only tests, and result semantics

**Status:** experimental registry evidence  
**As of:** 2026-09-19  
**Scope:** narrow New York OCM seed. This is not a complete compliance ruleset.

New York is the fifth jurisdiction represented in the WeedDAO registry.

## A regulator-maintained testing-limits document changes frequently

The New York Office of Cannabis Management's current Cannabis Testing Limits document is revision-dated **February 9, 2026** and includes a detailed revision history spanning pesticides, metals, product categories, cannabinoids, residual solvents, microbial rules, terpenes, and other testing requirements.

This is exactly the kind of source that benefits from a time-aware registry rather than hard-coded application logic.

## Same analyte IDs, another regulatory context

New York Table 8 currently lists:

| WeedDAO ID | Target | New York limit |
|---|---|---:|
| `WDA-AN-000016` | Abamectin | 0.500 ppm |
| `WDA-AN-000017` | Acephate | 0.400 ppm |

For Abamectin, OCM uses CAS `71751-41-2`, matching the Oregon source and differing from the California DCC source already preserved in the analyte registry.

## Heavy-metal limits vary by route

New York's current Table 5 applies different oral and inhalation limits.

| WeedDAO ID | Target | Oral | Inhalation |
|---|---|---:|---:|
| `WDA-AN-000012` | Arsenic | 1.50 µg/g | 0.200 µg/g |
| `WDA-AN-000013` | Cadmium | 0.500 µg/g | 0.200 µg/g |
| `WDA-AN-000014` | Lead | 0.500 µg/g | 0.500 µg/g |
| `WDA-AN-000015` | Mercury | 3.00 µg/g | 0.100 µg/g |

The testing-limits document states that topicals use the oral limits.

This reinforces that WeedDAO needs product/use scope in addition to analyte + jurisdiction.

## "Required test" does not always mean "action limit"

For specified adult-use unextracted cannabis products, New York requires Total Viable Aerobic Bacteria Count and Total Yeast/Mold Count testing but treats the results as **Report Results Only** with no defined adult-use limit.

That distinction is important for interoperability:

- test required;
- result must be reported;
- no scalar pass/fail threshold in the applicable table.

A rules engine that assumes every required test must have a numeric action limit would get this wrong.

## Result-state semantics can be regulatory

New York instructs laboratories to use **TIC** ("tentatively identified, but not quantitatively confirmed") for certain pesticide results where standards do not permit quantitative confirmation.

That is another example of result semantics WeedDAO should preserve as data, not flatten into detected / not detected / numeric-only models.

## Potency and homogeneity are workflow rules too

The current testing-limits document requires Total THC to always be reported, uses different labeled-potency acceptance ranges for medical and adult-use products, and defines homogeneity testing for applicable concentrates and edible products.

It also requires five samples across an applicable lot for potency testing and describes a within-lot concentration rule.

These requirements demonstrate that regulatory intelligence includes:

- formulas and derived metrics;
- reporting obligations;
- product-type applicability;
- sampling rules;
- ranges rather than single thresholds.

## Laboratory qualification

The OCM Part 130 audit checklist requires ISO/IEC 17025 accreditation (or an Office-approved accreditation based on it) and recurring ISO/IEC 17043-approved proficiency testing.

This adds another independently sourced lab-qualification model to the registry.

## Why New York is commercially interesting

New York's revision history shows a recurring operational problem for laboratories and software vendors: even when the underlying regulation remains recognizable, the detailed testing limits, units, product applicability, reporting semantics, and analyte lists can change.

A future WeedDAO change-monitoring layer could answer:

- What changed between OCM testing-limit revisions?
- Which customer methods or data fields are affected?
- Did a test move from pass/fail to report-only or vice versa?
- Did a CAS identifier, action limit, or applicable product category change?
- Does a LIMS mapping still represent the current OCM rule correctly?

## Sources

- New York Office of Cannabis Management, Cannabis Testing Limits, revision February 9, 2026.
- New York OCM Part 130 Checklist, Version 5, effective January 30, 2026.
