---
document_id: DOC-IR-006
title: INT-REQ-006 — Webhook robustness
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-001, INT-REQ-003, INT-REQ-004, FR-013, FR-017]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-010]
---

# INT-REQ-006 — Webhook robustness

> Registry summary (`requirements-overview.md` §5): signed webhooks, idempotent handlers, 3 retries + exponential backoff + DLQ (BR-PLT-05). Rule text of record: **BR-PLT-02** (jobs retry 3× with exponential backoff, then DLQ; DLQ depth alerts).

**Dependency risk:** HIGH — shared control for all `DEP-05`/`DEP-06` inbound callbacks; failure stalls wallet credits and notification status handling.

## Purpose
Make every inbound webhook (payment provider callbacks, SMS delivery receipts, WhatsApp status updates) safe to receive repeatedly, hostile-input-proof, and never lost: verify → persist → process idempotently, with bounded retries and a dead-letter queue.

## Interface expectations

- **Receive & verify:** verify HMAC signature with constant-time comparison and check the replay window before parsing; acknowledge `200` only after the raw payload is durably persisted — total handling within 10 s.
- **Idempotency:** the provider transaction/message ID is the idempotency key (BR-PLT-03); processing the same webhook N times produces one domain effect (BR-PAY-08 for money paths).
- **Retries:** handler failures retry 3× with exponential backoff, then dead-letter queue; DLQ depth triggers an alert (BR-PLT-01, BR-PLT-02).
- **Replay:** stored raw payloads can be re-driven from the DLQ/console after a fix, with identical idempotency guarantees.

## Data exchanged
Raw body, signature/timestamp headers, source IP, received timestamp (stored for forensics), parsed domain event, correlation ID. Never logs secrets or full message bodies containing OTP codes (SEC-REQ-002).

## Failure behavior & fallback
Invalid signature → `401`, dropped, alert counter incremented; malformed payload → `422` logged, no partial processing; provider retries are safe because handlers are idempotent; handler crash/timeouts → BullMQ retry then DLQ; DLQ non-empty → ops alert (NFR-014) — never silent loss (NFR-007).

## Security
HMAC-SHA256 with constant-time compare, IP allowlist per provider, secrets from environment only (SEC-REQ-007), replay window on timestamp/nonce, and audit entries for any money-moving effect produced by a webhook (BR-PLT-06).

## Acceptance criteria

- AC-IR006-01: Idempotency — the same webhook delivered 3 times (and once out of order) results in exactly one domain effect and one ledger credit where applicable.
- AC-IR006-02: Forgery — a tampered payload or wrong signature is rejected with 401, increments a security metric, and produces no effect.
- AC-IR006-03: Retry path — a handler that always fails is retried 3 times with increasing backoff, lands in DLQ, and fires an alert.
- AC-IR006-04: Timeliness — the endpoint persists and acknowledges within 10 s under load; slow business logic never blocks the provider callback path.

## Related IDs

`BR-PLT-01` · `BR-PLT-02` · `BR-PLT-03` · `BR-PAY-03` · `BR-PAY-06` · `BR-PAY-08` · `SEC-REQ-002` · `SEC-REQ-007` · `SEC-REQ-010` · `FR-013` · `FR-017` · `NFR-007` · `INT-REQ-001` · `INT-REQ-003` · `INT-REQ-004`

## Verification method
Integration tests replaying captured provider fixtures (duplicate, out-of-order, forged, malformed), failure-injection test for retry/DLQ behavior, and load assertion on the 10 s acknowledgement bound.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
