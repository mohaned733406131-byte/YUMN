---
document_id: DOC-SEC-008
title: Security Findings Register (SEC-001 … SEC-015)
category: 09-security
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-003, SEC-REQ-004, SEC-REQ-007, SEC-REQ-008, SEC-REQ-009, SEC-REQ-010, SEC-REQ-011, SEC-REQ-012]
related_documents: [DOC-SEC-001, DOC-SEC-002, DOC-SEC-003, DOC-SEC-005, DOC-SEC-006, DOC-SEC-007, DOC-IR-003, DOC-OVR-010]
---

# Security Findings Register

Design-level findings raised while analyzing the yumn architecture against its own canon. **Every finding below is `OPEN`** — none is fixed, mitigated in code, or verified; no implementation exists yet. Findings are discovered by analysis, not by scanning; they complement (and feed) the vulnerability-management process of `SEC-REQ-012` and may be linked to `17-risk-management/risk-register.md` where they threaten objectives.

**Severity** = impact × likelihood *if the gap is exploited as designed today*. Reclassify only with evidence, bumping the version and adding a Change History row.

## Summary

| ID | Title | Severity | Affected area | Status |
|---|---|---|---|---|
| SEC-001 | Account recovery depends entirely on SMS availability (no email channel) | HIGH | Authentication, Notifications | OPEN |
| SEC-002 | Ledger/audit immutability rests solely on database privileges | MEDIUM | Financial data, Audit | OPEN |
| SEC-003 | Admin console shares origin with the public API | MEDIUM | Admin console, Sessions | OPEN |
| SEC-004 | Delivery code and OTP are interceptable via SIM swap | HIGH | Delivery, Authentication | OPEN |
| SEC-005 | Webhook replay window and nonce handling are unspecified | MEDIUM | Integrations, Wallet | OPEN |
| SEC-006 | OTP resend cooldown lacks a distributed per-destination guard | MEDIUM | Authentication, Rate limiting | OPEN |
| SEC-007 | Elasticsearch index content may include PII with no defined protection | MEDIUM | Search, Data protection | OPEN |
| SEC-008 | MinIO bucket exposure via listing/presigned URLs | MEDIUM | File storage, KYC | OPEN |
| SEC-009 | Refresh-token reuse detection is clock-skew sensitive | LOW | Sessions | OPEN |
| SEC-010 | CORS policy is unspecified anywhere in the canon | MEDIUM | API, Browser security | OPEN |
| SEC-011 | The sole authentication channel (DEP-06) is uncontracted and unvalidated | CRITICAL | Authentication, Dependency | OPEN |
| SEC-012 | Login is single-factor for privileged roles; OTP-at-login canon ambiguity | HIGH | Authentication, Admin console | OPEN |
| SEC-013 | Per-route rate-limit budgets are design-level and unvalidated under load | LOW | Rate limiting | OPEN |
| SEC-014 | Field-encryption key rotation and re-encryption procedure undefined | MEDIUM | Data protection, Secrets | OPEN |
| SEC-015 | Escrow release job may race dispute creation (TOCTOU on funds) | HIGH | Escrow, Financial integrity | OPEN |

---

## SEC-001 — Account recovery depends entirely on SMS availability
**Severity:** HIGH · **Area:** Authentication, Notifications · **Status:** OPEN

- **Description:** There is no email channel in v1 (`BR-NTF-01`, `GAP-03`, `C-06`), so password reset and every OTP-delivered verification flow ride on SMS with WhatsApp failover only (`BR-NTF-03`). If both providers are degraded, there is **no third recovery path** — users are locked out until carriers recover.
- **Impact:** Availability of authentication equals availability of `DEP-06`; mass lockout support load; reputational damage; pressure to weaken controls (e.g., disabling lockouts) during outages.
- **Recommendation:** Treat SMS/WhatsApp health as an authentication SLO (alert on send-failure rate); publish honest user messaging for outage windows; pre-build support tooling that assists lockouts without bypassing rules (`SEC-REQ-005` R5); track a formal gap entry in `20-validation/missing-information.md` for a v2 recovery channel.
- **Related:** `SEC-REQ-001`, `SEC-REQ-005`, `FR-001`, `FR-017`, `BR-NTF-01`, `BR-NTF-03`, `C-06`, `DEP-06`.

## SEC-002 — Ledger/audit immutability rests solely on database privileges
**Severity:** MEDIUM · **Area:** Financial data, Audit trail · **Status:** OPEN

