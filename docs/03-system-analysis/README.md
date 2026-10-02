---
document_id: DOC-SA-001
title: 03 System Analysis — README
category: 03-system-analysis
status: approved
version: 1.7
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [FR-011, FR-012, FR-015]
related_documents: [DOC-ROOT-001, DOC-OVR-002, DOC-REQ-001, DOC-BA-005, DOC-SA-010]
---

# 03 — System Analysis

## Purpose

Answers: **What does yumn do, and how does it behave — independent of any technology choice?** This directory holds the analytical system view: the system boundary, the context around the system, per-block functional analysis of every `FR-*`, logical data flows, technology-independent components, end-to-end sequence flows, edge cases, and failure handling.

It sits between `02-requirements/` (what the system *must* do — static statements of need) and `04-architecture/` (how the system is *structured* — technical realization). Requirements arrive here as behavior; they leave here as component responsibilities and flows that architecture must realize.

## Contents

| File / Directory | document_id | Purpose |
|---|---|---|
| [README.md](README.md) | DOC-SA-001 | This index — directory purpose, boundary vs architecture distinction, conventions |
| [system-boundary.md](core/system-boundary.md) | DOC-SA-002 | What is inside vs outside yumn (`C-18` custom build), boundary-crossing actors, external systems per `INT-REQ-*`, trust zones |
| [system-context.md](core/system-context.md) | DOC-SA-003 | Context view: the 7 actors and external entities around yumn, with responsibilities, inputs and outputs |
| [functional-analysis.md](core/functional-analysis.md) | DOC-SA-004 | Methodology §11 — per-block (`B01…B13`) analysis mapping every `FR-*` to behavior, validations, processing logic and outputs |
| [data-flow.md](core/data-flow.md) | DOC-SA-005 | ANALYSIS-level logical data flows between actors, processes and conceptual data stores (technical counterpart: `../04-architecture/core/data-flow.md`, DOC-ARCH-007) |
| [logical-components.md](core/logical-components.md) | DOC-SA-006 | Technology-independent logical components derived from `B01…B13`: responsibilities, provided interfaces, required interfaces, interactions |
| [sequence-flows.md](core/sequence-flows.md) | DOC-SA-007 | Key end-to-end sequence flows as text diagrams: browse→checkout→delivery→completion, return, vendor onboarding, wallet top-up, dispute |
| [edge-cases.md](core/edge-cases.md) | DOC-SA-008 | Edge cases per domain (`EC-NN`) with expected system behavior and the `BR-*` / `C-*` references that govern them |
| [failure-modes.md](core/failure-modes.md) | DOC-SA-009 | Failure modes (`FM-NN`) and analysis-level handling: provider outage, idempotency, double-debit, code mismatch, webhook retries, oversell |
| [state-transitions.md](core/state-transitions.md) | DOC-SA-010 | **The canonical 17-state order machine (`C-09`) — single source of truth for states and transitions** (pre-existing) |
| [erp-finance-departments.md](core/erp-finance-departments.md) | DOC-SA-011 | Finance/ERP department surface: platform + per-merchant books, six departments (accounts, sales, purchases, inventory, reports, periods), dept↔staff map, period-close mechanics, phasing — approved via `plan-develop.md` §8 (`D2`/`D3`/`D11`) |
| [`core/`](core/README.md) | DOC-SA-012 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-SA-013 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-SA-014 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-SA-015 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-SA-016 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## How 03 Differs From 04-Architecture

| Question | `03-system-analysis/` (this directory) | `04-architecture/` |
|---|---|---|
| Viewpoint | Analysis — behavior and meaning | Design — structure and technology |
| Typical wording | "When payment succeeds, the order enters `PLACED`" | "The `OrderModule` commits the transaction and publishes `order.placed` to Redis" |
| Technology | Named only as an external-contract fact (`INT-REQ-*` providers) | Central: containers, modules, deployment, stack |
| Data | Conceptual stores ("Wallet & Ledger Store") | Physical: PostgreSQL schemas `b01…b13`, MinIO buckets, ES indices |
| Unit of decomposition | Blocks `B01…B13` and logical components | Containers and NestJS modules |
| Diagram style | Context, DFD-level flows, sequence flows | C4 context/containers, deployment, module dependency rules |
| Stays valid if… | The tech stack changes | Stack choice changes invalidate it |

Rule of thumb: **03 says what happens and why; 04 says which component does it and with what.** A statement about a `BR-*` rule belongs in 03; a statement about a Prisma transaction belongs in 04. When both could describe an event (e.g. order placement), 03 defines the behavior contract and 04 documents its realization — they must never disagree, and any conflict is logged in `../20-validation/core/contradiction-audit.md`.

## Source of Truth For

- **System boundary and trust zones** — `system-boundary.md` (DOC-SA-002).
- **Context view (actors + external entities)** — `system-context.md` (DOC-SA-003).
- **Order state machine** — `state-transitions.md` (DOC-SA-010), the canonical 17 states required by `C-09`.
- **Edge-case and failure-mode inventories** (`EC-NN`, `FM-NN`) — `edge-cases.md` (DOC-SA-008), `failure-modes.md` (DOC-SA-009).

Behavioral documents in this directory **reference** `BR-*` IDs (DOC-BA-005) and `FR-*` IDs (DOC-REQ-001); they never restate or amend a rule definition.

## Dependencies

