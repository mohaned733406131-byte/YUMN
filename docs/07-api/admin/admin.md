---
document_id: DOC-API-019
title: API-ADM — Platform Administration, Roles, Audit, Tickets & Health (FR-002, FR-019, FR-020)
category: 07-api
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-27
author: analysis-agent
source_of_truth: false
related_requirements: [FR-002, FR-019, FR-020, FR-007, FR-013, FR-014, FR-015, FR-016, NFR-007, NFR-019, SEC-REQ-004, SEC-REQ-005, SEC-REQ-010, SEC-REQ-012, DATA-REQ-007, DATA-REQ-008, BR-PLT-06, BR-PLT-07, BR-VND-03, BR-VND-04, BR-PAY-04, BR-PAY-09, BR-RET-05, BR-SHP-03, BR-ORD-10, BR-REV-04]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-002, DOC-FR-020, DOC-BA-005, DOC-OVR-008]
---

# API-ADM — Platform Administration, Roles, Audit, Tickets & Health

**Group:** `API-ADM` · **FR-002 (roles), FR-019/FR-020 (admin console)** · **Endpoints:** `API-ADM-001…043` · **Base:** `/api/v1`

Deny-by-default RBAC (`FR-002`): every write requires the exact role; `MODERATOR` is read-only outside moderation/ticket actions; role assignment and platform settings are **`SUPER_ADMIN`-only** and each change writes an append-only audit entry (`SEC-REQ-004`, `SEC-REQ-010`, `BR-PLT-06`). Demoting/removing the final Super Admin is refused with `LAST_SUPER_ADMIN` (`UC-037`). The audit log is **cursor-paginated — the documented offset exception** (`pagination.md` §1, `UC-036`) and can never be written or deleted through the API (`AUDIT_LOG_IMMUTABLE`). This file also owns **support tickets** (customer-facing `/support/tickets` + admin queue): the delivery-code lock auto-creates a ticket with the full timeline (`BR-SHP-03`, `C-16`). Health endpoints are unauthenticated liveness/readiness probes (`BR-PLT-07`).

---

## 1. Endpoint Table

### 1.1 Users & vendor moderation

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-001 | `GET /admin/users` | `ADMIN`, `MODERATOR` | User directory (offset table); the **vendor/KYC queue is this list filtered** (`?role=VENDOR&kycStatus=&storeStatus=`) | `?page&pageSize&role&q&status&kycStatus&sort=createdAt_desc` → `200 { items: [ { id, phoneMasked, displayName, roles, status: "ACTIVE"\|"SUSPENDED", store?: { id, status }, kycStatus?, createdAt } ], page: {…}, total }` | `FORBIDDEN`, `VALIDATION_ERROR` | FR-020, SEC-REQ-004, `DATA-REQ-008`, `UC-036` |
| API-ADM-002 | `GET /admin/users/{id}` | `ADMIN`, `MODERATOR` | Full profile incl. roles, sessions count, store/KYC projection, `assignableRoles` (the fixed role catalog — there is no separate roles endpoint in v1), recent audit entries | → `200 { …user, sessions: { active }, store?, kyc?, assignableRoles: [ …FR-002 catalog ], recentActions: [ { at, action, actorId } ] }` | `NOT_FOUND`, `FORBIDDEN` | FR-002, FR-020, SEC-REQ-004 |
| API-ADM-003 | `POST /admin/users/{id}/suspend` | `ADMIN` | Suspend a user: sessions revoked, vendor store inherits suspension (`BR-VND-04`), wallet frozen (`BR-PAY-09`); required on 5 confirmed spam/abuse reports | `{ reason, note? }` → `200 { id, status: "SUSPENDED", suspendedAt, affected: { sessionsRevoked, storeSuspended, walletFrozen }, auditId }` | `REASON_REQUIRED`, `STATE_CONFLICT` (already suspended), `LAST_SUPER_ADMIN` (suspending the final Super Admin), `NOT_FOUND` | FR-020, SEC-REQ-005, `BR-PLT-06` |
| API-ADM-004 | `POST /admin/users/{id}/activate` | `ADMIN` | Reactivate a suspended user (reverse of API-ADM-003, per-scope flags) | `{ scopes: ["ACCOUNT","STORE","WALLET"], reason }` → `200 { id, status: "ACTIVE", auditId }` | `STATE_CONFLICT` (not suspended), `REASON_REQUIRED`, `KYC_NOT_APPROVED` (store reactivation blocked until KYC valid), `NOT_FOUND` | FR-020, `BR-VND-04` |

