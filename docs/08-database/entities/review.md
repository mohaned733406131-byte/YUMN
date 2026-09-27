---
document_id: DOC-DBE-015
entity_id: DB-015
title: Entity review (DB-015)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-006, DATA-REQ-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005]
---

# Entity: `review` (DB-015) — table `b02.review`

## Overview & purpose

Product reviews with ratings (B02, FR-006): **only the purchasing customer, only after delivery, 30-day window, one review per order item, editable once within 7 days** (BR-REV-01/02), integer rating 1–5 with ≤5 images (BR-REV-03), moderation by Moderator/Admin plus vendor response (BR-REV-04). Verified purchase is structural — the row FKs the exact `order_item` that was bought and delivered. Product/store rating denormalizations (BR-REV-05) are fed from visible rows only.

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `product_id` | uuid | no | — | FK `fk_review_product_id` → `b02.product` ON DELETE RESTRICT | reviewed product |
| `user_id` | uuid | no | — | FK `fk_review_user_id` → `b01.user` ON DELETE CASCADE | reviewer (owner key) |
| `store_id` | uuid | no | — | FK `fk_review_store_id` → `b03.store` ON DELETE RESTRICT | denorm for vendor inbox + ownership (DATA-REQ-008, BR-VND-07) |
| `order_id` | uuid | no | — | FK `fk_review_order_id` → `b06.order` ON DELETE RESTRICT | verified purchase evidence |
| `order_item_id` | uuid | no | — | FK `fk_review_order_item_id` → `b06.order_item` ON DELETE RESTRICT, **UNIQUE** | **one review per order item** (BR-REV-02) |
| `rating` | smallint | no | — | `ck_review_rating` `BETWEEN 1 AND 5` | integer stars (BR-REV-03) |
| `body` | text | yes | null | — | written review (optional — rating-only allowed) |
| `image_keys` | jsonb | yes | null | `ck_review_images_count`: `jsonb_array_length <= 5` | MinIO object keys (≤5 images — BR-REV-03; ≤5 MB/type/EXIF checked at upload — BR-CAT-08, SEC-REQ-011) |
| `status` | `review_status` | no | `'PENDING'` | enum `PENDING, APPROVED, REJECTED` | moderation queue (FR-006) |
| `is_hidden` | boolean | no | `false` | — | moderator/admin hide for abuse — keeps `APPROVED` history but removes visibility (BR-REV-04); every change writes an audit entry (BR-PLT-06) |
| `hidden_by` / `hidden_at` | uuid / timestamptz | yes | null | FK `hidden_by` → `b01.user` ON DELETE SET NULL | moderator actor evidence |
| `is_verified_purchase` | boolean | no | `true` | — | set true only when `order_item_id` belongs to the reviewer's DELIVERED order (app, BR-REV-01) |
| `edit_count` | smallint | no | `0` | `ck_review_edit_count` `<= 1` | **editable once** (BR-REV-02) |
| `edited_at` | timestamptz | yes | null | `edited_at > created_at` | — |
| `delivered_at` | timestamptz | no | — | — | snapshot used for the 30-day window check (BR-REV-01) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

**Supporting:** `b02.review_response(id, review_id UNIQUE, store_id, body, created_by, created_at, updated_at)` — **one vendor response per review** (BR-REV-04).

## Indexes

- PK `id`; `uq_review_order_item_id` (UNIQUE)
- `idx_review_product_id_visible` on `(product_id, created_at DESC)` WHERE `status='APPROVED' AND NOT is_hidden` — public list + rating aggregation (BR-REV-05)
- `idx_review_store_id_created_at` on `(store_id, created_at DESC)` — vendor moderation/response inbox
- `idx_review_user_id_created_at` on `(user_id, created_at DESC)` — "my reviews" + 7-day edit window

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `review` | `product` (DB-005) | N:1 | `fk_review_product_id` | RESTRICT |
| `review` | `user` (DB-001) | N:1 | `fk_review_user_id` | CASCADE |
| `review` | `store` (DB-003) | N:1 | `fk_review_store_id` | RESTRICT |
| `review` | `order` (DB-008) | N:1 | `fk_review_order_id` | RESTRICT |
| `review` | `order_item` (b06) | 1:1 | `fk_review_order_item_id` (UNIQUE) | RESTRICT |
| `review_response` | `review` / `store` | 1:0..1 / N:1 | `uq_review_response_review_id`, `fk_review_response_store_id` | CASCADE / CASCADE |

## Invariants & business rules enforced

**DB-enforced**

1. `rating BETWEEN 1 AND 5`; `image_keys` ≤ 5 entries (BR-REV-03).
2. Unique `order_item_id` → structurally **one review per order item** (BR-REV-02).
3. `edit_count <= 1` (one edit — BR-REV-02); status enum; `is_hidden` audit fields consistent.
4. FKs to product/user/store/order/order_item guarantee the review points at real, owned records (DATA-REQ-001).

**App-enforced**

1. Only the purchasing customer may create a review: `review.user_id` must equal `order.buyer_user_id` for the referenced `order_item` (BR-REV-01, ownership — DATA-REQ-008).
2. Only after `DELIVERED` and **within 30 days of delivery** (`delivered_at + 30 days`) (BR-REV-01).
3. One edit within 7 days of creation (BR-REV-02) — `edit_count`/`created_at` checked app-side.
4. Visibility for aggregation: `status='APPROVED' AND NOT is_hidden`; product `rating_avg/rating_count` and store rating updated incrementally by a job and reconciled nightly (BR-REV-05, DATA-REQ-006).
5. Moderation: Moderator/Admin may hide/reject with an audit entry; vendor may respond once via `review_response` (BR-REV-04).

## Example rows

```text
id=0198ff010-…  product_id=0198fa11-…  user_id=0198f2c4-…  store_id=0198f701-…  order_id=0198fa50-…  order_item_id=0198fa70-…  rating=5  body=جهاز ممتاز وتوصيل سريع  image_keys=["minio://reviews/2026/09/22/1.jpg"]  status=APPROVED  is_hidden=false  is_verified_purchase=true  edit_count=0  delivered_at=2026-09-21T16:30:00Z  created_at=2026-09-22T10:00:00Z
id=0198ff020-…  product_id=0198fa77-…  user_id=0198f3b1-…  store_id=0198f701-…  order_id=0198fb40-…  order_item_id=0198fb60-…  rating=3  body=NULL  image_keys=NULL  status=PENDING  is_hidden=false  is_verified_purchase=true  edit_count=0  delivered_at=2026-09-19T12:00:00Z  created_at=2026-09-20T18:22:00Z
id=0198ff030-…  product_id=0198fad0-…  user_id=0198f4d9-…  store_id=0198f812-…  order_id=0198fc10-…  order_item_id=0198fc40-…  rating=1  body=وصف غير صحيح  status=APPROVED  is_hidden=true  hidden_by=0198mod-…  hidden_at=2026-09-24T11:00:00Z  edit_count=1  edited_at=2026-09-23T09:30:00Z  delivered_at=2026-09-18T14:00:00Z  created_at=2026-09-19T08:00:00Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
