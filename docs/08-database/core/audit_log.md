---
document_id: DOC-DBE-018
entity_id: DB-018
title: Entity audit_log (DB-018)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-020, SEC-REQ-010, SEC-REQ-002, DATA-REQ-003, DATA-REQ-007, NFR-019]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005, DOC-OVR-007]
---

# Entity: `audit_log` (DB-018) — table `b13.audit_log`

## Overview & purpose

The **append-only, tamper-evident audit trail** of privileged and money actions (FR-020, SEC-REQ-010, BR-PLT-06): who did what, to which entity, with before/after state, from where, and in which correlation context. Nothing updates or deletes rows — including administrators (DATA-REQ-007) — and a SHA-256 hash chain makes silent tampering detectable (SEC-REQ-010). Retention ≥ 5 years (DATA-REQ-003 R4, NFR-019).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK (composite `(id, created_at)` — partitioned) | UUID v7 |
| `seq` | bigint | no | allocated from `b13.audit_chain` | `uq_audit_log_seq` UNIQUE | **global monotonic sequence** — chain order (SEC-REQ-010) |
| `created_at` | timestamptz | no | `now()` | partition key | append-only: **no `updated_at`, no mutable columns** |
| `actor_type` | `audit_actor_type` | no | `'USER'` | enum `USER, SYSTEM` | `SYSTEM` = background jobs/webhooks (ACT-07) |
| `actor_user_id` | uuid | yes | null | FK `fk_audit_log_actor_user_id` → `b01.user` ON DELETE RESTRICT; `actor_type='USER' → actor_user_id IS NOT NULL` (app) | NULL for `SYSTEM` (ACT-07) |
| `actor_role` | `role` | yes | null | enum `CUSTOMER, VENDOR, COURIER, ADMIN, SUPER_ADMIN, MODERATOR` | role **in effect** at action time (6 login roles — FR-002); NULL for SYSTEM |
| `actor_label` | varchar(80) | yes | null | — | human label for SYSTEM actions, e.g. `escrow-release-job` |
| `action` | varchar(80) | no | — | `<module>.<verb>` pattern, e.g. `order.state_change`, `wallet.freeze`, `kyc.decision` | stable action vocabulary for filtered search |
| `module` | char(3) | no | — | enum `b01…b13` | owning block of the touched entity (C-21 alignment) |
| `entity_type` | varchar(60) | no | — | e.g. `order`, `wallet_transaction`, `store` | — |
| `entity_id` | uuid | yes | null | — | NULL for platform-level actions (settings changes) |
| `before` | jsonb | yes | null | — | state snapshot prior to the action |
| `after` | jsonb | yes | null | — | state snapshot after; at least one of `before`/`after` present (app + CHECK) |
| `outcome` | `audit_outcome` | no | `'SUCCESS'` | enum `SUCCESS, DENIED, ERROR` | failed authorization attempts recorded too (SEC-REQ-004) |
| `ip` | inet | yes | null | — | client address (BR-PLT-06) |
| `user_agent` | varchar(255) | yes | null | — | client agent (BR-PLT-06) |
| `correlation_id` | uuid | no | — | — | request/trace id joining logs & metrics (NFR-014) |
| `reason` | varchar(255) | yes | null | — | required app-side for decisions (KYC rejection, refund approval, dispute resolution — BR-RET-06) |
| `prev_hash` | bytea(32) | no | — | — | hash of the previous `seq` entry (chain head for `seq=1`) |
| `entry_hash` | bytea(32) | no | — | `entry_hash = SHA256(prev_hash ‖ canonical(fields))` (app) | tamper evidence (SEC-REQ-010) |

**PII note:** snapshots contain column values **as stored** — phone/address fields are ciphertext (SEC-REQ-002), so an audit export never reveals readable PII. Audit rows are excluded from account-deletion erasure (retained ≥ 5 y, DATA-REQ-003 R4).

**Chain head:** `b13.audit_chain(id SMALLINT PK CHECK (id = 1), last_seq BIGINT, last_hash BYTEA, updated_at)` — row-locked while appending to serialize `seq` allocation (audit volume is far below order/ledger write rates, so contention is negligible; load test asserts this under NFR-003).

## Indexes

