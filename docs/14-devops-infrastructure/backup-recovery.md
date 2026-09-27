---
document_id: DOC-OPS-007
title: Backup & Recovery Execution (DATA-REQ-004)
category: 14-devops-infrastructure
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-004, NFR-006, NFR-005, DATA-REQ-003, DATA-REQ-007, SEC-REQ-006, SEC-REQ-007]
related_documents: [DOC-DR-004, DOC-DTA-005, DOC-NFD-004, DOC-SEC-005, DOC-OPS-006, DOC-OPS-008, DOC-DPL-004]
---

# Backup & Recovery — Execution of DATA-REQ-004

Requirement, acceptance criteria and RPO/RTO numbers live in [`02-requirements/data/DATA-REQ-004.md`](../02-requirements/data/DATA-REQ-004.md) (`RTO ≤ 1 h`, `RPO ≤ 15 min`, `NFR-006`, `C-26`); retention windows live in `16-data/retention-and-archival.md` (`RC-09`). This document is **how** the jobs run, where copies go, how restore works, and how the drill proves it.

## 1. Backup Matrix by Store

| Store | What is backed up | Method | Frequency | RPO (designed) | RTO (designed) | Why |
|---|---|---|---|---|---|---|
| **PostgreSQL 16** (`pgdata`) | Full logical dump | `pg_dump -Fc` (custom format, parallel) | **Nightly 02:00** + pre-deploy snapshot | 24 h via snapshot alone | ≤ 60 min | `DATA-REQ-004` R2 |
| **PostgreSQL 16** | WAL segments (continuous) | `archive_command` → ship every segment (**≤ 5 min**, `DOC-NFD-004` §6) | continuous | **≤ 15 min** (target ≤ 5 min for margin) | ≤ 60 min (PITR) | `DATA-REQ-004` R1, `AC-DR004-01` |
| **MinIO** (`miniodata`) | Media + KYC objects | nightly `tar` of bucket data **or** S3-API batch copy, with manifest checksums | **Nightly 03:00** | 24 h | ≤ 60 min | Objects are authoritative (`DOC-DTA-001` §3) |
| **Redis** (`redisdata`) | AOF + RDB files | AOF `everysec` is continuous; nightly file copy | continuous (AOF) + nightly copy | ~1 s (AOF) / 24 h (file copy) | ≤ 30 min | Cache is rebuildable; **queue payloads are replayable** (`NFR-007`) |
| **Elasticsearch** (`esdata`) | — | **No backup** — full reindex from PostgreSQL (nightly rebuild job) | rebuild only | 0 (derived) | ≤ 60 min (reindex) | `RC-08`, `DOC-DTA-001` §3 |
| **Prometheus / Grafana / Alertmanager** | — | **No backup** — dashboards, rules and routes are provisioned from the repo | n/a | 0 | ≤ 15 min (re-provision) | `DOC-ARCH-005` §4 |
| **App configuration + secrets** | `.env.<environment>`, nginx config, edge certs | Encrypted archive (`age`/`gpg`, passphrase in `BACKUP_ENCRYPTION_PASSPHRASE`) copied off-host | On change + weekly | 7 days | ≤ 15 min | `SEC-REQ-007`, `SEC-REQ-006` |
| **Audit trail** | Included in the PostgreSQL dump | Same as PostgreSQL | as above | ≤ 15 min | ≤ 60 min | `SEC-REQ-010`, `RC-06` |

**Session note (`INFERENCE`):** Redis also holds session/refresh-registry state. Loss of Redis is *acceptable* — access tokens are stateless JWT (15 min, `C-08`) and refresh tokens are single-use rotation records that can be re-validated against PostgreSQL; worst case users re-authenticate. What must **not** be lost silently is queue work, which the AOF plus BullMQ redelivery covers.

## 2. RTO / RPO Targets per Store

| Store | RPO target | RTO target | Evidence status |
|---|---|---|---|
| PostgreSQL (committed transactions) | **≤ 15 min** | **≤ 60 min** | `VERIFIED` — `NFR-006`, `C-26` |
| MinIO objects | ≤ 24 h (object snapshot) — `INFERENCE`; media loss of ≤ 24 h is recoverable but unacceptable for KYC docs, so KYC bucket is copied with the **pre-deploy** snapshot too | ≤ 60 min | `INFERENCE` (canon fixes DB RPO only) |
| Redis | ≤ 1 s (AOF) for queue payloads; cache loss unlimited-acceptable | ≤ 30 min | `INFERENCE` |
| Elasticsearch | n/a (rebuild) | ≤ 60 min to full reindex | `INFERENCE` |
| Config/secrets | ≤ 7 days (weekly copy) + on-change copy | ≤ 15 min | `INFERENCE` |
| Whole-host disaster (clean host) | **≤ 15 min** | **≤ 60 min** | `VERIFIED` — `AC-DR004-03` |

