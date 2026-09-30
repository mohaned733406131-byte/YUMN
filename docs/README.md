---
document_id: DOC-ROOT-001
title: yumn Analysis Documentation — Master Index
category: root
status: approved
version: 1.5
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: []
---

# yumn — Analysis Documentation Knowledge Base

| Field | Value |
|---|---|
| Project Name | **yumn** (Arabic: يُمن) |
| Project Description | Multi-vendor e-commerce marketplace for Yemen — Arabic-first (RTL), wallet-only payments, custom-built |
| Documentation Version | 1.3 |
| Last Updated | 2026-09-28 |
| Documentation Status | APPROVED — analysis complete, ready for design/implementation planning |
| Project Status | ANALYZED (pre-implementation) |
| Language | English (single language of record) |

---

## 1. What This Repository Is

This repository is the **single, self-contained analysis knowledge base** for the yumn platform. It was produced from scratch using:

- **Methodology:** `command.md` — *Comprehensive Software Project Analysis & Validation Agent* (56 analysis areas, 48-part final structure, evidence rules, absolute rules).
- **Structure:** `archdoc.md` — *Analysis Documentation Structure Specification* (24 numbered documentation domains, metadata, status, source-of-truth, cross-referencing, AI navigation rules). ✅ **Restored 2026-09-28** (session 008, `REC-01`/`TD-03`): the file had been a 0-byte placeholder whose content never existed in git history (defect `D-10`); its content was reconstructed from the structure as implemented by this README (§2–§5) and validated by `20-validation/consistency-audit.md`, with that provenance stated inside the file (`SPE-03`, finding `HAL-03`).

`command.md` is the governing methodology document (28.7 KB, present). The claim that both governing documents are "archived under `archive/`" is **not verifiable — `archive/` does not exist** in this repository; treat it as an unproven statement (`SPE-03`) until evidence appears. Nothing inside `docs/` references archived content: this analysis is independent, evidence-tagged, and internally consistent.

---

## 2. Documentation Map

| # | Directory | Domain | Source of Truth For |
|---|---|---|---|
| 00 | [project-overview](00-project-overview/README.md) | Project identity | Charter, scope, actors, constraints, assumptions, success criteria |
| 01 | [business-analysis](01-business-analysis/README.md) | Business/domain perspective | Business model, processes, **business rules**, workflows, use cases |
| 02 | [requirements](02-requirements/README.md) | Requirements | **All requirement IDs** (FR / NFR / SEC-REQ / DATA-REQ / INT-REQ), acceptance criteria |
| 03 | [system-analysis](03-system-analysis/README.md) | Analytical system view | Boundary, context, components, state transitions, edge cases, failures |
| 04 | [architecture](04-architecture/README.md) | Technical architecture | Architecture views, principles, ADRs reference, module boundaries |
| 05 | [frontend](05-frontend/README.md) | Frontend architecture | Structure, routing, state, forms, auth handling, RTL, performance |
| 06 | [backend](06-backend/README.md) | Backend architecture | Modules, services, business-logic placement, background processing |
| 07 | [api](07-api/README.md) | API contract | Conventions, error model, pagination, **endpoint specifications** |
| 08 | [database](08-database/README.md) | Data structure | Schema, **entities**, relationships, constraints, indexes, migrations |
| 09 | [security](09-security/README.md) | Security | Threat model, controls, RBAC, secrets, **security findings (SEC-nnn)** |
| 10 | [integrations](10-integrations/README.md) | External systems | Payment, SMS, messaging, delivery integrations and failure behavior |
| 11 | [ui-ux](11-ui-ux/README.md) | UX design intent | User flows, information architecture, design system, states, feedback |
| 12 | [non-functional](12-non-functional/README.md) | NFR detail | Measurable performance, availability, scalability, maintainability, observability |
| 13 | [testing](13-testing/README.md) | Testing | Strategy, plans, test levels, **test cases (TC-nnn)** |
| 14 | [devops-infrastructure](14-devops-infrastructure/README.md) | Infrastructure | Environments, Docker, CI/CD, configuration, secrets, monitoring |
| 15 | [deployment](15-deployment/README.md) | Deployment | Build/release process, rollback, health checks, production readiness |
| 16 | [data](16-data/README.md) | Data as a system concern | Data lifecycle, ownership, classification, retention, deletion |
| 17 | [risk-management](17-risk-management/README.md) | Risk | **Risk register (RISK-nnn)**, categories, mitigation plans |
| 18 | [decisions](18-decisions/README.md) | Decisions | Decision log, **ADRs** (ADR-001…) |
| 19 | [traceability](19-traceability/README.md) | Traceability | Requirement → rule → component → API → DB → test matrices |
| 20 | [validation](20-validation/README.md) | Validation | Consistency, completeness, hallucination, contradiction audits |
| 21 | [completion](21-completion/README.md) | Completion | Roadmap, quality gates, definition of done, final acceptance |
| 22 | [glossary](22-glossary/README.md) | Terminology | Canonical term names, business/technical terms, naming conventions |
| 23 | [templates](23-templates/README.md) | Templates | Reusable templates for every document type |

