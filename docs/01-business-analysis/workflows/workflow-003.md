---
document_id: DOC-WF-004
title: "WF-003 — Cart → 7-Step Checkout → Wallet Payment → Order Placed"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-005, FR-010, FR-011, FR-013]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-003 — Cart → 7-Step Checkout → Wallet Payment → Order Placed

| Field | Value |
|---|---|
| **Trigger** | Registered customer taps "Checkout" from a validated cart |
| **Actors** | Customer (`ACT-01`), System (`ACT-07` — pricing, reservation, ledger, timers) |
| **Blocks** | B05 Cart & Checkout · B07 Payment & Wallet · B06 Order Management · B02 Inventory · B12 Coupons · B10 Notifications |
| **Preconditions** | Logged in (guest must log in — WF-001); cart within `C-15` guards; wallet funded or top-up available |
| **Final state** | Master order + per-vendor sub-orders in `PLACED`, wallet debited, escrow funded, stock permanently deducted, notifications sent |

```text
[Checkout start]
 1 Cart review (server re-price, BR-CRT-04) ──► 2 Delivery address (≤10) ──► 3 Shipping zone & method (BR-SHP-01)
      │ invalid/inactive lines                 │ no address                   │ zone outside (C-17)
      ▼                                         ▼                              ▼
 ✗ BLOCKED until removed (BR-CRT-05)      ✗ ADDRESS_REQUIRED            ✗ NO_SHIPPING_ZONE
      │
      ▼
 4 Coupon (optional, one only) ──► 5 Wallet payment method ──► 6 Review totals (subtotal − discount + VAT 15% + shipping)
      │ invalid/expired/stacked               │ balance < total                    │
      ▼                                       ▼                                    ▼
 ✗ ERROR, NO ORDER ROW (BR-PRM-06)     [INSUFFICIENT BALANCE]                  [confirm]
      │                                       │                                    ▼
      │                                       └──► top-up flow (WF-009) ──► return to step 5
      │                                                                       │
      │                              out of bounds (C-14) / frozen wallet      │
      │                                       ▼                               ▼
      │                                ✗ REJECTED (BR-PAY-09, C-14)    7 Confirm: idempotency key
      └──────────────────────────────────────────────────────────────►►► ► order PLACED (master + sub-orders)
                                                                             │ duplicate submit
                                                                             ▼
                                                                     original order returned (BR-ORD-06)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | System | Re-validate cart, recompute prices server-side | B05 | `BR-CRT-04`, `BR-CRT-05` | price snapshots refreshed | Inactive/OOS/out-of-policy line → checkout blocked until removed (`BR-CRT-05`) |
| 2 | Customer | Select delivery address (≤10 saved) | B01 | `FR-003` | checkout session address | No address → `ADDRESS_REQUIRED` |
| 3 | System | Resolve shipping zone, weight, method → fee | B08 | `BR-SHP-01`, `C-17` | shipping fee on session | Domestic-only zones; outside Yemen → `NO_SHIPPING_ZONE` (`C-17`) |
| 4 | Customer | Apply coupon (optional) | B12 | `BR-PRM-01…06` | coupon usage counters | Expired/stacked/over-limit → validation error, **no order row** (`BR-PRM-06`) |
| 5 | Customer | Confirm wallet as payment method; System checks balance | B07 | `BR-PAY-01`, `BR-CRT-06`, `BR-PAY-05`, `BR-PAY-09` | balance pre-check | Only wallet accepted (else `PAYMENT_METHOD_NOT_ALLOWED`, `C-01`); balance < total → **insufficient balance branch → WF-009 top-up → resume**; frozen wallet → rejected (`BR-PAY-09`) |
| 6 | System | Compute totals: items − discount + VAT 15% on (subtotal − discount) + shipping; round half-up per sub-order | B07 | `BR-FIN-01`, `BR-FIN-02`, `BR-FIN-05` | displayed breakdown | Order total outside 500–5,000,000 YER → rejected (`C-14`, `BR-CAT-04`); price drift since add → re-confirmation (`BR-CRT-04`) |
| 7 | Customer | Confirm placement (idempotency key) | B05, B06 | `BR-ORD-06`, `BR-PLT-03`, `BR-PLT-04` | master order + sub-orders `PLACED` | Duplicate submit → original order returned (`BR-ORD-06`) |
| 8 | System | Debit wallet atomically; post double-entry ledger; fund escrow at master level | B07 | `BR-PAY-05`, `BR-PAY-06`, `BR-PAY-08`, `C-10` | wallet ledger rows, escrow row | Balance can never go negative (row-level lock); debit failure → whole saga rolls back, no order |
| 9 | System | Deduct stock permanently; close 15-min reservation | B02 | `BR-CAT-07`, `C-13` | stock decremented atomically | Insufficient stock at confirm → cancellation branch (WF-010 semantics) with notification |
| 10 | System | Fan out notifications | B10 | `BR-NTF-04`, `BR-NTF-05` | notification queue | Arabic/English template per locale; marketing opt-outs respected |

**Alternatives**
- **Insufficient balance:** stay in checkout, launch WF-009 (m-Floos/OneCash/bank transfer, 1,000–5,000,000 YER bounds `BR-PAY-02`), return to step 5 on credit.
- **Multi-vendor cart:** one master order, one sub-order per vendor; payment/escrow at master level (`BR-ORD-02`, `C-10`).
- **Free shipping coupon:** fee zeroed when coupon type is `free_shipping` (`BR-SHP-01`), VAT still on (subtotal − discount) only.

**Exceptions**
- Concurrent reservation expiry during checkout → stock check re-runs inside the order transaction; failure aborts cleanly (saga + compensating actions, `BR-PLT-04`).
- Provider/wallet service error mid-payment → idempotency key prevents double charge (`BR-PAY-08`).
- VAT treated as platform-collected tax liability (`BR-FIN-01`); remittance schedule depends on `ASM-10` (`UNSUPPORTED`, `DEP-09`).

**Rules applied:** `BR-CRT-01…06`, `BR-PRM-01/02/04/06`, `BR-PAY-01/02/05/06/08/09/10`, `BR-FIN-01/02/05`, `BR-ORD-02/06`, `BR-CAT-04/07`, `BR-PLT-03/04`, `BR-SHP-01` · Constraints: `C-01`, `C-05`, `C-10`, `C-13`, `C-14`, `C-15`, `C-17`.

**Data touched:** checkout session, cart lines, coupon usage, wallet balance + ledger (append-only), escrow record, master/sub-orders, order_status_history, stock, notifications.

**Systems:** B05 Cart & Checkout · B07 Payment & Wallet · B06 Order Management · B02 Product Catalog · B08 Shipping · B12 Content & CMS (coupons) · B10 Notifications.

**Final state:** master order `PLACED` with one sub-order per vendor; wallet debited the exact order total with balanced ledger rows; escrow funded; stock deducted; confirmation notification sent. Vendor SLA clock starts (WF-004).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
