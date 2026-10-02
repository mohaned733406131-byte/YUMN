---
document_id: DOC-DPL-006
title: Production Readiness — Go-Live Checklist & Sign-Off
category: 15-deployment
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-005, NFR-006, NFR-014, NFR-016, NFR-019, NFR-020, SEC-REQ-012, DATA-REQ-004, INT-REQ-007, INT-REQ-001, INT-REQ-003]
related_documents: [DOC-DPL-001, DOC-DPL-003, DOC-DPL-004, DOC-OPS-001, DOC-OPS-007, DOC-OPS-008, DOC-OVR-010, DOC-SEC-005]
---

# Production Readiness — Go-Live Checklist & Sign-Off

The single checklist that must be complete before yumn accepts its first real customer, and before any subsequent launch milestone. **No row is implemented yet** — the project is pre-implementation (`docs/README.md` §6), so every status is `NOT DONE`.

**How to use:** each row is verified by a named method with a concrete evidence artifact. A row moves to `DONE` only when the evidence exists and is linked. Any `NOT DONE` row blocks launch; the sign-off section below is signed only when every row reads `DONE`.

Status vocabulary: `NOT DONE` · `DONE` · `WAIVED` (waiver requires sponsor + security sign-off and a recorded risk entry in `17-risk-management/core/risk-register.md`).

## 1. Infrastructure

| # | Item | Owner role | Verification method | Status | Evidence pointer |
|---|---|---|---|---|---|
| I-1 | Domains, TLS and CDN live in production (`DEP-08`) | DevOps | DNS resolves, valid cert, CDN proxying origin; expiry alert armed | NOT DONE | `00-project-overview/dependencies.md` DEP-08; `../../14-devops-infrastructure/core/host-hardening.md` §5 |
| I-2 | Production host provisioned from repo bootstrap, CIS baseline applied | DevOps | CIS scan report; `infra/host/` matches running host | NOT DONE | `../../14-devops-infrastructure/core/host-hardening.md` §7 |
| I-3 | Firewall: only 80/443 internet-facing; data tier unpublished | DevOps | External port scan + rendered-compose assertion | NOT DONE | `../../14-devops-infrastructure/core/docker-compose.md` §7 |
| I-4 | Compose overlay parity proven (service set + image digests staging = prod) | DevOps | `docker compose config` diff + digest record | NOT DONE | `../../14-devops-infrastructure/core/environments.md` §2 (PAR-1/2), `AC-NFR-016-01` |
| I-5 | Backups configured **and restored at least once** end-to-end | DevOps | Completed restore drill record within RTO/RPO | NOT DONE | `../../14-devops-infrastructure/core/backup-recovery.md` §6, `AC-DR004-03` |
| I-6 | Off-host encrypted backup copy verified (checksum re-download) | DevOps | Daily verification job green for 7 consecutive days | NOT DONE | `../../14-devops-infrastructure/core/backup-recovery.md` §4 |
| I-7 | SSH/remote access policy enforced (key-only, no root, bastion/IP allowlist) | DevOps | `sshd -T` audit + firewall review | NOT DONE | `../../14-devops-infrastructure/core/host-hardening.md` §2 |

## 2. Data

| # | Item | Owner role | Verification method | Status | Evidence pointer |
|---|---|---|---|---|---|
| D-1 | All migrations applied forward via `prisma migrate deploy`; zero failed rows | Backend lead | `_prisma_migrations` query + deploy log | NOT DONE | `../../08-database/core/migrations-and-evolution.md` §2 |
| D-2 | Category tree seeded (5 levels) and reference data loaded | Backend lead | Seed script report; row counts vs expected | NOT DONE | `../../14-devops-infrastructure/core/environments.md` §1 (reference data only) |
| D-3 | Commission tiers configured (5–20%, default 10%) in platform settings | Admin / business owner | Admin console `GET /admin/settings` inspection | NOT DONE | `FR-019`, `FR-020`, `BR-ESC-03` |
| D-4 | VAT settings configured and validated against order totals | Finance owner | VAT boundary tests green on production config | NOT DONE | `NFR-019`, `BR-FIN-01`, `AC-NFR-019-01` |
| D-5 | Retention periods configured per schedule; purge job scheduled | Backend lead | Config review vs `16-data/` schedule | NOT DONE | `../../16-data/core/retention-and-archival.md` §4, `DATA-REQ-003` R1 |
| D-6 | Search index built from PostgreSQL; Arabic analyzer active | Backend lead | Full reindex completes; sample Arabic queries return results | NOT DONE | `FR-009`, `10-integrations/` |
| D-7 | Append-only privileges applied to ledger/audit tables (`REVOKE UPDATE, DELETE`) | Backend lead | Privilege audit query | NOT DONE | `DATA-REQ-007`, `AC-DR007-01` |

## 3. Reliability

