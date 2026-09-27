---
document_id: DOC-API-003
title: API Error Model — Envelope, Status Mapping & Error-Code Catalog
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-010, FR-011, FR-012, FR-013, FR-015, FR-016, NFR-013, NFR-014, SEC-REQ-004, SEC-REQ-008, SEC-REQ-009]
related_documents: [DOC-API-001, DOC-API-002, DOC-FE-005, DOC-BA-005, DOC-OVR-008, DOC-SA-010]
---

# API Error Model

Single source of truth for **every** non-2xx response of the yumn API. Endpoint files list error *codes* only; the envelope, HTTP mapping and localization rules live here. Clients must never invent codes — an unknown code renders the generic localized fallback (`05-frontend/forms-and-validation.md` §5).

---

## 1. Canonical Error Envelope

Every error response body (all endpoints, all status codes ≥ 400):

```json
{
  "error": {
    "code": "INSUFFICIENT_FUNDS",
    "message": "الرصيد غير كافٍ — المطلوب ١٢٬٥٠٠ ر.ي",
    "messageKey": "errors.INSUFFICIENT_FUNDS",
    "details": [
      { "field": "amount", "issue": "OUT_OF_RANGE", "message": "المطلوب ١٢٬٥٠٠ ر.ي والرصيد ١٠٬٠٠٠ ر.ي" }
    ],
    "correlationId": "9f1c2f6e-4f1b-4a1a-9d5e-2a4c6b8e0f11",
    "retryable": false,
    "retryAfterSeconds": null
  }
}
```

| Field | Type | Required | Rule |
|---|---|---|---|
| `error.code` | string | yes | machine code, `SCREAMING_SNAKE_CASE`, locale-independent, from §4 catalog only |
| `error.message` | string | yes | human-readable, **localized** per `Accept-Language` (ar default, en parity) — `BR-PLT-05`, `C-24` |
| `error.messageKey` | string | yes | i18n catalog key `errors.<CODE>`; clients may render from their own catalog instead of `message` |
| `error.details[]` | array | when applicable | field-level issues; `{ field, issue, message }`; `field` uses dot-path (`items.0.quantity`); drives the client `fields` map (`DOC-FE-005` §5) |
| `error.correlationId` | string | yes | equals the `X-Correlation-Id` response header (`api-conventions.md` §7) |
| `error.retryable` | boolean | yes | `true` = safe for the client to retry the identical request (transient); `false` = requires user/input change |
| `error.retryAfterSeconds` | integer | on 429 / lock responses | mirrors the `Retry-After` header |

Success responses never contain an `error` object. HTTP status always agrees with §3.

## 2. Response Headers on Errors

| Header | Present on | Value |
|---|---|---|
| `X-Correlation-Id` | all responses | same as `error.correlationId` |
| `Retry-After` | 429, 423 lock responses | seconds until retry |
| `WWW-Authenticate` | 401 | `Bearer error="invalid_token"` |
| `Deprecation` / `Sunset` | deprecated routes | see `api-conventions.md` §9 |

## 3. HTTP Status Mapping

