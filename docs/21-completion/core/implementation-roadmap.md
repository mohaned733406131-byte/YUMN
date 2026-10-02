---
document_id: DOC-CMP-002
title: Implementation Roadmap — Phased Delivery Plan
category: 21-completion
status: approved
version: 1.2
created: 2026-09-27
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-013, FR-017, NFR-001, NFR-005, NFR-019]
related_documents: [DOC-OVR-003, DOC-OVR-009, DOC-OVR-010, DOC-RSK-002, DOC-RSK-003, DOC-RSK-004, DOC-TST-003, DOC-DPL-006, DOC-NFD-007, DOC-CMP-004]
---

# Implementation Roadmap (Phased Delivery Plan)

> **SCHEDULE FLOATS.** There are **no calendar dates, no effort estimates, and no sprint numbers in this document, by design.** Budget, team-size, and schedule baselines are `INSUFFICIENT EVIDENCE` (`ASM-14`, `00-project-overview/assumptions.md`) and must be established by the sponsor **before implementation kickoff** at Gate 0 (`00-project-overview/project-charter.md` Authority; `quality-gates.md`). Until `ASM-14` is resolved, all sequencing below is **relative and conditional**: one phase begins only when the previous phase's exit gate outcome is recorded.

**Authority:** this file is the delivery-model authority for the project — the charter cites it directly ("Delivery model | Phased (see `implementation-roadmap.md`)"). The sprint-cadence view derived from it for test planning is `roadmap.md` (precedence rule: this file wins on conflict — `21-completion/README.md` §3).

**Phase vocabulary** (fixed by `../../17-risk-management/core/mitigation-plans.md`): **Phase 0** = pre-implementation · **Phase 1** = core build · **Phase 2** = pilot & hardening · **Launch** = public availability · **Post-launch** = operation and review. **"Nothing is implemented yet" applies to every row below** (DOC-RSK-001 §1) — this plan describes work to be done, not work done.

---

## 0. Phase Summary

| Phase | Objective | Exit gate | Primary evidence produced |
|---|---|---|---|
| Phase 0 — pre-implementation | Close dependencies, verify dangerous assumptions, set baselines, pass Gate 0 | **Gate 0** | Signed contracts/opinions, re-scored `ASM-*`, baseline record, GAP triage record, analysis sign-off |
| Phase 1 — core build | Build all blocks `B01…B13` with tests; P0 use cases first | **Gate 1** | Executed plans (PLAN-01…PLAN-18), coverage reports, constraint tests `TST-CON-01…26`, SAST/dependency scans, staging baselines |
| Phase 2 — pilot & hardening | Prove the build under load, fault, and real usage | **Gate 2** | k6 reports, chaos/drill records, a11y + localization reports, UAT sheets, pilot report, production-readiness rollup |
| Launch | Public availability with authorized go-live | — (Gate 2 outcome authorizes) | Go-live checklist entries, alert inventory, payout-enablement evidence |
| Post-launch | Operate, measure, review, burn down debt | **Gate 3** | SLO dashboards, reconciliation reports, monthly review records, debt-register review, residual-risk dispositions |

```text
Phase 0 ──(Gate 0)──► Phase 1 ──(Gate 1)──► Phase 2 ──(Gate 2)──► Launch ──► Post-launch ──(Gate 3)──► review closure
```

---

## 1. Phase 0 — Pre-Implementation (no product code)

**Objective.** Remove every condition that would make build work wasted, blocked, or unlawful; establish the baselines the whole plan floats on; obtain Gate 0.

**Entry criteria.** Analysis knowledge base approved and status `APPROVED` across `docs/` (root README §6) — **met at v1.0** (`VERIFIED`).

**Exit criteria — all must hold for Gate 0 `PASS`:**

