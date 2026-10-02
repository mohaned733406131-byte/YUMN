---
document_id: DOC-NFD-010
title: 12 Non Functional — core/ portal folder
category: 12-non-functional
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-NFD-001]
---

# 12 Non Functional · `core/`

## Purpose

One of the five portal subfolders of `12-non-functional/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-NFD-010 | This portal index — purpose, file table |
| [accessibility.md](accessibility.md) | DOC-NFD-009 | Accessibility — Measurable Targets & Verification |
| [compliance-and-legal.md](compliance-and-legal.md) | DOC-NFD-007 | Compliance & Legal Detail — Data Protection, Wallet Regulation, VAT & Legal Deliverables |
| [maintainability.md](maintainability.md) | DOC-NFD-005 | Maintainability Detail — Standards, Test Pyramid, Docs-as-Code & Environment Parity |
| [observability.md](observability.md) | DOC-NFD-006 | Observability Detail — Signals, Dashboards, Alerting & Runbooks |
| [performance.md](performance.md) | DOC-NFD-002 | Performance Detail — Latency Budgets, Tooling & Degradation Under Load |
| [reliability.md](reliability.md) | DOC-NFD-004 | Reliability Detail — Availability Math, Degradation Matrix & Integrity Standards |
| [scalability.md](scalability.md) | DOC-NFD-003 | Scalability Detail — Capacity Model, Scaling Levers & Data Growth Path |
| [usability-and-support.md](usability-and-support.md) | DOC-NFD-008 | Usability & Support Detail — Task Efficiency, Localization Gates & Human Support Ops |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (8 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
