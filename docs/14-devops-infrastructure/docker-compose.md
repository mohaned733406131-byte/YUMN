---
document_id: DOC-OPS-003
title: Container Strategy (Docker Compose Service Inventory)
category: 14-devops-infrastructure
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-005, NFR-016, NFR-020, SEC-REQ-006, SEC-REQ-011]
related_documents: [DOC-ARCH-005, DOC-ARCH-003, DOC-ARCH-009, DOC-OPS-001, DOC-OPS-002, DOC-NFD-004]
---

# Container Strategy — Compose Service Inventory

Realizes the topology contract of `../04-architecture/core/deployment-view.md` (DOC-ARCH-005) as concrete Compose services. Governing constraints: `C-22` (Compose only), `C-19` (PostgreSQL only), `C-20` (BullMQ only), `NFR-016` (any Docker host, no lock-in).

## 1. Service Inventory

| Service | Image / build | Command | Restart | Scale (prod) | Memory limit (prod `INFERENCE`) | CPU limit |
|---|---|---|---|---|---|---|
| `edge` | `nginx:1.27-alpine` + repo `infra/edge/` config | `nginx -g 'daemon off;'` | `unless-stopped` | 1 | 128 MB | 0.5 |
| `web` | build `apps/web` (multi-stage) | `node server.js` (`next start`) | `unless-stopped` | 1 | 1024 MB | 2.0 |
| `api` | build `apps/api` (multi-stage) | `node dist/main.js` | `unless-stopped` | 1–N (start at 2) | 1024 MB each | 2.0 each |
| `worker` | **same image as `api`** | `node dist/worker.js` | `unless-stopped` | 1–N (start at 2) | 1024 MB each | 2.0 each |
| `migrate` | same image as `api` | `npx prisma migrate deploy` | `no` (one-shot) | 0 or 1 per deploy | 512 MB | 1.0 |
| `postgres` | `postgres:16` | default | `unless-stopped` | 1 | 4096 MB | 2.0 |
| `redis` | `redis:7` | `redis-server --appendonly yes` | `unless-stopped` | 1 | 2048 MB | 1.0 |
| `elasticsearch` | `docker.elastic.co/elasticsearch/elasticsearch:8.x` | default | `unless-stopped` | 1 (dev/staging), 1–3 later (`INFERENCE`) | 4096 MB | 2.0 |
| `minio` | `minio/minio` | `server /data --console-address ":9001"` | `unless-stopped` | 1 | 1024 MB | 1.0 |
| `prometheus` | `prom/prometheus` | default | `unless-stopped` | 1 | 1024 MB | 1.0 |
| `grafana` | `grafana/grafana` | default | `unless-stopped` | 1 | 512 MB | 0.5 |
| `alertmanager` | `prom/alertmanager` | default | `unless-stopped` | 1 | 256 MB | 0.25 |
| `sms-sink` | `axllent/mailpit` | default | `unless-stopped` | 1 (dev/staging only) | 128 MB | 0.25 |

Limits are **starting values**; actual sizing is validated by the k6 run at `C-25` scale on staging (`AC-S-05`) and by the resource dashboard (`DOC-NFD-006` §5 panel 4). Data-service limits are raised, not removed, when growth requires it.

## 2. Image Sources & Multi-Stage Builds

| Image | Base | Build stages | Final contents |
|---|---|---|---|
| `api` / `worker` | `node:20-alpine` (pinned digest) | ① `deps`: install from `package-lock.json` (full, incl. dev) → ② `build`: `tsc` + Prisma generate → ③ `runner`: `node:20-alpine`, `npm ci --omit=dev`, `dist/`, `prisma/schema`, non-root user | Runtime only: `dist/`, `node_modules` (prod), `prisma/`, healthcheck script |
| `web` | `node:20-alpine` | ① `deps` → ② `build`: `next build` with `output: 'standalone'` → ③ `runner`: standalone output + `.next/static` + `public/` | Standalone server, static assets |
| `edge` | `nginx:1.27-alpine` | single stage + `infra/edge/nginx.conf` templates | Config, TLS material from volume (never baked) |
| data services | vendor official images | none (no custom layers) | Unmodified upstream |

Rules:

- **No secrets, no `.env`, no TLS keys in any image layer** (`SEC-REQ-007`); config arrives at runtime via `env_file` / mounts.
- Multi-stage builds keep dev toolchain, source maps policy, and build cache out of the runtime image; final images run as a dedicated non-root `yumn` UID.
- The `api` and `worker` services deliberately share **one image** so domain code can never diverge between HTTP and queue paths (`DOC-ARCH-003` §2 CNT-05).
- Base images are pinned to a version **and** digest in the Dockerfile; digest bumps arrive as dependency PRs, never silently.

## 3. Healthchecks

