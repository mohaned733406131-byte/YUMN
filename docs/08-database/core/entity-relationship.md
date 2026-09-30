---
document_id: DOC-DB-003
title: Entity-Relationship Register
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-008, FR-011, FR-012, NFR-017]
related_documents: [DOC-DB-001, DOC-DB-002, DOC-DB-005, DOC-BA-005, DOC-SA-010, DOC-OVR-008]
---

# Entity-Relationship Register

**This document is the register of the data model.** The 18 registered entities (`DB-001…DB-018`) are expanded one-per-file in [`entities/`](../entities-index.md); supporting tables are specified here. FK names follow `fk_<table>_<column>` (DOC-DB-001 §1). Cardinality notation: `1` (exactly one), `0..1` (optional one), `N` (many).

---

## 1. Bounded Areas — Text ERDs

### 1.1 Identity (`b01`)

```text
user (DB-001) 1 ──── N user_role        (role ∈ CUSTOMER|VENDOR|COURIER|ADMIN|SUPER_ADMIN|MODERATOR)
user            1 ──── N session        (device sessions, ≤5 active — BR-AUTH-06)
user            1 ──── N otp_challenge  (6-digit code stored as hash only — BR-AUTH-03)
user            1 ──── N address (DB-002)          (≤10 — FR-003)
user            1 ──── 1 wallet (DB-010)           (b07, created lazily on first use)
user            1 ──── 1 store (DB-003)            (b03, 0..1 before vendor onboarding — BR-VND-02)
governorate     1 ──── N address                    (reference data, seeded)
```

### 1.2 Catalog (`b02`, `b03`)

```text
store (DB-003) N ──── 1 user (owner_user_id)
store          1 ──── N store_member               (staff Viewer/Editor/Manager — BR-VND-06)
store          1 ──── N kyc_document               (object keys in MinIO)
store          1 ──── N store_follower             (follower = user — BR-VND-05)
store          1 ──── N product (DB-005)
category (DB-004) 0..1 ── N category (parent_id)   (self-tree, depth ≤5 — BR-CAT-03)
category       1 ──── N product
product (DB-005) 1 ──── 1 inventory (DB-006)       (product_id = PK of inventory)
product        1 ──── N product_image              (≤10 — BR-CAT-08; MinIO keys)
product        1 ──── N product_variant            (≤5 dims, ≤50 combos — BR-CAT-02)
product        1 ──── N product_attribute_value ── 1 category_attribute
review (DB-015) N ──── 1 product;  N ──── 1 user (reviewer);  1 ──── 1 order_item (unique)
review          1 ──── 0..1 review_response        (one per review — BR-REV-04)
inventory      1 ──── N stock_reservation          (15-min TTL — C-13)
```

### 1.3 Cart & Orders (`b05`, `b06`)

```text
cart (DB-007) 1 ──── 1 user                (only authenticated carts exist — BR-CRT-03)
cart           1 ──── N cart_item ──────── 1 product      (≤50 products / ≤10 units / ≤5 vendors — C-15)
cart           0..1 ─ 1 checkout_session
checkout_session 1 ── 1 order (DB-008)                  (idempotent placement — BR-ORD-06)

order (DB-008, master) N ──── 1 user (buyer_user_id)
order                    1 ──── N sub_order  ──── 1 store       (one sub-order per vendor — C-10)
order                    1 ──── N order_item ──── 1 sub_order ── 1 product   (100M rows — NFR-017)
order                    1 ──── N order_status_history           (append-only — BR-ORD-03)
order                    0..1 ─ 1 payment (DB-009)               (captured before/at placement)
order                    0..1 ─ 1 coupon (DB-016)                (one coupon per order — BR-PRM-02)
order                    N ──── 1 address                        (+ immutable snapshot jsonb)
```

### 1.4 Payment, Wallet & Escrow (`b07`)

```text
payment (DB-009) N ──── 0..1 order (kind = ORDER) ;  N ──── 1 user (payer)
payment           1 ──── 0..1 refund
wallet (DB-010)   1 ──── 1 user (user_id UNIQUE)
wallet            1 ──── N wallet_transaction (DB-011)   ← append-only ledger, balance cache
wallet_transaction N ──── 0..1 order / payment / refund / payout   (reference polymorph + CHECK)
escrow (DB-012)   1 ──── 1 sub_order (UNIQUE)  ;  N ──── 1 order (denorm)  ;  N ──── 1 store
refund            N ──── 1 payment ;  0..1 ──── 1 return_request
payout            N ──── 1 store ;  N ──── N escrow (via payout_escrow allocation)
```

### 1.5 Delivery & Returns (`b08`, `b09`, `b13`)

