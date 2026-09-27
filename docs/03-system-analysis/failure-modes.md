---
document_id: DOC-SA-009
title: Failure Modes & Analysis-Level Handling
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-011, FR-013, FR-015, NFR-006, NFR-007, NFR-008]
related_documents: [DOC-SA-008, DOC-SA-010, DOC-BA-005, DOC-IR-006, DOC-REQ-001]
---

# Failure Modes & Analysis-Level Handling

What can go wrong, how the system *detects* it, and what it *does* — expressed behaviorally, before any technical mechanism is chosen. Technical realization (queues, retries, transactions, alerting) is documented in `04-architecture/data-flow.md` (DOC-ARCH-007) and `10-integrations/`; resilience test cases derive from this register in `13-testing/`. IDs `FM-01…FM-18` are referenced from `edge-cases.md` (DOC-SA-008) where a scenario is both an edge case and a failure mode.

## 1. Failure Mode Register

| ID | Component | Failure | Detection | Immediate behavior | Recovery | Data impact |
|---|---|---|---|---|---|---|
| FM-01 | SMS provider | Timeout / error on OTP send | Provider response timeout | Failover to secondary provider, then WhatsApp | Queued retry; receipts logged | None (no state change) |
| FM-02 | WhatsApp Business | Template rejected / channel down | API rejection | Notification falls back to SMS/in-app record | Template re-approval; channel resumes | Message record marked failed |
| FM-03 | m-Floos / OneCash | Callback never arrives | Missing callback within window | Top-up stays **pending**; wallet not credited | Reconciliation poll verifies; credit on confirmation | No ledger post until verified |
| FM-04 | Payment provider | Provider debited customer but platform crashed before order | Callback replay / reconciliation mismatch | On restart, verified credit is applied to wallet, **not** auto-charged to an order | Customer re-initiates checkout with funded wallet | Credit posted once (idempotent) |
| FM-05 | Order creation | Payment succeeded, order write failed | Saga step failure | Compensating refund of the debit; cart restored | Customer retries; same idempotency key returns clean result | No orphan debit; no phantom order |
| FM-06 | Wallet | Concurrent double-spend attempt | Balance check failure under lock | Losing transaction fails with insufficient-balance error | Retry with new key only if user re-confirms | Balance never negative |
| FM-07 | Refund / payment / top-up | Duplicate submission | Idempotency key hit | Original result returned; no second ledger post | None needed | Single posting pair |
| FM-08 | Delivery code | Wrong code entered | Verification mismatch | Attempts 1–2 show remaining; 3rd locks 24 h + auto ticket | Lock expires; admin/support may resolve | Attempt counter recorded |
| FM-09 | Webhook | Invalid signature / replayed payload | Signature & nonce check | Payload rejected, nothing written | Provider resends genuine event | None |
| FM-10 | Webhook | Valid payload processed twice | Handler idempotency | Second delivery no-ops | None | Single effect |
| FM-11 | Job queue | Job fails 3 times | Retry exhaustion | Moved to dead-letter queue; DLQ depth alert raised | Operator replays after fix; alert routed to on-call | No silent loss (`NFR-007`) |
| FM-12 | Stock | Reservation expires exactly while checkout confirms | TTL race | Deterministic order: expiry releases, checkout re-reserves or fails with conflict | Customer action or automatic re-reserve attempt | Stock never negative |
| FM-13 | Elasticsearch | Search index unavailable | Query errors / health check | Browse-by-category fallback remains; search shows degraded results | Index rebuild/resync from catalog when restored | Stale-tolerant index |
| FM-14 | Redis | Cache unavailable | Connection errors | Reads fall through to database; catalog reads slower but correct | Cache warms on recovery | None (cache is derived) |
| FM-15 | Redis | Queue broker unavailable | Enqueue failures | Domain writes that require jobs are retried/queued locally; user gets success-with-pending semantics where safe | Jobs drain when Redis returns | No lost order/payment — jobs are re-enqueued |
| FM-16 | PostgreSQL | Primary database unavailable | Health/readiness failure | Traffic held at readiness gate; writes unavailable; system reports degraded (`BR-PLT-07`) | Restore/replica promotion within RTO ≤ 1 h, RPO ≤ 15 min | Up to 15 min of committed work at risk per RPO |
| FM-17 | MinIO | Object storage unavailable | Upload/download errors | Product image upload blocked with clear error; existing images with cached URLs unaffected | Uploads resume when storage returns | No partial images accepted |
| FM-18 | Escrow scheduler | Release job down | No matured releases processed / schedule lag | Escrow simply stays held — fail-safe direction; no incorrect early release | Backlog processed on recovery; vendors notified of delay | Money stays in held state (conservative) |

