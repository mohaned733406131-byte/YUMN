---
document_id: DOC-OPS-006
title: Monitoring & Observability Stack (How Signals Are Run)
category: 14-devops-infrastructure
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-014, NFR-005, NFR-020, INT-REQ-007, SEC-REQ-010, DATA-REQ-004]
related_documents: [DOC-NFD-006, DOC-NFD-004, DOC-OPS-001, DOC-OPS-003, DOC-OPS-007, DOC-SEC-005, DOC-DTA-005]
---

# Monitoring & Observability Stack — Execution

**What** to observe is canon in `12-non-functional/observability.md` (DOC-NFD-006): signal schema, metric catalog, the 12-dashboard inventory, alert severities and thresholds, the top-10 runbooks. **How** those signals are collected, stored, routed and retained is this document. Nothing here invents a threshold; everything here makes an existing threshold measurable (`INT-REQ-007`).

## 1. Stack Placement (single host, `C-22`)

| Component | Service | Role |
|---|---|---|
| Prometheus | `prometheus` | Scrapes every target; evaluates alert rules; long-term TSDB |
| Alertmanager | `alertmanager` | Dedupe, group, silence, **route by severity** to receivers |
| Grafana | `grafana` | Dashboards (12), alert UI, log exploration |
| Loki | `loki` | Log aggregation store (§6) |
| Promtail | `promtail` (Docker log driver or sidecar) | Ships container stdout JSON into Loki |
| Blackbox exporter | `blackbox` | HTTP/TCP probes for uptime + internal endpoint checks |
| Node exporter | `node-exporter` | Host CPU/mem/disk/FD metrics |
| Postgres exporter | `postgres-exporter` | DB metrics (pool, WAL, locks, lag) |
| Redis exporter | `redis-exporter` | Hit ratio, evictions, memory |
| Elasticsearch exporter | `es-exporter` | Cluster health, indexing lag |
| cAdvisor | `cadvisor` | Container CPU/mem/restarts |

No SaaS monitoring dependency — `NFR-016` forbids cloud-vendor lock-in; an external uptime prober is the one deliberate exception (§5) because a monitor inside the host cannot see host failure (`DOC-NFD-004` §1).

## 2. Prometheus Scrape Configuration

```yaml
scrape_configs:
  - job_name: api
    metrics_path: /metrics
    scrape_interval: 15s
    static_configs: [{ targets: ["api:3000"], labels: { service: "api" } }]
  - job_name: worker
    scrape_interval: 15s
    static_configs: [{ targets: ["worker:3000"], labels: { service: "worker" } }]
  - job_name: node
    static_configs: [{ targets: ["node-exporter:9100"] }]
  - job_name: postgres
    static_configs: [{ targets: ["postgres-exporter:9187"] }]
  - job_name: redis
    static_configs: [{ targets: ["redis-exporter:9121"] }]
  - job_name: elasticsearch
    static_configs: [{ targets: ["es-exporter:9114"] }]
  - job_name: bullmq
    scrape_interval: 15s
    metrics_path: /metrics
    static_configs: [{ targets: ["worker:3000"], labels: { source: "bullmq" } }]
  - job_name: minio
    static_configs: [{ targets: ["minio:9000"] }]
  - job_name: cadvisor
    static_configs: [{ targets: ["cadvisor:8080"] }]
  - job_name: blackbox-http
    metrics_path: /probe
    params: { module: [http_2xx] }
    static_configs:
      - targets: ["http://web:3000/", "http://api:3000/healthz", "http://api:3000/readyz"]
  - job_name: self
    static_configs: [{ targets: ["prometheus:9090"] }]
```

