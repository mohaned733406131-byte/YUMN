---
document_id: DOC-BA-004
title: Business Processes (BP-01 … BP-15)
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-007, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-019, FR-020]
related_documents: [DOC-BA-001, DOC-BA-005, DOC-BA-006, DOC-BA-007]
---

# Business Processes

The 15 major business processes of the yumn marketplace, `BP-01…BP-15`. Each entry is compact: **trigger → actor → numbered steps → systems touched → rules applied (`BR-*`) → final state → failure paths**. Step sequences are analysis-level descriptions of canon flows; where a sequence detail is not fixed by canon it is derived (`INFERENCE`) from the cited rules. Detailed end-to-end walks with step tables live in `workflows/` (`WF-001…WF-012`); the rule definitions themselves live only in `business-rules.md`.

## BP-01 — Vendor Onboarding & KYC

- **Trigger:** prospective vendor submits registration + KYC documents. **Actor:** Vendor (`ACT-02`); Admin (`ACT-04`) decides.
- **Steps:** 1) register with phone + password + OTP (`FR-001`); 2) create store (one per account); 3) submit KYC documents; 4) Admin reviews and decides within SLA; 5) on approval, vendor publishes first product; 6) vendor is paid only after KYC-approved payout cycle.
- **Systems:** B01 Identity, B03 Store Management, B13 Admin console, B10 Notifications.
- **Rules:** `BR-VND-01` (no publish before APPROVED), `BR-VND-02`, `BR-VND-03` (≤48 h decision, resubmission allowed), `BR-VND-06`, `BR-VND-07`, `BR-AUTH-01…03`, `BR-PLT-06` (decision audited).
- **Final state:** KYC = APPROVED → store live → first listing publishable.
- **Failure paths:** rejection → resubmit (`BR-VND-03`); SLA breach → escalation to Admin queue; suspension later → `BR-VND-04` (products hidden, orders frozen, payouts held).

## BP-02 — Product Listing

- **Trigger:** vendor creates/edits a product. **Actor:** Vendor (`ACT-02`, staff Editor/Manager per `BR-VND-06`).
- **Steps:** 1) enter mandatory Arabic name, price (YER), category, ≥1 image; 2) optional variants (≤5 dimensions, ≤50 combinations, unique SKU); 3) set stock (integer ≥0); 4) upload images (≤10, ≤5 MB, jpg/png/webp, EXIF stripped); 5) submit → ACTIVE.
- **Systems:** B02 Product Catalog, object storage, B04 Search index.
- **Rules:** `BR-CAT-01…08`, `BR-VND-01`, `BR-VND-07` (store scoping), `BR-PLT-05` (Arabic-first text).
- **Final state:** product ACTIVE → visible in search/storefront (`BR-CAT-06`).
- **Failure paths:** missing Arabic name/price/image → validation error; non-physical type (subscription/trial/sample/rental) rejected (`BR-CAT-05`); delete = soft-delete, only ACTIVE surfaces; suspended vendor's products hidden (`BR-VND-04`).

## BP-03 — Customer Registration & Login

- **Trigger:** guest taps register/login. **Actor:** Customer (`ACT-01`); System (`ACT-07`) sends OTP.
- **Steps:** 1) enter phone `^7[0-9]{8}$` + password (≥8 chars, upper/lower/digit); 2) OTP requested (6 digits, 5 min); 3) verify ≤3 attempts; 4) account active; 5) login issues JWT (15 min access / 7-day rotating refresh); 6) guest cart merges.
- **Systems:** B01 Identity, B10 Notifications (SMS → WhatsApp failover), B05 Cart.
- **Rules:** `BR-AUTH-01…08`, `BR-NTF-02…04`, `BR-CRT-03` (cart merge, server wins on conflict).
- **Final state:** authenticated session (≤5 devices), profile editable (`FR-003`).
- **Failure paths:** 3 wrong OTPs → resend cooldown 60 s (max 3 resends/10 min); 5 failed logins → 15-min lockout (logged); refresh-token reuse → session family revoked (`BR-AUTH-05`); password reset invalidates all sessions (`BR-AUTH-07`).

