---
document_id: DOC-FE-003
title: Routing — Route Map, Guards, Code Splitting & Slug Policy
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-002, FR-004, FR-009, FR-010, FR-011, FR-012, FR-013, FR-020, NFR-011, NFR-013, SEC-REQ-004]
related_documents: [DOC-FE-001, DOC-FE-002, DOC-FE-006, DOC-OVR-007]
---

# Routing — Route Map, Guards, Code Splitting & Slug Policy

**Principle:** route guards are a *usability* layer. Every guard below has a server-side equivalent that independently denies the request (`SEC-REQ-004`, `DOC-BE-004`). URL structure is locale-prefixed, RTL-safe, and stable.

---

## 1. URL Conventions

| Rule | Decision |
|---|---|
| Locale prefix | `/{locale}/…` — `ar` is default and canonical (bare paths 307-redirect to `/ar/...`); `en` is parity (`C-24`, `DOC-FE-008`) |
| API base | `/api/v1/...` — never locale-prefixed, never mixed with page routes |
| Casing | lowercase kebab-case segments only |
| IDs in URLs | database public IDs (sortable, opaque), never sequential integers (enumeration hardening) |
| Trailing slash | canonical without trailing slash; middleware normalizes (avoids duplicate-content SEO issues on ISR pages) |
| Query strings | filters/search/page only; never state-bearing secrets |

## 2. Route Map — S1 Customer Web (`web-customer`)

| Segment | Routes | Access | Render | FRs |
|---|---|---|---|---|
| **Public catalog** | `/[locale]`, `/[locale]/c/{category-slug}`, `/[locale]/p/{product-slug}`, `/[locale]/store/{store-slug}`, `/[locale]/search`, `/[locale]/deals` | Public (guest OK) | ISR | FR-004, FR-008, FR-009, FR-019 |
| **Content (CMS)** | `/[locale]/page/{page-slug}`, `/[locale]/help/*` | Public | ISR | FR-019 |
| **Auth** | `/[locale]/login`, `/[locale]/register`, `/[locale]/verify-otp`, `/[locale]/reset-password` | Public; authenticated users redirect to `/account` | CSR | FR-001 |
| **Cart & checkout** | `/[locale]/cart`, `/[locale]/checkout/{address|shipping|payment|review|confirm}` | Customer (login gate at entry — cart browsable by guest) | CSR | FR-010, FR-011 |
| **Account** | `/[locale]/account/{profile|addresses|orders|orders/{id}|wallet|wallet/top-up|returns|reviews|notifications|sessions}` | Customer | CSR | FR-003, FR-012, FR-013, FR-016, FR-017 |
| **Wishlist / follows** | `/[locale]/account/wishlist`, `/[locale]/account/following` | Customer | CSR | FR-008 (BR-VND-05) |
| **Order tracking** | `/[locale]/track/{order-id}` | Owner only (or tokenized guest view of a placed order) | CSR | FR-012, FR-015 |

## 3. Route Map — S2 Vendor Panel (`web-vendor`)

| Segment | Routes | Access | FRs |
|---|---|---|---|
| Onboarding | `/[locale]/vendor/{apply|kyc/{status,submit}}` | Authenticated user without store → allowed; approved vendor redirected to dashboard | FR-007 |
| Dashboard | `/[locale]/vendor/dashboard` | Vendor (any staff role) | FR-018 |
| Catalog | `/[locale]/vendor/products`, `/[locale]/vendor/products/new`, `/[locale]/vendor/products/{id}` | Vendor — Editor/Manager write, Viewer read (BR-VND-06) | FR-004, FR-005 |
| Inventory | `/[locale]/vendor/inventory` | Editor/Manager | FR-005 |
| Orders | `/[locale]/vendor/orders`, `/[locale]/vendor/orders/{id}` | Owner/Manager confirm; Editor fulfill | FR-012 |
| Finance | `/[locale]/vendor/finance/{wallet|payouts|statements|commission}` | Owner only (money scope) | FR-014, FR-018 |
| Store settings | `/[locale]/vendor/store/{profile|zones|hours|staff|policy}` | Owner only for staff/policy; Editor for profile | FR-008, BR-VND-06 |
| Reviews | `/[locale]/vendor/reviews` | Editor/Manager (one response per review, BR-REV-04) | FR-006 |
| Returns | `/[locale]/vendor/returns`, `/[locale]/vendor/returns/{id}` | Owner/Manager; 72-hour inspection clock UI (BR-RET-05) | FR-016 |

## 4. Route Map — S3 Admin Console (`web-admin`)

| Segment | Routes | Access | FRs |
|---|---|---|---|
| Ops dashboard | `/[locale]/admin/dashboard` | Admin, Super Admin | FR-018, FR-020 |
| KYC queue | `/[locale]/admin/kyc`, `/[locale]/admin/kyc/{id}` | Admin+ ; 48-hour SLA badges (BR-VND-03) | FR-007 |
| Orders & disputes | `/[locale]/admin/orders`, `/[locale]/admin/disputes/{id}` | Admin+ (Moderator read-only) | FR-012, FR-020 |
| Finance ops | `/[locale]/admin/finance/{top-up-verifications|wallet-freezes|reconciliation|payouts}` | Admin+ (bank top-up verify = BR-PAY-04) | FR-013, FR-014 |
| Moderation | `/[locale]/admin/moderation/{reviews|content|banners}` | Moderator, Admin, Super Admin (BR-REV-04) | FR-006, FR-019 |
| Users & vendors | `/[locale]/admin/users`, `/[locale]/admin/vendors` | Admin+ | FR-003, FR-007 |
| Platform | `/[locale]/admin/{settings|roles|audit|tickets|reports}` | roles/settings = Super Admin only; audit = Admin+ read; tickets = Moderator+ | FR-020, SEC-REQ-010 |
| Refunds | `/[locale]/admin/refunds` | Admin+ | FR-016 |