| # | Criterion | Canon |
|---|---|---|
| 1 | Budget, team-size, and schedule baselines set by sponsor (`ASM-14` re-scored with evidence) | `00-project-overview/assumptions.md` escalation rule; charter Authority |
| 2 | Dangerous / blocking assumptions resolved: `ASM-03`, `ASM-04`, `ASM-12` (+ `ASM-14`) | `assumptions.md` L39 escalation rule |
| 3 | Gate-critical dependencies opened **or** their mitigation accepted in writing: `DEP-05`, `DEP-06` (and `DEP-10` before any B07 money build) | `00-project-overview/dependencies.md`; `../../17-risk-management/core/risk-review-process.md` §7 G-R3 |
| 4 | GAP register triaged: `GAP-01…GAP-07` dispositioned with owners (Gate-0 blockers flagged) | `00-project-overview/project-scope.md` UNCERTAIN SCOPE; `17-risk-management/core/risk-register.md` RISK-011 action |
| 5 | Analysis sign-off path opened — `00-project-overview/project-charter.md` sign-off flows to `final-acceptance.md` | charter L87 |
| 6 | Documentation link validation run across `docs/` (every cited path exists) | root README §11 validation rules |

**Content (what actually happens):**

- **Dependency closure — `DEP-01 … DEP-12` (`00-project-overview/dependencies.md`):**
  - `DEP-01…DEP-04`, `DEP-07` — status **Available** (`VERIFIED`): no action beyond environment bring-up (`../../14-devops-infrastructure/core/environments.md`).
  - `DEP-05` — m-Floos + OneCash merchant API access, status **NOT STARTED**: request sandbox credentials from **both** providers; start contract negotiation (SLA, API-change notice). Blocks `FR-013` production top-ups.
  - `DEP-06` — SMS provider contract (Telesom and/or Sabafon) + WhatsApp Business API approval, status **NOT STARTED**: this is the **hardest blocker** — registration (`FR-001`) has no fallback path. `risk-review-process.md` §7 G-R3: `DEP-06` signed **before Gate 0**.
  - `DEP-08` (domains/TLS/CDN) — **Not started**: needed for Launch, started here so it is not a launch-day surprise.
  - `DEP-09` (legal opinions: VAT, data protection) — **Not started**: feeds `ASM-10`/`ASM-13` and `AC-S-24`.
  - `DEP-10` (Central Bank position on closed-loop wallets) — **Not started**: existential for `C-01`; written position required before payment build (§Phase 1 money scope).
  - `DEP-11` (design assets) — **Partial** (brand tokens exist in `../../11-ui-ux/core/design-system.md`): close the remaining copy/logo gaps before frontend build.
  - `DEP-12` (test device lab + carrier SIMs) — **Not started**: required by `../../13-testing/core/test-plans.md` §g before mobile verification can complete.
- **Assumption verification:** `ASM-03` (provider merchant APIs — `UNSUPPORTED`), `ASM-04` (SMS/WhatsApp reachability — `UNSUPPORTED`), `ASM-12` (Central Bank permits closed-loop wallets — `DANGEROUS`), `ASM-14` (baselines — `UNSUPPORTED`). Also run the Phase-0 verification actions recorded for `ASM-05`, `ASM-09` (vendor discovery interviews) and `ASM-11` (sponsor confirmation of the 10K target) per `../../17-risk-management/core/mitigation-plans.md`.
- **GAP triage:** `GAP-01` growth targets, `GAP-02` delivery-code admin override, `GAP-03` email channel, `GAP-04` loyalty depth, `GAP-05` commission tiers, `GAP-06` vendor cash-out mode, `GAP-07` fleet partners — each gets a decision or an explicit "defer with owner" (`RISK-011` requires `GAP-01…GAP-06` resolved before Gate 0).
- **Design/decision readiness:** ledger design review signed (RISK-001 Phase 0 exit evidence), stack register + ADR-required rule adopted (`technology-stack.md` §8), architecture process agreed.

**Dependencies consumed:** `DEP-05`, `DEP-06`, `DEP-08`, `DEP-09`, `DEP-10`, `DEP-11`, `DEP-12`; `ASM-03`, `ASM-04`, `ASM-05`, `ASM-09`, `ASM-11`, `ASM-12`, `ASM-14`; `GAP-01…GAP-07`.

