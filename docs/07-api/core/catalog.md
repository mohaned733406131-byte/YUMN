---
document_id: DOC-API-009
title: API-CAT — Catalog, Products, Inventory & Reviews (FR-004, FR-005, FR-006)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-012, FR-015, NFR-004, SEC-REQ-011, DATA-REQ-008, BR-CAT-01, BR-CAT-02, BR-CAT-03, BR-CAT-04, BR-CAT-05, BR-CAT-06, BR-CAT-07, BR-CAT-08, BR-REV-01, BR-REV-02, BR-REV-03, BR-REV-04, BR-REV-05, BR-VND-01, BR-VND-07]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-004, DOC-FR-005, DOC-FR-006, DOC-BA-005, DOC-OVR-008]
---

# API-CAT — Product Catalog, Inventory & Reviews

**Group:** `API-CAT` · **FR-004 (catalog), FR-005 (inventory), FR-006 (reviews)** · **Endpoints:** `API-CAT-001…022` · **Base:** `/api/v1`

Public reads return **ACTIVE, non-deleted products of non-suspended stores only** (`BR-CAT-06`, `BR-VND-04`). Publishing requires store KYC = APPROVED (`BR-VND-01`). Vendor writes are scoped to the caller's `store_id` (`BR-VND-07`). Prices are integer YER > 0 with sale price strictly below original (`BR-CAT-04`); product types are physical goods only (`BR-CAT-05`). **No wishlist endpoints exist** — persistent wishlists are explicitly out of scope for v1 (`FR-010` out-of-scope notes).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-CAT-001 | `GET /categories` | Public | Full category tree (depth ≤5, slugs unique per level) | `?locale` → `200 { items: [ { id, slug, nameAr, nameEn, parentId, children: [...] , productCount } ] }` — tree is small, single response, cacheable ≥ 5 min | `VALIDATION_ERROR` | FR-004, `BR-CAT-03`, `UC-001`, `NFR-004` |
| API-CAT-002 | `GET /categories/{slug}` | Public | One category: sub-categories + its product listing (cursor feed) | `?limit&cursor&sort&priceMin&priceMax` → `200 { category: {…}, children: [...], products: { items: [...], page: {…} } }` | `NOT_FOUND`, `VALIDATION_ERROR` | FR-004, FR-009, `BR-CAT-03/06`, `UC-001` |
| API-CAT-003 | `GET /products` | Public | Browse the catalog with filters and sort (cursor feed) | `?category&store&priceMin&priceMax&ratingMin&inStock&sort&limit&cursor` → `200 { items: [ { id, slug, nameAr, nameEn, price, salePrice, currency, store: {slug,nameAr}, rating, reviewCount, inStock, imageUrl } ], page: {…} }` | `VALIDATION_ERROR` (unknown filter), `NOT_FOUND` (bad cursor) | FR-004, FR-009, `BR-CAT-06`, `pagination.md` §1 |
| API-CAT-004 | `GET /products/{slug}` | Public | Product detail: prices, variants (≤5 dims, ≤50 combos), attributes, images, stock, return policy, store summary | → `200 { id, slug, names, description, price, salePrice, currency, categoryPath, attributes, variants: [ { sku, options, priceDelta, stock } ], images: [urls], availableStock, isReturnable, returnPeriodDays, store: {…}, rating, reviewCount, relatedProductIds }` | `NOT_FOUND` (inactive/deleted ⇒ 404), `VALIDATION_ERROR` | FR-004, FR-005, `BR-CAT-01/02/06`, `C-11`, `UC-007` |
| API-CAT-005 | `GET /store/products` | `VENDOR` | Own product table (all statuses incl. DRAFT/INACTIVE), offset pagination | `?page&pageSize&status&q&sort=updatedAt_desc` → `200 { items: [ { id, slug, nameAr, status, price, stock, available, updatedAt } ], page: {…}, total }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-004, `BR-VND-07`, `BR-CAT-06` |
| API-CAT-006 | `POST /store/products` | `VENDOR` (Editor/Manager/Owner) | Create a product draft | `{ nameAr, nameEn?, descriptionAr?, descriptionEn?, categorySlug, price, salePrice?, attributes?, variants?, stock, isReturnable?, returnPeriodDays? }` → `201 { …product, status: "DRAFT" }` | `VALIDATION_ERROR`, `PRODUCT_TYPE_NOT_ALLOWED`, `PRICE_INVALID`, `VARIANT_LIMIT_EXCEEDED`, `KYC_NOT_APPROVED`, `STORE_SUSPENDED` | FR-004, `BR-CAT-01/02/04/05`, `BR-VND-01`, `UC-017` |
| API-CAT-007 | `GET /store/products/{id}` | `VENDOR` | Full product for edit form | → `200 { …product, images, variants, reservations }` | `NOT_FOUND` (foreign store ⇒ 404), `STORE_SUSPENDED` | FR-004, `BR-VND-07` |
| API-CAT-008 | `PUT /store/products/{id}` | `VENDOR` (Editor/Manager/Owner) | Replace product content/pricing/policy; re-validates publish rules | full body → `200 { …product }` | `NOT_FOUND`, `PRICE_INVALID`, `VARIANT_LIMIT_EXCEEDED`, `VALIDATION_ERROR`, `STORE_SUSPENDED` | FR-004, `BR-CAT-01/02/04`, `UC-017` |
| API-CAT-009 | `DELETE /store/products/{id}` | `VENDOR` (Owner/Manager) | **Soft-delete** — product disappears from search/storefront; history retained | → `204` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-004, `BR-CAT-06`, `AC-FR004-04` |
| API-CAT-010 | `POST /store/products/{id}/publish` | `VENDOR` (Editor/Manager/Owner) | Publish: server re-validates `BR-CAT-01` completeness | → `200 { …product, status: "ACTIVE" }` — also enqueues the search index job | `PRODUCT_NOT_PUBLISHABLE`, `KYC_NOT_APPROVED`, `NOT_FOUND`, `STORE_SUSPENDED` | FR-004, `BR-CAT-01`, `BR-VND-01`, `AC-FR007-02`, `UC-017` |
| API-CAT-011 | `POST /store/products/{id}/unpublish` | `VENDOR` (Editor/Manager/Owner) | Withdraw from sale (status → `INACTIVE`); existing orders unaffected | → `200 { …product, status: "INACTIVE" }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-004, `BR-CAT-06` |
| API-CAT-012 | `POST /store/products/{id}/images` | `VENDOR` (Editor/Manager/Owner) | Upload a product image (multipart) | `multipart { file, position? }` → `201 { imageId, url, position }` — ≤10/product, ≤5 MB, jpg/png/webp only, EXIF stripped, malware scanned | `IMAGE_LIMIT_EXCEEDED`, `PAYLOAD_TOO_LARGE`, `UNSUPPORTED_MEDIA_TYPE`, `FILE_SCAN_FAILED`, `VALIDATION_ERROR` | FR-004, `BR-CAT-08`, SEC-REQ-011, `UC-017`, `api-conventions.md` §10 |
| API-CAT-013 | `DELETE /store/products/{id}/images/{imageId}` | `VENDOR` (Editor/Manager/Owner) | Remove an image (min 1 remains once ACTIVE) | → `204` | `NOT_FOUND`, `VALIDATION_ERROR` | FR-004, `BR-CAT-08` |
| API-CAT-014 | `GET /store/inventory` | `VENDOR` | Inventory table: `available = stock − reserved`, per SKU/variant (offset) | `?page&pageSize&q&lowStock` → `200 { items: [ { sku, productId, variantLabel, stock, reserved, available, updatedAt } ], page: {…}, total }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-005, `BR-CAT-07`, `UC-018` |
| API-CAT-015 | `GET /store/inventory/{sku}` | `VENDOR` | Single SKU detail incl. active reservations and TTL expiry times | → `200 { sku, stock, reserved, available, reservations: [ { orderId, quantity, expiresAt } ], reservationTtlMinutes: 15 }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-005, `C-13`, `BR-CAT-07` |
| API-CAT-016 | `PATCH /store/inventory/{sku}` | `VENDOR` (Editor/Manager/Owner) | Manual adjustment (set or ± delta) with reason — audited | `{ set?: n, delta?: ±n, reason }` → `200 { sku, stock, reserved, available }` — stock is an integer ≥ 0; adjusting below active reservations is refused | `INVALID_STOCK`, `STOCK_BELOW_RESERVATIONS`, `NOT_FOUND`, `VALIDATION_ERROR` | FR-005, `BR-CAT-07`, `BR-PLT-06`, `UC-018`, `AC-FR005-01` |
| API-CAT-017 | `POST /reviews` | `CUSTOMER` | Create a review for an own order item (verified purchase) | `{ orderItemId, rating: 1–5, comment?, imageFileIds?: [...] }` → `201 { …review, status: "PUBLISHED" }` — eligibility: order DELIVERED, ≤30 days, purchaser only, one per order item | `REVIEW_NOT_ELIGIBLE`, `REVIEW_ALREADY_EXISTS`, `VALIDATION_ERROR` (rating bounds, >5 images, >5 MB), `FILE_SCAN_FAILED` | FR-006, `BR-REV-01/02/03`, `AC-FR006-01/02/03`, SEC-REQ-011 |
| API-CAT-018 | `PATCH /reviews/{id}` | `CUSTOMER` (author) | Edit own review — exactly once within 7 days of creation | `{ rating?, comment?, imageFileIds? }` → `200 { …review }` | `REVIEW_EDIT_WINDOW_CLOSED`, `NOT_FOUND`, `VALIDATION_ERROR` | FR-006, `BR-REV-02` |
| API-CAT-019 | `GET /products/{slug}/reviews` | Public | Review list for a product (cursor feed), localized RTL rendering | `?rating&limit&cursor&sort` → `200 { items: [ { id, rating, comment, images, authorName, verifiedPurchase: true, createdAt, vendorResponse?, hidden: false } ], page: {…}, ratingSummary: { average, count, distribution } }` — hidden reviews excluded (`BR-REV-05`) | `NOT_FOUND`, `VALIDATION_ERROR` | FR-006, `BR-REV-04/05`, `DATA-REQ-008` |
| API-CAT-020 | `POST /reviews/{id}/report` | `CUSTOMER` | Report a review for moderation (reason + optional note) | `{ reason, note? }` → `201 { reportId, status: "OPEN" }` | `NOT_FOUND`, `VALIDATION_ERROR`, `RATE_LIMITED` | FR-006, `BR-REV-04`, `UC-038` |
| API-CAT-021 | `GET /store/reviews` | `VENDOR` | Visible reviews for the own store's products (offset table) | `?page&pageSize&rating&sort` → `200 { items: [ …review + { productId, orderReference } ], page: {…}, total }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-006, `BR-VND-07`, `UC-024` |
| API-CAT-022 | `POST /store/reviews/{id}/responses` | `VENDOR` (Owner/Editor) | Vendor response — exactly one per review, bilingual (ar/en) | `{ responseAr, responseEn? }` → `201 { response }` — audit-logged on creation | `RESPONSE_ALREADY_EXISTS`, `NOT_FOUND`, `VALIDATION_ERROR` | FR-006, `BR-REV-04`, `UC-024`, `BR-PLT-05` |

