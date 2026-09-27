---
document_id: DOC-ARCH-003
title: Container View
category: 04-architecture
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-004, NFR-007, NFR-016]
related_documents: [DOC-ARCH-002, DOC-ARCH-005, DOC-ARCH-007, DOC-SA-003, DOC-REQ-001]
---

# Container View

The deployable/runtime containers of yumn (`CNT-01…CNT-10`), their responsibilities, the data each owns, and how they communicate. This expands the C4 container diagram in `architecture-overview.md` (DOC-ARCH-002); concrete services, ports, networks and volumes are in `deployment-view.md` (DOC-ARCH-005).

## 1. Container Inventory

| ID | Container | Technology | Process | Responsibility | Data it owns |
|---|---|---|---|---|---|
| CNT-01 | Web application | Next.js 14 (Node 20 / TS 5) | SSR + static pages | Customer storefront, vendor panel, admin console (3 shells in one app — `INFERENCE`); RTL-first UI, client routing, form/state handling | Browser-local state only; guest cart mirror (`BR-CRT-03`) |
| CNT-02 | Customer mobile app | React Native 0.73 | Mobile process | Browse, wallet, orders, returns, reviews, push registration | Device-local cache; no authoritative data |
| CNT-03 | Courier mobile app | React Native 0.73 | Mobile process | Assignment list, pickup/transit updates, delivery-code entry | Device-local cache; no authoritative data |
| CNT-04 | API — NestJS modular monolith | NestJS 10 (Node 20, TS 5) | HTTP server | Synchronous domain logic for `B01…B13`, RBAC, validation, REST contract, webhook intake | In-process state only (stateless across restarts) |
| CNT-05 | Worker — BullMQ consumers | Same NestJS codebase, worker entrypoint | Background process | Async jobs: notifications, escrow maturity, payouts, reservation TTL expiry, search indexing, reconciliation, escalations | Job payloads in Redis (CNT-06) |
| CNT-06 | Redis 7 | Redis 7 | Data service | BullMQ queues, read cache, rate-limit counters, optimistic-lock/coordination helpers, TTL keys | Ephemeral/derived data (never the system of record) |
| CNT-07 | PostgreSQL 16 | PostgreSQL 16 | Data service | System of record: schemas `b01…b13` — identity, catalog, inventory, cart, orders, wallet/ledger, escrow/payout, delivery, returns, notifications, content, analytics, audit | All authoritative relational data (`C-19`) |
| CNT-08 | Elasticsearch 8 | Elasticsearch 8 | Data service | Arabic-aware full-text search, facets, suggestions for `FR-009` | Search index (derived, rebuildable) |
| CNT-09 | MinIO | MinIO (S3-compatible) | Data service | Product/review/KYC/proof images and other media | Object storage (`DEP-07`) |
| CNT-10 | Reverse proxy / edge | Nginx or equivalent (`INFERENCE`) | Edge process | TLS termination, routing to CNT-01/CNT-04, static asset serving, request-size limits | — |

> Compose may additionally run Prometheus/Grafana for observability (`INT-REQ-007`) — operational containers, listed in `deployment-view.md`.

## 2. Responsibilities in Detail

### CNT-01 Web application (Next.js 14)
- Server-side rendering for discovery performance (`NFR-002`: LCP < 2.5 s on 4G, JS < 200 KB gzipped).
- Three role shells: storefront (`ACT-01`), vendor panel (`ACT-02`), admin console (`ACT-04/05/06`) — route-level separation, shared design system (`NFR-013` Arabic default, `C-24`).
- Client-side guards are **UX only**; security is enforced in CNT-04 (`SEC-REQ-004`).
- Guest cart kept locally, merged at login (`BR-CRT-03`).

### CNT-02 / CNT-03 Mobile apps (React Native 0.73)
- Same REST contract as CNT-01; JWT access 15 min / refresh 7 days single-use rotation (`C-08`, `SEC-REQ-003`).
- CNT-03 contains the delivery-code entry flow and attempt feedback (`BR-SHP-03`); it never receives location services (`BR-SHP-05`, `C-16`).
- Push tokens registered for `BR-NTF-01` push channel.

### CNT-04 API (NestJS modular monolith)
- Hosts all 13 modules (`component-view.md`); the only container allowed to write to CNT-07.
- Performs authentication, RBAC + ownership checks per request (`SEC-REQ-004`), validation, idempotency-key handling (`BR-PLT-03`), money transactions (`BR-PLT-04`).
- Exposes REST endpoints (contract in `07-api/`) and verified webhook endpoints (`INT-REQ-006`).
- Stateless: horizontal scaling by adding replicas (same image) — `NFR-018`.