**Risks owned (register: `17-risk-management/core/risk-register.md`):** `RISK-006` (SMS/WhatsApp non-contracting — blocking at Gate 0), `RISK-012` (Central Bank position — blocking at Gate 0), `RISK-003` (wallet provider commercial failure → `DEP-05`), `RISK-004` (VAT ambiguity → `DEP-09`), `RISK-005` (ops complexity vs small team → `ASM-14` capacity), `RISK-002` (vendor adoption → `ASM-05`/`ASM-09` interviews, `GAP-05`), `RISK-011` (scope creep from unresolved gaps), `RISK-008` (performance shortfall → `ASM-11` confirmation), `RISK-001` (ledger design review signature).

**Evidence produced:** no test evidence (nothing exists to test). Evidence = signed contracts and written opinions, re-scored assumption rows with evidence links, sponsor baseline record, GAP decision log, signed ledger design review, link-validation report. All of it is presented at **Gate 0**.

---

## 2. Phase 1 — Core Build (blocks `B01…B13`, P0 first)

**Objective.** Build the platform's thirteen blocks with verification running alongside — never after — and reach a state where Gate 1 can be judged on evidence.

**Entry criteria.** Gate 0 outcome = `PASS` (or `PASS WITH FINDINGS` with every finding dispositioned in writing). Ledger design review signed (RISK-001 kill criterion: without it, Phase 1 money work does not start).

**Exit criteria — mapped to Gate 1:**

| # | Criterion | Canon |
|---|---|---|
| 1 | Plans executed for every completed range; P0/P1 test cases 100% PASS, 0 CRITICAL/HIGH open | `../../13-testing/core/test-plans.md` §a common exit |
| 2 | Coverage against the AC registry (273 ACs) with zero uncovered ACs in built scope | `02-requirements/acceptance-criteria.md`; `AC-S-03` |
| 3 | Money-path suites green (checkout/payment/wallet, escrow, ledger invariant) | `../../01-business-analysis/core/stakeholder-needs.md` STK-01; `00-project-overview/stakeholders.md` conflicts table |
| 4 | Performance evidence vs NFRs at staging scale | `../../13-testing/core/test-plans.md` §b; `AC-S-05` |
| 5 | Security findings triaged — 0 open CRITICAL/HIGH security defects | `../../09-security/core/security-findings.md`; `test-plans.md` §c exit |
| 6 | Constraint tests `TST-CON-01…26` 26/26 PASS for constraints touched by built scope | `../../13-testing/core/constraint-tests.md`; `AC-S-02` |

**Content:**

- **Blocks:** `B01` Identity & Access → `B13` Platform Administration, all thirteen in scope (`00-project-overview/project-context.md` §Platform Decomposition).
- **P0 use cases first — 17 of 40 (`VERIFIED` count from `../../01-business-analysis/use-case-index.md` §3: P0 = 17, P1 = 18, P2 = 5):**
  `UC-002` (register + OTP), `UC-003` (login), `UC-009` (add to cart), `UC-011` (checkout with wallet payment), `UC-013` (confirm receipt with delivery code), `UC-015` (vendor register + KYC), `UC-017` (product listing), `UC-019` (accept incoming order), `UC-020` (ready for pickup), `UC-026` (accept delivery assignment), `UC-027` (confirm pickup), `UC-030` (confirm delivery with 6-digit code), `UC-031` (approve/reject KYC), `UC-033` (manage orders & disputes), `UC-037` (roles & permissions), `UC-039` (auto-release escrow), `UC-040` (OTP with provider failover).
  P1 follows P0; P2 (`UC-008`, `UC-014`, `UC-023`, `UC-024`, `UC-036`) is deferrable within the phase but must exist before Gate 1 if its FR is claimed `VERIFIED`.
