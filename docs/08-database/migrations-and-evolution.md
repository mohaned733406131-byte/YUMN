---
document_id: DOC-DB-006
title: Migrations and Schema Evolution
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-005, NFR-020, NFR-009, NFR-017]
related_documents: [DOC-DB-001, DOC-DB-002, DOC-DB-005, DOC-OVR-008]
---

# Migrations and Schema Evolution

**Governing requirement:** DATA-REQ-005 — *expand-contract migrations; backward-compatible deploys* (NFR-020 zero-downtime deploys). Prisma Migrate is the only tool that changes the schema; handwritten SQL is allowed only **inside** Prisma migration folders (partitioning, generated columns, partial indexes, triggers — DOC-DB-002 §2).

---

## 1. Workflow

```text
1. branch:     feat/<ticket>            (one schema change set per PR)
2. develop:    npx prisma migrate dev --name <descriptive_name>
               → creates migrations/<timestamp>_<name>/migration.sql
               → applies to local yumn_dev + regenerates client
3. review:     PR must include migration.sql (human-readable), impact notes,
               expand/contract classification, and EXPLAIN evidence if queries change
4. CI gate:    validate → drift check → shadow-DB up migrate → down-order check → app tests
5. deploy:     prisma migrate deploy        (forward-only, in order, never prompts)
6. verify:     post-deploy smoke: constraint-presence tests + health endpoints (BR-PLT-07)
```

Branching model: **migration files live on the same feature branch as the code that needs them** — no long-lived `migration` branch, no hand-merging of timestamped folders. Two PRs touching the same tables must rebase and regenerate so timestamps order correctly (CI fails on out-of-order or duplicate timestamps).

---

## 2. Forward-Only in Production

- Production runs **`prisma migrate deploy` only**. `migrate dev` (which may reset/repair) is forbidden outside local dev (DOC-DB-002 §4).
- **No `migrate down` in production.** "Rollback" of a bad migration is a **forward fix**: a new migration that reverses the change safely within the expand/contract pattern (§4). Dev-only `migrate reset` exists for local re-seeding.
- Each migration folder may contain an optional `migration_down.sql` kept in-repo **for documentation/dev use only**; CI asserts it is never referenced by any deploy pipeline.
- Migrations are idempotent-safe by ordering: `migrate deploy` records applied history in `_prisma_migrations`; a failed migration leaves the database on the last good version and the deploy job halts (no partial rollout past the failed step).

---

## 3. Expand/Contract Pattern (DATA-REQ-005, NFR-020)

Every breaking change ships as **two or three releases**, never one:

| Phase | Release | Schema | App code |
|---|---|---|---|
| **1. Expand** | release N | additive: new nullable column / new table / new index `CONCURRENTLY` / new enum value (`ADD VALUE`) | still writes old shape; **dual-writes** new column when both exist |
| **2. Migrate** | release N+1 | backfill in batches (chunked `UPDATE … WHERE id IN (SELECT … LIMIT 1000)` job, throttled; no long locks) | reads/writes new shape; old column kept in sync if risk is high |
| **3. Contract** | release N+2 (only after N+1 is stable & metrics clean) | removal/rename/NOT NULL tighten: drop old column, drop old enum value (requires recreate for PG enums — done via table rewrite in a maintenance window only if unavoidable) | no references to old shape |

Concrete examples for yumn:

| Change | Expand | Contract |
|---|---|---|
| Rename `stores.hub_location` → structured fields | add `hub_governorate_code`, `hub_district` nullable; dual-write | drop `hub_location` |
| Tighten `NOT NULL` on a legacy nullable column | add as nullable → backfill → `ALTER COLUMN … SET NOT NULL` + `VALIDATE CONSTRAINT` (non-blocking in PG 16) | — |
| Add a new order state | `ALTER TYPE order_state ADD VALUE 'X'` (canon change to `C-09`/`DOC-SA-010` required first) | n/a |
| Replace a CHECK expression | `ADD CONSTRAINT` new → `VALIDATE` → `DROP CONSTRAINT` old | both never overlap on failure |
| Drop an index | create replacement index **first** (`CREATE INDEX CONCURRENTLY` via raw SQL in migration) | drop the old one |

Rules that make this zero-downtime (NFR-020):

- **Additive DDL first.** `ALTER TABLE … ADD COLUMN … NULL` without default is metadata-only in PG 16; with a constant default it is also non-rewriting (PG 11+). Column rewrites are never done inline.
- `CREATE INDEX CONCURRENTLY` for any index on a table with data (Prisma emits plain `CREATE INDEX` — the migration file is edited to use `CONCURRENTLY` + `AND NOT EXISTS` guard); review enforces this.
- No `ALTER TYPE … RENAME` / `DROP VALUE` (not supported / locks) — enum contraction uses expand/contract table rebuild in a window, or leaves the value dormant.
- Application code from release N must run unchanged against schema N+1 (backward-compatible queries) — that is what makes rolling deploys safe with a shared database (C-22 Docker Compose, rolling container replacement).

---

## 4. Seed & Reference Data

Seeds are **versioned migration data**, not scripts run by hand.

