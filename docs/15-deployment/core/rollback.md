---
document_id: DOC-DPL-004
title: Rollback Strategy & Decision Tree
category: 15-deployment
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-005, NFR-006, NFR-007, NFR-020, DATA-REQ-005, DATA-REQ-004]
related_documents: [DOC-DPL-003, DOC-OPS-007, DOC-DB-006, DOC-NFD-004, DOC-NFD-006, DOC-TST-003]
---

# Rollback Strategy & Decision Tree

**Target: a completed rollback within 15 minutes with evidence** (`AC-S-20`, `AC-NFR-020-02`). The strategy depends entirely on *what kind of change failed* — application code and configuration roll back cheaply; schema changes do **not** roll back at all.

## 1. Rollback Strategies by Change Type

| Change type | Rollback method | Time budget | Data risk | Notes |
|---|---|---|---|---|
| **App configuration (env var / feature flag)** | Revert the env file value or flip the flag, then restart affected services (or wait ≤ flag TTL 30 s) | ≤ 5 min | None | Cheapest path — always try flags first |
| **Feature flag only** | `feature:{flag}` ← off | ≤ 1 min | None | Preferred containment for risky behaviour |
| **App code (container image)** | Redeploy the **previous image tags** (N-1; images kept to **N-2**) with `docker compose up -d` | ≤ 15 min | None — provided no schema change was applied | The default code rollback |
| **Edge / nginx config** | `nginx -t` + reload previous config from git | ≤ 5 min | None | Config is in the repo |
| **Monitoring/alert config** | Revert repo file, provisioning reloads | ≤ 5 min | None | Never roll back the app to fix monitoring |
| **DB schema (expand phase applied)** | **No schema rollback.** Keep the new schema; roll back **app containers only** — the schema is backward compatible by design | ≤ 15 min | None | Core benefit of expand/contract (`DOC-DB-006` §3) |
| **DB schema (contract phase applied)** | **Forward fix only.** Contract phases run in a maintenance window after the app version has been stable — never reverse them in place | hours (planned) | Medium | Reversal = new migration restoring the old shape, or restore |
| **Bad migration that failed mid-run** | `migrate deploy` halts on failure; DB stays on the last good version → fix forward with a corrected migration | ≤ 15 min to stop, + fix time | Low | Never `migrate down` in production (`DOC-DB-006` §2) |
| **Data corruption discovered** | Restore from backup per [`../../14-devops-infrastructure/core/backup-recovery.md`](../../14-devops-infrastructure/core/backup-recovery.md) §6 to a point before corruption | ≤ 60 min (RTO) | **RPO ≤ 15 min accepted** | Highest-cost path; requires incident command |
| **Elasticsearch mapping issue** | Reindex from PostgreSQL (drop/recreate index + full rebuild) — ES is derived (`RC-08`) | ≤ 60 min | None | Never restore ES from backup |
| **Redis loss / bad cache data** | Flush cache namespace (not the queue DB); queues recover via AOF + BullMQ redelivery | ≤ 5 min | Cache only | Queue DB flush is a last resort with incident review |
| **Dependency/CVE discovered post-deploy** | Roll back image, then rebuild on a patched base | ≤ 15 min | None | SLA still applies to the fix (`SEC-C-24`) |

## 2. Rollback Trigger Criteria

| Trigger | Threshold | Action | Source |
|---|---|---|---|
| Error rate | **> 1% for 5 minutes** after deploy | Automatic rollback recommendation → operator confirms | Deploy watch (`DOC-DPL-003` §5) |
| Health failure | `/readyz` failing on any replica > 60 s, or `/healthz` unreachable | Automatic rollback | `BR-PLT-07` |
| Smoke suite failure | Any item in `DOC-DPL-003` §5 fails | **Manual rollback** — deploy is not considered complete | Runbook gate |
| 5xx spike | ≥ 0.1% 5xx during the deploy window | Rollback (goal is 0 failed requests) | `AC-NFR-020-02` |
| DLQ depth | > 0 caused by the new release | Rollback; then replay DLQ | `BR-PLT-02` |
| Migration failure | `migrate deploy` non-zero | **Halt** — do not roll back the schema; fix forward | `DOC-DB-006` §2 |
| Money-path anomaly | Ledger imbalance, duplicate credit, negative balance | Immediate rollback + incident; consider restore | `AC-S-14`, `NFR-008` |
| Latency regression | p95 write > 500 ms for 5 min post-deploy | Rollback | `NFR-001` |
| Security finding | Critical vuln introduced by the release | Rollback + patch | `SEC-REQ-012` |
| Error-budget burn | Deploy pushes burn above 2× allowed rate | Rollback + freeze | `DOC-NFD-004` §2 |

**Two-person decision for data-affecting rollbacks:** restoring from backup or running a contract reversal requires the ops owner **and** the incident commander; everything else can be executed by the on-call engineer who then records it.

## 3. Decision Tree

