---
document_id: DOC-SEC-007
title: Security Control Catalog (SEC-C-01 … SEC-C-24)
category: 09-security
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-002, SEC-REQ-003, SEC-REQ-004, SEC-REQ-005, SEC-REQ-006, SEC-REQ-007, SEC-REQ-008, SEC-REQ-009, SEC-REQ-010, SEC-REQ-011, SEC-REQ-012]
related_documents: [DOC-SEC-001, DOC-SEC-003, DOC-SEC-004, DOC-SEC-005, DOC-SEC-006, DOC-SEC-008, DOC-SR-000]
---

# Security Control Catalog

Every control traces to at least one `SEC-REQ-*`; every `SEC-REQ-*` is covered by ≥1 control. **Status of every control in v1.0 is `DESIGNED`** — no implementation exists yet (root README §6), and none may be marked `IMPLEMENTED`/`VERIFIED` before the corresponding test in `13-testing/` passes.

## 1. Control Catalog

| ID | SEC-REQ | Control | Implementation layer | Status | Verification method |
|---|---|---|---|---|---|
| SEC-C-01 | 001 | OTP issue/verify pipeline: 6 digits, 5-min TTL, 3 attempts, 60 s cooldown, ≤3 resends/10 min, purpose-bound, single-use | Node (auth module) + Redis counters | DESIGNED | Negative OTP tests `AC-SR001-01/02`, log scan |
| SEC-C-02 | 001 | OTP failover delivery: SMS primary → secondary SMS → WhatsApp inside validity window; failover never duplicates a successful send | Node (SmsProviderPort adapter) | DESIGNED | Failover test `AC-SR001-05`, `AC-IR003-01/02` |
| SEC-C-03 | 002 | Credential storage: bcrypt cost 12 only; no plaintext password column anywhere; never logged/returned | Node (crypto) + DB schema | DESIGNED | Storage inspection `AC-SR002-01`, log scan `AC-SR002-02` |
| SEC-C-04 | 002, 006 | Field-level AES-256 encryption of classified PII/KYC/bank-reference columns; keys outside the DB | Node (crypto service) + DB | DESIGNED | Raw-dump inspection `AC-SR002-03`, `AC-SR006-02` |
| SEC-C-05 | 006 | Edge TLS 1.3-only + HTTP→HTTPS redirect + HSTS on every response; cert-expiry alerting | WAF/CDN (`DEP-08`) + edge config | DESIGNED | CI TLS scan `AC-SR006-01`, cert alert test `AC-SR006-04` |
| SEC-C-06 | 006 | Encrypted transport to PostgreSQL/Redis/ES/MinIO; plaintext connections refused | process config (`sslmode=require` etc.) | DESIGNED | Connection attempt test `AC-SR006-03` |
| SEC-C-07 | 003 | JWT RS256 algorithm-pinned, 15-min access, 7-day refresh, issuer/audience checked, deny-by-default validation | Node (auth guard) | DESIGNED | Lifetime boundary + tamper vectors `AC-SR003-01/04` |
| SEC-C-08 | 003 | Refresh single-use rotation with family revocation + user alert on reuse | Node + Redis/DB session registry | DESIGNED | Rotation-reuse test `AC-SR003-02`, `AC-FR001-03` |
| SEC-C-09 | 003 | Session registry: ≤5 devices, oldest eviction, global invalidation on password reset | Node + Redis/DB | DESIGNED | Device-limit + revocation tests `AC-SR003-03/05` |
| SEC-C-10 | 004 | Deny-by-default RBAC guard at route level; every endpoint maps to exactly one decision per role | Node (guards, `DOC-BE-004`) | DESIGNED | Matrix sweep `AC-SR004-01`, fail-closed `AC-SR004-04` |
| SEC-C-11 | 004 | Resource-ownership predicate (`user_id`/`store_id`/assignment) evaluated in every service query | Node (service layer) + DB queries | DESIGNED | IDOR suite `AC-SR004-02`, `AC-FR002-01/02` |
| SEC-C-12 | 005 | Account lockout: 5 consecutive failures → 15-min automatic lock; lock events logged | Redis counters + Node | DESIGNED | Lockout persistence test `AC-SR005-01` |
| SEC-C-13 | 005 | Delivery-code lockout: 3 failures → 24 h confirmation lock + auto support ticket | Node (shipping module) | DESIGNED | `AC-SR005-03`, `AC-IR005-03` |
| SEC-C-14 | 007 | Runtime-only secret injection via env/`env_file`; fail-fast startup; no defaults | process (Compose env under `C-22`) | DESIGNED | Startup test `AC-SR007-02`, repo audit `AC-SR007-03` |
| SEC-C-15 | 007 | CI secret scanning on every change; seeded canary blocks merge | CI (GitHub Actions) | DESIGNED | Canary pipeline test `AC-SR007-01` |
| SEC-C-16 | 008 | Parameterized queries only (Prisma); lint rule bans string-built SQL in the repository layer | Node (repository) + DB | DESIGNED | SQLi suite `AC-SR008-01`, static lint `AC-SR008-04` |
| SEC-C-17 | 008 | Context-aware output encoding for all UGC (ar/en, LTR/RTL) + CSP without `unsafe-inline` | Node (headers) + client rendering | DESIGNED | Stored-XSS browser test `AC-SR008-02` |
| SEC-C-18 | 008 | CSRF: SameSite cookies (defense in depth) **plus** synchronizer/double-submit token on every cookie-auth state change | Node (guard) + client | DESIGNED | CSRF negative test `AC-SR008-03` |
| SEC-C-19 | 008 | Input validation at the edge of business logic: type, length, range, format (`^7[0-9]{8}$`, integer YER bounds) | Node (DTO validation, `DOC-BE-009`) | DESIGNED | Boundary/negative tests across endpoints |
| SEC-C-20 | 009 | Rate-limit budgets (§3) in Redis, per IP and per account, 429 + `Retry-After`, applied before expensive logic | Node (middleware) + Redis | DESIGNED | Threshold tests `AC-SR009-01/02`, bypass `AC-SR009-03` |
| SEC-C-21 | 010 | Append-only audit: INSERT+SELECT-only DB role, hash chain, verification job, ≥5-year retention | DB privileges + Node (audit writer) | DESIGNED | Permission test `AC-SR010-01`, tamper test `AC-SR010-02` |
| SEC-C-22 | 011 | Upload pipeline: jpg/png/webp ≤5 MB, magic-byte + declared-type check, EXIF strip, no SVG/HTML, AV scan before retrievable, inert serving | Node (upload service) + MinIO (`DEP-07`) | DESIGNED | `AC-SR011-01…04` |
| SEC-C-23 | 012 | CI security gates: SAST + dependency/SCA on every PR (merge-blocking) and DAST against staging per release (promotion-blocking) | CI (GitHub Actions) | DESIGNED | Gate tests `AC-SR012-01/02` |
| SEC-C-24 | 012 | Remediation SLA: CRITICAL ≤ 7 days; HIGH ≤ 30 days (`INFERENCE`); periodic base-image/dependency upgrade review | process (security owner) | DESIGNED | SLA evidence review `AC-SR012-03/04` |

