---
document_id: DOC-NFD-002
title: Performance Detail — Latency Budgets, Tooling & Degradation Under Load
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-002, NFR-003, NFR-004, NFR-015, FR-009, FR-010, FR-011, FR-013]
related_documents: [DOC-NFD-001, DOC-NFR-001, DOC-NFR-002, DOC-NFR-004, DOC-AC-001, DOC-OVR-008, DOC-FE-009]
---

# Performance Detail — Latency Budgets, Tooling & Degradation Under Load

Elaborates **NFR-001 (API response time), NFR-002 (client performance) and NFR-004 (caching)**. Requirement statements stay in `02-requirements/`; this file adds the sub-budgets, per-surface splits, tooling and load-shedding policy that make those statements operable. Acceptance remains `AC-NFR-001-01/02`, `AC-NFR-002-01/02`, `AC-NFR-004-01/02` at the 10,000-user gate (`C-25`, `AC-S-05`).

## 1. Latency Budgets — API (server-side, measured at the gateway)

All values hold during the reference k6 run (10,000 VUs, 30-min steady state) unless marked `INFERENCE`.

| Endpoint class | Examples | p50 | p95 (gate) | p99 (secondary) | Source |
|---|---|---|---|---|---|
| Reads — catalog | product, category, store, banner | ≤ 40 ms | **< 200 ms** | ≤ 400 ms | NFR-001 |
| Reads — search | query + facets + sort | ≤ 60 ms | < 200 ms | ≤ 400 ms | NFR-001 |
| Reads — account | orders list, order detail, wallet balance, transactions | ≤ 40 ms | < 200 ms | ≤ 400 ms | NFR-001 |
| Writes — cart | add/update/remove (reservation refresh) | ≤ 80 ms | **< 500 ms** | ≤ 1,000 ms | NFR-001 |
| Writes — checkout/order create | 7-step confirm (saga: stock + wallet + escrow + sub-orders) | ≤ 250 ms | < 500 ms | ≤ 1,000 ms | NFR-001 |
| Writes — wallet | top-up credit, payment, refund | ≤ 150 ms | < 500 ms | ≤ 1,000 ms | NFR-001 |
| Writes — admin/vendor | KYC decision, settings, listings, moderation | ≤ 120 ms | < 500 ms | ≤ 1,000 ms | NFR-001 |
| Auth | login, OTP verify | ≤ 120 ms (excl. SMS delivery) | < 500 ms | ≤ 1,000 ms | NFR-001 |
| Health | `/healthz`, `/readyz` | — | **< 1 s** (probe target < 100 ms `INFERENCE`) | — | NFR-020 |

Error budget during the run: **< 0.1%** 5xx+timeouts across all classes (`AC-NFR-001-01/02`).

## 2. Latency Budgets — Client-Facing (perceived)

| Metric | Customer web (S1) gate | Vendor panel (S2) / Admin (S3) | Customer app (S4) / Courier (S5) |
|---|---|---|---|
| LCP | **< 2.5 s** on simulated 4G, mid-tier mobile | < 3.5 s informational | first meaningful paint < 2.0 s (`INFERENCE`) |
| INP | ≤ 200 ms | ≤ 250 ms (`INFERENCE`) | frame time ≤ 16 ms on list scroll (`INFERENCE`) |
| CLS | ≤ 0.1 | ≤ 0.1 | ≤ 0.1 |
| TTFB (cached/ISR) | < 500 ms edge | < 500 ms | n/a (API per §1) |
| Initial JS | **< 200 KB gzipped** per route entry; no vendor chunk > 100 KB | < 350 KB gzipped (`DOC-FE-009` §2) | JS bundle < 300 KB (`INFERENCE`, Hermes) |
| Fonts | Arabic + Latin ≤ **150 KB** combined, `font-display: swap` | same subset shared | bundled, no runtime fetch |
| Route navigation (client) | < 300 ms to interactive on catalog routes | < 400 ms (`INFERENCE`) | screen transition ≤ 250 ms (`INFERENCE`) |

