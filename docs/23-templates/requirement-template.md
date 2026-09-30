---
document_id: DOC-TPL-002
title: Requirement Template (FR / NFR / SEC-REQ / DATA-REQ / INT-REQ)
category: 23-templates
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-REQ-001, DOC-ROOT-001, DOC-FR-013, DOC-GL-003]
---

# Requirement Template (DOC-TPL-002)

**When to use:** a new file in `02-requirements/<family>/` — `FR-NNN.md`, `NFR-NNN.md`, `SEC-REQ-NNN.md`, `DATA-REQ-NNN.md`, `INT-REQ-NNN.md`. Authority: `02-requirements/` registries; exemplar: `../02-requirements/core/FR-013.md`.

## Rules

- **Filename = ID** (DOC-GL-003 §1): `FR-013.md`. Mint the next number only in the family's registry (`requirements-overview.md` / DOC-REQ-001) — never reuse or renumber.
- Frontmatter: `category: 02-requirements`, `source_of_truth: true`, `related_requirements` lists every FR/NFR/SEC-REQ/DATA-REQ/INT-REQ **and BR** the statement depends on.
- A requirement states *what*, not *how*: no implementation, no invented numbers. Any value not in canon gets `INFERENCE` or a `GAP-NN` (DOC-GL-002 §"Evidence tags").
- Section set is fixed below; unused sections are written as `— none beyond IDs cited` rather than deleted, so documents stay diff-comparable.
- Acceptance criteria IDs: `AC-FRnnn-nn` / `AC-NFR-nnn-nn` / `AC-SRnnn-nn` / `AC-DRnnn-nn` / `AC-IRnnn-nn` (DOC-GL-003 §3.1), each Given/When/Then with a binary outcome.

## Template

```text
---
document_id: DOC-<family>-<nnn>
title: <req-id> — <human title>
category: 02-requirements
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: true
related_requirements: [<peer-req-ids>, <br-ids>]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# <req-id> — <human title>

**Block:** <b01…b13> · **Priority:** <Critical|High|Medium|Low> · **Status:** approved · **Registry:** `DOC-REQ-001` §<n>

<One-paragraph statement of the requirement covering scope, guarantees and exclusions, citing IDs in parentheses.>

## Rationale

- Traces <OBJ-nn> — why this requirement exists in one or two bullets.
- Relationship to neighbouring requirements (<peer-req> precondition / consequence).

## Requirements Detail

- <Numbered-or-bulleted atomic statements; each ends with the governing IDs (`BR-…`, `C-…`, `SEC-REQ-…`, `INT-REQ-…`).>
- <Negative scope as explicit statements: "no <forbidden-thing> exists anywhere" with the forbidding constraint ID.>

## Preconditions

- <State the world that must hold before this requirement applies, each with its owning ID.>

## Expected Result

<One observable paragraph: what a user/operator sees when everything works. No implementation detail.>

## Acceptance Criteria

- **<ac-id-1>** — Given <state>, when <action>, then <observable outcome> (<governing IDs>).
- **<ac-id-2>** — Given <state>, when <action>, then <observable outcome> (<governing IDs>).

## Business Rules Applied

- `<BR-ID>` short gloss — <never restate the full rule text, cite it> (DOC-ROOT-001 §4).

## Constraints Honored

- `<C-ID>` short gloss.

## Dependencies

- **FR:** <req-ids and their role in one clause each>.
- **NFR/SEC/DATA/INT:** <ids>.
- **DEP:** <dependency-ids — flag production blockers>.

## Verification Method

- <How tests/audits will prove it: test levels, invariant checks, negative tests — pointers to `13-testing/`, not test bodies.>

## Out of Scope Notes

- <Explicit exclusions with their IDs; unresolved unknowns as `GAP-NN` (never silently dropped).>

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | <date> | Initial version | Initial analysis |
```

## Family Variations

| Family | Filename / frontmatter | Section swaps |
|---|---|---|
| FR | `FR-NNN.md`, `source_of_truth: true` | as above |
| NFR | `NFR-NNN.md` | *Requirements Detail* = measurable targets table (`Target | Driver IDs | Verification`); add `AC-S-*` cross-links |
| SEC-REQ | `SEC-REQ-NNN.md` | *Requirements Detail* = numbered `R1…Rn` control statements; ACs shaped `AC-SRnnn-nn` |
| DATA-REQ | `DATA-REQ-NNN.md` | *Requirements Detail* = numbered `R1…Rn` with retention/privacy IDs (`16-data/`) |
| INT-REQ | `INT-REQ-NNN.md` | *Requirements Detail* = provider, auth, timeouts/retries, idempotency, failure mode per `10-integrations/` |

## Pre-Submission Checklist

1. ID minted in the registry; filename equals the ID; no placeholder `<…>` remains.
2. Every rule/constraint/actor cited by ID — no copied definitions, no new synonyms for register terms (DOC-GL-002).
3. Every number (limits, durations, thresholds) traces to canon or carries `INFERENCE`/`GAP-NN`.
4. ACs binary and observable; each uses an existing pattern from DOC-GL-003 §3.1.
5. Frontmatter complete; `related_requirements` covers both directions of traceability (to-be: `19-traceability/`).
6. `version` + Change History row on any edit to an approved file (root README §9).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
