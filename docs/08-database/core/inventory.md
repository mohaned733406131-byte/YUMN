---
document_id: DOC-DBE-006
entity_id: DB-006
title: Entity inventory (DB-006)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-005, DATA-REQ-006, NFR-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005]
---

# Entity: `inventory` (DB-006) — table `b02.inventory`

## Overview & purpose

One stock row per product implementing FR-005: stock levels, **15-minute reservation TTL (`C-13`)**, permanent deduction on payment, restoration on cancellation, and **oversell prohibition** (BR-CAT-07). The row is the serialization point for stock: reservations and deductions take a row lock here inside the payment/order transaction (NFR-008 idempotency), so concurrent buyers cannot drive stock negative even when app logic fails (`ck_inventory_no_negative`).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `product_id` | uuid | no | app-generated | **PK** + FK `fk_inventory_product_id` → `b02.product` ON DELETE RESTRICT | 1:1 with product (product_id doubles as PK) |
| `store_id` | uuid | no | — | FK `fk_inventory_store_id` → `b03.store` ON DELETE RESTRICT | denormalized owner key for vendor stock queries (DATA-REQ-008) |
| `qty_on_hand` | bigint | no | `0` | `ck_inventory_no_negative` (`>= 0`) | physical units |
| `qty_reserved` | bigint | no | `0` | `ck_inventory_no_negative` (`>= 0 AND <= qty_on_hand`) | held units (C-13, cart countdown) |
| `qty_available` | bigint **generated** | — | `GENERATED ALWAYS AS (qty_on_hand - qty_reserved) STORED` | `ck_inventory_no_negative` (`>= 0`) | sellable units; never written directly |
| `reservation_expires_at` | timestamptz | yes | null | — | expiry of the newest reservation batch recorded on this row — informational for the TTL sweeper; authoritative per-line expiry lives in `b02.stock_reservation.expires_at` (C-13) |
| `version` | integer | no | `0` | `>= 0` (`ck_inventory_version_non_negative`) | optimistic lock for non-locking reads (doc DOC-DB-005 §4) |
| `low_stock_threshold` | integer | no | `5` | `>= 0` | vendor alerting hint (FR-005 ops view) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

**Supporting table `b02.stock_reservation`:** `(id, inventory_id, cart_item_id, qty, status ∈ {HELD, RELEASED, CONSUMED}, expires_at = created_at + 15 min, created_at)` with `UNIQUE(cart_item_id) WHERE status='HELD'` and a partial index on `expires_at` (the TTL sweeper's access path, DOC-DB-004 §1.2).

## Indexes

- PK `product_id` — stock check is a single-row lookup (hot path HP-4)
- `idx_inventory_store_id` on `(store_id)` — vendor stock list
- (sweeper) `idx_stock_reservation_expires_at` on `stock_reservation(expires_at)` WHERE `status='HELD'`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `inventory` | `product` (DB-005) | 1:1 | `fk_inventory_product_id` (PK) | RESTRICT |
| `inventory` | `store` (DB-003) | N:1 | `fk_inventory_store_id` | RESTRICT |
| `stock_reservation` | `inventory` | N:1 | `fk_stock_reservation_inventory_id` | CASCADE |
| `stock_reservation` | `cart_item` (b05) | N:1 | `fk_stock_reservation_cart_item_id` | CASCADE |

## Invariants & business rules enforced

**DB-enforced**

1. **No negative stock, ever:** `qty_on_hand >= 0`, `qty_reserved >= 0`, `qty_reserved <= qty_on_hand`, `qty_available >= 0` — together they make oversell structurally impossible (BR-CAT-07, DATA-REQ-001).
2. `qty_available` is a **generated column** — cannot be forged by an application write.
3. `version >= 0`; `product_id` PK guarantees exactly one stock row per product.

**App-enforced (with DB row lock as backstop)**

1. Reserve: inside a transaction, `SELECT … FOR UPDATE` the inventory row, check `qty_available >= qty`, insert `stock_reservation` (`expires_at = now() + 15 min`), `qty_reserved += qty` (C-13). The row lock serializes concurrent reservations (NFR-008).
2. TTL expiry: sweeper job releases reservations with `expires_at <= now()` — `qty_reserved -= qty`, status `RELEASED` (C-13, BR-CRT-02). Idempotent: re-running never double-releases (status guard).
3. Payment success: `qty_on_hand -= qty`, reservation → `CONSUMED` (permanent deduction, FR-005).
4. Cancellation/refund: `qty_on_hand += qty` restoration with an audit entry (FR-005; adjustments are visible in ops reports).
5. Optimistic path: stock displayed to users is read without lock (`version` unchanged); any conflicting write bumps `version` and the losing writer retries (409-style conflict handling app-side).
6. Reconciliation job compares `qty_on_hand` against reservation/consumption events and alerts on drift (DATA-REQ-006).

## Example rows

```text
product_id=0198fa11-…  store_id=0198f701-…  qty_on_hand=48  qty_reserved=6   qty_available=42  reservation_expires_at=2026-09-26T14:35:00Z  version=127  low_stock_threshold=5  updated_at=2026-09-26T14:20:00Z
product_id=0198fa77-…  store_id=0198f701-…  qty_on_hand=0   qty_reserved=0   qty_available=0   reservation_expires_at=NULL                  version=3    low_stock_threshold=5  updated_at=2026-09-25T09:11:02Z
product_id=0198fad0-…  store_id=0198f812-…  qty_on_hand=15  qty_reserved=0   qty_available=15  reservation_expires_at=NULL                  version=42   low_stock_threshold=2  updated_at=2026-09-24T13:00:00Z
```

(stock_reservation examples: `qty=2, status=HELD, expires_at=2026-09-26T14:35:00Z` — two active holds behind row 1.)

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
