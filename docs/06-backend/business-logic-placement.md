---
document_id: DOC-BE-005
title: Business Logic Placement — Rule ID → Module → Service → Enforcement Point
category: 06-backend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, NFR-008, NFR-010, SEC-REQ-004]
related_documents: [DOC-BE-001, DOC-BE-002, DOC-BE-006, DOC-BA-005]
---

# Business Logic Placement

Every critical rule in `01-business-analysis/business-rules.md` executes **server-side** in a named service/domain class. This file is the authoritative map: **rule ID → module → service → enforcement point**. Rules are never redefined here — only located.

Module names follow `DOC-BE-002` §3 (`b01-identity` … `b13-platform`).

---

## 1. Master Placement Table

| Rule(s) | Concern | Module | Service / Domain class | Enforcement point |
|---|---|---|---|---|
| `BR-AUTH-01…08` | identity, OTP, lockout, sessions | b01-identity | `AuthService`, `OtpService`, `SessionService`, `TokenService` | controller pipes + service guards (`DOC-BE-003`) |
| `BR-CAT-01/02/04/05/08` | publishable product, variants, price bounds, product types, images | b02-catalog | `ProductDomain.validateForPublish()`, `ProductService` | product create/update DTO + domain validation |
| `BR-CAT-03` | category tree depth ≤5, slug uniqueness | b02-catalog | `CategoryService` | service precondition + DB unique constraint |
| `BR-CAT-06` | soft delete; only ACTIVE visible | b02-catalog | `ProductRepository` scope | repository default filter + storefront queries |
| `BR-CAT-07`, `C-13` | stock ≥0, atomic deduction, 15-min reservation TTL | b02-catalog | `InventoryService.reserve()/deduct()/release()` | DB row lock in transaction; TTL job (`DOC-BE-006` §5) |
| `BR-VND-01/02/03/06` | KYC gating, one store, 48-h SLA, staff roles | b03-store | `VendorService`, `KycService` | guards on product publish; job escalation at 48 h |
| `BR-VND-04/05/07` | suspension effects, followers, store scoping | b03-store | `StoreService` + repositories | ownership filter on every vendor query (`DOC-BE-004` §4) |
| `BR-CRT-01…06` | cart limits, countdown, merge, server totals, checkout guards, balance check | b05-checkout | `CartService`, `CheckoutService` | add/merge mutations + order placement saga |
| `BR-ORD-01/02/03` | 17 states, master/sub, append-only history | b06-order | `OrderStateMachine`, `OrderService` | state transition guard; `order_status_history` insert-only |
| `BR-ORD-04/05/07/08/09` | cancel windows, dispute freeze, sub-order advancement, code-gated DELIVERED, timeline visibility | b06-order (+ b08-shipping) | `OrderService.transition()`, `TimelineQuery` | transition guards + query scoping |
| `BR-ORD-06`, `BR-PLT-03` | idempotent order creation | b05-checkout | `CheckoutService.placeOrder()` | `Idempotency-Key` middleware (`DOC-BE-009` §5) |
| `BR-ORD-10` | 24-h CONFIRMED escalation | b06-order | repeatable job `b06.order.sla.check` | background job + notification (`DOC-BE-006` §6) |
| `BR-PAY-01…10` | wallet-only, top-up bounds, callbacks, bank verify, no-negative, double-entry, refunds, idempotency, freeze, integer YER | b07-wallet | `WalletService`, `TopUpService`, `PaymentService`, `LedgerService` | payment intent creation; row lock + ledger post in transaction |
| `BR-ESC-01…08` | 7-day hold, release conditions, commission, reversal, payout batching, KYC gate, refund ordering, reconciliation | b07-wallet | `EscrowService`, `CommissionService`, `PayoutService`, `ReconciliationService` | release job, payout job, daily reconciliation job |
| `BR-SHP-01…07` | shipping fee, code issue/lock, first-accept assignment, no GPS, escalation, proof | b08-shipping | `ShippingService`, `AssignmentService`, `DeliveryCodeService` | fee calc at checkout; code verify endpoint; optimistic lock on assignment |
| `BR-RET-01…07` | window, states, refund composition, 3-day credit, 72-h inspection, admin arbiter, commission reversal | b09-returns | `ReturnService`, `InspectionService` | return request guard; inspection deadline job |
| `BR-NTF-01…05` | channels, mandatory security notices, OTP failover, bilingual templates, opt-out | b10-notification | `NotificationService`, `TemplateService`, `PreferenceService` | fan-out job; preference check at enqueue |
| `BR-PRM-01…06` | coupon constraints, non-stacking, scope, types, rejection | b12-content | `CouponService.apply()` | checkout validation step — rejects before order row exists |
| `BR-REV-01…05` | eligibility window, one per item, rating bounds, response/moderation, store rating | b02-catalog (+ b13-platform) | `ReviewService`, `ModerationService` | create guard; moderation writes audit |
| `BR-PLT-01…07` | queue naming, retry/DLQ, idempotency keys, ACID/saga, localization, audit, health | cross-cutting | shared modules + jobs (`DOC-BE-006`) | infra-level, per file |
| `BR-FIN-01…05` | VAT, totals, reconciliation, statements, rounding | b07-wallet (+ b11-analytics) | `PricingService` (domain), `StatementService` | pricing domain used by checkout; monthly statement job |

