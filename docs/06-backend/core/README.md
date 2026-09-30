---
document_id: DOC-BE-010
title: 06 Backend — core/ portal folder
category: 06-backend
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-BE-001]
---

# 06 Backend · `core/`

## Purpose

One of the five portal subfolders of `06-backend/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-BE-010 | This portal index — purpose, file table |
| [authentication.md](authentication.md) | DOC-BE-003 | Authentication — Implementation Placement (FR-001, SEC-REQ-001…003) |
| [authorization.md](authorization.md) | DOC-BE-004 | Authorization — Implementation Placement (FR-002, SEC-REQ-004) |
| [backend-architecture.md](backend-architecture.md) | DOC-BE-002 | Backend Architecture — NestJS Modular Monolith Layout |
| [background-processing.md](background-processing.md) | DOC-BE-006 | Background Processing — BullMQ Queues, Jobs & Scheduling |
| [business-logic-placement.md](business-logic-placement.md) | DOC-BE-005 | Business Logic Placement — Rule ID → Module → Service → Enforcement Point |
| [caching.md](caching.md) | DOC-BE-007 | Caching — Redis Strategy, TTLs, Invalidation & Non-Cacheable Data |
| [error-handling.md](error-handling.md) | DOC-BE-008 | Error Handling — Exception Filters, Error Codes & Structured Logging |
| [validation.md](validation.md) | DOC-BE-009 | Validation — DTOs, Business Validation, Idempotency & Payload Limits |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (8 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
