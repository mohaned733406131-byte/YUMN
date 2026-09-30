---
document_id: DOC-BE-006
title: Background Processing — BullMQ Queues, Jobs & Scheduling
category: 06-backend
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-27
author: analysis-agent
source_of_truth: false
related_requirements: [FR-014, FR-017, FR-018, FR-009, NFR-007, NFR-008, NFR-014, INT-REQ-006]
related_documents: [DOC-BE-001, DOC-BE-002, DOC-BE-005, DOC-BA-005]
---

# Background Processing — BullMQ Queues, Jobs & Scheduling

All asynchronous work runs on **BullMQ over Redis 7** — the only job system (`C-20`). Queue names follow `BR-PLT-01`: **`{block}.{entity}.{action}`**. Retries follow `BR-PLT-02` / `INT-REQ-006`: **3 attempts, exponential backoff, then dead-letter queue (DLQ) with alert**.

---

## 1. Queue Register (by block)

| Queue name (BR-PLT-01) | Block | Producer | Example jobs |
|---|---|---|---|
| `b01.auth.session.sweep` | B01 | auth service | expired-session cleanup |
| `b02.inventory.expire` | B02 | cart/checkout | 15-min reservation TTL release (`C-13`) |
| `b02.catalog.index` | B02 | product service | ES index upsert/delete |
| `b02.review.rating-recompute` | B02 | review service | incremental store rating (`BR-REV-05`) |
| `b03.vendor.kyc.sla` | B03 | kyc service | 48-h decision escalation (`BR-VND-03`) |
| `b04.search.banner-refresh` | B04 | content publish | merchandising cache refresh |
| `b05.checkout.saga-compensate` | B05 | checkout saga | compensating refund/stock restore (`BR-PLT-04`) |
| `b06.order.sla.check` | B06 | scheduler | CONFIRMED >24 h escalation (`BR-ORD-10`) |
| `b06.order.timeline-project` | B06 | state change | timeline read-model update |
| `b07.wallet.topup.reconcile` | B07 | top-up service | provider poll/callback reconciliation (`INT-REQ-001`) |
| `b07.escrow.release` | B07 | scheduler | 7-day escrow release (`BR-ESC-01/02`, `C-12`) |
| `b07.payout.batch` | B07 | scheduler | vendor payouts 3–7 business days (`BR-ESC-05`) |
| `b07.ledger.daily-reconcile` | B07 | scheduler | balance checks, finance alerts (`BR-ESC-08`, `BR-FIN-03`) |
| `b08.shipping.assign-offer` | B08 | order ready | offer to eligible couriers (`BR-SHP-04`) |
| `b08.shipping.code-expire` | B08 | delivery code | code TTL cleanup (`BR-SHP-02`) |
| `b08.shipping.failed-attempt-sla` | B08 | delivery service | 3rd failure → admin escalation (`BR-SHP-06`) |
| `b09.return.inspect-check` | B09 | scheduler | 72-h auto-approve (`BR-RET-05`) |
| `b09.return.refund-credit` | B09 | REFUNDED state | wallet credit ≤3 business days (`BR-RET-04`) |
| `b10.notification.fanout` | B10 | domain events | SMS/WhatsApp/push/in-app dispatch (`FR-017`) |
| `b10.notification.template-render` | B10 | fanout | per-locale render (`BR-NTF-04`) |
| `b11.analytics.rollup` | B11 | scheduler | dashboard aggregates (FR-018) |
| `b11.analytics.export` | B11 | admin request | report CSV/XLSX generation |
| `b12.content.publish` | B12 | admin CMS | ISR revalidation ping + cache purge |
| `b13.platform.webhook.send` | B13 | events | signed outbound webhooks (`INT-REQ-006`) |
| `b13.platform.audit.retention` | B13 | scheduler | retention housekeeping (DATA-REQ-003) |
| `b07.wallet.credit` | B07 | top-up/bank verify | wallet credit posting for verified top-ups (`BR-PAY-04`); queue-depth alert (`BR-PLT-02`) |
| `b08.shipping.code-issue` | B08 | delivery (OUT_FOR_DELIVERY) | issue 6-digit code to buyer via notifications (`BR-SHP-02`, `C-16`) |
| `b09.return.decision-escalate` | B09 | return module | 48-h escalation to admin review (DOC-SA-010 §2) |
| `b10.notification.delivery` | B10 | fanout | per-channel provider dispatch — SMS primary, WhatsApp failover, push (channel = job lane, not a separate queue) (`BR-NTF-03`, `INT-REQ-003`); receipts logged |
| `b13.ticket.auto-close` | B13 | admin module | DLQ triage alerts + ticket housekeeping (`BR-PLT-02`, `INT-REQ-007`) |

