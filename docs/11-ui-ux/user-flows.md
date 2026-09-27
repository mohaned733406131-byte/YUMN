---
document_id: DOC-UX-002
title: Critical User Flows
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-007, FR-009, FR-010, FR-011, FR-012, FR-013, FR-015, FR-016, FR-017, FR-019, FR-020]
related_documents: [DOC-UX-001, DOC-UX-003, DOC-UC-000, DOC-WF-001, DOC-BA-005, DOC-SA-010, DOC-REQ-001]
---

# Critical User Flows

Nine end-to-end flows as the design-level counterpart of `01-business-analysis/` use cases (`UC-001…UC-040`) and workflows (`WF-001…WF-012`). Steps are numbered; **decision points are marked `D1`, `D2`…** with their branches; rule and requirement IDs are referenced, never restated. State names are the canonical 17 (`C-09`, `DOC-SA-010`).

## Flow Index

| ID | Flow | Primary actor | UC refs | WF refs | Priority |
|---|---|---|---|---|---|
| FL-01 | Registration & login (phone + OTP) | Customer | UC-002, UC-003, UC-004 | WF-001 | P0 |
| FL-02 | Browse → search → PDP → cart → checkout → top-up → confirmation | Customer | UC-001, UC-006, UC-007, UC-009, UC-010, UC-011 | WF-002, WF-003, WF-009 | P0 |
| FL-03 | Order tracking → 6-digit code handoff | Customer | UC-012, UC-013 | WF-005 | P0 |
| FL-04 | Return request → refund | Customer | UC-021 (vendor side) | WF-007 | P0 |
| FL-05 | Vendor: onboarding + KYC → listing → fulfillment → payout view | Vendor | UC-015, UC-017, UC-019, UC-020, UC-022 | WF-011, WF-004, WF-006 | P0 |
| FL-06 | Courier: job offer → pickup → transit → code verify | Delivery Provider | UC-025, UC-026, UC-027, UC-028, UC-029, UC-030 | WF-005 | P0 |
| FL-07 | Admin: KYC approval · dispute resolution · refund approval | Admin | UC-031, UC-033, UC-034 | WF-008 | P0 |
| FL-08 | Coupon apply at checkout | Customer | UC-023 (creation) | WF-012 | P1 |
| FL-09 | Review after delivery | Customer | UC-024 (vendor response) | — | P1 |

---

## FL-01 — Registration & Login (phone + OTP)

Entry: app/web first launch or "تسجيل الدخول / Sign in". Surfaces: S1, S4 (vendor/admin reuse the same identity flow).

1. User enters phone matching `^7[0-9]{8}$` (`BR-AUTH-01`). Inline validation rejects format before submit (`FR-012` usability: explained in locale).
2. **D1 — Existing account?** No → registration form: password per `BR-AUTH-02` (+ confirm field). Yes → password field. Either path sends a 6-digit OTP (5-min expiry, 60 s resend cooldown, ≤3 resends/10 min — `BR-AUTH-03`, `SEC-REQ-001`).
3. OTP screen: 6 separate digit inputs (one accessible field group), auto-advance, auto-submit on 6th digit; countdown renders in locale digits (`DOC-UX-007`).
4. **D2 — OTP result?** Correct within 5 min → session issued, land on account/return-to-`next`. Wrong → inline error with attempts left (3 → 1). Expired → resend action becomes primary. Attempts exhausted → verification blocked, security notice sent (`BR-NTF-02`), support entry shown (FL-07 ties to auto-ticket patterns).
5. **D3 — Session limits?** 6th device login → oldest session ends silently with a notification (`BR-AUTH-06`, `AC-FR001-04`).
6. Lockout branch: 5 consecutive failed logins → 15-min lock screen with countdown and support link (`BR-AUTH-04`).
7. Guest cart (if any) merges on login; server values win on conflict (`BR-CRT-03`).

