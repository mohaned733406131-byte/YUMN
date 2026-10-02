---
document_id: DOC-SEC-009
title: 09 Security — core/ portal folder
category: 09-security
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-SEC-001]
---

# 09 Security · `core/`

## Purpose

One of the five portal subfolders of `09-security/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-SEC-009 | This portal index — purpose, file table |
| [authentication.md](authentication.md) | DOC-SEC-003 | Authentication Security Design (FR-001) |
| [data-protection.md](data-protection.md) | DOC-SEC-006 | Data Protection — Encryption, Hashing & Log Masking |
| [rbac.md](rbac.md) | DOC-SEC-004 | RBAC — Definitive Permission Matrix (7 Actors) |
| [secrets-management.md](secrets-management.md) | DOC-SEC-005 | Secrets Management Policy |
| [security-controls.md](security-controls.md) | DOC-SEC-007 | Security Control Catalog (SEC-C-01 … SEC-C-24) |
| [security-findings.md](security-findings.md) | DOC-SEC-008 | Security Findings Register (SEC-001 … SEC-015) |
| [threat-model.md](threat-model.md) | DOC-SEC-002 | Threat Model — Assets, Trust Boundaries, STRIDE & Top Threats |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (7 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
