---
document_id: DOC-SR-011
title: SEC-REQ-011 — File upload security
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-006, SEC-REQ-012, FR-004, FR-007]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-011 — File upload security

> Registry summary (`requirements-overview.md` §3): type/size validation, EXIF strip, malware scan, no SVG execution; ≤5 MB images.

**Priority:** High · **STRIDE:** Tampering (T), Information disclosure (I) · **Failure impact:** HIGH

## Description
User-uploaded files — product images (≤10 per product), review images (≤5), KYC documents, and bank-transfer receipts — are validated by type and size, stripped of metadata, malware-scanned, and served from object storage (DEP-07 MinIO) as inert data that is never executed on the platform's origin.

## Security rationale
Uploads are the classic path to stored XSS (SVG/HTML), remote code execution (executable/script content), malware distribution, and metadata leakage (EXIF GPS/identity on customer photos). Threat: malicious payload storage and privacy leakage through file metadata → STRIDE **Tampering** and **Information disclosure**.

## Requirement statements

- R1: Accepted image formats are jpg/png/webp only; each file ≤5 MB; product images ≤10 and review images ≤5 (BR-CAT-08, BR-REV-03); size/type limits apply to KYC and receipt uploads as well (FR-007, INT-REQ-002).
- R2: Validation uses declared content type **and** file signature (magic bytes), not the filename extension alone; extension spoofing is rejected (`INFERENCE` — derived from the registry's type-validation requirement).
- R3: EXIF metadata (including GPS) is stripped from images on upload before storage (BR-CAT-08).
- R4: No SVG (or other active vector/HTML) content is accepted or ever rendered as executable; uploaded files are served with an inert content type and cannot execute on the platform origin.
- R5: Every upload is malware-scanned before it becomes retrievable; infected files are quarantined, rejected to the uploader, and alert operations.

## Acceptance criteria

- AC-SR011-01: Type test — uploads of `.svg`, `.html`, `.exe`, and double-extension payloads (e.g. `x.php.jpg` with script content) are rejected with a stable error code.
- AC-SR011-02: Size test — a 5 MB + 1 byte file is rejected; a 4.9 MB valid JPEG is accepted; the limit holds on every upload surface.
- AC-SR011-03: EXIF test — a JPEG containing GPS/identity EXIF is stored with those bytes absent (byte-level comparison of stored object vs source).
- AC-SR011-04: Malware test — a standard test signature file is not retrievable, is quarantined, and raises an alert; scanning completes before the file is served.

## Related IDs

`BR-CAT-08` · `BR-REV-03` · `FR-004` · `FR-006` · `FR-007` · `SEC-REQ-006` · `SEC-REQ-012` · `INT-REQ-002` · `DEP-07`

## Verification method

Integration tests on every upload endpoint (product, review, KYC, receipt), byte-level object inspection, malware-scan tool evidence, and DAST confirmation that no uploaded content executes on-origin.

## Failure impact

**HIGH** — stored XSS or executable content on the platform origin compromises users and admins; leaked EXIF metadata violates data-minimization expectations (DATA-REQ-002, NFR-019); malware distribution destroys marketplace trust.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
