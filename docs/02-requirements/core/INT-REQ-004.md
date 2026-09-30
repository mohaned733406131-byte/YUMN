---
document_id: DOC-IR-004
title: INT-REQ-004 — WhatsApp Business notifications
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-003, INT-REQ-006, FR-001, FR-017]
related_documents: [DOC-REQ-001, DOC-OVR-010, DOC-BA-005]
---

# INT-REQ-004 — WhatsApp Business notifications

> Registry summary (`requirements-overview.md` §5): template messages for OTP fallback, order updates; approval-gated templates.

**Dependency risk:** HIGH — `DEP-06` WhatsApp Business API approval is **NOT STARTED**; mitigated because SMS remains the primary OTP channel (BR-NTF-03).

## Purpose
Deliver transactional notifications over WhatsApp Business (FR-017) — OTP fallback (BR-NTF-03), order lifecycle updates, security notices — using only pre-approved message templates in Arabic and English.

## Interface expectations

- **Send:** `sendTemplate(templateName, phone, params, locale)` through the Business API with 10 s timeout; queue-based via BullMQ (C-20) with 3 retries + exponential backoff then DLQ (BR-PLT-01, BR-PLT-02).
- **Templates:** every template is registered and **approved before use**; template names and parameter lists are versioned in `10-integrations/`; unapproved or rejected template IDs fail the job to DLQ with an alert.
- **Status:** delivery status callbacks arrive as signed webhooks per INT-REQ-006 and are logged per message.
- **Environments:** WhatsApp Business sandbox/test number certification before production (DEP-06 gate).

## Data exchanged
Recipient phone (`^7[0-9]{8}$`), approved template name + parameters (order reference, status, amount in YER — never full PII or credentials), locale `ar`/`en` (BR-NTF-04), correlation ID, delivery status. Message bodies with OTP codes stay out of logs (`INFERENCE`, per SEC-REQ-002 discipline).

## Failure behavior & fallback
Template rejected by the provider → job to DLQ + alert, no silent substitution; API timeout/outage → queued retries; persistent failure on OTP traffic → SMS primary path already succeeded or is retried (BR-NTF-03); marketing-category opt-out honored while security messages still send (BR-NTF-02, BR-NTF-05).

## Security
Webhook signature verification with constant-time compare + IP allowlist; Business API credentials and webhook secrets in environment only (SEC-REQ-007); user opt-out state enforced per channel (BR-NTF-05); no marketing templates may carry financial data.

## Acceptance criteria

- AC-IR004-01: Fallback — when the SMS primary fails, the OTP is delivered over WhatsApp inside its 5-minute validity window (BR-NTF-03).
- AC-IR004-02: Approval gate — submitting an unapproved template ID fails to DLQ and raises an alert; no message is sent.
- AC-IR004-03: Preferences — a user with marketing opt-out still receives OTP/security messages; opted-out marketing categories produce zero sends (BR-NTF-02/05).
- AC-IR004-04: Localization — each template renders in `ar` and `en` and follows the user's locale with Arabic default (BR-NTF-04, C-24).

## Related IDs

`DEP-06` · `C-24` · `FR-001` · `FR-017` · `BR-NTF-02` · `BR-NTF-03` · `BR-NTF-04` · `BR-NTF-05` · `BR-PLT-02` · `SEC-REQ-007` · `INT-REQ-003` · `INT-REQ-006` · `RISK-006`

## Verification method
Integration tests against the provider sandbox (send, status callback, template rejection), preference/opt-out matrix tests, and bilingual template rendering checks; approval evidence recorded in `10-integrations/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
