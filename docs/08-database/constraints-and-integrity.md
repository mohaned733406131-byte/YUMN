---
document_id: DOC-DB-005
title: Constraints and Integrity Enforcement
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-006, DATA-REQ-007, DATA-REQ-008, SEC-REQ-010, NFR-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-006, DOC-BA-005, DOC-OVR-008, DOC-SA-010]
---

# Constraints and Integrity Enforcement

**Policy: integrity that can be expressed in SQL belongs in the database (DATA-REQ-001); rules that need business context, cross-row aggregates, or external data stay app-layer with tests — plus the explicit DB backstops listed in §5–§6.** Every constraint below is named (`ck_/uq_/fk_`, DOC-DB-001 §1) and lands in a Prisma migration (DOC-DB-006).

---

## 1. Foreign Key Rules (ON DELETE semantics)

| Policy | Applies to | Value | Why |
|---|---|---|---|
| `RESTRICT` | all financial/history references: `order.*`, `sub_order.*`, `order_item.*`, `payment`, `wallet`, `wallet_transaction`, `escrow`, `refund`, `payout`, `shipment`, `return_*`, `review.order_id`, `audit_log` | no parent deletion ever | records are retained for ≥5 years (DATA-REQ-003, NFR-019); account deletion **anonymizes**, never drops rows |
| `CASCADE` | pure owned child collections: `user_role`, `session`, `otp_challenge`, `address`, `cart`, `cart_item`, `notification_preference`, `store_member`, `kyc_document`, `stock_reservation`, `shipment_attempt` | children removed with parent | no independent lifecycle, no financial value |
| `SET NULL` | optional lookbacks: `order.address_id`, `order.coupon_id`, `shipment.courier_id`, `order_item.product_id`, `return_request.refund_id` | keep the fact, drop the link | snapshots on the child row preserve history (e.g., `order.shipping_address_snapshot`) |
| No `ON DELETE` (default `NO ACTION`) | reference data (`governorate`, `shipping_zone`) | deletion blocked | seeded data (DOC-DB-006 §5) |

Additional rules:

- Every FK has a **named** constraint `fk_<table>_<column>` applied through Prisma `@relation(map:)` so schema and DB cannot drift (DOC-DB-002 §2).
- FK columns are indexed automatically by their index plan (DOC-DB-004); a new FK without an index on the child side is a review defect.
- Cross-schema FKs are allowed (single database, `C-19`); cross-schema **writes** are not (schema privileges, DOC-DB-002 §1.2).

---

## 2. CHECK Constraints (DB-enforced rules)

### 2.1 Money & amounts

