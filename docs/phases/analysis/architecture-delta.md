---
document_id: DOC-PHA-005
title: Architecture Delta — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-ARCH-001, DOC-PHA-002]
related_requirements: [NFR-016]
---

# Architecture Delta — analysis phase

## Purpose
Record what this phase changed in the system architecture. For phase 0 the architecture was *defined, not modified*: the canonical structure lives in [`../../04-architecture/core/architecture-overview.md`](../../04-architecture/core/architecture-overview.md) and this file confirms the phase introduced **no delta** beyond authoring that baseline.

## Scope
- In scope: blocks `B01…B13`, containers, deployment topology, module boundaries as specified in `04-architecture/`.
- Out of scope: code-level component changes (none exist).

## Actors / roles
Architecture authority: tech lead (PENDING sign-off) · Author of record: analysis-agent.

## Preconditions
`ADR-001…ADR-010` ACCEPTED; constraints `C-19`…`C-22` (monolith, PostgreSQL-only, BullMQ-only, Compose-only) immutable.

## Main flow
1. Analysis derives candidate architecture from requirements + constraints.
2. Decisions recorded as ADRs ([`18-decisions/ADR/`](../../18-decisions/ADR/)).
3. Views published: [container](../../04-architecture/core/container-view.md), [component](../../04-architecture/core/component-view.md), [deployment](../../04-architecture/core/deployment-view.md), [data-flow](../../04-architecture/core/data-flow.md), [module boundaries](../../04-architecture/core/module-boundaries.md).

## Alternate / exception flows
- Spec contradiction (`SPE-04`: API vocabulary vs DB enums, defect `D-06`) → **stop and reconcile via ADR before any code**; no ad-hoc mapping layers.
- Underspecified race `ORD-08`/`D-12` → ADR required before implementing that transition.

## Postconditions
Baseline architecture `APPROVED`; **no architecture change introduced by phase 0** — delta = ∅.

## Data entities touched
None (documentation only).

## Invariants
`C-19` PostgreSQL only · `C-20` BullMQ only · `C-21` monolith only · `C-22` Compose only · no GPS columns (`C-16`) · money columns `<name>_yer` bigint (`DAT-03`).

## Open questions (COM-01)
1. Sponsor/tech-lead review of `RULES_HINTS.md` §8 — PENDING (blocks phase-gate use per AUD-05).
2. Path-spelling reconciliation (`D-08`): ops docs cite `apps/api`/`apps/web` — canonical tree is `../../05-frontend/core/frontend-architecture.md` §1 + `../../06-backend/core/backend-architecture.md` §1.

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 3, session 005) | analysis-agent |
