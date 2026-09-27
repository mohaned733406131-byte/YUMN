---
document_id: DOC-CMP-004
title: Quality Gates — Gate 0 to Gate 3
category: 21-completion
status: approved
version: 1.0
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-013, NFR-001, NFR-005, NFR-019, SEC-REQ-012, DATA-REQ-004]
related_documents: [DOC-OVR-003, DOC-OVR-009, DOC-OVR-010, DOC-OVR-011, DOC-TST-001, DOC-TST-003, DOC-TST-004, DOC-RSK-002, DOC-RSK-004, DOC-SEC-008, DOC-DPL-006, DOC-NFD-007, DOC-UX-001, DOC-BA-006, DOC-CMP-002, DOC-CMP-006]
---

# Quality Gates

The gate system that the rest of `docs/` points at: `00-project-overview/project-charter.md` (baseline mandate), `00-project-overview/assumptions.md` (escalation rule), `00-project-overview/stakeholders.md` (conflict resolution), `01-business-analysis/stakeholder-needs.md` (STK-01), `13-testing/README.md` (§1, L25), `13-testing/test-plans.md` (L17, L46), `17-risk-management/` (phase-gate risk check), `11-ui-ux/README.md` (§7, L114), `17-risk-management/risk-register.md` (phase-gate scope audit).

**Methodology:** a gate is not a meeting or an opinion — it is an evidence review with a recorded outcome (root README §11; `13-testing/README.md` §1: "No gate is passed by opinion").

---

## 1. Outcome Vocabulary

| Outcome | Meaning |
|---|---|
| `PASS` | Every entry criterion met and every required evidence artifact present and green |
| `PASS WITH FINDINGS` | Gate proceeds, but each finding has an owner, a severity (`CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`), and a written disposition recorded before the next gate |
| `FAIL` | **Block.** The transition guarded by this gate does not happen; work stays in the current phase. Re-presentation requires new evidence, not argument |

**What `FAIL` means operationally:** Phase 1 does not start on a Gate 0 `FAIL`; Phase 2 does not start on a Gate 1 `FAIL`; go-live does not occur on a Gate 2 `FAIL`; closure/acceptance does not occur on a Gate 3 `FAIL`. The sponsor may accept a gate-blocking risk **only explicitly, in writing**, with the acceptance recorded as a register status change (`17-risk-management/risk-review-process.md` §4) — never by silence, never by schedule pressure.

**Conflict rule (non-negotiable):** where schedule pressure meets quality, **quality gates in money paths win** — recorded in `00-project-overview/stakeholders.md` ("Speed-to-market vs quality gates | `21-completion/quality-gates.md` — gates are non-negotiable for money paths") and `01-business-analysis/stakeholder-needs.md` STK-01 (sponsor "may trade quality for schedule — quality gates in money paths are non-negotiable"). If scope must give, scope gives: tests, monitoring, backups, and money-path gates are never traded (RISK-005 decision rule, `17-risk-management/mitigation-plans.md`).

**Standing input to every gate:** `20-validation/critical-findings.md` (open critical items must be dispositioned), plus `20-validation/missing-information.md` (GAP register), `20-validation/contradiction-audit.md`, and `20-validation/consistency-audit.md`. Evidence status: `INSUFFICIENT EVIDENCE` — `20-validation/` is declared in root README §2 but not yet authored in `docs/`; gates consume it by path, and its authoring is tracked as `TD-10` in `21-completion/technical-debt.md`.

---

## 2. Checks Embedded at Every Gate

**Phase-gate risk check** — mandated at every gate by `17-risk-management/risk-review-process.md` §1 and §7; run and recorded as part of the gate (this file embeds it, per §10 of that process):

