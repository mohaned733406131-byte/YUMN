---
document_id: DOC-SR-004
title: SEC-REQ-004 — Server-side authorization
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-003, SEC-REQ-010, FR-002, FR-020]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-004 — Server-side authorization

> Registry summary (`requirements-overview.md` §3): RBAC + ownership checks on every endpoint; frontend guards are UX only, never security.

**Priority:** Critical · **STRIDE:** Elevation of privilege (E) · **Failure impact:** CRITICAL

## Description
Every API request is authorized on the server against the RBAC matrix for the 7 actors (Customer, Vendor, Delivery Provider, Admin, Super Admin, Moderator, System) plus resource ownership. UI hiding, route guards, and client-side role checks are presentation only and never grant access (FR-002).

## Security rationale
Any authenticated user can call any endpoint directly with a crafted request; if authorization lives only in the frontend, a customer can invoke admin refunds or read another vendor's store data. Threat: horizontal movement between tenants and vertical escalation to privileged roles → STRIDE **Elevation of privilege**.

## Requirement statements

- R1: Authorization is evaluated at the service layer on every request, deny-by-default; an unknown role or missing permission results in 403 (or 404 for non-owned resources where enumeration would leak existence).
- R2: The role × action matrix for all 7 actors is defined in `../../09-security/core/rbac.md` (control) and every endpoint must map to exactly one decision per role.
- R3: Ownership is enforced with the role check: vendor queries scoped to `store_id` with cross-store access denied at the service layer (BR-VND-07); order/timeline visibility restricted per BR-ORD-09; customers see only their own resources.
- R4: Privileged and money actions (role change, KYC decision, wallet freeze, refund, payout, dispute resolution) additionally require an audit entry (BR-PLT-06, SEC-REQ-010).
- R5: The `System` actor is non-human: it authenticates only through internal mechanisms and can never be used for interactive login or to bypass ownership checks.

## Acceptance criteria

- AC-SR004-01: Matrix test — an automated suite calls every API endpoint as each of the 7 roles and asserts the expected allow/deny decision; no endpoint is left untested.
- AC-SR004-02: Ownership tests — customer B reading/modifying customer A's order, wallet, or reviews is denied; a vendor querying another store's products/orders receives 403/404.
- AC-SR004-03: Direct-API test — actions hidden in the UI (e.g. admin refund, moderator role change) called with a low-privilege token are rejected server-side with identical results whether reached via UI or raw HTTP.
- AC-SR004-04: Deny-by-default test — a request with no/invalid role context, or an endpoint missing an authorization mapping, fails closed rather than open.

## Related IDs

`FR-002` · `FR-003` · `FR-020` · `BR-VND-07` · `BR-ORD-09` · `BR-PLT-06` · `SEC-REQ-003` · `SEC-REQ-010` · `DATA-REQ-008` · `C-21`

## Verification method

Automated authorization-matrix and cross-tenant integration tests in CI (one case per role × endpoint), plus manual penetration testing of privilege-escalation paths; control detail in `../../09-security/core/rbac.md`.

## Failure impact

**CRITICAL** — full platform compromise: any user could act as admin or as another vendor/customer, exposing funds, KYC documents, and the entire order/ledger history.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
