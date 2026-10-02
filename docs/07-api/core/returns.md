---
document_id: DOC-API-015
title: API-RET — Returns, Refunds & Disputes (FR-016)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-016, FR-012, FR-013, FR-014, FR-015, FR-017, FR-020, NFR-008, DATA-REQ-007, SEC-REQ-011, BR-RET-01, BR-RET-02, BR-RET-03, BR-RET-04, BR-RET-05, BR-RET-06, BR-RET-07, BR-ORD-04, BR-ORD-05, BR-PAY-07, BR-PAY-08, BR-ESC-04, BR-ESC-07]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-016, DOC-SA-010, DOC-BA-005, DOC-OVR-008]
---

# API-RET — Returns, Refunds & Disputes

**Group:** `API-RET` · **FR-016** · **Endpoints:** `API-RET-001…017` · **Base:** `/api/v1`

Return window = delivery confirmation + product `returnPeriodDays`; `isReturnable = false` or elapsed window ⇒ rejection (`BR-RET-01`, `C-11`). State sequence inside the 17-state machine: `RETURN_REQUESTED → RETURN_APPROVED / RETURN_REJECTED → RETURN_RECEIVED → REFUNDED` (`BR-RET-02`). Vendor decision SLA **48 h** (auto-escalate to admin), inspection SLA **72 h** (auto-approve), wallet credit ≤ **3 business days** (`BR-RET-04/05`). Refund composition: item value; shipping refunded only for platform/vendor fault (`BR-RET-03`). Disputes freeze escrow for the affected sub-orders until admin resolution (`BR-ORD-05`); admin is final arbiter with an audit entry (`BR-RET-06`, `BR-PLT-06`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-RET-001 | `POST /orders/{id}/returns` | `CUSTOMER` (order owner) | Open a return request for order items — `DELIVERED/COMPLETED → RETURN_REQUESTED` | `{ items: [ { orderItemId, quantity, reasonCode, note?, imageFileIds? } ], reasonCode }` → `201 { returnId, subOrderId, state: "RETURN_REQUESTED", window: { deliveryAt, deadline, daysRemaining }, refundEstimate: { itemValue, shippingRefundable } }` | `WINDOW_EXPIRED`, `NOT_RETURNABLE`, `STATE_CONFLICT`, `DISPUTE_ALREADY_OPEN`, `VALIDATION_ERROR`, `FILE_SCAN_FAILED`, `NOT_FOUND` | FR-016, `BR-RET-01/03`, `C-11`, `AC-FR016-01/02`, `UC-021` |
| API-RET-002 | `GET /returns` | `CUSTOMER` | Own return requests (cursor feed) | `?state&limit&cursor` → `200 { items: [ { returnId, orderId, subOrderId, state, openedAt, decisionDueAt? } ], page: {…} }` | `AUTH_INVALID`, `VALIDATION_ERROR` | FR-016, `DATA-REQ-008` |
| API-RET-003 | `GET /returns/{id}` | `CUSTOMER` (owner), `VENDOR` (own store), `ADMIN`/`MODERATOR` | Return detail: items, reason/evidence, policy math, decision, inspection, refund status | → `200 { returnId, orderId, subOrderId, state, items, policy: { isReturnable, returnPeriodDays, windowDeadline }, decision?: { outcome, reason, by, at }, inspection?: { outcome, notes, images, at, autoApproved }, refund: { status, amount, walletCredit: { reference, creditedAt? } }, pickup: { status, deliveryId? }, timeline: [...] }` | `NOT_FOUND`, `TIMELINE_ACCESS_DENIED` | FR-016, `BR-RET-02/05`, `BR-ORD-09` |
| API-RET-004 | `GET /store/returns` | `VENDOR` | Own-store return queue with SLA age (offset table) | `?page&pageSize&state&sort=decisionDueAt_asc` → `200 { items: [ { returnId, orderId, state, customerNameMasked, openedAt, decisionDueAt, overdue } ], page: {…}, total }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-016, `BR-VND-07`, `BR-RET-05` |
| API-RET-005 | `GET /store/returns/{id}` | `VENDOR` | Vendor return view: item, reason, evidence, policy + window calculation | → `200 { …return (as API-RET-003), eligibility: { withinWindow, daysRemaining } }` | `NOT_FOUND` (foreign store ⇒ 404) | FR-016, `UC-021`, `C-11` |
| API-RET-006 | `POST /store/returns/{id}/approve` | `VENDOR`, `ADMIN` | Approve — `RETURN_REQUESTED → RETURN_APPROVED`; schedules the return pickup through the delivery engine | `{ note? }` → `200 { state: "RETURN_APPROVED", version, pickup: { status: "OFFERED" }, slaClearedAt }` — decision must land within 48 h | `STATE_CONFLICT`, `RETURN_WINDOW_CLOSED`, `NOT_FOUND`, `STORE_SUSPENDED` | FR-016, `BR-RET-02`, `BR-SHP-04` mechanics, `UC-021`, `DOC-SA-010` §2 |
| API-RET-007 | `POST /store/returns/{id}/reject` | `VENDOR`, `ADMIN` | Reject with mandatory reason — `RETURN_REQUESTED → RETURN_REJECTED` (later settles to `COMPLETED`) | `{ reason, note? }` → `200 { state: "RETURN_REJECTED", version, historyEntry }` | `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND`, `STORE_SUSPENDED` | FR-016, `BR-RET-02`, `UC-021`, `DOC-SA-010` §2 |
| API-RET-008 | `GET /returns/{id}/pickup` | `CUSTOMER` (owner), `VENDOR`, `ADMIN` | Return pickup schedule/status (read-only — pickup assignment reuses the courier flow, customer scheduling is out of scope) | → `200 { status: "OFFERED"\|"ASSIGNED"\|"PICKED_UP"\|"RECEIVED", courier?: { nameMasked }, assignedAt?, receivedAt? }` | `NOT_FOUND`, `STATE_CONFLICT` (no pickup for a rejected return) | FR-016, FR-015, `BR-SHP-04`, `C-16` (no GPS) |
| API-RET-009 | `POST /store/returns/{id}/inspection` | `VENDOR` (Manager/Owner), `ADMIN` | Inspection record after `RETURN_RECEIVED` — pass ⇒ refund, fail ⇒ admin review; must conclude within **72 h** or the return auto-approves | `{ outcome: "PASS"\|"FAIL", notes, imageFileIds? }` → `200 { state: "REFUNDED"\|"DISPUTED", inspection: {…}, refund: { status: "PENDING", expectedCreditBy } }` | `INSPECTION_WINDOW_PASSED` (auto-approval already ran), `STATE_CONFLICT`, `VALIDATION_ERROR`, `NOT_FOUND` | FR-016, `BR-RET-05`, `AC-FR016-03`, `C-09` |
| API-RET-010 | `GET /admin/returns` | `ADMIN`, `MODERATOR` | Platform return queue incl. 48 h SLA breaches auto-escalated from vendors (offset) | `?page&pageSize&state&overdue&sort=decisionDueAt_asc` → `200 { items: [ …return summary + { escalated: true\|false, vendorDecisionOverdue } ], page: {…}, total }` | `FORBIDDEN` (scoped fields for Moderator) | FR-016, FR-020, `BR-RET-05`, `BR-VND-03` |
| API-RET-011 | `POST /admin/returns/{id}/approve` | `ADMIN` | Admin approves on behalf of a stalled/disputed case (final authority) | `{ reason }` → `200 { state: "RETURN_APPROVED", version, auditId }` — audit entry required | `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND` | FR-016, FR-020, `BR-RET-06`, `BR-PLT-06` |
| API-RET-012 | `POST /admin/returns/{id}/reject` | `ADMIN` | Admin rejection with reason (policy/dispute conflicts resolved here) | `{ reason, note? }` → `200 { state: "RETURN_REJECTED", version, auditId }` | `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND` | FR-016, `BR-RET-06`, `BR-PLT-06` |
| API-RET-013 | `POST /orders/{id}/dispute` | `CUSTOMER` (buyer), `VENDOR` (own sub-order) | Open a dispute — sub-order `DELIVERED/COMPLETED → DISPUTED`, escrow frozen | `{ subOrderId, ground, note?, imageFileIds? }` → `201 { disputeId, state: "DISPUTED", escrowFrozen: true, evidenceDueBy }` | `DISPUTE_ALREADY_OPEN`, `STATE_CONFLICT`, `EVIDENCE_REQUIRED`, `VALIDATION_ERROR`, `NOT_FOUND` | FR-016, FR-012, `BR-ORD-05`, `DOC-SA-010` §2 |
| API-RET-014 | `GET /disputes` | `CUSTOMER` (own), `VENDOR` (own), `ADMIN`/`MODERATOR` (all) | Dispute list, role-scoped (cursor for parties; offset for admin via `?page`) | `?state&limit&cursor` → `200 { items: [ { disputeId, orderId, subOrderId, state, openedBy, openedAt, escrowFrozen, dueAt } ], page: {…} }` | `AUTH_INVALID`, `VALIDATION_ERROR` | FR-016, FR-020, `BR-ORD-05`, `BR-ORD-09` |
| API-RET-015 | `GET /disputes/{id}` | Parties + `ADMIN`/`MODERATOR` | Dispute detail with evidence and timeline | → `200 { disputeId, state: "OPEN"\|"RESOLVED_BUYER"\|"RESOLVED_VENDOR", ground, notes, evidence: [ { by, fileId, at } ], timeline, resolution? }` | `NOT_FOUND`, `TIMELINE_ACCESS_DENIED` | FR-016, `BR-ORD-05` |
| API-RET-016 | `POST /disputes/{id}/evidence` | `CUSTOMER` (own), `VENDOR` (own), `ADMIN` | Submit evidence (text + files) before the due date | `multipart { note?, file? }` or JSON `{ note, imageFileIds? }` → `201 { evidenceId, at }` — ≤5 images/files, scanned | `EVIDENCE_REQUIRED`, `PAYLOAD_TOO_LARGE`, `UNSUPPORTED_MEDIA_TYPE`, `FILE_SCAN_FAILED`, `STATE_CONFLICT` (already resolved), `NOT_FOUND` | FR-016, SEC-REQ-011 |
| API-RET-017 | `POST /disputes/{id}/resolve` | `ADMIN` (final arbiter) | Resolve: buyer win ⇒ `DISPUTED → REFUNDED` (refund flow executes); vendor win ⇒ `DISPUTED → COMPLETED` | `{ outcome: "BUYER"\|"VENDOR", reason }` → `200 { state, escrowFrozen: false, resolution, auditId, refund?: { status } }` — escrow unfreezes into the chosen path; commission reversed proportionally on buyer win | `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND`, `ARBITRATION_FORBIDDEN` (non-admin) | FR-016, FR-020, `BR-ORD-05`, `BR-RET-06/07`, `BR-ESC-04/07`, `AC-FR020-03`, `DOC-SA-010` §2 |

## 2. Behavior Notes

- **Window math** (`BR-RET-01`, `C-11`): `deadline = deliveryConfirmedAt + product.returnPeriodDays`; evaluated server-side at request time — `WINDOW_EXPIRED` (elapsed) and `NOT_RETURNABLE` (`isReturnable = false`) are distinct rejections.
- **Refund composition & timing** (`BR-RET-03/04`, `AC-FR016-04`): amount = item value (+ shipping when fault is platform/vendor); wallet credit ≤ 3 business days after `REFUNDED`; idempotent execution (`BR-PAY-08`) with balanced ledger rows (`BR-PAY-06`); receipt/status surfaced via `wallet.md` `GET /orders/{id}/refund`.
- **Auto-approve** (`BR-RET-05`, `AC-FR016-03`): an uninspected `RETURN_RECEIVED` return after 72 h transitions to `REFUNDED` by `SYSTEM`; a late vendor inspection then returns `INSPECTION_WINDOW_PASSED`.
- **Escalation** (`BR-VND-03` pattern): a vendor decision not made within 48 h auto-escalates to `GET /admin/returns` with an admin notification — the case is never left pending.
- **Escrow/commission effects** (`BR-RET-07`, `BR-ESC-04/07`): refund draws escrow first, then vendor payable; commission reverses proportionally; a dispute freezes only its sub-order's escrow (`BR-ORD-05`).
- **Cancellation refunds** share the same engine: `CANCELLED → REFUNDED` (`BR-ORD-04`) — status reported by `GET /orders/{id}/refund` (`API-WAL-014`).
- **Notifications**: each transition notifies customer and vendor in their locale (`BR-NTF-04`, FR-017).
- **No exchanges**: refund-only in v1 — no swap/exchange endpoints exist (FR-016 out-of-scope).

## 3. Pagination / Idempotency / Caching

| Endpoint(s) | Mode |
|---|---|
| `API-RET-002`, `API-RET-014` (party feeds) | cursor |
| `API-RET-004`, `API-RET-010` (queues) | offset |
| others | single resource |

Refund execution is idempotency-keyed (`BR-PAY-08`); approve/reject/dispute actions are guarded by `version` (409 `STATE_CONFLICT`). All responses `Cache-Control: no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
