---
document_id: DOC-PHA-017
title: Permissions & Roles — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-SEC-003, DOC-BE-003]
related_requirements: [SEC-REQ-004]
---

# Permissions & Roles — analysis phase

> Managed by the system admin (original rule 8). Enforcement is server-side (SEC-02, principle P1/P2);
> every row needs an automated authorization test. **Canonical 26-row capability matrix: [`../../09-security/core/rbac.md`](../../09-security/core/rbac.md)** — this phase artifact maps the template rows onto that canon; role ↔ enum ↔ DB parity table is `rbac.md` §8 (7 API identities / 10 enum values / 6 persisted + `SYSTEM`).

| Role | Operation (CRUD/action) | Resource | Allow? | Enforcement point | Test id |
|---|---|---|---|---|---|
| CUSTOMER | read | marketplace catalog (public) | yes | public route (no auth) | `AC-SR004-01` |
| CUSTOMER | create | own order (wallet pay) | yes (own) | service:order.create + ownership | `AC-FR013-*`, `TST-CON-01` |
| CUSTOMER | read | own orders / wallet / addresses | yes (own rows) | policy:ownership (`user_id`) | `AC-SR004-02` |
| CUSTOMER | update | another customer's order/PII | **no** → 404 (enumeration-safe) | service:ownership | `AC-SR004-02/03` (IDOR suite) |
| VENDOR | create/update | own store products, inventory, coupons | yes (`store_id` scope; staff Viewer/Editor/Manager via `b03.store_member`) | route guard + service:store scope | `AC-FR002-01…03` |
| VENDOR | update | another vendor's store | **no** → 403/404 | service:store scope | `AC-SR004-02` |
| COURIER | read/accept | same-zone delivery assignments | yes (first-accept, optimistic lock) | service:assignment + version lock | `BR-SHP-04` race test, `TC-005` tier |
| COURIER | update | order state → `DELIVERED` (bypassing code) | **no** | state machine guard (`ORD-04`) | `TST-CON-16` |
| ADMIN | approve/reject | KYC, refunds, disputes, top-up verification, wallet freeze | yes | service:privileged + P5 audit row | `TC-109`, `AC-SR010-03` |
| ADMIN | update | platform roles | **no** (sole `SUPER_ADMIN`) | guard:role | `TC-110` (`ROLE_ASSIGNMENT_FORBIDDEN`) |
| SUPER_ADMIN | manage | roles & platform settings | yes | guard:role + versioned settings | `TC-110`, `TC-114` |
| MODERATOR | read | audit log / settings (admin console) | **no** (conflict under sweep — see Open questions) | guard:role (fail-closed) | `TC-114` |
| SYSTEM | create | scheduled jobs, webhook intake, auto rules (escrow release, SLA escalations) | yes (internal identity, never logs in) | internal call path, `audit_log.actor_type='SYSTEM'` | `TC-112`, `TC-107` |
| *unknown / unmapped role* | any | any | **no → 403, never 200** | deny-by-default (P2) | `AC-SR004-04`, `TC-114` |

## Notes
- UI hiding is presentation only — never counted as authorization (P1).
- New roles/operations are appended here in the same commit that adds the operation (IMP-03 / DOC-05).
- Per-feature `permissions-<feature>.md` files + enforcement tests are **Phase 1+ deliverables** — the phase closes with this design matrix, honestly marked design-level.

## Open questions (COM-01)
1. `MODERATOR` read of audit log / platform settings: `../../07-api/admin/admin.md` `API-ADM-022`/`API-ADM-024` grant it, `rbac.md` rows 22/24 and `UC-036` deny it — **reconcile before coding** (deferred sweep item, session 004 backlog; `SPE-04`).

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 15 / IMP-03, session 005) | analysis-agent |
