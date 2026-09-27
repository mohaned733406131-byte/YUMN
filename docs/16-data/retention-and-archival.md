---
document_id: DOC-DTA-005
title: Retention & Archival Schedule
category: 16-data
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-003, DATA-REQ-004, DATA-REQ-007, NFR-017, NFR-019, SEC-REQ-010, FR-003, FR-020]
related_documents: [DOC-DTA-001, DOC-DTA-002, DOC-DTA-004, DOC-DTA-006, DOC-DR-003, DOC-DR-004, DOC-BA-005]
---

# DOC-DTA-005 — Retention & Archival Schedule

## 1. Purpose & Principles

Authoritative retention schedule for every data class: **how long it is kept, why, where it goes when the operational need ends, and how it is finally removed.** Implements `DATA-REQ-003` (configurable retention, deletion workflow, financial ≥ 5 years) and supplies the backup window required by `DATA-REQ-004` R5.

| # | Principle |
|---|---|
| R1 | Keep only what a documented purpose or legal need requires (`DATA-REQ-002`) — minimization is the default, retention the exception |
| R2 | Periods are **configuration** consumed by a scheduled purge job; changing one is a config change, not a code release (`DATA-REQ-003` R1) |
| R3 | Financial and audit records are exempt from erasure until their floor elapses (`DATA-REQ-003` R3/R4) — never deleted early; a purge attempt on a guarded row **blocks and alerts** (`AC-DR003-03`) |
| R4 | Every purge run writes evidence: actor, scope, row counts, timestamp (`DATA-REQ-003` R5) |
| R5 | Archival is not deletion — archived rows remain readable for reports until class expiry, then purge applies |
| R6 | Where evidence is missing, the period is tagged `INFERENCE` or `INSUFFICIENT EVIDENCE`, never presented as fact (root README §8) |

## 2. Legal Basis & Evidence Status

| Statement | Evidence | Ref |
|---|---|---|
| Financial records and privileged-action audit entries retained **≥ 5 years** | `VERIFIED` — stated requirement | `NFR-019`, `DATA-REQ-003` R3 |
| PDPA-aligned controls (minimization, retention, deletion, user rights) must be implemented | `VERIFIED` — stated requirement; detail of Law No. (11) of 2012 unknown | `NFR-019`, `ASM-13`, `DEP-09` |
| **Exact Yemeni statutory retention periods** (tax, commerce, data protection) beyond the 5-year floor | **`INSUFFICIENT EVIDENCE`** — no legal opinion on file; `DEP-09` not started | — |
| Chosen policy: **10 years** for financial + audit classes | `INFERENCE` — conservative margin above the verified 5-year floor; adjustable by config when `DEP-09` delivers | §4, §5.1 |

> **GAP-STYLE NOTE (open evidence gap):** the precise statutory retention obligations applicable to yumn in Yemen are `INSUFFICIENT EVIDENCE` and must be confirmed through `DEP-09` (legal opinions) / `ASM-13`. This item is to be recorded in `20-validation/missing-information.md` when that register is authored. No new `GAP-NNN` ID is minted here — gap IDs are assigned only in the canonical GAP register (`00-project-overview/project-scope.md` §Open items). All periods below marked `INFERENCE` are provisional until that legal opinion lands; the ≥5-year financial/audit floor is `VERIFIED` and never lowered.

## 3. Retention Classes (canonical definitions)

| ID | Class | Period | Applies to |
|---|---|---|---|
| **RC-01** | Ephemeral | ≤ 24 hours (most: minutes) | OTP codes (5 min), rate-limit counters, cart stock reservations (15 min, `C-13`), delivery code attempts |
| **RC-02** | Short operational | 90 days | Login/IP metadata, notification delivery status, delivery attempt history, non-security app logs |
| **RC-03** | Operational | 12 months (metrics series: 13 months for year-over-year comparison) | Support tickets, moderation records, metrics series, hot audit partition, exports |
| **RC-04** | Account lifecycle | Account lifetime + 24 months inactivity trigger, then anonymize | Profile, addresses, device tokens, sessions, email |
| **RC-05** | Financial | **10 years** (`INFERENCE`; floor ≥ 5 y `VERIFIED`) | Ledger, wallet transactions, escrow/payouts, orders, VAT/invoices, commissions, refunds, bank-transfer references |
| **RC-06** | Audit | **10 years** (`INFERENCE`; floor ≥ 5 y `VERIFIED`), immutable until purge | Privileged/money audit entries, KYC decisions audit |
| **RC-07** | KYC | 5 years after account closure (`INFERENCE`) | KYC document files + metadata |
| **RC-08** | Derived/volatile | Until invalidated / 30 days max | ES index docs, Redis cache, BullMQ payloads, search synonyms |
| **RC-09** | Backup | WAL 14 days; daily snapshots 35 days (`INFERENCE`) | Recovery copies (Postgres + object manifest) |

## 4. Retention Schedule

