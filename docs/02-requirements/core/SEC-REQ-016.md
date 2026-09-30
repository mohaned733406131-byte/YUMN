---
document_id: DOC-SR-016
title: SEC-REQ-016 — Per-destination OTP resend limits
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-009, SEC-REQ-005, FR-001]
related_documents: [DOC-REQ-001, DOC-OVR-012]
---

# SEC-REQ-016 — Per-destination OTP resend limits

> Registry summary (`requirements-overview.md` §3): OTP resend cooldown and resend caps enforced globally per hashed destination phone (not only per session/IP), with a per-destination metric and alert against OTP bombing of a victim number.

**Priority:** Medium · **STRIDE:** Denial of Service (D) · **Failure impact:** MEDIUM

## Description
Existing limits stop one requester hammering OTPs (BR-AUTH-03: 60 s cooldown, max 3 resends per 10 minutes; `SEC-REQ-009` per-IP/per-user rate limits), but they are keyed to the *requester*. `../../09-security/core/security-findings.md` `SEC-006` (lines 83–89, severity MEDIUM) records the gap at line 86: "nothing in the canon mandates a per-**destination** limit across different requesters". This requirement adds a global cap keyed to the hashed destination phone, plus the metric and alert that make OTP bombing of a victim visible (`SEC-006`, `../../09-security/core/threat-model.md` TM-02 residual — `VERIFIED`).

## Security rationale
Distributed requesters (many IPs/sessions/devices) can each stay under their per-IP/per-user limits while collectively flooding one victim's phone with SMS/WhatsApp OTPs — an SMS-bombing harassment attack that also burns provider budget and trains victims to ignore OTP messages (making real OTP attacks likelier). A per-destination counter closes the distributed gap; the alert turns silent abuse into a detected incident. Threat: distributed OTP flooding of a victim number → STRIDE **Denial of Service** (resource/harassment), with secondary social-engineering impact.

## Requirement statements

- R1: Resend cooldown and resend caps are ALSO enforced globally per hashed destination phone across different requesters, sessions and IPs — the per-session/IP limits of BR-AUTH-03/`SEC-REQ-009` remain in force and are never the only guard (`SEC-006` line 86).
- R2: The per-destination counter is keyed by a hashed phone value (never the raw number in metrics/logs — `DATA-REQ-002`), so the control itself does not create a phone-number oracle.
- R3: A per-destination OTP-resend metric exists and an alert fires when a destination approaches or exceeds the global cap — the operational signal required by `SEC-006` (`INFERENCE` for the exact threshold, `VERIFIED` for the required metric + alert).
- R4: A destination at its global cap receives the standard rate-limit response (no indication of why, no per-destination detail leaked back to the requester).

## Acceptance criteria

- AC-SR016-01: Given OTP resend requests for one phone arriving from many distinct IPs/sessions, when the global per-destination resend cap is exceeded, then further requests are rejected even though each requester individually stays under its per-IP/per-user limits.
- AC-SR016-02: Given the per-destination counter, when it is inspected, then the key is a hashed phone value — the raw phone number appears in no metric label or log line (DATA-REQ-002).
- AC-SR016-03: Given a destination approaching the global cap, when the metric threshold is crossed, then the alert fires to the security/on-call route within the alerting window (INT-REQ-007).
- AC-SR016-04: Given a rejected request at the cap, when the response is compared to a generic rate-limit rejection, then no per-destination reason or victim-state detail is disclosed.

## Related IDs

`SEC-REQ-009` · `SEC-REQ-005` · `SEC-REQ-013` · `FR-001` · `FR-017` · `BR-AUTH-03` · `SEC-006` · `TM-02`

## Verification method

Distributed-source load/abuse test against the OTP resend endpoint (many IPs, one destination); metric and alert existence check in the observability stack; log/label scan for raw phone numbers; findings tracked in `../../09-security/core/security-findings.md` (`SEC-006`).

## Failure impact

**MEDIUM** — the attack harasses victims and inflates SMS spend rather than moving funds, but it degrades the OTP channel users trust for real security events (normalizing ignored OTP messages aids real takeovers), and `SEC-006`/TM-02 currently carry it as an unmitigated residual.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial requirement | Session-011 owner directive (`prompt-011.md` §4.7) — delta accepted in `DOC-OVR-012` §5 (source: `security-findings.md` `SEC-006` lines 83–89; `threat-model.md` TM-02) |
