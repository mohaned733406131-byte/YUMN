---
document_id: DOC-UX-003
title: Information Architecture — Sitemaps, Navigation & URL↔Screen Map
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-003, FR-004, FR-007, FR-009, FR-010, FR-011, FR-012, FR-013, FR-017, FR-018, FR-019, FR-020]
related_documents: [DOC-UX-001, DOC-UX-002, DOC-FE-003, DOC-FE-001, DOC-OVR-002, DOC-REQ-001]
---

# Information Architecture — Sitemaps, Navigation & URL↔Screen Map

The design-level site/app map for all five clients. Route paths here are the **IA-level contract**: `../05-frontend/core/routing.md` (`DOC-FE-003`) owns implementation mechanics (guards, code splitting, redirects); this file owns *what exists, where it sits in navigation, and which block it serves*. Any screen added anywhere must appear here first (rule 5, `DOC-UX-001` §6).

## 1. S1 — Customer Web Storefront

### 1.1 Primary navigation (header, persistent)

| Item | Destination | Notes | Block |
|---|---|---|---|
| Logo | `/ar` home | returns to default locale home | — |
| Categories | mega-menu (levels 1 → 5) | see §3; hover/focus-expand on desktop, drawer on mobile | B04 |
| Search | `/ar/search` | always-visible field, Arabic-aware (`FR-009`) | B04 |
| Deals | `/ar/deals` | featured/deal merchandising (`FR-019`) | B12 |
| Cart | `/ar/cart` | badge = distinct product count (≤ 50, `C-15`) | B05 |
| Account | `/ar/account/*` | logged-in only; avatar menu | B01 |
| Language switch | header utility slot | see §8 | B01 |

Guest-visible: home, categories, search, deals, product, store, CMS pages, login/register. Cart is browsable by guests; checkout requires login (`DOC-FE-003` §2).

### 1.2 Secondary navigation (account area — `/ar/account`)

| Section | Path segment | Contents | FR |
|---|---|---|---|
| Profile | `profile` | name, phone (change = OTP-gated), optional email (never login, `BR-AUTH-08`), locale preference | FR-003 |
| Addresses | `addresses` | list ≤ 10, add/edit/delete, default marker | FR-003 |
| Orders | `orders`, `orders/{id}` | list, detail, timeline, cancel, return, review entry points | FR-012 |
| Wallet | `wallet`, `wallet/top-up` | balance, transactions ledger view, top-up methods, pending top-ups | FR-013 |
| Returns | `returns` | requests, status, refund ETA | FR-016 |
| Reviews | `reviews` | my reviews, edit window (7 days) | FR-006 |
| Notifications | `notifications` | in-app inbox + preference toggles | FR-017 |
| Sessions | `sessions` | ≤ 5 devices, revoke (`C-08`, `BR-AUTH-06`) | FR-003 |
| Wishlist / Following | `wishlist`, `following` | saved products, followed stores (`BR-VND-05`) | FR-008 |
| Support | `support` → tickets | open ticket, history (human only) | FR-020 |

### 1.3 Footer (persistent)

Help center / FAQ (CMS, `FR-019`) · About · Terms of Service · Privacy Policy · Return policy explainer (`C-11`) · Escrow & wallet explainer · Contact/support · Language switch (secondary placement) · Store registration CTA (vendor funnel, `FR-007`).

### 1.4 Checkout sub-IA (modal-independent step host)

`cart revalidation → address → shipping → wallet payment → review → confirm → confirmation` — seven steps (`FR-011`), each a distinct URL segment (`DOC-FE-003` §2), with a persistent order-summary rail (desktop) / collapsible summary (mobile). Progress indicator uses Arabic ordinals (`DOC-FE-008` §5).

## 2. Category Browse Structure

- Tree depth ≤ 5 levels, slugs unique per level (`BR-CAT-03`).
- Breadcrumb: Home → L1 → … → L5 (mirrors under RTL).
- Category landing: filter rail (facets) + sort + product grid; facet counts must equal returned totals (`AC-FR009-04`).
- Leaves render product cards; parent nodes render subcategory chips first, then products (progressive disclosure, P4).
- Banners/featured/deal slots are admin-scheduled (`FR-019`, `AC-FR009-05`) and expire automatically.

## 3. S2 — Vendor Panel Sections

