---
document_id: DOC-UX-004
title: Design System — Tokens, Components & Voice
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-002, NFR-011, NFR-013, FR-012, FR-017, FR-019]
related_documents: [DOC-UX-001, DOC-UX-006, DOC-UX-007, DOC-FE-007, DOC-FE-009, DOC-SA-010, DOC-OVR-010]
---

# Design System — Tokens, Components & Voice

Single source of truth for yumn's visual language (`DEP-11` points here for brand tokens). `../../05-frontend/core/rtl-and-styling.md` (`DOC-FE-007`) owns the *mechanics* (Tailwind logical properties, token plumbing, font loading); this file owns the *values and usage rules*. Light theme only in v1 (consistent with `DOC-FE-007` §6). Raw hex/px values appear only in this file.

## 1. Color Tokens — Brand (Yemeni green identity)

Green anchors the brand ("yumin/يُمن" — fortune), echoing Yemeni identity. Scale is used for fills, hovers and text-on-light pairing.

| Token | Hex | Use |
|---|---|---|
| `green-50` | `#ECFDF3` | tinted backgrounds, selected rows, success banner bg |
| `green-100` | `#D1FADF` | hover tint on light surfaces |
| `green-200` | `#A6F4C5` | divider accents on green surfaces |
| `green-300` | `#6CE9A6` | chart accents |
| `green-400` | `#32D583` | non-text indicators (progress bars) |
| `green-500` | `#12B76A` | icons/graphs on white (≥3:1, UI components) |
| `green-600` | `#039855` | brand fills, solid badges, hero accents — **not** for small text on white (3.7:1) |
| `green-700` | `#027A48` | **default primary button bg** (white text 5.4:1 ✓ AA), links, text on white (5.4:1) |
| `green-800` | `#05603A` | pressed states, strong headings on green-50 |
| `green-900` | `#054F31` | brand-heavy footers, high-emphasis display text |

**Rule:** text-sized brand text and text on brand fills always use `green-700` or darker; `green-600` and lighter are for fills, icons and non-text graphics only.

## 2. Color Tokens — Semantic (all AA-verified pairs)

| Role | Text on tint | Tint bg | Border | Text on white | Notes |
|---|---|---|---|---|---|
| Success / positive | `#027A48` (5.4:1) | `#ECFDF3` | `#A6F4C5` | `#027A48` | confirmed payments, completed states |
| Warning / pending | `#B54708` (5.4:1) | `#FFFAEB` | `#FEDF89` | `#B54708` | SLA countdowns, pending top-ups |
| Danger / error | `#B42318` (6.6:1) | `#FEF3F2` | `#FDA29B` | `#B42318` | destructive actions, blocked, disputed |
| Info / neutral-blue | `#175CD3` (6.0:1) | `#EFF8FF` | `#B2DDFF` | `#175CD3` | placed/confirmed, links-adjacent info |
| Violet / in-progress | `#6941C6` | `#F4F3FF` | `#D9D6FE` | `#6941C6` | processing states |
| Teal / transit | `#0F766E` (5.5:1) | `#F0FDFA` | `#99F6E4` | `#0F766E` | courier movement states |
| Text primary | — | — | — | `#101828` | headings, prices (≈17:1) |
| Text secondary | — | — | — | `#475467` (7.7:1) | body copy, labels |
| Text muted | — | — | — | `#667085` (5.0:1) | placeholders, meta — still AA |
| Text disabled | — | — | — | `#98A2B3` | disabled-only (exempt from AA per WCAG) |
| Surface | — | `#FFFFFF` page, `#F9FAFB` section, `#F2F4F7` subtle | `#D0D5DD` decorative | — | elevation via surface, not shadow alone |
| Control border | — | — | `#667085` (≥3:1 on white) | — | input/select borders must be ≥3:1 |
| Focus ring | — | — | — | `#175CD3` 2 px + 2 px offset | visible in both directions |

## 3. Typography

Per `DOC-FE-007` §5: **Cairo** (Arabic UI/headings), **Noto Naskh Arabic** (long-form legal/CMS), **Inter → system stack** (Latin fallback).

| Token | Size / line-height (en) | Size / line-height (ar) | Weight | Use |
|---|---|---|---|---|
| `text-xs` | 12/16 | 12/20 | 400–500 | meta, timestamps, badge labels (never below 12 px) |
| `text-sm` | 14/20 | 14/24 | 400–500 | secondary UI, table cells, helper text |
| `text-base` | 16/24 | 16/28 | 400–600 | body, forms, product titles (default body size) |
| `text-lg` | 18/28 | 18/32 | 600 | section titles |
| `text-xl` | 20/28 | 20/36 | 600 | card headers, prices in PDP |
| `text-2xl` | 24/32 | 24/40 | 700 | page titles, wallet balance |
| `text-3xl` | 30/38 | 30/48 | 700 | dashboard KPIs, confirmation hero |

