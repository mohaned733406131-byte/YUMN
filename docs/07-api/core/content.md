---
document_id: DOC-API-017
title: API-CNT — Pages, Banners, Promotions & Coupons (FR-019, FR-011)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-019, FR-007, FR-008, FR-011, FR-017, FR-002, DATA-REQ-004, BR-PRM-01, BR-PRM-02, BR-PRM-03, BR-PRM-04, BR-PRM-05, BR-PRM-06, BR-VND-05, BR-PLT-06, SEC-REQ-004]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-019, DOC-BA-005, DOC-OVR-008]
---

# API-CNT — Content Pages, Banners, Promotions & Coupons

**Group:** `API-CNT` · **FR-019 (admin content), FR-011 (coupon validation)** · **Endpoints:** `API-CNT-001…020` · **Base:** `/api/v1`

Static/marketing content is database-backed and editable by admins with **role gating** (`SEC-REQ-004`). Coupons are validated server-side at cart/checkout — the client never applies discounts itself (`FR-011`). Coupon rules (`BR-PRM-*`): single-store or platform scope, **non-stackable with any other coupon** (`BR-PRM-06`), discount ≤ **90%** of the discounted amount, validity ≤ **90 days**, `maxDiscount` optional, per-user usage caps, `usageLimit` optional; expired/unknown/ineligible ⇒ distinct validation errors. Banners carry a `visibleTo` role list and optional schedule window; v1 has **no email channels** (`BR-NTF-01`) and **no wishlists** (FR-010 out-of-scope).

---

## 1. Endpoint Table

### 1.1 Public content

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-CNT-001 | `GET /pages/{slug}` | Public | Render a published CMS page (terms, privacy, about, help topics) | → `200 { slug, title: { ar, en }, bodyBlocks: [...], publishedAt, updatedAt }` | `NOT_FOUND` (unpublished ⇒ 404), `VALIDATION_ERROR` | FR-019, SEC-REQ-012, `UC-016` |
| API-CNT-002 | `GET /home` | Public (role-aware via token) | Home payload: hero banners, active promotions, followed-store highlights, featured categories | `?surface=CUSTOMER\|GUEST` → `200 { banners: [...], promotions: [ { code, label, discountPercent, endsAt } ], categories: [...], followFeed?: [ { storeId, name, newProductCount } ] }` — personalized slice only when authenticated | `VALIDATION_ERROR` | FR-007, FR-008, `BR-VND-05`, `UC-015` |
| API-CNT-003 | `GET /promotions` | Public | Active coupon/promotion gallery | `?scope=PLATFORM\|STORE&limit&cursor` → `200 { items: [ { code, scope, storeId?, label: { ar, en }, discountPercent, maxDiscount?, startsAt, endsAt, terms } ], page: {…} }` | `VALIDATION_ERROR` | FR-007, FR-011, `BR-PRM-01/03/04` |
| API-CNT-004 | `POST /coupons/validate` | `CUSTOMER` | Check a coupon against the current cart before checkout (server is the only judge) | `{ code, cartSnapshot? }` → `200 { valid, code?, discountAmount?, reason?, reasonKey? }` — `discountAmount` computed with half-up rounding per store (`BR-FIN-01`) | `COUPON_INVALID` (unknown/expired/used/wrong store/under `min_order_amount` — `details[].issue` distinguishes: `NOT_FOUND`, `EXPIRED`, `USAGE_LIMIT_REACHED`, `ALREADY_USED_BY_USER`, `MIN_NOT_MET`, `NOT_APPLICABLE`), `COUPON_STACKING_NOT_ALLOWED`, `VALIDATION_ERROR` | FR-011, `BR-PRM-01…08`, `AC-FR011-03`, `UC-011` |

