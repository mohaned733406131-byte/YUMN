---
document_id: DOC-DTA-004
title: Data Classification Scheme & Element Inventory
category: 16-data
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-002, DATA-REQ-003, DATA-REQ-007, SEC-REQ-002, SEC-REQ-006, SEC-REQ-007, SEC-REQ-008, SEC-REQ-010]
related_documents: [DOC-DTA-001, DOC-DTA-002, DOC-DTA-003, DOC-DTA-005, DOC-DR-002, DOC-BA-005]
---

# DOC-DTA-004 — Data Classification Scheme & Element Inventory

## 1. Purpose

Single authoritative classification register for every data element yumn stores. `DATA-REQ-002` R1 forbids any PII field that has no entry here; `SEC-REQ-006` R2 derives encryption from these levels. Classification precedes every other decision (storage, access, masking, retention, logging).

## 2. Classification Levels

| Level | Definition | Default handling rules |
|---|---|---|
| **PUBLIC** | Intended for anyone, including guests; publication is the purpose | Served over TLS; integrity protected; no access control beyond anti-abuse; may be cached/CDN'd |
| **INTERNAL** | Non-personal operational data; exposure is an efficiency loss, not a harm | Authenticated roles only; no external sharing; acceptable in application logs with IDs (never payloads) |
| **CONFIDENTIAL** | Personal data or commercial data whose exposure harms a person or the business | Role + ownership scoping; AES-256 at rest; masked in non-prod and in support views; never in logs/metrics; sharing only per `data-lifecycle.md` §2 |
| **RESTRICTED** | Highest-risk data: credentials, verification secrets, KYC identity documents, financial immutability records | Least-privilege access with named reviewers; AES-256 at rest + keys outside the DB (`SEC-REQ-007`); access logged; never leaves the platform; masked/redacted in non-prod; retention per `retention-and-archival.md` |

**Rules:** (a) an element takes the **highest** level present in any component (e.g. order = CONFIDENTIAL because it embeds contact PII); (b) levels are assigned here, controls are implemented in `09-security/`; (c) new fields require an inventory row **before** the migration that adds them (`DATA-REQ-002` R1).

## 3. Retention Classes & Masking Notation (defined here, applied everywhere)

Retention classes `RC-01…RC-09` are **defined authoritatively in `retention-and-archival.md` §3**; short form:

| ID | Class | Period (summary) |
|---|---|---|
| RC-01 | Ephemeral | ≤ 24 hours (OTP, counters, reservations TTL) |
| RC-02 | Short operational | 90 days (IP/login metadata, notification status) |
| RC-03 | Operational | 12 months (tickets, ops records, hot audit) |
| RC-04 | Account lifecycle | Active + 24 months inactivity → anonymize (profile, addresses) |
| RC-05 | Financial | 10 years (`INFERENCE`; floor ≥ 5 years `VERIFIED`, `NFR-019`) |
| RC-06 | Audit | 10 years, immutable then scheduled purge (`INFERENCE`; floor ≥ 5 years `VERIFIED`) |
| RC-07 | KYC | 5 years after account closure (`INFERENCE`) |
| RC-08 | Derived/volatile | Until invalidated (ES, Redis, queues) |
| RC-09 | Backup | WAL 14 days / snapshots 35 days (`INFERENCE`) |

Masking rules (used by the inventory column and by `data-deletion-and-privacy.md` §7):

| ID | Masking rule | Example |
|---|---|---|
| MASK-01 | Partial mask — keep last 4 characters, rest replaced | `712345678` → `******5678` |
| MASK-02 | Irreversible pseudonym — HMAC of value with environment salt; format preserved for joins | phone → `usr_9f3c…` |
| MASK-03 | Full redaction | `[REDACTED]` (document bytes, OTP, tokens) |
| MASK-04 | Synthetic replacement — generated Arabic name/address of same shape | `محمد علي` → `مستخدم تجريبي 0421` |
| MASK-05 | Value kept, identifiers pseudonymized (financial rows usable for analytics) | amounts retained, `user_id` → MASK-02 token |
| MASK-06 | Secret substitution — real secret never copied; sandbox/rotated value used | provider keys, JWT signing keys |

## 4. Element Inventory

Columns: **Store** — Postgres (system of record) / Redis / ES / MinIO / Logs / Metrics. Encryption — at-rest expectation per `SEC-REQ-006`/`SEC-REQ-007`. Access — abbreviated per `data-ownership.md` §2.

