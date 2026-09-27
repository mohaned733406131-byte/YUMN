---
document_id: DOC-RSK-004
title: Risk Review Process (Governance)
category: 17-risk-management
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-014, FR-020]
related_documents: [DOC-RSK-001, DOC-RSK-002, DOC-RSK-003, DOC-ROOT-001, DOC-SEC-008, DOC-OVR-008]
---

# Risk Review Process (DOC-RSK-004)

Governance for how risks enter the register, how they change, who reviews them, when they escalate, and how they connect to findings (`SEC-NNN`), gaps (`GAP-NNN`), constraints (`C-01…C-26`), and the quality gates (`21-completion/quality-gates.md`, `20-validation/`).

## 1. Cadence

| Review | Frequency | Chair | Required participants | Output |
|---|---|---|---|---|
| Standing risk review | **Monthly** — first occurrence 2026-10-26, then the 26th of each month (or next working day) | Product owner | Sponsor (informed; required for CRITICAL), Technical lead, DevOps lead, Security officer, Finance (Admin), Business development | Updated register + change-history rows; score changes with rationale; burndown snapshot |
| Phase-gate risk check | At **every gate** in `21-completion/quality-gates.md` (Gate 0 before implementation, and each subsequent gate) | Project sponsor | Gate participants + risk owners of that phase | Gate decision: mitigate-to-plan, accept-with-conditions, or block |
| Trigger-based review | Within **5 working days** of the trigger (§3) | Whoever detects the trigger | Affected risk owner(s) | Ad-hoc register update or explicit "no change" note |
| Post-incident review | Within 48 h of any incident touching money, auth, or availability | Technical lead | Owner of the impacted risk + Security officer | Re-scored risk + corrective actions |

Cadence is a floor, not a ceiling: any participant may request an ad-hoc review; refusing to review a raised concern must itself be recorded in `20-validation/contradiction-audit.md`.

## 2. Roles & Responsibilities

| Role | Responsibility |
|---|---|
| Project sponsor | Owns RISK-012 and RISK-017; approves acceptance of any CRITICAL risk; receives escalations within 24 h; signs gate risk decisions |
| Product owner | Chairs the standing review; owns adoption/business risks (RISK-002, RISK-011, RISK-015, RISK-022, RISK-024) |
| Technical lead | Owns technical integrity risks (RISK-001 engineering half, RISK-007, RISK-008, RISK-021); enforces ADR/stack discipline |
| DevOps lead | Owns operational risks (RISK-005, RISK-014, RISK-019, RISK-023); produces availability/backup evidence |
| Security officer | Screens findings for risk mirroring (§6); owns RISK-009 (with Technical lead) and RISK-020 (with Legal) |
| Business development | Owns provider commercial risks (RISK-003, RISK-006) and courier supply (RISK-018) |
| Finance (Admin) | Owns money-leakage risks (RISK-010, RISK-013); is the operational authority for RISK-001 contingency |
| Legal liaison | Owns regulatory evidence delivery (RISK-004, RISK-020, `DEP-09`) |
| QA lead | Produces verification evidence for mitigations (tests, drills) — evidence, not ownership |

Ownership transfer (e.g., staffing change) is a register update: owner column changes with date and reason; **an ownerless risk is a review failure**, flagged at the next meeting.

## 3. Triggers for Out-of-Cycle Review

1. Any new `CRITICAL` finding (`SEC-NNN`) in `09-security/security-findings.md`.
2. Any change to a `DEP-*` status (especially `DEP-05`, `DEP-06`, `DEP-08`, `DEP-09`, `DEP-10`), or a dependency newly marked NOT STARTED/failed.
3. Any assumption changing status (`ASM-*`) — particularly toward `UNSUPPORTED`/`DANGEROUS`.
4. Any new `GAP-NNN` or a gap resolved (may create or close a risk).
5. Provider contract, pricing, or outage events; any P1/P2 incident; any reconciliation mismatch (`J1`/`J2`) in production.
6. Scope changes propagated from `00-project-overview/project-scope.md` or a new/superseding ADR in `18-decisions/ADR/`.
7. Regulatory communication (tax or Central Bank) touching `DEP-09`/`DEP-10`.

