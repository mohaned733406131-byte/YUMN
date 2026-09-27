---
document_id: DOC-DR-008
title: DATA-REQ-008 — Ownership boundaries
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, SEC-REQ-004, FR-002, FR-008, NFR-009]
related_documents: [DOC-REQ-001, DOC-BA-005]
---

# DATA-REQ-008 — Ownership boundaries

> Registry summary (`requirements-overview.md` §4): every tenant-scoped row carries owner keys (user_id/store_id) enforced by queries + tests.

## Description

Multi-vendor isolation is a data-level guarantee: every row that belongs to a user, store, or delivery assignment carries explicit owner keys, every query is scoped by them, and a standing cross-tenant test suite proves no surface can read or write across the boundary.

## Requirement statements

- R1: Every tenant-scoped table carries owner key columns (`user_id`, `store_id`, and `courier_id` where applicable) with foreign keys and indexes supporting scoped access paths (DATA-REQ-001).
- R2: All reads and writes include the owner predicate at the repository/service layer; vendor queries are scoped to `store_id` with cross-store access denied at the service layer (BR-VND-07).
- R3: Visibility follows BR-ORD-09: buyer sees own orders, vendor sees own sub-orders, courier sees own delivery, admin/moderator see only their scoped subsets; the `System` role is not an escape hatch for unscoped reads.
- R4: Background jobs (BullMQ, C-20) are parameterized by owner and must touch only rows of that owner; jobs processing store X never read or write store Y rows.
- R5: The cross-tenant test suite covers every tenant-scoped entity and runs on every change; adding an entity without adding its cases fails the coverage gate (`INFERENCE` — operationalizes the registry's "enforced by queries + tests").

## Acceptance criteria

- AC-DR008-01: Schema audit — every tenant-scoped table has the expected owner key column(s), FK, and index; the missing-owner report is empty.
- AC-DR008-02: Cross-tenant suite — for each entity, user A/store X fixtures receive zero rows or 403/404 for every read/write endpoint when addressing user B/store Y resources.
- AC-DR008-03: Job isolation test — a worker processing store X's jobs produces zero row changes in store Y partitions (row-level assertion before/after).
- AC-DR008-04: Coverage gate — CI fails if a new tenant-scoped entity is added without cross-tenant test cases.

## Related IDs

`BR-VND-07` · `BR-ORD-09` · `FR-002` · `FR-008` · `SEC-REQ-004` · `DATA-REQ-001` · `C-10` · `C-20` · `NFR-009`

## Verification method

Automated cross-tenant integration test suite in CI, schema audit report, and background-job isolation tests with seeded multi-tenant fixtures.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
