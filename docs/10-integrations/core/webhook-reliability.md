---
document_id: DOC-INT-007
title: Webhook Reliability — Inbound & Outbound Contract
category: 10-integrations
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [INT-REQ-006, INT-REQ-001, INT-REQ-003, INT-REQ-004, FR-013, FR-017]
related_documents: [DOC-INT-000, DOC-INT-001, DOC-INT-002, DOC-IR-006, DOC-BA-005, DOC-SEC-008]
---

# Webhook Reliability (`INT-REQ-006`)

Design for every webhook yumn receives (providers → yumn) and sends (yumn → downstream consumers). Rule of record: **`BR-PLT-02`** — jobs retry 3× with exponential backoff, then DLQ; DLQ depth triggers an alert (`BR-PLT-01`). Goal: *verify → persist → process idempotently, never lose an event, never trust an unverified one.*

## 1. Inbound Webhooks (providers → yumn)

Sources: m-Floos/OneCash payment callbacks, SMS delivery receipts (DLRs), WhatsApp status updates (`INT-REQ-001/003/004`).

### 1.1 Processing pattern: verify → persist → 200 → process

```text
POST /webhooks/{provider}
 1. size/CT checks            → reject 413/415 before parsing
 2. IP allowlist              → reject 403 (unknown source)
 3. HMAC over RAW body        → constant-time compare → reject 401 + security metric
 4. timestamp within window   → reject 401 (expired)  [replay guard, §1.2]
 5. persist raw payload + headers + source IP + received_at + correlationId
 6. respond 200  (total ≤ 10 s; realistically < 1 s — persist-then-ack)
 7. enqueue job → domain handler (idempotent, §1.4) with retries (§2)
```

- **200 only after durable persistence** — slow business logic never blocks the provider callback path (`AC-IR006-04`).
- Malformed payload after verification → `422`, logged, **no partial processing**.
- Invalid signature → `401`, dropped, counter incremented (`AC-IR006-02`).

### 1.2 Signature, timestamp & replay protection

| Control | Design | Canon |
|---|---|---|
| Signature | HMAC-SHA256 over the raw request body with the provider's webhook secret, constant-time comparison | `INT-REQ-006` security |
| Timestamp window | Signature covers a timestamp header; requests outside **±5 minutes** of server time are rejected (`INFERENCE` — window length is a design parameter, not in canon; tracked `SEC-005`) | `INT-REQ-006` "replay window" |
| Nonce / duplicate guard | Provider transaction/message ID persisted at step 5; a repeat within/after the window short-circuits to `200` with **no reprocessing** | `BR-PLT-03`, `AC-IR006-01` |
| Allowlist | Per-provider source IP ranges; reviewed when providers change | `INT-REQ-006` security, `INT-REQ-001` |
| Secrets | Webhook secrets from environment only; dual-secret grace period supported if the provider allows rotation (`INFERENCE`) | `SEC-REQ-007` (S-05) |
| Forensics | Raw body + headers + IP + timestamp retained for investigation; secrets and OTP bodies redacted from any log view | `INT-REQ-006` data exchanged, `SEC-REQ-002` |

### 1.3 Idempotency keys

- The **provider transaction/message ID is the idempotency key** (`BR-PLT-03`); N deliveries → exactly **one** domain effect (`AC-IR006-01`).
- Money paths additionally carry the platform idempotency key so a webhook credit and a poll credit cannot both post (`BR-PAY-08`, `wallet-providers.md` §5).
- Idempotency is enforced at the **database** (unique constraint), not only in memory — replicas and restarts must not weaken it (`DATA-REQ-001`).

### 1.4 Handler retries & DLQ (inbound processing)

| Stage | Behavior |
|---|---|
| Handler failure | Retry 3× with exponential backoff: **~1 min → ~5 min → ~30 min** (`INFERENCE` — canon fixes "3 retries + exponential backoff + DLQ" in `BR-PLT-02`, not the exact delays; chosen so transient provider/db issues self-heal within an hour) |
| Exhausted | Entry → **DLQ** with raw payload + error + correlation ID; alert fires (`BR-PLT-01`) |
| Admin replay | DLQ console (admin-only, `FR-020`) lists entries; an admin can **re-drive** a stored payload after a fix with identical idempotency guarantees (`INT-REQ-006` replay) — replay writes an audit entry (`SEC-REQ-010` R2) and is deny-by-default RBAC (`rbac.md`) |
| Poison messages | A payload that fails deserialization is `422`'d at ingress and never enqueued; a payload failing at domain level lands in DLQ after retries |

### 1.5 Ordering caveats

