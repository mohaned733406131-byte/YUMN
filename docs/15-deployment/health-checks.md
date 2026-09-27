---
document_id: DOC-DPL-005
title: Health Checks & Readiness Model
category: 15-deployment
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-005, NFR-007, NFR-020, INT-REQ-007]
related_documents: [DOC-ARCH-005, DOC-OPS-003, DOC-OPS-006, DOC-NFD-006, DOC-NFD-004, DOC-INT-001, DOC-API-001]
---

# Health Checks & Readiness Model

Two probes, two questions: **is the process alive?** (`/healthz`) and **should it receive traffic?** (`/readyz`). Both must respond in **< 1 s**; an instance leaving rotation must be removed in **≤ 30 s** (`BR-PLT-07`, `NFR-020`, `AC-NFR-020-01`).

## 1. Endpoint Definitions

| Endpoint | Question | Checks | Response | Consumers |
|---|---|---|---|---|
| `GET /healthz` | Is the process alive? | **None** — process up, event loop responsive | `200 { status: "UP", version, uptimeSeconds }` · `503 SERVICE_UNAVAILABLE` during shutdown | Compose healthcheck (restart gate), edge liveness, uptime prober |
| `GET /readyz` | Should this instance serve requests? | Postgres, Redis, BullMQ readiness; **Elasticsearch and providers are reported but non-gating** | `200 { status: "READY", checks: [ { name, status, latencyMs } ] }` · `503` when a **required** check is DOWN | Edge upstream gate, LB rotation, deploy smoke, Prometheus probe |

| Rule | Detail |
|---|---|
| No dependency checks on `/healthz` | A DB outage must not cause a restart loop of healthy app processes |
| `503` never leaks internals | Response carries check **names** only — no hostnames, ports, credentials (`SEC-REQ-008`) |
| Shutdown awareness | During SIGTERM drain `/healthz` returns 503 so the edge stops routing to the draining instance |
| Timing budget | Each probe ≤ 1 s total; individual dependency checks have a **150 ms budget** and are executed concurrently (`INFERENCE`) |
| Version in payload | `version` = image tag/commit, so smoke tests can assert the deployed build |

### 1.1 Path naming note (open reconciliation)

Infrastructure probes use **`/healthz`** and **`/readyz`** — the paths fixed by `BR-PLT-07`, `NFR-005`, `NFR-020`, `04-architecture/deployment-view.md`, and `13-testing/test-cases/TC-001.md`. The API endpoint register specifies the same two checks at `GET /health/live` (API-ADM-042) and `GET /health/ready` (API-ADM-043) with identical semantics. The API therefore serves **both** path spellings during v1; a single spelling must be chosen by a canon reconciliation before implementation (`20-validation/contradiction-audit.md`).

## 2. Readiness — Required vs Degraded Checks

| Dependency | Readiness effect | Rationale | Canon |
|---|---|---|---|
| PostgreSQL | **Required** — DOWN ⇒ `503` | Without the system of record nothing correct can be served | `NFR-007` |
| Redis (queue + cache) | **Required** — DOWN ⇒ `503` for the API | Money paths, rate limits and idempotency state depend on it; fail fast rather than serve unsafe responses | `NFR-007`, `DOC-NFD-004` §4 |
| BullMQ enqueue capability | **Required** | Jobs must be enqueueable or async work silently stalls | `BR-PLT-02` |
| **Elasticsearch** | **Non-gating** — reported `DEGRADED`, instance stays **READY** | ES down ⇒ category browse + PDP still serve from DB/Redis; search shows fallback (`DOC-INT-001` §3, `DEP-04`) | `NFR-007` |
| Provider adapters (SMS/WhatsApp/wallet) | **Non-gating** — reported `DEGRADED` | Channels fail over (`BR-NTF-03`) or degrade to bank transfer (`BR-PAY-04`) | `NFR-007`, `DOC-NFD-004` §4 |
| MinIO | **Non-gating** for reads; uploads fail gracefully with a clear message | Existing images are CDN/edge-cached; orders/wallet unaffected | `DOC-NFD-004` §4 |
| Prometheus/Loki | Non-gating | Observability loss must not take the app down | — |

