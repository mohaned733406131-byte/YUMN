---
document_id: DOC-DB-004
title: Indexes and Performance Strategy
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-001, NFR-003, NFR-004, NFR-007, NFR-017, NFR-018]
related_documents: [DOC-DB-001, DOC-DB-002, DOC-DB-003, DOC-DB-005]
---

# Indexes and Performance Strategy

Rules: **every query in a hot path must be index-backed (zero unexpected sequential scans)**, index names follow `idx_`/`uq_` (DOC-DB-001 §1), partial indexes are preferred over wide indexes when the predicate is stable, and every index below exists because a named query needs it. Volume drivers: **10M products, 100M order lines, 5-year retention** (NFR-017), p95 < 200 ms read / < 500 ms write (NFR-001), 10K concurrent users (C-25).

---

## 1. Index List by Table

### 1.1 Identity & Content (`b01`, `b03`, `b12`)

| Table | Index | Type | Backs (query) |
|---|---|---|---|
| `user` | PK `id` | btree | — |
| `user` | `uq_user_phone_hash` on `phone_hash` | UNIQUE | login/registration lookup, uniqueness (BR-AUTH-01) |
| `user` | `uq_user_email_hash` on `email_hash` WHERE `email_hash IS NOT NULL` | UNIQUE partial | optional email uniqueness (BR-AUTH-08) |
| `user` | `idx_user_status_created_at` on `(status, created_at DESC)` | compound | admin user list; partial `WHERE status='ACTIVE'` for authz cache warm paths |
| `user_role` | `uq_user_role_user_id_role` | UNIQUE | RBAC resolution per request (SEC-REQ-004) |
| `user_role` | `idx_user_role_role` | btree | admin "who has role X" listing |
| `session` | `uq_session_user_id_device_id` | UNIQUE | single row per device (BR-AUTH-06) |
| `session` | `idx_session_user_id_active` on `(user_id, last_seen_at DESC)` WHERE `revoked_at IS NULL` | partial | enforce ≤5 active sessions; session list UI |
| `otp_challenge` | `idx_otp_target_hash_created_at` on `(target_hash, created_at DESC)` | compound | OTP verify + resend-cooldown count (BR-AUTH-03) |
| `address` | PK `id` | btree | — |
| `address` | `idx_address_user_id` on `(user_id, is_default DESC, updated_at DESC)` | compound | address book (FR-003), checkout default-address fetch |
| `address` | `uq_address_user_id_default` on `(user_id)` WHERE `is_default` AND `deleted_at IS NULL` | UNIQUE partial | one default address per user |
| `store` | `uq_store_slug` | UNIQUE | storefront URL `/store/<slug>` (FR-008) |
| `store` | `uq_store_owner_user_id` | UNIQUE | one store per vendor (BR-VND-02) |
| `store` | `idx_store_status` on `(status, created_at DESC)` WHERE `status = 'ACTIVE'` | partial | public storefront listing |
| `store` | `idx_store_kyc_status_submitted_at` on `(kyc_status, kyc_submitted_at)` WHERE `kyc_status = 'PENDING'` | partial | KYC 48-h SLA queue (BR-VND-03) |
| `store_member` | `uq_store_member_store_id_user_id` | UNIQUE | staff role resolution (BR-VND-06) |
| `store_follower` | `uq_store_follower_store_id_user_id`; `idx_store_follower_user_id` | UNIQUE / btree | follow toggle; follower notification fan-out (BR-VND-05) |
| `coupon` | `uq_coupon_code` | UNIQUE | coupon validation at checkout (BR-PRM-01) |
| `coupon` | `idx_coupon_active_window` on `(starts_at, ends_at)` WHERE `is_active` | partial | active-coupon picker (vendor/admin) |
| `coupon` | `idx_coupon_store_id` ON `(store_id)` WHERE `store_id IS NOT NULL` | partial | vendor's coupon list (BR-PRM-03) |
| `coupon_redemption` | `uq_coupon_redemption_coupon_id_order_id` | UNIQUE | one redemption per order (BR-PRM-02) |
| `coupon_redemption` | `idx_coupon_redemption_coupon_id_user_id` on `(coupon_id, user_id, redeemed_at)` | compound | per-user usage limit (BR-PRM-04) |

### 1.2 Catalog (`b02`)

