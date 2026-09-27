---
document_id: DOC-SR-002
title: SEC-REQ-002 — Credential storage
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-006, SEC-REQ-007, FR-001, NFR-019]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-002 — Credential storage

> Registry summary (`requirements-overview.md` §3): passwords bcrypt (cost 12); never store plaintext; phone numbers encrypted at rest.

**Priority:** Critical · **STRIDE:** Information disclosure (I), Spoofing (S) · **Failure impact:** CRITICAL

## Description
Credentials and identity data are stored only in irreversible or encrypted form: passwords as bcrypt cost-12 hashes, classified PII (phone numbers, names, addresses, KYC references) encrypted at rest with AES-256 (SEC-REQ-006), and no secret or verification code written in readable form to any store or log.

## Security rationale
A database dump, stolen backup, or insider read must not yield usable credentials or readable PII. Plaintext or weakly hashed passwords turn a storage breach into mass account takeover; unencrypted phone numbers expose the platform's entire identity graph. Threat: bulk credential/PII disclosure → STRIDE **Information disclosure**, enabling **Spoofing**.

## Requirement statements

- R1: Passwords are hashed with bcrypt cost 12 (BR-AUTH-02); input policy is ≥8 characters containing upper case, lower case, and a digit, enforced before hashing.
- R2: Plaintext passwords are never persisted, never returned by any API, and never written to logs, traces, or error reports (`VERIFIED` — BR-AUTH-02 "never logged").
- R3: Phone numbers and classified PII are encrypted at rest with AES-256; encryption keys are held outside the database (SEC-REQ-007) and never stored beside the ciphertext.
- R4: OTP values, password-reset tokens, and provider credentials are excluded from application logs (`INFERENCE` — extends the BR-AUTH-02 never-logged principle to all verification material).
- R5: Backups and database exports contain no usable credential or readable PII without the external key service.

## Acceptance criteria

- AC-SR002-01: Storage inspection test — the users table contains only bcrypt hashes; cost factor 12 confirmed by re-hash verification; no plaintext-password column exists in the schema.
- AC-SR002-02: Automated log-scan test across the auth flow suite asserts that password and OTP values appear in zero log lines.
- AC-SR002-03: Encryption test — a raw database dump shows ciphertext for classified columns; decryption succeeds only through the key service, not with database credentials alone.
- AC-SR002-04: Policy test — passwords shorter than 8 characters or missing a required character class are rejected at registration and at password change with a stable error code.

## Related IDs

`BR-AUTH-01` · `BR-AUTH-02` · `C-06` · `FR-001` · `SEC-REQ-006` · `SEC-REQ-007` · `NFR-019` · `DEP-09`

## Verification method

Unit tests for hashing and policy, database/backup inspection evidence, automated log scanning in CI, and code review of all persistence paths handling credentials.

## Failure impact

**CRITICAL** — a single storage breach exposes every customer's credential and identity data, enabling mass account takeover of funded wallets and a reportable personal-data incident under PDPA-aligned controls (NFR-019, `DEP-09`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
