---
document_id: DOC-SR-003
title: SEC-REQ-003 — Token security
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-004, SEC-REQ-007, SEC-REQ-008, FR-001, FR-003]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-003 — Token security

> Registry summary (`requirements-overview.md` §3): JWT RS256; access 15 min; refresh 7 days single-use rotation; httpOnly + SameSite cookies; ≤5 devices (C-08).

**Priority:** Critical · **STRIDE:** Spoofing (S), Elevation of privilege (E) · **Failure impact:** CRITICAL

## Description
Session material follows the C-08 baseline: RS256-signed JWT access tokens with a 15-minute lifetime, refresh tokens valid 7 days with single-use rotation, delivered as httpOnly + SameSite cookies, with at most 5 active device sessions per user. Token validation is deny-by-default.

## Security rationale
Stolen, replayed, or forged tokens are the shortest path to acting as another user — including moving wallet funds. Single-use rotation detects refresh-token theft; short access lifetime bounds exposure; cookie flags keep tokens out of script reach. Threat: session hijacking, token forgery/replay, session proliferation → STRIDE **Spoofing** and **Elevation of privilege**.

## Requirement statements

- R1: Access tokens are JWTs signed with RS256 only (algorithm pinned; `alg: none` and HMAC confusion rejected), lifetime 15 minutes; refresh tokens live 7 days (C-08).
- R2: Refresh tokens are single-use and rotate on every use; presenting an already-used token revokes the entire session family, alerts the user, and writes an audit entry (BR-AUTH-05, BR-PLT-06).
- R3: A maximum of 5 active device sessions per user; a login beyond the limit evicts the oldest session (BR-AUTH-06).
- R4: Password reset or change invalidates all existing sessions immediately (BR-AUTH-07).
- R5: Tokens are delivered and stored in httpOnly + SameSite cookies (Secure in production); they are never readable from JavaScript or persisted in localStorage; CSRF protection is provided by SEC-REQ-008.
- R6: On every request the server verifies signature, expiry, issuer/audience, and live session status; an unknown or revoked session is denied by default.

## Acceptance criteria

- AC-SR003-01: Boundary test — an access token is accepted at 14:59 and rejected with 401 after 15:00 minutes.
- AC-SR003-02: Rotation-reuse test — replaying a consumed refresh token revokes the whole family, emits the user alert, and blocks both tokens from further use.
- AC-SR003-03: Device-limit test — a 6th concurrent login evicts the oldest session; active session count never exceeds 5.
- AC-SR003-04: Tamper test — `alg: none`, HS256-signed, and signature-stripped tokens are rejected; cookie flags httpOnly and SameSite present on every auth response.
- AC-SR003-05: Revocation test — after password reset, the old refresh token fails immediately and previously issued access tokens are denied at their next authorization check (≤15 min propagation).

## Related IDs

`BR-AUTH-05` · `BR-AUTH-06` · `BR-AUTH-07` · `C-08` · `FR-001` · `FR-003` · `SEC-REQ-004` · `SEC-REQ-007` · `SEC-REQ-008` · `SEC-REQ-010`

## Verification method

Security integration tests (lifetime boundaries, rotation reuse, revocation), HTTP response cookie-flag inspection, and JWT tamper test vectors, executed in CI and re-run during the penetration test.

## Failure impact

**CRITICAL** — forged or replayed tokens grant full impersonation of any user, including privileged actors, bypassing OTP entirely and enabling direct wallet and order manipulation.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
