---
document_id: DOC-DBE-012
entity_id: DB-012
title: Entity escrow (DB-012)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-014, DATA-REQ-006, DATA-REQ-007, NFR-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005, DOC-OVR-008, DOC-SA-010]
---

# Entity: `escrow` (DB-012) — table `b07.escrow`

## Overview & purpose

The buyer-protection hold at the heart of the yumn trust model (`C-12`, FR-014). One row **per sub-order** records the amount held from the master capture, when it was funded, when it becomes releasable (**DELIVERED + 7 days**, BR-ESC-01), its state (`HELD / RELEASED / REFUNDED / FROZEN`), and — recorded **at release** — the commission split (BR-ESC-03, 5–20 % per vendor tier, default 10 %). Disputes freeze release (BR-ORD-05); refunds draw from held funds first (BR-ESC-07).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `sub_order_id` | uuid | no | — | FK `fk_escrow_sub_order_id` → `b06.sub_order` ON DELETE RESTRICT, **UNIQUE** | exactly one hold per sub-order (C-10 allocation) |
| `order_id` | uuid | no | — | FK `fk_escrow_order_id` → `b06.order` ON DELETE RESTRICT | denorm for dispute/ops queries |
| `store_id` | uuid | no | — | FK `fk_escrow_store_id` → `b03.store` ON DELETE RESTRICT | vendor payable owner key (DATA-REQ-008) |
| `amount_yer` | bigint | no | — | `>= 0` (`ck_escrow_amounts`) | held amount = sub-order total at funding time |
| `currency` | char(3) | no | `'YER'` | `ck_currency_yer` | C-04 |
| `state` | `escrow_state` | no | `'HELD'` | enum `HELD, RELEASED, REFUNDED, FROZEN` | BR-ESC-01/02, BR-ORD-05 |
| `funded_at` | timestamptz | no | `now()` | — | set when the master payment captures at `PLACED` (DOC-SA-010 §1) |
| `release_at` | timestamptz | yes | null | `release_at = delivered_at + interval '7 days'` (set app-side on DELIVERED) | **7-day hold** (BR-ESC-01, `C-12`) |
| `delivered_at` | timestamptz | yes | null | — | copied from the sub-order's delivery timestamp when state → DELIVERED |
| `released_at` | timestamptz | yes | null | `ck_escrow_released_complete` | set by release job |
| `commission_rate_bps` | smallint | yes | null | `ck_escrow_rate_band` 500–2000 | **snapshotted at release** from the vendor tier (BR-ESC-03) |
| `commission_amount_yer` | bigint | yes | null | `>= 0` when present | computed at release: line subtotal after coupon × rate (BR-ESC-03); reversed proportionally on later refund (BR-ESC-04) |
| `payout_amount_yer` | bigint | yes | null | `>= 0` when present | `amount_yer − commission − refunded` at release — what the vendor can be paid |
| `refunded_amount_yer` | bigint | no | `0` | `>= 0 AND <= amount_yer` | cumulative refunds charged against this hold first (BR-ESC-07) |
| `frozen_reason` | varchar(255) | yes | null | `state='FROZEN' → frozen_reason IS NOT NULL` (app + CHECK) | open dispute id/notes (BR-ORD-05) |
| `frozen_at` | timestamptz | yes | null | — | — |
| `version` | integer | no | `0` | `>= 0` | optimistic lock: release vs dispute race (DOC-SA-010 §5) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

## Indexes