Gates run per page per locale (home, category, product, checkout) — `AC-NFR-002-01/02` fail the pipeline on breach.

## 3. Throughput Assumptions (feeds load-test design — `INFERENCE`)

| Assumption | Value | Basis |
|---|---|---|
| Concurrent user model | 10,000 engaged users, each issuing 1 request every 2–4 s | derived engagement rate for browse/cart mix — stated assumption, not canon |
| Aggregate request rate | **2,500 – 5,000 req/s** peak | 10,000 ÷ (2…4 s) |
| Read/write split | ~70% reads / ~30% writes | browse-heavy marketplace profile |
| Read rate reaching DB | ≤ 20% of read requests after cache (≥ 80% hit, NFR-004) → **350 – 700 queries/s** DB reads | cache absorption model |
| Search share | ~15% of reads, of which ~40% are suggestions-as-you-type | `INFERENCE` |
| OTP burst profile | registration peaks 10–20 OTP requests/s (campaign/launch) | `INFERENCE`; `SEC-REQ-009` buckets bound abuse |
| Image traffic | ~35% of page bytes; 60% served from CDN cache (`INFERENCE`) | product-image-dominant pages |

These assumptions are **test-profile inputs only**; they are not commitments. Re-derive quarterly from RUM data (§7).

## 4. Server-Side Component Budgets

| Component | Budget | Gate basis |
|---|---|---|
| PostgreSQL — indexed read query p95 | ≤ 25 ms | keeps API p95 < 200 ms with headroom (`INFERENCE` split) |
| PostgreSQL — write transaction p95 (wallet/order) | ≤ 80 ms incl. commit | `INFERENCE` |
| Connection pool (PgBouncer) | utilisation < 80%; pool wait p95 ≤ 50 ms | `AC-NFR-003-02` |
| Redis cache-hit response p95 | **< 50 ms** | `AC-NFR-004-01` |
| Cache staleness (price/stock/visibility) | ≤ 5 s everywhere; checkout never uses cache older than 5 s | `AC-NFR-004-02` |
| Catalog cache hit ratio (24 h) | **≥ 80%** on product/category/store reads | `AC-NFR-004-01` |
| Search (ES) query p95 | ≤ 80 ms incl. Arabic analysis (`INFERENCE`) | keeps search class inside 200 ms |
| BullMQ | enqueue p95 ≤ 50 ms; drain to baseline ≤ 5 min after load run | `AC-NFR-003-02` |
| API host | CPU avg < 70%, memory < 75% during reference run | `AC-NFR-003-02` |

## 5. Per-Surface Performance Rules (design ↔ budget)

| Surface | Critical path | Budget owner rule |
|---|---|---|
| S1 customer web | home → PDP → cart → checkout → confirm | LCP/INP/CLS gates (§2); money routes never ISR-cached (`DOC-FE-002` §4) |
| S2 vendor panel | order inbox → accept → fulfill | CSR dashboards; charts lazy-loaded; tables paginate ≤ 50 rows |
| S3 admin console | queue → decision (KYC/dispute/refund) | decision round-trip (click → confirmed) < 1 s (`INFERENCE`); no blocking modals on slow queries |
| S4 customer app | list scroll, cart, wallet refresh | wallet balance refetch ≤ 200 ms visible; pull-to-refresh always available |
| S5 courier app | queue refresh → accept → code entry | accept round-trip < 1 s (race sensitivity, `BR-SHP-04`); code verify < 500 ms |

## 6. Measurement Tooling

