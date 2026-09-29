---
document_id: DOC-OVR-001
title: 00 Project Overview — README
category: 00-project-overview
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-29
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-ROOT-001]
---

# 00 — Project Overview

## Purpose

Answers: **What is the project? Why does it exist? Who uses it? What are its goals, scope, constraints, and success criteria?**

This directory is the identity layer of the knowledge base. Every other directory depends on it; it depends on nothing.

## Contents

| File | Purpose |
|---|---|
| [project-context.md](project-context.md) | System definition, problem statement, market/domain context, compliance context, 13-block decomposition |
| [project-charter.md](project-charter.md) | Executive summary, authority, vision, mission, high-level deliverables |
| [project-objectives.md](project-objectives.md) | `OBJ-01…OBJ-12` measurable objectives |
| [project-scope.md](project-scope.md) | IN / OUT / FUTURE / UNCERTAIN scope + scope-creep control |
| [stakeholders.md](stakeholders.md) | Stakeholder register, roles, goals, conflicts |
| [actors-and-roles.md](actors-and-roles.md) | The 7 actors, role hierarchy, RBAC summary |
| [project-constraints.md](project-constraints.md) | `C-01…C-26` non-negotiable constraints + verification methods |
| [assumptions.md](assumptions.md) | `ASM-01…ASM-15` with evidence status and verification |
| [dependencies.md](dependencies.md) | `DEP-01…DEP-12` internal/external dependencies |
| [success-criteria.md](success-criteria.md) | Measurable acceptance-level success criteria |

## Source of Truth For

Project identity · scope · actors · constraints · assumptions · dependencies · success criteria.

## Dependencies

None (root of the analysis).

## Related Directories

- `01-business-analysis/` — consumes actors & constraints to derive rules
- `02-requirements/` — every requirement traces back to `OBJ-*` / `C-*`
- `17-risk-management/` — risks reference `ASM-*` and `DEP-*`

## Naming Conventions

`OBJ-` objectives · `C-` constraints · `ASM-` assumptions · `DEP-` dependencies · `STK-` stakeholders · `ACT-` actors.

## Important Note

All quantitative targets (scale, availability, performance) originate here and in `02-requirements/non-functional/`. Changing a value here requires propagation to NFRs, architecture, and tests (consistency rule → `20-validation/consistency-audit.md`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial publication | Analysis-phase authoring (root README §7) |
| 1.1 | 2026-09-29 | `## Change History` section added | Session 009 `CHK-05` re-run — consistency finding 2; root README §9.2 requires the section on every document |
