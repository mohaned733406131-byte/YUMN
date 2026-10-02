---
document_id: DOC-ARCH-001
title: 04 Architecture — README
category: 04-architecture
status: approved
version: 1.4
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-003, NFR-005, NFR-009, NFR-018]
related_documents: [DOC-ROOT-001, DOC-SA-001, DOC-OVR-008, DOC-REQ-001, DOC-ARCH-002]
---

# 04 — Architecture

## Purpose

Answers: **How is yumn structured, and which technologies realize it?** This directory is the technical counterpart of `03-system-analysis/`: it takes the behavior, flows and logical components defined there and gives them a structure — containers, modules, deployment topology, data-flow mechanics, scalability levers, the concrete stack, and the index of architectural decisions.

It is the entry point for architects and developers (root README §3) and the source material for `06-backend/`, `07-api/`, `08-database/`, `14-devops-infrastructure/` and `18-decisions/`.

## Contents

| File / Directory | document_id | Purpose |
|---|---|---|
| [README.md](README.md) | DOC-ARCH-001 | This index — directory purpose, dependencies, conventions, quality rules |
| [architecture-overview.md](core/architecture-overview.md) | DOC-ARCH-002 | **Source of truth for technical architecture:** C4 level-1 context + containers, principles (`C-18`, `C-21`), quality attributes (`C-25`, `C-26`), major technology choices |
| [container-view.md](core/container-view.md) | DOC-ARCH-003 | The deployable containers — Next.js 14 web, RN 0.73 apps, NestJS API monolith, PostgreSQL 16, Redis 7, BullMQ workers, Elasticsearch 8, MinIO — and how they communicate |
| [component-view.md](core/component-view.md) | DOC-ARCH-004 | Internal components/modules of the NestJS monolith per `B01…B13`: responsibilities, provided interfaces, dependencies |
| [deployment-view.md](core/deployment-view.md) | DOC-ARCH-005 | Docker Compose deployment (`C-22`): services, ports, networks, volumes, dev/staging/prod parity, no-K8s rationale |
| [module-boundaries.md](core/module-boundaries.md) | DOC-ARCH-006 | Modular-monolith boundaries: allowed dependencies, enforcement via lint/import rules, shared kernel, cross-cutting concerns |
| [data-flow.md](core/data-flow.md) | DOC-ARCH-007 | TECHNICAL data flow: request path, BullMQ async paths, caching layers, event flow, storage — counterpart to `../03-system-analysis/core/data-flow.md` |
| [scalability.md](core/scalability.md) | DOC-ARCH-008 | How the architecture meets `C-25` (10,000 concurrent) and `NFR-003`/`NFR-018`: read scaling, caching, pooling, statelessness, ES offload, scale-out path without K8s |
| [technology-stack.md](core/technology-stack.md) | DOC-ARCH-009 | Full stack register: layer, technology, version, rationale, constraint reference, alternatives considered |
| [architecture-decisions-reference.md](core/architecture-decisions-reference.md) | DOC-ARCH-010 | Index of architectural decisions (`ADR-001…ADR-010`) with rationale summaries, each pointing to its ADR in `18-decisions/core/` |
| [`core/`](core/README.md) | DOC-ARCH-011 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-ARCH-012 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-ARCH-013 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-ARCH-014 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-ARCH-015 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## Source of Truth For

- **Technical architecture (principles, C4 context/containers, quality-attribute drivers)** — `architecture-overview.md` (DOC-ARCH-002).
- **Container inventory and communication** — `container-view.md` (DOC-ARCH-003).
- **Deployment topology** — `deployment-view.md` (DOC-ARCH-005).
- **Stack register** — `technology-stack.md` (DOC-ARCH-009).
- **ADR index** — `core/architecture-decisions-reference.md` (DOC-ARCH-010); individual ADR texts live only in `18-decisions/core/`.

Behavior, rules and requirement definitions are **not** redefined here — they are referenced by ID from `03-system-analysis/`, `01-business-analysis/business-rules.md` (DOC-BA-005) and `02-requirements/requirements-overview.md` (DOC-REQ-001).

## Dependencies

| Direction | Directory | What flows |
|---|---|---|
| Consumes | `03-system-analysis/` | System boundary, context, logical components (`LC-*`), data flows, edge cases, failure modes, 17-state machine |
| Consumes | `00-project-overview/` | Constraints `C-01…C-26`, blocks `B01…B13`, assumptions `ASM-*`, dependencies `DEP-*` |
| Consumes | `02-requirements/` | `NFR-*` quality targets, `SEC-REQ-*`, `INT-REQ-*`, `DATA-REQ-*` |
| Feeds | `06-backend/`, `05-frontend/`, `07-api/`, `08-database/` | Module structure, request paths, data-flow mechanics become implementation guides |
| Feeds | `14-devops-infrastructure/`, `15-deployment/` | Compose topology, environments, health gates |
| Feeds | `18-decisions/` | Decisions indexed in DOC-ARCH-010 are written as full ADRs there |
| Feeds | `12-non-functional/`, `13-testing/` | Scalability levers become load-test scenarios (`NFR-003`), availability targets (`NFR-005`) |

## Conventions