## 4. Escalation Thresholds

| Condition | Escalation | Deadline |
|---|---|---|
| **Any new CRITICAL risk** (score ≥ 20) | Written notice to **project sponsor** + add to next steering discussion | **Within 24 h of identification** |
| Any risk re-scored **into CRITICAL** | Same as above, plus immediate register update | 24 h |
| CRITICAL risk whose mitigation misses its plan date | Sponsor decision: re-plan, accept with conditions, or block the gate | At the missed date (no waiting for monthly review) |
| New HIGH risk (12–19) | Notify risk owner + product owner; scheduled into next monthly review | 5 working days |
| Mitigation evidence failing (e.g., drill miss, contract slip) | Owner reports at monthly review with corrective action | Next monthly review |
| Constraint conflict surfaced by a mitigation (`C-01…C-26`) | Log in `20-validation/contradiction-audit.md`; constraints win (DOC-ARCH-010 §6, root README §9) | Immediately |
| Gate-blocking risk unresolved | Gate is **not passed**; sponsor may only accept explicitly, in writing, with the acceptance recorded as a register status change | At the gate |

Escalation never happens by implication: the escalation is a written record (register note, review minutes, or validation-audit entry).

## 5. Register Update Rules (no silent changes)

1. **Change management is root README §9**: edit the document, bump `version`, add a `## Change History` row stating what changed and why.
2. Every score change records: old score → new score, driver (evidence or event), date, and reviewer.
3. Status values: `OPEN` → `MITIGATING` (plan started, evidence partial) → `MONITORING` (mitigation complete, evidence linked) → `CLOSED` (target state achieved *and* verified). `ACCEPTED` is a response decision recorded on an open risk, not a terminal status. **Nothing may be set to `MITIGATING`/`MONITORING`/`CLOSED` without a linked evidence artifact** (test report, signed contract, drill record, audit sign-off) — at v1.0 all 24 risks are `OPEN` because no implementation exists.
4. Severity follows score mechanically (DOC-RSK-001 §3.3); manual severity overrides are prohibited — if the band feels wrong, the probability/impact rationale must be re-argued instead.
5. Impacted documents are updated in the same change set (consistency rule) and the change set is recorded in `20-validation/consistency-audit.md`.
6. Risks are never deleted; `CLOSED` entries remain with their full history.

## 6. Relationship to Findings (`SEC-NNN`) and Gaps (`GAP-NNN`)

**Finding ≠ risk.** The two registers answer different questions and use different scales:

| | Security finding (`SEC-NNN`) | Risk (`RISK-NNN`) |
|---|---|---|
| Question | What design defect exists today? | What future event could harm an objective, and how bad? |
| Severity meaning | Exploitability/impact *if the gap is exploited as designed today* | Probability × Impact on project objectives |
| Scope | Security only | All eight categories (DOC-RSK-001 §2) |
| Lives in | `09-security/security-findings.md` | `17-risk-management/risk-register.md` |

**Screening rule (finding → risk):** every finding is screened at the monthly review; it *feeds* (mirrors into) a register entry **when it threatens a project objective or critical path**, not merely when it is severe. Worked examples from canon: `SEC-011` (uncontracted sole auth channel) ↔ `RISK-006`; `SEC-002`/`SEC-015` (immutability, escrow TOCTOU) feed `RISK-001`. A HIGH finding may feed a risk that is already registered — the finding adds a *trigger*, not a duplicate. Closure of a finding does not auto-close a risk (and vice versa); each is closed on its own evidence.

**Gap → risk:** a gap is missing information; it *generates* a risk when the missing information blocks or threatens an objective. Examples: `GAP-03` (email channel) is already absorbed into `BR-NTF-01` scope and RISK-006's no-third-path residual; `GAP-05` (commission tiers) feeds RISK-002/RISK-022; `GAP-07` (fleet partners) feeds RISK-018; `GAP-01` (growth targets) limits RISK-024 measurement. Resolving a gap triggers a re-screen (§3.4), and may retire the risk it created.

