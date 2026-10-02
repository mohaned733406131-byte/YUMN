---
document_id: DOC-DBE-008
entity_id: DB-008
title: Entity order (DB-008)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-011, FR-012, DATA-REQ-001, DATA-REQ-007, DATA-REQ-008, NFR-008, NFR-017]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005, DOC-SA-010, DOC-OVR-008]
---

# Entity: `order` (DB-008) — table `b06.order` (+ `sub_order`, `order_item`, `order_status_history`)

## Overview & purpose

The master order — one per checkout (**BR-ORD-02, `C-10`**) — carrying the buyer, the 17-state machine (`C-09`, `DOC-SA-010`), all money columns, wallet-only payment (`C-01`), and the idempotency key (BR-ORD-06). Per-vendor **sub-orders** execute fulfillment, commission and payout; **order_item** lines are the 100M-row volume table (NFR-017); **order_status_history** is the append-only timeline (BR-ORD-03, BR-ORD-09). This entity is the anchor for escrow (DB-012), shipment (DB-013), returns (DB-014) and disputes (`b13.dispute`).

## Field table

### `b06.order` (master)

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `order_no` | char(16) | no | app-generated | `uq_order_order_no` | human reference, e.g. `YM-260926-8F3K2Q` — not the PK |
| `buyer_user_id` | uuid | no | — | FK `fk_order_buyer_user_id` → `b01.user` ON DELETE RESTRICT | owner key (DATA-REQ-008) |
| `state` | `order_state` | no | `'PLACED'` | enum = **exactly 17 values** (C-09) | aggregate state; per-vendor machine on `sub_order` (DOC-SA-010 §4) |
| `subtotal_yer` | bigint | no | — | `>= 0` | Σ of line items before discount |
| `discount_yer` | bigint | no | `0` | `>= 0` | coupon discount (one coupon — BR-PRM-02) |
| `vat_yer` | bigint | no | — | `>= 0` | Σ of sub-order VAT (BR-FIN-01, half-up per BR-FIN-05) |
| `shipping_yer` | bigint | no | — | `>= 0` | Σ of sub-order shipping; untaxed (BR-FIN-01) |
| `total_yer` | bigint | no | — | `ck_order_total_range` `BETWEEN 500 AND 5000000` (C-14); `ck_order_money_consistent` `total = subtotal − discount + vat + shipping` (BR-FIN-02); equals `Σ sub_order.total_yer` via deferred trigger `ct_order_totals_match_suborders` | wallet debit amount |
| `currency` | char(3) | no | `'YER'` | `ck_currency_yer` | C-04 |
| `payment_method` | `payment_method` | no | `'WALLET'` | `NOT (payment_method = 'WALLET') → CHECK failed` (C-01, BR-PAY-01) | COD/cards/BNPL impossible |
| `payment_id` | uuid | no | — | FK `fk_order_payment_id` → `b07.payment` ON DELETE RESTRICT | captured intent in the same transaction (BR-PLT-04) |
| `checkout_session_id` | uuid | yes | null | FK → `b05.checkout_session` ON DELETE SET NULL | traceability of the 7-step flow (FR-011) |
| `idempotency_key` | varchar(128) | no | — | `uq_order_idempotency_key` | duplicate submit returns original (BR-ORD-06, BR-PLT-03) |
| `address_id` | uuid | yes | null | FK `fk_order_address_id` → `b01.address` ON DELETE SET NULL | live link |
| `shipping_address_snapshot` | jsonb | no | — | app-validated structure | **immutable** copy (governorate, district, street ciphertext ref, recipient) — survives address edits/deletion (DATA-REQ-001/003) |
| `coupon_id` | uuid | yes | null | FK `fk_order_coupon_id` → `b12.coupon` ON DELETE SET NULL | + `coupon_code` snapshot varchar |
| `version` | integer | no | `0` | `>= 0` | optimistic locking → stale transition returns **409 `STATE_CONFLICT`** (DOC-SA-010 §5) |
| `placed_at` | timestamptz | no | `now()` | — | wallet debited + escrow funded at this moment (DOC-SA-010 §1) |
| `completed_at` / `cancelled_at` | timestamptz | yes | null | — | terminal markers |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | `created_at` = `placed_at` |

