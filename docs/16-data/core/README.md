---
document_id: DOC-DTA-008
title: 16 Data — core/ portal folder
category: 16-data
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-DTA-001]
---

# 16 Data · `core/`

## Purpose

One of the five portal subfolders of `16-data/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-DTA-008 | This portal index — purpose, file table |
| [data-classification.md](data-classification.md) | DOC-DTA-004 | Data Classification Scheme & Element Inventory |
| [data-deletion-and-privacy.md](data-deletion-and-privacy.md) | DOC-DTA-006 | Data Deletion, Anonymization & Privacy Procedures |
| [data-lifecycle.md](data-lifecycle.md) | DOC-DTA-002 | Data Lifecycle by Category |
| [data-ownership.md](data-ownership.md) | DOC-DTA-003 | Data Ownership & Access Matrix |
| [data-quality.md](data-quality.md) | DOC-DTA-007 | Data Quality Framework |
| [retention-and-archival.md](retention-and-archival.md) | DOC-DTA-005 | Retention & Archival Schedule |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (6 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
