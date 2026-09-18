# Outreach copy — request expert review (v0.1-alpha)

Tone: invite technical/domain review. Not sales. No adoption claims. No tokens, blockchain, or product pitch.

**Core message:** We are seeking expert review of an experimental open cannabis data standard (working draft `v0.1-alpha`) — a shared JSON language for cultivation and related lab summaries so different platforms and organizations can exchange data more consistently.

**Tagline:** Different platforms. Different organizations. One shared data language.

---

## Grower / cultivation operator

Subject: Review request — draft cultivation data format (WeedDAO v0.1-alpha)

Hi —

We are preparing an experimental open data format for cultivation batch records (environment, harvest, optional lab summaries). It is a proposed shared data language, not a certification program and not regulatory.

If you have 10–15 minutes, we would value a grower’s eye on whether the required fields and optional grow/harvest sections match real batch records. Brief: `docs/external-review-brief.md`. Feedback via issue templates or the RFC doc; identity optional.

Thank you for considering an expert review.

---

## Laboratory

Subject: Review request — draft lab-result shapes in WeedDAO v0.1-alpha

Hi —

We published an experimental cultivation-record JSON schema that includes optional cannabinoid, terpene, and safety structures for exchange (not a lab method standard).

We are asking labs and LIMS practitioners to review whether `{value, unit}` analytes, the terpene array, and the optional safety block are usable when mapping COAs. Start with `docs/external-review-brief.md` (questions 3, 4, and 8). Identity optional.

Thank you for considering an expert review.

---

## Researcher

Subject: Review request — provenance and missing-data semantics (WeedDAO v0.1-alpha)

Hi —

WeedDAO `v0.1-alpha` is a proposed open cannabis data standard (working draft) for cultivation records with explicit provenance and gap reasons (`null` + `not_measured` / `not_applicable` / `withheld`), plus reported vs genetically verified cultivar identity.

We would appreciate research feedback on whether those semantics support reproducible exchange. Brief and questions: `docs/external-review-brief.md`. Not a claim of adoption; experimental only.

Thank you for considering an expert review.

---

## Software developer

Subject: Review request — JSON Schema cultivation record (WeedDAO v0.1-alpha)

Hi —

We have an Apache-2.0 JSON Schema (Draft 2020-12) for a cultivation record, plus examples and `scripts/validate.py`. Goal: a small interoperability shape different systems can map to — not a platform lock-in.

If you can spare ~10 minutes: `docs/quickstart.md`, then note mapping friction via the implementation-feedback issue template. Schema version is frozen at `0.1-alpha` for this review round except genuine defects.

Thank you for considering an expert review.
