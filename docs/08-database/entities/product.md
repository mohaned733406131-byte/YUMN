---
document_id: DOC-DBE-005
entity_id: DB-005
title: Entity product (DB-005)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-004, FR-005, FR-006, FR-009, DATA-REQ-006]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005]
---

# Entity: `product` (DB-005) — table `b02.product`

## Overview & purpose

The sellable item at the heart of B02: Arabic-first naming (BR-CAT-01), integer YER pricing (BR-PAY-10, C-04), category assignment (≤5 levels, BR-CAT-03), images (≤10, BR-CAT-08), variants (≤5 dimensions / ≤50 combinations, BR-CAT-02), per-product return policy (C-11), rating denormalization (BR-REV-05) and search-sync flags (FR-009). Physical goods only — subscription/trial/sample/rental types are rejected (BR-CAT-05), and the DB enforces that structurally. Capacity target: 10M products (NFR-017) — the index set in DOC-DB-004 §1.2 is sized for that.

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `store_id` | uuid | no | — | FK `fk_product_store_id` → `b03.store` ON DELETE RESTRICT | tenant owner key (DATA-REQ-008, BR-VND-07) |
| `category_id` | uuid | no | — | FK `fk_product_category_id` → `b02.category` ON DELETE RESTRICT | required for publish (BR-CAT-01) |
| `name_ar` | varchar(200) | no | — | `length(btrim(name_ar)) > 0` | **mandatory Arabic name** (BR-CAT-01) |
| `name_en` | varchar(200) | yes | null | — | optional English (BR-CAT-01) |
| `slug` | varchar(220) | no | — | `uq_product_store_id_slug` | product URL within store |
| `description_ar` | text | yes | null | — | — |
| `description_en` | text | yes | null | — | — |
| `price_yer` | bigint | no | — | `ck_product_price_positive` (`> 0`) | whole YER (BR-PAY-10). Note: the 500-YER floor is an **order** bound (C-14), not a product bound (BR-CAT-04) |
| `sale_price_yer` | bigint | yes | null | `ck_product_sale_price`: `> 0 AND < price_yer` | active sale price (BR-CAT-04) |
| `currency` | char(3) | no | `'YER'` | `ck_currency_yer` | single currency (C-04) |
| `product_type` | `product_type` | no | `'PHYSICAL'` | enum with **only** `PHYSICAL` + CHECK `= 'PHYSICAL'` | DB-level rejection of subscription/trial/sample/rental (BR-CAT-05) |
| `is_returnable` | boolean | no | `true` | — | store default applied at create (C-11) |
| `return_period_days` | smallint | no | — | `>= 0` | merchant-configured window; return window = delivery + this (BR-RET-01, C-11) |
| `weight_grams` | integer | yes | null | `> 0` when present | input to shipping fee `f(zone, weight, method)` (BR-SHP-01) |
| `status` | `product_status` | no | `'DRAFT'` | enum `DRAFT, ACTIVE, DISABLED` | only `ACTIVE` appears in search/storefront (BR-CAT-06) |
| `rating_avg` | numeric(3,2) | no | `0` | `BETWEEN 0 AND 5` | denormalized from visible reviews (BR-REV-05) |
| `rating_count` | integer | no | `0` | `>= 0` | shown with average (BR-REV-05) |
| `search_dirty` | boolean | no | `true` | — | set on any content change; ES sync worker drains (FR-009; ES not SoR) |
| `search_synced_at` | timestamptz | yes | null | — | last successful ES sync |
| `created_by` | uuid | no | — | FK → `b01.user` ON DELETE RESTRICT | vendor staff actor for audit (BR-PLT-06) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |
| `deleted_at` | timestamptz | yes | null | — | **soft-delete** (BR-CAT-06); `status` set `DISABLED` by the same operation |

**Images:** a separate table `b02.product_image(id, product_id, object_key, position, checksum, created_at)` with `UNIQUE(product_id, position)` — chosen over a JSON array so image ordering, orphan-object reconciliation against MinIO (DATA-REQ-006), and ≤10-count checks are relational and indexable (BR-CAT-08).

## Indexes

