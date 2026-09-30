---
document_id: DOC-API-002
title: API Conventions — REST Rules, Headers, Idempotency & Uploads
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-011, FR-013, NFR-001, NFR-013, NFR-014, SEC-REQ-003, SEC-REQ-004, SEC-REQ-009, SEC-REQ-011, DATA-REQ-008]
related_documents: [DOC-API-001, DOC-API-003, DOC-API-004, DOC-REQ-001, DOC-BA-005, DOC-OVR-008, DOC-BE-003, DOC-FE-005]
---

# API Conventions

Rules that apply to **every** endpoint in `07-api/`. Endpoint files assume these conventions and do not repeat them.

---

## 1. Base URL & Resource Naming

| Rule | Value / example |
|---|---|
| Base path | `https://api.yumn.ye/api/v1` (TLS 1.3 only, `SEC-REQ-006`) — `/api/v1` is never locale-prefixed |
| Naming | lowercase kebab-case nouns, plural for collections: `/orders`, `/store/products`, `/support/tickets` |
| Identifiers | opaque string IDs (UUID) in paths; slugs (`slug`) used for public, SEO-facing reads: `/products/{slug}`, `/categories/{slug}`, `/stores/{slug}` |
| Nesting depth | max 2 levels of resource nesting in paths (`/store/orders/{id}/confirm`); deeper relations expressed via query params or linked IDs in responses |
| Sub-resources | vendor-owned collections hang off `/store/...`; platform-owned collections off `/admin/...`; customer collections off the root (`/orders`, `/cart`) |
| Verbs in paths | nouns only; actions expressed via HTTP method or a terminal action segment on POST (`/confirm`, `/publish`, `/approve`) |
| No trailing slash | `/orders/` is a different cache key than `/orders` — servers redirect 308 to the canonical form |
| Case sensitivity | paths are case-sensitive; IDs are lowercase |

## 2. HTTP Methods Semantics

| Method | Semantics | Success codes | Idempotent | Side effects |
|---|---|---|---|---|
| `GET` | Read a resource or collection; never mutates state | 200 | Yes | None (cache allowed) |
| `POST` | Create a resource **or** invoke an action segment | 201 (create), 200 (action) | Only where an `Idempotency-Key` is required (§6) | Yes |
| `PUT` | Full replacement of a resource (or of a settings block) | 200 | Yes (same body ⇒ same state) | Yes |
| `PATCH` | Partial update of fields | 200 | No | Yes |
| `DELETE` | Remove a resource (soft-delete where the domain requires it) | 204 (no body), 200 if a deletion object is returned | Yes (repeat delete ⇒ 404 or idempotent 204) | Yes |

Additional rules:

- **Method override is forbidden** — no `X-HTTP-Method-Override`; every action has its own real route.
- **GET is side-effect free** — no state writes, no counters incremented inside GET handlers (metrics are captured out of band).
- **Safe preconditions**: 412 `PRECONDITION_FAILED` is reserved for `If-Match` failures on settings resources using optimistic locking (`PUT /admin/settings/{key}` carries `expectedVersion`).

## 3. Authentication & Session Headers

| Header | Direction | Rule |
|---|---|---|
| `Authorization: Bearer <access-token>` | request | RS256 JWT, 15-minute expiry, claims `sub`, `roles`, `sid` — `C-08`, `SEC-REQ-003` |
| `X-Session-Id: <sid>` | request | optional echo of the session id; server cross-checks `sid` is live in the session registry on every authenticated call (`DOC-BE-003` §3) |
| `Cookie: yumn_refresh=...` | request | web clients only: httpOnly + SameSite refresh cookie (7 days, single-use rotation); mobile clients store the opaque refresh token in encrypted storage |
| `WWW-Authenticate: Bearer error="invalid_token"` | response | on 401 responses |
| `Accept-Language: ar \| en` | request | selects localized messages/fields; default `ar` (`C-24`, `BR-PLT-05`) |
| `Accept: application/json` | request | required for JSON endpoints; 406 if unsupported |

Auth lifecycle (specified in `auth.md`): OTP → login → refresh (single-use rotation; reuse revokes the session family, `BR-AUTH-05`) → logout. A revoked/expired access token returns 401 `TOKEN_EXPIRED` (refreshable) or 401 `AUTH_INVALID` (re-login required).

## 4. Authorization: Roles & Ownership

