---
document_id: DOC-AC-001
title: Acceptance Criteria (Authoritative AC Registry)
category: 02-requirements
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009, NFR-010, NFR-011, NFR-012, NFR-013, NFR-014, NFR-015, NFR-016, NFR-017, NFR-018, NFR-019, NFR-020, SEC-REQ-001, SEC-REQ-002, SEC-REQ-003, SEC-REQ-004, SEC-REQ-005, SEC-REQ-006, SEC-REQ-007, SEC-REQ-008, SEC-REQ-009, SEC-REQ-010, SEC-REQ-011, SEC-REQ-012, DATA-REQ-001, DATA-REQ-002, DATA-REQ-003, DATA-REQ-004, DATA-REQ-005, DATA-REQ-006, DATA-REQ-007, DATA-REQ-008, INT-REQ-001, INT-REQ-002, INT-REQ-003, INT-REQ-004, INT-REQ-005, INT-REQ-006, INT-REQ-007, INT-REQ-008]
related_documents: [DOC-REQ-001, DOC-REQ-002, DOC-NFR-000, DOC-OVR-008, DOC-OVR-011, DOC-BA-005]
---

# Acceptance Criteria — Authoritative AC Registry

**This document is the single, authoritative registry of every acceptance criterion (`AC-*`) in the yumn project.** It is referenced by the functional requirement files (`functional/FR-nnn.md`), by the non-functional files (`non-functional/NFR-nnn.md` via their Verification sections), and by `13-testing/` (which converts ACs into test cases `TC-nnn`) and `19-traceability/` (AC → test mapping). No other document may invent, redefine or contradict an AC listed here; requirement files reference their AC IDs and quote them only in condensed form. The registry defines **253 ACs**: 94 FR + 40 NFR + 50 SR + 32 DR + 33 IR + 4 cross-cutting scenarios.

Requirement IDs themselves remain assigned exclusively in `requirements-overview.md` (`DOC-REQ-001`).

## ID Formats and Rules

| Group | Pattern | Example | Count |
|---|---|---|---|
| Functional | `AC-FRnnn-nn` | `AC-FR013-02` | 94 (FR-001…FR-020, 4–5 per FR) |
| Non-functional | `AC-NFR-nnn-nn` | `AC-NFR-005-01` | 40 |
| Security | `AC-SR001-nn` | `AC-SR004-01` | 50 (SEC-REQ-001…012, 4–5 per SEC-REQ) |
| Data | `AC-DR001-nn` | `AC-DR004-01` | 32 (DATA-REQ-001…008, 4 each) |
| Integration | `AC-IR001-nn` | `AC-IR003-01` | 33 (INT-REQ-001…008, 4–5 per INT-REQ) |
| Cross-cutting scenarios | `AC-XCUT-nn` | `AC-XCUT-02` | 4 |

Rules: every AC is a one-line **Given / When / Then** statement with an objectively observable outcome; an AC is binary (PASS/FAIL — no partial credit); **all** ACs of a requirement must pass for that requirement to be marked `VERIFIED` (per `AC-S-01`/`AC-S-03`); AC IDs are never reused or renumbered.

---

## 1. Functional Requirements — `AC-FR001-01` …

### FR-001 — Identity, Authentication & Session Management

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR001-01 | A phone matching `^7[0-9]{8}$` and a compliant password | Registration is submitted | The account is created UNVERIFIED and a 6-digit OTP valid 5 minutes is dispatched by SMS (C-06, BR-AUTH-01/03) |
| AC-FR001-02 | An account with 5 consecutive failed logins | A further login attempt is made | Login is refused, the account is locked for 15 minutes, and a lock event is recorded (BR-AUTH-04) |
| AC-FR001-03 | A refresh token already used once | The same token is presented again | It is rejected, the entire session family is revoked, and the user is alerted (C-08, BR-AUTH-05) |
| AC-FR001-04 | A user with 5 active device sessions | A 6th device logs in | A new session exists and the oldest session fails on its next request (BR-AUTH-06) |
| AC-FR001-05 | The correct OTP within 5 minutes (or a wrong/expired one) | The OTP is submitted | Correct OTP verifies the phone and issues a session; after 3 failed attempts verification is rejected (BR-AUTH-03) |

### FR-002 — Roles, Permissions & Access Control

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR002-01 | Customer A requests Customer B's order by ID | The API call is processed | 403 is returned and no order data is disclosed (SEC-REQ-004) |
| AC-FR002-02 | Vendor X's staff submits an edit for Vendor Y's product | The request is processed | It is denied by `store_id` scoping at the service layer (BR-VND-07) |
| AC-FR002-03 | A vendor staff member attempts to change their own role to Owner | The change is processed | It is rejected — only the Owner invites, removes or changes staff roles (BR-VND-06) |
| AC-FR002-04 | An admin performs a state-changing privileged action | It completes | An append-only audit entry with actor, action, entity and timestamp exists (BR-PLT-06) |
| AC-FR002-05 | A vendor staff member with role Viewer | They call a vendor write endpoint directly via API | The server responds 403 — frontend guards are bypassed but authorization still holds (SEC-REQ-004) |

### FR-003 — User & Profile Management

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR003-01 | A user who already has 10 saved addresses | An 11th address is submitted | The request is rejected with a limit error and no row is created (addresses ≤ 10) |
| AC-FR003-02 | A user who changes their password with a valid OTP | The change commits | All previously issued sessions are invalid and re-login is required (BR-AUTH-07) |
| AC-FR003-03 | A user with 3 active device sessions | One device is revoked | That device's refresh token fails on next use while the other two remain valid (session management ≤ 5 devices) |
| AC-FR003-04 | A confirmed account deletion | The workflow completes | PII is purged/anonymised while financial records remain retained ≥ 5 years (DATA-REQ-003, NFR-019) |
| AC-FR003-05 | A user editing profile fields on one surface | They save and open another surface | Updated values are visible on all four surfaces within 5 seconds |

### FR-004 — Product Catalog Management

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR004-01 | A product with no Arabic name | Publish is attempted | Validation fails and no ACTIVE product exists (BR-CAT-01) |
| AC-FR004-02 | A variant definition with 6 dimensions | It is saved | Validation rejects it — ≤ 5 dimensions and ≤ 50 combinations, SKU unique within store (BR-CAT-02) |
| AC-FR004-03 | A 12 MB JPEG or any SVG upload | The image is submitted | The upload is rejected — ≤ 5 MB, jpg/png/webp only, EXIF stripped, ≤ 10 images (BR-CAT-08, SEC-REQ-011) |
| AC-FR004-04 | A soft-deleted product | Storefront or search queries run | It never appears in results (BR-CAT-06) |
| AC-FR004-05 | A product violating any catalog rule (price ≤ 0, sale ≥ original, 6th category level, duplicate SKU in store) | It is saved | The specific validation error is returned and no row persists (BR-CAT-02/03/04) |

### FR-005 — Inventory Management

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR005-01 | 3 concurrent checkouts for the last available unit | All are processed | Exactly one succeeds and stock never goes below 0 (BR-CAT-07, C-13) |
| AC-FR005-02 | A reservation created at t0 | 15 minutes pass without payment | The reserved quantity is released automatically and available stock rises again (C-13) |
| AC-FR005-03 | A paid order whose handlers run a second time with the same idempotency key | The handlers run again | Stock is deducted exactly once — permanent deduction happens only on payment (BR-CAT-07, BR-PLT-03) |
| AC-FR005-04 | A paid order that is cancelled | The cancel flow runs | The deducted quantity is restored to available stock within 5 seconds |

