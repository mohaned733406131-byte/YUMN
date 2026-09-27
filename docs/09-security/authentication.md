---
document_id: DOC-SEC-003
title: Authentication Security Design (FR-001)
category: 09-security
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-003, SEC-REQ-001, SEC-REQ-002, SEC-REQ-003, SEC-REQ-005, SEC-REQ-009]
related_documents: [DOC-SEC-001, DOC-SEC-002, DOC-SEC-007, DOC-FR-001, DOC-BA-005, DOC-OVR-008, DOC-BE-003]
---

# Authentication — Security Design

Security design for `FR-001` (Identity, Authentication & Session Management). **Implementation placement** (guards, services, queue names, file layout) is owned by `06-backend/authentication.md` (`DOC-BE-003`) — this document defines the *what*, that one defines the *where*. All rule IDs below are canon from `01-business-analysis/business-rules.md`.

## 1. Identity Model

| Property | Rule | Source |
|---|---|---|
| Primary identifier | Yemeni mobile number matching `^7[0-9]{8}$`, unique platform-wide | `BR-AUTH-01` |
| Email | Optional, verified if provided, **never** used for login or OTP | `BR-AUTH-08`, `C-06` |
| Social login / SSO / biometrics as server auth | Excluded | `C-06`, `C-07` |
| Password policy | ≥8 chars containing upper case, lower case, digit; bcrypt cost 12; never logged | `BR-AUTH-02` |
| Password reset | Via OTP only; invalidates **all** existing sessions | `BR-AUTH-07` |

## 2. Phone + OTP Lifecycle (request → verify → session issue)

| Step | Actor action | Server behavior | Hardening |
|---|---|---|---|
| 1. Request | Submits phone `^7[0-9]{8}$` (registration / reset / sensitive change) | Validates format; checks rate budgets (per phone **and** per IP); creates OTP record: 6 numeric digits, TTL 5 min, attempt counter 0, purpose tag, initiating-session binding | Cooldown 60 s between sends; ≤3 resends per 10 min per phone (`BR-AUTH-03`); stricter than the 100 req/min standard (`SEC-REQ-009`) |
| 2. Dispatch | — | `SmsProviderPort.send(...)` with SMS primary; automatic failover to secondary SMS, then WhatsApp (`BR-NTF-03`, `INT-REQ-003`) | OTP body never written to logs/traces (`SEC-REQ-002` R4); correlation ID only |
| 3. Verify | Enters 6 digits | Constant-rate compare against stored value; max **3** verification attempts per code; expired/consumed codes rejected with distinct error codes; success consumes the code immediately (single-use) | 4th attempt rejected; a fresh code never inherits the previous code's attempts (`AC-SR005-02`) |
| 4. Session issue | — | On success for registration/login: issue JWT access token (15 min) + refresh token (7 d) as httpOnly + SameSite cookies; register device session | Session capped at 5 devices (`BR-AUTH-06`); audit/security notice sent (`BR-NTF-02`) |
| 5. Failure paths | Wrong code / expired / throttled | Distinct localized error codes (`BR-PLT-05`), no session material issued, counters incremented, lockout events logged | Client-side throttling is UX only — all counters server-side in Redis (`DEP-03`) |

**Purpose binding:** an OTP issued for password reset can never complete a registration or a phone/payout change (`SEC-REQ-001` R1) — the purpose tag is checked at step 3.

## 3. Password Rules (at registration and change)

- Enforced **before** hashing: length ≥ 8, at least one upper-case, one lower-case, one digit (`BR-AUTH-02`); rejection returns a stable error code (`AC-SR002-04`).
- Hashing: bcrypt cost **12** only; no plaintext ever persisted, returned, logged, or traced (`SEC-REQ-002` R1/R2).
- Login: phone + password; **5 consecutive failures → 15-minute lockout**, auto-expiring, lock event logged (`BR-AUTH-04`, `SEC-REQ-005` R1); the correct password remains rejected for the whole window (`AC-SR005-01`).
- Lock state and remaining attempts are visible to support tooling (`FR-020`) so staff can assist **without** unlocking manually (no manual override weakens the rule).