```text
shipment (DB-013) 1 ──── 1 sub_order (kind = OUTBOUND, UNIQUE)
shipment           0..1 ─ 1 user (courier_id, role COURIER)
shipment           1 ──── N shipment_attempt   (failed attempts — BR-SHP-03/06)
shipment           1 ──── N shipment_offer     (first-accept race — BR-SHP-04)
shipping_zone      1 ──── N shipping_rate      (fee = f(zone, weight, method) — BR-SHP-01)

return_request (DB-014) N ──── 1 order ; N ──── 1 sub_order ; N ──── 1 store
return_request        1 ──── N return_item ──── 1 order_item   (refund = item value — BR-RET-03)
return_request        1 ──── N return_evidence  (MinIO keys)
return_request        0..1 ─ 1 refund  (b07 — wallet credit ≤3 business days, BR-RET-04)

dispute (b13)        N ──── 1 order ;  0..1 ── 1 sub_order     (escrow FROZEN while open — BR-ORD-05)
support_ticket (b13) N ──── 0..1 order / shipment              (auto-created on 3rd code failure — BR-SHP-03)
```

### 1.6 Content & Promotions (`b12`)

```text
coupon (DB-016) 0..1 ── 1 store        (NULL = platform coupon — BR-PRM-03)
coupon           1 ──── N coupon_redemption ──── 1 order   (usage & per-user limits — BR-PRM-04)
banner / cms_page  N ── 1 user (created_by)                (authored in B12, consumed by B04/B12)
```

### 1.7 Notifications & Audit (`b10`, `b13`)

```text
notification (DB-017) N ──── 1 user
notification_preference N ── 1 user   UNIQUE(user_id, channel, category)   (BR-NTF-05)
audit_log (DB-018)    0..1 ─ 1 user (actor_user_id; NULL for actor_type = SYSTEM)
audit_log              1 ──── 1 audit_chain (single head row: seq + prev_hash)
```

---

## 2. Relationship Table (FK register)