- PK `id`; `uq_product_store_id_slug`
- `idx_product_store_id_status` on `(store_id, status, updated_at DESC)` — vendor panel
- `idx_product_category_id_status` on `(category_id, status)` WHERE `deleted_at IS NULL` — category browse
- `idx_product_storefront` on `(category_id, rating_avg DESC, created_at DESC)` WHERE `status='ACTIVE' AND deleted_at IS NULL` — pre-filtered, pre-sorted storefront listing (BR-CAT-06)
- `trgm_name_ar`, `trgm_name_en` — GIN trigram **search fallback** (NFR-007, DOC-DB-004 §4)
- `idx_product_search_dirty` on `(updated_at)` WHERE `search_dirty` — ES sync worker

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `product` | `store` (DB-003) | N:1 | `fk_product_store_id` | RESTRICT |
| `product` | `category` (DB-004) | N:1 | `fk_product_category_id` | RESTRICT |
| `inventory` (DB-006) | `product` | 1:1 | PK/FK `product_id` | RESTRICT |
| `product_image`, `product_variant`, `product_attribute_value` | `product` | N:1 | `fk_product_image_product_id`, … | CASCADE / RESTRICT / CASCADE |
| `cart_item` (b05), `order_item` (b06), `review` (DB-015) | `product` | N:1 / N:0..1 / N:1 | `fk_cart_item_product_id`, `fk_order_item_product_id`, `fk_review_product_id` | RESTRICT / **SET NULL** / RESTRICT |

`order_item` keeps a full product-name snapshot, so deleting a product never rewrites order history (SET NULL + snapshot, DATA-REQ-001).

## Invariants & business rules enforced

**DB-enforced**

1. `name_ar` NOT NULL non-empty (BR-CAT-01); `price_yer > 0`; sale price strictly below original (BR-CAT-04).
2. `product_type = 'PHYSICAL'` — non-physical types cannot exist in the schema (BR-CAT-05).
3. `return_period_days >= 0`; `currency = 'YER'`; status enum (`DRAFT/ACTIVE/DISABLED`).
4. Unique `(store_id, slug)`; FKs require an existing store and category.

**App-enforced**

1. Publish gate: a product becomes `ACTIVE` only if category exists, ≥1 image, stock ≥0, store `ACTIVE` with `kyc_status='APPROVED'` (BR-CAT-01, BR-VND-01) — multi-table conditions.
2. ≤10 images, ≤5 MB each, jpg/png/webp, EXIF stripped (BR-CAT-08, SEC-REQ-011) — upload validation.
3. Variants: ≤5 dimensions, ≤50 combinations, SKU unique within store (BR-CAT-02) — combination math is app-side; SKU uniqueness is DB (UNIQUE).
4. Soft-delete: `deleted_at` set + `status='DISABLED'`; only `ACTIVE` rows index to ES/search (BR-CAT-06).
5. Rating/job denormalization is incremental and reconciled nightly against visible reviews (BR-REV-05, DATA-REQ-006).
6. Changing content sets `search_dirty=true` in the same transaction (search rebuild never loses changes — NFR-007).

## Example rows

```text
id=0198fa11-…  store_id=0198f701-…  category_id=0198f97c-…  name_ar=هاتف نوكيا 105  name_en=Nokia 105  slug=nokia-105  price_yer=95000  sale_price_yer=89000  currency=YER  product_type=PHYSICAL  is_returnable=true  return_period_days=7  weight_grams=95  status=ACTIVE  rating_avg=4.40  rating_count=57  search_dirty=false  search_synced_at=2026-09-25T22:10Z
id=0198fa77-…  store_id=0198f701-…  category_id=0198f944-…  name_ar=شاحن سريع 20 واط  name_en=Fast Charger 20W  slug=fast-charger-20w  price_yer=4500  sale_price_yer=NULL  currency=YER  product_type=PHYSICAL  is_returnable=true  return_period_days=7  weight_grams=120  status=DRAFT  rating_avg=0.00  rating_count=0  search_dirty=true
id=0198fad0-…  store_id=0198f812-…  category_id=0198f900-…  name_ar=ساعة رقمية  name_en=Digital Watch  slug=digital-watch  price_yer=15000  sale_price_yer=NULL  currency=YER  product_type=PHYSICAL  is_returnable=false  return_period_days=0  status=DISABLED  rating_avg=3.90  rating_count=12  deleted_at=2026-09-24T13:00Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
