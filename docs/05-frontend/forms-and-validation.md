---
document_id: DOC-FE-005
title: Forms & Validation — Shared Schemas, Validation UX & Error Mapping
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-004, FR-010, FR-011, FR-013, NFR-011, NFR-012, SEC-REQ-002, SEC-REQ-011]
related_documents: [DOC-FE-001, DOC-FE-004, DOC-FE-006, DOC-BA-005]
---

# Forms & Validation — Shared Schemas, Validation UX & Error Mapping

**Rule:** client validation is for *speed and clarity*; the server is the *source of truth*. Shared Zod schemas in `packages/validation` mirror server DTO rules so both sides reject identical payloads — but the client never assumes its validation is final (`BR-CRT-04`, `DOC-BE-009`).

---

## 1. Validation Architecture

```text
packages/validation (Zod schemas, shared by all 5 apps)
        │  imported by
        ├── form components (onChange/onSubmit UX)
        └── api-sdk (payload pre-flight assertions in dev builds)
                │
                ▼
        NestJS DTO validation (class-validator)  ← authoritative
                │
                ▼
        business validation in service/domain layer (limits, state, funds)
```

| Layer | Tool | Purpose | Failure mode |
|---|---|---|---|
| Client schema | Zod in `packages/validation` | instant field feedback, disable submit | UX only |
| Client business mirror | same package (limit calculators) | pre-blocking C-15 messages | UX only |
| Server schema | class-validator DTOs | reject malformed payloads (`DOC-BE-009`) | `400 VALIDATION_ERROR` |
| Server business | service/domain guards | enforce limits, funds, states | domain error codes (`DOC-BE-008`) |

## 2. Canonical Field Rules (mirrored from canon)

| Field | Rule | Source ID | Client schema |
|---|---|---|---|
| Phone | `^7[0-9]{8}$`, no spaces in payload; input mask applied for display only | `BR-AUTH-01`, FR-001 | `z.string().regex(/^7\d{8}$/)` |
| Password | ≥8 chars with upper + lower + digit; never logged | `BR-AUTH-02` | `z.string().min(8).superRefine(...)` + strength meter |
| OTP | exactly 6 digits | `BR-AUTH-03` | `z.string().length(6).regex(/^\d{6}$/)` |
| Product price | integer YER > 0; sale price < original price | `BR-CAT-04`, `BR-PAY-10` | `z.number().int().positive()` |
| Order total bounds | 500 – 5,000,000 YER | `C-14` | server-echoed; client shows guard message |
| Top-up amount | 1,000 – 5,000,000 YER | `BR-PAY-02` | `z.number().int().min(1000).max(5_000_000)` |
| Cart quantity | ≤10 units/product; ≤50 products; ≤5 vendors | `C-15` | mirrored calculators + server reject |
| Address | ≤10 per customer; governorate/district required | FR-003 | `z.array(...).max(10)` |
| Rating | integer 1–5; ≤5 images ≤5 MB each | `BR-REV-03` | `z.number().int().min(1).max(5)` |
| Images | jpg/png/webp only, ≤5 MB, ≤10/product | `BR-CAT-08`, `SEC-REQ-011` | MIME + size pre-check before upload |
| Variant dimensions | ≤5 dimensions, ≤50 combinations; SKU unique per store | `BR-CAT-02` | combinatorics counter in form |
| Coupon code | one per order, validity checked server-side | `BR-PRM-01/02` | format-only client check |
| Delivery code | exactly 6 digits, 3 attempts | `BR-SHP-02/03`, `C-16` | `z.string().length(6)` + attempt UI |

**Money in inputs:** entered as integer YER (no decimals accepted); thousands separators are display-only and stripped before validation (`BR-PAY-10`). Floating-point arithmetic on money is prohibited anywhere in the client.

## 3. Form Strategy by Flow

| Form | Steps / fields | UX pattern | Key rules mirrored |
|---|---|---|---|
| Register | phone → password → confirm | single-column RTL, live phone mask, password checklist | `BR-AUTH-01/02` |
| Login | phone → password | error counter aware of lockout; lock message after 5th failure | `BR-AUTH-04` |
| OTP verify | 6-digit boxes | auto-advance, paste support, cooldown timer, attempts left | `BR-AUTH-03` |
| Password reset | OTP → new password | invalidates-all-sessions notice on success | `BR-AUTH-07` |
| Address add/edit | governorate → district → line → phone | dependent selects; ≤10 addresses | FR-003 |
| Product create/edit | info → pricing → variants → images → stock | sectioned wizard; publish disabled until BR-CAT-01 complete | `BR-CAT-01/02/04` |
| Checkout | address → shipping → wallet → review → confirm | server totals only; disable confirm while revalidating | FR-011, `BR-CRT-06` |
| Top-up | method → amount → reference/callback | amount bounds inline; bank method explains admin verification | `BR-PAY-02/04` |
| Return request | order item → reason → photos (optional) | window check client-side (delivery + returnPeriodDays) | `BR-RET-01`, `C-11` |
| Review | stars → text → images | one per order item, editable once in 7 days | `BR-REV-01/02` |
| Delivery code entry | 6 digits → confirm | attempts countdown; on lock show support-ticket notice | `BR-SHP-03`, `C-16` |