- **Description:** Append-only guarantees (`DATA-REQ-007`, `SEC-REQ-010` R1) are enforced by withholding UPDATE/DELETE from the application role and by a hash chain. A superuser/host-level operator can still rewrite rows and recompute the chain; there is no external anchor (WORM storage, off-host signed checkpoint).
- **Impact:** Insider or host-compromise tampering could hide theft; the 5-year evidentiary value (`NFR-019`) is only as strong as the host.
- **Recommendation:** Ship the daily chain-verification job as mandatory (not optional); export signed chain checkpoints to separate storage; restrict PostgreSQL superuser access and log its use; consider off-host anchoring in v2.
- **Related:** `SEC-REQ-010`, `DATA-REQ-007`, `BR-PAY-06`, `BR-PLT-06`, `NFR-019`.

## SEC-003 — Admin console shares origin with the public API
**Severity:** MEDIUM · **Area:** Admin console, Sessions · **Status:** OPEN

- **Description:** Nothing in the canon separates the admin console (`FR-020`) from the public API origin; cookies and CSP are therefore shared across a high-privilege surface and an internet-facing one. Any XSS on a public route (TM-09) becomes a path to admin session material.
- **Impact:** A single XSS or CSRF defect escalates from customer to ADMIN/SUPER_ADMIN context — refunds, KYC, payouts, role management.
- **Recommendation:** Serve the console from a separate origin with its own cookie scope and strict CSP, or at minimum distinct cookies + `frame-ancestors 'none'` + dedicated rate budgets; revisit with `SEC-012` (step-up factor).
- **Related:** `SEC-REQ-003`, `SEC-REQ-004`, `SEC-REQ-008`, `FR-020`, `rbac.md` §8.

## SEC-004 — Delivery code and OTP are interceptable via SIM swap
**Severity:** HIGH · **Area:** Delivery, Authentication · **Status:** OPEN

- **Description:** Both the 6-digit delivery code (`BR-SHP-02`, `C-16`) and OTPs are delivered to the MSISDN. An attacker who performs a carrier-level SIM swap/port receives both — defeating the platform's only delivery-proof mechanism (no GPS exists, `BR-SHP-05`) and enabling password reset (`BR-AUTH-07`).
- **Impact:** Theft of delivered goods with escrow implications; account takeover of funded wallets; the 3-attempt lockout (`BR-SHP-03`) does not help because the attacker receives the *correct* code.
- **Recommendation:** Mandatory security notice on every reset/login (`BR-NTF-02` already supports this — make delivery failures alert too); consider binding delivery confirmation to courier-side verification of order details; record carrier-level detection signals as a post-launch control; document as residual risk in `threat-model.md` TM-01/TM-06.
- **Related:** `SEC-REQ-001`, `SEC-REQ-005`, `FR-015`, `C-16`, `BR-SHP-02`, `BR-SHP-03`.

## SEC-005 — Webhook replay window and nonce handling are unspecified
**Severity:** MEDIUM · **Area:** Integrations, Wallet · **Status:** OPEN

- **Description:** `INT-REQ-006` requires a "replay window on timestamp/nonce" but neither the window length nor the nonce store is defined anywhere; a captured-but-validly-signed callback could be re-posted within an unbounded window if implementation defaults are careless.
- **Impact:** Replayed "payment success" callbacks → duplicate-credit attempts (idempotency is the second line of defense, not the first).
- **Recommendation:** Fix a concrete window (design choice: ±5 minutes), persist processed nonces/provider-transaction IDs with TTL ≥ window, reject outside-window requests before signature evaluation, and assert it in `AC-IR006-02`-style tests. Spec lives in `10-integrations/webhook-reliability.md`.
- **Related:** `SEC-REQ-007`, `INT-REQ-006`, `INT-REQ-001`, `BR-PAY-03`, `BR-PAY-08`.

## SEC-006 — OTP resend cooldown lacks a distributed per-destination guard
**Severity:** MEDIUM · **Area:** Authentication, Rate limiting · **Status:** OPEN

- **Description:** The 60 s cooldown and ≤3 resends/10 min (`BR-AUTH-03`) are specified *per phone*; nothing in the canon mandates a per-**destination** limit across different requesters, which is the dimension SMS pumpers rotate on (many IPs, one victim number).
- **Impact:** OTP bombing of a victim number (harassment + SMS budget burn) and continued pumping despite per-IP limits.
- **Recommendation:** Enforce the cooldown/resend caps keyed on a hashed destination phone **globally**, not just per session/IP; add a per-destination metric and alert; covered by control `SEC-C-20` with the key noted as `INFERENCE`.
- **Related:** `SEC-REQ-009`, `SEC-REQ-005`, `BR-AUTH-03`, `FR-001`, `threat-model.md` TM-02.

