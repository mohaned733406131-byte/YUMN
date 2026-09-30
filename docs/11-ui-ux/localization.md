---
document_id: DOC-UX-007
title: Localization — Content & Translation Rules
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-013, NFR-012, FR-017, FR-019, FR-004, BR-PLT-05, BR-NTF-04, BR-PAY-10]
related_documents: [DOC-UX-001, DOC-UX-004, DOC-FE-008, DOC-FE-007, DOC-REQ-001, DOC-OVR-008]
---

# Localization — Content & Translation Rules

Content and translation **rules** for the two supported locales (`C-24`: `ar` default, `en` parity). The i18n *mechanism* (libraries, catalogs, routing, ICU plumbing) is owned by `../05-frontend/core/internationalization.md` (`DOC-FE-008`); this file owns what is translated, how text behaves, and the editorial standards. Both must agree — where they overlap, canon (`BR-PLT-05`, `BR-NTF-04`, `BR-PAY-10`, `NFR-013`) decides.

## 1. Locale Model

| Rule | Decision | Source |
|---|---|---|
| Default locale | `ar` for every new user, guest and device (unknown device locale → `ar`) | `C-24`, `AC-XCUT-03` |
| Second locale | `en` with **complete feature parity** — no feature exists in only one locale | `NFR-013` |
| Third locale | none in v1 (adding one is a scope change, not a config change) | `C-24` |
| Switch behavior | header/utility toggle; same path, `lang`/`dir` update, profile preference persisted, checkout/cart/OTP-timer state preserved | `DOC-FE-008` §2/§7 |
| Switch granularity | one interaction from anywhere; applies across surfaces | `NFR-013` |
| Notification language | recipient's locale at send time; templates exist in 2/2 locales | `BR-NTF-04` |
| Server-generated text | error/message keys localized client-side from the same catalogs | `DOC-FE-008` §3 |

## 2. What Is Translated vs Not

| Content class | Policy | Rationale / rule |
|---|---|---|
| UI chrome: nav, buttons, labels, empty/error copy | **Translated (both)** — 100% of keys | `BR-PLT-05`, `NFR-013` CI gate |
| Order state names (all 17), workflow/SLA messages | **Translated (both)** | shared vocabulary across 4 surfaces (`C-09`) |
| Notification templates (SMS, WhatsApp, in-app, push) | **Translated (both)** — template inventory diff in CI | `BR-NTF-04` |
| Validation & API error messages (by code) | **Translated (both)** | `NFR-012` inline validation in locale |
| CMS pages, banners, help/FAQ | **Translated (both)** — publishing requires both locales or an explicit, visible `en` fallback marker | `FR-019`, parity promise |
| Category names | admin-maintained per-locale fields | discovery quality (`FR-004`) |
| Product names/descriptions | vendor-authored; may carry `ar` + `en` fields — each locale renders its own field, falling back to **Arabic** | Arabic-first catalog |
| Store/vendor names, brands | kept as authored (usually Arabic); never machine-transliterated in UI | identity |
| Reviews, Q&A, seller replies | displayed as written, in a `dir`-aware container | authenticity |
| Legal/tax text (terms, privacy, VAT lines) | translated; authoritative version noted on the page | compliance (`NFR-019`) |
| Machine translation of any user- or platform-generated text | **Prohibited in v1** | quality/trust (`DOC-FE-008` §6) |
| Vendor-supplied bilingual content quality | **not platform-guaranteed** — `ar` name is mandatory (`BR-CAT-01`), `en` is optional and may be absent; UI must tolerate mixed-quality `en` fields without layout breakage | `INFERENCE` — content-quality caveat |

## 3. Numerals & Number Formatting

| Context | Policy |
|---|---|
| Displayed money, counts, dates in `ar` | **Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩)** via `Intl.NumberFormat('ar-YE')` — **canon-fixed** (`BR-PAY-10`, `NFR-013`, `AC-XCUT-03` step 3) |
| Displayed numbers in `en` | Latin digits |
| Grouping | locale default: Arabic thousands separator `٬` in `ar` (e.g. ١٥٬٠٠٠) |
| Storage & transport | integer YER only; never formatted strings on the wire (`BR-PAY-10`, `BR-FIN-05`) |
| User **input** (prices, quantities, top-up amounts) | both Arabic-Indic and Latin accepted, **normalized to Latin integers** before validation/submission (`DOC-FE-005` §2) — this is the price-clarity guarantee: users type what they know, the system validates one canonical form |
| Phone entry | Latin digits only in the `^7[0-9]{8}$` field mask, with an Arabic-labelled example; phone renders in an LTR island |
| Delivery code / OTP entry | Latin digits in input slots (matches SMS content), localized labels around them |
| Mixed content | never mix digit systems inside one formatted value; code/ID/phone islands always `dir="ltr"` |

**Decision note:** a Western-digit-only display policy was considered for price clarity and rejected — canon (`BR-PAY-10`, verified by `AC-XCUT-03`) mandates Arabic-Indic display in `ar`. Clarity is instead delivered by (a) input normalization to Latin for validation, (b) tabular numerals, (c) always showing the `ر.ي`/`YER` unit, and (d) never abbreviating money.

## 4. Currency Display

| Locale | Format | Example |
|---|---|---|
| `ar` | value + ` ر.ي` (symbol after the number in RTL flow) | ١٥٬٠٠٠ ر.ي |
| `en` | value + ` YER` | 15,000 YER |

