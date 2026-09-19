# Cannlytics upstream pin

| Item | Value |
|------|--------|
| Repository | https://github.com/cannlytics/cannabis_results |
| Hugging Face dataset | https://huggingface.co/datasets/cannlytics/cannabis_results |
| Pinned commit SHA | `a4e05a9f7367ac0b1637bd84773875b3bd1453ec` |
| Commit message | Initial commit: Current state of Cannabis Results dataset code as of 2026-02-01 |
| Schema source path | `config/results_schema.py` (`LabResult`, `ResultDetail`, `normalize_status`) |
| License | **CC BY 4.0** (Creative Commons Attribution 4.0 International) |

## Attribution

Downstream WeedDAO compatibility artifacts that incorporate or derive from Cannlytics Cannabis Results schema/data must retain CC BY 4.0 attribution to Cannlytics.

Synthetic fixtures under `compat/cannlytics/fixtures/` are **schema-shape derived** and are not copied from proprietary COA PDFs or fabricated certificate numbers.

## Verification

```bash
gh api repos/cannlytics/cannabis_results/commits/a4e05a9f7367ac0b1637bd84773875b3bd1453ec --jq .sha
```

Expected: `a4e05a9f7367ac0b1637bd84773875b3bd1453ec`