Rules: Arabic line-height is looser (1.7) — per-locale tokens, never a single value; **minimum rendered size 12 px**, body minimum 16 px on mobile (`DOC-UX-006` §7); tabular numerals (`tnum`) for all money/counters; money always `text-base` or larger and never truncated; prices weight ≥ 600.

## 4. Spacing, Radii, Elevation

- **Spacing:** 4-pt scale `space-1…space-16` = 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64 … (logical, direction-neutral; `ms/me/ps/pe` only — `DOC-FE-007` §2). Section rhythm on mobile uses 16/24; card padding 16; form field gap 20.
- **Radii:** `radius-sm 4` (inputs, chips) · `radius-md 8` (buttons, cards) · `radius-lg 12` (modals, panels) · `radius-xl 16` (bottom sheets) · `radius-pill 999` (badges, pills). RN uses the same values.
- **Elevation:** `e1` `0 1px 2px rgba(16,24,40,0.06)` cards at rest · `e2` `0 4px 12px rgba(16,24,40,0.10)` menus/dropdowns · `e3` `0 -8px 24px rgba(16,24,40,0.12)` bottom sheets · modal scrim `rgba(16,24,40,0.55)`. Elevation never substitutes for a border on interactive elements (3:1 edge rule, `DOC-UX-006`).

## 5. Core Components & States

