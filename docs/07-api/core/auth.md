---
document_id: DOC-API-006
title: API-ATH — Authentication & Session Endpoints (FR-001)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-003, SEC-REQ-001, SEC-REQ-002, SEC-REQ-003, SEC-REQ-005, SEC-REQ-009, BR-AUTH-01, BR-AUTH-02, BR-AUTH-03, BR-AUTH-04, BR-AUTH-05, BR-AUTH-06, BR-AUTH-07, BR-AUTH-08]
related_documents: [DOC-API-002, DOC-API-003, DOC-FR-001, DOC-BE-003, DOC-BA-005, DOC-OVR-008]
---

# API-ATH — Authentication & Session Management

**Group:** `API-ATH` · **FR-001** · **Covers:** SEC-REQ-001, SEC-REQ-003, SEC-REQ-005 · **Endpoints:** `API-ATH-001…012` · **Base:** `/api/v1`

Phone (`^7[0-9]{8}$`) is the sole primary identifier (`BR-AUTH-01`, `C-06`). OTP is 6 digits / 5-minute expiry / 3 verification attempts / 60 s resend cooldown / max 3 resends per 10 minutes (`BR-AUTH-03`). Access token 15 min, refresh 7 days single-use rotation, ≤5 device sessions (`C-08`, `BR-AUTH-05`, `BR-AUTH-06`). All security notifications are mandatory and cannot be opted out (`BR-NTF-02`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ATH-001 | `POST /auth/register/start` | Public | Create a pending account for a new phone and dispatch the registration OTP | `{ phone, password, locale?, channel? }` → `201 { status: "OTP_SENT", phoneMasked, expiresAt, resendAfterSeconds, cooldownSeconds }` — password validated + bcrypt cost 12 before any row is written | `PHONE_INVALID`, `PHONE_ALREADY_REGISTERED`, `PASSWORD_POLICY_VIOLATION`, `VALIDATION_ERROR`, `RATE_LIMITED` | FR-001, `BR-AUTH-01/02/03`, `UC-002`, SEC-REQ-001/002/009 |
| API-ATH-002 | `POST /auth/otp/request` | Public | (Re)send an OTP for a context: `REGISTER`, `LOGIN`, `PASSWORD_RESET`, `SENSITIVE_CHANGE` | `{ phone, context }` → `200 { status: "OTP_SENT", expiresAt, resendAfterSeconds, attemptsAllowed: 3 }` — SMS primary with automatic WhatsApp failover; response identical whether or not the account exists (anti-enumeration) | `PHONE_INVALID`, `OTP_RESEND_COOLDOWN`, `OTP_RESEND_LIMIT`, `RATE_LIMITED`, `PROVIDER_DOWN` | FR-001, `BR-AUTH-03`, `BR-NTF-03`, INT-REQ-003/004, SEC-REQ-001/009 |
| API-ATH-003 | `POST /auth/otp/verify` | Public | Verify the 6-digit code; on success for `REGISTER`/`LOGIN` issues the token pair, for `PASSWORD_RESET` returns a single-use reset token, otherwise marks the step-up verified | `{ phone, code, context }` → `200 { verified: true, accessToken?, refreshToken?, expiresIn: 900, sessionId?, resetToken? }` — atomic attempt decrement; correct code deletes the Redis key | `OTP_EXPIRED`, `OTP_VERIFICATION_FAILED` (with `attemptsRemaining`), `OTP_MAX_ATTEMPTS`, `VALIDATION_ERROR`, `RATE_LIMITED` | FR-001, `BR-AUTH-03`, `BR-AUTH-07` (reset path revokes all), SEC-REQ-001/005 |
| API-ATH-004 | `POST /auth/login` | Public | Password login; issues access (15 min) + refresh (7 d, single-use) and registers the device session | `{ phone, password, deviceName? }` → `200 { accessToken, refreshToken, expiresIn: 900, sessionId, user: { id, roles, displayName, locale } }` — 6th concurrent session evicts the oldest (`BR-AUTH-06`); failed counter resets on success | `INVALID_CREDENTIALS`, `ACCOUNT_LOCKED` (+`retryAfterSeconds`), `OTP_NOT_VERIFIED` (unverified phone), `RATE_LIMITED` | FR-001, `BR-AUTH-04`, `BR-AUTH-06`, `C-08`, `UC-003`, SEC-REQ-005 |
| API-ATH-005 | `POST /auth/refresh` | Public (refresh credential) | Rotate the refresh token and mint a new access token; web sends the httpOnly `yumn_refresh` cookie, mobile sends `{ refreshToken }` | body/cookie → `200 { accessToken, refreshToken, expiresIn: 900, sessionId }` — old refresh is consumed; presenting a consumed token revokes the whole session family and triggers a mandatory alert | `TOKEN_EXPIRED`, `REFRESH_TOKEN_REUSED` (family revoked), `AUTH_INVALID`, `SESSION_NOT_FOUND` | FR-001, `BR-AUTH-05`, `C-08`, SEC-REQ-003, `DOC-BE-003` §3 |
| API-ATH-006 | `POST /auth/logout` | Any authenticated | Revoke the current session (`sid`) only; access tokens die at next verification | `Authorization` required; `{ refreshToken? }` → `204` — other devices remain signed in | `AUTH_INVALID`, `SESSION_NOT_FOUND` | FR-001, `BR-AUTH-06`, SEC-REQ-003 |
| API-ATH-007 | `POST /auth/logout-all` | Any authenticated | Revoke every session of the user (all devices) | → `204` — session registry cleared; all refresh tokens invalid immediately | `AUTH_INVALID` | FR-001, FR-003, `BR-AUTH-06/07`, SEC-REQ-003 |
| API-ATH-008 | `POST /auth/password/reset/start` | Public | Begin password reset: dispatch OTP; **always** answers the generic success shape to prevent account enumeration | `{ phone, channel? }` → `200 { status: "OTP_SENT", expiresAt, resendAfterSeconds }` regardless of account existence | `PHONE_INVALID`, `OTP_RESEND_COOLDOWN`, `OTP_RESEND_LIMIT`, `RATE_LIMITED` | FR-001, `BR-AUTH-03`, `UC-004`, SEC-REQ-001 |
| API-ATH-009 | `POST /auth/password/reset/verify` | Public | Validate the reset OTP and issue a short-lived (10 min), single-use `resetToken` | `{ phone, code }` → `200 { resetToken, expiresIn: 600 }` — consuming an OTP does not yet change the password | `OTP_EXPIRED`, `OTP_VERIFICATION_FAILED`, `OTP_MAX_ATTEMPTS` | FR-001, `UC-004`, SEC-REQ-001/005 |
| API-ATH-010 | `PUT /auth/password` | Public with `resetToken`, or Any authenticated with current password + OTP step-up | Set a new password (reset flow) or change it (authenticated flow); **all** existing sessions are invalidated on success | `{ newPassword, resetToken? , currentPassword?, otpCode? }` → `204` — new password must differ from the stored hash; bcrypt cost 12; sessions revoked (`BR-AUTH-07`) | `PASSWORD_POLICY_VIOLATION`, `INVALID_CREDENTIALS`, `OTP_NOT_VERIFIED`, `TOKEN_EXPIRED`, `VALIDATION_ERROR` | FR-001, FR-003, `BR-AUTH-02/07`, `UC-004`, SEC-REQ-001/002 |
| API-ATH-011 | `GET /auth/sessions` | Any authenticated | List the ≤5 active device sessions: `{ sessionId, deviceName, ipMasked, createdAt, lastSeenAt, current: boolean }` | → `200 { items: [...], total }` (small list, single page) | `AUTH_INVALID` | FR-001, FR-003, `BR-AUTH-06`, `DOC-BE-003` §6 |
| API-ATH-012 | `DELETE /auth/sessions/{sessionId}` | Any authenticated | Revoke one device session; the target refresh token fails on next use | → `204` — idempotent: deleting an already-revoked session still returns 204 | `AUTH_INVALID`, `NOT_FOUND` (foreign session ⇒ 404 per ownership rule) | FR-001, FR-003, `BR-AUTH-06`, `AC-FR003-03` |

## 2. Flow Notes

- **Registration** (`UC-002`): `API-ATH-001` → `API-ATH-003` (`context=REGISTER`) marks the phone `VERIFIED`, the account becomes `ACTIVE`, and the token pair is issued. Password is set at registration; `API-ATH-010` covers later changes.
- **Login** (`UC-003`): `POST /auth/login` → 200, or `ACCOUNT_LOCKED` after 5 consecutive failures (15-minute lock, lock event audited — `BR-AUTH-04`, `SEC-REQ-005`). Successful login clears the failure counter.
- **Reset** (`UC-004`): `008 → 009 → 010` — success revokes **all** sessions (`BR-AUTH-07`) and sends a mandatory security notification.
- **Refresh reuse** (`AC-FR001-03`): a replayed refresh token ⇒ `401 REFRESH_TOKEN_REUSED`, session family revoked, user alerted.
- **Device cap** (`AC-FR001-04`): the 6th login succeeds and evicts the oldest session — its next request fails with `SESSION_NOT_FOUND`.
- **Step-up**: sensitive changes (password change, deletion request) require a fresh OTP (`context=SENSITIVE_CHANGE`) ⇒ `OTP_NOT_VERIFIED` without it (`SEC-REQ-001`).
- **Rate limits** (`api-conventions.md` §8): OTP endpoints 5/min/IP + 3 resends/10 min/user; login 10/min/IP.
- **No email auth, no social login, no biometrics** — endpoints for these do not exist (`C-06`, `C-07`).

## 3. Pagination / Idempotency / Caching

No paginated collections (session list ≤ 5). `POST /auth/login` and `POST /auth/otp/*` are **not** idempotent-keyed — retry semantics are governed by attempt counters. All responses `Cache-Control: no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
