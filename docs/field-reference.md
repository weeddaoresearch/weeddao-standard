# Field reference — Cultivation Record v0.1-alpha

Companion to [specification-v0.1-alpha.md](specification-v0.1-alpha.md). Field constraints are defined normatively by the JSON Schema; this document summarizes them for implementers.

**Schema version:** `0.1-alpha`

## Top-level

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `schema_version` | yes | const `"0.1-alpha"` | Must match this draft |
| `record_id` | yes | string | Opaque; UUID recommended |
| `cultivation_batch_id` | yes | string | Opaque batch id |
| `created_at` | yes | date-time | ISO 8601 |
| `updated_at` | no | date-time \| null | |
| `producer` | no | object \| null | See below |
| `cultivar` | no | object \| null | |
| `cultivation` | no | object \| null | |
| `environment` | no | object \| null | Units in field names |
| `irrigation_nutrition` | no | object \| null | |
| `harvest` | no | object \| null | |
| `post_harvest` | no | object \| null | |
| `lab_results` | no | object \| null | |
| `outcomes` | no | object \| null | |
| `provenance` | no | object \| null | Record/section methods |
| `extensions` | no | object \| null | Namespaced bag |
| `data_gaps` | no | object \| null | path → `not_measured` \| `not_applicable` \| `withheld` |

## producer

| Field | Type | Notes |
|-------|------|-------|
| `organization_name` | string \| null | Org/trade name; avoid personal names |
| `organization_id` | string \| null | Opaque |
| `facility_id` | string \| null | Opaque; no street address required |
| `jurisdiction` | string \| null | e.g. region code |
| `license_id` | string \| null | Public license id if appropriate |

## cultivar

| Field | Type | Notes |
|-------|------|-------|
| `reported_name` | string \| null | As reported |
| `reported_type` | enum \| null | `indica`, `sativa`, `hybrid`, `ruderalis`, `hemp`, `unknown` |
| `breeder_reported` | string \| null | |
| `identity_status` | enum | `reported`, `genetically_verified`, `unknown` |
| `genetic_verification` | object \| null | `method`, `laboratory`, `reference_id`, `verified_name`, `verified_at` |
| `notes` | string \| null | |

## cultivation

| Field | Type | Notes |
|-------|------|-------|
| `method` | enum \| null | `indoor`, `outdoor`, `greenhouse`, `mixed`, `other` |
| `medium` | enum \| null | `soil`, `coco`, `rockwool`, `hydroponic`, `aeroponic`, `living_soil`, `other` |
| `cycle_start` / `cycle_end` | date \| null | |
| `veg_days` / `flower_days` | integer \| null | ≥ 0 |
| `plant_count` | integer \| null | ≥ 0 |
| `notes` | string \| null | |

## environment

| Field | Unit | Notes |
|-------|------|-------|
| `average_day_temp_c` | °C | |
| `average_night_temp_c` | °C | |
| `min_temp_c` / `max_temp_c` | °C | |
| `average_rh_percent` | % | 0–100 |
| `min_rh_percent` / `max_rh_percent` | % | |
| `average_vpd_kpa` | kPa | |
| `co2_ppm` | ppm | |
| `ppfd_umol_m2_s` | µmol/m²/s | |
| `dli_mol_m2_day` | mol/m²/day | |
| `photoperiod_hours` | hours | 0–24 |
| `phase` | enum \| null | `veg`, `flower`, `full_cycle`, `other` |
| `provenance` | ProvenanceMethod | |
| `notes` | string \| null | |

## irrigation_nutrition

| Field | Notes |
|-------|-------|
| `method` | `hand_water`, `drip`, `flood`, `ebb_flow`, `nft`, `dwc`, `other` |
| `water_source` | free text |
| `average_ph` | 0–14 |
| `average_ec_ms_cm` | mS/cm |
| `average_ppm` | ppm (document scale in notes if needed) |
| `nutrient_program` | free text |
| `organic` | boolean \| null |
| `runoff_ph` / `runoff_ec_ms_cm` | optional |
| `provenance` | ProvenanceMethod |
| `notes` | string \| null |

## harvest

| Field | Unit / type |
|-------|-------------|
| `harvest_date` | date \| null |
| `wet_weight_g` | grams |
| `dry_weight_g` | grams |
| `trim_weight_g` | grams |
| `plant_count_harvested` | integer |
| `notes` | string \| null |

## post_harvest

| Field | Unit |
|-------|------|
| `dry_method` | string |
| `dry_temp_c` | °C |
| `dry_rh_percent` | % |
| `dry_days` | number |
| `cure_days` | number |
| `cure_rh_percent` | % |
| `cure_temp_c` | °C |
| `notes` | string \| null |

## lab_results

| Field | Notes |
|-------|-------|
| `lab_name` / `lab_id` | optional identifiers |
| `certificate_id` | COA / report id |
| `tested_at` | date-time |
| `sample_id` | opaque |
| `cannabinoids` | object of CannabinoidMeasurement |
| `terpenes` | array of TerpeneEntry |
| `safety` | optional LabSafety |
| `provenance` | ProvenanceMethod |
| `notes` | string \| null |

### CannabinoidMeasurement

| Field | Notes |
|-------|-------|
| `value` | number \| null |
| `unit` | `%`, `mg/g`, `mg/ml`, `mg/serving` |
| `status` | `not_measured` \| `not_applicable` \| `withheld` |
| `provenance` | ProvenanceMethod |

Keys: `thc`, `thca`, `cbd`, `cbda`, `cbg`, `cbga`, `cbc`, `cbn`, `thcv`, `total_thc`, `total_cbd`, `total_cannabinoids`.

### TerpeneEntry

| Field | Notes |
|-------|-------|
| `name` | string (required) |
| `value` | number \| null |
| `unit` | `%`, `mg/g`, `ppm` |
| `status` | gap reason optional |

### safety (optional)

Sub-objects: `pesticides`, `heavy_metals`, `microbials`, `mycotoxins`, `residual_solvents` — each may include `status` (`pass`, `fail`, `not_tested`, `partial`, `not_applicable`) and optional analyte arrays.

## outcomes

| Field | Notes |
|-------|-------|
| `yield_g_per_plant` | grams |
| `yield_g_per_m2` | grams |
| `yield_g_per_watt` | grams |
| `quality_grade` | implementation-defined label |
| `notes` | string \| null |

## provenance (record-level)

Keys may include: `record`, `environment`, `irrigation_nutrition`, `lab_results`, `cultivar`, `harvest`, `notes`.

Values use ProvenanceMethod: `self_reported` | `sensor_measured` | `laboratory_verified` | `third_party_verified` | `derived`.

## Data gaps

Example:

```json
"data_gaps": {
  "lab_results.cannabinoids.thcv": "not_measured",
  "producer.license_id": "withheld"
}
```

Never encode gaps as `-1`, `999`, or sentinel `0`.
