---
document_id: DOC-DBE-009
entity_id: DB-009
title: Entity payment (DB-009)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-011, FR-013, SEC-REQ-008, DATA-REQ-007, INT-REQ-001, INT-REQ-002, INT-REQ-006]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005, DOC-OVR-008]
---

# Entity: `payment` (DB-009) — table `b07.payment`

## Overview & purpose

The intent/attempt record for money entering the platform: **order checkout payments (wallet-only, `C-01`)** and **wallet top-ups via m-Floos, OneCash, or bank transfer (`C-05`, INT-REQ-001/002)**. Captures state (`PENDING → AUTHORIZED → CAPTURED / FAILED / REFUNDED`), the mandatory idempotency key (BR-PAY-08, BR-PLT-03), provider references for idempotent callbacks (INT-REQ-006) and admin verification evidence for bank transfers (BR-PAY-04). Payments **never** hold truth about balances — every actual movement posts to the ledger `b07.wallet_transaction` (DB-011) inside the same transaction (BR-PAY-06, NFR-008).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `kind` | `payment_kind` | no | — | enum `ORDER, TOPUP` | which flow this intent belongs to |
| `order_id` | uuid | yes | null | FK `fk_payment_order_id` → `b06.order` ON DELETE RESTRICT; `kind='ORDER' → order_id NOT NULL` (CHECK) | NULL only for top-ups |
| `payer_user_id` | uuid | no | — | FK `fk_payment_payer_user_id` → `b01.user` ON DELETE RESTRICT | wallet owner (owner key, DATA-REQ-008) |
| `method` | `payment_method` | no | — | `ck_payment_method_wallet_only`: ORDER → `WALLET`; TOPUP → `MFLOOS / ONECASH / BANK_TRANSFER` | C-01, C-05, BR-PAY-01 |
| `amount_yer` | bigint | no | — | `> 0`; ORDER → `BETWEEN 500 AND 5000000` (C-14); TOPUP → `BETWEEN 1000 AND 5000000` (BR-PAY-02) | integer YER (BR-PAY-10) |
| `currency` | char(3) | no | `'YER'` | `ck_currency_yer` | C-04 |
| `state` | `payment_state` | no | `'PENDING'` | enum `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED` | `REFUNDED` only for `kind='ORDER'` (CHECK) |
| `idempotency_key` | varchar(128) | no | — | `uq_payment_idempotency_key` | BR-PAY-08 / BR-PLT-03 |
| `provider` | `payment_provider` | no | — | enum `INTERNAL_WALLET, MFLOOS, ONECASH, BANK` | `INTERNAL_WALLET` for order payments (no external rail) |
| `provider_ref` | varchar(120) | yes | null | partial `UNIQUE(provider, provider_ref)` | external transaction id — idempotent callback handling (INT-REQ-006) |
| `provider_status_raw` | jsonb | yes | null | — | sanitized callback/poll payload (no secrets, SEC-REQ-007) |
| `failure_code` | varchar(60) | yes | null | `state='FAILED' → failure_code IS NOT NULL` (app + CHECK) | e.g. `WALLET_INSUFFICIENT_FUNDS`, `PROVIDER_TIMEOUT` |
| `verified_by` | uuid | yes | null | FK → `b01.user` ON DELETE SET NULL | admin verifying a bank transfer (BR-PAY-04) |
| `verified_at` | timestamptz | yes | null | `method='BANK_TRANSFER' → state<> 'CAPTURED' OR verified_at IS NOT NULL` (app) | evidence of manual verification |
| `expires_at` | timestamptz | yes | null | — | PENDING intents swept to FAILED after expiry (app job) |
| `captured_at` | timestamptz | yes | null | `state='CAPTURED' → captured_at IS NOT NULL` | — |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

## Indexes