| # | Check | Pass criterion |
|---|---|---|
| G-R1 | Risks whose owning phase is the one being gated | Status `MITIGATING`/`MONITORING` with linked evidence, or explicit sponsor acceptance |
| G-R2 | New CRITICAL risks since the last gate | Escalated within 24 h and dispositioned |
| G-R3 | Gate-critical dependencies | `DEP-06` signed before Gate 0; `DEP-10` before payment build; `DEP-09` before launch |
| G-R4 | Assumption verification | `ASM-03`, `ASM-04`, `ASM-12`, `ASM-14` re-scored with evidence |
| G-R5 | Constraint verification plan | `AC-S-02`-facing constraint tests exist for constraints touched by mitigations |
| G-R6 | Register hygiene | No silent changes (`20-validation/consistency-audit.md` clean); ID sequences intact |
| G-R7 | Contingency readiness | Kill criteria of the top-8 plans (`17-risk-management/mitigation-plans.md`) known to gate participants |

**Documentation checks at every gate:**

| # | Check | Pass criterion |
|---|---|---|
| D-1 | Link validation | Every path cited by documents in scope resolves to an existing file (root README §11) |
| D-2 | Debt register review | `21-completion/technical-debt.md` reviewed; every open `TD-NN` has owner + disposition |
| D-3 | ID discipline | No cited `FR`/`TC`/`BR`/`RISK`/`ASM`/`DEP`/`GAP`/`AC`/`SEC` ID is absent from its owning register |
| D-4 | Evidence tags | Gate submissions classify statements `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE` |

---

## 3. Gate 0 — Pre-Implementation Readiness

**Mandated explicitly:** `00-project-overview/project-charter.md` L46 — "Budget, staffing, and schedule baselines are `INSUFFICIENT EVIDENCE` at this stage (see `ASM-14`) — they must be established before implementation kickoff (`21-completion/quality-gates.md`, Gate 0)". Also mandated by the `00-project-overview/assumptions.md` escalation rule (blocking assumptions `ASM-03`, `ASM-04`, `ASM-12`, `ASM-14` must be resolved "before the quality gate that precedes implementation") and by `17-risk-management/risk-register.md` (`RISK-011` phase-gate scope audit; `RISK-006`/`RISK-012` blocking).

**Purpose:** authorize the start of implementation. Nothing has been built; this gate judges readiness, not product.

**Entry criteria:** analysis knowledge base approved; this gate review convened with participants below.

**Checklist:**

| # | Check | Pass criterion | Canon | Evidence status today |
|---|---|---|---|---|
| 0.1 | Baselines established | Sponsor sets budget, team size, and schedule baselines; `ASM-14` re-scored with evidence | charter L46; `assumptions.md` | `INSUFFICIENT EVIDENCE` — not set |
| 0.2 | Dangerous assumptions resolved | `ASM-03` (provider merchant APIs), `ASM-04` (SMS/WhatsApp reachability), `ASM-12` (Central Bank permits closed-loop wallets — `DANGEROUS`) resolved or explicitly accepted in writing | `assumptions.md` escalation rule; G-R4 | `UNSUPPORTED` ×2, `DANGEROUS` ×1 |
| 0.3 | Gate-critical dependencies opened or mitigated | `DEP-06` signed (registration has no fallback); `DEP-05` sandbox granted from **both** m-Floos and OneCash, or an explicit sponsor decision to launch bank-transfer-only | `dependencies.md`; G-R3; `mitigation-plans.md` RISK-006/003 kill criteria | both **NOT STARTED** |
| 0.4 | Regulatory position before money build | `DEP-10` written Central Bank position on file before any B07 money-flow implementation | `dependencies.md`; RISK-012 kill criteria | Not started |
| 0.5 | GAP register triaged | `GAP-01…GAP-07` dispositioned with owners; Gate-0 blockers flagged in `20-validation/missing-information.md` | `00-project-overview/project-scope.md`; RISK-011 action ("Resolve `GAP-01…GAP-06` decisions before Gate 0") | register authored; decisions pending |
| 0.6 | Analysis sign-off | Charter sign-off path opened → `21-completion/final-acceptance.md` (all `AC-S-*` remain `PENDING` until evidence exists) | charter L87 | PENDING |
| 0.7 | Documentation link validation | Link pass across `docs/` with findings triaged (root README §11) | root README §11 | to be run at the gate |
| 0.8 | Risk check | G-R1…G-R7 run; Gate 0 is **the strictest** — `RISK-006` (`DEP-06`) and `RISK-012` (`DEP-10`) are blocking by canon | `risk-review-process.md` §7 | — |

