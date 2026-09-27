---
document_id: DOC-SA-010
title: State Transitions — Canonical 17-State Order Machine
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-012, FR-015, FR-016]
related_documents: [DOC-OVR-008, DOC-BA-005]
---

# State Transitions — Order Lifecycle

**Single source of truth for the order state machine (C-09: exactly 17 states).** Every surface (customer, vendor, courier, admin), API transition guard, database check, and test uses this enumeration.

## 1. The 17 States (canonical enumeration)

| # | State | Category | Meaning |
|---|---|---|---|
| 1 | `PLACED` | Active | Order created; wallet debited; escrow funded; awaiting vendor confirmation |
| 2 | `CONFIRMED` | Active | Vendor accepted the sub-order(s) within SLA |
| 3 | `PROCESSING` | Active | Vendor is preparing/packing items |
| 4 | `READY_FOR_PICKUP` | Active | Package ready; awaiting courier |
| 5 | `ASSIGNED` | Active | Courier accepted the delivery assignment |
| 6 | `PICKED_UP` | Active | Courier physically has the package |
| 7 | `IN_TRANSIT` | Active | Moving between hubs / to destination zone |
| 8 | `OUT_FOR_DELIVERY` | Active | Courier en route to buyer; delivery code issued |
| 9 | `DELIVERED` | Settling | 6-digit code verified; escrow 7-day hold starts (BR-ESC-01) |
| 10 | `COMPLETED` | Terminal | Escrow released to vendor; all obligations done |
| 11 | `CANCELLED` | Terminal* | Order cancelled; refund flow triggered (→ REFUNDED) |
| 12 | `RETURN_REQUESTED` | Return | Buyer requested return inside policy window |
| 13 | `RETURN_APPROVED` | Return | Vendor/admin approved; pickup scheduled |
| 14 | `RETURN_REJECTED` | Return | Return denied (policy/inspection) |
| 15 | `RETURN_RECEIVED` | Return | Vendor received returned item; inspection due (72 h, BR-RET-05) |
| 16 | `REFUNDED` | Terminal | Wallet refund completed |
| 17 | `DISPUTED` | Exception | Escrow frozen; admin resolution in progress |

States 1–8 = **pre-delivery**; 9–10 = **settlement**; 11 = cancellation; 12–15 = return flow; 16 = money-back terminal; 17 = exception overlay.

## 2. Transition Table (authoritative)

| From | To | Trigger | Actor | Guards |
|---|---|---|---|---|
| PLACED | CONFIRMED | Vendor accepts | Vendor / System (auto-accept config) | Vendor KYC approved, store active |
| PLACED | CANCELLED | Buyer cancels | Customer | Within PLACED (BR-ORD-04) |
| CONFIRMED | PROCESSING | Vendor starts fulfillment | Vendor | — |
| CONFIRMED | CANCELLED | Cancel before dispatch | Customer / Vendor / Admin | Before READY_FOR_PICKUP (BR-ORD-04) |
| PROCESSING | READY_FOR_PICKUP | Pack complete | Vendor | Stock already deducted at PLACED |
| PROCESSING | CANCELLED | Admin/vendor cancel | Vendor / Admin | Pre-dispatch only |
| READY_FOR_PICKUP | ASSIGNED | Courier accepts | Delivery Provider | Same zone, first-accept wins (BR-SHP-04) |
| ASSIGNED | PICKED_UP | Pickup confirmed | Delivery Provider | — |
| ASSIGNED | READY_FOR_PICKUP | Courier releases assignment | Delivery Provider / Admin | — |
| PICKED_UP | IN_TRANSIT | Departure scan | Delivery Provider | — |
| IN_TRANSIT | OUT_FOR_DELIVERY | Final leg started | Delivery Provider | 6-digit code issued (BR-SHP-02) |
| OUT_FOR_DELIVERY | DELIVERED | Code verified | Delivery Provider (enter) + Customer (shares) | Code correct; attempts < 3 (BR-SHP-03) |
| OUT_FOR_DELIVERY | IN_TRANSIT | Failed attempt (returns to transit) | Delivery Provider | Attempt < 3; attempt count recorded |
| OUT_FOR_DELIVERY | (admin review) | 3rd failed attempt | System | Escalation, not a state — support ticket created (BR-SHP-06) |
| DELIVERED | COMPLETED | Escrow release after 7 days | System | No dispute; 7 days elapsed (BR-ESC-02) |
| DELIVERED | RETURN_REQUESTED | Buyer opens return | Customer | Within return window (BR-RET-01) |
| DELIVERED | DISPUTED | Buyer/vendor raises dispute | Customer / Vendor | Before COMPLETED; escrow frozen (BR-ORD-05) |
| COMPLETED | RETURN_REQUESTED | Late-window return | Customer | Still within return window (BR-RET-01) |
| COMPLETED | DISPUTED | Post-completion dispute | Customer / Vendor / Admin | Within policy; admin-only after release |
| RETURN_REQUESTED | RETURN_APPROVED | Approval | Vendor / Admin | Decision within 48 h SLA; auto-escalate to admin after 48 h |
| RETURN_REQUESTED | RETURN_REJECTED | Rejection | Vendor / Admin | Reason required |
| RETURN_APPROVED | RETURN_RECEIVED | Pickup + receipt | Delivery Provider / Vendor | — |
| RETURN_RECEIVED | REFUNDED | Inspection passed (or 72 h auto) | Vendor / System | Wallet credited ≤3 business days (BR-RET-04) |
| RETURN_REJECTED | COMPLETED | Rejection final | System | Notification sent |
| CANCELLED | REFUNDED | Refund execution | System | Wallet credited; escrow unwound |
| DISPUTED | COMPLETED | Resolved for vendor | Admin | Audit entry required |
| DISPUTED | REFUNDED | Resolved for buyer | Admin | Refund flow executes |
| REFUNDED | — | Terminal | — | — |

