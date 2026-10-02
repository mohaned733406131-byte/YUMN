---
document_id: DOC-DR-004
title: DATA-REQ-004 — Backup & restore
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-003, DATA-REQ-007, FR-013, NFR-006]
related_documents: [DOC-REQ-001, DOC-OVR-008, DOC-OVR-010]
---

# DATA-REQ-004 — Backup & restore

> Registry summary (`requirements-overview.md` §4): continuous WAL + daily snapshots; quarterly restore drills (NFR-006).

## Description

PostgreSQL data is protected by continuous WAL archiving plus daily full snapshots, giving point-in-time recovery within the NFR-006 objectives (RTO ≤ 1 h, RPO ≤ 15 min) and C-26 availability commitments; recoverability is proven by scheduled restore drills, not assumed.

## Requirement statements

- R1: WAL segments are archived continuously with no gap exceeding the 15-minute RPO (NFR-006, C-26), enabling point-in-time recovery to any moment inside the retention window.
- R2: A full snapshot is taken daily; snapshot and WAL jobs are monitored, and job failure raises an operations alert (NFR-014) rather than failing silently.
- R3: Backups are encrypted at rest, stored off the primary host, and access is limited to the operations role (`INFERENCE` — standard safeguard supporting C-26).
- R4: Restore drills are executed **quarterly**: restore to a point in time, verify integrity (row counts, ledger balance Σ debits = Σ credits per BR-PAY-06), and complete within RTO ≤ 1 hour; each drill produces a dated record.
- R5: Backup retention periods are defined in `16-data/` and aligned with DATA-REQ-003 (purged data may persist in backups only until backup expiry, which is documented).

## Acceptance criteria

- AC-DR004-01: Continuity test — monitoring confirms the maximum gap between archived WAL segments stays ≤ 15 minutes (RPO evidence).
- AC-DR004-02: Failure-injection test — a forced snapshot failure alerts operations within the alerting window defined in `../../12-non-functional/core/observability.md`.
- AC-DR004-03: Drill record — the latest quarterly restore completes within 1 hour, passes integrity checks including zero ledger imbalance, and is documented with elapsed time and scope.
- AC-DR004-04: Protection review — backup storage requires encryption at rest and authorized (role-restricted) access; unauthenticated restore attempts fail.

## Related IDs

`NFR-006` · `NFR-014` · `C-26` · `C-19` · `DATA-REQ-003` · `DATA-REQ-007` · `BR-PAY-06` · `BR-ESC-08` · `DEP-02`

## Verification method

Backup monitoring evidence, quarterly restore drill (scheduled operational test with integrity assertions), and configuration review; drill results recorded against NFR-006 in `12-non-functional/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
