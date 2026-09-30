---
document_id: DOC-BA-005
title: Business Rules (BR Registry)
category: 01-business-analysis
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016]
related_documents: [DOC-OVR-008, DOC-BA-001]
---

# Business Rules — Canonical Registry

**Single source of truth for all business rules.** Rule IDs: `BR-<DOMAIN>-NN`. Domains: `AUTH CAT VND CRT ORD PAY ESC SHP RET NTF PRM REV PLT FIN INV`. Rules are enforced by backend services and verified by test cases (`13-testing/`); rules never contradict constraints (`C-01…C-26`).

**104 rules.**

---

## AUTH — Authentication & Identity (8)

| ID | Rule |
|---|---|
| BR-AUTH-01 | Phone number (format `^7[0-9]{8}$`) is the primary user identifier and must be unique across the platform. |
| BR-AUTH-02 | Passwords require ≥8 characters containing upper case, lower case, and a digit; stored with bcrypt cost 12; never logged. |
| BR-AUTH-03 | OTP: 6 digits, 5-minute expiry, max 3 verification attempts, resend cooldown 60 s, max 3 resends per 10 minutes. |
| BR-AUTH-04 | 5 consecutive failed logins lock the account for 15 minutes; lock events are logged. |
| BR-AUTH-05 | Refresh tokens are single-use: rotation on every use; presenting an already-used token revokes the entire session family and alerts the user. |
| BR-AUTH-06 | Maximum 5 active device sessions per user; new login beyond the limit removes the oldest session. |
| BR-AUTH-07 | Password reset (via OTP) invalidates all existing sessions. |
| BR-AUTH-08 | Email is optional and must be verified if provided; it is never used for login or OTP delivery. |

## CAT — Catalog, Products & Inventory (8)

| ID | Rule |
|---|---|
| BR-CAT-01 | A publishable product requires: Arabic name (mandatory), price in YER, category, ≥1 image, stock ≥0, and a store. |
| BR-CAT-02 | Variants: ≤5 dimensions, ≤50 combinations; SKU unique within a store. |
| BR-CAT-03 | Category tree depth ≤5 levels; slugs unique per level. |
| BR-CAT-04 | Price must be > 0; sale price < original price; order totals bounded 500–5,000,000 YER (C-14). |
| BR-CAT-05 | Product types are physical goods only — subscription, trial, sample, and rental types are rejected at validation. |
| BR-CAT-06 | Product deletion is soft-delete; only ACTIVE products appear in search/storefront. |
| BR-CAT-07 | Stock is an integer ≥ 0; oversell is prohibited — deduction is atomic and reservation expires after 15 minutes (C-13). |
| BR-CAT-08 | Product images: ≤10 per product, ≤5 MB each, formats jpg/png/webp only, EXIF stripped on upload. |

## VND — Vendors, Stores & KYC (7)

| ID | Rule |
|---|---|
| BR-VND-01 | A vendor cannot publish products until KYC status = APPROVED. |
| BR-VND-02 | One store per vendor account in v1. |
| BR-VND-03 | KYC decisions must be made within 48 hours of submission; rejection allows resubmission. |
| BR-VND-04 | Suspended vendor: products hidden from storefront, new orders blocked, existing orders frozen, payouts held pending review. |
| BR-VND-05 | Customers may follow a store; vendors see their follower list and count; followers receive new-product/offers notifications. |
| BR-VND-06 | Vendor staff roles are Viewer / Editor / Manager; only the Owner invites, removes, or changes staff roles. |
| BR-VND-07 | Every vendor-facing query is scoped to `store_id` ownership; cross-store access is denied at the service layer. |

## CRT — Cart (6)

| ID | Rule |
|---|---|
| BR-CRT-01 | Cart limits: ≤50 distinct products, ≤10 units per product, ≤5 vendors per cart (C-15). |
| BR-CRT-02 | Adding items starts/refreshes a 15-minute reservation countdown; expiry releases reserved stock. |
| BR-CRT-03 | Guest carts live client-side and merge on login; on quantity conflict the server value wins. |
| BR-CRT-04 | Totals are always recalculated server-side at checkout; any price change since add-to-cart is shown for re-confirmation. |
| BR-CRT-05 | Items that became inactive, out-of-stock, or out-of-policy block checkout until removed. |
| BR-CRT-06 | Checkout requires wallet balance ≥ order total at confirmation time (C-01). |

