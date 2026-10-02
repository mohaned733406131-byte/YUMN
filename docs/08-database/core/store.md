---
document_id: DOC-DBE-003
entity_id: DB-003
title: Entity store (DB-003)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-007, FR-008, SEC-REQ-002, DATA-REQ-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-005, DOC-BA-005]
---

# Entity: `store` (DB-003) — table `b03.store`

## Overview & purpose

The vendor storefront — the tenant boundary for the whole marketplace (B03). Realizes FR-007 (vendor onboarding & KYC, ≤48-h decision) and FR-008 (storefront configuration). Every vendor-scoped query in the system keys off `store_id` (BR-VND-07, DATA-REQ-008). One store per vendor account in v1 (BR-VND-02); products cannot go live until `kyc_status = 'APPROVED'` (BR-VND-01); suspension hides products, blocks new orders, freezes existing ones and holds payouts (BR-VND-04).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `owner_user_id` | uuid | no | — | FK `fk_store_owner_user_id` → `b01.user` ON DELETE RESTRICT, **UNIQUE** | BR-VND-02 one store per vendor |
| `name_ar` | varchar(120) | no | — | `length(btrim(name_ar)) > 0` | Arabic primary (C-24) |
| `name_en` | varchar(120) | yes | null | — | English parity (C-24) |
| `slug` | varchar(140) | no | — | `uq_store_slug`, `^[a-z0-9-]+$` app-side | storefront URL key |
| `description_ar` / `description_en` | text | yes | null | — | marketing copy |
| `status` | `store_status` | no | `'PENDING'` | enum `PENDING, ACTIVE, SUSPENDED, CLOSED` | FR-007/FR-008 lifecycle; suspension semantics = BR-VND-04 |
| `kyc_status` | `kyc_status` | no | `'PENDING'` | enum `PENDING, APPROVED, REJECTED` | gate for publishing (BR-VND-01) |
| `kyc_submitted_at` | timestamptz | yes | null | — | starts 48-h decision SLA (BR-VND-03) |
| `kyc_decided_at` | timestamptz | yes | null | `kyc_decided_at > kyc_submitted_at` | — |
| `kyc_decided_by` | uuid | yes | null | FK → `b01.user` ON DELETE SET NULL | admin/moderator actor (audit, BR-PLT-06) |
| `kyc_rejection_reason` | text | yes | null | `kyc_status='REJECTED' → kyc_rejection_reason IS NOT NULL` (app + CHECK) | resubmission resets to `PENDING` (BR-VND-03) |
| `commission_rate_bps` | smallint | no | `1000` | `ck_store_commission_rate_band` 500–2000 | per-vendor tier override; default 10 % (BR-ESC-03) |
| `hub_governorate_code` | char(2) | no | — | FK → `b01.governorate` | hub/origin — **text only, no GPS** (`C-16`) |
| `hub_district` | varchar(80) | no | — | — | zone resolution input |
| `hub_street_ciphertext` | bytea | yes | null | — | encrypted detail (SEC-REQ-002) |
| `operating_hours` | jsonb | no | `'{}'` | app-validated: weekday → `[open, close]` in `HH:MM` | affects accept SLA display (FR-008) |
| `is_returnable_default` | boolean | yes | null | — | `NULL` = inherit platform setting (`b13.platform_setting`) — C-11 policy layering |
| `return_period_days_default` | smallint | yes | null | `>= 0` when present | store-level default for new products (C-11) |
| `rating_avg` | numeric(3,2) | no | `0` | `BETWEEN 0 AND 5` | denormalized; recomputed incrementally by job (BR-REV-05) |
| `rating_count` | integer | no | `0` | `>= 0` | shown next to average (BR-REV-05) |
| `follower_count` | integer | no | `0` | `>= 0` | denormalized from `store_follower` (BR-VND-05) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |
| `closed_at` | timestamptz | yes | null | — | set when `status='CLOSED'` |

