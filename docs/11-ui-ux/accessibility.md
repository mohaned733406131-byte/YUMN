---
document_id: DOC-UX-006
title: Accessibility — UX Patterns for WCAG 2.1 Level AA
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-011, NFR-012, NFR-013, FR-001, FR-011, FR-015, FR-017]
related_documents: [DOC-UX-001, DOC-UX-004, DOC-UX-005, DOC-FE-007, DOC-NFR-011, DOC-AC-001]
---

# Accessibility — UX Patterns for WCAG 2.1 Level AA

**Target level: WCAG 2.1 Level AA — confirmed against `NFR-011` (registry `DOC-REQ-001` §2) and `OBJ-03`.** This file specifies the *design-side* patterns; `12-non-functional/` holds the measurable targets (≥95% automated pass, 0 critical violations) and `13-testing/` executes the checklist in §11. Applies to all five surfaces in both `ar` (RTL) and `en` (LTR) — `AC-NFR-011-01` scans both locales.

## 1. Perceivable

### 1.1 Contrast (AA: ≥4.5:1 text, ≥3:1 large text & UI components)

| Token pair | Ratio | Status |
|---|---|---|
| `#101828` on `#FFFFFF` (headings/prices) | ≈17:1 | AA ✓ (AAA) |
| `#475467` on `#FFFFFF` (body) | 7.7:1 | AA ✓ |
| `#667085` on `#FFFFFF` (meta/placeholder) | 5.0:1 | AA ✓ |
| `#027A48` on `#FFFFFF` (links, primary button text on white) | 5.4:1 | AA ✓ |
| `#FFFFFF` on `#027A48` (primary button) | 5.4:1 | AA ✓ |
| `#B42318` on `#FEF3F2` (error text/tint) | 6.6:1 | AA ✓ |
| `#B54708` on `#FFFAEB` (warning) | ≈5.1:1 | AA ✓ |
| `#175CD3` on `#EFF8FF` (info badge) | ≈5.5:1 | AA ✓ |
| `#0F766E` on `#F0FDFA` (transit badge) | ≈5.2:1 | AA ✓ |
| `#6941C6` on `#F4F3FF` (processing badge) | ≈5.9:1 | AA ✓ |
| `#344054` on `#F2F4F7` (cancelled badge) | ≈9.3:1 | AA ✓ |
| `#667085` border on `#FFFFFF` (input edges) | 5.0:1 | ≥3:1 ✓ |
| `#175CD3` focus ring on `#FFFFFF` / `#027A48` | ≥3:1 both | ≥3:1 ✓ |

Forbidden: `#039855`-and-lighter as small text; `#98A2B3` for anything except disabled controls (WCAG exempts disabled state).

### 1.2 Images, icons & media

- Meaningful icons/images: Arabic (or English) accessible name; decorative: `aria-hidden="true"` (`DOC-UX-004` §7).
- Product images: alt = localized product name + variant; never bare "image".
- No text baked into images (banners must carry a real text layer; `FR-019` CMS banners include alt/aria fields).
- Loading skeletons are `aria-hidden`; the live region announces "جارٍ التحميل / Loading".

### 1.3 Structure & orientation

- One `h1` per page; heading levels never skip; section landmarks (`header/nav/main/aside/footer`).
- Breadcrumbs are an ordered list with `aria-current`.
- In RTL, reading/tab order follows logical DOM order = visual RTL order (`DOC-FE-007` §7); no `tabindex > 0` anywhere.

## 2. Operable

### 2.1 Touch targets

