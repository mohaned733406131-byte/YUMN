---
document_id: DOC-WF-005
title: "WF-004 — Vendor Order Acceptance → Fulfillment → READY_FOR_PICKUP"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-005, FR-012, FR-017]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-004 — Vendor Order Acceptance → Fulfillment → READY_FOR_PICKUP

| Field | Value |
|---|---|
| **Trigger** | Vendor sub-order(s) reach `PLACED` after successful wallet payment (WF-003) |
| **Actors** | Vendor (`ACT-02`), System (`ACT-07` — SLA timer, notifications), Admin (`ACT-04` — escalation receiver) |
| **Blocks** | B06 Order Management · B02 Inventory · B10 Notifications · B13 Admin (escalation queue) |
| **Preconditions** | Vendor KYC = APPROVED, store active; stock already deducted at `PLACED` |
| **Final state** | Sub-order `READY_FOR_PICKUP`, awaiting courier offer (WF-005) |

```text
[PLACED] ── vendor notified ──► accept? ──yes──► [CONFIRMED] ── start packing ──► [PROCESSING]
              │                     │                      │                            │
              │                     │ no response ≥24 h     │ decline/unable              │ pack complete
              │                     ▼                      ▼                            ▼
              │            ✗ auto-escalate to admin   cancellation path            [READY_FOR_PICKUP]
              │              (BR-ORD-10, never silent)  (BR-ORD-04, WF-010)                │
              │                     │                                                 courier offer (BR-SHP-04)
              ▼                     ▼                                                       │
     store suspended? ──yes──► ✗ new orders blocked, existing frozen (BR-VND-04)            ▼
              │ no                                                          WF-005 assignment
              ▼
        timeline appended at every transition (BR-ORD-03), notifications fanned out (BR-NTF-04)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | System | Notify vendor of new sub-order; start 24 h SLA timer | B06, B10 | `BR-ORD-10`, `BR-NTF-04` | SLA deadline, notification rows | Store suspended → new orders blocked, existing frozen (`BR-VND-04`) |
| 2 | Vendor | Accept sub-order | B06 | `BR-ORD-04`, `BR-VND-07` | state → `CONFIRMED`, history row (actor, time) | Only own `store_id` sub-orders visible/denied cross-store (`BR-VND-07`); invalid transition → `409 STATE_CONFLICT` |
| 3 | Vendor | Begin packing | B06 | `BR-ORD-03` | state → `PROCESSING`, history row | Stock was already deducted at `PLACED` — no second deduction (`BR-CAT-07`, `C-13`) |
| 4 | Vendor | Complete packing | B06 | `BR-ORD-03` | state → `READY_FOR_PICKUP`, history row | Partial fulfillment not permitted — sub-order moves as a unit (`BR-ORD-07`) |
| 5 | System | Close SLA timer; offer delivery to zone couriers | B08 | `BR-SHP-04` | delivery offer (first accept wins) | Offer continues in WF-005 |
| 6 | System | Fan out status notifications to buyer | B10 | `BR-NTF-04`, `BR-NTF-05` | notification queue | Marketing opt-out never suppresses order status notices |
| 7 | System (watcher) | Detect vendor silence at 24 h from `CONFIRMED` | B06, B13 | `BR-ORD-10` | escalation ticket, audit entry | Escalates to admin review **with notification — never silent auto-cancel** |
| 8 | Admin | Resolve escalation (chase vendor, cancel, or reassign) | B13 | `BR-ORD-04`, `BR-PLT-06` | state change or ticket resolution | Cancel before dispatch → WF-010 refund path |

**Alternatives**
- **Auto-accept configuration:** System may auto-advance `PLACED → CONFIRMED` when a vendor enables it (`state-transitions.md` transition table) — same guards apply.
- **Vendor decline:** treated as cancellation intent → guard checked (pre-`READY_FOR_PICKUP`) → WF-010.
- **Vendor staff:** Editor/Manager roles may process orders per store permissions; only Owner manages staff (`BR-VND-06`).

**Exceptions**
- Suspension mid-fulfillment → existing orders frozen, new orders blocked (`BR-VND-04`); Admin decides on frozen orders.
- Race: customer cancels while vendor confirms → guards evaluated inside the order transaction; cancel wins only pre-`READY_FOR_PICKUP` (`state-transitions.md` §5).
- Vendor attempts to skip states (e.g. `PLACED → READY_FOR_PICKUP`) → forbidden (state machine, `BR-ORD-01`).
- Duplicate vendor action (double-tap accept) → idempotent: history is append-only, transition no-ops (`BR-ORD-03`).

**Rules applied:** `BR-ORD-01/03/04/07/09/10`, `BR-CAT-07`, `BR-VND-04/06/07`, `BR-SHP-04`, `BR-NTF-04/05`, `BR-PLT-06` · Constraints: `C-09`, `C-10`, `C-13`.

**Data touched:** sub-orders (state), order_status_history (append-only), SLA timers, notifications, escalation tickets, audit log.

**Systems:** B06 Order Management · B02 Product Catalog (stock already settled) · B08 Shipping (offer) · B10 Notifications · B13 Platform Administration.

**Final state:** sub-order `READY_FOR_PICKUP` with a complete history trail and delivery offer published to eligible same-zone couriers.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