| Constraint | Table | Expression | Canon |
|---|---|---|---|
| `ck_wallet_balance_non_negative` | `wallet` | `balance_yer >= 0` | BR-PAY-05 — balance never negative |
| `ck_order_total_range` | `order` | `total_yer BETWEEN 500 AND 5000000` | C-14 |
| `ck_order_money_non_negative` | `order` | `subtotal_yer >= 0 AND discount_yer >= 0 AND vat_yer >= 0 AND shipping_yer >= 0` | DATA-REQ-001 |
| `ck_order_money_consistent` | `order` | `total_yer = subtotal_yer - discount_yer + vat_yer + shipping_yer` | BR-FIN-02 (row-local form; Σ-sub-order equality is §5) |
| `ck_sub_order_money_consistent` | `sub_order` | same identity as above | BR-FIN-02 |
| `ck_sub_order_vat_formula` | `sub_order` | `vat_yer = (subtotal_yer - discount_yer) * 15 / 100` with half-up: `((subtotal_yer - discount_yer) * 15 + 50) / 100` (integer arithmetic) | BR-FIN-01, BR-FIN-05 |
| `ck_payment_order_amount_range` | `payment` | `NOT (kind='ORDER') OR total-range 500…5,000,000` | C-14 |
| `ck_payment_topup_amount_range` | `payment` | `NOT (kind='TOPUP') OR amount_yer BETWEEN 1000 AND 5000000` | BR-PAY-02 |
| `ck_payment_amount_positive` | `payment` | `amount_yer > 0` | DATA-REQ-001 |
| `ck_product_price_positive` | `product` | `price_yer > 0` | BR-CAT-04 (the 500-YER floor is an **order** bound — C-14 — not a product bound) |
| `ck_product_sale_price` | `product` | `sale_price_yer IS NULL OR (sale_price_yer > 0 AND sale_price_yer < price_yer)` | BR-CAT-04 |
| `ck_wallet_transaction_amount_nonzero` | `wallet_transaction` | `amount_yer <> 0` | ledger rows are movements (BR-PAY-06) |
| `ck_escrow_amounts` | `escrow` | `amount_yer >= 0 AND refunded_amount_yer >= 0 AND refunded_amount_yer <= amount_yer AND (payout_amount_yer IS NULL OR payout_amount_yer >= 0) AND (commission_amount_yer IS NULL OR commission_amount_yer >= 0)` | BR-ESC-01/07 |
| `ck_escrow_rate_band` | `escrow` | `commission_rate_bps BETWEEN 500 AND 2000` | BR-ESC-03 (5–20 %) |
| `ck_store_commission_rate_band` | `store` | `commission_rate_bps BETWEEN 500 AND 2000` (column `DEFAULT 1000`) | BR-ESC-03 default 10 % |
| `ck_coupon_value` | `coupon` | `value_percent BETWEEN 1 AND 90` when `type='PERCENT'`; `value_yer > 0` when `type='FIXED'` | BR-PRM-01/05 |
| `ck_currency_yer` | `order`, `payment`, `wallet`, `wallet_transaction`, `product` | `currency = 'YER'` | C-04 single currency |
| `ck_review_rating` | `review` | `rating BETWEEN 1 AND 5` | BR-REV-03 |
| `ck_order_item_qty_positive` | `order_item` | `qty >= 1 AND unit_price_yer > 0` | DATA-REQ-001, BR-CAT-04 |
| `ck_cart_item_qty` | `cart_item` | `qty BETWEEN 1 AND 10` | C-15 (≤10 units per product) |

### 2.2 Identity, format & OTP

| Constraint | Table | Expression | Canon |
|---|---|---|---|
| `ck_user_phone_hash_present` | `user` | `phone_ciphertext IS NOT NULL AND octet_length(phone_ciphertext) > 0 AND phone_hash IS NOT NULL` | BR-AUTH-01 + SEC-REQ-002 (phone stored as AES-256 ciphertext; HMAC lookup hash) |
| *(format `^7[0-9]{8}$`)* | — | **app-layer** — the plaintext never exists in the DB, so a SQL regex on the column is impossible by design | BR-AUTH-01 (validated pre-encryption; unit tests) |
| `ck_otp_code_hash_length` | `otp_challenge` | `octet_length(code_hash) >= 32` (SHA-256/bcrypt of a 6-digit code) | BR-AUTH-03 — 6-digit shape enforced app-side; only hash stored (SEC-REQ-002) |
| `ck_otp_expires_in_window` | `otp_challenge` | `expires_at > created_at AND expires_at - created_at <= interval '5 minutes'` | BR-AUTH-03 |
| `ck_otp_attempts` | `otp_challenge` | `attempts BETWEEN 0 AND 3` | BR-AUTH-03, SEC-REQ-005 |
| `ck_shipment_code_hash` | `shipment` | `octet_length(delivery_code_hash) >= 32` | SEC-REQ-002 (never plaintext), BR-SHP-02 |
| `ck_shipment_code_attempts` | `shipment` | `code_attempts BETWEEN 0 AND 3` | BR-SHP-03 |
| `ck_user_email_optional` | `user` | `email_ciphertext IS NULL OR email_hash IS NOT NULL` | BR-AUTH-08 |

### 2.3 States (enums)

Native PostgreSQL enum types (Prisma enums) + `NOT NULL`; **the CHECK is the enum type itself** — no other value can enter the column.