| Element | Minimum |
|---|---|
| Buttons, links, icon buttons (all surfaces) | **44 × 44 CSS px** (WCAG 2.1 SC 2.5.5 is 44px; we apply it to all, not just AA's 24px SC 2.5.8) |
| Inputs & select fields | 48 px height (web + RN) |
| OTP/code digit cells | ≥ 44 × 52 px each with 8 px gaps |
| Stepper chevrons, qty +/- | 44 × 44 hit area even if glyph is 20 px |
| Bottom-tab items (S4/S5) | ≥ 44 px wide, full tab height |
| Adjacent targets | ≥ 8 px separation; list rows separated by dividers with 12 px padding |

Hit areas must not shrink or shift under icon mirroring (`DOC-FE-007` §7).

### 2.2 Keyboard (web S1–S3)

- 100% of core-journey tasks completable with keyboard only (`NFR-011` metric).
- Visible focus ring (§1.1) on every interactive element; `:focus-visible` for pointer users, always-on for keyboard; focus never clipped by RTL overflow.
- Logical order: skip-to-content link → header → main → footer; modals trap focus and restore it to the trigger; ESC closes non-destructive dialogs only.
- Checkout 7-step host: each step reachable via Tab; "continue" is the default focus target after valid submit; back navigation preserves focus position.
- No keyboard traps anywhere (including embedded CMS content and the numeric code keypad on S5 — arrow/Enter operable).
- Destructive confirmations: initial focus lands on the *safe* action (cancel), never on delete/refund.

### 2.3 Timing, motion & seizures

- Countdowns (OTP 5 min, reservation 15 min, code attempts) never auto-submit or auto-advance a step without user action; expiring sessions prompt re-auth rather than wiping the route (`DOC-FE-003` §9).
- **Reduced motion:** `prefers-reduced-motion: reduce` (web) and OS reduce-motion (RN) disable shimmer, shake-on-error (replace with icon + text), and page/sheet transitions (instant); success check animation becomes a static icon.
- No autoplaying media; no flashing content above 3 Hz (WCAG 2.3.1) — banners are static images only.
- Carousels (home hero): no auto-advance, or pausable with visible pause control if introduced later (v1: no auto-advance — `INFERENCE`).

### 2.4 Navigation aids

- Persistent primary nav + breadcrumbs (catalog/CMS) + pagination (announced: "صفحة ٢ من ١٠ / Page 2 of 10").
- Search field has an explicit accessible name ("بحث في يمن / Search yumn") even when the visible affordance is icon-only.
- Deep links from notifications land on the same screen in the same locale (`DOC-UX-008` §4).

## 3. Understandable

### 3.1 Form error association

- Every input has a programmatic label (`<label>`/`aria-labelledby`) — placeholder is never the label.
- Errors: `aria-invalid="true"` + `aria-describedby` pointing to the error text; error text has `role="alert"` (or live-region announcement on dynamic validation); focus moves to the first invalid field on submit.
- Error copy names the field, the problem and the fix in the active locale (`DOC-UX-005` §4); format hints shown *before* failure (e.g., phone `7XXXXXXXX`).
- Required fields: visual marker on the logical start side + `aria-required="true"` (visual asterisk alone is insufficient).
- Client-side validation only as a courtesy; server errors are mapped back to the same fields by error code (`DOC-FE-005` §5).

### 3.2 Predictability & input assistance

- Same nav, order and labels across all pages of a surface; language switch in a consistent slot (`DOC-UX-003` §8).
- OTP/6-digit inputs: single logical field group (`role="group"` + one label); paste of 6 digits supported; auto-submit announced via live region.
- No unexpected context changes on focus (no auto-opening menus that jump focus).
- Blocks/captchas: not used in v1; if introduced they must have an accessible alternative (recorded as design constraint).

### 3.3 Status badges — never color alone (all 17 order states)

- Every badge renders **icon + localized text label + tint** (`DOC-UX-004` §6). The text label is the source of meaning; color reinforces.
- In tables/lists, state is repeated in a text column for screen readers; badge element itself is `aria-label`-free when its text content already reads the state.
- State *changes* in timelines are announced politely (`aria-live="polite"`) on the tracking screen — e.g., "الطلب الآن في الطريق / Order is now out for delivery".
- Attempt counters (delivery code 3→1, OTP 3→1) and SLA countdowns are announced as text, not shown as a colored bar only.

## 4. Robust & Arabic RTL specifics

| Concern | Rule |
|---|---|
| Language | `<html lang="ar" dir="rtl">` (default) / `lang="en" dir="ltr"`; mixed-content islands (phone `^7[0-9]{8}$`, 6-digit codes, IDs) wrapped `dir="ltr"` |
| Screen-reader language switch | assistive tech must switch pronunciation on locale change — `lang` attribute updates on switch, verified in TalkBack/VoiceOver passes |
| Announcements | Arabic TTS must read numbers/dates correctly (locale digits in strings, `DOC-UX-007` §3) |
| Landmarks/labels | Arabic accessible names on all icon-only controls (e.g., bell = "الإشعارات") |
| Live regions | toasts success → `role="status"`; errors/alerts → `role="alert"`; countdown thresholds → polite live region |
| Hit/focus in RTL | focus ring, scrollers and dropdowns start from the logical start edge (`DOC-FE-007` §7) |
| RN parity | S4/S5: every control carries `accessibilityRole`/`accessibilityLabel`; the 6-digit keypad exposes digits in logical order; TalkBack/VoiceOver complete FL-01…FL-03 |

## 5. Per-Surface Priorities

| Surface | Highest-risk patterns | Priority checks |
|---|---|---|
| S1 customer web | checkout forms, code entry, badges, focus in RTL | keyboard-only FL-02, axe scan both locales |
| S2 vendor panel | dense tables, bulk actions, status badges | table semantics (`scope`, captions), row action labels |
| S3 admin console | modals for money actions, audit views | dialog focus trap, confirm-focus-on-safe, aria-live queue updates |
| S4 customer app | bottom tabs, sheets, countdowns | TalkBack: FL-01/02/03 end-to-end |
| S5 courier app | numeric keypad, attempts feedback | VoiceOver/TalkBack on code entry incl. attempt announcements |

## 6. Microcopy & readability

- Minimum rendered font sizes: 12 px (meta), **16 px body on mobile** (`DOC-UX-004` §3); line-height ≥1.7 for Arabic body.
- Line length ≤ 75 characters for long-form (CMS/help) in `en`; Arabic paragraphs left ragged, never justified with letter-spacing hacks.
- Links distinguished by more than color alone in body text (underline) — color-only links fail 1.4.1.
- Avoid ALL-CAPS Arabic (meaningless) and avoid uppercase transforms on English inside RTL contexts.
- Numbers in assistive text read naturally: "١٥٬٠٠٠ ريال يمني" announced correctly in `ar` locale tests.

## 7. Explicitly Out of Scope / Known Limits

- WCAG 2.1 AAA is **not** targeted (`NFR-011` = AA) — cited AAA contrast above is incidental, not required.
- Pre-recorded captions (SC 1.2) — v1 ships no video/audio content; if added, captions become required (record in `20-validation/missing-information.md` before adoption).

## 8. Design-Side Accessibility Rules (for authors in this domain)

1. Every new component in `DOC-UX-004` carries a contrast row in §1.1 before approval.
2. Every new screen defines its focus order and error-association pattern in its design entry.
3. Color may never be the sole carrier of meaning (state, error, required, success).
4. Motion added to a component must declare its reduced-motion fallback.
5. Accessibility regressions are release blockers (`AC-S-10`, `AC-NFR-011-01/02`).

## 9. Relationship to Measurement

| This file (design intent) | Measured in | Verified by |
|---|---|---|
| Patterns, contrast tables, touch/keyboard rules | `12-non-functional/` NFR-011 elaboration (≥95% axe pass, 0 critical) | `AC-NFR-011-01` |
| Screen-reader & keyboard journeys (FL-01…FL-03) | manual passes, recordings | `AC-NFR-011-02` |
| §10 checklist below | `13-testing/` (test cases `TC-*`) | `AC-S-10` |

## 10. Testing Checklist (pointer to `13-testing/`)

Execute per release, per locale, per surface:

1. axe-core scan: 0 critical, 0 serious; ≥95% pass on every customer page (`ar` and `en`).
2. Keyboard-only run of registration → order → tracking → return (FL-01, FL-02, FL-03, FL-04).
3. TalkBack (Android) and VoiceOver (iOS/Safari) run of the same journeys; record evidence.
4. Focus-visibility inspection at 320/768/1280 px in both directions; no focus loss in modals/sheets.
5. Contrast spot-check of every token pair in §1.1 against live renders.
6. Touch-target measurement (44 × 44) on S4/S5 controls and all web icon buttons.
7. Reduced-motion pass: shimmer/shake/transitions disabled under OS setting.
8. Badge/state comprehension: all 17 states identifiable without color (label + icon present).
9. Form-error association: `aria-describedby`/`aria-invalid` present on every validated field.
10. Live-region behavior: toast, countdown threshold and state-change announcements audible.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
