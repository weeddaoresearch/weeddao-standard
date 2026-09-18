# Governance

## Purpose

This repository maintains the **WeedDAO Open Cannabis Data Standard**, currently at **`0.1-alpha`**. The goal is a shared, optional data language for cultivation and related lab records — a coordination layer among growers, laboratories, researchers, and software systems.

This project does **not** certify operators, regulate markets, or claim to be an official industry authority.

## Principles

1. **Openness** — Schema, examples, tests, and docs are public under Apache-2.0.
2. **Clarity over marketing** — Describe the work as proposed and experimental. Avoid “world’s standard,” “official,” or adoption claims.
3. **Interoperability** — Prefer fields and enums that different organizations can map to without losing meaning.
4. **Privacy by design** — No required PII; opaque identifiers preferred.
5. **Evidence of provenance** — Distinguish self-reported, sensor, lab, third-party, and derived data.
6. **No speculative finance layer** — Blockchain, tokens, NFTs, and crypto assets are out of scope.

## Roles (lightweight, for alpha)

| Role | Responsibility |
|------|----------------|
| Maintainers | Merge changes, cut draft tags, keep schema/docs consistent |
| Contributors | Propose changes via issues/PRs and RFC comments |
| Reviewers | Anyone providing technical or domain feedback |

During `0.1-alpha`, maintainers may apply judgment to keep the draft coherent. Broader multi-stakeholder process can evolve if the draft gains sustained interest — that evolution is **not** claimed here.

## Decision process

1. **Discussion** — Issue or RFC comment stating the problem and options.
2. **Proposal** — Concrete schema and/or doc diff.
3. **Review** — Check against principles, tests, and privacy notes.
4. **Decision** — Maintainer merge, defer, or request changes.
5. **Record** — Notable decisions appear in [CHANGELOG.md](CHANGELOG.md).

Consensus is preferred. Where consensus is unavailable, maintainers document the choice and rationale.

## Versioning

- `0.1-alpha` is experimental. Field sets and enums may change based on comment.
- `schema_version` in instance documents must match the schema draft they claim to follow.
- A future non-alpha version, if any, would be a separate, explicit decision — not implied by this document.

## Out of scope

- Regulatory compliance frameworks
- Product certification or grading authorities
- Payment, identity, or ledger systems
- Requiring personal contact data or precise residential addresses

## Conflicts of interest

Contributors should disclose affiliations when proposing changes that primarily benefit a single vendor’s proprietary format. Vendor-neutral interoperability remains the priority.

## Changes to governance

Amendments to this file follow the same proposal/review process as schema changes and should be noted in the changelog.