### 1.2 KYC review

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-005 | `GET /admin/kyc` | `ADMIN`, `MODERATOR` (read), `ADMIN` decide | KYC queue with **48 h SLA** age (`BR-VND-03`) (offset) | `?page&pageSize&status&sort=slaDueAt_asc` → `200 { items: [ { submissionId, vendorId, storeName, status: "PENDING"\|"IN_REVIEW", submittedAt, slaDueAt, overdue, documents: { count } } ], page: {…}, total }` | `FORBIDDEN`, `VALIDATION_ERROR` | FR-007, FR-020, `BR-VND-03`, `UC-035` |
| API-ADM-006 | `GET /admin/kyc/{id}` | `ADMIN`, `MODERATOR` | Submission detail: documents (image/PDF links, scanned), extracted fields, history | → `200 { …submission, documents: [ { fileId, kind, url, scanStatus } ], extracted: {…}, timeline }` | `NOT_FOUND` | FR-007, SEC-REQ-011 |
| API-ADM-007 | `POST /admin/kyc/{id}/approve` | `ADMIN` | Approve KYC — `PENDING/IN_REVIEW → APPROVED`; unlocks publishing, payouts (`BR-VND-01`, `BR-ESC-06`) | `{ note? }` → `200 { status: "APPROVED", decidedAt, by, auditId }` — must land before SLA auto-escalation, else `KYC_DECISION_LATE` | `KYC_DECISION_LATE`, `STATE_CONFLICT`, `NOT_FOUND`, `FORBIDDEN` (Moderator) | FR-007, `BR-VND-01/03`, `UC-035` |
| API-ADM-008 | `POST /admin/kyc/{id}/reject` | `ADMIN` | Reject KYC with mandatory reason; vendor may resubmit | `{ reason, note? }` → `200 { status: "REJECTED", reason, decidedAt, auditId }` | `KYC_DECISION_LATE`, `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND`, `FORBIDDEN` | FR-007, `BR-VND-03`, `UC-035` |

### 1.3 Store lifecycle

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-009 | `GET /admin/stores` | `ADMIN`, `MODERATOR` | Store directory (offset) | `?page&pageSize&status&q&governorate` → `200 { items: [ { id, name, ownerId, status, kycStatus, rating?, createdAt } ], page: {…}, total }` | `FORBIDDEN`, `VALIDATION_ERROR` | FR-019, FR-020 |
| API-ADM-010 | `GET /admin/stores/{id}` | `ADMIN`, `MODERATOR` | Store detail: status, KYC link, commission tier, products count, open returns/disputes | → `200 { …store, commission: { tierPercent }, counts: { products, ordersOpen, returnsOpen }, kycStatus }` | `NOT_FOUND` | FR-019, `BR-ESC-03` |
| API-ADM-011 | `POST /admin/stores/{id}/approve` | `ADMIN` | Approve a newly created store — `PENDING → ACTIVE` (blocked until KYC approved) | `{ note? }` → `200 { status: "ACTIVE", auditId }` | `KYC_NOT_APPROVED`, `STATE_CONFLICT`, `NOT_FOUND` | FR-007, `BR-VND-01`, `UC-015` |
| API-ADM-012 | `POST /admin/stores/{id}/suspend` | `ADMIN` | Suspend a store: delists products, blocks orders, freezes escrow payouts for open cases | `{ reason, note? }` → `200 { status: "SUSPENDED", affected: { productsDelisted, ordersBlocked }, auditId }` — moderation hide stays reversible separately | `REASON_REQUIRED`, `STATE_CONFLICT`, `NOT_FOUND` | FR-019, `BR-VND-04`, `BR-ESC-06` |
| API-ADM-013 | `POST /admin/stores/{id}/activate` | `ADMIN` | Re-activate a suspended store | `{ reason }` → `200 { status: "ACTIVE", auditId }` | `STATE_CONFLICT`, `KYC_NOT_APPROVED`, `REASON_REQUIRED`, `NOT_FOUND` | FR-019, `BR-VND-04` |

