---
document_id: DOC-BE-003
title: Authentication — Implementation Placement (FR-001, SEC-REQ-001…003)
category: 06-backend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-017, NFR-014, SEC-REQ-001, SEC-REQ-002, SEC-REQ-003, SEC-REQ-005, SEC-REQ-009]
related_documents: [DOC-BE-001, DOC-BE-002, DOC-BE-004, DOC-BA-005]
---

# Authentication — Implementation Placement

**Security design** (threats, controls, token architecture rationale) lives in `../../09-security/core/authentication.md`. This file states *where FR-001 / SEC-REQ-001…003 are coded* inside the monolith (`DOC-BE-002` §1). Rules referenced: `BR-AUTH-01…08`, `BR-NTF-02/03`.

---

## 1. Placement Map

| Concern | Module / file | Layer |
|---|---|---|
| Phone-format & uniqueness (`BR-AUTH-01`) | `b01-identity/domain/phone.ts` + `auth.service.register()` | Domain + Service |
| Password policy + bcrypt cost 12 (`BR-AUTH-02`, SEC-REQ-002) | `b01-identity/domain/password.policy.ts`, `shared/crypto/bcrypt.ts` | Domain + Shared |
| OTP generation / expiry / attempts (`BR-AUTH-03`) | `b01-identity/domain/otp.ts` (pure) + `otp.service.ts` (Redis persistence) | Domain + Service |
| OTP delivery (SMS → WhatsApp failover) | `integrations/sms`, `integrations/whatsapp` ← `b10-notification` orchestration (`INT-REQ-003`, `BR-NTF-03`) | Integration |
| Login + lockout (`BR-AUTH-04`) | `b01-identity/auth.service.login()` with Redis failure counter | Service |
| JWT issuance (RS256, 15 min) | `shared/auth/jwt.strategy.ts` + `b01-identity/token.service.ts` | Shared + Service |
| Refresh rotation, family revocation (`BR-AUTH-05`, C-08) | `b01-identity/token.service.refresh()` + `session.repository` (Redis) | Service |
| Session registry, 5-device cap (`BR-AUTH-06`) | `b01-identity/session.service.ts` (Redis `session:{userId}` sorted set) | Service |
| Password reset → revoke all (`BR-AUTH-07`) | `b01-identity/auth.service.resetPassword()` | Service |
| Rate limits on auth endpoints (SEC-REQ-009) | `shared/auth/rate-limit.guard.ts` + Redis counters | Shared |
| Route guards | `shared/auth/jwt-auth.guard.ts`, `roles.guard.ts` | Shared (`DOC-BE-004`) |
| Auth events → logs/notifications | `shared/events` → `b10-notification` (lockout, new device, reset) | Events |

## 2. OTP Lifecycle (implementation)

```text
POST /auth/otp/request  → otp.service
   generate 6 digits (crypto.randomInt) → store Redis key otp:{phone}:{ctx}
   TTL 300 s (5 min, BR-AUTH-03); counters: attempts(3), resends(3/10 min); resend cooldown 60 s
   enqueue b10.notification.delivery (SMS primary) → on provider timeout enqueue WhatsApp failover (INT-REQ-003)

POST /auth/otp/verify   → otp.service
   atomic GET/DECR attempts → correct: delete key, mark verified, issue tokens
   wrong ≤2: return attempts remaining
   3rd wrong: delete key → OTP_MAX_ATTEMPTS → security notification (BR-NTF-02)
   expired: OTP_EXPIRED → allow resend per cooldown
```

| Aspect | Implementation note |
|---|---|
| Storage | Redis only — never DB (ephemeral, TTL-native, supports atomic decrement) |
| Entropy | `crypto.randomInt` — no `Math.random` (SEC-REQ-001) |
| Logging | phone masked in logs; OTP value never logged (`SEC-REQ-002`, `SEC-REQ-007`) |
| Failover | delivery delegated to notification module; failure path never reveals channel state to unauthenticated callers beyond generic response |
| Channels | SMS primary / WhatsApp fallback (`BR-NTF-03`); no email (`GAP-03`, `BR-NTF-01`) |

## 3. Token Issuance & Refresh (C-08, SEC-REQ-003)

