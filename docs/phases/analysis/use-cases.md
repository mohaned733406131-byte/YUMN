---
document_id: DOC-PHA-006
title: Use Cases — analysis phase roll-up
category: phases
status: approved
version: 1.1
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-BA-004, DOC-PHA-007]
related_requirements: []
---

# Use Cases — analysis phase roll-up

## Purpose
Index every operation the system supports, as authored during analysis. The **canonical use-case files live in [`01-business-analysis/use-cases/`](../../01-business-analysis/use-cases/README.md) (`UC-001`…`UC-042`)**; this roll-up (CORE-03 item 4) proves completeness against the phase boundary and links the flows artifact (item 5).

## Scope
All functionality of the four shells: customer web + customer mobile, vendor panel, admin console, courier mobile.

## Actors / roles
Canonical actor list: [`00-project-overview/actors-and-roles.md`](../../00-project-overview/actors-and-roles.md) — `customer`, `vendor`, `courier`, `support`, `moderator`, `admin`, `super admin`, `system` (7 API roles; see [permissions-matrix.md](permissions-matrix.md)).

## Inventory (42 use cases — titles verified against the files, 2026-09-28)

| Actor group | Use cases | Canonical index |
|---|---|---|
| Guest / customer — discovery & identity | `UC-001`…`UC-005` (browse as guest, register phone+OTP, login, reset password, addresses) | [`use-cases/README.md`](../../01-business-analysis/use-cases/README.md) |
| Customer — commerce | `UC-006`…`UC-014` (search, product detail, follow store, add to cart, manage cart, checkout with wallet, track order, confirm receipt with code, contact support) | same |
| Customer — money | `UC-041`, `UC-042` (top up wallet, view wallet statement) | same |
| Vendor — store & catalog | `UC-015`…`UC-024` (register+KYC, store profile, listings, inventory, incoming orders, ready for pickup, return response, finances/payouts, coupons, review responses) | same |
| Courier — delivery execution | `UC-025`…`UC-030` (view deliveries, accept assignment, confirm pickup, transit + attempts, failed attempt, 6-digit code confirmation) | same |
| Admin / platform operations | `UC-031`…`UC-040` (KYC decisions, moderation, orders & disputes, bank-transfer top-up verification, platform settings, audit log, roles, flagged content, escrow auto-release, OTP provider failover) | same |

## Preconditions
Each `UC-NNN` file carries its own preconditions, main/alternate/exception flows, postconditions and related IDs per [`23-templates/use-case-template.md`](../../23-templates/use-case-template.md).

## Main flow
Requirement → use case → workflow → API endpoint → entity → test: `FR-013 → BR-PAY-04 → UC-021 → API-WAL-002 → wallet → TC-031 → AC-FR013-01` (cross-referencing example, root README §5).

## Postconditions
42/42 use cases present; traceability matrices in [`19-traceability/`](../../19-traceability/README.md) cover every use case (`UC-*` 42 registered, consistency check `CHK` series).

## Invariants
No use case may describe a forbidden capability: COD/cards/BNPL/crypto (`C-01…C-04`), GPS/real-time tracking (`C-16`), email-primary/social login (`C-06`), third locale (`C-24`).

## Open questions (COM-01)
1. `UC-036` (Moderator) conflicts with `07-api/endpoints/admin.md` `API-ADM-022/024` on settings/audit-read — deferred sweep item (session 004 backlog).

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 4, session 005) | analysis-agent |
| 2026-09-28 | 1.1 | Inventory → 42 use cases: `UC-041`/`UC-042` added (customer money row), ranges/totals re-synced | Session-007 UC gap from `describ.md` §8 |