| Enum type | Values | Used by | Canon |
|---|---|---|---|
| `order_state` | exactly the 17 values: `PLACED, CONFIRMED, PROCESSING, READY_FOR_PICKUP, ASSIGNED, PICKED_UP, IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED, COMPLETED, CANCELLED, RETURN_REQUESTED, RETURN_APPROVED, RETURN_REJECTED, RETURN_RECEIVED, REFUNDED, DISPUTED` | `order.state`, `sub_order.state` | C-09, BR-ORD-01, DOC-SA-010 §1 |
| `payment_state` | `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED` | `payment.state` | payment intent lifecycle (FR-013) |
| `payment_method` | `WALLET, MFLOOS, ONECASH, BANK_TRANSFER` + `ck_payment_method_wallet_only`: `NOT (kind='ORDER') OR method='WALLET'` and `NOT (kind='TOPUP') OR method IN ('MFLOOS','ONECASH','BANK_TRANSFER')` | `payment.method` | C-01, C-05, BR-PAY-01 |
| `escrow_state` | `HELD, RELEASED, REFUNDED, FROZEN` | `escrow.state` | BR-ESC-01/02, BR-ORD-05 |
| `user_status` | `ACTIVE, SUSPENDED, DELETED` | `user.status` | FR-003 (DATA-REQ-003) |
| `role` | `CUSTOMER, VENDOR, COURIER, ADMIN, SUPER_ADMIN, MODERATOR` | `user_role.role` | FR-002 (6 login roles; `System` ACT-07 is not a login role — `audit_log.actor_type='SYSTEM'`) |
| `store_status` | `PENDING, ACTIVE, SUSPENDED, CLOSED` | `store.status` | FR-007/FR-008 |
| `kyc_status` | `PENDING, APPROVED, REJECTED` | `store.kyc_status` | BR-VND-01/03 |
| `product_status` | `DRAFT, ACTIVE, DISABLED` | `product.status` | BR-CAT-06, FR-004 |
| `return_state` | `REQUESTED, APPROVED, REJECTED, RECEIVED, INSPECTED` | `return_request.state` | BR-RET-02 (+ inspection, BR-RET-05) |
| `dispute_state` | `OPEN, UNDER_REVIEW, RESOLVED` + `dispute_resolution ∈ {VENDOR_FAVOURED, BUYER_FAVOURED}` | `dispute` | DISPUTED transitions (DOC-SA-010 §2) — `INFERENCE` for internal values |
| `notification_channel` | `SMS, WHATSAPP, IN_APP, PUSH` (**no `EMAIL` value**) | `notification.channel` | BR-NTF-01, GAP-03 |
| `notification_status` | `QUEUED, SENT, FAILED` | `notification.status` | FR-017 |
| `review_status` | `PENDING, APPROVED, REJECTED` (+ `is_hidden boolean`) | `review` | BR-REV-04 |
| `coupon_type` | `PERCENT, FIXED, FREE_SHIPPING, BUY_X_GET_Y` | `coupon.type` | BR-PRM-05 |
| `shipment_state` | `READY_FOR_PICKUP, ASSIGNED, PICKED_UP, IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED, CANCELLED` | `shipment.state` | delivery subset of DOC-SA-010 §2 |
| `ledger_type` | `TOPUP, ORDER_HOLD, ORDER_CAPTURE, RELEASE, REFUND, PAYOUT, COMMISSION, ADJUSTMENT` | `wallet_transaction.type` | BR-PAY-06/08, FR-013/014 |
| `ledger_account` | `CUSTOMER_WALLET, ESCROW_HELD, VENDOR_PAYABLE, PLATFORM_CASH, COMMISSION_INCOME, REFUND_CLEARING, ROUNDING_ACCOUNT` | `wallet_transaction.account` | BR-PAY-06 double-entry, BR-FIN-05 rounding account |

Enum evolution: PostgreSQL enums only support `ADD VALUE` (and only before first use in some paths) — removals/renames go through the expand/contract pattern (DOC-DB-006 §4); adding an order state would require a canon change to `C-09` first.

### 2.4 Conditional CHECKs worth calling out