| Rule | Detail |
|---|---|
| Role values | `CUSTOMER`, `VENDOR`, `COURIER`, `ADMIN`, `SUPER_ADMIN`, `MODERATOR`; `SYSTEM` is a non-interactive service identity with no endpoints (it acts through internal jobs) |
| Declaration | every endpoint file lists a **Roles** column; `Public` = no auth required; `Any authenticated` = any of the six roles |
| Enforcement | server-side only: role check + ownership check before business logic (`SEC-REQ-004`, FR-002) |
| Ownership | resource rows carry `user_id` / `store_id` (`DATA-REQ-008`); customer reads are scoped to `sub`; vendor queries are scoped to the caller's `store_id` at the service layer (`BR-VND-07`) |
| Cross-tenant reads | return **404 `NOT_FOUND`** for resources that exist but belong to another tenant (prevents IDOR disclosure); 403 `FORBIDDEN` is used when the caller is authenticated, the resource is in their scope, but the *action* is not permitted for their role |
| Deny by default | no implicit grants; an endpoint without an explicit role grant is inaccessible (`FR-002`) |
| Privileged writes | `ADMIN`/`SUPER_ADMIN`/`MODERATOR` state-changing actions write append-only audit entries (`BR-PLT-06`, `SEC-REQ-010`) |

## 5. Content, Money, Dates, Localization

| Concern | Rule |
|---|---|
| Request/response media type | `application/json; charset=utf-8`; multipart only for file uploads (§10) |
| Money | **integer YER** in every field named `*Amount`, `price`, `balance`, `fee`, `total`, `commission`, `refund` — never floats, never strings with separators (`BR-PAY-10`, `C-04`) |
| Money fields | always include the currency implicitly as `currency: "YER"` on wallet/order objects; no other currency exists in v1 (`C-04`) |
| Money math | server computes all totals; clients send only chosen inputs (address, method, coupon) — totals are echoed, never trusted (`BR-CRT-04`) |
| Timestamps | ISO-8601 UTC with `Z` suffix: `2026-09-26T14:03:22Z` — field names end in `At` |
| Dates without time | ISO date `YYYY-MM-DD` for report boundaries (`from`, `to`) |
| Durations | integers plus explicit unit in the field name: `reservationExpiresAt` (timestamp), `returnPeriodDays` (days) |
| Locale display | server returns raw values; Arabic-Indic numeral formatting is a client concern (`BR-PAY-10`) — APIs never pre-format money into strings |
| Localization | error `message` is localized via `Accept-Language`; machine `code` is locale-independent (see `error-model.md` §5) |
| Nullable/omitted | absent optional field = "not set"; `null` = "explicitly cleared" — PATCH distinguishes the two |
| Booleans | `true`/`false`, never `"true"` |

## 6. Idempotency-Key Header

Required (server rejects with 400 `IDEMPOTENCY_KEY_REQUIRED` when missing) on:

| Operation | Rule reference |
|---|---|
| `POST /orders` (order creation) | `BR-ORD-06`, `BR-PLT-03` |
| `POST /wallet/topups` (top-up initiation) | `BR-PAY-08`, `BR-PLT-03` |
| `POST /wallet/payments/authorize` and capture | `BR-PAY-08`, `BR-PLT-03` |
| Stock reservation performed by `POST /checkout/session` | `BR-PLT-03`, `C-13` |
| `POST /coupons/validate` (coupon application) | `BR-PLT-03` |
| Refund execution (admin/system re-triggers) | `BR-PAY-08`, `BR-PLT-03` |
| `POST /cart/merge` | `../../05-frontend/core/state-management.md` |

Semantics:

1. Client generates a UUID v4 per logical operation and reuses it on every retry of that operation.
2. Server stores `(endpoint, key)` → first response (status + body hash) with a retention window of **24 hours**.
3. Replay with the same key **and same request fingerprint** ⇒ returns the stored response verbatim (HTTP status identical).
4. Same key, different fingerprint ⇒ **409 `IDEMPOTENCY_CONFLICT`**.
5. Processing in flight ⇒ **409 `IDEMPOTENCY_IN_PROGRESS`** with `Retry-After`.

## 7. Correlation IDs (Observability)