| Status | Meaning | Codes in this contract |
|---|---|---|
| 400 | Malformed/unusable request | `VALIDATION_ERROR`, `IDEMPOTENCY_KEY_REQUIRED`, `UNSUPPORTED_MEDIA_TYPE` (also 415), `MALFORMED_REQUEST` |
| 401 | Not authenticated / token problem | `AUTH_INVALID`, `TOKEN_EXPIRED`, `SESSION_NOT_FOUND` |
| 403 | Authenticated but not permitted | `FORBIDDEN`, `INVALID_ROLE`, `CODE_LOCKED`, `ACCOUNT_FREEZE_ACTION_DENIED` |
| 404 | Resource missing **or** out of tenant scope | `NOT_FOUND` |
| 405 | Method not allowed on route | `METHOD_NOT_ALLOWED` |
| 409 | State/booking conflict | `STATE_CONFLICT`, `CANCEL_WINDOW_CLOSED`, `DUPLICATE_RESOURCE`, `IDEMPOTENCY_CONFLICT`, `IDEMPOTENCY_IN_PROGRESS`, `ASSIGNED_ELSEWHERE`, `PRICE_CHANGED`, `LAST_SUPER_ADMIN` |
| 412 | Optimistic-lock precondition failed | `PRECONDITION_FAILED` |
| 413 | Upload too large | `PAYLOAD_TOO_LARGE` |
| 415 | Unsupported upload media type | `UNSUPPORTED_MEDIA_TYPE` |
| 422 | Semantically invalid (business rule) | `INSUFFICIENT_FUNDS`, `TOPUP_LIMIT`, `ORDER_VALUE_OUT_OF_RANGE`, `LIMIT_EXCEEDED`, `CART_LIMIT_EXCEEDED`, `MAX_VENDORS_EXCEEDED`, `MAX_ADDRESSES_REACHED`, `PAYMENT_METHOD_NOT_ALLOWED`, `WALLET_FROZEN`, `STOCK_UNAVAILABLE`, `INVALID_STOCK`, `STOCK_BELOW_RESERVATIONS`, `CART_ITEM_INELIGIBLE`, `OTP_MAX_ATTEMPTS`, `OTP_EXPIRED`, `OTP_VERIFICATION_FAILED`, `OTP_RESEND_COOLDOWN`, `OTP_RESEND_LIMIT`, `PASSWORD_POLICY_VIOLATION`, `PHONE_INVALID`, `WINDOW_EXPIRED`, `NOT_RETURNABLE`, `CODE_INVALID`, `CODE_ATTEMPTS_EXCEEDED`, `KYC_NOT_APPROVED`, `ONE_STORE_PER_VENDOR`, `COUPON_INVALID`, `COUPON_STACKING_NOT_ALLOWED`, `EVIDENCE_REQUIRED`, `REASON_REQUIRED`, `NO_SHIPPING_ZONE`, `FILE_SCAN_FAILED`, `RETURN_WINDOW_CLOSED` |
| 423 | Locked (temporal lock) | `ACCOUNT_LOCKED` |
| 429 | Rate limited | `RATE_LIMITED` |
| 500 | Unexpected server fault | `INTERNAL_ERROR` |
| 503 | Dependency degraded | `PROVIDER_DOWN`, `SEARCH_UNAVAILABLE`, `SERVICE_UNAVAILABLE` |
| 504 | Upstream timeout | `TIMEOUT` |

Client guidance (from `05-frontend/forms-and-validation.md` §5): 401 `TOKEN_EXPIRED` ⇒ silent refresh; 403 ⇒ role landing, never a toast on foreign resources (show 404 behavior); 409 `STATE_CONFLICT` ⇒ refetch + "status changed" banner; 422 `INSUFFICIENT_FUNDS` ⇒ show shortfall + link to top-up; 429 ⇒ countdown from `Retry-After`; 5xx ⇒ generic message + `correlationId`, never raw text (`SEC-REQ-008`).

## 4. Error-Code Catalog (by domain)

Codes are globally unique; a code appears under exactly one domain. `HTTP` column repeats §3 for convenience.

### 4.1 PLT — Platform / Generic (apply everywhere)

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `VALIDATION_ERROR` | 400 | no | DTO/field validation failed; `details[]` lists each offending field |
| `MALFORMED_REQUEST` | 400 | no | Unparseable JSON, wrong content type |
| `IDEMPOTENCY_KEY_REQUIRED` | 400 | no | Required header missing on an idempotent operation (`BR-PLT-03`) |
| `AUTH_INVALID` | 401 | no | Missing/garbage token, revoked session, failed signature |
| `TOKEN_EXPIRED` | 401 | refresh | Access token past 15 minutes (`C-08`) |
| `SESSION_NOT_FOUND` | 401 | no | `sid` absent from the session registry (logged out/evicted) |
| `FORBIDDEN` | 403 | no | Role or action not permitted (deny-by-default, `FR-002`) |
| `INVALID_ROLE` | 403 | no | Requested/target role not assignable by this caller |
| `NOT_FOUND` | 404 | no | Resource missing **or** outside caller scope (IDOR-safe) |
| `METHOD_NOT_ALLOWED` | 405 | no | HTTP verb not on the route |
| `DUPLICATE_RESOURCE` | 409 | no | Unique constraint: phone/SKU/code already taken |
| `IDEMPOTENCY_CONFLICT` | 409 | no | Same key, different request fingerprint |
| `IDEMPOTENCY_IN_PROGRESS` | 409 | yes | Same key still processing; retry after `retryAfterSeconds` |
| `PRECONDITION_FAILED` | 412 | no | Stale `expectedVersion` on optimistic-locked settings |
| `PAYLOAD_TOO_LARGE` | 413 | no | Body/upload above the configured limit (`SEC-REQ-011`) |
| `UNSUPPORTED_MEDIA_TYPE` | 415 | no | Upload type outside the allowed set |
| `RATE_LIMITED` | 429 | yes | Per-IP/per-user quota exceeded (`SEC-REQ-009`) |
| `INTERNAL_ERROR` | 500 | yes | Unhandled fault; message is generic + `correlationId` (`SEC-REQ-008`) |
| `SERVICE_UNAVAILABLE` | 503 | yes | Shutdown/deploy window; health gating (`BR-PLT-07`) |
| `TIMEOUT` | 504 | yes | Internal dependency exceeded its deadline |