| Job | Feeds (metric classes from `DOC-NFD-006` §3) |
|---|---|
| `api` | RED HTTP (100% of endpoints), error classes, correlation of deploy markers |
| `worker` + `bullmq` | queue depth per `{block}.{entity}.{action}` (`BR-PLT-01`), DLQ depth, retries, failures, drain time, worker heartbeat |
| `node` | CPU, memory, disk, disk-forecast, open FDs |
| `postgres` | pool utilization, wait p95, query duration, connections, WAL rate |
| `redis` | hit ratio, evictions, memory, `cache_requests_total{hit|miss}` |
| `elasticsearch` | cluster health, query p95, indexing lag |
| `minio` | capacity, request errors |
| `blackbox-http` | availability SLI (successful probes / total, `DOC-NFD-004` §7) |
| `self` | monitoring-plane health (dead-man's-switch source) |

Every alert rule declared in `DOC-NFD-006` §6 has a corresponding Prometheus rule file under `infra/monitoring/rules/`; the alert/dashboard coverage diff job (`AC-S-18`) fails CI when a critical signal lacks a rule.

## 3. Grafana Dashboard Provisioning

Dashboards are **code**: JSON in `infra/monitoring/dashboards/`, provisioned at container start; the Grafana volume is cache only (`DOC-OPS-003` §4). The inventory mirrors `DOC-NFD-006` §5 one-for-one:

| # | Dashboard | PromQL / data source | Audience |
|---|---|---|---|
| 1 | Global / SLO | `blackbox` availability vs 99.99%, error-budget burn, MTTD/MTTR, deploy markers | on-call lead, sponsor |
| 2 | Latency (per surface S1–S5) | `histogram_quantile` over `http_request_duration_seconds` | on-call |
| 3 | Errors | `rate(http_errors_total[5m])`, top failing routes | on-call |
| 4 | Resources | `node`, `cadvisor`, container health/restarts | on-call |
| 5 | PostgreSQL | pool, locks, WAL rate, slow queries | on-call |
| 6 | Redis | hit ratio, evictions, memory | on-call |
| 7 | Queues/workers | BullMQ depth, DLQ, retries, drain time | on-call |
| 8 | Integrations | per-provider latency/error, SMS vs WhatsApp delivery | integrations owner |
| 9 | Business | orders by status, GMV, wallet/escrow flows (0 PII labels) | ops, business |
| 10 | Search | ES query p95, indexing lag, fallback-mode flag | on-call |
| 11 | Security/auth | OTP rates, lockouts, 429s, anomalous logins | security on-call |
| 12 | Frontend RUM | p75 Core Web Vitals by route/locale | frontend owner |

Datasources (Prometheus, Loki) are provisioned identically in every environment; only the URL differs.

## 4. Alertmanager Routing (severity → channel)

Routing is configuration in `infra/monitoring/alertmanager.yml`; thresholds stay in `DOC-NFD-006` §6.

| Severity | Meaning | Primary receiver | Secondary | Ack SLA |
|---|---|---|---|---|
| **P1 (page)** | user-facing impact, money or availability risk now | On-call phone push (ntfy/Telegram/PagerDuty-class channel chosen at launch, `DEP-06` channel inventory) | — | page ≤ **1 min**, ack ≤ **15 min** (`AC-NFR-014-02`) |
| **P2 (urgent)** | degraded, no immediate outage | Team chat channel | auto-ticket | ack ≤ 1 h |
| **P3 (ticket)** | trend / hygiene | Ticket queue | — | next business day |
| **P4 (info)** | annotation only | Dashboard marker | — | none |

Routing rules:

```text
route:
  group_by: [alertname, severity, service]
  group_wait: 30s          # P1 pages fast; grouping only collapses duplicates
  group_interval: 5m
  repeat_interval: 4h      # P1 repeats every 30 min until resolved
  receivers:
    - when: severity = "backup_failed"        → ops owner + P1 page
    - when: severity = "page"                 → on-call pager
    - when: severity = "urgent"               → chat + ticket
    - when: severity = "ticket"               → ticket
    - when: severity = "info"                 → null (dashboard marker)
inhibit_rules:                                 # a P1 suppresses its own P2/P3 children
  - source: { severity: page }   target: { severity: [ticket, urgent] }
```

Operational rules: every **P1** links a runbook section (`DOC-NFD-006` §7); a **dead-man's-switch** alert (`watchdog`) fires weekly to prove the paging path itself works; silences require an expiry ≤ 8 h and a reason; alert inventory diff is the deliverable of `AC-S-18`.

### 4.1 Backup-specific routing

Backup freshness failures are first-class P1s (`DATA-REQ-004` R2): `backup-check.yml` and Prometheus rules alert when **WAL age > 15 min** or **snapshot age > 24 h** (`AC-NFR-006-02`), routed to `backup_failed` → ops owner + page.

## 5. Uptime Checks (external synthetics)

| Check | Target | Interval | Source | Purpose |
|---|---|---|---|---|
| External HTTPS probe | `https://yumn.ye/` (customer storefront) | 60 s | Third-party uptime service (external to the host) | Availability SLI for `AC-NFR-005-01` — an in-host monitor cannot detect host loss |
| External API probe | `https://api.yumn.ye/api/v1/healthz` | 60 s | same | Liveness from the internet's point of view |
| Login-flow synthetic | register→OTP→login against a dedicated synthetic account | 5 min | same | Catches "process up, app broken" |
| Internal probe | `/readyz`, `/healthz` on `api`, `/` on `web` | 15 s | `blackbox` inside the host | Fast MTTD (≤ 1 min, `AC-NFR-005-02`) |
| TLS expiry probe | edge certificate | daily | `blackbox` | Pre-expiry alert (`SEC-REQ-006` R4) |

Two consecutive failed probes ⇒ alert within 1 minute; partial degradation (e.g. ES down with browse fallback) is **not** downtime but is alerted as degraded (`DOC-NFD-004` §1).

## 6. Log Pipeline — Collection, Storage, Query

**Decision: Docker `json-file` (rotated) → Promtail → Grafana Loki → Grafana Explore.**

| Option | Verdict | Why |
|---|---|---|
| `json-file` + `docker logs` viewer only | Rejected as the *sole* answer | Cannot satisfy `NFR-014`'s **≥ 30 days hot, queryable** logs with correlation-ID search across `api`/`worker`/`web`; `docker logs` is unindexed and lost on container replacement |
| ELK (Elasticsearch + Logstash + Kibana) | Rejected | Three extra heavyweight services for logs; ES is already sized for search, not log volume; operational cost contradicts `C-21`/`C-22` simplicity |
| **Loki (chosen)** | Selected | Single small container, label-based indexing (cheap), ships into the **existing** Grafana, satisfies 30-day hot queryable logs and `requestId` search; no new UI to learn |

Pipeline: `stdout → Docker json-file (rotated) → Promtail (Docker discovery) → Loki (stream labels: service, env, level, module) → Grafana Explore / dashboards`.

| Rule | Detail |
|---|---|
| Label cardinality | Loki labels are low-cardinality only (`service`, `env`, `level`, `module`); **`requestId` and `userId` are indexed fields in the log body, never labels** |
| Redaction before ship | Promtail drops/scrubs forbidden fields per `DOC-NFD-006` §2 allowlist; secrets never leave the host |
| Audit-grade money lines | Additionally written to the DB audit trail (`BR-PLT-06`, `SEC-REQ-010`) — **the log store is never the audit system of record** |
| Query example | `{service="api"} \|= "requestId" \|= "<uuid>"` — Loki is optional in `local`; `docker logs <service>` suffices for the developer loop |

## 7. Retention of Metrics & Logs

| Signal | Store | Hot/queryable retention | Archive | Source |
|---|---|---|---|---|
| Application logs (no PII by rule) | Loki | **30 days** hot (`NFR-014` minimum) | none | `DOC-DTA-005` `RC-02` (90 d non-security logs) → shipped to cold file archive, then aged out |
| Audit-grade money log lines | PostgreSQL audit trail | **10 years** (`INFERENCE`) | cold partition | `RC-06`, `NFR-019` |
| Metrics series | Prometheus TSDB | **13 months** (year-over-year comparison) | none | `RC-03` |
| Traces (sampled) | OTel-compatible backend, 7 d sampled | 7 days | none | `DOC-NFD-006` §1 |
| Business metrics | Prometheus counters | 30 days hot + 13-month series | none | `DOC-NFD-006` §1 |
| Alert history + CI run logs | Alertmanager annotations; GitHub Actions runs | 90 days | none | `RC-02` |
| Container json-file files | Docker rotation (10 MB × 5 per container) | hours–days | none | crash forensics only |

Retention is configured in `infra/monitoring/` and verified by the weekly config review; changing a period is a config change, not a code release (`DATA-REQ-003` R1).

## 8. What Is NOT Monitored in v1 (honest scope)

| Not monitored | Why | Compensating control |
|---|---|---|
| Multi-host / cross-region health | v1 is a single host per environment (`C-22`) — there is no second host to compare | External uptime prober + RTO/RPO restore (`DOC-OPS-007`) |
| Per-kernel-interrupt / hardware health (RAID, SMART, ECC) | Cloud VM assumption; provider owns hardware | Disk-forecast alert; provider status page watch (`INFERENCE`) |
| Distributed tracing of third-party outbound spans beyond logged attributes | Provider APIs do not propagate `traceparent` reliably | Per-provider latency/error metrics + integration dashboard |
| Mobile client crashes / native ANR | Separate RN release train; no crash-reporting SDK committed in v1 | Store review feedback + support tickets (`FR-020`) |
| Cost / billing metrics | Single-VM footprint tracked manually | Monthly ops review (`INFERENCE`) |
| Database query *plans* in production continuously | Expensive; CI compares plans on a seeded staging DB instead | `08-database/indexes-and-performance.md` §2 regression gate |
| Email channel | No email channel in v1 (`BR-NTF-01`) | n/a |
| PII-level user journey analytics | Privacy minimization (`DATA-REQ-002`); metrics carry no PII labels | Aggregate business metrics only |

Residual availability risk (single host, no HA failover) is **declared**, not hidden: `12-non-functional/reliability.md` §3. Monitoring detects fast; recovery is bounded by RTO ≤ 1 h — it does not eliminate host loss.

## 9. Verification

| Check | Method | Evidence |
|---|---|---|
| All targets scraped | Prometheus "targets" page all UP; CI smoke | `AC-IR007-01` |
| Dashboards render | Grafana provisioning log + screenshot in release record | `AC-S-18` |
| Alert routes to on-call | Staged alert drill; measure page ≤ 1 min, ack ≤ 15 min | `AC-NFR-014-02` |
| Coverage diff | Job asserts every endpoint has RED metrics **and** a dashboard row | `AC-S-18` |
| Dead-man's-switch | Weekly `watchdog` check in the alert inventory | `DOC-NFD-006` §6 |
| Backup alerts fire | Failure-injection test on a backup run | `AC-DR004-02` |
| No secrets in logs | Rolling 1,000-line audit script (daily) | `AC-NFR-014-01` |
| Retention matches schedule | Config review against `DOC-DTA-005` §4 | `RC-02/03` evidence |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
