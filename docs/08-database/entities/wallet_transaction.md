---
document_id: DOC-DBE-011
entity_id: DB-011
title: Entity wallet_transaction (DB-011)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-013, FR-014, DATA-REQ-006, DATA-REQ-007, SEC-REQ-010, NFR-008, NFR-017, NFR-019]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005]
---

# Entity: `wallet_transaction` (DB-011) — table `b07.wallet_transaction`

## Overview & purpose

The **append-only double-entry ledger** of the platform — the single source of truth for all money (BR-PAY-06, DATA-REQ-007). Every balance change (top-up, order hold/capture, release, refund, payout, commission, adjustment) posts here as signed rows grouped into balanced entry sets. Corrections are **compensating entries, never edits** (DATA-REQ-007); the wallet balance (DB-010) and escrow/payable views are caches of this table. Partitioned monthly by `created_at` for the 100M-scale volume and 5-year financial retention (NFR-017, NFR-019).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK (composite `(id, created_at)` — partitioned) | UUID v7 |
| `created_at` | timestamptz | no | `now()` | partition key | **no `updated_at` — append-only** |
| `entry_group_id` | uuid | no | app-generated | — | all rows of one business event share it; Σ `amount_yer` per group = 0 (validated by job, BR-PAY-06) |
| `type` | `ledger_type` | no | — | enum `TOPUP, ORDER_HOLD, ORDER_CAPTURE, RELEASE, REFUND, PAYOUT, COMMISSION, ADJUSTMENT` | business classification (FR-013/FR-014) |
| `account` | `ledger_account` | no | — | enum `CUSTOMER_WALLET, ESCROW_HELD, VENDOR_PAYABLE, PLATFORM_CASH, COMMISSION_INCOME, REFUND_CLEARING, ROUNDING_ACCOUNT` | double-entry account (BR-PAY-06, BR-FIN-05 rounding account) |
| `wallet_id` | uuid | yes | null | FK `fk_wallet_transaction_wallet_id` → `b07.wallet` ON DELETE RESTRICT; CHECK `account='CUSTOMER_WALLET' → wallet_id IS NOT NULL` | NULL for platform/escrow/payable postings |
| `amount_yer` | bigint | no | — | `amount_yer <> 0` (`ck_wallet_transaction_amount_nonzero`) | **signed**: `> 0` credit to the account, `< 0` debit (BR-PAY-10 integer YER) |
| `balance_after_yer` | bigint | yes | null | CHECK `account='CUSTOMER_WALLET' → balance_after_yer IS NOT NULL`; else must be NULL | running wallet balance at posting time — statement display (FR-013) |
| `currency` | char(3) | no | `'YER'` | `ck_currency_yer` | C-04 |
| `reference_type` | `ledger_ref_type` | yes | null | enum `ORDER, SUB_ORDER, PAYMENT, REFUND, PAYOUT, ESCROW, ADJUSTMENT` | — |
| `reference_id` | uuid | yes | null | `reference_type IS NOT NULL ⇔ reference_id IS NOT NULL` (app + CHECK) | evidence link (BR-ESC-08) |
| `idempotency_key` | varchar(160) | no | — | `uq_wallet_transaction_idempotency_key` | ledger posts exactly once (BR-PAY-08, BR-PLT-03) |
| `description` | varchar(255) | no | — | — | human-readable memo (localized at read time — C-24) |
| `actor_type` | `actor_type` | no | `'SYSTEM'` | enum `USER, ADMIN, SYSTEM` | who caused the posting |
| `actor_user_id` | uuid | yes | null | FK → `b01.user` ON DELETE RESTRICT | NULL for automated/system postings (ACT-07) |

**There are no `UPDATE` or `DELETE` privileges on this table for any application role** (DOC-DB-005 §7): immutability is enforced by `GRANT SELECT, INSERT` only, with DDL reserved to the migration role.

## Indexes