### 4.2 AUTH — Authentication & Sessions

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `PHONE_INVALID` | 422 | no | Phone does not match `^7[0-9]{8}$` (`BR-AUTH-01`) |
| `PHONE_ALREADY_REGISTERED` | 409 | no | Duplicate registration (`BR-AUTH-01`, `UC-002`) |
| `INVALID_CREDENTIALS` | 401 | no | Wrong phone/password (counter increments → lock) |
| `ACCOUNT_LOCKED` | 423 | yes | 5 consecutive failures ⇒ 15-minute lock (`BR-AUTH-04`, `SEC-REQ-005`); `retryAfterSeconds` set |
| `PASSWORD_POLICY_VIOLATION` | 422 | no | Password lacks ≥8 chars with upper + lower + digit (`BR-AUTH-02`) |
| `OTP_EXPIRED` | 422 | resend | OTP older than 5 minutes (`BR-AUTH-03`) |
| `OTP_VERIFICATION_FAILED` | 422 | yes | Wrong OTP with attempts remaining; `details[].issue = ATTEMPTS_REMAINING` with count |
| `OTP_MAX_ATTEMPTS` | 422 | no | 3rd wrong verification attempt; OTP invalidated (`BR-AUTH-03`) |
| `OTP_RESEND_COOLDOWN` | 422 | yes | Resend within the 60-second cooldown; `retryAfterSeconds` |
| `OTP_RESEND_LIMIT` | 422 | yes | More than 3 resends in 10 minutes (`BR-AUTH-03`) |
| `TOKEN_INVALID` | 401 | no | Malformed/failed-signature JWT (distinct from expired) |
| `REFRESH_TOKEN_REUSED` | 401 | no | Single-use refresh replayed ⇒ session family revoked + user alerted (`BR-AUTH-05`) |
| `SESSION_LIMIT_REACHED` | 409 | no | >5 active devices when eviction is refused by policy (`BR-AUTH-06`) — normal 6th login succeeds by evicting the oldest |
| `OTP_NOT_VERIFIED` | 403 | no | Step-up OTP required for this operation but not completed (`SEC-REQ-001`) |

### 4.3 USR — Profile, Addresses, Data Lifecycle

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `MAX_ADDRESSES_REACHED` | 422 | no | 11th address (limit 10, FR-003 `AC-FR003-01`) |
| `ADDRESS_REQUIRED` | 422 | no | Checkout/default-address flows with no usable address |
| `EMAIL_ALREADY_REGISTERED` | 409 | no | Optional email taken by another account |
| `EMAIL_NOT_VERIFIED` | 403 | no | Feature requiring a verified optional email (`BR-AUTH-08`) |
| `DELETION_PENDING` | 409 | yes | Deletion request already open |
| `DELETION_BLOCKED` | 409 | no | Deletion refused (open orders/returns/payouts must settle first) |
| `FILE_SCAN_FAILED` | 422 | no | Malware scan rejected an upload (`SEC-REQ-011`) |

### 4.4 VND — Vendors, Stores, KYC

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `ONE_STORE_PER_VENDOR` | 409 | no | Second store creation attempt (`BR-VND-02`, `UC-015`) |
| `KYC_NOT_APPROVED` | 403 | no | Publishing/payout attempt before KYC = APPROVED (`BR-VND-01`) |
| `KYC_IN_REVIEW` | 409 | yes | New submission while a case is under review (`BR-VND-03`) |
| `STORE_SUSPENDED` | 403 | no | Action blocked on a suspended store (`BR-VND-04`) |
| `STAFF_LIMIT_REACHED` | 422 | no | Vendor staff roster at its configured maximum |
| `STAFF_SELF_ESCALATION` | 403 | no | Staff member changing own role (`BR-VND-06`, `AC-FR002-03`) |
| `FOLLOW_LIMIT_REACHED` | 422 | yes | Too many store follows for one account |

