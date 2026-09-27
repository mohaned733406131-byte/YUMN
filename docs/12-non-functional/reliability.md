---
document_id: DOC-NFD-004
title: Reliability Detail — Availability Math, Degradation Matrix & Integrity Standards
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-005, NFR-006, NFR-007, NFR-008, NFR-020, NFR-019, INT-REQ-001, INT-REQ-003, INT-REQ-006]
related_documents: [DOC-NFD-001, DOC-NFR-005, DOC-NFR-006, DOC-NFR-007, DOC-NFR-008, DOC-AC-001, DOC-OVR-008, DOC-BA-005]
---

# Reliability Detail — Availability Math, Degradation Matrix & Integrity Standards

Elaborates **NFR-005 (uptime), NFR-007 (fault tolerance), NFR-008 (data integrity)** and the operational half of **`C-26`**, with recovery mechanics (`NFR-006`) and supportability hooks (`NFR-020`). Requirement statements stay in `02-requirements/non-functional/`; acceptance is `AC-NFR-005-*`, `AC-NFR-006-*`, `AC-NFR-007-*`, `AC-NFR-008-*`.

## 1. Availability Math

| Window | Budget at 99.99% | Source |
|---|---|---|
| 1 year | **52.56 min** (52 min rounded) | derived from `C-26` |
| Rolling 30 days | **4.32 min** | `C-26`, `AC-NFR-005-01` |
| 1 day | 86.4 ms (practical floor: an outage < probe interval may be invisible) | derived |
| 1 week | 1.008 min | derived |

Accounting rules:

- Availability = `1 − (sum of failed probes / total probes)` on 60-s probes of public critical routes, cross-checked by an **independent external monitor** (monitoring-plane failure must not hide real downtime).
- Planned maintenance counts against the budget unless separately approved and announced in advance (approval recorded in the incident log).
- A **partial degradation is not downtime** if all critical routes still succeed (e.g., ES down with browse fallback per `NFR-007`) — but it must be alerted and logged as a degraded incident.

## 2. Error Budget Policy (burn-rate governance)

| Signal | Threshold | Action |
|---|---|---|
| Budget burn (30-day) | implies > 2× allowed downtime remaining burn-rate | **page on-call** (`AC-NFR-005-01` burn alert armed) |
| Single incident consuming > 50% of monthly budget | after restore | incident review within 48 h; freeze non-critical releases until review |
| Budget exhausted (0 min left) | — | **change freeze**: only reliability fixes ship until window rolls |
| Two consecutive months exhausted | — | escalate to sponsor; scale-out/reliability work takes priority over features (feeds `21-completion/` gates) |
| Healthy (< 50% consumed at month mid) | — | normal change cadence (`DOC-NFD-005` §7) |

Detection/recovery bounds: **MTTD ≤ 1 min** (2 consecutive failed probes → alert ≤ 1 min, `AC-NFR-005-02`); **MTTR tracked against RTO ≤ 1 h** (`NFR-006`); on-call ack ≤ 15 min (`AC-NFR-014-02`).

## 3. Redundancy & Honest Single-Host Caveat (`C-22`)

| Layer | v1 design | Residual risk (flagged) |
|---|---|---|
| API | N stateless replicas behind LB (intra-host) | survives process crash, **not host loss** |
| PostgreSQL 16 (`C-19`) | single primary + continuous WAL archiving + daily snapshots | **host/disk loss = failover to restore** (RTO ≤ 1 h), not hot standby — RPO ≤ 15 min holds (`NFR-006`) |
| Redis (`C-20` backing) | single instance, persistence enabled (AOF/RDB) | queue backlog recovery via BullMQ redelivery + Redis restore; cache loss is harmless (rebuildable) |
| Elasticsearch | single node | degrade to DB browse (`NFR-007`) |
| MinIO / object storage | single instance, versioned | media degrade (§4); uploads blocked gracefully |
| Deployment host | **Docker Compose on one host (`C-22`)** | **residual risk vs `C-26`: no HA failover for the host itself.** 99.99% then depends on host reliability + fast restore. Honest position: process-level failures meet the SLO; host-level failure is mitigated by RTO/RPO, not eliminated. Multi-host HA is a post-v1 decision requiring an ADR and a `C-22` scope amendment |
| DNS/TLS/CDN | `DEP-08` edge in front | edge absorbs static outage; origin outage still counts |

