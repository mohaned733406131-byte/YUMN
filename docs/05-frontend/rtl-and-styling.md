---
document_id: DOC-FE-007
title: RTL & Styling — CSS Strategy, Logical Properties, Numbers & Fonts
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-011, NFR-013, NFR-015, BR-PAY-10]
related_documents: [DOC-FE-001, DOC-FE-002, DOC-FE-008, DOC-OVR-008]
---

# RTL & Styling

yumn is **Arabic-first RTL with full English LTR parity** (`C-24`, `NFR-013`). This file fixes the CSS strategy, direction rules, icon policy, number/currency formatting, fonts and design tokens used by all five apps.

---

## 1. CSS Strategy — Decision

**Choice: Tailwind CSS v3 with logical properties for web; tokens-driven `StyleSheet` for React Native.**

| Option | Verdict | Why |
|---|---|---|
| Tailwind CSS + logical utilities | **Selected** | first-class `ms-*`/`me-*`/`ps-*`/`pe-*`/`start-*`/`end-*` utilities; atomic classes compile to logical CSS properties → one codebase for `rtl`/`ltr`; tree-shaken; fits bundle budget (`NFR-002`); simple token integration |
| CSS Modules / vanilla CSS with manual flipping | Rejected | manual `direction` overrides proliferate; hard to lint; drift between surfaces |
| CSS-in-JS (styled-components/emotion) | Rejected | runtime cost hurts LCP (`NFR-002`), complicates SSR/ISR caching, larger bundle |
| Sass mixins for mirror | Rejected | build-time only, no runtime locale switch, duplicated class systems |

**React Native:** no CSS. Direction-aware styles come from a `useDirection()` hook returning `isRTL`, plus token-based spacing (`marginStart` etc. via RN's logical props on 0.73).

## 2. Direction Baseline

| Rule | Detail |
|---|---|
| Root | `<html lang="ar" dir="rtl">` on `web-customer` default; `lang="en" dir="ltr"` under `/en` |
| Switching | locale switch re-renders with correct `dir`; no full reload needed; URL updates per DOC-FE-008 |
| CSS reset | `html { direction: var(--dir) }`; no `float:left/right` anywhere — use logical utilities only |
| Layout primitives | `flex` row order flips automatically under RTL; grid placement uses `start/end` |
| Prohibited classes | `ml-*`, `mr-*`, `pl-*`, `pr-*`, `left-*`, `right-*`, `text-left`, `text-right` — lint rule fails CI; use `ms/me/ps/pe/start/end/text-start/text-end` |
| Exceptions (deliberate no-flip) | numeric progress bars bound to time (not direction), embedded LTR blobs (phone numbers, code snippets) wrapped in `dir="ltr"` islands |
| RN | styles use `marginStart/End`, `paddingStart/End`, `textAlign: 'start'`; `I18nManager.isRTL` drives icons and row order |

## 3. Icons — Mirrored vs Directional

| Icon category | Examples | Policy |
|---|---|---|
| Directional | back/forward arrows, chevrons, slide indicators, progress "next" | **mirror** under RTL (auto via `transform: scaleX(-1)` in a `<Icon rtl>` wrapper or asset variant) |
| Non-directional | search, cart, heart, bell, home, star, wallet, close, plus | never mirror |
| Navigation | bottom tab bar order | mirrors with layout; **labels and order follow `dir`** |
| Semantic/text-adjacent | "reply" arrow, share, logout | mirror reply/logout; keep brand logos untouched |
| Clocks/time | timeline markers | mirror only the direction of travel glyphs, not clock faces |
| Verification | RTL icon regression suite in `13-testing/` — no arrow points "west" in RTL where it means "forward" |

Rule of thumb: mirror anything describing *movement or sequence*, never anything describing *identity*.

## 4. Currency & Number Formatting

| Topic | Decision | Source |
|---|---|---|
| Currency | Yemeni Rial, code `YER`, Arabic display symbol `ر.ي`, English `YER` | `C-04`, `BR-PAY-10` |
| Digit style — `ar` locale | **Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩)** for all user-facing money and counts, formatted via `Intl.NumberFormat('ar-YE')` | `BR-PAY-10` |
| Digit style — `en` locale | Latin digits | NFR-013 parity |
| Digit style — inputs | Arabic-Indic **and** Latin accepted in numeric inputs; normalized to Latin integers before validation/submission | DOC-FE-005 §2 |
| Grouping | locale default (Arabic thousands separator `٬` in `ar`) | `BR-PAY-10` |
| Storage/transport | integer YER only — never floats, never formatted strings on the wire | `BR-PAY-10`, `BR-FIN-05` |
| Rounding | never done client-side; server rounds half-up to whole YER per sub-order (`BR-FIN-05`) — client displays exactly what the server returns | BR-FIN-05 |
| Order breakdown | subtotal − discount + VAT 15% + shipping, each line localized; shipping shown as untaxed | `BR-FIN-01` |
| Mixed-content islands | phone numbers `^7[0-9]{8}$` and delivery codes render `dir="ltr"` inside RTL text | DOC-FE-003 §8 |