> Honest caveat: with a single host (`C-22`), RTO ≤ 1 h assumes a **clean replacement host** is available (spare VM or rebuilt instance) and that image pulls, migrations, and restore are executed from the runbook without redesign. Host procurement time is outside our control and is tracked as residual risk (`DOC-NFD-004` §3).

## 3. Encryption & Access (`SEC-REQ-006`, `SEC-REQ-007`)

| Control | Design |
|---|---|
| Encryption at rest | Every backup artifact is encrypted **before** it leaves the host (AES-256 via `age`/`gpg`, key = `BACKUP_ENCRYPTION_PASSPHRASE`, itself stored in the host env file mode `0600` and in the CI/ops secrets store) |
| Transport | Off-host copy uses TLS-only endpoints; no plaintext S3/SSH channel |
| Access | Off-host bucket/container restricted to the **ops role only**; no application role can read backups; unauthenticated restore attempts must fail (`AC-DR004-04`) |
| Key separation | Backup passphrase ≠ database credentials ≠ `DATA_ENCRYPTION_KEY` (field encryption) — compromise of one does not expose the others |
| Never in git | Backup keys, dumps, and env archives are blocked by `.gitignore` + secret scan (`SEC-REQ-007`) |
| Non-prod | A restored backup is **masked** before use in dev/staging (`DATA-REQ-002`, `DOC-OPS-002` PAR-5) |

## 4. Off-Host Storage Location

| Item | Location | Notes |
|---|---|---|
| Primary off-host target | Object storage bucket `s3://yumn-backups/<env>/` via an S3-compatible provider (`BACKUP_OFFHOST_TARGET`) | Region outside the primary host's region/provider where practical (`INFERENCE`) |
| Secondary copy | Weekly full set copied to a second location (different provider or physical media held by the ops owner) | 3-2-1 rule under `NFR-016` portability — no cloud lock-in |
| Layout | `<env>/postgres/<date>/<file>.dump`, `<env>/postgres/wal/<segment>`, `<env>/minio/<date>.tar.zst`, `<env>/config/<date>.enc` | Manifest file with checksums per artifact |
| Secrets directory | Encrypted config archive only; **plaintext env files are never uploaded** | `SEC-REQ-007` |
| Retention | See §7 — governed by `RC-09` | Aging out only; **no selective backup editing** (`DOC-DTA-005` §5.7) |

## 5. Scheduling & Alerting

| Job | Schedule (UTC) | Owner | On failure |
|---|---|---|---|
| WAL archiving | continuous | postgres container | segment age alert at **15 min** → P1 page (`AC-NFR-006-02`) |
| `pg_dump` snapshot | daily 02:00 | `backup` helper container | job failure → alert within the alerting window → P1 `backup_failed` |
| MinIO object copy | daily 03:00 | `backup` helper | failure → P1 `backup_failed` |
| Config/secrets archive | on change + Sunday 04:00 | ops owner (script) | failure → P1 |
| Off-host copy verification | daily 04:30 (checksum re-download of a random artifact) | `backup` helper | failure → P1 |
| Freshness monitor | every 15 min (`backup-check.yml` + Prometheus rule) | CI/Alertmanager | WAL age > 15 min or snapshot age > 24 h → **page** |
| Weekly restore **spot check** | Monday (restore one table into an isolated container, assert row counts) | ops owner | failure → P1 + treat as potential data-loss incident |
| Quarterly full drill | calendar (Jan/Apr/Jul/Oct), see §8 | ops owner + QA witness | drill failure blocks the next release (`AC-S-17`) |

## 6. Restore Procedure (step-by-step)

Preconditions: disaster declared, clean Docker host ready, images and env files available from an encrypted source, off-host credentials held by the ops role.

1. **Provision & prepare** — build the host per `infra/host/`, install Docker, clone the repo, place `.env.production` (from the encrypted config archive), pull the release image tags being restored.
2. **Fetch & decrypt** — download the newest full snapshot + all WAL segments after it; verify manifest checksums; decrypt with `BACKUP_ENCRYPTION_PASSPHRASE`.
3. **Start data tier only** — `docker compose up -d postgres redis minio elasticsearch`; wait for healthchecks green.
4. **Restore PostgreSQL** — stop the DB, restore the snapshot into the empty `pgdata` volume (`pg_restore --clean --if-exists`), start DB, apply WAL replay to the **target point in time** (now minus acceptable RPO, or the last known-good timestamp).
5. **Verify DB integrity (hard gates)** — see §6.1; any failure ⇒ stop and re-evaluate the restore point.
6. **Restore MinIO** — extract the object archive into `miniodata`; verify object count and a checksum sample against DB rows referencing them.
7. **Reindex search** — start Elasticsearch, run the full reindex job from PostgreSQL; do **not** restore any ES snapshot.
8. **Restore config** — decrypt env/config archive into place; confirm boot validation passes (§`DOC-OPS-005` §3).
9. **Start the application** — `migrate deploy` (forward-only, idempotent for already-applied history) → `api` → `worker` → `web` → `edge`.
10. **Verify runtime** — `/healthz` + `/readyz` green, post-deploy smoke suite (`DOC-DPL-003` §5) passes, queue backlog drains, DLQ empty.
11. **Record** — write the drill/incident record: start/end timestamps, elapsed time, restore point, RTO/RPO achieved, checks performed, operator.