- **Critical-path test plans:** `PLAN-01` Authentication, `PLAN-02` Authorization, `PLAN-09` Shopping cart, `PLAN-10` Checkout/payment/wallet, `PLAN-11` Order lifecycle are the Phase-1 critical path (`../../13-testing/core/test-plans.md` L46). Their entry criteria (OTP mock adapter + SMS sandbox, RBAC matrix, cart fixtures, money boundary fixtures + ledger invariant harness, 17-state fixtures) are themselves Phase 1 deliverables.
- **Architecture-boundary work:** ADRs `ADR-001…ADR-010` are the accepted decision set (`18-decisions/core/`, index `04-architecture/core/architecture-decisions-reference.md`); ports/adapters for payment providers (`ADR-009`) keep the custody model swappable under `RISK-012`.
- **Money scope is conditional:** B07 payment/wallet build proceeds only if `DEP-10` yields a favourable or conditional written position (`mitigation-plans.md` RISK-012 kill criteria — adverse position stops B07 money-flow implementation).

**Dependencies consumed:** `DEP-01…DEP-04`, `DEP-07` (available), `DEP-05` (sandbox adapters + bank-transfer rail `INT-REQ-002` as guaranteed fallback), `DEP-06` (two-provider failover + WhatsApp fallback per `BR-NTF-03`), `DEP-11` (design assets for frontend), `DEP-10` (gates money scope); `ASM-15` (Arabic search spike in Phase 1); `GAP-05` must not leak into shipped commission behaviour before a decision record exists.

**Risks owned:** `RISK-001` (ledger integrity — implementation of append-only postings, single write path, `J1`/`J2` jobs, property tests), `RISK-006` (failover implementation), `RISK-003` (both adapters behind `PaymentProviderPort`, circuit breakers), `RISK-012` (no regulator/provider assumptions in domain code), `RISK-008` (query/index review, cache, pagination), `RISK-005` (Compose topology, observability, health/readiness gates).

**Evidence produced (→ Gate 1):** executed `PLAN-01…PLAN-18` ranges with evidence links on each TC; constraint-suite results; coverage report vs AC registry (80/95/90 floors, `AC-S-08`); `PERF-07` per-PR client performance and early k6 baselines; `SEC-P-01…SEC-P-09` scan reports; staged `J1`/`J2` with seeded-mismatch test; architecture conformance test (only `LedgerService` writes the ledger).

---

## 3. Phase 2 — Pilot & Hardening (staging, load tests, drills)

**Objective.** Prove the built system behaves under real load, real faults, real devices, and real users — and close the operational gaps that only appear under pressure.

**Entry criteria.** Gate 1 outcome = `PASS` (or `PASS WITH FINDINGS` with written dispositions); staging at parity with production image digests.

**Exit criteria — mapped to Gate 2:**

| # | Criterion | Canon |
|---|---|---|
| 1 | Load tests at target: p95 read < 200 ms / write < 500 ms at 10,000 concurrent for 30 min | `test-plans.md` §b PERF-01; `AC-S-05`; `C-25` |
| 2 | Drills all PASS: failover, webhook storm, Redis restart, queue stop, ES down, DR restore, replica kill, alert fire | `test-plans.md` §d CHAOS-01…08 |
| 3 | Production-readiness checklist rolled up (52 rows `DONE` or explicitly `WAIVED`) | `../../15-deployment/core/production-readiness.md` §8 |
| 4 | Compliance sign-off checklist complete for `AC-S-24` | `../../12-non-functional/core/compliance-and-legal.md` §5 |
| 5 | Launch-blocking gaps closed or explicitly waived with owner | `../../20-validation/core/missing-information.md` (GAP register) |
| 6 | Accessibility + localization + device-lab + migration/rollback plans exited | `test-plans.md` §e, §f, §g, §h |

**Content:**

