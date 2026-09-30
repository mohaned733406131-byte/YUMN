---
document_id: DOC-NFD-003
title: Scalability Detail — Capacity Model, Scaling Levers & Data Growth Path
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-003, NFR-017, NFR-018, NFR-001, NFR-004, NFR-016, FR-018]
related_documents: [DOC-NFD-001, DOC-NFR-003, DOC-NFR-017, DOC-NFR-018, DOC-AC-001, DOC-OVR-008, DOC-NFD-002]
---

# Scalability Detail — Capacity Model, Scaling Levers & Data Growth Path

Elaborates **NFR-003 (concurrency), NFR-017 (storage growth) and NFR-018 (scale-out path)**. Canon fixes the targets (10,000 concurrent per `C-25`; 10M products / 100M order lines; efficiency ≥ 80%); this file adds the derivation model, the lever order under `C-22` (Docker Compose, no Kubernetes), the bottleneck sequence, and the partitioning/sharding path.

## 1. Capacity Model — from "10,000 concurrent" to engineering numbers

All rates below are derived from **stated assumptions** (`INFERENCE`), not canon — they size tests and infrastructure, not commitments.

| Step | Assumption | Result |
|---|---|---|
| 1 | 10,000 *concurrently engaged* users (`C-25`) | baseline VU count for k6 |
| 2 | Each engaged user issues 1 request every 2–4 s (browse/cart mix) | **2,500 – 5,000 req/s** aggregate |
| 3 | 70% reads / 30% writes (`INFERENCE` browse-heavy profile) | 1,750–3,500 read rps · 750–1,500 write rps |
| 4 | ≥ 80% catalog-read cache hit (`NFR-004`) | DB serves ≤ 350–700 read qps (+write path) |
| 5 | Checkout funnel: ≤ 3% of engaged users in checkout simultaneously | ≤ 300 concurrent checkout sessions → order-create writes ≤ 30–90/s peak (`INFERENCE`) |
| 6 | Wallet row-lock critical section ≤ 10 ms (`BR-PAY-05`) | theoretical wallet TPS ≫ required peak; pool/latency become limits first |
| 7 | Images ≈ 35% of bytes, ≥ 60% CDN-served | origin image load ≈ 40–90 rps (`INFERENCE`) |

**Sizing rule:** provision for step-2 peak + 30% headroom; validate with k6 (§6). Assumptions re-derived quarterly from RUM (`DOC-NFD-002` §7).

## 2. Growth Projections (formulas — no fabricated numbers)

Actual commercial forecasts are `GAP-01` (`../../20-validation/core/missing-information.md` — pending). Until resolved, growth is expressed as formulas:

| Quantity | Formula | Inputs to fill |
|---|---|---|
| Orders per day | `orders_day = DAU × conversion_rate × orders_per_user` | DAU, CVR, AOV behavior |
| GMV per month | `GMV = orders_day × 30 × AOV_YER` | AOV (integer YER, `BR-PAY-10`) |
| Order lines (5-yr) | `lines_5y = orders_day × 365 × 5 × lines_per_order` — must stay ≤ **100,000,000** (`NFR-017`) | lines_per_order |
| Products (5-yr) | `products_5y = base_catalog + vendors_month × products_per_vendor × months` ≤ **10,000,000** (`NFR-017`) | vendor growth |
| Storage/day | `storage_day = lines_day × bytes_line + images_day × bytes_image + events_day × bytes_event` | schema row widths |
| Peak-day multiplier | `peak = 1 + promo_lift + seasonality_lift` (Eid/Ramadan campaigns) | `INFERENCE` |
| Concurrency trajectory | `VUs_next = VUs_current × (1 + growth_30d)`; scale-test trigger at **> 30% growth** (`NFR-018`) | RUM |

Each formula is exercised with sponsor inputs at Gate 0 (`ASM-14`) and re-run quarterly; **forecast vs actual disk variance ≤ 10%** (`AC-NFR-017-02`).

## 3. Scaling Levers Under `C-22` (Docker Compose only — no Kubernetes)

Available levers (in the order they are applied):