### 1.4 Categories & attributes (platform taxonomy)

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-014 | `GET /admin/categories` | `ADMIN`, `MODERATOR` (read); taxonomy edits are `ADMIN` | Full category tree incl. drafts and per-locale slugs | `?includeHidden` → `200 { items: [ { id, parentId, name: { ar, en }, slug: { ar, en }, level, path, sortOrder, isActive, productCount } ] }` (tree, not paged) | `FORBIDDEN`, `VALIDATION_ERROR` | FR-004, `BR-CAT-03`, `UC-017` |
| API-ADM-015 | `POST /admin/categories` | `ADMIN` | Create a category node | `{ parentId?, name: { ar, en }, slug: { ar, en }, sortOrder?, attributeIds? }` → `201 { …category, level }` — depth ≤ 5 enforced | `CATEGORY_DEPTH_EXCEEDED`, `SLUG_TAKEN`, `VALIDATION_ERROR`, `FORBIDDEN` | FR-004, `BR-CAT-03` |
| API-ADM-016 | `PUT /admin/categories/{id}` | `ADMIN` | Rename/re-slug/reorder/move a node | `{ name?, slug?, parentId?, sortOrder?, isActive? }` → `200 { …category }` — move revalidates the 5-level depth and creates slug redirects | `CATEGORY_DEPTH_EXCEEDED`, `SLUG_TAKEN`, `VALIDATION_ERROR`, `NOT_FOUND`, `FORBIDDEN` | FR-004, `BR-CAT-03`, SEC-REQ-012 (slug redirects) |
| API-ADM-017 | `DELETE /admin/categories/{id}` | `ADMIN` | Delete an empty category (soft — keeps history; products force a prior move) | → `204` | `STATE_CONFLICT` (children or products present ⇒ move them first), `NOT_FOUND`, `FORBIDDEN` | FR-004, `BR-CAT-03` |
| API-ADM-018 | `GET /admin/attributes` | `ADMIN`, `MODERATOR` (read) | Attribute dictionary used by products/filters (offset; `total` exact) | `?page&pageSize&type&active` → `200 { items: [ { id, name: { ar, en }, type: "TEXT"\|"NUMBER"\|"SELECT"\|"MULTI_SELECT", options?, active, productCount } ], page: {…}, total: { value, relation } }` | `FORBIDDEN` | FR-004 |
| API-ADM-019 | `POST /admin/attributes` | `ADMIN` | Create an attribute | `{ name: { ar, en }, type, options?, unit?, filterable? }` → `201 { …attribute }` | `DUPLICATE_RESOURCE`, `VALIDATION_ERROR`, `FORBIDDEN` | FR-004 |
| API-ADM-020 | `PUT /admin/attributes/{id}` | `ADMIN` | Update or disable an attribute | `{ name?, options?, active?, filterable? }` → `200 { …attribute }` — disabling keeps historical product values readable | `VALIDATION_ERROR`, `NOT_FOUND`, `FORBIDDEN` | FR-004 |
| API-ADM-021 | `DELETE /admin/attributes/{id}` | `ADMIN` | Delete an attribute **never used by products** (hard-delete guard) | → `204` | `STATE_CONFLICT` (in use ⇒ disable instead), `NOT_FOUND`, `FORBIDDEN` | FR-004 |

### 1.5 Platform settings

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-022 | `GET /admin/settings` | `ADMIN`, `MODERATOR` (read) | All platform settings with schemas, defaults and versions (`UC-035`) | `?group` → `200 { settings: [ { key, group: "GENERAL"\|"PAYMENT"\|"LOGISTICS"\|"COMMISSION"\|"SECURITY", value, schema, defaultValue, version, updatedBy, updatedAt } ] }` — includes commission tiers (5–20%, default 10%, `BR-ESC-03`), top-up/order bounds, return windows, shipping zones | `FORBIDDEN` | FR-019, `BR-ESC-03`, `UC-035`, `stores.md` (commission read) |
| API-ADM-023 | `PUT /admin/settings/{key}` | `SUPER_ADMIN` | Update one setting with optimistic locking | `{ value, expectedVersion }` → `200 { key, value, version, auditId }` — value validated against the setting's schema (e.g., commission tier must stay 5–20) | `SETTINGS_VERSION_CONFLICT` (409, stale `expectedVersion`), `VALIDATION_ERROR` (schema/BR bounds), `PRECONDITION_FAILED`, `FORBIDDEN` (non–Super Admin), `NOT_FOUND` | FR-019, `BR-PLT-06`, `UC-035`, SEC-REQ-004 |