**Constraint relationship:** constraints are never risks and never traded to reduce one; a mitigation that conflicts with `C-01…C-26` is invalid and logged as a contradiction, not implemented.

## 7. Phase-Gate Checks

At each gate in `21-completion/quality-gates.md`, the gate review runs this checklist and records the result (gate document + `20-validation/analysis-validation.md` where applicable):

| # | Check | Pass criterion |
|---|---|---|
| G-R1 | All risks whose **owning phase** is the one being gated | Status `MITIGATING`/`MONITORING` with evidence, or explicit sponsor acceptance |
| G-R2 | New CRITICAL risks since last gate | Escalated within 24 h (§4) and dispositioned |
| G-R3 | Gate-critical dependencies | `DEP-06` signed before Gate 0; `DEP-10`/`DEP-09` closed before payment build/launch respectively (see `risk-register.md` RISK-006/012/004) |
| G-R4 | Assumption verification | `ASM-03`, `ASM-04`, `ASM-12`, `ASM-14` re-scored with evidence (assumptions.md escalation rule) |
| G-R5 | Constraint verification plan | `AC-S-02`-facing constraint tests exist for constraints touched by mitigations |
| G-R6 | Register hygiene | No silent changes since last gate (`consistency-audit.md` clean); ID sequence intact |
| G-R7 | Contingency readiness | Kill criteria of top-8 plans (`mitigation-plans.md`) known to the gate participants |

Gate 0 is the strictest: RISK-006 (`DEP-06`) and RISK-012 (`DEP-10`) are blocking by canon (`dependencies.md`, `assumptions.md` escalation rule).

## 8. Risk Burndown Reporting

| Element | Definition |
|---|---|
| Report owner | Product owner; produced monthly with the review |
| Distribution | Sponsor, steering (STK-01/STK-02), risk owners; archived with review notes |
| Burndown measure | Count and score-sum of **open** risks by severity band, trended month over month; a risk is "burned down" only when it leaves `OPEN`/`MITIGATING` with linked evidence — re-scoring up is shown as a spike, never smoothed |
| Companion views | (a) score distribution by category (taxonomy coverage); (b) mitigation-plan progress for the current top 8 (step done / evidence linked / metric on target); (c) dependency & assumption status strip (`DEP-*`, `ASM-*` driving risks); (d) gate readiness status for the next gate |
| Honesty rule | Before implementation, burndown is **flat by construction** — zero risks can close. The report must state this explicitly rather than showing artificial progress (DOC-RSK-001 §1) |
| Escalation feed | Any risk increasing two bands, or entering CRITICAL, appears at the top of the report with the 24-h escalation note |

## 9. Allocating New Risk IDs

1. New risk = next free sequential number: `RISK-001…RISK-024` exist → the next is **`RISK-025`**, then `RISK-026`, … (`RISK-NNN`, root README §5).
2. **IDs are never reused**, even after `CLOSED`; a conceptually similar risk that recurs gets a new ID and a reference to the closed one.
3. IDs are allocated only in `risk-register.md` (single allocator — the register is the source of truth); the proposing participant drafts the entry, the product owner assigns the ID at (or before) the review.
4. No other document may mint `RISK-*` IDs; citations elsewhere must already exist in the register (a citation to a non-existent risk ID is a consistency-audit defect).
5. Number gaps are prohibited (no skipping to "reserve" numbers) — the sequence is dense so that ID arithmetic ("is 007 in the register?") stays valid for navigators like root README §5.

## 10. Relationship to Validation & Completion Domains

- `20-validation/consistency-audit.md` — records every risk-document impact set from §5.
- `20-validation/contradiction-audit.md` — receives constraint conflicts, severity disputes, and unreconciled citations.
- `20-validation/missing-information.md` — owns `GAP-NNN`; §6 links gaps to the risks they feed.
- `21-completion/quality-gates.md` — embeds §7 checks; `21-completion/final-acceptance.md` verifies that no CRITICAL risk was closed without evidence and that gate acceptances are signed.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
