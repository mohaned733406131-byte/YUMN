---
document_id: DOC-SR-007
title: SEC-REQ-007 — Secrets management
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-006, SEC-REQ-008, SEC-REQ-012, FR-020, NFR-020]
related_documents: [DOC-REQ-001, DOC-OVR-008, DOC-OVR-010]
---

# SEC-REQ-007 — Secrets management

> Registry summary (`requirements-overview.md` §3): all secrets via environment/secrets manager; CI secret scanning; no keys in repo.

**Priority:** Critical · **STRIDE:** Information disclosure (I) · **Failure impact:** CRITICAL

## Description
All secrets — database/Redis credentials, RS256 private signing keys, m-Floos/OneCash merchant credentials (DEP-05), SMS/WhatsApp provider credentials (DEP-06), webhook HMAC secrets, and TLS keys — are supplied at runtime from the environment or a secrets manager, never from source code, images, or Compose files committed to the repository.

## Security rationale
A single committed key is game-over regardless of how strong the rest of the design is: git history is hard to purge, and provider keys grant direct ability to send OTPs, forge webhooks, or move money. Threat: credential exposure through source control, images, logs, or bundles → STRIDE **Information disclosure** (with direct financial consequence via DEP-05/DEP-06 credentials).

## Requirement statements

- R1: Every secret is read from environment variables or a secrets manager at runtime; no secret literal appears in source code, fixtures, Docker images, or committed Docker Compose files (C-22) — Compose uses `${VAR}`/`env_file` indirection only.
- R2: CI runs secret scanning on every change; a commit containing a credential fails the pipeline and is blocked from merge.
- R3: Application startup fails fast with a non-sensitive error when a required secret is missing; no default, fallback, or example credential is ever used.
- R4: Secrets never appear in logs, error messages, traces, client-side bundles, or `/metrics` labels (cross SEC-REQ-002 / SEC-REQ-006).
- R5: A documented rotation procedure covers periodic rotation and immediate rotation on suspected compromise or staff departure (`INFERENCE` — operational control derived from DEP-05/DEP-06 external-credential exposure).

## Acceptance criteria

- AC-SR007-01: Pipeline test — a seeded canary secret in a branch is detected by the CI secret scan and the build fails.
- AC-SR007-02: Startup test — removing a required environment variable causes fail-fast startup failure whose error message contains no other secret value.
- AC-SR007-03: Repository audit — automated scan finds zero credential literals in code, Compose files, fixtures, and documentation.
- AC-SR007-04: Log/trace scrub test — provider credentials, HMAC secrets, and JWT keys are absent from application logs and traces during a full auth + top-up test run.

## Related IDs

`SEC-REQ-006` · `SEC-REQ-008` · `SEC-REQ-012` · `FR-020` · `NFR-020` · `C-22` · `DEP-05` · `DEP-06` · `DEP-08`

## Verification method

CI secret-scan evidence, repository audit, startup integration test in the deployment pipeline, and log/trace inspection; configuration review by the security owner in `09-security/`.

## Failure impact

**CRITICAL** — committed or leaked provider/webhook/signing keys allow forging payment callbacks, hijacking OTP delivery, and reading production data, with direct money movement and full loss of trust in the token system.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
