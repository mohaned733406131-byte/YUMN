---
document_id: DOC-FE-006
title: Authentication Handling (Client) — OTP, Tokens & Session UX
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-002, FR-003, NFR-011, NFR-013, SEC-REQ-001, SEC-REQ-003, SEC-REQ-005]
related_documents: [DOC-FE-001, DOC-FE-003, DOC-FE-004, DOC-FE-005]
---

# Authentication Handling (Client)

How the five apps implement **FR-001** on the client. Security *design* lives in `../../09-security/core/authentication.md`; server implementation in `../../06-backend/core/authentication.md`. This file covers client flows, storage, guards and UX — always subordinate to server rules (`SEC-REQ-004`).

---

## 1. Client Auth Flows

| Flow | Steps (client) | Server-anchored rules |
|---|---|---|
| **Register** | phone → password (+confirm) → submit → account created → OTP screen | `BR-AUTH-01/02`, `SEC-REQ-001` |
| **OTP verify** | 6 boxes → auto-submit on 6th digit → success → authenticated | 6 digits, 5-min expiry, 3 attempts (`BR-AUTH-03`) |
| **Login** | phone + password → tokens issued (if OTP already verified per flow) | lockout after 5 failures / 15 min (`BR-AUTH-04`) |
| **Resend** | cooldown button 60 s → resend; disabled after 3 resends/10 min | `BR-AUTH-03` |
| **Password reset** | phone → OTP → new password → all sessions invalidated | `BR-AUTH-07` |
| **Logout** | revoke refresh server-side → clear memory token + query cache | session removal |
| **Logout everywhere** | iterate session list → revoke each (`/account/sessions`) | `BR-AUTH-06`, FR-003 |

## 2. OTP Screen Behavior

| Element | Behavior |
|---|---|
| Input | 6-digit numeric; auto-advance; paste allowed; `inputMode="numeric"` on mobile keyboards |
| Expiry | countdown from server-provided 5-minute expiry; at 0 → "code expired", resend enabled |
| Attempts | server returns attempts remaining; UI shows "2 محاولات متبقية"; at `OTP_MAX_ATTEMPTS` → lock message + disable submit |
| Cooldown | resend button disabled 60 s with visible timer; after 3 resends in 10 min show wait message |
| Delivery channel | SMS primary; if provider fails, server fails over to WhatsApp (`BR-NTF-03`, `INT-REQ-003`) — UI copy says "check SMS or WhatsApp" |
| Localization | all strings ar (default) / en (`BR-NTF-04`, `C-24`) |
| Security notices | OTP/login/lockout notices cannot be suppressed in preferences (`BR-NTF-02`) |
| Never | auto-read SMS beyond OS one-time-code autofill; never log the code |

## 3. Token Storage

| Platform | Access token (15 min, `C-08`) | Refresh token (7 days, single-use) | User profile / roles |
|---|---|---|---|
| **Web (3 apps)** | in-memory module variable; re-derived after refresh | **httpOnly + Secure + SameSite cookie set by server** — never readable by JS, never in `localStorage`/`sessionStorage` (`SEC-REQ-003`) | memory (query cache), cleared on logout |
| **RN (2 apps)** | in memory while app alive | Keychain (iOS) / Keystore (Android) encrypted storage — not plain `AsyncStorage` | encrypted storage |
| **Rejected** | `localStorage` for refresh; URL query tokens; tokens in Redux/Zustand persisted stores; tokens in logs (`SEC-REQ-007`) |

CSRF posture for cookie-based refresh: same-site cookie + CSRF token on state-changing auth endpoints (`SEC-REQ-008`); API SDK always sends `X-Requested-With` and same-origin requests.

## 4. Silent Refresh Handling

