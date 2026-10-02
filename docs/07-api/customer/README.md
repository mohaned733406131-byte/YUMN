---
document_id: DOC-API-023
title: 07 Api — customer/ portal folder
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

# 07 Api · `customer/`

## Purpose

One of the five portal subfolders of `07-api/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **customer-app-specific material (buyers)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-API-023 | This portal index — purpose, file table |
| [cart.md](cart.md) | DOC-API-011 | API-CRT — Shopping Cart (FR-010) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (1 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