## 2. Notification Fan-Out (FR-017, BR-NTF-*)

```text
domain event (OrderConfirmed, OtpRequested, WalletCredited, …)
  → b10.notification.fanout (single job, contains event ID — no message bodies)
      → resolve recipients + locale (user preference, ar default — BR-NTF-04)
      → preference check (security notices non-disableable — BR-NTF-02)
      → per-channel child jobs:
           b10.notification.template-render → b10.notification.delivery (channel = job lane: sms | whatsapp | push)
           in-app: direct DB write (always)
      → SMS primary; provider timeout/error → WhatsApp failover (BR-NTF-03, INT-REQ-003)
      → delivery receipts logged
```

| Property | Value |
|---|---|
| Channels | SMS, WhatsApp, in-app, push (FCM/APNs) — **no email v1** (`GAP-03`) |
| Deduplication | BullMQ `jobId = hash(eventId, recipient, channel)` → retries idempotent |
| Ordering | per-recipient ordering enforced by sequential job chaining for OTP flows |
| Backpressure | per-channel rate limiting via queue `limiter` (protect provider quotas, `SEC-REQ-009` alignment) |

## 3. Money Jobs (escrow, payouts, reconciliation)

| Job | Schedule | Semantics |
|---|---|---|
| `b07.escrow.release` | every 15 min sweep + per-order delayed job at `DELIVERED + 7 d` | re-checks BR-ESC-02 conditions at execution time (payload = order IDs only) |
| `b07.payout.batch` | daily at business-day window | batches released payables ≥1,000 YER; KYC/suspension gate (`BR-ESC-05/06`) |
| `b07.ledger.daily-reconcile` | daily | Σ ledger balanced; wallet+escrow+payable vs provider statements; mismatch → alert (`BR-ESC-08`, `BR-FIN-03`) |
| `b07.wallet.topup.reconcile` | every 5 min | polls pending top-ups, matches callbacks (`INT-REQ-001`), never credits on client claim (`BR-PAY-03`) |
| `b09.return.refund-credit` | on demand + sweep | wallet credit ≤3 business days (`BR-RET-04`) |

**Safety:** money jobs run inside the same service/domain code as synchronous flows (`DOC-BE-005`) — the queue only decides *when*, never *what*.

## 4. Stock TTL (C-13)

| Aspect | Implementation |
|---|---|
| Reservation | `expires_at` column set at reserve time (15 min) |
| Sweeper | `b02.inventory.expire` repeatable every 60 s: `SELECT … WHERE expires_at <= now AND state = RESERVED` → release each, emit `StockReleased` |
| Idempotency | release updates guarded by `state = RESERVED` predicate — double execution is a no-op |
| Payment race | permanent deduction happens in the payment transaction; expiry job skips rows already deducted |
| Latency budget | release within 60 s of expiry; UI countdown uses server timestamp (05 state doc §4) |

## 5. Order SLA Escalations (BR-ORD-10, BR-SHP-06)

| Job | Trigger | Action |
|---|---|---|
| `b06.order.sla.check` | repeat hourly: orders CONFIRMED 24 h | create admin review item + notify customer (`BR-ORD-10` — never silent auto-cancel) |
| `b08.shipping.failed-attempt-sla` | on 3rd failed attempt | support ticket + timeline note (`BR-SHP-06`) |
| `b03.vendor.kyc.sla` | 48 h after submission | escalate to admin queue (`BR-VND-03`) |
| `b09.return.inspect-check` | 72 h after RETURN_RECEIVED | auto-approve return (`BR-RET-05`) |
| return decision 48 h | state doc §2 guard | auto-escalate pending return approval to admin |