## 2. Coverage Check — SEC-REQ → Controls

| SEC-REQ | Controls | SEC-REQ | Controls |
|---|---|---|---|
| 001 | C-01, C-02 | 007 | C-14, C-15 |
| 002 | C-03, C-04 | 008 | C-16, C-17, C-18, C-19 |
| 003 | C-07, C-08, C-09 | 009 | C-20 (+ C-01, C-12 budgets) |
| 004 | C-10, C-11 | 010 | C-21 |
| 005 | C-12, C-13 (+ C-01, C-20) | 011 | C-22 |
| 006 | C-04, C-05, C-06 | 012 | C-23, C-24 |

## 3. Rate-Limit Budgets (`SEC-REQ-009`, `SEC-C-20`)

| Route / surface | Budget | Key | Justification |
|---|---|---|---|
| Standard API (default) | **100 req/min** | per IP **and** per user | The canonical standard in `SEC-REQ-009` R1 — baseline for all non-special routes |
| OTP request (send) | **3 per 10 min per phone** + 60 s cooldown | per phone + per IP (10/10 min) | Directly `BR-AUTH-03`; prevents SMS pumping and OTP bombing (`TM-02`); IP dimension defeats number-rotation attacks (`INFERENCE` for the IP figure) |
| OTP verify | **3 attempts per code** | per code + per account | `BR-AUTH-03` — a 6-digit code is 10⁶ space; 3 attempts per code with fresh-code reset bounds online guessing |
| Login | **5 per 15 min** | per account + per IP | Mirrors `BR-AUTH-04` lockout so the limiter and the lockout never disagree; IP key catches distributed password spraying (`INFERENCE` for IP figure) |
| Top-up initiation | **10 per min** per user | per user + per IP | Money path: cheaper to throttle than to reconcile fraudulent initiations; stricter than standard per `SEC-REQ-009` R2 and `INT-REQ-001` rate-limit expectation (`INFERENCE` for the figure) |
| Checkout / order creation | **10 per min** per user | per user | Money + stock-reservation side effects (`C-13`); prevents reservation hoarding (`TM-11`) (`INFERENCE`) |
| Search / catalog browse | **60 per min** per user | per user + per IP | Below standard because each query hits Elasticsearch (`DEP-04`); still generous for human browsing; blocks scraping (`TM-11`) (`INFERENCE`) |
| Delivery-code verification | **3 attempts per shipment** | per shipment | `BR-SHP-03` — not a rate but an attempt cap; 24 h lock + auto ticket |
| Inbound webhooks | Per-provider IP allowlist + body-size cap; no generic per-IP throttle | per provider | Provider retries must never be mistaken for abuse; authenticity comes from HMAC, not from quotas (`INT-REQ-006`) |
| File upload | ≤5 MB per file, ≤10 per product / ≤5 per review, per-user upload rate `INFERENCE` | per user | `BR-CAT-08`, `BR-REV-03`, `SEC-REQ-011` |