| Index | Type | Backs |
|---|---|---|
| PK `(id, created_at)` | btree (partitioned) | — |
| `uq_audit_log_seq` | UNIQUE | chain ordering (SEC-REQ-010) |
| `idx_audit_entity` on `(entity_type, entity_id, created_at DESC)` | compound (partitioned) | "full history of this order/wallet/store" (FR-020) |
| `idx_audit_actor_created` on `(actor_user_id, created_at DESC)` WHERE `actor_user_id IS NOT NULL` | partial (partitioned) | per-admin action review |
| `idx_audit_action_created` on `(action, created_at DESC)` | compound (partitioned) | filtered searches (`wallet.freeze`, `kyc.decision`) |
| `idx_audit_correlation_id` on `(correlation_id)` | btree (partitioned) | trace ↔ audit join (NFR-014) |

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `audit_log` | `user` (actor) | N:0..1 | `fk_audit_log_actor_user_id` | RESTRICT — audit survives account deletion |
| `audit_log` | `audit_chain` (head, logical) | N:1 ordering | app-enforced via `prev_hash` | n/a — chain never broken |

No FKs to audited entities (`entity_type/entity_id` polymorph): audit rows must outlive the entity and its module's schema changes (DATA-REQ-005).

## Invariants & business rules enforced

**DB-enforced**

1. **Append-only privileges:** application roles receive `SELECT, INSERT` only — `UPDATE`, `DELETE`, `TRUNCATE` are revoked (DATA-REQ-007, SEC-REQ-010). Even Super Admin cannot edit the trail through any API path.
2. Unique `seq`; `actor_type/actor_user_id` consistency; at least one of `before`/`after` (app + CHECK); outcome enum.
3. Partitioned by `created_at` — retention drops/archives whole partitions, never row-deletes inside the ≥5-year window (DATA-REQ-003, NFR-019).

**App-enforced**

1. **Who is audited:** every privileged action (role/permission change, KYC decision, refund/dispute resolution, store suspension, settings change, wallet freeze) and every money action (top-up verification, capture, release, payout, adjustment) writes exactly one row in the same transaction as the action (BR-PLT-06, SEC-REQ-010).
2. Actor context: user id + role in effect; `System` jobs log `actor_type='SYSTEM'` with `actor_label` (ACT-07; System has no login role — DOC-DB-005 §2.3).
3. **Hash chain:** nightly verification recomputes `entry_hash` across `seq` order; any mismatch pages security (SEC-REQ-010). Chain writes are serialized via the `audit_chain` head row inside the same transaction.
4. Read access per role scope: admins platform-scope, vendors own-store scope (via entity join), moderators scoped, System write-only (DOC-OVR-007 permission table).
5. Deletion/anonymization runs append an evidence row with actor, scope, row counts and timestamp (DATA-REQ-003 R5).

## Example rows

```text
seq=10412  id=0198ff200-…(2026-09)  actor_type=USER   actor_user_id=0198f701-owner…  actor_role=VENDOR  action=order.state_change  module=b06  entity_type=sub_order  entity_id=0198fc10-…  before={"state":"CONFIRMED"}  after={"state":"PROCESSING"}  outcome=SUCCESS  ip=41.86.x.x  correlation_id=0198ff1f0-…  prev_hash=0x7a31…  entry_hash=0x99c0…  created_at=2026-09-26T14:35:10Z
seq=10413  id=0198ff210-…(2026-09)  actor_type=SYSTEM  actor_user_id=NULL  actor_label=escrow-release-job  action=escrow.release  module=b07  entity_type=escrow  entity_id=0198ff91-…  before={"state":"HELD"}  after={"state":"RELEASED","commission_amount_yer":8850}  outcome=SUCCESS  correlation_id=0198ff1f8-…  prev_hash=0x99c0…  entry_hash=0x1b47…  created_at=2026-09-28T16:31:02Z
seq=10414  id=0198ff220-…(2026-09)  actor_type=USER   actor_user_id=0198mod-…  actor_role=MODERATOR  action=review.hide  module=b02  entity_type=review  entity_id=0198ff030-…  before={"is_hidden":false}  after={"is_hidden":true}  outcome=SUCCESS  reason=inappropriate content  ip=41.86.x.y  correlation_id=0198ff205-…  prev_hash=0x1b47…  entry_hash=0x5d02…  created_at=2026-09-24T11:00:00Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
