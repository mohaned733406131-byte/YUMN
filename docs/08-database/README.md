---
document_id: DOC-DB-001
title: Database Domain — Overview and File Index
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-002, DATA-REQ-005, DATA-REQ-007, DATA-REQ-008, NFR-017]
related_documents: [DOC-OVR-002, DOC-OVR-008, DOC-REQ-001, DOC-BA-005, DOC-SA-010]
---

# Database Domain — Overview and File Index

**Scope of `08-database/`:** the relational data model of yumn — architecture decisions, the entity-relationship register, index strategy, DB-level constraints, migration/evolution workflow, and one entity document per registered entity (`DB-001…DB-018`). This README is the entry point and the conventions contract for every file in this directory.

**Baseline:** PostgreSQL 16 is the only relational database (`C-19`); Prisma 5 is the ORM/migration tool; Redis 7, Elasticsearch 8 and MinIO are deliberately *not* part of this schema (see [database-overview.md](database-overview.md)). The database is the **system of record** for money; Elasticsearch and Redis never are.

**Design posture:** integrity is enforced in the database first (DATA-REQ-001), business rules that span rows or require context stay app-layer (with DB backstops where cheap), and every tenant-scoped table carries owner keys (DATA-REQ-008).

---

## 1. Naming Conventions (binding for all files here)

| Kind | Convention | Examples |
|---|---|---|
| Schemas | `b01…b13` — one per block (B01…B13, `DOC-OVR-002` §Platform Decomposition) | `b06.order`, `b07.wallet` |
| Tables | **singular `snake_case`** — chosen so entity file name = table name = Prisma `@@map` value, and to avoid irregular plural forms (`category` → `category`, not `categories`). Reserved words (`user`, `order`) are always quoted in DDL; Prisma quotes identifiers automatically. | `user`, `sub_order`, `wallet_transaction` |
| Columns | `snake_case`; FKs `<entity>_id`; timestamps `*_at` (`timestamptz`, UTC); booleans `is_*`/`has_*` | `buyer_user_id`, `released_at`, `is_frozen` |
| Money columns | integer YER with **`_yer` suffix** (see §3) | `price_yer`, `balance_yer`, `amount_yer` |
| Primary keys | `id` (`uuid`) on every table; composite `(id, created_at)` on partitioned tables | — |
| Indexes | `idx_<table>_<col>_<col>`; unique `uq_<table>_<col>_<col>`; partial indexes state the predicate in the index doc, not the name | `idx_order_buyer_user_id_state_created_at` |
| Check constraints | `ck_<table>_<rule>` | `ck_order_total_range` |
| Foreign keys | `fk_<table>_<column>` (applied through Prisma `@relation(map: …)` so `schema.prisma` and the database cannot drift) | `fk_sub_order_order_id` |
| Enum types | snake_case type name, `SCREAMING_SNAKE_CASE` values | `order_state = 'OUT_FOR_DELIVERY'` |
| Entity documents | `entities/<table>.md`, frontmatter `entity_id: DB-NNN` | `entities/wallet_transaction.md` → `DB-011` |
| Soft delete | `deleted_at timestamptz NULL` where deletion is soft (BR-CAT-06); account deletion is anonymization, not row drop (DATA-REQ-003) | `product.deleted_at` |
| Append-only tables | `created_at` only — no `updated_at`, `UPDATE`/`DELETE` revoked (§4) | `wallet_transaction`, `order_status_history`, `audit_log` |

> The full register of top-level documents and entities is in §4 below. Relationship detail lives in [entity-relationship.md](entity-relationship.md); DB-enforced rules in [constraints-and-integrity.md](constraints-and-integrity.md).

---

## 2. ID Strategy — UUID v7 (application-generated)

**Decision: every business table uses a client-generated UUID v7 in a `uuid` primary key column.**

