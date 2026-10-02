---
document_id: DOC-INT-001
title: Integration Layer Architecture (Ports, Async, Degradation)
category: 10-integrations
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-001, INT-REQ-003, INT-REQ-004, INT-REQ-005, INT-REQ-006, INT-REQ-007, INT-REQ-008]
related_documents: [DOC-INT-000, DOC-INT-002, DOC-INT-007, DOC-IR-000, DOC-IR-008, DOC-BA-005, DOC-BE-006]
---

# Integration Layer Architecture

Source of truth for *how* yumn integrates: the ports-and-adapters boundary, sync vs async execution, the common cross-cutting concerns every integration obeys, what happens when each provider is down, and how integration behavior is observed. Per-provider contracts live in the sibling files; requirements live in `02-requirements/`.

## 1. Ports & Adapters (`INT-REQ-008`)

```text
domain modules (wallet · orders · notifications · shipping)
        │  depends only on            never sees
        ▼                             ▼
 ┌─────────────────────┐      vendor JSON/XML, vendor error
 │ PaymentProviderPort │      strings, vendor IDs, SDK types
 │ SmsProviderPort     │◄───  (blocked by CI import/lint rule,
 │ WhatsAppPort        │       AC-IR008-01/03)
 │ DeliveryProviderPort│
 └─────────┬───────────┘
           │ implemented by (adapter folder owns credentials,
           ▼            HTTP client, payload mapping, signing)
 ┌──────────────────────────────────────────────┐
 │ mFloosAdapter · OneCashAdapter · SmsPrimary  │
 │ SmsSecondary · WhatsAppAdapter · InternalFleet│
 └──────────────────────────────────────────────┘
```

| Element | Design | Canon |
|---|---|---|
| Ports | Provider-neutral interfaces with normalized DTOs: integer YER amount, phone, platform reference, status enum | `INT-REQ-008` |
| Error taxonomy | Every adapter failure maps to `TIMEOUT` / `REJECTED` / `PROVIDER_DOWN` / `SIGNATURE_INVALID`; unknown vendor errors map to `PROVIDER_DOWN` — never an exception escaping into a domain transaction | `INT-REQ-008` failure section |
| Selection & failover | Primary/secondary choice is **configuration evaluated through the port** — no `if vendor == …` branches in services | `INT-REQ-008` |
| Credentials | Injected per adapter from environment only; adapters are the only code holding provider signing logic | `SEC-REQ-007`, `INT-REQ-008` security |
| Boundary enforcement | Import/lint rule fails the build on vendor references outside adapter folders; shared contract suite runs against every adapter | `AC-IR008-01/04`, `NFR-009` |
| Substitution test | Swapping mock ↔ sandbox ↔ production adapter requires **zero domain edits** | `AC-IR008-02` |

## 2. Sync vs Async

| Mode | Used for | Mechanics |
|---|---|---|
| **Synchronous (request/response)** | Outbound provider calls (initiate top-up, send SMS attempt, send template) | 10 s timeout per call; adapter returns normalized result or `TIMEOUT` |
| **Synchronous (inbound webhook, fast-ack)** | Provider callbacks: payment confirmations, DLRs, WhatsApp status | Verify signature → **durably persist raw payload** → acknowledge `200` within 10 s → processing continues asynchronously (`INT-REQ-006`) |
| **Asynchronous (BullMQ, `C-20`)** | All domain follow-up: wallet credit posting, notification fan-out, reconciliation, escrow release, DLQ processing | Queue names `{block}.{entity}.{action}` (`BR-PLT-01`); 3 retries with exponential backoff then DLQ + alert (`BR-PLT-02`) |
| **Scheduled (repeatable jobs)** | Daily reconciliation, poll-fallback for pending top-ups, audit-chain verification, DLQ depth metrics | Worker container, same image (`DOC-BE-006`) |

**Rule:** no HTTP request path ever blocks on more than one external call; anything slower than the `NFR-001` write budget (p95 < 500 ms) moves to a queue.

