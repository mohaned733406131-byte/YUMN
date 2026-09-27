---
document_id: DOC-WF-002
title: "WF-001 — Customer Registration & Login"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-003, FR-017]
related_documents: [DOC-WF-001, DOC-BA-005, DOC-OVR-008]
---

# WF-001 — Customer Registration & Login (OTP, lockout branches)

| Field | Value |
|---|---|
| **Trigger** | Guest submits the registration form or the login form (phone + password) |
| **Actors** | Customer (`ACT-01`), System (`ACT-07` — OTP dispatch, session issuance) |
| **Blocks** | B01 Identity & Access · B10 Notifications (OTP) · B05 Cart (merge on login) |
| **Preconditions** | Phone matches `^7[0-9]{8}$`; SMS/WhatsApp provider reachable (`DEP-06`) |
| **Final state** | Authenticated session (≤5 devices) + guest cart merged; or account locked 15 min; or OTP rejected after 3 attempts |

```text
[Register: phone + password] ──► validate format ──► send OTP (6d, 5 min) ──► verify ≤3 attempts
        │                              │                       │                      │
        │                              │ format invalid        │ provider timeout      │ 3 wrong codes
        │                              ▼                       ▼                      ▼
        │                        ✗ PHONE_INVALID        OTP → WhatsApp failover   resend cooldown 60 s
        │                                                 (BR-NTF-03)            (max 3 / 10 min)
        ▼                                                                            │ exhausted
[Account created] ──► [Login: phone + password] ──► check lockout ──► verify creds   ▼
        │                                        │                  │        ✗ OTP_VERIFICATION_FAILED
        │                                        │ 5 failed logins  │ ok
        │                                        ▼                  ▼
        │                                   ✗ locked 15 min    issue JWT (15 min access / 7 d refresh)
        │                                   (BR-AUTH-04)            │
        │                                                            ▼
        └──────────────────── guest cart merge (server wins) ◄── session active (≤5 devices)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Customer | Submit phone + password | B01 | `BR-AUTH-01`, `BR-AUTH-02` | draft registration row | Non-matching phone → `PHONE_INVALID`, stop |
| 2 | System | Dispatch 6-digit OTP | B10 | `BR-AUTH-03`, `BR-NTF-03`, `BR-NTF-02` | OTP code (hash), send log | SMS timeout/failure → automatic WhatsApp failover (`INT-REQ-003`); resend cooldown 60 s, max 3 resends / 10 min |
| 3 | Customer | Enter OTP | B01 | `BR-AUTH-03` | verification attempt counter | 1–2 wrong → retry shown; 3rd wrong → `OTP_VERIFICATION_FAILED`, new code required |
| 4 | System | Create/verify account; issue session | B01 | `BR-AUTH-06`, `C-08` | user row, session rows, audit entry | >5 active devices → oldest session removed; OTP valid 5 min then expires |
| 5 | Customer | Login with phone + password | B01 | `BR-AUTH-04`, `BR-AUTH-02` | failed-login counter | 5 consecutive failures → lock 15 min + lock event logged; lockout notice is a security notice (cannot be opted out, `BR-NTF-02`) |
| 6 | System | Issue JWT pair | B01 | `C-08`, `BR-AUTH-05` | access token (15 min), refresh token (7 d, rotating) | Reused refresh token → whole session family revoked + user alerted (`BR-AUTH-05`) |
| 7 | System | Merge guest cart on first login | B05 | `BR-CRT-03` | cart line items merged | Quantity conflict → server value wins (`BR-CRT-03`) |
| 8 | Customer | (Optional) reset password via OTP | B01 | `BR-AUTH-07`, `BR-AUTH-03` | password hash, all sessions revoked | Reset invalidates every existing session (`BR-AUTH-07`) |

**Alternatives**
- **WhatsApp OTP failover:** provider timeout/error on SMS → same OTP flow over WhatsApp template (`BR-NTF-03`, `INT-REQ-004`).
- **Email present:** optional and verifiable but never used for login or OTP delivery (`BR-AUTH-08`); no email-primary or social login paths exist (`C-06`).
- **Session cap:** new login beyond 5 devices evicts the oldest session silently (`BR-AUTH-06`).

**Exceptions**
- OTP/SMS provider fully down (`DEP-06`, `RISK-006`) → registration blocked; no bypass exists (OTP mandatory, `SEC-REQ-001`).
- Brute-force on OTP endpoint → stricter per-IP/user rate limits (`SEC-REQ-009`).
- Biometrics (`C-07`) and email auth (`C-06`) are rejected by design — device unlock only, never server auth.

**Rules applied:** `BR-AUTH-01…08`, `BR-NTF-02…04`, `BR-CRT-03`, `BR-PLT-05`, `BR-PLT-06` · Constraints: `C-06`, `C-08`, `C-24` · Security: `SEC-REQ-001`, `SEC-REQ-003`, `SEC-REQ-005`.

**Data touched:** users (phone unique, password hash bcrypt-12), sessions (≤5), refresh-token families, OTP codes (hashed, 5-min expiry), failed-login counters, audit log (lock events), merged cart lines.

**Systems:** B01 Identity & Access · B10 Notifications · B05 Cart & Checkout · B13 (audit visibility).

**Final state:** active session + merged cart and welcome/security notification sent; or account locked (15 min) with lock event logged and user notified; or OTP rejected pending a fresh code.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