## SEC-007 — Elasticsearch index content may include PII with no defined protection
**Severity:** MEDIUM · **Area:** Search, Data protection · **Status:** OPEN

- **Description:** `SEC-REQ-006` covers Postgres-classified fields and MinIO, but the search index (`DEP-04`, `FR-009`) is never mentioned: what is indexed (store owner names? order-derived text?), whether index snapshots are encrypted, and how deletion propagates (index vs source) are all undefined.
- **Impact:** A forgotten copy of PII outside the protected stores; account-deletion obligations (`DATA-REQ-003`) silently unmet for indexed fields; snapshot exposure.
- **Recommendation:** Define index field allowlist (public catalog fields only, `DATA-REQ-002`), encrypt/restrict index snapshots, wire index deletion into the account-deletion workflow, and add a "PII in index" test to `13-testing/`.
- **Related:** `SEC-REQ-006`, `DATA-REQ-002`, `DATA-REQ-003`, `FR-009`, `NFR-019`.

## SEC-008 — MinIO bucket exposure via listing/presigned URLs
**Severity:** MEDIUM · **Area:** File storage, KYC · **Status:** OPEN

- **Description:** KYC documents and bank receipts (`A-07`) sit in MinIO (`DEP-07`). Bucket policies (anonymous listing blocked?), presigned-URL TTL, and whether app and media share an origin are not specified anywhere; a misconfigured bucket or long-lived URL leaks identity documents.
- **Impact:** Bulk identity-document disclosure; GDPR/PDPA-style reportable incident; trust collapse for vendor KYC.
- **Recommendation:** Deny anonymous access & listing on all buckets, short presigned TTLs, separate media origin, server-generated object keys, quarterly bucket-policy review; verify in tests.
- **Related:** `SEC-REQ-006`, `SEC-REQ-011`, `FR-007`, `INT-REQ-002`, `DATA-REQ-002`.

## SEC-009 — Refresh-token reuse detection is clock-skew sensitive
**Severity:** LOW · **Area:** Sessions · **Status:** OPEN

- **Description:** Single-use rotation (`BR-AUTH-05`) plus 15-minute access lifetimes assume well-synchronized clocks; skewed host time causes false reuse detections (mass session revocations with user alerts) or extended acceptance windows.
- **Impact:** Availability nuisance and alert fatigue at low skew; weakened expiry enforcement at high skew.
- **Recommendation:** NTP on all hosts as a deployment prerequisite; define a small leeway (seconds) on `exp`/`iat` checks; alert on clock drift; test family-revocation under injected skew.
- **Related:** `SEC-REQ-003`, `BR-AUTH-05`, `C-08`, `NFR-020`.

## SEC-010 — CORS policy is unspecified anywhere in the canon
**Severity:** MEDIUM · **Area:** API, Browser security · **Status:** OPEN

- **Description:** No document defines allowed origins, credentialed-CORS behavior, or preflight rules for the Next.js web app, vendor panel, or admin console. An implementation could default to `*` with credentials or over-broad origins.
- **Impact:** Cross-origin reading of authenticated responses; amplifies XSS/CSRF exposure, especially combined with `SEC-003`.
- **Recommendation:** Explicit allowlist per surface (exact origins, credentials true only for known origins, methods/headers allowlist), deny-by-default preflight, documented in `07-api/` conventions and enforced by a single middleware; add a CORS test case.
- **Related:** `SEC-REQ-008`, `SEC-REQ-003`, `FR-001`.

## SEC-011 — The sole authentication channel (DEP-06) is uncontracted and unvalidated
**Severity:** CRITICAL · **Area:** Authentication, Dependency · **Status:** OPEN

- **Description:** `DEP-06` (SMS provider contract + WhatsApp Business approval) is **NOT STARTED** and is a Phase 0 gate; `INT-REQ-003` rates its dependency risk CRITICAL because "registration is blocked". Failover, DLR logging, and shortcode certification are therefore entirely unvalidated against real carriers (`DEP-12` test lab also not started).
- **Impact:** The security properties of `SEC-REQ-001` R5 (OTP survives provider failure) are unproven; launch cannot be secured; an unvetted provider choice could log OTPs or reuse sender IDs.
- **Recommendation:** Prioritize `DEP-06` commercial close; require written no-log guarantees for message bodies; run the failover drill and DLR verification (`AC-IR003-01…04`) in sandbox **before** any production credential; keep `RISK-006` escalated.
- **Related:** `SEC-REQ-001`, `INT-REQ-003`, `INT-REQ-004`, `FR-001`, `DEP-06`, `DEP-12`, `RISK-006`.