This residual risk is recorded (not hidden) — candidate for `17-risk-management/risk-register.md` if not already covered, and for sponsor discussion at Gate 0.

## 4. Failure Domains & Graceful Degradation Matrix

Expected behavior when each domain fails (design contracts from `NFR-007`, `AC-XCUT-04`):

| Failure | Scope lost | User-visible behavior | Recovery bound | Alert |
|---|---|---|---|---|
| **Elasticsearch down** | search + suggestions | category browse + PDP keep serving from DB/Redis; search box shows friendly fallback | auto-recover ≤ 60 s after ES returns; no restart needed | page if > 5 min |
| **Redis down** | cache, session store | catalog falls back to DB with stricter rate limits; sessions survive on access tokens (≤ 15 min, `C-08`); error rate < 1% during drill | restore ≤ 5 min; hit ratio rebuilds | page immediately |
| **BullMQ workers stopped** | async jobs | jobs persist; resume on restart; **3 retries → DLQ** (`BR-PLT-02`); DLQ depth > 0 → alert ≤ 1 min | backlog drains ≤ 5 min post-recovery | page on DLQ depth |
| **Primary SMS provider blocked/timeout** | SMS channel | automatic failover to WhatsApp within the request window (`BR-NTF-03`, `INT-REQ-003`); combined OTP delivery ≥ 99% | failover immediate; provider switch manual | ticket if failover > 5% of sends |
| **Both SMS + WhatsApp down** | OTP delivery | OTP screen states "check SMS or WhatsApp"; retries with backoff; in-app remains; support can re-trigger manually | escalate to `DEP-06` vendor | **page** (registration blocked) |
| **Payment provider (m-Floos/OneCash) down** | instant top-ups | top-up degrades to **bank transfer + admin verification** (`BR-PAY-04`, `C-05` fallback); wallet payments from existing balance unaffected | provider recovery or manual ops | page if > 15 min (launch-critical path, `DEP-05`) |
| **Lost/duplicated payment callback** | credit accuracy | wallet credits exactly once after reconciliation poll; never on client claim (`BR-PAY-03`) | reconciliation ≤ 15 min cadence (`INFERENCE`) | page on mismatch |
| **MinIO down** | media upload/read | existing images: CDN-cached where possible; new uploads blocked with clear message; orders/wallet unaffected | restore ≤ 30 min | ticket |
| **PostgreSQL primary lost** | all writes | platform read-mostly impossible → fail fast with maintenance page (honest 5xx, no fake success); PITR restore on clean host | **RTO ≤ 1 h / RPO ≤ 15 min** (`NFR-006`) | **page immediately** |
| **API replica killed mid-load** | that replica | LB drains ≤ 30 s; 0 failed sessions | automatic | ticket |
| **Disk 70% / DLQ growth** | capacity | alerts before user impact; no silent drops | operator action ≤ 15 min ack | page/warn by threshold |
| **Clock skew / job storm** | scheduling | BullMQ backoff + rate caps; reconciliation catches drift | self-healing + daily job | ticket |

## 5. Retry & Idempotency Standards

| Rule | Standard | Canon |
|---|---|---|
| Job/webhook retries | 3 attempts, exponential backoff (1×, 4×, 16× base `INFERENCE`), then DLQ; DLQ depth alert ≤ 1 min | `BR-PLT-02`, `INT-REQ-006`, `AC-IR006-03` |
| Idempotency keys | **mandatory** for payment, order creation, stock reservation, coupon application, refund | `BR-PLT-03` |
| Replay semantics | same key → original result, never a duplicate side effect | `AC-NFR-008-02` |
| Client retries | safe only because all retryable writes are idempotent; UI retry buttons map to these | `DOC-UX-005` §4 |
| Money operations | single ACID transaction; multi-step order creation = saga with compensating actions | `BR-PLT-04`, `NFR-008` |
| Provider callbacks | signature-verified, idempotent handlers, at-least-once delivery tolerated | `INT-REQ-006` |
| Never-retry list | non-idempotent admin actions (KYC decision, role change) require explicit user confirmation, not auto-retry | `INFERENCE` |

## 6. Data Durability & Integrity Controls