| Table | Index | Type | Backs (query) |
|---|---|---|---|
| `category` | `uq_category_root_slug` on `(slug)` WHERE `parent_id IS NULL` | UNIQUE partial | root slugs unique (BR-CAT-03) |
| `category` | `uq_category_parent_slug` on `(parent_id, slug)` WHERE `parent_id IS NOT NULL` | UNIQUE partial | sibling slugs unique (BR-CAT-03) |
| `category` | `idx_category_parent_position` on `(parent_id, position)` | compound | navigation tree ordering |
| `category` | `idx_category_status_level` on `(status, level)` | compound | admin tree editor, depth validation (≤5, BR-CAT-03) |
| `product` | PK `id` | btree | — |
| `product` | `uq_product_store_id_slug` | UNIQUE | product URL within store |
| `product` | `idx_product_store_id_status` on `(store_id, status, updated_at DESC)` | compound | vendor product list (FR-004) |
| `product` | `idx_product_category_id_status` on `(category_id, status)` WHERE `deleted_at IS NULL` | compound partial | category browse (FR-009) |
| `product` | `idx_product_storefront` on `(category_id, rating_avg DESC, created_at DESC)` WHERE `status='ACTIVE' AND deleted_at IS NULL` | compound partial | storefront/category listing without filtering deleted/disabled rows (BR-CAT-06) |
| `product` | `trgm_name_ar` on `name_ar` USING gin (pg_trgm) | GIN trigram | **search fallback** when Elasticsearch is down (NFR-007, §4) |
| `product` | `trgm_name_en` on `name_en` USING gin (pg_trgm) | GIN trigram | English fallback search |
| `product` | `idx_product_search_dirty` on `(updated_at)` WHERE `search_dirty` | partial | ES sync worker drains dirty rows (FR-009; ES is not SoR) |
| `product_image` | `uq_product_image_product_id_position`; `idx_product_image_object_key` | UNIQUE / btree | render order ≤10 images (BR-CAT-08); orphan-object reconciliation (DATA-REQ-006) |
| `product_variant` | `uq_product_variant_sku_store_id` | UNIQUE | SKU unique within store (BR-CAT-02) |
| `product_variant` | `idx_product_variant_product_id` on `(product_id)` WHERE `is_active` | partial | variant matrix in vendor panel |
| `inventory` | PK/FK `product_id` | btree | stock check = single-row lookup (FR-005) |
| `inventory` | `idx_inventory_store_id` on `(store_id)` | btree | vendor stock list |
| `stock_reservation` | `idx_stock_reservation_expires_at` on `(expires_at)` WHERE `status='HELD'` | partial | **15-min TTL sweeper** releases expired holds (C-13) |
| `stock_reservation` | `uq_stock_reservation_cart_item_id` on `(cart_item_id)` WHERE `status='HELD'` | UNIQUE partial | one live hold per cart line (idempotent reserve, BR-PLT-03) |
| `review` | `uq_review_order_item_id` | UNIQUE | one review per order item (BR-REV-02) |
| `review` | `idx_review_product_id_visible` on `(product_id, created_at DESC)` WHERE `status='APPROVED' AND NOT is_hidden` | compound partial | public review list + rating aggregation (BR-REV-05) |
| `review` | `idx_review_store_id_created_at` on `(store_id, created_at DESC)` | compound | vendor moderation inbox (BR-REV-04) |
| `review` | `idx_review_user_id_created_at` on `(user_id, created_at DESC)` | compound | "my reviews" (edit window, BR-REV-02) |
| `review_response` | `uq_review_response_review_id` | UNIQUE | one vendor response per review (BR-REV-04) |

### 1.3 Cart & Checkout (`b05`)

| Table | Index | Type | Backs (query) |
|---|---|---|---|
| `cart` | `uq_cart_user_id_active` on `(user_id)` WHERE `status='ACTIVE'` | UNIQUE partial | one active cart per user (BR-CRT-03 merge-on-login) |
| `cart` | `idx_cart_updated_at` on `(updated_at)` WHERE `status='ACTIVE'` | partial | abandonment sweeper (→ `ABANDONED`, releases reservations, C-13) |
| `cart_item` | PK `id` | btree | — |
| `cart_item` | `uq_cart_item_cart_id_product_id_variant_id` (NULLS NOT DISTINCT) | UNIQUE | idempotent add-to-cart, one line per product/variant |
| `cart_item` | `idx_cart_item_cart_id` on `(cart_id)` | btree | cart render (all lines for one cart) |
| `checkout_session` | `uq_checkout_session_idempotency_key` | UNIQUE | duplicate-submit returns original order (BR-ORD-06) |
| `checkout_session` | `idx_checkout_session_user_id_status` on `(user_id, status, created_at DESC)` | compound | resume checkout (FR-011 7-step) |