## 5. Fonts

| Item | Decision |
|---|---|
| Arabic primary | **Cairo** (UI, headings, buttons) — strong hinting, wide glyph coverage, web-friendly |
| Arabic long-form | **Noto Naskh Arabic** for legal/CMS body text (readability at paragraph length) |
| Latin/UI fallback | Inter → system stack (`-apple-system, Segoe UI, Roboto, sans-serif`) |
| Numerals | feature `tnum` (tabular figures) for prices in tables and wallets so amounts don't jitter |
| Loading | self-hosted WOFF2 subsets from MinIO/CDN with `font-display: swap`; Arabic subset priority for `ar` locale (LCP care — `NFR-002`) |
| RN | bundled via `react-native-config`/asset registry — no runtime font fetch flicker |
| Line-height | Arabic needs looser leading: base line-height 1.7 for Arabic body vs 1.5 for Latin (per-locale token) |

## 6. Design Tokens

Single source: `packages/design-tokens` → consumed as CSS custom properties (web) and JS constants (RN).

| Token group | Examples | Notes |
|---|---|---|
| Color | brand green scale, semantic `success/warning/danger/info`, surface/text/inverse | WCAG AA contrast pairs verified (`NFR-011`); light theme only in v1 |
| Spacing | 4-pt scale (`--space-1…--space-16`) | logical, direction-neutral |
| Radius/elevation | card, sheet, pill | consistent across web/RN |
| Type scale | `--text-xs…--text-3xl` + per-locale line-height | locale-aware (§5) |
| Motion | durations, easing; `prefers-reduced-motion` honored | accessibility |
| Direction tokens | `--icon-flip`, `--divider-inline` | consumed by icon/layout wrappers |
| Breakpoints | sm 640 / md 768 / lg 1024 / xl 1280 | mobile-first — market is mobile-dominant |

Tokens are the only place raw hex/px values may appear; CI lint rejects literals in components.

## 7. Accessibility & Layout Checks (RTL-specific)

| Check | Requirement |
|---|---|
| Focus rings | visible in both directions; never clipped by flipped overflow |
| Scroll/overflow | horizontal scrollers start at correct edge under RTL (no forced scroll-to-end) |
| Tables | numeric columns stay `text-end`-aligned per locale; row action column mirrors |
| Forms | labels/asterisks/errors follow `dir`; required marker on logical start side |
| Touch targets | ≥44 px, mirrored hit areas unaffected by icon flip |
| Keyboard | tab order follows logical DOM order, which equals visual order under RTL (`NFR-011`) |
| Contrast | ≥4.5:1 text, ≥3:1 UI components (`NFR-011` WCAG 2.1 AA) |

## 8. Verification

- ESLint rule `no-physical-properties` fails CI on `ml/mr/pl/pr/left/right/text-left/text-right`.
- Visual regression snapshots for a golden set of components in `ar` (RTL) and `en` (LTR).
- Lighthouse pass on ISR pages in both locales; font payload tracked in DOC-FE-009 budgets.
- Manual QA checklist: icon mirroring, digit style, tabular numerals, focus visibility per locale.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
