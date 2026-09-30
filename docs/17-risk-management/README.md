---
document_id: DOC-RSK-001
title: Risk Management Domain Overview
category: 17-risk-management
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-008, NFR-014, FR-020]
related_documents: [DOC-OVR-003, DOC-OVR-009, DOC-OVR-010, DOC-ROOT-001, DOC-SEC-008]
---

# Risk Management — Domain Overview (DOC-RSK-001)

## 1. Purpose & Scope

This domain owns the **canonical risk register (`RISK-NNN`)** for yumn: how risks are categorized, scored, responded to, reviewed, and escalated. It is the single source of truth for risk IDs (root README §5); every other document that mentions a risk must reference the ID, never restate or re-score it.

**Honest status note (read first):** yumn is at `ANALYZED (pre-implementation)` status. **Nothing is implemented yet.** No mitigation below exists in code, infrastructure, or contracts — every mitigation is a *plan* with an owner and a phase. Consequently **all 24 register entries are `OPEN`**, all security findings (`SEC-001…SEC-015`) are `OPEN`, and every mitigation success metric is a *target to be proven*, not an achieved state. No risk may be shown as `MITIGATED`/`CLOSED` until evidence (test, drill, contract, sign-off) is linked from `risk-register.md` per `risk-review-process.md` §5.

## 2. Risk Taxonomy

Eight categories; every risk carries exactly one primary category (secondary categories are noted in the risk detail, not in the summary table).

| Category | Definition for yumn | Register entries |
|---|---|---|
| **Technical** | Defects, capacity, or degradation in the built system (search, performance, devices, queues) | RISK-007, RISK-008, RISK-016 |
| **Financial** | Direct monetary loss, leakage, or mis-settlement (fraud, promo abuse, reconciliation loss) | RISK-010, RISK-013 |
| **External / Provider** | Third parties yumn depends on but does not control (wallet rails, SMS/WhatsApp, couriers) | RISK-003, RISK-006, RISK-018 |
| **Regulatory** | Law, regulator, or tax-authority positions that constrain or invalidate the model | RISK-004, RISK-012, RISK-020 |
| **Business / Adoption** | Marketplace supply/demand dynamics, positioning, and market-fit quality | RISK-002, RISK-015, RISK-022, RISK-024 |
| **Operational** | How the platform is built, run, and staffed (complexity, staffing, launch readiness, scope) | RISK-005, RISK-011, RISK-014, RISK-017, RISK-019 |
| **Security** | Adversarial compromise of accounts, data, or the supply chain | RISK-009, RISK-021 |
| **Data** | Integrity and durability of stored state (ledger correctness, queue-backed state) | RISK-001, RISK-023 |

Category counts: Technical 3 · Financial 2 · External/Provider 3 · Regulatory 3 · Business/Adoption 4 · Operational 5 · Security 2 · Data 2 = **24 risks**.

## 3. Scoring Model

`Score = Probability (1–5) × Impact (1–5)`; the score maps mechanically to a severity band. Scores are integers only.

### 3.1 Probability scale

| P | Label | Meaning |
|---|---|---|
| 1 | Rare | No plausible path observed in analysis; would require an exceptional combination of events |
| 2 | Unlikely | Possible but counter-measures already in canon make occurrence improbable |
| 3 | Possible | Conditions exist today (open dependency, unsupported assumption, unvalidated control) |
| 4 | Likely | Condition is present and unowned/unresolved at analysis time; expected without intervention |
| 5 | Almost certain | Already occurring or structurally guaranteed |

### 3.2 Impact scale

| I | Label | Meaning |
|---|---|---|
| 1 | Negligible | Localized inconvenience; no requirement, constraint, or objective affected |
| 2 | Minor | Single-flow defect; recoverable within normal operations |
| 3 | Moderate | Affects a persona or a launch-readiness criterion (`AC-S-*`); recoverable within days |
| 4 | Major | Blocks a critical path (checkout, payouts, onboarding) or breaches a constraint target (`C-25`, `C-26`) |
| 5 | Severe | Existential: money integrity, legality of the model, or platform launch itself |

### 3.3 Severity bands