| # | Lever | What it buys | Configuration notes |
|---|---|---|---|
| L1 | **Vertical host upgrade** (CPU/RAM/disk) | first, cheapest-in-ops step on a single host | monitor §4 thresholds before acting |
| L2 | **Stateless API replicas** (same image, N containers behind the Compose-managed LB/nginx) | horizontal read+write throughput; `NFR-018` requires 0 in-process session state | scaling efficiency ≥ 80% at 1→4 replicas (`AC-NFR-018-01`) |
| L3 | **Connection pooling** (PgBouncer) | protects PostgreSQL from replica fan-out | pool < 80% util; wait p95 ≤ 50 ms (`DOC-NFD-002` §4) |
| L4 | **Redis** (cache + sessions + BullMQ backing) | absorbs read amplification (≥ 80% hit, `NFR-004`) | maxmemory policy with TTL discipline; non-TTL keys not evicted under load (`AC-NFR-004-01`) |
| L5 | **BullMQ worker replicas** | decouples async work (notifications, reconciliation, exports) from request path | queue names `{block}.{entity}.{action}` (`BR-PLT-01`); drain ≤ 5 min (`AC-NFR-003-02`) |
| L6 | **PostgreSQL read replicas** | reporting/analytics/search indexing off the primary (`FR-018`) | lag < 5 s under load (`AC-NFR-018-01`); never read-your-writes paths (wallet/checkout use primary) |
| L7 | **Elasticsearch offload** | search traffic out of SQL; Arabic analyzer (`FR-009`) | degraded mode = DB/browse fallback (`NFR-007`) |
| L8 | **CDN/edge** (images, ISR catalog pages) | origin offload for static/media | `DEP-08`; money routes never edge-cached |
| L9 | **Partitioning + retention** (§5) | keeps single-node write path within budget at 100M rows | `NFR-017` |
| L10 | **Sharding by tenant key** (§5.3) | beyond-Compose ceiling — documented as a *future* path, not v1 | requires ADR before adoption (`18-decisions/`) |

No lever introduces microservices (`C-21`), Kubernetes (`C-22`) or a second database (`C-19`).

## 4. What Scales First — Bottleneck Order (expected)

Verified by the reference load run; alerts are configured against this order (`DOC-NFD-006`):

| Order | Bottleneck | Early warning signal | Primary response |
|---|---|---|---|
| 1 | **PostgreSQL write path** (row locks on wallets/stock, WAL, commit latency) | write p95 > 400 ms; lock wait p95; pool util ≥ 80% | L3 pool tuning → L6 read offload for non-critical reads → L1 vertical |
| 2 | **Redis** (memory, single-thread saturation, eviction pressure) | hit ratio < 80%; evictions/min > 0 for non-TTL; Redis CPU > 70% | key-size/TTL audit → L1 → shard-by-role split (cache vs queue instances) |
| 3 | **Elasticsearch** (heap, thread pools, indexing contention) | search p95 > 200 ms; ES thread-pool rejected > 0 | reduce suggestion traffic (`DOC-NFD-002` §8) → L7 sizing → dedicated data nodes |
| 4 | API host CPU / event loop lag | CPU ≥ 70%, p95 inflation without DB signals | L2 replicas |
| 5 | BullMQ backlog | queue depth ↑, DLQ depth > 0 | L5 workers; shed marketing jobs first |
| 6 | Object storage / CDN | origin image p95 > 300 ms | L8 cache rules, image variants |

Rationale: marketplace write paths are serialized by correctness rules (`BR-PAY-05`, `BR-CAT-07`) before compute becomes scarce — which is why DB writes are expected to bind first.

## 5. Data Growth Path (NFR-017)

### 5.1 Volume targets & partitioning

| Table (top 3 by volume) | 5-year horizon | Plan |
|---|---|---|
| Order lines | 100,000,000 rows | **monthly partitions**; retention drops partitions (never row-by-row delete) |
| Ledger entries | grows with every money event | monthly partitions; append-only (`DATA-REQ-007`), never updated |
| Order status history | 17-state machine × orders (`BR-ORD-03`) | monthly/quarterly partitions; 5-year retention |
| Notifications, audit log (secondary) | high write, slower read | quarterly partitions; audit ≥ 5 years (`NFR-019`) |

Products (10M) and users are **not** partitioned in v1 — indexed B-trees suffice; revisit at 25% of target (`INFERENCE` trigger).