- PK `id`
- `uq_payment_idempotency_key`
- `uq_payment_provider_ref` partial UNIQUE on `(provider, provider_ref)` WHERE `provider_ref IS NOT NULL` — duplicate callbacks no-op (INT-REQ-006)
- `idx_payment_order_id` partial on `(order_id)` WHERE `order_id IS NOT NULL`
- `idx_payment_payer_created` on `(payer_user_id, created_at DESC)` — wallet history/top-up list
- `idx_payment_state_kind_created` on `(state, kind, created_at)` WHERE `state IN ('PENDING','AUTHORIZED')` — expiry sweeper + reconciliation window (BR-ESC-08)

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `payment` | `order` (DB-008) | N:0..1 | `fk_payment_order_id` | RESTRICT |
| `payment` | `user` (DB-001) | N:1 | `fk_payment_payer_user_id` | RESTRICT |
| `refund` (supporting) | `payment` | N:1 | `fk_refund_payment_id` | RESTRICT — `(id, payment_id, amount_yer, reason, state ∈ {PENDING, PROCESSING, COMPLETED, FAILED}, idempotency_key UNIQUE, created_at)` |
| `order` (DB-008) | `payment` | 1:1 | `fk_order_payment_id` | RESTRICT |
| `wallet_transaction` (DB-011) | `payment` (reference) | N:0..1 | reference polymorph (`reference_type='PAYMENT'`) | RESTRICT |

## Invariants & business rules enforced

**DB-enforced**

1. Method restrictions: order payments are **wallet-only** (C-01/BR-PAY-01); top-ups limited to the three permitted rails (C-05). Cards/BNPL/crypto have no enum value to express them.
2. Amount bounds: orders 500–5,000,000 YER (C-14); top-ups 1,000–5,000,000 YER (BR-PAY-02); positive and YER-only.
3. Idempotency key unique; provider reference unique per provider → callback/poll replays return the same outcome (BR-PAY-08, BR-PLT-03, INT-REQ-006).
4. State/`captured_at`/`failure_code` consistency CHECKs; `REFUNDED` restricted to order payments.

**App-enforced**

1. Capture path for order payments: `SELECT … FOR UPDATE` wallet → check `balance_yer >= amount` → post ledger (`ORDER_HOLD`/`ORDER_CAPTURE`) → mark `CAPTURED` → create order `PLACED` — one transaction, compensating saga on partial failure (BR-PAY-05, BR-PLT-04).
2. Top-up crediting only after **verified provider callback or reconciled poll**, never on client claim (BR-PAY-03); bank transfers credit only after admin verifies the reference (BR-PAY-04, INT-REQ-002) — sets `verified_by/verified_at` + audit entry (BR-PLT-06).
3. Frozen wallets (BR-PAY-09) can't create ORDER/TOPUP payments but still accept refunds (credit side).
4. Refund execution creates a `refund` row + ledger `REFUND` posting and moves `payment.state → REFUNDED` when fully refunded (BR-PAY-07).
5. Escalation of FAILED/PENDING beyond `expires_at` is a sweeper job with audit trail; reconciliation matches `CAPTURED` payments against provider statements daily (BR-ESC-08, BR-FIN-03).

## Example rows

```text
id=0198fd01-…  kind=ORDER   order_id=0198fc01-…  payer_user_id=0198f2c4-…  method=WALLET        amount_yer=215750  state=CAPTURED   idempotency_key=pay_ck_9c1e…  provider=INTERNAL_WALLET  provider_ref=NULL   captured_at=2026-09-26T14:22:03Z
id=0198fd22-…  kind=TOPUP   order_id=NULL        payer_user_id=0198f2c4-…  method=MFLOOS        amount_yer=50000   state=CAPTURED   idempotency_key=top_44ab…     provider=MFLOOS           provider_ref=MF-20260926-7781  provider_status_raw={"status":"success"}  captured_at=2026-09-26T09:03:44Z
id=0198fd45-…  kind=TOPUP   order_id=NULL        payer_user_id=0198f3b1-…  method=BANK_TRANSFER amount_yer=200000  state=AUTHORIZED idempotency_key=top_51cd…     provider=BANK            provider_ref=TRF-9921-HUTHA  verified_by=NULL  verified_at=NULL  (awaiting admin verification — BR-PAY-04)
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