| Step | Behavior | Placement |
|---|---|---|
| Issue | access JWT (RS256, 15 min, claims: `sub`, roles, `sid`) + refresh token (opaque, 7 d) rotated into httpOnly cookie (web) / encrypted storage (RN) | `token.service` |
| Refresh | validate refresh → **single-use**: mark consumed in Redis; issue new pair; old cookie invalid | `token.service.refresh()` |
| Reuse detected | consumed-token replay ⇒ revoke entire session family (`BR-AUTH-05`) + alert user | `session.service.revokeFamily()` |
| Logout | delete `sid` from session registry → access tokens die at next check | `session.service` |
| Verification on each request | JWT signature via JWKS (RS256) **and** `sid` active check in Redis (revocation within TTL) | `JwtAuthGuard` (shared/auth) |
| Key management | keys from environment/secrets manager, never repo (`SEC-REQ-007`) | `shared/config` |

## 4. Password Handling (SEC-REQ-002)

| Rule | Implementation |
|---|---|
| Policy | ≥8 chars, upper + lower + digit — enforced in `password.policy.ts` (domain) and DTO pipe; server is source of truth |
| Hashing | bcrypt cost 12 via `shared/crypto/bcrypt.ts`; cost constant reviewed, not configurable per request |
| Comparison | constant-time via bcrypt verify; failures increment lockout counter |
| Never logged | logger has allow-list fields; password fields stripped by serializer |
| Reset | OTP-verified reset re-hashes, revokes all sessions (`BR-AUTH-07`), sends mandatory security notification |

## 5. Lockout (BR-AUTH-04, SEC-REQ-005)

| Item | Value | Implementation |
|---|---|---|
| Trigger | 5 consecutive failed logins | Redis `lock:fail:{phone}` counter, INCR on failure, EXPIRE 15 min at 5th |
| Lock | login refused for 15 min with `ACCOUNT_LOCKED` + retry-after | `auth.service.login()` checks lock first |
| Reset | on successful login | DEL counter |
| Audit | lock events logged + audit entry | `b13-platform` audit writer (BR-PLT-06) |
| Notification | lockout notice mandatory (non-disableable) | `b10-notification` (`BR-NTF-02`) |
| OTP limits | separate from login lock: 3 OTP attempts, 3 resends/10 min (`BR-AUTH-03`) | Redis counters per §2 |
| Delivery-code lock | 3 failures → 24 h + ticket — handled in `b08-shipping`, not here (`BR-SHP-03`) | see `business-logic-placement.md` |

## 6. Session Registry & Device Cap (BR-AUTH-06)

| Item | Implementation |
|---|---|
| Storage | Redis sorted set `sessions:{userId}` scored by last-seen; entry holds `sid`, device label, IP (masked), created |
| 6th login | `session.service.create()` inserts; if size > 5, remove oldest (LRU) → that `sid` fails its next request |
| Visibility | `GET /auth/sessions` reads registry → user can revoke individually or all (`FR-003`) |
| Propagation | revocation is effective immediately for new requests (Redis check in guard) |
| Password change/reset | `revokeAll(userId)` (`BR-AUTH-07`) |

## 7. Rate Limiting & Abuse (SEC-REQ-009)

| Endpoint class | Limit (starting point) | Mechanism |
|---|---|---|
| Standard API | 100 req/min per user/IP | `RateLimitGuard`, Redis sliding window |
| OTP request/verify | stricter (e.g. 5/min/IP, 3/10 min/user) | dedicated counters (`BR-AUTH-03` resends) |
| Login | 10/min/IP + per-account lockout (§5) | dual counters |
| Top-up initiation | stricter tier | `b07-wallet` applies guard |
| Response | `429 RATE_LIMITED` + `Retry-After` | error model (`DOC-BE-008`) |

## 8. What the Client May Do (boundary)

Clients request OTP, submit credentials, hold tokens and render guards (`../../05-frontend/core/authentication-handling.md`). Clients **cannot**: set their own roles, extend token lifetimes, bypass attempt counters, or read another session. Frontend behavior is UX parity only (`SEC-REQ-004`).

## 9. Verification

| Test type | Cases |
|---|---|
| Unit (`NFR-010`) | OTP expiry/attempt arithmetic, lockout counter, rotation/reuse detection, password policy |
| Integration | register → OTP (with failover) → login → refresh → logout; 6th-device eviction (`AC-FR001-04`) |
| Security | reused refresh revokes family (`AC-FR001-03`); 5-failure lockout (`AC-FR001-02`); no plaintext password anywhere; rate limits return 429 |
| Constraint | `TST-CON-*` for `C-06` (no email/social login path exists) and `C-08` (token TTLs) |

Related design doc (must stay consistent): `../../09-security/core/authentication.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