### `b06.sub_order` (supporting — one per vendor, C-10)

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | — |
| `order_id` | uuid | no | — | FK `fk_sub_order_order_id` → `b06.order` ON DELETE RESTRICT | — |
| `store_id` | uuid | no | — | FK `fk_sub_order_store_id` → `b03.store` ON DELETE RESTRICT; `UNIQUE(order_id, store_id)` | **exactly one sub-order per vendor** (BR-ORD-02) |
| `state` | `order_state` | no | `'PLACED'` | same 17-value enum | the lifecycle executes here (DOC-SA-010 §4) |
| `subtotal_yer`, `discount_yer`, `vat_yer`, `shipping_yer`, `total_yer` | bigint | no | — | row-local identity + `ck_sub_order_vat_formula`: `vat = ((subtotal − discount) * 15 + 50) / 100` | BR-FIN-01/02/05 (half-up at sub-order level) |
| `version` | integer | no | `0` | `>= 0` | optimistic lock (BR-ORD-07, first-accept races) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 | — |

### `b06.order_item` (supporting — partitioned by `created_at`, NFR-017)

`(id uuid, order_id FK, sub_order_id FK, store_id FK, product_id FK ON DELETE SET NULL, variant_id NULL, product_name_ar snapshot, product_name_en snapshot NULL, unit_price_yer bigint > 0, qty smallint >= 1, discount_yer bigint >= 0, line_subtotal_yer bigint = unit*qty − discount, image_key varchar NULL, created_at timestamptz)` — PK `(id, created_at)`; snapshots keep history valid after product deletion.

### `b06.order_status_history` (supporting — append-only, partitioned)

`(id uuid, order_id FK NOT NULL, sub_order_id FK NULL, from_state order_state NULL, to_state order_state NOT NULL, actor_type enum {CUSTOMER, VENDOR, COURIER, ADMIN, SUPER_ADMIN, MODERATOR, SYSTEM}, actor_user_id FK NULL, reason text NULL, metadata jsonb, created_at)` — written app-side on every transition and backstopped by trigger T3 (DOC-DB-005 §6). `UPDATE`/`DELETE` revoked (BR-ORD-03, DATA-REQ-007).

**Dispute support** lives in `b13.dispute(id, order_id, sub_order_id NULL, raised_by_user_id, state ∈ {OPEN, UNDER_REVIEW, RESOLVED}, resolution ∈ {VENDOR_FAVOURED, BUYER_FAVOURED} NULL, resolved_by NULL, resolved_at NULL, notes, created_at)` — FR-020; while a dispute is open the affected `escrow` row is `FROZEN` (BR-ORD-05).

## Indexes

| Table | Index |
|---|---|
| `order` | PK `id`; `uq_order_order_no`; `uq_order_idempotency_key` |
| `order` | `idx_order_buyer_state_created` `(buyer_user_id, state, created_at DESC)` — **hot path** customer list |
| `order` | `idx_order_buyer_created_at` `(buyer_user_id, created_at DESC)`; `idx_order_state_created_at` `(state, created_at DESC)` (ops queues, BR-ORD-10); `idx_order_created_at` |
| `sub_order` | `uq_sub_order_order_id_store_id`; `idx_sub_order_store_state_created` `(store_id, state, created_at DESC)` — **hot path** vendor panel; `idx_sub_order_order_id`; `idx_sub_order_store_id_settlement` partial |
| `order_item` | PK `(id, created_at)`; `idx_order_item_order_id`; `idx_order_item_sub_order_id`; `idx_order_item_product_created` — all composite with `created_at` (partitioned) |
| `order_status_history` | PK `(id, created_at)`; `idx_osh_order_created` `(order_id, created_at)` — **timeline**; `idx_osh_sub_order_created` partial |

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `order` | `user` (buyer) | N:1 | `fk_order_buyer_user_id` | RESTRICT |
| `order` | `payment` (DB-009) | N:1 | `fk_order_payment_id` | RESTRICT |
| `order` | `address` (DB-002) | N:0..1 | `fk_order_address_id` | SET NULL (+ snapshot) |
| `order` | `coupon` (DB-016) | N:0..1 | `fk_order_coupon_id` | SET NULL (+ code snapshot) |
| `sub_order` | `order` / `store` (DB-003) | N:1 / N:1 | `fk_sub_order_order_id`, `fk_sub_order_store_id` | RESTRICT |
| `order_item` | `order` / `sub_order` / `product` (DB-005) | N:1 / N:1 / N:0..1 | `fk_order_item_order_id`, `fk_order_item_sub_order_id`, `fk_order_item_product_id` | RESTRICT / RESTRICT / SET NULL |
| `order_status_history` | `order` / `sub_order` | N:1 / N:0..1 | `fk_order_status_history_order_id`, `fk_order_status_history_sub_order_id` | RESTRICT |
| `escrow` (DB-012), `shipment` (DB-013), `return_request` (DB-014), `dispute` (b13) | `order`/`sub_order` | see DOC-DB-003 §2 | — | RESTRICT |

