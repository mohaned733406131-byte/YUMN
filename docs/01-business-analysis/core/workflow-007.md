---
document_id: DOC-WF-008
title: "WF-007 — Return Request → Approval → Pickup → Inspection → REFUNDED"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-016, FR-012, FR-017]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-007 — Return Request → Approval → Pickup → Inspection → REFUNDED

| Field | Value |
|---|---|
| **Trigger** | Buyer requests a return for a delivered item inside the merchant return policy window |
| **Actors** | Customer (`ACT-01`), Vendor (`ACT-02`), Delivery Provider (`ACT-03` — return pickup), Admin (`ACT-04` — arbitration), System (`ACT-07` — timers, auto-approve, refund) |
| **Blocks** | B09 Returns & Refunds · B06 Orders · B08 Shipping · B07 Payment & Wallet · B10 Notifications |
| **Preconditions** | Sub-order `DELIVERED` or `COMPLETED`; `isReturnable = true`; now ≤ delivery confirmation + `returnPeriodDays` |
| **Final state** | `REFUNDED` — wallet credited (item value; shipping only on platform/vendor fault) with proportional commission reversal; or `RETURN_REJECTED` → `COMPLETED` |

```text
[DELIVERED / COMPLETED] ── buyer opens return ──► policy check ──► ok ──► [RETURN_REQUESTED]
        │                                   │ not returnable / window elapsed
        │                                   ▼
        │                            ✗ REJECTED AT SUBMISSION (BR-RET-01)
        ▼
[RETURN_REQUESTED] ── vendor/admin decides ──► approve ──► [RETURN_APPROVED] ── courier pickup + vendor receipt ──► [RETURN_RECEIVED]
        │                                        │ reject with reason                    │
        │                                        ▼                                       ▼ inspection ≤72 h
        │                                 [RETURN_REJECTED] ──► [COMPLETED]        pass or 72 h timeout (BR-RET-05)
        │                                                        ▲                       │
        │                                                        │                       ▼
        └── policy vs dispute conflict ──► Admin final arbiter ───┘                wallet credit ≤3 business days
             (BR-RET-06, audited)                                                  [REFUNDED] (BR-RET-04)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Customer | Open return request with reason | B09 | `BR-RET-01`, `C-11` | return request row | `isReturnable = false` or window elapsed → rejected at submission (`BR-RET-01`) |
| 2 | System | Validate window = delivery confirmation + `returnPeriodDays` | B09, B06 | `BR-RET-01` | window check result | Window computed from delivery confirmation, not order date |
| 3 | Vendor / Admin | Approve or reject with reason | B09 | `BR-RET-02`, `BR-ORD-03` | state → `RETURN_APPROVED` or `RETURN_REJECTED` + history | Rejection → `RETURN_REJECTED`, later finalizes to `COMPLETED` with notification |
| 4 | System | Schedule return pickup (courier) | B08 | `BR-SHP-04` | return shipment/assignment | Same zone offer mechanics as outbound (`BR-SHP-04`) |
| 5 | Delivery Provider | Pick up and vendor receives item | B09, B08 | `BR-RET-02` | state → `RETURN_RECEIVED` | Custody recorded via courier identity + timestamp (no GPS, `C-16`) |
| 6 | Vendor | Inspect item | B09 | `BR-RET-05` | inspection result | **Must conclude ≤72 h — otherwise return auto-approves** (`BR-RET-05`) |
| 7 | System | Execute refund: item value (+ shipping if platform/vendor fault) | B07 | `BR-RET-03`, `BR-PAY-07` | state → `REFUNDED`; wallet credit initiated | Shipping refunded only when fault is platform/vendor-side (`BR-RET-03`) |
| 8 | System | Credit customer wallet ≤3 business days | B07 | `BR-RET-04`, `BR-PAY-06/08` | double-entry ledger rows | Idempotent — double refund attempts no-op (`BR-PAY-08`); frozen wallets still receive refunds (`BR-PAY-09`) |
| 9 | System | Reverse commission proportionally; adjust escrow | B07 | `BR-RET-07`, `BR-ESC-04`, `BR-ESC-07` | commission reversal entries; escrow drawdown | Escrow first, then vendor payable if insufficient (`BR-ESC-07`) |
| 10 | System | Notify all parties | B10 | `BR-NTF-04`, `BR-NTF-05` | notification rows | Arabic/English templates; status notices always delivered |

**Alternatives**
- **Return opened after `COMPLETED` but still in window:** allowed (`state-transitions.md`: `COMPLETED → RETURN_REQUESTED` with `BR-RET-01` guard).
- **Buyer and vendor disagree:** Admin is final arbiter; decision written to audit log (`BR-RET-06`).
- **Dispute raised instead of clean return:** route to WF-008; escrow freezes, return flow paused per state guards.

**Exceptions**
- Inspection stalls past 72 h → auto-approve protects the buyer (`BR-RET-05`).
- Item not returned / pickup fails → remains `RETURN_APPROVED`/`RETURN_RECEIVED` pending ops handling (support ticket, `FR-020`); no canon SLA beyond 72 h inspection — `INSUFFICIENT EVIDENCE`.
- Refund after commission already released → proportional reversal (`BR-ESC-04`); if payable insufficient, vendor owes the difference (`BR-ESC-07`).
- Return outside policy claimed as dispute → `BR-RET-06` (admin arbiter) governs.

**Rules applied:** `BR-RET-01…07`, `BR-ESC-04/07`, `BR-PAY-06/07/08/09`, `BR-ORD-03`, `BR-SHP-04`, `BR-NTF-04/05` · Constraints: `C-11`, `C-16` · Related: `OBJ-02` (refund integrity).

**Data touched:** return requests, order states + history, inspection records (72 h timer), return shipments, wallet ledger (credit), commission reversals, escrow balance, audit entries, notifications.

**Systems:** B09 Returns & Refunds · B06 Order Management · B08 Shipping & Delivery · B07 Payment & Wallet · B10 Notifications · B13 Admin (arbitration).

**Final state:** `REFUNDED` with wallet credited within 3 business days, commission reversed proportionally, escrow adjusted, all parties notified — or `RETURN_REJECTED` finalized to `COMPLETED` with reason and notification.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
