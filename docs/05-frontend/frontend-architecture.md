---
document_id: DOC-FE-002
title: Frontend Architecture — Monorepo, Layering & Rendering Strategy
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-004, FR-009, FR-011, FR-018, NFR-002, NFR-009, NFR-013, NFR-015]
related_documents: [DOC-FE-001, DOC-FE-003, DOC-FE-009, DOC-OVR-008]
---

# Frontend Architecture — Monorepo, Layering & Rendering Strategy

**Applies to:** all five client applications listed in `DOC-FE-001` §1. Stack is fixed by canon: **Next.js 14 (App Router)** for the three web surfaces, **React Native 0.73** for the two mobile apps, **TypeScript 5** everywhere.

---

## 1. Monorepo Layout

```text
yumn/
├─ apps/
│  ├─ web-customer/        # S1 — Next.js 14 storefront (SSR/ISR + CSR)
│  ├─ web-vendor/          # S2 — Next.js 14 vendor panel (CSR dashboard)
│  ├─ web-admin/           # S3 — Next.js 14 admin console (CSR dashboard)
│  ├─ mobile-customer/     # S4 — React Native 0.73 customer app
│  └─ mobile-courier/      # S5 — React Native 0.73 courier app
├─ packages/
│  ├─ api-sdk/             # typed fetch client + endpoint typings (single source for all apps)
│  ├─ ui/                  # cross-surface primitives (Button, Input, Modal, Money, Skeleton)
│  ├─ validation/          # shared Zod schemas (see DOC-FE-005)
│  ├─ i18n/                # message catalogs ar-YE / en + formatters (see DOC-FE-008)
│  ├─ design-tokens/       # colors, spacing, type scale, RTL rules (see DOC-FE-007)
│  ├─ config-eslint/       # shared lint + import-boundary rules
│  └─ config-ts/           # shared tsconfig bases (web / native)
├─ package.json            # pnpm workspaces
└─ turbo.json              # task graph: build / lint / test / typecheck
├─ api/                    # NestJS monolith (owned by 06-backend — not part of this domain)
```

**Rules:**

- One package manager (pnpm workspaces) and one task runner (Turborepo) — no per-app dependency drift (`NFR-009`).
- `apps/*` may depend on `packages/*`; `packages/*` may never depend on `apps/*` (enforced by lint import-boundary rules).
- `apps/*` never import from another app. Cross-surface reuse goes through `packages/`.
- The NestJS API lives beside the apps in the same repository but is a separate build unit; `packages/api-sdk` is the only code that knows HTTP details.

## 2. Layering Inside an App

Every app follows the same four layers, top-down dependency only:

```text
routes / screens  →  features  →  components  →  api-sdk / packages
   (composition)      (logic)      (presentation)    (transport & shared)
```

| Layer | Owns | Never owns |
|---|---|---|
| **Routes / screens** (`app/` or `screens/`) | URL/page composition, data fetching orchestration, guard wrapping, metadata | Business rules, fetch plumbing, styling primitives |
| **Features** (`features/<domain>/`) | Domain UI logic: cart aggregation, checkout step machine, order timeline mapping, wallet formatting | Direct `fetch` calls (must go through `api-sdk`), global state mutation |
| **Components** (`components/`) | Presentational, props-driven, RTL-safe, accessible (`NFR-011`) | Knowledge of endpoints, roles, or tokens |
| **API SDK** (`packages/api-sdk`) | Typed endpoints, error normalization to the `07-api` error model, retry/refresh interception | UI decisions, business validation |

**Example — checkout in `web-customer`:**

```text
app/[locale]/checkout/page.tsx            route: guard + layout + step host
features/checkout/steps/address-step.tsx   feature: address pick/validate (FR-011)
features/checkout/use-checkout-machine.ts  feature: 7-step state machine (CSR)
components/checkout/summary-card.tsx       component: totals display (server numbers)
packages/api-sdk/orders.ts                 SDK: POST order with idempotency key (BR-PAY-08)
```

## 3. Shared-Code Strategy

