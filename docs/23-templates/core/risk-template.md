---
document_id: DOC-TPL-009
title: Risk Register Entry Template (RISK-NNN)
category: 23-templates
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-RSK-001, DOC-RSK-002, DOC-RSK-004, DOC-GL-003]
---

# Risk Template (DOC-TPL-009)

**When to use:** appending a new risk **entry** to `17-risk-management/core/risk-register.md` (DOC-RSK-002) — risks are rows in the register, never separate files. **Authority: DOC-RSK-001 (scoring model, categories, ranking, response strategies), DOC-RSK-002 (register format), DOC-RSK-004 (review/escalation governance)**. Exemplar entries: `RISK-001`, `RISK-003` in `risk-register.md`.

## Rules

- **Mint the next ID in `risk-register.md` only:** allocation is `RISK-001…RISK-024`; the next risk is **`RISK-025`** (DOC-GL-003 §3).
- **Scoring:** `Score = Probability (1–5) × Impact (1–5)`, integers only. Bands (DOC-RSK-001 §3): **≥ 20 CRITICAL · 12–19 HIGH · 6–11 MEDIUM · ≤ 5 LOW** — computed, never chosen by feel.
- **Response strategy** from DOC-RSK-001 §4: `Mitigate · Transfer · Avoid · Accept` (combinations allowed, primary first); ranking everywhere: **score descending → impact descending → ID ascending**.
- Every risk updates **both** places in the register in the same change: a row in §1 Summary Table (11 columns) and a detail block in §2 (`### RISK-NNN — title`).
- Owner is an owner **role** (from `stakeholders.md`), not a person; `Status: OPEN` until mitigation produces evidence (honest-status rule: nothing is implemented yet — DOC-RSK-001 §1).
- Description/Trigger/Impact/Mitigation/Contingency cite existing IDs (`SEC-NNN`, `GAP-NN`, `DEP-nn`, `ASM-nn`, `BR-*`, `AC-S-*`, `RISK-*`) — never invent them; cross-link sibling risks explicitly.
- Severity distributions and the "Top 8" line are recomputed after any addition (they are derived, not hand-kept).

## Template

```text
<!-- 1. Summary Table row — insert in ID order in §1 of risk-register.md -->

| RISK-<nnn> | <short title — the loss event, not the cause> | <Category> | <P 1–5> | <I 1–5> | <P×I> | **<CRITICAL|HIGH|MEDIUM|LOW>** | <Mitigate|Transfer|Avoid|Accept (+combos)> | <owner role> | OPEN | <linked DEP/ASM/SEC/REQ IDs> |

<!-- 2. Detail block — append in §2 of risk-register.md -->

### RISK-<nnn> — <title>

**Category:** <Category> · **P** <n> · **I** <n> · **Score** <n> · **Severity:** <band> · **Response:** <strategy> · **Owner:** <role> · **Status:** OPEN

- **Description:** <the risk event in one or two sentences — mechanism, cause chain, and why it threatens this project — each claim cited (`RISK-*`, `BR-*`, `C-*`, `ASM-*`, charter/STK references).>
- **Trigger / early-warning indicators:** <observable early signals — metric thresholds, reconciliation/job mismatches, gate conversions, provider status — that would tell us the risk is materializing.>
- **Impact if realized:** <concrete consequences: money, trust, schedule, constraint breach — ranked, with IDs (e.g. constraint `C-nn` breached, objective `OBJ-nn` missed).>
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| <specific control/verification with its governing ID> | <role> | <Phase 0 | Phase 1 | Phase 2 | Post-launch | Launch> |

- **Contingency plan:** <what we do when the risk fires anyway — freezes, paging, rollbacks, communications, who decides — citing runbook/governance IDs.>
- **Residual risk:** <what remains after mitigation, honestly stated — accepted only with its monitor/trigger.>
- **Linked IDs:** <comma-separated canon IDs: requirements, rules, findings, dependencies, gaps, workflows, other risks.>

<!-- 3. Same change: recompute §1 "Distribution" and "Top N" lines; bump risk-register.md version + Change History row -->
```

## Pre-Submission Checklist

1. ID is `RISK-025` (or next free) minted only in `risk-register.md`; title states the loss event; category from DOC-RSK-001 §2.
2. Score computed as P×I with band matched exactly (≥20/12–19/6–11/≤5); response strategy from §4; ranking lines recomputed.
3. Summary row **and** detail block both added; owner is a role; all cited IDs (`SEC-*`, `GAP-*`, `DEP-*`, `ASM-*`, `AC-S-*`, sibling `RISK-*`) exist in canon.
4. Trigger indicators are observable; contingency is actionable; residual risk is explicit — none of the three omitted.
5. `risk-register.md` version bumped + Change History row added (root README §9); distribution counts updated.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