### 5.2 Retention & safety

- Financial/audit records: **5-year floor** (`DATA-REQ-003`, `NFR-019`); retention job dry-run must prove **0** in-window rows deleted (`AC-NFR-017-02`).
- Archive before drop; disk alert at 70% capacity; forecast variance ≤ 10%/quarter.

### 5.3 Sharding path (documented, not v1)

1. Precondition: L2/L6/L9 exhausted and write p95 still in breach for 2 consecutive load runs.
2. Candidate key: `store_id`-preserving **hash sharding of orders/ledger** by order-id range, keeping wallets global (single-ledger invariant `BR-ESC-08` requires global reconciliation).
3. Requires: ADR (`18-decisions/core/`), dual-write-free expand-contract migration (`DATA-REQ-005`), reconciliation job re-design, and re-run of `AC-NFR-008-*`.
4. Explicitly **out of v1 scope**; recorded so growth is never improvised (`NFR-018` "documented path").

## 6. Load-Test Acceptance (k6)

| Test | Profile | Pass criteria | AC |
|---|---|---|---|
| Reference mixed run | 10,000 VUs, ramp 5 min, hold 30 min, browse-cart-pay mix | NFR-001 p95s hold; errors < 0.1% for whole window | `AC-NFR-003-01`, `AC-NFR-001-01/02` |
| Resource headroom (same run) | Prometheus 15 s samples | CPU < 70%, mem < 75%, pool < 80%, queue drain ≤ 5 min | `AC-NFR-003-02` |
| Scaling curve | fixed VUs at 1 / 2 / 4 API replicas | efficiency ≥ 80% (4-replica throughput ≥ 3.2× single) | `AC-NFR-018-01` |
| Replica kill | mid-load kill of 1 API replica | LB drains ≤ 30 s; 0 failed sessions; errors < 0.1% | `AC-NFR-018-01`, `AC-XCUT-04` |
| Read-replica lag | reporting load on replica | lag < 5 s; checkout p95 unaffected | `AC-NFR-018-01` |
| Volume test | 10M products + 100M order lines bulk-loaded | p95 within NFR-001; 0 unexpected seq scans on hot paths | `AC-NFR-017-01` |
| Partition/retention review | SQL inspection + dry-run | 3 tables partitioned; 5-y protection proven; variance ≤ 10% | `AC-NFR-017-02` |
| Runbook rehearsal | 10k → 50k steps | steps published, on-call reviewed, validated ≥ 25k step | `AC-NFR-018-02` |

## 7. Scale-Out Runbook Skeleton (10k → 50k, per NFR-018)

| Step | Action | Capacity gained (est., `INFERENCE`) | Validation |
|---|---|---|---|
| 0 | Baseline reference run (10k) | proof of v1 gate | §6 row 1–2 |
| 1 | Add API replicas 1 → 2 → 4 | ~1.9× / ~3.2× throughput | scaling curve, replica-kill |
| 2 | Tune pool sizes (PgBouncer max, ES threads) | removes wait p95 ceiling | pool < 80% at 2× load |
| 3 | Enable read replica; route reporting (`FR-018`) | frees primary 10–20% | lag < 5 s |
| 4 | Redis: raise memory / split cache vs queue instances | restores ≥ 80% hit ratio | hit-ratio dashboard |
| 5 | ES: add data node / adjust shards | search stays < 200 ms | search p95 |
| 6 | Add BullMQ workers 1 → N | drain time ≤ 5 min | queue depth dashboard |
| 7 | Host vertical step (L1) | remaining CPU headroom | CPU < 70% |
| 8 | Re-run reference profile at each step; stop when all gates hold | acceptance at 25k/50k | §6 |

Every step is rehearsed in staging to at least the 25k step before publication (`AC-NFR-018-02`); the runbook is owned with `NFR-020` runbooks (`DOC-NFD-004` §8).

## 8. Verification Hooks

`AC-NFR-003-01/02` (concurrency) · `AC-NFR-017-01/02` (volume/partitioning) · `AC-NFR-018-01/02` (scale-out) · supporting `AC-NFR-001-*`, `AC-NFR-004-*`, `AC-S-05`. Test execution plans live in `13-testing/`; infra sizing in `14-devops-infrastructure/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
