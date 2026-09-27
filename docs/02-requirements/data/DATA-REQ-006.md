---
document_id: DOC-DR-006
title: DATA-REQ-006 — Data quality validation
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-007, FR-005, FR-013, NFR-008]
related_documents: [DOC-REQ-001, DOC-BA-005]
---

# DATA-REQ-006 — Data quality validation

> Registry summary (`requirements-overview.md` §4): validation at write time + reconciliation jobs (stock, wallet, escrow).

## Description

Invalid state is prevented at the point of write by layered validation (DB constraints + service rules), and cross-entity consistency is proven continuously by reconciliation jobs over stock, wallet, escrow, and provider statements — mismatches are alerted, never silently tolerated.

## Requirement statements

- R1: Write-time validation rejects: negative wallet balance (BR-PAY-05), oversell or negative stock (BR-CAT-07), unbalanced ledger postings (BR-PAY-06), invalid coupon application (BR-PRM-06), and out-of-policy state transitions (BR-ORD-01) — each with a stable error code.
- R2: A daily reconciliation job compares ledger totals against wallets, escrows, vendor payables, and external provider statements (BR-ESC-08, BR-FIN-03); any mismatch raises a finance alert and produces a mismatch report — no silent pass (`VERIFIED` — BR-ESC-08/BR-FIN-03).
- R3: A stock-quality job audits the 15-minute reservation TTL (C-13), releasing expired holds so available stock never drifts from reservations (cross FR-005).
- R4: Quality metrics (freshness of reconciliation, invalid-write counts, imbalance count) are exported to observability with alerting (NFR-014); zero imbalance is a standing invariant (NFR-008).
- R5: Reconciliation jobs are idempotent and retried with the platform's standard 3× exponential backoff then DLQ (BR-PLT-01, BR-PLT-02).

## Acceptance criteria

- AC-DR006-01: Negative-write suite — each invalid case in R1 is rejected with no partial rows committed.
- AC-DR006-02: Seeded-mismatch test — introducing a deliberate discrepancy (e.g. wallet total ≠ ledger) causes the reconciliation job to report it and fire an alert within the run.
- AC-DR006-03: Clean-data test — running reconciliation on consistent data reports zero mismatches and completes within its scheduled window.
- AC-DR006-04: TTL audit test — reservations expired beyond 15 minutes are released and stock availability matches reservations exactly afterwards.

## Related IDs

`BR-PAY-05` · `BR-PAY-06` · `BR-CAT-07` · `BR-ESC-08` · `BR-FIN-03` · `BR-PRM-06` · `BR-PLT-02` · `C-13` · `FR-005` · `FR-013` · `NFR-008` · `NFR-014`

## Verification method

Unit/integration tests for write-time validation; reconciliation job tests against seeded consistent and inconsistent datasets; alert assertion in the observability test suite.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
