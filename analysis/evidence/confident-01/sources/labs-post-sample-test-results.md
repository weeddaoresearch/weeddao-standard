# Submit test results

`POST /v0/labs/sample/{sample_id}/test_results`

> **Authentication:** every request must send `X-ConfidentLims-APIKey`, `X-ConfidentLims-Timestamp` (unix seconds) and `X-ConfidentLims-Signature`, an HMAC-SHA256 signature of the request. The examples below call `sign_request()` from the [Request Signing guide](https://api.confidentcannabis.com/v0/docs/request-signing.md) — read it first. Request bodies are form-encoded (`application/x-www-form-urlencoded`), never JSON.

Submit test results for a sample. The payload surface is deliberately large so
that it can describe any assay, but you only need to send what was actually
tested - never include compounds that were not tested.

Results may be submitted while the sample's order is in any valid status, but
every result is stored as a DRAFT and stays invisible to the client until the
sample is published or its order moves to the completed stage. Set
`publish_data` to `true` to publish the results, together with any draft CoA and
CoA additions, as soon as they are submitted.

Each request replaces all previous test result data for the sample, so always
submit the complete set of results in one call.

## Request payload

`test_results` is a single JSON-encoded object. Build it with every tested
category, then serialize it to a string and send it as the `test_results` form
field.

```json
{
  "categories": {
    "cannabinoids": {
      "info_fields": {
        "input_units": "%",
        "report_units": "%",
        "date_tested": "2026-08-14",
        "status": 1
      },
      "compounds": [
        {"name": "thca", "value": "21.34", "lod": "0.01", "loq": "0.03"},
        {"name": "d9_thc", "value": "0.68", "lod": "0.01", "loq": "0.03"}
      ]
    }
  }
}
```

Any compound returned by `GET /compounds` may be listed, within its own
category. Setting `"skip_coa": true` alongside `categories` submits the data
without generating a CoA.

### Compound object

`name` and `value` are required; every other key is optional metadata, reported
in the same units as `value` unless noted otherwise.

- `name`: compound key for what was tested
- `value`: the test result, as a string, e.g. `"1.02"`
- `lod`: limit of detection
- `loq`: limit of quantitation
- `limit`: value above which this test fails
- `max`: upper limit of quantitation
- `spike`: spike recovery for the analyte
- `stdev`: standard deviation of the sample replicate results
- `regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `qualifiers`: testing qualifiers, where the regulator defines them
- `rsd`: relative standard deviation of the analyte values
- `rpd`: relative percent difference of the analyte values
- `limitrangehigh`: upper limit when restricting value to a range
- `limitrangelow`: lower limit when restricting value to a range
- `purity_percent`: purity percentage for the analyte

### General rules

- All test values are numeric but must be submitted as **strings**, so that JSON
  encoding and decoding cannot lose precision. Sending bare numbers will likely produce
  inaccurate data.
- Percentages are numbers between 0 and 100: report 23.1% as `23.1`, not `0.231`.
- Statuses are integer IDs: `1` passed, `2` failed, `3` completed. Completed means the assay
  could neither pass nor fail.
- `input_units` and `report_units` are required in `info_fields` for every category
  except `general`, and must come from that category's allowed units.
- `unit_weight` is required whenever a unit field for the category is `mg/unit`, and
  `ml_weight` whenever one is `mg/ml`. Both drive mass-to-mass unit conversions, so a
  conversion that needs one and does not get it fails. When testing a cookie, send the
  weight of a whole cookie; when testing a liquid, send the weight of one millilitre.
- `footnote` carries anything that should accompany the assay on the CoA - the
  definition of total THC and total CBD, dry weight versus wet weight, or other
  extraordinary QC data.

### Error codes

A failed submission returns 400 with an `error_code`, plus `error_field` and
`error_category` where they apply.

- `invalid_sample_id` - no sample found with the requested id.
- `invalid_order_status` - the sample's order cannot accept test results.
- `invalid_field` - a field or category had the wrong type, or the category is unknown.
- `unknown_compound` - an unknown compound was submitted.
- `duplicate_compound` - a compound was given twice.
- `conversion_error` - a result value could not be converted.
- `missing_required_field` - a required field is missing.
- `invalid_date` - an invalid date was given; dates are `YYYY-MM-DD`.
- `suspicious_date` - a date much older than expected (before 2012) was given.
- `invalid_status` - an invalid value was given for a status field.
- `invalid_unit` - a category was reported in an unsupported unit.
- `significant_digits_outside_range` - `digits` must be between 1 and 8 when `digits_method` is `significant`.
- `invalid_data` - any other validation failure; `error_field` and `error_category` may be absent.

## Categories

Each category below lists its allowed units, the defaults applied when a field is omitted, and every info field it accepts. The API also accepts `dna`, `miscellaneous`, `ph` and `shelflife`, which follow the same structure but have no published option set.

#### `alkaloids`

Allowed units: `%`, `mg/container`, `mg/g`, `mg/ml`, `mg/serving`, `mg/unit`, `ppb`, `ppm`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `servings_per_container`: Number of servings per container
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `units_per_serving`: Number of units per serving
- `wet_weight`: weight of aliquot as received

#### `anabolic_steroids`

Allowed units: `%`, `mg/container`, `mg/g`, `mg/ml`, `mg/serving`, `mg/unit`, `ppb`, `ppm`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `servings_per_container`: Number of servings per container
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `units_per_serving`: Number of units per serving
- `wet_weight`: weight of aliquot as received

#### `cannabinoids`

Allowed units: `%`, `mg/container`, `mg/g`, `mg/ml`, `mg/serving`, `mg/unit`, `ppb`, `ppm`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `container_description`: Description of container (eg. bottle, box, tin)
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `method`: testing method - eg, GC-FID, HPLC, etc
- `metrc_co_d9_thc_status`: pass or fail integer ID from the status enum
- `metrc_me_total_thc_mg_package_status`: pass or fail integer ID from the status enum
- `metrc_me_total_thc_mg_serving_status`: pass or fail integer ID from the status enum
- `metrc_mi_potency_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_potency_status`: pass or fail integer ID from the status enum
- `metrc_mi_potency_value`: optional value for the 'Potency' field in Metrc
- `metrc_mi_total_cbd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_total_thc_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_total_thc_status`: DEPRECATED
- `metrc_mi_total_thc_value`: DEPRECATED
- `metrc_mn_other_adc_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mn_other_adc_status`: pass or fail integer ID from the status enum
- `metrc_mn_other_adc_value`: value for the 'Other ADC (mg/g) Full Panel ' field in Metrc. value should be in mg/serving
- `metrc_mn_thc_purity_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mn_thc_purity_status`: pass or fail integer ID from the status enum
- `metrc_mn_thc_purity_value`: value for the 'THC Purity (% or mg/g)' field in Metrc
- `metrc_mn_total_cannabinoids_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mn_total_cannabinoids_status`: pass or fail integer ID from the status enum
- `metrc_mn_total_cbd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mn_total_cbd_status`: pass or fail integer ID from the status enum
- `metrc_mn_total_thc_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mn_total_thc_status`: pass or fail integer ID from the status enum
- `metrc_mt_total_cbd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mt_total_cbd_status`: pass or fail integer ID from the status enum
- `metrc_mt_total_thc_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mt_total_thc_status`: pass or fail integer ID from the status enum
- `metrc_oh_total_cbd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_oh_total_cbd_status`: pass or fail integer ID from the status enum
- `metrc_oh_total_thc_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_oh_total_thc_status`: pass or fail integer ID from the status enum
- `metrc_or_cbd_pct_rsd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_cbd_pct_rsd_status`: pass or fail integer ID from the status enum
- `metrc_or_cbd_pct_rsd_value`: Percent Relative Standard Deviation value for state traceability system
- `metrc_or_cbd_rpd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_cbd_rpd_status`: pass or fail integer ID from the status enum
- `metrc_or_cbd_rpd_value`: Relative Percent Difference value for state traceability system
- `metrc_or_d8_thc_pct_rsd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_d8_thc_pct_rsd_status`: pass or fail integer ID from the status enum
- `metrc_or_d8_thc_pct_rsd_value`: Percent Relative Standard Deviation value for state traceability system
- `metrc_or_d8_thc_rpd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_d8_thc_rpd_status`: pass or fail integer ID from the status enum
- `metrc_or_d8_thc_rpd_value`: Relative Percent Difference value for state traceability system
- `metrc_or_potency_control_study_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_potency_control_study_status`: pass or fail integer ID from the status enum
- `metrc_or_potency_process_validation_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_potency_process_validation_status`: pass or fail integer ID from the status enum
- `metrc_or_potency_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_potency_status`: pass or fail integer ID from the status enum
- `metrc_or_thc_pct_rsd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_thc_pct_rsd_status`: pass or fail integer ID from the status enum
- `metrc_or_thc_pct_rsd_value`: Percent Relative Standard Deviation value for state traceability system
- `metrc_or_thc_rpd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_thc_rpd_status`: pass or fail integer ID from the status enum
- `metrc_or_thc_rpd_value`: Relative Percent Difference value for state traceability system
- `metrc_or_total_cbd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_total_thc_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_total_thc_status`: pass or fail integer ID from the status enum
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `servings_per_container`: Number of servings per container
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `totalcbd_outsidelimitrange`
- `totalthc_outsidelimitrange`
- `unit_description`: definition of one unit when any unit fields are 'mg/unit'
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `units_per_serving`: Number of units per serving
- `wet_weight`: weight of aliquot as received

#### `endotoxins`

Allowed units: `eu/g`, `eu/mg`, `eu/ml`

Defaults: `input_units` = `eu/ml`, `report_units` = `eu/ml`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `servings_per_container`: Number of servings per container
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `units_per_serving`: Number of units per serving
- `wet_weight`: weight of aliquot as received

#### `flavonoids`

Allowed units: `%`, `mg/container`, `mg/g`, `mg/ml`, `mg/serving`, `mg/unit`, `ppb`, `ppm`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `wet_weight`: weight of aliquot as received

#### `foreign_matter`

Allowed units: `%`, `mg/lb`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `metrc_mi_foreign_organic_matter_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_foreign_organic_matter_value`: value for the 'Foreign organic matter' field in Metrc.
- `metrc_nv_visual_inspection_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum

#### `homogeneity`

Allowed units: `%`, `mg/unit`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `0`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'

#### `metals`

Allowed units: `mg/g`, `ppb`, `ppm`

Defaults: `input_units` = `ppb`, `report_units` = `ppb`, `digits` = `0`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `metrc_mi_metals_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_metals_status`: pass or fail integer ID from the status enum
- `metrc_mi_metals_value`: optional value for the 'Metals' field in Metrc
- `metrc_or_metals_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_metals_status`: pass or fail integer ID from the status enum
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum

#### `microbials`

Allowed units: `cfu`, `cfu/g`, `cfu/m^3`, `cfu/ml`, `cfu/plate`, `cq`, `mpn/g`

Defaults: `input_units` = `cfu/g`, `report_units` = `cfu/g`, `digits` = `0`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `metrc_co_microbials_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_co_microbials_status`: pass or fail integer ID from the status enum
- `metrc_co_microbials_value`: optional value for the 'Microbials' field in Metrc
- `metrc_mi_microbials_infused_bool`: boolean true/false flag (0=false/1=true) to denote if the sample is an infused product
- `metrc_mi_microbials_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_microbials_status`: pass or fail integer ID from the status enum
- `metrc_mi_microbials_value`: optional value for the 'Microbials' field in Metrc
- `metrc_nv_microbials_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_nv_microbials_status`: pass or fail integer ID from the status enum
- `metrc_nv_microbials_value`: value for the 'Microbials' field in Metrc
- `metrc_or_microbials_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_microbials_status`: pass or fail integer ID from the status enum
- `metrc_or_microbiological_process_validation_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_microbiological_process_validation_status`: pass or fail integer ID from the status enum
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `wet_weight`: weight of aliquot as received

#### `moisture`

Allowed units: `%`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `1`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `wet_weight`: weight of aliquot as received

#### `mycotoxins`

Allowed units: `mg/g`, `ppb`, `ppm`

Defaults: `input_units` = `ppb`, `report_units` = `ppb`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `metrc_mi_mycotoxins_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_mycotoxins_status`: pass or fail integer ID from the status enum
- `metrc_mi_mycotoxins_value`: optional value for the 'Mycotoxins' field in Metrc
- `metrc_or_mycotoxins_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_mycotoxins_status`: pass or fail integer ID from the status enum
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum

#### `nutrients`

Allowed units: `%`, `mg/container`, `mg/g`, `mg/ml`, `mg/serving`, `mg/unit`, `ppb`, `ppm`

Defaults: `input_units` = `ppm`, `report_units` = `ppm`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `report_units`: the primary units displayed on the certificate of analysis
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `servings_per_container`: Number of servings per container
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `units_per_serving`: Number of units per serving
- `wet_weight`: weight of aliquot as received

#### `peptides`

Allowed units: `%`, `iu`, `mg/container`, `mg/g`, `mg/ml`, `mg/serving`, `mg/unit`, `ppb`, `ppm`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `servings_per_container`: Number of servings per container
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `units_per_serving`: Number of units per serving
- `wet_weight`: weight of aliquot as received

#### `pesticides`

Allowed units: `mg/g`, `ppb`, `ppm`

Defaults: `input_units` = `ppm`, `report_units` = `ppm`, `digits` = `3`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `metrc_co_other_pesticide_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_co_other_pesticide_status`: pass or fail integer ID from the status enum
- `metrc_co_other_pesticide_value`: the sum of all pesticide detections in ppm excluding Abamectin, Azoxystrobin, Bifenazate, Etoxazole, Imazalil, Imidacloprid, Malathion, Myclobutanil, Permethrin, Spinosad, Spiromesifen, Spirotetramat, and Tebuconazole
- `metrc_co_pesticide_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_co_pesticide_status`: pass or fail integer ID from the status enum
- `metrc_co_pesticide_value`: the total sum of all pesticides detected in ppm
- `metrc_mi_pesticides_chemical_residue_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_pesticides_chemical_residue_status`: pass or fail integer ID from the status enum
- `metrc_mi_pesticides_chemical_residue_value`: optional value for the 'Chemical Residue' field in Metrc
- `metrc_or_limited_batch_pesticide_testing_regulatornotes`: DEPRECATED: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_pesticides_control_study_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_pesticides_control_study_status`: pass or fail integer ID from the status enum
- `metrc_or_pesticides_process_validation_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_pesticides_process_validation_status`: pass or fail integer ID from the status enum
- `metrc_or_pesticides_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_pesticides_status`: pass or fail integer ID from the status enum
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `volume`: volume of the aliquot in the solution
- `wet_weight`: weight of aliquot as received

#### `solvents`

Allowed units: `%`, `mg/g`, `ppb`, `ppm`

Defaults: `input_units` = `ppm`, `report_units` = `ppm`, `digits` = `3`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `metrc_co_solvents_other_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_co_solvents_other_status`: pass or fail integer ID from the status enum
- `metrc_co_solvents_other_value`: the sum of all residual solvent detections in ppm excluding Benzene, Butanes, Heptanes, Hexane, Toluene, and Total Xylenes
- `metrc_co_solvents_remediated_bool`: boolean true/false flag (0=false/1=true) to denote if the sample is from a batch made from remediated product
- `metrc_co_solvents_residual_regulatornotes`: DEPRECATED: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_co_solvents_residual_status`: DEPRECATED: pass or fail integer ID from the status enum
- `metrc_mi_solvents_residual_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_mi_solvents_residual_status`: pass or fail integer ID from the status enum
- `metrc_mi_solvents_residual_value`: optional value for the 'Residual Solvents' field in Metrc
- `metrc_or_solvents_control_study_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_solvents_control_study_status`: pass or fail integer ID from the status enum
- `metrc_or_solvents_pct_rsd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_solvents_pct_rsd_status`: pass or fail integer ID from the status enum
- `metrc_or_solvents_pct_rsd_value`: value for the 'Solvents (RPD)' field in Metrc
- `metrc_or_solvents_process_validation_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_solvents_process_validation_status`: pass or fail integer ID from the status enum
- `metrc_or_solvents_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_solvents_rpd_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_solvents_rpd_status`: pass or fail integer ID from the status enum
- `metrc_or_solvents_rpd_value`: Relative Percent Difference value for state traceability system
- `metrc_or_solvents_status`: pass or fail integer ID from the status enum
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `wet_weight`: weight of aliquot as received

#### `terpenes`

Allowed units: `%`, `mg/container`, `mg/g`, `mg/ml`, `mg/serving`, `mg/unit`, `ppb`, `ppm`

Defaults: `input_units` = `%`, `report_units` = `%`, `digits` = `2`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `container_description`: Description of container (eg. bottle, box, tin)
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `dry_weight`: weight of aliquot after drying
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `ml_weight`: the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `servings_per_container`: Number of servings per container
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum
- `totalterpenes_outsidelimitrange`
- `unit_description`: definition of one unit when any unit fields are 'mg/unit'
- `unit_weight`: the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
- `units_per_serving`: Number of units per serving
- `volume`: volume of the aliquot in the solution
- `wet_weight`: weight of aliquot as received

#### `water_activity`

Allowed units: `aw`

Defaults: `input_units` = `aw`, `report_units` = `aw`, `digits` = `5`, `digits_method` = `round`

Info fields:

- `analytical_batch_id`: optional analytical batch ID for QC samples
- `analytical_batch_id_2`: optional second analytical batch ID for QC samples
- `date_prepared`: date the sample was prepared for this assay
- `date_tested`: date the sample was tested for this assay
- `digits`: number of digits to display on the certificate of analysis; see digits_method
- `digits_method`: round rounds to digits decimal places, significant rounds to digits significant figures
- `footnote`: footnote to accompany this assay
- `input_units`: units the data is being submitted in, from the category's allowed units
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `qc_blank_dup_id`: optional sample ID for QC Blank duplicate
- `qc_blank_id`: optional sample ID for QC Blank
- `qc_blank_trip_id`: optional sample ID for QC Blank triplicate
- `qc_control_study_id`: optional sample ID for Control Study
- `qc_lcs_dup_id`: optional sample ID for QC Lab Control Sample duplicate
- `qc_lcs_id`: optional sample ID for QC Lab Control Sample
- `qc_lcs_trip_id`: optional sample ID for QC Lab Control Sample triplicate
- `qc_sample_dup_id`: optional sample ID for QC sample duplicate
- `qc_sample_id`: optional sample ID for QC sample
- `qc_sample_trip_id`: optional sample ID for QC sample triplicate
- `qc_spike_dup_id`: optional sample ID for QC Spike duplicate
- `qc_spike_id`: optional sample ID for QC Spike
- `qc_spike_trip_id`: optional sample ID for QC Spike triplicate
- `report_units`: the primary units displayed on the certificate of analysis
- `reported_as_wet`: optional flag for if numbers are reported including moisture weight (wet) or converted (dry)
- `secondary_report_units`: the secondary units displayed on the certificate of analysis
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report
- `status`: pass or fail integer ID from the status enum

#### `general`

Allowed units: none. This category carries no numeric results.

Info fields:

- `amended`: has the data been amended
- `amended_notes`: optional notes detailing the amendment to the lab data
- `footnote`: footnote to accompany this assay
- `metrc_co_contaminants_regulatornotes`: DEPRECATED: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_co_contaminants_status`: DEPRECATED: pass or fail integer ID from the status enum
- `metrc_nv_subcontract_testing_value`: DEPRECATED
- `metrc_ok_retest_all_value`: value for the 'Retest (All)' field in Metrc
- `metrc_ok_subcontract_all_value`: DEPRECATED
- `metrc_or_r_and_d_test_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_subcontracted_test_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `metrc_or_tic_regulatornotes`: notes posted to state traceability systems such as METRC or BioTrack
- `notes`, `notes_2` through `notes_10`: optional testing notes for this assay
- `retest_id`
- `retest_sample_id`
- `signatory_name`: name of lab employee to appear on certificate of analysis
- `signatory_title`: title of lab employee to appear on certificate of analysis
- `signature`: URL of the signature image for the report

## Path parameters

- `sample_id` (string, required)

## Body parameters (application/x-www-form-urlencoded)

- `publish_data` (boolean, optional, default `False`) — Publish the results, and any draft CoA and CoA additions, as soon as they are stored. Defaults to false, which leaves everything in draft.
  Example: `True`
- `date_published` (string, optional) — Publication date to record when `publish_data` is true. Defaults to the time of the request.
- `test_results` (string, required) — The results, as a JSON-encoded object. See the description above for its structure and for the fields each category accepts.
  Example:

  ```json
  {
    "categories": {
      "cannabinoids": {
        "info_fields": {
          "input_units": "%",
          "report_units": "%",
          "date_prepared": "2026-08-13",
          "date_tested": "2026-08-14",
          "method": "HPLC-DAD",
          "digits": 2,
          "status": 1
        },
        "compounds": [
          {
            "name": "thca",
            "value": "21.34",
            "lod": "0.01",
            "loq": "0.03"
          },
          {
            "name": "d9_thc",
            "value": "0.68",
            "lod": "0.01",
            "loq": "0.03"
          },
          {
            "name": "cbda",
            "value": "0.11",
            "lod": "0.01",
            "loq": "0.03"
          },
          {
            "name": "cbd",
            "value": "0.04",
            "lod": "0.01",
            "loq": "0.03"
          }
        ]
      },
      "moisture": {
        "info_fields": {
          "input_units": "%",
          "report_units": "%",
          "date_tested": "2026-08-14",
          "status": 3
        },
        "compounds": [
          {
            "name": "moisture",
            "value": "11.20"
          }
        ]
      },
      "water_activity": {
        "info_fields": {
          "input_units": "aw",
          "report_units": "aw",
          "date_tested": "2026-08-14",
          "status": 1
        },
        "compounds": [
          {
            "name": "water_activity",
            "value": "0.58",
            "limit": "0.65"
          }
        ]
      }
    }
  }
  ```

## Responses

### 200 Success

No fields beyond the success envelope.

Example:

```json
{
  "success": true
}
```

### 400 Bad request

The request was malformed or failed validation. Validation failures include per-field messages in `error_details`. Possible `error_code` values: `invalid_request`, `request_too_old`.

### 401 Unauthorized

Authentication failed. Possible `error_code` values: `missing_api_key`, `invalid_api_key`, `invalid_credentials_type`, `api_access_restricted`, `api_access_denied`, `missing_signature`, `missing_timestamp`, `invalid_timestamp`, `invalid_signature`.

### 403 Permission denied

The API key is valid but does not have permission for this endpoint (for example, a client key calling a labs endpoint). Possible `error_code` values: `permission_denied`.

### 404 Not found

The requested record does not exist or is not visible to this organization. Possible `error_code` values: `not_found`.

## Examples

### cURL

```bash
# X-ConfidentLims-Signature: see the Request Signing guide - https://api.confidentcannabis.com/v0/docs/request-signing.md
curl -X POST 'https://api.confidentcannabis.com/v0/labs/sample/{sample_id}/test_results' \
  -H 'X-ConfidentLims-APIKey: YOUR_API_KEY' \
  -H 'X-ConfidentLims-Timestamp: UNIX_TIMESTAMP' \
  -H 'X-ConfidentLims-Signature: REQUEST_SIGNATURE' \
  --data-urlencode 'test_results={
  "categories": {
    "cannabinoids": {
      "info_fields": {
        "input_units": "%",
        "report_units": "%",
        "date_prepared": "2026-08-13",
        "date_tested": "2026-08-14",
        "method": "HPLC-DAD",
        "digits": 2,
        "status": 1
      },
      "compounds": [
        {
          "name": "thca",
          "value": "21.34",
          "lod": "0.01",
          "loq": "0.03"
        },
        {
          "name": "d9_thc",
          "value": "0.68",
          "lod": "0.01",
          "loq": "0.03"
        },
        {
          "name": "cbda",
          "value": "0.11",
          "lod": "0.01",
          "loq": "0.03"
        },
        {
          "name": "cbd",
          "value": "0.04",
          "lod": "0.01",
          "loq": "0.03"
        }
      ]
    },
    "moisture": {
      "info_fields": {
        "input_units": "%",
        "report_units": "%",
        "date_tested": "2026-08-14",
        "status": 3
      },
      "compounds": [
        {
          "name": "moisture",
          "value": "11.20"
        }
      ]
    },
    "water_activity": {
      "info_fields": {
        "input_units": "aw",
        "report_units": "aw",
        "date_tested": "2026-08-14",
        "status": 1
      },
      "compounds": [
        {
          "name": "water_activity",
          "value": "0.58",
          "limit": "0.65"
        }
      ]
    }
  }
}'
```

### Python

```python
import time
import requests

# sign_request() is defined in the Request Signing guide:
# https://api.confidentcannabis.com/v0/docs/request-signing.md
from sign_request import sign_request

API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
path = '/v0/labs/sample/{sample_id}/test_results'

data = {
    "test_results": "{\n  \"categories\": {\n    \"cannabinoids\": {\n      \"info_fields\": {\n        \"input_units\": \"%\",\n        \"report_units\": \"%\",\n        \"date_prepared\": \"2026-08-13\",\n        \"date_tested\": \"2026-08-14\",\n        \"method\": \"HPLC-DAD\",\n        \"digits\": 2,\n        \"status\": 1\n      },\n      \"compounds\": [\n        {\n          \"name\": \"thca\",\n          \"value\": \"21.34\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        },\n        {\n          \"name\": \"d9_thc\",\n          \"value\": \"0.68\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        },\n        {\n          \"name\": \"cbda\",\n          \"value\": \"0.11\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        },\n        {\n          \"name\": \"cbd\",\n          \"value\": \"0.04\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        }\n      ]\n    },\n    \"moisture\": {\n      \"info_fields\": {\n        \"input_units\": \"%\",\n        \"report_units\": \"%\",\n        \"date_tested\": \"2026-08-14\",\n        \"status\": 3\n      },\n      \"compounds\": [\n        {\n          \"name\": \"moisture\",\n          \"value\": \"11.20\"\n        }\n      ]\n    },\n    \"water_activity\": {\n      \"info_fields\": {\n        \"input_units\": \"aw\",\n        \"report_units\": \"aw\",\n        \"date_tested\": \"2026-08-14\",\n        \"status\": 1\n      },\n      \"compounds\": [\n        {\n          \"name\": \"water_activity\",\n          \"value\": \"0.58\",\n          \"limit\": \"0.65\"\n        }\n      ]\n    }\n  }\n}",
    # optional form fields go here - they are signed too
}

headers = {'X-ConfidentLims-Timestamp': str(int(time.time()))}
headers['X-ConfidentLims-Signature'] = sign_request(
    'POST', path, headers, data, API_KEY, API_SECRET)
headers['X-ConfidentLims-APIKey'] = API_KEY

response = requests.post(
    'https://api.confidentcannabis.com' + path,
    headers=headers,
    data=data,
)
print(response.json())
```

### JavaScript

```javascript
// signRequest() is defined in the Request Signing guide:
// https://api.confidentcannabis.com/v0/docs/request-signing.md
import { signRequest } from './sign_request.js';

const API_KEY = 'YOUR_API_KEY';
const API_SECRET = 'YOUR_API_SECRET';
const path = "/v0/labs/sample/{sample_id}/test_results";

const data = {
  "test_results": "{\n  \"categories\": {\n    \"cannabinoids\": {\n      \"info_fields\": {\n        \"input_units\": \"%\",\n        \"report_units\": \"%\",\n        \"date_prepared\": \"2026-08-13\",\n        \"date_tested\": \"2026-08-14\",\n        \"method\": \"HPLC-DAD\",\n        \"digits\": 2,\n        \"status\": 1\n      },\n      \"compounds\": [\n        {\n          \"name\": \"thca\",\n          \"value\": \"21.34\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        },\n        {\n          \"name\": \"d9_thc\",\n          \"value\": \"0.68\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        },\n        {\n          \"name\": \"cbda\",\n          \"value\": \"0.11\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        },\n        {\n          \"name\": \"cbd\",\n          \"value\": \"0.04\",\n          \"lod\": \"0.01\",\n          \"loq\": \"0.03\"\n        }\n      ]\n    },\n    \"moisture\": {\n      \"info_fields\": {\n        \"input_units\": \"%\",\n        \"report_units\": \"%\",\n        \"date_tested\": \"2026-08-14\",\n        \"status\": 3\n      },\n      \"compounds\": [\n        {\n          \"name\": \"moisture\",\n          \"value\": \"11.20\"\n        }\n      ]\n    },\n    \"water_activity\": {\n      \"info_fields\": {\n        \"input_units\": \"aw\",\n        \"report_units\": \"aw\",\n        \"date_tested\": \"2026-08-14\",\n        \"status\": 1\n      },\n      \"compounds\": [\n        {\n          \"name\": \"water_activity\",\n          \"value\": \"0.58\",\n          \"limit\": \"0.65\"\n        }\n      ]\n    }\n  }\n}",
  // optional form fields go here - they are signed too
};

const headers = { 'X-ConfidentLims-Timestamp': String(Math.floor(Date.now() / 1000)) };
headers['X-ConfidentLims-Signature'] = signRequest(
  "POST", path, headers, data, API_KEY, API_SECRET);
headers['X-ConfidentLims-APIKey'] = API_KEY;

const response = await fetch("https://api.confidentcannabis.com" + path, {
  method: "POST",
  headers,
  body: new URLSearchParams(data),
});
console.log(await response.json());
```

---

HTML version: https://api.confidentcannabis.com/v0/docs/labs/post-sample-test-results  
OpenAPI spec for this section: https://api.confidentcannabis.com/v0/docs/labs/openapi.json  
Request Signing guide: https://api.confidentcannabis.com/v0/docs/request-signing.md
