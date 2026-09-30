---
document_id: DOC-IR-000
title: Integration Requirements — README (INT-REQ Index)
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-001, INT-REQ-002, INT-REQ-003, INT-REQ-004, INT-REQ-005, INT-REQ-006, INT-REQ-007, INT-REQ-008]
related_documents: [DOC-REQ-001, DOC-REQ-002, DOC-OVR-010]
---

# Integration Requirements (`INT-REQ-001` … `INT-REQ-008`)

## Purpose

Expands the 8 integration requirement IDs registered in [`requirements-overview.md` §5](requirements-overview.md) into interface expectations, data contracts, failure behavior, security controls, and dependency risk ratings. The registry is canonical: IDs and titles here never diverge from it, and no integration requirement exists that is not registered.

## Index

| ID | File | Title | Primary dependency | Dependency risk |
|---|---|---|---|---|
| INT-REQ-001 | [INT-REQ-001.md](core/INT-REQ-001.md) | Wallet top-up providers | DEP-05 (m-Floos, OneCash) | HIGH |
| INT-REQ-002 | [INT-REQ-002.md](core/INT-REQ-002.md) | Bank transfer top-up | internal admin flow | MEDIUM |
| INT-REQ-003 | [INT-REQ-003.md](core/INT-REQ-003.md) | SMS provider failover | DEP-06 (Telesom/Sabafon) | CRITICAL |
| INT-REQ-004 | [INT-REQ-004.md](core/INT-REQ-004.md) | WhatsApp Business notifications | DEP-06 (WhatsApp Business API) | HIGH |
| INT-REQ-005 | [INT-REQ-005.md](core/INT-REQ-005.md) | Delivery orchestration | internal engine (v1) | LOW |
| INT-REQ-006 | [INT-REQ-006.md](core/INT-REQ-006.md) | Webhook robustness | DEP-05 / DEP-06 callbacks | HIGH |
| INT-REQ-007 | [INT-REQ-007.md](core/INT-REQ-007.md) | Observability export | Prometheus / Grafana stack | MEDIUM |
| INT-REQ-008 | [INT-REQ-008.md](core/INT-REQ-008.md) | Provider abstraction | design constraint on 001/003/004/005 | MEDIUM |

## Relation to `10-integrations/`

- This directory owns the **requirements** — what any integration must guarantee, with acceptance criteria `AC-IRnnn-nn` and a dependency risk rating.
- `10-integrations/` owns the **contracts** — concrete endpoints, payload schemas, provider-specific failure matrices, and sequence detail for each external system.
- Requirements are provider-agnostic by design (INT-REQ-008); provider-specific facts belong only in `10-integrations/`, referenced here by path.

## Shared Interface Expectations

Applies to every external integration unless a file states otherwise:

- **Flow:** initiate → callback (signed) → poll fallback → idempotent finalization.
- **Timeouts:** 10 s per outbound call; **retries:** 3 with exponential backoff, then dead-letter queue (BR-PLT-02); DLQ depth alerts (BR-PLT-01).
- **Webhooks:** HMAC-signed with constant-time verification, IP allowlist, replay window, secrets from environment only (SEC-REQ-007).
- **Environments:** provider sandbox certified before production traffic (DEP-05, DEP-06 gate).
- **Rate limits:** platform limits (SEC-REQ-009, 100 req/min standard) plus provider-imposed quotas respected and surfaced as metrics.

## Naming & ID Conventions

- Files: `INT-REQ-nnn.md`. Document IDs: `DOC-IR-000` (this index) … `DOC-IR-008`. Acceptance criteria: `AC-IRnnn-nn` (e.g. `AC-IR001-03`).
- IDs are assigned only in `requirements-overview.md`; every file carries frontmatter with `category: 02-requirements`, `status: approved`, `source_of_truth: true`.

## Severity & Evidence Conventions

- **Dependency risk** — `CRITICAL` (platform unusable without it) · `HIGH` (major feature blocked, workaround exists) · `MEDIUM` (degraded operation/manual load) · `LOW` (no external v1 dependency).
- Statements are evidence-tagged `VERIFIED` · `INFERENCE` · `INSUFFICIENT EVIDENCE`; dependency status per `00-project-overview/dependencies.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial index (8 requirements) | Initial analysis |
