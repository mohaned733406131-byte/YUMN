---
document_id: DOC-IR-008
title: INT-REQ-008 — Provider abstraction
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-001, INT-REQ-003, INT-REQ-004, INT-REQ-005, NFR-009]
related_documents: [DOC-REQ-001, DOC-OVR-010]
---

# INT-REQ-008 — Provider abstraction

> Registry summary (`requirements-overview.md` §5): payment/SMS interfaces behind adapters — no vendor types leak into domain code.

**Dependency risk:** MEDIUM — design/architecture risk: leakage of vendor specifics would amplify `DEP-05`/`DEP-06` churn into domain code; the requirement itself is what mitigates that exposure.

## Purpose
Insulate the domain (wallet, orders, notifications, delivery) from vendor specifics through ports-and-adapters, so provider swaps, sandbox→production transitions, and failover logic never require domain changes — critical while DEP-05/DEP-06 commercial terms are still open.

## Interface expectations

- **Ports:** domain code depends only on provider-neutral interfaces (`PaymentProviderPort`, `SmsProviderPort`, `WhatsAppPort`, `DeliveryProviderPort`) with normalized DTOs: integer YER amount, phone, platform reference, status enum, normalized error taxonomy (`TIMEOUT`, `REJECTED`, `PROVIDER_DOWN`, `SIGNATURE_INVALID`).
- **Adapters:** vendor SDKs, HTTP clients, payload mapping, and credentials live exclusively in adapter modules; each adapter certifies against the same contract-test suite (sandbox first — INT-REQ-001/003/004).
- **Selection/failover:** primary/secondary choice and fallback rules are configuration evaluated through the port, not `if vendor == …` branches in services.
- **Boundaries:** enforced inside the modular monolith (C-21) — module boundary rules in CI (NFR-009).

## Data exchanged
Internal DTOs only cross the adapter boundary; vendor-specific JSON/XML, vendor error strings, and vendor identifiers never appear in domain objects, API responses, logs, or events (`INFERENCE` — operationalizes the registry's "no vendor types leak into domain code").

## Failure behavior & fallback
Adapters translate vendor failures into the normalized taxonomy so retry/failover/degradation logic (INT-REQ-001/003/006) is provider-agnostic; an unknown vendor error maps to `PROVIDER_DOWN` — never to an exception that escapes into domain transactions.

## Security
Vendor credentials are injected per adapter from environment/secrets manager only (SEC-REQ-007); normalized errors and logs never echo credential material; adapters are the only code permitted to hold provider-specific signing logic (HMAC per INT-REQ-006).

## Acceptance criteria

- AC-IR008-01: Architecture test — an import/lint rule fails the build if any vendor SDK or vendor-specific type is referenced outside its adapter folder.
- AC-IR008-02: Substitution test — swapping a mock adapter for the real sandbox adapter requires zero edits to domain modules (domain compiles and all domain tests pass unchanged).
- AC-IR008-03: Leak test — static scan finds zero vendor identifiers (m-Floos, OneCash, Telesom, Sabafon, WhatsApp vendor types) in domain code, API response schemas, and log statements.
- AC-IR008-04: Contract parity — the identical contract-test suite passes against every adapter implementation (mock, provider A, provider B).

## Related IDs

`DEP-05` · `DEP-06` · `C-18` · `C-21` · `FR-013` · `FR-017` · `NFR-009` · `SEC-REQ-007` · `INT-REQ-001` · `INT-REQ-003` · `INT-REQ-004` · `INT-REQ-005` · `INT-REQ-006`

## Verification method
Automated architecture/import-boundary test in CI, dependency-inversion compilation check, static scan for vendor identifiers, and shared contract-test suite execution per adapter.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