### CNT-05 Workers (BullMQ)
- Same build artifact as CNT-04 with a different entrypoint command (Compose service `worker`), guaranteeing identical domain code.
- Consumes queues named `{block}.{entity}.{action}` (`BR-PLT-01`, `C-20`); retries 3× exponential then DLQ with alert (`BR-PLT-02`).
- Runs timers that must survive client absence: 15-min stock TTL (`C-13`), 24-h escalation (`BR-ORD-10`), 72-h inspection (`BR-RET-05`), 7-day escrow (`BR-ESC-02`), payout batches (`BR-ESC-05`), daily reconciliation (`BR-ESC-08`).

### CNT-06 Redis / CNT-07 PostgreSQL / CNT-08 Elasticsearch / CNT-09 MinIO
- Only CNT-07 is authoritative; CNT-06/CNT-08 hold derived data and may be rebuilt (`NFR-007`).
- CNT-07 holds all money data inside ACID transactions (`NFR-008`); `DATA-REQ-004` governs WAL + snapshots.
- CNT-08 receives documents from CNT-05 index jobs; stale-tolerant with category-browse fallback.
- CNT-09 stores only validated, size-limited, EXIF-stripped images (`SEC-REQ-011`).

## 3. Communication Matrix

| From → To | Protocol / mechanism | Payload | Sync? | Notes |
|---|---|---|---|---|
| CNT-01/02/03 → CNT-10 | HTTPS (TLS 1.3) | REST/JSON | Sync | Only entry path (`SEC-REQ-006`) |
| CNT-10 → CNT-01 | HTTP (internal network) | HTML/JSON | Sync | SSR + static |
| CNT-10 → CNT-04 | HTTP (internal network) | REST/JSON | Sync | JWT verified at CNT-04 |
| CNT-04 → CNT-07 | Prisma over TCP | SQL (parameterized) | Sync | Single writer of record; pooling in CNT-04 |
| CNT-04 → CNT-06 | Redis protocol | Cache get/set, `LPUSH`/`BULL` queue ops | Sync | Cache misses fall through to CNT-07 |
| CNT-04 → CNT-05 (via CNT-06) | BullMQ enqueue | Job DTO | Async | Domain events that need background work |
| CNT-05 → CNT-07 | Prisma over TCP | SQL | Sync | Worker applies job effects transactionally |
| CNT-05 → CNT-06 | Redis protocol | Job ack/retry/DLQ, cache invalidation | Sync | |
| CNT-05 → CNT-08 | HTTP (bulk/index API) | Search documents | Async | Index writes after catalog/content changes |
| CNT-05/04 → CNT-09 | S3 API (HTTPS internal) | Images | Sync (upload) | Pre-signed or proxied upload (`INFERENCE`) |
| CNT-04/05 → external providers | HTTPS via adapters | Provider payloads | Sync (egress) | `INT-REQ-008`; secrets from environment (`SEC-REQ-007`) |
| External → CNT-04 | HTTPS webhook endpoints | Signed events | Async (inbound) | Verify → idempotent handle → enqueue (`INT-REQ-006`) |
| CNT-04/05 → Prometheus/Grafana | HTTP scrape (`INT-REQ-007`) | Metrics | Async | RED metrics per endpoint (`NFR-014`) |

## 4. Ownership & Consistency Rules

1. **One writer rule:** only CNT-04 and CNT-05 write to CNT-07, and both run the same domain code; no container writes to CNT-07 directly except migrations run by operators/deploy (`DATA-REQ-005`).
2. **Derived data rule:** anything in CNT-06 (cache), CNT-08 (index) must be reconstructible from CNT-07 — losing them degrades, never corrupts (`NFR-007`).
3. **Read-your-writes:** after a successful write, subsequent reads by the same session observe the change (cache invalidation on write for catalog/order/wallet reads) — `INFERENCE`, required for correct UX.
4. **No container-to-container domain calls inside PostgreSQL** (no dblink, no foreign data wrappers) — keeps `C-19` as a single consistent store.
5. **Mobile clients hold no authority:** every mobile action revalidates server-side (`SEC-REQ-004`).

## 5. Scaling Hooks (see `scalability.md`)

| Container | Scale unit | Mechanism |
|---|---|---|
| CNT-01 | Replicas behind edge | Stateless SSR/static serving |
| CNT-04 | Replicas (same image) | Load balancer; readiness gate (`BR-PLT-07`) |
| CNT-05 | Replicas | BullMQ competes on queues — natural work distribution |
| CNT-06/07/08/09 | Vertical first; CNT-07 read replicas later | `NFR-018` documented path |
| CNT-10 | Single or replicated | Edge health checks |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
