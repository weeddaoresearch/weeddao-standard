# Privacy guidance — v0.1-alpha

The WeedDAO Open Cannabis Data Standard is designed so that **personally identifiable information (PII) is not required** to produce a valid cultivation record.

This document is guidance for implementers. It is **not** legal advice and **not** a compliance certification.

## Principles

1. **Minimum necessary** — Share only fields needed for the intended exchange.
2. **Opaque identifiers** — Prefer `organization_id`, `facility_id`, `record_id`, and batch IDs over names, emails, or phone numbers.
3. **Organizational over personal** — Use organization or facility labels; avoid individual grower home addresses and personal contact channels in standard fields.
4. **Withheld is first-class** — If a value exists but must not be shared, use `null` and mark `withheld` in `status` or `data_gaps`.
5. **Jurisdiction awareness** — Local law may restrict what cultivation or patient-related data can leave a facility. The schema does not override those rules.

## What the schema does not require

- Personal names
- Email addresses
- Phone numbers
- Street / postal addresses of individuals
- Government ID numbers of persons
- Precise geolocation of private residences

Optional `producer` fields are oriented to **organizations**, public license identifiers, and coarse jurisdiction labels.

## Recommended practices

| Situation | Practice |
|-----------|----------|
| Multi-tenant software export | Issue opaque facility IDs; strip user account emails from exports |
| Research collaboration | Share de-identified batch records; keep a private linkage table offline |
| Public example datasets | Use synthetic IDs and fictional org names (as in `examples/`) |
| License numbers | Include only when disclosure is appropriate and lawful |
| Cultivar genetic reports | Share reference IDs, not customer contact sheets |

## Gap reason `withheld`

Use when the producing system knows a value but policy or consent prevents emission:

```json
{
  "producer": {
    "organization_name": null,
    "facility_id": "fac-redacted-01"
  },
  "data_gaps": {
    "producer.organization_name": "withheld"
  }
}
```

## Relationship to lab and patient data

`0.1-alpha` focuses on cultivation and associated lab analytics for material lots. It is **not** a clinical or patient-record standard. Do not overload this schema with patient PII.

## Security note

Validation of JSON shape is not access control. Systems exchanging records still need appropriate authentication, authorization, transport security, and retention policies — topics intentionally outside this data-format draft.
