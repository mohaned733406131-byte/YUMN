---
document_id: DOC-OPS-001
title: DevOps & Infrastructure — README (14-devops-infrastructure Index)
category: 14-devops-infrastructure
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-005, NFR-006, NFR-014, NFR-016, NFR-017, NFR-020, DATA-REQ-004, INT-REQ-007, SEC-REQ-007, SEC-REQ-012]
related_documents: [DOC-ARCH-005, DOC-ARCH-009, DOC-OVR-008, DOC-OVR-010, DOC-SEC-005, DOC-DTA-005, DOC-NFD-004, DOC-NFD-006]
---

# 14-devops-infrastructure — How yumn Is Run

**yumn (يُمن)** — multi-vendor marketplace for Yemen; wallet-only payments (`C-01`), modular monolith (`C-21`), **Docker Compose only, no Kubernetes** (`C-22`, `ADR-004`).

## 1. Purpose & Boundary

This domain owns the **HOW of running yumn**: environments, container definitions, pipelines, configuration, observability plumbing, backup execution, and host security operations. It is the implementation layer that satisfies requirements defined elsewhere — it never restates them.

| This domain owns | This domain does **not** own | Rule of thumb |
|---|---|---|
| Environment matrix and parity rules | What a requirement means (`02-requirements/`) | "Which env, which file, which flag?" → here |
| Compose services, networks, volumes, healthchecks | Topology contract / C4 views (`04-architecture/`) | "Which container, which port?" → here (contract: `DOC-ARCH-005`) |
| GitHub Actions workflows and merge gates | Coverage thresholds and test levels (`13-testing/`, `12-non-functional/`) | "What blocks the merge?" → here |
| Env-var inventory, feature-flag mechanics | Secret classes, rotation policy, access matrix (`09-security/`) | "Which variable, which consumer?" → here |
| Prometheus/Grafana/Alertmanager wiring, log pipeline | SLIs, dashboard *content*, alert *thresholds* (`12-non-functional/observability.md`) | "How is the signal collected?" → here |
| Backup jobs, restore procedure, drill schedule | Backup *classes*, retention windows, RPO/RTO numbers (`16-data/`, `NFR-006`, `DATA-REQ-004`) | "Which command, which cron?" → here |
| Host patching, firewall, TLS renewal, image scanning | Threat model, control catalogue, findings (`09-security/`) | "Which port, which scan?" → here |

**One-sentence test:** if the question is about *targets, thresholds, policy, or meaning*, it belongs to `12-non-functional/`, `09-security/`, `16-data/`, or `02-requirements/`; if it is about *the mechanism that makes it real*, it belongs here.

## 2. File Index

| # | File | Document ID | Content | Source of truth |
|---|---|---|---|---|
| 1 | [README.md](README.md) | `DOC-OPS-001` | Domain charter, topology summary, pointer map, index | Yes |
| 2 | [environments.md](environments.md) | `DOC-OPS-002` | Environment matrix, parity rules (ADR-004), compose overlays, refresh/teardown, mobile build envs | Yes |
| 3 | [docker-compose.md](docker-compose.md) | `DOC-OPS-003` | Service inventory, image sources, limits, healthchecks, volumes, networks, port map, upgrades | Yes |
| 4 | [ci-cd.md](ci-cd.md) | `DOC-OPS-004` | GitHub Actions workflows, PR gate steps, quality gates, caching, branch protection, E2E placement | Yes |
| 5 | [configuration.md](configuration.md) | `DOC-OPS-005` | Config hierarchy, full env-var inventory, feature flags, drift prevention, boot validation | Yes |
| 6 | [monitoring-stack.md](monitoring-stack.md) | `DOC-OPS-006` | Scrape jobs, Grafana provisioning, alert routing, log pipeline, uptime checks, retention, honest v1 scope | Yes |
| 7 | [backup-recovery.md](backup-recovery.md) | `DOC-OPS-007` | Backup matrix per store, RTO/RPO execution, encryption, off-host copy, restore steps, quarterly drill | Yes |
| 8 | [host-hardening.md](host-hardening.md) | `DOC-OPS-008` | OS patching, SSH policy, firewall/port exposure, Docker hygiene, TLS renewal, scan cadence | Yes |

