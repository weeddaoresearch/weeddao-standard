# Querying the experimental WeedDAO testing-rules registry

The `registry-rfc` branch now includes a small query CLI.

It is intentionally simple: the goal is to prove that the open registry can answer useful cross-jurisdiction questions before building an API or hosted service.

## Examples

### Compare Abamectin across jurisdictions as of September 19, 2026

```bash
python scripts/query_registry.py \
  --analyte WDA-AN-000016 \
  --as-of 2026-09-19
```

This should surface the currently effective Oregon and New York records. California Phase I does not become effective until October 1, 2026, so it is excluded by default for a September 19 query.

### Include future / out-of-period rules

```bash
python scripts/query_registry.py \
  --analyte WDA-AN-000016 \
  --as-of 2026-09-19 \
  --include-out-of-period
```

### Show New York action limits

```bash
python scripts/query_registry.py \
  --jurisdiction US-NY \
  --requirement-type action_limit \
  --as-of 2026-09-19
```

### Find reporting-only / reporting requirements

```bash
python scripts/query_registry.py \
  --requirement-type reporting_requirement \
  --as-of 2026-09-19
```

### Machine-readable output

```bash
python scripts/query_registry.py --analyte WDA-AN-000016 --json
```

## What this proves

The query layer can distinguish:

- jurisdiction;
- analyte identity;
- test category;
- requirement type;
- effective date;
- source-native threshold and unit;
- rules with no scalar threshold;
- authoritative source metadata.

It deliberately does **not** convert units, decide legal conflicts, or infer missing product-scope logic.

Those should be explicit future layers rather than hidden behavior.

## Commercial boundary

The CLI and public registry can remain open.

Potential commercial capabilities above it include:

- continuously monitored regulator sources;
- revision diffs;
- customer-specific rule applicability;
- unit-aware comparison;
- method / LOQ impact analysis;
- alerts;
- hosted API;
- audit logs and conformance attestations.
