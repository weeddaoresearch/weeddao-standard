# External review brief — WeedDAO Open Cannabis Data Standard v0.1-alpha

**Audience:** growers, laboratories, researchers, software developers  
**Reading time:** about 2 minutes  
**Draft status:** proposed / under development / experimental working draft  

## WHAT

WeedDAO Open Cannabis Data Standard `v0.1-alpha` is a **proposed JSON shape** for a cultivation record: batch identity, optional grow and environment summaries, harvest, and lab results. It is a **shared data language** for exchange — not a product, not a certification program, and not a regulation.

## WHY

Grow software, LIMS, research databases, and spreadsheets often encode the same facts differently (units, missing values, cultivar names, COA panels). A small, explicit exchange format makes it easier to compare and move records **without** forcing everyone onto one platform.

## WHAT it covers

- **Required:** `schema_version`, `record_id`, `cultivation_batch_id`, `created_at`
- **Optional:** producer, cultivar (reported vs genetically verified), cultivation, environment (units in field names), irrigation/nutrition, harvest, post-harvest, lab cannabinoids/terpenes/safety, outcomes, provenance, extensions, data gaps
- **Semantics:** `null` + `not_measured` / `not_applicable` / `withheld` (no magic-number sentinels); provenance methods such as `self_reported`, `sensor_measured`, `laboratory_verified`

Artifacts: schema under `schemas/`, examples under `examples/`, validator `scripts/validate.py`, field list in [field-reference.md](field-reference.md).

## WHAT to evaluate

Please judge fitness for **your** workflows. Especially answer:

1. **Required set** — Are `schema_version`, `record_id`, `cultivation_batch_id`, and `created_at` the right minimal required fields?
2. **Environment units** — Are Celsius / % / kPa / ppm / µmol/m²/s / mol/m²/day the right defaults for a cross-jurisdiction exchange format?
3. **Cannabinoid shape** — Is `{value, unit}` per analyte preferable to a flat numeric map?
4. **Terpene extensibility** — Is an open array sufficient, or should `0.1-alpha` ship a recommended name vocabulary?
5. **Cultivar identity** — Is the `reported` vs `genetically_verified` split clear enough for seed-to-sale and research use?
6. **Provenance enum** — Missing methods? Overlap between `third_party_verified` and `laboratory_verified`?
7. **Missing-data semantics** — Does `null` + `not_measured` / `not_applicable` / `withheld` cover real export cases without magic numbers?
8. **Safety block** — Right level of detail for optional contaminant panels?

How to respond: issue templates in `.github/ISSUE_TEMPLATE/`, or [request-for-comments.md](request-for-comments.md). Identity is optional. This draft is **experimental, not regulatory**.

---

Different platforms.  
Different organizations.  
One shared data language.
