---
document_id: DOC-DR-007
title: DATA-REQ-007 — Financial immutability
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-004, DATA-REQ-006, FR-013, FR-014, NFR-008]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# DATA-REQ-007 — Financial immutability

> Registry summary (`requirements-overview.md` §4): ledger append-only: corrections via compensating entries, never UPDATE/DELETE of postings.

## Description

The double-entry ledger backing every wallet, escrow, commission, refund, and payout movement is append-only. Corrections are expressed as new balanced postings that reference the original transaction; historical rows are never modified or removed — enforced by database permissions, not by application discipline alone.

## Requirement statements

- R1: The application database role holds `SELECT`/`INSERT` only on ledger tables: `UPDATE` and `DELETE` privileges are denied at the PostgreSQL level (`VERIFIED` pattern — registry "ledger append-only via DB permissions").
- R2: Corrections (refunds, commission reversals per BR-ESC-04, rounding adjustments per BR-FIN-05) are written as compensating debit/credit pairs referencing the original transaction; the original rows remain byte-identical.
- R3: Every transaction posts balanced rows — Σ debits = Σ credits — and amounts are integer YER with half-up rounding to whole YER at sub-order level (BR-PAY-10, BR-FIN-05); non-integer writes are rejected by column type/CHECK.
- R4: A standing invariant verifies zero ledger imbalance continuously and as part of daily reconciliation (NFR-008, BR-ESC-08); any imbalance is CRITICAL-severity and alerts finance immediately.
- R5: Ledger retention follows DATA-REQ-003 (≥ 5 years) and is recoverable per DATA-REQ-004; reports and statements (BR-FIN-04) are generated from ledger reads only.

## Acceptance criteria

- AC-DR007-01: Permission test — direct `UPDATE` and `DELETE` on ledger tables as the application role fail with privilege errors.
- AC-DR007-02: Correction test — executing a refund and a commission reversal creates compensating rows; row hashes prove original postings unchanged.
- AC-DR007-03: Invariant test — Σ debits equals Σ credits across all transactions; a seeded imbalance is detected by the invariant check and alerted.
- AC-DR007-04: Type test — writing a fractional or otherwise invalid YER amount to a ledger column is rejected.

## Related IDs

`BR-PAY-06` · `BR-PAY-10` · `BR-ESC-04` · `BR-ESC-08` · `BR-FIN-04` · `BR-FIN-05` · `FR-013` · `FR-014` · `NFR-008` · `NFR-019` · `C-01` · `C-12`

## Verification method

Database permission tests, compensating-entry integration tests with row-hash comparison, invariant-check job tests (clean and seeded-imbalance), and code review of all posting paths.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
