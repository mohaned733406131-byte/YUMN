---
document_id: DOC-API-021
title: 07 Api — admin/ portal folder
category: 07-api
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-API-001]
---

# 07 Api · `admin/`

## Purpose

One of the five portal subfolders of `07-api/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **admin-console-specific material (platform operators)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-API-021 | This portal index — purpose, file table |
| [admin.md](admin.md) | DOC-API-019 | API-ADM — Platform Administration, Roles, Audit, Tickets & Health (FR-002, FR-019, FR-020) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (1 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