| Concern | Shared via | Notes |
|---|---|---|
| HTTP, auth headers, refresh retry | `packages/api-sdk` | One interceptor implements silent refresh (DOC-FE-006 §4) |
| Validation schemas | `packages/validation` | Zod schemas mirrored from server DTOs (DOC-FE-005) |
| Strings, dates, numbers | `packages/i18n` | Single catalog import path; no strings in components (`BR-PLT-05`) |
| Visual primitives, tokens | `packages/ui` + `packages/design-tokens` | Web uses Tailwind classes from tokens; RN maps tokens to StyleSheet (`DOC-FE-007`) |
| Domain constants (order states, statuses) | `packages/api-sdk/types` | Enumerations generated from the API contract — must equal the 17 states (`C-09`, `03-system-analysis/state-transitions.md`) |
| Feature logic (cart math, formatting) | feature folder, promoted to `packages/` only when a second app needs it | Avoid premature sharing |

**Anti-patterns (rejected in review):** copy-pasted components between apps; importing `web-customer/features/*` from `web-vendor`; hand-rolled fetch in screens; locale strings inside components.

## 4. Rendering Strategy per Surface

| Surface | Strategy | Rationale / requirements |
|---|---|---|
| S1 catalog & category pages | **ISR** (revalidate ~60 s), static shell + streamed dynamic slots | SEO for product discovery (FR-004, FR-009); cacheable at CDN; supports NFR-002 bundle target |
| S1 product detail pages | **ISR** with on-demand revalidation on price/stock/publish events | Content changes rarely; price display always labelled "server-confirmed at checkout" (`BR-CRT-04`) |
| S1 search results | **CSR** over Elasticsearch-backed API (FR-009) | Personalized/faceted; not SEO-critical per query; degrades gracefully if search is down (NFR-007) |
| S1 cart / checkout / account / wallet | **CSR only** | Authenticated, money-sensitive, never cached (wallet balance, order status are non-cacheable — DOC-BE-007) |
| S1 static content pages (CMS) | **ISR** (FR-019) | Admin-published pages; revalidate on publish event |
| S2 vendor panel | **CSR** + SSR auth bootstrap | Dashboards are private; SSR only to attach session cookie & avoid auth flash |
| S3 admin console | **CSR** + SSR auth bootstrap | Same as S2; audit/dispute views always fresh |
| S4 / S5 mobile | **Native CSR** | No server rendering; initial data via cached queries + skeletons (DOC-FE-009) |

**Guardrails:**

- Never ISR/SSR any route that displays wallet balance, order state, or personalized data — those must be request-time fresh (`DOC-BE-007` non-cacheable list).
- `middleware.ts` in each Next.js app handles locale resolution, session-cookie forwarding, and route guard pre-checks only (never authorization decisions — `SEC-REQ-004`).
- ISR pages must render identically in `dir="rtl"` and `dir="ltr"` (visual regression tests in `13-testing/`).

## 5. Build & Type Safety

| Item | Decision |
|---|---|
| Language | TypeScript 5 strict mode across all apps/packages |
| API typings | Generated from the API contract in `07-api/`; CI fails on drift |
| Lint gates | ESLint + Prettier + import boundaries in CI (`NFR-009`) |
| Bundle budgets | Enforced by CI size-limit on `web-customer` (DOC-FE-009 §2) |
| Environment config | Only `NEXT_PUBLIC_*` / build-time env for public config; secrets never enter the bundle (`SEC-REQ-007`) |
| Target browsers | Last 2 versions Chrome/Safari/Firefox/Edge; Android 10+, iOS 15+ (`NFR-015`) |

## 6. Relationship to Backend

| Topic | Contract |
|---|---|
| Transport | HTTPS JSON REST under `/api/v1` (see `07-api/`) |
| Errors | Single error shape consumed by `packages/api-sdk` and mapped in DOC-FE-005 §5 |
| Auth | Cookie-based refresh + bearer access token (DOC-FE-006); server enforces RBAC (`DOC-BE-004`) |
| Jobs | Clients never trigger jobs directly — they call endpoints; BullMQ fan-out is server-side (DOC-BE-006) |

## 7. Verification

- Lint/import-boundary rules fail CI on cross-app imports.
- Bundle-size gate fails CI if `web-customer` exceeds its gzipped budget (DOC-FE-009).
- Typecheck of generated API types fails on contract drift.
- Visual RTL/LTR regression suite covers shared components (`13-testing/`, `NFR-013`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