### 1.2 Admin — pages

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-CNT-005 | `GET /admin/pages` | `ADMIN`, `MODERATOR` | CMS page list incl. drafts (offset) | `?page&pageSize&status&sort=updatedAt_desc` → `200 { items: [ { id, slug, title, status: "DRAFT"\|"PUBLISHED", updatedAt } ], page: {…}, total }` | `FORBIDDEN` | FR-019, `SEC-REQ-004` |
| API-CNT-006 | `POST /admin/pages` | `ADMIN` | Create a page draft | `{ slug, title: { ar, en }, bodyBlocks }` → `201 { id, status: "DRAFT", createdAt }` | `SLUG_TAKEN`, `VALIDATION_ERROR`, `FORBIDDEN` | FR-019, `UC-016` |
| API-CNT-007 | `GET /admin/pages/{id}` | `ADMIN`, `MODERATOR` | Page detail incl. draft content and publish history | → `200 { …page, publishedAt?, history: [ { at, by, action } ] }` | `NOT_FOUND` | FR-019 |
| API-CNT-008 | `PUT /admin/pages/{id}` | `ADMIN` | Update draft content (never mutates a live page silently) | `{ title?, bodyBlocks?, status? }` → `200 { …page, updatedAt }` | `NOT_FOUND`, `VALIDATION_ERROR`, `FORBIDDEN` | FR-019, `BR-PLT-06` |
| API-CNT-009 | `POST /admin/pages/{id}/publish` | `ADMIN` | Publish — `DRAFT → PUBLISHED`, public read switches atomically | → `200 { status: "PUBLISHED", publishedAt, auditId }` | `STATE_CONFLICT` (already published), `NOT_FOUND`, `FORBIDDEN` | FR-019, `BR-PLT-06`, `SEC-REQ-010` |
| API-CNT-010 | `DELETE /admin/pages/{id}` | `ADMIN` | Archive a page (soft delete; public route stops resolving) | → `204` | `NOT_FOUND`, `FORBIDDEN`, `STATE_CONFLICT` (referenced by an active campaign ⇒ archive only) | FR-019, `SEC-REQ-010` |

### 1.3 Admin — banners

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-CNT-011 | `GET /admin/banners` | `ADMIN`, `MODERATOR` | Banner list with schedule and targeting (offset) | `?page&pageSize&active` → `200 { items: [ { id, label, imageUrl, surface, visibleTo: ["CUSTOMER","VENDOR"], startsAt?, endsAt?, active } ], page: {…}, total }` | `FORBIDDEN` | FR-019, SEC-REQ-004 |
| API-CNT-012 | `POST /admin/banners` | `ADMIN` | Create a banner (image upload first via the shared upload endpoint) | `{ label, imageUrl, surface, visibleTo, startsAt?, endsAt? }` → `201 { …banner, active }` | `VALIDATION_ERROR`, `PAYLOAD_TOO_LARGE`, `FORBIDDEN` | FR-019, SEC-REQ-011 |
| API-CNT-013 | `PUT /admin/banners/{id}` | `ADMIN` | Edit banner content/targeting/schedule | `{ … }` → `200 { …banner }` | `NOT_FOUND`, `VALIDATION_ERROR`, `FORBIDDEN` | FR-019 |
| API-CNT-014 | `DELETE /admin/banners/{id}` | `ADMIN` | Remove a banner | → `204` (idempotent) | `NOT_FOUND`, `FORBIDDEN` | FR-019, `SEC-REQ-010` |

