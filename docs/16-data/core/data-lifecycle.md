---
document_id: DOC-DTA-002
title: Data Lifecycle by Category
category: 16-data
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [DATA-REQ-002, DATA-REQ-003, DATA-REQ-004, DATA-REQ-006, DATA-REQ-007, DATA-REQ-008, FR-003, FR-017, NFR-017]
related_documents: [DOC-DTA-001, DOC-DTA-003, DOC-DTA-004, DOC-DTA-005, DOC-DTA-006, DOC-DR-003, DOC-BA-005]
---

# DOC-DTA-002 — Data Lifecycle by Category

## 1. Purpose & Scope

Defines the end-to-end lifecycle for every major data category on yumn: **CREATE → STORE → USE → SHARE → ARCHIVE → DELETE**, with the trigger, the owner role, and the governing `DATA-REQ-` / `BR-` references for each stage. Categories not listed here inherit the closest profile plus their classification entry in `data-classification.md` (inventory is authoritative for element-level handling).

## 2. Stage Definitions

| Stage | Definition | Question answered |
|---|---|---|
| **CREATE** | The moment the data first enters the platform: source system, actor, and consent/purpose basis | Where does it come from, on what authority? |
| **STORE** | Primary and secondary persistence locations, encryption, and the system of record | Where does it live, encrypted how? |
| **USE** | Legitimate processing purposes, read paths, and jobs that consume it | Why may it be read? |
| **SHARE** | Disclosure outside the creating service — internal processors only; **never sold** | Who else sees it? |
| **ARCHIVE** | Transition from hot operational storage to cold/archive storage when the operational need ends | When does it stop being operational? |
| **DELETE** | Terminal erasure or irreversible anonymization, with trigger and evidence | When does it die, and how is that proven? |

**Sharing rule (applies to every category):** yumn never sells, rents, or barter-data. Disclosure is limited to (a) the counterparty of the transaction itself (vendor sees buyer fulfillment data; courier sees assigned shipment fields), and (b) contracted processors acting only on yumn's instructions — SMS/WhatsApp providers (`INT-REQ-003`, `INT-REQ-004`), wallet providers (`INT-REQ-001`), object-storage host (`DEP-07`). Processor detail: `10-integrations/`.

## 3. Category Lifecycles

### 3.1 User Profile & Identity (phone, name, password hash, optional email)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Registration: phone `^7[0-9]{8}$`, password, display name; email only if volunteered and then verified; consent = account creation | `BR-AUTH-01`, `BR-AUTH-08`, `FR-001` |
| STORE | Postgres (system of record); phone AES-256 encrypted at rest; bcrypt cost-12 hash; sessions/OTP state in Redis with TTL | `SEC-REQ-002`, `SEC-REQ-006`, `DATA-REQ-004` |
| USE | Authentication, order fulfillment identity, profile display, ownership scoping (`user_id`) | `FR-003`, `DATA-REQ-008` |
| SHARE | Phone shown to vendor/courier only for fulfillment of the user's own order; never exported or sold | `DATA-REQ-002` R4 |
| ARCHIVE | Row-level archive 24 months after account closure, then anonymization per schedule | `RC-04` |
| DELETE | Trigger: confirmed account deletion (`FR-003`) or inactive-account purge. Profile PII anonymized; phone irreversibly disidentified | `DATA-REQ-003`, `DOC-DTA-006` |
| Owner | Customer (ACT-01) owns; platform (yumn) is custodian | `DOC-DTA-003` |

### 3.2 Addresses (governorate, district, street, recipient name/phone)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | User-created address book entries, ≤10 per user; no geocoding, no GPS coordinates ever collected | `FR-003`, `C-16`, `DATA-REQ-002` R3 |
| STORE | Postgres, PII-encrypted (recipient name/phone columns) | `SEC-REQ-006` |
| USE | Checkout shipping selection, shipping-zone costing, courier delivery instructions | `FR-011`, `BR-SHP-01` |
| SHARE | Full address + contact phone disclosed to the assigned courier and the fulfilling vendor for that shipment only | `BR-ORD-09` |
| ARCHIVE | With the order record once delivered and past dispute/return windows | `RC-05` |
| DELETE | Deleted immediately on address-book removal by the user; order copies retained as financial record (disidentified at deletion request) | `DOC-DTA-006` |
| Owner | Customer (ACT-01); platform custodian | `DOC-DTA-003` |

