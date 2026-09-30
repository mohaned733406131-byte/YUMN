---
document_id: DOC-TPL-005
title: Test Case Template (TC-NNN.md)
category: 23-templates
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-TST-006, DOC-TST-002, DOC-AC-001, DOC-GL-003]
---

# Test Case Template (DOC-TPL-005)

**When to use:** `13-testing/test-cases/TC-NNN.md`. **Authority: DOC-TST-006 §1 (anatomy) + §2 (locked allocation)**; level-selection rule in `testing-strategy.md` §3. Exemplar: `../13-testing/core/TC-001.md`.

## Rules

- IDs come from the **locked allocation** (DOC-TST-006 §2): never renumber, never reuse, never cross into another domain's range. New cases fill the next free slot of their range; a case for an uncovered behavior needs an allocation amendment in DOC-TST-006 first.
- Filename `TC-NNN.md` (zero-padded); frontmatter `document_id: DOC-TC-NNN`, `category: 13-testing`, `source_of_truth: false`, `related_requirements` = every ID the case exercises.
- Each case maps to **≥1 AC or rule** (`AC-S-03`); expectations cite canon (AC/BR/C), never implementation internals.
- Negative cases state the error code **and** the "nothing persisted" assertion; timing cases use injectable clocks; Arabic-first journeys default to locale `ar`.
- Test data uses the reserved `79xxxxxxx` phone block and exact boundary values — never vague samples.

## Template

```text
---
document_id: DOC-TC-<nnn>
title: TC-<nnn> — <single verifiable claim>
category: 13-testing
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: false
related_requirements: [<fr-nfr-sec-req-ids>, <br-ids>]
related_documents: [DOC-TST-006, DOC-TST-002]
---

# TC-<nnn> — <single verifiable claim>

| Field | Value |
|---|---|
| Objective | <1–2 sentences: the single behavior being proven, phrased as a verifiable claim> |
| Level | <unit|integration|e2e|performance|security|a11y> — per strategy §3 |
| Priority | <P0|P1|P2> |
| Automation | <Yes — <tool> | No — <reason>> |

## Preconditions
- <Environment, accounts, seed state, provider mode — re-creatable from `test-data-and-environments.md`.>
- <Endpoints/health gates that must hold before step 1.>

## Test Data

| Field | Value |
|---|---|
| <input name> | <exact value — e.g. phone `791234567`, boundary amount `999`, locale `ar`> |
| <expected artifact> | <exact expected value — e.g. OTP `481902` sampled from sandbox> |

## Steps
1. <`METHOD /path` with exact payload / UI path / tool command — record status, body, `X-Correlation-Id`.>
2. <Next action — include the negative/boundary variant.>
3. <DB/log/inbox inspection needed to assert persistence effects.>

## Expected Result
- <Step n returns `<status>` with `<exact body fields>`; observable, binary — PASS/FAIL with no interpretation.>
- <Row/ledger/queue effects: exact counts and values; "none of the negative steps created a row".>
- <Negative steps: exact error codes + nothing persisted.>
- <No secret/PII appears in logs, if applicable.>

## Related IDs

| Kind | ID | Assertion |
|---|---|---|
| FR | <FR-nnn> | <what this requirement line asserts> |
| BR | <BR-…> | <rule exercised> |
| AC | <ac-id> | <acceptance criterion closed by this case> |
| API | <API-GRP-nnn> | <endpoint exercised, if any> |
| C | <C-nn> | <constraint proven, if the case feeds `TST-CON-NN`> |

## Constraints
- <`C-nn` and `TST-CON-NN` when this case feeds the constraint register; otherwise `—`.>

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | <date> | Initial version | Initial analysis |
```

## Pre-Submission Checklist

1. ID is the next free slot in its DOC-TST-006 §2 range; range/domain unchanged.
2. Eleven anatomy sections present in order (Objective → … → Change History).
3. Expected results are binary and cite canon IDs; negative paths assert both error code and no-persistence.
4. Test data exact and re-creatable; phones from the reserved block; locale stated.
5. Maps to ≥1 AC or rule; `related_requirements` lists every exercised ID; no leftover `<…>`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
