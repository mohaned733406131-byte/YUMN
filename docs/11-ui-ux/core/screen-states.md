---
document_id: DOC-UX-005
title: Screen States — Loading, Empty, Error, Offline & Confirmation Patterns
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-007, NFR-012, FR-001, FR-010, FR-011, FR-012, FR-013, FR-015, FR-017]
related_documents: [DOC-UX-001, DOC-UX-002, DOC-UX-004, DOC-FE-009, DOC-BA-005, DOC-SA-010]
---

# Screen States — Loading, Empty, Error, Offline & Confirmation Patterns

The state registry every screen must implement (design-completeness gate, `DOC-UX-001` §7). Governing principle **P5: never a dead end** — every non-success state offers at least one recovery action (`NFR-012`: 0 unrecoverable dead ends).

## 1. State Taxonomy & Selection Guide

| State | Trigger | Presentation rule |
|---|---|---|
| Loading (initial) | no data yet, request in flight | skeleton matching final geometry — never a bare spinner on full pages (`CLS = 0`) |
| Loading (action) | button/submit in flight | inline: button spinner, width preserved, `aria-busy` |
| Empty | request succeeded with zero items | illustration + explanation + primary recovery action |
| Error (field) | validation or per-field failure | inline below the field, `role="alert"`, focus moved to first error |
| Error (block) | section failed (e.g., recommendations) | inline block error + retry; rest of page keeps working |
| Error (page) | page-level fetch failed | page error with retry + home/search fallback |
| Error (global) | auth/network/session | toast or full-screen condition per §5 |
| Offline | RN: no connectivity; web: navigator offline | persistent banner + queued safe actions + cached reads |
| Partial data | some sections loaded, others failed | render loaded sections; failed sections show block error (never block the page) |
| Validation | user input rejected | pre-submit inline where possible; locale-explained (`NFR-012`) |
| Success | action completed | toast (non-blocking) or dedicated confirmation screen (transactional) |

**Channel selection matrix:** input mistakes → inline · background success/failure → toast · transaction outcomes (order placed, payment failed) → confirmation screen or persistent banner · data loss risk → modal · page failure → page state.

## 2. Loading Strategy (skeletons)

| Screen | Skeleton shape | Min time before showing (INFERENCE) |
|---|---|---|
| Home / category | hero block + 2×2 card grid rows | 150 ms (avoid flash) |
| PDP | gallery 1:1 block, title lines, price line, CTA bar | 150 ms |
| Search results | 6 result rows with facet rail | 150 ms |
| Cart / checkout review | line rows + totals block | 100 ms |
| Order list / timeline | 4 order rows | 100 ms |
| Wallet | balance block + 8 transaction rows | 100 ms |
| Vendor/admin tables | 10 table rows + header | 100 ms |
| Dashboards/KPI | KPI tiles + chart placeholders | 100 ms |

Rules: skeletons mirror the loaded layout exactly; shimmer only when motion is allowed (`DOC-UX-006` §8); after **8 s** show a "taking longer than usual" banner with retry (P3 low-bandwidth empathy); per-request timeouts map to §4 page/block error, never to an infinite skeleton.

## 3. Empty States (with recovery actions)

| Screen | Copy pattern (ar / en) | Recovery actions |
|---|---|---|
| Empty cart | "سلتك فارغة / Your cart is empty" | بحث / Search · تصفح الأقسام / Browse categories · عروض / Deals |
| No orders | "لا توجد طلبات بعد / No orders yet" | ابدأ التسوق / Start shopping |
| No search results | "لا نتائج لـ «{query}» / No results for "{query}"" | مسح الفلاتر / Clear filters · اقتراحات كتابة / spelling suggestions · popular categories |
| No results under filter | "لا توجد منتجات مطابقة / No matching products" | إزالة الفلتر / Remove filter (per-facet remove) |
| Empty wallet transactions | "لا توجد حركات بعد / No transactions yet" | شحن الرصيد / Top up |
| Empty notifications | "لا إشعارات / You're all caught up" | تعديل التفضيلات / Notification preferences |
| Vendor: no products | "لم تنشر أي منتج / No products yet" | إضافة منتج / Add product (KYC-gated, `BR-VND-01`) |
| Vendor: no orders | "لا طلبات جديدة / No new orders" | مراجعة المخزون / Check inventory |
| Courier: empty queue | "لا توجد توصيلات متاحة / No deliveries available" | تحديث / Refresh · سجل / History |
| Admin queue empty | "القائمة فارغة / Queue clear" | — (genuine end state; show last-checked time) |
| Followed stores none | "لا تتابع أي متجر / Not following any stores" | استكشاف المتاجر / Explore stores |

