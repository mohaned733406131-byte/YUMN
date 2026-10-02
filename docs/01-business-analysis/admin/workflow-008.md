---
document_id: DOC-WF-009
title: "WF-008 — Dispute → Escrow Freeze → Admin Resolution"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-012, FR-014, FR-020]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-008 — Dispute → Escrow Freeze → Admin Resolution

| Field | Value |
|---|---|
| **Trigger** | Buyer or vendor raises a dispute on a sub-order (before or after `COMPLETED`, per policy) |
| **Actors** | Customer (`ACT-01`) / Vendor (`ACT-02`) raise; Admin (`ACT-04`) resolves; System (`ACT-07` — freeze, timers, execution) |
| **Blocks** | B06 Order Management · B07 Payment & Wallet (escrow) · B13 Admin · B10 Notifications |
| **Preconditions** | Sub-order exists with settlement pending or settled within policy; evidence available from timeline + delivery proof |
| **Final state** | Resolved → `COMPLETED` (vendor wins) or `REFUNDED` (buyer wins), with mandatory audit entry; escrow released or unwound |

```text
[Raise dispute] ──► sub-order(s) → [DISPUTED] ──► escrow FROZEN (all affected sub-orders)
        │                  │                            │
        │ who: buyer or    │ cross-sub-order            │ release attempted meanwhile
        │ vendor           │ freeze scope: only         ▼
        │                  │ affected sub-orders     ✗ NO RELEASE (BR-ESC-02)
        ▼                  ▼
 evidence gathered: order timeline (BR-ORD-09), code proof (BR-SHP-07), notifications, ledger
        │
        ▼
 [Admin reviews] ──► resolution decision
        │                     │
        │                     ├── vendor wins ──► [COMPLETED] ──► escrow releases (WF-006)
        │                     └── buyer wins  ──► refund flow ──► [REFUNDED] (wallet credit)
        ▼
 audit entry required (actor, action, entity, before/after, IP, time) + notify both parties
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Customer / Vendor | Raise dispute with reason/evidence | B06 | `BR-ORD-05` | state → `DISPUTED`, dispute record | Raising is allowed pre-`COMPLETED` (and post-`COMPLETED` within policy per `state-transitions.md`) |
| 2 | System | Freeze escrow for affected sub-orders | B07 | `BR-ORD-05`, `BR-ESC-02` | escrow frozen flag | Freeze covers only affected sub-orders; unaffected sub-orders keep settling (`state-transitions.md` §4) |
| 3 | System | Block any release attempt while frozen | B07 | `BR-ESC-02` | release eligibility = false | Release is impossible until resolution — never partially released |
| 4 | System / Admin | Assemble evidence pack | B06, B08, B10 | `BR-ORD-09`, `BR-SHP-07` | evidence snapshot refs | Without GPS (`C-16`): proof = delivery code + timestamp + courier identity + timeline |
| 5 | Admin | Decide outcome | B13 | `BR-RET-06`, `BR-PLT-06` | decision row + audit entry | Admin is final arbiter where policy and dispute conflict; decision must be audited |
| 6a | System | Vendor wins → `COMPLETED`, release escrow | B06, B07 | `BR-ESC-02`, `BR-ORD-01` | state → `COMPLETED`; release resumes (WF-006) | Commission computed per `BR-ESC-03` as normal |
| 6b | System | Buyer wins → refund flow | B07, B06 | `BR-ESC-07`, `BR-PAY-07` | state → `REFUNDED`; wallet credit | Refund draws escrow first, then vendor payable if escrow insufficient (`BR-ESC-07`) |
| 7 | System | Reverse commission proportionally on buyer-win | B07 | `BR-ESC-04`, `BR-RET-07` | commission reversal entries | Post-release refunds reverse proportionally |
| 8 | System | Notify both parties; close dispute | B10 | `BR-NTF-04` | notification rows, dispute closed | Buyer/vend notice in user locale (Arabic default) |

**Alternatives**
- **Dispute during 7-day hold:** frozen hold simply extends — release gate re-evaluated after resolution.
- **Dispute after `COMPLETED` (post-release):** admin-only resolution path per `state-transitions.md`; refund recovers from payable (`BR-ESC-07`).
- **Parallel return:** a `RETURN_*` state also blocks release (`BR-ESC-02`); admin coordinates so both flows don't double-refund (idempotency, `BR-PAY-08`).

**Exceptions**
- Admin indecision → escrow stays frozen (safe default); no canon resolution SLA exists — `INSUFFICIENT EVIDENCE`, tracked as support/dispute ops metric (`BO-10`).
- Attempted release during freeze → rejected by gate (`BR-ESC-02`); zero such releases is acceptance criterion (`OBJ-02`).
- Unaudited resolution → forbidden (`BR-PLT-06`, `SEC-REQ-010`).
- Evidence tampering → history is append-only (`BR-ORD-03`); ledger append-only (`DATA-REQ-007`).

**Rules applied:** `BR-ORD-03/05/09`, `BR-ESC-02/04/07`, `BR-RET-06/07`, `BR-PAY-07/08`, `BR-SHP-07`, `BR-NTF-04`, `BR-PLT-06` · Constraints: `C-10`, `C-12`, `C-16`.

**Data touched:** sub-order states + history, dispute records, escrow freeze flags, evidence references, audit log, wallet ledger (on buyer-win), commission reversals, notifications.

**Systems:** B06 Order Management · B07 Payment & Wallet · B08 Shipping (proof) · B10 Notifications · B13 Platform Administration.

**Final state:** dispute closed with an audited decision; escrow either released (→ WF-006 payout) or consumed by refund (→ wallet credit); both parties notified.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