KYC **documents** (IDs, licences) live in `b03.kyc_document(store_id, object_key, doc_type, checksum, uploaded_at)` — object bytes in MinIO, keys only in Postgres (SEC-REQ-011, DOC-DB-002 §5).

## Indexes

- `uq_store_slug`, `uq_store_owner_user_id` (UNIQUE)
- `idx_store_status` on `(status, created_at DESC)` WHERE `status='ACTIVE'` — public listing
- `idx_store_kyc_status_submitted_at` on `(kyc_status, kyc_submitted_at)` WHERE `kyc_status='PENDING'` — 48-h SLA queue (BR-VND-03)
- PK `id`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `store` | `user` (owner) | 1:1 | `fk_store_owner_user_id` | RESTRICT |
| `store_member` | `store` | N:1 | `fk_store_member_store_id` | CASCADE (staff Viewer/Editor/Manager — BR-VND-06) |
| `kyc_document`, `store_follower` | `store` | N:1 | `fk_kyc_document_store_id`, `fk_store_follower_store_id` | CASCADE |
| `product` (DB-005) | `store` | N:1 | `fk_product_store_id` | RESTRICT |
| `sub_order` (b06), `escrow` (DB-012), `payout`, `coupon` (DB-016) | `store` | N:1 / N:0..1 | `fk_sub_order_store_id`, `fk_escrow_store_id`, `fk_payout_store_id`, `fk_coupon_store_id` | RESTRICT / RESTRICT / RESTRICT / SET NULL |

## Invariants & business rules enforced

**DB-enforced**

1. One store per vendor — `UNIQUE(owner_user_id)` (BR-VND-02; strict v1 reading: reopening after `CLOSED` requires an admin action, not a second row).
2. Unique slug; `commission_rate_bps` band 500–2000 (BR-ESC-03).
3. `kyc_status`/`status` enums; KYC decision fields consistent (`decided_at` after `submitted_at`, rejection reason required).
4. Hub stored as governorate/district/text — **no lat/lon columns** (`C-16`).

**App-enforced**

1. Publishing products requires `kyc_status='APPROVED'` (BR-VND-01); KYC decision within 48 h of `kyc_submitted_at`, rejection allows resubmission (BR-VND-03).
2. Suspension behavior: hide products, block new orders, freeze existing orders, hold payouts (BR-VND-04) — status checked in each affected service.
3. Only the Owner invites/removes/changes staff roles; staff cannot self-escalate (BR-VND-06).
4. Every vendor-facing query filters `store_id` (BR-VND-07); cross-store access denied + CI cross-tenant suite (DATA-REQ-008).
5. Payouts require `kyc_status='APPROVED'` and `status <> 'SUSPENDED'` (BR-ESC-06).

## Example rows

```text
id=0198f701-…  owner_user_id=0198f3b1-…  name_ar=متجر الحرمين  name_en=Al-Harmain Store  slug=al-harmain  status=ACTIVE  kyc_status=APPROVED  kyc_submitted_at=2026-09-10T09:00Z  kyc_decided_at=2026-09-11T14:20Z  commission_rate_bps=1000  hub_governorate_code=SA  hub_district=المنصورة  rating_avg=4.60  rating_count=132  follower_count=58
id=0198f7ab-…  owner_user_id=0198f2c4-…  name_ar=بيت العسل  name_en=Honey House       slug=honey-house  status=PENDING kyc_status=PENDING   kyc_submitted_at=2026-09-25T11:00Z  commission_rate_bps=1000  hub_governorate_code=TA  hub_district=الحوطة    rating_avg=0.00  rating_count=0   follower_count=0
id=0198f812-…  owner_user_id=0198f4d9-…  name_ar=سوق اليمن  name_en=Yemen Market      slug=yemen-market status=SUSPENDED kyc_status=APPROVED kyc_submitted_at=2026-08-02T08:30Z  kyc_decided_at=2026-08-02T18:10Z  commission_rate_bps=1500  hub_governorate_code=AE  hub_district=المنارة   rating_avg=4.10  rating_count=77   follower_count=41
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
