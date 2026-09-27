---
document_id: DOC-SA-001
title: 03 System Analysis — README
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
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
| [system-boundary.md](system-boundary.md) | DOC-SA-002 | What is inside vs outside yumn (`C-18` custom build), boundary-crossing actors, external systems per `INT-REQ-*`, trust zones |
| [system-context.md](system-context.md) | DOC-SA-003 | Context view: the 7 actors and external entities around yumn, with responsibilities, inputs and outputs |
| [functional-analysis.md](functional-analysis.md) | DOC-SA-004 | Methodology §11 — per-block (`B01…B13`) analysis mapping every `FR-*` to behavior, validations, processing logic and outputs |
| [data-flow.md](data-flow.md) | DOC-SA-005 | ANALYSIS-level logical data flows between actors, processes and conceptual data stores (technical counterpart: `04-architecture/data-flow.md`, DOC-ARCH-007) |
| [logical-components.md](logical-components.md) | DOC-SA-006 | Technology-independent logical components derived from `B01…B13`: responsibilities, provided interfaces, required interfaces, interactions |
| [sequence-flows.md](sequence-flows.md) | DOC-SA-007 | Key end-to-end sequence flows as text diagrams: browse→checkout→delivery→completion, return, vendor onboarding, wallet top-up, dispute |
| [edge-cases.md](edge-cases.md) | DOC-SA-008 | Edge cases per domain (`EC-NN`) with expected system behavior and the `BR-*` / `C-*` references that govern them |
| [failure-modes.md](failure-modes.md) | DOC-SA-009 | Failure modes (`FM-NN`) and analysis-level handling: provider outage, idempotency, double-debit, code mismatch, webhook retries, oversell |
| [state-transitions.md](state-transitions.md) | DOC-SA-010 | **The canonical 17-state order machine (`C-09`) — single source of truth for states and transitions** (pre-existing) |

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

Rule of thumb: **03 says what happens and why; 04 says which component does it and with what.** A statement about a `BR-*` rule belongs in 03; a statement about a Prisma transaction belongs in 04. When both could describe an event (e.g. order placement), 03 defines the behavior contract and 04 documents its realization — they must never disagree, and any conflict is logged in `20-validation/contradiction-audit.md`.

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
| Consumes | `01-business-analysis/` | 99 rules `BR-*`, processes `BP-01…BP-15`, workflows `WF-001…WF-012`, use cases `UC-001…UC-040` |
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
| API endpoint groups | `API-<GROUP>-NNN` | `API-TOP-*` (top-up group, cited by `C-05`) | registry `07-api/` — not yet authored; never cite an endpoint ID that is not in that registry |
| Database entities | `DB-NNN` in schema `b01…b13` | wallet schema `b07` | registry `08-database/` — not yet authored; here stores are conceptual (`DS1…DS16`) |
| Test cases | `TC-NNN` | — | registry `13-testing/` — not yet authored; here verification is described by scenario, not by TC ID |

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
| "What does block Bxx actually do?" | `functional-analysis.md` (DOC-SA-004) | relevant `FR-*` file in `02-requirements/functional/` |
| "What data moves where?" | `data-flow.md` (DOC-SA-005) | `04-architecture/data-flow.md` for the technical path |
| "How does the order flow end to end?" | `sequence-flows.md` (DOC-SA-007) | `01-business-analysis/workflows/` for step tables |
| "What can go wrong?" | `edge-cases.md` (DOC-SA-008) | `failure-modes.md` (DOC-SA-009) |
| "What are the exact order states?" | `state-transitions.md` (DOC-SA-010) | `13-testing/` for the state-machine suite |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
