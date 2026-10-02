---
document_id: DOC-UX-008
title: Feedback & Engagement — Notifications, Promotions, Reviews, Trust & Support
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-006, FR-017, FR-019, FR-020, FR-008, NFR-012, NFR-013]
related_documents: [DOC-UX-001, DOC-UX-002, DOC-UX-003, DOC-UX-005, DOC-FE-001, DOC-BA-005, DOC-REQ-001]
---

# Feedback & Engagement — Notifications, Promotions, Reviews, Trust & Support

Design intent for every surface where yumn talks back to users: preferences, inbox, promotions, review prompts, trust cues and support entry points. Channel mechanics and fan-out are owned by `FR-017`/`06-backend`; coupon engine mechanics by `FR-019`.

## 1. Channel Model (v1)

| Channel | Role | Design constraints |
|---|---|---|
| SMS | primary for OTP & urgent alerts (`BR-NTF-03`) | ≤ 160 chars Arabic-normalized; sender = "yumn/يمن"; no marketing to opted-out users |
| WhatsApp | OTP failover + rich order updates (`INT-REQ-004`) | approval-gated templates only; locale follows user (`BR-NTF-04`) |
| In-app | guaranteed channel; full history | always available regardless of OS permissions |
| Push | convenience for order/delivery events | opt-in required; permission not a precondition for any task |
| **Email** | **not a channel in v1** — UI must never show an email preference or "we'll email you" copy | `BR-NTF-01`, `GAP-03` (pending product-owner confirmation) |

## 2. Notification Preference Center (`/{locale}/account/notifications`)

### 2.1 Information architecture of the screen

Two-axis grid: **category rows × channel columns** (SMS · WhatsApp · In-app · Push), each cell a toggle. Sections:

| Section | Categories | Default state |
|---|---|---|
| **Security (locked)** | OTP, login alerts, password change, account lockout, wallet freeze | ON — **toggle disabled with lock icon + explanation** "إشعارات أمنية لا يمكن إيقافها / Security notifications can't be turned off" (`BR-NTF-02`) |
| Orders & delivery | order confirmed, out for delivery, delivered, return updates | ON |
| Wallet & money | top-up credited, refund credited, payout-related (vendor) | ON |
| Store & catalog | followed-store new products/offers (`BR-VND-05`), restocks | ON (follow-level control also exists on the store page) |
| Platform & promotions | deals, banners-by-push, campaigns | **OFF** (opt-in marketing, `BR-NTF-05`) |

### 2.2 Interaction rules

1. Per-channel opt-out is independent: disabling WhatsApp marketing does not touch SMS orders (`BR-NTF-05`).
2. Toggles save optimistically with rollback toast on failure; saved state visible within one interaction (`DOC-UX-005` §9).
3. When push is globally denied at OS level, the Push column shows a "blocked at system level" state with device-level instructions — other channels unaffected.
4. Channel availability reflects reality: if a user has never provided consent for WhatsApp, that column is dimmed with an explanation, not silently missing.
5. Copy never mentions email anywhere on this screen (`GAP-03` compliance).

## 3. Push Opt-In Prompts

| Moment | Trigger | Copy intent |
|---|---|---|
| Primary ask | immediately **after** the first successful action (registration complete or first order placed) — never on cold launch | "فعّل الإشعارات لتصلك تحديثات طلباتك / Turn on notifications for order updates" — benefit = transactional |
| Re-ask | if denied, re-surface only at the next order placement or delivery event | once per context, never nag loops |
| Pre-prompt | in-app explainer before the OS dialog (single card) | sets expectation: order + delivery updates |
| Denied permanently | state shown in preference center (§2.2-3) | in-app inbox remains the guaranteed path |

No engagement notifications are enabled by default beyond transactional (`INFERENCE` default posture aligned with `BR-NTF-05` opt-in marketing).

## 4. In-App Notification Center

Entry: bell icon in header (all web surfaces) with **unread badge** (`99+` cap), and the notifications section of account/mobile.

