---
document_id: DOC-FE-010
title: 05 Frontend — core/ portal folder
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-FE-001]
---

# 05 Frontend · `core/`

## Purpose

One of the five portal subfolders of `05-frontend/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-FE-010 | This portal index — purpose, file table |
| [authentication-handling.md](authentication-handling.md) | DOC-FE-006 | Authentication Handling (Client) — OTP, Tokens & Session UX |
| [forms-and-validation.md](forms-and-validation.md) | DOC-FE-005 | Forms & Validation — Shared Schemas, Validation UX & Error Mapping |
| [frontend-architecture.md](frontend-architecture.md) | DOC-FE-002 | Frontend Architecture — Monorepo, Layering & Rendering Strategy |
| [frontend-performance.md](frontend-performance.md) | DOC-FE-009 | Frontend Performance — Budgets, Caching, Perceived Performance & RUM |
| [internationalization.md](internationalization.md) | DOC-FE-008 | Internationalization — ar-YE Default, en Parity & Content Policy |
| [routing.md](routing.md) | DOC-FE-003 | Routing — Route Map, Guards, Code Splitting & Slug Policy |
| [rtl-and-styling.md](rtl-and-styling.md) | DOC-FE-007 | RTL & Styling — CSS Strategy, Logical Properties, Numbers & Fonts |
| [state-management.md](state-management.md) | DOC-FE-004 | State Management — Server State, UI State & Cart Strategy |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (8 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