**Not permitted (explicitly forbidden):** skipping states; returning from DELIVERED to pre-delivery states; editing history rows (BR-ORD-03); reaching DELIVERED without code (BR-ORD-08, C-16); REFUNDED without corresponding ledger entries (BR-PAY-06).

## 3. Diagram

```text
PLACED → CONFIRMED → PROCESSING → READY_FOR_PICKUP → ASSIGNED → PICKED_UP
   │         │             │                              │           │
   │         └──────┬──────┘                              │           ▼
   │                ▼                                     │      IN_TRANSIT
   │         (cancel window ends at READY_FOR_PICKUP)     │           │
   │                                                      │           ▼
   │                                                      └──► OUT_FOR_DELIVERY ──code──► DELIVERED
   │                                                   │   │
   │                                    7d, no dispute │   │ within window
   ▼                                                   ▼   ▼
CANCELLED ──► REFUNDED                            COMPLETED → RETURN_REQUESTED
                                                            │        │
                                              ┌─────────────┤        ├─► RETURN_REJECTED → COMPLETED
                                              ▼             ▼        ▼
                                         DISPUTED    RETURN_APPROVED → RETURN_RECEIVED → REFUNDED
                                          │  │
                              vendor win ─┘  └─ buyer win → REFUNDED
```

## 4. Master vs Sub-Order State Semantics

- The machine above executes **per sub-order** (per vendor).
- **Master order** aggregates: enters `PLACED` when payment succeeds; reaches `COMPLETED` only when every sub-order is `COMPLETED` or `REFUNDED` (BR-ORD-07).
- Payment, escrow funding, and buyer-facing timeline operate at master level; fulfillment, commission, payout operate at sub-order level (C-10).
- A dispute on one sub-order freezes only that sub-order's escrow; the master completes when all sub-orders settle.

## 5. Concurrency & Guards

| Concern | Handling |
|---|---|
| Simultaneous transitions | Optimistic locking on `version` column; invalid transition → `409 STATE_CONFLICT` |
| Duplicate code entry | Idempotent: first success wins; later attempts no-op with same result |
| Race: cancel vs assign | Transition guards evaluated inside the order transaction; cancel wins only if state is pre-READY_FOR_PICKUP |
| Double refund | Idempotency key (BR-PAY-08); ledger posts once |

## 6. Verification

- Unit tests enumerate all 17 states and every allowed/forbidden transition (≥ 1 test per row of §2).
- Integration test: full happy path PLACED → COMPLETED.
- Constraint test `TST-CON-09`: state count == 17 and no other states exist in code.
- Negative tests: forbidden skips (e.g., PLACED → DELIVERED) rejected.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
