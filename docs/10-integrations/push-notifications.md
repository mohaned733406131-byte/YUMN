---
document_id: DOC-INT-006
title: Push Notifications — FCM & APNs Integration
category: 10-integrations
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-27
author: analysis-agent
source_of_truth: false
related_requirements: [FR-017, FR-003, INT-REQ-004, INT-REQ-008, NFR-013]
related_documents: [DOC-INT-000, DOC-INT-001, DOC-INT-005, DOC-IR-004, DOC-FR-017, DOC-BA-005]
---

# Push Notifications — FCM + APNs (`FR-017`)

Push delivery for the React Native apps (Android via **FCM**, iOS via **APNs**) behind a single `PushPort` so platform specifics never leak into notification logic (`INT-REQ-008` pattern applied to a first-party channel). Endpoint/payload contracts are specified in `07-api/endpoints/notifications.md`; this file owns token lifecycle, fan-out, staleness, and fallback behavior.

## 1. Architecture

```text
domain event (order · delivery · return · escrow · KYC · store)
   → notification rules engine (category, channel set, locale, preferences)
   → BullMQ job  b10.notification.delivery          (BR-PLT-01, 3× retry → DLQ, BR-PLT-02)
   → PushPort.send(deviceTokens[], payload)
        ├─ FcmAdapter  (service account, env S-08)
        └─ ApnsAdapter (.p8 key, env S-08, HTTP/2)
   ← receipt/token-invalid results feed token lifecycle (§2)
```

- Queue-based: pushes are best-effort fan-out, never inline with order/payment transactions.
- Credentials from environment only (`SEC-REQ-007` inventory S-08); never logged.
- Normalized errors: `TIMEOUT / REJECTED / PROVIDER_DOWN / SIGNATURE_INVALID` (`INT-REQ-008`).

## 2. Device Token Lifecycle (`FR-017`)

| Event | Behavior |
|---|---|
| App login / permission grant | Client registers token with device platform tag (android/ios), app version, locale → `device_token` row bound to `user_id` (`DATA-REQ-008` owner scope) |
| Re-registration (token refresh) | New token upserts the old entry for the same device; old token retired |
| Logout on device | **Unregister** the token for that device only (other sessions keep theirs) |
| Account deletion (`DATA-REQ-003`) | All tokens for the user purged |
| Send result: invalid/unregistered token | Adapter reports `NOT_FOUND` → token marked stale immediately; **never retried** |
| Send result: transient failure | Retry per queue policy (3× backoff) while token still active |
| Targeting rule | Notifications target **only active (non-stale) tokens** (`FR-017`) |
| Cap (design, `INFERENCE`) | ≤ 5 tokens per user (mirrors the 5-session device cap `BR-AUTH-06` for consistency) |

## 3. Payload Contract (deep links)

Canonical contract lives in `07-api/endpoints/notifications.md`; the push payload must contain:

| Field | Content | Rule |
|---|---|---|
| `title` / `body` | Localized per `BR-NTF-04` — ar default, en parity, user locale | no hardcoded strings (`BR-PLT-05`, `C-24`) |
| `data.type` | Notification category (`ORDER_STATUS`, `DELIVERY_CODE`, `SECURITY`, `PROMO`, …) | drives deep-link routing + quiet-hours logic |
| `data.ref` | Entity reference (order id, topup id) — **opaque IDs only** | no PII in payload (`INFERENCE`, `SEC-REQ-006` R5 discipline) |
| `data.deepLink` | App route per the 07-api endpoint spec (e.g., order detail screen) | validated against an allowlist of routes — arbitrary URLs never accepted |
| `data.correlationId` | Correlation ID | ties to logs/metrics (`NFR-014`) |
| `badge` / `sound` | Badge increment for in-app unread; sound per category | badge count mirrors in-app unread state (§4) |

**Payload hygiene:** iOS `mutable-content`/notification-service extension may localize; preview text must not contain secrets, full phone numbers, or OTP codes except in the authentication-class message where the code *is* the content (FCM/APNs transport is TLS, `SEC-REQ-006`).

## 4. Topics, Fan-Out & Badge/Read State

