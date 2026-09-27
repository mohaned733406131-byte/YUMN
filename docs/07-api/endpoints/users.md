---
document_id: DOC-API-007
title: API-USR — User Profile, Addresses, Preferences & Data Lifecycle (FR-003)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-003, FR-001, FR-017, NFR-013, SEC-REQ-001, SEC-REQ-006, SEC-REQ-011, DATA-REQ-002, DATA-REQ-003, DATA-REQ-008, BR-AUTH-01, BR-AUTH-07, BR-AUTH-08]
related_documents: [DOC-API-002, DOC-API-003, DOC-FR-003, DOC-BA-005, DOC-OVR-008]
---

# API-USR — User & Profile Management

**Group:** `API-USR` · **FR-003** · **Covers:** SEC-REQ-001, SEC-REQ-006, SEC-REQ-011, DATA-REQ-002, DATA-REQ-003 · **Endpoints:** `API-USR-001…013` · **Base:** `/api/v1`

Everything is owner-scoped to the authenticated `sub` (`DATA-REQ-008`): reading another user's profile/addresses returns 404 `NOT_FOUND`. Address book is capped at **10** (`AC-FR003-01`); the phone number is an **immutable** primary identifier; optional email must be verified and is never usable for login/OTP (`BR-AUTH-08`). Session management lives in `auth.md` (API-ATH-011/012); notification preferences live in `notifications.md` (API-NTF-006/007).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-USR-001 | `GET /users/me` | Any authenticated | Read own profile | → `200 { id, phoneMasked, displayName, email?, emailVerified, locale, avatarUrl?, roles, createdAt }` — phone returned masked (`7712***45`), never in full after registration | `AUTH_INVALID` | FR-003, `BR-AUTH-01/08`, SEC-REQ-006 |
| API-USR-002 | `PATCH /users/me` | Any authenticated | Update display name, optional email, locale (Arabic default); phone is immutable | `{ displayName?, email?, locale? }` → `200 { …profile }` — setting `email` marks it unverified and dispatches an OTP to it | `VALIDATION_ERROR`, `EMAIL_ALREADY_REGISTERED`, `DUPLICATE_RESOURCE`, `RATE_LIMITED` | FR-003, `BR-AUTH-01/08`, `C-24` |
| API-USR-003 | `POST /users/me/email/verify` | Any authenticated | Confirm the optional email with the 6-digit code sent to it | `{ code }` → `200 { emailVerified: true }` — email never becomes a login factor | `OTP_EXPIRED`, `OTP_VERIFICATION_FAILED`, `OTP_MAX_ATTEMPTS` | FR-003, `BR-AUTH-08`, SEC-REQ-001 |
| API-USR-004 | `GET /addresses` | `CUSTOMER` | List own saved addresses (≤10), default flagged | `?page&pageSize` (offset, default 50) → `200 { items: [ { id, label, recipientName, recipientPhone, governorate, district, line1, landmark?, notes?, isDefault } ], page: {…} }` | `AUTH_INVALID`, `VALIDATION_ERROR` | FR-003, FR-011, `UC-005`, `DATA-REQ-008` |
| API-USR-005 | `POST /addresses` | `CUSTOMER` | Add an address (Arabic text fully supported, no GPS fields — `C-16`) | `{ label?, recipientName, recipientPhone, governorate, district, line1, landmark?, notes?, isDefault? }` → `201 { …address, Location }` — creating the 1st address makes it default | `MAX_ADDRESSES_REACHED`, `ADDRESS_REQUIRED`, `VALIDATION_ERROR`, `PHONE_INVALID` | FR-003, `AC-FR003-01`, `UC-005`, `C-24` |
| API-USR-006 | `PUT /addresses/{id}` | `CUSTOMER` | Replace one address | full address body → `200 { …address }` | `NOT_FOUND`, `MAX_ADDRESSES_REACHED`, `VALIDATION_ERROR` | FR-003, `UC-005` |
| API-USR-007 | `PUT /addresses/{id}/default` | `CUSTOMER` | Make this address the checkout default (clears the previous flag atomically) | → `200 { …address }` | `NOT_FOUND`, `VALIDATION_ERROR` | FR-003, FR-011, `UC-005` |
| API-USR-008 | `DELETE /addresses/{id}` | `CUSTOMER` | Remove an address; if it was default, the next address becomes default | → `204` | `NOT_FOUND`, `VALIDATION_ERROR` (last address of an in-flight checkout) | FR-003, `UC-005` |
| API-USR-009 | `GET /users/me/preferences` | Any authenticated | Read account preferences (locale, default address, distance-free display options) | → `200 { locale, defaultAddressId?, orderConfirmationChannel, marketingOptIn: { sms, whatsapp, push } }` — notification categories themselves live in API-NTF | `AUTH_INVALID` | FR-003, FR-017, `BR-NTF-05` |
| API-USR-010 | `PUT /users/me/preferences` | Any authenticated | Update preferences | same shape → `200 { …preferences }` — security categories cannot be set here (server ignores them) | `VALIDATION_ERROR`, `PREFERENCE_IMMUTABLE` | FR-003, FR-017, `BR-NTF-02/05` |
| API-USR-011 | `POST /users/me/avatar` | Any authenticated | Upload a profile avatar image | `multipart/form-data { file }` → `201 { fileId, avatarUrl, width, height }` — jpg/png/webp, ≤5 MB, EXIF stripped, malware scanned, re-encoded (`SEC-REQ-011`) | `VALIDATION_ERROR`, `PAYLOAD_TOO_LARGE`, `UNSUPPORTED_MEDIA_TYPE`, `FILE_SCAN_FAILED` | FR-003, SEC-REQ-011, `api-conventions.md` §10 |
| API-USR-012 | `POST /users/me/deletion-request` | Any authenticated (OTP step-up required) | Open the account-deletion workflow with explicit confirmation | `{ confirmation: "DELETE", otpCode }` → `201 { requestId, status: "PENDING", effectiveAt, purgeScope: ["profile","addresses","devices"], retention: "financial_records_5y" }` — PII purge/anonymize scheduled; financial records retained ≥ 5 years | `OTP_NOT_VERIFIED`, `DELETION_PENDING`, `DELETION_BLOCKED`, `VALIDATION_ERROR` | FR-003, DATA-REQ-003, NFR-019, `AC-FR003-04`, SEC-REQ-001 |
| API-USR-013 | `DELETE /users/me/deletion-request` | Any authenticated | Cancel a pending deletion request before `effectiveAt` | → `204` | `NOT_FOUND`, `DELETION_BLOCKED` (already executed) | FR-003, DATA-REQ-003 |

## 2. Behavior Notes

- **Deletion blocking conditions** (`DELETION_BLOCKED`): open orders, active returns/disputes, non-zero wallet balance, pending vendor payouts, or an active store — the response lists the blocking reasons in `details[]` so the user can settle them first.
- **Post-deletion**: the phone number remains reserved for the retention period to prevent impersonation; personal fields are purged/anonymized while ledger rows are untouched (`DATA-REQ-003`, `DATA-REQ-007`).
- **PII at rest**: phone, email, addresses encrypted (AES-256) — `SEC-REQ-006`; only the fields listed here are collectable (`DATA-REQ-002`).
- **Password change** is not here: `PUT /auth/password` (API-ATH-010) — it invalidates all sessions (`BR-AUTH-07`).
- **Deletion requires OTP** issued via `POST /auth/otp/request { context: "SENSITIVE_CHANGE" }` (`SEC-REQ-001`).
- **Locale** affects every subsequent localized response (`Accept-Language` overrides the stored locale only for that request).

## 3. Pagination / Idempotency / Caching

`GET /addresses` uses **offset** pagination (§ `pagination.md` — bounded ≤10 rows). Writes are not idempotency-keyed (natural idempotency on PUT/DELETE). All responses `Cache-Control: no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
