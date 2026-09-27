---
document_id: DOC-OPS-004
title: CI/CD Pipelines (GitHub Actions)
category: 14-devops-infrastructure
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-010, SEC-REQ-007, SEC-REQ-012, DATA-REQ-005, AC-S-08, AC-S-09]
related_documents: [DOC-OPS-001, DOC-OPS-003, DOC-OPS-005, DOC-DPL-003, DOC-TST-002, DOC-SEC-005, DOC-DB-006]
---

# CI/CD Pipelines (GitHub Actions)

GitHub Actions is the only CI/CD system (`04-architecture/technology-stack.md` §4). Pipelines are **gates, not suggestions**: every rule below fails the run rather than warning. Deployment promotion semantics (staging auto, production manual) live in [`15-deployment/`](../15-deployment/README.md); this file owns the workflow definitions and merge gates.

## 1. Workflow Inventory

| Workflow file | Name | Trigger | Purpose | Blocking? |
|---|---|---|---|---|
| `ci.yml` | CI | `pull_request` to `main`, `push` to `main` | PR gate: install → lint → typecheck → unit → build → migration lint → image build smoke → secret scan | **Yes — required check** |
| `nightly-e2e.yml` | Nightly E2E | `schedule` 02:00 UTC daily + `workflow_dispatch` | Playwright critical journeys + TC-* API suite against `staging` | Yes for release; report-only on `main` |
| `release.yml` | Release | `push` of tag `v*.*.*` | Build & push versioned images, generate release notes, promote to production behind approval | Yes — production deploy gate |
| `deploy-staging.yml` | Deploy staging | `push` to `main` (after `ci.yml`) | Pull `:<sha>` images on the staging host, migrate, restart, run smoke | Yes — failure blocks the merge-deploy loop |
| `mobile-build.yml` | Mobile build | `push` to `main` affecting `apps/mobile/**`, `workflow_dispatch` | RN 0.73 build via EAS/Gradle/Xcode — **outside Compose** (`DEP-12`) | Report-only for web merges |
| `dependency-audit.yml` | Dependency audit | `schedule` weekly + `pull_request` | npm audit, Dependabot/Renovate PRs, base-image digest bumps, Trivy image scan | Yes — critical findings block |
| `codeql.yml` | CodeQL SAST | `push`/`pull_request` to `main`, `schedule` weekly | SAST analysis for `SEC-REQ-012` (`SEC-C-23`) | Yes — critical/high block |
| `backup-check.yml` | Backup freshness | `schedule` every 15 min | Verifies WAL age ≤ 15 min and snapshot age ≤ 24 h; raises alert if stale | Yes — failure pages (`AC-DR004-01/02`) |

## 2. PR Gate (`ci.yml`) — Ordered Steps

| # | Step | Command (shape) | Fails the run when |
|---|---|---|---|
| 1 | Checkout + setup | `actions/checkout`, `actions/setup-node` (Node 20, npm cache) | Runner/setup error |
| 2 | Install | `npm ci` | Lockfile out of sync with `package.json` |
| 3 | Format | `prettier --check .` | Any unformatted file |
| 4 | Lint | `eslint . --max-warnings=0` **incl. module-boundary rules** | Any lint error/warning; any illegal cross-block import (`NFR-009`, `DOC-ARCH-006`) |
| 5 | Typecheck | `tsc --noEmit` (project references) | Any type error |
| 6 | Unit tests + coverage | `jest --coverage --ci` | Test failure **or** coverage below thresholds (§4) |
| 7 | Build | `next build` (web) + `nest build` (api) | Build error; bundle budget breach (`NFR-002`) |
| 8 | Migration lint | Prisma validate + `migrate diff` drift check + destructive-pattern scan (M1–M9, `DOC-DB-006` §5) | Drift, out-of-order timestamps, unlabeled destructive change |
| 9 | Seed/fixture assertions | Seed scripts run against an ephemeral Postgres; assert Σ ledger = 0 | Fixture invariant broken |
| 10 | Compose config | `docker compose config -q` + policy assertions (`DOC-OPS-003` §10) | Render error or policy violation |
| 11 | Secret scan | `gitleaks detect --redact --no-banner` | Any credential literal or seeded canary (`AC-SR007-01`) |
| 12 | Dependency audit | `npm audit --audit-level=high` + SCA | High/critical vulnerability above SLA |
| 13 | Docker build smoke | Build `api`, `worker`, `web` images; run `api` container and hit `/healthz` | Image build failure or health endpoint not answering |
| 14 | Upload artifacts | Coverage report, logs, rendered compose config | — |

Unit-suite budget: **< 3 minutes** so it runs on every PR (`NFR-010`); full regression must stay **< 30 minutes** with 0 flakes (`AC-S-09`).

## 3. Branch Protection & Required Checks

Branch: **`main`** (single long-lived branch; feature branches → PR).

| Rule | Setting |
|---|---|
| Required status checks | `lint`, `typecheck`, `unit (coverage)`, `build`, `migration-lint`, `secret-scan`, `dependency-audit`, `compose-config`, `docker-smoke` |
| Required approvals | ≥ 1 review; ≥ 2 for changes under `apps/api/src/b07-wallet/**`, `b06-orders/**`, `prisma/**`, `.github/workflows/**`, `infra/**` |
| Stale reviews dismiss | Yes |
| Force push | Blocked on `main` |
| Signed commits | Required for release tags |
| Linear history | Required (squash or rebase) |
| Deploy environments | `staging` auto; `production` requires reviewer approval (GitHub Environment protection) |
| Admin bypass | Disabled — no `bypass` for the protection ruleset |

## 4. Quality Gates — What Fails the Pipeline

