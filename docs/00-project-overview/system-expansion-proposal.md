---
document_id: DOC-OVR-012
title: System Expansion Proposal — Session 011 (400+ use cases, portal-partitioned structure)
category: 00-project-overview
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-OVR-001, DOC-OVR-005, DOC-OVR-008, DOC-UC-000, DOC-BA-005, DOC-REQ-001]
---

# System Expansion Proposal (Session 011)

## 1. Directive, standing, and honesty markers

- **Source:** owner directive received 2026-09-30 at the start of session 011
  (`prompt-011.md` §1) — expand boundaries, requirements, rules, constraints, processes and
  the whole analysis; target **"over 400 use cases"**; portal-partition every folder
  `01-…` … `23-templates`. Recorded as an **owner directive**, not as an independently
  verified finding (`GEN-03`, `SPE-03`).
- **Owner-supplied target vs. derived number (published side by side, never blended):**
  - Owner target: **over 400 use cases** — `INSUFFICIENT EVIDENCE` until this session's
    inventory/matrix supports it (session-010 "over 350" precedent).
  - Derived in this proposal: **420 UC files** = 210 existing (`UC-001…210`) + 210 proposed
    (`UC-211…420`), contiguous, registered below **before** minting.
- **Mandated cycle:** this artifact is phase (a) *propose*; §9 is phase (b) *evaluate*
  against the rule system; phase (c) *implement* follows change control (phase 4) and the
  structure migration (phase 5) per `prompt-011.md` §4.
- **Evidence discipline:** every proposed UC row carries a **source document** already in the
  corpus; every proposed requirement/BR delta carries an exact path + line/section. Anything
  unsourced goes to the explicit PENDING list in §9.7 — never to silence (`AUD-04`, `SPE-03`,
  "approval ≠ evidence" — `prompt-next.md` §6).

## 2. Boundary / scope modifications proposed

| # | Modification | From → To (if accepted) | Governing route |
|---|---|---|---|
| S1 | Use-case corpus expanded | 210 → **420** UC files (`UC-211…420`) | Allocation registered in `naming-conventions.md` **before** minting (phase 4) |
| S2 | Requirement registry expanded | 68 → **73** IDs (`SEC-REQ-013…016`, `DATA-REQ-009`) | `02-requirements/requirements-overview.md` + FR/SEC/DATA files (phase 7) |
| S3 | Business-rule registry expanded | 104 → **111** rules (7 new, §5) | `01-business-analysis/business-rules.md` + BR sections (phase 7) |
| S4 | Documentation tree restructured | flat `docs/01…23` → **portal-partitioned** (`root + core/admin/vendor/customer/delivery`) | `naming-conventions.md` folder-path scheme row first (phase 4), then scripted migration (phase 5) |
| S5 | Constraint register `C-01…C-26` | **no change** — none proposed (§7) | Root README §9 only; owner-locked |
| S6 | `senior-rules/YUMN_RULES.md` (94 rules) | **no rule-text change** — path references realigned to the portal split as a factual correction (pin stays 2.2.0; session 005/008 precedent) | Rule text only via `senior-rules/core/00` §0.5 → proposed, **deferred** (§7) |
| S7 | Workflows `WF-001…012`, endpoints (221), TCs (114), ADRs, entities | counts unchanged; **paths** move per §8 placement table | Migration only, no ID changes |
| S8 | What this proposal does **not** claim | No new TCs/ACs (the `AC-UC*` gap remains an open FAIL finding, `CHK-12`/`CHK-13`); no gate moves; Gate 0 stays `FAIL`; nothing becomes `VERIFIED`; sponsor-owned items surfaced, not dispositioned | `DOD-10`, `prompt-011.md` §1 |

## 3. Working interpretation — what "23 folders" means (confirmed here per directive)

1. **"23 folders" = `docs/01-business-analysis` … `docs/23-templates`** (the 23 numbered
   domains). `docs/00-project-overview`, `docs/phases/`, and `docs/sessions/` are
   section-level/overview material and are **not** portal-partitioned.
2. Each of the 23 folders ends with **five portal subfolders** — `core/`, `admin/`,
   `vendor/`, `customer/`, `delivery/` — plus its `README.md` at folder root.
3. **Placement rules:** portal-specific material → its portal folder; shared/platform-wide
   material → `core/`; cross-portal gateways (folder `README.md`, registries, indexes such as
   the UC index `DOC-UC-000`, `business-rules.md`, requirements/ADR/risk/decision registries)
   → **folder root**.
4. **The `01-business-analysis` example is literal:** `use-cases/` (210 files) and
   `workflows/` (13 files) are dissolved and partitioned into the five portal folders; the UC
   index and `business-rules.md` stay at the folder root. Dissolved subfolder index files are
   renamed to `*-index.md` gateway files at folder root so no README collides with the folder
   `README.md`: use-case-index.md, workflow-index.md, functional-index.md,
   non-functional-index.md, security-index.md, data-index.md, integration-index.md,
   endpoints-index.md, entities-index.md, test-cases-index.md (created by the phase-5
   migration).
5. Existing UC→portal assignment (unchanged semantics, now physical): customer `UC-001…014`,
   `UC-041…042`, `UC-141…182`; vendor `UC-015…024`, `UC-183…204`; delivery `UC-025…030`,
   `UC-205…210`; admin `UC-031…038`, `UC-084…140`; core `UC-039…040`, `UC-043…083`.
   Workflows: customer `WF-001/002/003/009/010`, vendor `WF-004/011`, delivery `WF-005`,
   admin `WF-008/012`, core `WF-006/007`. Endpoint registers: `admin.md` → admin,
   `delivery.md` → delivery, `cart.md` → customer, remainder → core.

## 4. Proposed additional use cases — `UC-211…UC-420` (210 rows)

**Allocation (registered in `naming-conventions.md` phase 4 BEFORE any minting):**

| Portal | UC range | New UCs | Resulting portal total (existing + new) | Actor(s) |
|---|---|---:|---:|---|
| `core` (shared / system) | `UC-211…255` | 45 | 88 | System (ACT-07) |
| `admin` | `UC-256…305` | 50 | 115 | Admin / Super Admin / Moderator |
| `customer` | `UC-306…360` | 55 | 113 | Customer |
| `vendor` | `UC-361…395` | 35 | 67 | Vendor |
| `delivery` | `UC-396…420` | 25 | 37 | Delivery Provider |
| **Total** | **`UC-211…420`** | **210** | **420** | — |

Minting target file location: `docs/<domain>/<portal>/UC-nnn.md` per the portal a UC belongs
to (use cases live under `docs/01-business-analysis/<portal>/`), template v1.2 verbatim.

### 4.1 Portal `core` — UC-211…255 (45 UCs)

Actor: System (ACT-07).

