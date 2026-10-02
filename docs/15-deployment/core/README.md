---
document_id: DOC-DPL-007
title: 15 Deployment — core/ portal folder
category: 15-deployment
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-DPL-001]
---

# 15 Deployment · `core/`

## Purpose

One of the five portal subfolders of `15-deployment/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-DPL-007 | This portal index — purpose, file table |
| [build-and-release.md](build-and-release.md) | DOC-DPL-002 | Build & Release Artifacts |
| [deployment-process.md](deployment-process.md) | DOC-DPL-003 | Production Deployment Process (Runbook) |
| [health-checks.md](health-checks.md) | DOC-DPL-005 | Health Checks & Readiness Model |
| [production-readiness.md](production-readiness.md) | DOC-DPL-006 | Production Readiness — Go-Live Checklist & Sign-Off |
| [rollback.md](rollback.md) | DOC-DPL-004 | Rollback Strategy & Decision Tree |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (5 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