| # | Element | Purpose (why it exists) | Class | Store | Encryption expectation | RC | Non-prod mask | Access roles |
|---|---|---|---|---|---|---|---|---|
| 1 | Phone number (`^7[0-9]{8}$`) | Primary identity, OTP delivery, fulfillment contact (`BR-AUTH-01`, `C-06`) | CONFIDENTIAL | Postgres | AES-256 at rest; never in logs | RC-04 | MASK-01/02 | Owner R/W; Admin masked R; Courier R* assigned window |
| 2 | Password hash | Authentication | RESTRICTED | Postgres | bcrypt cost 12, salted; plaintext never stored/logged (`SEC-REQ-002`) | RC-04 | MASK-06 (dummy hash) | System verify-only |
| 3 | OTP code | Step-up verification (6 digits, 5 min, 3 attempts) | RESTRICTED | Redis | TTL 300 s; never logged; attempt counters (`BR-AUTH-03`) | RC-01 | MASK-03 | System only |
| 4 | JWT access token | Session assertion (15 min, RS256) | CONFIDENTIAL | Redis/client | Signed; never logged; not stored server-side in plaintext | RC-01 | MASK-06 | Bearer only |
| 5 | Refresh token (hash) | Session continuity (7 d, single-use rotation, ≤5 devices) | RESTRICTED | Postgres | Stored as hash; reuse revokes family (`BR-AUTH-05`) | RC-04 | MASK-06 | System only |
| 6 | Display name | Profile presentation | CONFIDENTIAL | Postgres, ES* | AES-256 at rest | RC-04 | MASK-04 | Owner W; public read of vendor/store-facing names |
| 7 | Email (optional, never login) | Contact fallback if provided (`BR-AUTH-08`) | CONFIDENTIAL | Postgres | AES-256 at rest | RC-04 | MASK-02 | Owner R/W; Admin masked R |
| 8 | Address: governorate/district/street | Shipping destination & zone costing | CONFIDENTIAL | Postgres | AES-256 at rest; no GPS fields exist (`C-16`) | RC-04/05 | MASK-04 | Owner RW*; Vendor/Courier R assigned order |
| 9 | Recipient name + phone on address | Delivery contact | CONFIDENTIAL | Postgres | AES-256 at rest | RC-04/05 | MASK-01/04 | Owner RW*; Courier R* active delivery (`DOC-DTA-003` §3.3) |
| 10 | Session/login IP + timestamp | Security forensics, lockout evidence (`BR-AUTH-04`) | CONFIDENTIAL | Postgres | AES-256 at rest | RC-02 | MASK-02 | Owner R own; Admin R platform scope |
| 11 | Push device token | Push delivery (`FR-017`) | CONFIDENTIAL | Postgres | AES-256 at rest; revoked on deletion | RC-04 | MASK-06 | System only |
| 12 | Bank-transfer reference | Admin verification of top-up (`BR-PAY-04`) | CONFIDENTIAL | Postgres | AES-256 at rest | RC-05 | MASK-01 | Admin/Super Admin; owner sees own |
| 13 | Wallet provider reference (m-Floos/OneCash) | Callback/poll correlation (`INT-REQ-001`) | CONFIDENTIAL | Postgres | AES-256 at rest; provider credentials separate (MASK-06) | RC-05 | MASK-02 | System, Admin |
| 14 | Wallet balance | Spendable funds | CONFIDENTIAL | Postgres | AES-256 at rest; row-locked atomic ops (`BR-PAY-05`) | RC-05 | MASK-05 | Owner R; Admin freeze only (`BR-PAY-09`) |
| 15 | Ledger posting (debit/credit pair) | Financial record of every movement | RESTRICTED | Postgres | AES-256 at rest; append-only, no UPDATE/DELETE (`DATA-REQ-007`) | RC-05 | MASK-05 | System W; parties R own; Admin aggregate R |
| 16 | Escrow hold / payable / payout row | 7-day hold & settlement (`C-12`, `BR-ESC-05`) | RESTRICTED | Postgres | AES-256; append-only corrections | RC-05 | MASK-05 | System W; Vendor R own; Finance/Admin R |
| 17 | Commission rate & monthly statement | Vendor economics (`BR-ESC-03`, `BR-FIN-04`) | INTERNAL | Postgres | Standard at-rest | RC-05 | MASK-05 | Vendor R own; Admin R |
| 18 | KYC document file (identity papers) | Vendor identity verification (`FR-007`) | RESTRICTED | MinIO | AES-256 object encryption; malware-scanned, EXIF-stripped (`SEC-REQ-011`) | RC-07 | MASK-03 (never copied) | Admin/Super Admin named reviewers only |
| 19 | KYC metadata (type, status, reviewer, timestamps) | Workflow & 48 h SLA evidence (`BR-VND-03`) | CONFIDENTIAL | Postgres | AES-256 at rest; audit-logged | RC-07 | MASK-02 | Vendor R own status; Admin RW |
| 20 | Store profile (name, branding, zones, settings) | Storefront identity (`FR-008`) | PUBLIC | Postgres | Standard at-rest | RC-04 | none needed | Owner RW*; Admin RW moderation |
| 21 | Product price / stock / SKU | Commerce core (`BR-CAT-04`, `BR-CAT-07`) | INTERNAL | Postgres, ES | Standard at-rest | RC-05 | keep or jitter numeric | Owner RW*; public R |
| 22 | Product image | Merchandising (`BR-CAT-08`) | PUBLIC | MinIO | Transport TLS; integrity by object key | RC-05 | reuse redaction set | Public R; Owner W |
| 23 | Review text + rating (1–5) | Social proof (`BR-REV-03`) | PUBLIC | Postgres, ES | Standard at-rest; moderation state controls visibility | RC-05 | MASK-04 on author name | Public R; author W once/7 d (`BR-REV-02`) |
| 24 | Review image (≤5, ≤5 MB) | Review evidence (`FR-006`) | PUBLIC | MinIO | Upload-validated (`SEC-REQ-011`) | RC-05 | redaction set | Public R; author W |
| 25 | Return evidence image | Return inspection (`FR-016`) | CONFIDENTIAL | MinIO | AES-256 object encryption | RC-05 | MASK-03 | Owner R own; Vendor R own return; Admin R |
| 26 | Coupon code + usage record | Promotions (`BR-PRM-01`) | INTERNAL / code CONFIDENTIAL when per-user | Postgres | Standard at-rest | RC-05 | keep | Owner RW*; Admin all |
| 27 | Order record (buyer contact, totals, state) | Fulfillment & finance (`C-10`, `C-09`) | CONFIDENTIAL | Postgres | AES-256 on contact columns | RC-05 | MASK-05 + MASK-04 | Parties per `DOC-DTA-003` §2 |
| 28 | Delivery confirmation code (6 digits) | Proof of delivery (`BR-SHP-02`, `C-16`) | RESTRICTED | Redis/Postgres | TTL-bound; 3 attempts → 24 h lock (`BR-SHP-03`); never logged | RC-01/02 | MASK-03 | Courier/System verify |
| 29 | Notification content & delivery status | User communication (`FR-017`) | CONFIDENTIAL (contains PII) | Postgres | AES-256 on body; provider sees only template + phone | RC-02 | MASK-04 | Recipient R own; System W |
| 30 | Support ticket & dispute text | Resolution (`FR-020`) | CONFIDENTIAL | Postgres | AES-256 at rest | RC-03 | MASK-04 | Requester R/W; Moderator/Admin RW |
| 31 | Audit log entry (actor, action, before/after, IP) | Accountability (`BR-PLT-06`, `SEC-REQ-010`) | RESTRICTED | Postgres | Append-only + hash chain; no secrets/full PII payloads (`SEC-REQ-010` R3) | RC-06 | MASK-05 | Per role scope; System W |
| 32 | Search index document | Discovery (`FR-009`) | INTERNAL | ES | Derived; no PII fields beyond display names | RC-08 | same as source | Read all; System W |
| 33 | Cache entry (catalog, profile, counters) | Performance & rate limits (`NFR-004`, `SEC-REQ-009`) | INTERNAL (CONFIDENTIAL if contains PII) | Redis | Volatile, TTL-bound; no secrets (`SEC-REQ-007` R4) | RC-08 | MASK-02 for PII keys | System only |
| 34 | BullMQ job payload | Async work (`C-20`) | INTERNAL | Redis | Owner-keyed; no secrets/PII beyond IDs | RC-08 | ID pseudonymization | System only |
| 35 | Application/audit-adjacent logs | Diagnostics (`NFR-014`) | INTERNAL (by construction) | Logs | **No PII, secrets, OTP, tokens** (`SEC-REQ-006` R5, `SEC-REQ-007` R4, `SEC-REQ-002` R4) | RC-02 | n/a — never contains PII | Ops |
| 36 | Metrics & dashboard series | SRE visibility (`INT-REQ-007`) | INTERNAL | Metrics | No PII in labels (`SEC-REQ-006` R5) | RC-03 | n/a | Ops, roles per `FR-018` |
| 37 | Backup set (WAL + snapshot) | Recovery (`DATA-REQ-004`) | RESTRICTED (inherits contents) | Backup storage | Encrypted at rest, operations-role access only | RC-09 | MASK-06 keys; no non-prod restores unmasked | Operations role |
| 38 | VAT/invoice records (`BR-FIN-01`) | Statutory tax evidence (`NFR-019`) | RESTRICTED | Postgres | AES-256; append-only corrections | RC-05 | MASK-05 | Finance/Admin R |

