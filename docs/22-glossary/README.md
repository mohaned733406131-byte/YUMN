---
document_id: DOC-GL-001
title: Glossary Domain — Terminology Governance & File Index
category: 22-glossary
status: approved
version: 1.2
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-ROOT-001, DOC-OVR-002, DOC-OVR-007, DOC-BA-005, DOC-TPL-001]
---

# 22 — Glossary

**Scope of `22-glossary/`:** the canonical vocabulary of the yumn project — what every term means, how it is written in Arabic and English, and how identifiers and artifacts are *named* across all 24 documentation domains. This README is the domain index and the **governance contract** for terminology; the term definitions themselves live in [core/terminology.md](core/terminology.md), and the naming rules live in [core/naming-conventions.md](core/naming-conventions.md).

Terminology errors are documentation defects: a document that uses "buyer" for ACT-01, invents an 18th order state, or renames a queue breaks cross-domain traceability even if every individual sentence reads well. Domain 22 exists so that meaning and naming are decided once.

---

## 1. What This Domain Owns

| File | document_id | Authority |
|---|---|---|
| [README.md](README.md) | DOC-GL-001 | This file — governance process, scope, index |
| [core/terminology.md](core/terminology.md) | DOC-GL-002 | **Single source of truth for term definitions** (root README §4: "Terminology → `22-glossary/core/terminology.md`") |
| [core/naming-conventions.md](core/naming-conventions.md) | DOC-GL-003 | **Authoritative naming rules for authors** — file names, all ID series, code, DB, API, queues, branches, locales, dates, numerals |

What this domain does **not** own: business-rule *definitions* (DOC-BA-005), requirement *statements* (DOC-REQ-001), state-machine *transitions* (DOC-SA-010), API *contracts* (DOC-API-002/003). Glossary rows only define the term and point at the authoritative document by ID — they never restate rule text (root README §4).

## 2. Terminology Governance

### 2.1 The one rule

**`22-glossary/core/terminology.md` is the source of truth for what a term means.** Every other document may *use* a term; no other document may *define, rename, or narrow* it.

### 2.2 Adding a term before use

A term is introduced **before** it appears in any new or edited document:

1. Check [core/terminology.md](core/terminology.md) — if the concept exists under another name, adopt that name instead of minting a synonym (e.g. "buyer", "shopper", "purchaser" are all rejected; the register fixes **Customer** for `ACT-01`).
2. If the concept is genuinely new, add a row to `core/terminology.md` in A–Z position with: Arabic equivalent (or `—` for loanwords), one-sentence definition, category (`Business` / `Technical` / `Process`), the domain/IDs where the term binds, and see-also pointers.
3. Bump the `version` of `core/terminology.md`, add a Change History row, and record the change in `../20-validation/core/consistency-audit.md` (root README §9).
4. Only then may the term be used in domain documents. A term that appears anywhere in `docs/` without a register row is a **missing-information finding** for `../20-validation/core/missing-information.md`.

### 2.3 Conflict resolution

| Situation | Resolution |
|---|---|
| Two documents use different words for one concept | The register's canonical term wins; the losing document is edited (consistency rule, root README §9.4) |
| A document's usage contradicts the register's *definition* | Logged in `../20-validation/core/contradiction-audit.md` until resolved; constraints (`C-01…C-26`) and rules (`BR-*`) outrank the glossary if a true collision occurs |
| A term is ambiguous across languages (e.g. Arabic "مشرف" for both moderator and admin) | The register's disambiguation note governs; UI catalogs follow `../11-ui-ux/core/design-system.md` §8 voice rules |
| A term is proposed for deprecation | Row status moves to "deprecated" with a replacement pointer; the ID/term is never reused |

### 2.4 Evidence and status

Definitions are statements about canon. Where a definition goes beyond cited canon it is tagged `INFERENCE`; where canon is silent the row says so and feeds `../20-validation/core/missing-information.md` rather than inventing facts (root README §8). Register and naming documents carry `status: approved`, `source_of_truth: true`.

### 2.5 Relationship to templates

`23-templates/` templates use `<angle-bracket placeholders>` — placeholders are content there, not terminology. A filled document must use register terms, never placeholder text; conversely, a placeholder name (e.g. `<actor>`) is not a project term and is never added to the register.

## 3. How to Use This Domain

| Reader | Read |
|---|---|
| Authoring or reviewing any document | [core/terminology.md](core/terminology.md) — search for each key term you are about to use |
| Creating a new file / ID / table / endpoint / queue | [core/naming-conventions.md](core/naming-conventions.md) — the "defined-in" column tells you which registry issues the ID |
| Translating or writing Arabic copy | core/terminology.md `Arabic` column + `../11-ui-ux/core/design-system.md` §8 + `../11-ui-ux/core/localization.md` |
| Running a validation audit | Both files; mismatches are consistency/contradiction findings (`20-validation/`) |

## 4. File Index

| # | File | document_id | Purpose |
|---|---|---|---|
| 1 | [README.md](README.md) | DOC-GL-001 | Domain overview, terminology governance, index |
| 2 | [core/terminology.md](core/terminology.md) | DOC-GL-002 | Canonical A–Z term register (~110 terms, bilingual, evidence-linked) |
| 3 | [core/naming-conventions.md](core/naming-conventions.md) | DOC-GL-003 | Cross-domain naming rules: documents, IDs, code, DB, API, queues, git, locales, dates, numerals |
| [`core/`](core/README.md) | DOC-GL-004 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-GL-005 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-GL-006 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-GL-007 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-GL-008 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## 5. Consistency Rule

Changing a canonical term propagates to: `00-project-overview` (actor names) → `01-business-analysis` (UC/WF wording) → `02-requirements` (statement vocabulary) → `07-api` (path/resource nouns, error messages) → `08-database` (column/table vocabulary) → `11-ui-ux` / `05-frontend` (UI copy, catalogs) → `13-testing` (expected results) → `19-traceability` → `../20-validation/core/consistency-audit.md`. Changing a *naming rule* additionally propagates to `06-backend`, `14-devops-infrastructure`, and the CI lint configuration that enforces it.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-GL-004…DOC-GL-008) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
| 1.2 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
