---
document_id: DOC-DEC-003
title: 18 Decisions — core/ portal folder
category: 18-decisions
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-DEC-001]
---

# 18 Decisions · `core/`

## Purpose

One of the five portal subfolders of `18-decisions/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-DEC-003 | This portal index — purpose, file table |
| [ADR-001.md](ADR-001.md) | DOC-ADR-001 | "ADR-001: PostgreSQL 16 as the sole relational database" |
| [ADR-002.md](ADR-002.md) | DOC-ADR-002 | "ADR-002: Modular monolith instead of microservices" |
| [ADR-003.md](ADR-003.md) | DOC-ADR-003 | "ADR-003: NestJS 10 as the backend framework" |
| [ADR-004.md](ADR-004.md) | DOC-ADR-004 | "ADR-004: Docker Compose deployment; no Kubernetes in v1" |
| [ADR-005.md](ADR-005.md) | DOC-ADR-005 | "ADR-005: Redis 7 + BullMQ as the only queue/cache substrate" |
| [ADR-006.md](ADR-006.md) | DOC-ADR-006 | "ADR-006: Elasticsearch 8 for search & discovery" |
| [ADR-007.md](ADR-007.md) | DOC-ADR-007 | "ADR-007: MinIO for object storage" |
| [ADR-008.md](ADR-008.md) | DOC-ADR-008 | "ADR-008: React Native 0.73 + Next.js 14 for all client surfaces" |
| [ADR-009.md](ADR-009.md) | DOC-ADR-009 | "ADR-009: Wallet-only payments with provider adapters" |
| [ADR-010.md](ADR-010.md) | DOC-ADR-010 | "ADR-010: Phone + OTP authentication with short-lived JWTs" |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (10 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