| UC ID | Title | Actor | Block | FR/BR refs | Priority | Source document |
|---|---|---|---|---|---|---|
| UC-211 | Enforce OTP and Login Rate-Limit Budgets With 429 and Retry-After | System | B01 | FR-001, BR-AUTH-03, BR-AUTH-04 | P1 | `docs/09-security/core/security-controls.md` |
| UC-212 | Evict the Oldest Device Session on the Sixth Concurrent Login | System | B01 | FR-001, BR-AUTH-06 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-213 | Invalidate Every Session When a Password Reset Succeeds | System | B01 | FR-001, BR-AUTH-07 | P1 | `docs/07-api/core/auth.md` |
| UC-214 | Expire OTP Challenges After Five Minutes and Reset Attempt Counters | System | B01 | FR-001, BR-AUTH-03 | P1 | `docs/06-backend/core/caching.md` |
| UC-215 | Lift the Account Lock Automatically After the 15-Minute Timeout | System | B01 | FR-001, BR-AUTH-04 | P1 | `docs/09-security/core/security-controls.md` |
| UC-216 | Anonymize Profile PII for Accounts Dormant 24 Months After Notice | System | B01 | FR-003 | P2 | `docs/16-data/retention-and-archival.md` |
| UC-217 | Serialize Contended Stock Reservations to Prevent Oversell | System | B02 | FR-005, BR-CAT-07, BR-INV-02 | P0 | `docs/08-database/core/constraints-and-integrity.md` |
| UC-218 | Resolve the Reservation-Expiry Race at Checkout Confirmation | System | B02 | FR-005, BR-INV-01, BR-CRT-02 | P0 | `docs/03-system-analysis/core/failure-modes.md` |
| UC-219 | Purge Orphaned Product Images Only When No Order References Them | System | B02 | FR-004, BR-CAT-06 | P2 | `docs/16-data/data-lifecycle.md` |
| UC-220 | Delete Superseded KYC Document Sets When a Resubmission Is Accepted | System | B03 | FR-007, BR-VND-03 | P2 | `docs/16-data/retention-and-archival.md` |
| UC-221 | Purge KYC Objects and Metadata Five Years After Account Closure | System | B03 | FR-007 | P2 | `docs/16-data/data-lifecycle.md` |
| UC-222 | Rebuild the Search Index From Source After an Outage | System | B04 | FR-009 | P1 | `docs/03-system-analysis/core/failure-modes.md` |
| UC-223 | Serve Category Browse From Cache While Search Is Degraded | System | B04 | FR-009 | P1 | `docs/12-non-functional/core/reliability.md` |
| UC-224 | Alert on Search Indexing Lag Beyond the Five-Minute Delete SLO | System | B04 | FR-009, BR-CAT-06 | P2 | `docs/14-devops-infrastructure/core/monitoring-stack.md` |
| UC-225 | Return the Original Order on Idempotent Checkout Replay | System | B05 | FR-011, BR-ORD-06, BR-PLT-03 | P0 | `docs/06-backend/core/validation.md` |
| UC-226 | Reject Order Totals Outside the 500–5,000,000 YER Bounds | System | B05 | FR-011, BR-CAT-04 | P0 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-227 | Expire Idempotency-Key Records After 24 Hours | System | B05 | FR-011, BR-PLT-03 | P2 | `docs/06-backend/core/caching.md` |
| UC-228 | Auto-Accept PLACED Orders for Stores With Auto-Accept Enabled | System | B06 | FR-012, BR-ORD-01 | P2 | `docs/03-system-analysis/core/state-transitions.md` |
| UC-229 | Roll the Master Order Up to COMPLETED When Every Sub-Order Settles | System | B06 | FR-012, BR-ORD-07 | P1 | `docs/03-system-analysis/core/state-transitions.md` |
| UC-230 | Append the State-History Backstop Row on Every Order Transition | System | B06 | FR-012, BR-ORD-03 | P1 | `docs/08-database/core/constraints-and-integrity.md` |
| UC-231 | Auto-Cancel Top-Ups Left Pending Beyond the Confirmation Window | System | B07 | FR-013, BR-PAY-03 | P1 | `docs/10-integrations/core/wallet-providers.md` |
| UC-232 | Open a Circuit Breaker on a Failing Top-Up Provider and Degrade to Bank Transfer | System | B07 | FR-013, BR-PAY-04 | P1 | `docs/10-integrations/core/wallet-providers.md` |
| UC-233 | Serialize Concurrent Wallet Debits to Keep Balances Non-Negative | System | B07 | FR-013, BR-PAY-05 | P0 | `docs/03-system-analysis/core/failure-modes.md` |
| UC-234 | Credit Refunds Into Frozen Wallets While Debits Stay Blocked | System | B07 | FR-013, BR-PAY-09 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-235 | Drain the Escrow Release Backlog After Scheduler Recovery | System | B07 | FR-014, BR-ESC-01, BR-ESC-02 | P1 | `docs/03-system-analysis/core/failure-modes.md` |
| UC-236 | Post Ledger Corrections as Compensating Entries Only | System | B07 | FR-013, BR-PAY-06 | P1 | `docs/08-database/core/constraints-and-integrity.md` |
| UC-237 | Route VAT Rounding Residuals to the Platform Rounding Account | System | B07 | FR-013, BR-FIN-01, BR-FIN-05 | P2 | `docs/06-backend/core/validation.md` |
| UC-238 | Issue a Fresh 6-Digit Delivery Code at OUT_FOR_DELIVERY | System | B08 | FR-015, BR-SHP-02 | P0 | `docs/06-backend/core/background-processing.md` |
| UC-239 | Award a Delivery Offer to the First Courier Acceptance Only | System | B08 | FR-015, BR-SHP-04 | P0 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-240 | Lift the Delivery-Code Confirmation Lock After 24 Hours | System | B08 | FR-015, BR-SHP-03 | P1 | `docs/03-system-analysis/core/failure-modes.md` |
| UC-241 | Auto-Approve Returns Left Uninspected for 72 Hours | System | B09 | FR-016, BR-RET-05 | P1 | `docs/06-backend/core/background-processing.md` |
| UC-242 | Auto-Escalate Return Decisions Stalled Past 48 Hours | System | B09 | FR-016 | P1 | `docs/06-backend/core/background-processing.md` |
| UC-243 | Advance the Order to COMPLETED After a Rejected Return | System | B09 | FR-016, BR-RET-02 | P1 | `docs/03-system-analysis/core/state-transitions.md` |
| UC-244 | Deduplicate Notification Fan-Out by Event, Recipient, and Channel | System | B10 | FR-017, BR-PLT-03 | P1 | `docs/06-backend/core/background-processing.md` |
| UC-245 | Throttle Per-Channel Notification Sends to Protect Provider Quotas | System | B10 | FR-017 | P1 | `docs/06-backend/core/background-processing.md` |
| UC-246 | Record SMS and WhatsApp Delivery Receipts per Message | System | B10 | FR-017 | P1 | `docs/10-integrations/core/sms-provider.md` |
| UC-247 | Publish the Weekly Retention Purge Report | System | B11 | FR-018 | P2 | `docs/16-data/retention-and-archival.md` |
| UC-248 | Enforce Retention Windows on Metrics, Logs, and Traces | System | B11 | FR-018 | P2 | `docs/14-devops-infrastructure/core/monitoring-stack.md` |
| UC-249 | Purge CDN and ISR Caches When Content Is Published | System | B12 | FR-019 | P1 | `docs/06-backend/core/caching.md` |
| UC-250 | Invalidate the Coupon Validation Cache on Admin Disable | System | B12 | FR-019, BR-PRM-04 | P2 | `docs/06-backend/core/caching.md` |
| UC-251 | Verify the Audit Hash Chain Nightly and Alert on Tamper | System | B13 | FR-020, BR-PLT-06 | P0 | `docs/08-database/core/constraints-and-integrity.md` |
| UC-252 | Page On-Call When Backup Freshness Breaches Its Window | System | B13 | FR-020 | P0 | `docs/14-devops-infrastructure/core/monitoring-stack.md` |
| UC-253 | Run the Daily Retention Purge With Floor Guards and Evidence | System | B13 | FR-020, BR-PLT-01, BR-PLT-02 | P1 | `docs/16-data/retention-and-archival.md` |
| UC-254 | Create Next-Month Table Partitions Ahead of Deployment | System | B13 | FR-020 | P1 | `docs/08-database/core/migrations-and-evolution.md` |
| UC-255 | Cascade Primary-Data Deletion to Search, Cache, Queues, and Objects | System | B13 | FR-020 | P1 | `docs/16-data/data-lifecycle.md` |

> - sources verified: every path was confirmed to exist in `E:\YUMN\docs` (full recursive file listing) and the file was opened and skimmed for the cited behavior before the row was minted. Key sections relied on: `background-processing.md` §1–§5 (30-queue register, fan-out dedup/backpressure, SLA jobs, `b08.shipping.code-issue`), `caching.md` §1/§3/§4 (OTP/idempotency TTLs, invalidation events, stampede/cold-start), `validation.md` §5/§6 (idempotency replay, integer rounding), `error-handling.md` (not rowed, mined for cross-checks), `state-transitions.md` §2/§4 (auto-accept actor, RETURN_REJECTED→COMPLETED by System, master roll-up), `failure-modes.md` (FM-12/13/18, §2.4/§2.5), `edge-cases.md` (EC-08/19/23/31/34), `webhook-reliability.md`, `sms-provider.md` §3 (DLR), `wallet-providers.md` §3/§6/§8, `observability.md`, `reliability.md` §4, `constraints-and-integrity.md` §3/§4/§6/§7, `migrations-and-evolution.md` §5/§8, `monitoring-stack.md` §4.1/§7, `backup-recovery.md` §5, `security-controls.md` §3/SEC-C-12/SEC-C-21, `data-lifecycle.md` §3.5/§3.6/§4, `retention-and-archival.md` §5.2/§5.3/§6, and `../07-api/core/auth.md` (API-ATH-004/010). BR IDs were taken only from the 104-rule registry in `docs/01-business-analysis/business-rules.md`; FR IDs only from FR-001…FR-020 (`02-requirements/requirements-overview.md`); block↔FR mapping follows `../06-backend/core/backend-architecture.md` §3 (B01=FR-001…003 … B13=FR-020).

> - shortfall: none — 45 of 45 rows produced (UC-211…UC-255, contiguous), all source-backed; no scenario or source was fabricated.

> - duplicate-check: every title was diffed against the §2 index of `docs/01-business-analysis/use-case-index.md` (all 210 existing titles, especially the 43 System rows UC-039/040/043–083) and against the §5.1 PENDING list (FX rates, Al-Kuraimi/Jeeb, email login, escrow-maturity vendor note, flags console, departments, invoices, provider registry, wishlist, calendar, search-analytics UI, engagement stats, PWA install, analytics UI, cart abandonment, re-open support ticket, moderator audit-log access, vendor right-of-reply) — none of the 45 rows duplicates, paraphrases, or anticipates a PENDING item. Adjacent-but-distinct pairs were deliberately differentiated: UC-215 (lock expiry) vs UC-044 (lock trigger); UC-240 (24 h lock lift) vs UC-208/UC-065 (lockout UX + auto-ticket); UC-241/UC-242 (system timers) vs UC-195/UC-125 (human decisions); UC-235 (scheduler-recovery backlog) vs UC-039 (7-day release); UC-251 (hash-chain verification) vs UC-083 (retention/redaction); UC-253 (cross-class purge job) vs UC-083; UC-224 (indexing-lag alert) vs UC-067 (incremental index sync); UC-222 (outage rebuild) vs UC-067. Portal rule enforced: Actor = `System` (ACT-07) on all 45 rows — no human-portal UCs. Priority mix: P0 = 9, P1 = 25, P2 = 11; block mix: B01 6, B02 3, B03 2, B04 3, B05 3, B06 3, B07 7, B08 3, B09 3, B10 3, B11 2, B12 2, B13 5.

### 4.2 Portal `admin` — UC-256…305 (50 UCs)

Actor: Admin / Super Admin / Moderator (ACT-04/05/06).

