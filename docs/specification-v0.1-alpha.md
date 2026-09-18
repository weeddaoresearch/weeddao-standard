# WeedDAO Open Cannabis Data Standard — Specification v0.1-alpha

**Status:** Experimental draft — open for comment  
**Schema:** `schemas/weeddao-cultivation-record-v0.1-alpha.schema.json`  
**JSON Schema dialect:** Draft 2020-12  
**License:** Apache-2.0  

> Different platforms. Different organizations. One shared data language.

## 1. Positioning

This document specifies a **proposed** cultivation record format intended as a **coordination and data-exchange layer** between growers, laboratories, researchers, and software systems. It does not replace those actors or their tools.

This draft is:

- **Not** a regulatory standard
- **Not** a certification or compliance scheme
- **Not** finalized
- **Not** a claim of adoption or official industry status

Comments are welcome via the [request for comments](request-for-comments.md).

## 2. Document types

The primary document type in `0.1-alpha` is the **Cultivation Record**: a JSON object describing one cultivation batch and optional related measurements and outcomes.

## 3. Conformance

A JSON document conforms to this draft if:

1. It is valid JSON.
2. It validates against `weeddao-cultivation-record-v0.1-alpha.schema.json` using a Draft 2020-12 capable validator.
3. `schema_version` is exactly `"0.1-alpha"`.
4. Required fields are present and non-empty where constrained.

Systems **MAY** store additional properties. Prefer the `extensions` object with namespaced keys for vendor-specific data to reduce collisions.

## 4. Required fields

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string (const) | Must be `"0.1-alpha"` |
| `record_id` | string | Unique record id within the producing system |
| `cultivation_batch_id` | string | Batch identifier |
| `created_at` | string (date-time) | Creation timestamp (ISO 8601; UTC recommended) |

No other fields are required. No personally identifiable information is required.

## 5. Optional top-level sections

| Section | Purpose |
|---------|---------|
| `producer` | Organization / facility metadata (non-PII preferred) |
| `cultivar` | Reported vs genetically verified identity |
| `cultivation` | Method, medium, cycle timing |
| `environment` | Climate and light with explicit units |
| `irrigation_nutrition` | Water / nutrient summary |
| `harvest` | Harvest weights and dates |
| `post_harvest` | Dry / cure parameters |
| `lab_results` | Cannabinoids, terpenes, optional safety |
| `outcomes` | Yield and quality summaries |
| `provenance` | How data was obtained |
| `extensions` | Namespaced extension bag |
| `data_gaps` | Map of paths → gap reasons |
| `updated_at` | Last update timestamp |

All of the above section objects **MAY** be omitted or set to `null`.

## 6. Units

Environment fields encode units in the field name:

| Field pattern | Unit |
|---------------|------|
| `*_temp_c`, `*_c` (temps) | Celsius |
| `*_rh_percent`, `*_percent` (humidity) | % relative humidity |
| `*_vpd_kpa` | kPa |
| `*_ppm` (CO₂ / dissolved solids as labeled) | ppm |
| `ppfd_umol_m2_s` | µmol/m²/s |
| `dli_mol_m2_day` | mol/m²/day |
| harvest `*_g` | grams |
| EC `*_ec_ms_cm` | mS/cm |

Cannabinoid and terpene measurements use `{ "value": number|null, "unit": "..." }` with constrained unit enums in the schema.

## 7. Cannabinoids and terpenes

### Cannabinoids

Under `lab_results.cannabinoids`, each of the following **MAY** appear as a `CannabinoidMeasurement`:

`thc`, `thca`, `cbd`, `cbda`, `cbg`, `cbga`, `cbc`, `cbn`, `thcv`, `total_thc`, `total_cbd`, `total_cannabinoids`

Each measurement:

```json
{ "value": 22.4, "unit": "%", "status": null, "provenance": "laboratory_verified" }
```

`unit` enum: `"%"`, `"mg/g"`, `"mg/ml"`, `"mg/serving"`.

### Terpenes

`lab_results.terpenes` is an **array** of `{ "name", "value", "unit" }` (plus optional `status`). This list is intentionally extensible.

## 8. Lab safety (optional)

`lab_results.safety` **MAY** include structures for pesticides, heavy metals, microbials, mycotoxins, and residual solvents. Absence of a safety section does **not** imply a pass or fail.

## 9. Provenance

Allowed provenance method values:

- `self_reported`
- `sensor_measured`
- `laboratory_verified`
- `third_party_verified`
- `derived`

Provenance **MAY** be attached at record level (`provenance`), section level, or on individual measurements.

## 10. Missing data

- Use JSON `null` for unknown or absent numeric/string values when the key is present.
- Document **why** with:
  - companion `status` / gap fields using `not_measured` | `not_applicable` | `withheld`, and/or
  - the top-level `data_gaps` map
- **Do not** use magic numbers (`-1`, `999`, `0` as sentinels) to mean “missing.”

## 11. Cultivar identity

- `reported_name` / `reported_type` / `breeder_reported` reflect source or grower reporting.
- `identity_status`: `reported` | `genetically_verified` | `unknown`
- Optional `genetic_verification` object holds method, lab, reference, and verified name when applicable.

Do not treat a marketing name as genetically verified unless `identity_status` and verification fields say so.

## 12. Privacy

See [privacy.md](privacy.md). The schema does not require names, emails, phone numbers, or street addresses of individuals.

## 13. Extensibility

- Top-level `additionalProperties` is allowed so implementations can experiment carefully.
- Prefer `extensions` with reverse-DNS / org-prefixed keys for durable vendor data.
- Future draft versions will be explicitly versioned; this document covers only `0.1-alpha`.

## 14. Normative references

- JSON Schema Draft 2020-12
- ISO 8601 date / date-time representations as commonly used with JSON Schema `format`

## 15. Non-goals for 0.1-alpha

- Full supply-chain track-and-trace
- Regulatory form replacements
- Ranking or certifying cultivators
- Any ledger, token, or crypto integration