| Control | Mechanism | Verification |
|---|---|---|
| WAL shipping | continuous, segment shipped **≤ 5 min** (so RPO ≤ 15 min holds with margin) | backup-age alert at 15 min (`AC-NFR-006-02`) |
| Snapshots | daily DB + MinIO; retention 30 d WAL / 35 daily / 12 monthly | freshness alert at 24 h |
| Restore drills | **quarterly**, timed end-to-end on a clean host, followed by reconciliation proving completeness | `AC-NFR-006-01`, `AC-DR004-03` |
| Ledger immutability | append-only postings; corrections via compensating entries only; CI rule blocks UPDATE/DELETE on ledger tables | `DATA-REQ-007`, `AC-DR007-01/02` |
| Double-entry | every balance change = balanced debit+credit in one ACID txn | `BR-PAY-06`, `AC-S-14` |
| Daily reconciliation | Σ ledger = 0; wallet+escrow+payable = provider statements; mismatch alerts finance ≤ 15 min | `BR-ESC-08`, `BR-FIN-03`, `AC-S-14` |
| Invariants under concurrency | balance never negative (`BR-PAY-05`); stock never negative (`BR-CAT-07`); 0 orphan rows (FKs in DB) | `AC-NFR-008-02`, `AC-DR001-01/04` |
| Financial retention | ≥ 5 years, audit chain tamper-evident | `NFR-019`, `SEC-REQ-010` |

## 7. SLI / SLO Definitions

| SLI | Definition | SLO (window) |
|---|---|---|
| Availability SLI | successful probes / total probes on critical routes | ≥ 99.99% (rolling 30 d) |
| Latency SLI | fraction of API requests within class budget (§`DOC-NFD-002` §1) | ≥ 99% of reads < 200 ms; ≥ 99% of writes < 500 ms (30 d) |
| Correctness SLI | reconciliation mismatches per day | **0** (30 d) — `AC-S-14` |
| OTP delivery SLI | delivered OTPs / requested (SMS+WhatsApp combined) | ≥ 99% (7 d) |
| Queue health SLI | jobs completing vs DLQ (excluding injected drills) | DLQ depth 0 at day end |
| Recovery SLO | RTO / RPO on drill | ≤ 1 h / ≤ 15 min (per drill) |

SLO breaches drive the error-budget policy (§2); dashboards and alert wiring are specified in `DOC-NFD-006`.

## 8. Chaos / Game-Day Plan (staging-first, quarterly)

| # | Drill | Injected failure | Pass condition | AC |
|---|---|---|---|---|
| 1 | Search outage | stop ES container | browse + cart + wallet checkout complete, error < 1%, recover ≤ 60 s | `AC-NFR-007-01` |
| 2 | Cache outage | kill Redis | same as above; sessions survive; no 5xx storm | `AC-NFR-007-01` |
| 3 | Queue outage | stop workers, inject 100 jobs | 0 lost/duplicated jobs; DLQ alert ≤ 1 min | `AC-NFR-007-02` |
| 4 | Provider outage | block primary SMS | failover to WhatsApp; combined success ≥ 99% | `AC-IR003-01/04` |
| 5 | Callback chaos | replay + drop payment callbacks | exactly-once credit after reconciliation | `AC-IR001-01/02` |
| 6 | Replica kill | kill API replica under load | LB drain ≤ 30 s, 0 failed sessions | `AC-NFR-018-01` |
| 7 | DR drill | declare disaster, restore on clean host | RTO ≤ 1 h, RPO ≤ 15 min, reconciliation clean | `AC-NFR-006-01` |
| 8 | Deploy/rollback | staging deploy + rollback | 0 failed customer requests; rollback ≤ 15 min | `AC-NFR-020-02` |

Cadence: drills 1–6 monthly (automated where possible), 7 quarterly (`DATA-REQ-004`), 8 every release. Results feed runbooks (`NFR-020`, top-10 incidents) and `13-testing/`.

## 9. Verification Hooks

`AC-NFR-005-01/02` (availability + probe/alert) · `AC-NFR-006-01/02` (RTO/RPO + backup freshness) · `AC-NFR-007-01/02` (degradation drills) · `AC-NFR-008-01/02` (integrity) · `AC-S-06`, `AC-S-14`, `AC-S-15`, `AC-S-17`, `AC-XCUT-04` (failure-mode sweep).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
