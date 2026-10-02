---
document_id: DOC-SR-014
title: SEC-REQ-014 — Per-surface CORS policy
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-008, SEC-REQ-003, FR-001]
related_documents: [DOC-REQ-001, DOC-OVR-012]
---

# SEC-REQ-014 — Per-surface CORS policy

> Registry summary (`requirements-overview.md` §3): exact origin allowlist for web/vendor/admin, credentialed CORS only for known origins, methods/headers allowlist, deny-by-default preflight enforced by a single middleware, with a CORS test case.

**Priority:** Medium · **STRIDE:** Information Disclosure (I) · **Failure impact:** MEDIUM

## Description
The canon defines no CORS behaviour anywhere: `../../09-security/core/security-findings.md` `SEC-010` (lines 115–121, severity MEDIUM) states "No document defines allowed origins, credentialed-CORS behavior, or preflight rules". This requirement fixes an explicit per-surface policy — the customer web, vendor panel and admin console each declare their exact origins, and everything else is denied by default. Registration recorded in `DOC-OVR-012` §5; decision anchor `../../18-decisions/core/ADR-010.md` line 70 (`VERIFIED`).

## Security rationale
A missing CORS policy lets any origin read authenticated responses if credentials are ever allowed broadly: reflected or wildcard origins with `Access-Control-Allow-Credentials: true` expose session-bearing API responses to attacker pages (session theft → wallet/escrow actions under the victim's cookies, C-08). Deny-by-default preflight removes whole classes of cross-origin abuse. Threat: cross-origin data theft → STRIDE **Information Disclosure**.

## Requirement statements

- R1: Each surface (customer web, vendor panel, admin console) declares an exact origin allowlist — scheme + host + port, never wildcards; origins are configuration, not code (`SEC-010` recommendation).
- R2: `Access-Control-Allow-Credentials: true` is returned only for origins on that allowlist; unknown origins receive no CORS headers at all (deny-by-default).
- R3: Allowed methods and headers are an explicit allowlist; preflight (`OPTIONS`) is evaluated by a single middleware that enforces allowlist → deny-by-default consistently for every route (`INFERENCE` for "single middleware" — sources mandate one policy, the middleware shape is the implementation of that policy).
- R4: A CORS test case (required by `SEC-010`) asserts allow behaviour for each registered origin and deny behaviour for an unlisted origin, and runs in CI.

## Acceptance criteria

- AC-SR014-01: Given the configured allowlist origins, when each preflights and sends a credentialed request, then the correct `Access-Control-Allow-*` headers are returned.
- AC-SR014-02: Given an origin not on the allowlist, when it sends a preflight or credentialed request, then no CORS headers are returned and the browser blocks the read — deny-by-default holds.
- AC-SR014-03: Given the CORS configuration, when it is inspected, then no wildcard origin combined with credentialed access exists anywhere, and methods/headers are explicit allowlists.
- AC-SR014-04: Given the CORS test case in CI, when a route bypasses the shared middleware or widens the policy, then the test fails and blocks the merge.

## Related IDs

`SEC-REQ-008` · `SEC-REQ-003` · `SEC-REQ-004` · `FR-001` · `NFR-011` · `ADR-010` · `SEC-010`

## Verification method

Automated CORS contract tests (allowed/denied origins per surface) in CI; configuration review of the origin allowlist; middleware coverage check proving every route passes the same policy; findings tracked in `../../09-security/core/security-findings.md` (`SEC-010`).

## Failure impact

**MEDIUM** — an unspecified policy invites permissive defaults; a wrongly permissive CORS configuration with credentials exposes authenticated API responses (orders, wallet balance, PII) to arbitrary origins, though exploitation requires a browser session context rather than direct fund movement.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial requirement | Session-011 owner directive (`prompt-011.md` §4.7) — delta accepted in `DOC-OVR-012` §5 (source: `security-findings.md` `SEC-010` lines 115–121; `ADR-010` line 70) |
