---
document_id: DOC-SEC-004
title: RBAC — Definitive Permission Matrix (7 Actors)
category: 09-security
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-002, FR-020, SEC-REQ-004, SEC-REQ-010, DATA-REQ-008]
related_documents: [DOC-SEC-001, DOC-SEC-002, DOC-SEC-007, DOC-FR-002, DOC-BA-005, DOC-OVR-007, DOC-BE-004]
---

# RBAC — Authorization Design (Source of Truth)

**This document is the definitive role × capability matrix** for the 7 canonical actors (`DOC-OVR-007` ACT-01…ACT-07). `06-backend/authorization.md` (`DOC-BE-004`) maps these decisions to guards and service-layer checks; it never redefines a decision. Expands `FR-002` / `SEC-REQ-004`.

## 1. Authorization Principles

| # | Principle | Canon |
|---|---|---|
| P1 | **Server-side only.** Every request is authorized in the service layer; UI hiding, route guards and client-side role checks are presentation, never security | `SEC-REQ-004` |
| P2 | **Deny-by-default.** An endpoint without an explicit grant for the caller's role returns localized 403; unknown role/missing mapping fails closed | `SEC-REQ-004` R1/R2, `AC-SR004-04` |
| P3 | **Role AND ownership.** The role grant is necessary but not sufficient — resource ownership (`user_id`, `store_id`, assignment) is evaluated in the same check | `DATA-REQ-008`, `BR-VND-07`, `BR-ORD-09` |
| P4 | **Route-level + resource-level.** Route guards decide *who may call*; service checks decide *which rows*; neither alone is sufficient | `SEC-REQ-004` R1 |
| P5 | **Privileged/money actions audit-chained.** Role change, KYC decision, wallet freeze, refund, payout, dispute resolution, top-up verification write an append-only audit entry | `BR-PLT-06`, `SEC-REQ-010` R2 |
| P6 | **`SYSTEM` is non-human.** Authenticates only through internal mechanisms, can never log in interactively, never bypasses ownership checks | `SEC-REQ-004` R5 |
| P7 | **Non-owners get 403 (or 404 where enumeration would leak existence)** | `SEC-REQ-004` R1 |

**Legend:** ✔ = allowed (scope noted) · ✖ = denied · — = not applicable. Every ✖ must return 403/404 server-side regardless of what the UI shows (`AC-SR004-03`).

## 2. Permission Matrix (capabilities × roles)