| UC ID | Title | Actor | Block | FR/BR refs | Priority | Source document |
|---|---|---|---|---|---|---|
| UC-256 | Investigate Account-Lockout and OTP-Abuse Signals | Admin | B01 | FR-001, FR-020, BR-AUTH-04 | P1 | `docs/12-non-functional/core/observability.md` |
| UC-257 | Execute the Incident Rotation Runbook for a Leaked Secret | Super Admin | B01 | FR-001, FR-020, BR-AUTH-05, BR-PAY-09 | P0 | `docs/09-security/core/secrets-management.md` |
| UC-258 | Force Session Revalidation After a Signing-Key Rotation | Super Admin | B01 | FR-001, FR-002, BR-AUTH-05, BR-AUTH-06 | P1 | `docs/09-security/core/secrets-management.md` |
| UC-259 | Audit Four-Eyes Compliance on Money Operations | Admin | B01 | FR-002, FR-020, BR-PLT-06 | P1 | `docs/09-security/core/rbac.md` |
| UC-260 | Review a Target's Recent Administrative Actions Before Enforcement | Admin | B01 | FR-002, FR-020, BR-PLT-06 | P2 | `docs/07-api/admin/admin.md` |
| UC-261 | Sample-Verify Completed Data-Deletion Requests | Admin | B01 | FR-003, FR-020 | P1 | `docs/16-data/data-deletion-and-privacy.md` |
| UC-262 | Deactivate a Category Node from the Storefront | Admin | B02 | FR-004 | P2 | `docs/07-api/admin/admin.md` |
| UC-263 | Confirm Rating Recomputation After a Review Is Hidden | Admin | B02 | FR-006, BR-REV-05 | P2 | `docs/07-api/core/catalog.md` |
| UC-264 | Confirm a Hidden Product Is Delisted From Search and Storefront | Admin | B02 | FR-004, FR-019, BR-CAT-06 | P2 | `docs/07-api/admin/admin.md` |
| UC-265 | Prioritize the Overdue KYC Queue Before the 48-Hour SLA | Admin | B03 | FR-007, FR-020, BR-VND-03 | P1 | `docs/07-api/admin/admin.md` |
| UC-266 | Clear a KYC Blocker That Prevents Store Reactivation | Admin | B03 | FR-007, FR-019, BR-VND-01 | P1 | `docs/07-api/admin/admin.md` |
| UC-267 | Verify the Cascade Effects of a Store Suspension | Admin | B03 | FR-007, FR-020, BR-VND-04 | P2 | `docs/07-api/admin/admin.md` |
| UC-268 | Set the Platform Commission Tier Within the 5-20% Bound | Super Admin | B03 | FR-014, FR-019, BR-ESC-03 | P1 | `docs/07-api/admin/admin.md` |
| UC-269 | Cancel an Order as the Platform of Last Resort | Admin | B06 | FR-012, FR-014, BR-ORD-04 | P1 | `docs/07-api/core/orders.md` |
| UC-270 | Force a Sub-Order State Correction Within the 17-State Table | Admin | B06 | FR-012, FR-020, BR-ORD-01, BR-ORD-03, BR-PLT-06 | P0 | `docs/07-api/core/orders.md` |
| UC-271 | Assemble the Order Timeline Evidence Pack for a Dispute | Admin | B06 | FR-012, FR-016, BR-ORD-05, BR-ORD-09 | P1 | `docs/11-ui-ux/core/user-flows.md` |
| UC-272 | Trace a Master Order to Its Sub-Orders During an Investigation | Admin | B06 | FR-012, BR-ORD-02 | P2 | `docs/07-api/core/orders.md` |
| UC-273 | Investigate an Escalated Illegal Order-State Transition | Admin | B06 | FR-012, FR-020, BR-ORD-01, BR-PLT-06 | P1 | `docs/16-data/data-quality.md` |
| UC-274 | Second-Approve a Large Bank-Transfer Top-Up | Super Admin | B07 | FR-013, FR-020, BR-PAY-04 | P1 | `docs/10-integrations/core/bank-transfer-topup.md` |
| UC-275 | Cross-Check Pending Top-Ups Against the Bank Statement | Admin | B07 | FR-013, FR-014, BR-PAY-04 | P1 | `docs/10-integrations/core/bank-transfer-topup.md` |
| UC-276 | Release an Unused Authorization Hold Manually | Admin | B07 | FR-013, BR-PAY-08 | P1 | `docs/07-api/core/wallet.md` |
| UC-277 | Record the Disposition of a Reconciliation Mismatch | Admin | B07 | FR-013, FR-014, BR-ESC-08, BR-FIN-03, BR-PLT-06 | P0 | `docs/07-api/core/analytics.md` |
| UC-278 | Approve the Vendor Payout Batch for Execution | Admin | B07 | FR-014, FR-020, BR-ESC-05, BR-PLT-06 | P0 | `docs/09-security/core/rbac.md` |
| UC-279 | Freeze Payouts and Top-Up Crediting on a Ledger-Integrity Alarm | Admin | B07 | FR-013, FR-014, FR-020, BR-PAY-06, BR-PAY-09 | P0 | `docs/17-risk-management/risk-register.md` |
| UC-280 | Run the Pre-Launch Money-Cycle Audit | Admin | B07 | FR-013, FR-014, BR-FIN-03, BR-PAY-06 | P0 | `docs/17-risk-management/risk-register.md` |
| UC-281 | Reassign a Stalled Delivery Back to the Offer Pool | Admin | B08 | FR-015, BR-SHP-04 | P1 | `docs/07-api/delivery/delivery.md` |
| UC-282 | Pull Delivery Proof for a Dispute Review | Admin | B08 | FR-015, FR-016, BR-SHP-07, BR-ORD-09 | P2 | `docs/07-api/delivery/delivery.md` |
| UC-283 | Arbitrate a Dispute and Choose the Prevailing Party | Admin | B09 | FR-016, FR-020, BR-ORD-05, BR-RET-06, BR-RET-07 | P0 | `docs/07-api/core/returns.md` |
| UC-284 | Attach Platform Evidence to a Dispute Case | Admin | B09 | FR-016, BR-ORD-05 | P1 | `docs/07-api/core/returns.md` |
| UC-285 | Track Open Disputes and Their Frozen Escrow Exposure | Admin | B09 | FR-014, FR-016, BR-ORD-05 | P1 | `docs/07-api/core/returns.md` |
| UC-286 | Verify Refund Credits Within the 3-Business-Day SLA | Admin | B09 | FR-013, FR-016, BR-RET-04, BR-PAY-07 | P1 | `docs/07-api/core/wallet.md` |
| UC-287 | Run the Orders Report | Admin | B11 | FR-018, FR-020 | P2 | `docs/07-api/core/analytics.md` |
| UC-288 | Run the GMV Report | Admin | B11 | FR-018, FR-020 | P2 | `docs/07-api/core/analytics.md` |
| UC-289 | Run the Returns and Refunds Report | Admin | B11 | FR-016, FR-018 | P2 | `docs/07-api/core/analytics.md` |
| UC-290 | Monitor Queue Depths and SLA Breaches as Moderator | Moderator | B11 | FR-018, FR-020, BR-ORD-10 | P2 | `docs/07-api/core/analytics.md` |
| UC-291 | Review a CMS Page's Publish History Before Republishing | Admin | B12 | FR-019, BR-PLT-06 | P2 | `docs/07-api/core/content.md` |
| UC-292 | Disable a Store Coupon for Promotion Abuse | Admin | B12 | FR-019, BR-PRM-03 | P1 | `docs/07-api/core/content.md` |
| UC-293 | Investigate Coupon-Abuse Patterns Across Orders and Refunds | Admin | B12 | FR-011, FR-019, BR-PRM-01, BR-PRM-02, BR-ESC-04 | P2 | `docs/17-risk-management/risk-register.md` |
| UC-294 | Hide Reported Content With a Reason as Moderator | Moderator | B13 | FR-006, FR-019, BR-REV-04 | P1 | `docs/07-api/admin/admin.md` |
| UC-295 | Isolate Auto-Created Delivery-Code Tickets in the Support Queue | Admin | B13 | FR-015, FR-020, BR-SHP-03 | P2 | `docs/07-api/admin/admin.md` |
| UC-296 | Investigate an Audit Hash-Chain Verification Failure | Admin | B13 | FR-020, BR-PLT-06 | P0 | `docs/16-data/data-quality.md` |
| UC-297 | Extract Audit Evidence for a Security Incident | Admin | B13 | FR-020, BR-PLT-06 | P1 | `docs/12-non-functional/core/observability.md` |
| UC-298 | Re-Drive a Failed Job From the Dead-Letter Queue | Admin | B13 | FR-020, BR-PLT-01, BR-PLT-02 | P1 | `docs/10-integrations/core/webhook-reliability.md` |
| UC-299 | Dispose of Aged Data-Quality Quarantine Records | Admin | B13 | FR-020, BR-PLT-06 | P1 | `docs/16-data/data-quality.md` |
| UC-300 | Review the Weekly Retention Purge Report | Admin | B13 | FR-020 | P2 | `docs/16-data/retention-and-archival.md` |
| UC-301 | Investigate a Guard-Blocked Retention Purge Attempt | Admin | B13 | FR-020 | P1 | `docs/16-data/retention-and-archival.md` |
| UC-302 | Resolve a Settings Version Conflict After a Concurrent Edit | Super Admin | B13 | FR-019, FR-020, BR-PLT-06 | P2 | `docs/07-api/admin/admin.md` |
| UC-303 | Track Critical Security Findings Against the 7-Day Remediation SLA | Admin | B13 | FR-020 | P1 | `docs/09-security/core/security-controls.md` |
| UC-304 | Audit the Evidence Entry of a Completed Purge Run | Admin | B13 | FR-020 | P2 | `docs/16-data/retention-and-archival.md` |
| UC-305 | Review the Monthly Security Severity Report | Admin | B13 | FR-020 | P2 | `docs/09-security/core/security-controls.md` |

