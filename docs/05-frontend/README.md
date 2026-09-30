---
document_id: DOC-FE-001
title: Frontend Domain Overview & File Index
category: 05-frontend
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-003, FR-010, FR-011, FR-012, NFR-002, NFR-011, NFR-013, NFR-015, SEC-REQ-004]
related_documents: [DOC-ROOT-001, DOC-REQ-001, DOC-OVR-008, DOC-OVR-007]
---

# Frontend Domain — Overview & Index

The frontend domain defines how the yumn client applications are structured, routed, styled, secured and measured. yumn ships **four surface families, five client applications**: three Next.js 14 web surfaces and two React Native 0.73 apps. Every client is Arabic-first RTL (`C-24`), bilingual (`NFR-013`), wallet-only aware (`C-01`), and treats server-side authorization as the only security boundary (`SEC-REQ-004`).

---

## 1. Surface Register — Who Uses What

| # | Surface | App / Stack | Primary Actors (ACT-*) | Purpose | Rendering |
|---|---|---|---|---|---|
| S1 | Customer web storefront | Next.js 14 (App Router) | ACT-01 Customer (+ guests) | Catalog, search, product pages, cart, checkout, account, orders, wallet | SSR/ISR for catalog & product SEO pages; CSR for cart/checkout/account |
| S2 | Vendor panel | Next.js 14 (App Router) | ACT-02 Vendor (Owner/Staff) | KYC, store config, catalog & inventory, order fulfillment, finance, analytics | CSR (dashboard) with SSR shell for auth bootstrap |
| S3 | Admin console | Next.js 14 (App Router) | ACT-04 Admin, ACT-05 Super Admin, ACT-06 Moderator | Platform ops, KYC decisions, disputes, audit, moderation, settings, reports | CSR (dashboard) with SSR shell for auth bootstrap |
| S4 | Customer mobile app | React Native 0.73 | ACT-01 Customer | Browse, cart, checkout, wallet, order tracking, returns, reviews, notifications | Native CSR |
| S5 | Courier mobile app | React Native 0.73 | ACT-03 Delivery Provider | Assignment queue, pickup, transit scans, delivery code entry, earnings | Native CSR |

> Surfaces S4 and S5 form the single "mobile apps" surface counted in requirement texts (e.g. FR-001 "four surfaces"). They share one design system and one API SDK but are separate binaries with separate review pipelines.

**Actors with no interactive frontend:** ACT-07 System (`00-project-overview/actors-and-roles.md`) — background jobs and automated engines interact only through the API and BullMQ queues (see `../06-backend/core/background-processing.md`).

## 2. What Each Surface Covers (by requirement family)

| Concern | Customer web (S1) | Customer mobile (S4) | Vendor panel (S2) | Admin console (S3) | Courier app (S5) |
|---|---|---|---|---|---|
| Auth: phone + OTP, sessions (FR-001) | ✔ | ✔ (deep links) | ✔ | ✔ | ✔ |
| Role-gated routes (FR-002) | customer routes | customer routes | vendor routes | admin/moderator routes | courier routes |
| Catalog browse & search (FR-004, FR-009) | ✔ SSR/ISR | ✔ CSR | catalog authoring | oversight | ✖ |
| Cart & 15-min reservation (FR-010, C-13) | ✔ | ✔ | ✖ | ✖ | ✖ |
| 7-step checkout (FR-011, C-01) | ✔ | ✔ | ✖ | ✖ | ✖ |
| Order lifecycle view/actions (FR-012, C-09) | buyer view | buyer view | sub-order fulfillment | full override view | delivery states only |
| Wallet & top-ups (FR-013) | ✔ | ✔ | payouts view | freeze/verify (BR-PAY-04, BR-PAY-09) | earnings view |
| Escrow/payout visibility (FR-014) | ✖ | ✖ | ✔ | ✔ | ✖ |
| Returns (FR-016) | request | request | approve/inspect (BR-RET-05) | arbitrate (BR-RET-06) | return pickup |
| Reviews (FR-006) | write/own | write/own | respond (BR-REV-04) | hide + audit | ✖ |
| Notifications prefs (FR-017) | ✔ | ✔ push tokens | ✔ | ✔ | ✔ push tokens |
| Dashboards/reports (FR-018) | ✖ | ✖ | ✔ store scope | ✔ platform scope | ✖ |
| KYC submission / decision (FR-007) | ✖ | ✖ | submit | decide ≤48 h (BR-VND-03) | ✖ |
| Moderation, disputes, audit (FR-020) | ✖ | ✖ | respond | ✔ | ✖ |

