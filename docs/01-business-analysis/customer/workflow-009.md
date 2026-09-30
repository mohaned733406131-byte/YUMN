---
document_id: DOC-WF-010
title: "WF-009 — Wallet Top-Up (m-Floos/OneCash Callback, Bank Transfer Admin Verification)"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-020]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-009 — Wallet Top-Up (m-Floos/OneCash Callback, Bank Transfer Admin Verification)

| Field | Value |
|---|---|
| **Trigger** | Customer initiates a top-up (directly or from WF-003's insufficient-balance branch) |
| **Actors** | Customer (`ACT-01`), System (`ACT-07` — provider adapter, reconciliation), Admin (`ACT-04` — bank verification), external provider |
| **Blocks** | B07 Payment & Wallet · B13 Admin · B10 Notifications · BullMQ jobs |
| **Preconditions** | Authenticated customer; wallet not frozen (`BR-PAY-09`); amount within 1,000–5,000,000 YER |
| **Final state** | Wallet credited with balanced double-entry ledger rows; or pending/failed top-up recorded; or admin-rejected with audit |

```text
[Choose method] ──┬── m-Floos / OneCash ──► initiate with provider ──► pending ──► provider callback / poll
                  │                                                     │                 │ verified
                  │                                                     │ provider        ▼
                  │                                                     │ error      credit wallet (BR-PAY-03)
                  │                                                     ▼                 │
                  │                                               ✗ retry ×3 → DLQ        ▼
                  │                                               + alert (BR-PLT-02)  ledger posted (BR-PAY-06)
                  │
                  └── bank transfer ──► customer pays bank ──► submits reference ──► PENDING ADMIN VERIFICATION
                                                                                        │
                                                         ┌──────────────────────────────┼──────────────────────┐
                                                         │ admin matches reference      │ mismatch              │ no response
                                                         ▼                              ▼                      ▼
                                                   credit wallet (BR-PAY-04)      ✗ REJECTED + audit      stays pending → reminder
                                                         │
                                                         ▼
                                              ledger posted → confirmation → usable for checkout (WF-003)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Customer | Choose method and amount | B07 | `BR-PAY-02`, `C-05` | top-up intent row | <1,000 or >5,000,000 YER → rejected; no method outside m-Floos/OneCash/bank transfer (`C-05`) |
| 2 | System | Check wallet status | B07 | `BR-PAY-09` | — | Frozen wallet cannot top up (refunds still allowed) |
| 3a | System | Initiate provider payment (wallet rails) | B07 adapter | `INT-REQ-001`, `BR-PAY-03` | provider reference, status = pending | Never credit on client claim — only verified callback/poll |
| 3b | Customer | Pay via bank and submit transfer reference | B07, B13 | `BR-PAY-04`, `INT-REQ-002` | reference, status = pending-verification | Reference required before admin review |
| 4 | System | Receive callback / poll reconciliation | B07 | `BR-PAY-03`, `BR-PAY-08` | status → verified | Duplicate callback → idempotent single credit (`BR-PAY-08`) |
| 5 | Admin | Verify bank reference against statement | B13 | `BR-PAY-04`, `BR-PLT-06` | decision + audit entry | Mismatch → reject with reason + audit; no credit |
| 6 | System | Credit wallet atomically | B07 | `BR-PAY-05`, `BR-PAY-06` | balance += amount; balanced ledger rows (append-only) | Balance check under row-level lock; ledger imbalance impossible (`AC-S-14`) |
| 7 | System | Format confirmation | B07, B10 | `BR-PAY-10`, `BR-NTF-04` | notification rows | Integer YER stored; `ar-YE` display with Arabic-Indic numerals |
| 8 | System | Retry/DLQ handling on provider failure | jobs | `BR-PLT-01/02` | job records, DLQ depth | 3 retries × exponential backoff → DLQ → alert (`BR-PLT-02`) |
| 9 | System | Daily reconciliation vs provider statements | B07 | `BR-ESC-08`, `BR-FIN-03` | reconciliation report | Mismatch alerts finance — never auto-adjusts money |

**Alternatives**
- **Return to checkout:** credited balance immediately usable in WF-003 step 5 (same session resume).
- **Provider outage:** pending top-ups remain pending; fallback funding path is bank transfer (`C-05`).
- **Insufficient bank proof / suspected fraud:** Admin rejects + audit; support ticket path (`FR-020`).

**Exceptions**
- Forged callback → signature/verification of provider callback required (`INT-REQ-006` signed webhooks, idempotent handlers).
- Amount out of bounds at any step → rejected (`BR-PAY-02`).
- Negative/zero amount or float amounts → rejected; amounts stored as integer YER (`BR-PAY-10`).
- Client claims success but no callback → no credit (`BR-PAY-03` — never trust client claim).

**Rules applied:** `BR-PAY-02/03/04/05/06/08/09/10`, `BR-ESC-08`, `BR-FIN-03`, `BR-PLT-01/02/06` · Constraints: `C-05`, `C-01` · Integrations: `INT-REQ-001`, `INT-REQ-002`, `INT-REQ-006`.

**Data touched:** top-up intents, provider references/callbacks, wallet balances, double-entry ledger (append-only), admin decision + audit rows, reconciliation reports, job/DLQ records.

**Systems:** B07 Payment & Wallet · provider adapters (m-Floos, OneCash) · B13 Platform Administration · B10 Notifications · BullMQ (reconciliation, retries).

**Final state:** wallet balance increased and ledger balanced; customer notified; top-up visible in wallet history — or a recorded, audited rejection/pending state with clear customer messaging.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
