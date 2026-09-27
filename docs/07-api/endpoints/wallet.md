---
document_id: DOC-API-013
title: API-WAL — Wallet, Payments, Escrow & Payouts (FR-013, FR-014)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-013, FR-014, FR-011, FR-016, FR-018, FR-020, NFR-008, NFR-019, SEC-REQ-006, SEC-REQ-009, DATA-REQ-007, DATA-REQ-008, INT-REQ-001, INT-REQ-002, INT-REQ-006, BR-PAY-01, BR-PAY-02, BR-PAY-03, BR-PAY-04, BR-PAY-05, BR-PAY-06, BR-PAY-07, BR-PAY-08, BR-PAY-09, BR-PAY-10, BR-ESC-01, BR-ESC-02, BR-ESC-03, BR-ESC-05, BR-ESC-06, BR-ESC-07, BR-RET-04]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-013, DOC-FR-014, DOC-BA-005, DOC-OVR-008]
---

# API-WAL — Wallet, Payments, Escrow & Vendor Payouts

**Group:** `API-WAL` · **FR-013 (wallet/payments), FR-014 (escrow/commission/payouts)** · **Endpoints:** `API-WAL-001…014` · **Base:** `/api/v1`

YER-only wallet, one per user. **Top-up bounds 1,000–5,000,000 YER** (`BR-PAY-02`); **order bounds 500–5,000,000 YER** (`C-14`); balance never negative (`BR-PAY-05`); every balance change posts balanced double-entry append-only ledger rows (`BR-PAY-06`, `DATA-REQ-007`); refunds credit the wallet only (`BR-PAY-07`); money operations are idempotent (`BR-PAY-08`); frozen wallets cannot pay or top up but still receive refunds (`BR-PAY-09`). m-Floos/OneCash credit only after a verified callback/reconciled poll (`BR-PAY-03`, `INT-REQ-001`); bank transfers only after admin verification (`BR-PAY-04`, `INT-REQ-002`). Escrow: 7 days from `DELIVERED` (`BR-ESC-01`, `C-12`); commission 5–20% default 10% at release (`BR-ESC-03`); payout min 1,000 YER (`BR-ESC-05`). No card/BNPL/crypto fields exist anywhere in this group (`C-01`–`C-04`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-WAL-001 | `GET /wallet` | `CUSTOMER` (owner) | Balance, status, limits | → `200 { userId, balance, currency: "YER", status: "ACTIVE"\|"FROZEN", limits: { topUpMin: 1000, topUpMax: 5000000, orderMin: 500, orderMax: 5000000 }, lastTransactionAt }` | `AUTH_INVALID` | FR-013, `BR-PAY-02/09/10`, `C-14` |
| API-WAL-002 | `GET /wallet/transactions` | `CUSTOMER` (owner) | Append-only ledger view for the owner (cursor feed) | `?type&from&to&limit&cursor` → `200 { items: [ { id, type: "TOPUP"\|"ORDER_PAYMENT"\|"REFUND"\|"ESCROW_HOLD"\|"PAYOUT", direction: "CREDIT"\|"DEBIT", amount, balanceAfter, reference: { kind, id }, status, createdAt } ], page: {…}, total: { value, relation } }` — exact totals always (money views are never estimated) | `AUTH_INVALID`, `VALIDATION_ERROR` | FR-013, `BR-PAY-06/10`, `DATA-REQ-007/008` |
| API-WAL-003 | `POST /wallet/topups` | `CUSTOMER` | Initiate a top-up — **requires `Idempotency-Key`** | `{ amount, method: "MFLOOS"\|"ONECASH"\|"BANK_TRANSFER", reference?, proofFileId? }` → `201 { topupId, status: "PENDING_PROVIDER"\|"PENDING_VERIFICATION", amount, method, paymentInstruction: { …provider payload \| bank beneficiary details }, expiresAt }` — amount bounds checked before contacting any provider | `TOPUP_LIMIT`, `WALLET_FROZEN`, `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `VALIDATION_ERROR`, `TOPUP_PROVIDER_ERROR`, `RATE_LIMITED` | FR-013, `BR-PAY-02/03/04/08`, `C-05`, INT-REQ-001/002, `AC-FR013-01`, SEC-REQ-009 |
| API-WAL-004 | `GET /wallet/topups/{id}` | `CUSTOMER` (owner) | Poll top-up status (provider callback/poll reconciliation, admin verification) | → `200 { topupId, amount, method, status: "PENDING_PROVIDER"\|"PENDING_VERIFICATION"\|"CREDITED"\|"REJECTED", creditedAt?, rejectionReason?, reference }` | `NOT_FOUND` | FR-013, `BR-PAY-03/04`, INT-REQ-001/002, `UC-034` |
| API-WAL-005 | `POST /wallet/topups/{id}/proof` | `CUSTOMER` (owner) | Attach bank-transfer proof (slip image/PDF) for admin verification | `multipart { file }` → `201 { proofFileId, status: "PENDING_VERIFICATION" }` — pdf/image ≤ 5 MB, scanned, EXIF stripped | `NOT_FOUND`, `PAYLOAD_TOO_LARGE`, `UNSUPPORTED_MEDIA_TYPE`, `FILE_SCAN_FAILED`, `VALIDATION_ERROR` | FR-013, SEC-REQ-011, INT-REQ-002, `UC-034` |
| API-WAL-006 | `POST /wallet/payments/authorize` | `CUSTOMER` | Hold funds for a checkout session (balance gate before confirm) — **requires `Idempotency-Key`** | `{ checkoutSessionId, amount }` → `201 { paymentId, status: "AUTHORIZED", heldAmount, expiresAt }` — hold never exceeds available balance; holds expire with the checkout session | `INSUFFICIENT_FUNDS`, `WALLET_FROZEN`, `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `NOT_FOUND`, `VALIDATION_ERROR` | FR-011, FR-013, `BR-CRT-06`, `BR-PAY-05/08`, `C-13` |
| API-WAL-007 | `POST /wallet/payments/{id}/capture` | `SYSTEM` (internal — not callable by clients) | Execute the debit inside the order-creation saga: balanced ledger posting + escrow funding, exactly once | internal payload (order reference) → `200 { paymentId, status: "CAPTURED", ledgerReference }` — replay with the same key no-ops (`BR-PAY-08`); failure of any leg triggers compensating release | `INSUFFICIENT_FUNDS`, `WALLET_FROZEN`, `IDEMPOTENCY_CONFLICT`, `STATE_CONFLICT` | FR-011, FR-013, `BR-PAY-05/06/08`, `BR-PLT-04`, `NFR-008` |
| API-WAL-008 | `POST /wallet/payments/{id}/release` | `SYSTEM` (internal), `ADMIN` (manual) | Release an unused/expired authorization hold back to available balance | `{ reason }` → `200 { paymentId, status: "RELEASED" }` | `STATE_CONFLICT`, `NOT_FOUND`, `REASON_REQUIRED` | FR-013, `C-13`, `BR-PAY-08` |
| API-WAL-009 | `GET /wallet/escrow` | `CUSTOMER` (own orders), `VENDOR` (own sub-orders) | Escrow status view: held amounts, release eligibility | `?orderId&limit&cursor` → `200 { items: [ { subOrderId, orderId, storeId?, amountHeld, state, deliveredAt?, releaseEligibleAt, releasedAt?, frozenBy: "NONE"\|"DISPUTE"\|"RETURN" } ], totals: { held, released } }` | `NOT_FOUND`, `TIMELINE_ACCESS_DENIED` | FR-014, `BR-ESC-01/02`, `BR-ORD-05`, `C-12` |
| API-WAL-010 | `GET /store/finance/overview` | `VENDOR` | Finance dashboard data: payable balance, escrow held, pending payout, period sales | `?from&to` → `200 { availablePayable, escrowHeld, pendingPayout, belowMinimumRollover, period: { salesYER, orders, refundsYER, commissionYER }, commissionRatePercent, payoutThreshold: 1000 }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-014, FR-018, `BR-ESC-03/05`, `BR-FIN-04`, `BR-VND-07`, `UC-022` |
| API-WAL-011 | `POST /store/payouts` | `VENDOR` (Owner) | Request a payout of the available payable balance — **requires `Idempotency-Key`** | `{ amount, destination? }` → `201 { payoutId, status: "REQUESTED", amount, destinationMasked, estimatedExecution }` — batched execution 3–7 business days after release; amounts < 1,000 YER roll over | `PAYOUT_BELOW_MINIMUM`, `PAYOUT_NOT_ELIGIBLE`, `INSUFFICIENT_FUNDS` (payable), `KYC_NOT_APPROVED`, `STORE_SUSPENDED`, `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `VALIDATION_ERROR` | FR-014, `BR-ESC-05/06`, `GAP-06`, `UC-022` |
| API-WAL-012 | `GET /store/payouts` | `VENDOR` | Payout history (offset table) | `?page&pageSize&status&from&to` → `200 { items: [ { payoutId, amount, status: "REQUESTED"\|"SCHEDULED"\|"EXECUTED"\|"REJECTED"\|"ROLLED_OVER", requestedAt, executedAt?, reference } ], page: {…}, total }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-014, `BR-ESC-05`, `NFR-019` |
| API-WAL-013 | `GET /store/payouts/{id}` | `VENDOR` | Payout detail incl. ledger references and rejection reason | → `200 { …payout, ledgerEntries: [...], statementMonth }` | `NOT_FOUND` | FR-014, `BR-FIN-04` |
| API-WAL-014 | `GET /orders/{id}/refund` | `CUSTOMER` (owner), `ADMIN` | Refund receipt/status for an order (cancellation or return path) | → `200 { orderId, subOrders: [ { subOrderId, status: "PENDING"\|"COMPOSED"\|"CREDITED", amount, itemValue, shippingRefunded, walletCredit: { reference, creditedAt? }, expectedCreditBy } ] , commissionReversed? }` — wallet credit within 3 business days of `REFUNDED` | `NOT_FOUND`, `TIMELINE_ACCESS_DENIED` | FR-016, FR-013, `BR-RET-03/04`, `BR-PAY-07`, `BR-ESC-04/07`, `UC-021` |

## 2. Behavior Notes

- **Top-up lifecycle** (`INT-REQ-001/002`): `POST /wallet/topups` creates the pending record → provider redirect/instructions → verified callback **or** reconciled poll credits the ledger (`BR-PAY-03`, never on client claim); `BANK_TRANSFER` waits for `POST /admin/topups/{id}/verify` in `admin.md` (`BR-PAY-04`, `UC-034`). Replayed callbacks credit exactly once (`AC-FR013-02`).
- **Never-negative debit** (`BR-PAY-05`): row-level locking with an atomic balance check inside an ACID transaction; failure ⇒ 422 `INSUFFICIENT_FUNDS` with the shortfall in `details[]` (`AC-FR013-03`).
- **Ledger** (`BR-PAY-06`, `DATA-REQ-007`): every balance change posts balanced debit+credit rows; no endpoint updates or deletes ledger postings (attempts ⇒ 405 `LEDGER_IMMUTABLE`); corrections are compensating entries.
- **Escrow release** (`BR-ESC-01/02`, `C-12`): `DELIVERED + 7 days` and state ∉ {DISPUTED, RETURN_*, REFUNDED} ⇒ `SYSTEM` releases to vendor payable exactly once (idempotent job). Commission is computed at release (`BR-ESC-03`); refunds reverse proportionally (`BR-ESC-04`), drawing escrow first then vendor payable (`BR-ESC-07`).
- **Refunds** (`BR-PAY-07`, `BR-RET-04`): always credit the customer wallet — no external cash-out; the return/cancel flow triggers the engine, `API-WAL-014` reports status and the ledger credit reference.
- **Authorization/capture split**: `API-WAL-006` is client-callable (funds hold aligned with the 15-minute checkout session); `API-WAL-007` executes inside the `POST /orders` saga and is callable only by `SYSTEM` — clients reach it exclusively through order confirmation.
- **Freeze** (`BR-PAY-09`): `status = FROZEN` ⇒ `WALLET_FROZEN` on pay/top-up; refunds still credit. Freeze/unfreeze is admin-only (`admin.md`).
- **Rate limiting** (`SEC-REQ-009`): stricter tier on `API-WAL-003` (10/min/user) and `API-WAL-006`.
- **Reconciliation** (`BR-ESC-08`, `BR-FIN-03`): daily job compares ledger/wallet/escrow/payable totals with provider statements — surfaced to operators via `GET /admin/reconciliation` (`analytics.md`).

## 3. Pagination / Idempotency / Caching

| Endpoint(s) | Mode |
|---|---|
| `API-WAL-002`, `API-WAL-009` | cursor (exact totals on the ledger) |
| `API-WAL-012` | offset |
| others | single resource |

Mandatory idempotency keys: `API-WAL-003`, `API-WAL-006`, `API-WAL-011`, plus internal capture/refund (`BR-PAY-08`, `BR-PLT-03`). All responses `Cache-Control: no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
