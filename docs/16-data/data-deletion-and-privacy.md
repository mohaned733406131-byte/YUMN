---
document_id: DOC-DTA-006
title: Data Deletion, Anonymization & Privacy Procedures
category: 16-data
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [DATA-REQ-002, DATA-REQ-003, DATA-REQ-004, FR-003, FR-017, NFR-019, SEC-REQ-010]
related_documents: [DOC-DTA-001, DOC-DTA-002, DOC-DTA-004, DOC-DTA-005, DOC-DR-003, DOC-BA-005]
---

# DOC-DTA-006 — Data Deletion, Anonymization & Privacy Procedures

## 1. Purpose & Principles

Executable procedures for erasing or disidentifying personal data — the operational half of `DATA-REQ-003` and the account-deletion workflow of `FR-003`. Retention rules live in `retention-and-archival.md`; this document defines **what happens on request and on schedule**.

| # | Principle |
|---|---|
| P1 | Delete the **person**, preserve the **record**: financial/audit history survives in disidentified form (`DATA-REQ-003` R2/R3) |
| P2 | Erasure is never partial-by accident — every store that holds the data is touched in one operation (§5 cascade) |
| P3 | Every deletion produces evidence: actor, request ID, scope, counts, timestamp (`DATA-REQ-003` R5) |
| P4 | Anonymization must be **irreversible** — no mapping table, no recoverable key (§7) |
| P5 | Derived stores (ES, Redis, queues) are invalidated, never left to expire naturally (`DOC-DTA-002` §4) |
| P6 | Backups age out — residual copies are documented, not promised away (§5.5) |
| P7 | Non-production never sees unmasked production PII (§9) |

## 2. Account Deletion Request Flow (`FR-003`, `DATA-REQ-003`)

| Step | Actor | Action | System effect | Evidence |
|---|---|---|---|---|
| 1. Request | Customer | Initiates deletion in profile settings; explicit confirmation dialog | `deletion_request` row created (state `PENDING`) | Request ID + timestamp |
| 2. Identity proof | Customer | OTP verification (`SEC-REQ-001`); re-auth if session older than 15 min | Request moves to `VERIFIED`; failed OTP = rejected request | OTP attempt log (no code stored, `SEC-REQ-002` R4) |
| 3. Impact notice | System | Shows what will be erased, what is retained and why (orders/ledger ≥ 5 y), and the residual-backup window (≤ 35 days) | Consent/acknowledgement recorded on the request | Acknowledgement record |
| 4. Cooling window | System | **14 days** hold (`INFERENCE`) allowing withdrawal via login | State `COOLING`; account read-only | State history |
| 5. Liquidation guard | System | Outstanding obligations checked: open orders, active disputes, positive wallet balance, store with live orders | Blocking issues surfaced: wallet balance must be spent/refunded (wallet cannot pay out to bank — `BR-PAY-07`), store must be closed, KYC workflow terminated | Guard report |
| 6. Execution | System (job `system.privacy.erase`) | Cascade erase/anonymize across all stores (§5) | Primary PII removed; financial rows disidentified | Per-store counts |
| 7. Verification | System | Post-erase queries assert zero retrievable PII for the subject in each store (§6) | `VERIFIED_ERASE` state | Verification report attached to request |
| 8. Notification | System | SMS/WhatsApp confirmation to the phone **before** it is disidentified (sent in step 6 window) — if unreachable, in-app record only | Confirmation logged | Notification receipt (RC-02) |
| 9. Audit | System | One audit entry for the whole operation (subject pseudonym, steps, counts) | Append-only audit row (`SEC-REQ-010`) | Audit chain position |

**SLA:** execution completes within **30 calendar days** of step 2 (`INFERENCE` — `NFR-019` requires an account-deletion request "fulfilled within the published SLA" but no duration is stated anywhere in canon; the value must be published and confirmed with `DEP-09`). Two-person control (requester + Admin oversight) applies only to vendor/store closures with open financial exposure.

**Right of erasure is not absolute:** records under `RC-05`/`RC-06`/`RC-07` are retained per `retention-and-archival.md` §4 and are exempt until their floor elapses (`DATA-REQ-003` R3) — the request acknowledges this in step 3.

## 3. Deleted vs Anonymized Matrix