## 3. Common Concerns (apply to every integration)

| Concern | Design | Canon |
|---|---|---|
| **Auth to provider** | Per-adapter credential (API key/secret or merchant credential) from env; OAuth-style tokens cached in memory with expiry handling inside the adapter; never logged | `SEC-REQ-007`, `INT-REQ-008` |
| **Timeouts** | 10 s per outbound call; inbound webhook total handling ≤ 10 s (verify + persist + ack) | `INT-REQ-001/003/004/006` |
| **Retries** | 3 attempts, exponential backoff, then **dead-letter queue** with alert; never infinite retry | `BR-PLT-02`, `BR-PLT-01` |
| **Idempotency** | Provider transaction/message ID is the idempotency key; N deliveries → exactly 1 domain effect; money ops additionally require platform idempotency keys | `BR-PLT-03`, `BR-PAY-08`, `BR-PLT-04` |
| **Circuit breaker** | Repeated `PROVIDER_DOWN`/`TIMEOUT` results open the circuit for a cooldown: calls fail fast with `PROVIDER_DOWN` instead of tying up workers; half-open probe on cooldown expiry (`INFERENCE` — canon mandates failover and degradation, not a named breaker pattern) | `NFR-007` graceful degradation |
| **Sandbox vs production** | Distinct credentials and endpoints per environment; sandbox acceptance suite must pass **before** production credentials are issued | `DEP-05`/`DEP-06` gates, `AC-IR001-05` |
| **Correlation IDs** | Generated at ingress (or reused from provider reference); attached to logs, metrics, queue jobs, DLQ entries, and audit entries | `NFR-014`, `INT-REQ-006` |
| **Rate-limit harmony** | Platform budgets (`SEC-REQ-009`) plus provider-imposed quotas are both enforced; provider throttles surface as metrics, not silent failures | `INT-REQ-000` shared expectations |
| **Security baseline** | HMAC + constant-time compare + IP allowlist on every inbound webhook; no secrets/OTP bodies in logs | `SEC-REQ-007`, `SEC-REQ-002` |

## 4. Graceful Degradation — when a provider is DOWN

| Provider / dependency | Detection | User-visible behavior | Platform action | Canon |
|---|---|---|---|---|
| m-Floos or OneCash (single provider) | Circuit open / timeout rate | Top-up via that provider disabled; other provider + bank transfer still offered | Ops alert; pending top-ups continue via poll/reconciliation | `INT-REQ-001` failure section |
| Both wallet providers | Both circuits open | **Top-up UI degrades to bank transfer only** (banner + FAQ text, ar/en) | Ops alert; reconciliation continues for in-flight txs | `C-05`, `INT-REQ-001`, `RISK-003` |
| SMS primary | Timeout/error on send | Automatic failover to secondary SMS — user notices nothing | DLR logged; metric incremented | `INT-REQ-003`, `AC-IR003-01` |
| Both SMS providers | Failover exhausted | **OTP falls back to WhatsApp** (`BR-NTF-03`); if WhatsApp also fails → registration/verification unavailable, honest error + retry guidance | Immediate on-call alert | `BR-NTF-03`, `AC-IR003-04`, `RISK-006` |
| WhatsApp Business | Template/API failure | Notification falls back to SMS where the category allows; OTP unaffected (SMS primary already) | DLQ + alert on persistent failure | `INT-REQ-004`, `BR-NTF-03` |
| Push (FCM/APNs) | API failure / token errors | Notification still lands in **in-app** center; security messages may fall back to SMS | Token pruning on invalid tokens | `FR-017`, `BR-NTF-02` |
| Elasticsearch (`DEP-04`) | Health/timeout | Search degraded → category browse still works | Alert; no order impact | `NFR-007`, `DEP-04` |
| Redis (`DEP-03`) | Health | Rate limits/session/cache degrade → fail-closed on auth where required; queue backlog grows | Alert (highest priority — money paths) | `NFR-007`, `BR-PLT-07` |
| MinIO (`DEP-07`) | Health | New uploads paused with clear error; existing media served from CDN cache if any | Alert | `NFR-007` |
| Prometheus/Grafana (`INT-REQ-007`) | Scrape gap | **No user impact** — observability never blocks traffic | `up == 0` alert | `NFR-007`, `INT-REQ-007` |
| Courier fleet (internal) | Engine errors | Orders remain `READY_FOR_PICKUP`; no silent auto-cancel | Ops alert | `INT-REQ-005`, `BR-ORD-10` |

