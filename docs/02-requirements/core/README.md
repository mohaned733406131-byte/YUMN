---
document_id: DOC-REQ-003
title: 02 Requirements — core/ portal folder
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-REQ-002]
---

# 02 Requirements · `core/`

## Purpose

One of the five portal subfolders of `02-requirements/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-REQ-003 | This portal index — purpose, file table |
| [DATA-REQ-001.md](DATA-REQ-001.md) | DOC-DR-001 | DATA-REQ-001 — Integrity constraints |
| [DATA-REQ-002.md](DATA-REQ-002.md) | DOC-DR-002 | DATA-REQ-002 — Personal data minimization |
| [DATA-REQ-003.md](DATA-REQ-003.md) | DOC-DR-003 | DATA-REQ-003 — Retention & deletion |
| [DATA-REQ-004.md](DATA-REQ-004.md) | DOC-DR-004 | DATA-REQ-004 — Backup & restore |
| [DATA-REQ-005.md](DATA-REQ-005.md) | DOC-DR-005 | DATA-REQ-005 — Schema evolution |
| [DATA-REQ-006.md](DATA-REQ-006.md) | DOC-DR-006 | DATA-REQ-006 — Data quality validation |
| [DATA-REQ-007.md](DATA-REQ-007.md) | DOC-DR-007 | DATA-REQ-007 — Financial immutability |
| [DATA-REQ-008.md](DATA-REQ-008.md) | DOC-DR-008 | DATA-REQ-008 — Ownership boundaries |
| [FR-001.md](FR-001.md) | DOC-FR-001 | FR-001 — Identity, Authentication & Session Management |
| [FR-002.md](FR-002.md) | DOC-FR-002 | FR-002 — Roles, Permissions & Access Control |
| [FR-003.md](FR-003.md) | DOC-FR-003 | FR-003 — User & Profile Management |
| [FR-004.md](FR-004.md) | DOC-FR-004 | FR-004 — Product Catalog Management |
| [FR-005.md](FR-005.md) | DOC-FR-005 | FR-005 — Inventory Management |
| [FR-006.md](FR-006.md) | DOC-FR-006 | FR-006 — Reviews & Ratings |
| [FR-007.md](FR-007.md) | DOC-FR-007 | FR-007 — Vendor Onboarding & KYC |
| [FR-008.md](FR-008.md) | DOC-FR-008 | FR-008 — Store Management & Storefront Configuration |
| [FR-009.md](FR-009.md) | DOC-FR-009 | FR-009 — Search & Discovery |
| [FR-010.md](FR-010.md) | DOC-FR-010 | FR-010 — Shopping Cart |
| [FR-011.md](FR-011.md) | DOC-FR-011 | FR-011 — Checkout & Order Placement |
| [FR-012.md](FR-012.md) | DOC-FR-012 | FR-012 — Order Lifecycle Management |
| [FR-013.md](FR-013.md) | DOC-FR-013 | FR-013 — Wallet & Payment Processing |
| [FR-014.md](FR-014.md) | DOC-FR-014 | FR-014 — Escrow, Commission & Vendor Payouts |
| [FR-015.md](FR-015.md) | DOC-FR-015 | FR-015 — Shipping & Delivery |
| [FR-016.md](FR-016.md) | DOC-FR-016 | FR-016 — Returns & Refunds |
| [FR-017.md](FR-017.md) | DOC-FR-017 | FR-017 — Notifications & Messaging |
| [FR-018.md](FR-018.md) | DOC-FR-018 | FR-018 — Analytics & Reporting |
| [FR-019.md](FR-019.md) | DOC-FR-019 | FR-019 — Content & Promotions (CMS + Coupons) |
| [FR-020.md](FR-020.md) | DOC-FR-020 | FR-020 — Platform Administration, Settings & Audit |
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

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (68 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