### FR-006 — Reviews & Ratings

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR006-01 | An order in CONFIRMED state | The customer submits a review | It is rejected — reviews allowed only after DELIVERED (BR-REV-01) |
| AC-FR006-02 | Delivery 31 days ago | A review is submitted | It is rejected — the 30-day review window has elapsed (BR-REV-01) |
| AC-FR006-03 | A rating of 6 or 6 attached images | The review is submitted | Validation fails and nothing is stored — integer 1–5, ≤ 5 images, ≤ 5 MB each (BR-REV-03) |
| AC-FR006-04 | A review hidden by a moderator | The rating recompute job runs | It is excluded from the average and the visible count, with an audit entry (BR-REV-04/05) |
| AC-FR006-05 | A customer submitting a second review for the same item or editing after 7 days | The submission is processed | It is rejected — one review per order item, one edit within 7 days, one vendor response per review (BR-REV-02/04) |

### FR-007 — Vendor Onboarding & KYC

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR007-01 | A submitted KYC application | 48 hours elapse without a decision | The case is escalated/alerted so the SLA breach is visible (BR-VND-03, OBJ-06) |
| AC-FR007-02 | KYC status ≠ APPROVED | The vendor attempts to publish a product | Publishing is denied (BR-VND-01) |
| AC-FR007-03 | An approved vendor is suspended | Storefront and ordering are exercised | Products are hidden, new orders blocked, existing orders frozen and payouts held (BR-VND-04) |
| AC-FR007-04 | A REJECTED application | The vendor resubmits complete documents | The case re-enters review under the same 48-hour SLA (BR-VND-03) |

### FR-008 — Store Management & Storefront Configuration

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR008-01 | A vendor who already owns a store | A second store creation is submitted | It is rejected — one store per vendor in v1 (BR-VND-02) |
| AC-FR008-02 | A customer following a store | The store publishes a new product | Followers receive a notification subject to their preferences; the vendor sees follower list and count (BR-VND-05) |
| AC-FR008-03 | A suspended store | Its storefront is requested | Its products are hidden and new orders are blocked (BR-VND-04) |
| AC-FR008-04 | A shipping zone outside domestic coverage | It is saved | The configuration is rejected — domestic Yemen fulfillment only (C-17) |
| AC-FR008-05 | Vendor staff with roles Viewer/Editor/Manager | Each exercises its permitted actions | Only permitted actions succeed and only the Owner invites, removes or changes staff roles (BR-VND-06) |

### FR-009 — Search & Discovery

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR009-01 | An Arabic query using variant letter forms (e.g. alef variants) | It is searched | Matching products are returned thanks to Arabic normalization (Arabic-aware analyzer) |
| AC-FR009-02 | A soft-deleted or inactive product | Any search or sort query runs | It never appears in results (BR-CAT-06) |
| AC-FR009-03 | The search cluster unavailable | A customer browses by category | Browsing returns correct products from DB/cache — no hard failure, friendly fallback (NFR-007, DEP-04) |
| AC-FR009-04 | A filter+sort combination | It is applied | Results match all filters, ordering is deterministic, and facet counts equal returned totals |
| AC-FR009-05 | Admin-configured banners/merchandising in an active window | A customer opens the home/category page | Configured banners and featured/deal placements render during the window and disappear after expiry (FR-019) |

### FR-010 — Shopping Cart

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR010-01 | A cart already containing products from 5 vendors | A 6th vendor's product is added | The add is rejected with a vendor-limit error (C-15) |
| AC-FR010-02 | A quantity of 10 for a product | The customer attempts 11 units | The update is rejected — ≤ 10 per product, ≤ 50 products (C-15, BR-CRT-01) |
| AC-FR010-03 | A countdown started at add-to-cart | 15 minutes elapse without checkout | Reserved stock is released and affected items are flagged stale (BR-CRT-02, C-13) |
| AC-FR010-04 | A product price changed after add-to-cart | The customer proceeds to checkout | The new price is shown and requires re-confirmation; totals are recalculated server-side (BR-CRT-04) |
| AC-FR010-05 | An inactive, out-of-stock or out-of-policy item in the cart | Checkout is attempted | Checkout is blocked until the offending item is removed; a guest cart merges on login with server value winning (BR-CRT-05, BR-CRT-03) |

### FR-011 — Checkout & Order Placement

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR011-01 | An order total of 499 YER (or above 5,000,000 YER) | Confirm is attempted | Validation rejects it — order bounds 500–5,000,000 YER (C-14) |
| AC-FR011-02 | A duplicate confirm with the same idempotency key | It is processed | The original order is returned with no second order or wallet debit (BR-ORD-06, BR-PLT-03) |
| AC-FR011-03 | Insufficient wallet balance at confirmation | It is processed | No order is created and no ledger entry posts — balance ≥ total is mandatory (BR-CRT-06) |
| AC-FR011-04 | A cart spanning 3 vendors | The order is placed | 1 master + 3 sub-orders exist and the master total equals the sum of sub-order totals (C-10, BR-ORD-02) |
| AC-FR011-05 | `payment_method != wallet` (COD, card, anything) | Order creation is processed | `PAYMENT_METHOD_NOT_ALLOWED` is returned and no order row exists (C-01, BR-PAY-01) |

### FR-012 — Order Lifecycle Management

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR012-01 | The order state enumeration in code | It is enumerated | Exactly 17 states exist and no others, covered by 17/17 state-machine tests (C-09, BR-ORD-01) |
| AC-FR012-02 | An order in PLACED | A transition to DELIVERED is attempted | It is rejected with 409 STATE_CONFLICT and history is unchanged |
| AC-FR012-03 | An order in READY_FOR_PICKUP | The customer attempts cancellation | It is denied — customer may cancel only while PLACED/CONFIRMED (BR-ORD-04) |
| AC-FR012-04 | All sub-orders COMPLETED or REFUNDED | The master order is evaluated | The master becomes COMPLETED — a sub-order cannot advance past its own vendor's steps (BR-ORD-07) |
| AC-FR012-05 | Any state change by any actor | The order history is queried | `order_status_history` is append-only with actor, timestamp and reason — states are never overwritten (BR-ORD-03) |

### FR-013 — Wallet & Payment Processing

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR013-01 | A top-up request of 999 YER (or above 5,000,000 YER) | It is submitted | It is rejected — top-up bounds 1,000–5,000,000 YER (BR-PAY-02) |
| AC-FR013-02 | A replayed m-Floos callback for an already-credited transaction | It is processed | The wallet is credited exactly once — never on client claim (BR-PAY-03) |
| AC-FR013-03 | A balance of 10,000 YER and a 12,000 YER payment | It is attempted | The payment fails and the balance remains 10,000 YER — never negative, atomic row lock (BR-PAY-05) |
| AC-FR013-04 | An order submission with a non-wallet payment method | It is processed | `PAYMENT_METHOD_NOT_ALLOWED` is returned and no ledger entry posts (C-01, BR-PAY-01) |
| AC-FR013-05 | Any successful balance change (top-up, payment, refund, freeze effect) | The ledger is inspected | Balanced debit + credit rows exist in one ACID transaction and are append-only (BR-PAY-06, DATA-REQ-007) |

### FR-014 — Escrow, Commission & Vendor Payouts

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR014-01 | A sub-order DELIVERED at day 0 with no dispute | Day 7 elapses | Escrow releases to vendor payable automatically, exactly once (C-12, BR-ESC-01/02) |
| AC-FR014-02 | A sub-order in DISPUTED at day 7 | The release job runs | No release occurs until admin resolution (BR-ESC-02, BR-ORD-05) |
| AC-FR014-03 | A 10,000 YER line subtotal after coupon discount at the default 10% rate | Commission is released | Commission posted is 1,000 YER — rate is per-vendor tier 5–20% (BR-ESC-03) |
| AC-FR014-04 | A refund after commission release | The refund executes | Commission is reversed proportionally and escrow/payable are adjusted per BR-ESC-07 (BR-ESC-04) |
| AC-FR014-05 | A released payable ≥ 1,000 YER | The payout batch runs | Payout executes 3–7 business days after release; amounts below the threshold roll over (BR-ESC-05) |

