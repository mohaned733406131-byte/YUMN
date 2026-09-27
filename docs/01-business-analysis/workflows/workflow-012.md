---
document_id: DOC-WF-013
title: "WF-012 — Coupon Creation (Admin/Vendor) → Redemption at Checkout"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-011, FR-013, FR-019]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-012 — Coupon Creation (Admin/Vendor) → Redemption at Checkout

| Field | Value |
|---|---|
| **Trigger** | Admin creates a platform coupon or a vendor creates a store coupon; later, a customer applies a code at checkout |
| **Actors** | Admin (`ACT-04`) / Vendor (`ACT-02`) create; Customer (`ACT-01`) redeems; System (`ACT-07`) validates & applies |
| **Blocks** | B12 Content & CMS (coupon engine) · B05 Cart & Checkout · B07 Payment & Wallet (VAT/commission base) · B11 Analytics |
| **Preconditions** | Creator authorized (admin: platform coupons; vendor: own store, `BR-VND-07`); checkout session exists (WF-003) |
| **Final state** | One coupon applied to the order with recomputed totals (or a validation error with **no order row**) |

```text
[Admin] ── platform coupon ──┐
                             ├──► define: code, type, window ≤90 d, limits ──► coupon ACTIVE (BR-PRM-01, BR-PRM-03)
[Vendor] ── store coupon ────┘         │                                             │
                                       │ invalid: window >90 d, discount >90%, dup code
                                       ▼
                                ✗ REJECTED AT CREATION

[Customer at checkout, step 4] ── enter code ──► validate ──┬── ok ──► apply once (no stacking, BR-PRM-02)
        ▲                                                    │              │
        │                                                    │ expired /    ▼
        │                                                    │ used-up /    recompute totals server-side:
        │                                                    │ min not met   items − discount = base
        │                                                    │               ├─ VAT = 15% × base (BR-FIN-01)
        │                                                    ▼               ├─ commission base excludes discount (BR-ESC-03)
        │                                             ✗ ERROR, NO ORDER      └─ free_shipping? fee = 0 (BR-SHP-01)
        │                                                 ROW (BR-PRM-06)                     │
        └─────────────────────────── confirm (WF-003 step 6–7) ◄──────────────────────────────┘
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Admin / Vendor | Create coupon with code, type, validity, limits | B12 | `BR-PRM-01`, `BR-PRM-03`, `BR-PRM-05` | coupon row (scope: platform or store) | Validity window >90 days → rejected; vendor coupons are scoped to own `store_id` (`BR-VND-07`) |
| 2 | System | Validate creation parameters | B12 | `BR-PRM-01` | — | Duplicate code, >90% discount, bad type → rejected at creation |
| 3 | Admin | Optional oversight: list/disable vendor coupons | B12, B13 | `BR-PRM-03`, `BR-PLT-06` | status flag + audit entry | Admin can always disable any coupon (`BR-PRM-03`) |
| 4 | Customer | Enter coupon code at checkout step 4 | B05 | `BR-PRM-04` | checkout session coupon ref | Optional step — no coupon is the default path |
| 5 | System | Validate: exists, active, window, min amount, per-user/global usage | B12 | `BR-PRM-04`, `BR-PRM-06` | — | Expired / fully used / below `min_order_amount` → validation error **before order creation** (`BR-PRM-06`) |
| 6 | System | Enforce one coupon per order | B05 | `BR-PRM-02` | single coupon slot | Second coupon attempt → rejected (no stacking) |
| 7 | System | Recompute totals server-side | B05, B07 | `BR-CRT-04`, `BR-FIN-01`, `BR-FIN-05` | VAT recomputed on (subtotal − discount); shipping excluded from VAT | Price drift since add-to-cart → re-confirmation (`BR-CRT-04`) |
| 8 | System | Apply shipping rule if type = `free_shipping` | B08 | `BR-SHP-01` | shipping fee = 0 | Otherwise fee unchanged (`BR-SHP-01`) |
| 9 | Customer | Confirm order | B05, B06 | `BR-ORD-06`, `BR-PLT-03` | order row with discount lines; coupon usage counters incremented | Duplicate submit → original order returned; coupon reserved atomically (idempotency, `BR-PLT-03`) |
| 10 | System | Record commission base for later release | B07 | `BR-ESC-03` | commission base = line subtotal after coupon discount | Commission computed at escrow release (WF-006), never at checkout |

**Alternatives**
- **`buy-X-get-Y` / fixed / percentage types:** all resolved in step 7's server-side recalculation (`BR-PRM-05`).
- **Vendor store coupon:** only redeemable against that vendor's lines; admin can list/disable it (`BR-PRM-03`).
- **Coupon becomes invalid between apply and confirm** (used up concurrently): step 5/9 re-validate inside the order transaction → error, no order row (`BR-PRM-06`).

**Exceptions**
- Stacking attempt → single-slot enforcement (`BR-PRM-02`).
- Discount exceeding 90% of order value → invalid (`BR-PRM-01`).
- Coupon abuse (per-user limit hit) → rejected per-user; global limit decrements atomically (`BR-PRM-04`).
- Invalid coupon must never leave a partial order — validation precedes order creation (`BR-PRM-06`, `BR-ORD-06`).
- Refund after redemption → usage counters restored per refund path; commission reversal already handled by `BR-ESC-04` (WF-007).

**Rules applied:** `BR-PRM-01…06`, `BR-CRT-04`, `BR-FIN-01/05`, `BR-ESC-03`, `BR-SHP-01`, `BR-ORD-06`, `BR-VND-07`, `BR-PLT-03/06` · Constraints: `C-10`, `C-14` (total bounds still enforced after discount).

**Data touched:** coupons (scope, window, limits, status), checkout session (applied code, discount lines), order rows (discount, VAT, commission base), coupon usage counters, audit entries.

**Systems:** B12 Content & CMS · B05 Cart & Checkout · B07 Payment & Wallet · B08 Shipping · B06 Order Management · B11 Analytics (redemption reporting).

**Final state:** exactly one coupon applied (or none), totals recomputed with VAT on the discounted base, commission base recorded net of discount, coupon usage counters incremented — or a validation error with no order row.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
