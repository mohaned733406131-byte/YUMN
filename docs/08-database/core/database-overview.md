---
document_id: DOC-DB-002
title: Database Architecture Overview (PostgreSQL 16 + Prisma 5)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-004, DATA-REQ-005, NFR-003, NFR-004, NFR-007, NFR-018, NFR-020]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-006, DOC-OVR-008, DOC-OVR-002]
---

# Database Architecture Overview

**Decisions recorded here:** how PostgreSQL 16 is partitioned into schemas for the modular monolith, what Prisma 5 is and is not responsible for, how connections are pooled at `C-25` scale, how environments are isolated, and which data deliberately lives *outside* PostgreSQL.

---

## 1. Single Database, Schema-per-Module (aligned with C-21)

**Decision: one PostgreSQL 16 database per environment, subdivided into 13 schemas `b01…b13`, one per block.** This realizes the canon statement in `DOC-OVR-002`: *"Each block maps 1:1 to a database schema (`b01…b13`)"*, and it is the data-layer expression of the modular monolith (`C-21`).

| Option | Verdict | Reason |
|---|---|---|
| **Schema-per-module (`b01…b13`)** | **Chosen** | Module boundary visible in the database itself: `b07` (money) is owned by the payment module, and cross-schema object access is reviewable in one place. Schemas give object-level privileges per module role without paying for multiple databases. |
| Single flat schema with table prefixes (`b07_wallet`) | Rejected as primary scheme | Prefixes are convention-only — nothing stops `b06` code from writing `b07_wallet`; privileges cannot be granted per prefix. Retained only as a naming echo (`idx_`/`ck_` names), never as structure. |
| Database-per-module | Rejected | Cross-schema transactions would become impossible; order placement must atomically write `b05/b06/b07` rows in one ACID transaction (NFR-008, BR-PLT-04). `C-19` mandates one PostgreSQL, and multi-database XA adds operational cost with no v1 benefit. |
| Microservice DB-per-service | Out of scope | Forbidden by `C-21` (modular monolith, `ADR-002`). |

### 1.1 Schema map

| Schema | Block | Owns (entities + key supporting tables) |
|---|---|---|
| `b01` | B01 Identity & Access | `user` (DB-001), `address` (DB-002), `user_role`, `session`, `otp_challenge`, `governorate` |
| `b02` | B02 Product Catalog | `category` (DB-004), `product` (DB-005), `inventory` (DB-006), `review` (DB-015), `product_image`, `product_variant`, `stock_reservation`, `category_attribute`, `product_attribute_value` |
| `b03` | B03 Store Management | `store` (DB-003), `store_member`, `kyc_document`, `store_follower` |
| `b04` | B04 Search & Discovery | No base tables in v1 — query path reads `b02` + Elasticsearch; merchandising content is authored in `b12` (see §5) |
| `b05` | B05 Cart & Checkout | `cart` (DB-007), `cart_item`, `checkout_session` |
| `b06` | B06 Order Management | `order` (DB-008), `sub_order`, `order_item`, `order_status_history` |
| `b07` | B07 Payment & Wallet | `payment` (DB-009), `wallet` (DB-010), `wallet_transaction` (DB-011), `escrow` (DB-012), `refund`, `payout` |
| `b08` | B08 Shipping & Delivery | `shipment` (DB-013), `shipment_attempt`, `shipment_offer`, `shipping_zone`, `shipping_rate` |
| `b09` | B09 Returns & Refunds | `return_request` (DB-014), `return_item`, `return_evidence` |
| `b10` | B10 Notifications | `notification` (DB-017), `notification_preference` |
| `b11` | B11 Analytics & Reporting | No base tables — reads run against `b06/b07` on the read replica (NFR-018) |
| `b12` | B12 Content & CMS | `coupon` (DB-016), `coupon_redemption`, `banner`, `cms_page` |
| `b13` | B13 Platform Administration | `audit_log` (DB-018), `audit_chain`, `platform_setting`, `support_ticket`, `dispute` |

### 1.2 Boundary mechanics