| # | Section | Path prefix | Contents | Roles (`BR-VND-06`) |
|---|---|---|---|---|
| 1 | Onboarding | `/ar/vendor/apply`, `kyc/*` | application, KYC status, resubmission | applicant |
| 2 | Dashboard | `/ar/vendor/dashboard` | orders needing action, sales snapshot, follower count | all staff |
| 3 | Products | `/ar/vendor/products/*` | list, create, edit, images, variants, pricing | Editor/Manager write, Viewer read |
| 4 | Inventory | `/ar/vendor/inventory` | stock levels, reservations view | Editor/Manager |
| 5 | Orders | `/ar/vendor/orders/*` | inbox, accept, fulfill, ready-for-pickup, timeline | Owner/Manager confirm, Editor fulfill |
| 6 | Returns | `/ar/vendor/returns/*` | inspection queue with 72 h countdown (`BR-RET-05`) | Owner/Manager |
| 7 | Reviews | `/ar/vendor/reviews` | respond (once per review, `BR-REV-04`) | Editor/Manager |
| 8 | Finance | `/ar/vendor/finance/*` | wallet/escrow/payable, payouts, statements, commission | **Owner only** (money scope) |
| 9 | Store settings | `/ar/vendor/store/*` | profile, zones (domestic only, `C-17`), hours, staff, return policy | Owner: staff/policy; Editor: profile |
| 10 | Coupons | `/ar/vendor/coupons` | store coupons (≤ 90 days, ≤ 90%, `BR-PRM-01`) | Owner/Manager |
| 11 | Analytics | `/ar/vendor/analytics` | sales/finance/ops reports + export (`FR-018`) | Owner/Manager |

## 4. S3 — Admin Console Sections

| # | Section | Path prefix | Contents | Roles |
|---|---|---|---|---|
| 1 | Ops dashboard | `/ar/admin/dashboard` | KPIs: orders/min, top-up volume, queue depths, SLA clocks | Admin, Super Admin |
| 2 | KYC queue | `/ar/admin/kyc/*` | review/decide with 48 h SLA badges (`BR-VND-03`) | Admin+ |
| 3 | Users & vendors | `/ar/admin/users`, `/admin/vendors` | search, suspend, view sessions | Admin+ |
| 4 | Catalog & moderation | `/ar/admin/moderation/*` | reviews, content, banners (`UC-032`, `UC-038`) | Moderator, Admin, Super Admin |
| 5 | Orders & disputes | `/ar/admin/orders`, `/admin/disputes/*` | timelines, dispute resolution, cancel override | Admin+ (Moderator read-only) |
| 6 | Returns & refunds | `/ar/admin/refunds` | approval queue, refund preview | Admin+ |
| 7 | Finance ops | `/ar/admin/finance/*` | bank top-up verification (`BR-PAY-04`), wallet freezes (`BR-PAY-09`), reconciliation (`BR-ESC-08`), payouts | Admin+ |
| 8 | Delivery ops | `/ar/admin/delivery` | assignments, code-lockout tickets, escalations (`BR-SHP-06`) | Admin+ |
| 9 | Support tickets | `/ar/admin/tickets` | human ticket queue, code-lockout escalations (`AC-FR020-02`) | Moderator+ |
| 10 | CMS & promotions | `/ar/admin/cms/*`, `/admin/coupons` | pages, banners, platform coupons (`FR-019`) | Admin+ |
| 11 | Reports | `/ar/admin/reports` | sales/finance/ops exports (`FR-018`) | Admin+ |
| 12 | Platform | `/ar/admin/settings`, `/roles`, `/audit` | settings, RBAC (`UC-037`), append-only audit log (`UC-036`) | settings/roles: Super Admin; audit: Admin+ read |

## 5. S4 — Customer Mobile App (RN 0.73)

Tab bar (5 tabs, RTL order mirrors): **الرئيسية Home · البحث Search · السلة Cart · المحفظة Wallet · حسابي Account**.
Stacks: OrderStack (list → detail → track → return → review), CheckoutStack (mirrors §1.4), AuthStack (login → register → OTP). Deep links `yumn://orders/{id}`, `yumn://wallet/top-up`, `yumn://verify-otp` resolve to guarded screens (`DOC-FE-003` §5).

## 6. S5 — Courier Mobile App (RN 0.73)

Tabs (4): **المتاحة Queue (available jobs) · نشطة Active · سجل History · ملفي Profile**.
Drill-ins: PickupDetail → Transit actions → CodeEntry (6-digit keypad, attempts remaining) → DeliveryProof (code + timestamp + optional photo, `BR-SHP-07`). No location tab, no map, no GPS affordance (`C-16`, `BR-SHP-05`).

## 7. URL ↔ Screen Map (IA level)

Canonical shape `/{locale}/…`; `ar` default, bare paths resolve to `/ar` (`DOC-FE-003` §1). IDs below are IA anchors — implementation details (render mode, guards) belong to `DOC-FE-003`.

