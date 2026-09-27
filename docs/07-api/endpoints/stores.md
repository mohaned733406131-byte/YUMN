---
document_id: DOC-API-008
title: API-VND — Vendor Onboarding, KYC, Store Configuration & Followers (FR-007, FR-008)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-007, FR-008, FR-004, FR-014, FR-017, NFR-012, SEC-REQ-011, DATA-REQ-008, BR-VND-01, BR-VND-02, BR-VND-03, BR-VND-04, BR-VND-05, BR-VND-06, BR-VND-07, BR-ESC-03, BR-ESC-06]
related_documents: [DOC-API-002, DOC-API-003, DOC-FR-007, DOC-FR-008, DOC-BA-005, DOC-OVR-008]
---

# API-VND — Vendor Onboarding, KYC & Store Management

**Group:** `API-VND` · **FR-007, FR-008** · **Endpoints:** `API-VND-001…021` · **Base:** `/api/v1`

One store per vendor (`BR-VND-02`); publishing blocked until KYC = APPROVED (`BR-VND-01`); KYC decisions within 48 h with unlimited resubmission after rejection (`BR-VND-03`); suspended store ⇒ products hidden, new orders blocked, existing orders frozen, payouts held (`BR-VND-04`). All `/store/*` queries are scoped to the caller's `store_id` at the service layer (`BR-VND-07`, `DATA-REQ-008`) — another vendor's store returns 404 `NOT_FOUND`. **Single hub per store: no GPS/coordinate fields exist anywhere in this group** (`C-16`, `BR-SHP-05`).

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-VND-001 | `GET /vendor/onboarding/status` | `VENDOR` | Current onboarding step for the caller | → `200 { step: "NONE"\|"PENDING_KYC"\|"APPROVED"\|"REJECTED"\|"SUSPENDED", kycStatus, submittedAt?, decidedAt?, resubmissionAllowed, slaDueAt? }` | `AUTH_INVALID` | FR-007, `UC-015`, `BR-VND-03` |
| API-VND-002 | `POST /vendor/application` | `VENDOR` | Submit the vendor application (store legal/trade name, category, contact, domestic address) — creates the single store draft | `{ legalName, tradeName, categorySlug, contactPhone, address: { governorate, district, line1 } }` → `201 { applicationId, storeId, status: "PENDING_KYC" }` | `ONE_STORE_PER_VENDOR`, `VALIDATION_ERROR`, `STORE_SUSPENDED` | FR-007, `BR-VND-02`, `UC-015`, `C-17` |
| API-VND-003 | `PUT /vendor/application` | `VENDOR` | Edit a draft/rejected application and resubmit (rejection allows unlimited resubmission) | same shape → `200 { applicationId, status: "PENDING_KYC", slaDueAt }` — resubmission restarts the 48-hour SLA | `NOT_FOUND`, `KYC_IN_REVIEW`, `VALIDATION_ERROR` | FR-007, `BR-VND-03`, `AC-FR007-04` |
| API-VND-004 | `POST /vendor/kyc/documents` | `VENDOR` | Upload KYC documents from the platform-configured required set | `multipart/form-data { docType, file }` → `201 { documentId, docType, status: "UPLOADED" }` — pdf ≤5 MB (images ≤5 MB jpg/png/webp), magic-byte check, malware scan, EXIF strip; no SVG | `VALIDATION_ERROR`, `PAYLOAD_TOO_LARGE`, `UNSUPPORTED_MEDIA_TYPE`, `FILE_SCAN_FAILED`, `KYC_IN_REVIEW` | FR-007, SEC-REQ-011, `UC-015`, `api-conventions.md` §10 |
| API-VND-005 | `GET /vendor/kyc` | `VENDOR` | Own KYC case detail: status, uploaded documents, decision, reason, SLA age | → `200 { status, documents: [...], decision?: { outcome, reason, decidedAt, decidedBy }, submittedAt, slaDueAt }` | `NOT_FOUND` (no case yet) | FR-007, `BR-VND-03` |
| API-VND-006 | `GET /store` | `VENDOR` | Own store profile + operating settings + **read-only commission tier** | → `200 { id, slug, nameAr, nameEn, descriptionAr?, descriptionEn?, logoUrl?, bannerUrl?, contact: {...}, status, kycStatus, commission: { tierPercent: 10, min: 5, max: 20, source: "PLATFORM_DEFAULT" }, autoAcceptOrders, returnPolicy: { isReturnable, returnPeriodDays }, followerCount, rating: { average, count } }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-008, `UC-016`, `BR-ESC-03`, `BR-VND-07`, `BR-REV-05`, `C-11` |
| API-VND-007 | `PUT /store` | `VENDOR` (Editor/Manager/Owner) | Replace profile + branding + operating settings | full store body → `200 { …store }` — commission tier is **never** writable (platform-set) | `NOT_FOUND`, `STORE_SUSPENDED`, `VALIDATION_ERROR`, `KYC_NOT_APPROVED` (publish-affecting fields) | FR-008, `UC-016`, `BR-VND-04/06`, `SEC-REQ-011` |
| API-VND-008 | `GET /store/hours` | `VENDOR` | Read operating hours (weekly schedule, single hub — no geofencing) | → `200 { timezone: "Asia/Aden", days: [ { day: "SAT", open: "09:00", close: "22:00", closed: false }, … ] }` | `NOT_FOUND` | FR-008, `C-16` |
| API-VND-009 | `PUT /store/hours` | `VENDOR` (Editor/Manager/Owner) | Update operating hours | same shape → `200 { …hours }` | `VALIDATION_ERROR`, `STORE_SUSPENDED` | FR-008 |
| API-VND-010 | `GET /store/shipping-zones` | `VENDOR` | Read configured domestic shipping zones/fees for the store | → `200 { items: [ { zoneSlug, governorates: [...], feeYER, freeOverYER? } ], domesticOnly: true }` | `NOT_FOUND` | FR-008, FR-015, `BR-SHP-01`, `C-17` |
| API-VND-011 | `PUT /store/shipping-zones` | `VENDOR` (Owner) | Replace the zone/fee configuration | full list → `200 { items: [...] }` — any zone outside domestic Yemen coverage is rejected | `NO_SHIPPING_ZONE`, `VALIDATION_ERROR`, `STORE_SUSPENDED` | FR-008, `AC-FR008-04`, `C-17`, `BR-SHP-01` |
| API-VND-012 | `GET /stores/{slug}` | Public | Storefront page: profile, branding, rating summary, follower state, active products (cursor feed) | `?limit&cursor` → `200 { id, slug, nameAr, nameEn, logoUrl?, bannerUrl?, rating: { average, count }, followerCount, isFollowing: boolean, status, products: { items: [...], page: {…} } }` — suspended/hidden stores return 404; only ACTIVE products listed | `NOT_FOUND`, `VALIDATION_ERROR` | FR-008, `UC-001`, `UC-008`, `BR-CAT-06`, `BR-REV-05`, `BR-VND-04` |
| API-VND-013 | `POST /stores/{id}/follow` | `CUSTOMER` | Follow a store (idempotent — repeat ⇒ 200 same state) | → `200 { isFollowing: true, followerCount }` — followers receive new-product/offer notifications per preferences | `NOT_FOUND`, `STORE_SUSPENDED`, `RATE_LIMITED`, `FOLLOW_LIMIT_REACHED` | FR-008, `BR-VND-05`, `UC-008`, `BR-PLT-03` |
| API-VND-014 | `DELETE /stores/{id}/follow` | `CUSTOMER` | Unfollow (notifications cease from that point) | → `200 { isFollowing: false, followerCount }` — idempotent | `NOT_FOUND` | FR-008, `BR-VND-05`, `UC-008` |
| API-VND-015 | `GET /store/followers` | `VENDOR` | Follower list + count for the own store (offset pagination) | `?page&pageSize&sort=createdAt_desc` → `200 { items: [ { userId, displayName, followedAt } ], page: {…} }` | `NOT_FOUND`, `STORE_SUSPENDED` | FR-008, `BR-VND-05`, `DATA-REQ-008` |
| API-VND-016 | `GET /store/staff` | `VENDOR` (all staff roles) | List vendor staff accounts and roles | → `200 { items: [ { userId, displayName, role: "VIEWER"\|"EDITOR"\|"MANAGER", invitedAt, lastActiveAt } ], ownerUserId }` | `NOT_FOUND` | FR-002, FR-007, `BR-VND-06` |
| API-VND-017 | `POST /store/staff` | `VENDOR` (Owner only) | Invite a staff member by phone with a Viewer/Editor/Manager role | `{ phone, role }` → `201 { userId, role }` — invitee must already hold a platform account | `NOT_FOUND`, `INVALID_ROLE`, `STAFF_LIMIT_REACHED`, `VALIDATION_ERROR`, `FORBIDDEN` | FR-002, `BR-VND-06`, `UC-015` |
| API-VND-018 | `PATCH /store/staff/{userId}/role` | `VENDOR` (Owner only) | Change a staff member's role; self-escalation blocked | `{ role, reason }` → `200 { userId, role }` — audit entry written | `STAFF_SELF_ESCALATION`, `LAST_SUPER_ADMIN`-style guard for removing the last Owner ⇒ `FORBIDDEN`, `INVALID_ROLE`, `NOT_FOUND` | FR-002, `BR-VND-06`, `AC-FR002-03` |
| API-VND-019 | `DELETE /store/staff/{userId}` | `VENDOR` (Owner only) | Remove a staff member (their sessions revoked) | → `204` | `NOT_FOUND`, `FORBIDDEN` | FR-002, `BR-VND-06` |
| API-VND-020 | `GET /store/payout-account` | `VENDOR` (Owner) | Read the configured payout destination (masked) | → `200 { method: "BANK_TRANSFER"\|"MOBILE_WALLET", bankName?, accountMasked, holderName, verifiedAt? }` | `NOT_FOUND` | FR-014, `BR-ESC-05/06`, `GAP-06` |
| API-VND-021 | `PUT /store/payout-account` | `VENDOR` (Owner) | Set/update the payout destination; re-verification required after change | `{ method, bankName?, accountNumber, holderName }` → `200 { …payoutAccount }` — full account number is write-only, never returned | `VALIDATION_ERROR`, `KYC_NOT_APPROVED`, `STORE_SUSPENDED` | FR-014, `BR-ESC-06`, SEC-REQ-006 |

## 2. Behavior Notes

- **KYC SLA** (`BR-VND-03`): `slaDueAt = submittedAt + 48h`; breach escalates the case to the admin queue (`GET /admin/kyc` in `admin.md`) and alerts reviewers — surfaced here only as `slaDueAt`.
- **Suspension effects** (`BR-VND-04`): while `status = "SUSPENDED"`, write endpoints return `STORE_SUSPENDED`, storefront reads (`API-VND-012`) return 404, and payout/publish operations elsewhere fail with `STORE_SUSPENDED` / `KYC_NOT_APPROVED`.
- **Commission display** (`BR-ESC-03`): `commission.tierPercent` is read-only on `GET /store`; only `SUPER_ADMIN` changes tiers via `PUT /admin/settings/{key}` (`admin.md`).
- **Product sub-resource linkage (FR-004)**: the vendor's product/inventory collections hang off this store scope but are **specified in `catalog.md`**: `GET/POST /store/products`, `GET/PUT /store/products/{id}`, `DELETE /store/products/{id}`, `POST /store/products/{id}/publish|unpublish`, `POST /store/products/{id}/images`, `GET /store/inventory`, `PATCH /store/inventory/{sku}` — all inherit `store_id` ownership from this group (`BR-VND-07`).
- **Store rating** is recomputed incrementally from visible reviews (`BR-REV-05`) and is cached (`NFR-004`).
- **Auto-accept**: `autoAcceptOrders = true` lets `SYSTEM` execute `PLACED → CONFIRMED` (transition guard in `state-transitions.md` §2).

## 3. Pagination / Idempotency / Caching

| Endpoint(s) | Mode |
|---|---|
| `API-VND-012` products, `API-VND-015` followers, `API-VND-016` staff | cursor for storefront products; offset for followers/staff (bounded tables) |
| Everything else | single resource |

Follow/unfollow are idempotent (`BR-PLT-03`). Storefront reads may be cached ≤ 30 s (`NFR-004`); `/store*` reads are `no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