> - **sources verified:** every row cites one repo-relative path opened and skimmed this session. Primary evidence: `docs/07-api/{admin,orders,returns,wallet,delivery,analytics,content,catalog}.md` (API-ADM-002/005/011/012/013/016/023/024/027/028/039, API-ORD-011/013/014, API-RET-014/016/017, API-WAL-008/014, API-SHP-003/005, API-ANL-006/007/009, API-CNT-007/017); `docs/09-security/{rbac,secrets-management,security-controls}.md` (four-eyes `ORG-01`/L205, incident rotation runbook §7, SEC-C-24 + monthly severity report); `docs/10-integrations/{bank-transfer-topup,webhook-reliability}.md` (two-person control, statement cross-check S-10, admin-only DLQ re-drive); `docs/16-data/{data-quality,retention-and-archival,data-deletion-and-privacy}.md` (DQ-06, J10, quarantine §6 Admin disposition, weekly purge report + guard-blocked purge, monthly sampling QA); `docs/12-non-functional/core/observability.md` (dashboard #11, runbook #10); `docs/17-risk-management/risk-register.md` (RISK-001 mitigation + contingency, RISK-013 contingency); `docs/11-ui-ux/core/user-flows.md` (FL-07 evidence panels); `docs/02-requirements/requirements-overview.md` (FR-001…FR-020 only); `docs/01-business-analysis/business-rules.md` (104 BR IDs, all cited IDs confirmed present with the stated meaning).

> - **actor note:** on-call / security-owner duties in `observability.md` and `security-controls.md` are mapped to Admin (ACT-04); key/secrets authority and the commission-tier write are mapped to Super Admin (ACT-05) per `stores.md` L53 (`SUPER_ADMIN` changes tiers via `PUT /admin/settings/{key}`).

> - **shortfall: none** — 50 of 50 planned rows delivered, UC-256 … UC-305 contiguous, no gaps.

> - **duplicate-check:** compared against all 210 titles in `docs/01-business-analysis/use-case-index.md` §2 (admin console = UC-031…038, UC-084…140). No title repeats an existing use case. Closest pairs and why they are distinct: UC-268 vs UC-035 (specific commission-tier write bounded by BR-ESC-03, not generic settings management); UC-266 vs UC-097 (the `KYC_NOT_APPROVED` blocker path, not the reactivation itself); UC-270/UC-283 vs UC-033 (single audited override/arbiter endpoints, not queue management); UC-286 vs UC-126/UC-129 (3-business-day credit SLA verification, not receipt monitoring or queue triage); UC-294 vs UC-032/UC-038 (Moderator-scoped hide with mandatory reason; UC-032 is Admin, UC-038 is review-only); UC-295 vs UC-100 (`source=AUTO` slice of the queue); UC-297 vs UC-036 (incident-scoped extraction runbook step, not routine log viewing); UC-303 vs UC-305 (per-finding remediation SLA vs monthly severity report review); UC-287/288/289 vs UC-085 and UC-130…133 (same "Run the X Report" verb pattern already used by the four existing specific-report UCs — these three mint the only `API-ANL-007` families not yet covered: `orders`, `gmv`, `returns`).

> - **not minted (PENDING / no evidence):** flags console (M-13), departments UI (M-14), invoices (M-15), provider registry (M-16), calendar (M-19), analytics UI (M-24), moderator audit-log access (unresolved security finding per README §5.1), re-open support ticket (no API), report scheduling (no source), admin delivery-code override (explicitly never in v1 — D7 / `rbac.md` ORG-04 / GAP-02), direct ledger writes (SYSTEM-only, `rbac.md` rows 15-16), FX rates, email login, cart abandonment, wishlist, PWA install.

### 4.3 Portal `customer` — UC-306…360 (55 UCs)

Actor: Customer (ACT-01).

| UC ID | Title | Actor | Block | FR/BR refs | Priority | Source document |
|---|---|---|---|---|---|---|
| UC-306 | Delete an Address Used by an In-Flight Checkout | Customer | B01 | FR-003, FR-011 | P2 | `docs/07-api/core/users.md` |
| UC-307 | Hit the 10-Address Cap and Free Up a Slot | Customer | B01 | FR-003 | P2 | `docs/07-api/core/users.md` |
| UC-308 | Keep Past Orders on Their Address Snapshot After Editing the Book | Customer | B01 | FR-003, FR-012 | P2 | `docs/08-database/core/address.md` |
| UC-309 | Recover After a Refresh-Token Reuse Revokes the Session Family | Customer | B01 | FR-001, BR-AUTH-05 | P1 | `docs/05-frontend/core/state-management.md` |
| UC-310 | Sit Through the 15-Minute Lockout Countdown After Five Failed Logins | Customer | B01 | FR-001, BR-AUTH-04 | P1 | `docs/11-ui-ux/core/user-flows.md` |
| UC-311 | Collect the OTP via WhatsApp When SMS Delivery Fails | Customer | B01 | FR-001, FR-017, BR-NTF-03 | P1 | `docs/07-api/core/notifications.md` |
| UC-312 | Hit the OTP Attempt Cap and Read the Blocked-Verification Notice | Customer | B01 | FR-001, BR-AUTH-03, BR-NTF-02 | P1 | `docs/11-ui-ux/core/screen-states.md` |
| UC-313 | Attach Photos to a Product Review and Handle Upload Rejections | Customer | B02 | FR-006, BR-REV-03 | P2 | `docs/07-api/core/catalog.md` |
| UC-314 | Attempt a Review After the 30-Day Window and Get Rejected | Customer | B02 | FR-006, BR-REV-01 | P2 | `docs/07-api/core/catalog.md` |
| UC-315 | Filter a Product's Reviews by Rating | Customer | B02 | FR-006, BR-REV-05 | P2 | `docs/07-api/core/catalog.md` |
| UC-316 | Read the Vendor's Published Response Beneath Your Review | Customer | B02 | FR-006, BR-REV-04 | P2 | `docs/07-api/core/catalog.md` |
| UC-317 | Check the Return Policy and Window on the Product Page | Customer | B02 | FR-004, FR-016, BR-RET-01 | P2 | `docs/07-api/core/catalog.md` |
| UC-318 | List the Stores You Follow | Customer | B03 | FR-008, BR-VND-05 | P2 | `docs/05-frontend/core/routing.md` |
| UC-319 | Unfollow a Store and Stop Its Notifications | Customer | B03 | FR-008, FR-017, BR-VND-05 | P2 | `docs/07-api/core/stores.md` |
| UC-320 | Open a Suspended Storefront and Find It Unavailable | Customer | B03 | FR-008, BR-VND-04 | P2 | `docs/07-api/core/stores.md` |
| UC-321 | Combine Search Filters and Compare Facet Counts | Customer | B04 | FR-009 | P1 | `docs/07-api/core/search.md` |
| UC-322 | Sort Results by Relevance, Price, Rating, or Newest | Customer | B04 | FR-009 | P2 | `docs/07-api/core/search.md` |
| UC-323 | Recover from a Zero-Result Search with Suggestions and Popular Categories | Customer | B04 | FR-009 | P1 | `docs/07-api/core/search.md` |
| UC-324 | Fall Back to Category Browse When Search Is Unavailable | Customer | B04 | FR-009 | P1 | `docs/11-ui-ux/core/screen-states.md` |
| UC-325 | Add Past a Cart Guard and Leave the Cart Unchanged | Customer | B05 | FR-010, BR-CRT-01 | P1 | `docs/07-api/customer/cart.md` |
| UC-326 | Re-Reserve Stock When a Cart Line's 15-Minute Countdown Expires | Customer | B05 | FR-010, FR-005, BR-CRT-02 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-327 | Re-Confirm a Price That Changed Since Add-to-Cart | Customer | B05 | FR-010, FR-011, BR-CRT-04 | P0 | `docs/07-api/customer/cart.md` |
| UC-328 | Remove an Ineligible Line That Blocks Checkout | Customer | B05 | FR-010, BR-CRT-05 | P1 | `docs/07-api/customer/cart.md` |
| UC-329 | Merge the Guest Cart Into the Account Cart on Login | Customer | B05 | FR-010, BR-CRT-03 | P1 | `docs/07-api/customer/cart.md` |
| UC-330 | Resume Checkout After Topping Up the Wallet Shortfall | Customer | B05 | FR-011, FR-013, BR-CRT-06 | P0 | `docs/11-ui-ux/core/screen-states.md` |
| UC-331 | Retry a Duplicate Confirm and Receive the Original Order | Customer | B05 | FR-011, BR-ORD-06, BR-PLT-03 | P0 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-332 | Reject an Order Total Outside the 500-5,000,000 YER Bounds | Customer | B05 | FR-011, BR-CAT-04 | P1 | `docs/07-api/core/orders.md` |
| UC-333 | Handle a Shipping-Zone Gap for the Selected Address | Customer | B05 | FR-011, FR-015, BR-SHP-01 | P1 | `docs/01-business-analysis/customer/workflow-003.md` |
| UC-334 | Filter the Order List by Status | Customer | B06 | FR-012 | P2 | `docs/07-api/core/orders.md` |
| UC-335 | Refresh the Order Screen After a Status Conflict | Customer | B06 | FR-012, BR-ORD-01 | P2 | `docs/05-frontend/core/forms-and-validation.md` |
| UC-336 | Receive the 24-Hour Escalation Notice on a Stalled Order | Customer | B06 | FR-012, FR-017, BR-ORD-10 | P2 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-337 | Get the Cancel-Window Refusal After READY_FOR_PICKUP | Customer | B06 | FR-012, BR-ORD-04 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-338 | Open the Order Receipt With the Full VAT Breakdown | Customer | B06 | FR-011, FR-012, BR-FIN-01 | P2 | `docs/11-ui-ux/core/feedback-and-engagement.md` |
| UC-339 | Filter Wallet Transactions by Type and Date Range | Customer | B07 | FR-013, BR-PAY-06 | P1 | `docs/07-api/core/wallet.md` |
| UC-340 | Poll a Top-Up Awaiting Provider Confirmation | Customer | B07 | FR-013, BR-PAY-03 | P1 | `docs/07-api/core/wallet.md` |
| UC-341 | Upload a Bank-Transfer Slip for Admin Verification | Customer | B07 | FR-013, BR-PAY-04 | P1 | `docs/07-api/core/wallet.md` |
| UC-342 | Work With a Frozen Wallet (Pay and Top-Up Blocked, Refunds Still Received) | Customer | B07 | FR-013, BR-PAY-09 | P0 | `docs/11-ui-ux/core/screen-states.md` |
| UC-343 | Check Refund Status and the 3-Business-Day Wallet Credit Date | Customer | B07 | FR-016, FR-013, BR-RET-04, BR-PAY-07 | P1 | `docs/07-api/core/wallet.md` |
| UC-344 | Reject a Top-Up Outside the 1,000-5,000,000 YER Bounds | Customer | B07 | FR-013, BR-PAY-02 | P2 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-345 | Read Wallet Amounts Correctly as Arabic-Indic Numerals with a Screen Reader | Customer | B07 | FR-013, BR-PAY-10 | P2 | `docs/12-non-functional/core/accessibility.md` |
| UC-346 | Retrieve the Delivery Code In-App When No SMS Arrives | Customer | B08 | FR-015, FR-017, BR-SHP-02 | P0 | `docs/07-api/delivery/delivery.md` |
| UC-347 | See Failed Delivery Attempts Reflected in Your Order Timeline | Customer | B08 | FR-015, FR-012, BR-ORD-03 | P2 | `docs/11-ui-ux/core/user-flows.md` |
| UC-348 | Open the 24-Hour Code-Lockout Notice and Its Auto-Created Ticket | Customer | B08 | FR-015, FR-020, BR-SHP-03 | P1 | `docs/11-ui-ux/core/screen-states.md` |
| UC-349 | Follow Delivery Progress Without a Map | Customer | B08 | FR-015, BR-SHP-05 | P2 | `docs/11-ui-ux/core/user-flows.md` |
| UC-350 | Check Return Eligibility Before Submitting a Request | Customer | B09 | FR-016, BR-RET-01 | P0 | `docs/07-api/core/returns.md` |
| UC-351 | Open a Late-Window Return on a Completed Order | Customer | B09 | FR-016, BR-RET-01 | P1 | `docs/03-system-analysis/core/state-transitions.md` |
| UC-352 | Watch a Return Auto-Approve After the 72-Hour Inspection Timeout | Customer | B09 | FR-016, BR-RET-05 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-353 | Read the Refund Composition (Item Value Versus Shipping) | Customer | B09 | FR-016, BR-RET-03 | P2 | `docs/01-business-analysis/core/workflow-007.md` |
| UC-354 | Resolve a Conflict Between an Open Dispute and a New Return | Customer | B09 | FR-016, FR-012, BR-ORD-05 | P2 | `docs/07-api/core/returns.md` |
| UC-355 | Filter the Notification Inbox by Category and Unread State | Customer | B10 | FR-017 | P2 | `docs/07-api/core/notifications.md` |
| UC-356 | Disable a Marketing Channel Without Silencing Order Alerts | Customer | B10 | FR-017, BR-NTF-05 | P1 | `docs/11-ui-ux/core/feedback-and-engagement.md` |
| UC-357 | See Locked Security Toggles in the Preference Center | Customer | B10 | FR-017, BR-NTF-02 | P1 | `docs/11-ui-ux/core/feedback-and-engagement.md` |
| UC-358 | Keep Using the App When Push Permission Is Denied | Customer | B10 | FR-017 | P1 | `docs/11-ui-ux/core/screen-states.md` |
| UC-359 | Add a Message and Attachment to an Open Support Ticket Thread | Customer | B13 | FR-020 | P2 | `docs/07-api/admin/admin.md` |
| UC-360 | Rate the Support Resolution in the Post-Ticket Survey | Customer | B13 | FR-020 | P2 | `docs/11-ui-ux/core/feedback-and-engagement.md` |

> - sources verified: every cited path was confirmed to exist in the repo (directory listings of `docs/07-api/`, `docs/11-ui-ux/`, `docs/05-frontend/`, `docs/03-system-analysis/`, `docs/01-business-analysis/`, `docs/08-database/`, `docs/12-non-functional/`) and then read/skimmed for the specific behavior: `cart.md` (guard ladder, reservation countdown, priceChanges, blockers, guest merge), `orders.md` (idempotent confirm, ORDER_VALUE_OUT_OF_RANGE, `?status` filter), `wallet.md` (API-WAL-002 filters, API-WAL-004/005 top-up poll+proof, API-WAL-014 refund receipt), `returns.md` (WINDOW_EXPIRED vs NOT_RETURNABLE, DISPUTE_ALREADY_OPEN), `search.md` (facets, sort modes, zero-result, degradation), `catalog.md` (review media/eligibility/list filters, PDP return policy, vendor response), `users.md` (MAX_ADDRESSES_REACHED, in-flight-checkout delete guard), `notifications.md` (inbox filters, SMS->WhatsApp failover), `stores.md` (unfollow, suspended storefront 404), `delivery.md` (API-SHP-013 in-app code), `admin.md` (API-ADM-038 thread reply), `user-flows.md` FL-01/FL-03/FL-06, `screen-states.md` §5-§8, `feedback-and-engagement.md` §2/§5/§7/§9, `routing.md` §2/§9, `forms-and-validation.md` §5 (409 STATE_CONFLICT), `state-management.md` §5 (reuse revocation), `edge-cases.md` EC-01/05/11/13/15/21/23/35/38/42, `state-transitions.md` §2 (COMPLETED -> RETURN_REQUESTED), `workflow-003.md` (NO_SHIPPING_ZONE), `workflow-007.md` (refund composition), `../08-database/core/address.md` (shipping_address_snapshot), `../12-non-functional/core/accessibility.md` §7 (Arabic-Indic SR pronunciation). BR IDs checked against the 104-ID registry in `docs/01-business-analysis/business-rules.md`; FR IDs checked against `docs/02-requirements/requirements-overview.md` (FR-001…FR-020 only).

> - shortfall: none (55 of 55 rows produced, UC-306 … UC-360)

> - duplicate-check: every title was diffed against index §2 of `docs/01-business-analysis/use-case-index.md` for the 58 existing Customer rows (UC-001…014, UC-041…042, UC-141…182) and rejected/reworded if it duplicated or paraphrased one (e.g. distinct edges chosen over "Manage Addresses", "Track Order", "Top Up Wallet", "Resend an OTP", "Contact Support"); all §5.1 PENDING items were excluded — no wishlist (UC-318/319 cover follows only, not `/account/wishlist`), no cart-abandonment recovery (UC-329 is login-time guest-cart merge), no PWA install, no search analytics UI, no engagement stats, no FX display, no email login, no support-ticket reopening (UC-359 appends to an already-open thread via API-ADM-038), and no vendor right-of-reply (UC-316 is the customer reading an already-published response on a visible review).

### 4.4 Portal `vendor` — UC-361…395 (35 UCs)

Actor: Vendor (ACT-02).

| UC ID | Title | Actor | Block | FR/BR refs | Priority | Source document |
|---|---|---|---|---|---|---|
| UC-361 | Resolve Publish Blockers on an Incomplete Listing | Vendor | B02 | FR-004, BR-CAT-01 | P1 | `docs/07-api/core/catalog.md` |
| UC-362 | Upload Product Images Within Count and Format Limits | Vendor | B02 | FR-004, BR-CAT-08 | P1 | `docs/07-api/core/catalog.md` |
| UC-363 | Correct Price Validation Rejections on a Listing Draft | Vendor | B02 | FR-004, BR-CAT-04 | P2 | `docs/08-database/core/product.md` |
| UC-364 | Define Product Variants Within Dimension and SKU Limits | Vendor | B02 | FR-004, BR-CAT-02 | P1 | `docs/07-api/core/catalog.md` |
| UC-365 | Filter the Inventory Table for Low-Stock SKUs | Vendor | B02 | FR-005, BR-CAT-07 | P2 | `docs/07-api/core/catalog.md` |
| UC-366 | Recover From a Stock Adjustment Blocked by Active Reservations | Vendor | B02 | FR-005, BR-INV-03 | P1 | `docs/07-api/core/catalog.md` |
| UC-367 | Confirm Search Visibility After a Catalog Change | Vendor | B04 | FR-004, FR-009, BR-CAT-06 | P2 | `docs/07-api/core/catalog.md` |
| UC-368 | Set Weekly Store Operating Hours | Vendor | B03 | FR-008, BR-VND-04 | P2 | `docs/07-api/core/stores.md` |
| UC-369 | Revise KYC Documents Rejected at Upload | Vendor | B03 | FR-007, BR-VND-03 | P2 | `docs/07-api/core/stores.md` |
| UC-370 | Block Demotion of the Last Store Owner | Vendor | B03 | FR-002, BR-VND-06 | P1 | `docs/07-api/core/stores.md` |
| UC-371 | Handle Store Suspension During Active Fulfillment | Vendor | B03 | FR-007, FR-012, BR-VND-04 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-372 | Handle Staff Invitation Rejections (Unregistered Phone or Staff Limit) | Vendor | B03 | FR-002, BR-VND-06 | P2 | `docs/07-api/core/stores.md` |
| UC-373 | Define Domestic Shipping Zones and Store Fees | Vendor | B08 | FR-008, FR-015, BR-SHP-01 | P1 | `docs/07-api/core/stores.md` |
| UC-374 | Enable Auto-Accept for Incoming Sub-Orders | Vendor | B06 | FR-012, BR-ORD-01 | P1 | `docs/01-business-analysis/vendor/workflow-004.md` |
| UC-375 | Start Fulfillment on a Confirmed Sub-Order | Vendor | B06 | FR-012, BR-ORD-03 | P0 | `docs/07-api/core/orders.md` |
| UC-376 | View the Append-Only Timeline for an Own Sub-Order | Vendor | B06 | FR-012, BR-ORD-03, BR-ORD-09 | P2 | `docs/07-api/core/orders.md` |
| UC-377 | Recover From a State Conflict on a Concurrent Order Action | Vendor | B06 | FR-012, BR-ORD-01 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-378 | Handle a Closed Cancellation Window on a Dispatched Sub-Order | Vendor | B06 | FR-012, BR-ORD-04 | P2 | `docs/07-api/core/orders.md` |
| UC-379 | Triage the Sub-Order Queue by SLA Age | Vendor | B06 | FR-012, BR-ORD-10 | P2 | `docs/07-api/core/orders.md` |
| UC-380 | Track Overdue Return Decisions Before the 48-Hour Escalation | Vendor | B09 | FR-016, BR-RET-02 | P1 | `docs/07-api/core/returns.md` |
| UC-381 | Track the Return Pickup Status After Approval | Vendor | B09 | FR-016, FR-015, BR-SHP-04 | P2 | `docs/07-api/core/returns.md` |
| UC-382 | Handle a Return Auto-Approved After the 72-Hour Inspection Window | Vendor | B09 | FR-016, BR-RET-05 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-383 | Raise a Dispute on an Own Sub-Order | Vendor | B09 | FR-016, FR-012, BR-ORD-05 | P0 | `docs/07-api/core/returns.md` |
| UC-384 | Verify Return-Window Eligibility Before a Decision | Vendor | B09 | FR-016, BR-RET-01 | P1 | `docs/07-api/core/returns.md` |
| UC-385 | Monitor Frozen Escrow Holds on Own Sub-Orders | Vendor | B07 | FR-014, BR-ORD-05, BR-ESC-02 | P2 | `docs/07-api/core/wallet.md` |
| UC-386 | Handle a Payout Request Below the 1,000 YER Minimum | Vendor | B07 | FR-014, BR-ESC-05 | P2 | `docs/07-api/core/wallet.md` |
| UC-387 | Investigate a Rejected Payout's Reason and Ledger References | Vendor | B07 | FR-014, BR-ESC-06 | P2 | `docs/07-api/core/wallet.md` |
| UC-388 | Resolve Payout Holds While KYC or Store Status Is Blocked | Vendor | B07 | FR-014, BR-ESC-06, BR-VND-04 | P1 | `docs/03-system-analysis/core/edge-cases.md` |
| UC-389 | Re-Verify the Payout Account After a Destination Change | Vendor | B07 | FR-014, BR-ESC-06 | P1 | `docs/07-api/core/stores.md` |
| UC-390 | Compare Store Metrics Against the Previous Period | Vendor | B11 | FR-018, BR-VND-07 | P2 | `docs/07-api/core/analytics.md` |
| UC-391 | Resolve a Report Export Row-Cap Rejection | Vendor | B11 | FR-018, BR-VND-06 | P2 | `docs/07-api/core/analytics.md` |
| UC-392 | Adjust Schedule and Limits or Disable an Active Store Coupon | Vendor | B12 | FR-019, BR-PRM-04 | P1 | `docs/07-api/core/content.md` |
| UC-393 | Resolve Store Coupon Creation Rejections (Bounds and Duplicate Code) | Vendor | B12 | FR-011, BR-PRM-01 | P2 | `docs/01-business-analysis/admin/workflow-012.md` |
| UC-394 | Configure Vendor Notification Preferences for Store Events | Vendor | B10 | FR-017, BR-NTF-02, BR-NTF-05 | P2 | `docs/07-api/core/notifications.md` |
| UC-395 | Open a Support Ticket About a Payout or Payment Issue | Vendor | B13 | FR-020, BR-PLT-03 | P2 | `docs/07-api/admin/admin.md` |

> - sources verified: read the UC master index (`docs/01-business-analysis/use-case-index.md` §2 vendor rows UC-015…024 / UC-183…204, §5.1 PENDING list) and the full BR registry (`docs/01-business-analysis/business-rules.md`, 104 IDs across 15 domains) plus the FR-001…FR-020 list (`docs/02-requirements/acceptance-criteria.md`); then opened every cited source file and matched each row to a concrete endpoint, rule, edge case, or workflow step: `docs/07-api/{catalog,stores,orders,wallet,returns,analytics,content,notifications,admin}.md` (API-CAT-006/008/010/012/014/016 + §2 indexing note; API-VND-004/008/009/010/011/017/018/021; API-ORD-005/006/009/011; API-WAL-009/011/013; API-RET-004/005/008/009/013/016; API-ANL-001/003; API-CNT-019/020; API-NTF-006/007; API-ADM-035), `docs/01-business-analysis/vendor/workflow-004.md` (auto-accept alternative), `docs/01-business-analysis/admin/workflow-012.md` (coupon creation validation step 2), `docs/03-system-analysis/core/edge-cases.md` (EC-13/14/17/38), `docs/08-database/core/product.md` (price/sale-price CHECK constraints, search-sync flags). All 13 cited paths exist in the repo; every FR/BR ID used was cross-checked against the registries — no invented IDs. Deliberately dropped: bulk CSV inventory import (explicitly out of scope per `docs/02-requirements/core/FR-004.md` §out-of-scope) and monthly statements (adjacent to PENDING `M-15` Invoices); no non-physical-product-type row was kept because the create/update request schemas carry no `product_type` field (weak evidence).

> - shortfall: none (35 of 35 rows produced for UC-361…UC-395; no fabricated scenarios — every row maps to an endpoint, rule, EC, or workflow step shown above)

> - duplicate-check: read index §2 and excluded all 32 existing vendor titles (UC-015…024, UC-183…204); excluded all PENDING items §5.1 (M-01 FX, M-04 escrow-maturity vendor note, M-14 departments, M-15 invoices, M-19 calendar, M-20 vendor right-of-reply to a hidden review, and "reopen a support ticket"); near-neighbours were differentiated by goal/state rather than wording — e.g. UC-375 covers CONFIRMED→PROCESSING while UC-020 covers PROCESSING→READY_FOR_PICKUP; UC-382 covers the missed-72h auto-approve branch while UC-195 covers on-time inspection; UC-383 covers vendor-initiated disputes while UC-196 covers responding to a buyer's dispute; UC-392/393 cover coupon update/disable and creation-rejection branches while UC-023/UC-203 only create/list; UC-389 covers post-change payout re-verification while UC-187 covers initial configuration; UC-385 monitors escrow freeze state (API-WAL-009 `frozenBy`) and intentionally avoids any escrow-maturity note framing (M-04); UC-395 opens a payment/payout-scoped ticket while UC-204 opens an order-scoped ticket. Portal constraint held throughout: primary actor is Vendor (ACT-02) only, vendor-panel surface only.

### 4.5 Portal `delivery` — UC-396…420 (25 UCs)

Actor: Delivery Provider (ACT-03).

| UC ID | Title | Actor | Block | FR/BR refs | Priority | Source document |
|---|---|---|---|---|---|---|
| UC-396 | Decline a Delivery Offer Without Claiming It | Delivery Provider | B08 | FR-015, BR-SHP-04 | P1 | `docs/08-database/core/shipment.md` |
| UC-397 | Review the Shipment Attempt Log Before a Retry | Delivery Provider | B08 | FR-015, BR-SHP-06 | P1 | `docs/07-api/delivery/delivery.md` |
| UC-398 | Upload an Optional Delivery Photo as Extra Proof | Delivery Provider | B08 | FR-015, BR-SHP-07 | P2 | `docs/07-api/delivery/delivery.md` |
| UC-399 | Finish on the Proof Success Screen and Continue to the Next Job | Delivery Provider | B08 | FR-015, BR-SHP-07 | P2 | `docs/11-ui-ux/core/screen-states.md` |
| UC-400 | Disable Code Entry When the Job Is Reassigned or Released | Delivery Provider | B08 | FR-015, BR-SHP-04 | P1 | `docs/11-ui-ux/core/screen-states.md` |
| UC-401 | Recover from Delivery-Code Entry Rate Limiting | Delivery Provider | B08 | FR-015, BR-SHP-03 | P2 | `docs/07-api/delivery/delivery.md` |
| UC-402 | Keep Attempt and Lock Progress Across an App Restart | Delivery Provider | B08 | FR-015, BR-SHP-03 | P2 | `docs/03-system-analysis/core/failure-modes.md` |
| UC-403 | Work a Delivery Whose Attempts Are Frozen for Admin Review | Delivery Provider | B08 | FR-015, BR-SHP-06 | P1 | `docs/07-api/delivery/delivery.md` |
| UC-404 | Hear Code Attempt Feedback via Screen Reader | Delivery Provider | B08 | FR-015, BR-SHP-03 | P2 | `docs/12-non-functional/core/accessibility.md` |
| UC-405 | Track Personal Delivery Stats on the Courier Profile | Delivery Provider | B08 | FR-015 | P2 | `docs/07-api/delivery/delivery.md` |
| UC-406 | Register This Courier Device for Job Push Notifications | Delivery Provider | B10 | FR-017 | P1 | `docs/07-api/core/notifications.md` |
| UC-407 | Open a Delivery Job from a Push Deep Link | Delivery Provider | B10 | FR-017, FR-015 | P1 | `docs/07-api/core/notifications.md` |
| UC-408 | Fall Back to the In-App Inbox When Push Delivery Fails | Delivery Provider | B10 | FR-017 | P2 | `docs/10-integrations/core/push-notifications.md` |
| UC-409 | Configure Delivery Notification Channels as a Courier | Delivery Provider | B10 | FR-017, BR-NTF-05 | P2 | `docs/07-api/core/notifications.md` |
| UC-410 | Resume a Delivery Deep Link After Signing In | Delivery Provider | B01 | FR-001, FR-015 | P2 | `docs/05-frontend/core/routing.md` |
| UC-411 | Re-Authenticate When the Session Expires Mid-Job | Delivery Provider | B01 | FR-001, FR-015 | P1 | `docs/11-ui-ux/core/screen-states.md` |
| UC-412 | Switch the Courier App Language Between Arabic and English | Delivery Provider | B01 | FR-003 | P2 | `docs/11-ui-ux/core/information-architecture.md` |
| UC-413 | Record Vendor Receipt of an Approved Return Package | Delivery Provider | B09 | FR-016, BR-RET-02 | P0 | `docs/01-business-analysis/core/workflow-007.md` |
| UC-414 | Escalate a Failed Return Pickup to Operations | Delivery Provider | B09 | FR-016, FR-020 | P2 | `docs/01-business-analysis/core/workflow-007.md` |
| UC-415 | Browse Completed Jobs in the History Tab | Delivery Provider | B08 | FR-015 | P2 | `docs/05-frontend/core/routing.md` |
| UC-416 | Handle Access Denied When Opening a Delivery You Do Not Own | Delivery Provider | B08 | FR-015, BR-ORD-09 | P2 | `docs/07-api/delivery/delivery.md` |
| UC-417 | Record a Failed Pickup Attempt When the Store Is Not Ready | Delivery Provider | B08 | FR-015, BR-SHP-06 | P1 | `docs/08-database/core/shipment.md` |
| UC-418 | Wait and Retry Later When the Customer Is Unavailable | Delivery Provider | B08 | FR-015, BR-SHP-03 | P1 | `docs/01-business-analysis/delivery/workflow-005.md` |
| UC-419 | Work Only with a Masked Buyer Code at the Door | Delivery Provider | B08 | FR-015, BR-SHP-02 | P1 | `docs/07-api/delivery/delivery.md` |
| UC-420 | Type the Delivery Code with Latin Digits in the Arabic Interface | Delivery Provider | B08 | FR-015, BR-PLT-05 | P2 | `docs/11-ui-ux/core/localization.md` |

> - sources verified: Read `docs/01-business-analysis/use-case-index.md` §2 index first, then read all 12 existing courier UC files (UC-025…UC-030, UC-205…UC-210) in full to map covered scenarios. Each cited source was opened and matched to the row: `docs/07-api/delivery/delivery.md` (API-SHP-003 attempts/proof, -009 `buyerCodeMasked` + CUSTOMER-only -013, -012 photo upload, -014 stats, §2 rate limiter / `DELIVERY_ATTEMPTS_EXCEEDED` / visibility scoping); `docs/07-api/core/notifications.md` (API-NTF-006/007/008, §2 deep-link contract `surface: COURIER`); `docs/10-integrations/core/push-notifications.md` (§6 in-app mirror, §7 provider-outage fallback); `docs/01-business-analysis/delivery/workflow-005.md` step 6 (customer absence — attempt not consumed) and `workflow-007.md` step 5 + Exceptions (return custody, failed return pickup); `docs/03-system-analysis/core/failure-modes.md` §2.5 (lock/attempts survive app restart); `docs/03-system-analysis/core/edge-cases.md` §4 (EC-29/30/31 — checked, already covered by UC-030/UC-208/UC-026); `docs/08-database/core/shipment.md` (`shipment_offer` DECLINED/EXPIRED, `shipment_attempt` outcomes incl. PICKUP_FAILED); `docs/11-ui-ux/core/screen-states.md` §4/§7/§9; `docs/11-ui-ux/core/information-architecture.md` §6/§8 (S5 tabs, S5 locale row); `docs/11-ui-ux/core/localization.md` (Latin digits in code slots); `docs/05-frontend/core/routing.md` §5/§6 (S5 `History` tab, deep-link auth bounce, ACT-03 landing); `docs/12-non-functional/core/accessibility.md` (S5 / FL-06 attempts announcements); `docs/09-security/core/rbac.md` §5/§6 (courier least-privilege, historically-delivered reads, 403 scoping). FR refs restricted to FR-001…FR-020 and BR refs to the 104 IDs extracted from `docs/01-business-analysis/business-rules.md` (grep of the BR table). No file in the repo was modified.

> - shortfall: none — 25/25 rows produced. Caveat (transparency, not a shortfall): UC-396 and UC-417 are backed at entity level only (`shipment_offer.status = DECLINED`, `shipment_attempt.outcome = PICKUP_FAILED`); v1 `delivery.md` has no dedicated endpoint for decline or pickup-failure — the row documents a real modeled behavior but the API gap should be closed or the row demoted at review time. Two task focus areas were deliberately NOT minted because no source describes them: batch/multi-package pickup (sources model one shipment per sub-order; multi-job is only UC-026 A2/UC-028 A1) and shift/idle sweeps (background register has only `assign-offer`, `code-expire`, `code-issue`, `failed-attempt-sla` — all System-actor).

> - duplicate-check: Compared every proposed title against the §2 index titles of UC-025…UC-030 and UC-205…UC-210, then against those 12 files' scenario sections (read in full). Near-misses resolved deliberately: UC-417 narrows to the pickup-side attempt record (UC-027 E1 is a one-line exception; UC-029 is the *delivery* attempt), UC-398 targets the standalone proof-photo upload endpoint (existing UCs only mention photos in passing), UC-418 is WF-005 step 6 "absence → retry, attempt not consumed" (vs UC-030 A2 refusal → failed attempt), UC-403 is the post-escalation blocked state (UC-029 records the 3rd attempt; UC-136 is the admin side), UC-400 is assignment *changed by another actor* while the code screen is open (UC-205 is the courier's own release), UC-405/UC-415/UC-416 are stats/history/scoping reads distinct from UC-206/UC-209/UC-025. UC-409 parallels customer UC-177 but is a different portal/actor and was retitled for the courier context. Sanity gates: no row mentions GPS, geolocation or real-time tracking (C-16 / BR-SHP-05), no row introduces COD, all rows use primary actor `Delivery Provider`, blocks limited to B01/B08/B09/B10, priorities only P0/P1/P2.