### 1.4 Orders (`b06`)

| Table | Index | Type | Backs (query) |
|---|---|---|---|
| `order` | PK `id` | btree | — |
| `order` | `uq_order_order_no` | UNIQUE | order lookup by human reference (support, BR-ORD-09) |
| `order` | `uq_order_idempotency_key` | UNIQUE | idempotent order creation (BR-ORD-06, BR-PLT-03) |
| `order` | `idx_order_buyer_state_created` on `(buyer_user_id, state, created_at DESC)` | compound | **hot path:** customer order list filtered by status (FR-012) |
| `order` | `idx_order_buyer_created_at` on `(buyer_user_id, created_at DESC)` | compound | customer order history unfiltered |
| `order` | `idx_order_state_created_at` on `(state, created_at DESC)` | compound | admin ops queues (CONFIRMED > 24 h escalation BR-ORD-10, CANCELLED review) |
| `order` | `idx_order_created_at` on `(created_at)` | btree | time-range dashboards; partition maintenance reference (NFR-017) |
| `sub_order` | `uq_sub_order_order_id_store_id` | UNIQUE | one sub-order per vendor (C-10, BR-ORD-02) |
| `sub_order` | `idx_sub_order_store_state_created` on `(store_id, state, created_at DESC)` | compound | **hot path:** vendor order panel filtered by state |
| `sub_order` | `idx_sub_order_order_id` on `(order_id)` | btree | master aggregate fetch (BR-ORD-07) |
| `sub_order` | `idx_sub_order_store_id_settlement` on `(store_id, updated_at)` WHERE `state IN ('DELIVERED','COMPLETED')` | partial | settlement/payout preparation scans |
| `order_item` | PK `(id, created_at)` — partitioned | btree | 100M rows (NFR-017) |
| `order_item` | `idx_order_item_order_id` on `(order_id, created_at)` | compound (partitioned) | order detail lines |
| `order_item` | `idx_order_item_sub_order_id` on `(sub_order_id, created_at)` | compound (partitioned) | sub-order detail (vendor view) |
| `order_item` | `idx_order_item_product_created` on `(product_id, created_at DESC)` | compound (partitioned) | product sales history; FR-018 reports |
| `order_status_history` | PK `(id, created_at)` — partitioned | btree | append-only timeline (BR-ORD-03) |
| `order_status_history` | `idx_osh_order_created` on `(order_id, created_at)` | compound (partitioned) | **customer timeline** (BR-ORD-09) |
| `order_status_history` | `idx_osh_sub_order_created` on `(sub_order_id, created_at)` WHERE `sub_order_id IS NOT NULL` | partial (partitioned) | vendor timeline scope |

### 1.5 Payment, Wallet, Escrow (`b07`)