### 3.3 Orders (master/sub-orders, status history, timelines)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Idempotent order creation at checkout; one master per checkout, one sub-order per vendor | `BR-ORD-06`, `C-10` |
| STORE | Postgres; state constrained to exactly 17 values; `order_status_history` append-only with actor/timestamp/reason | `C-09`, `BR-ORD-03`, `DATA-REQ-001` |
| USE | Fulfillment by vendor/courier, buyer tracking, admin operations, analytics aggregation | `BR-ORD-09`, `FR-012` |
| SHARE | Buyer: own orders. Vendor: own sub-orders + buyer fulfillment contact. Courier: assigned shipment only. Admin/Moderator: scoped. Never cross-customer | `DATA-REQ-008`, `DOC-DTA-003` |
| ARCHIVE | Orders older than 35 days after final state (including returns) move to cold partition; retained for financial horizon | `RC-05`, `NFR-017` |
| DELETE | Never hard-deleted inside the financial retention window; on account deletion buyer identity is disassociated (tombstone), amounts/line items remain | `DATA-REQ-003`, `DOC-DTA-006` |
| Owner | Buyer + fulfilling Vendor (shared per sub-order); platform custodian | `C-10` |

### 3.4 Payments, Wallet, Ledger, Escrow & Payouts

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Top-ups (provider callback/poll or admin-verified bank transfer), order payments, refunds, commission, payouts — every movement posts balanced double-entry rows | `BR-PAY-03`, `BR-PAY-04`, `BR-PAY-06` |
| STORE | Postgres ledger tables with `SELECT`/`INSERT` only for the app role — no `UPDATE`/`DELETE` | `DATA-REQ-007` |
| USE | Balance display, escrow release engine (7-day hold), payout batching, statements, VAT/reporting | `C-12`, `BR-ESC-05`, `BR-FIN-04` |
| SHARE | Provider references shared with m-Floos/OneCash for reconciliation only; vendor sees own payable ledger; no actor may modify postings | `BR-ESC-08`, `DOC-DTA-003` |
| ARCHIVE | Partitioned by month; cold after 12 months, retained ≥ 5 years minimum — policy set to **10 years** (`INFERENCE`) | `RC-05`, `retention-and-archival.md` |
| DELETE | **Exempt from erasure** until retention elapses; corrections only via compensating entries, never row removal | `DATA-REQ-007`, `DATA-REQ-003` R3 |
| Owner | Customer/Vendor own their balances; platform is legal custodian of the ledger | `DOC-DTA-003` |

### 3.5 KYC Documents (vendor identity documents)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Vendor uploads during onboarding; submission = consent to verification; rejection allows resubmission | `FR-007`, `BR-VND-03` |
| STORE | MinIO (object bytes) + Postgres metadata (type, status, reviewer, timestamps); classified RESTRICTED | `DEP-07`, `data-classification.md` |
| USE | Admin KYC review within 48 h; payout eligibility gate | `BR-VND-03`, `BR-ESC-06` |
| SHARE | Reviewers (Admin/Super Admin) only; never exposed to customers, other vendors, or couriers | `DOC-DTA-003` |
| ARCHIVE | Approved set archived 5 years after account closure (fraud/dispute exposure), then purged | `RC-06` |
| DELETE | On rejection-superseded cycles: object deleted at resubmission acceptance; on closure: per schedule | `DOC-DTA-005` |
| Owner | Vendor owns the document; platform custodian as verifier | `DATA-REQ-008` |