- **Load & performance:** `PERF-01…PERF-06` on staging (k6), exit = all thresholds green on three consecutive runs; breach = CRITICAL (SLO) or HIGH.
- **Reliability drills:** `CHAOS-01…CHAOS-08`, including `CHAOS-06` DB failover/restore proving RTO ≤ 1 h / RPO ≤ 15 min with zero lost money (`AC-S-17`) and `CHAOS-08` alert fire drill (`AC-S-18`).
- **Rehearsals:** migration expand-contract, deploy rehearsal, rollback drill ≤ 15 min (`test-plans.md` §h; `AC-S-20`), seed/fixture re-baseline.
- **Usability/accessibility/locale:** axe sweeps ≥ 95% automated / 0 critical (`AC-S-10`), RTL visual regression with 0 defects (`AC-S-11`), keyboard-only and screen-reader passes, six localization checks green.
- **Mobile verification:** Maestro P0 smoke + push + carrier-real OTP on the `DEP-12` device lab (`test-plans.md` §g).
- **Pilot:** recruit and run **≥ 10 pilot vendors** through KYC → listing → sale → payout (`AC-S-21`); end-to-end money cycle audit top-up → order → escrow → commission → payout → refund (`AC-S-22`); support/dispute/code-lockout escalation process live (`AC-S-23`).
- **Hardening fixes:** security findings re-triaged (deferred items need written risk acceptance in `17-risk-management/core/risk-register.md`), performance regressions fixed, alert tuning to severity definitions.

**Dependencies consumed:** `DEP-05` production credentials path, `DEP-06` template approval + real-carrier drill, `DEP-09` legal opinions (blocking `AC-S-24`), `DEP-12` device lab, `DEP-08` (start — domains/TLS/CDN for public launch).

**Risks owned:** `RISK-001` (seeded-corruption drill detected within one run — `AC-S-14` unprovable otherwise; restore drill proving ledger replay; money-cycle audit), `RISK-008` (k6 at 1× and 2× target), `RISK-005` (runbooks for top 10 incidents `AC-S-19`, DR drill, rollback rehearsal), `RISK-002` (pilot recruitment, weekly feedback), `RISK-006` (real-carrier failover drill, approved templates), `RISK-012` (legal sign-off inputs, dry-run of bank-transfer fallback `BR-PAY-04`), `RISK-004` (`J5` reconciliation green).

**Evidence produced (→ Gate 2):** k6 reports; drill records; coverage and defect queries; UAT sign-off sheets per surface referencing plan IDs (`AC-S-04`); pilot report; production-readiness rollup (52 rows) with four signatures; compliance evidence pack; GAP closure records.

---

## 4. Launch (public availability)

**Objective.** Put the platform into public service with every authorization recorded — no gate is bypassed by schedule pressure.

**Entry criteria — Gate 2 `PASS` requires, at minimum:**

1. Production-readiness: **all 52 rows `DONE` or explicitly `WAIVED`**, plus sponsor, QA lead, security owner, and ops owner signatures (`../../15-deployment/core/production-readiness.md` §9).
2. Critical-path dependencies closed: `DEP-06` (registration), `DEP-10` (wallet legitimacy), `DEP-05` (production top-ups), `DEP-09` (legal sign-off), `DEP-08` (public launch) — ordering per `00-project-overview/dependencies.md`.
3. Money-path quality gates green and non-negotiable (`00-project-overview/stakeholders.md` conflicts table; `../../01-business-analysis/core/stakeholder-needs.md` STK-01).
4. `AC-S-24` legal/compliance sign-offs on file; unresolved blocking items (notably the Central Bank position) stop launch.

**Content:** go-live checklist entries per risk plan (payout batch enabled only after `J1`/`J2` green for 7 consecutive days; production SMS/WhatsApp credentials issued only after the sandbox suite passes; production dashboards + saturation alerts live before first traffic); on-call rotation sized to the team with escalation contacts tested; maintenance-mode and rollback paths verified.

**Risks owned:** `RISK-001` (payout-enablement condition), `RISK-006` (two active channels — launch without two channels is prohibited, no OTP bypass), `RISK-012` (launch only with a favourable or conditional opinion; conditions encoded as config + tests), `RISK-005` (on-call readiness), `RISK-008` (SLO dashboards before first traffic), `RISK-014` (launch infrastructure readiness — `DEP-08` domains, TLS, CDN).