## BP-04 — Search → Cart → Checkout

- **Trigger:** customer browses and decides to buy. **Actor:** Customer (`ACT-01`); System recalculates.
- **Steps:** 1) Arabic-aware search/filter/category browse; 2) open PDP (ACTIVE products only); 3) add to cart (≤50 products, ≤10 units each, ≤5 vendors); 4) 15-min reservation countdown starts/refreshes; 5) 7-step checkout: cart review → address → shipping → coupon → wallet → review totals → confirm; 6) server-side total recalculation incl. VAT; 7) wallet debit → order `PLACED` (master + per-vendor sub-orders).
- **Systems:** B04 Search, B05 Cart & Checkout, B07 Wallet, B06 Orders, B02 Inventory, B12 Coupons, B10 Notifications.
- **Rules:** `BR-CRT-01…06`, `BR-FIN-01/02/05`, `BR-PRM-02/04/06`, `BR-PAY-01/05/08`, `BR-ORD-02/06`, `BR-CAT-07`, `BR-PLT-03/04`, `C-14`, `C-15`, `C-13`.
- **Final state:** order `PLACED`; stock reserved/deducted; escrow funded.
- **Failure paths:** balance < total → blocked, customer top-ups (`BR-CRT-06`); price changed since add-to-cart → re-confirmation (`BR-CRT-04`); inactive/OOS item → checkout blocked until removed (`BR-CRT-05`); invalid/expired coupon → error, **no order row** (`BR-PRM-06`); out-of-bounds total → rejected (`C-14`); duplicate submit → original order returned (`BR-ORD-06`).

## BP-05 — Order Fulfillment (Vendor)

- **Trigger:** order `PLACED`, vendor notified. **Actor:** Vendor (`ACT-02`); System enforces SLA.
- **Steps:** 1) vendor accepts → `CONFIRMED`; 2) starts packing → `PROCESSING`; 3) pack complete → `READY_FOR_PICKUP`; 4) stock already deducted at `PLACED`; 5) timeline written at every transition.
- **Systems:** B06 Orders, B10 Notifications, B13 Admin (escalation view).
- **Rules:** `BR-ORD-03` (append-only history), `BR-ORD-09`, `BR-ORD-10` (24 h SLA at CONFIRMED → admin review, never silent auto-cancel), `BR-VND-04` (suspension freezes orders), `BR-CAT-07`.
- **Final state:** sub-order `READY_FOR_PICKUP`, awaiting courier (`BR-SHP-04` zone offer).
- **Failure paths:** vendor silent ≥24 h → escalation to admin with notification (`BR-ORD-10`); cancellation allowed until `READY_FOR_PICKUP` (`BR-ORD-04`); suspended vendor → new orders blocked, existing frozen (`BR-VND-04`).

## BP-06 — Delivery Confirmation

- **Trigger:** sub-order `READY_FOR_PICKUP`. **Actor:** Delivery Provider (`ACT-03`), Customer (`ACT-01`) shares code; System (`ACT-07`) verifies.
- **Steps:** 1) offer to eligible same-zone couriers, first accept wins → `ASSIGNED`; 2) pickup → `PICKED_UP`; 3) departure → `IN_TRANSIT`; 4) final leg → `OUT_FOR_DELIVERY`, **6-digit code issued to buyer**; 5) courier enters code → verified → `DELIVERED`; 6) escrow hold clock starts.
- **Systems:** B08 Shipping, B06 Orders, B10 Notifications, B07 Escrow.
- **Rules:** `BR-SHP-02…07`, `BR-ORD-08`, `BR-ORD-03`, `BR-ESC-01`, `C-16`.
- **Final state:** `DELIVERED`; proof = code + timestamp + courier identity (`BR-SHP-07`).
- **Failure paths:** wrong code 1–2 → remaining attempts shown, order returns to `IN_TRANSIT` if attempt <3; 3rd failure → 24 h confirmation lock + auto support ticket (`BR-SHP-03`) and admin review with full timeline (`BR-SHP-06`); courier releases assignment → back to `READY_FOR_PICKUP`; no GPS is ever requested (`BR-SHP-05`).