## ORD — Orders & Lifecycle (10)

| ID | Rule |
|---|---|
| BR-ORD-01 | The lifecycle has exactly 17 states — enumeration and transitions defined in `../03-system-analysis/core/state-transitions.md` (C-09). |
| BR-ORD-02 | One master order per checkout; one sub-order per vendor; master total = Σ sub-order totals; payment & escrow at master level (C-10). |
| BR-ORD-03 | State changes are append-only in `order_status_history` with actor, timestamp, and reason; states are never overwritten. |
| BR-ORD-04 | Customer may cancel only while PLACED or CONFIRMED; vendor/admin cancellation allowed until READY_FOR_PICKUP; cancellation always triggers wallet refund flow. |
| BR-ORD-05 | DISPUTED freezes escrow release for all affected sub-orders until admin resolution. |
| BR-ORD-06 | Order creation requires an idempotency key; duplicate submissions return the original order. |
| BR-ORD-07 | A sub-order cannot advance past its own vendor's fulfillment steps; master COMPLETED requires all sub-orders COMPLETED or REFUNDED. |
| BR-ORD-08 | State may reach DELIVERED only via successful 6-digit delivery-code verification (C-16). |
| BR-ORD-09 | Order timeline is visible to: buyer (own), vendor (own sub-orders), assigned courier (own delivery), admin/moderator (scoped). |
| BR-ORD-10 | An order still at CONFIRMED 24 h after confirmation is escalated to admin review (notification sent); it is never silently auto-cancelled without notification. |

## PAY — Wallet & Payments (10)

| ID | Rule |
|---|---|
| BR-PAY-01 | Only wallet payment is accepted for orders; any other method is rejected with `PAYMENT_METHOD_NOT_ALLOWED` (C-01). |
| BR-PAY-02 | Top-up bounds: minimum 1,000 YER, maximum 5,000,000 YER per transaction. |
| BR-PAY-03 | m-Floos / OneCash top-ups credit the wallet only after a verified provider callback (or reconciled poll), never on client claim. |
| BR-PAY-04 | Bank-transfer top-ups credit the wallet only after admin verification of the reference (INT-REQ-002). |
| BR-PAY-05 | Wallet balance can never go negative; payment uses row-level locking with atomic balance check. |
| BR-PAY-06 | Every balance change posts balanced double-entry ledger rows (debit + credit); ledger is append-only (DATA-REQ-007). |
| BR-PAY-07 | Refunds always credit the wallet — never external cash-out to cards/banks (except vendor payouts, BR-ESC-05). |
| BR-PAY-08 | Payments, top-ups, and refunds are idempotent via idempotency keys (BR-PLT-03). |
| BR-PAY-09 | Admin can freeze a wallet (legal/security); frozen wallets cannot pay or top up, but receive refunds. |
| BR-PAY-10 | Amounts are stored as integer YER (no floats); display via `ar-YE` locale formatting with Arabic-Indic numerals. |

## ESC — Escrow, Commission & Payouts (8)

| ID | Rule |
|---|---|
| BR-ESC-01 | On DELIVERED, funds for the sub-order are held in escrow for 7 days (C-12). |
| BR-ESC-02 | Escrow releases to vendor payable only when: 7 days elapsed AND no active dispute AND state ∉ {DISPUTED, RETURN_*, REFUNDED}. |
| BR-ESC-03 | Commission = (line subtotal after coupon discount) × commission rate; rate is per-vendor tier 5–20%, default 10%. |
| BR-ESC-04 | Commission is computed at release; if the order is refunded later, commission is reversed proportionally. |
| BR-ESC-05 | Payouts are batched and executed 3–7 business days after release; minimum payout amount 1,000 YER (below threshold rolls over). |
| BR-ESC-06 | Payouts require KYC = APPROVED and a non-suspended store. |
| BR-ESC-07 | Refunds draw from escrow-held funds first, then from vendor payable if escrow is insufficient (vendor liability). |
| BR-ESC-08 | Daily reconciliation: Σ ledger entries must balance; wallet + escrow + payable totals must equal provider statements; mismatch alerts finance. |

