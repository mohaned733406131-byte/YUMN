---
document_id: DOC-API-016
title: API-NTF — Notifications, Preferences & Devices (FR-017)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-017, FR-001, FR-003, FR-007, FR-008, FR-012, FR-015, FR-016, FR-019, NFR-013, SEC-REQ-009, INT-REQ-003, INT-REQ-004, DATA-REQ-008, BR-NTF-01, BR-NTF-02, BR-NTF-03, BR-NTF-04, BR-NTF-05, BR-PLT-01, BR-PLT-02]
related_documents: [DOC-API-002, DOC-API-003, DOC-FR-017, DOC-BA-005, DOC-OVR-008]
---

# API-NTF — Notification Center, Preferences & Devices

**Group:** `API-NTF` · **FR-017** · **Endpoints:** `API-NTF-001…010` · **Base:** `/api/v1`

Channels: **SMS, WhatsApp, in-app, push — no email in v1** (`BR-NTF-01`, `GAP-03`); requesting email ⇒ 422 `CHANNEL_NOT_SUPPORTED`. Security notifications (OTP, login, password change, lockout) cannot be disabled (`BR-NTF-02`). Templates exist in ar/en and follow the user locale, Arabic default (`BR-NTF-04`, `C-24`). OTP delivery is SMS-primary with automatic WhatsApp failover (`BR-NTF-03`, `INT-REQ-003`). Delivery runs on BullMQ with 3 retries + exponential backoff + DLQ (`BR-PLT-01/02`). The in-app center is owner-scoped (`DATA-REQ-008`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-NTF-001 | `GET /notifications` | Any authenticated | In-app inbox (cursor feed): read/unread state, category, channel fan-out record | `?unreadOnly&category&limit&cursor` → `200 { items: [ { id, category: "SECURITY"\|"ORDER"\|"DELIVERY"\|"RETURN"\|"PROMOTION"\|"STORE_FOLLOW"\|"SYSTEM", title, body, severity, readAt?, channels: [ { channel: "SMS"\|"WHATSAPP"\|"IN_APP"\|"PUSH", status: "SENT"\|"FAILED", sentAt } ], deepLink, createdAt } ], page: {…} }` | `AUTH_INVALID`, `VALIDATION_ERROR` | FR-017, `BR-NTF-01`, `DATA-REQ-008` |
| API-NTF-002 | `GET /notifications/unread-count` | Any authenticated | Unread badge count (cheap read for all surfaces) | → `200 { total, byCategory: { ORDER: 3, PROMOTION: 1 } }` | `AUTH_INVALID` | FR-017 |
| API-NTF-003 | `POST /notifications/{id}/read` | Any authenticated (owner) | Mark one notification read (idempotent) | → `200 { id, readAt }` | `NOT_FOUND` (foreign ⇒ 404) | FR-017, `DATA-REQ-008` |
| API-NTF-004 | `POST /notifications/read-all` | Any authenticated | Mark the whole inbox read | `?category?` → `200 { marked: n }` | `AUTH_INVALID` | FR-017 |
| API-NTF-005 | `DELETE /notifications/{id}` | Any authenticated (owner) | Remove one in-app notification (does not unsend channel deliveries) | → `204` | `NOT_FOUND` | FR-017 |
| API-NTF-006 | `GET /notifications/preferences` | Any authenticated | Per-category, per-channel opt-in matrix | → `200 { categories: [ { category, security: true, channels: { SMS: true, WHATSAPP: true, IN_APP: true, PUSH: true } } ], emailSupported: false }` — security rows are returned with `locked: true` and immutable `true` | `AUTH_INVALID` | FR-017, `BR-NTF-01/02/05`, `GAP-03` |
| API-NTF-007 | `PUT /notifications/preferences` | Any authenticated | Update marketing/transactional opt-ins per channel | `{ updates: [ { category, channel, enabled } ] }` → `200 { categories: [...] }` — attempts to change a security category are rejected; `channel: "EMAIL"` rejected | `PREFERENCE_IMMUTABLE`, `CHANNEL_NOT_SUPPORTED`, `VALIDATION_ERROR` | FR-017, `BR-NTF-02/05`, `AC-FR017-01` |
| API-NTF-008 | `POST /devices` | Any authenticated | Register a push token for this device (login-time or first launch) | `{ token, platform: "ANDROID"\|"IOS"\|"WEB", deviceName? }` → `201 { deviceId, token, registeredAt }` — same token re-registered by another user detaches it from the previous owner | `DEVICE_TOKEN_INVALID`, `RATE_LIMITED`, `VALIDATION_ERROR` | FR-017, `SEC-REQ-009` |
| API-NTF-009 | `DELETE /devices/{token}` | Any authenticated (owner) | Unregister a push token (logout/device removal) — notifications target only active tokens | → `204` (idempotent) | `DEVICE_NOT_FOUND`, `NOT_FOUND` (foreign token) | FR-017, FR-003 |
| API-NTF-010 | `GET /devices` | Any authenticated | List the owner's registered devices/tokens with last-seen | → `200 { items: [ { deviceId, platform, deviceName, registeredAt, lastPushAt? } ] }` (≤5 devices, matches the session cap) | `AUTH_INVALID` | FR-017, FR-003, `BR-AUTH-06` |

## 2. Deep-Link Payload Contract

Every in-app notification (and every push payload) carries a structured `deepLink` so clients navigate deterministically on all four surfaces:

```json
{
  "deepLink": {
    "surface": "CUSTOMER" | "VENDOR" | "COURIER" | "ADMIN",
    "route": "/orders/{orderId}",
    "entity": { "type": "ORDER", "id": "…", "subOrderId": "…" },
    "action": "VIEW" | "CONFIRM" | "REVIEW" | "RESOLVE",
    "locale": "ar"
  }
}
```

| Rule | Detail |
|---|---|
| `surface` | which app/screen family opens; clients ignore notifications whose surface they do not serve |
| `route` | app-relative path only — never an absolute URL, never attacker-supplied (server-generated from templates) |
| `entity.type` | one of `ORDER`, `SUB_ORDER`, `RETURN`, `DISPUTE`, `DELIVERY`, `TOPUP`, `PAYOUT`, `KYC`, `TICKET`, `REVIEW`, `PRODUCT`, `STORE`, `COUPON`, `PROMOTION`, `SESSION`, `ACCOUNT` |
| `action` | coarse intent; the client re-fetches the entity (stale-state safe — a notification never embeds authoritative business state) |
| Push payload | `{ notification: { title, body }, data: { …deepLink, category, severity } }` — body already localized per `BR-NTF-04` |
| Security notices | carry `deepLink.action = "VIEW"` to the relevant security screen (e.g., `/account/sessions`) — never to an external URL |

## 3. Behavior Notes

- **Fan-out events** (FR-017): order/delivery/return/escrow-payout/KYC/store events trigger `b10.notification.delivery` jobs; per-event channel set = opted-in channels for non-security categories, **always all applicable channels** for security categories (`BR-NTF-02`, `AC-FR017-01`).
- **Failover** (`BR-NTF-03`, `AC-FR017-02`): SMS provider timeout/failure automatically retries the same template through WhatsApp (`INT-REQ-003`); both attempts appear in the `channels[]` delivery record.
- **No email** (`BR-NTF-01`, `GAP-03`, `AC-FR017-04`): no email field, channel or preference exists anywhere in this group; the response explicitly advertises `emailSupported: false`.
- **Follow notifications** (`BR-VND-05`): new-product/offer notifications are delivered only to customers following the store (`POST /stores/{id}/follow`) and only when their preferences allow the `PROMOTION`/`STORE_FOLLOW` categories.
- **Rate limiting** (`SEC-REQ-009`): notification-triggering endpoints (OTP request, top-up) carry stricter tiers; push-token registration is limited to 10/min/user.
- **Read state** is per in-app record only — SMS/WhatsApp/push deliveries are immutable and only logged (`INT-REQ-003` delivery receipts).

## 4. Pagination / Idempotency / Caching

`API-NTF-001` uses **cursor** pagination (default 20, max 50); `API-NTF-010` returns a bounded list (≤5). Read/mark-read/delete are idempotent. All responses `Cache-Control: no-store` except `API-NTF-002` (≤ 5 s micro-cache acceptable).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
