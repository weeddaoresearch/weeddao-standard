# WeedDAO ↔ WCIA / OpenTHC Interoperability Crosswalk

**Status:** experimental RFC companion  
**Reviewed:** 2026-09-19

## Why this exists

WeedDAO does not need the cannabis industry to abandon existing identifiers.

A stronger interoperability strategy is:

> **Use WeedDAO where its semantic model adds value, and preserve crosswalks to identifiers systems already in use.**

WCIA's `wcia-analytes` project describes itself as a standardized collection of cannabis analyte names and identifiers for interoperability. OpenTHC's public base-data catalog uses the same ULID-style lab metric identifiers for examples including Cannabidiol and Activated Total THC.

That makes WCIA/OpenTHC an important bridge rather than a competitor to erase.

## Initial result

The current WeedDAO seed contains 19 analyte/aggregate concepts.

The first reviewed crosswalk finds:

- **14 straightforward one-to-one mappings**;
- **3 mappings that are one-to-one only with an important definition/speciation note**;
- **1 one-to-many/component-set relationship** — Abamectin;
- **1 concept with no exact WCIA match identified** — Total cannabinoids.

This is useful precisely because the non-exact cases are visible instead of being forced into a false universal ID.

## Most important finding — Abamectin

WeedDAO currently carries a regulator-facing `Abamectin` concept because multiple state testing tables use that label.

WCIA represents at least two analytes:

- Abamectin B1a — `01EDPT1CHZJTASPX5X38PWWP3Y`
- Abamectin B1b — `01FQFG9EJB2ZNCCGA3W92QF32P`

Therefore WeedDAO must **not** pretend `WDA-AN-000016` has one exact WCIA equivalent.

Relationship:

`WeedDAO regulator-facing concept → related WCIA component analytes`

That difference is exactly the kind of semantic edge case WeedDAO is designed to preserve.

## Total THC / Total CBD

WCIA/OpenTHC define activated-total concepts. OpenTHC describes Activated Total THC as delta-9 THC + delta-9 THCA × 0.877.

A source field merely labeled "Total THC" should not be crosswalked blindly unless its calculation semantics are known.

The crosswalk therefore uses `exact_with_definition_note`, not unconditional exactness.

## Metals

Basic element identity maps cleanly for arsenic, cadmium, lead and mercury, but regulations can narrow the actual measured species, such as **inorganic arsenic** or **total mercury**.

WeedDAO retains that distinction in rule/method context instead of proliferating identifiers prematurely.

## Design consequence

WeedDAO identifiers should support external identifiers/crosswalk relationships such as:

- `exact`
- `exact_with_definition_note`
- `related_component_set`
- `broader_than`
- `narrower_than`
- `no_exact_match_identified`

This allows software to translate safely without pretending every vocabulary is structurally identical.

## Machine-readable file

See:

`compatibility/wcia-analyte-crosswalk-0.1-draft.json`

## CLI

Translate IDs with:

```bash
python scripts/crosswalk_analyte_ids.py --weeddao WDA-AN-000003
```

or:

```bash
python scripts/crosswalk_analyte_ids.py --wcia 018NY6XC00LMK7KHD3HPW0Y90N
```

Use `--json` for machine-readable output.

## Strategic implication

A future federal framework does not require WeedDAO to "win" an identifier war.

If WeedDAO can connect:

**WCIA/OpenTHC IDs ↔ WeedDAO semantics ↔ regulatory TestSpecs ↔ customer dependencies**

then an existing software vendor can adopt WeedDAO's impact layer without replacing its own metric IDs.

That reduces adoption friction considerably.

## Sources reviewed

- `conflabs/wcia-analytes`, version shown as 0.9.9 in its README.
- WCIA cannabinoid, cannabinoid-total, metals and pesticide files.
- OpenTHC public base-data catalog / lab metric examples.

No affiliation or endorsement is implied.