| Service | Probe | Interval / timeout / retries / start-period | Failure effect |
|---|---|---|---|
| `edge` | `curl -fsS http://localhost/healthz` | 10s / 3s / 3 / 5s | Container unhealthy → edge marked down in dashboard; alert P2 |
| `web` | `wget -qO- http://localhost:3000/` | 15s / 5s / 3 / 30s | Unhealthy → alert; edge upstream marked down (§7) |
| `api` | `wget -qO- http://localhost:3000/healthz` (liveness) | 10s / 3s / 3 / 20s | Unhealthy → Compose restarts container |
| `api` (readiness, orchestrator-side) | `/readyz` polled by edge upstream + Prometheus probe | 10s / 3s / 2 / — | 503 → removed from upstream ≤ 30 s (`BR-PLT-07`) |
| `worker` | no HTTP port; **BullMQ heartbeat metric** (`bullmq_worker_heartbeat` exported by the process) | scrape 15s | No heartbeat 2 scrape intervals → P1 alert |
| `postgres` | `pg_isready -U $POSTGRES_USER` | 10s / 5s / 5 / 30s | Unhealthy → P1 page (`NFR-006`) |
| `redis` | `redis-cli ping \| grep PONG` | 10s / 3s / 5 / 10s | Unhealthy → P1 page |
| `elasticsearch` | `curl -fsS localhost:9200/_cluster/health` | 20s / 5s / 5 / 60s | Unhealthy → **degraded search only**; readiness stays green (`DOC-OPS-006` §5) |
| `minio` | `curl -fsS localhost:9000/minio/health/live` | 15s / 5s / 3 / 20s | Unhealthy → P3 ticket |
| `prometheus` | `/-/healthy` | 15s / 5s / 3 / 15s | Unhealthy → P2 (monitoring blind spot) |
| `grafana` | `/api/health` | 15s / 5s / 3 / 15s | Unhealthy → P3 |

Health endpoint semantics (liveness vs readiness, degraded policy, graceful shutdown) are specified in [`15-deployment/health-checks.md`](../15-deployment/health-checks.md) — this file only wires the probes.

## 4. Volumes

| Volume | Service | Driver | Backup class | Notes |
|---|---|---|---|---|
| `pgdata` | `postgres` | local | **Critical** — system of record | WAL archiving enabled (`archive_mode=on`, `archive_command` ships ≤ 5 min, `DOC-NFD-004` §6) |
| `redisdata` | `redis` | local | Medium | AOF `everysec` + RDB snapshot; queue replay relies on it (`C-20`) |
| `esdata` | `elasticsearch` | local | **None — rebuildable** | Full reindex from Postgres nightly (`RC-08`) |
| `miniodata` | `minio` | local | **High** — images, KYC docs | Included in nightly object backup (`DOC-OPS-007`) |
| `promdata` | `prometheus` | local | Low | TSDB retention per `DOC-OPS-006` §7 |
| `grafanadata` | `grafana` | local | Low | Dashboards/datasources provisioned from repo — volume is cache only |
| `alertdata` | `alertmanager` | local | Low | Routes provisioned from repo |
| `edgecerts` | `edge` | local | Medium (secret) | TLS material mounted read-only; **never** baked into images (`SEC-REQ-006`, `DEP-08`) |
| `backups` | `backup` helper | local (staging area) | n/a | Transient drop before off-host copy |

## 5. Networks

| Network | Driver | Members | Exposure rule |
|---|---|---|---|
| `net-edge` | bridge | `edge`, `web`, `api` | Only path from host/internet into the application |
| `net-app` | bridge | `api`, `worker`, `postgres`, `redis`, `elasticsearch`, `minio`, `prometheus`, `grafana`, `alertmanager`, `migrate` | Data tier **unreachable from the host**; no published ports for data services in staging/prod |

- `worker` joins `net-edge` **only** if a job must call the API in-process (default: it does not).
- Egress to providers (SMS, WhatsApp, m-Floos, OneCash, APNs/FCM) leaves through the default bridge; no inbound provider path except the signed webhook route on `edge` → `api` (`INT-REQ-006`).
- No container ever receives the Docker socket, and no container joins `host` network mode.

## 6. Restart Policies, Logging, Tags

| Concern | Setting | Rationale |
|---|---|---|
| Restart policy | `unless-stopped` for all long-running services; `no` for `migrate` and one-shot jobs | Self-healing after crash/reboot (`C-26` process-level defense) |
| Logging driver | `json-file` with `max-size: 10m`, `max-file: 5` per container | Simple, no extra daemon under `C-22`; rotated by Docker; collected by the pipeline in `DOC-OPS-006` §6 |
| Log format | Structured JSON written to **stdout** by the app (`DOC-NFD-006` §2 schema) | One collection point; no log files inside containers |
| Image tags | `ghcr.io/yumn/<service>:<git-sha>` for every build; release adds `:<semver>` and `:latest` **only on release tags** | Reproducible rollback target N-2 (`15-deployment/rollback.md`) |
| Image pull policy | `always` in staging/prod deploy step; local uses `build:` | Ensures digest parity (PAR-2) |
| OOM behaviour | `oom_kill_disable: false` + per-service memory limits | A runaway container is killed and restarted, not allowed to starve the host |
| Ulimits | `nofile` raised for `postgres`/`elasticsearch`/`api` | Pool and socket headroom under `C-25` |