- Each module gets a PostgreSQL **role** (`app_b06`, `app_b07`, …) with `USAGE` on its own schema, `SELECT` on reference schemas it must read (e.g. `b06` reads `b01.user`, `b03.store`), and **no write grant on other modules' schemas** — the DB mirror of enforced module boundaries (NFR-009, `C-21`) and of ownership boundaries (DATA-REQ-008).
- Cross-schema **foreign keys are allowed and used** (they cost nothing inside one database) — they encode real relationships (`b06.sub_order.store_id → b03.store`). Cross-schema **writes are not**: only the owning module's role may `INSERT/UPDATE/DELETE` its tables.
- Money schema `b07` gets the tightest grants: `wallet_transaction` and `audit_log` are `SELECT`/`INSERT` only for every app role (see DOC-DB-005 §6).

---

## 2. Prisma 5 — Role and Limits

**Role:** Prisma 5 is the single data-access layer and the migration engine for the whole monolith.

- **One `schema.prisma` with the `multiSchema` preview feature enabled**, each model tagged `@@schema("b0x")`. This keeps one generated client (one type system for the monolith) while preserving physical schema-per-module separation. Module ownership is enforced in review: a PR touching model X must belong to module b0X.
- Models map with `@@map("<table>")` to the singular snake_case names (DOC-DB-001 §1); relations carry `map:` names so FK constraint names match `fk_<table>_<column>`.
- **Migrations:** `prisma migrate dev` in development, `prisma migrate deploy` in CI/prod — workflow in DOC-DB-006 (DATA-REQ-005).
- **Transaction API** (`$transaction`) is mandatory for multi-statement money/order flows (NFR-008, BR-PLT-04); interactive transactions get explicit timeouts (default 5 s raised to 15 s only for order placement).
- **Parameterization:** Prisma's query engine parameterizes all inputs (SEC-REQ-008); raw SQL (`$queryRaw`) is restricted, must use tagged templates, and is flagged in review.

**What Prisma does *not* cover (explicit gaps, each handled deliberately):**

| Gap | Handling |
|---|---|
| Table partitioning (NFR-017) | Prisma has no partition DDL — partitioned tables are created/extended by handwritten SQL inside Prisma migration folders (`migrations/<ts>_partition_order_item/migration.sql`), documented in DOC-DB-006 §6 |
| Generated columns (`inventory.qty_available`) | Same: handwritten SQL in migration files; Prisma model marks the field `@ignore` for writes or maps it read-only |
| `CHECK`/exclusion constraints beyond enums | Handwritten SQL in migrations; Prisma `@relation`/`@unique` cover FK/unique only (DOC-DB-005) |
| UUID v7 defaults | Generated in application code (DOC-DB-001 §2) |
| Row-level security policies | Not used in v1 — ownership is enforced by scoped queries + tests (DATA-REQ-008), with schema privileges as the hard stop |

---

## 3. Connection Pooling (target: 10,000 concurrent users, C-25 / NFR-003)

**Decision: PgBouncer in transaction pooling mode in front of PostgreSQL; Prisma's built-in pool bounded per instance.**

```text
clients → API replicas (stateless, NFR-018) → Prisma pool (connection_limit=N)
        → PgBouncer (transaction mode) → PostgreSQL 16 (max_connections ≈ 200 app + 20 admin/replication)
workers  → BullMQ consumers (C-20) with a separate, small Prisma pool → PgBouncer
```

Sizing model (used as the baseline in load tests, NFR-003):

| Knob | Value | Rationale |
|---|---|---|
| Assumed read RPS at C-25 peak | ≈ 4,000 RPS (10,000 concurrent × ~0.4 req/s user think-time profile) | input to k6 profile; validated by load test |
| p95 DB time per request | < 25 ms hot path | keeps NFR-001 (p95 < 200 ms) achievable with DB share of the budget |
| Prisma `connection_limit` per API replica | 10–15 | `concurrent requests × 1` with headroom; replicas × limit stays under PgBouncer pool |
| PgBouncer `default_pool_size` | 25 per database/user | ≈ `max_connections 200 / (replica count + workers)` headroom formula documented in 14-devops |
| Reserved connections | 10 for migrations/`psql` admin | a deployment never starves DDL or the health probe |
| Transaction mode constraints | no session state: no `SET LOCAL`-dependent features, prepared-statement caching disabled on the Prisma URL (`?pgbouncer=true` legacy flag / statement cache off) | documented so nobody builds a feature on session features |

Rules:

