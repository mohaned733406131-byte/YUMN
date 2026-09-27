---
document_id: DOC-DBE-001
entity_id: DB-001
title: Entity user (DB-001)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-002, FR-003, SEC-REQ-002, DATA-REQ-002, DATA-REQ-003]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-005, DOC-BA-005, DOC-OVR-007]
---

# Entity: `user` (DB-001) — table `b01.user`

## Overview & purpose

The account record for every human actor of yumn — Customer (ACT-01), Vendor (ACT-02), Courier (ACT-03), Admin/Moderator (roles) — and the anchor for ownership of wallets, orders, addresses and sessions. Realizes FR-001 (identity/auth), FR-002 (roles), FR-003 (profile, deletion, ≤5 sessions). Phone is the **primary identifier and unique** (BR-AUTH-01, `C-06`); passwords are bcrypt cost-12 hashes and may be absent for OTP-only service-created accounts (BR-AUTH-02); email is optional and never used for login (BR-AUTH-08). PII minimization (DATA-REQ-002) and deletion/anonymization (DATA-REQ-003) shape the column set: nothing is stored that the platform does not need.

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 (DOC-DB-001 §2) |
| `phone_ciphertext` | bytea | no | — | `ck_user_phone_phone_ciphertext_present` | AES-256-GCM ciphertext of the phone (SEC-REQ-002 R3); key held outside DB (SEC-REQ-007) |
| `phone_nonce` | bytea(12) | no | — | — | GCM nonce, stored beside ciphertext |
| `phone_hash` | bytea(32) | no | — | `uq_user_phone_hash` | HMAC-SHA256(normalized phone, external pepper) — login lookup + uniqueness (BR-AUTH-01) |
| `password_hash` | text | yes | null | — | bcrypt cost 12 (BR-AUTH-02); `NULL` for OTP-only accounts (e.g., courier provisioned by admin) |
| `email_ciphertext` | bytea | yes | null | `ck_user_email_optional` | optional (BR-AUTH-08) |
| `email_hash` | bytea(32) | yes | null | `uq_user_email_hash` (partial) | uniqueness of provided emails |
| `email_verified_at` | timestamptz | yes | null | — | verification required if present (BR-AUTH-08) |
| `full_name_ciphertext` | bytea | yes | null | — | display name = PII (SEC-REQ-002) |
| `status` | `user_status` | no | `'ACTIVE'` | enum: `ACTIVE, SUSPENDED, DELETED` | suspended = login blocked; deleted = PII erased/anonymized (DATA-REQ-003 R2) |
| `default_locale` | `locale` | no | `'AR'` | enum `AR, EN` | Arabic-first (`C-24`) |
| `phone_verified_at` | timestamptz | no | — | — | set on successful registration OTP (SEC-REQ-001) |
| `failed_login_count` | smallint | no | `0` | `>= 0` | 5 failures → 15-min lock (BR-AUTH-04) |
| `locked_until` | timestamptz | yes | null | — | lock expiry (BR-AUTH-04) |
| `last_login_at` | timestamptz | yes | null | — | informational + session management |
| `deletion_requested_at` | timestamptz | yes | null | — | starts DATA-REQ-003 deletion workflow |
| `anonymized_at` | timestamptz | yes | null | `anonymized_at > deletion_requested_at` | PII crypto-shredded/zeroed; row retained for financial history |
| `created_at` | timestamptz | no | `now()` | — | — |
| `updated_at` | timestamptz | no | `now()` | trigger T1 | — |
| `deleted_at` | timestamptz | yes | null | — | soft-delete marker aligned with `status='DELETED'` |

Roles are **not** an array column — they live in `b01.user_role(user_id, role, granted_by, granted_at)` with `UNIQUE(user_id, role)` so grants are FK-integrity-checked, auditable (BR-PLT-06) and RBAC-resolvable in one index lookup (FR-002).

## Indexes

- `uq_user_phone_hash` on `phone_hash` (UNIQUE) — login + registration uniqueness
- `uq_user_email_hash` on `email_hash` WHERE `email_hash IS NOT NULL` (UNIQUE partial)
- `idx_user_status_created_at` on `(status, created_at DESC)` — admin user lists
- PK `id`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `user_role` | `user` | N:1 | `fk_user_role_user_id` | CASCADE |
| `session` | `user` | N:1 | `fk_session_user_id` | CASCADE |
| `otp_challenge` | `user` | N:1 | `fk_otp_challenge_user_id` | CASCADE |
| `address` (DB-002) | `user` | N:1 | `fk_address_user_id` | CASCADE |
| `wallet` (DB-010) | `user` | 1:1 | `fk_wallet_user_id` | RESTRICT |
| `store` (DB-003) | `user` | 0..1:1 | `fk_store_owner_user_id` | RESTRICT |
| `order` (DB-008) | `user` | N:1 | `fk_order_buyer_user_id` | RESTRICT |
| `review` (DB-015), `notification` (DB-017), `audit_log` (DB-018) | `user` | N:0..1 | `fk_review_user_id`, `fk_notification_user_id`, `fk_audit_log_actor_user_id` | CASCADE / CASCADE / RESTRICT |

## Invariants & business rules enforced

**DB-enforced**

1. `phone_hash` unique → phone unique across the platform (BR-AUTH-01).
2. Ciphertext + hash columns are `NOT NULL` (`ck_user_phone_phone_ciphertext_present`) — no plaintext phone column exists anywhere (SEC-REQ-002 AC-SR002-03).
3. `user_status` enum restricts values; `failed_login_count >= 0`.
4. `user_role.role` restricted to the 6 login roles; `System` (ACT-07) is **not** a role — system actions write `audit_log.actor_type='SYSTEM'` with `actor_user_id NULL` (DOC-DB-005 §2.3).

**App-enforced (tests cover them)**

1. Format `^7[0-9]{8}$` checked **before encryption** (plaintext never reaches the DB) — BR-AUTH-01.
2. Password policy ≥8 chars w/ upper+lower+digit, bcrypt cost 12 (BR-AUTH-02).
3. Max 5 active sessions: count query + oldest-revocation (BR-AUTH-06); `session` uniqueness per device backs it.
4. 5 failed logins → `locked_until = now() + 15 min`, lock events audited (BR-AUTH-04); password reset revokes all sessions (BR-AUTH-07).
5. Account deletion: anonymize PII, keep FK-reachable financial rows ≥5 years (DATA-REQ-003 R2/R3); `anonymized_at` evidence entry written (DATA-REQ-003 R5).

**Canon note:** SEC-REQ-002 requires phone ciphertext in any raw dump; storing the phone as an equality-indexable plaintext column would satisfy uniqueness but violate that requirement — hence the cipher + HMAC-hash split (interpretation recorded here, not a change to canon).

## Example rows

```text
id=0198f2c4-…-v7   phone_hash=0x8f3a…  password_hash=$2b$12$…  status=ACTIVE  default_locale=AR  phone_verified_at=2026-09-14T10:12:03Z  created_at=2026-09-14T10:11:58Z
id=0198f3b1-…-v7   phone_hash=0x1c09…  password_hash=NULL      status=ACTIVE  default_locale=AR  phone_verified_at=2026-09-20T08:00:11Z  created_at=2026-09-20T07:59:50Z   (courier, OTP-only)
id=0198f4d9-…-v7   phone_hash=0x77be…  password_hash=$2b$12$…  status=DELETED default_locale=AR  deletion_requested_at=2026-09-25T12:00:00Z  anonymized_at=2026-09-25T12:00:41Z
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
