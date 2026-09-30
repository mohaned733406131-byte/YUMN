---
document_id: DOC-DBE-017
entity_id: DB-017
title: Entity notification (DB-017)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-017, SEC-REQ-002, DATA-REQ-002, INT-REQ-003, INT-REQ-004, INT-REQ-006]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-004, DOC-DB-005, DOC-BA-005]
---

# Entity: `notification` (DB-017) — table `b10.notification`

## Overview & purpose

The persisted record of every outbound message (B10, FR-017) across the four v1 channels — **SMS, WhatsApp, in-app, push; no email channel (BR-NTF-01, GAP-03)**. Each row carries the template key, localized payload, delivery status, read state, deep link and a dedup key so BullMQ retries and webhook redeliveries never spam the user (BR-PLT-02, INT-REQ-006). Security notifications (OTP, login, password change, lockout) are flagged and cannot be disabled by preferences (BR-NTF-02).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `user_id` | uuid | no | — | FK `fk_notification_user_id` → `b01.user` ON DELETE CASCADE | recipient (owner key) |
| `channel` | `notification_channel` | no | — | enum `SMS, WHATSAPP, IN_APP, PUSH` — **no `EMAIL` value exists** | BR-NTF-01 (GAP-03) |
| `category` | `notification_category` | no | `'ORDER'` | enum `SECURITY, ORDER, MARKETING, SYSTEM` | preference granularity (BR-NTF-05) |
| `template_key` | varchar(80) | no | — | `^[a-z]+(\.[a-z_]+)+$` app-side, e.g. `otp.login`, `order.delivered` | registered templates exist in ar + en (BR-NTF-04) |
| `locale` | `locale` | no | `'AR'` | enum `AR, EN` | follows user locale at enqueue time; Arabic default (C-24, BR-NTF-04) |
| `payload` | jsonb | no | `'{}'` | — | template variables only — **never contains OTP codes, passwords or tokens** (SEC-REQ-002 R4); order deep-link data, amounts as integers |
| `status` | `notification_status` | no | `'QUEUED'` | enum `QUEUED, SENT, FAILED` | queue → worker → provider (BR-PLT-01) |
| `read_at` | timestamptz | yes | null | — | in-app read marker (separate from delivery status) |
| `deep_link` | varchar(255) | yes | null | — | in-app route, e.g. `yumn://order/YM260926-8F3K2Q` (FR-017) |
| `dedup_key` | varchar(160) | yes | null | partial `UNIQUE(user_id, dedup_key)` | fan-out/retry idempotency (INT-REQ-006, BR-PLT-03) |
| `is_security` | boolean | no | `false` | `category='SECURITY' → is_security = true` (app + CHECK) | security notices cannot be opted out (BR-NTF-02) |
| `provider` | varchar(30) | yes | null | app enum: `SMS_PRIMARY, SMS_FAILOVER, WHATSAPP, FCM, APNS` | dual-provider failover evidence (INT-REQ-003) |
| `provider_message_id` | varchar(120) | yes | null | — | delivery receipt correlation (INT-REQ-003) |
| `failover_of` | uuid | yes | null | FK → `b10.notification` ON DELETE SET NULL | links WhatsApp fallback to the failed SMS (BR-NTF-03) |
| `failure_reason` | varchar(255) | yes | null | `status='FAILED' → failure_reason IS NOT NULL` (app) | drives retry/DLQ alerting (BR-PLT-02) |
| `sent_at` | timestamptz | yes | null | `status='SENT' → sent_at IS NOT NULL` (app) | — |
| `scheduled_for` | timestamptz | yes | null | — | delayed sends (marketing windows) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

**Supporting:** `b10.notification_preference(id, user_id, channel, category, enabled boolean, UNIQUE(user_id, channel, category))` — per-channel, per-category opt-out (BR-NTF-05); preferences are ignored for `SECURITY` (BR-NTF-02).

## Indexes

- PK `id`
- `idx_notification_user_created` on `(user_id, created_at DESC)` — in-app inbox (FR-017)
- `idx_notification_queue` on `(created_at)` WHERE `status='QUEUED'` — sender worker drain (BR-PLT-01)
- `uq_notification_user_dedup` partial UNIQUE on `(user_id, dedup_key)` WHERE `dedup_key IS NOT NULL`
- `idx_notification_template_created` on `(template_key, created_at)` — template delivery stats
- `notification_preference`: `uq_notification_pref_user_channel_category`

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `notification` | `user` (DB-001) | N:1 | `fk_notification_user_id` | CASCADE |
| `notification` (self) | `notification` | N:0..1 | `fk_notification_failover_of` | SET NULL |
| `notification_preference` | `user` | N:1 | `fk_notification_preference_user_id` | CASCADE |

Notifications reference orders/wallets only through `payload`/`deep_link` (no FK) — a template change must never break historical rows (DATA-REQ-005).

## Invariants & business rules enforced

**DB-enforced**

1. Channel enum contains exactly `SMS, WHATSAPP, IN_APP, PUSH` — **email is structurally impossible** (BR-NTF-01, GAP-03).
2. Status enum (`QUEUED/SENT/FAILED`); `sent_at`/`failure_reason` consistency CHECKs (app-verified at transition).
3. One row per `(user_id, dedup_key)` → duplicate enqueues collapse (INT-REQ-006).
4. `SECURITY` category forces `is_security=true`.

**App-enforced**

1. Preferences consulted at enqueue: marketing/other categories skipped when disabled for that channel (BR-NTF-05); **security notifications bypass preferences** (BR-NTF-02).
2. Template resolution renders ar + en from `template_key` + `locale` (BR-NTF-04, C-24); language follows user locale with Arabic default.
3. OTP delivery: SMS primary, automatic failover to WhatsApp on provider timeout/failure — creates the linked fallback row (`failover_of`) (BR-NTF-03, INT-REQ-003).
4. Worker claims `QUEUED` rows idempotently (status guard), retries 3× with backoff then DLQ + alert (BR-PLT-02); delivery receipts update `provider_message_id`/`sent_at` idempotently.
5. **Payload minimization (DATA-REQ-002):** payload contains only template variables — no OTP code, no password, no full phone; logs exclude secrets (SEC-REQ-002 R4).
6. Retention: delivery records follow the operational retention in `16-data/`; in-app unread state cleared on read (`read_at`).

## Example rows

```text
id=0198ff100-…  user_id=0198f2c4-…  channel=SMS       category=SECURITY  template_key=otp.login       locale=AR  payload={"ttl":"5m","attempts":3}  status=SENT     read_at=NULL  deep_link=NULL  dedup_key=otp:0198f2c4:20260926T1400  is_security=true  provider=SMS_PRIMARY  provider_message_id=SP-99121  sent_at=2026-09-26T14:00:02Z
id=0198ff110-…  user_id=0198f2c4-…  channel=WHATSAPP  category=SECURITY  template_key=otp.login       locale=AR  payload={"ttl":"5m","attempts":3}  status=SENT     read_at=NULL  dedup_key=otp:0198f2c4:20260926T1400b is_security=true  provider=WHATSAPP  provider_message_id=WA-4417  failover_of=0198ff100-…  sent_at=2026-09-26T14:00:31Z
id=0198ff120-…  user_id=0198f2c4-…  channel=IN_APP    category=ORDER     template_key=order.delivered locale=AR  payload={"order_no":"YM260926-8F3K2Q","total_yer":215750}  status=QUEUED  read_at=NULL  deep_link=yumn://order/YM260926-8F3K2Q  dedup_key=order.delivered:0198fc01  is_security=false
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
