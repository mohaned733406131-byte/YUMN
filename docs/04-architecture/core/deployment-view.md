---
document_id: DOC-ARCH-005
title: Deployment View (Docker Compose)
category: 04-architecture
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-005, NFR-006, NFR-016, NFR-020]
related_documents: [DOC-OVR-008, DOC-ARCH-003, DOC-ARCH-008, DOC-REQ-001, DOC-IR-007]
---

# Deployment View

How yumn runs in environments: one **Docker Compose** topology (`C-22`, `ADR-004`) with layered files for dev/staging/production parity. No Kubernetes, no cloud-vendor services in v1 (`NFR-016`). Exact compose syntax lives with the infrastructure definitions in `14-devops-infrastructure/`; this document fixes the *topology contract* that those files must satisfy.

## 1. Compose File Layout (environment parity)

| File | Purpose | Present in |
|---|---|---|
| `compose.yaml` | Base: all services, internal networks, volumes, healthchecks | dev, staging, prod |
| `compose.override.yaml` | Dev conveniences: hot reload, exposed dev ports, seed data, local mailhog-style stubs (`INFERENCE`) | dev only |
| `compose.staging.yaml` | Staging sizing, synthetic providers, test data | staging |
| `compose.prod.yaml` | Production sizing, no test data, strict ports, restart policies | prod |

Same image tags across environments (built by CI); only configuration differs. This is the parity mechanism required by `NFR-016`/`NFR-020` and the no-K8s stance of `C-22`.

## 2. Services

| Service | Image / build | Command | Exposed ports (prod) | Healthcheck | Scale |
|---|---|---|---|---|---|
| `edge` | nginx (or equivalent) | `nginx -g 'daemon off;'` | 80, 443 (public) | HTTP `/healthz` | 1 |
| `web` | built from `apps/web` (Next.js 14) | `next start` | internal 3000 | HTTP `/` | 1–2 (`INFERENCE`) |
| `api` | built from `apps/api` (NestJS 10) | `node dist/main` | internal 3000 | `/healthz` live, `/readyz` ready (`BR-PLT-07`) | 1–N (stateless) |
| `worker` | same image as `api` | `node dist/worker` (BullMQ consumers) | none | queue-heartbeat metric | 1–N |
| `postgres` | `postgres:16` | default | internal 5432 | `pg_isready` | 1 (+ backups) |
| `redis` | `redis:7` | default + AOF persistence | internal 6379 | `redis-cli ping` | 1 |
| `elasticsearch` | `elasticsearch:8` | default | internal 9200 | cluster health API | 1 (dev/staging), 1–3 (`INFERENCE`) |
| `minio` | `minio` | server | internal 9000, console 9001 (internal) | liveness endpoint | 1 |
| `prometheus` | `prometheus` | default | internal 9090 | `/-/healthy` | 1 (staging/prod) |
| `grafana` | `grafana` | default | internal 3000 | `/api/health` | 1 (staging/prod) |

Port numbers for internal services are the software defaults (`INFERENCE`); only `edge` publishes host ports in production.

## 3. Networks & Isolation

```text
            ┌──────────────── internet ────────────────┐
            │                                          │
        host:80/443 ──► [ edge ]                       │
                          │        net-edge (only edge + web + api)     
                          ├──► [ web ]                 │
                          └──► [ api ] ─┐              │
                                       │ net-app (api, worker, postgres, redis, elasticsearch, minio, prometheus)
                          [ worker ] ──┤               │
                                       ├──► postgres / redis / elasticsearch / minio
                                       └──► outbound to providers (SMS, WhatsApp, m-Floos/OneCash, push)
```

| Network | Members | Rule |
|---|---|---|
| `net-edge` | edge, web, api | The only path from the host/internet into the application |
| `net-app` | api, worker, postgres, redis, elasticsearch, minio, prometheus | Data tier unreachable from the host; no public ports for data services |
| (egress) | api, worker | Provider calls leave via the host network; secrets injected via environment (`SEC-REQ-007`) |

Data services are never published to the host in staging/prod — matches trust zones Z4 in DOC-SA-002.

## 4. Volumes

| Volume | Service | Durability need | Backup implication |
|---|---|---|---|
| `pgdata` | postgres | Critical (system of record) | Continuous WAL + daily snapshots; quarterly restore drills (`DATA-REQ-004`, `NFR-006`) |
| `redisdata` | redis | Medium (queues, AOF) | Jobs must be replayable; queue loss degrades but does not corrupt (`NFR-007`) |
| `esdata` | elasticsearch | Low (rebuildable index) | Reindex from catalog; no backup required |
| `miniodata` | minio | High (images, KYC docs) | Included in backup set; media referenced by DB rows |
| `promdata` / `grafanadata` | prometheus, grafana | Low | Dashboards/config recreated from repo (`INFERENCE`) |

