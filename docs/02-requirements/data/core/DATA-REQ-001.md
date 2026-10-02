---
document_id: DOC-DR-001
title: DATA-REQ-001 — Integrity constraints
category: 02-requirements
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-006, DATA-REQ-007, FR-004, FR-012, NFR-008]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# DATA-REQ-001 — Integrity constraints

> Registry summary (`requirements-overview.md` §4): FKs, unique/check constraints, NOT NULL where required; referential integrity enforced in DB not just app.

## Description

PostgreSQL 16 (C-19) is the final arbiter of data integrity: every relationship, uniqueness rule, and domain bound that business rules imply is declared as a database constraint in migrations, so invalid state is impossible even through application bugs, manual SQL, or a partially failed deploy.

## Requirement statements

- R1: Every relationship carries a foreign key with an explicit `ON DELETE` behavior; no orphan child rows can exist — inserting one directly via SQL must fail.
- R2: Uniqueness is DB-enforced for: phone number (BR-AUTH-01), SKU within a store (BR-CAT-02), category slug per level (BR-CAT-03), coupon code (BR-PRM-01), idempotency keys (BR-PLT-03), and master/sub-order references (C-10).
- R3: CHECK constraints enforce domain rules: price > 0 and sale price < original (BR-CAT-04), stock integer ≥ 0 (BR-CAT-07), rating 1–5 (BR-REV-03), order total 500–5,000,000 YER (C-14), top-up 1,000–5,000,000 YER (BR-PAY-02), amount integer YER (BR-PAY-10), cart guards 50/10/5 (C-15).
- R4: The order state column is constrained to exactly the 17 enumerated states (C-09, `../../../03-system-analysis/core/state-transitions.md`); no 18th value can be written.
- R5: `NOT NULL` on all money, ownership (`user_id`/`store_id`), state, and audit-timestamp columns; constraints are declared in migrations reviewed alongside schema changes (DATA-REQ-005).

## Acceptance criteria

- AC-DR001-01: Direct-SQL test — inserting a child row with a non-existent parent fails with a foreign-key violation, independent of any application code path.
- AC-DR001-02: Uniqueness test — duplicate phone, duplicate SKU in one store, and duplicate coupon code each fail with a unique violation mapped to a stable API error.
- AC-DR001-03: Boundary test — order totals of 499 and 5,000,001 YER rejected, 500 and 5,000,000 accepted; an order state outside the 17-value enum rejected.
- AC-DR001-04: Domain test — negative price, negative stock, and rating 0/6 inserts are rejected at the database level.

## Related IDs

`C-09` · `C-10` · `C-14` · `C-15` · `C-19` · `BR-AUTH-01` · `BR-CAT-02` · `BR-CAT-04` · `BR-CAT-07` · `BR-PAY-02` · `BR-PAY-10` · `BR-PLT-03` · `NFR-008` · `FR-012`

## Verification method

Database constraint test suite executed against a real PostgreSQL instance in CI (boundary + negative inserts), plus a migration review checklist confirming each declared constraint exists in DDL.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration (data/ + functional/ sections) | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