| IA screen | URL pattern | Locale | Primary FR | Block |
|---|---|---|---|---|
| Home | `/{locale}` | ar/en | FR-009, FR-019 | B04 |
| Category | `/{locale}/c/{category-slug}` | ar/en | FR-004, FR-009 | B02/B04 |
| Product detail (PDP) | `/{locale}/p/{product-slug}` | ar/en | FR-004, FR-006 | B02 |
| Storefront | `/{locale}/store/{store-slug}` | ar/en | FR-008 | B03 |
| Search results | `/{locale}/search` | ar/en | FR-009 | B04 |
| Deals | `/{locale}/deals` | ar/en | FR-019 | B12 |
| CMS page / help | `/{locale}/page/{page-slug}`, `/{locale}/help/*` | ar/en | FR-019 | B12 |
| Auth (login/register/OTP/reset) | `/{locale}/login` … `/{locale}/verify-otp` | ar/en | FR-001 | B01 |
| Cart | `/{locale}/cart` | ar/en | FR-010 | B05 |
| Checkout steps | `/{locale}/checkout/{address|shipping|payment|review|confirm}` | ar/en | FR-011 | B05 |
| Order list / detail / track | `/{locale}/account/orders`, `…/orders/{id}`, `/{locale}/track/{id}` | ar/en | FR-012, FR-015 | B06 |
| Wallet / top-up | `/{locale}/account/wallet`, `…/wallet/top-up` | ar/en | FR-013 | B07 |
| Return request | `/{locale}/account/returns` (+ detail) | ar/en | FR-016 | B09 |
| Notifications inbox | `/{locale}/account/notifications` | ar/en | FR-017 | B10 |
| Vendor panel | `/{locale}/vendor/…` (§3) | ar/en | FR-007, FR-008, FR-018 | B03 |
| Admin console | `/{locale}/admin/…` (§4) | ar/en | FR-020 | B13 |

Slugs are Latin transliterations, locale-independent (same path under `/ar/` and `/en/`) — policy owned by `DOC-FE-003` §8, content rules by `DOC-UX-007`.

## 8. Language Switch Placement

| Position | Surface | Behavior |
|---|---|---|
| Header utility (next to account) | S1, S2, S3 | two-state toggle `العربية / English`; keeps current path, updates `lang`/`dir`, persists to profile when logged in (`DOC-FE-008` §2, §7) |
| Footer secondary link | S1 | same behavior (discoverability for first-time users) |
| Account → Profile setting | S1, S4 | canonical preference (profile wins over cookie/header) |
| In-app setting row | S4, S5 | reloads catalogs without restart |
| OTP/SMS-driven entry | all | templates already localized (`BR-NTF-04`); no switch needed pre-login beyond the header toggle |

Arabic is default for every new user (`AC-XCUT-03` step 1); switching is a single interaction anywhere in the app (`NFR-013`).

## 9. B0x Mapping (blocks ↔ IA areas)

| Block | IA areas |
|---|---|
| B01 Identity & Access | auth screens, account profile/sessions, language switch, role landings |
| B02 Product Catalog | PDP, category browse, vendor product CRUD, reviews area |
| B03 Store Management | storefront, vendor onboarding/KYC, store settings, following |
| B04 Search & Discovery | search, filters/sorts, home merchandising, deals |
| B05 Cart & Checkout | cart, 7-step checkout host, mini-cart |
| B06 Order Management | order list/detail/track, vendor orders, admin orders |
| B07 Payment & Wallet | wallet, top-up, transactions, vendor finance, admin finance ops |
| B08 Shipping & Delivery | delivery code panel, courier app tabs, admin delivery ops |
| B09 Returns & Refunds | return flows, vendor returns, admin refunds |
| B10 Notifications | notification inbox, preference center, push opt-in |
| B11 Analytics & Reporting | vendor analytics, admin dashboard/reports |
| B12 Content & CMS | CMS pages, banners, coupons, help center |
| B13 Platform Administration | admin console shell, tickets, settings, roles, audit |

## 10. Navigation Rules

1. **Depth ≤ 3 clicks/taps** from home to any primary task (browse, cart, orders, wallet).
2. Role-gated items are hidden for unauthorized roles but the server independently enforces access (`SEC-REQ-004` — frontend guards are UX only).
3. The cart and notification badges are the only persistent numeric badges; unread counts cap display at `99+`.
4. Breadcrumbs appear on all catalog and CMS pages; account sections use section tabs instead.
5. 404 page offers search + home + category links (recovery, P5) in the current locale.
6. Every nav label exists in both locales (`NFR-013` parity; no hardcoded strings, `BR-PLT-05`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
