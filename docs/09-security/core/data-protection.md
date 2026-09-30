---
document_id: DOC-SEC-006
title: Data Protection — Encryption, Hashing & Log Masking
category: 09-security
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [SEC-REQ-002, SEC-REQ-006, SEC-REQ-007, SEC-REQ-010, FR-013, NFR-019]
related_documents: [DOC-SEC-001, DOC-SEC-005, DOC-SEC-007, DOC-SR-006, DOC-BA-005, DOC-OVR-008]
---

# Data Protection — Encryption Design (`SEC-REQ-006`)

How yumn protects data in transit, at rest, and in derived stores; what is hashed instead of stored; what is deliberately *not* encrypted. Requirement statements/ACs: `../../02-requirements/core/SEC-REQ-006.md`; classification detail belongs to `16-data/data-classification.md`.

## 1. In Transit — TLS

| Path | Requirement | Canon |
|---|---|---|
| Client ↔ edge/API (web, RN apps, admin console) | **TLS 1.3 only** on all external hosts; HTTP→HTTPS redirect; HSTS on every response; TLS 1.2 and below refused | `SEC-REQ-006` R1, `AC-SR006-01` |
| Provider callbacks ↔ yumn (m-Floos/OneCash, SMS DLRs, WhatsApp status) | HTTPS only, HMAC signature mandatory; unsigned/HTTP callbacks rejected 401 | `INT-REQ-001`, `INT-REQ-006` |
| API ↔ PostgreSQL | `sslmode=require` (target `verify-full` when CA distribution is automated); plaintext connection refused | `SEC-REQ-006` R3, `AC-SR006-03` |
| API ↔ Redis | TLS-required connection (`DEP-03`); plaintext refused | `SEC-REQ-006` R3 |
| API ↔ Elasticsearch / MinIO | Encrypted transport to both services; credentials sent only over TLS | `SEC-REQ-006` R3, `DEP-04`, `DEP-07` |
| Internal service-to-service (monolith containers on one host) | Loopback + Docker network isolation; TLS target ≥1.2 with 1.3 preferred (`INFERENCE` — canon fixes 1.3 for *external* hosts; internal links are constrained by single-host Compose under `C-22`) | `INFERENCE` |
| Certificates | Issued via `DEP-08`; expiry monitored with alerts before expiry | `SEC-REQ-006` R4, `C-26` |

No plaintext HTTP endpoint exists anywhere; any new route inherits HSTS + redirect by default (control `SEC-C-05`).

## 2. At Rest — What Is Encrypted

| Store | Data | Mechanism | Notes |
|---|---|---|---|
| PostgreSQL 16 | Classified PII: phone numbers, names, addresses, KYC references (`A-06`, `A-07`) | AES-256 **field-level** encryption for classified columns + disk/volume encryption for the data directory | Keys held **outside** the database, never beside the ciphertext (`SEC-REQ-002` R3, `SEC-REQ-007`) |
| PostgreSQL 16 | Financial records: wallet, ledger, escrow, payouts | Volume encryption at rest; amounts are not field-encrypted (they must be aggregated/queried by reconciliation jobs `BR-ESC-08`) — integrity is the priority and is enforced append-only (`DATA-REQ-007`) | `INFERENCE` — balance of confidentiality vs `NFR-008`/reconciliation |
| MinIO (`DEP-07`) | KYC documents, bank-transfer receipts, product/review images | Server-side encryption at rest (SSE) for all buckets; KYC bucket additionally private + presigned-URL only | Presigned URL exposure risk tracked `SEC-008` |
| Backups (WAL + daily snapshots) | Full copies | Encrypted at rest with keys distinct from production keys; restore drills verify key availability | `DATA-REQ-004`, `AC-SR006-02` |
| Redis 7 | Session registry, OTP values, rate counters | Not persisted as system of record: `appendonly no` for PII-bearing keys, TTL-bound, disk encryption if persistence enabled for BullMQ | See §6 |

## 3. At Rest — What Is Deliberately NOT Encrypted (and why)

| Data | Why not | Guard instead |
|---|---|---|
| Product catalog, categories, banners, prices | Public marketplace content by design | Integrity via Prisma/DB constraints (`DATA-REQ-001`) |
| Search index documents (public fields) | Derived from public catalog; encrypting breaks ES scoring/analyzers | Only public fields are indexed — PII minimization (`DATA-REQ-002`); PII-in-index risk tracked `SEC-007` |
| Order line items / shipping address in order records | Required for fulfillment queries and timelines | Access scoped by ownership (`DATA-REQ-008`, `BR-ORD-09`); field-level encryption reserved for classified identity columns |
| Metrics labels & aggregated reports | Must be queryable; cardinality-limited | Label allowlist, no PII (`INT-REQ-007`, `SEC-REQ-006` R5) |
| Audit log payload values | Must remain verifiable/chain-checkable | Hash chain + append-only privileges (`SEC-REQ-010`); entries carry no full PII payloads (R3) |

## 4. Hashing & Tokenized Storage