Empty illustrations: single-color line art, ≤ 40 KB, `aria-hidden`, never gendered or culturally insensitive; both locales carry their own caption.

## 4. Error Patterns

| Level | Example | Pattern | Retry |
|---|---|---|---|
| Inline field | phone format, required address | below field + icon + fix instruction (`^7[0-9]{8}` hint) | n/a (user edits) |
| Block | recommendations, review list failed | inline alert inside section, page unaffected | retry button |
| Page | orders page fetch failed | centered error, code reference `ERR-…`, home + search links | retry + auto-retry once |
| Global | session expired (15-min access, `C-08`) | stay on route, re-auth prompt, return to action after login (`DOC-FE-003` §9) | re-auth |
| Toast | "copied", "saved", settings updated | auto-dismiss 5 s | n/a |
| Server rejection | `PAYMENT_METHOD_NOT_ALLOWED`, `STATE_CONFLICT` (409) | map error **code** → localized message from `errors.json` (`DOC-FE-005` §5); never show raw codes | contextual (e.g., reload state) |
| Rate limited (429) | OTP/top-up abuse (`SEC-REQ-009`) | countdown until allowed + support link | timed |

Rules: network timeout ≠ error until the timeout elapses (show loading first); all retry buttons use idempotent operations (safe by design, `BR-PLT-03`); errors never display stack traces, SQL, or English-only text in the `ar` locale.

## 5. Offline & Degraded (RN apps S4/S5; web degradation)

| Condition | Behavior |
|---|---|
| No connectivity detected | persistent top banner "أنت غير متصل / You're offline"; reads served from cache where safe (never wallet balance older than 5 s, `NFR-004` staleness rule) |
| Action attempted offline | block writes with explanation; drafts (return reason, review text) preserved locally |
| Connectivity restored | banner clears, stale views auto-refresh, queued analytics flush |
| Search backend down (`NFR-007`) | search box shows "البحث غير متاح مؤقتاً / Search temporarily unavailable" + browse-by-category CTA — cart/PDP/checkout unaffected (`AC-FR009-03`) |
| Redis down | catalog falls back to DB with stricter rate limits; UI shows no change; rate-limit hits show §4 429 pattern |
| Push permission denied | app keeps working; in-app notification center is the guaranteed channel (`FR-017`) |
| SMS provider down | OTP screen copy states "check SMS **or WhatsApp**" (`BR-NTF-03`, `DOC-FE-006` §2) |

## 6. Wallet-Specific States

| State | Trigger | UI treatment |
|---|---|---|
| Balance healthy | balance ≥ pending total | balance card + ledger preview; green accent |
| **Insufficient balance** | checkout confirm (`BR-CRT-06`) | blocking panel in wallet-payment step: shortfall amount, primary "شحن الرصيد / Top up wallet" → deep link `/{locale}/account/wallet/top-up` with return-to-checkout; cart state preserved; **no order row created** (`AC-FR011-03`) |
| Top-up initiated (provider) | m-Floos/OneCash hand-off | status "بانتظار التأكيد من المزوّد / Awaiting provider confirmation"; poll → credit on verified callback only (`BR-PAY-03`); after 15 min without confirmation show "still checking" + support link (never a manual "credit me" button — client claims are ignored) |
| **Top-up pending admin verification** | bank transfer (`BR-PAY-04`, `INT-REQ-002`) | state "قيد التحقق الإداري / Pending admin verification" with submitted reference, expected SLA, and edit/cancel affordance until verified |
| Top-up failed | provider rejected | error + reason + "try another method" (only the three `C-05` rails offered) |
| Payment debited | order confirmed | immediate transaction row (debit) + order reference + escrow note (P2) |
| Refund credited | return/cancel (`BR-PAY-07`) | credit row + source (order/return ID) + "to wallet only" explanation |
| **Wallet frozen** | admin freeze (`BR-PAY-09`) | full-width warning banner: cannot pay or top up, refunds still received, contact support with ticket CTA |
| Ledger view empty/partial | first use / partial fetch | §3 empty state; partial → §1 partial-data rule |

Balance display: always integer YER with locale digits and `ر.ي`/`YER` suffix (`DOC-UX-007` §4), tabular numerals, never abbreviated ("1.5M" is forbidden for money).

## 7. Delivery Code Entry States (courier S5 + customer panel)

