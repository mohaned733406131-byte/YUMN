---
document_id: DOC-API-001
title: API Contract Domain — Overview, Versioning & File Map
category: 07-api
status: approved
version: 1.3
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, NFR-001, NFR-013, SEC-REQ-004, SEC-REQ-009]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008, DOC-SA-010, DOC-FE-005, DOC-BE-003]
---

# API Contract Domain — Overview & File Map

**This directory (`07-api/`) is the single source of truth for the yumn HTTP API contract.** It defines the REST conventions, canonical error model, pagination semantics, and a full specification of every endpoint group. Backend modules (`06-backend/`), the frontend API SDK (`05-frontend/`), and test suites (`13-testing/`) consume this contract; use-case touchpoints in `01-business-analysis/` are conceptual — where they differ in wording, this contract governs (per `UC-000`).

---

## 1. Scope & Audience

| Aspect | Value |
|---|---|
| Style | JSON REST over HTTPS |
| Base path | `/api/v1` |
| Content type | `application/json; charset=utf-8` (multipart only for uploads) |
| Auth | JWT Bearer access token (15 min) + refresh token (7 days, single-use rotation) — `C-08`, `SEC-REQ-003` |
| Roles | `CUSTOMER`, `VENDOR`, `COURIER`, `ADMIN`, `SUPER_ADMIN`, `MODERATOR` (plus non-interactive `SYSTEM`) — FR-002 |
| Localization | `Accept-Language: ar` (default) / `en`; all error messages localized — `C-24`, `BR-PLT-05` |
| Money | Integer YER only — `BR-PAY-10`, `C-04` |
| Audience | Backend implementers, frontend SDK authors, QA/contract testers, integrators |

The contract covers all 20 functional requirements (FR-001…FR-020) across 14 endpoint groups and **221 endpoints**. Non-functional behavior (performance, availability) is specified in `12-non-functional/`; security controls in `09-security/`; integration callback contracts in `10-integrations/`.

---

## 2. Versioning Strategy

| Rule | Detail |
|---|---|
| URL version prefix | All endpoints live under `/api/v1`; the major version is part of the path, never a header |
| Additive changes | New optional fields, new endpoints, new enum values that clients must tolerate — no version bump |
| Breaking changes | Removing/renaming fields, changing types, tightening validation, changing status codes → new prefix `/api/v2`; `v1` continues for at least 6 months with an end-of-life notice |
| Deprecation signal | Deprecated endpoints return `Deprecation: true` and `Sunset: <RFC-1123 date>` headers (see `api-conventions.md` §9) |
| Never versioned | Error envelope shape, pagination envelope, auth header scheme, money representation — these are contract constants fixed by `error-model.md` and `pagination.md` |
| Client tolerance | Clients must ignore unknown response fields (forward compatibility), per `05-frontend/` SDK rules |

---

## 3. File Map (link map — every file in this domain)

| # | File | Document ID | Type | Content |
|---|---|---|---|---|
| 1 | [README.md](README.md) | DOC-API-001 | Overview (source of truth) | This file: scope, versioning, file map, group → FR matrix |
| 2 | [api-conventions.md](core/api-conventions.md) | DOC-API-002 | Conventions (source of truth) | REST rules, naming, methods, auth headers, roles, money/dates, idempotency, correlation IDs, rate-limit headers, deprecation, multipart uploads |
| 3 | [error-model.md](core/error-model.md) | DOC-API-003 | Error model (source of truth) | Canonical error envelope, HTTP status mapping, full error-code catalog by domain, ar/en localization |
| 4 | [pagination.md](core/pagination.md) | DOC-API-004 | Conventions (source of truth) | Cursor vs offset decision, page sizes, filter/sort syntax, ES search result shape, total-count policy |
| 5 | [endpoints/README.md](endpoints-index.md) | DOC-API-005 | Index (source of truth) | Index of all 14 endpoint groups with DOC IDs, endpoint counts, FR coverage |
| 6 | [endpoints/auth.md](core/auth.md) | DOC-API-006 | Endpoint spec | **API-ATH** — OTP, login, refresh, logout, password, sessions |
| 7 | [endpoints/users.md](core/users.md) | DOC-API-007 | Endpoint spec | **API-USR** — profile, addresses, preferences, avatar, deletion |
| 8 | [endpoints/stores.md](core/stores.md) | DOC-API-008 | Endpoint spec | **API-VND** — vendor onboarding/KYC, store config, follow, staff, payout account |
| 9 | [endpoints/catalog.md](core/catalog.md) | DOC-API-009 | Endpoint spec | **API-CAT** — categories, products, images, inventory, reviews |
| 10 | [endpoints/search.md](core/search.md) | DOC-API-010 | Endpoint spec | **API-SRC** — ES-backed search, facets, suggest, degrade |
| 11 | [endpoints/cart.md](customer/cart.md) | DOC-API-011 | Endpoint spec | **API-CRT** — cart CRUD, guards, merge, checkout view |
| 12 | [endpoints/orders.md](core/orders.md) | DOC-API-012 | Endpoint spec | **API-ORD** — checkout, orders, vendor fulfillment, cancel, admin overrides |
| 13 | [endpoints/wallet.md](core/wallet.md) | DOC-API-013 | Endpoint spec | **API-WAL** — balance, ledger, top-ups, payments, escrow, payouts, refunds |
| 14 | [endpoints/delivery.md](delivery/delivery.md) | DOC-API-014 | Endpoint spec | **API-SHP** — courier jobs, scans, delivery code, profile/availability |
| 15 | [endpoints/returns.md](core/returns.md) | DOC-API-015 | Endpoint spec | **API-RET** — returns, inspection, refunds, disputes |
| 16 | [endpoints/notifications.md](core/notifications.md) | DOC-API-016 | Endpoint spec | **API-NTF** — notification center, preferences, devices, deep links |
| 17 | [endpoints/content.md](core/content.md) | DOC-API-017 | Endpoint spec | **API-CNT** — CMS pages/banners, home, coupons, promotions |
| 18 | [endpoints/analytics.md](core/analytics.md) | DOC-API-018 | Endpoint spec | **API-ANL** — vendor/admin dashboards, reports, statements, CSV export |
| 19 | [endpoints/admin.md](admin/admin.md) | DOC-API-019 | Endpoint spec | **API-ADM** — moderation, KYC, categories/attributes, settings, audit, roles, tickets, health |
| [`core/`](core/README.md) | DOC-API-020 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-API-021 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-API-022 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-API-023 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-API-024 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