**Required evidence:** signed contracts/approval receipts (SMS, WhatsApp, wallet providers), written Central Bank position, written legal opinions received so far (`DEP-09` items can be partial here — full set is due at Gate 2 for `AC-S-24`), sponsor baseline record, updated assumption rows with evidence links, GAP decision log, signed ledger design review (RISK-001 Phase 0 exit evidence), link-validation report.

**Participants:** **project sponsor (owns Gate 0)**, product owner (chairs risk review), technical lead, DevOps lead, security officer, business development, legal liaison, QA lead (evidence, not ownership), risk owners of the phase (`risk-review-process.md` §1).

**If `DEP-06` is unsigned:** Gate 0 `FAIL` — Phase 1 registration work may be built, but it cannot pass Gate 0 (`mitigation-plans.md` RISK-006 kill criterion). **If the `DEP-10` position is adverse:** B07 money-flow implementation stops; the sponsor chooses among the recorded redesign options before any payment-build spend (RISK-012 kill criteria) — this decision is itself recorded at Gate 0.

---

## 4. Gate 1 — Core-Build Exit (Phase 1 → Phase 2)

**Purpose:** judge whether the core build is real, covered, safe, and fast enough to justify pilot investment.

**Entry criteria:** Gate 0 `PASS` (or `PASS WITH FINDINGS` with written dispositions); evidence packages assembled per plan.

**Checklist:**

| # | Check | Pass criterion | Canon |
|---|---|---|---|
| 1.1 | Test evidence per plan | Every executed range meets the common exit: all TCs in range executed, P0/P1 100% PASS, 0 CRITICAL/HIGH open, evidence links on TCs | `13-testing/test-plans.md` §a |
| 1.2 | Critical-path plans green | `PLAN-01` Authentication, `PLAN-02` Authorization, `PLAN-09` Cart, `PLAN-10` Checkout/payment/wallet, `PLAN-11` Order lifecycle all exited | `test-plans.md` L46 (Phase-1 critical path) |
| 1.3 | Coverage vs AC registry | Coverage floors met (unit ≥ 80%, payment module ≥ 95%, auth ≥ 90%) and every AC in built scope maps to ≥ 1 passing test (253 ACs in `02-requirements/acceptance-criteria.md`) | `AC-S-08`, `AC-S-03`, G-TEST-1/G-TEST-3 |
| 1.4 | Money-path suites green | Checkout/payment/wallet + escrow + ledger invariant suites pass; `J1`/`J2` run in staging with seeded-mismatch detected within one run; ledger design promises implemented (append-only postings, single write path) | `AC-S-14`, `AC-S-15`; RISK-001 kill criterion; STK-01 rule |
| 1.5 | Constraint tests | `TST-CON-01…26` executed for constraints in scope; target 26/26 at release, with no regression in the touched set | `13-testing/constraint-tests.md`; `AC-S-02`; G-TEST-2 |
| 1.6 | Performance vs NFRs | k6 evidence at staging scale against `NFR-001/002/004`, `NFR-003` (`C-25`), `NFR-017`; early `PERF-01/04` runs green or remediated | `test-plans.md` §b; G-TEST-4 |
| 1.7 | Security findings triage | `SEC-P-01…SEC-P-09` results reviewed; `09-security/security-findings.md` entries triaged — 0 open CRITICAL/HIGH security defects; `SEC-011` (uncontracted sole auth channel, CRITICAL) and `SEC-015` (escrow TOCTOU, HIGH) closed or formally risk-accepted | `test-plans.md` §c exit; `security-findings.md`; G-TEST-5 |
| 1.8 | Design completeness | Customer-facing screens pass the design-complete gate (IA location, flow entry, all states, tokens, accessibility attributes, `ar`/`en` copy) | `11-ui-ux/README.md` L114 |
| 1.9 | Risk + debt checks | G-R1…G-R7 and D-1…D-4 run; debt register reviewed | §2 above |

