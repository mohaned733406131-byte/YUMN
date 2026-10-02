---
document_id: DOC-REQ-002
title: 02 Requirements — README
category: 02-requirements
status: approved
version: 1.3
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-REQ-001]
---

# 02 — Requirements

## Purpose

The **requirements source of truth**. Nothing else may define what the system must do.

## Source of Truth For

All requirement IDs: `FR-*` (functional), `NFR-*` (non-functional), `SEC-REQ-*` (security), `DATA-REQ-*` (data), `INT-REQ-*` (integration) — plus project-level acceptance criteria.

## Contents

| File / Directory | Purpose |
|---|---|
| [requirements-overview.md](requirements-overview.md) | **Canonical registry of all 68 requirement IDs** — read this first |
| [requirements-overview.md §1](requirements-overview.md) | Functional requirements index |
| [functional/](functional/index.md) | `FR-001…FR-020` — one file per requirement |
| [non-functional/](non-functional-index.md) | `NFR-001…NFR-020` — measurable quality requirements |
| [security/](security-index.md) | `SEC-REQ-001…SEC-REQ-012` |
| [data/](data/index.md) | `DATA-REQ-001…DATA-REQ-008` |
| [integration/](integration-index.md) | `INT-REQ-001…INT-REQ-008` |
| [acceptance-criteria.md](acceptance-criteria.md) | `AC-*` acceptance criteria grouped per FR |
| [`core/`](core/README.md) | DOC-REQ-003 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-REQ-004 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-REQ-005 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-REQ-006 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-REQ-007 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## Dependencies

- Consumes: `00-project-overview/` (objectives, constraints, actors)
- Consumes: `01-business-analysis/` (rules refine requirements; requirements never contradict rules)
- Produces for: `03-system-analysis/`, `04-architecture/`, `13-testing/`, `19-traceability/`

## Requirement File Anatomy

Every requirement file contains:

```text
ID · Title · Status · Priority · Source
Description
Rationale (why — traces to OBJ-* or C-*)
Dependencies (other FR/NFR/DEP)
Preconditions
Expected result
Acceptance criteria (AC-FRnnn-nn)
Verification method (test type / evidence)
Constraints honored (C-*)
Open questions (if any → GAP-*)
```

## Quality Rules

1. IDs are assigned **only** in `requirements-overview.md`.
2. A requirement without measurable acceptance criteria is incomplete.
3. Contradictions between requirements and rules/architecture go to `../20-validation/core/contradiction-audit.md` — never silently patched.
4. Deprecated requirements keep their ID with status `SUPERSEDED`; IDs are never reused.

## Naming Conventions

`FR-nnn.md` · `NFR-nnn.md` · `SEC-REQ-nnn.md` · `DATA-REQ-nnn.md` · `INT-REQ-nnn.md` · acceptance criteria `AC-FR012-01`.

## Related Directories

`01-business-analysis/` (rules) · `03-system-analysis/` (behavior) · `19-traceability/` (links) · `20-validation/` (audits) · `13-testing/` (verification)

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial publication | Analysis-phase authoring (root README §7) |
| 1.1 | 2026-09-29 | `## Change History` section added | Session 009 `CHK-05` re-run — consistency finding 2; root README §9.2 requires the section on every document |
| 1.2 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-REQ-003…DOC-REQ-007) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
| 1.3 | 2026-10-02 | Reference paths updated for the section-grouping migration (data/ + functional/ sections) | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
