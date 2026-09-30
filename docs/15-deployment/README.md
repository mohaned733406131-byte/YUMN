---
document_id: DOC-DPL-001
title: Deployment — README (15-deployment Index)
category: 15-deployment
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-005, NFR-006, NFR-020, DATA-REQ-004, DATA-REQ-005, SEC-REQ-012]
related_documents: [DOC-OPS-001, DOC-ARCH-005, DOC-DB-006, DOC-NFD-004, DOC-NFD-006, DOC-TST-003]
---

# 15-deployment — How yumn Reaches Production

**yumn (يُمن)** — multi-vendor marketplace for Yemen; wallet-only payments (`C-01`); modular monolith (`C-21`); Docker Compose on a single host per environment (`C-22`, `ADR-004`).

## 1. Purpose & Boundary

This domain owns the **release lifecycle**: what artifact ships, how it is versioned, the ordered production runbook, rollback strategy, the health model that gates traffic, and the go-live checklist. It consumes infrastructure from [`14-devops-infrastructure/`](../14-devops-infrastructure/README.md) and never redefines it.

| This domain owns | This domain does **not** own | Rule of thumb |
|---|---|---|
| Release artifacts, versioning, release notes, registry | Compose service definitions, images, networks (`../14-devops-infrastructure/core/docker-compose.md`) | "What ships and what is it called?" → here |
| Ordered deploy steps, deploy windows, maintenance page, deploy records | Workflow definitions and merge gates (`../14-devops-infrastructure/core/ci-cd.md`) | "What do I run, in what order, when?" → here |
| Rollback strategy by change type, triggers, decision tree | Backup execution mechanics (`../14-devops-infrastructure/core/backup-recovery.md`) | "How do we undo it safely?" → here |
| Health model: liveness/readiness semantics, probes, graceful shutdown | Alert thresholds and dashboards (`../12-non-functional/core/observability.md`) | "What makes a node ready to serve?" → here |
| Go-live checklist and sign-offs | What the requirements are (`02-requirements/`) | "Is everything proven before launch?" → here |
| — | Test case design (`13-testing/`) — this domain supplies *where* tests run | — |
| — | Schema migration rules (`../08-database/core/migrations-and-evolution.md`) — this domain executes them | — |

## 2. File Index

| # | File | Document ID | Content | Source of truth |
|---|---|---|---|---|
| 1 | [README.md](README.md) | `DOC-DPL-001` | Domain charter, release-flow summary, index, pointer map | Yes |
| 2 | [build-and-release.md](core/build-and-release.md) | `DOC-DPL-002` | Artifacts, SemVer + image tags, release branches/tags, notes, reproducibility, GHCR | No (supporting) |
| 3 | [deployment-process.md](core/deployment-process.md) | `DOC-DPL-003` | Production deploy runbook: pre-checks, ordered steps, windows, smoke, records, approvers | Yes |
| 4 | [rollback.md](core/rollback.md) | `DOC-DPL-004` | Rollback by change type, trigger criteria, decision tree, rehearsal, post-incident review | Yes |
| 5 | [health-checks.md](core/health-checks.md) | `DOC-DPL-005` | `/healthz` + `/readyz` semantics, probes, startup ordering, graceful shutdown, monitoring hooks | Yes |
| 6 | [production-readiness.md](core/production-readiness.md) | `DOC-DPL-006` | Go-live checklist grouped by area with owner, verification method, status, evidence; sign-off | No (supporting) |
| [`core/`](core/README.md) | DOC-DPL-007 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-DPL-008 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-DPL-009 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-DPL-010 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-DPL-011 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

Domain numbering prefix: **`DOC-DPL-NNN`**. Nothing outside this directory may mint a `DOC-DPL` ID.

## 3. Release Flow Summary

```text
  developer            CI                     staging                    production
 ───────────      ──────────────────       ──────────────────         ────────────────────
  feature branch
        │
        ▼
   open PR ────►  ci.yml
                  install → lint → typecheck
                  → unit (coverage gates)
                  → build → migration lint
                  → secret/dep/SAST scans
                  → docker build smoke
                        │ all required checks green
                        ▼
                  approve + merge to main
                        │
        ┌───────────────┴───────────────┐
        ▼                               │
  deploy-staging.yml                    │
  pull :<sha> images                    │
  → prisma migrate deploy               │
  → restart api/worker/web              │
  → smoke suite                         │
  → Playwright E2E (nightly)            │
        │                               │
        │  smoke + E2E green            │
        ▼                               │
   tag v1.4.0 ──────────────────►  release.yml
                                   build/push versioned images (GHCR)
                                          │
                                          ▼
                                   GitHub Environment
                                   "production"
                                   ── manual approval by ADMIN ──┐
                                                                ▼
                                                     deployment-process.md
                                                     pre-checks → pull → migrate
                                                     → api → worker → web → cache warm
                                                     → smoke → watch 15 min
                                                                │
                                          ┌─────────────────────┴──────────┐
                                          ▼                                ▼
                                   green: record release            red: rollback.md
                                   + post-deploy smoke              (≤ 15 min, AC-S-20)
```

