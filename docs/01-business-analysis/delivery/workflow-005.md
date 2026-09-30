---
document_id: DOC-WF-006
title: "WF-005 — Courier Assignment → Pickup → Transit → Delivery Code → DELIVERED"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-012, FR-015, FR-017]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-005 — Courier Assignment → Pickup → Transit → Delivery Code → DELIVERED

| Field | Value |
|---|---|
| **Trigger** | Sub-order reaches `READY_FOR_PICKUP` and a delivery offer is published (WF-004) |
| **Actors** | Delivery Provider (`ACT-03`), Customer (`ACT-01` — shares code), System (`ACT-07` — verification, timers, escalation), Admin (`ACT-04` — escalation receiver) |
| **Blocks** | B08 Shipping & Delivery · B06 Order Management · B10 Notifications · B13 Admin |
| **Preconditions** | Package ready; domestic Yemen address in a covered zone; **no GPS is ever requested or stored** (`C-16`) |
| **Final state** | Sub-order `DELIVERED` (proof: code + timestamp + courier identity) → escrow 7-day hold starts (WF-006); or 24 h confirmation lock + support ticket |

```text
[READY_FOR_PICKUP] ── offer same-zone couriers, first accept wins ──► [ASSIGNED]
       ▲                              │ another courier accepts second → ✗ rejected (optimistic lock, BR-SHP-04)
       │ courier releases             ▼
       └──────────────────── [ASSIGNED] ── pickup confirmed ──► [PICKED_UP] ── departure ──► [IN_TRANSIT]
                                                                        │
                                                                        ▼
                                              [OUT_FOR_DELIVERY] ── 6-digit code issued to buyer (BR-SHP-02)
                                                                        │
                                              ┌─────────────────────────┼──────────────────────────┐
                                              │ courier enters code     │ wrong (1st/2nd)          │ wrong (3rd)
                                              ▼                         ▼                          ▼
                                       code verified → [DELIVERED]   show attempts,            ✗ 24 h lock +
                                       (attempts < 3)                 back to [IN_TRANSIT]       support ticket (BR-SHP-03)
                                                                        (attempt < 3)             + admin review (BR-SHP-06)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | System | Offer delivery to eligible couriers in the same zone | B08 | `BR-SHP-04` | delivery offer rows | Eligibility = same zone; offer visible to multiple couriers |
| 2 | Delivery Provider | Accept the offer | B08 | `BR-SHP-04` | state → `ASSIGNED`, courier_id set | First accept wins via optimistic locking — second accept → `409`, no double assignment |
| 3 | Delivery Provider | Confirm physical pickup | B08 | `BR-ORD-03` | state → `PICKED_UP`, history row | No GPS/location check — identity + timestamp only (`BR-SHP-05`) |
| 4 | Delivery Provider | Departure scan | B08 | `BR-ORD-03` | state → `IN_TRANSIT` | Release assignment → back to `READY_FOR_PICKUP` (`state-transitions.md`) |
| 5 | Delivery Provider | Start final leg | B08 | `BR-SHP-02` | state → `OUT_FOR_DELIVERY`; **6-digit code issued to buyer** | Code delivered via notification channel(s) (`BR-NTF-04`); code is buyer-shared secret |
| 6 | Customer | Shares code with courier | — | `BR-SHP-02`, `C-16` | none | Customer absence → courier retry later (attempt not consumed unless a code is entered) |
| 7 | Delivery Provider | Enter code | B08 | `BR-ORD-08`, `BR-SHP-03` | attempt counter | Correct + attempts < 3 → `DELIVERED`; wrong 1st/2nd → show remaining attempts, sub-order returns to `IN_TRANSIT` |
| 8 | System | 3rd failure | B08, B13 | `BR-SHP-03`, `BR-SHP-06` | lock until now+24 h, auto support ticket, escalation record | Confirmation locked 24 h; ticket auto-created; admin review with full timeline |
| 9 | System | On `DELIVERED`: start escrow hold, notify parties | B07, B10 | `BR-ESC-01`, `BR-NTF-04` | escrow hold start timestamp (7 days) | Escrow clock drives WF-006; delivery proof = code + timestamp + courier identity (`BR-SHP-07`) |
| 10 | System | Attempt counter reset/timeout handling | B08 | `BR-SHP-03` | attempt state | After the 24 h lock expires, confirmation is allowed again; repeated pattern still routes to admin review (`BR-SHP-06`) |

**Alternatives**
- **Multiple sub-orders:** each sub-order runs its own assignment/delivery track; master completes only when all sub-orders settle (`BR-ORD-07`, `C-10`).
- **Optional photo proof:** courier may attach a photo — stored but never required (`BR-SHP-07`).
- **Admin dispatch assist:** Admin can view all deliveries and release assignments (`actors-and-roles.md` permission matrix).

**Exceptions**
- No courier accepts → sub-order remains `READY_FOR_PICKUP`; ops escalation via admin dispatch view (no canon SLA value — `INSUFFICIENT EVIDENCE`).
- Fraudulent code guessing → exactly 3 attempts, then 24 h lock (`BR-SHP-03`, `SEC-REQ-005`).
- Requesting GPS → forbidden by design (`BR-SHP-05`, `C-16`); no location API exists in the contract.
- Reaching `DELIVERED` without a verified code → forbidden (`BR-ORD-08`, `C-16`); covered by the constraint test suite (`../../13-testing/core/testing-strategy.md`).

**Rules applied:** `BR-SHP-02…07`, `BR-ORD-03/07/08`, `BR-ESC-01`, `BR-NTF-04`, `BR-PLT-06` · Constraints: `C-10`, `C-16`, `C-17` · Security: `SEC-REQ-005`.

**Data touched:** shipments/assignments, order states + history, delivery code (hashed), attempt counters, lock records, support tickets, escrow hold start, notifications.

**Systems:** B08 Shipping & Delivery · B06 Order Management · B07 Payment & Wallet (escrow trigger) · B10 Notifications · B13 Platform Administration.

**Final state:** sub-order `DELIVERED` with verifiable proof; buyer/vendor notified; 7-day escrow hold clock started (state machine: `DELIVERED → COMPLETED` only after hold + no dispute, WF-006).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
