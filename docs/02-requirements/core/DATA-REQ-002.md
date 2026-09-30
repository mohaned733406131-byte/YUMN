---
document_id: DOC-DR-002
title: DATA-REQ-002 — Personal data minimization
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-003, SEC-REQ-002, SEC-REQ-006, FR-003, NFR-019]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# DATA-REQ-002 — Personal data minimization

> Registry summary (`requirements-overview.md` §4): collect only needed PII; classify per `16-data/data-classification.md`.

## Description

Only personal data with a documented, active purpose is collected or exposed. Every PII field is classified under `16-data/data-classification.md`, every API response exposes only the fields its surface needs, and categories excluded by constraints (cards, GPS, email-primary identity) are never collected at all.

## Requirement statements

- R1: Each stored PII field maps to an explicit purpose documented in `16-data/data-classification.md`; a field without a purpose may not be added to the schema.
- R2: Registration collects phone, password, and display name only; email is optional and stored solely when the user provides it (BR-AUTH-08); addresses are collected only when the user creates them, ≤10 per user (FR-003).
- R3: No card data (C-02) and no location/GPS data (C-16, BR-SHP-05) may exist in any table, API field, log, or third-party call.
- R4: API responses expose only purposeful fields per surface — e.g. vendors receive buyer contact data only for fulfillment, never full profile histories (cross FR-002, DATA-REQ-008).
- R5: PDPA (Law 11/2012) alignment controls are applied as far as evidence allows; precise minimization/erasure obligations remain `INSUFFICIENT EVIDENCE` pending the `DEP-09` legal opinion.

## Acceptance criteria

- AC-DR002-01: Schema-to-purpose audit — every PII column has a documented purpose entry; the unmapped-field report is empty.
- AC-DR002-02: Negative schema test — no table, column, or endpoint contains card-number or GPS/location fields anywhere in the data model or API contract.
- AC-DR002-03: Registration API test — a request without email succeeds and stores no email value; supplying an optional email stores it without making it an identity (BR-AUTH-08).
- AC-DR002-04: Response-field test — representative list/detail endpoints are asserted against a per-endpoint PII allowlist; unexpected PII fields fail the test.

## Related IDs

`BR-AUTH-08` · `BR-SHP-05` · `C-02` · `C-16` · `FR-003` · `SEC-REQ-002` · `SEC-REQ-006` · `DATA-REQ-003` · `DATA-REQ-008` · `NFR-019` · `DEP-09`

## Verification method

Schema audit against the classification document, API contract tests with PII allowlists, and a data-model grep gate in CI for forbidden fields (card, lat/long); compliance detail deferred to `DEP-09` and `16-data/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