| Kind | Pattern | Example | Defined in |
|---|---|---|---|
| Documents | `DOC-ARCH-NNN` | DOC-ARCH-007 | frontmatter of each file |
| Decisions | `ADR-NNN` | ADR-004 | `core/architecture-decisions-reference.md`, authored in `18-decisions/core/` |
| Containers | `CNT-NN` | CNT-03 | `container-view.md` |
| Modules | module name = block (`B01…B13`) | `OrderModule` = B06 | `component-view.md` |
| Compose services | kebab-case service names | `api`, `worker`, `postgres` | `deployment-view.md` |
| Queues | `{block}.{entity}.{action}` | `b07.escrow.release` | `../06-backend/core/background-processing.md` §1 (rule `BR-PLT-01`) — single queue register |
| API endpoint groups | `API-<GROUP>-NNN` | `API-WAL-003` (top-up) | registry `../07-api/core/endpoints-index.md` — 14 groups, 221 endpoints |
| Database entities | `DB-NNN` in schemas `b01…b13` | `b06` orders schema | registry `../08-database/core/entities-index.md` — `DB-001…DB-018` |
| Test cases | `TC-NNN` | `TC-104` | registry `../13-testing/core/test-cases-index.md` — `TC-001…TC-114`; this directory references load/resilience scenarios by `NFR-*` instead |

## Quality Rules for This Directory

1. Architecture never violates a constraint: no microservices (`C-21`), no Kubernetes (`C-22`), no non-PostgreSQL RDBMS (`C-19`), no non-BullMQ queue (`C-20`), no commerce platform (`C-18`).
2. Every technology choice cites its constraint or `NFR-*` driver and an alternative considered (`technology-stack.md`).
3. Container/module/queue names introduced here are used consistently by `06-backend/`, `07-api/`, `14-devops-infrastructure/`.
4. Where an architecture detail is not fixed by canon, it is tagged `INFERENCE`.
5. Any conflict with `03-system-analysis/` (behavior contract) is logged in `../20-validation/core/contradiction-audit.md` — behavior wins over structure.
6. Decisions are changed only by writing/ superseding an ADR in `18-decisions/` (root README §9) and updating DOC-ARCH-010.

## Reading Order by Role

| Role | Read first | Then |
|---|---|---|
| Architect | DOC-ARCH-002 → DOC-ARCH-003 | DOC-ARCH-006, DOC-ARCH-010, DOC-SA-002/003 (behavior context) |
| Backend developer | DOC-ARCH-004 → DOC-ARCH-006 | DOC-ARCH-007, then `06-backend/`, `07-api/` |
| Frontend / mobile developer | DOC-ARCH-003 (client containers) | `05-frontend/`, `07-api/` |
| DevOps / SRE | DOC-ARCH-005 → DOC-ARCH-008 | `14-devops-infrastructure/`, `15-deployment/` |
| Tech lead / decision maker | DOC-ARCH-010 → DOC-ARCH-009 | `18-decisions/core/`, `17-risk-management/` |
| QA architect | DOC-ARCH-007 → DOC-ARCH-008 | `13-testing/`, `19-traceability/` |

## Cross-Document Contracts (what 04 owes to other directories)

| Consumer | Contract this directory provides | Owner file |
|---|---|---|
| `06-backend/` | Module list, allowed dependencies, queue names, cross-cutting placement | DOC-ARCH-004, DOC-ARCH-006, DOC-ARCH-007 |
| `07-api/` | Container entry points, request-path stages, error/health expectations | DOC-ARCH-003, DOC-ARCH-007 |
| `08-database/` | One-schema-per-block rule, system-of-record vs derived data split, partitioning intent | DOC-ARCH-006, DOC-ARCH-008 |
| `05-frontend/` | Client containers, SSR/RTL drivers, performance budgets | DOC-ARCH-003, DOC-ARCH-009 |
| `10-integrations/` | Adapter boundary (no provider types in domain), webhook intake path | DOC-ARCH-004, DOC-ARCH-007 |
| `12-non-functional/` | Scalability levers, degradation table, observability hooks | DOC-ARCH-008, DOC-ARCH-007 |
| `14-devops-infrastructure/`, `15-deployment/` | Compose service/network/volume topology, health gates, pipeline stages | DOC-ARCH-005 |
| `18-decisions/` | Reserved ADR numbers and rationale summaries to expand | DOC-ARCH-010 |
| `19-traceability/`, `20-validation/` | Constraint → decision mapping for audits | DOC-ARCH-009, DOC-ARCH-010 |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | Registry stub rows replaced: the three stale `07-api/`/`08-database/`/`13-testing/` registry stub rows now point at the real registries with paths, ID ranges and real examples (`API-WAL-003`, `DB-001…DB-018`, `TC-001…TC-114`) | `REC-08`/`TD-09` pay-down — stale stubs caused the stop-or-invent-ID failure mode root README §5 forbids |
| 1.2 | 2026-09-27 | Queues row: example corrected (`b07.wallet.topup` → `b07.escrow.release`) and Defined-in repointed from `data-flow.md` to the single queue register `../06-backend/core/background-processing.md` §1 | `REC-06`/`TD-07` pay-down — register ownership per `naming-conventions.md` §3 |
| 1.3 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-ARCH-011…DOC-ARCH-015) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
| 1.4 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |


