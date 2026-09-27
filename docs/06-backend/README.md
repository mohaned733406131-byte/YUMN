---
document_id: DOC-BE-001
title: Backend Domain Overview & File Index
category: 06-backend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-011, FR-012, FR-013, NFR-001, NFR-007, NFR-008, NFR-009, NFR-014]
related_documents: [DOC-ROOT-001, DOC-REQ-001, DOC-OVR-008, DOC-OVR-002]
---

# Backend Domain — Overview & Index

The backend is a **single NestJS 10 modular monolith** (`C-21`) on Node 20 / TypeScript 5, persisting to **PostgreSQL 16 via Prisma 5** (`C-19`), with **Redis 7 + BullMQ** for cache, rate limits and background jobs (`C-20`), **Elasticsearch 8** for search, and **MinIO** for object storage. It is the *only* place business rules are enforced — every frontend guard mirrors a server check (`SEC-REQ-004`).

---

## 1. Where Business Logic Lives

| Question | Answer |
|---|---|
| How many deployable services? | **One** — the NestJS monolith, containerized with Docker Compose (`C-21`, `C-22`) |
| How is code organized? | One NestJS module per canonical block `B01…B13` (`00-project-overview/project-context.md`) — see `backend-architecture.md` |
| Who may execute money/state/stock rules? | Only backend services/domain layer — never the client, never a job bypassing the service (`SEC-REQ-004`) |
| What runs asynchronously? | BullMQ workers in the same binary process pool, queues named `{block}.{entity}.{action}` (`BR-PLT-01`, `background-processing.md`) |
| What talks to externals? | Adapter modules behind interfaces (payments, SMS, WhatsApp, webhooks) — no vendor types in domain code (`INT-REQ-008`) |
| What is the API surface? | REST under `/api/v1`, contract in `07-api/` |
| How are errors surfaced? | Global filters producing the shared error model (`error-handling.md` ← `07-api/error-model.md`) |

## 2. Requirement → Backend Ownership (summary)

| FR family | Module block | Main file |
|---|---|---|
| FR-001…FR-003 identity/roles/profiles | B01 | `authentication.md`, `authorization.md` |
| FR-004…FR-006 catalog/inventory/reviews | B02 | `business-logic-placement.md` |
| FR-007…FR-008 vendors/stores | B03 | `backend-architecture.md` §3 |
| FR-009 search | B04 | `caching.md`, `background-processing.md` (index sync) |
| FR-010…FR-011 cart/checkout | B05 | `validation.md`, `business-logic-placement.md` |
| FR-012 orders | B06 | `business-logic-placement.md` §4 (state machine) |
| FR-013…FR-014 wallet/escrow/payouts | B07 | `business-logic-placement.md`, `background-processing.md` |
| FR-015 shipping | B08 | `business-logic-placement.md` |
| FR-016 returns | B09 | `business-logic-placement.md` |
| FR-017 notifications | B10 | `background-processing.md` (fan-out) |
| FR-018 analytics | B11 | `caching.md` (read models) |
| FR-019 content/promotions | B12 | `validation.md` (coupons) |
| FR-020 platform admin/audit | B13 | `authorization.md`, `error-handling.md` (audit hooks) |

## 3. File Index

| # | Filename | DOC ID | Purpose |
|---|---|---|---|
| 1 | `README.md` | DOC-BE-001 | This file — backend domain overview, logic ownership, file index |
| 2 | `backend-architecture.md` | DOC-BE-002 | Module-per-block layout, in-module layering, shared modules, Prisma data-access rules, FR→module map |
| 3 | `authentication.md` | DOC-BE-003 | Implementation placement of FR-001 / SEC-REQ-001…003: OTP, JWT, bcrypt, lockout, sessions, rate limits |
| 4 | `authorization.md` | DOC-BE-004 | Implementation placement of FR-002 / SEC-REQ-004: guards, interceptors, ownership scoping, RBAC pointers |
| 5 | `business-logic-placement.md` | DOC-BE-005 | Rule ID → module → service → enforcement point for the critical rules (payments, escrow, stock, states, returns) |
| 6 | `background-processing.md` | DOC-BE-006 | BullMQ queues/jobs, retries + DLQ, idempotency, scheduling, fan-out |
| 7 | `caching.md` | DOC-BE-007 | Redis cache strategy, TTLs, invalidation, stampede control, non-cacheable list, ES vs Redis |
| 8 | `error-handling.md` | DOC-BE-008 | Exception filters, error codes aligned with `07-api/error-model.md`, structured logging, domain errors |
| 9 | `validation.md` | DOC-BE-009 | DTO/schema validation, business vs schema validation, idempotency keys, payload/upload limits, integer money |

## 4. Architectural Guarantees (what this domain promises)

| Guarantee | Constraint/Requirement | Detailed in |
|---|---|---|
| One monolith, enforced module boundaries | `C-21`, NFR-009 | `backend-architecture.md` §6 |
| Exactly 17 order states, server-guarded, `409 STATE_CONFLICT` on violation | `C-09`, `BR-ORD-01` | `business-logic-placement.md` §4 |
| Wallet-only payment; no other method can be constructed | `C-01`, `BR-PAY-01` | `business-logic-placement.md` §3 |
| 15-min stock TTL, atomic deduction, no oversell | `C-13`, `BR-CAT-07` | `background-processing.md` §5 |
| Idempotency on payment/order/stock/coupon/refund | `BR-PLT-03`, NFR-008 | `validation.md` §5 |
| All jobs via BullMQ, 3× retry + backoff + DLQ | `C-20`, `BR-PLT-01/02` | `background-processing.md` |
| Structured logs + correlation IDs | NFR-014 | `error-handling.md` §4 |
| Server-side authorization on every endpoint | `FR-002`, `SEC-REQ-004` | `authorization.md` |
| No silent data loss; graceful degradation | NFR-007 | `background-processing.md` §8, `caching.md` §7 |

## 5. Upstream / Downstream Contracts

| Direction | Document | Dictates |
|---|---|---|
| Upstream | `02-requirements/requirements-overview.md` | FR/NFR/SEC/INT IDs implemented here |
| Upstream | `01-business-analysis/business-rules.md` | all 99 BR rules — enforced, never redefined |
| Upstream | `03-system-analysis/state-transitions.md` | authoritative transition table |
| Upstream | `00-project-overview/project-constraints.md` | `C-01…C-26` hard boundaries |
| Peer | `07-api/` | endpoint contracts + error model this code exposes |
| Peer | `08-database/` | schema, entities, indexes backing Prisma models |
| Peer | `09-security/` | authentication design, RBAC matrix (this domain implements them) |
| Peer | `10-integrations/` | provider contracts behind adapters |
| Downstream | `05-frontend/` | consumes the API; mirrors rules as UX only |
| Downstream | `13-testing/`, `12-non-functional/` | verification and measurement of everything above |

## 6. Out of Scope for This Domain

- Endpoint-by-endpoint contract definition → `07-api/`.
- Table/schema design → `08-database/`.
- Security *decisions* (threat model, RBAC matrix, control selection) → `09-security/` (this domain shows where they are coded).
- Infrastructure, CI/CD, environments → `14-devops-infrastructure/`, `15-deployment/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
