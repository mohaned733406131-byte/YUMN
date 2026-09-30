---
document_id: DOC-SA-012
title: 03 System Analysis — core/ portal folder
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-SA-001]
---

# 03 System Analysis · `core/`

## Purpose

One of the five portal subfolders of `03-system-analysis/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-SA-012 | This portal index — purpose, file table |
| [data-flow.md](data-flow.md) | DOC-SA-005 | Logical Data Flow (Analysis Level) |
| [edge-cases.md](edge-cases.md) | DOC-SA-008 | Edge Cases |
| [erp-finance-departments.md](erp-finance-departments.md) | DOC-SA-011 | ERP & Finance Departments — accounts, sales, purchases, inventory, reports, periods |
| [failure-modes.md](failure-modes.md) | DOC-SA-009 | Failure Modes & Analysis-Level Handling |
| [functional-analysis.md](functional-analysis.md) | DOC-SA-004 | Functional Analysis by Block (B01–B13) |
| [logical-components.md](logical-components.md) | DOC-SA-006 | Logical Components |
| [sequence-flows.md](sequence-flows.md) | DOC-SA-007 | Key Sequence Flows |
| [state-transitions.md](state-transitions.md) | DOC-SA-010 | State Transitions — Canonical 17-State Order Machine |
| [system-boundary.md](system-boundary.md) | DOC-SA-002 | System Boundary |
| [system-context.md](system-context.md) | DOC-SA-003 | System Context View |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (10 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
