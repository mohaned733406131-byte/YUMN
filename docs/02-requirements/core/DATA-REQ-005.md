---
document_id: DOC-DR-005
title: DATA-REQ-005 — Schema evolution
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-004, NFR-020, NFR-005]
related_documents: [DOC-REQ-001, DOC-OVR-008]
---

# DATA-REQ-005 — Schema evolution

> Registry summary (`requirements-overview.md` §4): expand-contract migrations; backward-compatible deploys (NFR-020).

## Description

Schema changes follow the expand–contract pattern so that the modular monolith (C-21) deployed on Docker Compose (C-22) can roll forward and roll back without downtime: every migration is compatible with both the previous and the next application release during the window in which both run.

## Requirement statements

- R1: Breaking changes are split across releases: **expand** (add nullable/new column or table, backfill, dual-read/write) → switch code → **contract** (drop/rename old structure) in a later release; no expand+contract in a single deploy.
- R2: Application version N must run correctly against schema N and against the expanded schema N+1; application version N+1 must run against the expanded schema (NFR-020 zero-downtime deploys).
- R3: Destructive DDL (`DROP`, `RENAME`, type-narrowing) is forbidden in the same release as the code change that stops using the structure it removes.
- R4: Migrations execute in CI against a production-like copy of the schema; the pipeline rejects migrations that fail the compatibility lint (unsafe destructive statement in the same release, missing rollback step).
- R5: Rollback of a release after the expand phase requires reverting only the application — the schema stays and is harmless to the previous version.

## Acceptance criteria

- AC-DR005-01: Compatibility test — app N passes critical-path tests against the expanded schema, and app N+1 passes against the pre-contract schema; both results recorded in CI.
- AC-DR005-02: Lint gate — a migration containing `DROP COLUMN` in the same release as the code that first stops reading it fails CI.
- AC-DR005-03: Rolling-deploy simulation — during migration, old and new instances serve traffic concurrently with zero 5xx responses (NFR-005 target unaffected).
- AC-DR005-04: Rollback drill — reverting the application deployment after an expand-phase migration succeeds with no schema rollback and no data loss.

## Related IDs

`NFR-020` · `NFR-005` · `NFR-009` · `C-19` · `C-21` · `C-22` · `DATA-REQ-001` · `DATA-REQ-004` · `DEP-02`

## Verification method

CI migration pipeline with compatibility lint, rolling-deploy integration test, and a documented rollback drill; migration catalogue reviewed in `08-database/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