Text form of the same chain:

```text
merge → CI → staging auto-deploy → smoke (+ E2E) → manual production approval
      → deploy (ordered steps) → verify (smoke + 15-min watch) → record
```

| Stage | Gate | Failure path |
|---|---|---|
| Merge to `main` | All required checks green (`../14-devops-infrastructure/core/ci-cd.md` §3) | No merge |
| Staging auto-deploy | Smoke suite green; 5xx spike < 0.1% over the 5-min window (`AC-NFR-020-02`) | Revert the merge or fix forward; staging never promotes a red build |
| Production approval | Manual review by a repository admin in the GitHub `production` environment | Approval withheld |
| Production deploy | Ordered runbook completed; `/readyz` green; post-deploy smoke green; error rate < 1% over 5 min | `rollback.md` decision tree |
| Mobile release | Decoupled — store review cadence, not tied to web deploys | Ship separately (`DOC-DPL-002` §2) |

## 4. What Lives Where — Pointer Map

| Question | Authoritative location |
|---|---|
| Which workflows run, what blocks a merge | `../14-devops-infrastructure/core/ci-cd.md` |
| Compose services, ports, volumes, image sources | `../14-devops-infrastructure/core/docker-compose.md` |
| Environment matrix, overlays, parity rules | `../14-devops-infrastructure/core/environments.md` |
| Env vars, feature flags, boot validation | `../14-devops-infrastructure/core/configuration.md` |
| Dashboards, alert routing, log pipeline, uptime probes | `../14-devops-infrastructure/core/monitoring-stack.md` |
| Backup jobs, restore steps, quarterly drill | `../14-devops-infrastructure/core/backup-recovery.md` |
| Host hardening, scanning cadence, TLS renewal | `../14-devops-infrastructure/core/host-hardening.md` |
| Migration ordering, expand/contract, forward-only rules | `../08-database/core/migrations-and-evolution.md` (`DOC-DB-006`) |
| Topology contract (services, restart, degraded mode, RTO/RPO placement) | `../04-architecture/core/deployment-view.md` |
| Availability math, error budget, degradation matrix, drills | `../12-non-functional/core/reliability.md` |
| Health endpoint timing, deploy observation window, rollback timing | `../12-non-functional/core/observability.md` §8 |
| API versioning (`/api/v1`) | `../07-api/core/api-conventions.md`, `07-api/README.md` |
| Test placement (E2E on staging, k6, DAST) | `../13-testing/core/testing-strategy.md` §7, `../13-testing/core/test-plans.md` |
| Degraded readiness semantics (ES down ⇒ ready) | `../10-integrations/core/integration-overview.md` §3–§4 |

## 5. Governing Principles

| # | Principle | Anchor |
|---|---|---|
| P1 | **Deploy is a rehearsed runbook, not improvisation.** Ordered steps, recorded, repeatable. | `NFR-020` |
| P2 | **Schema is forward-only.** Expand/contract; no `migrate down` in production; a bad migration is fixed forward or the data is restored from backup. | `DATA-REQ-005`, `DOC-DB-006` §2 |
| P3 | **Human gate on production.** No automatic promotion of a release to production. | `15-deployment` policy |
| P4 | **Health gates traffic.** Nothing serves requests until it reports ready; an instance is removed from rotation in ≤ 30 s. | `BR-PLT-07` |
| P5 | **Rollback must be faster than the damage.** Target ≤ 15 min, rehearsed every release cycle. | `AC-S-20` |
| P6 | **Zero failed customer requests on deploy** — if that cannot be guaranteed for a change, schedule a maintenance window. | `AC-NFR-020-02` |
| P7 | **Honest limits.** Single-host Compose gives brief connection drops on restart, not perfect zero-downtime; schema-heavy releases use a maintenance window. | `C-22`, `DOC-NFD-004` §3 |
| P8 | **Every deploy is recorded.** Who, what, when, image digests, result. | `BR-PLT-06` |

## 6. Reading Order & Verification

**Reading order:** this README → `health-checks.md` (the gate everything else depends on) → `build-and-release.md` → `deployment-process.md` → `rollback.md` → `production-readiness.md`.

**Verification:** this domain is verified through `AC-NFR-020-01` (health timing, runbooks), `AC-NFR-020-02` (deploy with 0 failed requests, rollback ≤ 15 min), `AC-S-19`/`AC-S-20` (runbook + rollback rehearsal evidence), `AC-DR004-*` (restore readiness before launch), `AC-S-05`/`AC-S-06` (load and availability gates), and the go-live sign-off in `production-readiness.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-DPL-007…DOC-DPL-011) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