- PK `id`; `uq_escrow_sub_order_id`
- `idx_escrow_due` on `(release_at)` WHERE `state='HELD'` — **release job** sweeps due holds (BR-ESC-01/02)
- `idx_escrow_state_order_id` on `(state, order_id)` — dispute freeze checks (BR-ORD-05)
- `idx_escrow_store_state` on `(store_id, state)` — vendor payable balance / payout eligibility (BR-ESC-05)

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `escrow` | `sub_order` (b06) | 1:1 | `fk_escrow_sub_order_id` | RESTRICT |
| `escrow` | `order` (DB-008) | N:1 | `fk_escrow_order_id` | RESTRICT |
| `escrow` | `store` (DB-003) | N:1 | `fk_escrow_store_id` | RESTRICT |
| `payout` (b07) ↔ `escrow` | N:N via `b07.payout_escrow(payout_id, escrow_id, amount_yer, UNIQUE(escrow_id))` | — | — | released holds enter payout batches (BR-ESC-05) |
| `dispute` (b13) | `escrow` | 1:0..n freeze effect via `order_id/sub_order_id` | app-enforced | open dispute ⇒ `state='FROZEN'` (BR-ORD-05) |

## Invariants & business rules enforced

**DB-enforced**

1. One escrow per sub-order (UNIQUE) — funding allocation can't double (NFR-008 idempotency).
2. Amount sanity: `amount_yer >= 0`, `0 <= refunded_amount_yer <= amount_yer`, commission band 500–2000 bps, `RELEASED → released_at + commission + rate` all present (`ck_escrow_released_complete`).
3. State enum (`HELD/RELEASED/REFUNDED/FROZEN`); frozen rows require a reason.

**App-enforced**

1. **Funding:** created in the order-placement transaction from the master capture — sub-order total moves `ESCROW_HELD` ← `CUSTOMER_WALLET` (BR-ORD-02, C-10).
2. **Release schedule:** on sub-order DELIVERED, set `delivered_at` and `release_at = delivered_at + 7 days` (BR-ESC-01, C-12).
3. **Release guard** (job sweeps `idx_escrow_due`): release only if `now() >= release_at` **AND** no open dispute **AND** sub-order state ∉ {DISPUTED, RETURN_*, REFUNDED} (BR-ESC-02). On release: compute commission from tier snapshot (BR-ESC-03), post ledger `RELEASE`/`COMMISSION` groups (BR-PAY-06), set `payout_amount_yer`, state → `RELEASED` — one transaction with `version` check.
4. **Freeze:** opening a dispute sets `FROZEN` (+reason); admin resolution unfreezes → `RELEASED` (vendor wins, audit entry required) or `REFUNDED` (buyer wins) (DOC-SA-010 §2, BR-ORD-05).
5. **Refunds:** charged against `refunded_amount_yer` first; shortfall drawn from vendor payable (BR-ESC-07); proportionate commission reversal on later refunds (BR-ESC-04, BR-RET-07).
6. **Reconciliation:** escrow-held total must equal Σ ledger `ESCROW_HELD` postings daily (BR-ESC-08, DATA-REQ-006); payout batch executes 3–7 business days after release, minimum 1,000 YER, KYC-approved vendors only (BR-ESC-05/06).

## Example rows

```text
id=0198ff80-…  sub_order_id=0198fc10-…  order_id=0198fc01-…  store_id=0198f701-…  amount_yer=215750  state=HELD       funded_at=2026-09-26T14:22:03Z  delivered_at=NULL  release_at=NULL  refunded_amount_yer=0  version=1
id=0198ff91-…  sub_order_id=0198fa21-…  order_id=0198fa50-…  store_id=0198f701-…  amount_yer=98000   state=RELEASED   funded_at=2026-09-18T11:00:00Z  delivered_at=2026-09-21T16:30Z  release_at=2026-09-28T16:30Z  released_at=2026-09-28T16:31Z  commission_rate_bps=1000  commission_amount_yer=8850  payout_amount_yer=89150  refunded_amount_yer=0  version=3
id=0198ffa4-…  sub_order_id=0198fb11-…  order_id=0198fb40-…  store_id=0198f812-…  amount_yer=45000   state=FROZEN      funded_at=2026-09-19T09:14:00Z  frozen_at=2026-09-24T10:00Z  frozen_reason=dispute_open  refunded_amount_yer=0  version=2
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