- Single currency only (`C-04`) — no locale ever renders USD/SAR.
- VAT line labeled in both locales: `ضريبة القيمة المضافة (١٥٪)` / `VAT (15%)`; shipping line explicitly marked untaxed where a breakdown is shown (`BR-FIN-01`).
- Negative amounts (refunds/debits) use locale-appropriate minus placement and always carry a textual descriptor (never color/parentheses alone).

## 5. Dates, Times & Durations

| Topic | Rule |
|---|---|
| Calendar | **Gregorian only in v1** — Hijri display is out of scope (future consideration, recorded not implemented) |
| `ar` format | `Intl.DateTimeFormat('ar-YE')` with Arabic-Indic digits, e.g. ٢٦‏/٠٩‏/٢٠٢٦ |
| `en` format | `2026-09-26` (tables) or `Sep 26, 2026` (prose) |
| Time zone | display in `Asia/Aden` (UTC+3); servers store UTC (`DOC-FE-008` §4) |
| Relative time | localized `Intl.RelativeTimeFormat`: "قبل ٥ دقائق" / "5 minutes ago" |
| SLA/cutoff dates (payout 3–7 business days, return windows, 48 h KYC) | show **calendar dates**, not raw day counts, in both locales |
| Countdowns (15-min reservation, 5-min OTP, lock timers) | locale digits + `tabular-nums`; announced accessibly (`DOC-UX-006` §3.3) |
| Week start / business-day math | Monday start; business days exclude Fri–Sat weekend for payout SLAs (`INFERENCE` — confirm with finance ops) |

## 6. Pluralization

- Arabic uses **six plural categories**: `zero`, `one`, `two`, `few`, `many`, `other` — catalogs must supply every applicable form; ICU MessageFormat style (`{count}`) with typed params (`DOC-FE-008` §3/§5).
- Test set for every pluralized string: **0, 1, 2, 3, 11, 100** (e.g. "لا منتجات" / "منتج واحد" / "منتجان" / "٣ منتجات" / "١١ منتجًا" / "١٠٠ منتج").
- Count-of-items strings never concatenate number + noun manually — always the plural key.
- Gender: prefer constructions that pluralize by object, not person; where gender is unavoidable, provide both forms and select by profile data (known gap: gender field is `INSUFFICIENT EVIDENCE` in profiles — until resolved, use neutral plural constructions).
- Ordinals in flows: Arabic ordinal words ("الخطوة ٣ من ٧" / "Step 3 of 7").

## 7. Transliteration for Slugs & Identifiers

| Rule | Decision |
|---|---|
| URL slugs | Latin transliteration of Arabic names — never raw Arabic path segments (`DOC-FE-003` §8) |
| Example | قهوة → `qahwa`; lowercased, diacritics stripped, `[^a-z0-9]` → `-` |
| Uniqueness | category slugs per level (`BR-CAT-03`); product/store platform-wide with opaque suffix on collision |
| Locale behavior | slugs are locale-independent: same path under `/ar/` and `/en/`; translation happens in page content, not in the URL |
| Display names | never replaced by transliteration in UI — transliteration exists for URLs, sharing and search only |
| Search | Arabic-aware normalization (alef variants etc.) is a search concern (`FR-009`), not a display concern |

## 8. Tone Guide (editorial)

| Attribute | Arabic standard | English standard |
|---|---|---|
| Register | formal Modern Standard Arabic; polite plural address (أنتم); **no dialect** in platform chrome | plain, direct, sentence case |
| Register exceptions | vendor-authored content stays as written | vendor-authored content unchanged |
| Brevity | ≤ 12 words for buttons/toasts; one idea per sentence | ≤ 8 words for buttons |
| Errors | problem + next action, no blame, no exclamation marks | same |
| Money copy | exact amounts with currency; calm, precise | same |
| Security copy | firm, factual, always includes a path forward (support/resend) | same |
| Addressing | never "عزيزي المستخدم" filler; use the person's name if known | no "Dear user" |
| Prohibited | slang, marketing hyperbole in transactional contexts, gendered defaults, emoji in platform messages | same |

## 9. Fallback & Missing-String Policy

| Situation | Behavior |
|---|---|
| Key missing in `en` at build | **CI failure** — release blocked (`NFR-013`: 0 missing keys) |
| Key missing at runtime (should not occur) | render the `ar` string (source catalog) + log a telemetry event tagged `i18n.missing`; never render the raw key |
| Vendor `en` product field empty | fall back to the `ar` field with no "translated" badge; layout must not break |
| CMS page published without `en` | blocked at publish unless an explicit fallback marker is set, shown visibly to `en` readers |
| Notification template missing in a locale | send blocked for that locale — falls back to the recipient's other complete template only if `ar` exists (`BR-NTF-04` gate) |
| Hardcoded string found in scan | CI lint failure (`BR-PLT-05`, `AC-NFR-013-01`) |

## 10. Quality Gates (design side)

1. Bilingual review of every new microcopy string before `status: approved` in this domain (author + native-speaker reviewer — `INFERENCE` on reviewer staffing).
2. RTL visual regression at 320/768/1280 px for core journeys: 0 defects (`AC-NFR-013-02`, `AC-S-11`).
3. Plural test set (§6) executed for every pluralized key.
4. Locale-format unit tests for money/date/numeral rendering (`BR-PAY-10`).
5. Template inventory: count × 2 locales (`BR-NTF-04`).
6. Usability evidence gathered in `ar` first; `en` parity checked by the same script (`NFR-012` measurement basis).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
