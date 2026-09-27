---
document_id: DOC-CMP-010
title: Final Acceptance — Sign-off & Evidence Requirements
category: 21-completion
status: approved
version: 1.0
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [AC-S-01, AC-S-02, AC-S-03, AC-S-04, AC-S-05, AC-S-06, AC-S-08, AC-S-10, AC-S-11, AC-S-12, AC-S-13, AC-S-14, AC-S-15, AC-S-16, AC-S-17, AC-S-18, AC-S-19, AC-S-20, AC-S-21, AC-S-22, AC-S-23, AC-S-24]
related_documents: [DOC-OVR-011, DOC-OVR-003, DOC-TST-003, DOC-TST-004, DOC-CMP-004, DOC-CMP-006, DOC-CMP-007, DOC-RSK-002, DOC-DPL-006, DOC-NFD-007]
---

# Final Acceptance — Sign-off & Evidence Requirements

The terminal document of the knowledge base: `00-project-overview/success-criteria.md` forward-references it ("Final acceptance is tracked in `21-completion/final-acceptance.md`"), and `00-project-overview/project-charter.md` (L87) routes sign-off here ("validity… `VOID`" until conditions are met). It defines **what** must be true, **who** signs, and **what evidence** each signature rests on — it does not run the gates (that is `21-completion/quality-gates.md`) nor decide acceptance (that is `20-validation/analysis-validation.md`, methodology item 48).

**Status as of 2026-09-27: `PENDING`.** No implementation exists; every `AC-S-*` remains `PENDING` until evidence exists (root README §6 — nothing is `VERIFIED`). Acceptance cannot be signed today, and nothing in this file may be pre-filled with outcomes.

---

## 1. What Acceptance Means

Final acceptance is a **two-layer judgment**, each layer with its own recorded outcome:

| Layer | Question answered | Decided by | Outcome vocabulary |
|---|---|---|---|
| **A — Knowledge base** | Is the analysis internally consistent, complete against its own promises, and approved? | Final quality assessment in `20-validation/analysis-validation.md` | `PASS · PASS WITH FINDINGS · FAIL` |
| **B — Product / platform** | Do the success criteria, gates, risk posture, and compliance obligations hold with real evidence? | Success-criteria evidence + gate history (Gates 0–3) | Per-gate outcomes + per-`AC-S-*` `PASS`/`FAIL` |

A `FAIL` on either layer blocks acceptance. `PASS WITH FINDINGS` on either layer requires every finding to carry severity (`CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`), an owner, and a written disposition — acceptance signs **with** the findings, never over them.

**Layer A minimum conditions** (root README §10 items 40–43, 45, 48):

1. Final quality assessment `PASS` or `PASS WITH FINDINGS` in `20-validation/analysis-validation.md`.
2. `20-validation/contradiction-audit.md` and `20-validation/consistency-audit.md` clean or findings dispositioned (documentation check D-4 at Gate 3).
3. Link validation run across `docs/` with every broken path fixed or explicitly accepted (root README §11; D-1).
4. `21-completion/technical-debt.md` reviewed at Gate 3 — no open `CRITICAL`/`HIGH` `TD-NN` without written disposition (D-2).
5. Every `REC-NN` (P0/P1) either accepted by its criterion or explicitly deferred with rationale (`21-completion/recommendations.md` §2 rule 4).

**Layer B minimum conditions:**

1. **All 24 success criteria** (`00-project-overview/success-criteria.md`, `AC-S-01…AC-S-24`) carry linked evidence — including `AC-S-01` cross-reference coverage, `AC-S-03` zero requirement→test gaps, `AC-S-05` k6 targets, `AC-S-06` 99.99% availability window, `AC-S-24` compliance sign-off.
2. **Gate history complete:** Gates 0, 1, 2, 3 each recorded in `21-completion/quality-gates.md` §7 with outcome, findings, and evidence links — Gate 3 `PASS`/`PASS WITH FINDINGS` is a precondition (quality-gates §6).
3. **Risk posture closed out:** no `CRITICAL` residual undispositioned (Gate 3 check 3.2); burndown produced honestly (`risk-review-process.md` §8); all risk-acceptance decisions explicitly in writing (`risk-review-process.md` §4).
4. **GAP register triaged:** every `GAP-*` closed or waived with an owner (Gate 2 check 2.5 / Gate 3).
5. **Production-readiness:** all 52 rows `DONE` or `WAIVED` with four signatures (Gate 2 check 2.3) — re-run delta before any subsequent milestone (`production-readiness.md` §9).
6. **Compliance pack complete:** the ten `AC-S-24` deliverables on file (`12-non-functional/compliance-and-legal.md` §5), including the written Central Bank position (`DEP-10`) and legal opinions (`DEP-09`).

---

## 2. Evidence Package Index

Assembled before the sign-off meeting; each artifact names its source path. Missing artifacts block the signature that depends on them.