| Rule | Detail |
|---|---|
| Request header | `X-Correlation-Id: <uuid>` — clients SHOULD send one; if absent, the gateway generates it |
| Response header | `X-Correlation-Id` echoed on **every** response, including errors |
| Error payload | the same value appears in the error envelope's `correlationId` (`error-model.md` §1) |
| Propagation | carried through the modular monolith into BullMQ job payloads and integration callbacks (`NFR-014`) |
| Access logs | every request logs method, path, status, duration, correlationId, `sub` (masked), role — never tokens, OTPs or passwords (`SEC-REQ-002`, `SEC-REQ-007`) |
| Client support flow | UI shows `correlationId` in "copy details" (`../../05-frontend/core/forms-and-validation.md` §5) |

## 8. Rate Limiting Headers (SEC-REQ-009)

Limits are enforced per IP **and** per authenticated user (Redis sliding window).

| Endpoint class | Limit | Examples |
|---|---|---|
| Standard API | 100 req/min | reads, profile, cart |
| OTP request/verify | 5/min/IP and 3 resends/10 min/user | `/auth/otp/request`, `/auth/otp/verify` |
| Login | 10/min/IP plus per-account lockout | `/auth/login` |
| Top-up initiation | stricter tier (10/min/user) | `/wallet/topups` |
| Order creation | stricter tier (10/min/user) | `POST /orders` |

Response headers on **every** response:

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | limit for the current window |
| `X-RateLimit-Remaining` | requests left in the window |
| `X-RateLimit-Reset` | Unix epoch seconds when the window resets |
| `Retry-After` | seconds to wait — present on 429 only |

Exceeding a limit ⇒ **429 `RATE_LIMITED`** with the headers above; the envelope's `retryAfterSeconds` mirrors `Retry-After`.

## 9. Deprecation Policy

| Stage | Behavior |
|---|---|
| Announce | endpoint marked deprecated in this contract (`status` table row in the group file) and in the changelog of `07-api/README.md` |
| Signal | deprecated endpoints return `Deprecation: true` and `Sunset: <RFC-1123 date>` response headers; the error model may add a `warning` field for the transition period |
| Minimum lifetime | ≥ 6 months between deprecation announcement and removal for any `v1` endpoint |
| Replacement | a `Link: rel="successor"` header points at the replacement route when one exists |
| Version bump | removal or breaking change of behavior requires `/api/v2`; `/api/v1` keeps serving the deprecated route until the sunset date |
| Field-level | fields are never repurposed; a retired field is ignored by the server and eventually removed in `v2` |

## 10. Multipart Uploads (SEC-REQ-011)

All file uploads use `POST` with `Content-Type: multipart/form-data`, a single `file` field (plus any JSON fields in a `meta` field).

| Rule | Value |
|---|---|
| Image types | `image/jpeg`, `image/png`, `image/webp` **only** — no SVG, no GIF, no HEIC |
| Image size | ≤ 5 MB per file (`SEC-REQ-011`, `BR-CAT-08`) |
| Document type | `application/pdf` only — KYC documents and bank-transfer top-up proofs (≤ 5 MB) |
| Count limits | product images ≤ 10/product (`BR-CAT-08`); review images ≤ 5 (`BR-REV-03`); delivery proof photo ≤ 1 (`BR-SHP-07`) |
| Server processing | magic-byte type check (never trust `Content-Type`), AV malware scan, EXIF/GPS metadata stripped, image re-encoded; no SVG ever rendered (`SEC-REQ-011`) |
| Response | returns a `fileId` + CDN URL (`https://cdn.yumn.ye/files/{fileId}`) stored in MinIO; subsequent domain calls reference `fileId` |
| Errors | 400 `VALIDATION_ERROR` (bad type/size), 413 `PAYLOAD_TOO_LARGE`, 415 `UNSUPPORTED_MEDIA_TYPE`, 422 `FILE_SCAN_FAILED` |
| Authorization | upload endpoints require an authenticated role; anonymous upload endpoints do not exist |

## 11. General Request/Response Rules

- **Collection responses** follow the pagination envelope in `pagination.md` (`items` + paging metadata). **Single-resource responses** return the object directly.
- **Location header** on 201: `Location: /api/v1/{collection}/{id}`.
- **204 No Content** for successful DELETE without a body.
- **Validation**: all input validated server-side by DTO pipes; failures return 400 `VALIDATION_ERROR` with per-field `details[]` (`../../05-frontend/core/forms-and-validation.md` §1 — client checks are UX only).
- **Optimistic concurrency**: order/state transitions use the resource `version`; a stale version or illegal transition ⇒ 409 `STATE_CONFLICT`.
- **Partial success**: not used — operations are atomic; a failure returns one error and changes nothing.
- **Batch endpoints**: not exposed in v1 (all writes are single-resource).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