Degradation is **explicit product behavior** (localized banners, honest errors), never a silent hang — availability targets stay meaningful (`C-26`, `NFR-005`).

## 5. Retry Schedule & DLQ (summary — full detail in `webhook-reliability.md`)

```text
initial attempt ──fail──► retry 1 (~1 min) ──fail──► retry 2 (~5 min) ──fail──► retry 3 (~30 min) ──fail──► DLQ + alert
                                                                        (delays: INFERENCE — stated in DOC-INT-007 §2)
```

- Handler/job failures retry **3× with exponential backoff, then DLQ**; DLQ depth is a metric **and** an alert (`BR-PLT-02`, `BR-PLT-01`).
- DLQ entries retain raw payload + correlation ID so they can be re-driven after a fix with identical idempotency guarantees (`INT-REQ-006` replay).
- The same pattern applies to alert notifications themselves (`BR-PLT-02` pattern per `INT-REQ-007`).

## 6. Security Responsibilities of the Integration Layer

| Area | Control home |
|---|---|
| Webhook authenticity (HMAC, allowlist, replay window) | `webhook-reliability.md`, `../../09-security/core/security-controls.md` |
| Provider secrets custody & rotation | `../../09-security/core/secrets-management.md` (S-04…S-07) |
| Money-effect audit entries from callbacks | `SEC-REQ-010` R2, `BR-PLT-06` |
| OTP/PII never in logs | `../../09-security/core/data-protection.md` §7 |
| Rate/abuse limits on integration endpoints | `SEC-REQ-009` budgets |
| No vendor leakage into domain | `INT-REQ-008` architecture tests |

## 7. Observability Export (`INT-REQ-007`)

| What | Examples | Where |
|---|---|---|
| RED metrics per endpoint | request rate, error ratio, duration for API + webhook routes | Prometheus scrape of internal-only `/metrics` ports |
| Integration-specific counters | provider send success/fail, failover count, callback verify failures (401s), circuit state, DLR latency | Prometheus, label allowlist only |
| Queue/DLQ depth | `b07.wallet.credit`, `b10.notification.delivery`, DLQ sizes | Prometheus → alert (`BR-PLT-02`) |
| Reconciliation mismatches | ledger vs provider statement deltas (`DATA-REQ-006`) | Prometheus → finance alert |
| Rate-limit signals | 429 counts per route (`SEC-REQ-009` R5) | Prometheus → abuse alert |
| Dashboards | per-provider health, queue/DLQ, database, reconciliation status | Grafana |
| Alert routing | severity-based routing to on-call; alert transport itself uses 3 retries + DLQ pattern | Alertmanager-style routing |

**Hard rules:** metrics endpoints bound to internal networks only; **no PII, phone numbers, tokens, or secrets** in labels or log payloads (`AC-IR007-03`); observability failure never blocks user traffic (`NFR-007`).

## 8. Verification

| Property | Test |
|---|---|
| No vendor leakage | import/lint scan + static scan for vendor identifiers (`AC-IR008-01/03`) |
| Substitution | mock adapter swap with zero domain edits (`AC-IR008-02`) |
| Contract parity | identical suite across mock/provider A/provider B (`AC-IR008-04`) |
| Degradation | provider-down simulations per `testing-and-sandboxes.md` |
| Observability | `up == 1`, alert fire drill, PII scrub of exports (`AC-IR007-01…03`) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | Monitored queue name corrected: `b10.notification.send` → `b10.notification.delivery` (`b07.wallet.credit` now registered in §1) | `REC-06`/`TD-07` pay-down |


