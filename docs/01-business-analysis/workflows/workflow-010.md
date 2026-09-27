---
document_id: DOC-WF-011
title: "WF-010 — Cancellation (Customer Pre-Dispatch) → Refund"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-005, FR-012, FR-013, FR-017]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-010 — Cancellation (Customer Pre-Dispatch) → Refund

| Field | Value |
|---|---|
| **Trigger** | Customer requests cancellation of their order while still pre-dispatch |
| **Actors** | Customer (`ACT-01`), System (`ACT-07` — guards, stock restore, refund), Vendor (`ACT-02`) / Admin (`ACT-04`) as alternative cancellers |
| **Blocks** | B06 Order Management · B02 Inventory · B07 Payment & Wallet · B10 Notifications · B13 Admin |
| **Preconditions** | Order in `PLACED` or `CONFIRMED` for the buyer (vendor/admin until `READY_FOR_PICKUP`); wallet-funded payment exists |
| **Final state** | Sub-order(s) `CANCELLED` → `REFUNDED`; stock restored; escrow unwound; wallet credited |

```text
[Customer taps Cancel]
        │
        ▼
state guard check ──► PLACED or CONFIRMED? ──yes──► cancel sub-order(s) ──► [CANCELLED] (actor+reason recorded)
        │                      │ no (PROCESSING by vendor/admin ok until READY_FOR_PICKUP)
        │                      │ READY_FOR_PICKUP or later
        │                      ▼
        │               ✗ REJECTED — dispatch window closed (BR-ORD-04) → 409 STATE_CONFLICT
        ▼
 stock: restore reserved/deducted quantity (BR-CAT-07, FR-005)
        │
        ▼
 escrow: unwind hold ──► refund: credit wallet (BR-PAY-07) with idempotency key (BR-PAY-08)
        │
        ▼
 [REFUNDED] ──► notifications to buyer + vendor (BR-NTF-04) ──► audit entry (BR-PLT-06)
        │
        └── duplicate cancel/refund taps ──► idempotent no-op, original outcome returned
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Customer | Request cancellation with reason | B06 | `BR-ORD-04` | cancellation request | Allowed only in `PLACED`/`CONFIRMED` (buyer) |
| 2 | System | Evaluate guard inside order transaction | B06 | `BR-ORD-04`, `C-09` | — | Vendor/Admin may cancel until `READY_FOR_PICKUP`; later → `409 STATE_CONFLICT` |
| 3 | System | Write `CANCELLED` with actor, timestamp, reason | B06 | `BR-ORD-03` | state + append-only history row | History never overwritten |
| 4 | System | Restore stock | B02 | `BR-CAT-07`, `FR-005` | stock incremented | Restoration is atomic; mirrors the deduction made at `PLACED` (`C-13`) |
| 5 | System | Unwind escrow hold for affected sub-orders | B07 | `BR-ESC-07`, `C-12` | escrow released back to refund pool | Multi-vendor: cancel per sub-order or whole order — master aggregates (`BR-ORD-02`) |
| 6 | System | Credit wallet with idempotency key | B07 | `BR-PAY-06/07/08`, `BR-PLT-03` | balanced ledger credit | Never external cash-out — wallet only (`BR-PAY-07`); frozen wallet still receives refund (`BR-PAY-09`) |
| 7 | System | Advance `CANCELLED → REFUNDED` | B06 | `BR-ORD-01` | state + history | Refund execution completes the money-back terminal state |
| 8 | System | Notify buyer and vendor | B10 | `BR-NTF-04/05` | notification rows | Arabic/English templates; status notices always delivered |
| 9 | System | Audit the money movement | B07 | `BR-PLT-06`, `SEC-REQ-010` | audit entry (actor, action, before/after) | Append-only, tamper-evident |

**Alternatives**
- **Vendor cancels** (out of stock, unable to fulfill): same guards (pre-`READY_FOR_PICKUP`) → same refund path (`BR-ORD-04`).
- **Admin cancels** (ops decision): same path + audit; used in escalation resolutions (`BR-ORD-10`).
- **Auto-escalation instead of silent cancel:** stale unconfirmed orders escalate to admin review first — never auto-cancel without notification (`BR-ORD-10`).

**Exceptions**
- Race: cancel vs courier assignment → guards evaluated in-transaction; cancel wins only pre-`READY_FOR_PICKUP` (`state-transitions.md` §5).
- Duplicate refund taps → idempotency key, ledger posts once (`BR-PAY-08`, `BR-PLT-03`).
- Cancel attempted after dispatch → rejected; customer must use return flow (WF-007) after delivery.
- Partial-vendor cancel → only that sub-order cancels; master completes when all sub-orders settle (`BR-ORD-07`).

**Rules applied:** `BR-ORD-01/02/03/04/07/10`, `BR-CAT-07`, `BR-PAY-06/07/08/09`, `BR-ESC-07`, `BR-NTF-04/05`, `BR-PLT-03/06` · Constraints: `C-09`, `C-10`, `C-12`, `C-13`.

**Data touched:** sub-order states + history, stock levels, escrow holds, wallet ledger (credit), notifications, audit log.

**Systems:** B06 Order Management · B02 Product Catalog · B07 Payment & Wallet · B10 Notifications · B13 Platform Administration.

**Final state:** order `CANCELLED → REFUNDED`, wallet credited the paid amount, stock restored, escrow unwound, both parties notified, full audit trail present.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