### FR-015 — Shipping & Delivery

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR015-01 | A zone, package weight and method (and an optional `free_shipping` coupon) | The fee is computed | Fee = f(zone, weight, method) and is zero when a free-shipping coupon applies (BR-SHP-01) |
| AC-FR015-02 | An order reaching OUT_FOR_DELIVERY | The buyer is notified | A 6-digit code is issued to the buyer; the courier must enter it to confirm delivery (C-16, BR-SHP-02) |
| AC-FR015-03 | 2 failed code attempts then a 3rd failure | The courier submits again | Remaining attempts are shown on 1–2; the 3rd locks confirmation for 24 h and auto-creates a support ticket (BR-SHP-03) |
| AC-FR015-04 | Two eligible couriers accepting the same delivery simultaneously | Both accepts commit | Exactly one assignment succeeds via optimistic locking (first accept wins) (BR-SHP-04) |
| AC-FR015-05 | The full delivery flow and API contract | GPS/location is requested or stored | No location data is ever requested, stored or returned (C-16, BR-SHP-05) |

### FR-016 — Returns & Refunds

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR016-01 | A product with `isReturnable=false` or a request after `returnPeriodDays` from delivery | The customer requests a return | The request is rejected per policy; window starts at delivery confirmation (C-11, BR-RET-01) |
| AC-FR016-02 | A return in RETURN_APPROVED | Inspection and fulfilment progress | States flow RETURN_REQUESTED → APPROVED/REJECTED → RETURN_RECEIVED → REFUNDED within the 17-state machine (BR-RET-02) |
| AC-FR016-03 | A received return with no vendor inspection for 72 hours | The SLA expires | The return auto-approves (BR-RET-05) |
| AC-FR016-04 | An approved refund | It is executed | The customer wallet is credited within 3 business days and commission/escrow adjust proportionally (BR-RET-04, BR-RET-07) |

### FR-017 — Notifications & Messaging

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR017-01 | Any notification request | The channel set is checked | Only SMS, WhatsApp, in-app and push are used — no email is sent in v1 (BR-NTF-01) |
| AC-FR017-02 | A user who disabled all optional categories | An OTP, login, password-change or lockout event occurs | The security notification is still delivered — it cannot be disabled (BR-NTF-02) |
| AC-FR017-03 | The primary SMS provider timing out or failing | An OTP is requested | Delivery fails over automatically to WhatsApp within the request window (BR-NTF-03, INT-REQ-003) |
| AC-FR017-04 | Templates for every notification type | The locale inventory is checked | Every template exists in Arabic and English and follows the user's locale (Arabic default) (BR-NTF-04) |
| AC-FR017-05 | A user opting out of marketing per channel | A campaign notification is triggered | The opted-out channel receives nothing while other channels/categories remain unaffected (BR-NTF-05) |

### FR-018 — Analytics & Reporting

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR018-01 | A vendor and an admin account | Each opens their dashboards | Vendor sees only its own store data; admin sees platform-wide data (BR-VND-07) |
| AC-FR018-02 | Completed transactions for a period | Sales, finance and operations reports are generated | Totals reconcile to the ledger (sales, commission, refunds, payouts) with zero unexplained variance |
| AC-FR018-03 | A report export request | The user exports | A CSV/XLSX download is produced with correct Arabic/English headers and locale-formatted numbers |
| AC-FR018-04 | The previous business day closed | The next morning arrives | Daily reconciliation and operational reports are available (OBJ-08) |

### FR-019 — Content & Promotions (CMS + Coupons)

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR019-01 | A coupon with validity > 90 days or discount > 90% | It is created | Creation is rejected (BR-PRM-01) |
| AC-FR019-02 | A second coupon submitted on an order that already has one | The second coupon is applied | Application is rejected — coupons never stack (BR-PRM-02) |
| AC-FR019-03 | An expired, fully-used or otherwise invalid coupon | Checkout validation runs | A validation error is returned and NO order row is created (BR-PRM-06) |
| AC-FR019-04 | Static pages, banners and featured/deal merchandising in CMS | A visitor loads the pages | Content renders per configuration in both locales and respects scheduling windows |

### FR-020 — Platform Administration, Settings & Audit

| AC ID | Given | When | Then |
|---|---|---|---|
| AC-FR020-01 | Any privileged or money-moving admin action | It executes | An append-only audit entry records actor, action, entity, before/after, IP and timestamp (BR-PLT-06, SEC-REQ-010) |
| AC-FR020-02 | A 3rd failed delivery-code attempt | The lock engages | A support ticket is auto-created and visible to support staff in the console (BR-SHP-03, AC-S-23) |
| AC-FR020-03 | A customer-raised order dispute | Admin resolution runs | Escrow release freezes for affected sub-orders and the resolution is audited (BR-ORD-05, BR-RET-06) |
| AC-FR020-04 | Platform settings (commission defaults, SLAs, limits) changed by admin | Subsequent transactions run | New settings take effect per documented precedence; role management changes apply immediately and are audited |

---

## 2. Non-Functional Requirements — `AC-NFR-001-01` …

Verification conditions for `non-functional/NFR-nnn.md`; measurement procedures live in `12-non-functional/`.

