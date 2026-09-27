---
document_id: DOC-DTA-007
title: Data Quality Framework
category: 16-data
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [DATA-REQ-001, DATA-REQ-006, DATA-REQ-007, DATA-REQ-008, NFR-008, NFR-014, FR-005, FR-013]
related_documents: [DOC-DTA-001, DOC-DTA-004, DOC-DTA-005, DOC-DR-006, DOC-DR-001, DOC-BA-005]
---

# DOC-DTA-007 — Data Quality Framework

## 1. Purpose

Operationalizes `DATA-REQ-006` (validation at write time + reconciliation jobs) and supplies the rule register behind `DATA-REQ-001`'s constraint list. Two complementary halves:

1. **Prevention** — invalid state is rejected at the point of write (DB constraints + service validation), so bad rows are rare by construction.
2. **Detection** — batch reconciliation and monitors prove cross-entity consistency continuously; mismatches alert, never pass silently (`AC-DR006-02`).

## 2. Quality Dimensions

| Dimension | Definition for yumn | Primary metric | Target |
|---|---|---|---|
| **Completeness** | Required fields present; no missing mandatory values (Arabic product name, owner keys, money columns) | % rows with mandatory fields null (counter-audit) | 0 for `NOT NULL`-guarded fields; ≤ 0.1% for optional fields |
| **Validity** | Values conform to format, range, enum, and type rules (phone regex, YER integers, 17 states, price bounds) | Write-time rejection count / attempted invalid writes | 100% of invalid writes rejected; 0 accepted violations |
| **Consistency** | Agreements that must hold across entities or within a row set (Σ debits = Σ credits, master = Σ sub-orders, FK integrity) | Mismatches per reconciliation run | 0 (any imbalance = CRITICAL) |
| **Timeliness** | Data arrives/updates within its promised window (index lag, reconciliation freshness, outbox age) | Age of freshest dataset / lag percentiles | See SLOs §8 |
| **Uniqueness** | Natural keys are unique platform-wide (phone, SKU per store, coupon code, idempotency key) | Duplicate-at-write attempts blocked | 0 duplicate rows in production |

## 3. Rule Register `DQ-01…DQ-18`

**Enforcement point:** `DB` = PostgreSQL constraint (final arbiter, `DATA-REQ-001`) · `APP` = service-layer validation before commit · `BATCH` = scheduled monitor/detection. **Owner** = role accountable for the rule's correctness. **Response** = what happens on violation.

| ID | Dimension | Rule | Source | Enforce | Owner | Response on violation |
|---|---|---|---|---|---|---|
| DQ-01 | Validity / Uniqueness | Phone matches `^7[0-9]{8}$` and is unique platform-wide | `BR-AUTH-01` | DB (`CHECK` + `UNIQUE`) + APP | Admin | Reject with stable error; duplicate registration blocked |
| DQ-02 | Completeness | Publishable product requires Arabic name, price (YER), category, ≥1 image, stock ≥0, store | `BR-CAT-01` | APP (publish gate) + DB `NOT NULL` on core columns | Vendor (own catalog) | Block publish; draft may save incomplete |
| DQ-03 | Validity | Price > 0; sale price < original price; both integer YER | `BR-CAT-04`, `BR-PAY-10` | DB `CHECK` + APP | Vendor / System | Reject write |
| DQ-04 | Validity | Order total within 500–5,000,000 YER | `C-14` | DB `CHECK` + APP | System (checkout) | Reject order creation |
| DQ-05 | Validity | Stock integer ≥ 0; deduction atomic; oversell prohibited | `BR-CAT-07`, `C-13` | DB `CHECK` + APP (row lock) | Vendor / System | Reject/deduct fails; reservation released on TTL |
| DQ-06 | Validity | Order state ∈ exactly the 17 enumerated states; transitions legal only | `C-09`, `BR-ORD-01` | DB `CHECK` + APP state machine | System | Reject transition; escalate illegal attempt to audit |
| DQ-07 | Consistency | Referential integrity: no orphan child rows; explicit `ON DELETE` per FK | `DATA-REQ-001` R1 | DB FK | Admin (schema) | Insert fails at DB; alert if triggered by migration bug |
| DQ-08 | Consistency | Every transaction posts balanced pairs — Σ debits = Σ credits | `BR-PAY-06`, `NFR-008` | APP (transaction) + BATCH (invariant) | System / Finance (Admin) | Unbalanced write impossible; detected imbalance = CRITICAL page |
| DQ-09 | Validity | All monetary amounts are integer YER (no fractional) | `BR-PAY-10`, `BR-FIN-05` | DB column type / `CHECK` | Finance (Admin) | Reject write |
| DQ-10 | Validity | Rating integer 1–5 | `BR-REV-03` | DB `CHECK` + APP | Customer / Moderator | Reject review submission |
| DQ-11 | Completeness / Validity | Address book ≤ 10 per user; address requires recipient name, phone, governorate, district, street | `FR-003` | APP + DB row count guard | Customer | Reject 11th address; incomplete address rejected |
| DQ-12 | Uniqueness / Validity | Coupon code unique; validity window ≤ 90 days; discount ≤ 90% | `BR-PRM-01` | DB `UNIQUE` + APP | Admin / Vendor (store coupons) | Reject coupon creation or application |
| DQ-13 | Uniqueness | SKU unique within a store | `BR-CAT-02` | DB `UNIQUE` (store_id, sku) | Vendor | Reject product/variant save |
| DQ-14 | Validity / Uniqueness | Category depth ≤ 5 levels; slug unique per level | `BR-CAT-03` | DB `UNIQUE` + APP | Admin | Reject category creation |
| DQ-15 | Completeness | Every tenant-scoped row carries owner key(s) (`user_id`/`store_id`/`courier_id`), `NOT NULL` | `DATA-REQ-008` R1 | DB `NOT NULL` + CI schema audit | Admin (schema) | Insert fails; CI coverage gate fails for missing case |
| DQ-16 | Validity | Cart guards: ≤ 50 products, ≤ 10 units/product, ≤ 5 vendors | `C-15` | APP | System (cart service) | Reject add-to-cart with guard error |
| DQ-17 | Validity | Top-up amount within 1,000–5,000,000 YER | `BR-PAY-02` | APP + DB `CHECK` | System | Reject top-up initiation |
| DQ-18 | Consistency | Master order total = Σ sub-order totals; sub-order total = (items − discount) + VAT + shipping | `BR-ORD-02`, `BR-FIN-02` | APP (transaction) + BATCH (recon J5) | System / Finance (Admin) | Order blocked at creation if mismatch; recon mismatch alerts |