```text
request (bearer access token in memory)
   │
   ├── 200 ──► done
   │
   └── 401 TOKEN_EXPIRED
          │
          single-flight refresh()  ── POST /auth/refresh (cookie)
          │        ├── success: new access token → retry original request once
          │        └── failure (revoked/rotated/reused)
          │                └── clear auth slice → route stays → next guarded
          │                    action prompts login with ?next= (DOC-FE-003 §9)
          └── concurrent callers await the same promise (no refresh storm)
```

- Proactive refresh at ~80% TTL while tab/app is foregrounded (DOC-FE-004 §5).
- Multi-tab coordination via `BroadcastChannel` so only one tab refreshes (rotation is single-use, `BR-AUTH-05`).
- Reuse detection result: server revokes the whole session family; client shows a localized "signed out for security" notice + login, and sends a mandatory security notification (`BR-NTF-02`).

## 5. Session Cap (5 Devices) UX — `BR-AUTH-06`, FR-003

| Situation | Client behavior |
|---|---|
| Viewing `/account/sessions` | list of active devices (label, last active, current-device marker) with revoke buttons |
| 6th login elsewhere | server evicts oldest session; evicted client's next request 401s → shows "your session ended because you signed in on a new device" (not a generic error) |
| Logout everywhere | confirm dialog (Arabic/English) → sequential revocation → local clear → login screen |
| Password change/reset | server invalidates all sessions (`BR-AUTH-07`); current device receives fresh tokens and re-authenticates; other devices are logged out on next request |

## 6. Role-Based Route Guards (UX only)

| Guard | Behavior | Server counterpart |
|---|---|---|
| `RequireAuth` | unauthenticated → `/login?next=` | 401 on protected endpoints |
| `RequireRole([...])` | wrong role → role landing redirect (DOC-FE-003 §6) | RBAC on every endpoint (`FR-002`, `DOC-BE-004`) |
| `RequireOwnership` (display) | foreign resource URL → 404 view | ownership query scoping (DATA-REQ-008) |
| Nav visibility | menu items filtered by role | irrelevant to security |

Roles come from the session profile (server-issued); clients **never** read roles from URL, query params, or persisted client state beyond the session lifetime. A tampered client still hits server checks (TC-011…TC-014).

## 7. Mobile Deep-Link Auth (RN)

| Case | Behavior |
|---|---|
| Cold start via `yumn://…` | resolve target → if unauthenticated, run auth stack, then navigate to original target (preserve `returnTo`) |
| OTP entry after redirect | `yumn://verify-otp?ctx=…` pre-fills context only — never the code itself |
| Session restore | read encrypted refresh token → silent refresh before rendering main tabs; show splash meanwhile |
| Biometric convenience | device-level unlock of the stored session only — **not** server authentication (`C-07`) |
| App switcher privacy | auth/sensitive screens use `FLAG_SECURE` / blur in app switcher |
| Logout | revoke + clear Keychain/Keystore entries; deep links land on login |

## 8. Client-Side Auth Security Rules

1. No password/OTP logging, analytics payloads, or crash-report breadcrumbs (`SEC-REQ-002`).
2. Passwords never stored client-side, never pre-filled into other forms.
3. `autocomplete` attributes correct (`tel`, `current-password`, `one-time-code`) — improves SMS autofill UX (`NFR-011`).
4. Rate-limit awareness: client backs off on `429` using `Retry-After` (`SEC-REQ-009`).
5. Lockout messaging after 5 failures mirrors `BR-AUTH-04` — but the server enforces the count.
6. On `FORBIDDEN`, do not render privileged UI leftovers (cache cleared on role/session change).

## 9. Verification

| Type | Cases |
|---|---|
| Unit | cooldown timers, attempts countdown, single-flight refresh, session-list rendering |
| Integration | register → OTP → login → refresh → logout across web + RN; 6th-device eviction behavior |
| Security tests | no refresh token in web storage (static scan); CSRF rejected; reused refresh revokes family (`AC-FR001-03`) |
| E2E (`13-testing/`) | lockout after 5 failures (`AC-FR001-02`), logout-everywhere, deep-link with expired session |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