### 4.5 CAT — Catalog & Inventory

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `PRODUCT_NOT_PUBLISHABLE` | 422 | no | Missing Arabic name/price/category/image/stock/store (`BR-CAT-01`) |
| `VARIANT_LIMIT_EXCEEDED` | 422 | no | >5 dimensions or >50 combinations (`BR-CAT-02`) |
| `CATEGORY_DEPTH_EXCEEDED` | 422 | no | Tree deeper than 5 levels (`BR-CAT-03`) |
| `PRICE_INVALID` | 422 | no | Price ≤ 0 or sale price ≥ original price (`BR-CAT-04`) |
| `PRODUCT_TYPE_NOT_ALLOWED` | 422 | no | Subscription/trial/sample/rental rejected (`BR-CAT-05`) |
| `IMAGE_LIMIT_EXCEEDED` | 422 | no | >10 product images (`BR-CAT-08`) |
| `STOCK_UNAVAILABLE` | 422 | no | Requested quantity exceeds available (on-hand − reserved) (`BR-CAT-07`) |
| `INVALID_STOCK` | 422 | no | Negative/non-integer stock adjustment |
| `STOCK_BELOW_RESERVATIONS` | 409 | no | Setting stock under active reservations (`UC-018`) |
| `REVIEW_NOT_ELIGIBLE` | 403 | no | Not the purchaser, order not DELIVERED, or 30-day window elapsed (`BR-REV-01`) |
| `REVIEW_ALREADY_EXISTS` | 409 | no | Second review for the same order item (`BR-REV-02`) |
| `REVIEW_EDIT_WINDOW_CLOSED` | 409 | no | Edit beyond 7 days or second edit (`BR-REV-02`) |
| `RESPONSE_ALREADY_EXISTS` | 409 | no | Vendor response already given (`BR-REV-04`) |

### 4.6 SRC — Search & Discovery

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `SEARCH_UNAVAILABLE` | 503 | yes | Elasticsearch down — client falls back to category browse (`NFR-007`, `FR-009`) |
| `QUERY_TOO_SHORT` | 422 | no | `q` below the minimum analyzed length |
| `FACET_INVALID` | 400 | no | Unknown facet/filter key for the index |

### 4.7 CRT — Cart

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `CART_LIMIT_EXCEEDED` | 422 | no | >50 distinct products in the cart (`BR-CRT-01`, `C-15`, `UC-009`) |
| `MAX_VENDORS_EXCEEDED` | 422 | no | Adding from a 6th store — ≤5 vendors per cart (`BR-CRT-01`, `C-15`, `UC-009`) |
| `UNIT_LIMIT_EXCEEDED` | 422 | no | >10 units of one product (`BR-CRT-01`, `C-15`) |
| `LIMIT_EXCEEDED` | 422 | no | Generic limit breach where no specific code applies (cart/top-up) |
| `CART_ITEM_INELIGIBLE` | 422 | no | Item inactive/out-of-stock/out-of-policy; blocks checkout until removed (`BR-CRT-05`) |
| `PRICE_CHANGED` | 409 | yes | Price changed since add-to-cart; requires re-confirmation (`BR-CRT-04`) |
| `RESERVATION_EXPIRED` | 409 | yes | 15-minute reservation TTL elapsed; re-add to resume (`C-13`, `BR-CRT-02`) |
| `GUEST_CART_CONFLICT` | 409 | yes | Merge collision resolved server-side; caller re-reads the cart (`BR-CRT-03`) |

### 4.8 ORD — Checkout, Orders & Lifecycle

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `STATE_CONFLICT` | 409 | no | Transition not allowed from the current one of the 17 states, or stale `version` (`C-09`, `BR-ORD-01`, `DOC-SA-010` §5) |
| `CANCEL_WINDOW_CLOSED` | 409 | no | Cancel after the window (customer: PLACED/CONFIRMED only; vendor/admin: until READY_FOR_PICKUP — `BR-ORD-04`) |
| `ORDER_VALUE_OUT_OF_RANGE` | 422 | no | Total outside 500–5,000,000 YER (`C-14`) |
| `CHECKOUT_SESSION_EXPIRED` | 409 | yes | Checkout snapshot/reservation older than 15 minutes (`C-13`) |
| `SUB_ORDER_NOT_YOURS` | 404 | no | Vendor acting on another vendor's sub-order (`BR-VND-07`, `DATA-REQ-008`) |
| `TIMELINE_ACCESS_DENIED` | 403 | no | Actor outside the timeline visibility matrix (`BR-ORD-09`) |
| `DISPUTE_ALREADY_OPEN` | 409 | yes | Dispute already active for the sub-order (`BR-ORD-05`) |

