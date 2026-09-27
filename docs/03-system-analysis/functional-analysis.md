---
document_id: DOC-SA-004
title: Functional Analysis by Block (B01–B13)
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-004, FR-007, FR-009, FR-010, FR-011, FR-012, FR-013, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-002, DOC-SA-010, DOC-SA-007]
---

# Functional Analysis (Methodology §11)

Per-block analysis of what the system does: for each of the 13 blocks (`B01…B13`, `DOC-OVR-002`) it maps the owning `FR-*` IDs to behavior, the validations that gate that behavior, the processing logic applied, and the outputs produced. Rules are referenced by ID only — definitions live in `business-rules.md` (DOC-BA-005); requirement statements live in `02-requirements/` (DOC-REQ-001).

**Reading key:** *Validations* = preconditions checked before the behavior commits. *Processing* = what the system computes/does. *Outputs* = observable results (state, data, notifications). Every block's outputs feed other blocks — cross-block handoffs are named at the end of each section.

## B01 — Identity & Access (`FR-001`, `FR-002`, `FR-003`)

| Aspect | Analysis |
|---|---|
| Behavior | Registration by phone + password with OTP verification; login; password reset via OTP; profile/address management; role & permission administration; session/device lifecycle |
| Validations | Phone matches `^7[0-9]{8}$` and is unique (`BR-AUTH-01`); password complexity ≥8 chars upper/lower/digit (`BR-AUTH-02`); OTP 6 digits / 5 min / 3 attempts with 60 s cooldown and ≤3 resends per 10 min (`BR-AUTH-03`); ≤10 addresses, ≤5 device sessions (`FR-003`, `BR-AUTH-06`); RBAC + ownership on every request (`SEC-REQ-004`) |
| Processing | bcrypt cost-12 hash on set/change; session family tracking with single-use refresh rotation (`BR-AUTH-05`); failed-login counter → 15-min lock at 5 (`BR-AUTH-04`); password reset revokes all sessions (`BR-AUTH-07`); OTP dispatch through B10 with provider failover (`BR-NTF-03`) |
| Outputs | Verified account; JWT access 15 min / refresh 7 days (`C-08`); active sessions list; roles (`ACT-01…ACT-06` mapping); lock events logged; security notifications (non-disableable, `BR-NTF-02`) |
| Handoffs | Authenticated identity → every block; RBAC decisions consumed by B03/B06/B07/B13; account lockout feeds B10 notifications |

## B02 — Product Catalog (`FR-004`, `FR-005`, `FR-006`)

| Aspect | Analysis |
|---|---|
| Behavior | Product/variant/category/attribute CRUD with images; stock ledger with reservation TTL; reviews and ratings |
| Validations | Publishable product needs Arabic name, YER price, category, ≥1 image, stock ≥0, a store (`BR-CAT-01`); ≤5 variant dimensions / ≤50 combinations, SKU unique per store (`BR-CAT-02`); category depth ≤5 (`BR-CAT-03`); price >0, sale < original, order totals 500–5,000,000 YER (`BR-CAT-04`, `C-14`); physical goods only (`BR-CAT-05`); images ≤10, ≤5 MB, jpg/png/webp, EXIF stripped (`BR-CAT-08`, `SEC-REQ-011`); review only by buyer after DELIVERED within 30 days, 1 per item, editable once in 7 days, rating 1–5, ≤5 images (`BR-REV-01…03`) |
| Processing | Soft-delete products; only ACTIVE visible (`BR-CAT-06`); stock integer ≥0 with atomic deduction and 15-min reservation expiry (`BR-CAT-07`, `C-13`); reservation granted by B05 at cart/checkout, permanent deduction at payment; review moderation by B13; store rating recomputed incrementally by a background job (`BR-REV-05`) |
| Outputs | Catalog entities for B04 search indexing; availability signal to B05; review feed to storefront; moderation flags to B13 |
| Handoffs | Stock reserve/release API consumed by B05/B06; product search documents pushed to B04; review content subject to B13 moderation |

## B03 — Store Management (`FR-007`, `FR-008`)

| Aspect | Analysis |
|---|---|
| Behavior | Vendor registration, KYC document submission and decisioning, store profile/branding/zones/operating settings, staff roles, follower feature |
| Validations | No product publishing before KYC = APPROVED (`BR-VND-01`); one store per vendor (`BR-VND-02`); KYC decision within 48 h (`BR-VND-03`); staff role changes only by Owner (`BR-VND-06`); every vendor query scoped by `store_id` (`BR-VND-07`) |
| Processing | Document intake with type/size/malware validation (`SEC-REQ-011`); suspension hides products, blocks new orders, freezes existing orders, holds payouts (`BR-VND-04`); follower subscriptions generate B10 notifications for new products/offers (`BR-VND-05`) |
| Outputs | KYC status gate consumed by B02 and B07; store entity with zones feeding B08 shipping; follower list for B10/B11 |
| Handoffs | Approval unlocks B02 publishing; store suspension state consulted by B06 (order blocking), B07 (payout hold), B04 (hiding) |

