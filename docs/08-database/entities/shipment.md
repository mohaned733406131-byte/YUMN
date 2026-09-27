---
document_id: DOC-DBE-013
entity_id: DB-013
title: Entity shipment (DB-013)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-015, SEC-REQ-002, SEC-REQ-005, DATA-REQ-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005, DOC-SA-010, DOC-OVR-008]
---

# Entity: `shipment` (DB-013) — table `b08.shipment`

## Overview & purpose

The delivery execution record for one sub-order (B08, FR-015): courier assignment (first-accept race, BR-SHP-04), the **delivery subset of the order states**, and the **6-digit delivery code** that replaces GPS (`C-16`, BR-SHP-02) — stored only as a hash with a 3-attempt lockout (BR-SHP-03, SEC-REQ-002). Zone is text, never coordinates (BR-SHP-05). A return pickup is a second shipment row with `kind='RETURN'` (FR-016 pickup leg).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `sub_order_id` | uuid | no | — | FK `fk_shipment_sub_order_id` → `b06.sub_order` ON DELETE RESTRICT; partial `UNIQUE(sub_order_id)` WHERE `kind='OUTBOUND'` | one outbound shipment per sub-order; returns ship separately |
| `order_id` | uuid | no | — | FK `fk_shipment_order_id` → `b06.order` ON DELETE RESTRICT | denorm for buyer tracking |
| `kind` | `shipment_kind` | no | `'OUTBOUND'` | enum `OUTBOUND, RETURN` | return leg links to `return_request` (DB-014) |
| `return_request_id` | uuid | yes | null | FK → `b09.return_request` ON DELETE RESTRICT; `kind='RETURN' → return_request_id IS NOT NULL` (app) | — |
| `courier_id` | uuid | yes | null | FK `fk_shipment_courier_id` → `b01.user` (role COURIER) ON DELETE SET NULL | assigned courier (owner key, DATA-REQ-008); attempts keep history |
| `state` | `shipment_state` | no | `'READY_FOR_PICKUP'` | enum `READY_FOR_PICKUP, ASSIGNED, PICKED_UP, IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED, CANCELLED` | **mirrors the delivery states of the order machine** (DOC-SA-010 §2); mirrored to `sub_order.state` app-side |
| `zone` | varchar(80) | no | — | — | shipping zone **text label** — no GPS, no coordinates (`C-16`, BR-SHP-05) |
| `method` | varchar(40) | no | `'STANDARD'` | — | delivery method input to `f(zone, weight, method)` (BR-SHP-01) |
| `delivery_code_hash` | bytea(32) | yes | null | `ck_shipment_code_hash` (`>= 32` bytes) | **SHA-256/HMAC of the 6-digit code — plaintext never stored** (SEC-REQ-002, BR-SHP-02) |
| `delivery_code_nonce` | bytea(16) | yes | null | — | salt/nonce for the hash |
| `code_issued_at` | timestamptz | yes | null | — | issued at OUT_FOR_DELIVERY (BR-SHP-02) |
| `code_attempts` | smallint | no | `0` | `ck_shipment_code_attempts` `BETWEEN 0 AND 3` | failed verifications (BR-SHP-03) |
| `code_locked_until` | timestamptz | yes | null | — | 3rd failure → lock **24 h** + auto support ticket (BR-SHP-03, SEC-REQ-005) |
| `failed_attempt_count` | smallint | no | `0` | `>= 0` | 3 failed delivery attempts → admin escalation (BR-SHP-06) |
| `version` | integer | no | `0` | `>= 0` | optimistic lock — **first accept wins** on assignment (BR-SHP-04) |
| `assigned_at` / `picked_up_at` / `out_for_delivery_at` / `delivered_at` | timestamptz | yes | null | monotonic ordering checked app-side | lifecycle timestamps |
| `delivery_verified_at` | timestamptz | yes | null | `delivered_at IS NOT NULL → delivery_verified_at IS NOT NULL` (app) | code + timestamp + courier identity = proof (BR-SHP-07) |
| `proof_photo_key` | varchar(200) | yes | null | — | optional photo in MinIO — never required (BR-SHP-07) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

**Supporting tables:**

- `b08.shipment_attempt(id, shipment_id, attempt_no, outcome ∈ {CODE_FAILED, DELIVERY_FAILED, PICKUP_FAILED}, courier_id, note, attempted_at)` — `UNIQUE(shipment_id, attempt_no)`; the evidence trail for BR-SHP-03/06/07.
- `b08.shipment_offer(id, shipment_id, courier_id, status ∈ {OFFERED, ACCEPTED, DECLINED, EXPIRED}, expires_at, responded_at)` — `UNIQUE(shipment_id, courier_id)`; broadcast offers, first `ACCEPTED` commits via `version` check (BR-SHP-04).

## Indexes