| From (table) | From (entity) | To (table) | Cardinality | FK name | ON DELETE | Notes |
|---|---|---|---|---|---|---|
| `b01.user_role` | — | `b01.user` | N:1 | `fk_user_role_user_id` | CASCADE | role grant rows removed with account |
| `b01.session` | — | `b01.user` | N:1 | `fk_session_user_id` | CASCADE | ≤5 active enforced app-side (BR-AUTH-06) |
| `b01.otp_challenge` | — | `b01.user` | N:1 | `fk_otp_challenge_user_id` | CASCADE | code stored as hash |
| `b01.address` | DB-002 | `b01.user` | N:1 | `fk_address_user_id` | CASCADE | ≤10 app-side (FR-003) |
| `b01.address` | DB-002 | `b01.governorate` | N:1 | `fk_address_governorate_code` | RESTRICT | seeded reference data |
| `b03.store` | DB-003 | `b01.user` | 1:1 | `fk_store_owner_user_id` | RESTRICT | UNIQUE → BR-VND-02 |
| `b03.store_member` | — | `b03.store` | N:1 | `fk_store_member_store_id` | CASCADE | staff roles (BR-VND-06) |
| `b03.store_member` | — | `b01.user` | N:1 | `fk_store_member_user_id` | CASCADE | UNIQUE(store_id, user_id) |
| `b03.kyc_document` | — | `b03.store` | N:1 | `fk_kyc_document_store_id` | CASCADE | object key + checksum |
| `b03.store_follower` | — | `b03.store` / `b01.user` | N:1 / N:1 | `fk_store_follower_store_id`, `fk_store_follower_user_id` | CASCADE | UNIQUE(store_id, user_id) |
| `b04` (no tables) | — | — | — | — | — | reads `b02` + Elasticsearch only |
| `b05.cart` | DB-007 | `b01.user` | 1:1 active | `fk_cart_user_id` | CASCADE | partial UNIQUE(user_id) WHERE status='ACTIVE' |
| `b05.cart_item` | — | `b05.cart` / `b02.product` | N:1 / N:1 | `fk_cart_item_cart_id`, `fk_cart_item_product_id` | CASCADE / RESTRICT | product removal blocks via RESTRICT |
| `b05.checkout_session` | — | `b05.cart`, `b01.user` | N:1 / N:1 | `fk_checkout_session_cart_id`, `fk_checkout_session_user_id` | CASCADE | one session → one order |
| `b06.order` | DB-008 | `b01.user` | N:1 | `fk_order_buyer_user_id` | RESTRICT | buyer owner key |
| `b06.order` | DB-008 | `b07.payment` | N:1 | `fk_order_payment_id` | RESTRICT | wallet capture (C-01) |
| `b06.order` | DB-008 | `b01.address` | N:0..1 | `fk_order_address_id` | SET NULL | snapshot jsonb keeps history after address edits/deletion |
| `b06.order` | DB-008 | `b12.coupon` | N:0..1 | `fk_order_coupon_id` | SET NULL | code snapshot kept on order |
| `b06.sub_order` | supporting | `b06.order` | N:1 | `fk_sub_order_order_id` | RESTRICT | one row per vendor (C-10) |
| `b06.sub_order` | supporting | `b03.store` | N:1 | `fk_sub_order_store_id` | RESTRICT | vendor owner key |
| `b06.order_item` | supporting | `b06.order` / `b06.sub_order` | N:1 / N:1 | `fk_order_item_order_id`, `fk_order_item_sub_order_id` | RESTRICT | partitioned by created_at |
| `b06.order_item` | supporting | `b02.product` | N:0..1 | `fk_order_item_product_id` | SET NULL | product may be deleted post-order; snapshot kept |
| `b06.order_status_history` | supporting | `b06.order` / `b06.sub_order` | N:1 / N:0..1 | `fk_order_status_history_order_id`, `fk_order_status_history_sub_order_id` | RESTRICT | append-only, partitioned |
| `b07.payment` | DB-009 | `b01.user` | N:1 | `fk_payment_payer_user_id` | RESTRICT | wallet owner |
| `b07.payment` | DB-009 | `b06.order` | N:0..1 | `fk_payment_order_id` | RESTRICT | NULL for top-ups |
| `b07.wallet` | DB-010 | `b01.user` | 1:1 | `fk_wallet_user_id` | RESTRICT | UNIQUE(user_id) |
| `b07.wallet_transaction` | DB-011 | `b07.wallet` | N:0..1 | `fk_wallet_transaction_wallet_id` | RESTRICT | NULL for non-wallet accounts |
| `b07.escrow` | DB-012 | `b06.sub_order` | 1:1 | `fk_escrow_sub_order_id` | RESTRICT | UNIQUE(sub_order_id) |
| `b07.escrow` | DB-012 | `b06.order` / `b03.store` | N:1 / N:1 | `fk_escrow_order_id`, `fk_escrow_store_id` | RESTRICT | denorm for dispute/settlement queries |
| `b07.refund` | supporting | `b07.payment` | N:1 | `fk_refund_payment_id` | RESTRICT | wallet credit via ledger |
| `b07.payout` | supporting | `b03.store` | N:1 | `fk_payout_store_id` | RESTRICT | min 1,000 YER; 3–7 business days |
| `b08.shipment` | DB-013 | `b06.sub_order` | 1 (outbound) | `fk_shipment_sub_order_id` | RESTRICT | UNIQUE(sub_order_id, kind) WHERE kind='OUTBOUND' |
| `b08.shipment` | DB-013 | `b01.user` | N:0..1 | `fk_shipment_courier_id` | SET NULL | courier role; history kept in attempts |
| `b08.shipment_attempt` | — | `b08.shipment` | N:1 | `fk_shipment_attempt_shipment_id` | CASCADE | attempt_no unique per shipment |
| `b08.shipment_offer` | — | `b08.shipment` / `b01.user` | N:1 / N:1 | `fk_shipment_offer_shipment_id`, `fk_shipment_offer_courier_id` | CASCADE | UNIQUE(shipment_id, courier_id) |
| `b08.shipping_rate` | — | `b08.shipping_zone` | N:1 | `fk_shipping_rate_zone_id` | RESTRICT | fee function input (BR-SHP-01) |
| `b09.return_request` | DB-014 | `b06.order` / `b06.sub_order` | N:1 / N:1 | `fk_return_request_order_id`, `fk_return_request_sub_order_id` | RESTRICT | buyer + store scoping |
| `b09.return_item` | — | `b09.return_request` / `b06.order_item` | N:1 / N:1 | `fk_return_item_return_request_id`, `fk_return_item_order_item_id` | CASCADE / RESTRICT | refund = item value (BR-RET-03) |
| `b09.return_evidence` | — | `b09.return_request` | N:1 | `fk_return_evidence_return_request_id` | CASCADE | image object keys |
| `b09.return_request` | DB-014 | `b07.refund` | N:0..1 | `fk_return_request_refund_id` | SET NULL | refund link |
| `b10.notification` | DB-017 | `b01.user` | N:1 | `fk_notification_user_id` | CASCADE | target user |
| `b10.notification_preference` | — | `b01.user` | N:1 | `fk_notification_preference_user_id` | CASCADE | UNIQUE(user_id, channel, category) |
| `b12.coupon` | DB-016 | `b03.store` | N:0..1 | `fk_coupon_store_id` | SET NULL | NULL = platform coupon (BR-PRM-03) |
| `b12.coupon_redemption` | — | `b12.coupon` / `b06.order` | N:1 / 1:1 | `fk_coupon_redemption_coupon_id`, `fk_coupon_redemption_order_id` | RESTRICT | UNIQUE(coupon_id, order_id) |
| `b13.dispute` | — | `b06.order` / `b06.sub_order` | N:1 / N:0..1 | `fk_dispute_order_id`, `fk_dispute_sub_order_id` | RESTRICT | freezes escrow (BR-ORD-05) |
| `b13.support_ticket` | — | `b06.order` / `b08.shipment` | N:0..1 / N:0..1 | `fk_support_ticket_order_id`, `fk_support_ticket_shipment_id` | SET NULL | created by system rules (BR-SHP-03) |
| `b13.audit_log` | DB-018 | `b01.user` | N:0..1 | `fk_audit_log_actor_user_id` | RESTRICT | NULL when actor_type = SYSTEM |
| `b02.review` | DB-015 | `b02.product` / `b01.user` / `b06.order` / `b06.order_item` | N:1 / N:1 / N:1 / 1:1 | `fk_review_product_id`, `fk_review_user_id`, `fk_review_order_id`, `fk_review_order_item_id` | RESTRICT / CASCADE / RESTRICT / RESTRICT | order_item unique → BR-REV-02 |

