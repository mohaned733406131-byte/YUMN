---
document_id: DOC-API-020
title: 07 Api — core/ portal folder
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

# 07 Api · `core/`

## Purpose

One of the five portal subfolders of `07-api/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-API-020 | This portal index — purpose, file table |
| [analytics.md](analytics.md) | DOC-API-018 | API-ANL — Vendor Analytics, Statements & Admin Reports (FR-018, FR-020) |
| [api-conventions.md](api-conventions.md) | DOC-API-002 | API Conventions — REST Rules, Headers, Idempotency & Uploads |
| [auth.md](auth.md) | DOC-API-006 | API-ATH — Authentication & Session Endpoints (FR-001) |
| [catalog.md](catalog.md) | DOC-API-009 | API-CAT — Catalog, Products, Inventory & Reviews (FR-004, FR-005, FR-006) |
| [content.md](content.md) | DOC-API-017 | API-CNT — Pages, Banners, Promotions & Coupons (FR-019, FR-011) |
| [error-model.md](error-model.md) | DOC-API-003 | API Error Model — Envelope, Status Mapping & Error-Code Catalog |
| [notifications.md](notifications.md) | DOC-API-016 | API-NTF — Notifications, Preferences & Devices (FR-017) |
| [orders.md](orders.md) | DOC-API-012 | API-ORD — Checkout & Order Lifecycle (FR-011, FR-012) |
| [pagination.md](pagination.md) | DOC-API-004 | API Pagination, Filtering, Sorting & Search Result Shape |
| [returns.md](returns.md) | DOC-API-015 | API-RET — Returns, Refunds & Disputes (FR-016) |
| [search.md](search.md) | DOC-API-010 | API-SRC — Search & Discovery (FR-009) |
| [stores.md](stores.md) | DOC-API-008 | API-VND — Vendor Onboarding, KYC, Store Configuration & Followers (FR-007, FR-008) |
| [users.md](users.md) | DOC-API-007 | API-USR — User Profile, Addresses, Preferences & Data Lifecycle (FR-003) |
| [wallet.md](wallet.md) | DOC-API-013 | API-WAL — Wallet, Payments, Escrow & Payouts (FR-013, FR-014) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (14 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
