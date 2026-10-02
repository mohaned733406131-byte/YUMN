---
document_id: DOC-TPL-008
title: Architecture Decision Record Template (ADR-NNN.md)
category: 23-templates
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-DEC-001, DOC-DEC-002, DOC-ARCH-010, DOC-GL-003]
---

# ADR Template (DOC-TPL-008)

**When to use:** a new file `18-decisions/core/ADR-NNN.md`. **Authority: DOC-DEC-001 §6 (required sections — an ADR missing any section fails review), §2 (lifecycle), §3 (numbering); DOC-ARCH-010 (decision index and cross-references)**. Exemplar: `../../18-decisions/core/ADR-001.md`.

## Rules

- **Mint the number only in `18-decisions/core/decision-log.md` (DOC-DEC-002 §1/§3):** `ADR-001…ADR-010` are reserved; the next new ADR is **`ADR-011`**. Filename = ID = `ADR-NNN.md`; `document_id: DOC-ADR-NNN` mirrors it; `category: 18-decisions`.
- **Required sections in fixed order (DOC-DEC-001 §6):** header → Status table (Status, Date, Deciders, Consulted, Informed) → Context → Decision → Alternatives Considered (table: option · pros · cons · why rejected — **minimum three**) → Consequences (positive · negative · neutral · introduced risks with `RISK-*` links) → Compliance (table of every driving `C-NN` + how satisfied; **`C-18` in every ADR**) → Related IDs → Change History.
- Status vocabulary per DOC-DEC-001 §2: `PROPOSED · ACCEPTED · DEPRECATED · SUPERSEDED` (frontmatter `status: approved` for accepted records).
- Superseding never edits an old ADR: write a **new** ADR and mark the old one `SUPERSEDED` (root README §9.3).
- Context cites the forces — constraints `C-NN`, requirements, quality attributes, neighbouring ADRs/dependencies — by ID; alternatives must include the *status-quo / do-nothing* or the *constraint-named* option where one exists.
- ADR files carry `source_of_truth: true` (they are the record of the decision); `related_requirements` lists the NFRs/requirements the decision serves.
- Every claim tagged `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE` (root README §8) — feasibility ADRs do not invent vendor facts.

## Template

```text
---
document_id: DOC-ADR-<nnn>
title: "ADR-<nnn>: <reserved title>"
category: 18-decisions
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: true
related_requirements: [<nfr-fr-data-req-ids>]
related_documents: [DOC-DEC-001, DOC-DEC-002, DOC-ARCH-010, DOC-OVR-008]
---

# ADR-<nnn>: <reserved title>

| Field | Value |
|---|---|
| **Status** | ACCEPTED |
| **Date** | <date> |
| **Deciders** | <roles who decided> |
| **Consulted** | <roles/stakeholders whose input shaped it> |
| **Informed** | <roles + stakeholder IDs> |

## Context

<The situation and the forces acting on the decision: the quality attributes, constraints (`C-NN`), requirements and neighbouring ADRs/dependencies that make this decision necessary — each cited by ID, never restated.>

- **Constraint `<C-nn>`:** <how it binds this decision>.
- **Neighbouring decisions:** `ADR-<nnn>` <relationship — supports/assumes/excludes>.
- **Dependencies:** `DEP-nn` <status and why it matters here>.

## Decision

**<One unambiguous paragraph: what IS being decided, in present tense, with explicit "no other … may …" boundaries where the decision excludes alternatives.>**

## Alternatives Considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| **<Option A — the status quo / do nothing>** | <genuine advantage> | <genuine disadvantage> | <reason, with IDs — e.g. excluded by `C-nn`> |
| **<Option B>** | <…> | <…> | <reason with IDs> |
| **<Option C>** | <…> | <…> | <reason with IDs> |

## Consequences

**Positive**

- <benefit — cite the quality attribute or risk it serves (`RISK-NNN`)>.

**Negative**

- <cost/limitation accepted — with the mitigation or ceiling it rolls up into>.

**Neutral**

- <fact that neither helps nor hurts but future work should know>.

**Risks introduced:** <new `RISK-NNN` links or "— none; feeds existing …">.

## Compliance

| Constraint | How this ADR satisfies it |
|---|---|
| **`C-18` custom build** | <always present — how this stays a custom build> |
| **`C-<nn>`** | <how satisfied, and how that is verified> |

## Related IDs

<C-nn> · <DEP-nn> · <NFR-/FR-/DATA-REQ-…> · <BR-*> · neighbours: `ADR-<nnn>` · risks: `RISK-NNN` · documents: <domain paths §section>.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | <date> | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
```

## Pre-Submission Checklist

1. Number minted in DOC-DEC-002 (next is ADR-011); filename = `ADR-NNN.md`; `document_id` mirrors.
2. All DOC-DEC-001 §6 sections present in order; ≥3 alternatives each with a substantive *why rejected*; `C-18` row exists in Compliance.
3. Context/Decision/Consequences cite only existing IDs (constraints, requirements, `RISK-*`, neighbouring ADRs); no invented facts without an evidence tag.
4. Supersessions create a new ADR and flip the old status — never rewrite history (root README §9.3).
5. Frontmatter complete (`category: 18-decisions`, `source_of_truth: true`); decision-log + architecture-decisions-reference updated in the same change; version + Change History row.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
