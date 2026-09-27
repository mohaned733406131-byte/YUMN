---
document_id: DOC-ARCH-008
title: Scalability
category: 04-architecture
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-003, NFR-004, NFR-017, NFR-018]
related_documents: [DOC-OVR-008, DOC-ARCH-003, DOC-ARCH-005, DOC-ARCH-007, DOC-REQ-001]
---

# Scalability

How the architecture meets `C-25` (**10,000 concurrent users**) while keeping `NFR-001` latency targets, and how it grows beyond that **without Kubernetes** (`C-22`) via the documented scale-out path of `NFR-018`. Measurement is by load tests (`k6`, `NFR-003`); targets are owned by `12-non-functional/`.

## 1. Target Decomposition

| Target | Source | Architectural answer |
|---|---|---|
| 10,000 concurrent users sustained within latency SLOs | `C-25`, `NFR-003` | Stateless API replicas + Redis cache + ES offload + worker isolation |
| p95 < 200 ms read / < 500 ms write | `NFR-001` | Cache hit paths, indexed queries, async side effects |
| Catalog cache hit ratio ≥ 80% | `NFR-004` | Redis read-through on product/category/banner reads |
| 10M products, 100M order-line records, 5-year retention | `NFR-017` | Index strategy + partitioning plan (§6) |
| Documented path beyond `C-25` | `NFR-018` | Read replicas, more replicas, partitioning — all Compose-compatible |
| No K8s in v1 | `C-22` | Horizontal scaling = `docker compose up --scale api=N` behind the edge |

**Load model (`INFERENCE`, to be validated by k6):** 10,000 concurrent sessions ≈ 1,000–2,000 req/s at typical browse ratios (mostly reads, ~80/20 read/write), burst multiplier 3×. Writes concentrate in checkout, wallet and delivery windows.

## 2. Levers, in Order of Use

| # | Lever | What it does | Where configured | IDs |
|---|---|---|---|---|
| L1 | Read caching (Redis) | Removes repeat catalog/content reads from the database | `data-flow.md` §3 | `NFR-004` |
| L2 | Search offload (Elasticsearch) | Complex queries/aggregations never hit PostgreSQL | `ADR-006` | `FR-009`, `NFR-001` |
| L3 | Async offload (BullMQ workers) | Notifications, indexing, reconciliation, timers never occupy request threads | `C-20`, `BR-PLT-01` | `NFR-001` |
| L4 | Stateless API replicas | Linear request-capacity growth by adding replicas | `deployment-view.md` | `NFR-018` |
| L5 | Connection pooling | Bounded PostgreSQL connections per replica; prevents connection storms | pool config in API/worker | `NFR-003` |
| L6 | Edge caching/CDN | Static + anonymous pages served off-origin | `DEP-08` | `NFR-002` |
| L7 | Index & query discipline | Covering indexes, pagination, no N+1 in hot paths | `08-database/` | `NFR-001` |
| L8 | Vertical scaling | Bigger host for PostgreSQL/Redis/ES within a Compose host | `deployment-view.md` | — |
| L9 | Read replicas | Read scaling for reports/feeds when L1–L7 are exhausted | §6 | `NFR-018` |
| L10 | Partitioning | Keeps hot tables small under 100M-row growth | §6 | `NFR-017` |

## 3. Read Scaling Path

```text
Client ─► Edge ─► [api ×N stateless replicas] ─┬─► Redis (cache hit → reply, ~80% catalog reads)
                                               ├─► Elasticsearch (search/facets)
                                               └─► PostgreSQL (misses, writes)
                                                        │
                                                 (future) read replicas for
                                                 analytics/feeds — §6, NFR-018
```

- **Why reads scale cheaply:** the hottest surfaces (browse, PDP, banners) are cache- or index-served; search aggregations live in ES; the storefront is SSR/static at the edge.
- **Consistency:** cache entries are invalidated on write in the same request; read replicas are only introduced for *lag-tolerant* reads (reports, feeds) — never for balance or checkout decisions (`INFERENCE`, required by `NFR-008`).
- **Writes stay on primary:** money, stock and order writes are low-volume relative to reads and are protected by pooling + locks (L5).