| # | Capability | CUSTOMER | VENDOR | COURIER | ADMIN | SUPER_ADMIN | MODERATOR | SYSTEM |
|---|---|---|---|---|---|---|---|---|
| 1 | Browse / search / cart | ✔ | ✔ | ✖ | ✔ | ✔ | ✔ | — |
| 2 | Place order, pay from own wallet | ✔ (own) | ✖ | ✖ | ✖ | ✖ | ✖ | — |
| 3 | View own orders & timeline | ✔ (own) | ✔ (own sub-orders) | ✔ (assigned) | ✔ (scoped) | ✔ | ✔ (scoped) | — |
| 4 | Manage products & inventory | ✖ | ✔ (own `store_id`, staff Editor/Manager) | ✖ | ✔ | ✔ | ✖ | auto (TTL release) |
| 5 | Manage store profile / settings / zones | ✖ | ✔ (own store) | ✖ | ✔ | ✔ | ✖ | — |
| 6 | Create / edit / disable coupons | ✖ | ✔ (store scope) | ✖ | ✔ (platform coupons) | ✔ | ✖ | — |
| 7 | Submit KYC documents | ✖ | ✔ (submit/resubmit only) | ✖ | — | — | — | — |
| 8 | Approve / reject / suspend KYC | ✖ | ✖ | ✖ | ✔ | ✔ | ✖ | — |
| 9 | Accept / release delivery assignment | ✖ | ✖ | ✔ (zone-eligible, first accept) | ✔ (dispatch override) | ✔ | ✖ | ✔ (engine) |
| 10 | Confirm delivery with 6-digit code | ✖ (buyer receives code, never submits) | ✖ | ✔ (own assignment) | ✔ (manual, audited) | ✔ | ✖ | ✖ |
| 11 | Request return / refund | ✔ (own, policy-window) | respond only | ✖ | — | — | — | — |
| 12 | Approve refund (to wallet) | ✖ | respond/inspect | ✖ | ✔ | ✔ | ✖ | ✔ (auto per rule) |
| 13 | Wallet freeze / unfreeze (`BR-PAY-09`) | ✖ | ✖ | ✖ | ✔ | ✔ | ✖ | ✖ |
| 14 | Verify bank-transfer top-up → credit (`BR-PAY-04`) | ✖ (submits request) | ✖ | ✖ | ✔ | ✔ | ✖ | ✖ |
| 15 | Direct ledger / balance adjustment (manual write) | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ (compensating entries only) |
| 16 | Read a customer's wallet balance / transactions | ✔ (own) | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ |
| 17 | View customer PII (phone, address, KYC refs) | ✔ (own) | limited (fulfillment fields of own orders — `INFERENCE`) | limited (assigned delivery address/phone — `INFERENCE`) | ✔ (platform, masked by default — `INFERENCE`) | ✔ | limited / masked (`INFERENCE`) | ✖ |
| 18 | Order state override (admin override of the 17 states) | ✖ | limited (own sub-orders, per `FR-012`) | delivery states only | ✔ | ✔ | ✖ | ✔ (automated transitions) |
| 19 | Resolve disputes / final arbitration (`BR-RET-06`) | file only | respond | ✖ | ✔ | ✔ | ✖ | ✖ |
| 20 | Moderate content, reviews, banners (hide/restore) | report only | respond (own) | ✖ | ✔ | ✔ | ✔ | auto-flag |
| 21 | Support tickets / customer assistance | own tickets | own store tickets | ✖ | ✔ | ✔ | ✔ | ✖ |
| 22 | Read audit log | ✖ | ✔ (own store scope) | ✔ (own scope) | ✔ (platform scope) | ✔ (full) | ✖ | write-only |
| 23 | Manage roles & permissions (platform) | ✖ | staff invite/remove only (`BR-VND-06`) | ✖ | ✖ | **✔ (sole)** | ✖ | ✖ |
| 24 | Platform settings & configuration | ✖ | store settings only | ✖ | limited (operational) | ✔ | ✖ | runtime config |
| 25 | Payout batch approval / execution (`BR-ESC-05`) | ✖ | view own statements | ✖ | ✔ | ✔ | ✖ | ✔ (scheduled) |
| 26 | Export reports / data extracts | ✖ (own history) | ✔ (own store analytics) | ✖ | ✔ | ✔ | ✖ | ✔ (scheduled) |

Consistency check: rows 1–3, 8, 12, 18, 20, 22–24 mirror the "Permission Summary per Actor" table in `DOC-OVR-007`; this matrix is the expanded, testable form referenced from there.

## 3. ADMIN vs SUPER_ADMIN Separation

| Concern | ADMIN (ACT-04) | SUPER_ADMIN (ACT-05) |
|---|---|---|
| Day-to-day operations (KYC decisions, refunds, disputes, top-up verification, moderation, tickets, dispatch) | ✔ | ✔ |
| Role & permission management (granting ADMIN/MODERATOR, changing the matrix) | **✖ — sole SUPER_ADMIN capability** | ✔ |
| Platform configuration (settings that alter rules, not just operations) | limited/operational only | ✔ |
| Payout batch approval | ✔ | ✔ |
| Audit log | platform scope read | full read |
| Rationale | Least privilege: operational admin rights are separable from meta-authorization; an ADMIN account theft must not yield the ability to mint more admins | `FR-020`, `DOC-OVR-007`, `AC-FR002-04` |

Self-escalation is impossible by construction: no endpoint accepts a role change for self, and the only role-management route is guarded to SUPER_ADMIN (row 23).

## 4. MODERATOR Scope (content/support only — no finance)

- **Allowed:** review/content moderation with audit entry (`BR-REV-04`), support tickets, escalation, scoped order timeline reads (row 3), report dashboards.
- **Explicitly denied:** refunds (12), wallet freeze (13), bank top-up verification (14), payouts (25), KYC approval (8), role management (23), audit log (22), PII beyond masked support view (17).
- Rationale: `DOC-OVR-007` defines Moderator as content moderation + support escalation; financial authority requires the ADMIN/SUPER_ADMIN accountability trail (`SEC-REQ-010`).