A degraded readiness response includes `status: "READY_DEGRADED"` with per-check detail, and sets the search-fallback flag consumed by dashboard #10 (`DOC-NFD-006` §5). Degraded state **alerts** (P2 if > 5 min) but does not fail readiness.

## 3. Probe Configurations

### 3.1 Compose healthchecks

```yaml
api:
  healthcheck:
    test: ["CMD", "wget", "-qO-", "http://localhost:3000/healthz"]
    interval: 10s
    timeout: 3s
    retries: 3
    start_period: 20s
postgres:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 30s
```

| Setting | Value | Why |
|---|---|---|
| `interval` | 10–20 s | Fast detection without probe storms |
| `timeout` | 3–5 s | A hung process fails quickly |
| `retries` | 3–5 | Avoids flapping on a single slow probe |
| `start_period` | 20–60 s | Absorbs boot (Prisma generate, Next.js boot) without false restarts |
| Effect of failure | Compose marks `unhealthy`; `restart: unless-stopped` recreates the container | Process-level self-healing (`C-26` defense) |

### 3.2 Edge (nginx) upstream checks

| Setting | Value |
|---|---|
| Passive | `proxy_next_upstream error timeout http_502 http_503 http_504` — a failed instance is skipped for that request |
| Active | Health endpoint polled every **10 s**, fall after 2 failures, rise after 1 success ⇒ removal/restore within **≤ 30 s** (`BR-PLT-07`) |
| Connection timeout | `proxy_connect_timeout 5s`, `proxy_read_timeout 60s` (longer for report/export routes) |
| Retry safety | Retries happen only for **idempotent** requests or those carrying an idempotency key (`BR-PLT-03`) |

### 3.3 Prometheus probe

`blackbox` exporter probes `/healthz` and `/readyz` every 15 s for metrics; the **external** 60 s prober covers public routes independently so a monitoring-plane failure cannot hide real downtime (`DOC-NFD-004` §1, `DOC-OPS-006` §5).

## 4. Startup Ordering

```text
postgres ─┐
redis    ─┼─ healthcheck: service_healthy ─► api, worker (app-level retries on top)
elasticsearch ─┤
minio    ─┘                │
                           ├─ api ready ─► web starts ─► edge upstream enables api/web
migrate (one-shot) ─► must succeed before api/worker restart   (depends_on: service_completed_successfully)
```

| Mechanism | Detail |
|---|---|
| Compose `depends_on` with conditions | Data services healthy → app starts; `migrate` completed → app starts |
| `depends_on` is **not** sufficient alone | App-level retries: Prisma connection retry ×10 with backoff (1→30 s), Redis retry ×10, ES optional-with-retry — so a slow data service does not crash-loop the app |
| Failure of `migrate` | Deploy halts (`service_completed_successfully` not satisfied) — never start the new app against an un-migrated DB |
| Idempotent boot | Any service can start in any order relative to *non-required* dependencies (ES, MinIO, providers) |
| No infinite crash-loop | After N failed boots the container stays up reporting `READY`-fail/`UNHEALTHY` and alerts fire — visible, not silent |

## 5. Graceful Shutdown

| Step | Detail |
|---|---|
| Signal | Docker sends `SIGTERM`; `stop_grace_period: 60s` |
| API | Stop accepting new connections; `/healthz` and `/readyz` → 503; edge removes instance ≤ 30 s; **drain in-flight requests** (up to grace period) |
| Worker (BullMQ) | Close the worker → **finish the current job** and ack it; unstarted jobs remain in the queue for the next process (`BR-PLT-01`); money jobs must complete, never be abandoned mid-transaction |
| Web | Finish in-flight SSR renders, then exit |
| Timeout | If the grace period expires, the process is killed — queue redelivery (`at-least-once` + idempotency, `BR-PLT-03`) makes this safe |
| After restart | `/readyz` must be green before the edge re-enables routing; queue depth returns to baseline ≤ 5 min |