| AC ID | Requirement | Given | When | Then |
|---|---|---|---|---|
| AC-NFR-001-01 | NFR-001 | k6 read scenario at 10,000 concurrent users | The 30-minute steady-state window is analysed | p95 read latency < 200 ms with error rate < 0.1% (AC-S-05) |
| AC-NFR-001-02 | NFR-001 | k6 write scenario at 10,000 concurrent users | The 30-minute steady-state window is analysed | p95 write latency < 500 ms (p99 ≤ 1,000 ms) with error rate < 0.1% |
| AC-NFR-002-01 | NFR-002 | Lighthouse CI mobile/4G run on home, category, product, checkout | Metrics are scored | LCP < 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 on all four pages |
| AC-NFR-002-02 | NFR-002 | The customer web production build | The bundle budget check runs | Initial JS < 200 KB gzipped and webfonts ≤ 150 KB combined |
| AC-NFR-003-01 | NFR-003 | k6 mixed profile held at 10,000 VUs for 30 minutes | The run completes | All NFR-001 thresholds hold and error rate < 0.1% for the whole window |
| AC-NFR-003-02 | NFR-003 | The same load run | Host/pool/queue metrics are reviewed | CPU < 70%, memory < 75%, pool < 80%, and queues drain to baseline within 5 minutes |
| AC-NFR-004-01 | NFR-004 | 24-hour catalog read traffic with cache metrics enabled | The hit ratio is computed | Hit ratio ≥ 80% on product/category/store read routes with cache-hit p95 < 50 ms |
| AC-NFR-004-02 | NFR-004 | A product/price/stock write committed | Reads are sampled for 5 seconds | The new value is visible ≤ 5 s everywhere and checkout never uses a cache older than 5 s |
| AC-NFR-005-01 | NFR-005 | Rolling 30-day external probe data post-launch | Availability is computed (AC-S-06) | Availability ≥ 99.99% (downtime ≤ 4.32 min/month) |
| AC-NFR-005-02 | NFR-005 | A simulated outage in staging | Probe and alert behaviour is observed | Page fires within 1 minute of 2 failed probes; all critical routes are probed every 60 s |
| AC-NFR-006-01 | NFR-006 | A disaster declared and restore started on a clean host | The drill is timed | Service write-ready within 1 hour (RTO) with ≤ 15 minutes of committed transactions lost (RPO) |
| AC-NFR-006-02 | NFR-006 | Backup jobs interrupted in a staged test | Backup-age monitoring runs | Freshness alerts fire at 15 min (WAL) / 24 h (snapshot) and quarterly drills are scheduled (AC-S-17) |
| AC-NFR-007-01 | NFR-007 | Elasticsearch and Redis containers stopped in staging | The core-journey smoke suite runs | Browse, cart and wallet checkout complete with error rate < 1% and zero data inconsistency |
| AC-NFR-007-02 | NFR-007 | Queue workers stopped and an SMS provider blocked | Jobs/notifications are retried | 3 retries → DLQ with alert within 1 minute; zero lost or duplicated jobs after recovery |
| AC-NFR-008-01 | NFR-008 | Daily reconciliation over 30 simulated days | Ledger totals are asserted | Σ ledger entries = 0 at every point and every posting is balanced double-entry (AC-S-14) |
| AC-NFR-008-02 | NFR-008 | Idempotent replays and concurrency tests executed | Results are tallied | 0 duplicate side effects, 0 negative balances, 0 negative stock, 0 orphan rows (AC-S-15) |
| AC-NFR-009-01 | NFR-009 | Dependency analysis of the full module graph | CI runs on a release PR | 0 cross-module boundary violations and all merged PRs passed lint/type/test gates |
| AC-NFR-009-02 | NFR-009 | Coverage report and doc audit for the release branch | The quality gate is evaluated | Coverage ≥ 80% overall / ≥ 95% payment / ≥ 90% auth; 13 module READMEs present; onboarding change ≤ 5 days (OBJ-10) |
| AC-NFR-010-01 | NFR-010 | The unit suite runs with outbound sockets blocked | CI reports coverage | Suite passes fully offline and meets the 80/95/90 coverage thresholds (AC-S-08) |
| AC-NFR-010-02 | NFR-010 | 10 consecutive CI runs of the regression suite | Timing and reruns are reviewed | Regression < 30 minutes with 0 reruns/flakes across all 10 runs (AC-S-09) |
| AC-NFR-011-01 | NFR-011 | axe-core scans of all customer pages in `ar` and `en` | The report is generated | Automated pass ≥ 95% with 0 critical and 0 serious violations (AC-S-10) |
| AC-NFR-011-02 | NFR-011 | Manual keyboard-only and TalkBack/VoiceOver passes | Core journeys are executed | Registration→order completes without a mouse or sighted UI, with visible focus and correct announcements |
| AC-NFR-012-01 | NFR-012 | Moderated sessions with first-time customers on mid-tier Android/4G | Timings are aggregated | Median registration→first order < 5 min in `ar` with task success ≥ 90% |
| AC-NFR-012-02 | NFR-012 | Moderated sessions with new vendors | Timings and SUS are aggregated | Median time to first published listing < 10 min and SUS ≥ 78 for customer and vendor personas |
| AC-NFR-013-01 | NFR-013 | The i18n key scan and template inventory run in CI | Coverage is compared | 100% of keys present in `ar`/`en`, 0 hardcoded strings, every template in both locales (BR-PLT-05) |
| AC-NFR-013-02 | NFR-013 | RTL visual regression and locale-format tests run | Results are reviewed | 0 RTL defects on core journeys; Arabic-Indic currency/date formatting correct (AC-S-11, BR-PAY-10) |
| AC-NFR-014-01 | NFR-014 | A 1,000-line production log sample and a traced request path | The audit runs | 100% structured JSON with correlation IDs end-to-end; 0 secrets/PII values present |
| AC-NFR-014-02 | NFR-014 | Metric coverage diff and a staged alert drill | Detection and paging are measured | RED metrics cover 100% of endpoints; page ≤ 1 min after trigger, ack ≤ 15 min (AC-S-18) |
| AC-NFR-015-01 | NFR-015 | Playwright cross-browser run (8 desktop/version combinations) | P1 flows are scored | 0 blocking defects on last-2-version Chrome/Safari/Firefox/Edge in both locales |
| AC-NFR-015-02 | NFR-015 | Device-lab pass (Android 10+, iOS 15+, 320–1440 px) | P1 flows are executed on devices | 0 blocking defects, including WhatsApp/SMS webview rendering of core read paths |
| AC-NFR-016-01 | NFR-016 | A clean Docker host and the documented procedure | `docker compose up` runs | Healthy stack + green smoke suite in ≤ 30 minutes with identical image digests across environments |
| AC-NFR-016-02 | NFR-016 | Dependency and infrastructure audit | Cloud-SDK/config references are searched | 0 cloud-vendor proprietary services/SDKs and 0 host-specific values baked into images |
| AC-NFR-017-01 | NFR-017 | Synthetic volume load of 10M products and 100M order lines | k6 and EXPLAIN checks run | p95 within NFR-001 budgets and 0 unexpected sequential scans on hot paths |
| AC-NFR-017-02 | NFR-017 | Schema and retention-job review | Partitioning and retention are verified | 3 high-volume tables partitioned; retention dry-run protects 5-year records; forecast variance ≤ 10% |
| AC-NFR-018-01 | NFR-018 | Scaling test at 1/2/4 API replicas plus a replica-kill test | Efficiency and errors are computed | Scaling efficiency ≥ 80%, 0 failed sessions on replica kill, read-replica lag < 5 s |
| AC-NFR-018-02 | NFR-018 | The 10k→50k scale-out runbook and its staging rehearsal | The runbook is reviewed | Steps are published, reviewed by on-call, and validated at least to the 25k-user step |
| AC-NFR-019-01 | NFR-019 | The VAT boundary test matrix (0/90% discounts, free shipping, split orders) | Tests execute | 100% correct: VAT = 15% × (subtotal − discount), shipping untaxed, shown in every breakdown (BR-FIN-01) |
| AC-NFR-019-02 | NFR-019 | Retention evidence, PDPA checklist and assumption resolutions | Compliance review runs | Financial/audit records retained ≥ 5 years, 100% PDPA controls implemented, sign-offs on file (AC-S-24) |
| AC-NFR-020-01 | NFR-020 | On-call readiness review | Runbooks, health endpoints and config are inspected | Top-10 runbooks exist and rehearsed; `/healthz`+`/readyz` < 1 s; repo/image secret scan clean (AC-S-19) |
| AC-NFR-020-02 | NFR-020 | A staging deploy followed by a rollback | Request errors during the window are measured | Deploy causes 0 failed customer requests (< 0.1% 5xx) and rollback completes ≤ 15 min (AC-S-20) |

---

## 3. Security Requirements — `AC-SR001-01` …

