---
document_id: DOC-SA-006
title: Logical Components
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-002, FR-011, FR-012, FR-013, FR-017, FR-020]
related_documents: [DOC-OVR-002, DOC-SA-004, DOC-SA-005, DOC-ARCH-004, DOC-ARCH-006, DOC-BA-005]
---

# Logical Components

Technology-independent components derived from the 13 blocks (`B01…B13`). A **logical component** is a bundle of behavior with a named responsibility, a set of interfaces it provides, and a set of interfaces it requires — no framework, language, or process implied. The NestJS module realization of these components is in `../../04-architecture/core/component-view.md` (DOC-ARCH-004); allowed dependencies between the realized modules are in `../../04-architecture/core/module-boundaries.md` (DOC-ARCH-006).

## 1. Component Inventory

| ID | Logical component | Derivation | Primary responsibility |
|---|---|---|---|
| LC-01 | Identity & Access | B01 | Accounts, credentials, OTP lifecycle, sessions, RBAC evaluation |
| LC-02 | Catalog | B02 | Products, variants, categories, attributes, publication state |
| LC-03 | Inventory | B02 | Stock levels, reservations, TTL expiry, atomic deduction |
| LC-04 | Reviews | B02 | Post-delivery reviews, ratings, vendor responses, moderation hooks |
| LC-05 | Store & Vendor | B03 | Vendors, KYC workflow, storefront configuration, staff roles, followers |
| LC-06 | Discovery | B04 | Query processing, filtering, ranking, browse, merchandising presentation |
| LC-07 | Cart | B05 | Cart contents, guards, guest merge, reservation countdown |
| LC-08 | Checkout | B05 | 7-step session, pricing/VAT computation, coupon application, order request assembly |
| LC-09 | Order Lifecycle | B06 | 17-state machine, master/sub aggregation, timelines, transitions, escalations |
| LC-10 | Wallet | B07 | Balance, top-ups, debits/credits, freezes, statements |
| LC-11 | Ledger | B07 | Double-entry postings, invariants, reconciliation inputs |
| LC-12 | Escrow & Commission | B07 | Holds, maturity guards, release, commission computation and reversal |
| LC-13 | Payout | B07 | Payable balances, batch windows, minimum threshold rollover |
| LC-14 | Shipping & Delivery | B08 | Zones, fees, assignments, shipment progress, delivery-code verification |
| LC-15 | Returns | B09 | Return windows, requests, decisions, inspection SLAs, refund triggers |
| LC-16 | Notification | B10 | Templates, preferences, channel fan-out, delivery receipts |
| LC-17 | Analytics & Reporting | B11 | Aggregation, dashboards, statements, exports |
| LC-18 | Content & Promotion | B12 | Pages, banners, coupon engine, featured/deal configuration |
| LC-19 | Administration & Audit | B13 | Settings, audit trail, support tickets, dispute handling, moderation oversight |
| LC-20 | Identity Provider Interface | cross-cutting (B01) | The verification seam used by LC-01 to reach SMS/WhatsApp for OTP (`SEC-REQ-001`) |
| LC-21 | Payment Provider Interface | cross-cutting (B07) | The seam to m-Floos/OneCash for top-up initiate/verify (`INT-REQ-001`, `INT-REQ-008`) |
| LC-22 | Messaging Provider Interface | cross-cutting (B10) | The seam to SMS/WhatsApp/push providers with failover (`INT-REQ-003/004`) |
| LC-23 | Job & Schedule Engine | cross-cutting | Timers, background work, retries — realization mandated as BullMQ (`C-20`, `BR-PLT-01`) |
| LC-24 | Audit Interceptor | cross-cutting (B13) | Captures privileged/money actions into the append-only trail (`BR-PLT-06`, `SEC-REQ-010`) |

> LC-20/21/22 are *interfaces, not vendors*: each hides provider specifics so domain logic never depends on a specific provider type (`INT-REQ-008`).

## 2. Responsibilities and Interfaces

### LC-01 Identity & Access
- **Provides:** `register()`, `verifyOtp()`, `login()`, `refreshSession()`, `resetPassword()`, `evaluatePermission(actor, action, resource)`, `listSessions()/revokeSession()`, `manageAddresses()` (≤10 per `FR-003`).
- **Requires:** LC-22 (OTP dispatch), LC-24 (lock/reset audit), LC-19 (role definitions).
- **Invariants:** unique phone (`BR-AUTH-01`); ≤5 sessions (`BR-AUTH-06`); single-use refresh rotation (`BR-AUTH-05`); password reset revokes all sessions (`BR-AUTH-07`).