## 5. Mobile Route Maps (React Native)

| App | Stack routes |
|---|---|
| S4 customer | `Splash → AuthStack{Login, Register, Otp} → MainTabs{Home, Search, Cart, Wallet, Account} → OrderStack{List, Detail, Track, Return, Review} → CheckoutStack` |
| S5 courier | `Splash → AuthStack → Tabs{Queue, Active, History, Profile} → PickupDetail → CodeEntry → DeliveryProof` |

Deep links: `yumn://orders/{id}`, `yumn://wallet/top-up`, `yumn://verify-otp?ctx=...` — every deep link resolves to a guarded route; unauthenticated targets bounce to the auth stack and return after login (DOC-FE-006 §7).

## 6. Guard Model

| Guard layer | Location | Decides | Never decides |
|---|---|---|---|
| Middleware pre-check | `middleware.ts` (web) | locale normalization; session cookie present? redirect to `/login?next=` | roles, ownership |
| Route-group layout | `app/[locale]/(vendor)/layout.tsx` etc. | render vs redirect to role-appropriate landing when role mismatched | data access |
| Component guard | `<RoleGate roles={[...]}>` | hide nav items / buttons (UX parity with server) | anything security-relevant |
| Screen guard (RN) | `RequireAuth` HOC | navigation gating | anything security-relevant |
| **Server** | every API endpoint | **actual authorization** (`DOC-BE-004`, `SEC-REQ-004`) | — |

Role → landing page mapping:

| Actor | Landing after auth | On role mismatch |
|---|---|---|
| ACT-01 Customer | `/account/orders` or `next` param | redirect `/` |
| ACT-02 Vendor | `/vendor/dashboard` | redirect `/` (or `/vendor/apply` if no store) |
| ACT-03 Courier | deep link into courier app | redirect login |
| ACT-04/05 Admin | `/admin/dashboard` | redirect `/` |
| ACT-06 Moderator | `/admin/moderation` | redirect `/` |

Forbidden = redirect (302 for guests to login; 307-locale-preserving), **404** only for nonexistent resources. Never leak existence of another user's resource: a customer visiting another customer's order URL gets **404**, not 403 (IDOR hygiene — mirrors `00-project-overview/actors-and-roles.md` authorization test 1 / TC-011).

## 7. Route-Level Code Splitting

- Next.js App Router: every route segment is a split boundary by default; `loading.tsx` skeletons per segment (DOC-FE-009 §5).
- Heavy interactive modules (image gallery, maps-free delivery timeline, chart widgets in vendor/admin dashboards) load via `next/dynamic` with explicit `loading` fallbacks.
- Above-the-fold product page JS stays within the customer-web bundle budget (`NFR-002`).
- Dashboard chart/report bundles are vendor/admin-only — never shipped to the storefront (budgets are per-app, DOC-FE-009 §2).

## 8. RTL-Safe Slug Policy (URL slugs)

| Rule | Decision |
|---|---|
| Slug language | **Latin transliteration** — Arabic display names are never raw URL segments; canonical slug is generated at entity creation |
| Generation | deterministic Arabic→Latin transliteration (e.g. `قهوة` → `qahwa`), lowercased, diacritics stripped, `[^a-z0-9]` → `-` |
| Uniqueness | category slugs unique per level (`BR-CAT-03`); product/store slugs unique platform-wide — collision resolved by appending a short opaque suffix (`-x7k2`) |
| Storage | slug persisted once at creation; renames create a redirect row (never silently change a live URL) |
| Locale behavior | slug is locale-independent (same URL under `/ar/` and `/en/`) — names are translated in the UI, not in the path |
| SEO | `<link rel="canonical">` + `hreflang` for `ar`/`en`; ISR pages expose `getStaticPaths` from published slugs only (`BR-CAT-06` — soft-deleted/INACTIVE products 404) |
| Rejected alternative | percent-encoded Arabic paths — fragile in share targets, SMS and QR contexts common in the Yemeni market |

## 9. 404 & Redirect Policy

| Case | Behavior |
|---|---|
| Unknown URL | 404 page in current locale, with search + home links (`NFR-011` accessible) |
| Soft-deleted/inactive product or store | 404 (never reveal deletion reason publicly) |
| Guest hitting guarded route | 307 to `/[locale]/login?next=<encoded>` ; after login return to `next` |
| Role mismatch | 307 to role landing (table §6) |
| Legacy/renamed slug | 308 permanent to canonical slug (SEO preserved) |
| Locale missing | resolve by `Accept-Language`, default `ar` |
| Session expired mid-route | stay on route, prompt re-auth, then continue — never hard-redirect to home (DOC-FE-006 §5) |
| Deprecated surface paths (v2) | 308 with changelog page; never client-side-only redirect (breaks crawlers) |

## 10. Verification

- Route inventory test: every route in §2–§5 has a matching guard test (`13-testing/`).
- TC-011…TC-014 cross-check: direct URL access to foreign resources returns 404/redirect as specified.
- RTL visual regression on all ISR route templates.
- Lighthouse/CI crawl confirms no authenticated page is ISR-cached.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