Domain numbering prefix: **`DOC-OPS-NNN`**. Nothing outside this directory may mint a `DOC-OPS` ID.

## 3. Topology Summary — One Docker Host per Environment

Every non-local environment is **exactly one Docker Compose host** (`C-22`). There is no cluster, no orchestrator control plane, no second application host in v1.

```text
                        Internet
                            │
                    Cloudflare (DEP-08): DNS · TLS · CDN · DDoS
                            │ HTTPS 443 (origin)
              ┌─────────────▼──────────────┐
              │  Docker host  (one per env)│
              │  ┌──────────────────────┐  │
 host:80/443 ─┼─►│ edge  (nginx)        │  │   net-edge
              │  └───┬──────────────┬───┘  │◄──── web, api
              │      ▼              ▼      │
              │   [ web ]        [ api ]───┼──────────────┐
              │  Next.js 14    NestJS 10   │  net-app     │
              │                 ▲   │      │◄── worker,   │
              │   [ worker ]────┘   │      │    postgres, │
              │   BullMQ consumers  │      │    redis,    │
              │                     │      │    elasticsearch,
              │                     ▼      │    minio, prometheus
              │        postgres · redis · elasticsearch · minio
              │        prometheus · grafana · alertmanager
              └──────────────────────────────┘
```

### 3.1 Service list (production)

| # | Service | Role | Image source | Public ports |
|---|---|---|---|---|
| 1 | `edge` | TLS termination, routing, static delivery | `nginx:1.27-alpine` + repo config | **80, 443 only** |
| 2 | `web` | Next.js 14 SSR + static (customer / vendor / admin shells) | custom multi-stage `apps/web/Dockerfile` | none |
| 3 | `api` | NestJS 10 HTTP API (stateless, 1–N) | custom multi-stage `apps/api/Dockerfile` | none |
| 4 | `worker` | BullMQ consumers, same image as `api`, different entrypoint | same image as `api` | none |
| 5 | `postgres` | PostgreSQL 16 — system of record (`C-19`) | `postgres:16` | none |
| 6 | `redis` | Redis 7 — cache, rate limits, BullMQ (`C-20`) | `redis:7` | none |
| 7 | `elasticsearch` | Elasticsearch 8 — Arabic-aware search (`DEP-04`) | `docker.elastic.co/elasticsearch/elasticsearch:8.x` | none |
| 8 | `minio` | S3-compatible object storage (`DEP-07`) | `minio/minio` | none (console internal) |
| 9 | `prometheus` | Metrics scrape + alert rules (`INT-REQ-007`) | `prom/prometheus` | none |
| 10 | `grafana` | Dashboards (12 inventory rows, `DOC-NFD-006` §5) | `grafana/grafana` | none |
| 11 | `alertmanager` | Alert routing to on-call | `prom/alertmanager` | none |
| 12 | `migrate` | One-shot `prisma migrate deploy` job (never long-running) | same image as `api` | none |
| 13 | `sms-sink` | **dev/staging only** — MailHog-class capture of outbound SMS/WhatsApp payloads | `axllent/mailpit` | dev: 8025 (UI) |

Totals: 13 defined services; production runs 12 (no `sms-sink`); local dev runs all 13 with relaxed ports (`DOC-OPS-002` §4).

### 3.2 Environments

`local` (developer laptop) → `dev` (shared branch environment) → `staging` (prod-like, E2E/perf/DAST) → `production`. Parity rule: **dev topology = prod topology** (`ADR-004`, `NFR-016`, `NFR-020`); only configuration, sizing, and provider credentials differ. Full matrix: `environments.md`.

## 4. What Lives Where — Pointer Map