## 3. Domain Principles (binding for every file here)

1. **RTL-first, not RTL-compatible** — `dir="rtl"` is the baseline; English flips to LTR (`C-24`, `DOC-FE-007`).
2. **Arabic default, English parity** — no hardcoded strings; message catalogs per locale (`BR-PLT-05`, `DOC-FE-008`).
3. **Frontend guards are UX only** — every route guard, hidden button and disabled state mirrors a server rule that independently enforces it (`SEC-REQ-004`, `DOC-BE-004`).
4. **Server is the source of truth** — prices, totals, VAT, stock, limits and order states are always recomputed by the backend (`BR-CRT-04`, `DOC-BE-005`).
5. **Money is integer YER** — clients format, never recompute rounding (`BR-PAY-10`, `BR-FIN-05`).
6. **Performance budget is a requirement** — customer web JS < 200 KB gzipped, LCP < 2.5 s on 4G (`NFR-002`, `DOC-FE-009`).
7. **No refresh token in web/local storage** — memory + httpOnly cookie strategy (`SEC-REQ-003`, `DOC-FE-006`).

## 4. File Index

| # | Filename | DOC ID | Purpose |
|---|---|---|---|
| 1 | `README.md` | DOC-FE-001 | This file — frontend domain overview, surface register, file index |
| 2 | `frontend-architecture.md` | DOC-FE-002 | Monorepo layout, folder structure, layering, shared packages, SSR/ISR vs CSR rendering strategy |
| 3 | `routing.md` | DOC-FE-003 | Route map per surface, role guards, code splitting, RTL-safe slug policy, 404/redirect rules |
| 4 | `state-management.md` | DOC-FE-004 | Server state (TanStack Query) vs UI state (Zustand), cart merge, silent token refresh, optimistic-update rules |
| 5 | `forms-and-validation.md` | DOC-FE-005 | Shared validation schemas mirroring server rules, validation UX, API error mapping, Arabic messages |
| 6 | `authentication-handling.md` | DOC-FE-006 | Client implementation of FR-001: OTP flows, token storage, refresh rotation, session cap UX, deep links |
| 7 | `rtl-and-styling.md` | DOC-FE-007 | CSS strategy, logical properties, icon mirroring, number/currency formatting, fonts, design tokens |
| 8 | `internationalization.md` | DOC-FE-008 | i18n libraries, locale routing, message catalogs, dates/plurals, dynamic-content translation policy |
| 9 | `frontend-performance.md` | DOC-FE-009 | Bundle budgets, code splitting, image pipeline, ISR/CDN caching, RN startup, Core Web Vitals, RUM |
| [`core/`](core/README.md) | DOC-FE-010 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-FE-011 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-FE-012 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-FE-013 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-FE-014 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## 5. Reading Order

| Audience | Read |
|---|---|
| New frontend engineer | DOC-FE-001 → DOC-FE-002 → DOC-FE-007 → DOC-FE-008 → DOC-FE-006 |
| Feature engineer (checkout) | DOC-FE-003 → DOC-FE-004 → DOC-FE-005 → `07-api/` endpoints |
| Security reviewer | DOC-FE-006 → `../09-security/core/authentication.md` → `../06-backend/core/authorization.md` |
| Perf/accessibility reviewer | DOC-FE-009 → DOC-FE-007 → `12-non-functional/` |

## 6. Upstream / Downstream Contracts

| Direction | Document | What it dictates here |
|---|---|---|
| Upstream | `02-requirements/requirements-overview.md` | FR/NFR/SEC IDs every client must satisfy |
| Upstream | `00-project-overview/project-constraints.md` | `C-01`, `C-06`, `C-08`, `C-15`, `C-16`, `C-24` visible behavior |
| Upstream | `../03-system-analysis/core/state-transitions.md` | The 17 states the UIs may render (no others) |
| Upstream | `11-ui-ux/` (planned) | Flows, design system, feedback states |
| Downstream | `07-api/` (planned) | Endpoint contracts, error model consumed by DOC-FE-005 |
| Downstream | `06-backend/` | Authoritative enforcement of every rule the UI mirrors |

## 7. Out of Scope for This Domain

- Server rendering internals, API design, database schema — see `06-backend/`, `07-api/`, `08-database/`.
- Native store-release mechanics (signing, rollout) — see `14-devops-infrastructure/`.
- Email surfaces — no email channel in v1 (`GAP-03`, `BR-NTF-01`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-FE-010…DOC-FE-014) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