| # | Item | Owner role | Verification method | Status | Evidence pointer |
|---|---|---|---|---|---|
| R-1 | Load test passed at **10,000 concurrent users** (`C-25`), p95 read < 200 ms / write < 500 ms, error < 0.1% | QA engineer | k6 30-min steady-state report | NOT DONE | `AC-S-05`, `AC-NFR-001-*`, `AC-NFR-003-*` |
| R-2 | Backup restore drill passed within RTO ≤ 1 h / RPO ≤ 15 min | Ops owner | Dated drill record with integrity gates | NOT DONE | `AC-S-17`, `AC-DR004-03` |
| R-3 | Rollback rehearsed ≤ 15 min on staging | Ops owner | Timed rehearsal evidence | NOT DONE | `AC-S-20`, `rollback.md` §5 |
| R-4 | Degradation drills passed (ES down, Redis down, queue stopped, replica kill) | QA engineer | Game-day records | NOT DONE | `../../12-non-functional/core/reliability.md` §8, `AC-NFR-007-*` |
| R-5 | Availability probes live internally + externally; error-budget alert armed | DevOps | Probe dashboard + alert drill | NOT DONE | `AC-NFR-005-02`, `../../14-devops-infrastructure/core/monitoring-stack.md` §5 |
| R-6 | Health endpoints meet timing (< 1 s) and rotation ≤ 30 s | Backend lead | Timed measurement | NOT DONE | `AC-NFR-020-01`, `BR-PLT-07` |
| R-7 | Honest residual risk accepted: single host, no host-level HA (`C-22`) | Sponsor | Written acceptance at Gate 0 | NOT DONE | `../../12-non-functional/core/reliability.md` §3 |

## 4. Security

| # | Item | Owner role | Verification method | Status | Evidence pointer |
|---|---|---|---|---|---|
| S-1 | All secrets rotated from dev values; environments disjoint | Ops owner | Config review of `.env.production` set | NOT DONE | `../../09-security/core/secrets-management.md` §3 |
| S-2 | ZAP-style DAST baseline clean against staging | Security owner | Scan report with 0 open critical | NOT DONE | `SEC-C-23`, `AC-SR012-02` |
| S-3 | `SEC-REQ-012` scan suite clean (SAST, dependency, image, secret) | Security owner | Pipeline reports + monthly severity report | NOT DONE | `../../14-devops-infrastructure/core/host-hardening.md` §8 |
| S-4 | Secret scan clean on repo and images | Security owner | `AC-SR007-01/03` results | NOT DONE | `AC-SR-16` |
| S-5 | Admin accounts: **no MFA in v1** — decision recorded: strong password (bcrypt cost 12) + admin console restricted by IP allowlist + RBAC + full audit | Security owner | Documented decision + IP allowlist configured + audit entries verified | NOT DONE | `SEC-REQ-002/004/010`; MFA exclusion recorded here as the v1 decision |
| S-6 | First admin accounts created interactively (no seeded credentials) and reviewed | Ops owner | Account inventory; no default passwords | NOT DONE | `../../14-devops-infrastructure/core/environments.md` §1 |
| S-7 | TLS 1.3 enforced; HSTS set; no weak ciphers | DevOps | SSL Labs-style scan | NOT DONE | `SEC-REQ-006` |
| S-8 | Log/trace scrub test clean (no secrets/PII in logs) | Backend lead | `AC-SR007-04` automated run | NOT DONE | `../../09-security/core/secrets-management.md` §4 |

## 5. Integrations

| # | Item | Owner role | Verification method | Status | Evidence pointer |
|---|---|---|---|---|---|
| G-1 | `DEP-05` m-Floos + OneCash **production** credentials obtained | Business development | Provider contract + live key in vault | NOT DONE | `DEP-05` (status: NOT STARTED) |
| G-2 | `DEP-06` SMS provider contract + WhatsApp Business approval (`Phase 0` gate) | Business development | Live keys; templates approved | NOT DONE | `DEP-06` (status: NOT STARTED) |
| G-3 | Provider sandboxes passed (contract tests + chaos drills) | QA engineer | Sandbox test report | NOT DONE | `../../10-integrations/core/testing-and-sandboxes.md` |
| G-4 | Webhook signatures verified end-to-end (HMAC, replay window, idempotency) | Backend lead | Signed-callback integration tests | NOT DONE | `INT-REQ-006`, `AC-IR006-01/02` |
| G-5 | SMS failover verified (primary → secondary → WhatsApp fallback) | QA engineer | Failover drill ≥ 99% combined delivery | NOT DONE | `INT-REQ-003`, `BR-NTF-03` |
| G-6 | Push credentials (FCM/APNs) issued for both apps | Mobile lead | Sandbox push received on lab devices | NOT DONE | `DEP-12`, `../../10-integrations/core/push-notifications.md` |
| G-7 | Reconciliation job running against provider statements | Finance owner | Daily reconciliation report, 0 mismatches | NOT DONE | `BR-ESC-08`, `AC-S-14` |

## 6. Operations