| Score | Severity | Meaning in this project | Count |
|---|---|---|---|
| ≥ 20 | **CRITICAL** | Existential or launch-blocking; sponsor-level attention, escalation within 24 h if new | 3 |
| 12 – 19 | **HIGH** | Threatens objectives or a critical path; mitigation plan required before the owning phase | 12 |
| 6 – 11 | **MEDIUM** | Managed mitigation required; reviewed monthly | 8 |
| ≤ 5 | **LOW** | Accepted with monitoring; may be low-probability/high-impact — contingency still documented | 1 |

Ranking rule used everywhere in this domain (summary order, "top N" selections, mitigation-plan selection): **score descending → impact descending → ID ascending**. Ties are normal; the rule makes every "top N" list deterministic.

## 4. Response Strategies

| Strategy | When applied | yumn examples |
|---|---|---|
| **Avoid** | Risk can be eliminated by not doing the risky thing or by closing the precondition before work starts | RISK-011 (scope creep — enforce `project-scope.md` scope-creep control); RISK-006 (close `DEP-06` before Phase 1) |
| **Mitigate** | Reducing probability and/or impact via design, process, or controls | RISK-001 (append-only ledger + reconciliation jobs `J1/J2`); RISK-005 (operational simplicity via `C-21`/`C-22`) |
| **Transfer** | Another party bears the impact (contract, provider SLA, professional advice) | RISK-003 (provider SLAs + bank-transfer fallback `BR-PAY-04`); RISK-004/RISK-020 (legal opinions `DEP-09`) |
| **Accept** | Cost of mitigation exceeds expected loss; monitored with a stated trigger | RISK-024 (competitive response — monitor only); residual tails of RISK-009/RISK-021 |

A register row states one **primary** strategy; contingency plans (in `risk-register.md`) always exist regardless of strategy, because acceptance of a probability is not acceptance of an unmanaged impact.

## 5. Review Cadence

| Event | Frequency / trigger | Output |
|---|---|---|
| Standing risk review | **Monthly** (first review 2026-10-26) | Updated register, changed scores with rationale, new/closed IDs |
| Phase-gate check | At every gate in `21-completion/quality-gates.md` (Gate 0 before implementation, and each subsequent gate) | Gate decision: risks owning that phase must be mitigated to plan or explicitly accepted by the sponsor |
| Trigger-based review | New CRITICAL finding (`SEC-NNN`), new/changed `DEP-*`/`ASM-*`/`GAP-*`, provider contract change, incident, scope change | Ad-hoc review within 5 working days |
| Validation audit | After any structural change (root README §9) | Entries in `20-validation/consistency-audit.md` |

Participants, update rules, escalation thresholds, burndown reporting, and ID-allocation rules: `risk-review-process.md` (DOC-RSK-004).

## 6. File Index

| # | File | Document ID | Content |
|---|---|---|---|
| 1 | `README.md` | DOC-RSK-001 | This overview: taxonomy, scoring, strategies, cadence |
| 2 | `risk-register.md` | DOC-RSK-002 | **Canonical register `RISK-001…RISK-024`** — summary table + per-risk detail |
| 3 | `mitigation-plans.md` | DOC-RSK-003 | Phased plans, controls, kill criteria and metrics for the top 8 risks by score |
| 4 | `risk-review-process.md` | DOC-RSK-004 | Governance: cadence, update rules, escalation, phase gates, ID allocation, finding/gap linkage |

## 7. Relationship to Findings, Gaps, and Constraints

- A **security finding (`SEC-NNN`, `../09-security/core/security-findings.md`)** is a design defect discovered by analysis; a **risk (`RISK-NNN`)** is the uncertainty that an event harms an objective. *Finding ≠ risk* — but every finding is screened: if it threatens an objective it feeds (mirrors) a register entry (e.g. `SEC-011` ↔ `RISK-006`). Rules for that screening: `risk-review-process.md` §6.
- A **gap (`GAP-NNN`, `20-validation/missing-information.md`)** is missing information; unresolved gaps *generate* risks (e.g. `GAP-03` supports notification-channel risk exposure; `GAP-07` feeds RISK-018).
- A **constraint (`C-01…C-26`)** is never a risk and can never be traded away to reduce one — mitigation may never violate a constraint (root README §9; conflicts go to `20-validation/contradiction-audit.md`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
