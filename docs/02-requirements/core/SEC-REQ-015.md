---
document_id: DOC-SR-015
title: SEC-REQ-015 — Object-storage access control
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-006, SEC-REQ-011, FR-007, DATA-REQ-002]
related_documents: [DOC-REQ-001, DOC-OVR-012]
---

# SEC-REQ-015 — Object-storage access control

> Registry summary (`requirements-overview.md` §3): deny anonymous access and listing on all MinIO buckets, short presigned-URL TTLs, separate media origin, server-generated object keys, and quarterly bucket-policy review verified in tests.

**Priority:** Medium · **STRIDE:** Information Disclosure (I) · **Failure impact:** MEDIUM

## Description
Object storage (MinIO — the presigned store in `../../09-security/core/security-controls.md` line 100) holds KYC documents, product media and user uploads, yet no canon document specifies bucket policy: `../../09-security/core/security-findings.md` `SEC-008` (lines 99–105, severity MEDIUM) asks "Bucket policies (anonymous listing blocked?), presigned-URL TTL … not specified anywhere". This requirement fixes deny-by-default bucket access, bounded presigned URLs, a separate media origin, server-generated keys and a recurring policy review. Registration recorded in `DOC-OVR-012` §5.

## Security rationale
An anonymously listable bucket publishes every uploaded KYC scan and private document to anyone with the endpoint; an over-long presigned URL leaks the same bytes the moment the link is copied or logged; user-controlled object keys enable path manipulation and overwrite of other tenants' objects. Media served from the API origin also inherits the session's cookie scope. Threat: bulk disclosure of PII and documents → STRIDE **Information Disclosure**.

## Requirement statements

- R1: Every MinIO bucket denies anonymous access and anonymous listing by default — access happens only through authenticated, authorized paths or short-lived presigned URLs (`SEC-008`).
- R2: Presigned URLs are minted only server-side, per-object, with a short, configuration-capped TTL so a leaked link expires before it can be broadly shared (exact TTL duration is a control-level configuration decision — `INFERENCE` for the value, `VERIFIED` for the requirement to cap it).
- R3: User-facing media is served from a separate media origin that carries no session cookies and no access to authenticated API routes (`SEC-008` / `DOC-OVR-012` wording).
- R4: Object keys are generated server-side (never taken raw from user input), scoped per owner (user/store), so clients cannot address, overwrite or enumerate another owner's objects (extends `DATA-REQ-008` ownership boundaries to object keys).
- R5: Bucket policies are reviewed quarterly and the review is recorded, with an automated test asserting anonymous access/listing stay denied (`SEC-008` recommendation).

## Acceptance criteria

- AC-SR015-01: Given every bucket, when an unauthenticated client attempts object read and bucket list, then both are denied — zero objects are disclosed.
- AC-SR015-02: Given a presigned URL, when it is requested after its TTL, then access is rejected; while valid, it grants only that single object and nothing else in the bucket.
- AC-SR015-03: Given user-supplied upload input containing an object key, when the upload is processed, then the stored key is the server-generated, owner-scoped one — a cross-owner key is never honored.
- AC-SR015-04: Given the quarterly review record, when the policy test runs each cycle, then anonymous access/listing remain denied and the review entry exists with date and reviewer.

## Related IDs

`SEC-REQ-006` · `SEC-REQ-011` · `DATA-REQ-002` · `DATA-REQ-008` · `FR-007` · `FR-004` · `INT-REQ-002` · `SEC-008`

## Verification method

Automated anonymous-access/listing tests against every bucket; presigned-URL expiry test; key-generation review (upload path inspection); quarterly bucket-policy review record inspection; findings tracked in `../../09-security/core/security-findings.md` (`SEC-008`).

## Failure impact

**MEDIUM** — exposure is document/PII bulk disclosure (KYC scans, private uploads) rather than direct ledger movement, but it is a PDPA-aligned control (`NFR-019`) and a single listable bucket leaks every tenant's documents at once.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial requirement | Session-011 owner directive (`prompt-011.md` §4.7) — delta accepted in `DOC-OVR-012` §5 (source: `security-findings.md` `SEC-008` lines 99–105; `security-controls.md` line 100) |
