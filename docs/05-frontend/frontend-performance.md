---
document_id: DOC-FE-009
title: Frontend Performance — Budgets, Caching, Perceived Performance & RUM
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-002, NFR-007, NFR-011, NFR-015, NFR-018]
related_documents: [DOC-FE-001, DOC-FE-002, DOC-FE-007, DOC-OVR-008]
---

# Frontend Performance

Meets **NFR-001** (server latency budgets the UI must not hide behind), **NFR-002** (LCP < 2.5 s on 4G, customer web JS < 200 KB gzipped) and **NFR-015** (browser/device matrix). Performance is gated in CI, not aspirational.

---

## 1. Targets

| Metric | Target | Applies to | Source |
|---|---|---|---|
| LCP | < 2.5 s on 4G mobile (emulated) | S1 customer web | NFR-002 |
| JS bundle (customer web) | < 200 KB gzipped initial | S1 | NFR-002 |
| JS bundle (vendor/admin) | < 350 KB gzipped initial (dashboards, code-split per route) | S2, S3 | NFR-002 baseline + DOC-FE-002 §7 |
| INP | < 200 ms | all web | Core Web Vitals |
| CLS | < 0.1 | all web | Core Web Vitals |
| FCP | < 1.8 s on 4G | S1 | derived |
| Time to interactive (RN) | < 3 s cold start on mid-range Android (Android 10 baseline) | S4, S5 | NFR-015 |
| API interactions | never exceed server budget: p95 < 200 ms read / < 500 ms write perceived end-to-end | all | NFR-001 |
| Route navigations (client) | < 300 ms to interactive on catalog routes | S1 | NFR-012 support |

## 2. Bundle Budgets & Enforcement

| App | Initial JS budget (gzip) | Enforcement |
|---|---|---|
| web-customer | 200 KB | `size-limit` in CI — build fails on exceed |
| web-vendor / web-admin | 350 KB | same |
| shared `packages/ui` | 15 KB per consumer | CI report |
| RN apps | 45 MB install ceiling (Play/App Store comfort), JS bundle < 5 MB gzipped | Metro bundle report in CI |

Budget tactics:

- Route-level code splitting mandatory (DOC-FE-003 §7); dashboards charts, galleries and PDF/export widgets load on demand.
- No heavyweight charting/calendar/icon packs on S1; icon set tree-shaken (DOC-FE-007).
- `next/dynamic` for non-critical widgets; polyfills only for the `NFR-015` matrix (target ES2017+).
- Dependency budget: bundlephoton/`depcheck` in CI flags duplicate heavy libs across apps.

## 3. Rendering & Caching (web)

| Technique | Usage |
|---|---|
| ISR | catalog/category/CMS pages revalidate ~60 s + on-demand revalidation on price/publish events (DOC-FE-002 §4) |
| CDN | static assets + ISR pages served from CDN in front of the app (see `14-devops-infrastructure/`); hashed immutable filenames |
| Streaming/SSR | product detail streams shell first; below-fold slots suspend |
| Never cached | wallet, orders, checkout — request-time fresh (DOC-BE-007 non-cacheable list) |
| Client cache | TanStack Query with stale-times per DOC-FE-004 §2; avoids refetch storms on back/forward |
| Hydration | only public catalog queries hydrated server-side; keeps hydration JS small |
| Degradation | search/cache down → browse still works via ISR + category pages (`NFR-007`) |

## 4. Image & Media Pipeline

| Item | Decision |
|---|---|
| Storage | product images in **MinIO**; delivery via CDN presigned/public bucket |
| Web formats | AVIF/WebP with responsive variants: widths 320–1600, generated at upload; originals kept privately |
| Web delivery | `next/image` with `sizes`, `priority` on LCP image, `placeholder=blurhash` for gallery |
| RN delivery | `react-native-fast-image` with disk cache + same variant widths |
| Budgets | ≤5 MB per image at upload (`BR-CAT-08`, `SEC-REQ-011`); **≤150 KB** transferred per above-the-fold image on 4G |
| Hero/LCP | product gallery first image preloaded via `fetchpriority=high`; Arabic font preloaded (DOC-FE-007 §5) |
| Stripping | EXIF stripped server-side at upload (`BR-CAT-08`) — also reduces payload |
| Video | none in v1 (out of scope) |

## 5. Perceived Performance

| Technique | Where |
|---|---|
| Skeletons | per route segment `loading.tsx`; identical geometry to loaded content (CLS = 0) |
| Optimistic UX | wishlist/follow only (DOC-FE-004 §6) — never money/order |
| Instant navigation | App Router prefetching on visible links for ISR catalog routes |
| Countdowns | reservation/OTP timers animate smoothly without re-rendering the tree |
| Feedback | all mutations get loading → success/error within 100 ms of click (button states) |
| Offline/poor network | cached shell renders immediately; queries retry with backoff; banners explain staleness |
| RN | splash → hydrate cached session (DOC-FE-006 §7) → skeleton tabs; no blank screens |

## 6. React Native Performance

| Concern | Policy |
|---|---|
| Cold start | < 3 s on Android 10 baseline device; measured in CI on emulator benchmark |
| Lists | flat/section lists with virtualization; product grids paginate 20/page from API |
| Re-renders | memoized components; query cache shared across screens; no deep state trees |
| Images | disk-cached, width-capped, blurhash placeholders |
| Release | Hermes engine on; bundle minified + bytecode; ProGuard/R8 on Android |
| JS thread | heavy parsing (large cart JSON) off the critical path; no synchronous storage on launch |
| Battery/network | polling only when visible (DOC-FE-004 §2); background push-driven updates |

## 7. Degradation & Resilience (`NFR-007`)

| Failure | Client behavior |
|---|---|
| Search API down | search page shows cached/fallback browse + localized notice (FR-009) |
| API slow | skeletons retained; never block navigation; request timeouts at 10 s with retry |
| CDN stale | ISR staleness acceptable for catalog; money routes unaffected |
| Image CDN down | blurhash placeholders retained; layout stable |
| Queue/notification delayed | in-app inbox remains source; no spinner-dependent flows |

## 8. Monitoring — RUM & Lab

| Layer | Tooling | What is captured |
|---|---|---|
| Lab (CI) | Lighthouse CI per route per locale (ar/en), bundle `size-limit`, RN benchmark | budgets in §1–§2; regressions fail the pipeline |
| Field (RUM) | Web Vitals library → analytics endpoint (`07-api`) with sampling 5% | LCP/INP/CLS distributions by locale, device, route |
| RN | crash/analytics SDK (self-hosted endpoint) + startup timing events | cold start, screen render times, JS errors |
| Correlation | RUM events carry `correlationId` where available (`NFR-014`) | ties client slowness to server traces |
| Alerting | Grafana dashboards aggregate RUM + RED metrics (`INT-REQ-007`) | p75 LCP regression > 20% alerts the team |
| Budgets in dashboards | per-app bundle size trend | prevents slow budget erosion |

## 9. Verification

| Check | Gate |
|---|---|
| `size-limit` budgets | CI must pass (§2) |
| Lighthouse CI (ar + en, mobile emulation) | LCP/CLS/INP within §1 |
| Bundle analyzer review | per release: no unexpected vendor chunks |
| RN cold-start benchmark | CI on Android 10 emulator image |
| Visual regression | skeletons match loaded layouts (CLS guard) |
| Load alignment | k6 (13-testing) confirms API p95 budgets so the UI never masks server regressions (NFR-001, C-25) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