| Question | Authoritative location | This domain's contribution |
|---|---|---|
| Availability target 99.99%, probe SLI, error budget, **single-host residual risk** | `12-non-functional/reliability.md` §1–§3 | Restart policies, healthchecks, uptime probes (`docker-compose.md`, `monitoring-stack.md`) |
| RED metrics, log schema, dashboard inventory, alert severity → route, runbook list | `12-non-functional/observability.md` | Scrape config, provisioning files, Alertmanager receivers (`monitoring-stack.md`) |
| Secrets classes, storage model, rotation cadence, access matrix | `09-security/secrets-management.md` | `env_file` wiring, `.gitignore` hygiene, CI secret scan job (`configuration.md`, `ci-cd.md`) |
| Vulnerability SLAs, scan gates | `02-requirements/security/SEC-REQ-012.md`, `09-security/security-controls.md` (`SEC-C-23/24`) | Workflow steps, image scans, Dependabot/Renovate cadence (`ci-cd.md`, `host-hardening.md`) |
| Backup classes, retention windows `RC-01…RC-09`, residual window | `16-data/retention-and-archival.md` §3–§5 | Job scripts, storage layout, restore runbook (`backup-recovery.md`) |
| RTO ≤ 1 h / RPO ≤ 15 min, drill acceptance | `02-requirements/data/DATA-REQ-004.md`, `NFR-006` | Execution of WAL archiving + quarterly drill (`backup-recovery.md`) |
| Topology contract (services, networks, volumes, restart, degraded mode) | `04-architecture/deployment-view.md` | Actual Compose YAML realizing that contract (`docker-compose.md`) |
| Stack versions and rejected alternatives | `04-architecture/technology-stack.md` | Pinned tags and base-image policy (`docker-compose.md`, `build-and-release.md` in `15-deployment/`) |
| Migration ordering, expand/contract, forward-only | `08-database/migrations-and-evolution.md` | `migrate` one-shot job placement (`deployment-process.md` in `15-deployment/`) |
| Degradation behaviour (ES down ⇒ browse works, etc.) | `10-integrations/integration-overview.md` §3–§4, `12-non-functional/reliability.md` §4 | Readiness policy that refuses to fail on ES (`health-checks.md` in `15-deployment/`) |
| Risks RISK-005 (small team vs 99.99%), RISK-014 (edge/DNS) | `17-risk-management/risk-register.md` | Operational mitigations executed here |

## 5. Governing Principles

| # | Principle | Anchor |
|---|---|---|
| P1 | **One host, honestly stated.** v1 has no host-level HA; 99.99% is defended by fast restore, not failover. Multi-host HA requires an ADR + `C-22` amendment. | `C-22`, `DOC-NFD-004` §3 |
| P2 | **Parity by construction.** Same images, same topology, layered config — differences are data, never structure. | `ADR-004`, `NFR-016` |
| P3 | **Data tier never published.** Only `edge` binds host ports in staging/prod. | `DOC-ARCH-005` §3, `SEC-REQ-006` |
| P4 | **Config and secrets are environment, never source.** Fail fast on missing required vars. | `SEC-REQ-007`, `NFR-020` |
| P5 | **Gates are mechanical.** Nothing passes CI by opinion: coverage, lint, types, scans, migration lint. | `NFR-009`, `AC-S-08`, `SEC-REQ-012` |
| P6 | **Forward-only schema.** Production runs `prisma migrate deploy`; rollback of DDL is a forward fix. | `DATA-REQ-005`, `DOC-DB-006` |
| P7 | **Every critical signal has an alert; every alert has a dashboard panel.** | `AC-S-18`, `DOC-NFD-006` §3 |
| P8 | **Backups are proven, not assumed.** Quarterly restore drill with ledger zero-imbalance check. | `DATA-REQ-004` R4, `AC-DR004-03` |

## 6. Reading Order & Verification

**Reading order:** this README → `environments.md` → `docker-compose.md` → `configuration.md` → `ci-cd.md` → `monitoring-stack.md` → `backup-recovery.md` → `host-hardening.md`. Deployment mechanics (release, rollback, health, go-live) continue in [`15-deployment/`](../15-deployment/README.md).

**Verification:** this domain is verified through `AC-NFR-005-*` (probes), `AC-NFR-014-*` (metric/alert coverage), `AC-NFR-020-01/02` (runbooks, health timing, deploy/rollback), `AC-DR004-*` (backup/drill), `AC-SR007-*` (secret hygiene), `AC-SR012-*` (scan gates), and `AC-NFR-016-01` (image-digest parity across environments). Evidence artifacts are CI run URLs, Grafana dashboards, and dated drill records.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