## 4. Concurrency Safety Under Load (scale ≠ race)

| Risk at scale | Countermeasure | IDs |
|---|---|---|
| Oversell storms on flash items | 15-min reservations + atomic deduction serialize contention at the row | `C-13`, `BR-CAT-07` |
| Wallet drain attempts | Row-level locking with balance check; idempotency absorbs retries | `BR-PAY-05/08` |
| Duplicate transitions | Optimistic version checks; losers get conflict, not corruption | DOC-SA-010 §5 |
| Queue floods (notification bursts) | Worker replicas scale independently; backpressure via queue depth metrics | `BR-PLT-01/02`, `NFR-014` |
| Rate-limit hotspots | Per-IP and per-user counters in Redis (shared across replicas) | `SEC-REQ-009` |

## 5. Identifying the Bottleneck (what breaks first, and the response)

| Symptom | Likely bottleneck | Response (no code change) | Response (code/config) |
|---|---|---|---|
| p95 read latency ↑, cache hit < 80% | Redis memory/eviction or cold cache | Vertical Redis; verify invalidation churn | Tune TTLs, increase Redis memory (`NFR-004`) |
| Database CPU ↑ / connections waiting | PostgreSQL saturation | Vertical host; add API replicas won't help | Pool sizing, query/index review (L5, L7) |
| Search latency ↑ | Elasticsearch single node | Vertical ES | Offload more aggregations; shard sizing (L2) |
| Worker backlog grows | Worker capacity | `--scale worker=N` | Split queues; tune retries (`BR-PLT-02`) |
| Write p95 ↑ near SLO | Lock contention on hot rows | Reduce lock scope via batching | Shorter transactions; hot-row splitting (`INFERENCE`) |
| Edge saturation | Static traffic | CDN absorbs | Longer edge TTLs (L6) |

Instrumentation for these decisions comes from RED metrics per endpoint and queue-depth/DLQ gauges (`NFR-014`, `INT-REQ-007`).

## 6. Growth Path Beyond `C-25` (still no K8s, `C-22` / `NFR-018`)

| Stage | Trigger | Changes | Stays the same |
|---|---|---|---|
| S1 — Today | ≤10k concurrent | 1× each data service; N× API/worker replicas | Compose topology |
| S2 — Read replicas | Reports/feeds crowd reads | Add `postgres` read-replica service; route analytics/feeds via replica DSN | Writes on primary; module code unchanged |
| S3 — Partitioning | Order-line/ledger history near `NFR-017` bounds | Range partitioning by month on high-growth tables; retention archival of >5-year data | Schema (expand-contract migrations, `DATA-REQ-005`) |
| S4 — Data vertical + ES cluster | Data-tier CPU/disk pressure | Bigger host; multi-node ES (`INFERENCE`) | Single PostgreSQL primary (`C-19`) |
| S5 — Read-path expansion | S2–S4 insufficient | Additional cache nodes; edge expansion; queue sharding by consumer groups | BullMQ only (`C-20`) |
| S6 — Beyond Compose ceiling | Multi-host requirement | Documented hand-off: same containers on multi-host orchestrator — **a v2 decision, out of scope now** | No rewrite; containers unchanged |

**Explicit non-levers:** microservices split (`C-21`), a second database (`C-19`), Kafka/RabbitMQ (`C-20`), Kubernetes (`C-22`) are all excluded for v1; any proposal to use them is a constraint change requiring change management (root README §9), not an architecture tweak.

## 7. Verification

| Check | Method | ID |
|---|---|---|
| 10k concurrency holds latency SLOs | k6 load test on staging, mixed scenario (browse/search/cart/checkout) | `NFR-003` |
| Cache hit ≥ 80% on catalog reads | Redis metrics during load test | `NFR-004` |
| No oversell/negative balance under load | Concurrency test suite (edge cases `EC-02`, `EC-06`, `EC-19`) | `C-13`, `BR-PAY-05` |
| Worker keeps up with burst | Queue-depth graphs at 3× burst | `BR-PLT-02` |
| Replicas add capacity linearly | Scale `api` from 1→N, measure throughput | `NFR-018` |
| Read-replica lag tolerated only where allowed | Architecture test on read paths | `NFR-008` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