## SHP — Shipping & Delivery (7)

| ID | Rule |
|---|---|
| BR-SHP-01 | Shipping fee = f(shipping zone, package weight, method); free when an applied coupon has type `free_shipping`. |
| BR-SHP-02 | At OUT_FOR_DELIVERY a 6-digit code is issued to the buyer; courier enters it to confirm delivery (C-16). |
| BR-SHP-03 | Code attempts: 1–2 show remaining attempts; 3rd failure locks confirmation for 24 hours and auto-creates a support ticket. |
| BR-SHP-04 | Courier assignment: offered to eligible couriers in the same zone; first accept wins (optimistic locking prevents double assignment). |
| BR-SHP-05 | The platform never requests or stores courier GPS location (C-16). |
| BR-SHP-06 | After 3 failed delivery attempts the order escalates to admin review with full timeline. |
| BR-SHP-07 | Delivery proof = code + timestamp + courier identity; optional photo is stored but never required. |

## RET — Returns & Refunds (7)

| ID | Rule |
|---|---|
| BR-RET-01 | Return window = delivery confirmation date + product `returnPeriodDays`; `isReturnable = false` or window elapsed → request rejected (C-11). |
| BR-RET-02 | Return states: RETURN_REQUESTED → RETURN_APPROVED / RETURN_REJECTED → RETURN_RECEIVED → REFUNDED (part of the 17-state machine). |
| BR-RET-03 | Refund amount = item value; shipping is refunded only when the fault is platform/vendor-side. |
| BR-RET-04 | Refund credits the customer wallet within 3 business days of REFUNDED state. |
| BR-RET-05 | Vendor inspection after RETURN_RECEIVED must conclude within 72 hours; otherwise the return auto-approves. |
| BR-RET-06 | Where policy and dispute conflict, the admin is final arbiter; decision is written to audit log. |
| BR-RET-07 | Refund triggers proportional commission reversal (BR-ESC-04) and escrow adjustment (BR-ESC-07). |

## NTF — Notifications (5)

| ID | Rule |
|---|---|
| BR-NTF-01 | Channels: SMS, WhatsApp, in-app, push — no email channel in v1 (GAP-03 pending confirmation). |
| BR-NTF-02 | Security notifications (OTP, login, password change, lockout) cannot be disabled by the user. |
| BR-NTF-03 | OTP delivery: SMS primary; automatic failover to WhatsApp on provider timeout/failure (INT-REQ-003). |
| BR-NTF-04 | Every notification template exists in Arabic and English; language follows user locale (Arabic default). |
| BR-NTF-05 | Users may opt out of marketing/notification categories independently per channel. |

## PRM — Promotions & Coupons (6)

| ID | Rule |
|---|---|
| BR-PRM-01 | Coupon constraints: unique code, validity window ≤ 90 days, percentage discount ≤ 90% of order value. |
| BR-PRM-02 | Coupons never stack — one coupon per order. |
| BR-PRM-03 | Coupon scope: platform coupons (admin-created) or store coupons (vendor-created, admin can list/disable). |
| BR-PRM-04 | Optional `min_order_amount`; usage limits per-user and global; expired/fully-used coupons rejected before order creation. |
| BR-PRM-05 | Types: percentage, fixed amount, free shipping, buy-X-get-Y. |
| BR-PRM-06 | Invalid coupon → validation error; no order row is created. |

## REV — Reviews & Ratings (5)

| ID | Rule |
|---|---|
| BR-REV-01 | Only the purchasing customer may review, and only after DELIVERED; window 30 days from delivery. |
| BR-REV-02 | One review per order item; editable once within 7 days. |
| BR-REV-03 | Rating is an integer 1–5; ≤5 images, ≤5 MB each. |
| BR-REV-04 | Vendor may respond once per review; Moderator/Admin may hide a review with audit entry (abuse/inappropriate). |
| BR-REV-05 | Store rating = average of visible product ratings with review count shown; recomputation is incremental via job. |

## PLT — Platform & Technical Business Rules (7)