- PK `id`; `uq_shipment_sub_order_kind_outbound` partial UNIQUE
- `idx_shipment_courier_state` on `(courier_id, state)` WHERE `courier_id IS NOT NULL` — courier app "my deliveries" (FR-015)
- `idx_shipment_dispatch` on `(zone, state)` WHERE `state IN ('READY_FOR_PICKUP','OUT_FOR_DELIVERY')` — assignment engine: eligible couriers in zone (BR-SHP-04)
- `idx_shipment_sub_order_id` — sub-order → delivery status
- `shipment_attempt`: `uq_shipment_attempt_shipment_id_attempt_no`; `idx_shipment_attempt_courier_created`
- `shipment_offer`: `uq_shipment_offer_shipment_id_courier_id`; `idx_shipment_offer_courier_status`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `shipment` | `sub_order` (b06) | 1 outbound / N with returns | `fk_shipment_sub_order_id` | RESTRICT |
| `shipment` | `order` (DB-008) | N:1 | `fk_shipment_order_id` | RESTRICT |
| `shipment` | `user` (courier) | N:0..1 | `fk_shipment_courier_id` | SET NULL |
| `shipment` | `return_request` (DB-014) | N:0..1 | `fk_shipment_return_request_id` | RESTRICT |
| `shipment_attempt`, `shipment_offer` | `shipment` | N:1 | `fk_shipment_attempt_shipment_id`, `fk_shipment_offer_shipment_id` | CASCADE |
| `support_ticket` (b13) | `shipment` | N:0..1 | `fk_support_ticket_shipment_id` | SET NULL — auto-created on 3rd code failure (BR-SHP-03) |

## Invariants & business rules enforced

**DB-enforced**

1. State enum = delivery subset of the canonical machine; code hash `NOT NULL`-shaped (≥32 bytes) — **no plaintext 6-digit code column exists** (SEC-REQ-002, BR-SHP-02).
2. `code_attempts BETWEEN 0 AND 3` (BR-SHP-03); attempt numbering unique per shipment.
3. One outbound shipment per sub-order; unique offers per courier; YER-free (no money columns — money stays in `b07`).

**App-enforced**

1. Assignment: offers broadcast to eligible same-zone couriers; accept executes `UPDATE … SET version = version + 1 WHERE id = ? AND version = ?` — zero rows → 409, another courier won (BR-SHP-04, DOC-SA-010 §5).
2. Code verification: at OUT_FOR_DELIVERY a random 6-digit code is generated, delivered to the buyer via SMS/WhatsApp (BR-SHP-02, BR-NTF-03); courier submits it → HMAC compare against `delivery_code_hash`; attempts 1–2 return remaining attempts; **3rd failure sets `code_locked_until = now() + 24 h`, creates a support ticket, and records an attempt** (BR-SHP-03, SEC-REQ-005). Success → `DELIVERED` on sub-order + `delivered_at`, escrow clock starts (BR-ESC-01).
3. State changes here mirror `sub_order.state` in the same transaction (ASSIGNED→PICKED_UP→IN_TRANSIT→OUT_FOR_DELIVERY→DELIVERED); failed attempt (code wrong, attempts < 3) returns shipment to `IN_TRANSIT` per DOC-SA-010 §2.
4. 3 failed delivery attempts → escalation to admin review with full timeline (BR-SHP-06) — a support ticket, **not** a new order state.
5. Delivery proof = code verification + timestamp + courier identity; optional photo stored as a MinIO key (BR-SHP-07). **No GPS coordinates in any column** (`C-16`, BR-SHP-05) — enforced by schema review.
6. Courier visibility scoped to own assignments; admin dispatch view only (BR-ORD-09, DATA-REQ-008).

## Example rows

```text
id=0198ff01-…  sub_order_id=0198fc10-…  order_id=0198fc01-…  kind=OUTBOUND  courier_id=0198f3b1-…  state=IN_TRANSIT       zone=SA-NORTH  delivery_code_hash=0x6b1f…  code_attempts=0  failed_attempt_count=0  version=4  assigned_at=2026-09-26T14:50:00Z  picked_up_at=2026-09-26T15:05:00Z
id=0198ff12-…  sub_order_id=0198fa21-…  order_id=0198fa50-…  kind=OUTBOUND  courier_id=0198f3b1-…  state=OUT_FOR_DELIVERY  zone=TA-CENTRAL delivery_code_hash=0xa30c…  code_issued_at=2026-09-21T15:40:00Z  code_attempts=1  failed_attempt_count=1  version=7  out_for_delivery_at=2026-09-21T15:40:00Z
id=0198ff24-…  sub_order_id=0198fa21-…  order_id=0198fa50-…  kind=OUTBOUND  courier_id=0198f3b1-…  state=DELIVERED  zone=TA-CENTRAL  code_attempts=2  failed_attempt_count=2  delivered_at=2026-09-21T16:30:00Z  delivery_verified_at=2026-09-21T16:30:12Z  proof_photo_key=minio://proof/2026/09/21/8f2a.jpg  version=9
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