## 6. Search Index Sync (FR-009, NFR-007)

| Aspect | Behavior |
|---|---|
| Trigger | product create/update/delete, price/stock change, category change → `b02.catalog.index` |
| Idempotency | job payload = product ID; consumer reads current DB state (last-write-wins), never applies stale payload deltas |
| Failure mode | DLQ alert; storefront keeps serving ISR/cached data — browse degrades gracefully (`NFR-007`) |
| Backfill | admin-triggered full reindex job (idempotent, batched by ID range) |
| Consistency | ES is **derived** — DB is source of truth; mismatch repaired by reindex |

## 7. Webhooks (INT-REQ-006, BR-PLT-02)

| Property | Value |
|---|---|
| Signing | HMAC-SHA256 over body + timestamp; signature header per `10-integrations/` |
| Delivery | `b13.platform.webhook.send` — **3 retries, exponential backoff** (e.g. 1 m / 5 m / 25 m), then **DLQ** |
| Idempotency | monotonic `event_id` so receivers can dedupe; our own handlers idempotent on inbound webhooks too |
| DLQ | depth > 0 → alert (BR-PLT-02); replay tooling in admin console (FR-020) |
| Security | no secrets in payloads; rotate signing secrets via environment/secrets manager (`SEC-REQ-007`) |

## 8. Job Reliability Semantics

| Concern | Policy |
|---|---|
| Retries | `attempts: 3`, exponential backoff, jitter (BR-PLT-02) |
| DLQ | failed-after-retries moves to `{queue}.dlq`; alert on depth; manual replay with audit entry |
| Poison messages | consumer wraps handler in try/catch; structured error logged with job ID + correlation ID (NFR-014); permanent failures classified non-retryable (validation) → immediate DLQ |
| Idempotency | every handler idempotent: `jobId` derived from business key; DB-state re-read; money ops use idempotency keys (BR-PLT-03) |
| Payloads | carry **IDs only** — never amounts, never PII beyond recipient ID; consumer fetches fresh state |
| Concurrency | per-queue `concurrency` limits; money queues concurrency low (serial-ish); notification queues high |
| Graceful shutdown | worker finishes in-flight job on SIGTERM (deploys, NFR-020) — no job loss (NFR-007) |
| Observability | queue depth, wait time, failure rate exported to Prometheus; DLQ alerts (`INT-REQ-007`, `../../12-non-functional/core/observability.md`) |
| Stalled jobs | BullMQ stalled-job detection re-enqueues; counted as reliability signal |

## 9. Scheduling Model

| Mechanism | Use |
|---|---|
| BullMQ repeatable jobs | periodic sweeps (stock TTL, SLA checks, reconciliation, rollups) — named `repeat.key` stable across deploys |
| Delayed jobs | per-entity timers (escrow release at +7 d, code expiry) |
| Leader election | single scheduler instance via Redis lock — prevents duplicate repeatable registration on multiple replicas |
| Time zone | schedules in `Asia/Aden` where business-day logic applies (payouts) |
| Missed runs | missed window → next tick processes with re-derived state (no drift) |

## 10. Verification

| Test | Coverage |
|---|---|
| Unit | handler idempotency (double-run no-op), backoff/DLQ classification |
| Integration | TTL expiry releases stock; escrow release only when BR-ESC-02 holds; webhook 3-failure → DLQ |
| Failure injection | Redis restart mid-job → job completes after recovery; worker kill → no loss (NFR-007) |
| Load | queue throughput at C-25 scale (k6 + queue-depth dashboards) |
| Naming | CI check that every queue matches `BR-PLT-01` pattern |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | Register extended 25 → 30 rows (`b07.wallet.credit`, `b08.shipping.code-issue`, `b09.return.decision-escalate`, `b10.notification.delivery`, `b13.ticket.auto-close`); §2 delivery lanes restated as lanes of the registered `b10.notification.delivery` queue | `REC-06`/`TD-07` pay-down — single queue register of record (also closes `CRIT-04` intra-file clause) |