| Constraint | Expression | Purpose |
|---|---|---|
| `ck_inventory_no_negative` | `qty_on_hand >= 0 AND qty_reserved >= 0 AND qty_reserved <= qty_on_hand AND qty_available >= 0` | **oversell impossible at DB level** (BR-CAT-07, FR-005) — `qty_available` is a generated column |
| `ck_inventory_version_non_negative` | `version >= 0` | optimistic lock integrity |
| `ck_payment_state_transition_shape` | `(state='REFUNDED') → kind='ORDER'` | top-ups are not "refunded" (they are reversed via ledger `ADJUSTMENT`/`REFUND` rows) |
| `ck_escrow_released_complete` | `state='RELEASED' → released_at IS NOT NULL AND commission_amount_yer IS NOT NULL AND commission_rate_bps IS NOT NULL` | commission computed at release (BR-ESC-03) |
| `ck_return_window` | `requested_at <= return_window_ends_at` | **deliberately NOT a DB CHECK** — see §5 note; window fields exist, enforcement is app-side so admin arbitration (BR-RET-06) is never blocked by DDL |
| `ck_notification_no_email` | enum has no `EMAIL` value | BR-NTF-01 (GAP-03) |
| `ck_coupon_window` | `ends_at > starts_at AND ends_at - starts_at <= interval '90 days'` | BR-PRM-01 |
| `ck_category_depth` | `level BETWEEN 1 AND 5` | BR-CAT-03, FR-004 (5 levels) |
| `ck_review_images_count` | `image_keys IS NULL OR jsonb_array_length(image_keys) <= 5` | BR-REV-03 |

---

## 3. UNIQUE Constraints

| Table | Constraint | Notes |
|---|---|---|
| `user` | `uq_user_phone_hash` | phone uniqueness (BR-AUTH-01) via HMAC lookup hash |
| `user` | `uq_user_email_hash` WHERE `email_hash IS NOT NULL` | optional email never duplicates (BR-AUTH-08) |
| `store` | `uq_store_slug`, `uq_store_owner_user_id` | storefront URL; **one store per vendor** (BR-VND-02) |
| `category` | `uq_category_parent_slug` (partial, `parent_id IS NOT NULL`), `uq_category_root_slug` (partial, `parent_id IS NULL`) | slugs unique **per level** (BR-CAT-03) — two partial indexes because Postgres treats NULL parents as distinct |
| `product` | `uq_product_store_id_slug` | product URL within a store |
| `product_variant` | `uq_product_variant_sku_store_id` | SKU unique within store (BR-CAT-02) |
| `order` | `uq_order_order_no`, `uq_order_idempotency_key` | human reference; duplicate submit returns original (BR-ORD-06) |
| `sub_order` | `uq_sub_order_order_id_store_id` | **exactly one sub-order per vendor** (C-10, BR-ORD-02) |
| `payment` | `uq_payment_idempotency_key`, `uq_payment_provider_ref` (partial) | idempotent money ops (BR-PAY-08, INT-REQ-006) |
| `wallet` | `uq_wallet_user_id` | one wallet per user (DB-010) |
| `wallet_transaction` | `uq_wallet_transaction_idempotency_key` | ledger posts once (BR-PLT-03) |
| `escrow` | `uq_escrow_sub_order_id` | one hold per sub-order |
| `shipment` | `uq_shipment_sub_order_kind_outbound` (partial) | one outbound shipment per sub-order; returns ship separately |
| `shipment_attempt` | `uq_shipment_attempt_shipment_id_attempt_no` | attempt counter integrity (BR-SHP-03) |
| `review` | `uq_review_order_item_id` | **one review per order item** (BR-REV-02) |
| `review_response` | `uq_review_response_review_id` | one vendor response (BR-REV-04) |
| `coupon` | `uq_coupon_code` | unique code (BR-PRM-01) |
| `coupon_redemption` | `uq_coupon_redemption_coupon_id_order_id` | one use per order; non-stackable (BR-PRM-02) |
| `cart` | `uq_cart_user_id_active` (partial) | one active cart per user |
| `cart_item` | `uq_cart_item_cart_id_product_id_variant_id` (`NULLS NOT DISTINCT`) | idempotent add-to-cart |
| `notification` | `uq_notification_user_dedup` (partial) | fan-out/retry dedup (INT-REQ-006) |
| `address` | `uq_address_user_id_default` (partial) | one default address |
| `session` | `uq_session_user_id_device_id` | ≤5 devices (BR-AUTH-06) — app-layer count check + this uniqueness |