**Process folders (not analysis domains):** [`phases/`](phases/README.md) — per-phase artifact sets (CORE-03/DOC-02, phase 0 created 2026-09-28) · [`sessions/`](sessions/README.md) — session work files with evidence (SES-01, created 2026-09-28). They carry `DOC-PHA-*` / `DOC-SES-*` IDs and are registered here so no document is an orphan (SPE-05).

---

## 3. How to Navigate

**Human readers** — follow the reading order below:

```text
1.  docs/README.md                      (this file)
2.  00-project-overview                 what & why
3.  01-business-analysis                domain rules & use cases
4.  02-requirements                     what the system must do
5.  03-system-analysis                  analytical behavior
6.  04-architecture                     how it is structured
7.  08-database                         data model
8.  06-backend                          server internals
9.  07-api                              contracts
10. 05-frontend                         client internals
11. 09-security                         security domain
12. 10-integrations                     external systems
13. 12-non-functional                   measurable quality
14. 13-testing                          verification
15. 14-devops-infrastructure            environments & pipelines
16. 15-deployment                       release & rollback
17. 17-risk-management                  risks
18. 18-decisions                        ADRs
19. 19-traceability                     cross-links
20. 20-validation                       audits
21. 21-completion                       roadmap & acceptance
```

**AI agents** — read each directory's `README.md` before analyzing that directory; never assume one directory yields complete knowledge. Start at the root README, then walk the order above.

**By role:**

| Role | Start Here |
|---|---|
| Product manager / stakeholder | 00 → 01 → 02 → 17 → 21 |
| Business analyst | 00 → 01 → 02 → 19 → 20 |
| Architect | 03 → 04 → 08 → 07 → 18 |
| Developer | 02 → 04 → 06 → 07 → 08 → 05 |
| QA engineer | 02 → 01 → 13 → 19 → 20 |
| Security engineer | 09 → 02/security → 06 → 07 → 13 |
| Designer | 11 → 05 → 00 |

---

## 4. Source-of-Truth Rules

One authoritative document per concept. Everywhere else, **reference the ID — never copy the definition**.

| Concept | Authoritative Location |
|---|---|
| Project identity, scope, constraints | `00-project-overview/` |
| Business rules | `01-business-analysis/business-rules.md` |
| Requirements | `02-requirements/` |
| System behavior (analysis level) | `03-system-analysis/` |
| Architecture | `04-architecture/` |
| API contract | `07-api/` |
| Database structure | `08-database/` |
| Security controls & findings | `09-security/` |
| Integration contracts | `10-integrations/` |
| Test cases | `13-testing/` |
| Decisions | `18-decisions/` |
| Terminology | `22-glossary/terminology.md` |

---

## 5. ID Conventions

Filenames: `lowercase-kebab-case.md`. Identifiers: `UPPERCASE-WITH-DASHES`. Never use names like `final.md`, `latest.md`, `new-final.md`.

| Kind | Pattern | Example | Defined In |
|---|---|---|---|
| Documents | `DOC-<CAT>-NNN` | `DOC-ARCH-004` | every file's frontmatter |
| Constraints | `C-NN` | `C-01` | `00-project-overview/project-constraints.md` |
| Objectives | `OBJ-NN` | `OBJ-03` | `00-project-overview/project-objectives.md` |
| Assumptions | `ASM-NN` | `ASM-05` | `00-project-overview/assumptions.md` |
| Dependencies | `DEP-NN` | `DEP-02` | `00-project-overview/dependencies.md` |
| Functional requirements | `FR-NNN` | `FR-012` | `02-requirements/core/` |
| Non-functional requirements | `NFR-NNN` | `NFR-005` | `02-requirements/core/` |
| Security requirements | `SEC-REQ-NNN` | `SEC-REQ-003` | `02-requirements/core/` |
| Data requirements | `DATA-REQ-NNN` | `DATA-REQ-004` | `02-requirements/core/` |
| Integration requirements | `INT-REQ-NNN` | `INT-REQ-002` | `02-requirements/core/` |
| Business rules | `BR-<DOMAIN>-NN` | `BR-PAY-04` | `01-business-analysis/business-rules.md` |
| Use cases | `UC-NNN` | `UC-017` | `01-business-analysis/<portal>/` |
| Workflows | `WF-NNN` | `WF-003` | `01-business-analysis/<portal>/` |
| Blocks | `B01…B13` | `B07` | `00-project-overview/project-context.md` |
| API endpoints | `API-<GROUP>-NNN` | `API-WAL-002` | `07-api/<portal>/` |
| Database entities | entity name + `DB-NNN` | `DB-006` | `08-database/core/` |
| Test cases | `TC-NNN` | `TC-021` | `13-testing/core/` |
| Risks | `RISK-NNN` | `RISK-007` | `17-risk-management/risk-register.md` |
| Decisions / ADRs | `ADR-NNN` | `ADR-003` | `18-decisions/core/` |
| Security findings | `SEC-NNN` | `SEC-011` | `09-security/core/` |
| Gaps | `GAP-NNN` | `GAP-03` | `20-validation/missing-information.md` |
| Constraint tests | `TST-CON-NN` | `TST-CON-09` | `13-testing/core/` |
| Acceptance criteria | `AC-<REQID>-NN` / `AC-S-NN` | `AC-FR013-01`, `AC-S-05` | `02-requirements/acceptance-criteria.md` |
| Validation audits | `AUD-NN` | `AUD-01` | `20-validation/README.md` |