| Data category | On account deletion | On scheduled purge | Why |
|---|---|---|---|
| Password hash, refresh tokens, device tokens, sessions | **Hard-deleted** (also in Redis) | Hard-deleted | No residual purpose |
| Profile name, optional email, locale | **Anonymized** (MASK-04/MASK-02 overwrite) | Anonymized at RC-04 expiry | Referential role in history |
| Phone (primary identifier) | **Disidentified**: replaced by irreversible pseudonym; original destroyed | Same | Cannot stay unique — but must not be recoverable (`BR-AUTH-01` uniqueness applies to live accounts only; pseudonym collision avoided by salted token) |
| Address book rows | **Hard-deleted** | Hard-deleted at RC-04 | Pure PII, no record value |
| Orders (buyer contact, addresses) | **Disidentified** (tombstone kept: amounts, items, states, dates) | Purged at RC-05 expiry | Tax/dispute evidence (`NFR-019`) |
| Ledger / wallet / escrow / payout rows | **Untouched** (already pseudonymous once identity columns are disidentified) | Purged at RC-05 expiry | `DATA-REQ-007` immutability + ≥5 y floor |
| Audit entries | **Untouched**; subject appears as pseudonym going forward | Sealed purge at RC-06 expiry | `SEC-REQ-010` |
| KYC documents | **Hard-deleted** only if no open investigation; otherwise held to RC-07 | Deleted at RC-07 (5 y post-closure) | Fraud exposure vs minimization |
| Vendor store + products (store closure) | Store soft-deleted → products de-published (ES purged); images kept while order refs exist | Hard purge at RC-05 | Catalog history in orders |
| Reviews by the user | Kept (content) with **author name anonymized**; hidden on request (`BR-REV-04` moderation path) | Purged at RC-05 | Rating integrity (`BR-REV-05`) |
| Notification history / inbox | Hard-deleted (in-app rows) + device tokens | Status rows purged at RC-02 | Message bodies already gone |
| Support tickets | Requester link disidentified; text anonymized (MASK-04) | Purged at RC-03 | QA value retained de-identified |
| Backups containing the subject | **Not edited** — ages out within the 35-day snapshot window (WAL copy ≤ 14 days) | Automatic | Backup integrity (`DATA-REQ-004`) |
| Metrics/analytics aggregates | Untouched (already aggregate, no PII labels) | TSDB retention | `SEC-REQ-006` R5 |

## 4. Anonymization Technique (irreversibility)

1. **Pseudonymization:** phone/email/user key → `HMAC-SHA256(value, environment_erase_salt)` truncated to a stable `subject_ref` token; format-preserving so joins still work (MASK-02).
2. **Salt handling:** the erase salt is **per-subject derived and then destroyed** (stored only for the duration of the operation), so the mapping cannot be recomputed later — this is what makes step 1 irreversible in practice (§7).
3. **Free-text:** names/addresses in surviving free text (tickets, review bylines) replaced by synthetic values (MASK-04) before the original is overwritten.
4. **Overwrite then verify:** columns are overwritten in place (not nulled) so old values are not recoverable from `NULL` patterns; verification queries (§6) run immediately after.
5. **Objects (MinIO):** hard delete + version purge + orphan-key sweep; object keys are non-guessable so deletion, not renaming, is mandatory.

## 5. Cascade Across Stores

| Store | Action | Timing | Owner |
|---|---|---|---|
| Postgres | Delete rows (addresses, tokens, inbox) or overwrite PII columns (profile, orders, tickets); FK-safe order: children first | Same transaction batch where possible | System job |
| Redis | Delete session family, profile/cart/recommendation keys, rate-limit keys for subject; revoke refresh sessions (`BR-AUTH-07` pattern) | Within minutes of step 6 | System job |
| Elasticsearch | Delete vendor/store docs (closure), update review display names, remove follower edges; nightly rebuild as backstop | ≤ 5 minutes (index-lag SLO, `DOC-DTA-005` §5.6) | Indexer job |
| MinIO | Delete KYC objects (per matrix), orphan image objects; preserve order-referenced product images | Same run | System job |
| BullMQ | Cancel/drain pending jobs parameterized by `user_id`/`store_id`; queues drained before bulk purge (`DOC-DTA-005` §6 step 2) | Before step 6 commits | System job |
| Notifications (providers) | No provider-side erasure assumed beyond contract; delivery receipts age out at RC-02 | Scheduled | Ops |
| Backups | **No mutation.** Residual window ≤ 35 days documented on the request (§2 step 3, `DATA-REQ-004` R5) | Aging-out | Ops |

## 6. Verification & Audit of Deletion