## B04 — Search & Discovery (`FR-009`)

| Aspect | Analysis |
|---|---|
| Behavior | Arabic-aware full-text search, filters, sorting, category browse, banner/deal merchandising surfaces |
| Validations | Only ACTIVE, in-policy products returned (`BR-CAT-06`); vendor zone/shipping eligibility applied before display; personalized content limited to non-security categories |
| Processing | Query understanding with Arabic normalization; faceted filtering by category/price/store/rating; ranking blends relevance and merchandising boosts from B12; graceful fallback to category browse if search is degraded (`NFR-007`) |
| Outputs | Result lists and PDP entry points for B05; impression/click signals for B11 |
| Handoffs | Consumes catalog documents from B02 and merchandising rules from B12; results link into B05 cart actions |

## B05 — Cart & Checkout (`FR-010`, `FR-011`)

| Aspect | Analysis |
|---|---|
| Behavior | Multi-vendor cart with guards; guest cart merge; 7-step checkout (address → shipping → wallet payment → review → confirm); idempotent order creation |
| Validations | ≤50 distinct products, ≤10 units/product, ≤5 vendors (`BR-CRT-01`, `C-15`); inactive/out-of-stock/out-of-policy items block checkout until removed (`BR-CRT-05`); server-side total recalculation with price-change re-confirmation (`BR-CRT-04`); wallet balance ≥ total at confirmation (`BR-CRT-06`, `C-01`); order total within 500–5,000,000 YER (`C-14`); coupon valid, non-stackable, ≤90% discount (`BR-PRM-01…04`, `BR-PRM-06`) |
| Processing | Reserve stock with 15-min TTL on add/refresh (`BR-CRT-02`, `C-13`); compute VAT = 15% × (subtotal − discount), shipping untaxed (`BR-FIN-01`); compute sub-order totals and round half-up per sub-order (`BR-FIN-02`, `BR-FIN-05`); on confirm — debit wallet, create master + sub-orders with idempotency key (`BR-ORD-06`, `BR-PLT-03`) in a saga with compensating actions (`BR-PLT-04`) |
| Outputs | Reserved stock; created master/sub-orders in `PLACED`; escrow funding entry; B10 confirmation notification; B04 cart count |
| Handoffs | Calls B02 for stock, B07 for payment, B06 for order creation, B08 for fee quote, B10 for notify, B02 for stock restore on failure |

## B06 — Order Management (`FR-012`)

| Aspect | Analysis |
|---|---|
| Behavior | Master/sub-order lifecycle over exactly 17 states, transitions with guards, timelines, actor-specific actions |
| Validations | Only transitions in the canonical table of `state-transitions.md` (`BR-ORD-01`, `C-09`); customer cancel only while PLACED/CONFIRMED, vendor/admin until READY_FOR_PICKUP (`BR-ORD-04`); DELIVERED only via 6-digit code (`BR-ORD-08`, `C-16`); timeline visibility scoped (`BR-ORD-09`); master COMPLETED only when all sub-orders COMPLETED or REFUNDED (`BR-ORD-07`) |
| Processing | Optimistic locking on `version`; append-only `order_status_history` with actor/timestamp/reason (`BR-ORD-03`); master aggregates sub-orders (payment & escrow at master level, fulfillment & payout per sub-order, `C-10`); 24-h CONFIRMED escalation with notification (`BR-ORD-10`); cancellation triggers refund flow and stock restoration |
| Outputs | Order state changes; history rows; notifications to buyer/vendor/courier; escrow freeze on dispute (`BR-ORD-05`) |
| Handoffs | State changes drive B07 (escrow/refund), B08 (fulfillment), B09 (returns), B10 (notifications), B11 (analytics), B13 (dispute/audit) |

## B07 — Payment & Wallet (`FR-013`, `FR-014`)

