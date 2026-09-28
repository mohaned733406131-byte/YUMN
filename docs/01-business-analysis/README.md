---
document_id: DOC-BA-001
title: 01 Business Analysis — README
category: 01-business-analysis
status: approved
version: 1.2
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [FR-011, FR-012, FR-020]
related_documents: [DOC-ROOT-001, DOC-OVR-001, DOC-REQ-002]
---

# 01 — Business Analysis

## Purpose

Answers: **How does the yumn marketplace actually work as a business?** This directory holds the business-side view of the platform: the business model, business objectives, end-to-end business processes, stakeholder and user needs, the canonical business-rule registry, use cases, and end-to-end workflows.

It is the bridge between `00-project-overview/` (what the project is) and `02-requirements/` (what the system must do): business needs and processes here are realized as `FR-*` requirements there, and every rule in `business-rules.md` is traceable to at least one `FR-*`.

## Contents

| File / Directory | document_id | Purpose |
|---|---|---|
| [README.md](README.md) | DOC-BA-001 | This index — directory purpose, dependencies, conventions |
| [business-model.md](business-model.md) | DOC-BA-002 | Multi-vendor marketplace model: value proposition, revenue streams, cost structure, partners, channels, metrics, worked unit economics |
| [business-objectives.md](business-objectives.md) | DOC-BA-003 | Business-side objectives `BO-01…BO-12` (liquidity, retention, payment trust, operational efficiency) with owner, metric, target |
| [business-processes.md](business-processes.md) | DOC-BA-004 | The 15 major business processes `BP-01…BP-15`: trigger, actors, steps, systems, rules applied, final state, failure paths |
| [business-rules.md](business-rules.md) | DOC-BA-005 | **The canonical business-rule registry — 104 rules `BR-<DOMAIN>-NN` (authoritative; see note below)** |
| [stakeholder-needs.md](stakeholder-needs.md) | DOC-BA-006 | Needs of each `STK-*` stakeholder group, how yumn addresses them, related `FR-*`/`BR-*`, conflict notes |
| [user-needs.md](user-needs.md) | DOC-BA-007 | Per-actor (`ACT-01…ACT-06`) needs: jobs-to-be-done, pains today, how addressed, success signals; guest vs registered customer |
| `use-cases/` | — | Use case specifications `UC-NNN` (one file per use case), derived from the processes here and consumed by `13-testing/` |
| [workflows/README.md](workflows/README.md) | DOC-WF-001 | Index and format specification for the 12 end-to-end workflows `WF-001…WF-012` |
| [workflows/](workflows/workflow-001.md) | DOC-WF-002…DOC-WF-013 | One file per workflow: ASCII flow + step table (actor, action, system, rules, data changes, failure handling) |

## Source of Truth For

- **Business rules** — `business-rules.md` (DOC-BA-005) is **the single authoritative registry of all 104 `BR-*` rules**. No other document may define, restate, or amend a rule; every other document only *references* rule IDs. Rule domains: `AUTH CAT VND CRT ORD PAY ESC SHP RET NTF PRM REV PLT FIN INV`.
- **Business processes** (`BP-01…BP-15`) — `business-processes.md`.
- **Business objectives** (`BO-01…BO-12`) — `business-objectives.md` (project objectives `OBJ-01…OBJ-12` remain in `00-project-overview/project-objectives.md`).
- **End-to-end workflows** (`WF-001…WF-012`) — `workflows/`.
- **Business/user/stakeholder needs** — `stakeholder-needs.md`, `user-needs.md`.

> **Authoritative-rule rule:** if any document in this repository conflicts with `business-rules.md`, `business-rules.md` wins and the conflict is logged in `20-validation/contradiction-audit.md` — never silently patched.

## Dependencies

| Direction | Directory | What flows |
|---|---|---|
| Consumes | `00-project-overview/` | Actors (`ACT-*`), constraints (`C-01…C-26`), objectives (`OBJ-*`), stakeholders (`STK-*`), scope, assumptions (`ASM-*`), dependencies (`DEP-*`) |
| Consumes | `02-requirements/` | Requirement registry `FR-001…FR-020` (rules and processes trace forward to them) |
| Feeds | `02-requirements/` | Processes and needs refine into `FR-*`; every `BR-*` traces to ≥1 `FR-*` |
| Feeds | `03-system-analysis/` | Processes and workflows are the source for behavior analysis and the 17-state machine checks (`C-09`) |
| Feeds | `09-security/`, `07-api/` | Actor/rule references from this directory drive RBAC and endpoint authorization checks |
| Feeds | `13-testing/`, `19-traceability/` | `BR-*`, `UC-*`, `WF-*` IDs appear in test cases and traceability matrices |

## Related Directories

`00-project-overview/` (inputs) · `02-requirements/` (outputs) · `03-system-analysis/` (behavior) · `13-testing/` (verification) · `19-traceability/` (links) · `20-validation/` (audits) · `22-glossary/` (terms)

## Naming Conventions

| Kind | Pattern | Example | Defined in |
|---|---|---|---|
| Business rules | `BR-<DOMAIN>-NN` | `BR-ESC-05` | `business-rules.md` (authoritative) |
| Use cases | `UC-NNN` | `UC-021` | `use-cases/` |
| Workflows | `WF-NNN` | `WF-006` | `workflows/README.md` |
| Business processes | `BP-NN` | `BP-07` | `business-processes.md` |
| Business objectives | `BO-NN` | `BO-03` | `business-objectives.md` |
| Documents | `DOC-BA-NNN` / `DOC-WF-NNN` | `DOC-BA-005` | frontmatter of each file |

Files use `lowercase-kebab-case.md`; workflow files are `workflow-NNN.md` where `NNN` is the zero-padded workflow number (`workflow-003.md` = `WF-003`).

## Quality Rules for This Directory

1. Never copy a rule definition — reference `BR-*` IDs only (root README §4).
2. Rules never contradict constraints (`C-01…C-26`); constraints win.
3. Every process and workflow names its failure paths, not just the happy path.
4. Actors used anywhere in this directory must be the canonical 7 (`ACT-01…ACT-07`, `00-project-overview/actors-and-roles.md`).
5. Statements are evidence-tagged (`VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`) where they go beyond the canon.
6. `business-rules.md` is modified only through change management (root README §9) — never edited as a side effect of another document change.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | Registry count sync: 99 → **104 rules** (`BR-INV-01…05` registered) | `CRIT-06`/`HAL-04` pay-down (session 008) — consumer of `business-rules.md` v1.1 (root README §9.4) |
| 1.2 | 2026-09-28 | §Source-of-Truth catch-up: the "single authoritative registry" bullet still said **99** rules and listed only **14** domains — synced to **104** + `INV` (the v1.1 sync had covered only the Contents row) | BR-count propagation catch-up (session 008 close) — root README §9.4; missed consumer of `business-rules.md` v1.1 |
