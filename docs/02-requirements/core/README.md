---
document_id: DOC-REQ-003
title: 02 Requirements — core/ portal folder
category: 02-requirements
status: approved
version: 1.2
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-REQ-002]
---

# 02 Requirements · `core/`

## Purpose

One of the five portal subfolders of `02-requirements/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-REQ-003 | This portal index — purpose, file table |
| [../data/core/](../data/core/) | — | DATA-REQ files — now in the `data/` section (index: `../data/index.md`) |
| [../functional/core/](../functional/core/) | — | FR files — now in the `functional/` section (index: `../functional/index.md`) |
| [INT-REQ-001.md](INT-REQ-001.md) | DOC-IR-001 | INT-REQ-001 — Wallet top-up providers |
| [INT-REQ-002.md](INT-REQ-002.md) | DOC-IR-002 | INT-REQ-002 — Bank transfer top-up |
| [INT-REQ-003.md](INT-REQ-003.md) | DOC-IR-003 | INT-REQ-003 — SMS provider failover |
| [INT-REQ-004.md](INT-REQ-004.md) | DOC-IR-004 | INT-REQ-004 — WhatsApp Business notifications |
| [INT-REQ-005.md](INT-REQ-005.md) | DOC-IR-005 | INT-REQ-005 — Delivery orchestration |
| [INT-REQ-006.md](INT-REQ-006.md) | DOC-IR-006 | INT-REQ-006 — Webhook robustness |
| [INT-REQ-007.md](INT-REQ-007.md) | DOC-IR-007 | INT-REQ-007 — Observability export |
| [INT-REQ-008.md](INT-REQ-008.md) | DOC-IR-008 | INT-REQ-008 — Provider abstraction |
| [NFR-001.md](NFR-001.md) | DOC-NFR-001 | NFR-001 — API Response Time |
| [NFR-002.md](NFR-002.md) | DOC-NFR-002 | NFR-002 — Client Performance |
| [NFR-003.md](NFR-003.md) | DOC-NFR-003 | NFR-003 — Concurrency |
| [NFR-004.md](NFR-004.md) | DOC-NFR-004 | NFR-004 — Caching |
| [NFR-005.md](NFR-005.md) | DOC-NFR-005 | NFR-005 — Uptime |
| [NFR-006.md](NFR-006.md) | DOC-NFR-006 | NFR-006 — RTO / RPO |
| [NFR-007.md](NFR-007.md) | DOC-NFR-007 | NFR-007 — Fault Tolerance |
| [NFR-008.md](NFR-008.md) | DOC-NFR-008 | NFR-008 — Data Integrity |
| [NFR-009.md](NFR-009.md) | DOC-NFR-009 | NFR-009 — Modularity & standards |
| [NFR-010.md](NFR-010.md) | DOC-NFR-010 | NFR-010 — Testability |
| [NFR-011.md](NFR-011.md) | DOC-NFR-011 | NFR-011 — WCAG 2.1 AA |
| [NFR-012.md](NFR-012.md) | DOC-NFR-012 | NFR-012 — Core-task efficiency |
| [NFR-013.md](NFR-013.md) | DOC-NFR-013 | NFR-013 — Bilingual RTL/LTR |
| [NFR-014.md](NFR-014.md) | DOC-NFR-014 | NFR-014 — Logging/metrics/tracing |
| [NFR-015.md](NFR-015.md) | DOC-NFR-015 | NFR-015 — Browsers/devices |
| [NFR-016.md](NFR-016.md) | DOC-NFR-016 | NFR-016 — Deployment |
| [NFR-017.md](NFR-017.md) | DOC-NFR-017 | NFR-017 — Storage growth |
| [NFR-018.md](NFR-018.md) | DOC-NFR-018 | NFR-018 — Scale-out path |
| [NFR-019.md](NFR-019.md) | DOC-NFR-019 | NFR-019 — Legal/data |
| [NFR-020.md](NFR-020.md) | DOC-NFR-020 | NFR-020 — Supportability |
| [SEC-REQ-001.md](SEC-REQ-001.md) | DOC-SR-001 | SEC-REQ-001 — Strong phone-based verification |
| [SEC-REQ-002.md](SEC-REQ-002.md) | DOC-SR-002 | SEC-REQ-002 — Credential storage |
| [SEC-REQ-003.md](SEC-REQ-003.md) | DOC-SR-003 | SEC-REQ-003 — Token security |
| [SEC-REQ-004.md](SEC-REQ-004.md) | DOC-SR-004 | SEC-REQ-004 — Server-side authorization |
| [SEC-REQ-005.md](SEC-REQ-005.md) | DOC-SR-005 | SEC-REQ-005 — Brute-force protection |
| [SEC-REQ-006.md](SEC-REQ-006.md) | DOC-SR-006 | SEC-REQ-006 — Transport & data encryption |
| [SEC-REQ-007.md](SEC-REQ-007.md) | DOC-SR-007 | SEC-REQ-007 — Secrets management |
| [SEC-REQ-008.md](SEC-REQ-008.md) | DOC-SR-008 | SEC-REQ-008 — Injection/XSS/CSRF defense |
| [SEC-REQ-009.md](SEC-REQ-009.md) | DOC-SR-009 | SEC-REQ-009 — Rate limiting & abuse control |
| [SEC-REQ-010.md](SEC-REQ-010.md) | DOC-SR-010 | SEC-REQ-010 — Audit trail integrity |
| [SEC-REQ-011.md](SEC-REQ-011.md) | DOC-SR-011 | SEC-REQ-011 — File upload security |
| [SEC-REQ-012.md](SEC-REQ-012.md) | DOC-SR-012 | SEC-REQ-012 — Vulnerability management |
| [SEC-REQ-013.md](SEC-REQ-013.md) | DOC-SR-013 | SEC-REQ-013 — Anti-enumeration uniform responses |
| [SEC-REQ-014.md](SEC-REQ-014.md) | DOC-SR-014 | SEC-REQ-014 — Per-surface CORS policy |
| [SEC-REQ-015.md](SEC-REQ-015.md) | DOC-SR-015 | SEC-REQ-015 — Object-storage access control |
| [SEC-REQ-016.md](SEC-REQ-016.md) | DOC-SR-016 | SEC-REQ-016 — Per-destination OTP resend limits |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (68 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration (data/ + functional/ sections) | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
| 1.2 | 2026-10-02 | Phase-7 propagation catch-up: Contents rows added for `SEC-REQ-013`…`SEC-REQ-016` (`DOC-SR-013`…`016`) | Session-013 wave-E leftover sweep — four phase-7 files exist in `core/` but were absent from the file table (verified on disk) |