**Cross-cutting rules:** counters live in Redis and are shared across replicas (`NFR-018`, `AC-SR009-03`); exceeded ⇒ `429` + `Retry-After` emitted **before** expensive business logic; 429 bursts are exported as metrics and alerted (`SEC-REQ-009` R5); budgets must not throttle the legitimate 10,000-user load test (`AC-SR009-04`, `C-25`).

## 4. Input Validation, Output Encoding & CSRF (detail)

**Input validation (`SEC-C-19`)** — DTO/schema validation before business logic (`DATA-REQ-001`): string length caps, enum membership, integer ranges (top-up 1,000–5,000,000 `BR-PAY-02`; order 500–5,000,000 `C-14`), phone regex `^7[0-9]{8}$` (`BR-AUTH-01`), idempotency-key presence for money/order routes (`BR-PLT-03`). Reject with stable localized error codes (`BR-PLT-05`) — never partial processing.

**Output encoding — Arabic/RTL-safe XSS defense (`SEC-C-17`)** —
- Context-aware encoding on render for **all** UGC: product names, review text, store profiles, coupon descriptions, support replies.
- RTL-specific hygiene: strip/bidirectionally neutralize U+202E–U+202F override characters in stored UGC before rendering (`INFERENCE` — prevents display spoofing in Arabic text), never interpret UGC as HTML/markup regardless of locale.
- JSON API responses with correct content types; no server-side HTML templating of user data.
- CSP: `default-src 'self'`; scripts without `unsafe-inline`; images from MinIO bucket origin only; `object-src 'none'`; `frame-ancestors 'none'` on admin routes (`INFERENCE` for exact directives).

**CSRF (`SEC-C-18`)** —
- Web surfaces authenticate with httpOnly + SameSite cookies (`SEC-REQ-003` R5) ⇒ SameSite is the **first** layer only.
- Every state-changing request from a cookie-authenticated web client additionally requires a CSRF token (synchronizer pattern, per `SEC-REQ-008` R4); missing/invalid ⇒ 403 (`AC-SR008-03`).
- Native RN clients are exempt (no ambient cookie credential) — they send credentials in explicit headers (`INFERENCE`).
- GET never mutates state (enforced by route review).

## 5. File Upload Controls (`SEC-REQ-011`, `SEC-C-22`)

| Step | Control |
|---|---|
| 1. Accept | jpg/png/webp only; ≤5 MB; count limits (`BR-CAT-08`, `BR-REV-03`); applies to KYC docs & bank receipts too (`FR-007`, `INT-REQ-002`) |
| 2. Validate | declared content type **and** magic bytes; double-extension/spoofed extension rejected; **no SVG/HTML/active vectors** ever accepted |
| 3. Sanitize | EXIF (incl. GPS) stripped before storage |
| 4. Scan | malware scan completes **before** the object becomes retrievable; infected ⇒ quarantine + reject + ops alert |
| 5. Store | MinIO (`DEP-07`), private bucket, presigned upload/download; object names are server-generated (no client path traversal) |
| 6. Serve | inert content type, `Content-Disposition` discipline, separate origin from the app where possible (`INFERENCE`) so nothing executes on the platform origin |

## 6. Vulnerability Management (`SEC-REQ-012`)

| Gate | Trigger | Blocking behavior |
|---|---|---|
| SAST + dependency/SCA | every pull request | new critical/high exposure ⇒ red build, merge blocked (`AC-SR012-01`) |
| Secret scan (C-15) | every change | any hit ⇒ merge blocked |
| DAST | staging, per release | open critical finding ⇒ no production promotion (`AC-SR012-02`) |
| Module-boundary lint | every PR | vendor SDK outside adapter folder / raw SQL concat ⇒ build fails (`AC-IR008-01`, `AC-SR008-04`) |
| SLA tracking | on confirmation | CRITICAL ≤ 7 days (registry), HIGH ≤ 30 days (`INFERENCE`), monthly severity report with no silent suppressions (`AC-SR012-03/04`) |

Tooling is GitHub Actions (project CI canon); exact tool selection and pipeline wiring belong to `../../14-devops-infrastructure/core/ci-cd.md`.

## 7. Change Control

Adding/removing/altering a control: update this catalog, bump version, add a Change History row, and propagate to `13-testing/` (new test) and, if a requirement is affected, to `02-requirements/` — never silently (root README §9).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
