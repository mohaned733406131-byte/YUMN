---
document_id: DOC-DBE-010
entity_id: DB-010
title: Entity wallet (DB-010)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-013, SEC-REQ-006, DATA-REQ-007, DATA-REQ-008, NFR-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-005, DOC-BA-005, DOC-OVR-008]
---

# Entity: `wallet` (DB-010) — table `b07.wallet`

## Overview & purpose

One wallet per user (FR-013): the customer-facing balance used for every order (`C-01` wallet-only) and topped up through the permitted rails (`C-05`). The balance is a **materialized cache** — the ledger `b07.wallet_transaction` (DB-011) is the source of truth and the only sanctioned way money moves (BR-PAY-06, DATA-REQ-007). Redis never holds balances (DOC-DB-002 §5).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `user_id` | uuid | no | — | FK `fk_wallet_user_id` → `b01.user` ON DELETE RESTRICT, **UNIQUE** | exactly one wallet per user (owner key, DATA-REQ-008) |
| `balance_yer` | bigint | no | `0` | `ck_wallet_balance_non_negative` (`>= 0`) | **cache** of Σ ledger postings; never negative (BR-PAY-05) |
| `currency` | char(3) | no | `'YER'` | `ck_currency_yer` | single currency (C-04) |
| `is_frozen` | boolean | no | `false` | — | admin/legal freeze (BR-PAY-09): no pay, no top-up; refunds still credit |
| `freeze_reason` | varchar(255) | yes | null | `is_frozen → freeze_reason IS NOT NULL` (app + CHECK) | recorded in audit (BR-PLT-06) |
| `frozen_at` / `frozen_by` | timestamptz / uuid | yes | null | FK `frozen_by` → `b01.user` ON DELETE SET NULL | actor evidence |
| `version` | integer | no | `0` | `>= 0` | optimistic guard for non-locking reads; money paths use `SELECT … FOR UPDATE` (BR-PAY-05) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | created lazily on first top-up/order attempt |

**Holds:** there is **no `held_yer` column** — by canon the wallet is debited when the order reaches `PLACED` and the funds move into escrow (DOC-SA-010 §1). Anything "held" for an in-flight checkout is represented as `ORDER_HOLD` ledger postings counted as restricted balance, not as a second money column; adding a parallel `held` balance would create two truths (violating DATA-REQ-007/006).

## Indexes

- `uq_wallet_user_id` — wallet fetch per request is an indexed 1:1 lookup
- PK `id`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `wallet` | `user` (DB-001) | 1:1 | `fk_wallet_user_id` | RESTRICT |
| `wallet_transaction` (DB-011) | `wallet` | N:0..1 | `fk_wallet_transaction_wallet_id` | RESTRICT — ledger rows survive any user operation |

## Invariants & business rules enforced

**DB-enforced**

1. `balance_yer >= 0` (`ck_wallet_balance_non_negative`) — a negative balance cannot be stored even by a buggy write (BR-PAY-05).
2. One wallet per user (UNIQUE `user_id`); YER only (C-04).
3. Freeze consistency: `is_frozen` requires a reason.

**App-enforced**

1. **Balance changes only via the ledger:** the only sanctioned write is `UPDATE wallet SET balance_yer = … , updated_at = now()` executed **inside the same transaction** that inserts the corresponding `wallet_transaction` row(s) — never alone, never outside `b07` module code (BR-PAY-06, C-21 module ownership). Other modules' roles have no `UPDATE` grant on `b07.wallet`.
2. Pay/top-up paths take `SELECT … FOR UPDATE` on the wallet row, then re-check `balance_yer >= amount` (BR-PAY-05, NFR-008 idempotency).
3. Frozen wallets reject order payments and top-ups but accept refunds (BR-PAY-09).
4. Daily reconciliation recomputes `balance_yer` from `SUM(wallet_transaction.amount_yer)` per wallet and alerts on any mismatch (BR-ESC-08, BR-FIN-03, DATA-REQ-006); restore drills assert zero imbalance (DATA-REQ-004).
5. Account deletion anonymizes the user but **never removes wallet or ledger rows** — financial records ≥ 5 years (DATA-REQ-003 R3, NFR-019).

## Example rows

```text
id=0198fe01-…  user_id=0198f2c4-…  balance_yer=412350  currency=YER  is_frozen=false  freeze_reason=NULL  version=64  created_at=2026-09-14T10:25:00Z  updated_at=2026-09-26T14:22:03Z
id=0198fe18-…  user_id=0198f3b1-…  balance_yer=0       currency=YER  is_frozen=false  freeze_reason=NULL  version=2   created_at=2026-09-20T08:05:12Z  updated_at=2026-09-20T08:05:12Z
id=0198fe29-…  user_id=0198f4d9-…  balance_yer=75000   currency=YER  is_frozen=true   freeze_reason=legal_hold  frozen_at=2026-09-25T12:10:00Z  frozen_by=0198fa11-admin…  version=9  updated_at=2026-09-25T12:10:00Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