| Aspect | Analysis |
|---|---|
| Behavior | Wallet balance, top-ups (mobile wallet + bank transfer), order payments, double-entry ledger, escrow hold/release, commission, payouts, refunds, freezes |
| Validations | Wallet-only payment (`BR-PAY-01`, `C-01`); top-up 1,000–5,000,000 YER (`BR-PAY-02`); credit only on verified callback/poll (`BR-PAY-03`) or admin-verified bank reference (`BR-PAY-04`); balance never negative under row locking (`BR-PAY-05`); frozen wallet can receive refunds but not pay/top up (`BR-PAY-09`); payout requires KYC approved and non-suspended store (`BR-ESC-06`) |
| Processing | Every balance change posts balanced debit+credit rows, append-only (`BR-PAY-06`, `DATA-REQ-007`); escrow funded at `PLACED`, held 7 days from DELIVERED (`BR-ESC-01`, `C-12`), released only when elapsed and no dispute/return/refund (`BR-ESC-02`); commission = line subtotal after coupon × per-vendor rate 5–20% (default 10%) computed at release (`BR-ESC-03`); payout batched 3–7 business days after release, min 1,000 YER rollover (`BR-ESC-05`); refunds draw escrow first then vendor payable (`BR-ESC-07`); idempotency on payment/top-up/refund (`BR-PAY-08`, `BR-PLT-03`) |
| Outputs | Wallet balance & statement; ledger postings; escrow state; commission records; payout batches; refund credits (≤3 business days for returns, `BR-RET-04`) |
| Handoffs | Payment result unblocks B06 order creation; ledger data feeds B11 and `BR-FIN-03` reconciliation; refund credits B09/B06 outcomes; provider calls isolated behind adapters (`INT-REQ-008`) |

## B08 — Shipping & Delivery (`FR-015`)

| Aspect | Analysis |
|---|---|
| Behavior | Shipping zones and fee calculation, courier assignment, pickup → transit → out-for-delivery, 6-digit code confirmation, failed-attempt handling |
| Validations | Fee = f(zone, weight, method), free with `free_shipping` coupon (`BR-SHP-01`); assignment offered only to eligible same-zone couriers, first accept wins under optimistic locking (`BR-SHP-04`); code attempts ≤3 then 24-h lock + support ticket (`BR-SHP-03`, `SEC-REQ-005`); no GPS requested or stored (`BR-SHP-05`, `C-16`); domestic destinations only (`C-17`) |
| Processing | Issue 6-digit code at OUT_FOR_DELIVERY (`BR-SHP-02`); verify entry to reach DELIVERED (`BR-ORD-08`); failed attempt returns to transit until 3rd, then escalates to admin review with timeline (not a new state, `BR-SHP-06`); proof = code + timestamp + courier identity, optional photo (`BR-SHP-07`) |
| Outputs | Shipment and assignment records; code issuance to buyer via B10; DELIVERED state; escalation ticket to B13 |
| Handoffs | Reads readiness from B06; writes outcomes back to B06; uses B10 for code delivery; assignments visible to `ACT-03` courier app |

## B09 — Returns & Refunds (`FR-016`)

| Aspect | Analysis |
|---|---|
| Behavior | Return request inside policy window, approval/rejection, pickup, inspection, wallet refund |
| Validations | Window = delivery confirmation + `returnPeriodDays`; `isReturnable=false` or window elapsed → rejected (`BR-RET-01`, `C-11`); only purchasing customer within window (`BR-RET-01`); state sequence must follow the 5 return states of the 17-state machine (`BR-RET-02`, `C-09`) |
| Processing | Vendor/admin decision within 48 h (auto-escalate to admin after 48 h per `state-transitions.md`); inspection conclusion within 72 h else auto-approve (`BR-RET-05`); refund = item value, shipping only if platform/vendor fault (`BR-RET-03`); wallet credit ≤3 business days (`BR-RET-04`); proportional commission reversal and escrow adjustment (`BR-RET-07`, `BR-ESC-04`, `BR-ESC-07`); admin is final arbiter where policy and dispute conflict (`BR-RET-06`) |
| Outputs | Return state progression; refund ledger postings; notifications; audit entry for admin decisions (`BR-PLT-06`) |
| Handoffs | Freezes escrow via B06/B07; return pickup reuses B08; outcome closes dispute path in B13 |

## B10 — Notifications (`FR-017`)

| Aspect | Analysis |
|---|---|
| Behavior | Multi-channel fan-out (SMS, WhatsApp, in-app, push), template management, preference centers, security notices |
| Validations | No email channel in v1 (`BR-NTF-01`, `GAP-03`); security notifications cannot be disabled (`BR-NTF-02`); templates exist in Arabic and English (`BR-NTF-04`, `C-24`); per-category, per-channel opt-out honored for marketing (`BR-NTF-05`) |
| Processing | Recipient preference resolution → template render (locale) → channel dispatch; OTP: SMS primary with automatic WhatsApp failover (`BR-NTF-03`, `INT-REQ-003`); failures queued with retry/DLQ (`BR-PLT-01`, `BR-PLT-02`); receipts logged for audit |
| Outputs | Delivered/failed message records; in-app inbox; delivery receipts; provider cost/volume metrics for B11 |
| Handoffs | Invoked by every block; provider adapters per `INT-REQ-008`; provider contracts are `DEP-05`/`DEP-06` |