| Component | Variants | Required states |
|---|---|---|
| Button | primary (green-700), secondary (outline), tertiary (ghost), danger, link | default · hover (`green-800`) · pressed · **focus ring** · disabled (opacity 50 + `aria-disabled`) · loading (spinner + kept width, `aria-busy`) |
| Sizes | sm (36) / md (44) / lg (52 px height) | touch target ≥ 44×44 for md+ (`DOC-UX-006`) |
| Input | text, tel, numeric-code, password, textarea, select | pristine · focused · filled · **error (below field, icon + text)** · disabled · read-only; label above (never placeholder-as-label); required marker on logical start |
| Card | product, order, store, KPI, coupon | default · pressed/selected (2 px green-700 border) · skeleton (`DOC-UX-005`) |
| Badge / chip | order state (§6), filter chip, count pill | tinted bg + text + icon; count pills cap at `99+` |
| Toast | success, error, info, warning | top-center (web) / top (RN), 5 s success, errors persist until dismissed; `role="status"` for success, `role="alert"` for errors |
| Modal (web) | confirm, destructive confirm, info | focus trapped, ESC closes non-destructive only, focus returns to trigger |
| Bottom sheet (RN) | action sheet, filter sheet, summary sheet | swipe + explicit close; scrim; snap points fixed per usage |
| Table | data table (vendor/admin) | sticky header, `text-end` numeric columns, row hover, empty state row, max 50 rows/page + pagination |
| Skeleton | page, card, list-row, table | geometry identical to loaded content (CLS = 0), shimmer only if motion allowed |
| Pagination | web: page numbers + prev/next; RN: infinite scroll + "load more" | current page announced; never more than 50 items/page in tables |
| Stepper | 7-step checkout, KYC wizard | current/complete/upcoming; Arabic ordinals; not clickable backwards past confirm |
| Banner (inline) | info, warning, success, error | persistent until resolved; never used for one-off confirmations (that's toast) |
| Countdown | reservation 15 min, OTP 5 min, SLA clocks | locale digits, tabular numerals, announced at thresholds (accessible, `DOC-UX-006`) |

## 6. Order-State Badge Map (all 17 — `C-09`, `DOC-SA-010`)

**Rule:** badge = tint + **icon + localized text label** — color is never the only signal (`DOC-UX-006` §6). Labels live in `orders.json` catalogs (both locales).

| # | State | Tone (bg / text) | Icon | Label (ar / en) |
|---|---|---|---|---|
| 1 | `PLACED` | info `#EFF8FF` / `#175CD3` | receipt | تم الطلب / Placed |
| 2 | `CONFIRMED` | info `#EFF8FF` / `#175CD3` | check-circle | تم التأكيد / Confirmed |
| 3 | `PROCESSING` | violet `#F4F3FF` / `#6941C6` | package | قيد التجهيز / Processing |
| 4 | `READY_FOR_PICKUP` | violet `#F4F3FF` / `#6941C6` | box-check | جاهز للاستلام / Ready for pickup |
| 5 | `ASSIGNED` | teal `#F0FDFA` / `#0F766E` | person-pin | تم إسناد المندوب / Assigned |
| 6 | `PICKED_UP` | teal `#F0FDFA` / `#0F766E` | truck | استلم المندوب الطرد / Picked up |
| 7 | `IN_TRANSIT` | teal `#F0FDFA` / `#0F766E` | route | في الطريق / In transit |
| 8 | `OUT_FOR_DELIVERY` | teal `#F0FDFA` / `#0F766E` | navigation | في طريق التوصيل / Out for delivery |
| 9 | `DELIVERED` | green `#ECFDF3` / `#027A48` | flag | تم التسليم / Delivered |
| 10 | `COMPLETED` | green `#ECFDF3` / `#027A48` | badge-check | مكتمل / Completed |
| 11 | `CANCELLED` | gray `#F2F4F7` / `#344054` | x-circle | ملغي / Cancelled |
| 12 | `RETURN_REQUESTED` | warning `#FFFAEB` / `#B54708` | undo | طلب إرجاع / Return requested |
| 13 | `RETURN_APPROVED` | warning `#FFFAEB` / `#B54708` | thumbs-up | الإرجاع معتمد / Return approved |
| 14 | `RETURN_REJECTED` | gray `#F2F4F7` / `#344054` | ban | الإرجاع مرفوض / Return rejected |
| 15 | `RETURN_RECEIVED` | violet `#F4F3FF` / `#6941C6` | inbox | تم استلام الإرجاع / Return received |
| 16 | `REFUNDED` | info `#EFF8FF` / `#175CD3` | wallet | تم الاسترداد / Refunded |
| 17 | `DISPUTED` | danger `#FEF3F2` / `#B42318` | alert-triangle | نزاع / Disputed |

Master orders aggregate sub-order badges: show the "most blocking" state (`DISPUTED` > return states > active > terminal) plus a per-vendor sub-order list (`BR-ORD-07`, `C-10`).

## 7. Iconography & RTL Rules

- Style: 24 px grid, 1.75 px stroke, rounded caps, outline default; filled only for active tab states.
- **Mirror** movement/sequence icons under RTL (back/forward arrows, chevrons, progress, reply); **never mirror** identity icons (search, cart, heart, bell, star, wallet, logos) — policy detail in `DOC-FE-007` §3.
- Decorative icons are `aria-hidden`; meaningful icons carry an Arabic or English accessible name (`DOC-UX-006`).
- Directional empty-state illustrations point *into* the content under RTL.

## 8. Voice & Tone

| Attribute | Rule | Example (ar / en) |
|---|---|---|
| Register | formal Modern Standard Arabic; respectful plural address (أنتم); no dialect in UI chrome (`DOC-UX-007` §8) | مرحباً بك / Welcome |
| Clarity | short sentences, concrete verbs, no jargon | تأكيد الطلب / Confirm order |
| Money tone | precise and calm; always show the number, never euphemize | تم خصم ١٥٬٠٠٠ ر.ي من محفظتك / 15,000 YER debited from your wallet |
| Errors | say what happened + what to do next; never blame the user | تعذّر إتمام العملية. حاول مرة أخرى / We couldn't complete this. Try again |
| Trust | explain escrow/holds at the moment of concern | محفظتك محمية حتى تستلم طلبك / Your money is held safely until you receive your order |
| Security | firm on lockouts/OTP, always offer a path | بعد ٣ محاولات، تم إيقاف التحقق لمدة ٢٤ ساعة / Verification locked for 24 h after 3 attempts — contact support |
| Prohibited | exclamation-heavy copy, slang, gendered constructions where Arabic requires pluralization by object (`DOC-FE-008` §5) | — |

## 9. Motion & Feedback Timing

| Interaction | Duration | Easing |
|---|---|---|
| Hover/press color shift | 120 ms | ease-out |
| Skeleton shimmer cycle | 1.4 s | linear |
| Modal/sheet enter | 200 ms | `cubic-bezier(0.2, 0, 0, 1)` |
| Toast enter/exit | 180 ms | ease-out |
| Success confirmation (check draw) | ≤ 600 ms | ease-out |

All motion respects `prefers-reduced-motion` (web) and OS reduce-motion (RN): shimmer becomes static tint, transitions become instant — a hard accessibility requirement (`DOC-UX-006` §8, `NFR-011`).

## 10. Token Governance

1. Tokens are defined here, packaged in `packages/design-tokens`, consumed as CSS custom properties (web) and JS constants (RN) (`DOC-FE-007` §6).
2. Components may not introduce raw hex/px values — CI lint fails on literals in components.
3. Changes to this file bump `version`, add a Change History row, and are re-verified against `DOC-UX-006` contrast tables before `status: approved`.
4. New semantic colors require an AA contrast entry in both `ar` and `en` rendering contexts before use.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
