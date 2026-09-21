# Get sample details

`GET /v0/clients/sample/{sample_id}`

> **Authentication:** every request must send `X-ConfidentLims-APIKey`, `X-ConfidentLims-Timestamp` (unix seconds) and `X-ConfidentLims-Signature`, an HMAC-SHA256 signature of the request. The examples below call `sign_request()` from the [Request Signing guide](https://api.confidentcannabis.com/v0/docs/request-signing.md) — read it first. Request bodies are form-encoded, never JSON.

Return full details for a single sample, including its batch and lot metadata, images, Certificate of Analysis and, once results have been published, the `lab_data` test results.

`sample_id` can be the sample ID as shown in Confident, the sample's public key, or the regulator sample ID from the state's seed-to-sale tracking system. Samples on another client's orders return a 404 rather than a permission error so that sample IDs are not leaked.

## Path parameters

- `sample_id` (string, required)

## Responses

### 200 Success

Fields (alongside the `success: true` envelope flag):

- `sample` (object)
  - `id` (string) — Sample ID
  - `order_id` (string) — Orders ID
  - `client_id` (integer) — Client ID
  - `lab` (object) — Lab
    - `id` (integer) — Lab ID
    - `name` (string) — Lab Name
  - `order_status_id` (integer) — Order Status ID
  - `order_status_name` (string) — Order Status Name
  - `sample_name` (string) — Name of Sample
  - `strain_name` (string) — Name of Sample Strain
  - `sample_industry_id` (integer) — Sample Industry ID
  - `sample_industry_name` (string) — Sample Industry Name
  - `sample_category_id` (integer) — Sample Category ID
  - `sample_category_name` (string) — Sample Category Name
  - `sample_type_id` (integer) — Sample Type ID
  - `sample_type_name` (string) — Sample Type Name
  - `sample_classification_id` (integer) — Sample Classification ID
  - `sample_classification_name` (string) — Sample Classification Name
  - `production_method_name` (string) — Production Method name
  - `production_method_id` (integer) — Production Method ID
  - `regulator_sample_id` (string) — Unique ID from the state's seed-to-sale tracking system of the sample tested by the lab
  - `regulator_batch_id` (string) — Unique ID from the state's seed-to-sale tracking system of the client's batch from which the sample tested by the lab came
  - `batch_id` (string) — Unique ID from the client's inventory management system of the client's batch from which the sample tested by the lab came
  - `harvest_id` (string) — Unique ID from the state's seed-to-sale tracking system of the client's harvest lot from which the sample tested by the lab came
  - `test_packages` (array of objects)
    - `id` (integer) — Unique ID for Test Package
    - `name` (string) — Test Package Name
    - `price` (number) — Package Price - if 0, call for price
    - `minimum_quantity` (number) — Minimum sample quantity required for testing
  - `last_modified` (timestamp) — Time this sample was last modified
  - `date_published` (timestamp) — Published Date [when sample was published]
  - `initial_weight` (number) — Sample weight at order verification
  - `initial_weight_unit` (number) — Unit type for Initial Weight
  - `test_types` (array of objects)
    - `id` (integer) — Unique ID for Test Type
    - `name` (string) — Test Type Name
    - `abbreviation` (string) — Test Type Abbreviation
  - `cover_image` (object)
    - `filename` (string)
    - `public_key` (string (uuid)) — Unique public key for file
    - `url` (string) — Public URL to access file
  - `images` (array of objects) — Will also contain cover image
    - `filename` (string)
    - `public_key` (string (uuid)) — Unique public key for file
    - `url` (string) — Public URL to access file
  - `notes` (string) — Notes about the sample
  - `batch_size` (number) — Size of the client's batch from which the sample tested by the lab came
  - `batch_size_unit` (string) — Unit type for batch size (units, lb, or g)
  - `lot_id` (string) — Unique ID from the client's inventory management system of the client's lot from which the sample tested by the lab came
  - `lot_size` (number) — Size of the client's lot from which the sample tested by the lab came
  - `lot_size_unit` (string) — Unit type for lot size (units, lb, or g)
  - `production_run_id` (string) — Unique ID from the client's inventory management system of the client's production run from which the sample tested by the lab came
  - `production_run_size` (number) — Size of the client's production run from which the sample tested by the lab came
  - `production_run_size_unit` (string) — Unit type for production run size (units, lb, or g)
  - `manifest_id` (string) — Unique ID from the state's seed-to-sale tracking system of the sample manifest from which the sample tested by the lab came
  - `regulator_lot_id` (string) — Unique ID from the state's seed-to-sale tracking system of the client's lot from which the sample tested by the lab came
  - `regulator_sample_id2` (string) — (for Leaf) Pre-Transfer Batch ID
  - `regulator_batch_id2` (string) — (for Leaf) Pre-Transfer Inventory/Lot ID
  - `production_date` (timestamp) — Harvest/Production Date [when sample was produced]
  - `date_samples_collected` (timestamp) — Collection Date [when sample was collected]
  - `public_url` (string) — Unique URL for viewing this sample or CoA without requiring a login. Should be added to CoAs and used for QR codes or other barcode images so end consumers can verify the integrity of the data
  - `units_per_serving` (number) — Serving Size
  - `servings_per_container` (number) — Number of Servings in one Container
  - `unit_description` (string) — Information describing what a "unit" means for this sample (i.e 1 Bottle)
  - `container_description` (string) — Information describing what a "unit" means for this sample (i.e 1 Gummy)
  - `regulatory_category_id` (integer) — Unique ID for sample's regulatory category
  - `solvents_used` (string) — Information about the solvents used in testing
  - `has_coa` (boolean) — True if sample has a Certificate of Analysis
  - `coa` (object) — URL expires after one hour
    - `filename` (string)
    - `public_key` (string (uuid)) — Unique public key for file
    - `url` (string) — Public URL to access file
  - `coa_additions` (array of objects) — URLs expire after one hour
    - `filename` (string)
    - `public_key` (string (uuid)) — Unique public key for file
    - `url` (string) — Public URL to access file
  - `lab_data` (object)
    - `date_created` (timestamp) — Timestamp of lab data creation time
    - `date_reported` (timestamp) — date laboratory data was uploaded to Confident and the Certificate of Analysis was created
    - `status` (integer) — 1=passed, 2=failed, 3=completed. Completed means there were no limits to pass or fail
    - `thc_total` (number) — Total Percentage THC in the sample
    - `thc_calculation` (string) — The calculation used for thc_total
    - `cbd_total` (number) — Total Percentage CBD in the sample
    - `cbd_calculation` (string) — The calculation used for cbd_total
    - `cannabinoid_total` (number) — Total Percentage cannabinoids in the sample
    - `cannabinoid_calculation` (string) — The calculation used for cannabinoid_total
    - `terpene_total` (number) — Total Percentage terpenes in the sample
    - `terpene_calculation` (string) — The calculation used for terpene_total
    - `categories` (object) — test categories
      - `cannabinoids` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'mg/unit')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `method` (string) — testing method - eg, GC-FID, HPLC, etc
          - `container_description` (string) — Description of container (eg. bottle, box, tin)
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `servings_per_container` (number) — Number of servings per container
          - `unit_description` (string) — definition of one unit when any unit fields are 'mg/unit'
          - `units_per_serving` (number) — Number of units per serving
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `terpenes` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'mg/unit')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `volume` (string) — volume of the aliquot in the solution
          - `container_description` (string) — Description of container (eg. bottle, box, tin)
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `servings_per_container` (number) — Number of servings per container
          - `unit_description` (string) — definition of one unit when any unit fields are 'mg/unit'
          - `units_per_serving` (number) — Number of units per serving
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `moisture` (object) — moisture generally only has 'percent_moisture' in the compound list
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('%')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [1] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `pesticides` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['ppm'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppb', 'ppm')
          - `report_units` (string) — ['ppm'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [3] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `volume` (string) — volume of the aliquot in the solution
          - `dry_weight` (string) — weight of aliquot after drying
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to 'ppm'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'ppm'
          - `limit` (number) — value above which this test fails. unit is 'ppm'
          - `lod` (number) — limit of detection. unit is 'ppm'
          - `max` (number) — upper limit of quantitation. unit is 'ppm'
          - `loq` (number) — limit of quantitation. unit is 'ppm'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `solvents` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['ppm'] units the data is being submitted in, from the category's allowed units ('mg/g', '%', 'ppb', 'ppm')
          - `report_units` (string) — ['ppm'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [3] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to 'ppm'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'ppm'
          - `limit` (number) — value above which this test fails. unit is 'ppm'
          - `lod` (number) — limit of detection. unit is 'ppm'
          - `max` (number) — upper limit of quantitation. unit is 'ppm'
          - `loq` (number) — limit of quantitation. unit is 'ppm'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `microbials` (object) — microbial results aren't converted from their input values
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['cfu/g'] units the data is being submitted in, from the category's allowed units ('cfu/g', 'cfu', 'cfu/m^3', 'mpn/g', 'cfu/ml', 'cq', 'cfu/plate')
          - `report_units` (string) — ['cfu/g'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [0] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects)
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is the same as input_units
          - `limit` (number) — value above which this test fails. unit is the same as input_units
          - `lod` (number) — limit of detection. unit is the same as input_units
          - `max` (number) — upper limit of quantitation. unit is the same as input_units
          - `loq` (number) — limit of quantitation. unit is the same as input_units
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `mycotoxins` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['ppb'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppb', 'ppm')
          - `report_units` (string) — ['ppb'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
        - `compounds` (array of objects) — most values have been converted to 'ppb'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'ppb'
          - `limit` (number) — value above which this test fails. unit is 'ppb'
          - `lod` (number) — limit of detection. unit is 'ppb'
          - `max` (number) — upper limit of quantitation. unit is 'ppb'
          - `loq` (number) — limit of quantitation. unit is 'ppb'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `water_activity` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['aw'] units the data is being submitted in, from the category's allowed units ('aw')
          - `report_units` (string) — ['aw'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [5] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
        - `compounds` (array of objects) — most values have been converted to 'aw'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'aw'
          - `limit` (number) — value above which this test fails. unit is 'aw'
          - `lod` (number) — limit of detection. unit is 'aw'
          - `max` (number) — upper limit of quantitation. unit is 'aw'
          - `loq` (number) — limit of quantitation. unit is 'aw'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `foreign_matter` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('%', 'mg/lb')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `homogeneity` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('%', 'mg/unit')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [0] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `metals` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['ppb'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppb', 'ppm')
          - `report_units` (string) — ['ppb'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [0] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
        - `compounds` (array of objects) — most values have been converted to 'ppb'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'ppb'
          - `limit` (number) — value above which this test fails. unit is 'ppb'
          - `lod` (number) — limit of detection. unit is 'ppb'
          - `max` (number) — upper limit of quantitation. unit is 'ppb'
          - `loq` (number) — limit of quantitation. unit is 'ppb'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `general` (object)
        - `info_fields` (object)
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
        - `compounds` (array of objects)
          - `name` (string) — compound_key for what is being tested
          - `value` (number)
      - `anabolic_steroids` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'mg/unit')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `servings_per_container` (number) — Number of servings per container
          - `units_per_serving` (number) — Number of units per serving
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `shelflife` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['days'] units the data is being submitted in, from the category's allowed units ('days')
          - `report_units` (string) — ['days'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [0] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
        - `compounds` (array of objects) — most values have been converted to 'days'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'days'
          - `limit` (number) — value above which this test fails. unit is 'days'
          - `lod` (number) — limit of detection. unit is 'days'
          - `max` (number) — upper limit of quantitation. unit is 'days'
          - `loq` (number) — limit of quantitation. unit is 'days'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `alkaloids` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'mg/unit')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `servings_per_container` (number) — Number of servings per container
          - `units_per_serving` (number) — Number of units per serving
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `miscellaneous` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['ppm'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'mg/unit')
          - `report_units` (string) — ['ppm'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to 'ppm'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'ppm'
          - `limit` (number) — value above which this test fails. unit is 'ppm'
          - `lod` (number) — limit of detection. unit is 'ppm'
          - `max` (number) — upper limit of quantitation. unit is 'ppm'
          - `loq` (number) — limit of quantitation. unit is 'ppm'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `endotoxins` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['eu/ml'] units the data is being submitted in, from the category's allowed units ('eu/mg', 'eu/g', 'eu/ml')
          - `report_units` (string) — ['eu/ml'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `servings_per_container` (number) — Number of servings per container
          - `units_per_serving` (number) — Number of units per serving
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to 'eu/ml'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'eu/ml'
          - `limit` (number) — value above which this test fails. unit is 'eu/ml'
          - `lod` (number) — limit of detection. unit is 'eu/ml'
          - `max` (number) — upper limit of quantitation. unit is 'eu/ml'
          - `loq` (number) — limit of quantitation. unit is 'eu/ml'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `peptides` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'iu', 'mg/unit')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `servings_per_container` (number) — Number of servings per container
          - `units_per_serving` (number) — Number of units per serving
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `dna` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('%')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [0] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `ph` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['ph'] units the data is being submitted in, from the category's allowed units ('ph')
          - `report_units` (string) — ['ph'] the primary units displayed on the certificate of analysis
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
        - `compounds` (array of objects) — most values have been converted to 'ph'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'ph'
          - `limit` (number) — value above which this test fails. unit is 'ph'
          - `lod` (number) — limit of detection. unit is 'ph'
          - `max` (number) — upper limit of quantitation. unit is 'ph'
          - `loq` (number) — limit of quantitation. unit is 'ph'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `flavonoids` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['%'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'mg/unit')
          - `report_units` (string) — ['%'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to '%'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is '%'
          - `limit` (number) — value above which this test fails. unit is '%'
          - `lod` (number) — limit of detection. unit is '%'
          - `max` (number) — upper limit of quantitation. unit is '%'
          - `loq` (number) — limit of quantitation. unit is '%'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte
      - `nutrients` (object)
        - `info_fields` (object)
          - `status` (integer) — pass or fail integer ID from the status enum
          - `input_units` (string) — ['ppm'] units the data is being submitted in, from the category's allowed units ('mg/g', 'ppm', 'mg/serving', 'mg/container', 'mg/ml', '%', 'ppb', 'mg/unit')
          - `report_units` (string) — ['ppm'] the primary units displayed on the certificate of analysis
          - `unit_weight` (number) — the weight in grams of the whole unit submitted for sampling when any unit fields are 'mg/unit'
          - `digits` (integer) — [2] number of digits to display on the certificate of analysis; see digits_method
          - `digits_method` (any) — ['round'] round rounds to digits decimal places, significant rounds to digits significant figures
          - `date_tested` (timestamp) — date the sample was tested for this assay
          - `notes` (string) — optional testing notes for this assay
          - `notes_2` (string) — optional testing notes for this assay
          - `notes_3` (string) — optional testing notes for this assay
          - `notes_4` (string) — optional testing notes for this assay
          - `footnote` (string) — footnote to accompany this assay
          - `signatory_name` (string) — name of lab employee to appear on certificate of analysis
          - `signatory_title` (string) — title of lab employee to appear on certificate of analysis
          - `dry_weight` (string) — weight of aliquot after drying
          - `ml_weight` (number) — the weight in grams of 1ml of sample when any unit fields are 'mg/ml'
          - `secondary_report_units` (string) — the secondary units displayed on the certificate of analysis
          - `servings_per_container` (number) — Number of servings per container
          - `units_per_serving` (number) — Number of units per serving
          - `wet_weight` (string) — weight of aliquot as received
        - `compounds` (array of objects) — most values have been converted to 'ppm'
          - `name` (string) — compound_key for what is being tested
          - `value` (number) — test result value - string representing numeric value (eg: "1.02"). unit is 'ppm'
          - `limit` (number) — value above which this test fails. unit is 'ppm'
          - `lod` (number) — limit of detection. unit is 'ppm'
          - `max` (number) — upper limit of quantitation. unit is 'ppm'
          - `loq` (number) — limit of quantitation. unit is 'ppm'
          - `rsd` (number) — relative standard deviation of the analyte values
          - `limitrangehigh` (number) — upper limit when restricting value to a range
          - `rpd` (number) — relative percent difference of the analyte values
          - `stdev` (number) — standard deviation of the sample replicate results
          - `limitrangelow` (number) — lower limit when restricting value to a range
          - `purity_percent` (number) — purity percentage for the analyte
          - `qualifiers` (string) — testing qualifiers, where the regulator defines them
          - `regulatornotes` (string) — notes posted to state traceability systems such as METRC or BioTrack
          - `spike` (number) — spike recovery for the analyte

Example:

```json
{
  "success": true,
  "sample": {
    "id": "2603CAL0142.0001",
    "order_id": "2603CAL0142",
    "client_id": 4821,
    "lab": {
      "id": 118,
      "name": "Cascade Analytical Labs"
    },
    "order_status_id": 4,
    "order_status_name": "Completed",
    "sample_name": "Blue Dream - Cured Flower",
    "strain_name": "Blue Dream",
    "sample_industry_id": 1,
    "sample_industry_name": "Cannabis & Hemp",
    "sample_category_id": 1,
    "sample_category_name": "Plant",
    "sample_type_id": 1,
    "sample_type_name": "Flower - Cured",
    "sample_classification_id": 4,
    "sample_classification_name": "Hybrid",
    "production_method_id": 1,
    "production_method_name": "Indoor",
    "regulator_sample_id": "1A4060300003B01000001234",
    "regulator_batch_id": "1A4060300003B01000000987",
    "batch_id": "BD-2026-03-A",
    "harvest_id": "HV-2026-01-BD",
    "test_packages": [
      {
        "id": 12,
        "name": "OR Recreational Flower Panel",
        "price": 275.0,
        "minimum_quantity": 5.0
      }
    ],
    "last_modified": "2026-03-18T14:05:51",
    "date_published": "2026-03-18T14:05:51",
    "initial_weight": 12.0,
    "initial_weight_unit": "g",
    "test_types": [
      {
        "id": 1,
        "name": "cannabinoids",
        "abbreviation": "CAN"
      }
    ],
    "cover_image": {
      "filename": "blue-dream-cured.jpg",
      "public_key": "c0a8f31e-3b0e-4f42-9a4c-1d9a8f2b7e30",
      "url": "https://images.confidentcannabis.com/blue-dream-cured.jpg"
    },
    "images": [
      {
        "filename": "blue-dream-cured.jpg",
        "public_key": "c0a8f31e-3b0e-4f42-9a4c-1d9a8f2b7e30",
        "url": "https://images.confidentcannabis.com/blue-dream-cured.jpg"
      }
    ],
    "notes": "Third harvest of the 2026 indoor run.",
    "batch_size": 4500.0,
    "batch_size_unit": "g",
    "lot_id": "LOT-2026-0311",
    "lot_size": 9000.0,
    "lot_size_unit": "g",
    "production_run_id": "RUN-2026-03",
    "production_run_size": 18000.0,
    "production_run_size_unit": "g",
    "manifest_id": "0000123456",
    "regulator_lot_id": "1A4060300003B01000000555",
    "regulator_sample_id2": null,
    "regulator_batch_id2": null,
    "production_date": "2026-02-24T00:00:00",
    "date_samples_collected": "2026-03-10T00:00:00",
    "public_url": "https://confidentcannabis.com/s/4d1f9a2c",
    "units_per_serving": null,
    "servings_per_container": null,
    "unit_description": null,
    "container_description": null,
    "regulatory_category_id": 3,
    "solvents_used": null,
    "has_coa": true,
    "coa": {
      "filename": "coa-2603CAL0142.0001.pdf",
      "public_key": "2b7f4c11-90a4-4a1c-8f0e-5c2d3b1a7788",
      "url": "https://files.confidentcannabis.com/coa.pdf"
    },
    "coa_additions": [],
    "lab_data": {
      "date_created": "2026-03-17T11:42:08",
      "date_reported": "2026-03-18T14:05:51",
      "status": 1,
      "thc_total": 21.4,
      "thc_calculation": "thca * 0.877 + d9_thc",
      "cbd_total": 0.12,
      "cbd_calculation": "cbda * 0.877 + cbd",
      "cannabinoid_total": 24.8,
      "cannabinoid_calculation": "sum of all cannabinoids",
      "terpene_total": 1.86,
      "terpene_calculation": "sum of all terpenes",
      "categories": {
        "cannabinoids": {
          "info_fields": {
            "status": 1,
            "input_units": "percent",
            "report_units": "percent",
            "date_tested": "2026-03-17T00:00:00",
            "method": "HPLC-DAD"
          },
          "compounds": [
            {
              "name": "thca",
              "value": "23.85",
              "lod": "0.01",
              "loq": "0.03"
            },
            {
              "name": "d9_thc",
              "value": "0.48",
              "lod": "0.01",
              "loq": "0.03"
            }
          ]
        }
      }
    }
  }
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
curl -X GET 'https://api.confidentcannabis.com/v0/clients/sample/{sample_id}' \
  -H 'X-ConfidentLims-APIKey: YOUR_API_KEY' \
  -H 'X-ConfidentLims-Timestamp: UNIX_TIMESTAMP' \
  -H 'X-ConfidentLims-Signature: REQUEST_SIGNATURE'
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
path = '/v0/clients/sample/{sample_id}'

headers = {'X-ConfidentLims-Timestamp': str(int(time.time()))}
headers['X-ConfidentLims-Signature'] = sign_request(
    'GET', path, headers, {}, API_KEY, API_SECRET)
headers['X-ConfidentLims-APIKey'] = API_KEY

response = requests.get(
    'https://api.confidentcannabis.com' + path,
    headers=headers,
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
const path = "/v0/clients/sample/{sample_id}";

const headers = { 'X-ConfidentLims-Timestamp': String(Math.floor(Date.now() / 1000)) };
headers['X-ConfidentLims-Signature'] = signRequest(
  "GET", path, headers, {}, API_KEY, API_SECRET);
headers['X-ConfidentLims-APIKey'] = API_KEY;

const response = await fetch("https://api.confidentcannabis.com" + path, {
  headers,
});
console.log(await response.json());
```

---

HTML version: https://api.confidentcannabis.com/v0/docs/clients/get-sample-details  
OpenAPI spec for this section: https://api.confidentcannabis.com/v0/docs/clients/openapi.json  
Request Signing guide: https://api.confidentcannabis.com/v0/docs/request-signing.md