**Evidence produced:** completed go-live checklist, alert inventory check (`AC-S-18`), first-week reconciliation reports.

---

## 5. Post-Launch (operation & review)

**Objective.** Keep the money correct, the SLOs honest, and the registers moving — then judge the outcome at Gate 3.

**Entry criteria.** Launch executed; monitoring and reconciliation jobs live (`J1`, `J2`, `J6`, `J5`, `J10` cadence per `../../16-data/core/data-quality.md` and the mitigation plans).

**Exit criteria — mapped to Gate 3:**

| # | Criterion | Canon |
|---|---|---|
| 1 | Availability evidence vs `AC-S-06` (99.99% over any rolling 30-day window) | `00-project-overview/success-criteria.md` |
| 2 | Residual CRITICAL items dispositioned: security findings, CRITICAL risks, open `GAP-*` | `../../09-security/core/security-findings.md`; `17-risk-management/core/risk-register.md` |
| 3 | Technical-debt register reviewed; every `TD-NN` has an owner and a decision | `technical-debt.md` |
| 4 | Assumptions re-scored against real data (`ASM-01`, `ASM-05`, `ASM-06`, `ASM-08`, `ASM-09`, plus `GAP-01` targets once set) | `00-project-overview/assumptions.md` |
| 5 | Monthly standing risk reviews and burndown produced; flat-by-construction honesty rule honored while pre-implementation | `../../17-risk-management/core/risk-review-process.md` §1, §8 |

**Content:** continuous RED metrics and quarterly load re-runs; monthly invariant attestation for the ledger; monthly provider performance review with a **second** SMS provider contract kept active; monthly ops review (alert volume, MTTR, manual steps); quarterly legal review and dependency/credential config review; cohort retention review and churn interviews; delta re-run of production readiness before any release that changes infrastructure, integrations, or compliance posture.

**Risks owned:** `RISK-001` (nightly `J1`/`J2`/`J10` forever, monthly attestation), `RISK-003` (`J6` daily, provider dashboards, quarterly commercial reviews), `RISK-004` (quarterly legal review), `RISK-005` (monthly ops review, simplify quarterly), `RISK-002` (cohort retention), `RISK-008` (quarterly load re-run), `RISK-011` (scope changes only through the gap/decision path), `RISK-024` (measurement against `GAP-01` targets once the sponsor sets them).

**Evidence produced (→ Gate 3):** SLO dashboards and incident records, reconciliation and attestation reports, monthly review minutes, updated registers (`ASM`, `GAP`, `TD`, `RISK`), production-readiness delta results.

---

## 6. Cross-Phase Rules

1. **Gates are blocking.** A `FAIL` outcome stops the transition; the sponsor may accept a gate-blocking risk only explicitly, in writing, recorded as a register status change (`risk-review-process.md` §4).
2. **The phase-gate risk check runs at every gate** (G-R1…G-R7) — embedded in `quality-gates.md`; this roadmap does not restate it.
3. **Money paths are non-negotiable.** Quality gates in money paths outrank schedule pressure (`stakeholders.md` L40; STK-01). Scope is cut instead of tests, monitoring, or backups (RISK-005 decision rule).
4. **Constraints outrank everything.** Any plan step that would violate `C-01…C-26` is void; conflicts are logged in `../../20-validation/core/contradiction-audit.md` (root README §9; `mitigation-plans.md` §9).
5. **No silent schedule invention.** Sequencing stays relative/conditional until `ASM-14` baselines land at Gate 0; estimates, dates, and sprint numbering are added only in downstream planning artifacts outside this knowledge base.
6. **Evidence flows forward, never backward.** Each phase's exit evidence becomes the next phase's entry assumption; nothing carries over unlinked.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 36,44,46,48 + charter pointer |
| 1.1 | 2026-09-30 | AC-registry count sync: 253 → **273 ACs** (`acceptance-criteria.md` v1.2) | Owner directive session 011 (`prompt-011.md` §4.7) — count consumer re-synced in same change set |
| 1.2 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
