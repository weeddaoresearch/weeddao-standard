# Texas registry proof — different regulatory model and regulatory drift

**Status:** experimental registry evidence  
**As of:** 2026-09-19  
**Scope:** Texas Compassionate-Use Program only. This is not legal advice or a complete Texas compliance ruleset.

Texas is a useful third jurisdiction because its testing model differs materially from the California and Oregon examples already in the registry.

## 1. Texas specifies required testing categories

37 TAC §12.7(b) requires representative samples of processed products to be tested for:

- tetrahydrocannabinol levels;
- cannabidiol levels;
- residual solvents;
- pesticides;
- fungicides;
- fertilizers;
- mold;
- heavy metals.

The current seed models these as required-test categories rather than inventing per-analyte action limits that the cited provision does not supply.

## 2. Texas reporting is tied directly to final package labeling

37 TAC §12.7(p) requires final package labels to include THC/CBD potency and a statement that the product was tested for contaminants, including findings and the testing date.

This means the rules registry needs to represent more than numeric action limits. It also needs **reporting requirements**.

## 3. Testing-provider structure is different

Texas DPS states in its dispensing-organization FAQ that Chapter 487 does not provide for state licensing of low-THC cannabis testing laboratories and that only licensed dispensing organizations may test low-THC products.

That is structurally different from states built around separately licensed independent cannabis laboratories.

This should remain visible in WeedDAO's jurisdiction metadata rather than being forced into a universal "licensed lab" assumption.

## 4. Current statute uses a dosage-unit THC definition

Texas Occupations Code §169.001(3), as amended effective September 1, 2025, defines low-THC cannabis using a maximum of **10 mg of tetrahydrocannabinols per dosage unit**.

The seed represents this separately from the testing-category rule because it is a product-definition requirement, not a laboratory action limit.

## 5. Apparent regulatory drift / conflict

The older text of 37 TAC §12.7(q), which has not been updated in the source materials reviewed here, still expresses the product rule as a percentage-by-weight THC ceiling plus a CBD minimum.

That does not match the current statutory definition in Occupations Code §169.001(3).

WeedDAO does **not** decide which text controls, silently overwrite one with the other, or present the older percentage rule as a current numeric testing threshold.

Instead:

- the current statute is encoded as its own sourced rule record;
- the older administrative-rule text is retained as a source-level conflict requiring legal/regulatory review;
- the conflict becomes a registry quality signal.

This is a strong example of why a durable testing-rules product cannot simply scrape regulations into one flat table.

## 6. Hemp rules are not substituted for TCUP rules

Texas also has detailed consumable-hemp testing rules under 25 TAC Chapter 300. Those rules expressly state that the relevant hemp-testing section does not apply to low-THC cannabis regulated under Health and Safety Code Chapter 487.

The TCUP seed therefore does **not** copy hemp analyte limits, accreditation assumptions, or COA requirements into the medical-cannabis ruleset.

## Commercial significance

A future WeedDAO regulatory-intelligence service could surface:

- required testing categories even where no numeric action limit is stated;
- reporting and labeling obligations;
- who is permitted to perform testing;
- statutory and administrative-rule conflicts;
- rules that changed but dependent text did not;
- requirements that belong to a neighboring program but do not legally apply to the customer's program.

That is more useful than a static "limits by state" spreadsheet.

## Sources

- Texas Department of Public Safety, Chapter 12 administrative rules, §12.7.
- Texas Department of Public Safety, Dispensing Organizations FAQ.
- Texas Occupations Code Chapter 169, §169.001(3), as amended by HB 46 effective September 1, 2025.
- Texas DSHS consumable-hemp rules, 25 TAC Chapter 300, used only to confirm that those hemp provisions are a separate program and are not imported into this TCUP seed.
