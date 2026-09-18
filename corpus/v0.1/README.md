# WeedDAO Public COA Corpus v0.1

Public evidence collection mapping real-world Certificates of Analysis to frozen WeedDAO Cultivation Record **v0.1-alpha**.

**Not claims of** industry adoption, certification, lab endorsement, or `FIRST_EXTERNAL_IMPLEMENTATION`. WeedDAO Research mapped these public sources for schema-validation evidence.

## Freeze
- Schema `schemas/weeddao-cultivation-record-v0.1-alpha.schema.json` is **FROZEN**
- SHA256: `31b0bdab4585954bebb9af1b06ac8b2d5a7b513ad1ca9694070836f1c723b5ee`
- Tag `v0.1-alpha` must not move
- ND / `<LOQ` / NOT TESTED are never coerced

## Layout
| Path | Description |
|------|-------------|
| `manifest.json` / `manifest.csv` | 50-case index |
| `cases/coa-NNN-source.json` | Source metadata |
| `mappings/coa-NNN-weeddao-record.json` | Mapped records |
| `reviews/coa-NNN-review.json` | Mapping result + gaps |
| `inputs/` | Verified manifest + extraction jsonl |
| `cache/` | Local fetch cache (gitignored) |

## Cases
- **COA-001..003** — hand-reviewed seed mappings
- **COA-004..050** — verified public sources (37 primary, 10 secondary OpenCOA)

## Validate
```bash
python scripts/validate.py
python scripts/validate.py corpus/v0.1/mappings/*.json
```

## Rebuild
```bash
/workspace/weeddao/.venv/bin/python corpus/v0.1/scripts/build_corpus.py
```

## Counts
- TOTAL=50 PRIMARY=37 SECONDARY=10
- FULL/PARTIAL/FAILED=0/50/0
