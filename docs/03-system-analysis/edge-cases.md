---
document_id: DOC-SA-008
title: Edge Cases
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-005, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015]
related_documents: [DOC-BA-005, DOC-OVR-008, DOC-SA-010, DOC-SA-009, DOC-REQ-001]
---

# Edge Cases

Boundary and race conditions that the system must handle deterministically, with the expected behavior for each. IDs `EC-01…EC-32` are referenced from test design (`13-testing/`) and traceability (`19-traceability/`). Every entry cites the governing `BR-*` / `C-*` / `SEC-REQ-*` / `NFR-*` IDs — definitions are never restated here. Failure-mode analysis of the same scenarios from the *recovery* angle is in `failure-modes.md` (DOC-SA-009).

## 1. Catalog, Stock & Cart

| ID | Edge case | Expected system behavior | Refs |
|---|---|---|---|
| EC-01 | Reservation TTL expires while the customer is still in checkout | Reserved stock auto-releases; checkout shows a re-reservation prompt; if stock is gone, checkout blocks until item removed | `C-13`, `BR-CRT-02`, `BR-CRT-05` |
| EC-02 | Two buyers reserve the last unit simultaneously | First commit wins via atomic check; second receives a stock-conflict error; stock never goes below 0 | `BR-CAT-07`, `C-13` |
| EC-03 | Payment succeeds after the 15-min reservation already released | Compensation: debit refunded, order not created, stock re-reserved or conflict surfaced | `BR-PLT-04`, `C-13` |
| EC-04 | Cart exceeds a guard: 51st product, 11th unit, or 6th vendor | Add rejected with a specific validation error; existing cart unchanged | `C-15`, `BR-CRT-01` |
| EC-05 | Guest cart merged at login contains an item already in the account cart | Server quantity wins on conflict; merge never exceeds per-product/per-vendor limits | `BR-CRT-03`, `C-15` |
| EC-06 | Price changed between add-to-cart and checkout | Server recalculates; changed line is flagged and requires explicit re-confirmation before payment | `BR-CRT-04` |
| EC-07 | Item became inactive/out-of-stock/out-of-policy at checkout | Checkout blocked until the item is removed; no partial silent drop | `BR-CRT-05` |
| EC-08 | Order total computed below 500 YER or above 5,000,000 YER | Order creation rejected at validation with boundary-specific message; no ledger movement | `C-14`, `BR-CAT-04` |
| EC-09 | Coupon invalid/expired/fully used/second coupon attempted | Validation error; **no order row is created**; no stock reservation consumed by the failed attempt | `BR-PRM-01/02/04/06` |
| EC-10 | Coupon would discount more than 90% of order value | Rejected at validation (discount capped by rule), order proceeds only after coupon adjustment/removal | `BR-PRM-01` |

## 2. Orders & Lifecycle

| ID | Edge case | Expected system behavior | Refs |
|---|---|---|---|
| EC-11 | Duplicate checkout submission (double-tap, retry, flaky network) | Idempotency key returns the **original** order; exactly one wallet debit, one stock deduction | `BR-ORD-06`, `BR-PLT-03` |
| EC-12 | Partial multi-vendor cancellation (1 of 3 sub-orders cancelled) | Cancelled sub-order refunds its share and restores its stock; other sub-orders continue; master completes only when every sub-order is COMPLETED or REFUNDED | `C-10`, `BR-ORD-07`, `BR-ORD-04` |
| EC-13 | Customer tries to cancel after READY_FOR_PICKUP | Customer cancel denied; vendor/admin cancel denied past the same boundary — only admin/dispute paths remain | `BR-ORD-04` |
| EC-14 | Two transitions race (e.g. vendor cancels while courier is assigned) | Optimistic locking: one transition commits, the loser gets `409 STATE_CONFLICT`; cancel wins only if state is pre-READY_FOR_PICKUP | `DOC-SA-010` §5 |
| EC-15 | Order remains at CONFIRMED 24 h | Escalated to admin review with notification to the customer and ops; never silently auto-cancelled | `BR-ORD-10` |
| EC-16 | Attempt to skip states (PLACED → DELIVERED) or reach DELIVERED without code | Transition rejected; invalid transition error; no status-history row written | `C-09`, `BR-ORD-08`, `DOC-SA-010` §2 |
| EC-17 | Vendor suspended between order placement and fulfillment | New orders to that store blocked; existing orders frozen pending review; payouts held | `BR-VND-04` |
| EC-18 | Master order has sub-orders in mixed terminal states (COMPLETED + REFUNDED) | Master aggregates to COMPLETED; both terminal outcomes are allowed by the rule | `BR-ORD-07` |

## 3. Wallet, Payment & Escrow