> Delete policy summary: **financial, order, and audit rows are `RESTRICT`** (rows are retained; deletion is anonymization per DATA-REQ-003, never row drop); pure child collections (sessions, carts, items, preferences) are `CASCADE`.

---

## 3. Master / Sub-Order Model (C-10)

| Aspect | Master `b06.order` | Sub-order `b06.sub_order` |
|---|---|---|
| Cardinality | 1 per checkout (BR-ORD-02) | exactly 1 per vendor per master — `UNIQUE(order_id, store_id)` |
| State | same 17-value `order_state` enum, maintained as the **aggregate** state | same enum, executed **per vendor** (DOC-SA-010 §4) |
| Completion rule | `COMPLETED` only when every sub-order is `COMPLETED` or `REFUNDED` (BR-ORD-07) — verified by deferred aggregate constraint (DOC-DB-005 §5) | sub-order never advances past its own vendor's steps |
| Money | `subtotal/discount/vat/shipping/total_yer`; `total_yer = Σ sub_order.total_yer` (deferred check) | row-level formula `total = subtotal − discount + vat + shipping`, half-up VAT per BR-FIN-05 |
| Payment | payment intent + wallet capture at master level (C-10) | — |
| Escrow | escrow **funded** from the master capture, then **allocated** into one escrow row per sub-order (`b07.escrow.sub_order_id` UNIQUE) | hold, 7-day release (BR-ESC-01), commission (BR-ESC-03), payout eligibility |
| Dispute | dispute row links to master and optionally to one sub-order; only the affected sub-order's escrow freezes (BR-ORD-05, DOC-SA-010 §4) | — |
| Fulfillment | — | shipment (DB-013), courier, delivery code |
| Timeline | customer-facing timeline = union of master events + own sub-order events (BR-ORD-09) | vendor sees own sub-order events only |

---

## 4. Ownership Boundaries (DATA-REQ-008)

| Table (owner key) | Owner | Scoped reads | Never allowed |
|---|---|---|---|
| `user`, `address`, `session`, `wallet`, `cart`, `notification` | `user_id` | customer sees own rows; admin per RBAC scope | any cross-customer read/write (IDOR tests) |
| `store`, `product`, `inventory`, `review.response`, `coupon (store)`, `payout` | `store_id` | vendor queries always filter `store_id` (BR-VND-07) | vendor X touching vendor Y rows — denied at service layer + CI cross-tenant suite |
| `order` | `buyer_user_id` | buyer: own; vendor: via `sub_order.store_id`; courier: via assigned `shipment`; admin/moderator: scoped (BR-ORD-09) | System/jobs as an unescape-hatch for unscoped reads (DATA-REQ-008 R3) |
| `shipment` | `courier_id` (assignment) | courier sees own assignments; admin dispatch view | courier reading other couriers' deliveries |
| `wallet_transaction`, `audit_log` | platform (append-only) | wallet owner reads own ledger; audit read per role scope; **nobody writes** (DATA-REQ-007, SEC-REQ-010) | UPDATE/DELETE by any app role |
| Reference data (`governorate`, `shipping_zone`, `platform_setting`) | platform | read for all modules; write by admin module only | module-local copies of reference data |

Enforcement stack (in order): schema/column privileges (DOC-DB-005 §6) → repository-layer owner predicate → ownership assertions in service code → **cross-tenant test suite covering every tenant-scoped entity, gated in CI** (DATA-REQ-008 AC-DR008-02/04). Background jobs are parameterized by owner (DATA-REQ-008 R4).

---

## 5. Reading Order

Entity files: [`../entities-index.md`](../entities-index.md) (DOC-DB-007). Constraints on every relationship above: DOC-DB-005. Index access paths per relationship: DOC-DB-004.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
