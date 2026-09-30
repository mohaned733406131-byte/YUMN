---
document_id: DOC-TPL-001
title: Templates Domain — Index, Placeholder & Authoring Rules
category: 23-templates
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-ROOT-001, DOC-GL-001, DOC-GL-003, DOC-UC-000, DOC-WF-001, DOC-TST-006, DOC-REQ-001, DOC-DEC-001, DOC-API-002, DOC-API-005, DOC-DB-001, DOC-DB-007, DOC-ARCH-010, DOC-SEC-008, DOC-RSK-002, DOC-RSK-004]
---

# 23 — Templates

**Scope of `23-templates/`:** reusable structural templates for every recurring document type in this knowledge base, so a new requirement, use case, test case, ADR, endpoint group, entity, finding, risk or audit is shaped exactly like its canon exemplars. This README is the domain index and the **authoring contract** for templates.

> This domain is *derived*: it mirrors structures that are defined elsewhere (DOC-UC-000, DOC-WF-001, DOC-TST-006, `../07-api/core/api-conventions.md`, `08-database/README.md` §1, DOC-ARCH-010 §8, DOC-SEC-008, DOC-RSK-002, root README §9). Where a template and its owning document disagree, **the owning document wins** — and the disagreement is logged in `../20-validation/core/contradiction-audit.md`.

## 1. File Index

| # | File | document_id | Template for | Mirror of (authority) | Canonical filled exemplar |
|---|---|---|---|---|---|
| 1 | [README.md](README.md) | DOC-TPL-001 | This index + placeholder/authoring rules | root README §5–§9 | — |
| 2 | [requirement-template.md](core/requirement-template.md) | DOC-TPL-002 | FR / NFR / SEC-REQ / DATA-REQ / INT-REQ files | `02-requirements/` registry + `FR-013` | `../02-requirements/core/FR-013.md` |
| 3 | [use-case-template.md](core/use-case-template.md) | DOC-TPL-003 | Use-case files `UC-NNN.md` | DOC-UC-000 | `../01-business-analysis/customer/UC-001.md` |
| 4 | [workflow-template.md](core/workflow-template.md) | DOC-TPL-004 | Workflow files `workflow-NNN.md` | DOC-WF-001 | `../01-business-analysis/customer/workflow-001.md` |
| 5 | [test-case-template.md](core/test-case-template.md) | DOC-TPL-005 | Test cases `TC-NNN.md` | DOC-TST-006 | `../13-testing/core/TC-001.md` |
| 6 | [api-endpoint-template.md](core/api-endpoint-template.md) | DOC-TPL-006 | Endpoint group docs `endpoints/<group>.md` | DOC-API-005, `../07-api/core/api-conventions.md` | `../07-api/core/wallet.md` (API-WAL) |
| 7 | [database-entity-template.md](core/database-entity-template.md) | DOC-TPL-007 | Entity docs `entities/<table>.md` | `08-database/README.md` §1–§2, DOC-DB-007 | `../08-database/core/user.md` (DB-001) |
| 8 | [adr-template.md](core/adr-template.md) | DOC-TPL-008 | ADR files `18-decisions/ADR/ADR-NNN.md` | DOC-DEC-001 §6 (required sections), §2–§3 (lifecycle, numbering) | `../18-decisions/core/ADR-001.md` |
| 9 | [risk-template.md](core/risk-template.md) | DOC-TPL-009 | Risk register entries `RISK-NNN` | DOC-RSK-002, DOC-RSK-004 | `17-risk-management/risk-register.md` |
| 10 | [security-finding-template.md](core/security-finding-template.md) | DOC-TPL-010 | Security findings `SEC-NNN` entries | DOC-SEC-008 | `../09-security/core/security-findings.md` (SEC-001…) |
| 11 | [validation-audit-template.md](core/validation-audit-template.md) | DOC-TPL-011 | Validation audit files / entries in `20-validation/` | root README §8–§9 | *(files in `20-validation/` pending authoring)* |

**Deliberately absent templates:** business-rule rows (minted only inside `01-business-analysis/business-rules.md` §Domain tables — copy a row, don't create a file), workflow/state-machine rows (owned by `../03-system-analysis/core/state-transitions.md`), glossary rows (DOC-GL-001 §2.2). Rely on those registries directly.

## 2. The Placeholder Convention

1. The **only** placeholders in this repository are `<angle-bracket>` tokens, and they may appear **only** inside `23-templates/` (DOC-GL-003 §2).
2. Placeholders are lowercase-with-hyphens: `<req-id>`, `<actor-name>`, `<group-code>`, `<table-name>`, `<date>` — never `<Title>` or `<ID_Here>`.
3. A placeholder names *what goes there*, not an example value. When you fill a template, **every** placeholder must be gone; a file shipping with leftover `<…>` is a validation finding (`../20-validation/core/missing-information.md`).
4. Placeholders are not terminology: they never enter `22-glossary/terminology.md` (DOC-GL-001 §2.5).
5. Template files themselves carry real frontmatter (`document_id: DOC-TPL-0NN`, `category: 23-templates`) and `source_of_truth: true` — within this domain the template is the authoritative statement of *shape*; the *content* authority for everything the document says remains the mirrored document named in §1 (a template and its owning document never disagree — §4).

## 3. How to Use a Template

1. Pick the template from §1; read its *Rules* section first (it states where the file lives, which registry issues the ID, and which exemplar to open).
2. Copy the template body into the **target domain** (never author new documents inside `23-templates/`), rename the file per DOC-GL-003 §1 (ID-named for FR/UC/TC, otherwise `lowercase-kebab-case.md`).
3. Fill every placeholder using canon: cite IDs (`BR-*`, `C-*`, `AC-*`) instead of restating definitions (root README §4), tag evidence (`VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`), use register terms only (DOC-GL-002).
4. Mint the ID only in its registry (DOC-GL-003 §3 *Defined in* column) — templates never allocate IDs.
5. Run the template's pre-submission checklist, then the domain review; status starts `DRAFT` → `APPROVED` per root README §6.

## 4. Cross-Domain Consistency Rule

Changing a template's structure propagates: update the mirrored authority (§1) → update every already-filled document of that type → record the sweep in `../20-validation/core/consistency-audit.md` → bump this domain's versions (root README §9.2, §9.4). Templates are never changed to *contradict* filled canon; if the exemplar evolves, the template follows it in the same change set.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