| Data | Schema | Where |
|---|---|---|
| Category tree (roots + level structure, bilingual names) | `b02.category` | seed migration `seed_initial_categories` (BR-CAT-03; positions stable) |
| Governorates (Yemen, bilingual) | `b01.governorate` | `seed_governorates` (reference for addresses + zones) |
| Shipping zones + base rates | `b08.shipping_zone`, `b08.shipping_rate` | `seed_shipping_zones` (BR-SHP-01, C-17 domestic only) |
| Platform settings (VAT rate 15 %, escrow days 7, payout min 1,000, return defaults) | `b13.platform_setting` | `seed_platform_settings` — values must match canon (`BR-FIN-01`, `C-12`, BR-ESC-05); changing a setting is a config change, not code (mirrors DATA-REQ-003 R1 philosophy) |
| Admin roles for bootstrap Super Admin | `b01.user`, `b01.user_role` | `seed_bootstrap_super_admin` — **credentials injected at deploy via environment, never in SQL** (SEC-REQ-007) |
| Notification template keys | `b10.notification` reference enum/`template_key` usage | template registry validated in tests against BR-NTF-04 (ar + en parity) |

Rules: seeds use explicit IDs (UUIDs pinned in the migration) so FKs from later data are stable; seeds are **idempotent** (`ON CONFLICT DO NOTHING`); product/store/order demo data is a separate `db/seed-dev.ts` (dev only, never deployed — DATA-REQ-002: no fake PII patterns in prod).

---

## 5. Migration CI Checks (gates)

| # | Gate | Fails when |
|---|---|---|
| M1 | `prisma validate` | schema.prisma syntax/preview-feature error |
| M2 | **Drift check**: `prisma migrate diff --from-migrations migrations/ --to-schema-datamodel schema.prisma --exit-code` | DB state ≠ migration history (someone changed prod by hand, or a migration is missing) |
| M3 | Shadow-DB replay: apply all migrations from scratch to an empty PostgreSQL 16 | any migration fails / non-deterministic SQL |
| M4 | **Destructive-change scan** on `migration.sql`: flags `DROP TABLE`, `DROP COLUMN`, `SET NOT NULL` without expand phase, `ALTER TYPE … DROP`, plain `CREATE INDEX` on non-empty tables | pattern found without a `contract:` label in the PR |
| M5 | Out-of-order timestamp check | two branches produced interleaved migration timestamps |
| M6 | Constraint-presence tests (DOC-DB-005 §8) | a named `ck_/uq_/fk_` disappeared |
| M7 | App test suite (unit + integration) against migrated DB | behavior broke (NFR-010) |
| M8 | Seed idempotency: run seed migrations twice | second run changes row counts |
| M9 | Partition rehearsal: partition-maintenance job dry-run in CI | next-month partitions missing for partitioned tables (NFR-017) |

---

## 6. Handwritten SQL Inventory (allowed exceptions)

| Concern | Why Prisma can't express it | File convention |
|---|---|---|
| Partition creation/maintenance (`order_item`, `wallet_transaction`, `order_status_history`, `audit_log`) | no partition DDL in Prisma | `migration.sql` with `CREATE TABLE … PARTITION BY RANGE` or `CREATE INDEX … ON … ()` + `ATTACH/CREATE DEFAULT PARTITION` statements (NFR-017) |
| Generated column `inventory.qty_available` | no `GENERATED ALWAYS AS` support | one-time `ALTER TABLE` in the inventory migration |
| `pg_trgm` extension + GIN indexes for search fallback | extension support limited | `CREATE EXTENSION IF NOT EXISTS pg_trgm;` (DOC-DB-004 §4) |
| Deferrable constraint triggers T2/T3, `updated_at` triggers T1 | no trigger support | `DO $$ … $$` blocks (DOC-DB-005 §6) |
| `REVOKE UPDATE, DELETE` on append-only tables; per-module role grants | no privilege modeling | `GRANT/REVOKE` in the migration that creates each table + a central `grants.sql` applied after migrate deploy (DOC-DB-005 §7) |
| Partial/compound indexes with expressions Prisma can't map | partial index predicates unsupported | plain SQL, kept in sync with DOC-DB-004 |

Every handwritten block carries a comment `-- HANDWRITTEN: <reason>` so the drift check and reviewers can find it.

---

## 7. Rollback Approach (by failure class)

| Failure | Response |
|---|---|
| Migration fails mid-deploy | deploy job stops at failed step; DB remains at last good version; fix → new forward migration; no data loss (failed statement is transactional per migration file) |
| Migration applies but app misbehaves (N+1 of expand/contract) | **roll back the app containers only** — schema stays (it is backward compatible by §3 design); this is the core benefit of expand/contract |
| Bad data written by new code | compensating migration / data-repair script reviewed like code; ledger repairs are compensating entries only (DATA-REQ-007), never UPDATE |
| Truly broken DDL needing reversion | forward migration reversing it (contract-phase style); dev-only `migration_down.sql` as a reference, never executed in prod (§2) |
| Worst case | restore from PITR (DATA-REQ-004: WAL, RPO ≤ 15 min) + replay forward migrations — documented runbook in `14-devops-infrastructure/` |

---

## 8. Operational Constraints Checklist (per migration PR)

- [ ] Classification: `expand` / `data-fix` / `contract`
- [ ] No table rewrite; no lock held > 1 s (checked with `pg_locks` capture in staging timing test)
- [ ] Indexes on populated tables use `CONCURRENTLY`
- [ ] Backfill is chunked, resumable, and emits progress metrics (NFR-014)
- [ ] Old app version still works against new schema (rolling deploy window, C-22)
- [ ] New schema works with old app version (same window)
- [ ] ENUM changes add values only (or carry an expand/contract table plan)
- [ ] Partitioned tables: next partition created before deploy
- [ ] Grants for new tables included (`app_b0x` roles)
- [ ] DOC-DB-004/DOC-DB-005 updated if indexes/constraints changed; entity doc bumped with `version` + Change History (root README §9)

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
