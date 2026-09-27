---
document_id: DOC-DBE-014
entity_id: DB-014
title: Entity return_request (DB-014)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-016, DATA-REQ-006, DATA-REQ-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005, DOC-SA-010, DOC-OVR-008]
---

# Entity: `return_request` (DB-014) — table `b09.return_request`

## Overview & purpose

The return/refund workflow (B09, FR-016) built on the order machine's return states (DOC-SA-010 §1 items 12–16). Records the buyer's request, the **return-window evidence** (BR-RET-01, `C-11`), vendor/admin decision, receipt and **inspection with a 72-hour deadline** (BR-RET-05), evidence images, and the link to the wallet refund (BR-RET-03/04).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `order_id` | uuid | no | — | FK `fk_return_request_order_id` → `b06.order` ON DELETE RESTRICT | buyer scoping (owner key with `buyer_user_id`) |
| `sub_order_id` | uuid | no | — | FK `fk_return_request_sub_order_id` → `b06.sub_order` ON DELETE RESTRICT | returns are per-vendor (C-10) |
| `store_id` | uuid | no | — | FK `fk_return_request_store_id` → `b03.store` ON DELETE RESTRICT | vendor queue owner key (DATA-REQ-008) |
| `buyer_user_id` | uuid | no | — | FK → `b01.user` ON DELETE RESTRICT | denorm for ownership checks |
| `state` | `return_state` | no | `'REQUESTED'` | enum `REQUESTED, APPROVED, REJECTED, RECEIVED, INSPECTED` | return workflow states (BR-RET-02 + inspection); order-level transition recorded in `order_status_history` |
| `reason` | varchar(60) | no | — | app-validated reason code (`DEFECTIVE`, `WRONG_ITEM`, `NOT_AS_DESCRIBED`, `DAMAGED_IN_TRANSIT`, `CHANGED_MIND`, `OTHER`) | structured reason (INFERENCE for the code list) |
| `reason_detail` | text | yes | null | `reason='OTHER' → reason_detail IS NOT NULL` (app) | buyer free text |
| `delivered_at` | timestamptz | no | — | copied from delivery confirmation | window start (BR-RET-01) |
| `return_period_days` | smallint | no | — | `>= 0` | snapshot of the product's policy at request time (C-11) — later policy edits don't rewrite history |
| `return_window_ends_at` | timestamptz | no | — | `= delivered_at + return_period_days days` (computed app-side at insert) | **window check field** (BR-RET-01) |
| `requested_at` | timestamptz | no | `now()` | — | checked against `return_window_ends_at` app-side — deliberately **not** a DB CHECK so admin arbitration (BR-RET-06) can accept late cases |
| `decided_at` | timestamptz | yes | null | — | approval/rejection timestamp; 48-h SLA auto-escalation app-side (DOC-SA-010 §2) |
| `decided_by` | uuid | yes | null | FK → `b01.user` ON DELETE SET NULL | vendor or admin actor (BR-RET-06: admin final arbiter, audited) |
| `rejection_reason` | text | yes | null | `state='REJECTED' → rejection_reason IS NOT NULL` (app + CHECK) | required by canon (DOC-SA-010 §2) |
| `received_at` | timestamptz | yes | null | — | set when vendor receives the item (state → RECEIVED) |
| `inspection_due_at` | timestamptz | yes | null | `inspection_due_at = received_at + interval '72 hours'` (set on RECEIVED) | **72-h inspection deadline** (BR-RET-05) — sweeper auto-approves on breach |
| `inspected_at` | timestamptz | yes | null | `inspected_at <= inspection_due_at` when met on time (late = auto path, recorded) | inspection conclusion |
| `inspection_outcome` | `inspection_outcome` | yes | null | enum `PASSED, FAILED` | PASSED → refund proceeds; FAILED handled via admin/dispute path (BR-RET-06) |
| `refund_id` | uuid | yes | null | FK `fk_return_request_refund_id` → `b07.refund` ON DELETE SET NULL | **refund link** (BR-RET-04 ≤ 3 business days) |
| `refund_amount_yer` | bigint | yes | null | `>= 0` when present | = returned item value (BR-RET-03) |
| `refund_shipping` | boolean | no | `false` | — | shipping refunded **only** for platform/vendor-side fault (BR-RET-03) |
| `version` | integer | no | `0` | `>= 0` | optimistic lock (vendor vs admin race) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

**Supporting tables:** `b09.return_item(id, return_request_id, order_item_id, qty, item_value_yer, UNIQUE(return_request_id, order_item_id))` — per-line quantities/values (BR-RET-03 refund = item value); `b09.return_evidence(id, return_request_id, object_key, kind ∈ {BUYER_PHOTO, VENDOR_PHOTO, CARRIER_PHOTO}, checksum, uploaded_at)` — MinIO keys only (SEC-REQ-011).

## Indexes