| Table | Index | Type | Backs (query) |
|---|---|---|---|
| `payment` | PK `id` | btree | — |
| `payment` | `uq_payment_idempotency_key` | UNIQUE | idempotent payment/top-up/refund (BR-PAY-08) |
| `payment` | `uq_payment_provider_ref` on `(provider, provider_ref)` WHERE `provider_ref IS NOT NULL` | UNIQUE partial | idempotent provider callbacks/polls (INT-REQ-001/006) |
| `payment` | `idx_payment_order_id` on `(order_id)` WHERE `order_id IS NOT NULL` | partial | order → payment fetch (checkout status) |
| `payment` | `idx_payment_payer_created` on `(payer_user_id, created_at DESC)` | compound | wallet history UI (top-ups listed) |
| `payment` | `idx_payment_state_kind_created` on `(state, kind, created_at)` WHERE `state IN ('PENDING','AUTHORIZED')` | partial | expiry sweeper + reconciliation window (BR-ESC-08) |
| `wallet` | `uq_wallet_user_id` | UNIQUE | wallet fetch per request (1:1, DB-010) |
| `wallet_transaction` | PK `(id, created_at)` — partitioned | btree | ledger volume (NFR-017) |
| `wallet_transaction` | `uq_wallet_transaction_idempotency_key` | UNIQUE | ledger posts exactly once (BR-PAY-08, BR-PLT-03) |
| `wallet_transaction` | `idx_wt_wallet_created` on `(wallet_id, created_at DESC)` | compound (partitioned) | **hot path:** wallet statement, newest first (FR-013) |
| `wallet_transaction` | `idx_wt_entry_group_id` on `(entry_group_id)` | compound (partitioned) | double-entry validation Σ per group = 0 (BR-PAY-06) |
| `wallet_transaction` | `idx_wt_reference` on `(reference_type, reference_id)` | compound (partitioned) | order/payment/refund → ledger evidence |
| `wallet_transaction` | `idx_wt_type_created` on `(type, created_at)` | compound (partitioned) | daily reconciliation by type (BR-ESC-08, BR-FIN-03) |
| `escrow` | PK `id`; `uq_escrow_sub_order_id` | btree / UNIQUE | per-sub-order hold (C-10 allocation) |
| `escrow` | `idx_escrow_due` on `(release_at)` WHERE `state='HELD'` | partial | **release job:** DELIVERED + 7 d → RELEASED (BR-ESC-01/02) |
| `escrow` | `idx_escrow_state_order_id` on `(state, order_id)` | compound | dispute freeze checks (BR-ORD-05) |
| `escrow` | `idx_escrow_store_state` on `(store_id, state)` | compound | vendor payable balance (BR-ESC-05) |
| `refund` | `uq_refund_idempotency_key` | UNIQUE | double-refund protection (BR-PAY-08) |
| `refund` | `idx_refund_state_created` on `(state, created_at)` WHERE `state='PENDING'` | partial | refund execution worker (BR-RET-04 ≤3 business days) |
| `payout` | `idx_payout_store_state_created` on `(store_id, state, created_at DESC)` | compound | vendor payout history (FR-014) |
| `payout` | `idx_payout_state` on `(state, eligible_at)` WHERE `state='ELIGIBLE'` | partial | batch job: ≥1,000 YER, 3–7 business days (BR-ESC-05) |

### 1.6 Delivery & Returns (`b08`, `b09`)

| Table | Index | Type | Backs (query) |
|---|---|---|---|
| `shipment` | `uq_shipment_sub_order_kind_outbound` on `(sub_order_id)` WHERE `kind='OUTBOUND'` | UNIQUE partial | one outbound shipment per sub-order |
| `shipment` | `idx_shipment_courier_state` on `(courier_id, state)` WHERE `courier_id IS NOT NULL` | compound partial | courier app: my active deliveries (FR-015) |
| `shipment` | `idx_shipment_dispatch` on `(zone, state)` WHERE `state IN ('READY_FOR_PICKUP','OUT_FOR_DELIVERY')` | compound partial | assignment engine: eligible couriers in zone (BR-SHP-04) |
| `shipment` | `idx_shipment_sub_order_id` | btree | sub-order → delivery status |
| `shipment_attempt` | `uq_shipment_attempt_shipment_id_attempt_no` | UNIQUE | attempt numbering for 3-strike lock (BR-SHP-03) |
| `shipment_attempt` | `idx_shipment_attempt_courier_created` on `(courier_id, created_at DESC)` | compound | courier delivery history/proof (BR-SHP-07) |
| `shipment_offer` | `uq_shipment_offer_shipment_id_courier_id` | UNIQUE | no duplicate offers |
| `shipment_offer` | `idx_shipment_offer_courier_status` on `(courier_id, status, expires_at)` | compound | courier offer inbox; first-accept race (BR-SHP-04) |
| `shipping_zone` / `shipping_rate` | `uq_shipping_zone_code`; `uq_shipping_rate_zone_method` | UNIQUE | fee lookup `f(zone, weight, method)` (BR-SHP-01) |
| `return_request` | PK `id` | btree | — |
| `return_request` | `idx_return_buyer_created` on `(buyer_user_id, created_at DESC)` | compound | customer returns list (FR-016) |
| `return_request` | `idx_return_store_state_created` on `(store_id, state, created_at DESC)` | compound | vendor return queue (BR-RET-02) |
| `return_request` | `idx_return_inspection_due` on `(inspection_due_at)` WHERE `state='RECEIVED'` | partial | **72-h inspection sweeper** → auto-approve (BR-RET-05) |
| `return_request` | `idx_return_order_id` on `(order_id)` | btree | order → returns |
| `return_item` | `uq_return_item_return_request_id_order_item_id` | UNIQUE | no duplicate item lines |
| `return_evidence` | `idx_return_evidence_return_request_id` | btree | evidence gallery (≤5 MB, SEC-REQ-011) |

### 1.7 Notifications & Audit (`b10`, `b13`)

