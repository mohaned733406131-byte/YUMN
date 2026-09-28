---
document_id: DOC-ARCH-007
title: Technical Data Flow
category: 04-architecture
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-27
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-004, NFR-007, NFR-008]
related_documents: [DOC-SA-005, DOC-ARCH-003, DOC-ARCH-004, DOC-ARCH-005, DOC-BA-005, DOC-REQ-001]
---

# Technical Data Flow

The realization of the logical flows `DF-01…DF-45` defined in [`03-system-analysis/data-flow.md`](../03-system-analysis/data-flow.md) (DOC-SA-005): which container, which path (sync request / async job / cache / event), and which storage holds the data. DOC-SA-005 owns *what moves*; this document owns *how it moves*.

## 1. Synchronous Request Path (the common case)

```text
Client (CNT-01/02/03)
  │ HTTPS, JWT access token (15 min, C-08)
  ▼
Edge (CNT-10): TLS termination, body-size limits, static assets, per-IP rate counters (SEC-REQ-009)
  │
  ▼
API (CNT-04, NestJS)
  1. global guards: rate limit → JWT verify → PermissionService.evaluate (SEC-REQ-004)
  2. ValidationPipe: transport validation (SEC-REQ-008)
  3. idempotency check for money/order/stock scopes (BR-PLT-03)
  4. module public service → domain logic (pure, unit-testable — NFR-010)
  5. Prisma unit-of-work → PostgreSQL (CNT-07)   [ACID for money ops — BR-PLT-04]
  6. cache write/invalidate → Redis (CNT-06)      [catalog/order reads — NFR-004]
  7. enqueue follow-up jobs → BullMQ via Redis    [notifications, indexing — BR-PLT-01]
  │
  ▼
Response JSON (error model per 07-api/) — target p95 < 200 ms read / < 500 ms write (NFR-001)
```

| Step | Detail | IDs |
|---|---|---|
| Read-through cache | Catalog/product/search-adjacent reads check Redis first; miss → PostgreSQL → populate; TTL + explicit invalidation on write | `NFR-004` (hit ratio ≥ 80% on catalog reads) |
| Write path | PostgreSQL is authoritative; cache entry invalidated in the same request | `C-19`, `NFR-008` |
| Optimistic lock | Order/assignment transitions use version checks → conflict error on race | DOC-SA-010 §5 |
| No provider calls inline | SMS/WhatsApp/push/top-up calls are enqueued or happen only in dedicated flows (top-up initiation) | `BR-PLT-01`, F10 in DOC-ARCH-006 |

## 2. Asynchronous Paths (BullMQ)

Queue naming is fixed by rule: `{block}.{entity}.{action}` (`BR-PLT-01`, `C-20`). **The single queue register is [`06-backend/background-processing.md`](../06-backend/background-processing.md) §1 — every name below appears there verbatim.** Workers (CNT-05) consume them with 3× exponential retries then DLQ + alert (`BR-PLT-02`).