## 2. Checkout, Pricing & VAT (`BR-PAY-*`, `BR-FIN-01/02`, `BR-PRM-06`)

Sequence inside `CheckoutService.placeOrder()` (single transaction + saga, `BR-PLT-04`):

```text
1. Idempotency-Key check           → replay returns original order (BR-ORD-06)
2. Cart revalidation               → items ACTIVE, in stock, limits C-15 (BR-CRT-05/01)
3. Coupon application              → b12 CouponService; invalid → 422, no order row (BR-PRM-06)
4. Pricing domain                  → subtotal − discount → VAT 15% on that base; shipping untaxed (BR-FIN-01)
                                     sub-order total = (items − discount) + VAT + shipping (BR-FIN-02)
                                     half-up rounding to whole YER per sub-order (BR-FIN-05)
5. Order bounds check              → 500 ≤ total ≤ 5,000,000 YER (C-14)
6. Wallet payment                  → row lock, balance ≥ total, no negative (BR-PAY-05/06, BR-CRT-06)
                                     method must be wallet — anything else rejected
                                     PAYMENT_METHOD_NOT_ALLOWED (BR-PAY-01, C-01)
7. Stock deduction                 → atomic, tied to payment (C-13, BR-CAT-07)
8. Master + sub-orders created     → state PLACED, history row appended (BR-ORD-02/03)
9. Events                          → notifications, index sync, SLA timers enqueued
Compensating actions on failure    → refund ledger entries, stock restore (BR-PLT-04)
```

VAT display parity: server returns the full breakdown; clients render it (`../05-frontend/core/forms-and-validation.md`).

## 3. Escrow Lifecycle (`BR-ESC-*`)

| Stage | Trigger | Module/Service | Guard |
|---|---|---|---|
| Fund | order PLACED (payment success) | b07 `EscrowService.fund()` | master-level payment only (C-10) |
| Hold | DELIVERED (code verified) | b06 → event → b07 | 7 days from DELIVERED (BR-ESC-01, C-12) |
| Release | `b07.escrow.release` job at +7 d | `EscrowService.release()` | 7 d elapsed ∧ no dispute ∧ state ∉ {DISPUTED, RETURN_*, REFUNDED} (BR-ESC-02) |
| Commission | at release | `CommissionService` | (line subtotal after coupon) × rate 5–20% (default 10%) (BR-ESC-03) |
| Reverse | refund after release | `CommissionService.reverse()` | proportional reversal (BR-ESC-04, BR-RET-07) |
| Freeze | DISPUTED raised | `OrderService` → escrow freeze | only that sub-order freezes (state doc §4) |
| Payout | after release | `PayoutService` batch job | 3–7 business days, min 1,000 YER rollover, KYC approved, store not suspended (BR-ESC-05/06) |
| Refund draw | refund due | `RefundService` | escrow first, then vendor payable (BR-ESC-07) |
| Reconcile | daily job | `ReconciliationService` | Σ ledger balanced; mismatch → finance alert (BR-ESC-08, BR-FIN-03) |