- **Verification queries** (run per store, per request): profile table lookup by phone/email returns zero rows; ES `search_after` on subject tokens returns zero docs; Redis key scan on subject pattern returns zero keys; MinIO list on subject prefixes returns zero objects. Results stored with the request.
- **Evidence entry:** actor, request ID, per-store counts, duration, timestamp — satisfies `DATA-REQ-003` R5 and `AC-DR003-04`.
- **Audit entry:** one append-only row per deletion, subject referenced only by pseudonym (no full PII in audit — `SEC-REQ-010` R3).
- **Metrics:** `privacy_erasure_runs_total`, `privacy_erasure_rows_total{store}`, `privacy_erasure_failures_total` → Grafana (`INT-REQ-007`, `NFR-014`); failure alert routes to on-call.
- **Sampling QA:** monthly manual re-check of 5 random completed requests; zero-hit rule — any hit is a `HIGH`-severity incident logged in `09-security/` findings and `20-validation/`.
- **Purge-vs-request guard:** scheduled purge jobs emit the same evidence so both paths are demonstrable (`AC-DR003-01`).

## 7. Hard-Delete, Tombstone & Re-Deanonymization Prohibition

| Mechanism | Definition | Used for |
|---|---|---|
| **Hard delete** | Row/object removed physically | Pure PII with no record value: addresses, tokens, sessions, inbox, KYC on expiry |
| **Tombstone** | Row retained, identity columns disassociated, business columns intact, `erased_at` stamped | Orders, ledger-linked records, audit subject references — anything inside `RC-05`/`RC-06` |
| **Soft delete** | Row marked inactive but fully recoverable (product `BR-CAT-06`) | Catalog only — **never** applied to personal-data erasure |

**Prohibition:** no process, job, admin tool, or support workflow may reconstruct an erased subject's identity from tombstones, backups, logs, or analytics. Concretely: (a) no mapping table or recoverable salt is retained after step 6; (b) restoring a pre-erasure backup over a post-erasure database is forbidden without a privacy review — quarterly restore drills (`DATA-REQ-004` R4) must be executed on backups **or** masked copies, never re-introducing erased PII into production; (c) support tooling has no "reveal erased user" capability — none is to be built. Violations are security findings (`SEC-nnn`, `09-security/`).

## 8. Right of Access / Data Export (`INFERENCE`)

`NFR-019` requires a documented, testable "data export/erasure rights path". v1 defines export as: authenticated customer requests a machine-readable archive (JSON) of profile, addresses, orders, wallet transactions, reviews, and tickets; generated by an async job (`system.privacy.export`), delivered as a MinIO pre-signed download valid 72 hours, itself logged as an audit event. Contains **only the requester's own data** (ownership tests apply). Export availability, format, and SLA are `INFERENCE` — no functional requirement mandates it; confirm scope with `DEP-09` before publishing.

## 9. Consent & Preference Records

| Record | Handling |
|---|---|
| Account creation (terms/privacy acceptance) | Stored as timestamped event with policy version; retained with account lifecycle (RC-04) + 12 months after erasure as proof of basis (`INFERENCE`) |
| Marketing/notification opt-outs per channel (`BR-NTF-05`) | Retained **after** deletion of the profile if the number may re-register — prevents re-spam; kept 24 months (`INFERENCE`) |
| Security notices (`BR-NTF-02`) | Not consent-gated; cannot be opted out |
| Consent evidence on deletion request | Attached to the request record, itself purged at RC-03 expiry once superseded by the audit entry |

## 10. PII in Non-Production Environments

| Rule | Detail |
|---|---|
| No raw production copies | Non-prod databases are seeded synthetically; restoring a production dump into dev/staging is forbidden (`SEC-REQ-006`, `DATA-REQ-002`) |
| Masking on any exception | If a masked restore is approved for a specific test need, apply per-element rules from `data-classification.md` §3: phone/email → MASK-02, names/addresses → MASK-04, KYC/OTP/secrets → MASK-03/MASK-06, financial identifiers → MASK-05, with amounts preserved only where the test requires them |
| Verification before first use | Scan script asserts zero unmasked phone patterns (`^7[0-9]{8}$`), email patterns, and KYC file keys in the non-prod dataset; scan result attached to the environment checklist (`14-devops-infrastructure/`) |
| Secrets | MASK-06 always: sandbox credentials for payment/SMS providers (`DEP-05`, `DEP-06`); production secrets never present outside production (`SEC-REQ-007`) |
| Logs in non-prod | Same logging rules as production (no PII/secrets) so debugging habits never diverge |

## 11. Verification Summary

- Deletion integration test: seeded subject → run flow → all §6 queries zero-hit; financial rows intact (`AC-DR003-02`, `AC-FR003-04`).
- Irreversibility review: no salt/mapping retained; code review of `system.privacy.erase`.
- Export test: archive contains only requester-owned records.
- Non-prod scan test: zero unmasked PII patterns in dev/staging seed.
- Evidence test: every run writes the evidence entry (`AC-DR003-04`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