## 5. Proposed requirement deltas (5) and business-rule deltas (7)

| Proposed ID | One-line statement | Source (exact path + section/line) | Related existing IDs | Priority |
|---|---|---|---|---|
| `SEC-REQ-013` | Anti-enumeration becomes a testable requirement: authentication/verification entry points always answer with the uniform success-shaped response and never confirm or deny account existence, resolving the current split between the §5 guidance and `API-ATH-001`'s `PHONE_ALREADY_REGISTERED`. | `docs/07-api/core/error-model.md` §5 "Localization of Error Messages" line 294; `docs/07-api/core/auth.md` §1 — API-ATH-002 line 28 ("response identical whether or not the account exists"), API-ATH-008 line 34, vs API-ATH-001 line 27 (`PHONE_ALREADY_REGISTERED`) | SEC-REQ-001, SEC-REQ-004, FR-001, BR-AUTH-01, BR-AUTH-03, UC-004, UC-141 | High |
| `SEC-REQ-014` | Explicit per-surface CORS policy: exact origin allowlist for web/vendor/admin, credentialed CORS only for known origins, methods/headers allowlist, deny-by-default preflight enforced by a single middleware, with a CORS test case. | `docs/09-security/core/security-findings.md` SEC-010 lines 115–121 ("No document defines allowed origins, credentialed-CORS behavior, or preflight rules") | SEC-REQ-008, SEC-REQ-003, FR-001; `docs/18-decisions/ADR/ADR-010.md` line 70 | Medium |
| `SEC-REQ-015` | Object-storage access control: deny anonymous access and listing on all MinIO buckets, short presigned-URL TTLs, separate media origin, server-generated object keys, and quarterly bucket-policy review verified in tests. | `docs/09-security/core/security-findings.md` SEC-008 lines 99–105 ("Bucket policies (anonymous listing blocked?), presigned-URL TTL … not specified anywhere"); `docs/09-security/core/security-controls.md` line 100 (presigned store) | SEC-REQ-006, SEC-REQ-011, FR-007, INT-REQ-002, DATA-REQ-002 | Medium |
| `SEC-REQ-016` | OTP resend cooldown and resend caps must also be enforced globally per hashed destination phone (not only per session/IP), with a per-destination metric and alert against OTP bombing of a victim number. | `docs/09-security/core/security-findings.md` SEC-006 lines 83–89 (line 86: "nothing in the canon mandates a per-**destination** limit across different requesters"); `docs/09-security/core/threat-model.md` TM-02 residual | SEC-REQ-009, SEC-REQ-005, BR-AUTH-03, FR-001 | Medium |
| `DATA-REQ-009` | Search-index data protection: index field allowlist (public catalog fields only), restricted/encrypted index snapshots, and index deletion wired into the account-deletion workflow, with a "PII in index" test. | `docs/09-security/core/security-findings.md` SEC-007 lines 91–97 (line 94: what is indexed and "how deletion propagates (index vs source) are all undefined"; line 95: `DATA-REQ-003` "silently unmet for indexed fields") | SEC-REQ-006, DATA-REQ-002, DATA-REQ-003, FR-009, NFR-019 | Medium |
| `BR-ESC-09` | Escrow release and dispute freeze are serialized: the release job evaluates the `BR-ESC-02` gate inside one transaction under the same row/aggregate lock that a concurrent freeze takes, the release is idempotent/reconcilable, and a concurrency test is required before launch. | `docs/09-security/core/security-findings.md` SEC-015 lines 155–161 (line 158 TOCTOU description; line 160 recommendation) | BR-ESC-01, BR-ESC-02, BR-ORD-05, FR-014, FR-016, NFR-008, SEC-REQ-010 | High |
| `BR-RET-08` | The return approval decision must be made within 48 h of `RETURN_REQUESTED`; if no decision lands within 48 h the case auto-escalates to admin review with notification — never silently pending. | `docs/03-system-analysis/core/state-transitions.md` line 66 ("Decision within 48 h SLA; auto-escalate to admin after 48 h"); `docs/03-system-analysis/core/functional-analysis.md` line 107; `docs/03-system-analysis/core/edge-cases.md` EC-39 line 81; `docs/03-system-analysis/core/data-flow.md` DF-28 line 27 | BR-RET-01, BR-RET-02, BR-RET-05 (72 h analogue), BR-VND-03 (48 h analogue), FR-016, FR-020 | High |
| `BR-AUTH-09` | The OTP verification-attempt counter is consumed only by wrong-code entry: provider/channel failures inside the OTP validity window never consume an attempt, leave the counter untouched, and offer retry. | `docs/03-system-analysis/core/failure-modes.md` §2.1 line 48 ("the OTP attempt counter is **not** consumed by provider failures (only by wrong-code entry)"); governing IDs line 50 cite no BR for this behavior | BR-AUTH-03, BR-NTF-03, SEC-REQ-001, SEC-REQ-005, INT-REQ-003, INT-REQ-004 | Medium |
| `BR-AUTH-10` | Account deletion is blocked while open orders, active returns/disputes, a non-zero wallet balance, pending vendor payouts, or an active store exist; the refusal enumerates every blocking reason so the user can settle them first. | `docs/07-api/core/error-model.md` §4.3 line 141 (`DELETION_BLOCKED` — "open orders/returns/payouts must settle first"); `docs/07-api/core/users.md` §2 line 43 ("Deletion blocking conditions … the response lists the blocking reasons in `details[]`") | FR-003, DATA-REQ-003, NFR-019, SEC-REQ-001 | Medium |
| `BR-PAY-11` | Wallet authorization-hold lifecycle: a hold never exceeds available balance and expires with the 15-minute checkout session, capture happens only inside the order saga (SYSTEM), and every uncaptured hold is released exactly once — capture XOR release, idempotent under replay and concurrency. | `docs/07-api/core/wallet.md` API-WAL-006 line 32, API-WAL-008 line 34, §4 line 49 ("Authorization/capture split"); `docs/01-business-analysis/core/UC-051.md` lines 21–45 (trigger, main scenario, E2) | FR-011, FR-013, BR-PAY-05, BR-PAY-06, BR-PAY-08, BR-CRT-06, BR-PLT-03, BR-PLT-04, C-13 | High |
| `BR-REV-06` | A user is auto-flagged for moderation on 5 confirmed spam/abuse reports, and the confirmed-report count drives auto-flagging of content in the moderation queue (the canon currently asserts the threshold while citing the wrong rule). | `docs/07-api/admin/admin.md` API-ADM-003 line 31 ("required on 5 confirmed spam/abuse reports"); API-ADM-027 line 85 (cites `BR-ORD-06 (5-report flag)` — but `docs/01-business-analysis/business-rules.md` line 81 shows BR-ORD-06 is order idempotency) | FR-019, FR-020, BR-REV-04, BR-PLT-06 | Medium |
| `BR-PLT-08` | Support-ticket lifecycle `OPEN → IN_PROGRESS → RESOLVED → CLOSED`: a staff reply moves an OPEN ticket to IN_PROGRESS, the customer may reopen a RESOLVED ticket exactly once before it is CLOSED, later replies are rejected with `TICKET_STATE_CONFLICT`, and auto-created tickets follow the same states. | `docs/07-api/admin/admin.md` §1.9 — API-ADM-036 line 104 (state enum), API-ADM-038 line 106 (IN_PROGRESS on staff reply), API-ADM-041 line 109 ("customer may reopen once … before it is closed"); `docs/01-business-analysis/core/business-processes.md` BP-15 line 148 ("resolve → close with resolution code") | FR-019, FR-020, BR-SHP-03, BR-ORD-09, BR-ORD-10, BR-PLT-06, DATA-REQ-008 | Medium |