## 2. Detailed Analyses

### 2.1 Provider Outage — SMS / WhatsApp (FM-01, FM-02)

- **Detection:** send timeout or explicit provider error; delivery receipts logged per `INT-REQ-003`.
- **Behavior:** OTP delivery is *attempt-chain* semantics: SMS primary → second SMS provider → WhatsApp template (`BR-NTF-03`, `INT-REQ-003/004`). Each hop preserves the same OTP code until expiry (6 min validity window: 5-minute expiry per `BR-AUTH-03`).
- **User-visible outcome:** if all channels fail within the OTP validity window, registration/login cannot complete — the UI states that verification is temporarily unavailable and offers retry; the OTP attempt counter is **not** consumed by provider failures (only by wrong-code entry).
- **Non-goals:** no email fallback (`BR-NTF-01`, `GAP-03`); OTP is never displayed in-app.
- **Governing IDs:** `INT-REQ-003`, `INT-REQ-004`, `BR-AUTH-03`, `BR-NTF-02/03`, `SEC-REQ-001`.

### 2.2 Provider Outage — Payment / Top-up (FM-03, FM-04)

- **Detection:** callback absent within the reconciliation window; poll against provider statement (`INT-REQ-001`).
- **Behavior:** the wallet credits **only** on a verified callback or reconciled poll — never on client claim (`BR-PAY-03`). Provider downtime therefore leaves top-ups in *pending*, which is safe: no money moved on the platform side that the provider does not confirm.
- **Asymmetry rule:** a platform crash *after* provider confirmation and *before* local post is closed by replay/reconciliation: the credit is applied idempotently to the wallet. It is never converted into an order charge automatically — checkout is a customer-initiated act with a fresh idempotency key (`BR-ORD-06`, `BR-PLT-03`).
- **Governing IDs:** `INT-REQ-001`, `BR-PAY-03/08`, `BR-PLT-03/04`, `NFR-008`.

### 2.3 Payment Succeeded but Order Creation Failed (FM-05)

- **Sequence:** debit → (failure in order write) → compensate.
- **Behavior:** multi-step order creation is a saga with compensating actions (`BR-PLT-04`). If sub-order creation fails after the wallet debit, the compensation credits the wallet back with the same idempotency key family, restores any reservations, and surfaces a retryable error. The customer never sees "paid, no order".
- **Invariants checked:** exactly one debit exists or exactly one debit+refund pair exists; never a debit without either an order or a refund; ledger stays balanced (`BR-PAY-06`, `BR-ESC-08`).
- **Governing IDs:** `BR-PLT-03/04`, `BR-ORD-06`, `NFR-008`, `DATA-REQ-006`.

### 2.4 Wallet Double-Debit Prevention (FM-06, FM-07)

- **Prevention layers:** (1) idempotency key on every payment/top-up/refund (`BR-PAY-08`, `BR-PLT-03`); (2) row-level locking with atomic balance check so concurrent debits serialize (`BR-PAY-05`); (3) append-only double-entry ledger so any residual anomaly is detectable by daily reconciliation (`BR-ESC-08`, `DATA-REQ-007`); (4) money operations confined to ACID transactions (`BR-PLT-04`, `NFR-008`).
- **If imbalance is ever detected:** reconciliation alerts finance; corrections are compensating entries only — postings are never updated or deleted (`DATA-REQ-007`).
- **Governing IDs:** `BR-PAY-05/06/08`, `BR-PLT-03/04`, `BR-ESC-08`, `DATA-REQ-007`, `NFR-008`.

### 2.5 Delivery Code Mismatch & Abuse (FM-08)

