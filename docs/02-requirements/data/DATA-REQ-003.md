---
document_id: DOC-DR-003
title: DATA-REQ-003 — Retention & deletion
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-002, DATA-REQ-007, FR-003, FR-020, NFR-017]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# DATA-REQ-003 — Retention & deletion

> Registry summary (`requirements-overview.md` §4): configurable retention; account deletion workflow; financial records ≥ 5 years (NFR-019).

## Description

Data is kept only as long as its category requires. Retention periods are configuration, not code; a scheduled purge job enforces them; customer account deletion erases/anonymizes PII while financial and audit records are retained for at least 5 years as required by NFR-019.

## Requirement statements

- R1: Retention periods are defined per data category as configuration consumed by a scheduled purge job; changing a period requires configuration change, not a code release (`INFERENCE` — operationalizes the registry's "configurable retention").
- R2: The account deletion workflow (FR-003) erases or irreversibly anonymizes customer PII (profile, addresses, contact data) and documents what was retained and why.
- R3: Financial records — ledger postings, wallet transactions, escrow/payout records, invoices/VAT records (BR-FIN-01) — are retained **≥ 5 years** (NFR-019) and are exempt from erasure until the period elapses.
- R4: Audit records for privileged/money actions follow the same ≥5-year floor (SEC-REQ-010); operational logs follow shorter documented periods defined in `16-data/`.
- R5: Every purge and deletion run writes an evidence entry (actor, scope, row counts, timestamp) so erasure can be demonstrated; backup retention windows and their effect on residual copies are documented (`INFERENCE`).
- R6: Exact PDPA erasure/retention timelines are `INSUFFICIENT EVIDENCE` pending `DEP-09`; the ≥5-year financial floor is `VERIFIED` (NFR-019).

## Acceptance criteria

- AC-DR003-01: Purge test — seeded records past their configured retention are removed by the job on schedule; metrics for rows purged are emitted.
- AC-DR003-02: Deletion test — an account-deletion request anonymizes profile PII while ledger/wallet rows remain intact and queryable for financial reporting.
- AC-DR003-03: Guard test — an attempt to purge a financial record younger than 5 years is blocked and raises an alert rather than deleting.
- AC-DR003-04: Evidence test — each purge/deletion run produces an audit entry with actor, scope, counts, and timestamp.

## Related IDs

`NFR-019` · `NFR-017` · `FR-003` · `FR-020` · `DATA-REQ-002` · `DATA-REQ-004` · `DATA-REQ-007` · `SEC-REQ-010` · `BR-FIN-01` · `DEP-09`

## Verification method

Scheduled-job integration tests against seeded data, database inspection after deletion, evidence-entry review, and configuration review of retention periods in `16-data/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
