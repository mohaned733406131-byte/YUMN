---
document_id: DOC-DBE-016
entity_id: DB-016
title: Entity coupon (DB-016)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-019, DATA-REQ-001]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005]
---

# Entity: `coupon` (DB-016) — table `b12.coupon`

## Overview & purpose

Coupon engine backing FR-019 and the PRM rules: unique code, **validity window ≤ 90 days**, percentage discount **≤ 90 %** of order value, optional `min_order_amount`, global and per-user usage limits, **one coupon per order — never stacked** (BR-PRM-01…06). Scope is platform (admin-created) or store (vendor-created; admin can list/disable) (BR-PRM-03). Invalid coupons fail validation **before any order row exists** (BR-PRM-06).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `code` | varchar(40) | no | app-generated | `uq_coupon_code`, uppercase-normalized app-side | unique human-entered code (BR-PRM-01) |
| `store_id` | uuid | yes | null | FK `fk_coupon_store_id` → `b03.store` ON DELETE SET NULL | `NULL` = platform coupon; set = store coupon (BR-PRM-03) |
| `created_by` | uuid | no | — | FK → `b01.user` ON DELETE RESTRICT | admin or vendor owner — audit (BR-PLT-06) |
| `type` | `coupon_type` | no | — | enum `PERCENT, FIXED, FREE_SHIPPING, BUY_X_GET_Y` | BR-PRM-05 |
| `value_percent` | smallint | yes | null | `BETWEEN 1 AND 90` when `type='PERCENT'` (CHECK) | ≤ 90 % (BR-PRM-01) |
| `value_yer` | bigint | yes | null | `> 0` when `type='FIXED'` (CHECK) | fixed YER discount |
| `max_discount_yer` | bigint | yes | null | `> 0` when present | cap for percent coupons |
| `min_order_amount_yer` | bigint | yes | null | `> 0` when present | optional threshold (BR-PRM-04) |
| `buy_qty` / `get_qty` | smallint | yes | null | `> 0` when `type='BUY_X_GET_Y'` (app) | X/Y config (BR-PRM-05) |
| `free_shipping_scope` | varchar(40) | yes | null | `type='FREE_SHIPPING' → free_shipping_scope IS NOT NULL` (app) | e.g. within-zone only (BR-SHP-01) |
| `starts_at` | timestamptz | no | `now()` | — | — |
| `ends_at` | timestamptz | no | — | `ck_coupon_window`: `ends_at > starts_at AND ends_at - starts_at <= interval '90 days'` | ≤ 90-day validity (BR-PRM-01) |
| `usage_limit` | integer | yes | null | `> 0` when present | global cap (BR-PRM-04) |
| `per_user_limit` | integer | yes | null | `> 0` when present | per-customer cap (BR-PRM-04) |
| `used_count` | integer | no | `0` | `>= 0` | denormalized global counter; `coupon_redemption` rows are authoritative (reconciled by job) |
| `is_active` | boolean | no | `true` | — | admin can disable a store coupon (BR-PRM-03) |
| `scope_note` | varchar(255) | yes | null | — | display text (C-24 localized at read) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

**Supporting:** `b12.coupon_redemption(id, coupon_id, order_id, user_id, discount_yer, redeemed_at)` — `UNIQUE(coupon_id, order_id)` (BR-PRM-02/04); `discount_yer` frozen per order is the input to commission calculation at escrow release (BR-ESC-03).

## Indexes

- PK `id`; `uq_coupon_code`
- `idx_coupon_active_window` on `(starts_at, ends_at)` WHERE `is_active` — active-coupon pickers
- `idx_coupon_store_id` on `(store_id)` WHERE `store_id IS NOT NULL` — vendor's coupons (BR-PRM-03)
- `coupon_redemption`: `uq_coupon_redemption_coupon_id_order_id`; `idx_coupon_redemption_coupon_id_user_id`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `coupon` | `store` (DB-003) | N:0..1 | `fk_coupon_store_id` | SET NULL |
| `coupon` | `user` (creator) | N:1 | `fk_coupon_created_by` | RESTRICT |
| `coupon_redemption` | `coupon` / `order` (DB-008) | N:1 / 1:1 | `fk_coupon_redemption_coupon_id`, `fk_coupon_redemption_order_id` | RESTRICT |
| `order` (DB-008) / `cart` (DB-007) | `coupon` | N:0..1 | `fk_order_coupon_id`, `fk_cart_coupon_id` | SET NULL |

## Invariants & business rules enforced

**DB-enforced**

1. Unique code (BR-PRM-01); validity window `> 0` and `<= 90 days` (`ck_coupon_window`).
2. Type-conditional value CHECKs: `PERCENT → 1..90`, `FIXED → > 0`, X/Y and free-shipping fields present for their types — a mis-shaped coupon cannot be stored (BR-PRM-01/05).
3. Positive limits, `used_count >= 0`; redemption unique per `(coupon_id, order_id)` → **one application per order** (BR-PRM-02).

**App-enforced**

1. **Non-stacking:** an order carries a single `coupon_id` column — structurally only one coupon can apply (BR-PRM-02); cart pre-apply is advisory and re-validated at checkout.
2. Validation before order creation: active, within window, not fully used (`used_count < usage_limit`), user's redemptions `< per_user_limit`, `subtotal >= min_order_amount_yer` — failure returns a validation error and **no order row is created** (BR-PRM-04/06).
3. Discount computation: percent capped by `max_discount_yer` and by 90 % of order value (BR-PRM-01); free-shipping coupons zero the shipping component (BR-SHP-01); all discount flows into `discount_yer` → VAT base `(subtotal − discount)` (BR-FIN-01).
4. Redemption rows inserted in the order-placement transaction (idempotency key, BR-PLT-03) and `used_count` incremented; daily job reconciles counter vs redemptions (DATA-REQ-006).
5. Scope checks: store coupon usable only for that store's sub-orders; platform coupons everywhere (BR-PRM-03).

## Example rows

```text
id=0198fe80-…  code=WELCOME10   store_id=NULL              created_by=admin…      type=PERCENT  value_percent=10  value_yer=NULL  max_discount_yer=20000  min_order_amount_yer=5000  starts_at=2026-09-01T00:00Z  ends_at=2026-11-29T23:59Z  usage_limit=10000  per_user_limit=1  used_count=412  is_active=true
id=0198fe91-…  code=HARMAIN5000 store_id=0198f701-…       created_by=0198f701-owner…  type=FIXED  value_percent=NULL  value_yer=5000  min_order_amount_yer=50000  starts_at=2026-09-20T00:00Z  ends_at=2026-10-19T23:59Z  usage_limit=500  per_user_limit=2  used_count=37  is_active=true
id=0198fea2-…  code=FREESHIP     store_id=NULL              created_by=admin…      type=FREE_SHIPPING  value_percent=NULL  value_yer=NULL  free_shipping_scope=ALL  starts_at=2026-09-25T00:00Z  ends_at=2026-12-24T23:59Z  usage_limit=NULL  per_user_limit=NULL  used_count=18  is_active=true
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
