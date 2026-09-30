---
document_id: DOC-OPS-002
title: Environments & Parity Rules
category: 14-devops-infrastructure
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-005, NFR-016, NFR-020, DATA-REQ-002, SEC-REQ-007]
related_documents: [DOC-ARCH-005, DOC-OPS-001, DOC-OPS-003, DOC-TST-002, DOC-INT-008, DOC-OVR-010]
---

# Environments & Parity Rules

Four environments — **local · dev · staging · production** — all running the *same* Compose topology on *one* Docker host each (`C-22`). Configuration differs; structure never does. This document is the environment matrix of record for infrastructure; the *testing* view of environments (fixtures, masking, reserved phone blocks) is `13-testing/testing-strategy.md` §7 and `13-testing/test-data-and-environments.md`.

## 1. Environment Matrix

| Aspect | local | dev (shared) | staging | production |
|---|---|---|---|---|
| **Purpose** | Developer loop, unit/integration work | Branch-level integration; demo to stakeholders | Prod-like verification: E2E, perf (k6), DAST, drills | Live marketplace |
| **Host** | Developer laptop / workstation | 1 small cloud VM | 1 medium cloud VM (prod-sized CPU/RAM class) | 1 production VM (sized for `C-25`, `DOC-NFD-003` §4) |
| **Compose files** | base + `compose.override.yaml` | base + `compose.dev.yaml` | base + `compose.staging.yaml` | base + `compose.prod.yaml` |
| **Image tags** | local build (hot reload) | CI `main` SHA tags | CI `main` SHA tags (same digests as prod, `AC-NFR-016-01`) | CI release tags (`git-sha` + SemVer release) |
| **Data** | Disposable; re-seeded on demand | Seeded, preserved between runs | Realistic subset, preserved, masked PII only | Production data — never copied out unmasked |
| **Real PII** | No | No (masked, `MASK-01…MASK-06`) | No (masked) | Yes |
| **Providers** | Fake adapters (in-process) | Fake adapters + `sms-sink` capture | Sandbox/fake only — **no real money** (`DOC-INT-008` §2) | Production credentials (`DEP-05`, `DEP-06`) |
| **Wallet top-up** | Mock ledger credit | Mock ledger credit | Sandbox provider or mock | Real m-Floos / OneCash + manual bank transfer |
| **OTP / SMS** | `sms-sink` UI (MailHog-class) | `sms-sink` UI | `sms-sink` + sandbox DLR stubs | Real Telesom/Sabafon + WhatsApp Business |
| **Seeded users** | Full fixture set (customer, vendor, courier, admin, moderator, super admin) | Same fixture set | Reduced set, **no privileged accounts with weak passwords** | **No seeded users at all** — bootstrap admin created once interactively, then disabled |
| **Seed data** | Categories, ~50 products, stores, coupons | Same | Realistic subset (~500 products), all category levels | Only **reference data**: category tree, commission tiers, VAT settings, platform settings (`FR-019`, `FR-020`) |
| **TLS** | None or self-signed local CA | Self-signed / internal CA | Valid certs via edge (`DEP-08` staging zone) | Valid certs: Cloudflare origin + edge TLS 1.3 (`SEC-REQ-006`, `DEP-08`) |
| **Access** | Developer machine | VPN or IP allowlist; engineer accounts | VPN/IP allowlist; engineer + QA accounts | Restricted: ops role + admin console behind RBAC (`SEC-REQ-004`) |
| **Observability** | Optional Prometheus | Prometheus + Grafana, P2 routes only | Full stack, all dashboards, **alerts to a test channel** | Full stack, all dashboards, alerts to on-call (`INT-REQ-007`) |
| **Backups** | None | None | Nightly snapshot (drill source) | WAL continuous + nightly snapshot + off-host copy (`DOC-OPS-007`) |
| **Load testing** | No | No | Yes — k6, weekly + pre-release (`AC-S-05`) | **No** load tests; passive probes + smoke only |
| **DAST / security scans** | No | No | ZAP-style baseline+active per release (`SEC-C-23`) | Passive only; scans run in CI/staging |
| **Teardown** | On demand (`docker compose down -v`) | Weekly refresh | Monthly refresh; reset before each release cycle | **Never** — see §5 |
| **Cost notes (`INFERENCE`)** | ~0 (laptop) | ~1 small VM, ~4 GB RAM | ~1 mid VM + storage, burst during k6 runs | 1 prod VM + CDN egress + backup storage; the only continuously billed app tier |

> **Optional fifth tier (testing view):** `13-testing/testing-strategy.md` §7 also lists a *prod-like (pre-release)* tier used for DR and rollback rehearsal at `C-25` scale. It is **not a separate topology** — it is production's Compose overlay applied to a throwaway host with sandbox credentials. Infrastructure provisions it on demand; it is destroyed after the rehearsal.

## 2. Parity Rules (ADR-004, NFR-016, NFR-020)

| # | Rule | Verification |
|---|---|---|
| PAR-1 | **Same topology.** Every environment defines the identical service set and networks; an environment may *disable* an optional service (e.g. `sms-sink` in prod) but may never add a service that exists nowhere else. | `docker compose config` diff across overlays — services section must match |
| PAR-2 | **Same images.** `staging` and `production` run byte-identical image digests for a given release; only env vars differ. | Image digest recorded in the release log; `AC-NFR-016-01` |
| PAR-3 | **Layered configuration only.** Differences live in `.env.<environment>` + Compose overlay, never in code branches, `if (env === 'production')` literals, or per-env commits. | Config review; grep gate for environment-name literals in `apps/` |
| PAR-4 | **Disjoint credentials.** dev / staging / production share **no** secret value; sandbox keys are never valid in production and vice versa. | `09-security/secrets-management.md` §3 access matrix |
| PAR-5 | **Non-prod never holds unmasked production PII.** Restored backups are masked before use (`DATA-REQ-002`). | `16-data/data-classification.md` masking rules; seed script assertion |
| PAR-6 | **Topology changes ship as code first.** A new service/volume/network is merged to `main` before any environment adopts it — dev proves it, staging verifies it, production inherits it. | PR review + `docker compose config` in CI |
| PAR-7 | **Parity is a test asset.** Image digests and service sets must match across envs or the release is blocked. | `AC-NFR-016-01` |

## 3. Compose Overlay Layout

Canonical file names follow `../04-architecture/core/deployment-view.md` §1 (Compose v2 reads `compose.yaml` by default; the legacy `docker-compose.yml` spelling is the same file if a tool enforces it).

| Canonical file | Legacy-equivalent name | Purpose | Present in |
|---|---|---|---|
| `compose.yaml` | `docker-compose.yml` | Base: all services, internal networks, volumes, healthchecks, restart policies | local, dev, staging, prod |
| `compose.override.yaml` | `docker-compose.override.yml` | Dev conveniences: hot reload (`node --watch`, Next dev), published dev ports, seed job, `sms-sink` | **local only** (auto-loaded by Compose) |
| `compose.dev.yaml` | `docker-compose.dev.yml` | Shared-dev sizing, CI-integration settings, `sms-sink`, seed service | dev |
| `compose.staging.yaml` | `docker-compose.staging.yml` | Prod sizing, synthetic/sandbox providers, test data job, alert routing to a test channel | staging |
| `compose.prod.yaml` | `docker-compose.prod.yml` | Production sizing, strict port publication (edge only), `unless-stopped` restarts, no test services | production |

Invocation pattern (identical shape everywhere; only the overlay name changes):

```bash
docker compose -f compose.yaml -f compose.prod.yaml --env-file .env.production up -d
docker compose -f compose.yaml -f compose.prod.yaml config   # lint + render before apply
```

What belongs **where**:

| Concern | Base | Override (local) | dev | staging | prod |
|---|---|---|---|---|---|
| Service definitions | ✔ | additive only | additive only | additive only | additive only |
| CPU/memory limits | defaults | relaxed | small | prod-like | full |
| Published host ports | edge 80/443 | + api 3000, web 3000, es 9200, minio 9000, sink 8025 | + sink 8025 | + sink 8025 (test only) | **edge only** |
| Restart policy | `unless-stopped` | `no` | `unless-stopped` | `unless-stopped` | `unless-stopped` |
| Seed/test services | — | ✔ | ✔ | ✔ | ✖ |
| Alertmanager receivers | default routes | none | none | test channel | on-call |

## 4. Refresh & Teardown Policy

| Environment | Refresh trigger | Procedure | Data loss tolerance |
|---|---|---|---|
| local | Developer request | `docker compose down -v && docker compose up -d && npm run seed` | Total — disposable |
| dev | Weekly (Sunday 02:00) **or** after a destructive migration rehearsal | `down -v` → pull new `main` images → `up -d` → run seed | Total; announced in the team channel |
| dev (incremental) | Every merge to `main` | Pull new image tags → recreate app services only; data services persist | None — schema changes apply forward (`DOC-DB-006`) |
| staging | Before every release cycle; always after a `contract`-phase migration | Recreate all services from current tags; re-seed fixtures; run smoke | Total (fixtures are code) |
| staging (prod-like tier) | After the rehearsal | Destroy host/containers; keep the drill report | Total |
| production | **Never torn down.** Schema changes are forward-only; data changes are governed by `16-data/` retention and the account-deletion workflow | `15-deployment/deployment-process.md` | n/a |

**Teardown safety interlocks:**

1. `down -v` is blocked by a guard script outside production (`COMPOSE_PRODUCTION=1` env must be unset and the `.env` file must be `.env.production` before destructive commands are allowed).
2. Production volume removal requires two-person confirmation and is never scripted.
3. Snapshot restore into any environment is a documented operation (`DOC-OPS-007` §6) — restoring *into* production is a disaster-recovery event, not a refresh.

## 5. Mobile Build Environments (outside Compose)

React Native 0.73 apps (`CNT-02` customer, `CNT-03` courier) are **not** containerized and are **not** deployed by this domain's pipelines — they are built by `EAS` / `Gradle` / `Xcode` toolchains on developer machines and CI runners, then distributed through store pipelines (`15-deployment/build-and-release.md` §2, `DEP-12`).

| Aspect | Simulator / emulator | Physical device (DEP-12 lab) |
|---|---|---|
| Used for | Local dev, fast UI iteration, Maestro smoke | Release QA, carrier/OTP testing, RTL rendering, push notifications |
| Backend target | Developer's `local` Compose stack via LAN IP or tunnel | Shared `dev` or `staging` environment (IP allowlist entry per device) |
| OTP delivery | `sms-sink` UI — no carrier involved | **Real carrier SIMs** (`DEP-12`) — the only way to validate `BR-NTF-03` failover and delivery receipts |
| Push (FCM/APNs) | Not validated | Validated against sandbox APNs / FCM test project |
| Coverage required | Optional | Android 10+ matrix and iOS 15+ (`NFR-015`); device-lab runs are **manual and release-blocking** |
| Automation | Maestro flows on emulator | Maestro flows on lab devices (`13-testing/testing-strategy.md` §2.3) |
| Artifacts | Debug builds (`.apk`/`.app`) | Signed internal/tracks builds for QA distribution |

**Rule:** an environment may not be called "staging-equivalent" for mobile unless it runs against the `staging` Compose stack **and** has been exercised on at least one physical Android and one physical iOS device from the `DEP-12` lab.

## 6. Verification

| Check | Method | Evidence |
|---|---|---|
| Topology parity | `docker compose config` service-set diff across overlays | CI artifact per PR (`AC-NFR-016-01`) |
| Digest parity staging↔prod | Release log records digests for both | Release record in `15-deployment/build-and-release.md` §5 |
| Credential disjointness | Config review: `.env.*` sets compared, values never equal | `09-security/secrets-management.md` §8 |
| No production PII in non-prod | Seed script asserts masked phone patterns; manual audit quarterly | `DATA-REQ-002` evidence |
| No seeded weak admin in prod | `seed --only=reference` is the only permitted production seed | Deployment log |
| Dev = prod topology | Service-set diff green in CI | PR check `compose-config` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