| Aspect | Design |
|---|---|
| Fan-out | Per-user targeting for personal events (order, delivery, security); **topic/fan-out groups** used only for platform-wide or store-follower broadcasts (`BR-VND-05` follower offers) |
| Topic naming | Namespaced opaque IDs (`store.{id}.followers`, `platform.announcements`) — no phone numbers in topic names |
| Read state authority | The **in-app notification center is the source of truth** for read/unread (`FR-017`); push is a transient pointer |
| Badge | Derived from in-app unread count; push increments optimistically, server reconciles on next open |
| Deduplication | Same entity+category within a short window collapses to one push (`INFERENCE`) to avoid spam |
| Ordering | No global ordering guarantee across providers; per-entity ordering approximated by queue serialization per user (`INFERENCE`) |

## 5. Token Staleness Handling

1. Adapter translates provider feedback into `INVALID_TOKEN` vs `TRANSIENT`.
2. `INVALID_TOKEN` → mark stale in the same transaction as the send-result write; subsequent fan-outs skip it.
3. Background sweep (daily, `INFERENCE`) prunes tokens with no successful send/refresh in 60 days — conservative window avoids killing valid iOS tokens.
4. Metrics: `push_invalid_token_total` by platform; a spike indicates app defect or credential problem → alert (`INT-REQ-007`).

## 6. Quiet Hours & Preferences

| Rule | Behavior | Canon / evidence |
|---|---|---|
| Marketing/promo pushes | Respected per-channel opt-out; **quiet hours** (design: 21:00–08:00 local, `INFERENCE`) defer non-urgent promo to the morning | `BR-NTF-05`; quiet-hours value not in canon |
| Transactional (order, delivery, payout) | Sent regardless of quiet hours | `FR-017` transactional classification (`INFERENCE` split) |
| Security (login, lockout, password change, family-revocation alert) | **Always delivered, never deferred, never disable-able** | `BR-NTF-02` |
| Locale | Follows user locale at send time | `BR-NTF-04`, `C-24` |
| In-app mirror | Every push notification is also recorded in the in-app center (`FR-017`) — push failure never loses the message | `FR-017` |

## 7. Fallback Chain

| Failure | Fallback | Canon |
|---|---|---|
| FCM/APNs outage or reject | Notification **remains in the in-app center**; no push retry storm | `FR-017`, `NFR-007` |
| Security notice where immediacy matters | In-app + (optionally) SMS — SMS is the universal channel for security-class messages | `BR-NTF-02`, `BR-NTF-03` |
| OTP | **Never push** — OTP flows are SMS (primary) / WhatsApp (failover) only | `BR-NTF-03`, `DOC-INT-005` §1 |
| Token invalid | Silent skip + prune; user still sees the message in-app on next open | §5 |
| Persistent adapter failure | 3 retries → DLQ → alert (never drops below visibility) | `BR-PLT-02`, `BR-PLT-01` |

## 8. Environments & Testing

| Aspect | Design |
|---|---|
| FCM | Separate service account per environment; sandbox project for staging (`INFERENCE`) |
| APNs | APNs **sandbox** topic for staging, production topic for prod; `.p8` key rotation per Apple cadence (`secrets-management.md` S-08) |
| E2E | Real-device push verification via the test-device lab (`DEP-12`) |
| Contract tests | Mock push adapter in CI so notification logic is testable without network (`NFR-010`) |

## 9. Verification

| Test | Assertion |
|---|---|
| Token lifecycle | register → refresh → stale-token skip → unregister on logout → purge on account deletion (`FR-017`) |
| Deep link | payload routes to the correct app screen per 07-api spec; unknown routes rejected |
| Preference matrix | promo opt-out / quiet hours / security-always (`BR-NTF-02`, `BR-NTF-05`) |
| Localization | ar/en payloads per locale (`AC-FR017-03` pattern) |
| Badge | in-app unread count and badge converge after open |
| Failure | provider outage → message present in in-app center; DLQ alert after retries |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | Pipeline queue name corrected: `b10.notification.send` → `b10.notification.delivery` per the canonical register | `REC-06`/`TD-07` pay-down |