---

## 4. Group → Requirement Mapping

| Group | File | Endpoints | FR coverage | Key SEC/DATA/INT coverage |
|---|---|---|---|---|
| API-ATH | `core/auth.md` | 12 | FR-001 | SEC-REQ-001, SEC-REQ-003, SEC-REQ-005, SEC-REQ-009 |
| API-USR | `core/users.md` | 13 | FR-003 | SEC-REQ-001, SEC-REQ-006, SEC-REQ-011, DATA-REQ-002, DATA-REQ-003 |
| API-VND | `core/stores.md` | 21 | FR-007, FR-008 | SEC-REQ-011, DATA-REQ-008 |
| API-CAT | `core/catalog.md` | 22 | FR-004, FR-005, FR-006 | SEC-REQ-011, DATA-REQ-008 |
| API-SRC | `core/search.md` | 3 | FR-009 | NFR-004, NFR-007 |
| API-CRT | `customer/cart.md` | 7 | FR-010 | SEC-REQ-004, NFR-008 |
| API-ORD | `core/orders.md` | 14 | FR-011, FR-012 | SEC-REQ-004, SEC-REQ-009, NFR-008 |
| API-WAL | `core/wallet.md` | 14 | FR-013, FR-014 | SEC-REQ-009, DATA-REQ-007, INT-REQ-001, INT-REQ-002 |
| API-SHP | `delivery/delivery.md` | 16 | FR-015 | SEC-REQ-011, INT-REQ-005 |
| API-RET | `core/returns.md` | 17 | FR-016 | DATA-REQ-007, SEC-REQ-011 |
| API-NTF | `core/notifications.md` | 10 | FR-017 | SEC-REQ-009, INT-REQ-003, INT-REQ-004 |
| API-CNT | `core/content.md` | 20 | FR-019 | BR-PLT-06 (audited content changes) |
| API-ANL | `core/analytics.md` | 9 | FR-018 | NFR-001, NFR-004 |
| API-ADM | `admin/admin.md` | 43 | FR-002, FR-020 | SEC-REQ-004, SEC-REQ-010, NFR-019 |
| **Total** | | **221** | **20 FR** | |

Every FR is reachable through at least one endpoint group; every endpoint belongs to exactly one group; endpoint IDs (`API-<GROUP>-NNN`) are sequential within a group starting at `001` and are never reused.

---

## 5. How to Use This Domain

1. Read `api-conventions.md` before writing any endpoint — it defines headers, money, dates, idempotency and rate limits that apply everywhere.
2. Read `error-model.md` — every endpoint's "Errors" column lists error **codes**; the envelope and HTTP status mapping are defined only in `error-model.md`.
3. Read `pagination.md` before implementing any list endpoint — the pagination mode (cursor/offset) is fixed per endpoint family.
4. Open the group file under `endpoints/` for the endpoint table: method, path, roles, request/response essentials, errors, and related FR/BR/SEC IDs.
5. Cross-check state-sensitive behavior against `../03-system-analysis/core/state-transitions.md` (17 states, `409 STATE_CONFLICT`) and `01-business-analysis/business-rules.md` (111 rules).

---

## 6. Contract Guarantees

- **Deny-by-default authorization** on every endpoint: role + ownership checked server-side (`SEC-REQ-004`, FR-002).
- **Wallet-only payments**: no endpoint accepts card, COD, BNPL or crypto instruments (`C-01`–`C-04`); non-wallet methods return `PAYMENT_METHOD_NOT_ALLOWED`.
- **No location endpoints**: no request or response in this contract contains courier GPS coordinates (`C-16`, `BR-SHP-05`).
- **Idempotency** on all money, order, stock-reservation, coupon and refund operations (`BR-PLT-03`, `BR-PAY-08`).
- **Exactly 17 order states** with guarded transitions; invalid transitions return `409 STATE_CONFLICT` (`C-09`, `BR-ORD-01`).
- **Correlation IDs** on every request/response pair for observability (`NFR-014`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | Checklist item 5 count sync: 99 → **104 rules** (`BR-INV-01…05` registered) | `CRIT-06`/`HAL-04` pay-down (session 008) — consumer of `business-rules.md` v1.1 (root README §9.4) |
| 1.2 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-API-020…DOC-API-024) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
| 1.3 | 2026-09-30 | Checklist item 5 count sync: 104 → **111 rules** (`business-rules.md` v1.2) | Owner directive session 011 (`prompt-011.md` §4.7) — consumer of `business-rules.md`; count re-synced in same change set |