## 4. Validation UX Conventions

| Moment | Behavior |
|---|---|
| On change | format/mask only (phone, currency); no error text while typing |
| On blur | run schema; inline error under field, `aria-invalid` + `aria-describedby` (`NFR-011`) |
| On submit | run full schema; focus first invalid field; block duplicate submits (button loading state) |
| Server error on field | map server field errors back onto the matching inputs (§5) |
| Server business error | toast/summary with localized message + corrective action |
| Async availability | availability checks (phone uniqueness, SKU, coupon) debounced 400 ms with `AbortController` |
| Language | every message from `packages/i18n` — Arabic default, English parity (`C-24`); no string literals |
| Screen readers | error summary region announced on failed submit (`role="alert"`) |
| Offline | queue-safe: forms keep input; submit shows offline banner and never silently drops data |

## 5. API Error Mapping (consumes `07-api/error-model.md`)

`packages/api-sdk` normalizes every non-2xx response into:

```ts
type AppError = {
  code: string;           // machine code from the shared error model
  messageKey: string;     // i18n key — client renders localized text
  fields?: Record<string, string>;  // server field → error code (400 only)
  correlationId?: string; // shown in "copy details" for support (NFR-014)
  retryable: boolean;
};
```

| HTTP | `code` examples (from `07-api/error-model.md`) | Client handling |
|---|---|---|
| 400 | `VALIDATION_ERROR` | bind `fields` to inputs (§4) |
| 401 | `TOKEN_EXPIRED` | silent refresh (DOC-FE-004 §5); `AUTH_INVALID` → login prompt |
| 403 | `FORBIDDEN` | redirect to role landing — never toast "access denied" on foreign resources (use 404 behavior) |
| 404 | `NOT_FOUND` | not-found page/inline empty state |
| 409 | `STATE_CONFLICT` | order screens: refetch + "status changed, refreshed" banner (`03-system-analysis/state-transitions.md`) |
| 409 | `DUPLICATE_RESOURCE` (phone/SKU taken) | field-level error |
| 422 | `INSUFFICIENT_FUNDS` | checkout: show shortfall, link to top-up (FR-013) |
| 422 | `STOCK_UNAVAILABLE` | cart: flag item, block until removed (`BR-CRT-05`) |
| 422 | `LIMIT_EXCEEDED` | cart/top-up: show which limit (C-15 / BR-PAY-02) |
| 422 | `OTP_MAX_ATTEMPTS` | OTP screen: lock timer + resend disabled (`BR-AUTH-03`) |
| 422 | `PAYMENT_METHOD_NOT_ALLOWED` | must never occur — programming error (`BR-PAY-01`) |
| 429 | `RATE_LIMITED` | countdown from `Retry-After`; stricter on OTP/top-up (`SEC-REQ-009`) |
| 5xx | `INTERNAL_ERROR` | generic localized "something went wrong" + correlation ID; never raw message (SEC-REQ-008) |

Field-error mapping table lives beside the error model; if a code is missing there, the client renders the generic fallback — clients never invent codes.

## 6. Arabic Error Message Style

| Rule | Example (ar-YE) | Example (en) |
|---|---|---|
| State the problem, not the code | "رقم الهاتف يجب أن يبدأ بالرقم 7 ويتكون من 9 أرقام" | "Phone must start with 7 and be 9 digits" |
| Money in Arabic-Indic digits when locale = ar | "الرصيد غير كافٍ — المطلوب ١٢٬٥٠٠ ر.ي" | "Insufficient balance — 12,500 YER required" |
| Actionable close | add what the user can do ("أعد المحاولة بعد X دقيقة") | "Try again in X minutes" |
| Server-provided | server messages are message **keys**, Arabic text ships in catalog | parity in `en` catalog |
| Never | raw exception text, English-only errors, concatenated fragments | — |

## 7. Verification

- Contract tests: shared Zod schema and server DTO reject the same fixture payloads (golden set in `13-testing/`).
- Static scan: no `z.`/inline validation duplicated outside `packages/validation` for canonical fields.
- Accessibility tests: every error state announced, focus moved (`NFR-011`).
- E2E: phone/password/OTP/top-up boundary cases at 499/500 and 5,000,000/5,000,001 YER (`C-14`, `BR-PAY-02`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
