---
document_id: DOC-DPL-003
title: Production Deployment Process (Runbook)
category: 15-deployment
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-005, NFR-020, DATA-REQ-004, DATA-REQ-005, SEC-REQ-010]
related_documents: [DOC-DPL-001, DOC-DPL-002, DOC-DPL-004, DOC-DPL-005, DOC-OPS-003, DOC-OPS-007, DOC-DB-006, DOC-NFD-006]
---

# Production Deployment Process (Runbook)

Executed after a release tag is created and a repository admin approves the GitHub `production` environment. Target: complete a normal release in **≤ 15 minutes** with **0 failed customer requests** (`AC-NFR-020-02`); roll back within 15 minutes if anything fails (`AC-S-20`).

## 1. Pre-Deploy Checks (all must be PASS)

| # | Check | How | Fail action |
|---|---|---|---|
| 1 | CI green on the tagged commit | GitHub checks panel | Do not deploy |
| 2 | Staging deployed with the same digests and green smoke + E2E | `deploy-staging.yml` result | Do not deploy |
| 3 | **Backup fresh**: WAL age ≤ 15 min, latest snapshot ≤ 24 h, off-host copy verified | `backup-check.yml` + backup dashboard | **Do not deploy** — fix backup first |
| 4 | Migration classification reviewed: every new migration labeled `expand` / `data-fix` / `contract`, backward-compatible with the **currently running** app version | PR review + `DOC-DB-006` checklist | Do not deploy |
| 5 | No open CRITICAL security finding in the release | Scan reports (`SEC-REQ-012`) | Do not deploy |
| 6 | Error budget healthy (no active burn-rate page, no change freeze) | SLO dashboard (`DOC-NFD-004` §2) | Reschedule |
| 7 | Rollback target known: previous release tag (N-1) and images N-2 available in GHCR | Release record | Do not deploy |
| 8 | Deploy window in policy (§4); maintenance page staged if schema-heavy | Calendar + change record | Reschedule |
| 9 | On-call engineer aware of the deploy window | Chat/notification | Reschedule |

**Approval:** GitHub Environment `production` requires a reviewer with the repository **admin** role; the approver may not be the same person who authored the release commit (two-person rule, `INFERENCE`).

## 2. Ordered Deploy Steps

```text
0. Announce      → status channel: release tag, window start, expected impact
1. Freeze        → stop staging promotions; pause non-critical jobs (retention purge, reindex)
2. Pre-snapshot  → trigger an on-demand PostgreSQL snapshot (extra restore point)
3. Pull          → docker compose pull (digest-pinned) for api/worker/web/edge config
4. Migrate       → docker compose run --rm migrate   →  prisma migrate deploy  (forward-only)
                   • halts the deploy on failure — no partial rollout past a failed step
5. Restart api   → one replica at a time, readiness-gated (/readyz green before the next)
6. Restart worker→ stop old, start new; drain in-flight jobs (SIGTERM, §3)
7. Restart web   → recreate web container; edge upstream re-checks /healthz
8. Edge reload   → nginx -t && nginx -s reload (config only, no connection drop)
9. Cache warm    → prime catalog/category/feature caches on read-heavy endpoints
10. Reindex      → only if mappings changed; otherwise nightly job covers it
11. Smoke        → post-deploy suite (§5)
12. Watch        → 15-minute observation on dashboards (errors, latency, queue depth, DLQ)
13. Record       → write the deploy record (§6)
14. Unfreeze     → resume paused jobs; close the announcement
```

Each step is a script under `infra/deploy/` so the runbook and the code cannot drift; a step that fails stops the sequence and invokes [`rollback.md`](rollback.md).

## 3. Graceful Worker Restart

| Step | Detail |
|---|---|
| SIGTERM to worker | Docker stop with `stop_grace_period: 60s` |
| BullMQ semantics | Worker finishes the **in-flight job** then stops; unstarted jobs stay in the queue and are picked up by the new process (`BR-PLT-01`) |
| Never force-kill money jobs | Grace period must exceed the longest money-job duration; verified by the queue-drain metric |
| After restart | Queue depth returns to baseline ≤ 5 min; DLQ depth must stay 0 (`DOC-NFD-004` §7) |

## 4. Zero-Downtime Limits — Honest Statement (`C-22`)

| Claim | Reality on a single Compose host |
|---|---|
| "Zero-downtime deploys" | **Approximately true for API process restarts**: N stateless replicas behind the edge with readiness gating keep a serving instance available; edge reload is connection-preserving |
| Connection blips | A brief **drop of in-flight requests** is possible while a replica is removed and re-added; clients retry because all writes are idempotency-keyed (`BR-PLT-03`). Target: 0 failed **customer-visible** requests, < 0.1% 5xx during the window (`AC-NFR-020-02`) |
| Single replica | If only one `api` replica is configured, a restart causes a **seconds-level gap** — acceptable only outside peak hours; otherwise scale to ≥ 2 replicas first |
| Schema-heavy releases | Migrations that lock tables or rewrite rows (enum contraction, `SET NOT NULL`, index builds on large tables) require a **maintenance window**: enable `maintenance_mode`, serve the static maintenance page, run the contract phase, then reopen |
| Data services | PostgreSQL/Redis/ES restarts are **not** zero-downtime on one host — schedule them in a maintenance window; DB restart is a restore-grade event (`RTO ≤ 1 h`) |
| Not available in v1 | Rolling deploys across hosts, blue/green, canary — these require a second host or an orchestrator, both excluded by `C-22` |

