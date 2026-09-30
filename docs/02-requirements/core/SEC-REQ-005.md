---
document_id: DOC-SR-005
title: SEC-REQ-005 — Brute-force protection
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-009, FR-001, FR-015]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-005 — Brute-force protection

> Registry summary (`requirements-overview.md` §3): account lockout 5 failures → 15 min; OTP 3 attempts; delivery code 3 attempts → 24 h lock.

**Priority:** High · **STRIDE:** Spoofing (S), Denial of service (D) · **Failure impact:** HIGH

## Description
Server-side counters throttle guessing attacks against the three credential surfaces of the platform: account passwords, verification OTPs, and the 6-digit delivery confirmation code. Counters are per account and per client, stored server-side, and cannot be reset by the client.

## Security rationale
Automated guessing of an 8-character password policy, a 6-digit OTP, or a 6-digit delivery code would otherwise succeed in minutes. Lockouts convert online guessing into a rate-limited, observable activity; the delivery-code lockout additionally protects against courier/bystander fraud on the no-GPS flow (C-16). Threat: online credential/code guessing → STRIDE **Spoofing**, with lockout-driven **Denial of service** as an abuse side-effect.

## Requirement statements

- R1: 5 consecutive failed logins lock the account for 15 minutes; lock events are logged (BR-AUTH-04); the lock expires automatically with no manual unlock required.
- R2: OTP verification allows maximum 3 attempts per code, with resend cooldown 60 s and maximum 3 resends per 10 minutes (BR-AUTH-03); a new code never inherits the previous code's attempts.
- R3: The 6-digit delivery code allows 3 failed attempts; the 3rd failure locks delivery confirmation for 24 hours and auto-creates a support ticket (BR-SHP-03, C-16).
- R4: Counters are maintained server-side per account and per IP; successful authentication resets the account counter; client-side JavaScript throttles are UX only.
- R5: Lockout state and remaining attempts are visible to support tooling (FR-020) so locked customers can be assisted without weakening the rule.

## Acceptance criteria

- AC-SR005-01: Lockout test — after 5 wrong passwords, the correct password is still rejected for the full 15 minutes and a lock event appears in the logs/audit trail.
- AC-SR005-02: OTP test — the 4th entry attempt is rejected, and a correct code entered after 3 failures cannot verify until a fresh OTP is issued.
- AC-SR005-03: Delivery test — the 3rd wrong code locks confirmation for 24 hours and a support ticket is created automatically (BR-SHP-03).
- AC-SR005-04: Bypass test — rotating client-side behavior or resetting local state does not clear server counters; per-IP throttling triggers when one IP hammers many accounts.

## Related IDs

`BR-AUTH-03` · `BR-AUTH-04` · `BR-SHP-03` · `BR-SHP-06` · `C-16` · `FR-001` · `FR-015` · `FR-020` · `SEC-REQ-001` · `SEC-REQ-009`

## Verification method

Negative security tests for each counter (password, OTP, delivery code) including expiry-boundary timing, plus audit-log inspection; automated in CI and confirmed in the penetration test.

## Failure impact

**HIGH** — unthrottled guessing leads to account takeover (password/OTP) or fraudulent delivery confirmation (code), enabling theft of escrowed goods and wallet balances; mass lockout attempts also degrade availability for legitimate users (C-26).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