- Every query path must be index-backed (DOC-DB-004); a slow query at this concurrency exhausts the pool long before CPU saturates.
- Pool saturation is an alertable metric (NFR-014): `pgbouncer_pools_server_connections` at 90 % of pool = warning.
- Read scaling path: reporting/analytical reads (B11) go to the **read replica** (NFR-018); money writes always hit the primary; replica lag > 5 s raises an alert (a vendor must not see stale stock).

---

## 4. Environments

| Environment | Database | Notes |
|---|---|---|
| local (dev) | `yumn_dev` on the Compose PostgreSQL 16 (C-22) | `prisma migrate dev` + seed (DOC-DB-006 §5) |
| CI | ephemeral database (service container) | shadow DB for `migrate diff` drift checks (DOC-DB-006 §7) |
| staging | `yumn_staging` — separate cluster/instance, masked data only | load/volume tests (NFR-017), restore drills (DATA-REQ-004) |
| production | `yumn_prod` — separate cluster, no cross-environment credentials (SEC-REQ-007) | WAL archiving + daily snapshots (DATA-REQ-004) |

No shared clusters across environments; migrations always run forward in order (`migrate deploy`), never `migrate dev` against staging/production.

---

## 5. What Lives OUTSIDE PostgreSQL (and why)

| Store | Holds | Why not Postgres | Integrity link to Postgres |
|---|---|---|---|
| **Redis 7** | Cache (NFR-004), BullMQ queues (C-20), rate-limit counters (SEC-REQ-009), OTP resend cooldowns, cart countdown echoes | ephemeral, high-churn, loss-tolerant | **Never a source of truth for money or stock.** Cache is rebuildable; queues are at-least-once with idempotent handlers (INT-REQ-006); losing Redis loses no committed state (NFR-007) |
| **Elasticsearch 8** | Product/search index (FR-009), Arabic analyzer | relevance ranking + faceting at scale | **Not the system of record.** Source rows are `b02.product`; `search_dirty` flag + reindex job rebuild the index from Postgres; on ES outage, browse falls back to Postgres trigram search (NFR-007 — see DOC-DB-004 §4) |
| **MinIO** | Product/review images, KYC document objects (SEC-REQ-011) | object payloads don't belong in rows; ≤5 MB files (BR-CAT-08) | Postgres stores only object **keys** (`product_image.object_key`) + checksums; a cleanup job reconciles keys ↔ objects (DATA-REQ-006) |
| **BullMQ (Redis)** | Scheduled jobs: reservation expiry (C-13), escrow release (C-12), escrow/payout timers, notification fan-out | queue semantics, retries (BR-PLT-01/02) | jobs are triggers only; every effect is a Postgres transaction with an idempotency key (BR-PLT-03) |

Consequence for the schema: **nothing in `b01…b13` stores data whose loss would violate a requirement.** Search index, caches, queues, and image bytes are all reconstructible from Postgres + MinIO.

---

## 6. Backup Posture (pointer)

Backup, WAL archiving, snapshot cadence, encryption at rest, and quarterly restore drills are specified in **DATA-REQ-004** and operationalized in **`14-devops-infrastructure/`** (not in this domain). This domain only guarantees that the schema is *restorable-compatible*: no DDL outside Prisma migrations, no session-dependent state, and restore verification includes the ledger balance assertion (`Σ credits = Σ debits`, BR-PAY-06) per DATA-REQ-004 AC-DR004-03.

Retention of data inside backups follows DATA-REQ-003 (financial/audit rows ≥ 5 years; backups expire on the documented window).

---

## 7. Decision Summary

| # | Decision | Drivers |
|---|---|---|
| DB-D-01 | One PostgreSQL 16 database, 13 schemas `b01…b13` | `C-19`, `C-21`, `DOC-OVR-002`, NFR-008 |
| DB-D-02 | Single Prisma 5 client, `multiSchema` preview, module-owned models | NFR-009, DOC-DB-006 |
| DB-D-03 | PgBouncer transaction pooling; per-replica Prisma `connection_limit` 10–15 | `C-25`, NFR-003, NFR-018 |
| DB-D-04 | Redis/Elasticsearch/MinIO hold only rebuildable or non-row data | NFR-004, NFR-007, DATA-REQ-006 |
| DB-D-05 | Read replica for analytics reads; primary for all money writes | NFR-018, DATA-REQ-007 |
| DB-D-06 | Backup mechanics owned by DATA-REQ-004 + `14-devops-infrastructure/` | DATA-REQ-004, `C-26` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