## 2. Behavior Notes

- **Stock semantics (FR-005 / `C-13`)**: public reads expose `availableStock = stock − reserved`. Checkout creates a 15-minute TTL reservation; expiry auto-releases (`BR-CRT-02`); payment success converts to a permanent atomic deduction exactly once (`BR-PLT-03`); cancellation/refund restores quantity. No endpoint ever drives stock below 0 (`BR-CAT-07`).
- **Search indexing**: create/edit/publish/unpublish/soft-delete enqueue BullMQ jobs (`{block}.{entity}.{action}`, 3 retries + DLQ — `BR-PLT-01/02`) that update Elasticsearch; index lag is eventual, browse-by-category remains authoritative during lag (`NFR-007`).
- **Moderation hide** of products/reviews is an admin/moderator action in `admin.md` (`POST /admin/moderation/{type}/{id}/hide`, `BR-REV-04`) — hidden items drop out of `API-CAT-019` averages after the recompute job.
- **Review eligibility** is validated server-side against order state (`SEC-REQ-004`) — UI affordances are UX only.
- **Variants**: SKU unique within the store (`BR-CAT-02`); duplicate ⇒ `DUPLICATE_RESOURCE`.

## 3. Pagination / Idempotency / Caching

| Endpoints | Mode |
|---|---|
| `API-CAT-002/003/019` (public feeds) | cursor (default 20, max 50) |
| `API-CAT-005/014/021` (vendor/admin-style tables) | offset (default 25, max 100) |
| `API-CAT-001` | single response (tree) |

Publish/unpublish are naturally idempotent (status set). Public catalog reads cacheable (`NFR-004`, target ≥ 80% hit ratio); `/store/*` reads are `no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
