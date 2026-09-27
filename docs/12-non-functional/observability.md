---
document_id: DOC-NFD-006
title: Observability Detail — Signals, Dashboards, Alerting & Runbooks
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-014, NFR-020, NFR-005, NFR-007, NFR-008, NFR-017, INT-REQ-007, SEC-REQ-010, FR-020]
related_documents: [DOC-NFD-001, DOC-NFR-014, DOC-NFR-020, DOC-AC-001, DOC-NFD-002, DOC-NFD-003, DOC-NFD-004]
---

# Observability Detail — Signals, Dashboards, Alerting & Runbooks

Elaborates **NFR-014 (logging/metrics/tracing)**, the telemetry half of **NFR-020 (supportability)** and the export contract **`INT-REQ-007`**. Stated targets (100% correlation-ID coverage, 100% RED coverage, ≤ 1 min page / ≤ 15 min ack, 30 d hot logs) are inherited unchanged; this file fixes the field schema, metric catalog, dashboard inventory, alert rules and runbook wiring that make them real. Acceptance: `AC-NFR-014-01/02`, `AC-NFR-020-01`, `AC-S-18`.

## 1. Signal Model (three pillars + business layer)

| Pillar | Scope | Storage | Retention |
|---|---|---|---|
| **Logs** | 100% backend output, structured JSON (§2) | log store (Loki/ELK-class — tooling choice in `14-devops-infrastructure/`) | hot/queryable **≥ 30 d** (`NFR-014`); audit-grade money records **≥ 5 y** (`NFR-019`) |
| **Metrics** | RED/USE per §3, 15 s scrape | Prometheus (2-week local + longer in Thanos-class tier `INFERENCE`) | per `INT-REQ-007` |
| **Traces** | correlation-ID-propagated request spans across HTTP → DB → Redis → BullMQ → outbound calls | trace backend (OTel-compatible) | 7 d sampled (§4) |
| **Business metrics** | orders, GMV, wallet ops, escrow — dashboards only, 0 PII | Prometheus counters | 30 d |

Tool stack (`INT-REQ-007`): Prometheus + Grafana for metrics, structured log store, alert route to on-call (PagerDuty/Telegram/ntfy-class per launch channel inventory `DEP-06`).

## 2. Log Schema & Redaction

Fixed field schema — **100% of backend log lines**, 0 unstructured lines per 1,000-line production sample (`AC-NFR-014-01`):

```json
{"ts":"ISO8601","level":"error|warn|info|debug","service":"api|worker|web",
 "module":"b07.wallet","requestId":"uuid","userId":"optional","msg":"..."}
```

| Rule | Detail |
|---|---|
| Correlation | `requestId` generated at the **edge**, propagated through NestJS handlers **and BullMQ jobs** (header → job payload → child job), present on every related line — 100% coverage |
| Block tagging | `module` carries the `bNN.entity` of origin (e.g., `b09.payments`) — enables per-block log dashboards and the 13-block ownership model (`DOC-OVR-009`) |
| Money audit entries | 100% of payment/escrow/payout ops write before/after audit lines (`BR-PLT-06`, `SEC-REQ-010`) with actor, delta, before/after balance fields — these lines are **audit-grade** (5-y retention, §1) |
| Redaction | passwords, OTPs, tokens, card/IBAN-like values, full phone numbers masked (`BR-AUTH-02`, `SEC-REQ-007`); redaction is schema-level allow-list, not regex guesswork (`INFERENCE`) |
| PII | logs store `userId`/masked phone only — never addresses/ID documents (those live in DB + audit trail) |
| Sample audit script | validates JSON schema + secret absence on a rolling 1,000-line extract (NFR-014 measurement method) — runs daily in CI |

## 3. Metric Catalog

