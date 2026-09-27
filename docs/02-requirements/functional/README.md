---
document_id: DOC-FR-000
title: Functional Requirements — README (FR-001 … FR-020)
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020]
related_documents: [DOC-REQ-001, DOC-REQ-002, DOC-BA-005, DOC-OVR-008]
---

# Functional Requirements — README

## Purpose

This directory holds the **detailed specification of the 20 functional requirements** of the yumn marketplace (`FR-001…FR-020`), one file per requirement. Each file expands — and must never contradict — its entry in the canonical registry [requirements-overview.md](../requirements-overview.md) (`DOC-REQ-001`).

## Contents

| File | ID | Title | Block | Priority |
|---|---|---|---|---|
| [FR-001.md](FR-001.md) | FR-001 | Identity, Authentication & Session Management | B01 | Critical |
| [FR-002.md](FR-002.md) | FR-002 | Roles, Permissions & Access Control | B01 | Critical |
| [FR-003.md](FR-003.md) | FR-003 | User & Profile Management | B01 | High |
| [FR-004.md](FR-004.md) | FR-004 | Product Catalog Management | B02 | Critical |
| [FR-005.md](FR-005.md) | FR-005 | Inventory Management | B02 | Critical |
| [FR-006.md](FR-006.md) | FR-006 | Reviews & Ratings | B02 | High |
| [FR-007.md](FR-007.md) | FR-007 | Vendor Onboarding & KYC | B03 | Critical |
| [FR-008.md](FR-008.md) | FR-008 | Store Management & Storefront Configuration | B03 | High |
| [FR-009.md](FR-009.md) | FR-009 | Search & Discovery | B04 | High |
| [FR-010.md](FR-010.md) | FR-010 | Shopping Cart | B05 | Critical |
| [FR-011.md](FR-011.md) | FR-011 | Checkout & Order Placement | B05 | Critical |
| [FR-012.md](FR-012.md) | FR-012 | Order Lifecycle Management | B06 | Critical |
| [FR-013.md](FR-013.md) | FR-013 | Wallet & Payment Processing | B07 | Critical |
| [FR-014.md](FR-014.md) | FR-014 | Escrow, Commission & Vendor Payouts | B07 | Critical |
| [FR-015.md](FR-015.md) | FR-015 | Shipping & Delivery | B08 | Critical |
| [FR-016.md](FR-016.md) | FR-016 | Returns & Refunds | B09 | Critical |
| [FR-017.md](FR-017.md) | FR-017 | Notifications & Messaging | B10 | High |
| [FR-018.md](FR-018.md) | FR-018 | Analytics & Reporting | B11 | Medium |
| [FR-019.md](FR-019.md) | FR-019 | Content & Promotions (CMS + Coupons) | B12 | High |
| [FR-020.md](FR-020.md) | FR-020 | Platform Administration, Settings & Audit | B13 | Critical |

## Source of Truth Statement

1. **`02-requirements/requirements-overview.md` (`DOC-REQ-001`) is the single registry of all requirement IDs.** It fixes every FR ID, title, block and priority. No file in this directory may add, rename, re-prioritize, merge or split an FR ID.
2. Each `FR-nnn.md` file is the source of truth for the **detail** of its requirement: requirements detail, preconditions, expected result, acceptance criteria (`AC-FRnnn-nn`), applied business rules, honored constraints, dependencies and verification method.
3. Business rules are defined only in `01-business-analysis/business-rules.md` (`DOC-BA-005`); constraints only in `00-project-overview/project-constraints.md` (`DOC-OVR-008`); order states only in `03-system-analysis/state-transitions.md` (`DOC-SA-010`). This directory **references those IDs — it never redefines them.**
4. If an FR file and the registry disagree, the registry wins and the discrepancy is logged in `20-validation/contradiction-audit.md` — never silently patched.

## Dependency on the Registry

`requirements-overview.md` is the **table of contents** of this directory: reading order is registry §1 → the individual `FR-nnn.md` file. Every FR file carries `related_documents: [DOC-REQ-001, …]` so traceability to the registry is explicit and machine-checkable.

## Naming Rule

- Files: `FR-NNN.md` with a zero-padded three-digit number matching the registry exactly (`FR-001.md` … `FR-020.md`); never `final.md`, `latest.md`, or any variant that does not carry the FR ID.
- Document IDs: `DOC-FR-NNN`, allocated 000 (this README) and 001…020 (one per FR).
- Acceptance criteria: `AC-FRnnn-01 … -04` — the numeric part matches the FR with no padding beyond three digits (`AC-FR012-01`).
- Never reuse a retired ID; a superseded requirement keeps its ID with status `SUPERSEDED`.

## Quality Rules

1. **Acceptance criteria are mandatory.** Every FR carries at least four objectively testable `AC-FRnnn-nn` entries written as given/when/then one-liners; an FR without measurable ACs is incomplete and blocks the quality gate (`DOC-REQ-001` §6, root README §11).
2. Every requirement carries: description, rationale (tracing to `OBJ-*` and/or `C-*`), requirements detail, preconditions, expected result, ACs, business rules applied (`BR-*`), constraints honored (`C-*`), dependencies (`FR/NFR/SEC-REQ/DATA-REQ/INT-REQ/DEP-*`), verification method and out-of-scope notes.
3. Only canon IDs may be referenced — never invent `BR-*`, `C-*`, `OBJ-*`, `NFR-*`, `SEC-REQ-*`, `DEP-*` or `FR-*` identifiers outside the registries.
4. Contradictions with rules/architecture go to `20-validation/contradiction-audit.md`; missing facts go to `20-validation/missing-information.md` as `GAP-*`.
5. A requirement is `approved` only when it passes the 7-question quality test (clarity, completeness, consistency, feasibility, testability, necessity, traceability).

## Related Directories

`../requirements-overview.md` (registry) · `../non-functional/` (NFR-001…020) · `../security/` (SEC-REQ-001…012) · `../data/` · `../integration/` · `../../01-business-analysis/` (rules) · `../../03-system-analysis/` (behavior) · `../../13-testing/` (verification)