| Index | Type | Backs |
|---|---|---|
| PK `(id, created_at)` | btree (partitioned) | — |
| `uq_wallet_transaction_idempotency_key` | UNIQUE | exactly-once posting (BR-PLT-03) |
| `idx_wt_wallet_created` on `(wallet_id, created_at DESC)` | compound (partitioned) | **hot path:** wallet statement newest-first (FR-013) |
| `idx_wt_entry_group_id` | btree (partitioned) | double-entry validation Σ per group = 0 (BR-PAY-06) |
| `idx_wt_reference` on `(reference_type, reference_id)` | compound (partitioned) | order/payment/refund → money evidence (BR-ORD-09 timeline, FR-020 audit) |
| `idx_wt_type_created` on `(type, created_at)` | compound (partitioned) | daily reconciliation by type (BR-ESC-08, BR-FIN-03) |

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `wallet_transaction` | `wallet` (DB-010) | N:0..1 | `fk_wallet_transaction_wallet_id` | RESTRICT |
| `wallet_transaction` | `user` (actor) | N:0..1 | `fk_wallet_transaction_actor_user_id` | RESTRICT |
| references (polymorph via `reference_type/reference_id`) | `order`/`payment`/`refund`/`payout`/`escrow` | N:0..1 each | app-validated (no FK across polymorphs) | rows are permanent regardless |

## Invariants & business rules enforced

**DB-enforced**

1. Append-only shape: only `created_at` (no mutable columns), `amount_yer <> 0`, YER only, unique `idempotency_key`.
2. Wallet postings must carry `wallet_id` **and** `balance_after_yer`; non-wallet postings must carry neither (conditional CHECKs) — keeps the table's two roles unambiguous.
3. Enum-restricted `type`/`account` — no free-form money rows.
4. **Immutability:** `UPDATE`/`DELETE`/`TRUNCATE` revoked for every app role (DATA-REQ-007, SEC-REQ-010); a stray attempt fails with `permission denied`.

**App-enforced (with daily verification)**

1. Every business event posts a **balanced set** in one transaction: e.g. top-up = `TOPUP / CUSTOMER_WALLET +x` + `TOPUP / PLATFORM_CASH −x`; order capture = `ORDER_CAPTURE / CUSTOMER_WALLET −x` + `+x / ESCROW_HELD`; commission split at release writes `COMMISSION / COMMISSION_INCOME +c` and `RELEASE / VENDOR_PAYABLE + (x−c)` (BR-PAY-06, BR-ESC-03).
2. `balance_after_yer` is computed from the locked wallet row inside that transaction — never incremented independently (BR-PAY-05).
3. Corrections = new `ADJUSTMENT` rows referencing the original group; never edits (DATA-REQ-007).
4. Daily reconciliation: Σ per `entry_group_id = 0`; wallet caches = Σ postings; escrow + payable totals = provider/finance statements — mismatch alerts finance (BR-ESC-08, BR-FIN-03, DATA-REQ-006).
5. Retention: partitions retained ≥ 5 years; purge attempts on young financial data alert instead of deleting (DATA-REQ-003 R3/R5, NFR-019).

## Example rows

```text
group=0198ff01-…  type=TOPUP         account=CUSTOMER_WALLET  wallet_id=0198fe01-…  amount_yer=+50000   balance_after_yer=462350  reference_type=PAYMENT  reference_id=0198fd22-…  idempotency_key=wt_top_44ab_1  actor_type=SYSTEM  created_at=2026-09-26T09:03:44Z
group=0198ff01-…  type=TOPUP         account=PLATFORM_CASH    wallet_id=NULL         amount_yer=-50000   balance_after_yer=NULL    reference_type=PAYMENT  reference_id=0198fd22-…  idempotency_key=wt_top_44ab_2  actor_type=SYSTEM  created_at=2026-09-26T09:03:44Z
group=0198ff20-…  type=ORDER_CAPTURE account=CUSTOMER_WALLET  wallet_id=0198fe01-…  amount_yer=-215750  balance_after_yer=246600  reference_type=ORDER    reference_id=0198fc01-…  idempotency_key=wt_ord_9c1e_1  actor_type=SYSTEM  created_at=2026-09-26T14:22:03Z
group=0198ff20-…  type=ORDER_CAPTURE account=ESCROW_HELD      wallet_id=NULL         amount_yer=+215750  balance_after_yer=NULL    reference_type=ORDER    reference_id=0198fc01-…  idempotency_key=wt_ord_9c1e_2  actor_type=SYSTEM  created_at=2026-09-26T14:22:03Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
