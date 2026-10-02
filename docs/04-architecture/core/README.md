---
document_id: DOC-ARCH-011
title: 04 Architecture — core/ portal folder
category: 04-architecture
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-ARCH-001]
---

# 04 Architecture · `core/`

## Purpose

One of the five portal subfolders of `04-architecture/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-ARCH-011 | This portal index — purpose, file table |
| [architecture-overview.md](architecture-overview.md) | DOC-ARCH-002 | Architecture Overview |
| [component-view.md](component-view.md) | DOC-ARCH-004 | Component View — NestJS Modules (B01–B13) |
| [container-view.md](container-view.md) | DOC-ARCH-003 | Container View |
| [data-flow.md](data-flow.md) | DOC-ARCH-007 | Technical Data Flow |
| [deployment-view.md](deployment-view.md) | DOC-ARCH-005 | Deployment View (Docker Compose) |
| [module-boundaries.md](module-boundaries.md) | DOC-ARCH-006 | Module Boundaries (Modular Monolith) |
| [scalability.md](scalability.md) | DOC-ARCH-008 | Scalability |
| [technology-stack.md](technology-stack.md) | DOC-ARCH-009 | Technology Stack Register |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (8 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