**Filename exception:** documents whose primary identifier *is* the content (requirements, use cases, test cases) are named after that ID — `FR-013.md`, `UC-007.md`, `TC-021.md`. Everything else uses `lowercase-kebab-case.md`.

**Cross-referencing example:** `FR-013 → BR-PAY-04 → UC-021 → API-WAL-002 → wallet → TC-031 → AC-FR013-01`

---

## 6. Document Status Definitions

```text
DRAFT          Work in progress
UNDER_REVIEW   Complete, awaiting review
APPROVED       Reviewed, accepted as source of truth
IMPLEMENTED    Realized in code
VERIFIED       Implemented AND verified by tests/audit
SUPERSEDED     Replaced by a newer document (keep for history)
DEPRECATED      No longer applicable (keep for history)
REJECTED       Reviewed and rejected
```

All documents in this repository are `APPROVED` at v1.0 unless noted otherwise. No document is `VERIFIED` — no implementation exists yet.

---

## 7. Document Metadata (required on every important file)

```yaml
---
document_id: DOC-<CAT>-NNN
title: <Title>
category: <directory name>
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true        # only for authoritative documents
related_requirements: []
related_documents: []
---
```

---

## 8. Evidence & Classification Rules (from methodology)

Every important statement is classified:

| Tag | Meaning |
|---|---|
| `VERIFIED` | Supported by direct project evidence (the approved project brief / charter in `00-project-overview`) |
| `INFERENCE` | Logically derived, not directly stated |
| `INSUFFICIENT EVIDENCE` | Cannot be concluded; the needed information is listed in `20-validation/` and `02-requirements` |

Findings are severity-classified: `CRITICAL` · `HIGH` · `MEDIUM` · `LOW` · `INFORMATIONAL`.
Conclusions carry confidence: `HIGH` · `MEDIUM` · `LOW`.

---

## 9. Change Management

1. Never silently change an approved document.
2. Update the document, bump its `version`, add a `## Change History` row.
3. If a decision is superseded, write a **new ADR** in `18-decisions/core/` and mark the old one `SUPERSEDED`.
4. Propagate changes to every impacted document (consistency rule) and record affected IDs in `20-validation/consistency-audit.md`.
5. Contradictions are never ignored — they are recorded in `20-validation/contradiction-audit.md` until resolved.
6. **Structure changes** (e.g. the session-011 portal partition of `01…23`): register the path scheme + ID allocation in `22-glossary/naming-conventions.md` first, move files only via a scripted migration that rewrites every citing path in the same change set, and keep both gates green after every change set (`validate.py` + `tools/check_citations.py` → 0 problems). Authority: owner directive `prompt-011.md` §1, proposal/evaluation `DOC-OVR-012`.

---

## 10. Methodology Coverage Map

Each section of the analysis methodology (`command.md` §53 — 48-part final structure) maps to its documentation home:

| Methodology Section | Location |
|---|---|
| 1. Executive Summary | `00-project-overview/project-charter.md` |
| 2. Project Understanding | `00-project-overview/project-context.md` |
| 3. Scope | `00-project-overview/project-scope.md` |
| 4. Stakeholders | `00-project-overview/stakeholders.md` |
| 5. Actors and Roles | `00-project-overview/actors-and-roles.md` |
| 6. Business Objectives | `00-project-overview/project-objectives.md` |
| 7. Requirements | `02-requirements/` |
| 8. Business Rules | `01-business-analysis/business-rules.md` |
| 9. Use Cases | `01-business-analysis/<portal>/` (gateway index `*-index.md` at folder root) |
| 10. End-to-End Workflows | `01-business-analysis/<portal>/` (gateway index `*-index.md` at folder root) |
| 11. Functional Analysis | `03-system-analysis/core/functional-analysis.md` |
| 12. Non-Functional Requirements | `02-requirements/core/` + `12-non-functional/` |
| 13. System Architecture | `04-architecture/core/architecture-overview.md` |
| 14. Frontend Architecture | `05-frontend/` |
| 15. Backend Architecture | `06-backend/` |
| 16. API Architecture | `07-api/` |
| 17. Database Architecture | `08-database/` |
| 18. Data Flow | `03-system-analysis/core/data-flow.md` + `04-architecture/core/data-flow.md` |
| 19. Authentication | `09-security/core/authentication.md` + `06-backend/core/authentication.md` |
| 20. Authorization | `09-security/core/rbac.md` + `06-backend/core/authorization.md` |
| 21. Security | `09-security/` |
| 22. Integrations | `10-integrations/` |
| 23. Performance | `12-non-functional/performance.md` |
| 24. Scalability | `12-non-functional/scalability.md` + `04-architecture/core/scalability.md` |
| 25. Reliability | `12-non-functional/reliability.md` |
| 26. Infrastructure | `14-devops-infrastructure/` |
| 27. Deployment | `15-deployment/` |
| 28. DevOps | `14-devops-infrastructure/ci-cd.md` |
| 29. Testing | `13-testing/` |
| 30. UX/UI | `11-ui-ux/` + `05-frontend/` |
| 31. Accessibility | `11-ui-ux/accessibility.md` + `12-non-functional/accessibility.md` |
| 32. Internationalization | `11-ui-ux/localization.md` + `05-frontend/core/internationalization.md` |
| 33. Maintainability | `12-non-functional/maintainability.md` |
| 34. Technology Decisions | `18-decisions/core/` |
| 35. Legal/Compliance | `00-project-overview/project-context.md` §Compliance + `12-non-functional/` |
| 36. Feasibility | `21-completion/feasibility-assessment.md` |
| 37. Risks | `17-risk-management/` |
| 38. Assumptions | `00-project-overview/assumptions.md` |
| 39. Dependencies | `00-project-overview/dependencies.md` |
| 40. Traceability Matrix | `19-traceability/` |
| 41. Missing Information | `20-validation/missing-information.md` |
| 42. Contradictions | `20-validation/contradiction-audit.md` |
| 43. Incorrect/Unsupported Claims | `20-validation/hallucination-audit.md` |
| 44. Technical Debt | `21-completion/technical-debt.md` |
| 45. Critical Findings | `20-validation/critical-findings.md` |
| 46. Recommendations | `21-completion/recommendations.md` |
| 47. Verification Strategy | `13-testing/testing-strategy.md` |
| 48. Final Quality Assessment | `20-validation/analysis-validation.md` + `21-completion/final-acceptance.md` |

---

## 11. Validation Rules

A document is complete only if it passes the quality gate (purpose, scope, terminology, evidence, assumptions, dependencies, related IDs, verification method, no unresolved contradiction, no unsupported claim presented as fact, status, version, source-of-truth definition). Audits live in `20-validation/`; they must be run after any structural change.

---

*End of root index. Next: [00-project-overview/README.md](00-project-overview/README.md)*

---

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-26 | 1.0 | Initial publication of the master index | analysis-agent |
| 2026-09-27 | 1.1 | §5 AUD-NN validation-audit ID row (registration for domain 20) | analysis-agent |
| 2026-09-28 | 1.2 | §1 `archdoc.md`/`archive/` claims corrected to honest state (defect `D-10`, SPE-03); §2 process-folder note (`phases/`, `sessions/`); §3 unverifiable `archdoc.md §38` reference removed | analysis-agent |
| 2026-09-28 | 1.3 | related_requirements: [] frontmatter key added (session 006 sweep: CHK-01) | analysis-agent |
| 2026-09-28 | 1.4 | §1 structure bullet updated: `archdoc.md` **restored** (session 008 `REC-01`/`TD-03`) — reconstruction provenance stated; `HAL-03`/`CRIT-08` closure evidence | analysis-agent |
| 2026-09-30 | 1.5 | §5 *Defined In* paths + §10 location cells realigned to the portal-partition scheme; §9 item 3 ADR path + **new §9.6** (structure-change procedure) | Owner directive session 011 (`prompt-011.md` §1) — change control before the phase-5 migration (`naming-conventions.md` v1.7, `DOC-OVR-012`) | analysis-agent |
