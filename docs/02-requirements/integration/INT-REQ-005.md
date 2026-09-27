---
document_id: DOC-IR-005
title: INT-REQ-005 — Delivery orchestration
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-006, INT-REQ-008, FR-015, FR-012]
related_documents: [DOC-REQ-001, DOC-SA-010, DOC-BA-005]
---

# INT-REQ-005 — Delivery orchestration

> Registry summary (`requirements-overview.md` §5): internal assignment engine; abstraction allows future external fleet APIs.

**Dependency risk:** LOW — no external fleet API exists in v1; the engine is internal, and future provider APIs plug in behind the INT-REQ-008 adapter boundary.

## Purpose
Coordinate courier assignment and delivery progression for the 17-state order machine (C-09) using an internal engine — offer/accept assignment within zone, pickup/transit/out-for-delivery scans, and 6-digit code confirmation — while keeping the door open for external delivery partners without GPS (C-16).

## Interface expectations

- **Assign:** eligible couriers in the same zone are offered the job; first accept wins with optimistic locking preventing double assignment (BR-SHP-04); release returns the job to the pool (`ASSIGNED → READY_FOR_PICKUP`).
- **Progress:** pickup, transit, and out-for-delivery events advance the state machine per `03-system-analysis/state-transitions.md`; delivery completes only via 6-digit code verification (BR-SHP-02, BR-ORD-08).
- **Timeouts/retries:** state events are idempotent; a crashed worker job retries 3× with backoff then DLQ with alert (BR-PLT-02); transitions use optimistic `version` locking → `409 STATE_CONFLICT` on races.
- **Abstraction:** all engine operations are exposed through a `DeliveryProviderPort` so a future external fleet API can be substituted without domain changes (INT-REQ-008).

## Data exchanged
Sub-order reference, shipping zone, courier identity/role, timestamps, delivery-code verification attempts (stored hashed, not in logs), attempt counts, optional photo (BR-SHP-07). **No GPS/location field exists anywhere** in the contract or schema (BR-SHP-05, C-16).

## Failure behavior & fallback
Courier abandons/releases → assignment returns to pool; 3rd failed delivery attempt → escalation ticket to admin with full timeline (BR-SHP-06, BR-SHP-03); engine outage → orders remain `READY_FOR_PICKUP` with an ops alert; no silent auto-cancel (BR-ORD-10).

## Security
Courier access limited to the Delivery Provider role with ownership checks on assigned deliveries (SEC-REQ-004, BR-ORD-09); delivery-code attempts capped at 3 → 24 h lock (SEC-REQ-005); manual reassignments write audit entries (BR-PLT-06).

## Acceptance criteria

- AC-IR005-01: Race test — two couriers accepting the same job concurrently: exactly one is assigned, the other receives a conflict response; no double assignment exists afterwards.
- AC-IR005-02: Privacy test — no location/GPS field appears in the API contract, schema, or logs (contract assertion + schema scan).
- AC-IR005-03: Code-lock test — the 3rd failed code locks confirmation for 24 hours and creates a support ticket (BR-SHP-03).
- AC-IR005-04: Substitution test — replacing the engine implementation with a mock/external adapter requires zero changes to domain modules (compile + contract tests).

## Related IDs

`C-09` · `C-16` · `FR-012` · `FR-015` · `BR-SHP-02` · `BR-SHP-03` · `BR-SHP-04` · `BR-SHP-05` · `BR-SHP-06` · `BR-ORD-08` · `BR-PLT-02` · `SEC-REQ-004` · `SEC-REQ-005` · `INT-REQ-008`

## Verification method
Concurrency/optimistic-locking integration tests, state-machine tests against the canonical 17-state table, contract test with a mock adapter, and a schema scan for forbidden location fields.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