| Design element | Rule |
|---|---|
| List | reverse-chronological, grouped "اليوم / Today", "سابقًا / Earlier"; each row = icon + localized title + 2-line preview + relative time (`DOC-UX-007` §5) |
| Unread state | unread rows: green-50 tint + start-edge dot + bold title; read = plain; badge clears on visiting the screen (per-row read stays granular) |
| Segments | tabs: الكل / All · المالية / Money · الطلبات / Orders · المتجر / Store · الترويج / Promotions (promotions hidden if opted out) |
| **Deep link** | every row taps through to the owning screen: order events → order detail; top-up verified → wallet; return → return detail; KYC decision (vendor) → KYC status; coupon/deal → product/deal page; ticket reply → ticket. Payload contract (title/body/action URL/locale/entity IDs) is specified in `../../07-api/core/notifications.md` (planned — see report of missing paths) |
| Actions | swipe/long-press: mark read/unread, delete (local dismiss only — never deletes the server record for security notices) |
| Retention in UI | 90 days visible, older reachable via wallet/order history (`INFERENCE`; server retention per `DATA-REQ-003`) |
| Security notices | pinned section behavior: cannot be dismissed permanently; render with danger accent (`BR-NTF-02`) |
| Parity | every in-app string exists in `ar` and `en` (`NFR-013`); deep link preserves current locale |

## 5. Promotion Surfaces

| Surface | Where | Rules |
|---|---|---|
| Home hero banner | S1/S4 home | admin-scheduled window, bilingual fields, alt text required (`FR-019`, `DOC-UX-006` §1.2) |
| Category/deal slots | category pages, `/deals` | featured/deal placements respect expiry (`AC-FR009-05`) |
| Product badges | PDP + cards | "عرض / Sale" only when sale price < original (`BR-CAT-03` price rule); never fake scarcity (no countdown timers on stock — `INFERENCE` honesty rule) |
| Store follow prompt | storefront (once per session) | ties to follower notifications (`BR-VND-05`) |
| First-order welcome coupon | registration success / first checkout | platform coupon (`BR-PRM-03`), subject to all PRM constraints: ≤ 90-day validity, ≤ 90% discount (`BR-PRM-01`), one per user (`BR-PRM-04`) — `INFERENCE` on offering mechanics |
| Coupons in cart/checkout | review step (FL-08) | available list + entry field; **non-stackable disclosure always visible**: "يمكن استخدام قسيمة واحدة فقط / One coupon per order" (`BR-PRM-02`) before first apply |
| Coupon error states | checkout | expired/used/ineligible → inline reason; no order row created (`BR-PRM-06`) |
| Push/SMS promotions | only opted-in channels/categories | frequency cap: ≤ 3 promotional pushes/week (`INFERENCE` — tune post-launch) |

Promotional messages are visually and verbally distinct from transactional ones (badge "عرض / Offer") so users never mistake a campaign for an order event.

## 6. Review Solicitation

**Timing (canon):** solicitation is offered **after `DELIVERED`** — not after `COMPLETED` — because `BR-REV-01` opens the review window at delivery with a 30-day expiry; `COMPLETED` occurs 7 days later at escrow release (`C-12`). Soliciting later would shrink the window and conflict with the rule.

| Rule | Design expression |
|---|---|
| Eligibility | only purchasing customer, only after `DELIVERED`, within 30 days (`BR-REV-01`) — prompt hidden otherwise (`DOC-UX-002` FL-09 D1) |
| Frequency | one prompt at delivery + one reminder at +7 days (`INFERENCE` on the reminder); never re-prompt after submission |
| Granularity | per order item — one review per item (`BR-REV-02`) |
| Edit | single edit within 7 days, shown as "تعديل / Edit" on own reviews |
| Images | ≤5, ≤5 MB each (`BR-REV-03`) with upload progress + reject reasons |
| Incentive | **none in v1** (no points/loyalty — FUTURE SCOPE, `GAP-04`) — prompt copy stays neutral: "شارك رأيك / Share your opinion" |
| Vendor side | respond once per review (`BR-REV-04`); moderation hides with audit (`UC-038`) |

## 7. Trust Signals