| # | Item | Owner role | Verification method | Status | Evidence pointer |
|---|---|---|---|---|---|
| O-1 | All 12 Grafana dashboards live and populated | DevOps | Dashboard inventory screenshot | NOT DONE | `../../12-non-functional/core/observability.md` §5, `AC-S-18` |
| O-2 | Alert routes live: P1 pages on-call, P2/P3 route correctly | DevOps | Staged alert drill: page ≤ 1 min, ack ≤ 15 min | NOT DONE | `AC-NFR-014-02`, `../../14-devops-infrastructure/core/monitoring-stack.md` §4 |
| O-3 | Top-10 runbooks written **and rehearsed** | Ops owner | Rehearsal log with dates | NOT DONE | `AC-S-19`, `../../12-non-functional/core/observability.md` §7 |
| O-4 | On-call rotation published with a working escalation path | Ops owner | Rotation schedule + dead-man's-switch proof | NOT DONE | `AC-NFR-014-02` |
| O-5 | Log pipeline live (30-day queryable, correlation IDs searchable) | DevOps | Loki query by `requestId` returns results | NOT DONE | `NFR-014`, `../../14-devops-infrastructure/core/monitoring-stack.md` §6 |
| O-6 | Backup freshness alerts proven (failure-injection) | Ops owner | Forced failure → alert received | NOT DONE | `AC-DR004-02` |
| O-7 | Deploy + rollback records auditable | Ops owner | Sample deploy record + audit query | NOT DONE | `BR-PLT-06`, `deployment-process.md` §6 |
| O-8 | Support tooling operable by support staff (tickets, disputes, code-lockout escalation) | Support lead | Support walkthrough without engineer assistance | NOT DONE | `AC-S-23`, `FR-020` |

## 7. Business

| # | Item | Owner role | Verification method | Status | Evidence pointer |
|---|---|---|---|---|---|
| B-1 | VAT configuration signed off for live orders | Finance owner | Sample production-like orders correct | NOT DONE | `NFR-019`, `AC-NFR-019-01` |
| B-2 | Commission tiers set and tested (5–20%, default 10%) | Business owner | Payout calculation test | NOT DONE | `BR-ESC-03` |
| B-3 | Return policy content published (merchant defaults + per-store overrides) | Product owner | Content review in admin console + storefront | NOT DONE | `C-11`, `FR-016` |
| B-4 | Support ticket queue **staffed** — human-only support, **no AI chatbot** in v1 | Support lead | Roster + on-shift coverage during launch hours | NOT DONE | `FR-020`, `project-scope.md` OUT OF SCOPE |
| B-5 | Legal documents published (privacy, terms, VAT notice) — `DEP-09` opinions received | Legal / sponsor | Pages live; opinions on file | NOT DONE | `DEP-09`, `NFR-019`, `AC-S-24` |
| B-6 | `DEP-10` Central Bank position on closed-loop wallets resolved | Sponsor / legal | Written position on file | NOT DONE | `DEP-10` (existential for `C-01`) |
| B-7 | Shipping zones, costs and delivery-code flow configured for domestic coverage | Ops owner | End-to-end delivery test with 6-digit code | NOT DONE | `C-16`, `C-17`, `FR-015` |
| B-8 | KYC review capacity meets the ≤ 48 h decision rule at expected volume | Ops owner | Staffing plan + queue metrics baseline | NOT DONE | `BR-VND-03`, `FR-007` |

## 8. Rollup

| Group | Rows | DONE | Blocking |
|---|---|---|---|
| Infrastructure | 7 | 0 | all |
| Data | 7 | 0 | all |
| Reliability | 7 | 0 | all |
| Security | 8 | 0 | all |
| Integrations | 7 | 0 | all |
| Operations | 8 | 0 | all |
| Business | 8 | 0 | all |
| **Total** | **52** | **0** | **52** |

Critical-path blockers (nothing else can proceed): `DEP-06` (registration), `DEP-10` (wallet legitimacy), `DEP-05` (production top-ups), `DEP-09` (legal sign-off), `DEP-08` (public launch) — ordering per `00-project-overview/dependencies.md`.

## 9. Sign-Off

Launch is authorized only when **all 52 rows read `DONE`** (or an explicitly recorded `WAIVED`) and the three signatures below are present.

| Role | Name | Confirms | Signature | Date |
|---|---|---|---|---|
| **Sponsor / project owner** | *(to be assigned)* | Business, legal and risk items (§7, `DEP-09`, `DEP-10`); residual-risk acceptance (R-7) | | |
| **QA lead** | *(to be assigned)* | Verification evidence complete: load (`R-1`), drills (`R-2`–`R-4`), test gates green | | |
| **Security owner** | *(to be assigned)* | Security group (§4) clean; secrets rotated; scan SLAs met; admin-access decision accepted (S-5) | | |
| **Ops owner** (informing) | *(to be assigned)* | Operations group (§6): dashboards, alerts, runbooks, on-call, backups | | |

| Review cadence | Trigger |
|---|---|
| Full re-run | Before every launch milestone (soft launch, public launch, region/zone expansion) |
| Delta review | Before any release that changes infrastructure, integrations, or compliance posture |
| Post-incident re-check | After any P1 with customer impact |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
