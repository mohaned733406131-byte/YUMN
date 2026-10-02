---
document_id: DOC-API-011
title: API-CRT — Shopping Cart (FR-010)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-010, FR-004, FR-005, FR-011, FR-013, FR-019, NFR-001, NFR-008, SEC-REQ-004, DATA-REQ-008, BR-CRT-01, BR-CRT-02, BR-CRT-03, BR-CRT-04, BR-CRT-05, BR-CRT-06]
related_documents: [DOC-API-002, DOC-API-003, DOC-FR-010, DOC-BA-005, DOC-OVR-008]
---

# API-CRT — Shopping Cart

**Group:** `API-CRT` · **FR-010** · **Endpoints:** `API-CRT-001…007` · **Base:** `/api/v1`

One server-side cart per authenticated customer, grouped by vendor so the multi-vendor split (`C-10`) is previewable before checkout. Hard guards: **≤50 distinct products, ≤10 units per product, ≤5 vendors** (`BR-CRT-01`, `C-15`). Every add/quantity change starts or refreshes the **15-minute stock-reservation countdown** (`BR-CRT-02`, `C-13`); expiry releases reserved stock. All guard/price/eligibility checks are re-evaluated server-side at checkout — client checks are UX only (`SEC-REQ-004`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-CRT-001 | `GET /cart` | `CUSTOMER` (authenticated wallet owner) | Read the cart: lines grouped by vendor, quantities, line totals, cart subtotal (integer YER), reservation countdown | → `200 { items: [ { id, product: { id, slug, nameAr, imageUrl }, variantSku?, quantity, unitPrice, lineTotal, store: { id, slug, nameAr }, reservationExpiresAt, flags: { stale, priceChanged, ineligible } } ], byStore: [ { storeId, itemsCount, subtotal } ], subtotal, estimatedVat, estimatedShipping, itemCount, distinctProducts, distinctStores, reservationExpiresAt }` | `AUTH_INVALID` | FR-010, `BR-CRT-02/04`, `BR-FIN-01`, `UC-010` |
| API-CRT-002 | `POST /cart/items` | `CUSTOMER` | Add a product/variant — starts or refreshes the 15-minute reservation for the line | `{ productId, variantSku?, quantity }` → `201 { …cartItem, reservationExpiresAt, …cart totals }` — server re-validates guards, availability and price | `CART_LIMIT_EXCEEDED`, `MAX_VENDORS_EXCEEDED`, `UNIT_LIMIT_EXCEEDED`, `STOCK_UNAVAILABLE`, `CART_ITEM_INELIGIBLE`, `NOT_FOUND` (inactive product), `VALIDATION_ERROR` | FR-010, `BR-CRT-01/02`, `C-15`, `UC-009`, `AC-FR010-01/02` |
| API-CRT-003 | `PATCH /cart/items/{id}` | `CUSTOMER` | Change quantity (re-validates ≤10/unit and ≤50 products; refreshes reservation) | `{ quantity }` → `200 { …cartItem, …cart totals }` | `UNIT_LIMIT_EXCEEDED`, `CART_LIMIT_EXCEEDED`, `STOCK_UNAVAILABLE`, `RESERVATION_EXPIRED`, `NOT_FOUND`, `VALIDATION_ERROR` | FR-010, `BR-CRT-01/02`, `C-15`, `UC-010`, `AC-FR010-02` |
| API-CRT-004 | `DELETE /cart/items/{id}` | `CUSTOMER` | Remove a line; its reserved stock is released immediately | → `204` (or `200 { …cart }` when the client requests the refreshed cart) | `NOT_FOUND` | FR-010, `BR-CRT-02`, `UC-010` |
| API-CRT-005 | `DELETE /cart` | `CUSTOMER` | Clear the whole cart (all reservations released) | → `204` | `NOT_FOUND` (empty cart is idempotent 204) | FR-010, `BR-CRT-02` |
| API-CRT-006 | `POST /cart/merge` | `CUSTOMER` | Merge the client-side guest cart into the account cart on login — **requires `Idempotency-Key`** | `Idempotency-Key` + `{ items: [ { productId, variantSku?, quantity } ] }` → `200 { …cart, merged: { added, updated, rejected: [ { productId, reason } ] } }` — on quantity conflict the **server value wins**; guard violations reject the affected guest line only | `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `CART_LIMIT_EXCEEDED`, `MAX_VENDORS_EXCEEDED` | FR-010, `BR-CRT-03`, `BR-PLT-03`, `../../05-frontend/core/state-management.md` |
| API-CRT-007 | `GET /cart/checkout-view` | `CUSTOMER` | Server-recomputed per-store sub-cart preview for checkout: authoritative totals, price-change and eligibility flags, wallet shortfall | → `200 { byStore: [ { storeId, storeName, items: [...], subtotal, discount, vat, shippingEstimate, total } ], totals: { subtotal, discount, vat, shippingEstimate, grandTotal }, priceChanges: [ { productId, oldPrice, newPrice } ], blockers: [ { productId, reason } ], wallet: { balance, shortfall }, reservationExpiresAt }` | `CART_ITEM_INELIGIBLE`, `RESERVATION_EXPIRED`, `PRICE_CHANGED`, `NOT_FOUND` (empty cart) | FR-010, FR-011, `BR-CRT-04/05/06`, `BR-FIN-01/02`, `C-10`, `C-14` |

## 2. Behavior Notes

- **Guard ladder** (`BR-CRT-01`, `C-15`): each mutation checks, in order — product eligibility → per-product unit limit (10) → distinct-product limit (50) → distinct-vendor limit (5) → stock availability. The first violation determines the code; violations never partially mutate the cart.
- **Reservation countdown** (`C-13`): `reservationExpiresAt = lastActivityAt + 15 min`; add/patch refreshes it; a `GET` does **not** refresh it (reads are side-effect free). Expiry ⇒ reserved quantity released by the BullMQ timer and affected lines flagged `stale` with `RESERVATION_EXPIRED` on the next mutation (`BR-PLT-01/02`).
- **Price changes** (`BR-CRT-04`): the cart stores the price snapshot at add time; `GET /cart/checkout-view` reports every divergence in `priceChanges` and the client must re-confirm before `POST /orders` (which recomputes anyway — `BR-CRT-04` server-side recalculation).
- **Ineligible items** (`BR-CRT-05`): inactive/out-of-stock/out-of-policy lines appear with `flags.ineligible = true` and a `blockers` entry in the checkout view; checkout is refused until they are removed.
- **Balance gate** (`BR-CRT-06`, `C-01`): the checkout view reports `wallet.shortfall` (≥ 0) so the customer can top up (`POST /wallet/topups`) before confirming; the authoritative check runs again inside `POST /orders`.
- **Guest carts** (`BR-CRT-03`): kept client-side (localStorage), never sent to the server before login; merge happens exactly once via `API-CRT-006`.
- **Estimated breakdown**: VAT is indicative — `VAT = 15% × (subtotal − discount)`, shipping untaxed (`BR-FIN-01`); authoritative totals are computed at checkout (`POST /checkout/session`).
- **Scoping**: one cart per `sub`; another customer's cart id returns 404 (`DATA-REQ-008`).

## 3. Pagination / Idempotency / Caching

The cart is a single bounded resource (≤50 lines) — no pagination. `POST /cart/merge` requires an idempotency key (`BR-PLT-03`). All cart responses `Cache-Control: no-store` (money-adjacent, must be live, `NFR-008`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