| Criterion | Why UUID v7 wins for yumn |
|---|---|
| Write scale | Stateless API replicas (NFR-018) and BullMQ workers (C-20) insert concurrently; a central `BIGSERIAL` sequence becomes a hot row under `C-25` (10,000 concurrent users). UUID v7 needs no coordination. |
| Index locality | UUID v7 is time-ordered, so B-tree inserts are append-mostly — critical for the 100M-row order-line and ledger tables (`NFR-017`), unlike random UUID v4. |
| No enumeration | IDs are not sequential/guessable, which is defense-in-depth for `SEC-REQ-004` ownership checks (authorization remains the real control — never ID opacity alone). |
| Partition friendliness | Partitioned tables use `(id, created_at)` primary keys; UUID v7 prefix ordering does not fight the `created_at` range key. |
| Tooling | Prisma 5 maps `@default(uuid())` to UUID **v4**, so v7 is generated in the application layer (one shared `newId()` helper) and supplied on every `create`. CI test asserts no v4 IDs enter the tables. |

**Natural (human) keys are used where people read them:** `order.order_no` (format `YM-<yymmdd>-<6 random chars>`, e.g. `YM-260926-8F3K2Q`), `store.slug`, `coupon.code`, `product.slug`. These are **unique business identifiers, not primary keys**, and are separately indexed.

**What is deliberately *not* used:** `BIGSERIAL`/identity columns as PKs (coordination hotspot, enumeration); integer surrogate IDs exposed via API (IDOR surface).

---

## 3. Money-as-Integer Rule (non-negotiable)

1. **All monetary values are `bigint` columns holding whole Yemeni Rials.** No floats, no `double precision`, no `numeric` with fractional scale, no minor units — YER has no subdivision in v1 (`BR-PAY-10`, `C-04`).
2. Money columns carry the **`_yer` suffix** so a missing conversion is visible in review: `price_yer`, `amount_yer`, `total_yer`, `commission_amount_yer`.
3. `currency` columns, where present, are `char(3)` with `CHECK (currency = 'YER')` — single currency (`C-04`).
4. Rounding is half-up to whole YER **per sub-order** (`BR-FIN-05`); the resulting `CHECK` lives on `b06.sub_order` (see DOC-DB-005).
5. Sums, products and VAT are computed in `bigint` arithmetic in SQL/CHECKs (`(x * 15 + 50) / 100` = half-up 15%); application code uses `bigint`/`BigInt` end to end.
6. The **ledger (`b07.wallet_transaction`) is the only source of truth for balances**; `wallet.balance_yer` is a materialized cache verified against the ledger by the daily reconciliation job (`BR-PAY-06`, `BR-ESC-08`, DATA-REQ-006). Redis is never a source of truth for money.

---

## 4. File Index

### 4.1 Top-level documents

| Doc ID | File | Purpose |
|---|---|---|
| DOC-DB-001 | [README.md](README.md) | This file: domain overview, conventions, ID & money rules, full index |
| DOC-DB-002 | [database-overview.md](database-overview.md) | PostgreSQL 16 architecture: schema-per-module, Prisma 5, pooling, environments, what lives outside Postgres |
| DOC-DB-003 | [entity-relationship.md](entity-relationship.md) | ER register: text ERDs per bounded area, relationship table, ownership boundaries, master/sub-order model |
| DOC-DB-004 | [indexes-and-performance.md](indexes-and-performance.md) | Table-by-table index list, hot-path justification, N+1 avoidance, partitioning (NFR-017), vacuum, EXPLAIN policy |
| DOC-DB-005 | [constraints-and-integrity.md](constraints-and-integrity.md) | FK rules, CHECK/UNIQUE/exclusion constraints, allowed triggers, append-only enforcement, app vs DB split |
| DOC-DB-006 | [migrations-and-evolution.md](migrations-and-evolution.md) | Prisma Migrate workflow (DATA-REQ-005): branching, expand/contract, seeds, rollback, CI gates |
| DOC-DB-007 | [entities/README.md](entities/README.md) | Entity index: DB-NNN → file → purpose → owning block |

### 4.2 Entities (18 registered entities)

