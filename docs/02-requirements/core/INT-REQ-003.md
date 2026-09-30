---
document_id: DOC-IR-003
title: INT-REQ-003 — SMS provider failover
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-004, INT-REQ-006, INT-REQ-008, FR-001, FR-017]
related_documents: [DOC-REQ-001, DOC-OVR-010, DOC-BA-005]
---

# INT-REQ-003 — SMS provider failover

> Registry summary (`requirements-overview.md` §5): two providers; primary → failover on timeout/error; delivery receipts logged.

**Dependency risk:** CRITICAL — `DEP-06` is **NOT STARTED** and is a Phase 0 gate; without OTP delivery, registration is blocked and the platform cannot start (hardest blocker).

## Purpose
Deliver OTPs and transactional notifications (FR-001, FR-017) reliably over two SMS providers (Telesom and/or Sabafon per DEP-06), switching automatically on provider timeout or error, with delivery receipts recorded for every message.

## Interface expectations

- **Send:** a single `send(template, phone, locale, purpose, correlationId)` interface; the adapter tries the primary provider, and on timeout (10 s) or error switches to the secondary within the OTP's 5-minute validity window (BR-AUTH-03).
- **Retry:** transient failures retry 3× with exponential backoff, then dead-letter queue with alert (BR-PLT-01, BR-PLT-02); the OTP resend cooldown of 60 s and ≤3 resends/10 min (BR-AUTH-03) still govern user-triggered attempts.
- **Receipts:** provider delivery receipts (DLRs) are received via signed webhook (10 s timeout, HMAC, allowlist) and logged per message with status (sent/delivered/failed).
- **Environments:** provider sandbox/shortcode certification before production (DEP-06 gate); both providers must pass the failover test suite.

## Data exchanged
Destination phone matching `^7[0-9]{8}$` (BR-AUTH-01), template identifier, locale `ar`/`en` (BR-NTF-04), correlation ID, message status/timestamps. Message bodies containing OTPs are excluded from application logs (`INFERENCE` — extends SEC-REQ-002 never-logged discipline to OTP codes); no PII in metric labels.

## Failure behavior & fallback
Primary timeout/error → secondary provider; both SMS providers down → WhatsApp channel fallback for OTP (BR-NTF-03) and an immediate ops alert (NFR-014); all channels down → registration/verification unavailable, surfaced honestly to the user with retry guidance, tracked as `RISK-006`.

## Security
Provider API keys in environment only (SEC-REQ-007); DLR webhooks HMAC-signed with IP allowlist (INT-REQ-006); per-IP/account send limits prevent SMS pumping (SEC-REQ-009); security notifications cannot be disabled by users (BR-NTF-02).

## Acceptance criteria

- AC-IR003-01: Failover test — simulated primary timeout results in an automatic secondary send that is delivered inside the OTP validity window.
- AC-IR003-02: Selectivity — failover occurs only on timeout/error; a successful primary send never produces a duplicate message.
- AC-IR003-03: Receipts — each message records a delivery receipt/status in logs and metrics, attributable by correlation ID.
- AC-IR003-04: Total outage — with both providers failing, an alert reaches on-call within the alerting window and the WhatsApp fallback is attempted (BR-NTF-03).

## Related IDs

`DEP-06` · `C-06` · `C-26` · `FR-001` · `FR-017` · `BR-AUTH-01` · `BR-AUTH-03` · `BR-NTF-02` · `BR-NTF-03` · `BR-NTF-04` · `SEC-REQ-007` · `SEC-REQ-009` · `INT-REQ-004` · `RISK-006`

## Verification method
Integration tests with stubbed providers covering failover, duplicate suppression, and dual-outage alerting; DLR webhook tests; carrier SIM verification per the test-device lab (`DEP-12`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