| Data class | RC | Retention period | Rationale | Archival location (after hot life) | Deletion method |
|---|---|---|---|---|---|
| OTP codes / step-up secrets | RC-01 | 5 minutes (+ 10-min resend window) | Verification only; long life = takeover risk (`BR-AUTH-03`) | None (never archived) | TTL auto-expiry |
| Stock reservations | RC-01 | 15 minutes | Anti-oversell window (`C-13`) | None | TTL auto-release |
| Delivery code attempts | RC-01→02 | Code valid while OUT_FOR_DELIVERY; attempts log 90 days | Abuse evidence (`BR-SHP-03`) | Cold row update | Purge job |
| Rate-limit counters | RC-01 | ≤ 1 hour rolling | Abuse control only (`SEC-REQ-009`) | None | TTL expiry |
| Application logs (no PII by rule) | RC-02 | 90 days | Debugging/ops need only (`NFR-014`) | Log store rotation | Log rotation deletes |
| Login/IP session metadata | RC-02 | 90 days | Security forensics vs minimization balance | Partition archive | Purge job (anonymize user link first) |
| Notification status + provider receipts | RC-02 | 90 days | Delivery disputes; body content not needed | Partition archive | Purge job |
| Push device tokens | RC-04 | Until account deletion or inactivity purge | Delivery purpose ends with account | None | Cascade delete |
| Profile PII (name, phone, email) | RC-04 | Active + 24 months inactive → **anonymize** (`INFERENCE`) | Minimization (`DATA-REQ-002`); dormant accounts hold no live purpose | Row remains, PII columns overwritten | Irreversible anonymization (see `DOC-DTA-006` §4) |
| Address book | RC-04 | With profile; order copies persist under RC-05 | Checkout convenience | Row archive | Delete rows; disidentify order copies |
| Cart contents (server-side) | RC-01→04 | 30 days after last activity | Abandoned-cart insight; low value | None | Purge job |
| Support tickets | RC-03 | 12 months after closure | Resolution quality/QA; contains PII | Cold partition | Purge job (anonymize requester link) |
| Product catalog & images | RC-05 | Life of product + 10 years if referenced by an order | Commercial/tax evidence of what was sold | Cold partition; objects in MinIO | Soft-delete now; hard purge only when no order reference |
| Reviews & review images | RC-05 | 10 years (`INFERENCE`) | Consumer-protection evidence; store rating history | Cold partition | Purge job at class expiry |
| Return evidence images | RC-05 | 10 years (`INFERENCE`) | Dispute evidence (`FR-016`, `BR-RET-06`) | MinIO lifecycle rule | Object lifecycle delete |
| Orders (master/sub, status history) | RC-05 | 10 years (`INFERENCE`; ≥ 5 y `VERIFIED`) | Tax, disputes, statistics (`NFR-017`, `NFR-019`) | Cold partition by month/year | Scheduled purge at expiry; identity already disidentified if account deleted |
| Ledger postings, wallet transactions | RC-05 | 10 years (`INFERENCE`; ≥ 5 y `VERIFIED`) | `DATA-REQ-007` immutability + `NFR-019` floor | Cold partition, append-only | Purge only via privileged maintenance role at expiry |
| Escrow / payable / payout / commission | RC-05 | 10 years (`INFERENCE`) | Settlement audits (`BR-ESC-08`) | Cold partition | As above |
| VAT / invoice records | RC-05 | 10 years (`INFERENCE`) | Statutory tax evidence (`BR-FIN-01`, `NFR-019`) | Cold partition | As above |
| Bank-transfer references & provider refs | RC-05 | 10 years (`INFERENCE`) | Reconciliation with providers (`INT-REQ-001/002`) | Cold partition | Purge at expiry |
| Coupon usage records | RC-05 | 10 years (`INFERENCE`) — tied to order financials they discount | Financial linkage | Cold partition | Purge with order class |
| KYC documents + metadata | RC-07 | 5 years after account closure (`INFERENCE`); rejected/superseded sets deleted at resubmission acceptance | Fraud investigations vs minimization | MinIO cold bucket | Object lifecycle delete + metadata purge |
| Audit entries (privileged/money) | RC-06 | 10 years (`INFERENCE`; ≥ 5 y `VERIFIED`), **immutable while retained** | `SEC-REQ-010`, `BR-PLT-06`, `NFR-019` | Hot 12 months → archived partition | Sealed purge after expiry (§5.4) |
| Search index documents | RC-08 | While source row alive; ≤ 5 min after source deletion | Derived, rebuildable (`FR-009`) | None | Index delete + periodic full rebuild |
| Redis cache / queue payloads | RC-08 | Seconds–hours TTL; queues drained before purge runs | Volatile by design | None | TTL / explicit key purge |
| Backups (WAL + snapshots) | RC-09 | WAL 14 days; snapshots 35 days (`INFERENCE`) | RPO ≤ 15 min support (`DATA-REQ-004`, `NFR-006`) + bounded residual | Backup storage | Window aging-out only — no selective backup edit |
| Metrics series | RC-03 | 13 months | Trend comparison year-over-year (`INT-REQ-007`) | Prometheus retention | TSDB retention policy |

## 5. Specific Resolutions