| AC ID | Requirement | Given | When | Then |
|---|---|---|---|---|
| AC-SR001-01 | SEC-REQ-001 | A phone matching `^7[0-9]{8}$` registration submits an OTP flow | Registration completes and wrong, expired or replayed codes are submitted | The account receives a 6-digit OTP valid 5 minutes; wrong, expired and replayed codes are rejected with distinct error codes and no session/token is issued (BR-AUTH-01/03) |
| AC-SR001-02 | SEC-REQ-001 | An OTP verification sequence reaches its attempt and resend limits | A 4th verification attempt, a resend before the 60 s cooldown, or a 4th resend within 10 minutes is submitted | Each is rejected — maximum 3 verification attempts, 60 s resend cooldown, maximum 3 resends per 10 minutes (BR-AUTH-03) |
| AC-SR001-03 | SEC-REQ-001 | Password-reset and sensitive-change endpoints are called with a valid access token but without a valid fresh OTP | The request is processed | The flow blocks — the request is rejected with 401/403/422 and no action completes |
| AC-SR001-04 | SEC-REQ-001 | The API contract is inspected for identity and OTP destinations | Every endpoint is checked | No endpoint accepts an email address as a login identity or OTP destination (BR-AUTH-08, C-06) |
| AC-SR001-05 | SEC-REQ-001 | The primary SMS provider times out while an OTP is requested | Provider failover runs | The OTP is delivered by the second provider and verified inside its 5-minute validity window (BR-NTF-03, INT-REQ-003) |
| AC-SR002-01 | SEC-REQ-002 | The users table is inspected | Password storage is examined | Only bcrypt hashes exist, the cost factor is 12 (confirmed by re-hash), and no plaintext-password column exists in the schema (BR-AUTH-02) |
| AC-SR002-02 | SEC-REQ-002 | The auth-flow test suite has run | Application logs and traces are scanned | Password and OTP values appear in zero log lines — no plaintext password is ever written to logs, traces or error reports |
| AC-SR002-03 | SEC-REQ-002 | A raw database/backup dump is taken | Classified columns (phone numbers, PII, financial fields) are examined | Ciphertext is stored (AES-256); decryption succeeds only through the external key service, never with database credentials alone (SEC-REQ-006/007) |
| AC-SR002-04 | SEC-REQ-002 | A password shorter than 8 characters or missing a required character class is submitted | Registration or password change is processed | The request is rejected with a stable error code (BR-AUTH-02) |
| AC-SR003-01 | SEC-REQ-003 | An RS256 access token at its lifetime boundary | The token is presented at 14:59 and again after 15:00 minutes | It is accepted before expiry and rejected with 401 after the 15-minute lifetime (C-08) |
| AC-SR003-02 | SEC-REQ-003 | A consumed refresh token from a 7-day session family | The same token is replayed | The whole session family is revoked, the user alert is emitted, and both tokens are blocked from further use — single-use rotation (BR-AUTH-05) |
| AC-SR003-03 | SEC-REQ-003 | A user with 5 active device sessions | A 6th concurrent login occurs | The oldest session is evicted and the active session count never exceeds 5 (BR-AUTH-06) |
| AC-SR003-04 | SEC-REQ-003 | Forged tokens (`alg: none`, HS256-signed, signature-stripped) and auth responses | The tokens are presented and cookie flags are inspected | Tampered tokens are rejected and every auth response carries httpOnly and SameSite cookie flags (Secure in production) (C-08) |
| AC-SR003-05 | SEC-REQ-003 | A password reset or change completes | Previously issued tokens are used again | The old refresh token fails immediately and previously issued access tokens are denied at their next authorization check (≤ 15 min propagation, BR-AUTH-07) |
| AC-SR004-01 | SEC-REQ-004 | The API contract and the RBAC matrix for the 7 actors | An automated suite calls every endpoint as each role | Every endpoint returns the expected allow/deny decision — no endpoint is left untested |
| AC-SR004-02 | SEC-REQ-004 | Customer B addressing customer A's order/wallet/reviews, or vendor X querying store Y | The read/write is attempted | It is denied with 403/404 and no data disclosed — ownership keys (`user_id`/`store_id`) scope access at the service layer (BR-VND-07) |
| AC-SR004-03 | SEC-REQ-004 | UI-hidden actions (admin refund, moderator role change) called with a low-privilege token | The call bypasses the frontend and hits the API directly | The server rejects it with identical results via UI or raw HTTP — frontend guards are never the security boundary |
| AC-SR004-04 | SEC-REQ-004 | A request with no/invalid role context, or an endpoint missing an authorization mapping | Authorization is evaluated | The request fails closed (deny-by-default 403/404), never open |
| AC-SR005-01 | SEC-REQ-005 | 5 consecutive wrong passwords | The correct password is submitted within 15 minutes | Login remains refused for the full 15-minute lock and a lock event appears in the logs/audit trail (BR-AUTH-04) |
| AC-SR005-02 | SEC-REQ-005 | 3 failed OTP entries | A 4th entry (or the correct code) is submitted | The attempt is rejected; verification resumes only after a fresh OTP is issued — OTP allows 3 attempts (BR-AUTH-03) |
| AC-SR005-03 | SEC-REQ-005 | 2 failed delivery-code attempts | The courier submits a 3rd wrong code | Confirmation is locked for 24 hours and a support ticket is created automatically (BR-SHP-03) |
| AC-SR005-04 | SEC-REQ-005 | Client-side counters rotated or local state reset; one IP hammering many accounts | The abuse is repeated | Server-side counters are unchanged and per-IP throttling engages — client behaviour cannot raise the effective limit |
| AC-SR006-01 | SEC-REQ-006 | The external TLS configuration | TLS endpoints are scanned (including TLS 1.2 and below) and plain HTTP is attempted | Only TLS 1.3 is accepted (no downgrade), older versions are refused, HTTP redirects to HTTPS, and HSTS headers are present |
| AC-SR006-02 | SEC-REQ-006 | PII/financial columns in a raw database or backup extract | Stored values are inspected | Classified columns are ciphertext (AES-256 at rest) and decryption requires the external key service |
| AC-SR006-03 | SEC-REQ-006 | Plaintext connection attempts to PostgreSQL and Redis | The connections are attempted | They are refused — configured endpoints require TLS |
| AC-SR006-04 | SEC-REQ-006 | A TLS certificate nearing expiry | Certificate monitoring runs | An ops alert fires before the certificate expires |
| AC-SR007-01 | SEC-REQ-007 | A seeded canary secret in a branch | The CI pipeline runs | The secret scan detects it and the build fails — CI secret scanning enabled (AC-S-16) |
| AC-SR007-02 | SEC-REQ-007 | A required environment variable removed | The application starts | Startup fails fast and the error message contains no other secret value — all secrets come from the environment/secrets manager |
| AC-SR007-03 | SEC-REQ-007 | Code, Compose files, fixtures and documentation | An automated credential scan runs | Zero credential literals are found — 0 secrets in version control |
| AC-SR007-04 | SEC-REQ-007 | A full auth + top-up test run | Application logs and traces are scanned | Provider credentials, HMAC secrets and JWT keys are absent from logs and traces |
| AC-SR008-01 | SEC-REQ-008 | OWASP-style SQL injection payloads against search, auth, filter and admin parameters | The payloads are submitted | No unauthorized rows, SQL errors or stack traces are returned — parameterized queries block injection |
| AC-SR008-02 | SEC-REQ-008 | `<script>` and event-handler payloads in product names, reviews and store profiles | The content is stored and then displayed | Values render encoded and CSP blocks inline execution — 0 exploitable XSS results |
| AC-SR008-03 | SEC-REQ-008 | A state-changing request carrying a valid session cookie | It is sent without, then with, a CSRF token | The token-less request is rejected with 403; the same request with a valid token succeeds |
| AC-SR008-04 | SEC-REQ-008 | The data-access layer | Static/architecture linting runs in CI | Raw SQL string concatenation is flagged and zero violations exist |
| AC-SR009-01 | SEC-REQ-009 | A sustained burst of 101 requests within a 60-second window from one IP or user | The requests are processed | Request 101 receives 429 + `Retry-After`; the next window succeeds normally — 100 req/min standard limit |
| AC-SR009-02 | SEC-REQ-009 | OTP resend/verify, login and top-up initiation endpoints | Their measured thresholds are compared | Each is strictly below the 100 req/min standard and enforced per account and per IP |
| AC-SR009-03 | SEC-REQ-009 | Spoofed/removed client headers and disabled client-side throttling | The bursts are replayed | The effective server-side limit is unchanged — client behaviour cannot raise it |
| AC-SR009-04 | SEC-REQ-009 | 10,000 legitimate concurrent users plus a scripted abusive client (C-25) | The load runs | p95 stays within NFR-001 budgets while the abusive client is throttled with 429s |
| AC-SR010-01 | SEC-REQ-010 | The audit tables | Direct `UPDATE`/`DELETE` is attempted as the application role | The statement fails with a privilege error — audit records are append-only |
| AC-SR010-02 | SEC-REQ-010 | An audit row manually altered or deleted | The verification job runs | The chain check fails and an alert is raised — tamper-evident chain |
| AC-SR010-03 | SEC-REQ-010 | Every privileged and money action in scope (role change, KYC decision, wallet freeze, refund, payout, dispute resolution) | Each action executes | Exactly one complete audit row with all required fields exists per action — 0 gaps for in-scope actions (BR-PLT-06) |
| AC-SR010-04 | SEC-REQ-010 | Audit records for money actions older than the current window | They are queried or exported | They remain queryable/exportable per the ≥ 5-year retention configuration |
| AC-SR011-01 | SEC-REQ-011 | Uploads of `.svg`, `.html`, `.exe` and double-extension payloads (e.g. `x.php.jpg` with script content) | Each upload is attempted | All are rejected with a stable error code — SVG is never accepted or executed |
| AC-SR011-02 | SEC-REQ-011 | A 5 MB + 1 byte file and a 4.9 MB valid JPEG | Each is uploaded on every upload surface | The oversized file is rejected and the valid JPEG is accepted — images ≤ 5 MB everywhere |
| AC-SR011-03 | SEC-REQ-011 | A JPEG containing GPS/identity EXIF metadata | The image is stored | The stored object lacks those bytes (byte-level comparison vs source) — EXIF is stripped |
| AC-SR011-04 | SEC-REQ-011 | A standard malware test signature file | The upload is processed | Scanning completes before the file is served; it is quarantined, not retrievable, and an alert is raised |
| AC-SR012-01 | SEC-REQ-012 | A known-vulnerable dependency introduced on a branch | The CI security job (SAST/dependency scan) runs | The job turns red and the merge is blocked — scans gate the pipeline |
| AC-SR012-02 | SEC-REQ-012 | A seeded critical DAST finding in staging | Release promotion is attempted | Production promotion is blocked until the finding is resolved |
| AC-SR012-03 | SEC-REQ-012 | A tracked critical vulnerability | The fix lifecycle runs | Confirmed date, fix date and verification evidence all fall within 7 days (AC-S-13) |
| AC-SR012-04 | SEC-REQ-012 | Scan output for the reporting month | The vulnerability report is generated | The report lists findings by severity with zero silent suppressions lacking justification |