### 1.4 Coupons — admin & store

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-CNT-015 | `GET /admin/coupons` | `ADMIN`, `MODERATOR` | Platform-wide coupon list (offset) | `?page&pageSize&status&scope` → `200 { items: [ { code, scope, storeId?, discountPercent, startsAt, endsAt, status: "ACTIVE"\|"DISABLED"\|"EXPIRED", usageCount, usageLimit?, maxDiscount? } ], page: {…}, total }` | `FORBIDDEN` | FR-019, FR-011, `BR-PRM-01/03` |
| API-CNT-016 | `POST /admin/coupons` | `ADMIN` | Create a platform or per-store coupon | `{ code, scope: "PLATFORM"\|"STORE", storeId?, discountPercent, maxDiscount?, startsAt, endsAt, usageLimit?, perUserLimit?, minOrderAmount? }` → `201 { …coupon, status: "ACTIVE" }` — validates ≤90% discount and ≤90-day window server-side (`COUPON_BOUNDS_EXCEEDED`) | `DUPLICATE_RESOURCE` (code taken), `COUPON_BOUNDS_EXCEEDED`, `VALIDATION_ERROR`, `FORBIDDEN` | FR-011, FR-019, `BR-PRM-01/03/04/07`, `UC-011` |
| API-CNT-017 | `POST /admin/coupons/{id}/disable` | `ADMIN` | Disable an active coupon immediately | `{ reason }` → `200 { status: "DISABLED", disabledAt }` — in-flight carts get `COUPON_INVALID` on next validate | `STATE_CONFLICT` (already disabled/expired), `REASON_REQUIRED`, `NOT_FOUND`, `FORBIDDEN` | FR-019, `BR-PRM-03` |
| API-CNT-018 | `GET /store/coupons` | `VENDOR` (Manager/Owner) | Own-store coupons (offset) | `?page&pageSize&status` → `200 { items: [ …coupon + { redemptionCount } ], page: {…}, total }` — other stores' coupons never listed | `NOT_FOUND`, `STORE_SUSPENDED` | FR-019, FR-011, `BR-PRM-01`, `BR-VND-03` |
| API-CNT-019 | `POST /store/coupons` | `VENDOR` (Manager/Owner) | Create a store-scoped coupon — **requires `Idempotency-Key`** | `{ code, discountPercent, maxDiscount?, startsAt, endsAt, usageLimit?, perUserLimit?, minOrderAmount? }` → `201 { …coupon, scope: "STORE", storeId, status: "ACTIVE" }` — same ≤90% / ≤90-day guard (`COUPON_BOUNDS_EXCEEDED`) | `DUPLICATE_RESOURCE` (code taken), `COUPON_BOUNDS_EXCEEDED`, `IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`, `VALIDATION_ERROR`, `STORE_SUSPENDED` | FR-011, `BR-PRM-01/03/04`, `UC-011` |
| API-CNT-020 | `PUT /store/coupons/{id}` | `VENDOR` (Owner) | Update schedule/limits or disable own coupon (never the discount percent after issuance) | `{ startsAt?, endsAt?, usageLimit?, perUserLimit?, status? }` → `200 { …coupon }` — code and discountPercent are immutable | `NOT_FOUND` (foreign ⇒ 404), `STATE_CONFLICT` (expired), `VALIDATION_ERROR`, `STORE_SUSPENDED` | FR-019, `BR-PRM-01/04` |

## 2. Behavior Notes

- **Coupon evaluation order** (`BR-PRM-06`, `AC-FR011-03`): validate → apply item/store discounts → reject any second coupon with `COUPON_STACKING_NOT_ALLOWED`; the client shows the server-provided `discountAmount` only.
- **Rounding** (`BR-FIN-01`): `discountAmount` computed per store with the 15%-VAT half-up scheme from `wallet.md`/`orders.md` — the same figure appears in `POST /orders` totals.
- **Immutability** (`BR-PRM-01`, `BR-PRM-04`): the issued coupon `code` (unique within scope) and `discountPercent` never change; schedule/limit edits and disablement are the only mutations.
- **Role gating** (`SEC-REQ-004`): write operations require `ADMIN`; `MODERATOR` gets read-only rows (`FORBIDDEN` with `AUTH_INSUFFICIENT_SCOPE` details); every publish/disable writes an audit entry (`SEC-REQ-010`).
- **Cacheability**: `API-CNT-001…003` are the only cacheable reads in the contract (`Cache-Control: max-age=60, stale-while-revalidate=300`, `ETag`); everything else is `no-store`.
- **Customer token hydration**: home/promotions payloads adapt to role and locale (`BR-NTF-04`, `C-24`).

## 3. Pagination / Idempotency / Caching

`API-CNT-003` (promotions) and all admin/store lists use **offset** except `API-CNT-003` which accepts `limit&cursor` (gallery feed); admin/store tables are **offset** (see `pagination.md` §1). Mandatory idempotency key: `API-CNT-019`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
