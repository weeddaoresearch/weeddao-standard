# Real-data compatibility audit

**Source:** Hugging Face `cannlytics/cannabis_results` state CSVs (`data/{st}/{st}-results-latest.csv`), sampled streaming/download **without** ingesting the full ~995k corpus or any PDFs.

**Cap:** max **2000** records, **~250 per state**.

**Machine summary:** [REAL_DATA_AUDIT.json](REAL_DATA_AUDIT.json)

| Metric | Value |
|--------|------:|
| Records audited | 2000 |
| States | CA, FL, HI, MA, MD, MI, NV, NY (8) |
| Structurally valid WeedDAO outputs | 1250 |
| Schema validation failures | 0 |
| Structurally unmappable | 750 |
| LOSSLESS_FOR_AVAILABLE_SEMANTICS | 35 |
| SEMANTICALLY_PARTIAL | 1215 |
| Subject type determinate / ambiguous | 642 / 608 |
| Multi-unit source / preserved | 129 / 129 |
| Traceability present / core-mapped | 197 / 197 |
| Extension usage records | 1250 |

Top ambiguities observed: `ND_UNRECOVERABLE` (null top-level floats), `SUBJECT_TYPE_AMBIGUOUS` (flowerish without harvest/lot metadata), `LIMIT_TYPE_AMBIGUOUS` (generic ResultDetail.limit).

**Attribution:** Dataset CC BY 4.0 — Cannlytics. This audit consumes normalized CSV fields only.