## 5. Configuration & Secrets

| Concern | Mechanism | IDs |
|---|---|---|
| Config | Environment variables per service; `.env` files per environment, never committed | `NFR-020`, `SEC-REQ-007` |
| Secrets | Injected by the deployer's secrets store; CI secret scanning; no keys in repo | `SEC-REQ-007`, `SEC-REQ-012` |
| Runtime settings | Platform settings from DB (`AdminModule`), but constraints `C-01…C-26` are not configurable | `FR-020` |
| Migrations | Expand-contract, run as a one-shot service/job before app start (`INFERENCE`) | `DATA-REQ-005`, `NFR-020` |
| Locale/time | UTC storage, `ar-YE` display formatting | `BR-PAY-10`, `NFR-013` |

## 6. Restart, Health & Availability (`C-26`, `NFR-005`)

| Mechanism | Detail | IDs |
|---|---|---|
| Restart policies | `unless-stopped` / `always` for all stateful and app services | `C-26` |
| Liveness | `/healthz` — process is up | `BR-PLT-07` |
| Readiness | `/readyz` — dependencies reachable; gate traffic before serving | `BR-PLT-07`, `NFR-005` |
| Graceful shutdown | In-flight requests drain; workers finish/return jobs | `NFR-020` |
| Zero-downtime deploy | Rolling restart of `api` replicas + expand-contract migrations | `NFR-020` |
| Degraded mode | If search/cache down, readiness still reports ok for core routes; degradation rules from DOC-SA-009 §3 | `NFR-007` |
| Backups | WAL archiving + daily snapshots on `pgdata`; MinIO data backed up with DB-consistent schedule | `DATA-REQ-004` |
| RTO/RPO | ≤ 1 h / ≤ 15 min — restore procedure + replica promotion documented in `15-deployment/` and runbooks | `NFR-006`, `C-26` |

## 7. CI/CD Pipeline Placement (GitHub Actions)

| Stage | Trigger | Actions | Gate |
|---|---|---|---|
| Lint & typecheck | push / PR | ESLint (incl. module-boundary rules), `tsc --noEmit` | Must pass (DOC-ARCH-006 enforcement) |
| Unit tests | push / PR | Jest suites per module | Coverage thresholds (`NFR-010`, AC-S-08) |
| Build images | merge to main | Build `api`/`worker`/`web` images, tag with commit SHA | Reproducible build |
| Integration tests | merge to main | Compose-based test stack: PostgreSQL, Redis, ES, MinIO | Contract + rule tests |
| Security scans | push / PR | SAST, dependency + secret scanning | Critical vulns block (`SEC-REQ-012`) |
| Deploy staging | merge to main | `compose.staging.yaml` up with new tags | Smoke tests + Playwright E2E |
| Deploy prod | manual approval | Pull tags, `compose.prod.yaml` up, rolling restart | Health/readiness green (`BR-PLT-07`) |
| Load test | scheduled / pre-release | k6 against staging (`NFR-003`, 10k concurrency) | Latency SLOs (`NFR-001`) |

## 8. Why No Kubernetes (`C-22`, `ADR-004`)

| Argument | Detail |
|---|---|
| Team & operability | Small-team operations benefit more from one comprehensible Compose file than from cluster control planes |
| Workload shape | One backend, a handful of services — nothing here needs pod scheduling across nodes in v1 |
| Cost/complexity | K8s adds etcd, CNI, ingress controllers, RBAC surface — all maintained with no product benefit at current scale |
| Scale-out needs met | Horizontal scale of `api`/`worker` replicas, vertical scale of data services, and the documented path in `scalability.md` cover `C-25` |
| Exit path | Container images and Compose services map 1:1 to any future orchestrator — no rewrite needed if v2 adopts one |

## 9. Environment Matrix

| Aspect | dev | staging | prod |
|---|---|---|---|
| Compose files | base + override | base + staging | base + prod |
| Data | seeded, disposable | realistic subset, preserved | production, backed up |
| Providers | sandbox (`DEP-05`), fake SMS | sandbox/synthetic | production credentials |
| TLS | local certs | valid certs | valid certs via edge (`DEP-08`) |
| Observability | optional | prometheus + grafana | prometheus + grafana + alert routes (`INT-REQ-007`) |
| Load testing | no | yes (k6) | no (non-disruptive checks only) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
