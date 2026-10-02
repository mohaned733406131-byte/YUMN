---
document_id: DOC-TPL-012
title: 23 Templates — core/ portal folder
category: 23-templates
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-TPL-001]
---

# 23 Templates · `core/`

## Purpose

One of the five portal subfolders of `23-templates/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-TPL-012 | This portal index — purpose, file table |
| [adr-template.md](adr-template.md) | DOC-TPL-008 | Architecture Decision Record Template (ADR-NNN.md) |
| [api-endpoint-template.md](api-endpoint-template.md) | DOC-TPL-006 | API Endpoint Group Template (endpoints/<group>.md) |
| [database-entity-template.md](database-entity-template.md) | DOC-TPL-007 | Database Entity Template (entities/<table>.md) |
| [requirement-template.md](requirement-template.md) | DOC-TPL-002 | Requirement Template (FR / NFR / SEC-REQ / DATA-REQ / INT-REQ) |
| [risk-template.md](risk-template.md) | DOC-TPL-009 | Risk Register Entry Template (RISK-NNN) |
| [security-finding-template.md](security-finding-template.md) | DOC-TPL-010 | Security Finding Template (SEC-NNN) |
| [test-case-template.md](test-case-template.md) | DOC-TPL-005 | Test Case Template (TC-NNN.md) |
| [use-case-template.md](use-case-template.md) | DOC-TPL-003 | Use Case Template (UC-NNN.md) |
| [validation-audit-template.md](validation-audit-template.md) | DOC-TPL-011 | Validation Audit Template (AUD-NN — 20-validation/) |
| [workflow-template.md](workflow-template.md) | DOC-TPL-004 | Workflow Template (workflow-NNN.md) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (10 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