| ID | Rule |
|---|---|
| BR-PLT-01 | Background jobs use BullMQ queues named `{block}.{entity}.{action}` (C-20). |
| BR-PLT-02 | Jobs retry 3× with exponential backoff, then dead-letter queue; DLQ depth triggers an alert. |
| BR-PLT-03 | Idempotency keys are mandatory for: payment, order creation, stock reservation, coupon application, refund. |
| BR-PLT-04 | Money operations run inside ACID transactions; multi-step order creation uses a saga with compensating actions. |
| BR-PLT-05 | Arabic-first: all user-facing text localized (ar default, en parity); no hardcoded strings (C-24). |
| BR-PLT-06 | Privileged and money actions write append-only audit entries (actor, action, entity, before/after, IP, timestamp). |
| BR-PLT-07 | Liveness/readiness health endpoints gate traffic; availability target 99.99% (C-26). |

## FIN — Finance & Tax (5)

| ID | Rule |
|---|---|
| BR-FIN-01 | VAT = 15% × (cart subtotal − coupon discount); shipping is not taxed; VAT is added on top and shown in every breakdown. |
| BR-FIN-02 | Sub-order total = (items − item discount) + VAT + shipping fee; order total = Σ sub-order totals (BR-ORD-02). |
| BR-FIN-03 | Daily automated reconciliation across ledger, wallets, escrows, payables, and provider statements (BR-ESC-08). |
| BR-FIN-04 | Vendors receive a monthly statement: sales, commission, refunds, payouts, adjustments. |
| BR-FIN-05 | All monetary rounding is half-up to whole YER at each sub-order level; rounding differences are posted to a platform rounding account. |

## INV — Inventory & Stock Reservations (5)

| ID | Rule |
|---|---|
| BR-INV-01 | A successful reservation holds stock atomically: on-hand stock is never oversold, one `stock_reservation` row is created per reserved cart line, and the reservation either commits (payment success → permanent deduction) or releases (expiry or cancellation) — reserve → commit/release (`FR-005`, `C-13`, `08-database/entities/inventory.md`). |
| BR-INV-02 | Stock invariant at all times: `stock ≥ reservedQuantity ≥ 0` (`qty_on_hand ≥ qty_reserved ≥ 0`, `qty_available` generated) — reserved quantity never exceeds on-hand stock and never goes negative (`BR-CAT-07`, `DATA-REQ-001`, `ck_inventory_no_negative`). |
| BR-INV-03 | Live reservations are protected: a manual stock adjustment that would set stock below active reservations is rejected with `409 STOCK_BELOW_RESERVATIONS`; the DB row stays unchanged (no partial writes) (`07-api/error-model.md`, `UC-018`). |
| BR-INV-04 | Unpaid reservations expire after 15 minutes: the TTL sweeper releases held quantity exactly once (status-guarded — a re-run never double-releases), the reservation moves to `RELEASED`, and a `RELEASE_TTL` ledger row records actor `SYSTEM` with a timestamp (`C-13`, `BR-CRT-02`, `FR-005`). |
| BR-INV-05 | Every inventory mutation (reserve, consume, release, manual adjustment, cancellation restoration) appends an append-only ledger row carrying actor, reason, delta and timestamp; corrections are new rows, never edits — the events the reconciliation job compares `qty_on_hand` against (`BR-PLT-06`, `FR-005`, `API-CAT-016`). |

---

## Rule Consistency Statement

Every rule above is traceable to at least one `FR-*` and is compatible with `C-01…C-26` (`VERIFIED` by pairwise review; see `20-validation/consistency-audit.md`). No rule permits COD, cards, GPS, microservices, or any excluded capability.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial registry (99 rules) | Initial analysis |
| 1.1 | 2026-09-28 | `INV` domain added — `BR-INV-01`…`BR-INV-05` (stock reservation lifecycle, `stock ≥ reserved ≥ 0` invariant, reservation-protected adjustment, 15-min TTL release, append-only mutation ledger); 99 → 104 rules, 14 → 15 domains | `CRIT-06`/`HAL-04` pay-down (session 008, owner-approved registration): the five IDs were cited by `TC-018`/`TC-019`/`TC-020` and undefined; wording derived from approved sources (`entities/inventory.md`, `C-13`, `BR-CAT-07`, `BR-CRT-02`, `error-model.md`, `API-CAT-016`) — never invented behavior |
