# Contributing

Thank you for interest in the WeedDAO Open Cannabis Data Standard (`0.1-alpha`).

This draft is **experimental and open for comment**. Contributions that improve clarity, correctness, interoperability, and privacy are welcome. This project is a proposed **data coordination layer**, not a product pitch or certification body.

## Ways to contribute

1. **Comments on the RFC** — see [docs/request-for-comments.md](docs/request-for-comments.md).
2. **Issues** — schema bugs, ambiguous field definitions, missing units, privacy concerns.
3. **Pull requests** — documentation fixes, additional valid/invalid fixtures, validator improvements, carefully scoped schema clarifications.
4. **Interoperability notes** — mappings from existing grow/LIMS/ERP exports (see [docs/interoperability.md](docs/interoperability.md)).

## Ground rules

- Keep the tone accurate: this is a **proposed / under-development** open standard. Do not market it as official, regulatory, certified, or “the industry standard.”
- Do **not** introduce blockchain, token, NFT, or crypto-related concepts.
- Do **not** require personally identifiable information (PII). Prefer opaque IDs and organizational metadata.
- Prefer additive, backward-compatible changes within `0.1-alpha` discussion; breaking changes should be called out explicitly in review.
- Missing data must remain semantic (`null` + `not_measured` / `not_applicable` / `withheld`). No magic-number sentinels.
- Match documentation to the schema. If you change one, update the other in the same change.

## Development setup

```bash
cd weeddao-standard
python3 -m venv ../.venv   # or any venv location you prefer
source ../.venv/bin/activate
pip install -r requirements.txt
python scripts/validate.py
```

All `tests/valid` records must pass; all `tests/invalid` records must fail.

## Pull request checklist

- [ ] `schema_version` remains `"0.1-alpha"` (unless intentionally proposing a new draft version in a separate process)
- [ ] Schema validates with Draft 2020-12
- [ ] Examples and tests updated
- [ ] `python scripts/validate.py` passes
- [ ] Docs updated for any field or semantics change
- [ ] No PII requirements introduced
- [ ] No blockchain/token/NFT/crypto content

## License

By contributing, you agree that your contributions are licensed under the Apache License 2.0 (see [LICENSE](LICENSE)).