Per `BR-SHP-03`, `C-16`, `SEC-REQ-005`:

| State | Condition | UI |
|---|---|---|
| Idle | before entry | 6-slot code input, numeric keypad, customer handover instructions |
| Entering | partial digits | slots fill; masked from shoulder-surfing with reveal toggle |
| Verifying | submit in flight | button spinner; inputs locked ≤ 3 s |
| Wrong code | validation failure | shake + error "الرمز غير صحيح / Incorrect code"; **attempts remaining: 2** then **1** shown explicitly |
| Success | verified | transition to proof screen (code + timestamp + courier identity, optional photo `BR-SHP-07`); order → `DELIVERED` |
| **Locked** | 3rd failure | lock notice: "تم إيقاف التأكيد لمدة ٢٤ ساعة / Confirmation locked for 24 h"; auto-created support ticket reference shown; retry after countdown; customer timeline updated (`AC-FR020-02`) |
| Already delivered | idempotent replay (`DOC-SA-010` §5) | success no-op with "already delivered" notice |
| Order reassigned/released | assignment changed | input disabled + explanation + back to queue |

Attempts counters are announced to screen readers on change (live region), not conveyed by color alone.

## 8. OTP Screen States

Per `BR-AUTH-03`, `SEC-REQ-001`, `SEC-REQ-005`:

| State | Condition | UI |
|---|---|---|
| Awaiting code | after request | 6-digit group input, auto-advance, auto-submit; delivery-channel hint "أرسلنا رمزًا إلى … عبر SMS أو WhatsApp" |
| Cooldown | < 60 s since send | resend disabled with countdown in locale digits |
| Ready to resend | ≥ 60 s | resend action enabled; counter shows "3 resends left in 10 minutes" |
| Correct | verified | brief success check → session → destination |
| Wrong | mismatch | inline error + attempts left **3 → 2 → 1** (explicit numbers) |
| Expired | > 5 min | "انتهت صلاحية الرمز / Code expired" + primary resend |
| Max attempts | 3 failures | verification blocked notice; security notification sent (`BR-NTF-02`); support entry; no silent retry loop |
| Too many resends | 3 resends / 10 min | cooldown notice with exact retry time |
| Session already verified | double submit | idempotent redirect to destination |

## 9. Success Confirmations

| Action | Confirmation style |
|---|---|
| Order placed | dedicated screen: order ID, sub-orders by vendor, escrow microcopy, "تتبع الطلب / Track order" primary (FL-02 step 10) |
| Top-up credited | toast + balance animation update + transaction row |
| Return submitted | screen with SLA (48 h decision, 72 h inspection) and state badge `RETURN_REQUESTED` |
| Review submitted | inline success + "one review per item" reminder (`BR-REV-02`) |
| Settings/preferences saved | toast "تم الحفظ / Saved" |
| Delivery confirmed (courier) | full-screen success + next job CTA |
| Admin action (approve/refund/freeze) | confirm modal → toast + audit reference visible in activity (`BR-PLT-06`) |

Success toasts use `role="status"`; confirmation screens are reachable again from history (never toast-only for money events).

## 10. Per-Screen State Coverage Matrix (primary screens)

| Screen | Loading | Empty | Block err | Page err | Offline | Success |
|---|---|---|---|---|---|---|
| Home / category | ✓ | ✓ (no products in category) | ✓ | ✓ | ✓ | — |
| Search | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| PDP | ✓ | ✓ (unavailable 404) | ✓ | ✓ | ✓ | add-to-cart toast |
| Cart | ✓ | ✓ | ✓ | ✓ | ✓ | guard errors (§4) |
| Checkout (7 steps) | ✓ | ✓ (empty cart) | ✓ | ✓ | write-blocked | confirmation screen |
| Wallet / top-up | ✓ | ✓ | ✓ | ✓ | write-blocked | §6 |
| Orders / tracking | ✓ | ✓ | ✓ | ✓ | ✓ | state badges (§6 of `DOC-UX-004`) |
| Return request | ✓ | ✓ | ✓ | ✓ | draft preserved | SLA screen |
| Vendor orders/inventory | ✓ | ✓ | ✓ | ✓ | write-blocked | toast |
| Admin queues (KYC/dispute/refund/tickets) | ✓ | ✓ (queue clear) | ✓ | ✓ | write-blocked | modal + audit ref |
| Courier queue / code entry | ✓ | ✓ | ✓ | ✓ | input blocked | §7 |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