### 5.1 Financial & audit horizon — why 10 years (`INFERENCE`)
`NFR-019` and `DATA-REQ-003` fix a **minimum of 5 years** (`VERIFIED`). This document sets **10 years** as the configured period: a margin above the floor that absorbs a stricter future legal opinion (`DEP-09`) without re-migrating cold partitions. Changing the period is a configuration edit (`DATA-REQ-003` R1); lowering it below 5 years is forbidden and blocked by the guard test (`AC-DR003-03`).

### 5.2 KYC documents after account closure
Clock starts at **closure**, not submission: 5 years retention (`RC-07`) for fraud/dispute exposure covering the transactions the vendor settled; then both object bytes and metadata are purged (no tombstone needed — workflow history is in the audit trail, `RC-06`). Superseded submissions from rejected cycles are deleted when the replacement is accepted, keeping exactly one active set.

### 5.3 Inactive-account policy (`INFERENCE`)
No login or user-initiated action for **24 consecutive months** ⇒ account marked `DORMANT` (30-day notice attempted via SMS/WhatsApp, `BR-NTF-01`), then profile PII is **anonymized** — not hard-deleted — so financial records (`RC-05`) keep their referent (see `DOC-DTA-006` §4). Reactivation before anonymization restores the account untouched; after anonymization the identity cannot be restored by design (§6 of `DOC-DTA-006`).

### 5.4 Audit immutability vs retention — resolved
Immutability (`SEC-REQ-010`, `DATA-REQ-007`) governs **content, not eternity**: entries are append-only and hash-chained while retained. Purge after the 10-year expiry runs as a **separate privileged maintenance path** (not the application role): (1) the chain segment being removed is verified intact, (2) a sealing record (segment range, row count, final hash, operator, timestamp) is written to the surviving audit trail, (3) rows are deleted, (4) evidence entry per `DATA-REQ-003` R5. The application role still holds no `UPDATE`/`DELETE` privilege — the purge is a controlled operations procedure, tested in the quarterly drill.

### 5.5 Notification & message content
Message **bodies** are not retained beyond successful delivery; only status/metadata survives 90 days (`RC-02`). Security notifications (OTP, login, password change, lockout) follow the same rule — their audit value lives in the audit trail, not in message text (`BR-NTF-02`).

### 5.6 Elasticsearch TTL
Index documents carry no independent life: deletion cascades within the 5-minute index-lag SLO (`DOC-DTA-006` §5), and a full nightly rebuild guarantees no orphan content survives bulk purges (`RC-08`).

### 5.7 Backups & the residual window
Purged data can persist in backups until the backup window rolls over (max **35 days**, `RC-09`). Every deletion confirmation and purge evidence entry states this residual window explicitly (`DATA-REQ-003` R5, `DATA-REQ-004` R5). Selective backup rewriting is forbidden (breaks restorability); restore drills must confirm ledger integrity (`AC-DR004-03`).

## 6. Purge & Archive Mechanics

| Step | Detail | Ref |
|---|---|---|
| 1. Config load | Retention periods read from configuration (env/config store), validated at startup | `DATA-REQ-003` R1 |
| 2. Schedule | Daily job `system.retention.purge` in BullMQ naming scheme `{block}.{entity}.{action}`; 3× backoff then DLQ, DLQ depth alerts | `BR-PLT-01`, `BR-PLT-02` |
| 3. Guard check | Classes RC-05/RC-06/RC-07 below their floor → skip + alert, never delete | `AC-DR003-03` |
| 4. Archive first | Rows leaving hot storage are copied to cold partition/schema before purge eligibility | `NFR-017` |
| 5. Delete | Class-specific method (§4): TTL, anonymize, hard delete, object lifecycle | `DOC-DTA-006` |
| 6. Cascade | ES, Redis keys, MinIO orphans updated in the same run | `DOC-DTA-002` §4 |
| 7. Evidence | Audit entry: actor (`System`), class, scope, row/object counts, duration, timestamp; emitted as metric for Grafana | `DATA-REQ-003` R5, `NFR-014` |
| 8. Report | Weekly retention report: rows per class purged, skipped-by-guard, backlog age | `14-devops-infrastructure/`, `12-non-functional/observability.md` |

**Archive mechanics:** monthly-range partitions on order/ledger/audit tables sized for 10-year storage (`NFR-017` forecasts 100M order-line records, 5-year horizon — partition plan accommodates 10); MinIO object lifecycle rules for images/KYC; Prometheus TSDB retention 13 months. Schema-evolution constraint: cold partitions must stay readable across expand–contract migrations (`DATA-REQ-005`, `DOC-DTA-002` §5).

## 7. Verification

- Purge test on seeded expired rows per class (`AC-DR003-01`); guard test for below-floor attempts (`AC-DR003-03`).
- Evidence test: each run produces the full evidence entry (`AC-DR003-04`).
- Backup-window review: documented residual ≤ 35 days (`DATA-REQ-004` R5).
- Quarterly restore drill includes retention-state inspection: no in-window financial row deleted (`AC-DR004-03`).
- Config review: all periods in this schedule present in the deployment configuration with matching values.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
