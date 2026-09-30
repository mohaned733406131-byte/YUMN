---
document_id: DOC-API-012
title: API-ORD — Checkout & Order Lifecycle (FR-011, FR-012)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-011, FR-012, FR-010, FR-013, FR-014, FR-015, FR-016, FR-020, NFR-008, SEC-REQ-004, SEC-REQ-009, DATA-REQ-001, DATA-REQ-008, BR-ORD-01, BR-ORD-02, BR-ORD-03, BR-ORD-04, BR-ORD-05, BR-ORD-06, BR-ORD-07, BR-ORD-08, BR-ORD-09, BR-ORD-10, BR-FIN-01, BR-FIN-02, BR-FIN-05, BR-PAY-01, BR-PAY-05, BR-PRM-06]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-011, DOC-FR-012, DOC-SA-010, DOC-BA-005, DOC-OVR-008]
---

# API-ORD — Checkout & Order Lifecycle

**Group:** `API-ORD` · **FR-011 (checkout), FR-012 (lifecycle)** · **Endpoints:** `API-ORD-001…014` · **Base:** `/api/v1`

Checkout follows the canonical sequence **address → shipping → wallet payment → review → confirm** and produces **one master order + one sub-order per vendor** (`C-10`, `BR-ORD-02`). The 17-state machine executes **per sub-order** exactly as specified in `../../03-system-analysis/core/state-transitions.md`; any invalid transition or stale `version` returns **409 `STATE_CONFLICT`** (`C-09`, `BR-ORD-01`). Status history is append-only with actor/timestamp/reason (`BR-ORD-03`). Timeline visibility: buyer (own), vendor (own sub-orders), assigned courier (own delivery), admin/moderator scoped (`BR-ORD-09`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ORD-001 | `POST /checkout/session` | `CUSTOMER` | Start checkout: snapshot the cart, resolve address + shipping fee, apply coupon (if any), compute authoritative per-store totals, place the 15-minute stock reservation — **requires `Idempotency-Key`** | `{ addressId, shippingMethod, couponCode?, paymentMethod: "wallet" }` → `201 { sessionId, expiresAt, byStore: [ { storeId, items, subtotal, discount, vat, shippingFee, total } ], totals: { subtotal, discount, vat, shippingFee, grandTotal }, priceChanges: [...], blockers: [...], wallet: { balance, shortfall } }` | `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `ADDRESS_REQUIRED`, `NO_SHIPPING_ZONE`, `COUPON_INVALID`, `COUPON_STACKING_NOT_ALLOWED`, `PRICE_CHANGED`, `CART_ITEM_INELIGIBLE`, `RESERVATION_EXPIRED`, `VALIDATION_ERROR` | FR-011, `BR-SHP-01`, `BR-FIN-01/02`, `BR-PRM-06`, `BR-PLT-03`, `C-13`, `UC-011` |
| API-ORD-002 | `POST /orders` | `CUSTOMER` | Confirm and pay: wallet debit (atomic, never negative) + escrow funding + stock lock + master/sub creation → `PLACED` — **requires `Idempotency-Key`** | `{ checkoutSessionId, confirmTotals: true }` → `201 { orderId, masterState: "PLACED", subOrders: [ { id, storeId, total, state } ], payment: { amount, ledgerReference }, totals: {…}, createdAt, Location }` — duplicate key returns the **original** order with the original status code | `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `IDEMPOTENCY_IN_PROGRESS`, `CHECKOUT_SESSION_EXPIRED`, `INSUFFICIENT_FUNDS`, `WALLET_FROZEN`, `PAYMENT_METHOD_NOT_ALLOWED`, `ORDER_VALUE_OUT_OF_RANGE`, `STOCK_UNAVAILABLE`, `PRICE_CHANGED`, `COUPON_INVALID`, `RATE_LIMITED` | FR-011, `BR-ORD-06`, `BR-PAY-01/05/06/08`, `BR-CRT-06`, `C-01/C-10/C-14`, `AC-FR011-01…04`, `UC-011`, SEC-REQ-009 |
| API-ORD-003 | `GET /orders` | `CUSTOMER` | Own master-order feed (cursor) | `?status&limit&cursor` → `200 { items: [ { orderId, masterState, subOrdersSummary: [ { storeName, state } ], grandTotal, createdAt, thumbnail } ], page: {…} }` | `AUTH_INVALID`, `VALIDATION_ERROR` | FR-012, `BR-ORD-09`, `DATA-REQ-008`, `UC-012` |
| API-ORD-004 | `GET /orders/{id}` | `CUSTOMER` (owner), `VENDOR` (own sub-order projection), `ADMIN`/`MODERATOR` (scoped) | Master order detail: sub-orders, totals breakdown, wallet receipt, per-sub-order state | → `200 { orderId, masterState, version, address: {…}, totals: { subtotal, discount, vat, shippingFee, grandTotal }, payment: { method: "wallet", amount, ledgerReference, paidAt }, subOrders: [ { id, storeId, storeName, state, items: [...], totals: {…}, escrow: { status, releaseEligibleAt? } } ], returnPolicyApplied }` — vendor callers receive a masked ship-to | `NOT_FOUND`, `TIMELINE_ACCESS_DENIED`, `AUTH_INVALID` | FR-012, `BR-ORD-02/07/09`, `BR-FIN-02`, `C-10`, `UC-012` |
| API-ORD-005 | `GET /orders/{id}/timeline` | `CUSTOMER` (own), `VENDOR` (own sub-rows), `COURIER` (assigned), `ADMIN`/`MODERATOR` (scoped) | Append-only status history per sub-order with actor, timestamp, reason | → `200 { orderId, entries: [ { subOrderId, from, to, actorRole, actorName?, reason?, at } ] }` — never editable (`BR-ORD-03`); entries filtered to the caller's visibility slice | `NOT_FOUND`, `TIMELINE_ACCESS_DENIED` | FR-012, `BR-ORD-03/09`, `DOC-SA-010` |
| API-ORD-006 | `GET /store/orders` | `VENDOR` | Own sub-order queue (offset table), filters by state/SLA age | `?page&pageSize&status&sort=slaAge_desc` → `200 { items: [ { id, masterOrderId, state, customerNameMasked, total, placedAt, confirmDueAt } ], page: {…}, total }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-012, `BR-VND-07`, `BR-ORD-10`, `UC-019` |
| API-ORD-007 | `GET /store/orders/{id}` | `VENDOR` | Sub-order detail: items, masked ship-to, totals, payment confirmed, timeline slice | → `200 { …subOrder, masterOrderId, timeline: [...], package: { weightBand?, weightKg? } }` | `NOT_FOUND` (foreign sub-order ⇒ 404), `STORE_SUSPENDED` | FR-012, `BR-ORD-09`, `BR-VND-07`, `UC-019` |
| API-ORD-008 | `POST /store/orders/{id}/confirm` | `VENDOR` | Accept: `PLACED → CONFIRMED` | `{ note? }` → `200 { id, state: "CONFIRMED", version, historyEntry }` — guard: KYC approved + store active | `STATE_CONFLICT`, `KYC_NOT_APPROVED`, `STORE_SUSPENDED`, `NOT_FOUND` | FR-012, `BR-ORD-01`, `DOC-SA-010` §2, `UC-019` |
| API-ORD-009 | `POST /store/orders/{id}/processing` | `VENDOR` | Start fulfillment: `CONFIRMED → PROCESSING` | `{ note? }` → `200 { id, state: "PROCESSING", version, historyEntry }` | `STATE_CONFLICT`, `STORE_SUSPENDED`, `NOT_FOUND` | FR-012, `DOC-SA-010` §2, `UC-020` |
| API-ORD-010 | `POST /store/orders/{id}/ready` | `VENDOR` | Pack complete: `PROCESSING → READY_FOR_PICKUP` (records package weight for the shipping fee) | `{ weightKg?, note? }` → `200 { id, state: "READY_FOR_PICKUP", version, historyEntry }` — **last state in which vendor/customer cancellation is possible** | `STATE_CONFLICT`, `VALIDATION_ERROR`, `NOT_FOUND` | FR-012, FR-015, `BR-SHP-01`, `UC-020` |
| API-ORD-011 | `POST /store/orders/{id}/cancel` | `VENDOR` (until `READY_FOR_PICKUP`), `ADMIN` | Vendor reject/cancel with reason — triggers the wallet refund flow | `{ reason }` → `200 { id, state: "CANCELLED", version, refund: { status: "PENDING" } }` | `CANCEL_WINDOW_CLOSED`, `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND` | FR-012, `BR-ORD-04`, `BR-ORD-10`, `DOC-SA-010` §2 |
| API-ORD-012 | `POST /orders/{id}/cancel` | `CUSTOMER` (only while `PLACED` or `CONFIRMED`) | Customer cancellation with reason — refund flow always runs | `{ reason }` → `200 { id, state: "CANCELLED", version, refund: { status: "PENDING" } }` | `CANCEL_WINDOW_CLOSED`, `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND` | FR-012, `BR-ORD-04`, `AC-FR012-03`, `DOC-SA-010` §2 |
| API-ORD-013 | `GET /admin/orders` | `ADMIN`, `MODERATOR` | Platform operations queue: filters for state, SLA age, disputes, escalations (offset) | `?page&pageSize&status&escalated&disputed&sort=slaAge_desc` → `200 { items: [ { orderId, masterState, subOrders: [...], flags: ["SLA_24H","DELIVERY_ESCALATION"], grandTotal, createdAt } ], page: {…}, total }` | `FORBIDDEN` (Moderator read-only subset) | FR-012, FR-020, `BR-ORD-09/10`, `UC-033` |
| API-ORD-014 | `POST /admin/orders/{id}/transition` | `ADMIN` | Force a state override **inside** the canonical 17-state transition table (never invents states) | `{ subOrderId, toState, reason }` → `200 { subOrderId, state, version, historyEntry, auditId }` — every call writes an append-only audit entry; master re-evaluated (`BR-ORD-07`) | `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND`, `FORBIDDEN` (Moderator) | FR-012, FR-020, `BR-ORD-01/03`, `BR-PLT-06`, `C-09`, `SEC-REQ-010` |

## 2. Behavior Notes

- **Idempotent order creation** (`BR-ORD-06`, `AC-FR011-02`): the `Idempotency-Key` maps to exactly one order; retries return the original order (same status code) with no second wallet debit.
- **Wallet-only** (`BR-PAY-01`, `C-01`–`C-03`): `paymentMethod` other than `wallet` ⇒ 422 `PAYMENT_METHOD_NOT_ALLOWED`; no COD/card/BNPL fields exist on any request schema.
- **Order bounds** (`C-14`): validated against server-computed `totals.grandTotal` before any order row exists ⇒ 422 `ORDER_VALUE_OUT_OF_RANGE` outside 500–5,000,000 YER.
- **Totals math** (`BR-FIN-01/02/05`): sub-order total = (items − item discount) + VAT + shipping; VAT = 15% × (subtotal − coupon discount), shipping untaxed; half-up rounding to whole YER per sub-order; master total = Σ sub-order totals.
- **Cancel windows** (`BR-ORD-04`): customer — `PLACED`/`CONFIRMED` only; vendor/admin — until `READY_FOR_PICKUP`; a late attempt returns 409 `CANCEL_WINDOW_CLOSED`. Cancellation always triggers the refund flow (`CANCELLED → REFUNDED` by `SYSTEM`).
- **24-hour SLA** (`BR-ORD-10`): a sub-order still `CONFIRMED` 24 h after confirmation is escalated to admin review with a notification — never silently auto-cancelled; surfaced as the `SLA_24H` flag on `API-ORD-013`.
- **Concurrency**: transitions are guarded inside the order transaction with optimistic locking on `version`; a stale version or forbidden move ⇒ 409 `STATE_CONFLICT` and history is unchanged (`AC-FR012-02`).
- **Master aggregation** (`BR-ORD-07`): the master reaches `COMPLETED` only when every sub-order is `COMPLETED` or `REFUNDED`; a dispute freezes only the affected sub-order's escrow (`BR-ORD-05`).
- **Role scoping**: vendors never see other vendors' sub-orders (404), customers never see foreign orders (404), couriers see only assigned deliveries (`BR-ORD-09`, `DATA-REQ-008`).
- **Related groups**: delivery scans/`DELIVERED` gating in `delivery.md` (API-SHP); returns/disputes in `returns.md`; wallet refunds/escrow in `wallet.md`; escalation tooling in `admin.md`.

## 3. Pagination / Idempotency / Caching

| Endpoint(s) | Mode |
|---|---|
| `API-ORD-003` (customer feed) | cursor |
| `API-ORD-006`, `API-ORD-013` (queues) | offset |
| others | single resource |

Mandatory idempotency keys: `API-ORD-001`, `API-ORD-002` (`BR-PLT-03`). All responses `Cache-Control: no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