**Maintenance page:** a static, cached page served by `edge` when `maintenance_mode` is on (`DOC-OPS-005` §4.1); `/healthz`, `/readyz` and asset paths stay exempt so probes and CDN keep working. Copy is bilingual (`ar` default, `en` parity, `BR-PLT-05`). Honest 5xx/maintenance responses — never fake success (`DOC-NFD-004` §4).

## 5. Post-Deploy Smoke Suite

Runs against production immediately after step 11; each item is a hard gate.

| # | Check | Endpoint / action | Pass |
|---|---|---|---|
| 1 | Liveness | `GET /healthz` | 200 < 1 s |
| 2 | Readiness | `GET /readyz` | 200, all required checks UP |
| 3 | Static home | `GET /` | 200, correct locale (`ar`), no console errors |
| 4 | API version banner | `GET /api/v1/…` health-adjacent endpoint | 200, expected build id |
| 5 | Login | Seed-less smoke account login (staging-only credential in prod is forbidden — use a dedicated smoke account created at launch) | 200 + valid tokens |
| 6 | Search | `GET /api/v1/search?q=…` | 200 with results **or** documented degraded mode (ES down ⇒ category browse still works) |
| 7 | Catalog read | Category browse + product detail | 200, cache hit ratio recovering |
| 8 | Checkout **sandbox** | Place a test order with a smoke account and a `SMOKE_TEST`-flagged wallet credit **only if** the environment flag permits; otherwise validate the checkout dry-run endpoint | Order created idempotently, ledger balanced |
| 9 | Queue health | BullMQ depth + DLQ | Depth draining, **DLQ = 0** |
| 10 | Error rate | 5-minute window on the error dashboard | **< 1%**, no 5xx spike |
| 11 | Migration state | `_prisma_migrations` latest = expected | Applied, no failed rows |
| 12 | Logs | Last 5 min of `api`/`worker` | No new error class; no secrets (audit script) |

**Observation window:** 15 minutes with dashboards #1–#4 and #7 open (`DOC-NFD-006` §5). Any P1 alert during the window ⇒ rollback decision tree (`DOC-DPL-004` §5).

> Test-data rule: production smoke never moves real customer money. Where a money-path check is required, it uses a dedicated smoke account with a segregated, clearly-labeled balance, and the transaction is reconciled out afterwards (`13-testing/testing-strategy.md` §7: production gets passive probes + smoke only).

## 6. Deploy Log / Audit Record

Every production deploy writes a `BR-PLT-06`-compatible entry (append-only) and a release record:

| Field | Content |
|---|---|
| Release tag + commit SHA | `v1.4.0` @ `9f3c1ab` |
| Image digests | `api`, `web` (worker shares `api`) |
| Migrations applied | list with phase labels |
| Start / end timestamps | UTC, wall-clock duration |
| Approver | GitHub username + role (ADMIN) |
| Executor | who ran the runbook (may equal approver only if policy allows; otherwise separate) |
| Result | SUCCESS / ROLLED_BACK / FAILED_STOPPED |
| Smoke outcome | pass/fail per item in §5 |
| Observations | any anomaly during the 15-min window |
| Evidence links | CI run, dashboards snapshot, staging E2E run |

Retention: deploy records are operational audit data — retained with the audit class (`RC-06`) since they are privileged platform actions.

## 7. Who May Deploy

| Role | Permission | Mechanism |
|---|---|---|
| Repository **admin** | Approve the `production` environment; trigger `release.yml` | GitHub Environment protection rules |
| Ops owner | Execute the runbook steps on the host | SSH key restricted by `DOC-OPS-008` §2 |
| Engineering (standard) | Merge to `main` → **staging only** | Branch protection |
| CI (no human) | Deploy to `staging` automatically | `deploy-staging.yml` |
| Anyone | **Nobody** may deploy to production without a tag + approval | Environment gate; no self-approval for the release author |

Emergency/rollback deploys follow the same approval path but with an expedited two-person confirmation recorded in the incident log.

## 8. Mobile App Releases — Decoupled

| Aspect | Policy |
|---|---|
| Coupling | Mobile releases are **not** gated by or gated on web deploys; they ship on the store-review cadence |
| Compatibility | Clients pin `/api/v1`; additive API changes deploy first, app updates follow |
| Coordinated change | A breaking API change requires a deprecation window: new version deployed, old version served until the app base has migrated (`07-api/api-conventions.md`) |
| QA gate | `DEP-12` device-lab pass (Android 10+, iOS 15+, carrier OTP) before store submission |
| Rollback | Store rollback = halt rollout + ship a fix build; server-side can revert via feature flags where possible |

## 9. Verification

| Check | Method | Evidence |
|---|---|---|
| Runbook executable by someone other than its author | Annual runbook walkthrough | Rehearsal log (`AC-S-19`) |
| Deploy with 0 failed requests | Staging deploy measurement | `AC-NFR-020-02` |
| Pre-deploy backup check really blocks | Failure-injection: stale backup ⇒ deploy refuses | `AC-DR004-02` |
| Approval gate real | Attempt deploy without approval | Environment ruleset export |
| Deploy record written | Audit query for the deploy event | `BR-PLT-06` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