## 5. Courier Least Privilege (assigned shipment only)

- COURIER can see **only** deliveries currently assigned (or historically delivered by them): order timeline scoped to the assigned sub-order (`BR-ORD-09`), buyer address/phone needed for drop-off (`INFERENCE`), code verification (row 10).
- Denied: catalog management, other customers' data, refunds, moderation, platform anything.
- Assignment is per-shipment, not per-zone read: releasing a job returns it to the pool and revokes that courier's access (`BR-SHP-04`, `INT-REQ-005`).
- Delivery-code attempts capped at 3 → 24 h lock + auto ticket (`BR-SHP-03`, `SEC-REQ-005` R3).

## 6. Ownership Enforcement (`DATA-REQ-008`)

| Resource | Owner key | Enforcement point | Cross-owner attempt |
|---|---|---|---|
| Wallet / transactions | `user_id` | repository scope + service check | 403, zero rows (`AC-SR004-02`) |
| Orders (customer side) | `user_id` (buyer) | service layer | 403/404, no data disclosure (`AC-FR002-01`) |
| Products / store / coupons | `store_id` | service layer (`BR-VND-07`) | 403 (`AC-FR002-02`) |
| Deliveries | courier assignment row | service layer | 403 (`BR-ORD-09`) |
| Reviews | purchasing customer + order item | service layer (`BR-REV-01`) | 403 |
| Notifications center | `user_id` | query scope | empty set |
| Audit log | platform, append-only | read per role scope; no UPDATE/DELETE for anyone | write attempt fails at DB privilege level (`AC-SR010-01`) |

Every tenant-scoped table carries owner keys; a repository method without an ownership predicate fails review and the matrix test suite (`AC-SR004-01` — every endpoint × every role, no endpoint untested).

## 7. Vendor Staff Sub-Roles (inside the VENDOR column)

| Staff role | Effective scope | Cannot |
|---|---|---|
| Viewer | read store data & analytics | modify anything |
| Editor | products, inventory, content edits | orders' financial actions, staff management |
| Manager | above + orders, coupons, store settings | invite/remove staff, change roles |
| Owner | all of the above + **staff invite/remove/role change** (`BR-VND-06`) | anything outside own store; self-escalation by staff is blocked (`AC-FR002-03`) |

Staff roles are attributes of the VENDOR actor — they never widen beyond `store_id`.

## 8. Admin Console Additional Controls

| Control | Design | Evidence |
|---|---|---|
| Same-origin exposure of the console | Documented gap: console shares origin with the public API in v1 → tracked `SEC-003` (MEDIUM, OPEN) | `security-findings.md` |
| Source-network restriction | IP allowlist / restricted network range for admin routes (`INFERENCE` — not mandated by canon; recommended alongside `DEP-08` CDN rules) | `INFERENCE` |
| Session hygiene | 15-min access + 5-device cap apply unchanged; privileged actions also require fresh audit trail | `SEC-REQ-003`, `BR-PLT-06` |
| Step-up factor | None beyond password login in v1 — tracked `SEC-012` (HIGH, OPEN) | `authentication.md` §7 |
| Break-glass | No impersonation/"view as customer" tooling exists (explicitly out of scope in `FR-002`) | `DOC-FR-002` |

## 9. Verification

| Test | Assertion | Canon |
|---|---|---|
| Matrix sweep | every endpoint called as each of 7 roles → expected allow/deny, none untested | `AC-SR004-01` |
| IDOR suite | cross-customer order, cross-store product, staff self-escalation, direct API call bypassing UI | `AC-SR004-02/03`, `AC-FR002-01…03` |
| Fail-closed | missing role context / unmapped endpoint → 403, never 200 | `AC-SR004-04` |
| Audit coverage | each privileged action in P5 produces exactly one complete audit row | `AC-SR010-03` |
| DB privilege | direct UPDATE/DELETE on audit tables as app role fails | `AC-SR010-01` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
