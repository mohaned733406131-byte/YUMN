---
document_id: DOC-SR-006
title: SEC-REQ-006 — Transport & data encryption
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-002, SEC-REQ-007, FR-013, NFR-019]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-006 — Transport & data encryption

> Registry summary (`requirements-overview.md` §3): TLS 1.3 enforced; AES-256 at rest for PII/financial fields.

**Priority:** Critical · **STRIDE:** Information disclosure (I), Tampering (T) · **Failure impact:** CRITICAL

## Description
All traffic — client↔API, service↔database/cache/queue, and provider callbacks — is encrypted in transit with TLS 1.3, and classified PII and financial fields are encrypted at rest with AES-256. Keys and certificates are managed outside code and configuration repositories (SEC-REQ-007).

## Security rationale
Yemeni mobile networks and public Wi-Fi are untrusted; unencrypted transit exposes OTPs, tokens, wallet balances, and delivery codes to interception and tampering (man-in-the-middle), while unencrypted storage exposes PII/financial records on disk, in snapshots, and in backups. Threat: eavesdropping and transit tampering → STRIDE **Information disclosure** and **Tampering**.

## Requirement statements

- R1: TLS 1.3 is enforced on all external endpoints; plain HTTP is redirected to HTTPS; HSTS is returned on every response (control detail in `09-security/`).
- R2: PII and financial fields (phone numbers, names, addresses, KYC references, ledger and wallet records) are encrypted at rest with AES-256 per `16-data/data-classification.md`.
- R3: Database, Redis, and internal service connections require encrypted transport (`sslmode=require` / TLS); plaintext connections are refused.
- R4: Encryption keys, TLS private keys, and certificates live in the environment/secrets manager (SEC-REQ-007), are never committed, and certificate expiry is monitored with alerts before expiry (supports C-26).
- R5: No PII, secrets, or tokens appear in logs, metrics labels, or error payloads (cross SEC-REQ-002 / SEC-REQ-007).
- R6: Compliance note — PDPA (Law 11/2012) control detail is `INSUFFICIENT EVIDENCE` pending `DEP-09`; no PCI-DSS scope exists because card data is never accepted (C-02).

## Acceptance criteria

- AC-SR006-01: TLS scan — only TLS 1.3 accepted on all external hosts; TLS 1.2 and below are refused; HTTP requests redirect to HTTPS and HSTS headers are present.
- AC-SR006-02: At-rest test — a raw database/backup extract shows ciphertext for classified columns; decryption requires the external key service.
- AC-SR006-03: Connection test — a plaintext connection attempt to PostgreSQL/Redis is refused; configured endpoints require TLS.
- AC-SR006-04: Certificate monitoring test — a certificate placed near expiry triggers an ops alert before expiration.

## Related IDs

`SEC-REQ-002` · `SEC-REQ-007` · `FR-001` · `FR-013` · `NFR-019` · `C-02` · `C-26` · `DEP-08` · `DEP-09`

## Verification method

Automated TLS/scanning tests in CI plus configuration review; database/backup extraction inspection; certificate-monitoring alert test; evidence recorded in `13-testing/` and `09-security/`.

## Failure impact

**CRITICAL** — interception of OTPs or tokens yields account takeover; tampering with payment callbacks yields fraudulent wallet credits; plaintext PII/financial storage is a reportable breach under PDPA-aligned controls (NFR-019).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