### 4.9 PAY / WAL — Wallet, Payments, Top-Ups, Escrow, Payouts

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `INSUFFICIENT_FUNDS` | 422 | no | Balance < amount (`BR-PAY-05`, `BR-CRT-06`); `details` carries shortfall |
| `TOPUP_LIMIT` | 422 | no | Top-up outside 1,000–5,000,000 YER (`BR-PAY-02`) |
| `PAYMENT_METHOD_NOT_ALLOWED` | 422 | no | Any non-wallet method (`BR-PAY-01`, `C-01`–`C-03`) |
| `WALLET_FROZEN` | 403 | no | Frozen wallet attempting pay/top-up; refunds still credit (`BR-PAY-09`) |
| `TOPUP_PROVIDER_ERROR` | 502 | yes | m-Floos/OneCash rejected or timed out (`INT-REQ-001`) |
| `TOPUP_CREDIT_PENDING` | 409 | yes | Balance queried/claimed before verified callback/admin verification (`BR-PAY-03`/`BR-PAY-04`) |
| `ESCROW_FROZEN` | 409 | yes | Release attempted while DISPUTED/RETURN_*/REFUNDED (`BR-ESC-02`) |
| `PAYOUT_BELOW_MINIMUM` | 422 | no | Payout request < 1,000 YER (`BR-ESC-05`) |
| `PAYOUT_NOT_ELIGIBLE` | 403 | no | KYC ≠ APPROVED or store suspended (`BR-ESC-06`) |
| `LEDGER_IMMUTABLE` | 405 | no | Attempt to modify an existing ledger posting (`DATA-REQ-007`) |

### 4.10 SHP — Shipping & Delivery

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `CODE_INVALID` | 422 | yes | Wrong 6-digit delivery code; `details` carries `attemptsRemaining` (1–2) (`BR-SHP-02`) |
| `CODE_ATTEMPTS_EXCEEDED` | 422 | no | 3rd wrong code: confirmation locked 24 h + support ticket auto-created (`BR-SHP-03`, `C-16`); `retryAfterSeconds` = lock remaining |
| `CODE_LOCKED` | 403 | yes | Delivery code submission attempted during the 24-hour lock |
| `CODE_ALREADY_VERIFIED` | 409 | no | Code already redeemed (idempotent success already recorded, `DOC-SA-010` §5) |
| `ASSIGNED_ELSEWHERE` | 409 | yes | Another courier accepted first — optimistic first-accept (`BR-SHP-04`, `UC-026`) |
| `DELIVERY_ATTEMPTS_EXCEEDED` | 409 | no | 3 failed delivery attempts ⇒ escalated to admin review (`BR-SHP-06`) |
| `NO_SHIPPING_ZONE` | 422 | no | Address/store outside domestic coverage (`C-17`, `BR-SHP-01`) |
| `COURIER_OFFLINE` | 409 | yes | Courier action while availability = offline |

### 4.11 RET — Returns, Refunds & Disputes

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `WINDOW_EXPIRED` | 422 | no | Return requested after delivery + `returnPeriodDays` (`BR-RET-01`, `C-11`) |
| `NOT_RETURNABLE` | 422 | no | `isReturnable = false` (`BR-RET-01`, `C-11`) |
| `RETURN_WINDOW_CLOSED` | 409 | no | Attempt to reopen/act on a return past its policy window |
| `INSPECTION_WINDOW_PASSED` | 409 | yes | Inspection submitted after 72 h — return auto-approved already (`BR-RET-05`) |
| `REFUND_IN_PROGRESS` | 409 | yes | Duplicate refund trigger; idempotent completion pending (`BR-PAY-08`) |
| `EVIDENCE_REQUIRED` | 422 | no | Dispute/evidence submission without required payload |
| `REASON_REQUIRED` | 422 | no | Reject/failed-attempt/resolve submitted without a reason |
| `ARBITRATION_FORBIDDEN` | 403 | no | Non-admin attempting final arbitration (`BR-RET-06`) |