## 4. Order State Transitions (C-09, `../03-system-analysis/core/state-transitions.md`)

| Aspect | Placement |
|---|---|
| Canonical table | `b06-order/domain/order-state.machine.ts` — code-generated/checked against `../03-system-analysis/core/state-transitions.md`; exactly 17 states (C-09, `TST-CON-09`) |
| Transition execution | `OrderService.transition(from, to, actor, reason)` — single entry point; **no direct `status` UPDATE anywhere else** (enforced by lint + architecture test) |
| Guards | machine validates from→to, actor eligibility (BR-ORD-04 cancel windows), preconditions (KYC, code verified, attempts) |
| Concurrency | optimistic lock on `version`; losing writer → **409 `STATE_CONFLICT`** (state doc §5) |
| History | append-only `order_status_history` row with actor/timestamp/reason (BR-ORD-03) |
| DELIVERED gate | only via `DeliveryCodeService.verify()` (BR-ORD-08, BR-SHP-02/03, C-16) |
| Client impact | invalid transition surfaced to UI as `STATE_CONFLICT` → frontend refetches (`../05-frontend/core/forms-and-validation.md` §5) |
| Master completion | sub-orders COMPLETED or REFUNDED → master COMPLETED (BR-ORD-07) |

## 5. Stock TTL (C-13, `BR-CAT-07`)

| Event | Code path |
|---|---|
| Reserve on cart add/checkout entry | `InventoryService.reserve()` — `expires_at = now + 15 min`, atomic |
| Expiry | job `b02.inventory.expire` (repeatable every minute; idempotent per reservation) releases holds, emits `StockReleased` (DOC-BE-006 §5) |
| Pay | `deduct()` inside payment transaction — permanent |
| Cancel/refund | `restore()` with ledger-consistent audit |
| Oversell prevention | DB check constraint `stock >= 0` + row lock; service rejects with `STOCK_UNAVAILABLE` |

## 6. Return Inspection Window (`BR-RET-05`)

| Step | Placement |
|---|---|
| RETURN_RECEIVED entered | `ReturnService.markReceived()` starts 72-h deadline (stored on return row) |
| Vendor submits inspection | `InspectionService.conclude(passed, reason)` before deadline |
| Deadline elapsed | job `b09.return.inspect-check` → auto-approve → proceeds to REFUNDED (BR-RET-05) |
| Refund credit | wallet credit within 3 business days of REFUNDED (BR-RET-04) — payout-style job in b07 |
| Window at request time | `ReturnService.request()` checks delivery date + `returnPeriodDays`/`isReturnable` (BR-RET-01, C-11) |

## 7. Anti-Patterns (rejected in review)

| Anti-pattern | Why forbidden |
|---|---|
| Rule logic in controllers or client code | not testable as domain; bypassable (`SEC-REQ-004`) |
| Direct `UPDATE orders SET status` outside `OrderService.transition` | breaks C-09 machine and history (BR-ORD-03) |
| Trusting client-provided totals/roles/stock | server recomputes (`BR-CRT-04`) |
| Job payloads carrying money amounts as authoritative | jobs re-read state; payload carries IDs only |
| Database triggers as primary rule engine | rules must be unit-testable without DB (`NFR-010`) |
| Silent auto-cancellation of stale orders | BR-ORD-10 requires escalation + notification, never silent cancel |

## 8. Verification

- Unit tests per domain class (no I/O) — `NFR-010`.
- One integration test per row group in §1 asserting the enforcement point rejects violations (`13-testing/`).
- Architecture test: only `OrderService` writes `orders.status` (C-09).
- Traceability: every `BR-*` ID maps to ≥1 test case (`19-traceability/`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