| ID | Edge case | Expected system behavior | Refs |
|---|---|---|---|
| EC-19 | Concurrent debits drain the balance below zero | Row-level locking + atomic balance check: one debit succeeds, others queue/fail; balance never negative | `BR-PAY-05` |
| EC-20 | Same top-up callback delivered twice (provider retry) | Idempotent: second delivery is a no-op; exactly one credit posted | `BR-PAY-03`, `BR-PAY-08` |
| EC-21 | Top-up amount at bounds (999 YER / 5,000,001 YER) | Rejected; valid range is 1,000–5,000,000 YER inclusive | `BR-PAY-02` |
| EC-22 | Bank-transfer reference never verified (admin backlog) | Wallet not credited; pending intent visible in admin queue; customer notified of pending status | `BR-PAY-04`, `INT-REQ-002` |
| EC-23 | Wallet frozen for legal/security reasons | Cannot pay or top up; **can still receive refunds** | `BR-PAY-09` |
| EC-24 | Escrow maturity timer fires at the same moment a dispute opens | Guard evaluation decides: active dispute → release blocked, escrow stays frozen; otherwise release proceeds | `BR-ESC-02`, `BR-ORD-05` |
| EC-25 | Refund due exceeds remaining escrow-held funds | Refund draws escrow first, then vendor payable (vendor liability); shortfall is recorded, never silently dropped | `BR-ESC-07` |
| EC-26 | Payout batch contains a vendor below the 1,000 YER minimum | Amount rolls over to the next batch; batch executes for eligible vendors only | `BR-ESC-05` |
| EC-27 | Payout due while store suspended or KYC lapsed | Payout held pending review; resumes or is resolved by admin per suspension outcome | `BR-ESC-06`, `BR-VND-04` |
| EC-28 | Daily reconciliation finds ledger/wallet/escrow totals mismatch | Mismatch alerts finance; no automatic "fix" writes; investigation path in B13 | `BR-ESC-08`, `BR-FIN-03` |

## 4. Delivery & Authentication

| ID | Edge case | Expected system behavior | Refs |
|---|---|---|---|
| EC-29 | Concurrent delivery-code entry attempts (courier retries + device retry) | First success wins; subsequent identical successes are no-ops with the same result; failures counted deterministically | `DOC-SA-010` §5, `BR-SHP-03` |
| EC-30 | Wrong code entered 3 times | 3rd failure locks confirmation for 24 h and auto-creates a support ticket; attempts 1–2 show remaining count | `BR-SHP-03`, `SEC-REQ-005` |
| EC-31 | Two couriers accept the same offer simultaneously | Optimistic locking — first accept wins; the second receives "no longer available" | `BR-SHP-04` |
| EC-32 | OTP resend abuse (spamming resend) | 60 s cooldown; max 3 resends per 10 minutes; 3 wrong codes burn the OTP; rate limits apply per IP/user | `BR-AUTH-03`, `SEC-REQ-009` |
| EC-33 | Reused (already-consumed) refresh token presented | Whole session family revoked and the user alerted; request rejected | `BR-AUTH-05`, `SEC-REQ-003` |
| EC-34 | 6th concurrent device login (limit is 5) | Oldest session evicted; exactly ≤5 active sessions remain | `BR-AUTH-06`, `C-08` |
| EC-35 | 5 consecutive failed logins | Account locked 15 minutes; lock event logged; security notification sent (not disableable) | `BR-AUTH-04`, `BR-NTF-02` |
| EC-36 | Registered phone re-registered by another user | Registration rejected — phone is unique platform-wide | `BR-AUTH-01` |

## 5. Returns, Reviews & Platform

| ID | Edge case | Expected system behavior | Refs |
|---|---|---|---|
| EC-37 | Return requested one day after `returnPeriodDays` elapsed | Rejected at validation with window dates shown; no pickup scheduled | `BR-RET-01`, `C-11` |
| EC-38 | Vendor never inspects within 72 h of RETURN_RECEIVED | Return auto-approves; refund path proceeds; vendor notified | `BR-RET-05` |
| EC-39 | Return approval untouched for 48 h | Auto-escalated to admin review with notification | `DOC-SA-010` §2 |
| EC-40 | Review submitted by a non-buyer or before DELIVERED | Rejected; only the purchasing customer after delivery, within 30 days | `BR-REV-01` |
| EC-41 | Second review edit after the 7-day window | Rejected — exactly one edit within 7 days | `BR-REV-02` |
| EC-42 | Search index down while catalog changes continue | Browse by category still works (graceful degradation); index catches up when restored | `NFR-007` |
| EC-43 | Notification provider down for security OTP | Automatic failover SMS → WhatsApp; if all channels fail, OTP attempt is queued/retried and user sees in-app guidance | `BR-NTF-03`, `INT-REQ-003` |
| EC-44 | Admin attempts a settings change that violates a constraint | Rejected by validation — constraints (`C-01…C-26`) are not runtime-configurable; attempt audited | `SEC-REQ-010`, `FR-020` |

## 6. Race Conditions Summarized (governing guard)

| Race | Winner rule | Guard mechanism |
|---|---|---|
| Last-unit stock (EC-02) | First atomic deduction | Integer stock ≥0 check inside the transaction (`BR-CAT-07`) |
| Duplicate checkout (EC-11) | First idempotency key | Key lookup returns original order (`BR-ORD-06`) |
| Cancel vs assign (EC-14) | Pre-READY_FOR_PICKUP cancel only | Transition guards evaluated in the order transaction |
| Escrow release vs dispute (EC-24) | Dispute freezes | Release checks active dispute + state set (`BR-ESC-02`) |
| Double refund (EC-20/EC-25) | Single ledger post | Idempotency key + append-only ledger (`BR-PAY-08`, `DATA-REQ-007`) |
| Double courier accept (EC-31) | First accept | Optimistic locking on assignment (`BR-SHP-04`) |
| Concurrent code entry (EC-29) | First success | Idempotent verification (`DOC-SA-010` §5) |

## Verification

Each `EC-*` maps to at least one negative or concurrency test in `13-testing/`; the constraint-driven ones (`EC-08`, `EC-16`, `EC-29`, `EC-30`) also tie to `TST-CON-14`, `TST-CON-09`, `TST-CON-16`. Coverage is tracked in `19-traceability/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
