---
document_id: DOC-SR-008
title: SEC-REQ-008 — Injection/XSS/CSRF defense
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-003, SEC-REQ-009, FR-001, FR-009]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-008 — Injection/XSS/CSRF defense

> Registry summary (`requirements-overview.md` §3): parameterized queries (Prisma), output encoding, CSP, CSRF tokens for cookie auth.

**Priority:** Critical · **STRIDE:** Tampering (T), Elevation of privilege (E) · **Failure impact:** CRITICAL

## Description
All untrusted input — URL params, request bodies, search queries (including Arabic text), uploaded filenames, and stored user content (product names, reviews, store profiles) — is neutralized against SQL injection, cross-site scripting, and cross-site request forgery across every API surface and rendered page.

## Security rationale
The marketplace stores money-relevant data (orders, ledger, coupons) behind one database; successful injection reads or alters that data directly. Stored XSS in Arabic-first user content steals httpOnly-adjacent session state or performs actions as the victim; CSRF rides the cookie-based session (SEC-REQ-003) to trigger payments/refunds. Threat: data tampering, script injection, forged state-changing requests → STRIDE **Tampering** and **Elevation of privilege**.

## Requirement statements

- R1: All database access goes through Prisma parameterized queries; no SQL is built by string concatenation anywhere in the repository layer.
- R2: All user-generated content is context-aware encoded on output; stored values such as product/review names are rendered inert regardless of locale (ar/en) or RTL markup.
- R3: A Content-Security-Policy header is served without `unsafe-inline` for scripts, blocking inline script execution in the browser.
- R4: Cookie-based state-changing requests require a CSRF token (double-submit or synchronizer pattern); SameSite cookies (SEC-REQ-003) provide defense in depth, not the sole control.
- R5: Input validation constrains type, length, and range at every endpoint before business logic runs (cross DATA-REQ-001).

## Acceptance criteria

- AC-SR008-01: SQLi test suite — OWASP-style payloads against search, auth, filter, and admin parameters return no unauthorized rows, no SQL errors, and no stack traces.
- AC-SR008-02: Stored-XSS test — `<script>` and event-handler payloads placed in product names, reviews, and store profiles are stored but displayed encoded; CSP blocks inline execution (asserted in a browser-driven test).
- AC-SR008-03: CSRF test — a state-changing request carrying a valid session cookie but no CSRF token is rejected with 403; the same request with a valid token succeeds.
- AC-SR008-04: Static/architecture check — linting flags any raw SQL string concatenation in the data-access layer; zero violations in CI.

## Related IDs

`FR-001` · `FR-004` · `FR-006` · `FR-009` · `SEC-REQ-003` · `SEC-REQ-009` · `DATA-REQ-001` · `C-24`

## Verification method

DAST scan against staging, browser-driven XSS/CSRF integration tests, SQLi payload suites in CI, and static linting of the repository layer; findings tracked as `SEC-nnn` in `09-security/`.

## Failure impact

**CRITICAL** — injection permits direct read/modify of wallets, orders, and the ledger; XSS enables session takeover of any user including admins; CSRF can trigger unauthorized refunds or purchases.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