## SEC-012 — Login is single-factor for privileged roles; OTP-at-login canon ambiguity
**Severity:** HIGH · **Area:** Authentication, Admin console · **Status:** OPEN

- **Description:** `FR-001` and `BR-AUTH-04` scope OTP to registration, reset, and sensitive changes — login is phone + password. Meanwhile the opening description of `SEC-REQ-001` says "every authentication … is gated by … OTP". The canon does not say clearly whether ADMIN/SUPER_ADMIN login requires OTP, and there is no step-up/MFA mechanism (`authentication.md` §7 decision: none in v1).
- **Impact:** An admin password compromise yields direct access to refunds, KYC, payouts, and role management (`TM-07`); ambiguity itself risks inconsistent implementation across surfaces.
- **Recommendation:** Resolve the ambiguity with a decision record (18-decisions/) before implementation; minimally require OTP (or equivalent step-up) at ADMIN/SUPER_ADMIN login and for every privileged money action; until resolved, treat admin-console exposure (`SEC-003`) as compounding.
- **Related:** `SEC-REQ-001`, `SEC-REQ-003`, `SEC-REQ-004`, `FR-001`, `FR-020`, `BR-AUTH-04`.

## SEC-013 — Per-route rate-limit budgets are design-level and unvalidated under load
**Severity:** LOW · **Area:** Rate limiting · **Status:** OPEN

- **Description:** `SEC-REQ-009` fixes only the 100 req/min standard; stricter budgets for OTP/login/top-up/search/checkout in `security-controls.md` §3 are `INFERENCE` figures not yet validated against the 10,000-concurrency load test (`C-25`).
- **Impact:** Budgets set too tight throttle legitimate users (revenue/UX); set too loose, they under-protect money endpoints.
- **Recommendation:** Validate every budget during the `NFR-003` load test with an abusive client profile (`AC-SR009-04`); adjust and re-version the control catalog with test evidence.
- **Related:** `SEC-REQ-009`, `NFR-001`, `NFR-003`, `C-25`, `SEC-C-20`.

## SEC-014 — Field-encryption key rotation and re-encryption procedure undefined
**Severity:** MEDIUM · **Area:** Data protection, Secrets · **Status:** OPEN

- **Description:** `SEC-REQ-002` R3 requires keys outside the DB, but no document defines key hierarchy (data key vs key-encryption key), who may decrypt, how a key rotation re-encrypts existing rows, or how decryption behaves during the rotation window.
- **Impact:** A botched rotation could make classified columns unreadable (outage) or leave old ciphertext under retired keys (forever-unrecoverable data / compliance gap).
- **Recommendation:** Specify key hierarchy, custody split (`secrets-management.md` S-12), online re-encryption job with checkpointing, and a restore-under-new-key drill alongside `DATA-REQ-004` backup drills.
- **Related:** `SEC-REQ-002`, `SEC-REQ-006`, `SEC-REQ-007`, `DATA-REQ-004`, `NFR-019`.

## SEC-015 — Escrow release job may race dispute creation (TOCTOU on funds)
**Severity:** HIGH · **Area:** Escrow, Financial integrity · **Status:** OPEN

- **Description:** `BR-ESC-02` releases escrow when 7 days elapsed AND no active dispute; `BR-ORD-05` freezes release on DISPUTED. A scheduled release job evaluating the condition and a dispute being created concurrently can interleave — the release reads "no dispute" before the freeze commits, paying out funds that should be held.
- **Impact:** Vendor receives funds that a valid dispute should have frozen; recovery depends on vendor solvency — direct money loss to buyers/platform.
- **Recommendation:** Serialize release and dispute-freeze on the same row/aggregate lock (or evaluate-and-release inside one transaction with the dispute check re-read under lock); make the release job idempotent and reconcilable (`BR-FIN-03`); add a concurrency test to `13-testing/` before launch.
- **Related:** `SEC-REQ-010`, `FR-014`, `FR-016`, `BR-ESC-01`, `BR-ESC-02`, `BR-ORD-05`, `NFR-008`.

---

## Register Rules

1. New findings continue the sequence `SEC-016`…; IDs are never reused, even after closure.
2. Closure requires: fix or accepted-risk decision, evidence link (test/audit), severity re-check, version bump, Change History row — a finding is never silently deleted.
3. Findings that threaten objectives are mirrored as `RISK-nnn` entries in `17-risk-management/risk-register.md` (e.g., `SEC-011` ↔ `RISK-006`).
4. `SEC-REQ-012` R4 requires recurring reporting of this register by severity with no unjustified suppressions.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis (15 findings, all OPEN) |