### 1.6 Audit & role management

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-024 | `GET /admin/audit-log` | `ADMIN`, `MODERATOR` | Append-only audit trail — **the sole cursor-paginated admin table** (`pagination.md` §1) | `?actorId&targetId&action&from&to&limit&cursor` → `200 { items: [ { id, at, actorId, actorRole, action, targetType, targetId, reason?, ipHash, correlationId } ], page: {…} }` — never editable (`AUDIT_LOG_IMMUTABLE` on any write attempt) | `FORBIDDEN`, `VALIDATION_ERROR` | FR-020, SEC-REQ-010, DATA-REQ-007, `UC-036`, `BR-PLT-06` |
| API-ADM-025 | `POST /admin/users/{id}/role` | `SUPER_ADMIN` | Grant a role (customer↔vendor flow, staff onboarding, admin promotion) | `{ role, reason? }` → `200 { id, roles: [...], auditId }` — granting `VENDOR` on a customer pre-creates the one-store draft (`BR-VND-02`) | `ROLE_ASSIGNMENT_FORBIDDEN` (caller not Super Admin), `INVALID_ROLE`, `LAST_SUPER_ADMIN` (guarded from any demotion side-effect), `STATE_CONFLICT`, `NOT_FOUND` | FR-002, SEC-REQ-004, `UC-037`, `BR-VND-02` |
| API-ADM-026 | `DELETE /admin/users/{id}/role` | `SUPER_ADMIN` | Revoke a role (demotion) — **never the final Super Admin** | `?role&reason=` → `200 { id, roles: [...], auditId }` | `LAST_SUPER_ADMIN`, `ROLE_ASSIGNMENT_FORBIDDEN`, `INVALID_ROLE` (cannot revoke the last role — the account always retains `CUSTOMER` base), `NOT_FOUND` | FR-002, SEC-REQ-004, `UC-037` |

### 1.7 Content moderation

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-027 | `GET /admin/moderation` | `ADMIN`, `MODERATOR` | Moderation queue: reported products/reviews/media, auto-flagged content (offset) | `?page&pageSize&type=PRODUCT\|REVIEW\|IMAGE&status=PENDING&sort=reportedAt_asc` → `200 { items: [ { type, id, storeId, reason, reports: n, reportedAt, currentStatus } ], page: {…}, total }` | `FORBIDDEN`, `VALIDATION_ERROR` | FR-019, `BR-REV-04`, `BR-ORD-06` (5-report flag) |
| API-ADM-028 | `POST /admin/moderation/{type}/{id}/hide` | `ADMIN`, `MODERATOR` | Hide content from all public surfaces (`BR-REV-04`; referenced by `catalog.md`) | `{ reason }` → `200 { type, id, hidden: true, hiddenBy, auditId }` — product ⇒ delisted; review ⇒ excluded from averages after recompute | `REASON_REQUIRED`, `STATE_CONFLICT` (already hidden), `NOT_FOUND` | FR-019, `BR-REV-04` |
| API-ADM-029 | `POST /admin/moderation/{type}/{id}/restore` | `ADMIN`, `MODERATOR` | Un-hide previously hidden content | `{ reason }` → `200 { type, id, hidden: false, auditId }` | `STATE_CONFLICT` (not hidden), `REASON_REQUIRED`, `NOT_FOUND` | FR-019, `BR-REV-04` |

