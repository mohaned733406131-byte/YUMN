---
document_id: DOC-API-014
title: API-SHP — Shipping, Courier Work & Delivery Confirmation (FR-015)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-015, FR-011, FR-012, FR-016, FR-017, FR-020, SEC-REQ-011, INT-REQ-005, BR-SHP-01, BR-SHP-02, BR-SHP-03, BR-SHP-04, BR-SHP-05, BR-SHP-06, BR-SHP-07, BR-ORD-08, BR-ORD-09]
related_documents: [DOC-API-002, DOC-API-003, DOC-FR-015, DOC-SA-010, DOC-BA-005, DOC-OVR-008]
---

# API-SHP — Shipping, Courier Work & Delivery Confirmation

**Group:** `API-SHP` · **FR-015** · **Endpoints:** `API-SHP-001…016` · **Base:** `/api/v1`

Domestic Yemen fulfillment only (`C-17`). Assignment is offered to eligible couriers in the same zone with **first-accept wins** via optimistic locking (`BR-SHP-04`). Flow: `READY_FOR_PICKUP → ASSIGNED → PICKED_UP → IN_TRANSIT → OUT_FOR_DELIVERY → DELIVERED`. At `OUT_FOR_DELIVERY` a **6-digit code** is issued to the buyer (`BR-SHP-02`); courier entry verifies it — 1–2 failures show remaining attempts, the 3rd failure locks confirmation for 24 hours and auto-creates a support ticket (`BR-SHP-03`, `C-16`). **No endpoint requests or stores GPS/location coordinates** (`BR-SHP-05`, `C-16`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-SHP-001 | `GET /deliveries/available` | `COURIER` | Open delivery offers for the courier's zone (cursor feed) | `?zone&limit&cursor` → `200 { items: [ { deliveryId, subOrderId, zoneSlug, pickupPoint: { governorate, district, line1 }, dropoffDistrict, weightBand, offeredFee, offerVersion, deadlineAt } ], page: {…} }` — no GPS, no live customer position | `NOT_FOUND` (no offers ⇒ empty items), `COURIER_OFFLINE`, `VALIDATION_ERROR` | FR-015, `BR-SHP-04/05`, `C-16`, `UC-025` |
| API-SHP-002 | `GET /deliveries/mine` | `COURIER` | Own job list across states (assigned/picked-up/in-transit/out-for-delivery) (cursor feed) | `?state&limit&cursor` → `200 { items: [ { deliveryId, orderId, storeName, state, dropoffDistrict, offeredFee, nextAction } ], page: {…} }` | `VALIDATION_ERROR` | FR-015, `BR-ORD-09`, `UC-025` |
| API-SHP-003 | `GET /deliveries/{id}` | `COURIER` (assignee), `ADMIN` | Delivery detail: pickup/drop-off addresses, package notes, attempt count, code status | → `200 { deliveryId, orderId, subOrderId, state, pickup, dropoff: { governorate, district, line1, recipientNameMasked, recipientPhoneMasked }, weightKg?, attempts: [ { at, outcome, reason? } ], code: { issuedAt, attemptsUsed, lockedUntil? }, proof: { photoUrl?, verifiedAt? } }` | `NOT_FOUND`, `TIMELINE_ACCESS_DENIED` | FR-015, `BR-SHP-06/07`, `BR-ORD-09` |
| API-SHP-004 | `POST /deliveries/{id}/accept` | `COURIER` | Accept an offer — `READY_FOR_PICKUP → ASSIGNED` (first accept wins) | `{ offerVersion }` → `200 { deliveryId, state: "ASSIGNED", version, assignedAt }` — optimistic check on `offerVersion`; losing race gets a conflict | `ASSIGNED_ELSEWHERE`, `STATE_CONFLICT`, `COURIER_OFFLINE`, `NOT_FOUND` | FR-015, `BR-SHP-04`, `AC-FR015-03`, `UC-026` |
| API-SHP-005 | `POST /deliveries/{id}/release` | `COURIER`, `ADMIN` | Release an assignment — `ASSIGNED → READY_FOR_PICKUP` (returns to the offer pool) | `{ reason }` → `200 { state: "READY_FOR_PICKUP", version, historyEntry }` | `STATE_CONFLICT`, `REASON_REQUIRED`, `NOT_FOUND` | FR-015, `DOC-SA-010` §2 |
| API-SHP-006 | `GET /deliveries/{id}/pickup` | `COURIER` | Pickup screen data: address, package notes, expected weight band | → `200 { deliveryId, pickup: {…}, package: { weightBand, notes? }, expectedWeightKg? }` | `NOT_FOUND` | FR-015, `UC-027` |
| API-SHP-007 | `POST /deliveries/{id}/pickup` | `COURIER` | Confirm physical pickup — `ASSIGNED → PICKED_UP` | `{ note? }` → `200 { state: "PICKED_UP", version, historyEntry, pickedUpAt }` | `STATE_CONFLICT`, `NOT_FOUND` | FR-015, `DOC-SA-010` §2, `UC-027` |
| API-SHP-008 | `POST /deliveries/{id}/transit` | `COURIER` | Departure scan — `PICKED_UP → IN_TRANSIT` (also the return-to-transit target after a failed attempt) | `{ hubNote? }` → `200 { state: "IN_TRANSIT", version, historyEntry }` | `STATE_CONFLICT`, `NOT_FOUND` | FR-015, `DOC-SA-010` §2, `UC-028` |
| API-SHP-009 | `POST /deliveries/{id}/out-for-delivery` | `COURIER` | Final leg — `IN_TRANSIT → OUT_FOR_DELIVERY`; **6-digit delivery code issued to the buyer** via SMS/WhatsApp/in-app | → `200 { state: "OUT_FOR_DELIVERY", version, codeIssued: true, codeDeliveryChannels: ["SMS","WHATSAPP","IN_APP"], buyerCodeMasked: "**4821" }` — the full code is only visible to the buyer | `STATE_CONFLICT`, `NOT_FOUND` | FR-015, FR-017, `BR-SHP-02`, `BR-NTF-03`, `UC-028` |
| API-SHP-010 | `POST /deliveries/{id}/code` | `COURIER` | Verify the buyer's 6-digit code — `OUT_FOR_DELIVERY → DELIVERED` (escrow hold starts) | `{ code }` → `200 { state: "DELIVERED", version, deliveredAt, proof: { code: true, courierId, verifiedAt } }` — duplicate successful submission is idempotent (first success wins) | `CODE_INVALID` (with `attemptsRemaining`), `CODE_ATTEMPTS_EXCEEDED` (3rd failure ⇒ 24 h lock + ticket), `CODE_LOCKED`, `CODE_ALREADY_VERIFIED`, `STATE_CONFLICT`, `VALIDATION_ERROR`, `NOT_FOUND` | FR-015, `BR-SHP-03`, `BR-ORD-08`, `C-16`, `AC-FR015-01/02`, `UC-030` |
| API-SHP-011 | `POST /deliveries/{id}/failed-attempt` | `COURIER` | Record a failed delivery attempt — `OUT_FOR_DELIVERY → IN_TRANSIT`, attempt logged | `{ reasonCode, note?, photoFileId? }` → `200 { state: "IN_TRANSIT", attemptNumber, remainingBeforeEscalation }` — 3rd failed attempt ⇒ escalation to admin review with full timeline (`DELIVERY_ATTEMPTS_EXCEEDED`) | `DELIVERY_ATTEMPTS_EXCEEDED`, `STATE_CONFLICT`, `REASON_REQUIRED`, `VALIDATION_ERROR`, `NOT_FOUND` | FR-015, `BR-SHP-06`, `DOC-SA-010` §2, `UC-029` |
| API-SHP-012 | `POST /deliveries/{id}/proof-photo` | `COURIER` | Attach the **optional** delivery photo (never required) | `multipart { file }` → `201 { photoUrl, uploadedAt }` — ≤5 MB jpg/png/webp, EXIF stripped, scanned | `PAYLOAD_TOO_LARGE`, `UNSUPPORTED_MEDIA_TYPE`, `FILE_SCAN_FAILED`, `NOT_FOUND` | FR-015, `BR-SHP-07`, SEC-REQ-011, `api-conventions.md` §10 |
| API-SHP-013 | `GET /orders/{id}/delivery-code` | `CUSTOMER` (order owner) | Read the buyer's own delivery code while the order is `OUT_FOR_DELIVERY` (in-app issuance channel) | → `200 { code: "482196", issuedAt, expiresAt?, attemptsRemaining }` — code hidden again after successful verification | `NOT_FOUND` (not issued / not owner), `STATE_CONFLICT` (already delivered) | FR-015, FR-017, `BR-SHP-02`, `C-16`, `UC-013` |
| API-SHP-014 | `GET /courier/profile` | `COURIER` | Own courier profile: zones served, availability, delivery stats | → `200 { displayName, phoneMasked, zones: [...], availability: "ONLINE"\|"OFFLINE", stats: { activeDeliveries, completed, successRatePercent } }` | `AUTH_INVALID` | FR-015, FR-002 |
| API-SHP-015 | `PUT /courier/profile` | `COURIER` | Update display name and served zones (domestic only) | `{ displayName?, zones? }` → `200 { …profile }` | `VALIDATION_ERROR`, `NO_SHIPPING_ZONE` (non-domestic zone) | FR-015, `C-17` |
| API-SHP-016 | `PUT /courier/availability` | `COURIER` | Go online/offline — offline couriers receive no offers and cannot accept | `{ availability: "ONLINE"\|"OFFLINE" }` → `200 { availability, changedAt }` | `VALIDATION_ERROR`, `STATE_CONFLICT` (offline while holding active jobs must be resolved first) | FR-015, FR-002, `BR-SHP-04` |

## 2. Behavior Notes

- **Code security** (`BR-SHP-03`, `C-16`): attempts 1–2 return `CODE_INVALID` with `attemptsRemaining` (2 then 1); attempt 3 returns `CODE_ATTEMPTS_EXCEEDED`, locks verification for **24 hours** (`lockUntil`/`retryAfterSeconds`) and auto-creates a support ticket with the full timeline (`admin.md` tickets). While locked, submissions return 403 `CODE_LOCKED`.
- **Idempotent code entry** (`DOC-SA-010` §5): the first successful verification wins; replaying the same success no-ops with the same `DELIVERED` result.
- **Escrow trigger**: reaching `DELIVERED` starts the 7-day escrow hold (`BR-ESC-01`, `C-12`) — visible in `wallet.md` `GET /wallet/escrow`.
- **Attempt accounting**: a courier-recorded `failed-attempt` is distinct from a wrong code entry; three failed attempts escalate (`BR-SHP-06`) with `DELIVERY_ATTEMPTS_EXCEEDED` on further attempts until an admin intervenes.
- **Proof** (`BR-SHP-07`): delivery proof = verified code + timestamp + courier identity; the photo is optional and never gates `DELIVERED`.
- **Visibility**: couriers see only assigned jobs (404 otherwise); customers see only their own orders (`BR-ORD-09`, `DATA-REQ-008`).
- **Return pickups** (`FR-016`) reuse these mechanics: `RETURN_APPROVED` triggers an assignment offer for the return package — the customer views status via `GET /returns/{id}/pickup` (`returns.md`).
- **Rate limits**: courier scan endpoints follow the standard tier; `API-SHP-010` gets a stricter per-courier limiter (5/min) to blunt code brute-forcing (`SEC-REQ-009`).

## 3. Pagination / Idempotency / Caching

`API-SHP-001/002` use **cursor** pagination (live feeds); all other endpoints are single-resource. Scans are naturally idempotent state-set operations guarded by `version`. All responses `Cache-Control: no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