---

## 4. Data Requirements — `AC-DR001-01` …

| AC ID | Requirement | Given | When | Then |
|---|---|---|---|---|
| AC-DR001-01 | DATA-REQ-001 | A child row with a non-existent parent | Direct SQL INSERT runs | The database rejects it with a foreign-key violation — integrity enforced below the application layer |
| AC-DR001-02 | DATA-REQ-001 | Duplicate phone, duplicate SKU within one store, or duplicate coupon code | The inserts are attempted | Each fails with a unique violation mapped to a stable API error |
| AC-DR001-03 | DATA-REQ-001 | Order totals of 499 and 5,000,001 YER and an order state outside the 17-value enum | The writes are attempted | The out-of-range values are rejected by CHECK constraints; 500 and 5,000,000 YER are accepted |
| AC-DR001-04 | DATA-REQ-001 | Negative price, negative stock, and a rating of 0 or 6 | The inserts are attempted | The database rejects them — NOT NULL/domain checks hold below the application layer |
| AC-DR002-01 | DATA-REQ-002 | The data inventory with every PII column mapped to a documented purpose | The schema-to-purpose audit runs | The unmapped-field report is empty and each field is classified per `16-data/data-classification.md` |
| AC-DR002-02 | DATA-REQ-002 | The data model and API contract | They are scanned for card-number and GPS/location fields | No table, column or endpoint contains them — only necessary PII is collected |
| AC-DR002-03 | DATA-REQ-002 | A registration request without an email (and one with an optional email) | The registration is processed | The request succeeds and stores no email value; an optional email is stored without becoming an identity (BR-AUTH-08) |
| AC-DR002-04 | DATA-REQ-002 | Representative list/detail endpoint responses | They are asserted against a per-endpoint PII allowlist | No unexpected PII fields are returned — the test fails otherwise |
| AC-DR003-01 | DATA-REQ-003 | Seeded records past their configured retention | The purge job runs on schedule | The records are removed and rows-purged metrics are emitted |
| AC-DR003-02 | DATA-REQ-003 | An account-deletion request | The account-deletion workflow runs | Profile PII is deleted/anonymised while ledger/wallet rows remain intact and queryable for financial reporting |
| AC-DR003-03 | DATA-REQ-003 | A financial record younger than 5 years | A purge is attempted | The purge is blocked and an alert is raised rather than deleting the record — financial records persist ≥ 5 years (NFR-019) |
| AC-DR003-04 | DATA-REQ-003 | Each purge/deletion run | It completes | An audit entry with actor, scope, counts and timestamp is produced |
| AC-DR004-01 | DATA-REQ-004 | WAL archiving in operation | The maximum gap between archived WAL segments is measured | The gap stays ≤ 15 minutes — RPO evidence |
| AC-DR004-02 | DATA-REQ-004 | A forced snapshot failure | Backup monitoring runs | Operations are alerted within the alerting window defined in `12-non-functional/observability.md` |
| AC-DR004-03 | DATA-REQ-004 | A quarterly restore drill (latest snapshot + WAL) executed on a clean host | Restore is timed end-to-end | It completes within RTO 1 h, passes integrity checks including zero ledger imbalance, and is documented with elapsed time and scope (NFR-006, AC-S-17) |
| AC-DR004-04 | DATA-REQ-004 | Backup storage and restore access | Protection is reviewed and an unauthenticated restore is attempted | Backups are encrypted at rest with role-restricted access; the unauthenticated attempt fails |
| AC-DR005-01 | DATA-REQ-005 | An expand-phase schema | App version N runs critical-path tests against the expanded schema and N+1 against the pre-contract schema | Both pass and both results are recorded in CI |
| AC-DR005-02 | DATA-REQ-005 | A migration containing `DROP COLUMN` in the same release as the code that first stops reading it | The migration lint gate runs | CI fails — expand-contract steps are mandatory |
| AC-DR005-03 | DATA-REQ-005 | A rolling deployment during the migration | Old and new application instances serve traffic concurrently | Zero 5xx responses occur and both versions coexist without errors during rollout (NFR-005, NFR-020) |
| AC-DR005-04 | DATA-REQ-005 | An application rollback after an expand-phase migration | The rollback is executed | It succeeds with no schema rollback and no data loss |
| AC-DR006-01 | DATA-REQ-006 | Stock, wallet and escrow writes violating the domain rules | The invalid writes are submitted | Each is rejected at write time with no partial rows committed |
| AC-DR006-02 | DATA-REQ-006 | A deliberate discrepancy (e.g. wallet total ≠ ledger) | The daily reconciliation job runs | The mismatch is reported and an alert fires within the run — never auto-corrected (BR-ESC-08) |
| AC-DR006-03 | DATA-REQ-006 | Consistent data | Reconciliation runs | It reports zero mismatches — 0 unexplained variance — and completes within its scheduled window |
| AC-DR006-04 | DATA-REQ-006 | Reservations older than 15 minutes | The TTL release job runs | Expired reservations are released and stock availability matches reservations exactly afterwards |
| AC-DR007-01 | DATA-REQ-007 | Direct `UPDATE` and `DELETE` on ledger tables as the application role | The statements execute | They fail with privilege errors — posted ledger entries can never be altered in place (BR-PAY-06) |
| AC-DR007-02 | DATA-REQ-007 | A correction to a posted ledger entry (refund, commission reversal) | The correction executes | Compensating rows are posted instead and row hashes prove the original postings unchanged (AC-S-14) |
| AC-DR007-03 | DATA-REQ-007 | The full ledger with a seeded imbalance introduced | Σ debits and Σ credits are compared by the invariant check | Σ debits = Σ credits across all transactions; the seeded imbalance is detected and alerted |
| AC-DR007-04 | DATA-REQ-007 | A fractional or otherwise invalid YER amount | It is written to a ledger column | The write is rejected — ledger amounts are integer YER |
| AC-DR008-01 | DATA-REQ-008 | Every tenant-scoped table | The schema is audited for owner key columns, foreign keys and indexes | Each table has the expected owner keys — the missing-owner report is empty |
| AC-DR008-02 | DATA-REQ-008 | User A/store X fixtures addressing user B/store Y resources | Every read/write endpoint is called | Each returns zero rows or 403/404 — `user_id`/`store_id` filter results and cross-tenant isolation is proven (BR-VND-07) |
| AC-DR008-03 | DATA-REQ-008 | A worker processing store X's jobs | It runs against shared partitions | Zero rows change in store Y partitions (row-level before/after assertion) |
| AC-DR008-04 | DATA-REQ-008 | A new tenant-scoped entity added without cross-tenant test cases | The CI gate runs | CI fails — cross-tenant test coverage is mandatory |