| # | Artifact | Source path | Serves |
|---|---|---|---|
| E-01 | Final quality assessment (layer A outcome) | `20-validation/analysis-validation.md` | Layer A |
| E-02 | Contradiction + consistency audit reports | `20-validation/contradiction-audit.md`, `20-validation/consistency-audit.md` | Layer A |
| E-03 | Requirements-to-tests traceability matrix (all `AC-S-*` → TCs → passing runs) | `19-traceability/requirements-to-tests.md` | Layer B (`AC-S-01`, `AC-S-03`) |
| E-04 | Success-criteria evidence table (24 rows, each with link + date + executor) | `00-project-overview/success-criteria.md` | Layer B |
| E-05 | Gate history (Gates 0–3 outcomes, findings, acceptances) | `21-completion/quality-gates.md` §7 | Both layers |
| E-06 | Executed test-plan results + coverage report (P0/P1 100% PASS, 0 CRITICAL/HIGH open) | `13-testing/test-plans.md` §a–§h; CI artifacts | Layer B |
| E-07 | Performance evidence (k6: `PERF-01…PERF-06`, `PERF-07`) | `13-testing/test-plans.md` §b; CI artifacts | `AC-S-05` |
| E-08 | Drill records: DR, deploy/rollback rehearsal, chaos | `13-testing/test-plans.md` §d/§h; `15-deployment/production-readiness.md` | `AC-S-17`, `AC-S-20` |
| E-09 | Security posture pack (SAST/DAST/secret/dependency, threat-model coverage, findings triage) | `09-security/security-findings.md`; CI artifacts | `AC-S-12`, `AC-S-13`, `AC-S-16` |
| E-10 | Compliance evidence pack (ten items incl. Central Bank position, legal opinions, bilingual notices, a11y statement) | `12-non-functional/compliance-and-legal.md` §5 | `AC-S-24` |
| E-11 | Production-readiness rollup with sponsor/QA/security/ops signatures | `15-deployment/production-readiness.md` §8/§9 | Gate 2 / launch |
| E-12 | Risk burndown + open-risk register with written acceptances | `17-risk-management/risk-review-process.md` §8; `17-risk-management/risk-register.md` | Layer B |
| E-13 | Debt + recommendation disposition reports | `21-completion/technical-debt.md`; `21-completion/recommendations.md` | Layer A |
| E-14 | GAP closure log + assumption re-score record (`ASM-01…ASM-14` with evidence) | `20-validation/missing-information.md`; `00-project-overview/assumptions.md` | Both layers |
| E-15 | Pilot + UAT evidence (≥ 10 vendors; four-surface UAT sign-offs) | `13-testing/test-plans.md` §g; `AC-S-04`, `AC-S-21` | Layer B |
| E-16 | Accessibility, localization, mobile device-lab reports | `13-testing/test-plans.md` §e/§f/§g | `AC-S-10`, `AC-S-11` |

---

## 3. Sign-off Table

Signatures are recorded with name, role, and date; each signer owns the evidence rows marked against them. Roles follow `00-project-overview/stakeholders.md` and the gate participant lists.

| Role | Signs for | Depends on evidence | Signature | Date |
|---|---|---|---|---|
| **Project sponsor** | Overall acceptance; baselines (`ASM-14`); risk acceptances; layer A/B outcome | E-01, E-04, E-05, E-12, E-14 | — | — |
| **Product owner** | Requirements completeness: all `AC-S-*` traced and covered; GAP triage | E-03, E-04, E-14 | — | — |
| **Technical lead** | Architecture & build integrity: constraints, ADR compliance, test evidence | E-06, E-07, E-13 | — | — |
| **QA lead** | Verification evidence: plan exits, coverage, zero CRITICAL/HIGH open | E-06, E-15, E-16 | — | — |
| **Security officer** | Security posture: findings triage, threat-model coverage, money-path controls | E-09, E-11 | — | — |
| **Legal liaison** | Compliance position: `DEP-09`/`DEP-10`, full `AC-S-24` checklist | E-10 | — | — |
| **DevOps / ops owner** | Operability: drills, production-readiness, monitoring, rollback evidence | E-08, E-11 | — | — |
| **Business development** | Commercial dependencies: `DEP-05`, `DEP-06`, pilot/vendor outcomes | E-15, E-14 | — | — |
| **Finance (Admin)** | Money-path correctness: ledger/reconciliation/payout audit evidence | E-06, E-11 | — | — |

**Acceptance decision** (recorded once all rows above are signed, or explicitly listing exceptions):

| Outcome | Recorded by | Sets |
|---|---|---|
| `ACCEPTED` | Project sponsor, with layer A assessment attached | `status:` of this document → version bump + Change History row |
| `ACCEPTED WITH FINDINGS` | Sponsor; each finding severity-classified with owner and disposition date | same, plus findings appendix |
| `REJECTED` | Sponsor; blocking layer/`AC-S-*` identified | work returns to the owning phase — no partial acceptance |

---

## 4. Current Readiness Snapshot (2026-09-27)

| Requirement | State | Blocker |
|---|---|---|
| Layer A final quality assessment | Not started | `20-validation/` not authored (`TD-10` / REC-09) |
| Gate history | 0 of 4 run (all `PENDING`) | Gate 0 prerequisites `INSUFFICIENT EVIDENCE` (`ASM-14`, `DEP-05`, `DEP-06`, `DEP-10`) |
| `AC-S-01…24` | All `PENDING` | No implementation, no test evidence (root README §6) |
| Debt/recommendations | 10 `TD-NN` `OPEN`; 15 `REC-NN` unaccepted | REC-03…REC-05, REC-09 are P0 |
| Compliance pack | 0 of 10 items on file | `DEP-09` Not started, `DEP-10` Not started |
| Production readiness | 0 of 52 rows `DONE` | Platform not built |

**Acceptance verdict today: `PENDING` — cannot be signed.** The path from here is exactly `21-completion/implementation-roadmap.md` → `21-completion/quality-gates.md` Gates 0→3 → this document.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 36,44,46,48 + charter pointer |