- PK `id`
- `idx_return_buyer_created` on `(buyer_user_id, created_at DESC)` — customer returns list (FR-016)
- `idx_return_store_state_created` on `(store_id, state, created_at DESC)` — vendor decision queue (BR-RET-02)
- `idx_return_inspection_due` on `(inspection_due_at)` WHERE `state='RECEIVED'` — **72-h sweeper** (BR-RET-05)
- `idx_return_order_id` on `(order_id)` — order page returns

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `return_request` | `order` (DB-008) / `sub_order` (b06) / `store` (DB-003) / `user` (buyer) | N:1 each | `fk_return_request_order_id`, `fk_return_request_sub_order_id`, `fk_return_request_store_id`, `fk_return_request_buyer_user_id` | RESTRICT |
| `return_request` | `refund` (b07) | N:0..1 | `fk_return_request_refund_id` | SET NULL |
| `return_item` | `return_request` / `order_item` (b06) | N:1 / N:1 | `fk_return_item_return_request_id`, `fk_return_item_order_item_id` | CASCADE / RESTRICT |
| `return_evidence` | `return_request` | N:1 | `fk_return_evidence_return_request_id` | CASCADE |
| `shipment` (DB-013) | `return_request` | N:0..1 (`kind='RETURN'`) | `fk_shipment_return_request_id` | RESTRICT — pickup leg |

## Invariants & business rules enforced

**DB-enforced**

1. State enum (`REQUESTED/APPROVED/REJECTED/RECEIVED/INSPECTED`); rejection requires a reason; window fields (`delivered_at`, `return_period_days`, `return_window_ends_at`) are mandatory and non-negative.
2. `refund_amount_yer >= 0`; unique (return_request, order_item) lines; evidence rows always FK-attached.

**App-enforced**

1. **Window check (BR-RET-01, C-11):** evaluated at `requested_at` against `return_window_ends_at` and the product's `is_returnable`. A request failing the check is **rejected** — either creation is refused with a policy error or the row is created directly in `state='REJECTED'` with `rejection_reason` (no approved return can result). The check is deliberately not a DB `CHECK` — when policy and dispute conflict the **admin is final arbiter** (BR-RET-06) and may accept a late request, which must remain possible.
2. State transitions mirror the canonical machine (RETURN_REQUESTED → APPROVED/REJECTED → RECEIVED → REFUNDED) — invalid moves return 409 (DOC-SA-010 §2/§5); decision SLA auto-escalates to admin after 48 h (DOC-SA-010 §2).
3. **Inspection deadline:** on RECEIVED set `inspection_due_at = received_at + 72 h`; if no conclusion by then the sweeper **auto-approves** the return (BR-RET-05) and writes an audit entry (BR-PLT-06).
4. Refund: amount = item value; shipping only for platform/vendor fault (BR-RET-03); wallet credit within 3 business days of REFUNDED (BR-RET-04) via `refund` row + ledger `REFUND` posting (BR-PAY-06); triggers proportionate commission reversal and escrow adjustment (BR-RET-07, BR-ESC-04/07).
5. Ownership: buyer sees own requests; vendor sees own store's requests; admin/moderator scoped (BR-ORD-09, DATA-REQ-008).

## Example rows

```text
id=0198fe50-…  order_id=0198fa50-…  sub_order_id=0198fa21-…  store_id=0198f701-…  buyer_user_id=0198f2c4-…  state=RECEIVED    reason=DEFECTIVE  delivered_at=2026-09-21T16:30:00Z  return_period_days=7  return_window_ends_at=2026-09-28T16:30:00Z  requested_at=2026-09-23T10:12:00Z  received_at=2026-09-25T09:00:00Z  inspection_due_at=2026-09-28T09:00:00Z  refund_amount_yer=NULL  refund_shipping=false  version=3
id=0198fe61-…  order_id=0198fb40-…  sub_order_id=0198fb11-…  store_id=0198f812-…  buyer_user_id=0198f3b1-…  state=INSPECTED   reason=CHANGED_MIND  delivered_at=2026-09-19T12:00:00Z  return_period_days=7  return_window_ends_at=2026-09-26T12:00:00Z  requested_at=2026-09-20T08:40:00Z  decided_at=2026-09-20T14:00:00Z  decided_by=0198f701-owner…  received_at=2026-09-22T10:10:00Z  inspection_due_at=2026-09-25T10:10:00Z  inspected_at=2026-09-23T17:45:00Z  inspection_outcome=PASSED  refund_id=0198fe70-…  refund_amount_yer=4500  refund_shipping=false  version=7
id=0198fe72-…  order_id=0198fa50-…  sub_order_id=0198fa21-…  store_id=0198f701-…  buyer_user_id=0198f4d9-…  state=REJECTED    reason=OTHER  reason_detail=past window by seller claim  delivered_at=2026-09-10T16:00:00Z  return_period_days=7  return_window_ends_at=2026-09-17T16:00:00Z  requested_at=2026-09-24T09:00:00Z  decided_at=2026-09-24T11:30:00Z  decided_by=admin…  rejection_reason=return window elapsed (BR-RET-01)  version=2
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
