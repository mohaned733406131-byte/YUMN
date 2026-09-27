---
document_id: DOC-BE-004
title: Authorization — Implementation Placement (FR-002, SEC-REQ-004)
category: 06-backend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-002, FR-020, SEC-REQ-004, SEC-REQ-010, DATA-REQ-008]
related_documents: [DOC-BE-001, DOC-BE-002, DOC-BE-003, DOC-BA-005]
---

# Authorization — Implementation Placement

**Design** (permission matrices, role definitions, control rationale) lives in `09-security/rbac.md`. This file covers **where FR-002 / SEC-REQ-004 are enforced in code** and the standard enforcement points every endpoint must use. The 7 actors are canonical (`00-project-overview/actors-and-roles.md`).

---

## 1. Enforcement Stack (outside-in)

```text
HTTP request
  → RateLimitGuard            (SEC-REQ-009)
  → JwtAuthGuard               (valid signature + active session — DOC-BE-003 §3)
  → RolesGuard                 (@RequireRoles — actor-level)
  → PermissionsGuard           (@RequirePermissions — granular, matrix-driven)
  → Ownership interceptor      (row-level scope — DATA-REQ-008)
  → Controller → Service → Domain  (business guards re-checked in domain, e.g. state machine)
  → Repository                 (mandatory ownership filter in query)
```

| Layer | File (per `DOC-BE-002` §1) | Defends against |
|---|---|---|
| `JwtAuthGuard` | `shared/auth/jwt-auth.guard.ts` | anonymous access |
| `RolesGuard` | `shared/auth/roles.guard.ts` | wrong actor (e.g. Customer hitting `/admin/*`) |
| `PermissionsGuard` | `shared/auth/permissions.guard.ts` | action beyond granted permission (Moderator approving refunds) |
| `@Ownership()` interceptor | `shared/auth/ownership.interceptor.ts` | IDOR — cross-customer/cross-store reads (TC-011, TC-012) |
| Repository scoping | block repositories (`DOC-BE-002` §5) | data leak if a higher layer is missed |
| Domain guards | e.g. `b06-order` state machine | illegal transitions regardless of caller role |

**Defense in depth rule:** authorization is checked at *minimum* twice for tenant-scoped resources — once at the boundary (role/permission) and once at the data layer (ownership). Never rely on hidden IDs or UI absence (`SEC-REQ-004`).

## 2. Role & Permission Model (coding side)

| Concept | Representation | Notes |
|---|---|---|
| Actors | enum `Role { CUSTOMER, VENDOR_OWNER, VENDOR_STAFF_VIEWER, VENDOR_STAFF_EDITOR, VENDOR_STAFF_MANAGER, COURIER, ADMIN, SUPER_ADMIN, MODERATOR, SYSTEM }` | maps to the 7 actors; vendor staff are ACT-02 sub-roles (`BR-VND-06`) |
| Permissions | string atoms `resource:action` (e.g. `product:update`, `refund:approve`, `audit:read`) | matrix defined in `09-security/rbac.md`; code reads it, never redefines it |
| Assignment | DB tables in `b01` (user roles) and `b03` (staff roles scoped to `store_id`) | only Super Admin manages platform roles; only Owner manages staff (`BR-VND-06`) |
| Claims | JWT carries role list + `sid` + `store_id` where applicable | roles checked from token; **privilege changes revoke/reissue sessions** so stale tokens can't escalate |
| System actor | service identity (`ACT-07`) with machine credentials — no interactive login | used by jobs/webhooks |

## 3. Enforcement Points by Endpoint Class