| Gate | Threshold | Canon |
|---|---|---|
| Coverage — overall | ≥ **80%** lines | `AC-S-08`, `NFR-010` |
| Coverage — payment/wallet/escrow (`b07`) | ≥ **95%** | `AC-S-08` |
| Coverage — auth (`b01`) | ≥ **90%** | `AC-S-08` |
| Unit regression duration | < 30 min, **0 reruns/flakes** across 10 consecutive runs | `AC-S-09` |
| Lint | 0 errors, 0 warnings, boundary rules included | `NFR-009` |
| Types | 0 errors (`strict` mode) | `NFR-009` |
| Migration lint | 0 drift, 0 out-of-order timestamps, destructive changes must carry a `contract:` label | `DATA-REQ-005`, `DOC-DB-006` §5 |
| Secret scan | **0** findings (`gitleaks`-class) | `SEC-REQ-007` R2, `AC-SR007-01` |
| SAST (CodeQL) | 0 unfixed **critical**; high must have a ticket + SLA | `SEC-REQ-012`, `SEC-C-24` |
| Dependency scan | 0 critical above SLA; `npm audit` high+ blocks | `SEC-REQ-012`, `SEC-C-23` |
| Image scan (Trivy) | 0 CRITICAL CVEs in the final image; HIGH needs ticket | `SEC-C-24` |
| Bundle budget (customer web) | JS < 200 KB gzipped | `NFR-002` |
| Log schema audit | Rolling 1,000-line extract: 100% JSON, 0 secrets | `AC-NFR-014-01` (daily job) |

## 5. Test Placement — Where TC-* and Playwright Run

| Suite | Tool | Runs on | Against | Blocking |
|---|---|---|---|---|
| Unit + rule tests | Jest | every PR | none (offline, sockets blocked) | Yes |
| Integration / API (`TC-*` API cases) | Jest + Supertest-style | every PR | ephemeral Postgres + Redis service containers | Yes |
| Migration validation | Prisma | every PR | ephemeral shadow DB | Yes |
| Web E2E critical journeys | Playwright | nightly + pre-release | **staging only** | Release-blocking |
| Full TC API regression | Jest/Supertest | nightly | staging | Release-blocking |
| Load (k6, `C-25`) | k6 | weekly + pre-release | staging | `AC-S-05` release gate |
| DAST (ZAP-style) | ZAP | per release | staging | Promotion-blocking (`SEC-C-23`) |
| Accessibility | axe-core + Lighthouse CI | every PR (customer pages) | built `web` | Yes (`AC-S-10`) |
| Mobile flows | Maestro | nightly on `DEP-12` lab devices | staging | Release-blocking for app releases |
| Production | — | **no test suites** beyond passive probes and post-deploy smoke | production | — |

Rule: **E2E never runs against production**; production credentials are unreachable from any test workflow (`13-testing/testing-strategy.md` §7, `DOC-INT-008` §2).

## 6. Caching, Matrix, Concurrency

| Concern | Setting |
|---|---|
| Node cache | `actions/setup-node` with `cache: npm` keyed on `package-lock.json` |
| Build cache | `actions/cache` for `node_modules`, `.next/cache`, `dist`, Prisma client generate output |
| Docker layer cache | `docker/build-push-action` with `GHA` cache backend; no cache mount that persists secrets |
| Test matrix | Node **20** only in v1 (single supported runtime, `DEP-01`); OS matrix `ubuntu-latest` (runner) — no Windows/macOS runners |
| Playwright matrix | Chromium + Firefox + WebKit (last-2-versions coverage, `NFR-015`) |
| Concurrency | `concurrency: { group: ci-<PR#>, cancel-in-progress: true }` for PRs; **never** cancel in-progress staging/prod deploys |
| Job timeout | 20 min default, 45 min for E2E/k6 |
| Retention | Run logs 90 days (`RC-02`); coverage artifacts 90 days |

## 7. Promotion Flow

```text
feature branch ──PR──► ci.yml (all required checks) ──approve/merge──► main
                                                          │
                                                          ├──► deploy-staging.yml
                                                          │      pull :<sha> → migrate deploy → restart → smoke
                                                          │      → nightly-e2e.yml against staging
                                                          │
                                                          └──► tag v1.4.0 ──► release.yml
                                                                 build+push versioned images
                                                                 → GitHub Environment "production"
                                                                 → reviewer approval (ADMIN)
                                                                 → 15-deployment/deployment-process.md runbook
```

- **Staging deploys automatically on every merge to `main`.**
- **Production deploys only from a release tag, after manual approval** by a repository admin, using the runbook in `15-deployment/deployment-process.md`.
- Re-running a failed deploy always re-runs from a clean, digest-pinned state — never from a half-applied manual change.

## 8. Badge & Status Policy

| Surface | Rule |
|---|---|
| README badges | `ci.yml` status, coverage %, nightly E2E status — refreshed on `main` only |
| Red badge on `main` | Treated as an incident for the owning block: fix forward or revert within the same day |
| Red badge on a PR | Merge blocked; no "merge anyway" |
| Release readiness | `release.yml` refuses to start if the latest `main` CI run is not green |
| Evidence | Every gate result links to a run URL recorded in the release record (`15-deployment/build-and-release.md` §5) |

## 9. Verification

| Check | Method | Evidence |
|---|---|---|
| Required checks actually required | Branch-protection API audit (quarterly) | Config export in repo `infra/gh/` |
| Coverage gate real | Deliberately lower a threshold in a branch → pipeline must fail | Negative test recorded at review |
| Secret scan catches planted credential | Seeded canary in a test branch | `AC-SR007-01` |
| E2E only on staging | Workflow trigger review + environment scoping | Workflow YAML review |
| No secrets in workflows | `gitleaks` over `.github/**`; secrets referenced only as `${{ secrets.* }}` | `SEC-REQ-007` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