### 5.1 Derivation method (evidence)

**Registries read (to fix next-free IDs and verify non-coverage):**
- `docs/02-requirements/requirements-overview.md` — 68 requirements; last IDs FR-020, NFR-020, SEC-REQ-012, DATA-REQ-008, INT-REQ-008 → deltas use SEC-REQ-013…016, DATA-REQ-009 (FR/NFR/INT: no uncovered item survived verification).
- `docs/01-business-analysis/business-rules.md` — 104 rules / 15 domains; last IDs in touched domains: BR-AUTH-08, BR-ESC-08, BR-PAY-10, BR-RET-07, BR-REV-05, BR-PLT-07 → deltas use BR-AUTH-09/10, BR-ESC-09, BR-PAY-11, BR-RET-08, BR-REV-06, BR-PLT-08 (existing domains only, per task rule).
- Constraints are owner-locked `C-01…C-26` → no new `C-NN`; candidates listed under Deferred.

**Documents mined for described-but-unregistered behavior:**
`docs/09-security/core/security-findings.md` (SEC-001…015), `docs/09-security/core/threat-model.md`, `docs/09-security/core/security-controls.md`, `docs/09-security/core/data-protection.md`; `docs/03-system-analysis/core/failure-modes.md` (FM-01…18), `edge-cases.md` (EC-39), `state-transitions.md`, `functional-analysis.md`, `data-flow.md`, `erp-finance-departments.md`, `system-boundary.md`, `sequence-flows.md`; `docs/07-api/core/error-model.md`, `api-conventions.md`, `../07-api/core/auth.md`, `admin.md`, `wallet.md`, `users.md`, `returns.md`, `delivery.md`; `docs/12-non-functional/core/usability-and-support.md`; `docs/20-validation/missing-information.md` (GAP-01…14); `docs/01-business-analysis/core/business-processes.md` (BP-14/15), `../01-business-analysis/core/UC-051.md`, `UC-004.md`, `UC-014.md`; `docs/18-decisions/ADR/ADR-010.md`.