### 4.12 NTF — Notifications & Devices

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `CHANNEL_NOT_SUPPORTED` | 422 | no | Email channel requested — not a v1 channel (`BR-NTF-01`, `GAP-03`) |
| `PREFERENCE_IMMUTABLE` | 403 | no | Attempt to disable a security notification category (`BR-NTF-02`) |
| `DEVICE_TOKEN_INVALID` | 422 | no | Malformed/duplicate push token registration |
| `DEVICE_NOT_FOUND` | 404 | no | Unregister of an unknown token |

### 4.13 PRM — Content, Coupons & Promotions

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `COUPON_INVALID` | 422 | no | Unknown/expired/fully used/under `min_order_amount` (`BR-PRM-04`, `BR-PRM-06`) — no order row created |
| `COUPON_STACKING_NOT_ALLOWED` | 422 | no | Second coupon on an order that already has one (`BR-PRM-02`) |
| `COUPON_BOUNDS_EXCEEDED` | 422 | no | Validity > 90 days or discount > 90% (`BR-PRM-01`) |
| `CONTENT_NOT_PUBLISHED` | 404 | no | Unpublished page/banner requested publicly |
| `SLUG_TAKEN` | 409 | no | Duplicate slug within its scope (`BR-CAT-03` pattern) |

### 4.14 ADM — Administration, Roles, Audit, Tickets

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `LAST_SUPER_ADMIN` | 409 | no | Demoting/removing the final Super Admin (`UC-037`) |
| `ROLE_ASSIGNMENT_FORBIDDEN` | 403 | no | Non–Super Admin attempting role management (FR-002, `UC-037`) |
| `SETTINGS_VERSION_CONFLICT` | 409 | yes | Concurrent platform-settings write (`UC-035` optimistic lock) |
| `AUDIT_LOG_IMMUTABLE` | 405 | no | Write/delete attempt against the append-only audit log (`SEC-REQ-010`, `DATA-REQ-007`) |
| `TICKET_STATE_CONFLICT` | 409 | no | Action on an already resolved/closed ticket |
| `KYC_DECISION_LATE` | 409 | yes | Decision attempted after the 48 h SLA auto-escalation moved the case (`BR-VND-03`) |

### 4.15 Integration/degradation codes (cross-cutting)

| Code | HTTP | Retryable | When raised |
|---|---|---|---|
| `PROVIDER_DOWN` | 503 | yes | SMS/WhatsApp/payment provider unavailable — failover or queued retry (`INT-REQ-003`, `NFR-007`) |
| `SIGNATURE_INVALID` | 400 | no | Webhook/callback signature verification failed (`INT-REQ-006`) |

## 5. Localization of Error Messages (ar/en)

| Rule | Detail |
|---|---|
| Two channels | `code` = machine contract (never localized); `message` = localized text; `messageKey` = catalog key |
| Catalogs | `errors.<CODE>` exists in **both** `ar` and `en` catalogs; Arabic is the default (`C-24`, `BR-PLT-05`, `BR-NTF-04`) |
| Selection | `Accept-Language` header (missing ⇒ `ar`); the chosen locale is echoed in a `Content-Language` response header |
| Parity | every code must ship with both locales before release — a missing key renders the English fallback and is a defect |
| Style | state the problem + corrective action; money shown with Arabic-Indic digits when locale = `ar` (`BR-PAY-10`); never expose raw exceptions, SQL, stack traces or internal hostnames (`SEC-REQ-008`) |
| Enumeration safety | authentication entry points return generic messages (e.g., `OTP_SENT` success shape on `password/reset/start`) so attackers cannot enumerate accounts (`UC-004`) |
| Field messages | `details[].message` follows the same localization rules as `message` |

Example pairs:

| Code | ar (default) | en |
|---|---|---|
| `STATE_CONFLICT` | "حالة الطلب لا تسمح بهذه العملية — تم تحديث الحالة" | "Order state does not allow this action — the state has changed" |
| `MAX_VENDORS_EXCEEDED` | "الحد الأقصى ٥ متاجر في السلة — أزل منتجات من متجر آخر" | "Maximum 5 stores per cart — remove items from another store" |
| `ACCOUNT_LOCKED` | "تم قفل الحساب لمدة ١٥ دقيقة بعد ٥ محاولات فاشلة" | "Account locked for 15 minutes after 5 failed attempts" |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