### 3.6 Product Images & Catalog Media

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Vendor upload; ≤10 images/product, ≤5 MB, jpg/png/webp, EXIF stripped at upload | `BR-CAT-08`, `SEC-REQ-011` |
| STORE | MinIO; Postgres stores object key + dimensions; thumbnails derived | `DEP-07`, `FR-004` |
| USE | Storefront, search results, product detail, cart thumbnails | `FR-009` |
| SHARE | PUBLIC — served to all viewers including guests; object keys are non-guessable | `data-classification.md` |
| ARCHIVE | Tied to product lifecycle; soft-deleted products remain until vendor purge | `BR-CAT-06` |
| DELETE | Product deletion = soft-delete; hard object purge when product row is purged by retention job (never while an order references it) | `DOC-DTA-005` |
| Owner | Vendor (own `store_id`) | `BR-VND-07` |

### 3.7 Notifications (outbox, delivery receipts, in-app inbox)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Fan-out on events; channels SMS, WhatsApp, in-app, push — **no email in v1** | `FR-017`, `BR-NTF-01`, `GAP-03` |
| STORE | Postgres outbox + delivery status; provider receipts logged without message PII; push device tokens in Postgres | `INT-REQ-003`, `SEC-REQ-006` R5 |
| USE | Delivery to user, in-app inbox read state, preference enforcement (security notices non-disableable) | `BR-NTF-02`, `BR-NTF-05` |
| SHARE | Content transmitted to the user's phone via provider processors; template text localized ar/en | `BR-NTF-04` |
| ARCHIVE | Sent-message metadata archived 90 days; body content not retained beyond delivery | `RC-02` |
| DELETE | Purge by schedule; user-initiated inbox clear deletes in-app rows; OTP rows expire at 5 minutes in Redis | `BR-AUTH-03`, `RC-01` |
| Owner | Customer (recipient) | `DOC-DTA-003` |

### 3.8 Audit Logs (privileged & money actions)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Written atomically with privileged/money actions: actor, action, entity, before/after, IP, timestamp | `BR-PLT-06`, `SEC-REQ-010` |
| STORE | Postgres append-only tables; hash chain each row to the previous; app role has no `UPDATE`/`DELETE` | `SEC-REQ-010` R1/R4 |
| USE | Investigations, dispute resolution, admin oversight; verification job recomputes the chain | `FR-020`, `SEC-REQ-010` R4 |
| SHARE | Read-only, scoped: Admin platform scope, Super Admin full, Vendor own-store scope, Moderator none, System write-only | `actors-and-roles.md`, `DOC-DTA-003` |
| ARCHIVE | Hot 12 months, then partition archive; retained **10 years** (`INFERENCE`, floor ≥ 5 years `VERIFIED`) | `RC-06`, `NFR-019` |
| DELETE | Scheduled purge only **after** the retention floor, executed by a privileged maintenance role that bypasses app permissions, with evidence entry; chain segment sealed before purge | `retention-and-archival.md` §7 |
| Owner | Platform (yumn) — nobody owns audit rows individually | `SEC-REQ-010` |

### 3.9 Search Index (Elasticsearch, derived)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Async index from Postgres product/store/review documents on create/update/publish events | `FR-009`, `BR-PLT-01` |
| STORE | Elasticsearch 8 — **derived, never source of truth** | `DEP-04`, `DOC-DTA-001` §3 |
| USE | Arabic-aware full-text search, filters, sorting, category browse | `FR-009` |
| SHARE | Never shared externally; index contains catalog fields only — no phone, address, order, or wallet data | `data-classification.md` §4 |
| ARCHIVE | Not archived — rebuildable from Postgres at any time | `RC-08` |
| DELETE | On product soft-delete: document removed from index within 5 minutes (`INFERENCE`, index-lag SLO in `data-quality.md`); on account deletion cascade: purge store docs; full rebuild available as disaster path | `DOC-DTA-006` §5 |
| Owner | Platform (derived from Vendor content) | `DATA-REQ-008` |