| Tool | What it measures | When | Evidence |
|---|---|---|---|
| **k6** reference scenarios (read-heavy, write-heavy, mixed browse-buy) at 10,000 VUs / 30 min | NFR-001 + NFR-003 gates | release candidate; before major releases; after > 30% traffic growth | JSON summary → `13-testing/` release report (`AC-S-05`) |
| k6 smoke profile (500 VUs / 5 min) | regression on every deploy to staging | per deploy | CI artifact |
| **Lighthouse CI** (mobile, 4G throttle) on 4 pages × 2 locales | NFR-002 gates | every PR | CI artifact (`AC-NFR-002-01`) |
| **size-limit / bundlesize** | gzipped entry bundle + fonts | every PR | build fails on breach (`AC-NFR-002-02`) |
| Prometheus RED histograms (15 s scrape) + Grafana | live p50/p95/p99 per endpoint class (§1) | continuous | dashboards (`DOC-NFD-006`) |
| Web Vitals RUM (5% sample) | p75 LCP/INP/CLS by locale/device/route | post-launch continuous | Prometheus export |
| RN perf monitors (React DevTools profiler, FrameMetrics/`InteractionManager`) | list jank, screen transition time, JS bundle size | on PR touching hot paths + pre-release device-lab pass | test notes |
| Redis `INFO stats` + `cache_requests_total` | hit ratio & staleness probes | 24 h windows | `AC-NFR-004-01/02` |
| EXPLAIN (ANALYZE, BUFFERS) on 20 hottest queries | query-plan regressions at volume | volume test (see `DOC-NFD-003` §6) | `AC-NFR-017-01` |

## 7. Profiling & Review Cadence

| Activity | Cadence | Output |
|---|---|---|
| Slow-endpoint review (p95 > 80% of budget) | weekly (ops) | Grafana annotation + ticket if trending |
| Full k6 reference run (10k) | per release candidate + quarterly | release report section |
| Flame-graph/CPU profile of API hot paths | monthly, or after any budget breach | optimization backlog entry |
| Frontend bundle budget review | every PR (automated) + monthly manual audit | size report |
| RUM p75 review | monthly | budget re-baseline proposals (change via this file, version bump) |
| Assumption re-derivation (§3) | quarterly | updated test profile |
| Database slow-query log review | weekly | index/tuning backlog |

## 8. Degradation Policy Under Load (shed non-critical work first)

When any §1/§4 budget is breached for 2 consecutive minutes, shed load in this **fixed order** (never shed money correctness — `NFR-008`):

| Priority | Work shed | Mechanism | User-visible effect |
|---|---|---|---|
| 1 (first) | Search-as-you-type suggestions | debounce ↑ to 400 ms, sample 50%, then disable | explicit search still works |
| 2 | Analytics & event ingestion | drop client RUM/events ≥ 50%, then 100% | none |
| 3 | Recommendation/banner secondary modules | serve last-known cache or hide module | home shows core grid |
| 4 | Report/export generation (vendor/admin) | queue only, no synchronous runs | "generating — will appear in reports" |
| 5 | Non-essential notifications (marketing categories) | pause campaign fan-out; transactional continue | promotions delayed (`BR-NTF-05` unaffected channels intact) |
| 6 | Read-replica-served analytics queries | detach reporting from primary (already routed) | none |
| Last resort | stricter rate limits on anonymous catalog reads | `SEC-REQ-009` buckets tightened 30% (`INFERENCE`) | occasional 429 with friendly message |

Hard floors (never shed): order creation, wallet debit/credit, escrow, ledger writes, OTP delivery, delivery-code verification, security notifications. Shedding is alerted and runbook-driven (`DOC-NFD-006` §6, `NFR-020`).

## 9. Verification Hooks

| Detail | Feeds AC |
|---|---|
| §1 read/write p95 under 10k VUs | `AC-NFR-001-01`, `AC-NFR-001-02` |
| §2 LCP/INP/CLS + bundle/font budgets | `AC-NFR-002-01`, `AC-NFR-002-02` |
| §4 hit ratio + staleness | `AC-NFR-004-01`, `AC-NFR-004-02` |
| §3–§6 test profile & tooling | `AC-NFR-003-01/02`, `AC-S-05` |
| §8 shedding drill (staging overload run) | supports `AC-NFR-007-01` (degradation visible, error rate < 1%) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