\* ES holds only element 6 (vendor/store display names) and catalog fields — customer PII is never indexed (`data-lifecycle.md` §3.9).

**Deliberately absent (never collected — `DATA-REQ-002` R3):** card numbers/PAN (`C-02`), GPS/coordinates/geo-fences (`C-16`, `BR-SHP-05`), biometric templates (`C-07`), national ID numbers (unless a future KYC requirement legally compels them — currently not collected; adding one requires a new inventory row + `DEP-09` legal review), email as identity (`BR-AUTH-08`).

## 5. Encryption & Key Expectations (summary of `SEC-REQ-006` / `SEC-REQ-007`)

| Layer | Expectation |
|---|---|
| In transit | TLS 1.3 everywhere: client↔API, service↔Postgres/Redis/ES/MinIO, provider callbacks |
| At rest | AES-256 for all CONFIDENTIAL/RESTRICTED elements (PII + financial fields) |
| Key management | Keys/certs outside code, repo, and database (`SEC-REQ-007`); never beside ciphertext (`SEC-REQ-002` R3) |
| Passwords | bcrypt cost 12 — never AES, never plaintext (`BR-AUTH-02`) |
| Backups | Encrypted at rest; restore without external key yields nothing readable (`SEC-REQ-002` R5) |

## 6. Leakage Rules — Redis, Elasticsearch, Logs, Metrics, Errors