| Queue | Producer | Consumer work | Triggers | Key rules |
|---|---|---|---|---|
| `b02.inventory.expire` | Cart/Order module | Release expired 15-min reservations; restore on cancel | TTL expiry, cancellation | `C-13`, `BR-CAT-07`, `BR-CRT-02` |
| `b05.checkout.saga-compensate` | Checkout saga | Refund debit + release stock when order write failed | Saga step failure | `BR-PLT-04`, `NFR-008` |
| `b06.order.sla.check` | Order module | 24-h CONFIRMED escalation with notification | delayed job at confirmation | `BR-ORD-10` |
| `b10.notification.fanout` | Order module | Order lifecycle notifications fan-out | every state change | `BR-ORD-09`, `BR-NTF-04` |
| `b07.wallet.topup.reconcile` | Wallet module | Poll provider for pending top-ups; apply verified credits | schedule + pending scan | `INT-REQ-001`, `BR-PAY-03` |
| `b07.escrow.release` | Escrow module | Check 7-day maturity guards; post release + commission | delayed 7 days from DELIVERED | `BR-ESC-01…04`, `C-12` |
| `b07.payout.batch` | Payout module | Build batch (3–7 business days, ≥1,000 YER), execute | schedule | `BR-ESC-05/06` |
| `b07.ledger.daily-reconcile` | Ledger module | Daily balancedness + provider statement comparison | daily schedule | `BR-ESC-08`, `BR-FIN-03` |
| `b08.shipping.code-issue` | Shipping module | Issue 6-digit code to buyer via notifications | at OUT_FOR_DELIVERY | `BR-SHP-02`, `C-16` |
| `b08.shipping.failed-attempt-sla` | Shipping module | Attempt-window handling / escalation after 3rd failure | delayed | `BR-SHP-03/06` |
| `b09.return.inspect-check` | Return module | 72-h auto-approval when vendor does not conclude | delayed 72 h from RETURN_RECEIVED | `BR-RET-05` |
| `b09.return.decision-escalate` | Return module | 48-h escalation to admin review | delayed | DOC-SA-010 §2 |
| `b10.notification.delivery` | any module | Render locale template → channel dispatch → receipt record | domain events | `BR-NTF-01…05`, `INT-REQ-003/004` |
| `b02.catalog.index` | Catalog/Content | Upsert/remove documents in Elasticsearch | product/review/banner changes | `FR-009`, `NFR-007` |
| `b02.review.rating-recompute` | Review module | Incremental store-rating recomputation | review change | `BR-REV-05` |
| `b11.analytics.rollup` | Analytics module | Period aggregates, vendor statements | schedule | `BR-FIN-04`, `FR-018` |
| `b13.ticket.auto-close` / DLQ consumer alerts | Admin module | Dead-letter triage, ticket housekeeping | DLQ depth alert | `BR-PLT-02`, `INT-REQ-007` |

**Ordering & idempotency:** workers assume at-least-once delivery; every handler is idempotent (idempotency key or natural key, e.g. reservation id + event) so retries are safe (`BR-PLT-03`, DOC-SA-009 FM-11).

## 3. Caching Layers

| Layer | Where | Contents | Invalidation | Target |
|---|---|---|---|---|
| HTTP cache / CDN | Edge + Cloudflare (`DEP-08`) | Static assets, immutable build files | Versioned asset URLs | `NFR-002` |
| SSR/page cache | Web container (CNT-01) | Anonymous discovery pages | Short TTL or on-publish | `NFR-002` |
| Application read cache | Redis (CNT-06) | Product detail, category trees, banners, feature flags, session-adjacent lookups | Write-time delete + TTL | `NFR-004` ≥ 80% hit on catalog reads |
| Rate-limit counters | Redis | Sliding-window counters per IP/user | Automatic expiry | `SEC-REQ-009` |
| Reservation/TTL keys | Redis | Reservation deadlines as expiring keys driving `b02.inventory.expire` | Expiry event | `C-13` |
| Search results | Elasticsearch | Not cached in Redis by default (ES is fast path) — optional micro-cache `INFERENCE` | Index refresh | `NFR-001` |

**Rule:** cache contents are always derivable from PostgreSQL/ES (DOC-ARCH-003 ownership rule); cache loss degrades latency only (`NFR-007`).

## 4. Event Flow

| Mechanism | Scope | Use | IDs |
|---|---|---|---|
| In-process domain events (`DomainEventBus`) | Inside API/worker process | Decouple module side effects (order placed → notify + index) | DOC-ARCH-006 §5 |
| BullMQ jobs (Redis-backed) | Across processes (API → worker) | All durable background work | `C-20`, `BR-PLT-01` |
| Outbox-style enqueue (`INFERENCE`) | DB row + relay | Guarantee "commit then enqueue" so events are not lost on crash | `NFR-007`, `BR-PLT-04` |
| Provider webhooks (inbound) | Internet → API | Top-up confirmations, messaging receipts — verified, idempotent, retried ×3 then DLQ | `INT-REQ-006`, `BR-PLT-02` |
| Metrics/health events | API/worker → Prometheus | RED metrics, queue depths, DLQ depth | `NFR-014`, `INT-REQ-007` |