**Not DB-enforced (app-layer + tests, by design):** ≤10 addresses (FR-003), ≤5 sessions (BR-AUTH-06), cart guards ≤50 products/≤5 vendors (C-15 — multi-row aggregates), ≤10 images (BR-CAT-08 — enforced via `jsonb_array_length` where possible), one coupon per order (`order.coupon_id` single column makes stacking structurally impossible), ≤50 combinations per variant set, 48-h KYC SLA (BR-VND-03), 24-h escalation (BR-ORD-10).

---

## 4. Exclusion / Anti-Anomaly Mechanisms

| Mechanism | Where | Effect |
|---|---|---|
| Generated column + CHECK | `inventory.qty_available GENERATED ALWAYS AS (qty_on_hand - qty_reserved) STORED`, `ck_inventory_no_negative` | stock **cannot** go negative even if app logic misbehaves (BR-CAT-07) |
| Row-level locking | `SELECT … FOR UPDATE` on the single `inventory` row; `wallet` row lock for balance check (BR-PAY-05) | concurrent reserve/pay serialize on one row — no overspend/negative balance |
| Optimistic `version` column | `inventory`, `order`, `sub_order`, `shipment`, `wallet`, `escrow` | stale write → `0 rows updated` → HTTP **409 `STATE_CONFLICT`** app-side (DOC-SA-010 §5) |
| `NULLS NOT DISTINCT` unique | `cart_item` composite unique | variant-less and variant rows don't collide or duplicate (PostgreSQL 15+ feature, available in 16) |
| Partial unique indexes | default addresses, active carts, one outbound shipment, provider refs | uniqueness scoped to the state where it matters |
| Transactional idempotency | `idempotency_key` UNIQUE + `SELECT`-before-insert | duplicate order/payment/top-up/refund returns the original result (BR-ORD-06, BR-PAY-08) |

True PostGIS-style **exclusion constraints** (`EXCLUDE USING gist`) are not required in v1: there are no time ranges or geometries to exclude (no GPS — `C-16`). If overlapping-reservation semantics were ever needed, `stock_reservation` would be the first candidate; the current model uses uniqueness + row locks instead.

---

## 5. Deferred Constraints (master/sub aggregates)

Two aggregates span rows and therefore cannot be plain row CHECKs:

| Constraint | Type | Verifies |
|---|---|---|
| `ct_order_totals_match_suborders` | `CONSTRAINT TRIGGER … DEFERRABLE INITIALLY DEFERRED` on `b06.sub_order` | at **COMMIT**: `order.total_yer = Σ(sub_order.total_yer)` and `order.vat_yer = Σ(sub_order.vat_yer)` for the touched order (BR-ORD-02, BR-FIN-02) |
| `ct_order_completed_suborders` | deferred constraint trigger on `b06.sub_order` | at **COMMIT**: if `order.state = 'COMPLETED'` then every sub-order state ∈ {`COMPLETED`, `REFUNDED`} (BR-ORD-07) |

Why deferred: during checkout and multi-vendor splits, master and sub-order rows are written inside **one transaction** (BR-PLT-04); an immediate FK-style check would fail mid-transaction on transient states. At commit the aggregate is consistent by construction.

Not deferred (kept immediate): row-local money identities (§2.1), enum membership, unique keys — they are true at statement end.

**Deliberate app-layer choices** (documented so nobody "fixes" them with triggers):

- **Return-window check** (BR-RET-01): fields `delivered_at` / `return_window_ends_at` are stored, but acceptance is decided app-side because the admin is the final arbiter when policy and dispute conflict (BR-RET-06); a hard DB CHECK could not be overridden by that rule.
- **17-state transition legality** (DOC-SA-010 §2): the DB enforces *vocabulary* (enum) and *monotonic history* (append-only `order_status_history`); the *from→to* matrix is enforced app-side so invalid transitions return **409** with a domain error instead of a 500 constraint violation, and unit tests enumerate all 17 states (DOC-SA-010 §6).
- **Cart guards** (C-15), **session cap** (BR-AUTH-06), **SLA timers** (BR-VND-03, BR-ORD-10): time/count based, multi-row — app-layer with jobs + tests.

---

## 6. Triggers vs App-Layer — the allowed list

**Only three trigger families exist in the entire schema.** Everything else is app-layer (§5).

