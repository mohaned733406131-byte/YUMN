---
document_id: DOC-DBE-002
entity_id: DB-002
title: Entity address (DB-002)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-003, SEC-REQ-002, DATA-REQ-002]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-005, DOC-BA-005]
---

# Entity: `address` (DB-002) — table `b01.address`

## Overview & purpose

Customer delivery addresses used at checkout (FR-011 step 1) and in the address book (FR-003: **≤10 addresses per user**). Structured for domestic shipping (`C-17`) by governorate/district so the shipping-zone function can resolve fees (BR-SHP-01), while keeping personally identifying fields encrypted at rest (SEC-REQ-002). **No GPS coordinates exist anywhere in this table (`C-16`).** Data minimization (DATA-REQ-002): only fields needed to deliver a parcel are stored.

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `user_id` | uuid | no | — | FK `fk_address_user_id` → `b01.user` ON DELETE CASCADE | owner key (DATA-REQ-008) |
| `governorate_code` | char(2) | no | — | FK `fk_address_governorate_code` → `b01.governorate` ON DELETE RESTRICT | reference data, seeded (DOC-DB-006 §4) |
| `district` | varchar(80) | no | — | `length(btrim(district)) > 0` | administrative district — kept plaintext because zone resolution needs it; not identifying alone |
| `street_ciphertext` | bytea | no | — | — | street line encrypted AES-256 (SEC-REQ-002 R3) |
| `building_no` | varchar(20) | yes | null | — | optional delivery detail |
| `label` | varchar(30) | no | `'Home'` | — | e.g. Home/Work — not PII |
| `recipient_name_ciphertext` | bytea | no | — | — | PII (SEC-REQ-002) |
| `recipient_phone_ciphertext` | bytea | no | — | — | PII; format validated app-side pre-encryption (BR-AUTH-01 pattern) |
| `recipient_phone_hash` | bytea(32) | no | — | — | HMAC lookup for "same recipient" dedup; no plaintext phone |
| `is_default` | boolean | no | `false` | partial `UNIQUE(user_id)` WHERE `is_default AND deleted_at IS NULL` | one default per user |
| `is_active` | boolean | no | `true` | — | archived addresses stay for order history links |
| `created_at` | timestamptz | no | `now()` | — | — |
| `updated_at` | timestamptz | no | `now()` | trigger T1 | — |
| `deleted_at` | timestamptz | yes | null | — | soft delete; orders keep `shipping_address_snapshot` (DB-008) |

**Columns that must never appear:** `latitude`, `longitude`, `geo`, or any location coordinate — structural absence verified by a schema-review test (`C-16`, BR-SHP-05).

## Indexes

- PK `id`
- `idx_address_user_id` on `(user_id, is_default DESC, updated_at DESC)` — address book + checkout default fetch
- `uq_address_user_id_default` partial UNIQUE on `(user_id)` WHERE `is_default AND deleted_at IS NULL`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `address` | `user` (DB-001) | N:1 | `fk_address_user_id` | CASCADE |
| `address` | `governorate` | N:1 | `fk_address_governorate_code` | RESTRICT |
| `order` (DB-008) | `address` | N:0..1 | `fk_order_address_id` | SET NULL (+ immutable snapshot on the order) |

## Invariants & business rules enforced

**DB-enforced**

1. `is_default` unique per user (partial UNIQUE).
2. Required non-empty `district`, `governorate_code` FK to seeded reference data (no free-text governorates → zone logic can't silently break).
3. No coordinate columns exist (schema-level rule, `C-16`).

**App-enforced**

1. ≤10 active addresses per user (FR-003) — count check before insert; the 11th is rejected with a validation error.
2. Phone format `^7[0-9]{8}$` before encryption (BR-AUTH-01).
3. Governorate/district combination must be a valid domestic pair (`C-17`) — validated against `shipping_zone` mapping at checkout (BR-SHP-01).
4. Address edits/deletion never mutate historical orders — orders carry `shipping_address_snapshot` (DATA-REQ-001: referential history preserved).
5. Retention: addresses are erased/anonymized with account deletion (DATA-REQ-003 R2); delivery history keeps only the snapshot.

## Example rows

```text
id=0198f501-…  user_id=0198f2c4-…  governorate_code=SA  district=المنصورة   label=Home  is_default=true   is_active=true  street_ciphertext=0x71ab…  created_at=2026-09-14T10:20:00Z
id=0198f5a7-…  user_id=0198f2c4-…  governorate_code=AE  district=المنارة    label=Work  is_default=false  is_active=true  street_ciphertext=0x9a44…  created_at=2026-09-18T17:41:09Z
id=0198f6b3-…  user_id=0198f3b1-…  governorate_code=TA  district=الحوطة      label=Home  is_default=true   is_active=true  street_ciphertext=0x0f5e…  created_at=2026-09-21T09:05:44Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