There is **no** general-purpose message broker: Redis/BullMQ is the only queue substrate (`C-20`).

## 5. Storage Responsibilities

| Store | Container | Data | Access pattern | Consistency |
|---|---|---|---|---|
| PostgreSQL schemas `b01…b13` | CNT-07 | System of record: identity, catalog, inventory, cart, orders, wallet/ledger, escrow/payout, delivery, returns, notifications metadata, content, analytics base, audit | High-volume point reads/writes; targeted indexes; later partitioning for history (`NFR-017`) | Strong (ACID); single writer per transaction (`BR-PLT-04`) |
| Redis | CNT-06 | Cache, counters, queues, TTL keys | Very high read QPS, short-lived | Eventual; disposable |
| Elasticsearch | CNT-08 | Product/store search documents with Arabic analysis | Complex queries, facets, aggregations | Eventual (index refresh lag acceptable) |
| MinIO | CNT-09 | Images: products, reviews, KYC docs, delivery proof photos | Write-once objects, read-often via CDN/proxy | Strong for object store; referenced by DB rows |
| BullMQ state | CNT-06 | Job payloads, retries, DLQ | Steady write, worker read | Exactly-once *effect* via idempotent handlers |

## 6. End-to-End Worked Flows (technical)

**Checkout confirm (sync + async):**
`Client → API: POST confirm(idempotencyKey)` → guard/validation → `WalletService.debit` (row lock + ledger pair, CNT-07) → saga step `OrderService.place` (master + subs, `PLACED`, CNT-07) → enqueue `b10.notification.fanout`, `b02.catalog.index` (order affects nothing in index; notification only) → cache invalidation → `201` response. Failure after debit → `b05.checkout.saga-compensate` job refunds (idempotent) — see DOC-SA-009 §2.3.

**Delivery confirm (sync):**
`Courier app → API: POST code` → `DeliveryCodeService.verify` (attempt counter in Redis/CNT-06 + state guard in CNT-07) → `OrderService.transition(OUT_FOR_DELIVERY → DELIVERED)` with version check → enqueue `b07.escrow.release` (delay 7 days) + `b10.notification.fanout` → response; customer receives code-based confirmation message.

**Escrow release (async, timed):**
`b07.escrow.release` fires → guard re-check (7 days, no dispute/return/refund) inside transaction → ledger posts (escrow → payable, commission per `BR-ESC-03`) → enqueue `b07.payout.batch` (delay to batch window) → audit entry (`BR-PLT-06`) → notifications to vendor.

**Top-up (inbound webhook):**
provider → `POST /webhooks/topups` (edge) → signature check → idempotent handler on reference → pending record matched → ledger credit pair → cache invalidation of balance → response 200; duplicate delivery no-ops (DOC-SA-009 FM-10).

## 7. Path Counterpart Map (DOC-SA-005 ↔ DOC-ARCH-007)

| Logical flows (DOC-SA-005) | Realized by |
|---|---|
| DF-01…DF-04 (identity/OTP) | §1 request path + `b10.notification.delivery` |
| DF-07…DF-09 (cart/reservation) | §1 + `b02.inventory.expire` |
| DF-10…DF-14 (checkout/order) | §6 checkout, saga + compensation |
| DF-16…DF-22 (delivery) | §1 sync verify + `b08.shipping.code-issue` |
| DF-23…DF-26 (escrow/payout) | §2 timers, §6 escrow release |
| DF-27…DF-30 (returns/refunds) | §2 `b09.*` queues |
| DF-31…DF-34 (top-ups) | §6 webhook path + `b07.wallet.topup.reconcile` |
| DF-35…DF-37 (disputes) | §1 admin commands + audit |
| DF-42…DF-45 (analytics/audit/failures) | §2 `b11.*`, §4 metrics, DLQ alerts |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | §2/§6/§7 queue names restated from the canonical register (`06-backend/background-processing.md` §1) — 14 names renamed, 2 already-conformant kept; intro now points at the register as the authority | `REC-06`/`TD-07` pay-down — closes `CT-04`/consistency finding 10 (consumer side) |
