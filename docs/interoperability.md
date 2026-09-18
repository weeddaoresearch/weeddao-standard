# Interoperability guidance — v0.1-alpha

This draft aims to be a **shared data language** that different platforms and organizations can map to — not a replacement for existing grow software, LIMS, ERP, or research databases.

> Different platforms. Different organizations. One shared data language.

## Goals

- Make export/import of cultivation + lab summaries predictable
- Preserve units and provenance across system boundaries
- Allow partial records (only required fields + whatever the source system knows)
- Avoid forcing a single vendor’s internal model onto everyone else

## Mapping strategy

1. **Identify required fields** — Always emit `schema_version`, `record_id`, `cultivation_batch_id`, `created_at`.
2. **Map what you have** — Omit or null optional sections you cannot populate.
3. **Preserve units** — Convert into the explicit WeedDAO field units (Celsius, %, kPa, ppm, µmol/m²/s, mol/m²/day, grams, mS/cm) rather than inventing parallel fields with ambiguous units.
4. **Label provenance** — If a value came from a sensor vs a typed form vs a COA, set the corresponding provenance method.
5. **Mark gaps** — Use `null` + `not_measured` / `not_applicable` / `withheld` instead of sentinel numbers.
6. **Namespace leftovers** — Put unmapped vendor fields under `extensions["your.org.prefix"]`.

## Suggested mappings (illustrative)

| Common source concept | WeedDAO target |
|----------------------|----------------|
| Batch / lot id | `cultivation_batch_id` |
| Strain / cultivar marketing name | `cultivar.reported_name` + `identity_status: "reported"` |
| Genetic assay accession | `cultivar.genetic_verification` + `identity_status: "genetically_verified"` |
| Room temp average (day) | `environment.average_day_temp_c` (convert °F → °C) |
| RH average | `environment.average_rh_percent` |
| VPD | `environment.average_vpd_kpa` |
| PPFD | `environment.ppfd_umol_m2_s` |
| DLI | `environment.dli_mol_m2_day` |
| COA THC / THCA / CBD… | `lab_results.cannabinoids.*` |
| Terpene panel rows | `lab_results.terpenes[]` |
| Pesticide panel | `lab_results.safety.pesticides` |
| Dry flower mass | `harvest.dry_weight_g` |

These mappings are **examples for implementers**, not certified integrations.

## Round-tripping

When importing a WeedDAO record into an internal model:

- Keep `record_id` / `cultivation_batch_id` as external references if your system uses different primary keys
- Do not silently drop provenance or gap status
- If you must flatten `{value, unit}` pairs, retain unit in a parallel column and reject ambiguous unitless numbers for regulated analytics where possible

## Partial interoperability

A system that only understands harvest weights and lab cannabinoids can still emit a valid record: required fields + `harvest` + `lab_results.cannabinoids`. Receivers should not require full environmental telemetry.

## Version negotiation

Receivers should inspect `schema_version`. For this draft, accept only `"0.1-alpha"` or explicitly document any compatibility shims. Do not assume forward compatibility with future draft numbers.

## Out of scope

- Real-time streaming protocols
- Authentication / authorization between organizations
- Payment or settlement layers
- Blockchain or token bridges

Interoperability here means **data shape and semantics**, not network topology.