**Coverage greps run (grep tool; `rg` unavailable on this Windows host):**
- `docs/02-requirements` × `enumerat|CORS|presign|bucket|48 h|reopen|hold` → matches only state-machine/stock-hold/KYC-48 h usages (FR-007, FR-012, AC-FR012-01); no requirement covers anti-enumeration at auth entry points, CORS, object-storage access, per-destination OTP limits, search-index PII, return 48 h SLA, ticket lifecycle, or wallet authorization holds.
- `docs/02-requirements` × `48 hours|auto-escalat|DELETION_BLOCKED|blocking condition|open orders` → only FR-007 (KYC) and FR-012 (24 h order escalation); FR-016 has no 48 h rule, FR-003 has no deletion-blocker rule.
- `docs/01-business-analysis/business-rules.md` × `hold|reopen|spam|report|ticket|consum|serializ|index|48` → only BR-VND-03 (KYC 48 h), BR-ESC-01 (7-day escrow), BR-INV-01 (stock holds), BR-SHP-03 (auto-creates tickets); no rule for return 48 h, OTP-attempt consumption, escrow/dispute serialization, report threshold, ticket states, deletion blockers, or payment holds.
- `docs/09-security` × `presigned|presign|anonymous` and `docs` × `CORS` → only SEC-008/SEC-010 findings and a `WEB_BASE_URL` config row; nothing in requirements.
- Each proposed statement was cross-checked against its related FR/NFR/SEC/DATA/INT file and the BR registry row before being accepted as a gap; borderline candidates (NFR-021 OTP-delivery SLO, MinIO-outage degradation, push-token detach, courier offline) were dropped as covered (NFR-007, FM-17 governing `SEC-REQ-011`, FR-017, FR-015) or weaker than the selected evidence.

**Counts:** 12 proposed deltas (4 High, 8 Medium) · 6 deferred / owner-decision candidates.

## 6. Deferred / owner-decision candidates (not part of this implementation)

