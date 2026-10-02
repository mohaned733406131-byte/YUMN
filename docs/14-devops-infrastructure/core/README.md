---
document_id: DOC-OPS-009
title: 14 Devops Infrastructure — core/ portal folder
category: 14-devops-infrastructure
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-OPS-001]
---

# 14 Devops Infrastructure · `core/`

## Purpose

One of the five portal subfolders of `14-devops-infrastructure/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-OPS-009 | This portal index — purpose, file table |
| [backup-recovery.md](backup-recovery.md) | DOC-OPS-007 | Backup & Recovery Execution (DATA-REQ-004) |
| [ci-cd.md](ci-cd.md) | DOC-OPS-004 | CI/CD Pipelines (GitHub Actions) |
| [configuration.md](configuration.md) | DOC-OPS-005 | Configuration Management & Environment Variable Inventory |
| [docker-compose.md](docker-compose.md) | DOC-OPS-003 | Container Strategy (Docker Compose Service Inventory) |
| [environments.md](environments.md) | DOC-OPS-002 | Environments & Parity Rules |
| [host-hardening.md](host-hardening.md) | DOC-OPS-008 | Single-Host Hardening & Vulnerability Management |
| [monitoring-stack.md](monitoring-stack.md) | DOC-OPS-006 | Monitoring & Observability Stack (How Signals Are Run) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (7 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