## 7. Port Map

| Service | Container port | Published in local | dev | staging | production | Purpose |
|---|---|---|---|---|---|---|
| `edge` | 80 | 8080 | 80 | 80 | **80** | HTTP → redirect to HTTPS |
| `edge` | 443 | 8443 | 443 | 443 | **443** | TLS termination, routing (`SEC-REQ-006`) |
| `web` | 3000 | 3001 | internal | internal | internal | SSR/static via `edge` |
| `api` | 3000 | 3000 | 3000 | internal | internal | REST `/api/v1` via `edge` |
| `postgres` | 5432 | 5432 | internal | internal | internal | Prisma |
| `redis` | 6379 | 6379 | internal | internal | internal | cache / BullMQ |
| `elasticsearch` | 9200 | 9200 | internal | internal | internal | search |
| `minio` | 9000 / 9001 | 9000 / 9001 | internal | internal | internal | S3 API / console |
| `prometheus` | 9090 | 9090 | 9090 | internal | internal | metrics |
| `grafana` | 3000 | 3000 | 3000 | internal* | internal* | dashboards |
| `alertmanager` | 9093 | 9093 | internal | internal | internal | alert routing |
| `sms-sink` | 8025 | 8025 | 8025 | 8025 (test) | **not running** | OTP/payload inspection |

\* Grafana/Prometheus are reachable in staging/prod through an ** SSH tunnel or an IP-allowlisted `edge` location** (`/grafana`), never directly published.

**Invariant:** in production the host publishes exactly two ports — 80 and 443. Any new published port is a review-blocking change.

## 8. Reverse Proxy Choice — Nginx (Traefik rejected for v1)

| Criterion | Nginx (chosen) | Traefik (considered) |
|---|---|---|
| Fit with `C-22` | Static, file-driven config rendered from templates; one container; no extra API | Label-driven discovery adds a learning surface and a second failure mode |
| TLS | Native termination + cert reload; pairs cleanly with Cloudflare origin certs (`DEP-08`) | Excellent ACME automation — valuable only if we ran our own public CA flow |
| Edge behaviour | Request-size limits, `proxy_buffering`, static asset serving, maintenance page, gzip/brotli | Comparable |
| Team familiarity | High for the operating team (`INFERENCE`) | Lower |
| Why not now | — | Traefik's advantages (auto-discovery, ACME) pay off with dynamic fleets; v1 has one fixed, tiny service set. Revisit only via ADR if the topology changes (`../04-architecture/core/technology-stack.md` §4 records the alternative as viable) |

## 9. Upgrading Images Safely

| Step | Action | Gate |
|---|---|---|
| 1 | New base-image/digest PR opened by the dependency bot | CI: build + unit + image scan (`SEC-REQ-012`) |
| 2 | Merge to `main` → CI builds and tags `ghcr.io/yumn/*:<sha>` | All PR checks green |
| 3 | Auto-deploy to `dev`, then `staging` | Smoke + Playwright suite green (`15-deployment/deployment-process.md` §5) |
| 4 | Promotion of the **same digest** to production | Manual approval; digest recorded in the release log |
| 5 | Rolling recreate: `api` (one replica at a time, readiness-gated) → `worker` → `web` → `edge` config reload | `/readyz` green before the next replica; error rate < 1% over 5 min |
| 6 | Verify | Post-deploy smoke suite; dashboards watched for 15 min |
| 7 | If anything fails | Rollback to N-2 image tags within 15 min (`AC-S-20`) |

**Hard rules:** never `docker compose pull` without a digest pin in staging/prod; never upgrade a data-service **major** version in place (PostgreSQL 16 → next major is a planned migration, not a container bump); never mix old and new `api`/`worker` images across a schema change that is not expand-phase (`DOC-DB-006` §3).

## 10. Verification

| Check | Method |
|---|---|
| Compose renders cleanly | `docker compose config -q` in CI on every PR |
| Only 80/443 published in prod overlay | CI assertion over rendered config |
| No `docker.sock`, no `privileged`, no `host` network | CI assertion over rendered config |
| Healthchecks defined on every long-running service | CI assertion over rendered config |
| Resource limits present in prod overlay | CI assertion over rendered config |
| Image digest parity staging↔prod | Release log + `AC-NFR-016-01` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