| Class | Metrics | Labels | Scrape |
|---|---|---|---|
| **RED — HTTP** (100% of endpoints) | `http_requests_total`, `http_request_duration_seconds` (histogram: 25/50/90/95/99 buckets around §`DOC-NFD-002` budgets), `http_errors_total{class=5xx|4xx|timeout}` | route, method, status, surface (S1–S5) | 15 s |
| **DB** | pool utilization, wait p95, query duration by class, connections, WAL rate, replication lag | — | 15 s (`DEP-02`) |
| **Redis** | hit ratio, evictions, memory, CPU, `cache_requests_total{hit|miss}` | — | 15 s (`DEP-03`) |
| **Queues** | BullMQ depth per `{block}.{entity}.{action}` queue, DLQ depth, job duration, retries, failures | queue | 15 s |
| **Workers** | jobs/s, failure rate, drain time | job type | 15 s |
| **Integrations** | outbound latency + error rate per provider (SMS, WhatsApp, m-Floos, OneCash, maps) | provider, endpoint | 15 s (`INT-REQ-007`) |
| **Business** | `orders_created_total{status}`, `wallet_ops_total{type}`, `escrow_released_total`, `otp_sent/delivered_total{channel}` | — | 15 s |
| **Client RUM** | p75 LCP/INP/CLS by route/locale/device, JS bundle size | route, locale | sampled 5% (`INFERENCE`) |
| **Process/host** | CPU, memory, disk, disk-forecast, open FDs | host | 15 s |

Rule: **every critical signal has an alert rule** and **every alert rule has a dashboard panel** — coverage diff job fails CI if an endpoint has RED metrics but no dashboard row (`AC-S-18`).

## 4. Tracing & Correlation

- One `requestId` = one trace root at the edge; spans: handler → DB query → Redis → queue enqueue → (worker consumer span, linked via job parent) → outbound provider calls.
- W3C `traceparent` propagated outbound to third parties where supported; otherwise logged as span attribute (`INFERENCE`).
- Sampling: **100% of error traces + money traces kept; 10% of successful read traffic** (`INFERENCE`) — always 100% of payment/escrow/payout spans for auditability.
- Trace UI deep-links attached to alert annotations → diagnosis starts from the alert, not from SSH.

## 5. Dashboard Inventory (Grafana)

| # | Dashboard | Key panels | Audience |
|---|---|---|---|
| 1 | **Global / SLO** | availability vs 99.99%, error budget burn (30 d), MTTD/MTTR, deploy markers | on-call lead, sponsor |
| 2 | **Latency (per surface S1–S5)** | p50/p95/p99 per endpoint class vs budgets | on-call |
| 3 | **Errors** | 5xx/4xx rate, top failing routes, uncaught exceptions | on-call |
| 4 | **Resources** | CPU/mem/disk/forecasts, pool utilization, containers healthy | on-call |
| 5 | **PostgreSQL** | queries, locks, WAL, lag, slow queries | on-call, DBA-role |
| 6 | **Redis** | hit ratio, evictions, memory, hit p95 | on-call |
| 7 | **Queues/workers** | depth, DLQ, retries, drain time | on-call |
| 8 | **Integrations** | per-provider latency, error, SMS vs WhatsApp delivery | on-call, integrations owner |
| 9 | **Business** | orders by status, GMV, wallet/escrow flows, conversion funnel | ops, business |
| 10 | **Search** | ES query p95, indexing lag, fallback-mode flag | on-call |
| 11 | **Security/auth** | OTP send/verify/fail rates, lockouts, 429s, anomalous logins | security on-call |
| 12 | **Frontend RUM** | p75 Core Web Vitals by route/locale/device | frontend owner |

## 6. Alert Rules (severity → route → action)

