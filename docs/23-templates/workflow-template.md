---
document_id: DOC-TPL-004
title: Workflow Template (workflow-NNN.md)
category: 23-templates
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-WF-001, DOC-SA-010, DOC-BA-005, DOC-GL-003]
---

# Workflow Template (DOC-TPL-004)

**When to use:** `01-business-analysis/workflows/workflow-NNN.md`. **Authority: DOC-WF-001 §2–§3** — mirror it exactly; differences are logged in `20-validation/contradiction-audit.md`. Exemplar: `../01-business-analysis/customer/workflow-001.md`.

## Rules

- Allocation: `WF-001…WF-012` all issued; a new workflow takes **WF-013+**, gets a `workflow-013.md` file, and is added to the DOC-WF-001 §1 index in the same change.
- **Numbering pitfall:** the file number is the WF number, but `document_id` runs **one ahead** because `DOC-WF-001` is the index (`workflow-001.md` = `WF-001` = `DOC-WF-002`). Always reference workflows by `WF-NNN`, never by document_id.
- Only the 17 canonical order states (`C-09`, DOC-SA-010) — escalations are not states; only `BR-*` IDs from DOC-BA-005; canonical 7 actors.
- Money lines obey wallet-only / integer-YER / refund-to-wallet (`C-01`, `BR-PAY-07`, `BR-PAY-10`).

## Template

```text
---
document_id: DOC-WF-<nnn+1>
title: "WF-<nnn> — <workflow title>"
category: 01-business-analysis
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: true
related_requirements: [<fr-ids>]
related_documents: [DOC-WF-001, DOC-BA-005, DOC-SA-010]
---

# WF-<nnn> — <workflow title> (<key branches>)

| Field | Value |
|---|---|
| **Trigger** | <the initiating user/system event> |
| **Actors** | <Actor> (`ACT-0n`)<, …> |
| **Blocks** | <b0n> <Block name> · <b0m> <Block name> |
| **Preconditions** | <state with IDs: phone regex, provider reachable, balance, KYC…> |
| **Final state** | <resulting order/wallet/session state, notifications sent, or terminal failure state> |

```text
[<entry action>] ──► <step> ──► <step> ──► <success end state>
        │                    │
        │ <condition A>      │ <condition B>
        ▼                    ▼
   ✗ <error code>      ✗ <error code>
   (<BR-*/C-* IDs>)    (<IDs>)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | <Actor> | <action> | <B0n> | `BR-…`, `C-…` | <rows/counters touched> | <error code + branch, IDs> |
| 2 | <Actor/System> | <action> | <B0m> | `BR-…` | <rows> | <failover/retry with IDs> |
| … | | | | | | |

**Alternatives**
- **<variant label>:** <alternate path and its rule IDs> (`BR-…`, `INT-REQ-…`).

**Exceptions**
- <failure / edge case> → <handling> (`DEP-…`, `RISK-…`, `SEC-REQ-…`).
- <constraint-enforced rejection> is rejected by design (`C-nn`).

**Rules applied:** `BR-…` ranges · Constraints: `C-…` · Security: `SEC-REQ-…`.

**Data touched:** <entities in narrative — never schema copy; `08-database/` owns schema>.

**Systems:** <blocks involved, e.g. B01 Identity & Access · B10 Notifications>.

**Final state:** <resulting state(s), notifications sent, or locked/rejected terminal state>.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | <date> | Initial version | Initial analysis |
```

## Pre-Submission Checklist

1. Ten-part anatomy in fixed order (frontmatter → metadata → ASCII flow → step table → alternatives → exceptions → rules → data → systems → final state → Change History).
2. ASCII flow: `→` happy path, labelled branches, `✗` failure exits — one code block.
3. Step table columns exactly: `Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling`.
4. Every `BR-*` cited exists; no invented states; `document_id` = WF number + 1.
5. Index row added (DOC-WF-001 §1) for new workflows; version bumped on edits.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