| Secret | Storage form | Parameters | Canon |
|---|---|---|---|
| Passwords | bcrypt hash | **cost 12**; verified by re-hash in tests | `BR-AUTH-02`, `SEC-REQ-002` R1 |
| OTP codes | value in Redis with **TTL = 5 min**; never in PostgreSQL; never in logs | 6 numeric digits; single-use; attempt counter alongside | `BR-AUTH-03`, `SEC-REQ-002` R4 |
| Password-reset tokens | single-use, short-TTL store; invalidation clears all sessions | — | `BR-AUTH-07` |
| **Delivery code (6-digit)** | **Hashed, never plaintext** — stored as a keyed hash over (code + shipment ID) so a DB dump yields no usable codes; verification compares hashes with attempt counter | 3 attempts → 24 h lock (`BR-SHP-03`); code excluded from logs | `INT-REQ-005` ("stored hashed, not in logs"), `SEC-REQ-005` R3 |
| Refresh tokens | random opaque value; DB stores only a hash + family id + used-flag | single-use rotation; reuse ⇒ family revocation | `BR-AUTH-05`, `SEC-REQ-003` R2 |
| Idempotency keys | stored as issued (not secret material) | unique constraint | `BR-PLT-03` |

## 5. Field-Level Encryption Scope

| Column class | Examples | Treatment | Key custody |
|---|---|---|---|
| Identity PII | phone, full name, address lines | AES-256 field-level; deterministic option only where exact-match lookup is required (`INFERENCE` — search must use hashed index or exact match) | Data key wrapped by key-encryption key held in env/key service (`S-12` in `secrets-management.md`) |
| KYC references & document pointers | document object key, document numbers | AES-256 field-level; MinIO object keys never enumerable | same |
| Bank references | bank name/reference used for top-up verification | AES-256 field-level; duplicate-reference uniqueness checked on the **hash**, not plaintext | same |
| Ledger amounts, wallet balances | — | **not** field-encrypted (aggregation/reconciliation requirement) | volume encryption + append-only |
| Secrets/credentials | provider keys | never in DB at all | env only (`SEC-REQ-007`) |

Re-encryption on key rotation is a batch job with progress logging; absence of a defined re-encryption procedure is tracked in `SEC-014`.

## 6. Redis Non-PII Policy

- Redis is cache, OTP carrier, rate-limit counter, session registry, and BullMQ backend (`DEP-03`) — **not** a PII store.
- Allowed values: opaque IDs (user UUID, session id), OTP digits (TTL 5 min), counters, serialized job payloads referencing IDs — job payloads must not embed phone numbers, addresses, or names (`INFERENCE`, extends `SEC-REQ-006` R5).
- Phone numbers appear in Redis only inside the short-lived OTP send path keyed by a hashed phone key (`INFERENCE`), evicted at TTL.
- Persistence: AOF/RDB disabled for PII-bearing instances unless required by BullMQ durability; any enabled persistence is disk-encrypted.
- Verification: sample scan of Redis keys/dumps for phone/address patterns in tests.

## 7. PII Masking in Logs, Metrics & Errors

| Surface | Rule | Example |
|---|---|---|
| Structured logs | Mask identifiers: keep last 3 digits only | `7712****9` |
| Correlation IDs | Opaque UUID; no embedded phone/order PII | `corr=8f3a…` |
| Metric labels | Allowlist (service, endpoint, status class, queue); zero PII | `http_requests_total{route="/api/v1/topups",status="429"}` |
| Error payloads | Stable error codes + localized message; no internal detail | `OTP_INVALID` |
| Provider logs | Request/response bodies redacted; signature headers truncated | — |
| Audit entries | actor id, action, entity ref, before/after **values diffed and scrubbed**, IP, timestamp — no secrets, no full PII payloads | `SEC-REQ-010` R3 |

Enforcement: automated log scan asserting zero phone/password/OTP patterns (`AC-SR002-02`, `AC-IR007-03`).

## 8. Backups & Key Management Responsibilities

| Aspect | Design | Canon |
|---|---|---|
| Backup contents | Continuous WAL + daily snapshots of PostgreSQL; MinIO bucket replication for documents | `DATA-REQ-004` |
| Backup encryption | Encrypted at rest with keys **separate** from production data keys; a backup is useless without the key custodian | `SEC-REQ-006` R2, `SEC-REQ-007` |
| Key custody | DevOps/ops owner holds key material; application receives keys via environment at runtime; **DB credentials alone never decrypt classified columns** | `AC-SR002-03` |
| Rotation | Per `secrets-management.md` §2 (S-12: annual / on algorithm change); rotation triggers batch re-encryption | `SEC-REQ-007` R5 |
| Recovery | Restore drills must prove decryption works post-restore (key availability is part of the drill) | `DATA-REQ-004`, `NFR-006` |
| Audit chain protection | Audit table privileges: app role has INSERT + SELECT only; chain verification job recomputes hashes | `SEC-REQ-010` R1/R4 |
| Compliance | PDPA (Law 11/2012) control specifics remain `INSUFFICIENT EVIDENCE` pending `DEP-09`; no PCI-DSS scope exists (`C-02`) | `SEC-REQ-006` R6, `NFR-019` |

## 9. Verification Summary

| Check | Method | Canon |
|---|---|---|
| TLS 1.3-only external, redirect, HSTS | automated TLS scan in CI | `AC-SR006-01` |
| Classified columns are ciphertext in raw dump | backup/extract inspection | `AC-SR006-02`, `AC-SR002-03` |
| Plaintext DB/Redis connection refused | connection attempt test | `AC-SR006-03` |
| Certificate near-expiry alerts | cert-monitoring alert test | `AC-SR006-04` |
| bcrypt cost 12, no plaintext column | storage inspection + re-hash | `AC-SR002-01` |
| Zero password/OTP/phone in logs | CI log scan | `AC-SR002-02` |
| Delivery code & refresh tokens stored hashed | schema/storage inspection | `INT-REQ-005`, `SEC-REQ-003` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