- **Behavior:** attempts 1–2 return remaining-attempt feedback; the 3rd failure locks confirmation for 24 hours and auto-creates a support ticket (`BR-SHP-03`). Lock and attempts are server-side; a courier app restart does not reset them.
- **Race:** concurrent submissions are serialized — first success wins; duplicate successes no-op (`state-transitions.md` §5, `EC-29`).
- **No GPS fallback exists** — evidence for support is code + timestamp + courier identity (+ optional photo) (`BR-SHP-05/07`, `C-16`).
- **Admin override question is open** (`GAP-02`) — v1 behavior is ticket-driven manual resolution only.
- **Governing IDs:** `BR-SHP-02/03/05/07`, `BR-ORD-08`, `SEC-REQ-005`, `C-16`.

### 2.6 Webhook Retries & Idempotency (FM-09, FM-10, FM-11)

- **Contract:** webhooks are signed; handlers are idempotent; delivery retries 3× with exponential backoff and then dead-letters (`INT-REQ-006`, `BR-PLT-02`).
- **DLQ handling:** DLQ depth triggers an alert (`BR-PLT-02`); an operator in B13 replays after fixing the cause — the idempotent handler makes replay safe.
- **Ordering:** handlers must not assume ordering; state derived from webhooks is validated against local intent records (e.g. top-up reference exists) before any ledger post.
- **Governing IDs:** `INT-REQ-006`, `BR-PLT-01/02`, `NFR-007`, `SEC-REQ-008`.

### 2.7 Stock Oversell Prevention (FM-12)

- **Layers:** (1) reservation with 15-minute TTL holds units during cart/checkout (`C-13`, `BR-CRT-02`); (2) atomic integer deduction with stock ≥0 invariant (`BR-CAT-07`); (3) permanent deduction occurs at payment, restoration on cancellation; (4) TTL expiry is processed as a job, and checkout confirmation re-checks reservation validity — a race between expiry and confirm resolves deterministically to either reserved or conflict, never to negative stock.
- **Governing IDs:** `C-13`, `BR-CAT-07`, `BR-CRT-02/05`, `BR-PLT-04`.

## 3. Degradation Modes (graceful, by design)

| Subsystem down | Service impact | Still works | Governing IDs |
|---|---|---|---|
| Search index | Search degraded | Category browse, direct PDP links, cart/checkout | `NFR-007` |
| Cache | Slower reads | All functionality (database serves reads) | `NFR-004` |
| Queue broker | Background work delayed | Synchronous flows; jobs drain later | `NFR-007`, `C-20` |
| SMS/WhatsApp | OTP/notification channels reduced | In-app inbox, alternate channel of the chain | `BR-NTF-03`, `INT-REQ-003` |
| Top-up provider | New top-ups pending | Existing balance spends normally | `INT-REQ-001`, `BR-PAY-03` |
| Object storage | New uploads blocked | Existing media served | `SEC-REQ-011` |
| Escrow scheduler | Releases delayed | Everything else; funds stay safely held | `BR-ESC-02` |
| Database | Writes blocked at readiness gate | Static assets; system reports degraded | `BR-PLT-07`, `NFR-005` |

**Non-negotiable degradation rule:** in every mode above, **money and stock invariants hold** — the system degrades to *slower or fewer features*, never to *incorrect balances, oversell, or early escrow release* (`NFR-007`, `NFR-008`).

## 4. Recovery Objectives Anchored Here

| Objective | Target | Failure modes governed |
|---|---|---|
| RTO | ≤ 1 hour (`C-26`, `NFR-006`) | FM-16, FM-17 (service restoration) |
| RPO | ≤ 15 minutes (`C-26`, `NFR-006`) | FM-16 (data loss bound), `DATA-REQ-004` |
| Availability | 99.99% monthly (`C-26`, `NFR-005`) | all — measured at readiness gate (`BR-PLT-07`) |
| No silent data loss | Queue retries + DLQ (`NFR-007`) | FM-11, FM-15 |
| Zero ledger imbalance | Daily reconciliation (`BR-ESC-08`, `BR-FIN-03`) | FM-05, FM-06, FM-07 |

## 5. Verification

Failure modes become resilience test cases in `13-testing/` (chaos-style provider simulations, duplicate-webhook tests, concurrency tests) and are traced in `19-traceability/`. Alert routes and runbook references belong to `12-non-functional/observability.md` and `14-devops-infrastructure/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