| Reality | Handling |
|---|---|
| Providers retry aggressively → duplicates and reordering are normal | Idempotency + status-machine guards make order irrelevant for correctness (`AC-IR006-01` includes out-of-order delivery) |
| No global ordering guarantee across providers or partitions | Domain handlers validate *current state* before acting; invalid transitions → `409 STATE_CONFLICT`-style no-op, not corruption (`INT-REQ-005` optimistic versioning pattern) |
| Late callbacks (after poll-based finalization) | Treated as idempotent no-ops or routed to reconciliation (`wallet-providers.md` §6) |
| Concurrency on the same entity | Optimistic `version` locking / row locks inside the ACID tx (`BR-PLT-04`) |

## 2. Outbound Retries (yumn → its own queues/consumers)

The same schedule governs BullMQ jobs that process webhooks and produce notifications (`BR-PLT-02`):

```text
initial attempt ──fail──► retry 1 (~1 min) ──fail──► retry 2 (~5 min) ──fail──► retry 3 (~30 min) ──fail──► DLQ + alert
```

- **Schedule of record: 3 retries with exponential backoff at ~1 min, ~5 min, ~30 min after the initial attempt, then DLQ** (delays `INFERENCE`; the "3 retries then DLQ" structure is `VERIFIED` in `BR-PLT-02`).
- Queue naming `{block}.{entity}.{action}` (`BR-PLT-01`); money jobs run inside ACID transactions with compensating actions (`BR-PLT-04`).

## 3. Outbound Webhooks (yumn → consumers, if any)

yumn has no mandatory outbound webhook consumers in v1 (vendor panel is in-app; there is no third-party seller API in scope). The contract is defined so it can be enabled without redesign (`INFERENCE` on the need; contract is design-level):

| Property | Rule |
|---|---|
| Signing | HMAC-SHA256 with a per-consumer secret + timestamp header — same scheme as inbound (symmetric expectations) |
| Retries | identical schedule: 3× exponential → DLQ → consumer-visible failure state |
| Idempotency | every delivery carries a stable event ID so consumers can dedupe |
| Secrets | per-consumer secret, rotatable with dual-secret grace; environment only (`SEC-REQ-007`) |
| Ordering | per-entity ordering attempted; consumers are documented as idempotency-required |

## 4. Monitoring & Alerting (DLQ depth)

| Signal | Source | Action |
|---|---|---|
| **DLQ depth > 0** (per queue) | BullMQ metrics → Prometheus | **Alert to on-call** — never a silent backlog (`BR-PLT-02`, `AC-IR006-03`) |
| DLQ depth growth rate | Prometheus | Page if growing during a provider incident |
| Webhook 401 rate (bad signature) | app metrics | Security alert — forgery/secret-rotation indicator (`AC-IR006-02`) |
| Ingress persistence latency | RED metrics | Warn if ack approaches the 10 s bound (`AC-IR006-04`) |
| Callback-to-credit latency (money path) | correlation IDs | Alert on p95 breaching design target; feeds reconciliation |
| Retry exhaustion count | queue metrics | Correlate with provider status page/incidents |
| Replay actions | audit log | Reviewed as privileged actions (`SEC-REQ-010`) |

Dashboards: queue/DLQ depth and per-provider callback health are required panels (`INT-REQ-007`, `AC-IR007-04`). Alert transport itself follows the 3× + DLQ pattern (`INT-REQ-007`).

## 5. Failure Matrix (inbound)

| Failure | Response | Effect |
|---|---|---|
| Unknown source IP | 403 | none |
| Bad/expired signature | 401 + metric | none (`AC-IR006-02`) |
| Oversized/non-JSON body | 413/415 | none |
| Valid but malformed payload | 422 + log | none (no partial processing) |
| Valid, duplicate | 200 | no-op (`AC-IR006-01`) |
| Valid, handler bug | retries → DLQ + alert | delayed, then replayable (`AC-IR006-03`) |
| Provider spams retries | idempotent short-circuit at persistence step | safe |
| Provider stops retrying (callback lost) | poll/reconciliation job finalizes (`wallet-providers.md`, `INT-REQ-001`) | event never lost |

## 6. Verification

| Test | Assertion | Canon |
|---|---|---|
| Idempotency | same webhook 3× and out-of-order → one effect, one ledger credit | `AC-IR006-01` |
| Forgery | tampered payload / wrong signature → 401, metric, zero effect | `AC-IR006-02` |
| Retry path | always-failing handler → 3 retries with increasing backoff → DLQ → alert | `AC-IR006-03` |
| Timeliness | persist + ack within 10 s under load | `AC-IR006-04` |
| Replay | DLQ replay after fix produces the same idempotent outcome | `INT-REQ-006` replay |
| Alerting | DLQ depth increase fires an on-call alert | `AC-IR007-02` pattern |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