### 1.8 Top-ups & wallet operations

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-030 | `GET /admin/topups` | `ADMIN`, `MODERATOR` (read) | Bank-transfer top-ups awaiting verification (`BR-PAY-04`) (offset) | `?page&pageSize&status=PENDING_VERIFICATION&method` → `200 { items: [ { topupId, userId, amount, method, proofFileId?, createdAt } ], page: {…}, total }` | `FORBIDDEN`, `VALIDATION_ERROR` | FR-013, FR-020, `BR-PAY-04`, `UC-034` |
| API-ADM-031 | `POST /admin/topups/{id}/verify` | `ADMIN` | Verify and credit the wallet — balanced ledger rows, idempotent | `{ note? }` → `200 { topupId, status: "CREDITED", creditedAt, ledgerReference, auditId }` — replay returns the same result (first success wins) | `STATE_CONFLICT` (already decided), `TOPUP_CREDIT_PENDING`, `NOT_FOUND` | FR-013, `BR-PAY-04/06/08`, `UC-034` |
| API-ADM-032 | `POST /admin/topups/{id}/reject` | `ADMIN` | Reject a top-up with reason (no ledger posting) | `{ reason, note? }` → `200 { status: "REJECTED", auditId }` | `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND` | FR-013, `BR-PAY-04` |
| API-ADM-033 | `POST /admin/wallets/{userId}/freeze` | `ADMIN` | Freeze a wallet (fraud/abuse) — pay/top-up blocked, refunds still credit | `{ reason, note? }` → `200 { userId, status: "FROZEN", auditId }` | `STATE_CONFLICT` (already frozen), `REASON_REQUIRED`, `NOT_FOUND` | FR-013, `BR-PAY-09` |
| API-ADM-034 | `POST /admin/wallets/{userId}/unfreeze` | `ADMIN` | Lift a freeze | `{ reason }` → `200 { userId, status: "ACTIVE", auditId }` | `STATE_CONFLICT` (not frozen), `REASON_REQUIRED`, `NOT_FOUND` | FR-013, `BR-PAY-09` |