**Layering rule:** every DQ rule with a `DB` enforcement also has an `APP` enforcement for user-friendly errors — but correctness never depends on the app layer alone (`DATA-REQ-001`). `BATCH`-only rules exist only where the condition cannot be expressed as a constraint (cross-row sums, external agreement).

## 4. Write-Time vs Batch Responsibilities

| | Write time | Batch / monitor |
|---|---|---|
| Catches | Single-row and single-transaction violations (DQ-01…DQ-17 core) | Cross-entity drift, external disagreement, job-caused divergence (DQ-08, DQ-18, §5 jobs) |
| Failure mode | Request rejected with stable error code | Alert + report + escalation — data stays in place until resolved (no silent auto-fix of money data) |
| Latency | Immediate | Per §5 schedules |

## 5. Reconciliation Jobs

All jobs run under the BullMQ naming scheme `{block}.{entity}.{action}`, are idempotent, retry 3× with exponential backoff, then dead-letter with depth alerting (`BR-PLT-01`, `BR-PLT-02`), and emit metrics to Prometheus/Grafana (`INT-REQ-007`, `NFR-014`).

| ID | Job | Scope | Schedule | Tolerance | Response on mismatch |
|---|---|---|---|---|---|
| J1 | Wallet balance vs ledger | Per account + global | Nightly 02:00 | **0 YER** | Finance alert + mismatch report; freeze affected payouts until resolved |
| J2 | Global ledger invariant | Σ all postings | Continuous check + nightly | **0 imbalance** | CRITICAL page (`NFR-008`, `AC-DR006-03`) |
| J3 | Escrow holds vs delivered orders | Orders in 7-day hold window | Nightly 02:30 | 0 rows | Alert finance; hold release paused for affected sub-orders (`C-12`) |
| J4 | Vendor payable vs releases/payouts | Per vendor | Nightly 03:00 | 0 YER | Alert finance; payout batch halted (`BR-ESC-05`) |
| J5 | Order totals vs line items + VAT | All orders of the day | Nightly 03:00 | 0 mismatch | Alert; order flagged for review; VAT errors escalated (`BR-FIN-01`, DQ-18) |
| J6 | Provider statement vs top-up ledger | m-Floos / OneCash | Daily after provider pull | 0 YER | Finance alert; top-up reconciliation hold (`INT-REQ-001`, `BR-ESC-08`) |
| J7 | Stock availability vs reservations | All products | Every 5 minutes | Exact match after TTL release | Release expired holds; alert on drift (`C-13`, `AC-DR006-04`) |
| J8 | ES index vs ACTIVE products | Full catalog | Nightly + on-demand | 0 missing/extra docs | Auto-reindex; alert if drift persists > 1 run (`FR-009`) |
| J9 | MinIO objects vs references | Product/review/KYC keys | Weekly | 0 orphans | Orphan report → quarantine then delete after 30 days |
| J10 | Audit hash-chain verification | All audit partitions | Hourly | Chain intact | Alert + freeze privileged writes for investigation (`SEC-REQ-010` R4) |
| J11 | Notification outbox staleness | Pending > 15 minutes | Every 5 minutes | 0 stuck | Retry via provider failover; escalate to DLQ alert (`INT-REQ-003`) |
| J12 | Session/device count vs cap | Per user | Daily | ≤ 5 sessions | Evict oldest (`BR-AUTH-06`); count anomaly alert |