## BP-07 — Cancellation & Refund Trigger

- **Trigger:** customer/vendor/admin cancels before dispatch. **Actor:** Customer (`ACT-01`) while `PLACED`/`CONFIRMED`; Vendor/Admin until `READY_FOR_PICKUP`.
- **Steps:** 1) cancel request; 2) transition guard evaluated in-transaction; 3) `CANCELLED` written with actor/reason; 4) reserved/deducted stock restored; 5) wallet refund flow executes; 6) escrow unwound; 7) notifications sent.
- **Systems:** B06 Orders, B07 Wallet/Escrow, B02 Inventory, B10 Notifications, B13 Admin.
- **Rules:** `BR-ORD-03/04`, `BR-CAT-07` (stock restoration), `BR-PAY-07/08`, `BR-ESC-07`, `BR-NTF-04`, `BR-PLT-03`.
- **Final state:** `CANCELLED` → `REFUNDED` (wallet credited; escrow unwound).
- **Failure paths:** cancel after `READY_FOR_PICKUP` → rejected (`409 STATE_CONFLICT`); race cancel-vs-assign → cancel wins only pre-`READY_FOR_PICKUP`; duplicate refund request → idempotent no-op (`BR-PAY-08`).

## BP-08 — Return Request → Refund

- **Trigger:** buyer requests a return (or return window policy applies). **Actor:** Customer, Vendor, Admin, Delivery Provider, System across stages.
- **Steps:** 1) buyer opens return at `DELIVERED`/`COMPLETED` within policy window; 2) vendor/admin approve (`RETURN_APPROVED`, pickup scheduled) or reject with reason; 3) courier picks up → vendor receives → `RETURN_RECEIVED`; 4) inspection concludes ≤72 h; 5) pass → `REFUNDED` → wallet credit ≤3 business days; 6) proportional commission reversal + escrow adjustment.
- **Systems:** B09 Returns, B06 Orders, B08 Delivery, B07 Wallet/Escrow/Commission, B10 Notifications.
- **Rules:** `BR-RET-01…07`, `C-11`, `BR-ESC-04/07`, `BR-PAY-07`, `BR-ORD-03`.
- **Final state:** `REFUNDED` (money back to wallet) or `RETURN_REJECTED` → back to `COMPLETED`.
- **Failure paths:** `isReturnable=false` or window elapsed → rejected (`BR-RET-01`); inspection >72 h → auto-approve (`BR-RET-05`); policy-vs-dispute conflict → Admin final arbiter, audited (`BR-RET-06`); shipping refunded only when fault is platform/vendor-side (`BR-RET-03`).

## BP-09 — Dispute Resolution

- **Trigger:** buyer or vendor raises a dispute (pre- or post-`COMPLETED`). **Actor:** Customer/Vendor raise; Admin (`ACT-04`) resolves.
- **Steps:** 1) dispute raised → affected sub-order(s) → `DISPUTED`; 2) escrow frozen; 3) evidence gathered from order timeline/code proof/notifications; 4) admin decides vendor-win or buyer-win; 5) outcome written to `COMPLETED` or `REFUNDED`; 6) audit entry required.
- **Systems:** B06 Orders, B07 Escrow, B13 Admin, B10 Notifications.
- **Rules:** `BR-ORD-05` (freeze), `BR-ESC-02` (no release while disputed), `BR-ESC-07` (refund draws escrow first), `BR-RET-06` (admin final arbiter), `BR-PLT-06` (audit), `BR-ORD-09`.
- **Final state:** resolved → `COMPLETED` (vendor) or `REFUNDED` (buyer); escrow released or unwound accordingly.
- **Failure paths:** resolution delayed → escrow stays frozen (never released, `BR-ESC-02`); evidence without GPS relies on code + timeline (`C-16`, `BR-SHP-07`); cross-sub-order dispute freezes only affected sub-orders (`state-transitions.md` §4).