### LC-02 Catalog / LC-03 Inventory / LC-04 Reviews
- **Provides (Catalog):** `createOrUpdateProduct()`, `publish()/softDelete()`, `getVisibleProducts()`, `getForCheckout(ids)`.
- **Provides (Inventory):** `reserve(items, ttl=15m)`, `release(reservationId)`, `deduct(orderId)`, `restore(orderId)`, `expireDueReservations()`.
- **Provides (Reviews):** `submit(review, orderItem)`, `respond(vendor)`, `hide(moderator)`, `recomputeStoreRating()`.
- **Requires:** LC-05 (store/KYC gate), LC-19 (moderation), LC-17 (rating aggregates), LC-24 (audit on moderation).
- **Invariants:** stock ≥0, no oversell (`BR-CAT-07`, `C-13`); review only after DELIVERED in window (`BR-REV-01`).

### LC-05 Store & Vendor
- **Provides:** `registerVendor()`, `submitKyc()`, `decideKyc()`, `updateStore()`, `assignStaffRole()`, `follow()/unfollow()`, `isSuspended(storeId)`.
- **Requires:** LC-16 (KYC/follow notifications), LC-24 (audit), LC-19 (queues).
- **Invariants:** one store per vendor (`BR-VND-02`); no listing before APPROVED (`BR-VND-01`); 48-h decision SLA (`BR-VND-03`); `store_id` scoping (`BR-VND-07`).

### LC-06 Discovery
- **Provides:** `search(query, filters, locale)`, `browseCategory(path)`, `applyMerchandising(results)`, `suggest()`.
- **Requires:** LC-02 (documents), LC-18 (banners/boosts), LC-07 (availability signals).
- **Invariants:** only ACTIVE products visible (`BR-CAT-06`); degrades to category browse when index unavailable (`NFR-007`).

### LC-07 Cart / LC-08 Checkout
- **Provides (Cart):** `addItem()`, `changeQuantity()`, `mergeGuestCart()`, `validateGuards()`, `getServerTotals()`.
- **Provides (Checkout):** `startSession()`, `selectAddress/Shipping()`, `quoteTotals()` (VAT 15% per `BR-FIN-01`), `applyCoupon()`, `confirm(idempotencyKey)`.
- **Requires:** LC-03 (reservation), LC-10 (balance/debit), LC-09 (order creation), LC-14 (fee quote), LC-18 (coupon), LC-16 (confirmations).
- **Invariants:** 50/10/5 guards (`BR-CRT-01`, `C-15`); balance ≥ total (`BR-CRT-06`); server totals authoritative (`BR-CRT-04`); invalid coupon ⇒ no order row (`BR-PRM-06`).

### LC-09 Order Lifecycle
- **Provides:** `place()`, `transition(from, to, actor, reason)`, `getTimeline(subject)`, `cancel()`, `aggregateMasterState()`, `escalateStale()`.
- **Requires:** LC-03 (stock restore on cancel), LC-10/12 (refund/escrow), LC-14 (fulfillment), LC-15 (returns), LC-16 (notifications), LC-19 (dispute/audit), LC-23 (timers).
- **Invariants:** exactly 17 states (`BR-ORD-01`, `C-09`); append-only history (`BR-ORD-03`); code-verified DELIVERED (`BR-ORD-08`); master completion rule (`BR-ORD-07`).

### LC-10 Wallet / LC-11 Ledger / LC-12 Escrow / LC-13 Payout
- **Provides (Wallet):** `getBalance()`, `startTopUp()`, `confirmTopUp(verifiedRef)`, `debit(order, key)`, `credit(reason, key)`, `freeze()/unfreeze()`, `statement()`.
- **Provides (Ledger):** `post(pair)`, `assertBalanced()`, `dailyReconciliation()`.
- **Provides (Escrow):** `fund(onDelivered)`, `checkMaturity()`, `release()`, `freeze()/unfreeze()`, `reverseCommission()`.
- **Provides (Payout):** `accumulate(payable)`, `buildBatch()`, `executeBatch()`.
- **Requires:** LC-21 (top-up provider), LC-09 (state guards), LC-19 (admin verification + audit), LC-23 (maturity/batch timers), LC-17 (statements).
- **Invariants:** no negative balance (`BR-PAY-05`); balanced append-only postings (`BR-PAY-06`, `DATA-REQ-007`); 7-day release guards (`BR-ESC-01/02`); 5–20% commission at release (`BR-ESC-03`); payout 3–7 business days, ≥1,000 YER (`BR-ESC-05`).