**Required evidence:** executed plan results with TC evidence links; coverage report from CI; constraint-suite results; k6 reports; SAST/dependency/secret-scan reports; authz matrix results (`SEC-P-05`); `J1`/`J2` seeded-mismatch test record; design-completeness sign-off.

**Participants:** technical lead (chair for build-integrity checks), QA lead (produces verification evidence), security officer, DevOps lead, product owner, risk owners of Phase 1, sponsor (informed; required for any CRITICAL acceptance).

---

## 5. Gate 2 — Pilot & Hardening Exit (Phase 2 → Launch)

**Purpose:** authorize public launch. This is the gate that protects real money and real customers.

**Entry criteria:** Gate 1 `PASS`; pilot and drill evidence assembled; production-readiness rollup complete.

**Checklist:**

| # | Check | Pass criterion | Canon |
|---|---|---|---|
| 2.1 | Load tests at target | `PERF-01` steady 10K concurrent, 30 min: p95 read < 200 ms, p95 write < 500 ms, p99 write ≤ 1,000 ms, error < 0.1%, CPU/mem/pool within budget; all thresholds green on three consecutive runs | `test-plans.md` §b; `AC-S-05`; `C-25`; G-TEST-4 |
| 2.2 | Drills | `CHAOS-01…CHAOS-08` all PASS conditions met and recorded; `CHAOS-06` proves RTO ≤ 1 h / RPO ≤ 15 min with zero lost money; rollback drill ≤ 15 min; zero silent data loss proven by post-drill reconciliation | `test-plans.md` §d, §h; `AC-S-17`, `AC-S-20`; G-TEST-7 |
| 2.3 | Production readiness | All 52 rows `DONE` or explicitly `WAIVED`, with sponsor, QA lead, security owner, and ops owner signatures | `15-deployment/production-readiness.md` §8, §9 |
| 2.4 | Compliance checklist | `AC-S-24` sign-off evidence assembled: the ten deliverables of `12-non-functional/compliance-and-legal.md` §5 on file (data-protection opinion, Central Bank position, VAT opinion, retention opinion, processor/DPA set, bilingual terms + privacy notice, return/refund policy confirmation, messaging-consent wording, accessibility statement, evidence pack) | `compliance-and-legal.md` §5; `AC-S-24` |
| 2.5 | GAP closure for launch blockers | Every `GAP-*` that blocks a launch claim is closed or waived in writing with an owner (e.g. `GAP-01` targets, `GAP-05` commission tiers before tiered plans ship, `GAP-06` payout mode) | `20-validation/missing-information.md`; RISK-002/RISK-011 actions |
| 2.6 | Pilot evidence | ≥ 10 pilot vendors completed KYC → listing → sale → payout; end-to-end money cycle proven (top-up → order → escrow → commission → payout → refund); support process live | `AC-S-21`, `AC-S-22`, `AC-S-23` |
| 2.7 | Accessibility / localization / mobile | §e, §f, §g plan exits green (0 critical a11y violations, 0 RTL defects on core journeys, 0 blocking device-matrix defects) | `test-plans.md` §e–§g; `AC-S-10`, `AC-S-11` |
| 2.8 | Security release posture | DAST clean of exploitable high/critical; dependency/secret scans clean; threat-model coverage 100% | `test-plans.md` §c; `AC-S-12`, `AC-S-13`, `AC-S-16`; G-TEST-5 |
| 2.9 | Risk + debt checks | G-R1…G-R7 and D-1…D-4 run; debt register reviewed; residual `CRITICAL`/`HIGH` risks explicitly accepted in writing | §2 above |

**Required evidence:** k6 reports; drill and rehearsal records; production-readiness rollup with signatures; compliance evidence pack; pilot report; UAT sign-off sheets per surface (`AC-S-04`); security scan reports; a11y/localization reports; GAP closure records.

**Participants:** project sponsor (chair for launch authorization), product owner, technical lead, QA lead, security officer, DevOps/ops owner, legal liaison, business development, Finance (Admin) (money-cycle audit), risk owners of Phase 2.