## 6. Circuit-Breaker Interplay

| Interaction | Behaviour |
|---|---|
| Readiness ≠ breaker | Readiness answers "can I serve safely **now**"; the circuit breaker (provider calls) answers "should I keep calling this provider" (`DOC-INT-001` §4) |
| Open breaker | Does **not** flip readiness — the app stays READY and degrades the affected channel (bank transfer fallback, in-app notifications) |
| Closed breaker + down DB | Readiness fails — the app must not pretend to serve |
| Observability | Breaker state is exported as a metric so dashboard #8 shows per-provider circuit state; a breaker open > 5 min pages (P2) |
| Degradation matrix | Authoritative behaviours live in `10-integrations/integration-overview.md` §3–§4 and `12-non-functional/reliability.md` §4 |

## 7. Monitoring Integration

| Signal | Source | Alert |
|---|---|---|
| Probe failure | blackbox + external prober | 2 consecutive failures ⇒ **page ≤ 1 min** (`AC-NFR-005-02`) |
| `/readyz` returning 503 | Prometheus `probe_success{job="blackbox-http"}` | P1 if > 60 s; P2 if degraded-only |
| Container unhealthy / restart loop | cAdvisor `container_restart_count` | Restart > 3 in 10 min ⇒ P1 |
| Instance not in rotation | Edge upstream active count vs expected replicas | P1 when serving replicas = 0 |
| Worker heartbeat missing | `bullmq_worker_heartbeat` absent 2 scrape intervals | P1 |
| Deploy marker | Deploy event annotation on dashboards #1–#3 | Correlate regressions to the release |
| Rollback trigger | Error-rate alert during the observation window | Invokes `DOC-DPL-004` §2 |

## 8. What Each Surface Exposes

| Surface | Liveness | Readiness / health | Additional signal |
|---|---|---|---|
| **api** (NestJS) | `/healthz` | `/readyz` (dependency policy §2) | Prometheus `/metrics`: RED, pool, breaker |
| **worker** (BullMQ) | Process alive (container status) | Not applicable — no HTTP traffic to gate | `bullmq_worker_heartbeat`, queue depth/DLQ metrics scraped from the worker `/metrics` port |
| **web** (Next.js) | `/healthz` (or `/` for the container check) | Not traffic-gated; static/SSR availability via edge probe | RUM metrics, build id header |
| **edge** (nginx) | `/healthz` local stub | N/A (it *is* the gate) | `nginx-status` → exporter (connections, upstream status) |
| **postgres / redis / es / minio** | Native health (§3.1) | Data services are not in the request path of the LB | Exporters → dashboards #5, #6, #10 |
| **Mobile apps** | n/a | n/a | Server sees client version via API telemetry (aggregate only) |

## 9. Verification

| Check | Method | Evidence |
|---|---|---|
| `/healthz` + `/readyz` < 1 s | Timed probe in CI + on-call review | `AC-NFR-020-01` |
| Removal from rotation ≤ 30 s | Kill a replica under load; measure drain | `BR-PLT-07`, `DOC-NFD-006` §8 |
| ES down ⇒ still READY | Chaos drill: stop ES, assert `READY_DEGRADED` and browse works | `AC-NFR-007-01`, `DOC-NFD-004` §8 drill 1 |
| DB down ⇒ 503, no restart storm | Chaos drill: stop postgres | `NFR-007` |
| Graceful drain loses nothing | Stop worker mid-job; assert job completes or redelivers exactly once | `BR-PLT-02/03` |
| 503 leaks nothing | Response schema test: no hostnames/credentials | `SEC-REQ-008` |
| Probe failure pages on-call | Simulated outage | `AC-NFR-005-02` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