### LC-14 Shipping & Delivery
- **Provides:** `quoteFee(zone, weight, method)`, `offerToCouriers()`, `accept()`, `recordPickup()`, `recordProgress()`, `issueCode()`, `verifyCode()`, `recordAttempt()`.
- **Requires:** LC-09 (state integration), LC-16 (code issuance), LC-19 (escalation after 3 attempts), LC-05 (store zones).
- **Invariants:** first-accept wins (`BR-SHP-04`); 3 failures ⇒ 24-h lock + ticket (`BR-SHP-03`); no location data (`BR-SHP-05`, `C-16`).

### LC-15 Returns
- **Provides:** `openRequest()`, `decide()`, `recordReceipt()`, `inspect()`, `autoApproveOnTimeout()`, `requestRefund()`.
- **Requires:** LC-09 (return states), LC-10 (refund credit), LC-14 (return pickup), LC-19 (audit/arbiter), LC-23 (72-h timer), LC-16 (notifications).
- **Invariants:** window per `BR-RET-01` (`C-11`); refund ≤3 business days (`BR-RET-04`); 72-h inspection auto-approval (`BR-RET-05`).

### LC-16 Notification
- **Provides:** `send(template, recipient, data, channels)`, `setPreference()`, `render(locale)`, `getReceipts()`.
- **Requires:** LC-22 (dispatch with failover), LC-01 (recipient preferences), LC-18 (locale content).
- **Invariants:** no email (`BR-NTF-01`, `GAP-03`); security sends non-disableable (`BR-NTF-02`); ar/en templates (`BR-NTF-04`, `C-24`).

### LC-17 Analytics / LC-18 Content / LC-19 Administration & Audit
- **Provides (Analytics):** `aggregate(period)`, `vendorDashboard(storeId)`, `adminDashboard()`, `statement(month)`, `export()`.
- **Provides (Content):** `publishPage()`, `scheduleBanner()`, `createCoupon()`, `validateCoupon()`, `disableCoupon()`.
- **Provides (Administration):** `updateSettings()`, `openTicket()`, `resolveTicket()`, `openDispute()`, `ruleDispute()`, `getAuditTrail()`, `assignRole()`.
- **Requires:** all domain components as read consumers; LC-23 for schedules; LC-24 writes its own audit.
- **Invariants:** scope isolation (`BR-VND-07`, `SEC-REQ-004`); coupon rules (`BR-PRM-01…06`); audit append-only (`SEC-REQ-010`).

### LC-23 Job & Schedule Engine
- **Provides:** `enqueue(queueName, payload, options)`, `schedule(delay/cron)`, `retryPolicy` (3× exponential then DLQ), `onDeadLetter()`.
- **Requires:** nothing domain-specific — it is invoked *by* components.
- **Invariants:** queue naming `{block}.{entity}.{action}` (`BR-PLT-01`, `C-20`); DLQ depth alerting (`BR-PLT-02`).

## 3. Interaction Matrix (Providing → Using)

| Provider ↓ / Using → | LC-01 | LC-03 | LC-09 | LC-10/12 | LC-14 | LC-16 | LC-19 | LC-23 |
|---|---|---|---|---|---|---|---|---|
| LC-01 Identity | — | — | authz | authz | authz | recipient prefs | role defs | — |
| LC-03 Inventory | — | — | stock ops | — | — | — | — | TTL expiry |
| LC-09 Order Lifecycle | — | restore | — | refund/escrow | fulfill | notify | dispute | stale-escalate |
| LC-10/12 Wallet & Escrow | — | — | payment guards | — | — | notify | verify/audit | maturity/batch |
| LC-14 Shipping | — | — | delivery events | — | — | issue code | escalate | attempt timers |
| LC-16 Notification | templates | — | — | — | — | — | — | retry |
| LC-19 Administration | roles | moderate | rule disputes | freeze payouts | — | tickets | — | schedules |
| LC-18 Content | — | — | — | coupon at pay | — | campaign notify | — | banner schedule |

Read-only consumers: LC-17 (Analytics) draws from LC-02/09/10/14 without appearing as a user of live transactions; LC-06 (Discovery) reads LC-02 documents and LC-18 boosts.

## 4. Component Rules

1. Components communicate through their named interfaces — no reaching into another component's internal data (the analysis-level form of the module rules in DOC-ARCH-006).
2. Money-touching components (LC-10, LC-11, LC-12, LC-13) are only entered through LC-08/LC-09/LC-15 orchestrations with an idempotency key (`BR-PLT-03`).
3. Provider-facing components (LC-20/21/22) are the only ones allowed to know provider vocabulary (`INT-REQ-008`).
4. Every component that changes privileged or money state emits an audit record via LC-24 (`BR-PLT-06`).
5. The 17-state machine belongs to LC-09 alone — no other component may assign order states (`BR-ORD-01`, `C-09`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