| # | Trigger | Tables | Behavior |
|---|---|---|---|
| T1 | `trg_<table>_set_updated_at` (`BEFORE UPDATE`) | every mutable table (~25) | sets `updated_at = now()`; body is 2 lines, no exceptions, no logging |
| T2 | `ct_order_totals_match_suborders`, `ct_order_completed_suborders` (`BEFORE INSERT OR UPDATE` on `sub_order`, `DEFERRABLE INITIALLY DEFERRED`) | `b06.sub_order`, `b06.order` | §5 aggregate verification at commit |
| T3 | `trg_order_state_history` (`AFTER UPDATE OF state ON order/sub_order`, not deferrable) | `b06.order`, `b06.sub_order` | appends one `order_status_history` row (from_state, to_state, actor, reason) **as a DB backstop** so a state change can never occur without history (BR-ORD-03); the app still writes its own enriched row first (idempotency via `metadata.source = 'app'`) |

Forbidden triggers: money computation (VAT/total/app commission), state-machine legality, permission checks, denormalized-aggregate maintenance (ratings, follower counts are updated by the owning module's job — BR-REV-05), and anything calling external systems. Rationale: triggers are invisible to Prisma's query path, hard to test per NFR-010 (business logic unit-testable without network/DB), and violate module ownership (C-21).

---

## 7. Financial Immutability — Append-Only Enforcement (DATA-REQ-007, SEC-REQ-010)

**Append-only tables:** `b07.wallet_transaction`, `b06.order_status_history`, `b13.audit_log`.

| Layer | Mechanism |
|---|---|
| 1. **Privileges (primary control)** | App roles (`app_b07`, `app_b06`, `app_b13`, …) receive **`SELECT, INSERT` only**. `UPDATE`, `DELETE`, `TRUNCATE` are **`REVOKE`d** — not granted, so no application connection can modify or remove a posting even by mistake or SQL injection in a parameterized query. `DDL` rights exist only in the migration role (DOC-DB-006). |
| 2. **Ownership** | only the owning module's role can `INSERT` (e.g. ledger inserts come from `app_b07`); `SELECT` is granted per role scope (buyer reads own wallet rows via scoped queries; audit read per RBAC — `DOC-OVR-007`). |
| 3. **Corrections, not edits** | a wrong posting is corrected by a compensating row (`type='ADJUSTMENT'`, opposite sign) referencing the original `entry_group_id` — never by editing it (BR-PAY-06, DATA-REQ-007). Refunds/postings are likewise new rows. |
| 4. **Tamper evidence** | `audit_log` carries `seq`, `prev_hash`, `entry_hash` (SHA-256 chain over canonical JSON); a nightly job recomputes the chain and alerts on mismatch (SEC-REQ-010). |
| 5. **Retention** | partitions older than the ≥5-year window are archived, never row-deleted inside the window (DATA-REQ-003, NFR-019); purge attempts on young financial rows must alert, not delete (AC-DR003-03). |
| 6. **Verification** | daily reconciliation: `wallet.balance_yer = Σ wallet_transaction.amount_yer (wallet_id)`; `Σ amount_yer per entry_group_id = 0`; escrow/payable totals vs provider statements — mismatch pages finance (BR-ESC-08, BR-FIN-03, DATA-REQ-006). |

Note: because privileges block `UPDATE/DELETE`, restore/repair of these tables is a **migration-role operation** with two-person review — it can never happen through the API.

---

## 8. Integrity Verification (how we know it works)

| Check | Mechanism | Canon |
|---|---|---|
| Schema audit: every tenant table has owner keys + FK + index | CI script against `information_schema` (missing-owner report must be empty) | DATA-REQ-008 AC-DR008-01 |
| Cross-tenant suite per entity | CI integration tests, coverage gate | DATA-REQ-008 AC-DR008-02/04 |
| Constraint presence tests | migration snapshot tests: assert `ck_/uq_/fk_` names exist | DATA-REQ-001 |
| State count = 17 | test inspects `order_state` enum values | `TST-CON-09`, C-09 |
| Ledger balance & zero-imbalance | daily job + restore drill assertion | BR-PAY-06, DATA-REQ-004 AC-DR004-03 |
| Immutability | negative test: app role `UPDATE` on ledger/audit → `permission denied` | DATA-REQ-007, SEC-REQ-010 |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