## BP-10 — Wallet Top-Up

- **Trigger:** customer adds funds. **Actor:** Customer; provider callback or Admin (`ACT-04`) for bank transfer.
- **Steps:** 1) choose m-Floos/OneCash or bank transfer; 2) amount 1,000–5,000,000 YER; 3a) wallet rails: initiate → provider callback/poll verified → credit; 3b) bank transfer: customer pays → submits reference → admin verifies → credit; 4) double-entry ledger posts; 5) confirmation shown.
- **Systems:** B07 Payment & Wallet, provider adapters, B13 Admin, BullMQ reconciliation jobs.
- **Rules:** `BR-PAY-02…06/08/10`, `BR-PLT-01…03`, `C-05`, `INT-REQ-001/002`.
- **Final state:** wallet balance increased; balanced ledger rows appended.
- **Failure paths:** unverified callback → no credit (never trust client claim, `BR-PAY-03`); bank reference not matched → credit withheld (`BR-PAY-04`); frozen wallet cannot top up (`BR-PAY-09`); out-of-bounds amount → rejected (`BR-PAY-02`); duplicate callback → idempotent (`BR-PAY-08`); provider outage → retry ×3 then DLQ + alert (`BR-PLT-02`).

## BP-11 — Commission & Vendor Payout

- **Trigger:** escrow hold matures (7 days after `DELIVERED`). **Actor:** System executes; Finance/Admin oversee.
- **Steps:** 1) release check: 7 days elapsed AND no dispute AND state ∉ {DISPUTED, RETURN_*, REFUNDED}; 2) commission = line subtotal after coupon discount × tier rate (5–20%, default 10%) computed at release; 3) vendor payable credited; 4) payout batched 3–7 business days, min 1,000 YER (below rolls over); 5) KYC + store-status gate; 6) monthly statement issued.
- **Systems:** B07 Escrow/Commission/Payouts, B11 Analytics (statements), BullMQ jobs.
- **Rules:** `BR-ESC-01…08`, `BR-FIN-03/04/05`, `C-10`, `C-12`, `BR-ORD-07`.
- **Final state:** sub-order `COMPLETED`; commission booked; payout executed or rolled over.
- **Failure paths:** dispute active → no release (`BR-ESC-02`); refund later → proportional commission reversal (`BR-ESC-04`); escrow insufficient for refund → vendor payable drawn (`BR-ESC-07`); KYC not approved / store suspended → payout withheld (`BR-ESC-06`); reconciliation mismatch → alert finance (`BR-ESC-08`).

## BP-12 — Coupon Creation & Redemption

- **Trigger:** admin creates a platform coupon or vendor creates a store coupon; customer applies at checkout. **Actor:** Admin/Vendor create; Customer redeems; System validates.
- **Steps:** 1) define code, type (percentage / fixed / free shipping / buy-X-get-Y), validity ≤90 days, optional min order amount, per-user and global limits; 2) vendor coupons remain listable/disableable by admin; 3) customer applies one coupon at checkout; 4) totals recalculated server-side; 5) invalid → error before order creation.
- **Systems:** B12 Content & CMS (coupon engine), B05 Checkout, B11 Analytics (usage).
- **Rules:** `BR-PRM-01…06`, `BR-CRT-04`, `BR-FIN-01` (VAT on subtotal − discount), `BR-ESC-03` (commission base excludes discount).
- **Final state:** discount applied once to the order; usage counters incremented; **or** no order row at all if invalid.
- **Failure paths:** stacking attempt → rejected (`BR-PRM-02`); expired/fully-used → rejected before order creation (`BR-PRM-04`, `BR-PRM-06`); discount >90% of order value → invalid (`BR-PRM-01`).