## Invariants & business rules enforced

**DB-enforced**

1. `state` can only hold one of the **17 canonical values** (C-09, BR-ORD-01) — enum type on both `order.state` and `sub_order.state`.
2. Money: non-negative components, `total = subtotal − discount + vat + shipping`, `total BETWEEN 500 AND 5000000` (C-14, BR-FIN-02), YER only; sub-order VAT formula half-up 15 % (BR-FIN-01, BR-FIN-05).
3. `payment_method = 'WALLET'` — any other method is rejected by CHECK (C-01, BR-PAY-01).
4. Unique `order_no` and `idempotency_key`; one sub-order per `(order_id, store_id)` (C-10).
5. Deferred triggers: `total = Σ sub_order.total`, `vat = Σ sub_order.vat`; `COMPLETED` implies all sub-orders ∈ {COMPLETED, REFUNDED} (BR-ORD-07) — verified at COMMIT (DOC-DB-005 §5).
6. History is append-only (privileges), and a state change without a history row is prevented by trigger T3 (BR-ORD-03).

**App-enforced (409 on violation)**

1. Transition legality per `DOC-SA-010` §2 matrix; skipping states, returning from DELIVERED to pre-delivery, or reaching DELIVERED without verified code is rejected → **409 `STATE_CONFLICT`** (BR-ORD-08, C-16). Optimistic `version` catches concurrent writers (DOC-SA-010 §5).
2. Actor permissions per surface: customer cancel only while PLACED/CONFIRMED; vendor/admin until READY_FOR_PICKUP; courier only delivery states; master COMPLETED only when all sub-orders settle (BR-ORD-04, BR-ORD-07, BR-ORD-09).
3. Timeline visibility: buyer (own), vendor (own sub-orders), courier (own delivery), admin/moderator scoped (BR-ORD-09).
4. Cancellation always triggers the wallet refund flow (BR-ORD-04); DISPUTED freezes escrow of affected sub-orders (BR-ORD-05).
5. Orders stuck at CONFIRMED for 24 h escalate to admin review with notification — never silent auto-cancel (BR-ORD-10).

**Canon note:** escrow is *funded* from the master payment (C-10: "payment & escrow at master level") but *held/released* as one row per sub-order (BR-ESC-01 "funds for the sub-order are held", BR-ORD-05 per-sub-order freeze). The model implements both: master capture → allocation into `b07.escrow` rows keyed by `sub_order_id` (DOC-DB-003 §3).

## Example rows

```text
order: id=0198fc01-…  order_no=YM260926-8F3K2Q  buyer_user_id=0198f2c4-…  state=IN_TRANSIT  subtotal_yer=194500  discount_yer=9500  vat_yer=27750  shipping_yer=3000  total_yer=215750  currency=YER  payment_method=WALLET  payment_id=0198fc50-…  idempotency_key=ck_9c1e…  version=7  placed_at=2026-09-26T14:22:03Z
sub_order: id=0198fc10-…  order_id=0198fc01-…  store_id=0198f701-…  state=IN_TRANSIT  subtotal_yer=194500  discount_yer=9500  vat_yer=27750  shipping_yer=3000  total_yer=215750  version=5
order_item: id=0198fc20-…(2026-09-26)  order_id=0198fc01-…  sub_order_id=0198fc10-…  product_id=0198fa11-…  product_name_ar=هاتف نوكيا 105  unit_price_yer=95000  qty=2  discount_yer=9500  line_subtotal_yer=180500
order_status_history: id=0198fc30-…(2026-09-26)  order_id=0198fc01-…  sub_order_id=0198fc10-…  from_state=PICKED_UP  to_state=IN_TRANSIT  actor_type=COURIER  actor_user_id=0198f3b1-…  created_at=2026-09-26T15:40:12Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