> **Canon note (logged as `SEC-012`):** `FR-001` and `BR-AUTH-04` scope OTP to registration, password reset, and sensitive changes — login is phone + password. The opening description of `SEC-REQ-001` reads broader ("every authentication … gated by … OTP"). This design follows the requirement statements (`SEC-REQ-001` R1) and `FR-001`; the ambiguity is tracked OPEN in `security-findings.md` and must be resolved before implementation.

## 4. JWT Architecture (`SEC-REQ-003`, `C-08`)

| Property | Value |
|---|---|
| Algorithm | **RS256 only**, algorithm pinned — `alg: none`, HMAC confusion, and signature-stripped tokens rejected (`AC-SR003-04`) |
| Access token lifetime | **15 minutes** (`C-08`) |
| Refresh token lifetime | **7 days**, **single-use** with rotation on every use (`C-08`, `BR-AUTH-05`) |
| Transport | httpOnly + SameSite cookies (Secure in production); never readable from JavaScript, never in localStorage (`SEC-REQ-003` R5); CSRF via `SEC-REQ-008` R4 |
| Validation on every request | Signature → expiry → issuer/audience → live session status; **deny-by-default** on unknown/revoked session (R6) |

**Access-token claims (design):**

| Claim | Content | Note |
|---|---|---|
| `sub` | user ID (UUID) | never the phone number — avoids PII in a decodable token |
| `sid` | session ID | links to the session registry for revocation checks |
| `role` / `roles` | principal role (`CUSTOMER`…`SYSTEM`) | display/UX hint only — **authorization is re-evaluated server-side** (`SEC-REQ-004`) |
| `scope` / permission stamp | coarse capability set | optional cache; a revoked grant must be re-read (registry is authoritative) |
| `iss`, `aud`, `iat`, `exp`, `jti` | standard | `jti` supports audit correlation |

**Refresh-token family (single-use rotation, `BR-AUTH-05`):**

1. Refresh token belongs to a **family** (one family per device session).
2. Presenting a valid refresh token issues a new refresh token (rotating) + new access token; the presented token is marked used.
3. Presenting an **already-used** token ⇒ assumed theft ⇒ **revoke the entire family**, alert the user (`BR-NTF-02` security notice), write an audit entry (`BR-PLT-06`, `AC-SR003-02`).
4. Clock-skew tolerance for reuse detection is a design parameter recorded at `SEC-009` (NTP-synchronized hosts; see `security-findings.md`).

**Session registry (`BR-AUTH-06`, `SEC-REQ-003` R3):**

| Aspect | Design |
|---|---|
| Location | Redis (`DEP-03`) with PostgreSQL as durable session record for revocation survives cache loss |
| Cap | **5 active device sessions per user**; 6th login evicts the **oldest** (`AC-SR003-03`) |
| Revocation | Password reset/change ⇒ invalidate all sessions immediately (`BR-AUTH-07`); logout revokes the family; lockout blocks refresh at next check |
| Propagation | Access tokens die at ≤15 min by lifetime; live checks deny revoked `sid` immediately (`AC-SR003-05`) |

## 5. Brute-Force & Rate-Limit Integration (`SEC-REQ-005`, `SEC-REQ-009`)

| Surface | Budget (server-side) | On breach | Rule |
|---|---|---|---|
| Login (per account) | 5 consecutive failures | 15-min lockout, event logged | `BR-AUTH-04` |
| Login (per IP) | 5 per 15 min | 429 + `Retry-After` | `security-controls.md` §5 (`INFERENCE`) |
| OTP request (per phone) | 3 per 10 min + 60 s cooldown | 429, no code issued | `BR-AUTH-03` |
| OTP verify (per code) | 3 attempts | code invalidated, fresh OTP required | `BR-AUTH-03` |
| OTP request (per IP) | 10 per 10 min | 429, security metric | `SEC-REQ-009` R2 (`INFERENCE`) |
| Delivery code (per shipment) | 3 attempts | 24 h lock + auto support ticket | `BR-SHP-03`, `C-16` |

