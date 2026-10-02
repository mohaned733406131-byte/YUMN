---
document_id: DOC-FE-008
title: Internationalization — ar-YE Default, en Parity & Content Policy
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-013, BR-NTF-04, FR-017, FR-019]
related_documents: [DOC-FE-001, DOC-FE-007, DOC-FE-003, DOC-OVR-008]
---

# Internationalization — `ar-YE` Default, `en` Parity

Exactly two locales exist: **Arabic (ar-YE) as default** and **English (en)** as full parity (`C-24`). No third locale, no machine translation in v1. This file defines library choices, routing, catalogs, date/number/plural rules and what is — and is not — translated.

---

## 1. Library Decisions

| App family | Library | Rationale |
|---|---|---|
| Next.js 14 (S1–S3) | **next-intl** | App Router native (server components, middleware locale routing, `Intl.*` APIs), small runtime, typed message keys |
| React Native (S4, S5) | **react-i18next** (with `i18next` + ICU plurals) | mature RN integration, offline catalogs, simple async locale switch |
| Shared | `packages/i18n` holds **identical JSON catalogs** + formatter helpers for both libraries; single source prevents drift |

Alternatives rejected: `next-i18next` (pages-router oriented), hand-rolled context (reinvents plurals/interpolation), per-app copies (drift).

## 2. Locale Routing & Resolution

| Rule | Decision |
|---|---|
| URL shape | `/{locale}/…` — `/ar/...` explicit canonical, `/en/...` for English; bare `/` → 307 → `/ar/...` (default) |
| Default | `ar` for everyone unless `Accept-Language` explicitly prefers `en` on first visit |
| Persistence | `NEXT_LOCALE` cookie + user profile preference (logged-in) — profile wins over cookie, cookie wins over header |
| Switching | locale toggle in header; keeps the current path (translated routes are locale-independent — DOC-FE-003 §8), updates `lang`/`dir`, resets scroll |
| SEO | `hreflang` alternates `ar`/`en`, canonical per locale; ISR pages render both variants |
| API | API is locale-neutral; clients send `Accept-Language` so **server-generated content** (notification templates BR-NTF-04, error messages) returns in the right language |
| RN | device locale honored on first launch (only `ar`/`en` accepted; anything else → `ar`), then user override |

## 3. Message Catalogs

```text
packages/i18n/
├─ ar/
│  ├─ common.json      navigation, buttons, generic labels
│  ├─ auth.json        FR-001 screens, OTP, lockout copy
│  ├─ cart.json        C-15 messages, reservation countdown
│  ├─ checkout.json    FR-011 steps, payment, VAT breakdown labels
│  ├─ orders.json      17 state labels + action labels (C-09)
│  ├─ wallet.json      top-up, balance, transactions
│  ├─ returns.json     FR-016, inspection/SLA copy
│  ├─ vendor.json      panel, KYC, catalog
│  ├─ admin.json       console, disputes, moderation
│  ├─ errors.json      API error codes → localized text (DOC-FE-005 §5)
│  └─ notifications.json  in-app inbox strings
└─ en/  (mirror structure, parity enforced in CI)
```

| Policy | Rule |
|---|---|
| Key naming | `feature.section.key` — e.g. `checkout.review.vatLabel` |
| Typing | message keys typed; missing-key build failure in CI (no silent fallback) |
| Parity gate | CI diff: every `ar` key exists in `en` and vice versa (NFR-013 parity) |
| Hardcoded strings | lint rule forbids user-visible literals in JSX/TS (`BR-PLT-05`) |
| Interpolation | ICU MessageFormat style (`{count}`, `{price}`) with typed params |
| Server errors | clients map error **codes** to catalog keys; server-provided message keys localized from the same catalogs |

## 4. Date, Time & Calendar

| Topic | Decision |
|---|---|
| Calendar | **Gregorian only** in v1 — Arabic calendar (Hijri) display is out of scope; `ar` uses Gregorian month/day names via `Intl.DateTimeFormat('ar-YE')` |
| Format | `ar-YE`: `٢٦‏/٠٩‏/٢٠٢٦` style with Arabic-Indic digits; `en`: ISO-like `2026-09-26` or `Sep 26, 2026` per surface |
| Time zone | `Asia/Aden` (UTC+3) fixed for all display and SLA countdowns; server timestamps are UTC, clients convert |
| Relative time | "قبل ٥ دقائق" / "5 minutes ago" via `Intl.RelativeTimeFormat` |
| Business days | payout/return SLAs (BR-ESC-05, BR-RET-04) show calendar dates, not raw day counts |
| Countdowns | reservation (15 min) and OTP (5 min) render in locale digits with `tabular-nums` |

## 5. Numbers, Currency, Plurals

| Topic | Decision |
|---|---|
| Numbers/money | follow DOC-FE-007 §4 (Arabic-Indic in `ar`, Latin in `en`, integer YER) |
| Plurals | ICU categories — Arabic has **six** plural forms (zero/one/two/few/many/other): catalogs must supply all applicable forms; `react-i18next` plural suffixes configured for ar |
| Counts of items | "منتج واحد", "منتجان", "٥ منتجات" style — plural rules tested for 0,1,2,3,11,100 |
| Gendered verbs | order/status messages avoid gendered constructions where Arabic requires them; where unavoidable, pluralize by object not person |
| Ordinals | checkout steps ("الخطوة ٣ من ٧") use Arabic ordinal words |

## 6. What Is Translated vs Kept As-Is

| Content | Policy | Reason |
|---|---|---|
| UI chrome, buttons, errors, notifications templates | **Translated** (both locales) | `BR-NTF-04`, `C-24` |
| Order state labels, rule-driven messages | **Translated** | shared vocabulary (`C-09`) |
| Vendor/store names, brand names | **Kept as authored** (usually Arabic) | identity; transliteration only for URL slugs (DOC-FE-003 §8) |
| Product names/descriptions | vendor-authored; a product may carry both ar & en fields — each locale renders its own field, falling back to Arabic | Arabic-first catalog |
| Category names | per-locale fields maintained by admin (`FR-004`) | discovery quality |
| CMS pages | per-locale fields (FR-019); publish requires both locales or explicitly marks `en` fallback | parity promise |
| Reviews, Q&A, user messages | displayed as written (Arabic dominant) inside `dir`-aware container | authenticity |
| Legal/tax labels | translated; authoritative text noted | compliance |
| Machine translation | **prohibited in v1** — no auto-translated user content, no MT of notifications | quality/trust; recorded for future consideration only |

## 7. Locale Switch Behavior Matrix

| State | On locale switch |
|---|---|
| Guest on ISR page | navigate to same path with new prefix; re-render; cookie set |
| Logged-in | update profile preference via API; UI switches instantly |
| Checkout in progress | drafts preserved (state is locale-independent); summary labels re-render |
| Cart | preserved — items keyed by product ID, not text |
| OTP countdown / timers | preserved (time-based, not string-based) |
| RN | in-app language setting reloads catalogs without restart |

## 8. Verification

| Test | Coverage |
|---|---|
| CI parity diff | missing key in either locale fails the build (NFR-013) |
| Lint | no user-visible string literals in code (`BR-PLT-05`) |
| Plural tests | 0/1/2/3/11/100 for Arabic plural categories |
| Visual RTL/LTR | golden component set per locale (DOC-FE-007 §7) |
| E2E | register→order flow completed in each locale; locale persists across reload |
| Notification tests | template renders in recipient locale (`BR-NTF-04`) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