```text
DEPLOY FAILED / ANOMALY DETECTED
│
├─ Is data at risk or corrupted?
│    YES ─► INCIDENT COMMANDER TAKES OVER
│            ├─ corruption bounded & time-known? ─► point-in-time restore (backup-recovery §6)
│            │                                       accept RPO ≤ 15 min, RTO ≤ 60 min
│            └─ unknown scope? ─► freeze writes, preserve evidence, restore to clean host,
│                                 reconcile (Σ ledger = 0) before reopening
│    NO ──▼
│
├─ Did `prisma migrate deploy` fail?
│    YES ─► HALT. DB is on last good version. NO schema rollback.
│            ├─ migration never applied ─► fix the migration file, re-run deploy
│            └─ migration partially applied ─► inspect `_prisma_migrations`;
│                                 write a corrective **forward** migration, then resume
│    NO ──▼
│
├─ Is the failure explainable by configuration or a feature flag?
│    YES ─► REVERT ENV / FLAG  (≤ 5 min) ─► restart or wait TTL ─► verify smoke ─► done
│    NO ──▼
│
├─ Was a CONTRACT-phase schema change applied in this release?
│    YES ─► maintenance page ON ─► forward-fix migration to restore the old shape
│            (or restore from backup if data is affected) ─► redeploy previous app ─► verify
│    NO ──▼
│
├─ Is search the only broken surface?
│    YES ─► reindex from PostgreSQL; do NOT roll back the app for an ES-only issue
│    NO ──▼
│
└─ ROLL BACK APPLICATION IMAGES (default)
     1. `docker compose pull` previous tag (N-1, images kept to N-2)
     2. `up -d` api (readiness-gated) → worker → web
     3. edge reload if config changed
     4. re-run smoke suite
     5. confirm error rate < 1% over 5 min
     6. record ROLLBACK in the deploy record + incident note
     7. if still failing ─► escalate to restore path (top of tree)
```

## 4. What Must NOT Be Done

| Prohibited | Why |
|---|---|
| `prisma migrate down` / `migrate dev` in production | Forward-only policy (`DOC-DB-006` §2); destructive and untested |
| Editing rows by hand to "undo" a release | Bypasses audit; ledger corrections are compensating entries only (`DATA-REQ-007`, `BR-PAY-06`) |
| Selective deletion/rewriting of backups | Breaks restorability (`DOC-DTA-005` §5.7) |
| Rolling back the app to fix a monitoring/alert problem | Wrong layer |
| Restoring a backup as a routine "rollback" | Restore is a disaster path with RPO acceptance, not a release tool |
| Force-pushing `main` to undo a merge | History is immutable; roll forward with a revert PR |
| Deploying an untested "quick fix" over a failed release | Fix forward through the same gates |

## 5. Rollback Rehearsal Requirement

| Aspect | Definition |
|---|---|
| Cadence | **Every release cycle** — at minimum once before each production release train; drill 8 of the quarterly game-day (`DOC-NFD-004` §8) |
| Environment | **Staging** with production-equivalent topology |
| Procedure | Deploy release N, introduce a deliberate failure (bad env value or buggy route), execute the full decision tree to a completed rollback |
| Pass criteria | Rollback completes **≤ 15 min**; 0 failed customer-equivalent requests (< 0.1% 5xx); smoke green afterwards; evidence recorded |
| Evidence | Timestamps, commands, dashboards export attached to the release record |
| Test design | Executable plan in `../../13-testing/core/test-plans.md` §h (rollback rehearsal) — referenced by `AC-S-20` |
| Failure to rehearse | No rehearsal ⇒ no release approval (checklist row in `production-readiness.md`) |

Additional rehearsals: quarterly **restore-from-backup** drill (`DOC-OPS-007` §8) covers the data-corruption branch; migration forward-fix rehearsal runs whenever a contract-phase migration is introduced.

## 6. Keeping Rollback Targets Available

| Requirement | Rule |
|---|---|
| Image retention | Release-tagged images kept **indefinitely**; at minimum the previous **N-2** releases must exist in GHCR before a new release deploys |
| Previous config | Previous `.env.<environment>` archived encrypted off-host on every config change (`DOC-OPS-007` §4) |
| Previous migration set | Git history — migrations are additive; rolling *code* back never requires removing migration files |
| Pre-deploy snapshot | Every production deploy triggers an on-demand PostgreSQL snapshot (step 2 of `DOC-DPL-003` §2) — the cheapest restore point |
| Known-good tag | The release record names the exact rollback target before deployment starts |

## 7. Post-Incident Review

| Step | Detail |
|---|---|
| Trigger | Any rollback, any failed deploy, any restore — mandatory |
| Timing | Within **48 h** of resolution (`DOC-NFD-004` §2 style) |
| Inputs | Deploy record, alert timeline, dashboards, log extracts by `requestId`, decision-tree path taken |
| Questions | Why did the gate not catch it earlier? Was the trigger threshold right? Did the rollback take ≤ 15 min? Was the runbook accurate? |
| Outputs | Action items with owners; updates to `DOC-DPL-003`/`DOC-DPL-004` if the runbook was wrong; new/adjusted alert if detection was slow; new test case if coverage was missing |
| Records | Incident entry + release record marked `ROLLED_BACK`; risk register updated if a new exposure appeared (`17-risk-management/core/risk-register.md`) |
| Sign-off | Incident commander closes; recurring rollback causes escalate to the error-budget freeze policy (`DOC-NFD-004` §2) |

## 8. Verification

| Check | Method | Evidence |
|---|---|---|
| Rollback ≤ 15 min | Staging rehearsal with timers | `AC-S-20` |
| 0 failed requests on deploy+rollback | Error dashboard over the window | `AC-NFR-020-02` |
| N-2 images present | Registry query before release | §6 |
| Decision tree accurate | Walkthrough during rehearsal; update doc on mismatch | Rehearsal log |
| Restore branch works | Quarterly drill (`DOC-OPS-007` §8) | `AC-DR004-03` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
