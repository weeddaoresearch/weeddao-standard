---
name: Schema problem
about: Report an objective defect, ambiguity, or inconsistency in the v0.1-alpha schema or docs
title: "[schema] "
labels: ["schema-problem", "v0.1-alpha"]
---

## Problem type

- [ ] Validation rejects a record that should be valid
- [ ] Validation accepts a record that should be invalid
- [ ] Schema and documentation disagree
- [ ] Ambiguous definition
- [ ] Broken example / test
- [ ] Other

## Description

What is wrong?

## Location

- **Schema path / field:** 
- **Doc section (if any):** 

## Evidence

```json
{
  "schema_version": "0.1-alpha",
  "record_id": "example",
  "cultivation_batch_id": "example",
  "created_at": "2026-09-18T10:00:00Z"
}
```

Validator output (if applicable):

```text
paste output of: python scripts/validate.py your-file.json
```

## Expected behavior

## Identity (optional)

- **Role / perspective:** grower / lab / researcher / developer / other
- **Organization (optional):** 
- **Contact (optional):** 