Success: authenticated on all four customer-facing surfaces within `NFR-012` budget (part of registration → first order < 5 min). Mapped: `UC-002`, `UC-003`, `UC-004`, `WF-001`, `FR-001`, `AC-FR001-01…05`.

## FL-02 — Browse → Search → PDP → Cart → Checkout → Top-up → Confirmation

Entry: home page (`/ar`), category (`/ar/c/{slug}`), search (`/ar/search`), or a banner/deal (`FR-019`).

1. Browse: category tree ≤ 5 levels (`BR-CAT-03`); featured/deal placements render inside admin-configured windows (`AC-FR009-05`).
2. Search: Arabic-normalized query (`FR-009`, `BR-PLT-05`); **D1 — results?** 0 results → recovery panel (spell-out suggestions, clear filters, popular categories — never a dead end, `NFR-012`). Results → facets + sort; **D2 — search unavailable?** (`NFR-007`) → friendly fallback "browse by category" — cart and PDP keep working (`AC-FR009-03`).
3. PDP (`/ar/p/{slug}`): gallery ≤ 10 images (`BR-CAT-08`), price + sale price, store card with rating (`BR-REV-05`), stock/reservation notice, return policy indicator (`C-11`), review list (only after `DELIVERED`, `BR-REV-01`).
4. Add to cart (`UC-009`): **D3 — guards (`C-15`, `BR-CRT-01`)** — 6th vendor → vendor-limit error; 11th unit → unit-limit error; 51st product → product-limit error. Success → mini-cart + 15-min reservation countdown starts (`C-13`, `BR-CRT-02`).
5. Cart (`/ar/cart`): grouped by vendor → sub-order preview; countdown per item; **D4 — price changed since add?** → price-change panel requiring re-confirmation (`BR-CRT-04`). **D5 — ineligible item?** (inactive / out of stock / out of policy) → checkout blocked until removed (`BR-CRT-05`).
6. Checkout (`FR-011`, seven-step session): (1) cart revalidation/reservation → (2) address (≤10, `FR-003`) → (3) shipping method/fee (`BR-SHP-01`; free via `free_shipping` coupon) → (4) wallet payment → (5) review with full breakdown (items − discount + **VAT 15%** + shipping, `BR-FIN-01`, shipping untaxed) → (6) confirm → (7) confirmation.
7. **D6 — wallet balance ≥ total? (`BR-CRT-06`)** No → *insufficient-balance panel*: shortfall shown, primary action "إضافة رصيد / Top up", deep-link to top-up (`FR-013`, `WF-009`), then return to review step with state preserved. Yes → continue.
8. Top-up branch (`WF-009`): choose m-Floos / OneCash / bank transfer (`C-05`); provider flow → pending state until verified callback (`BR-PAY-03`) — bank transfer stays "pending admin verification" (`BR-PAY-04`, `UC-034`). Balance credit posts ledger rows (`BR-PAY-06`).
9. Confirm: idempotency key on (`BR-ORD-06`, `BR-PLT-03`); **D7 — bounds `C-14`** 500–5,000,000 YER enforced; wallet-only (`C-01`, `BR-PAY-01`).
10. Success → confirmation screen: order number, master + per-vendor sub-orders (`C-10`), escrow explanation microcopy (P2, `DOC-UX-001`), delivery estimate, link to tracking (FL-03). **D8 — failure?** → no order row exists, wallet untouched, inline recovery (retry is safe — idempotent).

Mapped: `WF-002`, `WF-003`, `WF-009`, `UC-001/006/007/009/010/011`, `FR-004/009/010/011/013/015/019`, `AC-FR010-*`, `AC-FR011-*`, `AC-FR013-*`.

## FL-03 — Order Tracking → 6-Digit Code Handoff

Entry: order list (`/ar/account/orders`) → detail (`/ar/account/orders/{id}`) or push/SMS deep link.

