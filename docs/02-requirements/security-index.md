---
document_id: DOC-SR-000
title: Security Requirements — README (SEC-REQ Index)
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-002, SEC-REQ-003, SEC-REQ-004, SEC-REQ-005, SEC-REQ-006, SEC-REQ-007, SEC-REQ-008, SEC-REQ-009, SEC-REQ-010, SEC-REQ-011, SEC-REQ-012]
related_documents: [DOC-REQ-001, DOC-REQ-002, DOC-BA-005, DOC-OVR-008]
---

# Security Requirements (`SEC-REQ-001` … `SEC-REQ-012`)

## Purpose

Expands the 12 security requirement IDs registered in [`requirements-overview.md` §3](requirements-overview.md) into testable statements with acceptance criteria and verification methods. The registry is canonical: IDs and titles in this directory never diverge from it, and no security requirement exists that is not registered there.

## Index

| ID | File | Title | STRIDE focus | Failure impact |
|---|---|---|---|---|
| SEC-REQ-001 | [SEC-REQ-001.md](core/SEC-REQ-001.md) | Strong phone-based verification | Spoofing | CRITICAL |
| SEC-REQ-002 | [SEC-REQ-002.md](core/SEC-REQ-002.md) | Credential storage | Information disclosure | CRITICAL |
| SEC-REQ-003 | [SEC-REQ-003.md](core/SEC-REQ-003.md) | Token security | Spoofing, Elevation of privilege | CRITICAL |
| SEC-REQ-004 | [SEC-REQ-004.md](core/SEC-REQ-004.md) | Server-side authorization | Elevation of privilege | CRITICAL |
| SEC-REQ-005 | [SEC-REQ-005.md](core/SEC-REQ-005.md) | Brute-force protection | Spoofing, Denial of service | HIGH |
| SEC-REQ-006 | [SEC-REQ-006.md](core/SEC-REQ-006.md) | Transport & data encryption | Information disclosure, Tampering | CRITICAL |
| SEC-REQ-007 | [SEC-REQ-007.md](core/SEC-REQ-007.md) | Secrets management | Information disclosure | CRITICAL |
| SEC-REQ-008 | [SEC-REQ-008.md](core/SEC-REQ-008.md) | Injection/XSS/CSRF defense | Tampering, Elevation of privilege | CRITICAL |
| SEC-REQ-009 | [SEC-REQ-009.md](core/SEC-REQ-009.md) | Rate limiting & abuse control | Denial of service | HIGH |
| SEC-REQ-010 | [SEC-REQ-010.md](core/SEC-REQ-010.md) | Audit trail integrity | Repudiation, Tampering | HIGH |
| SEC-REQ-011 | [SEC-REQ-011.md](core/SEC-REQ-011.md) | File upload security | Tampering, Information disclosure | HIGH |
| SEC-REQ-012 | [SEC-REQ-012.md](core/SEC-REQ-012.md) | Vulnerability management | Elevation of privilege, Tampering | HIGH |

## Relation to `09-security/`

- This directory owns the **requirements** — what must hold, stated testably, with acceptance criteria `AC-SRnnn-nn`.
- `09-security/` owns the **controls** — threat model, RBAC matrix, encryption/secrets design, and findings `SEC-nnn`: the design response to these requirements.
- Every control traces forward to at least one `SEC-REQ-*`; control implementation details are never copied into a requirement file — reference `09-security/` documents instead.

## Naming & ID Conventions

- Files: `SEC-REQ-nnn.md`. Document IDs: `DOC-SR-000` (this index) … `DOC-SR-012`. Acceptance criteria: `AC-SRnnn-nn` (e.g. `AC-SR003-02`).
- IDs are assigned only in `requirements-overview.md`; statuses follow root README §6; every file carries frontmatter with `category: 02-requirements`, `status: approved`, `source_of_truth: true`.

## Severity & Evidence Conventions

- **Failure impact** — severity of the consequence when the requirement is unmet: `CRITICAL` · `HIGH` · `MEDIUM` · `LOW` · `INFORMATIONAL` (root README §8).
- **STRIDE tag** in each file names the threat category the requirement addresses (S/T/R/I/D/E).
- Material statements are evidence-tagged `VERIFIED` (project evidence) · `INFERENCE` (logically derived) · `INSUFFICIENT EVIDENCE`. Yemeni PDPA (Law 11/2012) control detail remains `INSUFFICIENT EVIDENCE` pending the legal opinion in `DEP-09`.
- Constraint-driven scope exclusions: no card data → PCI-DSS out of scope (`C-02`); no email-primary auth (`C-06`); no GPS/location data (`C-16`).

## Verification

Each requirement declares its verification method (integration/negative security test, scan, config review, code review, pen test) and maps into `13-testing/` + `09-security/`. A requirement whose acceptance criteria cannot pass is incomplete per `02-requirements/README.md` Quality Rules.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial index (12 requirements) | Initial analysis |