Counters live in Redis shared across replicas (`NFR-018`); removing/disabling client-side behavior changes nothing (`AC-SR005-04`, `AC-SR009-03`).

## 6. OTP Hardening Summary

- **Parameters fixed:** 6 digits · 5-min expiry · 3 attempts · 60 s resend cooldown · ≤3 resends/10 min (`BR-AUTH-03`) — never client-configurable.
- **Single-use + purpose-bound:** consumed/expired codes can never grant a session or complete an action (`SEC-REQ-001` R3).
- **Delivery:** SMS primary with automatic failover to secondary SMS then WhatsApp inside the 5-minute validity window (`BR-NTF-03`, `INT-REQ-003`, `AC-IR003-01`); failover never duplicates a successful send (`AC-IR003-02`).
- **Storage:** OTP value held in Redis with 5-minute TTL only — never in PostgreSQL, never in logs (`data-protection.md` §4).
- **Visibility:** security notifications (OTP, login, password change, lockout) cannot be disabled by the user (`BR-NTF-02`).
- **Abuse control:** per-IP and per-destination budgets defeat OTP pumping (`TM-02`); provider send limits surfaced as metrics (`SEC-REQ-009` R5).

## 7. MFA Decision (v1)

**Decision: no MFA factor beyond password + OTP-for-sensitive-events in v1.** *(INFERENCE — no requirement in the canon mandates multi-factor authentication; `C-07` excludes biometrics as server auth, `C-06` excludes alternative identity providers.)*

Rationale: the OTP channel already acts as a second factor for registration, reset, and sensitive changes; adding TOTP/hardware keys would introduce a new secret store and recovery path that the Yemeni market does not require at launch. **Recorded gap:** privileged roles (ADMIN, SUPER_ADMIN) receive no *additional* factor at login — tracked as `SEC-012` (HIGH, OPEN). Revisit at the first post-launch security review.

## 8. Session Invalidation Matrix

| Event | Access tokens | Refresh tokens | Sessions | User notified |
|---|---|---|---|---|
| Logout | rejected at next check | family revoked | removed | no |
| Password change/reset (`BR-AUTH-07`) | rejected ≤15 min propagation | all families revoked | all cleared | yes (security notice, `BR-NTF-02`) |
| Refresh reuse detected (`BR-AUTH-05`) | family revoked | family revoked | removed | **yes — alert** |
| 6th device login (`BR-AUTH-06`) | oldest session denied | oldest family revoked | count stays ≤5 | no (session list visible in `FR-003`) |
| Account lockout (`BR-AUTH-04`) | refresh denied during lock | refresh denied during lock | retained, blocked | yes (lockout notice) |
| Role/permission change (`SEC-REQ-004`) | re-authorized on next request | unaffected | retained | no |

## 9. Verification

| Check | Method | Canon reference |
|---|---|---|
| OTP boundary/lifecycle (4th attempt, early resend, 4th resend) | negative integration tests | `AC-SR001-02`, `AC-SR005-02` |
| Token lifetime boundaries (14:59 accept / 15:01 reject) | security test | `AC-SR003-01` |
| Refresh reuse → family revocation + alert | security test | `AC-SR003-02`, `AC-FR001-03` |
| Tamper vectors (`alg:none`, HS256 confusion) | JWT test vectors | `AC-SR003-04` |
| Lockout persistence across client resets | negative test | `AC-SR005-04` |
| No password/OTP in any log line | automated log scan in CI | `AC-SR002-02` |

**Implementation placement:** `06-backend/authentication.md` (`DOC-BE-003`) — NestJS guards, Redis counters, cookie handling, and module boundaries. This document never prescribes file names.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