| Endpoint class | Guards | Ownership check | Extra |
|---|---|---|---|
| Public catalog/search/CMS | none (anonymous) | n/a | inactive products 404 (`BR-CAT-06`) |
| Auth endpoints | rate limit only | n/a | `DOC-BE-003` |
| Customer resources (orders, wallet, addresses) | Jwt + `CUSTOMER` | `user_id == sub` | wallet: no admin read/write beyond freeze flag (`BR-PAY-09`) |
| Vendor store/catalog/orders | Jwt + vendor roles | `store_id == token.store_id` (`BR-VND-07`) | staff role granularity (Viewer read-only) |
| Courier deliveries | Jwt + `COURIER` | assignment row `courier_id == sub` | code verification attempts (`BR-SHP-03`) |
| Admin/moderator ops | Jwt + `ADMIN`/`MODERATOR`/`SUPER_ADMIN` | scope = platform (or per-matrix) | audit entry for privileged actions (`SEC-REQ-010`) |
| Financial ops (payouts, freezes, bank verify) | `SUPER_ADMIN`/`ADMIN` + permission atom | dual-control where matrix says so | append-only audit (`BR-PLT-06`) |
| System/job endpoints | service auth (internal token) | n/a | not exposed publicly |

## 4. Row-Level Ownership (DATA-REQ-008)

| Resource | Owner key | Scoping rule | Tests |
|---|---|---|---|
| Wallet & ledger | `user_id` | repository requires owner filter; no admin bypass (`actors-and-roles.md` ownership table) | TC-011 |
| Orders (master) | `customer_id` | buyer sees own; vendor sees own sub-orders via join on `store_id`; courier sees assigned shipment; admin per matrix (`BR-ORD-09`) | TC-011, TC-014 |
| Store & products | `store_id` | every vendor query scoped at service layer; cross-store = deny (`BR-VND-07`) | TC-012 |
| Deliveries | `courier_id` | own-assignment only | TC-013 |
| Reviews/returns | `order_item_id` → owner | only purchasing customer acts (`BR-REV-01`) | unit + integration |
| Audit log | platform append-only | read per role scope; nobody writes except system/admin actions | `SEC-REQ-010` |

Implementation: ownership predicates are **mandatory parameters** of repository methods (type system makes unscoped calls impossible) + architecture test asserting every tenant repository accepts a scope argument.

## 5. Admin / Moderator Matrix

- The definitive permission matrix is `09-security/rbac.md`; `06-backend/authorization.md` (this file) only maps it to guards.
- Coding pattern: `@RequirePermissions('kyc:decide')`, `@RequireRoles(Role.ADMIN, Role.SUPER_ADMIN)` — matrix changes require updating *both* docs and the permission registry in code, verified by a CI conformance test (matrix ↔ guard decorators diff).
- Escalation rules that must appear in code: self-role-change blocked (staff test 3), Moderator cannot approve money actions, Super Admin is the only role manager (`FR-020`).

## 6. Where Frontend Guards Fit

Route guards and hidden buttons in `05-frontend/routing.md` §6 are **UX mirrors only**. Consequences:

1. Every guard decorator has a corresponding (stronger) server check — never the reverse.
2. API responses to unauthorized callers are 403 `FORBIDDEN` (or 404 for foreign resources to avoid existence disclosure).
3. Test TC-014 style checks: call API directly with a banned/tampered client → denied.

## 7. Audit Hooks for Privileged Actions (SEC-REQ-010, BR-PLT-06)

| Action class | Examples | Requirement |
|---|---|---|
| Role/permission changes | invite/remove staff, change roles | audit + notify affected user |
| Money | wallet freeze, refund approval, payout release, bank top-up verify (`BR-PAY-04/09`) | append-only entry: actor, action, entity, before/after, IP, timestamp |
| Order overrides | admin state override, dispute resolution | audit + reason mandatory |
| Content moderation | hide review (`BR-REV-04`) | audit entry |

Emitted via `shared/events` → `b13-platform` audit writer; audit table is append-only (DATA-REQ-007 posture).

## 8. Verification

| Test | Coverage |
|---|---|
| Unit | permission registry resolution, ownership predicate logic |
| Integration | each endpoint class called with wrong role → 403; foreign ID → 404 |
| Conformance (CI) | RBAC matrix ↔ guard decorators diff must be empty |
| Security tests | TC-011…TC-014 (cross-user, cross-store, staff escalation, direct API bypass) |
| Regression | every `SEC-REQ-004` test in `02-requirements/security/` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