| Signal | Placement | Copy intent (P2) |
|---|---|---|
| Escrow explanation | checkout payment step, order confirmation, wallet payment rows, PDP reassurance strip | "محفظتك محمية — نحتفظ بالمبلغ حتى تستلم طلبك / Your money is held safely until you receive your order" (7-day hold explained in one sentence + link to help page) |
| Wallet balance freshness | wallet screen | balance + "آخر تحديث / last updated" with instant refresh — money screens never look stale (`NFR-004` 5-s staleness rule) |
| Ledger transparency | wallet transactions | every change = row with type, amount, related order, timestamp (`BR-PAY-06` visibility) |
| Vendor ratings | store header, PDP store card | average + count ("٤٫٦ من ٥ · ١٢٠ تقييم / 4.6 of 5 · 120 reviews"), visible-reviews basis (`BR-REV-05`) |
| Store badges | storefront | KYC-approved indicator (vendor verified); suspended stores show no products (`BR-VND-04`) — never surface internal status text |
| Delivery code promise | tracking + courier handoff copy | "لا يُسلَّم الطرد إلا برمز التحقق / Package handed over only with the 6-digit code" (`C-16`) |
| Refund guarantee | return flows | "يُعاد المبلغ إلى محفظتك خلال ٣ أيام عمل / Refund to wallet within 3 business days" (`BR-RET-04`) |
| Receipts | order confirmation | full breakdown incl. VAT 15% (`BR-FIN-01`) — transparency doubles as invoice evidence |
| Contact path | every trust surface links to support | see §8 |

## 8. Support Entry Points (human only)

**Scope lock:** support is **human ticketing only — no AI chatbot, no generative-AI support features** (project scope decision, `FR-020`, `project-scope.md`).

| Entry | Location | Behavior |
|---|---|---|
| مساعدة / Help | header (all surfaces) → help center | CMS FAQ/self-service (`FR-019`) first |
| فتح تذكرة / Open ticket | help center, order detail, wallet, tracking, error states | form: subject, category, related entity (order/wallet/KYC auto-attached), free text + optional screenshots; confirmation with ticket ID |
| Contextual escalation | delivered inline by failing states: code lockout (auto-created ticket, `BR-SHP-03`), dispute (admin queue), payment pending | pre-filled context — user never retypes the situation |
| Vendor support | vendor panel help | separate queue view (vendor tickets) |
| Admin/support console | S3 tickets section | human agents reply; SLA per severity (`../../12-non-functional/core/usability-and-support.md`) |
| No-chat affordances | everywhere | no chat bubble, no "Ask AI", no canned-bot first layer — presence of a bot UI would violate scope |

Multilingual: tickets carry the submitter's locale; agents answer in `ar` by default (`INFERENCE` on staffing language coverage).

## 9. Feedback Collection (product)

| Mechanism | When | Notes |
|---|---|---|
| CSAT micro-survey | after support ticket resolution (1–5 + optional comment) | single question, both locales |
| Task-success prompt | after first order / first listing (once) | feeds `NFR-012` measurement |
| In-app "إبلاغ عن مشكلة / Report a problem" | account → support | captures screen context (no PII beyond what user types, `DATA-REQ-002`) |
| Review analytics | vendor/admin dashboards | review volume, rating trend (`FR-018`) |

Aggregated outcomes feed `21-completion/` (usability/quality gates) via the loop defined in `../../12-non-functional/core/usability-and-support.md` §8.

## 10. Cross-References

- Rules: `BR-NTF-01…05`, `BR-PRM-01…06`, `BR-REV-01…05`, `BR-VND-05`, `BR-RET-04`, `BR-SHP-03`, `BR-PAY-06`.
- Requirements: `FR-017` (channels/preferences), `FR-019` (CMS/coupons), `FR-020` (tickets), `FR-006` (reviews), `FR-008` (follows).
- Related UX docs: `DOC-UX-002` (FL-08 coupon, FL-09 review), `DOC-UX-005` (error/offline states used by support entries), `DOC-UX-007` (bilingual copy rules).
- Gaps: `GAP-03` (email channel — excluded until confirmed), frequency caps and UI retention windows marked `INFERENCE`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
