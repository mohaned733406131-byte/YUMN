---
document_id: DOC-DBE-007
entity_id: DB-007
title: Entity cart (DB-007)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-010, FR-011, DATA-REQ-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005]
---

# Entity: `cart` (DB-007) — table `b05.cart`

## Overview & purpose

Server-side cart for **authenticated users** (B05), with item lines in `b05.cart_item`. Realizes FR-010: multi-vendor cart, guards **≤50 products, ≤10 units per product, ≤5 vendors (`C-15`, BR-CRT-01)**, 15-minute reservation countdown (C-13), server-side total reconciliation (BR-CRT-04).

**Guest carts decision:** guest carts are **not stored in the database** — canon BR-CRT-03 says guest carts live client-side and merge on login (server value wins on quantity conflict). Therefore `user_id` is `NOT NULL` and there is exactly one *active* DB cart per user; the merge is an app operation that creates/updates the user's active cart from local state after authentication.

## Field table

### `b05.cart`

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `user_id` | uuid | no | — | FK `fk_cart_user_id` → `b01.user` ON DELETE CASCADE; partial `UNIQUE(user_id)` WHERE `status='ACTIVE'` | owner key (DATA-REQ-008); one active cart (BR-CRT-03) |
| `status` | `cart_status` | no | `'ACTIVE'` | enum `ACTIVE, CHECKED_OUT, ABANDONED` | `CHECKED_OUT` set at order placement; `ABANDONED` by sweeper |
| `currency` | char(3) | no | `'YER'` | `ck_currency_yer` | C-04 |
| `coupon_id` | uuid | yes | null | FK → `b12.coupon` ON DELETE SET NULL | pre-applied coupon (one only — BR-PRM-02; final validation at checkout) |
| `reservation_expires_at` | timestamptz | yes | null | — | earliest cart-line reservation expiry → drives the countdown UI (C-13, BR-CRT-02) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |
| `abandoned_at` | timestamptz | yes | null | — | set by sweeper when `status='ABANDONED'` |

### `b05.cart_item` (supporting — specified here because the entity's items live in it)

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | — |
| `cart_id` | uuid | no | — | FK `fk_cart_item_cart_id` → `b05.cart` ON DELETE CASCADE | — |
| `product_id` | uuid | no | — | FK `fk_cart_item_product_id` → `b02.product` ON DELETE RESTRICT | product must exist while in cart |
| `variant_id` | uuid | yes | null | FK → `b02.product_variant` ON DELETE RESTRICT | optional variant |
| `qty` | smallint | no | `1` | `ck_cart_item_qty` `BETWEEN 1 AND 10` | ≤10 units per product (C-15) |
| `unit_price_snapshot_yer` | bigint | no | — | `> 0` | price at add-time; mismatch at checkout re-prompts (BR-CRT-04) |
| `reservation_id` | uuid | yes | null | FK → `b02.stock_reservation` ON DELETE SET NULL | live 15-min hold link (C-13) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |
| — | — | — | — | `UNIQUE(cart_id, product_id, variant_id) NULLS NOT DISTINCT` | one line per product/variant — idempotent add |

**Checkout session (supporting, `b05.checkout_session`):** `(id, cart_id, user_id, idempotency_key UNIQUE, step, shipping_address_id, status, expires_at, order_id, created_at)` — the 7-step checkout (FR-011) state; `order_id` links the session to the created order so duplicate submits return the original (BR-ORD-06).

## Indexes

- `uq_cart_user_id_active` partial UNIQUE on `(user_id)` WHERE `status='ACTIVE'`
- `idx_cart_updated_at` on `(updated_at)` WHERE `status='ACTIVE'` — abandonment sweeper
- `cart_item`: PK `id`; `uq_cart_item_cart_id_product_id_variant_id` (NULLS NOT DISTINCT); `idx_cart_item_cart_id` on `(cart_id)`
- `checkout_session`: `uq_checkout_session_idempotency_key`; `idx_checkout_session_user_id_status`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `cart` | `user` (DB-001) | 1 active per user | `fk_cart_user_id` | CASCADE |
| `cart` | `coupon` (DB-016) | N:0..1 | `fk_cart_coupon_id` | SET NULL |
| `cart_item` | `cart` / `product` (DB-005) | N:1 / N:1 | `fk_cart_item_cart_id`, `fk_cart_item_product_id` | CASCADE / RESTRICT |
| `stock_reservation` (b02) | `cart_item` | 0..1:1 | `fk_stock_reservation_cart_item_id` | CASCADE |
| `checkout_session` → `order` (DB-008) | 1:1 | `fk_checkout_session_order_id` | SET NULL |

## Invariants & business rules enforced

**DB-enforced**

1. One active cart per user (partial UNIQUE).
2. `qty BETWEEN 1 AND 10` per line (C-15); unique line per product/variant (NULLS NOT DISTINCT).
3. Money columns positive and YER-only.

**App-enforced (guards are multi-row, so they live in the service layer — C-15 validation tests cover them)**

1. ≤50 distinct products and ≤5 vendor stores per cart (C-15, BR-CRT-01) — counted across `cart_item JOIN product` at add-time *and* re-validated at checkout.
2. Adding/refreshing a line starts or refreshes the 15-minute reservation countdown; expiry releases reserved stock (BR-CRT-02, C-13).
3. Guest cart merge on login: client lines merged into the DB cart; **server quantity wins** on conflict (BR-CRT-03).
4. Totals recalculated server-side at checkout; price drift vs `unit_price_snapshot_yer` shown for re-confirmation (BR-CRT-04).
5. Inactive/out-of-stock/out-of-policy lines block checkout until removed (BR-CRT-05); wallet balance ≥ order total at confirmation (BR-CRT-06 → `b07`).
6. Abandonment: `ACTIVE` carts untouched for 24 h → `ABANDONED`, reservations released (ops rule; no canon conflict).
7. Checkout success: cart → `CHECKED_OUT`, its reservations converted to consumption on payment (FR-005/FR-011).

## Example rows

```text
cart:      id=0198fb01-…  user_id=0198f2c4-…  status=ACTIVE  currency=YER  coupon_id=NULL  reservation_expires_at=2026-09-26T14:35:00Z  updated_at=2026-09-26T14:20:00Z
cart_item: id=0198fb22-…  cart_id=0198fb01-…  product_id=0198fa11-…  variant_id=NULL  qty=2  unit_price_snapshot_yer=95000  reservation_id=0198fb40-…
cart_item: id=0198fb31-…  cart_id=0198fb01-…  product_id=0198fa77-…  variant_id=NULL  qty=1  unit_price_snapshot_yer=4500   reservation_id=NULL
cart:      id=0198fb55-…  user_id=0198f3b1-…  status=CHECKED_OUT  currency=YER  updated_at=2026-09-25T19:02:11Z  (converted by checkout_session 0198fb70-…)
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
