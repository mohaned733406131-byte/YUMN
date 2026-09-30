---
document_id: DOC-TPL-003
title: Use Case Template (UC-NNN.md)
category: 23-templates
status: approved
version: 1.3
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-UC-000, DOC-BA-005, DOC-REQ-001, DOC-GL-003]
---

# Use Case Template (DOC-TPL-003)

**When to use:** `01-business-analysis/<portal>/UC-NNN.md` — the portal folder (`core` / `admin` / `vendor` / `customer` / `delivery`) the UC's actor belongs to, per `naming-conventions.md` §1 *Portal partition* (files authored before session 011 live in `use-cases/` and are migrated by the phase-5 script). **Authority: DOC-UC-000 §1** — this template is a convenience mirror; if the two differ, DOC-UC-000 wins (flag it in `20-validation/contradiction-audit.md`). Exemplar: `../01-business-analysis/customer/UC-001.md`.

## Rules

- Allocation is `UC-001…UC-420` (`UC-001…UC-210` fully issued in session 010 per owner directive `prompt-010.md` §1; `UC-211…UC-420` allocated for session 011 minting per owner directive `prompt-011.md` §1); a genuinely new use case beyond the allocation takes **UC-421+**, must be added to the DOC-UC-000 §2 index and §3 actor totals in the same change.
- Filename `UC-NNN.md`; frontmatter `document_id: DOC-UC-NNN` where the number **matches** the UC number (`UC-041` → `DOC-UC-041`), `category: 01-business-analysis`, `source_of_truth: true`.
- **Exactly one primary actor** from the canonical 7 (`DOC-OVR-007`); supporting actors appear inside steps.
- Reference only **existing** `BR-*` (DOC-BA-005) and `FR-*` (DOC-REQ-001) IDs — never invent. API touchpoints are conceptual (`POST /orders`); `07-api/` owns the contract.
- Body 45–70 lines, nine sections in the fixed order below.

## Template

```text
---
document_id: DOC-UC-<nnn>
title: UC-<nnn> — <action-oriented title>
category: 01-business-analysis
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: true
related_requirements: [<fr-ids>]
related_documents: [DOC-UC-000, DOC-BA-005, DOC-OVR-007]
---

# UC-<nnn> — <action-oriented title>

## Header Info
- **Use Case ID:** UC-<nnn>
- **Title:** <title>
- **Actor:** <Actor name> (<ACT-0n>)< — qualifier if unauthenticated/preconditioned>
- **Trigger:** <the user/system event that starts the flow>
- **Priority:** <P0|P1|P2>
- **Goal:** <one sentence: what the actor achieves>
- **Preconditions:** <world-state bullets, each with governing IDs>

## Main Scenario
1. <Actor action> → system <response with conceptual endpoint> (<BR-*, C-* citations inline>).
2. <Actor action> → system <response> (<IDs>).
3. …

## Alternative Scenarios
- **A1 — <label>:** <legitimate alternate path and where it rejoins / ends>.
- **A2 — <label>:** <e.g. insufficient balance, lockout, stock conflict>.

## Exception Scenarios
- **E1 — <label>:** <failure (network, provider outage, concurrent modification)> → <system behaviour and error code> (<IDs>).
- **E2 — <label>:** <failure> → <behaviour> (<IDs>).

## Postconditions
- <Success end state, incl. order-state / ledger / reservation effects (`DOC-SA-010`, 17 states).>
- <Failure end state: what exists / does not exist (no half-written rows, no orphan holds).>

## Business Rules Applied
- <BR-IDs exactly as issued in DOC-BA-005 — no new IDs, no restated text>

## Related Requirements
- <FR-IDs> (<short title>)

## Permissions / Data / External Dependencies
- **Permissions:** <role(s) / Public / Any authenticated; ownership scope>.
- **Data involved:** <entities touched, read or write>.
- **External dependencies:** <providers, caches, queues with DEP-*/INT-REQ-* IDs>.

## Acceptance Criteria
- **AC-UC<nnn>-01:** Given <state>, when <action>, then <observable outcome> (<IDs>).
- **AC-UC<nnn>-02:** Given <state>, when <action>, then <observable outcome> (<IDs>).
```

## Pre-Submission Checklist

1. One primary actor among ACT-01…ACT-07; priority P0/P1/P2 justified against DOC-UC-000's scale.
2. Every inline ID exists (grep DOC-BA-005 / DOC-REQ-001); no coined terms (DOC-GL-002).
3. Postconditions name concrete state-machine effects where relevant; no 18th state invented (`C-09`, DOC-SA-010).
4. ACs shaped `AC-UCnnn-nn`, binary, and the file stays within 45–70 body lines.
5. Index (DOC-UC-000 §2/§3) updated if the UC is new; version + Change History bumped.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-29 | Allocation rule: `UC-001…UC-040` → **`UC-001…UC-210`** (42 issued + session-010 minting band; next free ID `UC-211+`) | Owner directive session 010 (`prompt-010.md` §1) — allocation synced in `naming-conventions.md` v1.5 §3 (SPE-05) |
| 1.2 | 2026-09-29 | Allocation wording: `42 issued … UC-043+ minting` → **fully issued in session 010** | Owner directive session 010 (`prompt-010.md` §1) — `UC-043…UC-210` minted; index `DOC-UC-000` v1.2 + §3 totals synced |
| 1.3 | 2026-09-30 | File location → **`01-business-analysis/<portal>/UC-NNN.md`** (portal partition); allocation → **`UC-001…UC-420`** (210 minted + `UC-211…420` allocated, next free `UC-421+`) | Owner directive session 011 (`prompt-011.md` §1) — allocation + path scheme registered first in `naming-conventions.md` v1.7 (SPE-05) |