---

## 5. Integration Requirements — `AC-IR001-01` …

| AC ID | Requirement | Given | When | Then |
|---|---|---|---|---|
| AC-IR001-01 | INT-REQ-001 | A m-Floos/OneCash sandbox top-up is initiated | A signed callback (or reconciled poll) arrives | The wallet is credited exactly once via the ledger with balanced rows (BR-PAY-03) |
| AC-IR001-02 | INT-REQ-001 | The same callback delivered 3 times, and a callback arriving after a poll-based credit | Each delivery is processed | A single credit results; later duplicates are no-ops — a missing/duplicate callback never double-credits |
| AC-IR001-03 | INT-REQ-001 | A callback whose amount/status differs from the initiated transaction | It is processed | It is rejected, finance is alerted, and no credit is posted |
| AC-IR001-04 | INT-REQ-001 | Unsigned, wrong-signature or expired-timestamp callbacks | They arrive | They return 401, are logged, and never credit the wallet |
| AC-IR001-05 | INT-REQ-001 | Production payment credentials | They are used before the sandbox acceptance suite passes | They remain unusable — production is gated on the sandbox suite (DEP-05 exit criterion) |
| AC-IR002-01 | INT-REQ-002 | A bank-transfer top-up submitted by a customer | Admin verification runs | Credit happens only after admin verifies the reference — no code path credits an unverified request (BR-PAY-04) |
| AC-IR002-02 | INT-REQ-002 | The same bank reference submitted twice | The second request is processed | It is rejected with a stable duplicate error and no second credit posts |
| AC-IR002-03 | INT-REQ-002 | A pending request that admin declines | The decline completes | The wallet remains untouched and a localized (ar/en) notification with the reason is delivered (BR-NTF-04) |
| AC-IR002-04 | INT-REQ-002 | Every approval and decline | The action is recorded | A complete audit entry exists (actor, entity, before/after, IP, timestamp) |
| AC-IR003-01 | INT-REQ-003 | The primary SMS provider timing out or erroring during an OTP request | Automatic failover runs | The OTP is delivered via the second provider inside its validity window |
| AC-IR003-02 | INT-REQ-003 | A successful primary send | Failover conditions are evaluated | Failover occurs only on timeout/error — no duplicate message is ever produced |
| AC-IR003-03 | INT-REQ-003 | Each outbound message | Delivery completes | A delivery receipt/status is recorded in logs and metrics, attributable by correlation ID |
| AC-IR003-04 | INT-REQ-003 | Both providers failing | The total outage is detected | An alert reaches on-call within the alerting window and the WhatsApp fallback is attempted; delivery receipts are logged (BR-NTF-03) |
| AC-IR004-01 | INT-REQ-004 | The SMS primary failing while an OTP is pending | The fallback sends the OTP over WhatsApp | Delivery occurs inside the OTP's 5-minute validity window (BR-NTF-03) |
| AC-IR004-02 | INT-REQ-004 | A message using an unapproved template ID | It is submitted for sending | It fails to DLQ and raises an alert; no message is sent — only approved templates are used |
| AC-IR004-03 | INT-REQ-004 | A user with marketing opt-out (and an OTP/security event) | Messages are sent per category | OTP/security messages are still delivered; opted-out marketing categories produce zero sends (BR-NTF-02/05) |
| AC-IR004-04 | INT-REQ-004 | WhatsApp Business templates for every notification type | Each template message is sent | Only approved templates are used, rendered in the user's locale (ar/en, Arabic default) with delivery status tracked (BR-NTF-04, C-24) |
| AC-IR005-01 | INT-REQ-005 | Two eligible couriers accepting the same job concurrently | Both accepts commit | Exactly one is assigned, the other receives a conflict response, and no double assignment exists — the internal engine assigns per BR-SHP-04 |
| AC-IR005-02 | INT-REQ-005 | The delivery API contract, schema and logs | They are scanned for location/GPS fields | No location/GPS field appears anywhere — no location data is requested, stored or returned |
| AC-IR005-03 | INT-REQ-005 | 2 failed delivery-code attempts | The courier submits the 3rd wrong code | Confirmation is locked for 24 hours and a support ticket is created (BR-SHP-03) |
| AC-IR005-04 | INT-REQ-005 | The engine implementation replaced with a mock/external adapter | Domain modules compile and their tests run | Zero domain-module changes are required — no external fleet type leaks into domain code (INT-REQ-008) |
| AC-IR006-01 | INT-REQ-006 | The same webhook delivered 3 times, including once out of order | Deliveries are handled | Exactly one domain effect (and one ledger credit where applicable) results — handlers are idempotent |
| AC-IR006-02 | INT-REQ-006 | A tampered payload or wrong signature | It is delivered to the endpoint | It is rejected with 401, increments a security metric, and produces no effect — signatures verify |
| AC-IR006-03 | INT-REQ-006 | A handler that always fails | Delivery handling occurs | It is retried 3 times with exponential backoff, lands in DLQ, and fires an alert; DLQ depth alerts follow (BR-PLT-02) |
| AC-IR006-04 | INT-REQ-006 | The webhook endpoint under load with slow business logic | Provider callbacks arrive | The endpoint persists and acknowledges within 10 s; slow logic never blocks the callback path |
| AC-IR007-01 | INT-REQ-007 | The observability stack deployed and traffic run | Targets and RED metrics are queried in Prometheus | All defined targets are up (`up == 1`) and RED metrics per endpoint are queryable |
| AC-IR007-02 | INT-REQ-007 | A simulated error spike and a simulated DLQ-depth increase | Alerting evaluates them | An alert fires and reaches the on-call destination within the window defined in `12-non-functional/observability.md` (AC-S-18) |
| AC-IR007-03 | INT-REQ-007 | A sampled metrics export and log stream | An automated PII scan runs | Zero phone numbers, tokens or secret values are found |
| AC-IR007-04 | INT-REQ-007 | Grafana with the deployed dashboards | The dashboards are opened | Dashboards for RED per endpoint, queue/DLQ depth, database health and reconciliation status exist and render from live data |
| AC-IR008-01 | INT-REQ-008 | A vendor SDK or vendor-specific type referenced outside its adapter folder | The import/lint rule runs | The build fails — domain code depends only on interfaces |
| AC-IR008-02 | INT-REQ-008 | The mock adapter swapped for the real sandbox adapter | Domain modules compile and domain tests run | Zero edits to domain modules are needed and all domain tests pass unchanged |
| AC-IR008-03 | INT-REQ-008 | Domain code, API response schemas and log statements | A static scan for vendor identifiers runs | Zero vendor identifiers (m-Floos, OneCash, Telesom, Sabafon, WhatsApp vendor types) are found outside adapters |
| AC-IR008-04 | INT-REQ-008 | The identical contract-test suite | It runs against every adapter implementation (mock, provider A, provider B) | The suite passes against each — contract parity holds |

---

## 6. Cross-Cutting Acceptance Scenarios

### AC-XCUT-01 — Money Cycle End-to-End

Full trust cycle proven in one continuous run (supports `AC-S-22`, `OBJ-02`): top-up → order → escrow → commission → payout → refund.