## BP-13 — Review Submission

- **Trigger:** buyer writes a review after delivery. **Actor:** Customer; Vendor responds; Moderator/Admin moderate.
- **Steps:** 1) eligibility check (purchasing customer, `DELIVERED`, within 30 days); 2) one review per order item, rating 1–5, ≤5 images ≤5 MB; 3) vendor may respond once; 4) buyer may edit once within 7 days; 5) store rating recomputed incrementally by job.
- **Systems:** B02 Reviews, B04 Search/storefront display, B10 Notifications, BullMQ recompute job.
- **Rules:** `BR-REV-01…05`, `BR-CAT-06` (visibility), `BR-PLT-01/02` (job queue).
- **Final state:** visible review; store rating updated with count shown.
- **Failure paths:** not-yet-delivered or window elapsed → blocked (`BR-REV-01`); second review → rejected (`BR-REV-02`); abuse/inappropriate → Moderator/Admin hides with audit entry (`BR-REV-04`); image >5 MB or wrong count → rejected (`BR-REV-03`).

## BP-14 — Content Moderation

- **Trigger:** review flag, reported content, or automated flag. **Actor:** Moderator (`ACT-06`) / Admin (`ACT-04`); System auto-flags.
- **Steps:** 1) flag raised (user report / auto); 2) moderator reviews content in context; 3) hide/remove or approve; 4) audit entry written (actor, action, entity, before/after); 5) vendor/customer notified if action taken.
- **Systems:** B13 Admin console, B02 Reviews, B12 CMS, audit log.
- **Rules:** `BR-REV-04`, `BR-PLT-06`, `BR-PLT-05`, `BR-VND-07` (store scoping).
- **Final state:** content hidden or restored; audit trail complete.
- **Failure paths:** disputed moderation → Admin escalation (admin is final arbiter per `BR-RET-06` pattern); scope beyond own store → denied (`BR-VND-07`).

## BP-15 — Support Ticketing

- **Trigger:** customer/vendor issue, code-lockout event, or escalation from another process. **Actor:** Customer/Vendor raise; Support/Admin/Moderator resolve; System auto-creates on lockout.
- **Steps:** 1) ticket created (origin, entity refs, severity); 2) auto-created tickets on 3rd failed delivery code (`BR-SHP-03`) and admin-review escalations (`BR-SHP-06`, `BR-ORD-10`); 3) agent views full order/timeline context (scoped by `BR-ORD-09`); 4) resolve → close with resolution code; 5) escalations reach Admin.
- **Systems:** B13 Admin (support tools, `FR-020`), B06 Orders (timeline), B10 Notifications.
- **Rules:** `BR-SHP-03/06`, `BR-ORD-09/10`, `BR-PLT-06`, `BR-NTF-04`.
- **Final state:** ticket closed with resolution; related lockout lifted when the 24 h period expires.
- **Failure paths:** no AI chatbot — human ticketing only (scope decision, `FR-020`); unresolved disputes → BP-09; context insufficient (no GPS) → rely on code + timeline evidence (`C-16`).

## Process Interaction Map (selected)

```text
BP-03 (register) ──► BP-04 (search→checkout) ──► BP-05 (fulfill) ──► BP-06 (deliver)
                                                                     │
                              ┌──────────────────────────────────────┤
                              ▼                                      ▼
                        BP-08 (return) ◄── BP-09 (dispute)     BP-11 (escrow→payout)
                              │                                      ▲
                              └──► BP-07 (cancel/refund) ────────────┘
BP-10 (top-up) ──funds──► BP-04 wallet payment        BP-12 (coupon) ──discounts──► BP-04
BP-01 (KYC) ──gates──► BP-02 (listing) ──gates──► BP-04 discovery
BP-13 (review) / BP-14 (moderation) / BP-15 (ticketing) ──support every stage
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version (15 processes) | Initial analysis |