### 1.9 Support tickets (customer-facing + admin queue)

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-035 | `POST /support/tickets` | `CUSTOMER`, `VENDOR`, `COURIER` | Open a support ticket (order/delivery/payment/manual: the 6-digit lock auto-creates one with the timeline attached) — **requires `Idempotency-Key`** | `{ category, subject, body, orderId?, attachmentFileIds? }` → `201 { ticketId, status: "OPEN", number: "SUP-000123", createdAt }` | `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `VALIDATION_ERROR`, `FILE_SCAN_FAILED`, `RATE_LIMITED` | FR-019, `BR-SHP-03`, SEC-REQ-011 |
| API-ADM-036 | `GET /support/tickets` | Any authenticated (own tickets only) | Own ticket feed — **cursor** (`pagination.md` §1 lists `GET /support/tickets` as a cursor stream) | `?status&limit&cursor` → `200 { items: [ { ticketId, number, subject, status: "OPEN"\|"IN_PROGRESS"\|"RESOLVED"\|"CLOSED", updatedAt, unreadFromSupport } ], page: {…} }` | `AUTH_INVALID`, `VALIDATION_ERROR` | FR-019, `DATA-REQ-008` |
| API-ADM-037 | `GET /support/tickets/{id}` | Ticket owner, `ADMIN`, `MODERATOR` | Ticket detail with the full message thread and linked entities | → `200 { ticketId, number, category, status, assignedTo?, messages: [ { id, byRole, body, attachmentFileIds?, at } ], linked: { orderId?, deliveryId? }, timeline? }` | `NOT_FOUND` (foreign ⇒ 404), `TIMELINE_ACCESS_DENIED` | FR-019, `BR-ORD-09` |
| API-ADM-038 | `POST /support/tickets/{id}/messages` | Ticket owner, `ADMIN`, `MODERATOR` | Append a message to the thread (customer reply or support reply — same endpoint, role-scoped projection) | `{ body, attachmentFileIds? }` → `201 { message }`; `IN_PROGRESS` once a staff member replies | `TICKET_STATE_CONFLICT` (resolved/closed), `VALIDATION_ERROR`, `FILE_SCAN_FAILED`, `NOT_FOUND` | FR-019, `DATA-REQ-008` |
| API-ADM-039 | `GET /admin/tickets` | `ADMIN`, `MODERATOR` | Support queue incl. auto-created delivery-code tickets and SLA escalations (offset) | `?page&pageSize&status&category&source=AUTO\|MANUAL&sort=updatedAt_asc` → `200 { items: [ { ticketId, number, category, source, status, userId, orderId?, assignedTo?, overdue } ], page: {…}, total }` | `FORBIDDEN`, `VALIDATION_ERROR` | FR-019, FR-020, `BR-SHP-03` |
| API-ADM-040 | `POST /admin/tickets/{id}/assign` | `ADMIN` (assigns to self or a moderator) | Claim/assign a ticket — `OPEN → IN_PROGRESS` | `{ assigneeId? }` → `200 { ticketId, status: "IN_PROGRESS", assignedTo, auditId }` | `TICKET_STATE_CONFLICT`, `NOT_FOUND`, `FORBIDDEN` (Moderator cannot reassign others' tickets) | FR-019, `BR-PLT-06` |
| API-ADM-041 | `POST /admin/tickets/{id}/resolve` | `ADMIN`, `MODERATOR` | Resolve a ticket with a resolution note — customer may reopen once from `GET /support/tickets/{id}` before it is closed | `{ resolution }` → `200 { ticketId, status: "RESOLVED", resolvedAt, auditId }` | `TICKET_STATE_CONFLICT` (already resolved/closed), `VALIDATION_ERROR` (resolution required), `NOT_FOUND` | FR-019, FR-020 |

### 1.10 Health probes (unauthenticated)

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ADM-042 | `GET /healthz` | Public | Liveness: process up, no dependency checks — polled by the orchestrator | → `200 { status: "UP", version, uptimeSeconds }` | `SERVICE_UNAVAILABLE` (process in shutdown) | FR-020, `BR-PLT-07`, NFR-007 |
| API-ADM-043 | `GET /readyz` | Public | Readiness: Postgres, Redis, BullMQ, Elasticsearch, providers reachable within budget; gates traffic (`BR-PLT-07`) | → `200 { status: "READY", checks: [ { name, status: "UP"\|"DOWN", latencyMs } ] }` — any DOWN ⇒ `503` + `SERVICE_UNAVAILABLE`, degraded search flips to category-browse fallback (`NFR-007`) | `SERVICE_UNAVAILABLE` (503 with per-check detail; never leaks hostnames — `SEC-REQ-008`) | FR-020, `BR-PLT-07`, NFR-007, `BR-ESC-07` |

## 2. Behavior Notes

- **Audit coverage** (`SEC-REQ-010`, `BR-PLT-06`): suspend/activate, KYC decisions, store approve/suspend, taxonomy edits, settings writes, role grant/revoke, moderation hide/restore, top-up verify/reject, wallet freeze/unfreeze, ticket assign/resolve, and every forced order transition (`orders.md API-ORD-014`) each return an `auditId` and append an immutable entry readable only through `API-ADM-024`.
- **Super Admin restrictions** (`UC-037`): only `PUT /admin/settings/{key}`, `POST|DELETE /admin/users/{id}/role` require `SUPER_ADMIN`; `LAST_SUPER_ADMIN` protects the final Super Admin from demotion, role revocation and suspension.
- **Moderator scope** (`SEC-REQ-004`): read across users/stores/KYC/queues + moderation hide/restore + ticket reply/resolve; no settings, roles, taxonomy, financial or suspend actions (403 `FORBIDDEN`).
- **SLA mechanics**: KYC 48 h (`BR-VND-03` → `KYC_DECISION_LATE`), return decision 48 h escalations surface as queue flags, delivery-code lock auto-ticket (`BR-SHP-03`) lands in `GET /admin/tickets` with `source: "AUTO"`.
- **Support thread integrity** (`DATA-REQ-008`): a ticket is visible only to its opener, assigned staff and admins — foreign tickets are 404; attachments follow the shared upload rules (`api-conventions.md` §10, `SEC-REQ-011`).
- **No PHI/secret leakage**: health checks report names/status/latency only; audit entries store `ipHash`, not raw IPs (`SEC-REQ-008`).
- **Related groups**: order overrides in `orders.md`, return/dispute arbitration in `returns.md`, top-up/freeze counterpart flows in `wallet.md`, reconciliation data in `analytics.md`.

## 3. Pagination / Idempotency / Caching

| Endpoint(s) | Mode |
|---|---|
| `API-ADM-024` (audit log) | **cursor — documented exception** (`pagination.md` §1) |
| `API-ADM-001`, `005`, `009`, `018`, `030`, `039` | offset |
| `API-ADM-036` (customer tickets) | cursor |
| `API-ADM-014` (tree), health, single resources | n/a |

Mandatory idempotency key: `API-ADM-035` (`BR-PLT-03`). Settings writes use optimistic locking via `expectedVersion` (409 `SETTINGS_VERSION_CONFLICT`). All responses `Cache-Control: no-store` (health: `no-store`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | `API-ADM-042/043` paths `/health/live` + `/health/ready` → `/healthz` + `/readyz` | `REC-05`/`TD-06` health-path canonization to the `BR-PLT-07` spelling used by probes/CI/monitoring; closes `CT-02` |