**Timeliness monitors** (feeds dimension metrics): `DQM-01` index lag p95, `DQM-02` reconciliation freshness (hours since last successful run), `DQM-03` queue depth/DLQ depth, `DQM-04` partition/archive job age.

## 6. Quarantine Handling

| Case | Handling |
|---|---|
| Row failing a batch check (e.g. orphan reference, unparseable payload) | Copy to `dq_quarantine` (source table, row key, rule ID, error, first/last seen, attempts); original left untouched until business decides |
| Retry | Exponential backoff 3× then park in DLQ; DLQ depth alerts on-call (`BR-PLT-02`) |
| Aging | Quarantine entries older than 24 h raise a `MEDIUM` alert; older than 72 h escalate to Admin review with daily report |
| Resolution paths | (a) fix source and reprocess, (b) Admin disposition (accept/void) written to audit trail, (c) purge if the record is beyond retention (`DOC-DTA-005`) |
| Money data | Never auto-corrected by jobs — mismatches stay visible until Finance resolves via compensating entries (`DATA-REQ-007`) |
| Reporting | Quarantine depth by rule is a standing Grafana panel (§7) |

## 7. Dashboards & Alerting

- **Grafana — "Data Quality" dashboard** (provisioned with the platform's Grafana via `INT-REQ-007`): reconciliation run status/freshness (J1–J12), mismatch counts by job, quarantine depth by rule, ledger imbalance gauge (target 0), ES index lag, DLQ depth, purge/evidence row counts (`DOC-DTA-005` §6), erasure metrics (`DOC-DTA-006` §6).
- **Alerts** follow `12-non-functional/observability.md` severity definitions: imbalance and chain-break = CRITICAL (page); provider/top-up mismatch = HIGH; quarantine aging and index-lag breaches = MEDIUM; single-run transient failures = LOW (auto-retried).
- Every panel carries its rule/job ID so an alert links straight to this register.

## 8. Data Quality SLOs

| SLO | Target | Window | On breach |
|---|---|---|---|
| Invalid writes accepted | 0 | Continuous | CRITICAL — treated as a defect in constraint coverage (`DATA-REQ-001`) |
| Ledger imbalance occurrences | 0 | Continuous | CRITICAL page (`NFR-008`) |
| Reconciliation freshness (J1–J6) | ≤ 24 h | Rolling | HIGH alert; finance report marked stale |
| Reconciliation completion | Within scheduled window (by 03:30) | Daily | MEDIUM alert |
| Mismatch alert MTTA | ≤ 15 min | Rolling | Ops review |
| Search index lag (DQM-01) | p95 ≤ 5 min | Rolling | MEDIUM; auto-reindex |
| Outbox staleness | 0 items pending > 15 min | Rolling | MEDIUM; failover engaged |
| Quarantine backlog age | ≤ 24 h | Rolling | Admin review (§6) |
| Mandatory-field completeness | 100% (`NOT NULL` fields) | Weekly audit | HIGH — schema/gate defect |
| Cross-tenant leakage | 0 rows across owners | Continuous (test suite) | CRITICAL (`AC-DR008-02`) |

## 9. Data Stewardship (who owns quality per domain)

| Domain | Steward role | Escalation |
|---|---|---|
| Identity & profile data | Admin (support operations) | Super Admin |
| Catalog & media (DQ-02, DQ-03, DQ-13, DQ-14) | Vendor owner of the store | Admin (platform taxonomy) |
| Orders & state machine (DQ-04, DQ-06, DQ-18) | System automation + Admin exception handling | Super Admin |
| Money: ledger, escrow, payouts (DQ-08, DQ-09, DQ-17, J1–J6) | Finance (Admin role) | Super Admin |
| Shipping & stock (DQ-05, J7) | Vendor + System | Admin |
| Reviews & content (DQ-10) | Moderator | Admin |
| Audit trail & chain (J10) | Platform (System writes, Admin verifies) | Super Admin |
| Indexes, caches, queues (J8, J9, J11, DQM-*) | System / operations | Admin |

## 10. Verification

- Negative-write suite: every rule in §3 has a rejection test; no partial rows commit (`AC-DR006-01`).
- Seeded-mismatch test: deliberate wallet/ledger discrepancy detected and alerted within one run (`AC-DR006-02`).
- Clean-data run: zero mismatches inside the scheduled window (`AC-DR006-03`).
- TTL audit: expired reservations released; availability matches reservations exactly (`AC-DR006-04`).
- Dashboard presence: SLOs §8 each have a panel and alert route (`13-testing/` observability tests, `14-devops-infrastructure/` provisioning).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