| entity_id | File | Doc ID | Owning schema / block | One-line purpose |
|---|---|---|---|---|
| DB-001 | [entities/user.md](entities/user.md) | DOC-DBE-001 | `b01` / B01 | Account identity: encrypted phone, password hash, roles, status, locale, deletion markers |
| DB-002 | [entities/address.md](entities/address.md) | DOC-DBE-002 | `b01` / B01 | Customer delivery addresses (≤10), governorate/district, default flag, no GPS |
| DB-003 | [entities/store.md](entities/store.md) | DOC-DBE-003 | `b03` / B03 | Vendor storefront: owner, names, slug, status, KYC, commission tier, hub text, hours |
| DB-004 | [entities/category.md](entities/category.md) | DOC-DBE-004 | `b02` / B02 | Category tree (≤5 levels), bilingual names, per-level unique slugs, position |
| DB-005 | [entities/product.md](entities/product.md) | DOC-DBE-005 | `b02` / B02 | Sellable item: Arabic-first names, price YER, return policy, status, rating denorm, search flags |
| DB-006 | [entities/inventory.md](entities/inventory.md) | DOC-DBE-006 | `b02` / B02 | Stock row per product: on-hand/reserved/available, 15-min reservation TTL, optimistic version |
| DB-007 | [entities/cart.md](entities/cart.md) | DOC-DBE-007 | `b05` / B05 | One active cart per logged-in user; items in `b05.cart_item`; guards per C-15 |
| DB-008 | [entities/order.md](entities/order.md) | DOC-DBE-008 | `b06` / B06 | Master order: order_no, 17-state enum, money columns, wallet-only, sub-orders, state history |
| DB-009 | [entities/payment.md](entities/payment.md) | DOC-DBE-009 | `b07` / B07 | Payment/top-up intents: state machine, wallet-only for orders, idempotency key, provider refs |
| DB-010 | [entities/wallet.md](entities/wallet.md) | DOC-DBE-010 | `b07` / B07 | One wallet per user: balance ≥ 0 (cache of ledger), freeze flag, YER only |
| DB-011 | [entities/wallet_transaction.md](entities/wallet_transaction.md) | DOC-DBE-011 | `b07` / B07 | Append-only double-entry ledger: signed amounts, balance_after, references, idempotency |
| DB-012 | [entities/escrow.md](entities/escrow.md) | DOC-DBE-012 | `b07` / B07 | Per-sub-order hold: funded at PLACED, release_at = DELIVERED + 7 d, commission at release |
| DB-013 | [entities/shipment.md](entities/shipment.md) | DOC-DBE-013 | `b08` / B08 | Delivery execution: courier, delivery-state mirror, hashed 6-digit code, attempt lock, zone text |
| DB-014 | [entities/return_request.md](entities/return_request.md) | DOC-DBE-014 | `b09` / B09 | Return lifecycle: window fields, 72-h inspection due date, evidence, refund link |
| DB-015 | [entities/review.md](entities/review.md) | DOC-DBE-015 | `b02` / B02 | Verified-purchase review: rating 1–5, moderation status, one per order item |
| DB-016 | [entities/coupon.md](entities/coupon.md) | DOC-DBE-016 | `b12` / B12 | Coupon definitions: type/value, ≤90-day window, usage limits, scope, non-stackable |
| DB-017 | [entities/notification.md](entities/notification.md) | DOC-DBE-017 | `b10` / B10 | Outbound message record: 4 channels (no email v1), template, dedup, read state |
| DB-018 | [entities/audit_log.md](entities/audit_log.md) | DOC-DBE-018 | `b13` / B13 | Append-only, hash-chained audit of privileged and money actions |

**Supporting tables** (sub_order, order_item, order_status_history, cart_item, stock_reservation, payout, refund, dispute, session, otp_challenge, user_role, …) have no separate entity document; they are specified inside the ER register (DOC-DB-003) and in the relationship/invariant sections of their aggregate's entity file.

---

## 5. How to Use This Domain

1. Read [database-overview.md](database-overview.md) for placement and non-Postgres stores.
2. Read [entity-relationship.md](entity-relationship.md) to see the whole model before touching any single table.
3. Open the entity file for the table you are changing; check its **Invariants** section first.
4. Before writing a migration, read [constraints-and-integrity.md](constraints-and-integrity.md) and [migrations-and-evolution.md](migrations-and-evolution.md).

Cross-domain references: requirements `02-requirements/` (esp. DATA-REQ-001…008), rules `01-business-analysis/business-rules.md`, states `../03-system-analysis/core/state-transitions.md`, constraints `00-project-overview/project-constraints.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
