---
document_id: DOC-SR-013
title: SEC-REQ-013 — Anti-enumeration uniform responses
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-004, FR-001]
related_documents: [DOC-REQ-001, DOC-OVR-012]
---

# SEC-REQ-013 — Anti-enumeration uniform responses

> Registry summary (`requirements-overview.md` §3): authentication/verification entry points answer with a uniform success-shaped response and never confirm or deny account existence.

**Priority:** High · **STRIDE:** Information Disclosure (I) · **Failure impact:** MEDIUM

## Description
Registration and verification entry points must behave identically whether or not the requested phone number is already registered. The canon currently splits: `../../07-api/core/error-model.md` §5 "Localization of Error Messages" (line 294) demands uniform, non-revealing responses, and `API-ATH-002` (line 28) states the response is "identical whether or not the account exists", while `API-ATH-001` (line 27) returns `PHONE_ALREADY_REGISTERED`. This requirement resolves the split in favour of the uniform response: no auth entry point confirms or denies account existence (`VERIFIED` source conflict — `DOC-OVR-012` §5 row `SEC-REQ-013`).

## Security rationale
Account enumeration turns registration/OTP endpoints into a phone-number oracle: an attacker confirms which numbers hold funded wallets or stores, then targets OTP bombing, phishing or account-takeover attempts only at real victims (see `SEC-REQ-016`, `SEC-006`). Uniform success-shaped responses remove the signal. Threat: targeted abuse guided by enumeration → STRIDE **Information Disclosure**.

## Requirement statements

- R1: Every authentication/verification entry point (registration, OTP request, password-reset initiation) returns the same status code, response body shape and user-facing message regardless of whether the account exists (`../../07-api/core/error-model.md` §5, `API-ATH-002`).
- R2: Existence-revealing error codes such as `PHONE_ALREADY_REGISTERED` are never returned from auth entry points; the existing-account case resolves out-of-band (e.g. the legitimate owner is notified) without telling the submitter (`VERIFIED` conflict resolution — `API-ATH-001` line 27 vs §5).
- R3: The uniform response is produced by a single shared response builder for auth flows so a future endpoint cannot reintroduce a distinguishing variant (`INFERENCE` — operationalizes R1/R2; the sources mandate the behaviour, not the code shape).
- R4: Marketing/onboarding flows that legitimately detect existing users (e.g. "already have an account?" prompts) use an authenticated or separately consented channel — never the anonymous auth entry points (`INFERENCE` derived from R1's scope: anonymous entry points only).

## Acceptance criteria

- AC-SR013-01: Given a registered phone and an unregistered phone, when each submits an OTP/registration request, then both receive identical status code, body shape and message — no existence signal.
- AC-SR013-02: Given the auth endpoint contracts, when they are scanned for codes like `PHONE_ALREADY_REGISTERED`, then no existence-revealing code appears in any anonymous auth entry-point response.
- AC-SR013-03: Given an existing account targeted by re-registration, when the flow completes, then the submitter learns nothing while the legitimate owner receives the out-of-band notification.
- AC-SR013-04: Given the anti-enumeration contract test in CI, when any auth entry point diverges in response shape between the exists/does-not-exist cases, then the test fails and blocks the merge.

## Related IDs

`SEC-REQ-001` · `SEC-REQ-004` · `SEC-REQ-016` · `FR-001` · `BR-AUTH-01` · `BR-AUTH-03` · `API-ATH-001` · `API-ATH-002` · `API-ATH-008`

## Verification method

Contract test suite over auth entry points asserting byte-equivalent exists/does-not-exist responses; API-contract review against `../../07-api/core/error-model.md` §5; error-code inventory scan; findings tracked in `../../09-security/core/security-findings.md`.

## Failure impact

**MEDIUM** — enumeration does not directly move funds, but it arms OTP bombing and targeted account-takeover campaigns against real victims (amplifies `SEC-006`/`SEC-REQ-016`), and breaks the uniform-error promise the canon already makes in §5.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial requirement | Session-011 owner directive (`prompt-011.md` §4.7) — delta accepted in `DOC-OVR-012` §5 (source: `error-model.md` §5 line 294; `auth.md` lines 27/28/34) |