| Channel | Rule | Ref |
|---|---|---|
| Application logs | No passwords, OTPs, tokens, provider credentials; no phone/address/PII payloads; IDs only | `SEC-REQ-002` R4, `SEC-REQ-006` R5, `SEC-REQ-007` R4 |
| Log integrity | Input validation/encoding prevents log-forging and injection through user-supplied strings | `SEC-REQ-008` |
| Audit trail | No secrets and no full PII payloads embedded in before/after values | `SEC-REQ-010` R3 |
| Error payloads / traces | Sanitized; stack details internal; correlation IDs instead of PII | `SEC-REQ-006` R5, `NFR-014` |
| Metrics labels | Cardinality-safe IDs only — never phone/user PII in label values | `SEC-REQ-006` R5 |
| Redis | TTL on every key; no plaintext passwords/OTP beyond their 5-min window; no secrets (`SEC-REQ-007` R4); cache never stores data that must survive (it is disposable, `DOC-DTA-001` §3) | `NFR-004`, `DATA-REQ-003` |
| Elasticsearch | Catalog + display-name fields only; a customer PII field in the index is a defect; purge on deletion within index-lag SLO | `FR-009`, `DOC-DTA-006` §5 |
| Export/analytics files | Generated through MASK-05; stored only where access is role-restricted; deleted after use | `FR-018`, `DATA-REQ-002` |
| CI/CD & repo | Secret scanning; no keys in source; sandbox credentials in non-prod | `SEC-REQ-007`, `SEC-REQ-012` |

## 7. Verification

- **Schema-to-purpose audit:** every PII column maps to an inventory row; unmapped-field report empty (`AC-DR002-01`).
- **Forbidden-field grep gate:** no card/lat/long columns or endpoints (`AC-DR002-02`).
- **Log-scan test:** zero occurrences of phone/OTP/password patterns in logs across the auth flow suite (`AC-SR002-02`).
- **Index-content test:** ES documents contain no customer phone/address fields.
- **Classification review:** any migration adding a column must add/adjust an inventory row (checked in migration review, `DATA-REQ-005`, `13-testing/`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