| Table | Index | Type | Backs (query) |
|---|---|---|---|
| `notification` | PK `id` | btree | — |
| `notification` | `idx_notification_user_created` on `(user_id, created_at DESC)` | compound | in-app inbox (FR-017) |
| `notification` | `idx_notification_queue` on `(created_at)` WHERE `status='QUEUED'` | partial | sender worker drains queue (BR-PLT-01/02) |
| `notification` | `uq_notification_user_dedup` on `(user_id, dedup_key)` WHERE `dedup_key IS NOT NULL` | UNIQUE partial | fan-out/retry dedup (INT-REQ-006) |
| `notification` | `idx_notification_template_created` on `(template_key, created_at)` | compound | template delivery stats (FR-017) |
| `notification_preference` | `uq_notification_pref_user_channel_category` | UNIQUE | per-channel opt-out (BR-NTF-05) |
| `audit_log` | PK `(id, created_at)` — partitioned | btree | append-only, ≥5 y retention (SEC-REQ-010, DATA-REQ-003) |
| `audit_log` | `uq_audit_log_seq` on `(seq)` | UNIQUE | hash-chain ordering (SEC-REQ-010) |
| `audit_log` | `idx_audit_entity` on `(entity_type, entity_id, created_at DESC)` | compound | "history of this order/wallet" (FR-020) |
| `audit_log` | `idx_audit_actor_created` on `(actor_user_id, created_at DESC)` WHERE `actor_user_id IS NOT NULL` | partial | admin action review |
| `audit_log` | `idx_audit_action_created` on `(action, created_at DESC)` | compound | filtered audit search (e.g. `wallet.freeze`) |

---

## 2. Hot Paths — Justification

| # | Query | Plan expected | Index |
|---|---|---|---|
| HP-1 | Customer order list by state | Index scan on `(buyer_user_id, state, created_at DESC)`, backward/index-only where possible | `idx_order_buyer_state_created` |
| HP-2 | Vendor order panel by state | Index scan `(store_id, state, created_at DESC)` on `sub_order` | `idx_sub_order_store_state_created` |
| HP-3 | Wallet statement newest-first | Index scan `(wallet_id, created_at DESC)` limited 20, no sort | `idx_wt_wallet_created` |
| HP-4 | Stock check/reserve | Single-row lookup by PK `inventory.product_id`, `FOR UPDATE` of that row only | PK + row lock (no lock ordering issue: one row per reserve) |
| HP-5 | Search fallback (ES down) | GIN trigram on `name_ar`, `LIMIT` + relevance order | `trgm_name_ar` (§4) |
| HP-6 | Escrow release sweep | Partial index `WHERE state='HELD'` + `release_at <= now()` range | `idx_escrow_due` |
| HP-7 | Reservation expiry sweep | Partial index `WHERE status='HELD'` on `expires_at` | `idx_stock_reservation_expires_at` |
| HP-8 | Delivery code verify | Row lookup `shipment` by PK; attempt uniqueness prevents bypass | PK + `uq_shipment_attempt_*` |
| HP-9 | Customer timeline | `order_status_history (order_id, created_at)` index-only scan | `idx_osh_order_created` |
| HP-10 | Storefront category page | Partial index excludes non-ACTIVE/deleted rows, pre-sorted by rating | `idx_product_storefront` |

---

## 3. N+1 Avoidance (Prisma 5)

1. **Batch by ID:** never loop `findUnique` per parent — use `findMany({ where: { orderId: { in: ids } } })` and group in memory (repository layer enforces this pattern).
2. **Explicit `select`/`include`:** nested relations are fetched with one `include` tree, never per-row lazy loads; deep trees (order → items → product → store) are fetched with bounded depth (≤ 3) per call.
3. **Aggregate in SQL:** rating averages (BR-REV-05), counts, and sums use `groupBy`/`aggregate`; client-side reduction of large sets is a review defect.
4. **Cursor pagination** (`cursor` + `where id < …`) for infinite lists instead of `OFFSET`, which degrades at depth on 100M-row tables (NFR-017).
5. **Guardrail:** slow-query log flags any statement > 50 ms with call-site; PR review checks repository methods for per-row queries; load test (NFR-003) fails on query-count-per-request regression.
6. Cross-module reads go through the owning module's repository (C-21), which returns pre-joined projections instead of letting callers traverse foreign schemas.

---

## 4. Search Fallback (NFR-007)

Elasticsearch is the primary search path (FR-009) but **is not the system of record**. On ES outage the degraded path runs against PostgreSQL:

```sql
SELECT id, name_ar, name_en, price_yer, store_id
FROM b02.product
WHERE status = 'ACTIVE' AND deleted_at IS NULL
  AND (name_ar ILIKE '%' || $1 || '%' OR name_en ILIKE '%' || $1 || '%')
ORDER BY rating_avg DESC, created_at DESC LIMIT 24;
```

Backed by the `pg_trgm` GIN indexes (`trgm_name_ar`, `trgm_name_en`) — enabled as an extension in the baseline migration. Fallback is ranked below ES in latency budget but must stay inside NFR-001 read p95 for the first 24 results; category browse never depends on ES at all (`idx_product_storefront`).

---

## 5. Partitioning (NFR-017)

| Table | Strategy | Key | Rationale |
|---|---|---|---|
| `b06.order_item` | Range, **monthly** partitions | `created_at` | 100M rows over 5 y ≈ 1.7M/month; retention drops whole partitions; hot partition stays cached |
| `b07.wallet_transaction` | Range, **monthly** partitions | `created_at` | ledger append-only; 5-year financial retention = drop/ archive partitions, never row deletes (DATA-REQ-003) |
| `b06.order_status_history` | Range, **monthly** partitions | `created_at` | highest write-rate append table; timeline queries are always recent-range |
| `b13.audit_log` | Range, **yearly→monthly as volume grows** | `created_at` | ≥5 y immutability + retention (SEC-REQ-010, DATA-REQ-003) |
| `b06.order` (master) | **Not partitioned in v1** | — | cardinality ≈ order_item ÷ lines; partitioning would force every FK (`sub_order`, `escrow`, `payment`) to carry `created_at` — revisit via migration (expand/contract, DOC-DB-006) if volume test shows bloat |

Mechanics:

- Primary keys on partitioned tables are composite `(id, created_at)`; FKs pointing at them must include `created_at` (Postgres requirement) — DOC-DB-003 FK register marks these.
- A **partition maintenance job** (BullMQ, BR-PLT-01) creates next month's partitions ahead of time and drops/archives partitions older than the retention window; it runs in dry-run mode first for financial tables (NFR-017 AC-NFR-017-02).
- Partition creation is handwritten SQL inside Prisma migrations (DOC-DB-002 §2, DOC-DB-006 §6).

---

## 6. Vacuum / Autovacuum

| Table class | Tables | Tuning |
|---|---|---|
| Append-only (no dead tuples) | `wallet_transaction`, `order_status_history`, `audit_log`, `notification` | default autovacuum for stats; no bloat concern; `fillfactor 100` |
| Hot-updated (state/qty churn) | `order`, `sub_order`, `inventory`, `wallet`, `shipment`, `cart_item` | `autovacuum_vacuum_scale_factor = 0.02`, `autovacuum_analyze_scale_factor = 0.01`, `fillfactor 90` so updated rows don't spill to new pages |
| Wide JSONB | `audit_log.before/after`, `notification.payload` | monitor `pg_stat_user_tables.n_dead_tup`; toast-heavy updates avoided (audit is insert-only) |

Rules:

- `VACUUM (FULL)` is **never** run in production (locks); bloat is handled by autovacuum tuning + `pg_repack` in a maintenance window if ever required.
- Alerting: dead-tuple ratio > 20 % on any hot table, and autovacuum not completed within 1 h (NFR-014).
- Index bloat checked quarterly against NFR-017 forecast (≤ 10 % disk variance).

---

## 7. EXPLAIN-Plan Review Policy

1. **Baseline capture:** the 20 hottest queries (HP table §2 + FR-018 report queries) have `EXPLAIN (ANALYZE, BUFFERS)` baselines stored in the repo under test fixtures; CI compares plans on a seeded staging DB.
2. **Regression gate:** any plan change introducing a **sequential scan on a hot path**, a sort of > 10k rows, or a cost increase > 2× fails CI (NFR-017 AC-NFR-017-01: "0 unexpected seq scans").
3. **PR rule:** a PR that adds/changes a repository query must attach its `EXPLAIN (ANALYZE)` output for a representative dataset (> 10k rows per touched table) — an empty-table plan is not evidence.
4. **Load corroboration:** plans are re-validated under the k6 profile (NFR-003) at the 10M/100M volume test (NFR-017); p95 must hold NFR-001.
5. **Drift review:** quarterly plan review as part of the capacity review; index usage tracked via `pg_stat_user_indexes` — an index with zero scans for two quarters is a candidate for removal (documented in this file's change history).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