1. Timeline shows state badge + append-only history with actor and timestamp (`BR-ORD-03`, `BR-ORD-09`).
2. Pre-dispatch states (`PLACED`/`CONFIRMED`): **D1 — cancel allowed?** Only while `PLACED`/`CONFIRMED` for customer (`BR-ORD-04`); after `READY_FOR_PICKUP` the cancel action is hidden with an explanatory tooltip (never a dead button).
3. `OUT_FOR_DELIVERY`: the **6-digit delivery code** panel appears (`BR-SHP-02`, `C-16`) — masked digits with a "show" toggle, copy/share action, and plain-language copy: "Give this code to the courier only when you receive your order." No GPS/map anywhere (`BR-SHP-05`).
4. Courier enters code (FL-06). **D2 — code correct?** → state → `DELIVERED`, escrow 7-day hold starts (`BR-ESC-01`), confirmation celebration + review invitation deferred (FL-09). Wrong → courier sees attempts left (3 → 1, `BR-SHP-03`); customer timeline records the attempt (`BR-ORD-03`).
5. **D3 — 3rd failed attempt** → confirmation locked 24 h, auto support ticket (`BR-SHP-03`, `AC-FR020-02`), customer sees "contact support" with the ticket pre-referenced (FL-07).
6. `DELIVERED` → escrow countdown surfaced ("funds held for seller for 7 days", `C-12`) → `COMPLETED` when released (`BR-ESC-02`) — a `System` transition, still shown in the timeline (`WF-006`).
7. Notifications: state changes push/SMS/WhatsApp per preferences (`FR-017`); in-app notification deep-links back to this screen (`DOC-UX-008`).

Mapped: `UC-012`, `UC-013`, `WF-005`, `FR-012`, `FR-015`, `AC-FR015-02/03/05`.

## FL-04 — Return Request → Refund

Entry: order detail → "طلب إرجاع / Request return" (visible only when eligible).

1. **D1 — eligibility (`C-11`, `BR-RET-01`)**: `isReturnable = false` or past `returnPeriodDays` from delivery → request rejected with the policy reason and, if applicable, a support path. Eligible → form.
2. Select items + reason (required) + optional photos (≤5, ≤5 MB, `BR-REV-03` conventions); shipping-fault toggle shown because shipping refunds only apply when fault is platform/vendor-side (`BR-RET-03`).
3. Submit → state `RETURN_REQUESTED`; customer sees SLA: vendor decision expected within 48 h, auto-escalation to admin after that; inspection window 72 h once received (`BR-RET-05`).
4. **D2 — outcome?** `RETURN_APPROVED` → pickup scheduling (same courier assignment mechanics as FL-06) → `RETURN_RECEIVED` → **D3 — inspection result?** passed (or 72 h elapsed → auto-approve) → `REFUNDED`; wallet credited ≤ 3 business days with a ledger row (`BR-RET-04`, `BR-PAY-06`). Rejected → `RETURN_REJECTED` → back to `COMPLETED` with reason + admin-appeal entry (`BR-RET-06`).
5. Refund microcopy states "to wallet only" (`BR-PAY-07`) and shows commission/escrow adjustment as a system note (vendor-facing, not customer-facing).

Mapped: `WF-007`, `UC-021`, `FR-016`, `AC-FR016-01…04`.

## FL-05 — Vendor: Onboarding + KYC → Listing → Fulfillment → Payout View

Entry: `/ar/vendor/apply` (no store yet).