### 6.1 Integrity acceptance gates (must all pass)

| # | Check | Pass criterion | Canon |
|---|---|---|---|
| 1 | Ledger zero-imbalance | `SUM(debit) = SUM(credit)` overall **and** per posting; **0** unbalanced rows | `BR-PAY-06`, `AC-S-14`, `AC-DR004-03` |
| 2 | Row counts vs pre-disaster snapshot | counts match or are explainable by the RPO window | `AC-DR004-03` |
| 3 | Order state consistency | no order in an illegal state (`C-09`); every sub-order maps to a master | `C-09`, `C-10` |
| 4 | Wallet/escrow/payable totals | match the last reconciliation report | `BR-ESC-08`, `AC-S-14` |
| 5 | FK integrity | `0` orphan rows | `DATA-REQ-001`, `AC-DR001-01` |
| 6 | Audit chain | hash chain verifies over the restored range | `SEC-REQ-010` |
| 7 | Retention state | no in-window financial row deleted | `AC-DR004-03` |
| 8 | Object/media count | MinIO objects ≥ count of DB references (orphans allowed, missing not) | `DOC-DTA-006` |

## 7. Retention of Backups (governed by `16-data/`)

| Artifact | Retention | Class | Source |
|---|---|---|---|
| WAL segments | **14 days** | `RC-09` | `DOC-DTA-005` §3 |
| Daily PostgreSQL snapshots | **35 days** | `RC-09` | `DOC-DTA-005` §3 |
| MinIO object copies | 35 days daily | `RC-09` (`INFERENCE`) | aligns with snapshot window |
| Config/secrets archives | 90 days (`INFERENCE`) | `RC-02`-class operational | shortest useful window for config rollback |
| Off-host secondary copies | Same windows; aging-out only | `RC-09` | selective deletion forbidden (`DOC-DTA-005` §5.7) |

**Residual window:** purged data may persist in backups until the window rolls over (max **35 days**); every deletion confirmation states this explicitly (`DATA-REQ-003` R5, `DOC-DTA-005` §5.7).

## 8. Quarterly Restore Drill

| Aspect | Definition |
|---|---|
| Cadence | **Quarterly** (`DATA-REQ-004` R4) — Jan / Apr / Jul / Oct, scheduled as a calendar event |
| Owner | Ops owner (execution) · QA engineer (witness + evidence) · Security owner (access checks) |
| Environment | Clean host or isolated throwaway stack — **never** the live environment |
| Scope | Full restore: PostgreSQL + WAL PITR to a chosen point, MinIO, config, reindex, app boot |
| Timing | Wall-clock measured against **RTO ≤ 60 min**; restore point proves **RPO ≤ 15 min** |
| Acceptance | All eight gates in §6.1 pass; elapsed time recorded; evidence pack attached |
| Evidence pack | Timestamps, commands, query outputs for each gate, dashboards screenshot, operator sign-off |
| Failure handling | Failed drill = failed `AC-DR004-03` ⇒ **release gate blocked** (`AC-S-17`); file an incident and fix before the next release |
| Recording | Result recorded against `NFR-006` in `12-non-functional/` and referenced from `15-deployment/production-readiness.md` |

**Mandatory drills:** quarterly full restore (`DATA-REQ-004`) · weekly spot check (§5) · failure-injection on backup job to prove the alert fires (`AC-DR004-02`) · WAL-gap test proving max gap ≤ 15 min (`AC-DR004-01`).

## 9. Verification Summary

| Control check | Method | AC |
|---|---|---|
| WAL gap ≤ 15 min | Monitoring over archived segments | `AC-DR004-01` |
| Backup failure alerts operations | Forced snapshot failure | `AC-DR004-02` |
| Drill within RTO + integrity | Quarterly drill record | `AC-DR004-03` |
| Encrypted + role-restricted storage | Access review + failed unauthenticated restore attempt | `AC-DR004-04` |
| Backup windows match `16-data/` | Config review vs `RC-09` | `DATA-REQ-004` R5 |
| Freshness alerts | Backup-age alert at 15 min (WAL) / 24 h (snapshot) | `AC-NFR-006-02` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