## B11 — Analytics & Reporting (`FR-018`)

| Aspect | Analysis |
|---|---|
| Behavior | Admin and vendor dashboards; sales, finance and operations reports; export |
| Validations | Admin vs vendor data scopes enforced (`BR-VND-07`, `SEC-REQ-004`); report windows bounded; exports exclude PII not needed for the report (`DATA-REQ-002`) |
| Processing | Aggregation jobs read from B06/B07/B02/B08 histories; monthly vendor statements (sales, commission, refunds, payouts, adjustments, `BR-FIN-04`); reconciliation views from `BR-FIN-03`/`BR-ESC-08`; trend materialization on schedule |
| Outputs | Dashboards, tables, exports (CSV), reconciliation alerts to finance |
| Handoffs | Read-mostly consumer of all blocks; never writes domain state; feeds B13 with anomaly signals |

## B12 — Content & CMS (`FR-019`)

| Aspect | Analysis |
|---|---|
| Behavior | Static pages, banner placement, coupon engine, featured/deal merchandising |
| Validations | Coupon: unique code, validity ≤90 days, discount ≤90%, one per order, optional `min_order_amount`, per-user/global usage limits (`BR-PRM-01…04`); invalid coupon → error and no order row (`BR-PRM-06`); coupon types percentage / fixed / free shipping / buy-X-get-Y (`BR-PRM-05`); platform vs store scoping (`BR-PRM-03`) |
| Processing | Banner scheduling and locale variants; merchandising boosts handed to B04; coupon application at checkout recalculation in B05; admin can disable any store coupon (`BR-PRM-03`) |
| Outputs | Published pages/banners; validated coupon applications; merchandising configuration |
| Handoffs | Consumed by B04 (displays), B05 (redemption), B13 (moderation/oversight), B11 (campaign performance) |

## B13 — Platform Administration (`FR-020`)

| Aspect | Analysis |
|---|---|
| Behavior | Admin console, platform settings, audit logging, support tickets, dispute handling, role management, content moderation oversight |
| Validations | Server-side RBAC on every privileged action (`SEC-REQ-004`); privileged and money actions require audit entries with before/after (`BR-PLT-06`, `SEC-REQ-010`); settings changes validated against constraint register (`C-01…C-26` are not runtime-configurable) |
| Processing | Dispute lifecycle: open → escrow freeze (`BR-ORD-05`) → evidence review → resolution writing to COMPLETED or REFUNDED (`state-transitions.md`); support tickets with human-only handling (`FR-020`); KYC queue (B03) and bank top-up queue (B07) adjudication; DLQ depth alert triage (`BR-PLT-02`) |
| Outputs | Decisions with audit trail; settings effective immediately; tickets and escalations; role grants (`UC-037`) |
| Handoffs | Consumes queues from every block; decisions feed B06 (dispute resolution), B07 (top-up credit, payout hold), B02/B12 (moderation) |

## Cross-Block Summary

| Flow | From → To | Trigger | Governing rules |
|---|---|---|---|
| Reserve / release stock | B05/B06 → B02 | cart add, TTL expiry, cancel | `BR-CRT-02`, `BR-CAT-07`, `C-13` |
| Pay → create order | B05 → B07 → B06 | checkout confirm | `BR-PAY-01`, `BR-ORD-06`, `BR-PLT-03/04` |
| Fulfill → deliver | B06 → B08 → B06 | vendor ready, code verified | `BR-SHP-02/04`, `BR-ORD-08` |
| Deliver → settle | B06 → B07 | DELIVERED + 7 days | `BR-ESC-01/02`, `BR-ESC-05` |
| Return → refund | B09 → B06/B07/B08 | return request | `BR-RET-01…07` |
| Dispute → freeze | B13 → B06/B07 | dispute raised | `BR-ORD-05`, `BR-ESC-02` |
| Everything → notify | any → B10 | domain events | `BR-NTF-01…05`, `INT-REQ-003/004` |
| Everything → report | B06/B07/B02/B08 → B11 | schedule / request | `BR-FIN-03/04`, `BR-ESC-08` |
| Everything → audit | privileged/money actions → B13 | every such action | `BR-PLT-06`, `SEC-REQ-010` |

## Verification

Each block section is checked by: requirement coverage (`19-traceability/` maps `FR-* → BR-* → block`), negative tests for every listed validation (`13-testing/`), and the constraint tests `TST-CON-01…TST-CON-26` for the constraints cited here. Endpoint-level verification uses the API groups that will be registered in `07-api/` (e.g. the top-up group `API-TOP-*` cited by `C-05`); data-level verification uses schemas `b01…b13` registered in `08-database/`. Behavioral sequences for the five headline flows are in `sequence-flows.md` (DOC-SA-007).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