| Step | Given | When | Then |
|---|---|---|---|
| 1 | An empty wallet of a verified customer | m-Floos top-up of 50,000 YER completes with verified callback | Wallet = 50,000 YER; balanced ledger rows posted once (BR-PAY-03/06) |
| 2 | Balance ≥ cart total from a KYC-approved vendor | Checkout with wallet payment and idempotency key | Master order + sub-order(s) created; total debited exactly once (C-01, C-10) |
| 3 | Order DELIVERED with valid 6-digit code | 7 days elapse with no dispute | Escrow holds then releases; commission 5–20% (default 10%) computed at release (C-12, BR-ESC-03) |
| 4 | Released payable ≥ 1,000 YER | Payout batch runs 3–7 business days later | Vendor paid once; ledger balanced; sub-threshold amounts roll over (BR-ESC-05) |
| 5 | A buyer return approved within policy | Refund executes | Customer wallet credited ≤ 3 business days; commission reversed proportionally (BR-RET-04/07) |
| 6 | All steps complete | Daily reconciliation runs | Σ ledger = 0; wallet+escrow+payable match statements — **0 mismatches** (BR-ESC-08, AC-S-14) |

### AC-XCUT-02 — Constraint Compliance Sweep (`C-01` … `C-26`)

One automated/manual pass verifying **26/26 constraints** (supports `AC-S-02`, `OBJ-12`).

| Constraint | Acceptance check (PASS condition) | Primary ref |
|---|---|---|
| C-01 | Order creation rejects every `payment_method != wallet`; 0 COD paths exist | AC-FR011-05 |
| C-02 | No card fields, endpoints or processors anywhere in contract/code | SEC static scan |
| C-03 | No BNPL/installment/credit feature or endpoint exists | Scope + code review |
| C-04 | Single fiat currency YER — no USD/SAR wallets, no crypto code paths | Payment module audit |
| C-05 | Only m-Floos, OneCash and manual bank transfer top-ups accepted | AC-IR001-01, AC-IR002-01 |
| C-06 | Phone+OTP only: no email-primary auth, no social login | AC-FR001-01 |
| C-07 | No server-side biometric authentication exists | Code review |
| C-08 | Access 15 min / refresh 7 days single-use rotation enforced | AC-FR001-03, AC-SR003-01/02 |
| C-09 | Exactly 17 order states; 17/17 state-machine tests pass | AC-FR012-01 |
| C-10 | One master per checkout, one sub-order per vendor; master = Σ subs | AC-FR011-04 |
| C-11 | Return eligibility honours `isReturnable`/`returnPeriodDays` from delivery | AC-FR016-01 |
| C-12 | Escrow releases no earlier than 7 days after DELIVERED | AC-FR014-01 |
| C-13 | 15-min reservation TTL with auto-release; permanent deduction on payment | AC-FR005-01/02 |
| C-14 | Orders < 500 or > 5,000,000 YER rejected at both boundaries | AC-FR011-01 |
| C-15 | Cart guards 50 products / 10 units / 5 vendors enforced | AC-FR010-01/02 |
| C-16 | Delivery needs 6-digit code; 3 fails → 24 h lock; no GPS requested or stored | AC-FR015-02/03/05 |
| C-17 | Shipping zones restricted to domestic Yemen addresses | Zone config test |
| C-18 | 100% custom build — no commerce platform dependency in the manifest | Dependency audit |
| C-19 | PostgreSQL 16 is the only relational DB in every environment | Deploy config review |
| C-20 | BullMQ is the only queue system — no RabbitMQ/Kafka present | Dependency audit |
| C-21 | Modular monolith with 0 boundary violations (no microservices) | AC-NFR-009-01 |
| C-22 | Docker Compose deployment only — no Kubernetes manifests | Deploy config review |
| C-23 | Greenfield scope — no migration/coexistence code paths | Scope audit |
| C-24 | Arabic default + full English parity; exactly two locales | AC-NFR-013-01/02 |
| C-25 | 10,000 concurrent users sustained within NFR-001 | AC-NFR-003-01 |
| C-26 | 99.99% availability; RTO ≤ 1 h; RPO ≤ 15 min | AC-NFR-005-01, AC-NFR-006-01 |

### AC-XCUT-03 — RTL / Arabic Sweep

Verifies the Arabic-first promise end to end (supports `AC-S-11`, `OBJ-03`, `C-24`).

| Step | Given | When | Then |
|---|---|---|---|
| 1 | A new user with no locale preference | They open any surface | Arabic (`ar`) is the default locale with `dir=rtl` applied |
| 2 | Core journeys at 320/768/1280 px in `ar` | Visual regression runs | 0 RTL layout defects — alignment, icons, drawers and focus order mirrored correctly |
| 3 | Money and dates displayed in `ar` | Amounts/times render | Integer YER in Arabic-Indic numerals; locale-formatted dates; no mixed-locale strings (BR-PAY-10) |
| 4 | The locale switch to English | The user switches and navigates | Full feature parity in `en` with `dir=ltr`, no missing labels or untranslated keys |
| 5 | SMS, WhatsApp, in-app and push templates | Notifications are sent per locale | Every template delivers correctly in `ar` (default) and `en` (BR-NTF-04) |
| 6 | Keyboard and screen reader in `ar` | Core journeys are executed | Focus order follows visual RTL order; TalkBack/VoiceOver announce Arabic correctly (NFR-011) |

### AC-XCUT-04 — Failure-Mode Sweep

Each failure is injected in staging; core journeys must behave as specified (supports `NFR-007`, `NFR-006`, `AC-S-17`).

| Failure injected | Expected behaviour (PASS condition) | Primary ref |
|---|---|---|
| Elasticsearch down | Category browse + product pages keep serving from DB/cache; search shows fallback; recovers ≤ 60 s | AC-NFR-007-01 |
| Redis down | Catalog falls back to DB with stricter rate limits; error rate < 1%; sessions survive on access tokens | AC-NFR-007-01 |
| BullMQ workers stopped | Jobs persist; resume on restart; 3 retries → DLQ; DLQ alert ≤ 1 min; 0 silent loss | AC-NFR-007-02 |
| Primary SMS provider blocked | OTP fails over to WhatsApp; delivery success ≥ 99% across both | AC-IR003-01/04 |
| Payment callback lost/duplicated | Wallet credits exactly once after reconciliation; never on client claim | AC-IR001-01/02 |
| Primary DB host lost | PITR restore within RTO ≤ 1 h / RPO ≤ 15 min; reconciliation proves 0 lost money | AC-NFR-006-01 |
| API replica killed mid-load | LB drains it in ≤ 30 s; 0 failed user sessions; error rate < 0.1% | AC-NFR-018-01 |
| Worker crashes mid-transaction | ACID rollback leaves no partial order/payment/stock row; retry with idempotency key succeeds | AC-NFR-008-02 |
| Duplicate webhook/order submission replay | Idempotency keys return the original result — no duplicate side effects | AC-FR011-02 |
| Disk/backlog pressure (DLQ depth, disk 70%) | Alerts fire; no data is silently dropped; on-call follows runbook ≤ 15 min ack | AC-NFR-014-02 |

---

## 7. How This Registry Is Used

- **Requirement files** (`functional/`, `non-functional/`) list their AC IDs and may condense — never rewrite — the text defined here.
- **`13-testing/`** derives test cases `TC-nnn`: every AC maps to ≥ 1 TC, and `19-traceability/` records requirement → AC → TC with zero gaps (`AC-S-03`).
- **Definition of VERIFIED**: a requirement is `VERIFIED` only when every one of its ACs is PASS with linked evidence (report, dashboard, recording) and no open CRITICAL/HIGH defect (`AC-S-07`).
- **Gaps and conflicts** are recorded in `20-validation/` — this registry is amended by editing this file, bumping its version, never by side documents.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial AC registry (94 FR + 40 NFR + 12 SR + 8 DR + 8 IR + 4 cross-cutting scenarios) | Initial analysis |
| 1.1 | 2026-09-26 | Expanded Security/Data/Integration ACs to sub-numbered IDs | Repo-wide reference consistency |