| Direction | Directory | What flows |
|---|---|---|
| Consumes | `00-project-overview/` | Actors `ACT-01…ACT-07`, constraints `C-01…C-26`, blocks `B01…B13`, scope exclusions |
| Consumes | `01-business-analysis/` | 111 rules `BR-*`, processes `BP-01…BP-15`, workflows `WF-001…WF-012`, use cases `UC-001…UC-420` |
| Consumes | `02-requirements/` | All 68 `FR-*` / `NFR-*` / `SEC-REQ-*` / `DATA-REQ-*` / `INT-REQ-*` |
| Feeds | `04-architecture/` | Logical components become modules; flows become technical data flows |
| Feeds | `07-api/`, `08-database/` | Behavior contracts become endpoints; conceptual stores become schemas `b01…b13` |
| Feeds | `13-testing/`, `19-traceability/` | `EC-*` / `FM-*` scenarios become negative and resilience test cases |

## Conventions

| Kind | Pattern | Example | Defined in |
|---|---|---|---|
| Documents | `DOC-SA-NNN` | `DOC-SA-005` | frontmatter of each file |
| Edge cases | `EC-NN` | `EC-04` | `edge-cases.md` |
| Failure modes | `FM-NN` | `FM-07` | `failure-modes.md` |
| Logical data flows | `DF-NN` | `DF-12` | `data-flow.md` |
| Logical components | `LC-NN` | `LC-04` | `logical-components.md` |
| Sequence flows | `SQ-NN` | `SQ-03` | `sequence-flows.md` |
| API endpoint groups | `API-<GROUP>-NNN` | `API-WAL-003` (top-up) | registry `../07-api/core/endpoints-index.md` — 14 groups (`ATH USR VND CAT SRC CRT ORD WAL SHP RET NTF CNT ANL ADM`), 221 endpoints; never cite an endpoint ID that is not in that registry |
| Database entities | `DB-NNN` in schema `b01…b13` | wallet schema `b07` | registry `../08-database/core/entities-index.md` — `DB-001…DB-018`, one file per entity; here stores are conceptual (`DS1…DS16`) |
| Test cases | `TC-NNN` | `TC-104` | registry `../13-testing/core/test-cases-index.md` — `TC-001…TC-114`; here verification is described by scenario and cited by `TC-` ID |

Files use `lowercase-kebab-case.md`. Statements beyond canon are evidence-tagged `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE` per root README §8.

## Quality Rules for This Directory

1. Never copy a rule or requirement definition — reference `BR-*` / `FR-*` IDs only (root README §4).
2. Nothing here may contradict `C-01…C-26`, the 17-state machine (DOC-SA-010), or `business-rules.md` — constraints and rules win.
3. Exactly 17 order states; "escalation to admin review" is an escalation, never an 18th state (`BR-SHP-06`, `BR-ORD-10`).
4. All 7 actors only — `ACT-01…ACT-07`; no invented roles.
5. Technology appears here only as an external contract (provider names in `INT-REQ-*`); implementation detail belongs in `04-architecture/`.
6. Every edge case and failure mode names its expected system behavior, not just the failure.

## Reading Order

| Need | Start with | Then |
|---|---|---|
| "What is in scope for the system?" | `system-boundary.md` (DOC-SA-002) | `system-context.md` (DOC-SA-003) |
| "What does block Bxx actually do?" | `functional-analysis.md` (DOC-SA-004) | relevant `FR-*` file in `02-requirements/` |
| "What data moves where?" | `data-flow.md` (DOC-SA-005) | `../04-architecture/core/data-flow.md` for the technical path |
| "How does the order flow end to end?" | `sequence-flows.md` (DOC-SA-007) | `01-business-analysis/` for step tables |
| "What can go wrong?" | `edge-cases.md` (DOC-SA-008) | `failure-modes.md` (DOC-SA-009) |
| "What are the exact order states?" | `state-transitions.md` (DOC-SA-010) | `13-testing/` for the state-machine suite |
| "How are the finance/ERP departments organised?" | `erp-finance-departments.md` (DOC-SA-011) | `../09-security/core/rbac.md` §11 for the permission model; `plan-develop.md` §4 for connector mechanics |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | Registry stub rows replaced: the three stale `07-api/`/`08-database/`/`13-testing/` registry stub rows now point at the real registries with paths, ID ranges and real examples (`API-WAL-003`, `DB-001…DB-018`, `TC-001…TC-114`) | `REC-08`/`TD-09` pay-down — stale stubs caused the stop-or-invent-ID failure mode root README §5 forbids |
| 1.2 | 2026-09-28 | Contents + reading-order rows added for `erp-finance-departments.md` (`DOC-SA-011`, minted here) | `plan-develop.md` §8 approval implementation (session 007) — new analysis document registered in its domain index (SPE-05) |
| 1.3 | 2026-09-28 | Consumes row count sync: 99 → **104 rules** (`BR-INV-01…05` registered) | `CRIT-06`/`HAL-04` pay-down (session 008) — consumer of `business-rules.md` v1.1 (root README §9.4) |
| 1.4 | 2026-09-29 | Consumes row use-case range sync: `UC-001…UC-040` → **`UC-001…UC-210`** (210 use-case files) | `prompt-010.md` §1 (session 010 owner directive — `UC-043`…`UC-210` minted) |
| 1.5 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-SA-012…DOC-SA-016) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
| 1.6 | 2026-09-30 | Consumes-row count sync: 104 → **111 rules** (`business-rules.md` v1.2); use-case range `UC-001…UC-210` → **`UC-001…UC-420`** (phase 6 minting complete) | Owner directive session 011 (`prompt-011.md` §4.6–4.7) — consumer of `business-rules.md` + UC index; counts re-synced in same change set |
| 1.7 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