1. Register account (FL-01) → vendor application: store name, category, zone, contact (`FR-008`; one store per vendor, `BR-VND-02`).
2. KYC submission: document upload (type/size validated, `SEC-REQ-011`), status screen with states DRAFT → SUBMITTED → UNDER_REVIEW → APPROVED / REJECTED (`FR-007`). **D1 — decision ≤ 48 h? (`BR-VND-03`)** SLA badge counts down; overdue cases surface an escalation notice. REJECTED → rejection reason + resubmit under the same SLA (`AC-FR007-04`).
3. **D2 — KYC = APPROVED? (`BR-VND-01`)** Not yet → product creation form is visible but "Publish" is disabled with an explanation; dashboard shows onboarding checklist. Approved → first listing (`UC-017`): Arabic name mandatory (`BR-CAT-01`), price, category (≤5 levels), ≥1 image, stock, SKU unique in store (`BR-CAT-02`), variants ≤5 dimensions (`BR-CAT-02`), physical goods only (`BR-CAT-05`).
4. Listing success → product `ACTIVE` in storefront/search (soft-delete semantics `BR-CAT-06`). **D3 — suspended store? (`BR-VND-04`)** → banner: products hidden, new orders blocked, existing orders frozen, payouts held.
5. Order fulfillment (`WF-004`): new-order inbox (`UC-019`) → accept within SLA (**D4 — SLA breach → `BR-ORD-10` escalation notice, never silent**) → `CONFIRMED` → `PROCESSING` → `READY_FOR_PICKUP` (`UC-020`).
6. Returns: inspection queue with 72 h countdown (`UC-021`, `BR-RET-05`).
7. Finance (`UC-022`, `WF-006`): balance, escrow-held amount with release countdown (7 days from `DELIVERED`, `C-12`), commission tier 5–20% (default 10%, `BR-ESC-03`), payables, payout batches 3–7 business days after release with 1,000 YER threshold and rollover (`BR-ESC-05`), monthly statement (`BR-FIN-04`).

Mapped: `WF-011`, `WF-004`, `WF-006`, `UC-015/017/019/020/022`, `FR-004/005/007/008/014/018`.

## FL-06 — Courier: Job Offer → Pickup → Transit → Code Verify

Entry: courier app (S5) queue tab.

1. Job offer appears for the courier's zone (`BR-SHP-04`): order count, pickup store, destination zone, fee. **D1 — accept?** Accept → optimistic locking; **D2 — won the race?** first accept wins (`AC-FR015-04`) — loser sees "assignment already taken".
2. Pickup at store → verify package → confirm pickup → `PICKED_UP` (`UC-027`).
3. Departure scan → `IN_TRANSIT` → final leg → `OUT_FOR_DELIVERY` (code issued to buyer, `BR-SHP-02`).
4. At the door: ask the customer for the 6-digit code → numeric keypad entry (`UC-030`). **D3 — correct?** → `DELIVERED`, proof = code + timestamp + courier identity, optional photo (`BR-SHP-07`). **D4 — wrong?** → attempts left 2 → 1 shown (`BR-SHP-03`); returns order to `IN_TRANSIT` between attempts (`DOC-SA-010`).
5. **D5 — 3rd failure** → 24 h lock, auto support ticket, order escalates to admin review (`BR-SHP-06`); courier UI shows locked state + history.
6. Failed-attempt recording (`UC-029`) notifies customer per preferences. **No location permission is ever requested** (`C-16`, `BR-SHP-05` — `VERIFIED` by absence of any location affordance).

Mapped: `UC-025…UC-030`, `WF-005`, `FR-015`, `AC-FR015-01…05`.

## FL-07 — Admin: KYC Approval · Dispute Resolution · Refund Approval

Entry: admin console (S3) queues.

1. **KYC queue (`UC-031`)**: cases sorted by SLA age; **D1 — approve/reject?** approve → vendor unlocked (`BR-VND-01`); reject → structured reason required → vendor resubmits (`AC-FR007-04`). Every decision writes an audit entry (`BR-PLT-06`, `SEC-REQ-010`).
2. **Bank top-up verification (`UC-034`)**: submitted reference + proof → **D2 — verified?** credit wallet (`BR-PAY-04`) or reject with reason. Credits are idempotent (`BR-PAY-08`).
3. **Dispute (`WF-008`, `UC-033`)**: customer/vendor raises dispute → `DISPUTED` → escrow frozen for affected sub-orders (`BR-ORD-05`). Evidence panels: order timeline, messages, delivery proof, photos.
4. **D3 — resolution?** resolve for vendor → `COMPLETED`; resolve for buyer → refund flow executes (wallet credit ≤ 3 business days, `BR-RET-04`). Refund approval posts proportional commission reversal (`BR-ESC-04`, `BR-RET-07`) — admin sees a preview of ledger effects before confirming.
5. **Delivery-code lockout escalations**: auto-created tickets (`BR-SHP-03`) land in the support queue with full timeline; support can verify identity and unlock per `GAP-02` policy (admin override currently `INSUFFICIENT EVIDENCE` — see `20-validation/missing-information.md`).
6. All privileged actions are confirmed via explicit dialogs with before/after preview and are audited (`AC-FR020-01`).

Mapped: `UC-031`, `UC-033`, `UC-034`, `WF-008`, `FR-007`, `FR-013`, `FR-016`, `FR-020`, `AC-S-23`.

## FL-08 — Coupon Apply at Checkout

Entry: checkout review step (`FR-011` step 5).

1. Coupon field + "available coupons" list (platform: admin-created; store: vendor-created — `BR-PRM-03`) with applicability hints.
2. Apply (`UC-023` creation is the vendor-side entry): validate — **D1 — valid?** active, within ≤ 90-day window, usage remaining, discount ≤ 90%, `min_order_amount` met (`BR-PRM-01`, `BR-PRM-04`).
3. **D2 — second coupon already applied?** → rejected: coupons never stack (`BR-PRM-02`) with copy "يمكن استخدام قسيمة واحدة فقط / One coupon per order".
4. Valid → discount line appears; totals recalculated server-side (`BR-CRT-04`); VAT base becomes subtotal − discount (`BR-FIN-01`); free-shipping type zeroes shipping (`BR-SHP-01`).
5. **D3 — expired/fully used at confirm?** → validation error, **no order row created** (`BR-PRM-06`), coupon removed, review step re-rendered with reason.
6. Success path continues FL-02 step 9. Notification of discount breakdown appears in order confirmation and order detail.

Mapped: `WF-012`, `UC-023`, `FR-019`, `AC-FR019-01…03`.

## FL-09 — Review After Delivery

Entry: post-`DELIVERED` prompt (in-app card + notification) and order detail.

1. **D1 — eligible? (`BR-REV-01`)**: only the purchasing customer, only after `DELIVERED`, within 30 days of delivery. Not yet delivered → action hidden (not disabled) with explanation.
2. Per order item: integer 1–5 stars, text, ≤5 images ≤5 MB (`BR-REV-03`) — **D2 — invalid input?** inline, locale-named errors (`NFR-012` inline validation rule).
3. **D3 — second review of same item, or edit after 7 days?** → rejected (`BR-REV-02`); one edit window within 7 days.
4. Submit → review visible after moderation checks; store rating recomputes incrementally (`BR-REV-05`).
5. Vendor responds once (`UC-024`, `BR-REV-04`); moderator may hide with audit entry (`UC-038`).

Mapped: `UC-024`, `UC-038`, `FR-006`, `AC-FR006-01…05`.

## Flow-Level Conventions

| Convention | Rule |
|---|---|
| Step granularity | one user action or one system response per step |
| Decision points | always labeled `Dn` with explicit branch outcomes (no implicit "happy path only") |
| Failure exits | named and mapped to a recovery screen in `DOC-UX-005` |
| State names | canonical 17 only (`C-09`); escalations are notifications/tickets, not states (`BR-SHP-06`, `BR-ORD-10`) |
| Money visibility | any step that changes a balance shows the ledger-visible result (P2) |
| Notifications | emitted per preferences (`FR-017`); security notices always (`BR-NTF-02`) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
