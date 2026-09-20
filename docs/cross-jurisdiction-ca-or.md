# Cross-jurisdiction proof — California vs Oregon

**Status:** experimental registry evidence  
**As of:** 2026-09-19  
**Scope:** Abamectin and Acephate only. This is not a complete compliance comparison.

This comparison demonstrates why WeedDAO needs stable analyte identifiers and time-aware testing rules.

## Same WeedDAO IDs, different rules

| WeedDAO ID | Target | California Phase I — inhalable | California Phase I — non-inhalable | Oregon active action level |
|---|---|---:|---:|---:|
| `WDA-AN-000016` | Abamectin | 0.10 µg/g | 0.3 µg/g | 0.5 ppm |
| `WDA-AN-000017` | Acephate | 0.10 µg/g | 5.0 µg/g | 0.4 ppm |

California Phase I becomes effective **2026-10-01**. Oregon's currently encoded Table 3 rule is effective **2022-03-31** and remains the active rule represented in this seed as of the date above.

For mass-per-mass concentration, 1 µg/g is numerically equivalent to 1 ppm, but the registry preserves the source-native unit expression instead of rewriting the regulator's text.

## A useful edge case discovered immediately

The two regulators use different CAS identifiers for the target labeled **Abamectin**:

- California DCC final text: `65195-55-3`
- Oregon OHA Table 3: `71751-41-2`

WeedDAO does **not** silently discard this disagreement or choose one regulator's identifier as universally correct.

Instead, `WDA-AN-000016` remains provisional and records both identifiers with source/context provenance.

That is exactly the type of problem a canonical registry must solve: identity should not be reduced to one free-text name or one external identifier without context.

Acephate provides the control case: both jurisdictions identify it as CAS `30560-19-1`, while still applying materially different action levels.

## Time-aware California comparison

California's approved rule also establishes Phase II values beginning **2028-04-01**:

| WeedDAO ID | Target | CA Phase II — inhalable | CA Phase II — non-inhalable |
|---|---|---:|---:|
| `WDA-AN-000016` | Abamectin | 0.10 µg/g | 0.10 µg/g |
| `WDA-AN-000017` | Acephate | 0.10 µg/g | 0.18 µg/g |

The analyte ID stays the same. The rule record changes by jurisdiction, product scope, and effective date.

## Why this matters commercially

A future WeedDAO rules service can answer questions such as:

- What action level applies to this analyte, product type, jurisdiction, and date?
- What changes on the next effective date?
- Which customer's method or LOQ may be affected?
- Does a source system use an external identifier that conflicts with another jurisdiction's identifier?
- Which data exports will need mapping or validation updates?

The **open registry** can define the identifiers and sourced rules.

The **commercial layer** can provide monitoring, diffs, customer-specific impact analysis, private mappings, alerts, hosted APIs, and later cryptographic conformance attestations.

## Sources

California: Department of Cannabis Control, DCC-2025-03-R Final Text of Regulations, approved/filed July 27, 2026 and effective October 1, 2026.

Oregon: OAR 333-007-0400 and Exhibit A Table 3, effective March 31, 2022.

Oregon OHA is conducting additional cannabis-testing rulemaking in 2026. Proposed changes are not treated as active requirements in this seed.
