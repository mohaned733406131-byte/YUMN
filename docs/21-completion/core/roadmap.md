---
document_id: DOC-CMP-003
title: Roadmap — Sprint-Cadence View for Test Planning
category: 21-completion
status: approved
version: 1.0
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-005]
related_documents: [DOC-CMP-002, DOC-CMP-004, DOC-TST-003, DOC-TST-001, DOC-OVR-009]
---

# Roadmap — Sprint-Cadence View

A **short, derived** file. It answers one question only: *how do the executable test plans attach to delivery cadence?* Everything else about sequencing lives in the delivery-model authority, `implementation-roadmap.md`.

**Derived from:** `implementation-roadmap.md` (phase vocabulary, entry/exit criteria, gate mapping).
**Consumer:** `../../13-testing/core/test-plans.md` cites this file.
**Precedence:** on any conflict — phase names, ordering, what a phase contains, gate mapping — **`implementation-roadmap.md` wins**; this file is regenerated from it (`21-completion/README.md` §3).

---

## 1. What the test domain promises (and what it does not)

From `../../13-testing/core/test-plans.md` L46, quoted verbatim:

> **Schedule pointer:** plans execute per sprint against `roadmap.md`; PLAN-01/02/09/10/11 are Phase-1 critical path. Sizing and sequencing detail: sprint test plan appendix maintained in CI, not in docs.

That sentence fixes this file's scope:

| In scope here | Deliberately NOT here |
|---|---|
| Which plans execute against which phase, and in what priority | Sprint counts, sprint lengths, calendar dates |
| The Phase-1 critical-path plan set (`PLAN-01`, `PLAN-02`, `PLAN-09`, `PLAN-10`, `PLAN-11`) | Sizing, estimates, staffing, budget — all `INSUFFICIENT EVIDENCE` (`ASM-14`) |
| Per-sprint-category entry/exit checklist tied to the phase gate | Task-level sequencing, story breakdown, assignment |
| Pointer to where cadence detail actually lives (the sprint test plan appendix, maintained in CI) | Duplicate copies of that detail (it never enters `docs/`) |

No sprint number is invented here: cadence detail is an operational artifact owned by the delivery team in CI, not a knowledge-base artifact. `ASM-14` baselines set at Gate 0 (`00-project-overview/assumptions.md`) are what make real sprint planning possible at all.

---

## 2. Plan-to-phase alignment

| Phase (from `implementation-roadmap.md`) | Plans executing | Cadence rule | Gate that consumes the evidence |
|---|---|---|---|
| Phase 0 — pre-implementation | None (nothing to execute) | Plan entry criteria are prepared: fixtures spec (`DOC-TST-005`), environments, harnesses (ledger invariant, clock-shift, timer injection) | Gate 0 |
| Phase 1 — core build | `PLAN-01`, `PLAN-02`, `PLAN-09`, `PLAN-10`, `PLAN-11` first (critical path), then `PLAN-03…PLAN-08`, `PLAN-12…PLAN-18` as their ranges become executable; `PERF-07` per PR; `SEC-P-01…SEC-P-03`, `SEC-P-05`, `SEC-P-07`, `SEC-P-08` per PR | Each sprint-category window runs the plans whose range is executable under the common entry criteria (stable FR + ACs, healthy environment, seeded fixtures, TCs `READY`) | Gate 1 |
| Phase 2 — pilot & hardening | `PERF-01…PERF-06`, `CHAOS-01…CHAOS-08`, accessibility §e, localization §f, device-lab §g, migration/rollback §h, per-release-candidate UAT (`AC-S-04`) | Fixed cadence from the plans themselves (weekly performance, integration-cadence chaos, nightly staging drills, per-release-candidate device and UAT passes) — expressed relative to the release, never as an absolute date | Gate 2 |
| Launch | Pre-release re-runs of performance, security DAST, rollback and deploy rehearsal | Before every release candidate | Gate 2 outcome authorizes go-live |
| Post-launch | Continuous: regression suite per change, `PERF-07`, `SEC-P-01…04`, scheduled drills (`CHAOS-06` quarterly and pre-launch), quarterly load re-run | Ongoing operational cadence | Gate 3 |

**Common exit criteria for every plan window** (`../../13-testing/core/test-plans.md` §a): all TCs in range executed, P0/P1 100% PASS, 0 CRITICAL/HIGH open, evidence links added to the TCs, `19-traceability/` updated.

---

## 3. Per-Sprint-Category Checklist Template

One row per cadence category; the team fills it every window. Entry and exit are inherited from the phase gate, so a category cannot exit without its gate accepting the evidence.

| Sprint category | Entry (all must hold) | Evidence to collect in-window | Exit (all must hold) | Gate fed |
|---|---|---|---|---|
| Phase-0 preparation | Analysis approved; environments and fixture specs available | Harness/fixture readiness notes; contract and opinion records as they arrive | Gate 0 checklist complete (`quality-gates.md`) | Gate 0 |
| Build window (Phase 1) | Previous category exited; FR + ACs stable for the range; TCs `READY`; fixtures seeded | Plan results for the range, coverage delta vs AC registry, constraint-test results, PR-level scan results | Common plan exit (P0/P1 100% PASS, 0 CRITICAL/HIGH) and Gate 1 checklist complete | Gate 1 |
| Hardening window (Phase 2) | Gate 1 outcome recorded; staging at parity with production image digests | k6 reports, drill records, a11y/localization reports, UAT sheets, defect query | Plan §b–§h exits green; production-readiness rows advancing; Gate 2 checklist complete | Gate 2 |
| Release-candidate window | Release candidate built; rollback script tested at least once | Deploy rehearsal, rollback drill, DAST, device-lab pass, UAT sign-off | 0 customer-visible errors; rollback timing recorded; release evidence filed | Gate 2 (pre-launch) |
| Operations window (post-launch) | Launch executed; monitoring and reconciliation live | Regression results, scheduled drills, reconciliation reports, SLO dashboards | Gate 3 checklist complete; no unreviewed CRITICAL residual | Gate 3 |

**Reporting rule:** each window's outcome is recorded as `PASS · PASS WITH FINDINGS · FAIL` against the gate it feeds, with findings severity-classified `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`. `FAIL` on a category does not renegotiate the phase — it blocks the phase exit.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 36,44,46,48 + charter pointer |
