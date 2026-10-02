---
document_id: DOC-API-005
title: Endpoint Groups Index — 14 Groups, 221 Endpoints
category: 07-api
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-03
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020]
related_documents: [DOC-API-001, DOC-API-002, DOC-API-003, DOC-API-004, DOC-REQ-001]
---

# Endpoint Groups Index

Index of all 14 endpoint groups. Each group lives in one file, uses one group code, and numbers its endpoints `API-<GROUP>-NNN` sequentially from `001`. Read `api-conventions.md`, `error-model.md` and `pagination.md` before implementing any group.

---

## 1. Group Index

| # | Group code | File | Document ID | Primary FRs | Endpoints | Pagination mode (default) |
|---|---|---|---|---|---|---|
| 1 | **API-ATH** | [auth.md](auth.md) | DOC-API-006 | FR-001 | 12 | n/a (single-resource) |
| 2 | **API-USR** | [users.md](users.md) | DOC-API-007 | FR-003 | 13 | offset (addresses), n/a otherwise |
| 3 | **API-VND** | [stores.md](stores.md) | DOC-API-008 | FR-007, FR-008 | 21 | offset (followers/staff), cursor (storefront products) |
| 4 | **API-CAT** | [catalog.md](catalog.md) | DOC-API-009 | FR-004, FR-005, FR-006 | 22 | cursor (public feeds), offset (vendor tables) |
| 5 | **API-SRC** | [search.md](search.md) | DOC-API-010 | FR-009 | 3 | cursor (search), n/a (suggest) |
| 6 | **API-CRT** | [cart.md](../customer/cart.md) | DOC-API-011 | FR-010 | 7 | n/a (single cart resource) |
| 7 | **API-ORD** | [orders.md](orders.md) | DOC-API-012 | FR-011, FR-012 | 14 | cursor (feeds), offset (admin table) |
| 8 | **API-WAL** | [wallet.md](wallet.md) | DOC-API-013 | FR-013, FR-014 | 14 | cursor (ledger), offset (payouts) |
| 9 | **API-SHP** | [delivery.md](../delivery/delivery.md) | DOC-API-014 | FR-015 | 16 | cursor (job feeds) |
| 10 | **API-RET** | [returns.md](returns.md) | DOC-API-015 | FR-016 | 17 | cursor (customer/vendor feeds), offset (admin) |
| 11 | **API-NTF** | [notifications.md](notifications.md) | DOC-API-016 | FR-017 | 10 | cursor (inbox) |
| 12 | **API-CNT** | [content.md](content.md) | DOC-API-017 | FR-019 | 20 | offset (CMS tables) |
| 13 | **API-ANL** | [analytics.md](analytics.md) | DOC-API-018 | FR-018 | 9 | n/a (date-range bounded) |
| 14 | **API-ADM** | [admin.md](../admin/admin.md) | DOC-API-019 | FR-002, FR-020 | 43 | offset (tables), cursor (audit log) |
| | | | | | **221** | |

## 2. FR → Group Coverage (every FR covered)

| FR | Title (registry `DOC-REQ-001` §1) | Group(s) |
|---|---|---|
| FR-001 | Identity, Authentication & Session Management | API-ATH |
| FR-002 | Roles, Permissions & Access Control | API-ADM (role management) + every group's Roles column |
| FR-003 | User & Profile Management | API-USR (+ API-ATH sessions) |
| FR-004 | Product Catalog Management | API-CAT (+ API-ADM category/attribute management) |
| FR-005 | Inventory Management | API-CAT (inventory sub-resource) |
| FR-006 | Reviews & Ratings | API-CAT |
| FR-007 | Vendor Onboarding & KYC | API-VND (+ API-ADM decisions) |
| FR-008 | Store Management & Storefront Configuration | API-VND |
| FR-009 | Search & Discovery | API-SRC (+ API-CNT merchandising) |
| FR-010 | Shopping Cart | API-CRT |
| FR-011 | Checkout & Order Placement | API-ORD (+ API-CRT, API-WAL payment step) |
| FR-012 | Order Lifecycle Management | API-ORD (+ API-SHP scans, API-ADM overrides) |
| FR-013 | Wallet & Payment Processing | API-WAL (+ API-ADM verification/freeze) |
| FR-014 | Escrow, Commission & Vendor Payouts | API-WAL |
| FR-015 | Shipping & Delivery | API-SHP |
| FR-016 | Returns & Refunds | API-RET (+ API-WAL refund receipt) |
| FR-017 | Notifications & Messaging | API-NTF |
| FR-018 | Analytics & Reporting | API-ANL |
| FR-019 | Content & Promotions (CMS + Coupons) | API-CNT |
| FR-020 | Platform Administration, Settings & Audit | API-ADM (+ API-ORD overrides, API-RET arbitration) |

## 3. Cross-Group Conventions Reminder

| Concern | Authoritative file |
|---|---|
| Headers, idempotency, rate limits, uploads, deprecation | [`api-conventions.md`](api-conventions.md) |
| Error envelope, status mapping, code catalog | [`error-model.md`](error-model.md) |
| Pagination mode, filters, sorts, search shape | [`pagination.md`](pagination.md) |
| Order state machine (17 states, `409 STATE_CONFLICT`) | `../../03-system-analysis/core/state-transitions.md` |
| Business rule text (BR-*) | `../../01-business-analysis/business-rules.md` |
| Requirement registry (FR/NFR/SEC/DATA/INT) | `../../02-requirements/requirements-overview.md` |

## 4. Endpoint ID Rules

- Format `API-<GROUP>-NNN`; numbering starts at `001` per group and increments by 1 per endpoint row.
- IDs are permanent: a removed endpoint keeps its number retired (never reused); a new endpoint takes the next free number.
- Groups map 1:1 to files; an endpoint never appears in two files (related endpoints are cross-referenced, not duplicated).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-03 | Outbound refs corrected after the move into `07-api/core/`: 14 `core/<sibling>` hrefs → `<sibling>` + 3 prose/label copies, 3 portal hrefs → `../<portal>/<file>.md`, 3 cross-domain `../…` → `../../…` | Session-011 section-grouping rename follow-up (prompt-013 §2 leftover sweep) — moved-file outbound links / stale pre-portal path claims |
