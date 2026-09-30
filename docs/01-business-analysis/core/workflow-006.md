---
document_id: DOC-WF-007
title: "WF-006 — Escrow: DELIVERED → 7-Day Hold → COMPLETED → Commission → Payout"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-014, FR-018, FR-020]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-006 — Escrow: DELIVERED → 7-Day Hold → COMPLETED → Commission → Payout

| Field | Value |
|---|---|
| **Trigger** | Sub-order reaches `DELIVERED` (WF-005) and the 7-day hold window elapses |
| **Actors** | System (`ACT-07` — escrow engine, commission, batches), Finance/Admin (`ACT-04`/`ACT-05` — oversight), Vendor (`ACT-02` — recipient) |
| **Blocks** | B07 Payment & Wallet (escrow, commission, payouts) · B06 Order Management · B11 Analytics (statements) |
| **Preconditions** | `DELIVERED` with valid proof; vendor KYC = APPROVED and store not suspended for payout |
| **Final state** | Sub-order `COMPLETED`; commission booked; vendor payable credited; payout batched/executed (≥1,000 YER) or rolled over |

```text
[DELIVERED] ── hold clock starts ──► 7 days ──► release check ──► all conditions true ──► commission computed
                   │                                  │
                   │ active dispute / state in        │ any condition false
                   │ {DISPUTED, RETURN_*, REFUNDED}   ▼
                   │                          ✗ HOLD (no release — BR-ESC-02)
                   ▼                                         │
            day 3–7: buyer may open return (WF-007)           │ conditions met later
            or dispute (WF-008) → freeze                     ▼
                                                    [COMPLETED] + vendor payable credited
                                                               │
                                                               ▼
                                              batch in 3–7 business days (min 1,000 YER)
                                              KYC + store gate ──► ✗ payout withheld (BR-ESC-06)
                                                               │
                                                               ▼
                                                    [PAYOUT EXECUTED] + monthly statement (BR-FIN-04)
                                                               │ refund after release
                                                               ▼
                                                    proportional commission reversal (BR-ESC-04)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | System | Start 7-day escrow hold on `DELIVERED` | B07 | `BR-ESC-01`, `C-12` | escrow hold row (release-eligible at T+7d) | Hold period is platform config with 7-day default (`ASM-09`) |
| 2 | System | Daily release evaluation job | B07 | `BR-ESC-02` | eligibility flags | Not eligible if: <7 days, active dispute, or state ∈ {DISPUTED, RETURN_*, REFUNDED} → no release |
| 3 | System | Advance sub-order `DELIVERED → COMPLETED` when eligible | B06 | `BR-ORD-01`, `BR-ORD-07` | state + history row | Master `COMPLETED` only when all sub-orders are `COMPLETED` or `REFUNDED` |
| 4 | System | Compute commission at release | B07 | `BR-ESC-03` | commission entry = line subtotal after coupon discount × tier rate (5–20%, default 10%) | Rate comes from vendor tier config; default 10% |
| 5 | System | Credit vendor payable (double-entry) | B07 | `BR-PAY-06`, `BR-FIN-05` | balanced ledger rows; rounding diffs → platform rounding account | Ledger never updated in place — corrections are compensating entries (`DATA-REQ-007`) |
| 6 | System | Add payable to payout batch (3–7 business days) | B07 | `BR-ESC-05` | batch rows | Amount < 1,000 YER → rolls over to next batch (`BR-ESC-05`) |
| 7 | System | Gate payout: KYC approved + store not suspended | B07, B03 | `BR-ESC-06` | hold flags | Failed gate → payout withheld pending review; notice to vendor |
| 8 | System | Execute payout | B07 | `BR-ESC-05`, `BR-PAY-06` | payout transactions + ledger | Provider/batch failure → retry ×3 then DLQ + alert (`BR-PLT-02`) |
| 9 | System | Reconcile daily; issue monthly statement | B07, B11 | `BR-ESC-08`, `BR-FIN-03`, `BR-FIN-04` | reconciliation report, statements | Σ ledger must balance; wallet+escrow+payable = provider statements; mismatch → alert finance, never auto-fix |
| 10 | System | Handle post-release refund (if return/dispute resolves later) | B07 | `BR-ESC-04`, `BR-ESC-07` | proportional commission reversal | Refund draws escrow first, then vendor payable (`BR-ESC-07`) |

**Alternatives**
- **Dispute before release:** freeze per sub-order only; other sub-orders settle normally (`BR-ORD-05`, WF-008).
- **Return opened in-window:** state moves to `RETURN_*` → release blocked (`BR-ESC-02`), WF-007 takes over.
- **Tiered commission:** rate per vendor tier 5–20%; blended take rate reported via `FR-018` dashboards.

**Exceptions**
- Clock/job failure → no release happens (release is a positive check, never implicit); DLQ alert (`BR-PLT-02`).
- Vendor suspended after release → already-executed payouts stand; future payouts held (`BR-VND-04`, `BR-ESC-06`).
- Reconciliation mismatch → finance alert + incident (`RISK-001` class); zero-imbalance is the acceptance bar (`AC-S-14`).
- Rounding: half-up to whole YER per sub-order; differences posted to platform rounding account (`BR-FIN-05`).

**Rules applied:** `BR-ESC-01…08`, `BR-FIN-03/04/05`, `BR-ORD-01/05/07`, `BR-PAY-06`, `BR-PLT-02`, `BR-VND-04` · Constraints: `C-10`, `C-12`.

**Data touched:** escrow holds, sub-order states + history, commission entries, vendor payables, payout batches/transactions, double-entry ledger (append-only), reconciliation reports, monthly statements.

**Systems:** B07 Payment & Wallet · B06 Order Management · B03 Store Management (KYC/suspension gates) · B11 Analytics & Reporting · BullMQ jobs (B13-configured).

**Final state:** sub-order `COMPLETED`, commission booked, vendor paid (or legitimately held/rolled over), ledger balanced, vendor informed via statement and notification.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