### 3.10 Cache & Queues (Redis)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Cache fills on read misses; BullMQ payloads created by domain events; OTP/session counters written at issuance | `NFR-004`, `C-20`, `BR-AUTH-03` |
| STORE | Redis 7 — volatile, TTL-bound, **not source of truth** | `DEP-03` |
| USE | Read acceleration, rate limiting (`SEC-REQ-009`), job execution with 3× backoff then DLQ | `BR-PLT-02` |
| SHARE | Never leaves the platform boundary | — |
| ARCHIVE | Not archived | `RC-01`/`RC-08` |
| DELETE | Natural TTL expiry (OTP 5 min, cache entries minutes, reservations 15 min per `C-13`); explicit key purge on account deletion and on data-change invalidation | `DOC-DTA-006` §5 |
| Owner | Platform | `DOC-DTA-003` |

### 3.11 Backups (WAL + daily snapshots)

| Stage | Detail | Ref |
|---|---|---|
| CREATE | Continuous WAL archiving (RPO ≤ 15 min) + daily full snapshot; encrypted at rest, off primary host | `DATA-REQ-004`, `NFR-006` |
| STORE | Backup storage, access limited to operations role | `DATA-REQ-004` R3 |
| USE | Point-in-time restore, quarterly restore drills with ledger-balance integrity check | `AC-DR004-03` |
| SHARE | Never shared; no restore into non-production without masking (`DOC-DTA-006` §7) | `SEC-REQ-006` |
| ARCHIVE | WAL 14 days; snapshots 35 days (`INFERENCE`) | `RC-09` |
| DELETE | Aging-out only — purged rows disappear from backups as the window rolls; deletion requests document this residual window | `DOC-DTA-006` §5, `AC-DR003-01` |
| Owner | Platform (operations role) | `DATA-REQ-004` |

## 4. Derived-Data Invalidation on Deletion (mandatory cascade)

Deleting or anonymizing primary data **must** invalidate every derived copy in the same operation; otherwise deleted PII resurfaces through search or cache. Cascade matrix:

| Primary data change | Elasticsearch | Redis cache | BullMQ | MinIO |
|---|---|---|---|---|
| Product updated/soft-deleted | Reindex or delete doc (≤ 5 min) | Invalidate product/store/catalog keys; purge listing pages | Cancel queued merchandising jobs for that product | Keep object until product purge |
| Review hidden/moderated | Remove/update doc | Invalidate store-rating keys | — | Keep images while visible reference exists |
| Account deleted / PII anonymized | Delete store docs (vendor), remove follower/review display names | Purge session, profile, cart, recommendation keys; revoke sessions | Drop pending jobs parameterized by `user_id` | Delete vendor KYC objects per schedule; keep product images owned by surviving store |
| Address removed | Not indexed | Invalidate checkout keys | — | — |
| Full purge job (retention) | Rebuild index from surviving rows if bulk purge occurred | `FLUSHDB`-scoped key patterns per category | Drain category-specific queues before purge | Object sweep by orphan-key report |

**Rule:** cache keys must be derived from owner keys (`user_id`/`store_id`) so invalidation is enumerable (`DATA-REQ-008` R2). Cache misses always rebuild from Postgres; no deletion may depend on cache expiry alone.

## 5. Schema-Evolution Interaction (`DATA-REQ-005`)

Expand–contract migrations never drop a column holding data inside an active retention window: the contract step runs only after backfill and archive consumers are off the old structure. Archived/cold partitions must remain readable by reports for the full `RC-05` horizon even after the hot schema evolves (08-database owns the migration mechanics; this domain owns the *readability horizon*).

## 6. Verification

- Cascade test: delete a product → assert absence in ES within the index-lag SLO, cache keys invalidated, MinIO object retained per schedule (`AC-DR003-01` pattern).
- Ledger immutability test: no lifecycle stage permits `UPDATE`/`DELETE` of postings (`AC-DR007-01`).
- Backup aging-out test: purge evidence states the residual window until which copies persist (`DATA-REQ-003` R5).
- Traceability: category → `DQ-` rule → `RC-` class recorded in `19-traceability/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