| Idea | Why deferred |
|---|---|
| Support severity S1–S4 response/resolution SLAs (candidate NFR/BR) | `docs/12-non-functional/core/usability-and-support.md` §5 "Support SLAs" line 100 marks all targets `INFERENCE` "and must be confirmed against sponsor capacity at launch readiness"; `docs/01-business-analysis/core/business-objectives.md` BO-11 line 52 records ticket SLA as `INSUFFICIENT EVIDENCE`. Sponsor decision first — a requirement would freeze unsanctioned numbers. |
| Webhook replay window (±5 min) + nonce/payload store (candidate INT-REQ) | `docs/09-security/core/security-findings.md` SEC-005 line 80 calls the window a "design choice" and assigns the spec to `../10-integrations/core/webhook-reliability.md`, which does not exist yet. Mint after that integration document lands; the key is also noted `INFERENCE`. |
| MFA / step-up at ADMIN & SUPER_ADMIN login (candidate SEC-REQ-013+ if minted later) | `docs/09-security/core/security-findings.md` SEC-012 lines 134–136 explicitly require "a decision record (18-decisions/) before implementation". A SEC-REQ minted now would pre-empt the ADR; also conflicts with `authentication.md` §7 ("none in v1"). |
| ERP/finance department surface (accounts, sales, purchases, inventory snapshots, period close) as FR-021+ / BR-FIN-06+ | `docs/03-system-analysis/core/erp-finance-departments.md` line 26 states the document "mints no new identifiers" by design; it is approved scope (D2/D3/D11) but plan wave discipline (SPE-03 / D-02) converts backlog rows to FR/BR only at their build wave, never earlier. |
| New owner-locked constraint (e.g. "C-27 — no AI chatbot or automated adjudication in v1") | The constraint register `C-01…C-26` is owner-locked (`RULES_HINTS.md`); the behavior already exists as a binding scope note (`docs/03-system-analysis/core/system-boundary.md` line 56, tied to `FR-020` / UC-014). Elevation to a `C-NN` is an owner change, not an analysis output. |
| Loyalty program, tiered/subscription commission, vendor cash-out behaviors (extend BR-PRM / BR-ESC-03 / BR-PAY) | Open owner gaps `GAP-04`, `GAP-05`, `GAP-06` — `docs/20-validation/missing-information.md` lines 37–39 (GAP-04/05 deferred per `plan-develop.md` §8 D8, GAP-06 OPEN). Rules cannot be written before the owner answers. |

## 7. Proposed constraint / process / rule changes — proposed, then deferred

| Proposed change | Route required | Evaluation |
|---|---|---|
| New owner constraint (e.g. `C-27` — no AI chatbot / automated adjudication in v1) | Root `docs/README.md` §9 + owner lock (`RULES_HINTS.md`; `C-01…C-26` are owner-locked) | **DEFER** — already binding as scope prose (`docs/03-system-analysis/core/system-boundary.md` §…, `FR-020`/UC-014); elevation is an owner change (`AUD-04`) |
| `YUMN_RULES.md` new/amended rule text (portal-split enforcement rule, UC-count floors) | `senior-rules/core/00` §0.5 → VERSION + CHANGELOG bump | **DEFER** — "propose, defer" per `prompt-011.md` §4.2; rule text changes are out of the assistant's unilateral reach |
| `YUMN_RULES.md` path references (`docs/03-system-analysis/core/state-transitions.md` etc.) realigned to the portal split | Factual prose correction (no pin move; session 005/008 precedent) | **ACCEPT** — implemented as part of the migration (phase 5), recorded in the session file |
| Folder-path scheme (`docs/<nn-domain>/<portal>/<file>`) + UC allocation `210 → 420` | `22-glossary/naming-conventions.md` version bump + CH row **before** any move (phase 4) | **ACCEPT** — this is process registration, not a constraint amendment |
| New process/constraint rows in root README §9 | Owner | **NONE PROPOSED** — §2 S5 |

## 8. Target folder structure and migration cost

- Scope: 23 folders; per-file placement (root / `core/` / portal) as implemented by the
  migration mapping. Gateway files that stay at folder root: section `README.md` (23),
  plus `business-rules.md`, `requirements-overview.md`, `acceptance-criteria.md`,
  `architecture-decisions-reference.md`, `risk-register.md`, `decision-log.md`,
  `terminology.md`, `naming-conventions.md`.

| Folder | Root (stays) | core/ | admin/ | vendor/ | customer/ | delivery/ | Moved |
|---|---:|---:|---:|---:|---:|---:|---:|
| `docs/01-business-analysis/` | 4 | 50 | 67 | 34 | 63 | 13 | 229 |
| `docs/02-requirements/` | 8 | 68 | 0 | 0 | 0 | 0 | 73 |
| `docs/03-system-analysis/` | 1 | 10 | 0 | 0 | 0 | 0 | 10 |
| `docs/04-architecture/` | 2 | 8 | 0 | 0 | 0 | 0 | 8 |
| `docs/05-frontend/` | 1 | 8 | 0 | 0 | 0 | 0 | 8 |
| `docs/06-backend/` | 1 | 8 | 0 | 0 | 0 | 0 | 8 |
| `docs/07-api/` | 2 | 14 | 1 | 0 | 1 | 1 | 18 |
| `docs/08-database/` | 2 | 23 | 0 | 0 | 0 | 0 | 24 |
| `docs/09-security/` | 1 | 7 | 0 | 0 | 0 | 0 | 7 |
| `docs/10-integrations/` | 1 | 8 | 0 | 0 | 0 | 0 | 8 |
| `docs/11-ui-ux/` | 1 | 7 | 0 | 0 | 0 | 0 | 7 |
| `docs/12-non-functional/` | 1 | 8 | 0 | 0 | 0 | 0 | 8 |
| `docs/13-testing/` | 2 | 118 | 0 | 0 | 0 | 0 | 119 |
| `docs/14-devops-infrastructure/` | 1 | 7 | 0 | 0 | 0 | 0 | 7 |
| `docs/15-deployment/` | 1 | 5 | 0 | 0 | 0 | 0 | 5 |
| `docs/16-data/` | 1 | 6 | 0 | 0 | 0 | 0 | 6 |
| `docs/17-risk-management/` | 2 | 2 | 0 | 0 | 0 | 0 | 2 |
| `docs/18-decisions/` | 2 | 10 | 0 | 0 | 0 | 0 | 10 |
| `docs/19-traceability/` | 1 | 2 | 0 | 0 | 0 | 0 | 2 |
| `docs/20-validation/` | 1 | 7 | 0 | 0 | 0 | 0 | 7 |
| `docs/21-completion/` | 1 | 7 | 0 | 0 | 0 | 0 | 7 |
| `docs/22-glossary/` | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| `docs/23-templates/` | 1 | 10 | 0 | 0 | 0 | 0 | 10 |
| **Total (23 folders)** | **41** | **393** | **68** | **34** | **64** | **14** | **583** |

- **Migration cost (scripted dry-run measured before this artifact):** 583 of 614 files move;
  **355 markdown links** + **1 directory link** + **1,525 backticked path tokens** rewritten
  across the corpus in the same change set, plus this artifact's own citations. Acceptance
  bar: `python tools/check_citations.py` → **0 problems** after each folder group
  (`prompt-011.md` §4.5).

## 9. Evaluation (phase b) — accept / reject / defer per proposal row

| § | Proposal rows | Disposition | Governing rule |
|---|---|---|---|
| §3 | Working interpretation (23 folders, 00/phases/sessions excluded, gateway-at-root rule) | **ACCEPT** | Owner directive (`prompt-011.md` §1); interpretation stated explicitly as required; `GEN-03` |
| §4 | UC allocation `UC-211…420` (5 portal ranges, 210 rows) | **ACCEPT** — register in `naming-conventions.md` before minting | `SPE-03` (allocation-before-mint), root README §5 |
| §4 | All 210 UC rows | **ACCEPT** — each row: source document present; duplicate-checked against `DOC-UC-000` §2 and the §5.1 PENDING list (per-portal QC notes quoted above); actor/portal/block consistent; no row anticipates a PENDING item | `AUD-04` (derived from existing corpus), `SPE-03`; QC evidence per portal |
| §5 | 12 deltas (5 requirements + 7 BRs) | **ACCEPT** — exact source path + line/section per row; related-ID chains verified against the registers | `AUD-04`/`SPE-03` (source document or owner approval — these carry sources) |
| §6 | 6 deferred candidates (support SLAs, webhook replay, MFA step-up, ERP/finance FR-021+, `C-27`, loyalty/commission) | **DEFER** — sponsor/ADR/GAP-gated; each row names its blocker | `D-02` wave discipline, `AUD-04`, `GAP-04/05/06`, `SEC-012` (ADR first) |
| §7 | `C-27` candidate + `YUMN_RULES` rule-text changes | **DEFER** ("propose, defer") | Owner-locked register; `core/00` §0.5 route |
| §7 | Path-scheme + allocation registration; `YUMN_RULES` path realignment | **ACCEPT** (factual/process; no pin move) | Root README §9 unchanged; session 005/008 factual-correction precedent |
| — | Rejected rows | **NONE** — no proposal row was rejected; every non-accepted row is deferred with its blocker named | Silence is not an option (`prompt-011.md` §4.3) |

**Owner-target honesty:** the derived inventory after minting must read **420 UC files,
contiguous `UC-001…420`**; until the mint + matrix re-run lands, the owner figure
("over 400") stays marked `INSUFFICIENT EVIDENCE`.

### 9.7 Consolidated PENDING list (stays un-minted / un-implemented)

1. **18-item UC backlog** (`DOC-UC-000` §5.1): FX rates, Al-Kuraimi/Jeeb rails, email login,
   escrow-maturity vendor note, flags console, departments UI, invoices, provider registry,
   wishlist, calendar, search-analytics UI, engagement stats, PWA install, analytics UI,
   cart abandonment, re-open support ticket, moderator audit-log access, vendor right-of-reply.
2. **§6 deferred deltas (6):** support severity SLAs, webhook replay window/nonce store,
   MFA/step-up decision, ERP/finance department surface (`FR-021+`), `C-27` elevation,
   loyalty/tiered commission/cash-out.
3. **§7 deferred rule changes:** `YUMN_RULES.md` rule-text additions (route: `core/00` §0.5).
4. **Unchanged open regardless:** Gate 0 `FAIL`; `SEC-001…015` open; citation-CI run
   `UNVERIFIED`; `origin/master` deletion pending; 9 FAIL checks in the 31-check sweep.

## 10. Acceptance criteria for the implementation phases

1. Change control (phase 4) lands **before** any file moves or ID minting: `naming-conventions.md`
   (allocation + folder-path scheme row), `terminology.md`, `use-case-template.md` (file
   location), root `docs/README.md` §5/§9 — version bump + CH row each.
2. Migration (phase 5) runs folder-group by folder-group; **both gates green after each group**
   (`validate.py` PASS; `check_citations.py` 0 problems).
3. UC minting (phase 6): 210 files, template v1.2 verbatim, IDs contiguous `UC-211…420`,
   disjoint subagent waves, orchestrator re-verifies counts/IDs/spot-reads.
4. Registry propagation (phases 7–8): indexes, matrices, dashboards, count consumers
   (grep `210` / old paths repo-wide; history rows in 20-/21- CH excepted).
5. Phase 9 full gate set: 31-check sweep, validator, citation check, `gitleaks dir` + `gitleaks git`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial publication: proposal (S1–S8, working interpretation, 210 UC rows `UC-211…420`, 12 deltas, 6 deferred, constraint/rule proposals) + evaluation (§9) + placement/cost table (§8) authored as one versioned artifact | Session 011 owner directive (`prompt-011.md` §1), phases 2–3; `DOC-OVR-012` registered in `00-project-overview/README.md` |