**Launch gate hard stops:** unresolved `DEP-09`/`DEP-10` items (2.4), any open CRITICAL security defect (2.8), any money-path suite failure (from 1.4, re-verified), production-readiness row short of `DONE`/`WAIVED` without written waiver (2.3).

---

## 6. Gate 3 — Post-Launch Review

**Purpose:** confirm the platform operates at its promises, residual risk is honest, and debt is being managed — closing the loop back to `21-completion/final-acceptance.md`.

**Entry criteria:** Launch executed; monitoring, reconciliation, and review cadences running.

**Checklist:**

| # | Check | Pass criterion | Canon |
|---|---|---|---|
| 3.1 | SLOs in service | Availability evidence against `AC-S-06` (99.99% over any rolling 30-day window) reviewed; latency/error SLOs monitored with RED metrics; alert inventory current | `AC-S-06`, `AC-S-18`; `12-non-functional/observability.md`; G-TEST-7 |
| 3.2 | Residual CRITICALs | No `CRITICAL` security finding or risk remains undispositioned; each residual has owner, severity, and written acceptance | `09-security/security-findings.md`; `risk-review-process.md` §4 |
| 3.3 | Debt register review | `21-completion/technical-debt.md`: every `TD-NN` reviewed — paid down, scheduled, or explicitly accepted with rationale | `21-completion/technical-debt.md`; D-2 |
| 3.4 | Assumption re-score with real data | Pilot/production evidence re-scores `ASM-01`, `ASM-05`, `ASM-06`, `ASM-08`, `ASM-09`; `GAP-01` targets set by sponsor are tracked | `assumptions.md`; RISK-002/RISK-024 actions |
| 3.5 | Risk burndown | Burndown report produced honestly (no smoothing; re-scoring up shown as a spike) | `risk-review-process.md` §8 |
| 3.6 | Production-readiness delta | Full re-run before any subsequent launch milestone; delta review before releases touching infrastructure, integrations, or compliance posture | `production-readiness.md` §9 cadence |
| 3.7 | Risk + debt checks | G-R1…G-R7 and D-1…D-4 run | §2 above |

**Required evidence:** SLO dashboards and incident records; reconciliation/attestation reports; monthly review minutes; updated `ASM`/`GAP`/`TD`/`RISK` registers; production-readiness delta results.

**Participants:** project sponsor, product owner (chairs the standing risk review), technical lead, DevOps lead, security officer, Finance (Admin), business development, legal liaison.

**Gate 3 → acceptance:** Gate 3 `PASS` or `PASS WITH FINDINGS` is a precondition for moving `21-completion/final-acceptance.md` from `PENDING` to `ACCEPTED`, together with a `PASS`/`PASS WITH FINDINGS` final quality assessment in `20-validation/analysis-validation.md` (root README §10 item 48) and signed gate history for Gates 0–3.

---

## 7. Gate Summary & Current Status

| Gate | Guards | Owner / chair | Outcome recorded in | Status as of 2026-09-27 |
|---|---|---|---|---|
| Gate 0 | Start of implementation | **Project sponsor** | This file + `20-validation/analysis-validation.md` | `PENDING` — prerequisites `INSUFFICIENT EVIDENCE` (`ASM-14`, `DEP-05`, `DEP-06`, `DEP-10`) |
| Gate 1 | Phase 1 → Phase 2 | Technical lead (sponsor for CRITICAL acceptances) | This file | `PENDING` — no implementation exists |
| Gate 2 | Phase 2 → Launch | Project sponsor | This file + `15-deployment/production-readiness.md` §9 | `PENDING` — production-readiness 0/52 rows `DONE` |
| Gate 3 | Post-launch closure → acceptance | Project sponsor + product owner | This file + `20-validation/analysis-validation.md` | `PENDING` — platform not launched |

Honesty rule: **no gate has been run, and none can pass today** — no implementation exists (root README §6: no document is `VERIFIED`). Records of future outcomes are created when the evidence exists; this file defines what will be judged, not what has been.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 36,44,46,48 + charter pointer |