| Sev | Meaning | Route | Examples (thresholds) |
|---|---|---|---|
| **P1 (page)** | user-facing impact or money/availability risk now | on-call phone push; **page ≤ 1 min** after condition; ack ≤ **15 min** (`AC-NFR-014-02`) | availability probe fail × 2; error rate > 1% 5 min; write p95 > budget 2 min; DLQ depth > 0; DB pool > 95%; backup age > 15 min; disk > 85%; OTP delivery < 95%; callback mismatch |
| **P2 (urgent)** | degraded, no immediate outage | chat channel + ticket; ack ≤ 1 h | cache hit ratio < 80% 30 min; search fallback mode active > 5 min; error budget burn > 2×; provider p95 > budget; disk > 70% |
| **P3 (ticket)** | trend / hygiene | ticket, next business day | slow-query regression; dependency CVE; doc-freshness failure; coverage drop |
| **P4 (info)** | annotation-only | dashboard marker | deploys, drills, feature-flag toggles |

Alert hygiene: multi-window burn-rate alerts for SLO (avoid flapping); every P1 has a linked runbook section (§7); dead-man's-switch alert proves the paging path itself works weekly; alert inventory diff = deliverable of `AC-S-18`.

## 7. Runbooks (NFR-020 / `AC-S-19`)

Top-10 operational incidents, each with **symptom → diagnosis → mitigation → escalation**, rehearsed at least once:

1. API latency/errors spike → §`DOC-NFD-002` §8 shedding ladder.
2. Database pool saturation / lock storm.
3. PostgreSQL primary failover/restore → `DOC-NFD-004` §6 PITR path (RTO ≤ 1 h).
4. Redis down (cache/session) → fallback expectations, restore steps.
5. Queue backlog / DLQ growth → replay + drain ≤ 5 min.
6. SMS/WhatsApp OTP delivery failure → provider failover (BR-NTF-03), manual re-trigger.
7. Payment provider outage/degraded callback → reconciliation poll, top-up fallback (BR-PAY-04).
8. Disk capacity / forecast breach → retention job, partition check (`DOC-NFD-003` §5).
9. Failed deploy → rollback ≤ 15 min (§8), 0 failed requests.
10. Security incident (secret leak, OTP abuse) → rotate `SEC-REQ-007`, lockout review, audit extraction.

Each runbook cites the metrics/dashboards (§5–§6) that confirm each step; ownership per block module (`DOC-OVR-009`); rehearsal log = evidence for `AC-NFR-020-01`/`AC-S-19`.

## 8. Health, Deploy & Rollback Telemetry (NFR-020 mechanics)

| Mechanism | Spec |
|---|---|
| `/healthz` (liveness) | < 1 s response, no dependency checks — container restart gate |
| `/readyz` (readiness) | < 1 s; checks DB + Redis + queue readiness; **unhealthy instance removed from LB rotation ≤ 30 s** (`BR-PLT-07`) |
| Deploy observation window | staging: 5-min window, 5xx spike **< 0.1%**, 0 failed customer requests (`AC-NFR-020-02`) |
| Rollback | rehearsed ≤ **15 min** with error monitoring live during window; evidence recorded (`AC-S-20`) |
| Migrations | expand-contract only (§`DOC-NFD-005` §1, `DATA-REQ-005`) — migration failure visible as job failure alert, never silent |
| Correlation on deploys | deploy marker panel overlay (§5 dashboards #1–#3) to attribute regressions |

## 9. Verification Hooks

| Detail | Feeds AC |
|---|---|
| §2 schema + correlation end-to-end (HTTP → queue → response) + redaction sample | `AC-NFR-014-01` |
| §3 RED coverage diff = every endpoint; §6 drill measures page ≤ 1 min, ack ≤ 15 min | `AC-NFR-014-02`, `AC-S-18` |
| §5 dashboard inventory + §6 alert inventory complete (every critical signal alertable) | `AC-S-18`, `AC-S-19` |
| §7 top-10 runbooks exist + rehearsal log | `AC-NFR-020-01`, `AC-S-19` |
| §8 health timing, rotation ≤ 30 s, config/secret audit | `AC-NFR-020-01` |
| §8 deploy 0 failed requests; rollback ≤ 15 min | `AC-NFR-020-02`, `AC-S-20` |
| §1 audit retention ≥ 5 y for money entries | `NFR-019`, `SEC-REQ-010`, `OBJ-08` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
