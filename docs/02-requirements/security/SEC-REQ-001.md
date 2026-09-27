---
document_id: DOC-SR-001
title: SEC-REQ-001 — Strong phone-based verification
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-002, SEC-REQ-003, SEC-REQ-005, SEC-REQ-009, FR-001, FR-003]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-001 — Strong phone-based verification

> Registry summary (`requirements-overview.md` §3): OTP required for registration, password reset, sensitive changes (6 digits, 5 min, 3 attempts).

**Priority:** Critical · **STRIDE:** Spoofing (S) · **Failure impact:** CRITICAL

## Description
Every account is identified by a Yemeni mobile number matching `^7[0-9]{8}$` (BR-AUTH-01), and every authentication or security-sensitive operation is gated by a server-issued one-time password delivered over SMS or WhatsApp (C-06). Scope: registration, password reset, and sensitive account/security changes.

## Security rationale
Because email-primary auth and social login are excluded (C-06, BR-AUTH-08), the phone number is the sole identity anchor; without a bound, expiring, server-issued OTP, anyone knowing a victim's number can register in that identity or reset their credentials. Threat: account takeover via identifier guessing and initiator spoofing → STRIDE **Spoofing**.

## Requirement statements

- R1: Registration, password reset, and each sensitive change (password change, phone change, payout detail change) require a fresh OTP issued to the account phone and bound to the initiating session and purpose.
- R2: OTP parameters are fixed by BR-AUTH-03: 6 numeric digits, 5-minute expiry, maximum 3 verification attempts, resend cooldown 60 s, maximum 3 resends per 10 minutes.
- R3: OTPs are single-use — a consumed or expired code can never grant a session or complete an action; verification success invalidates the code immediately.
- R4: Email is never accepted as an authentication identity or OTP destination (BR-AUTH-08, C-06); WhatsApp is a delivery channel only, never an identifier.
- R5: OTP delivery survives provider failure via automatic failover (INT-REQ-003, BR-NTF-03) so verification stays available at the 99.99% target (C-26).

## Acceptance criteria

- AC-SR001-01: Integration test — valid `^7[0-9]{8}$` registration issues an OTP; wrong, expired, or replayed codes are rejected with distinct error codes and no session/token is issued.
- AC-SR001-02: Boundary test — the 4th verification attempt is rejected; a resend before 60 s and a 4th resend within 10 minutes are both rejected.
- AC-SR001-03: Negative API test — password-reset and sensitive-change endpoints called with a valid access token but without a valid fresh OTP are rejected (401/403/422).
- AC-SR001-04: Contract test — no endpoint in the API contract accepts an email address as login identity or OTP destination.
- AC-SR001-05: Failover test — simulated primary SMS timeout triggers failover and the OTP is still delivered and verifiable inside its 5-minute window.

## Related IDs

`BR-AUTH-01` · `BR-AUTH-03` · `BR-AUTH-08` · `BR-NTF-03` · `C-06` · `C-26` · `FR-001` · `FR-003` · `SEC-REQ-005` · `INT-REQ-003` · `DEP-06`

## Verification method

Integration and negative security tests against the real OTP flow (provider failover simulated with a stub), run in CI and included in the penetration-test scope; evidence recorded in `13-testing/`.

## Failure impact

**CRITICAL** — account takeover at scale: an attacker who triggers or guesses OTPs gains control of wallets holding escrow-funded balances, with irreversible money movement (BR-PAY-05…BR-PAY-07) and PDPA exposure (NFR-019, `DEP-09`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
