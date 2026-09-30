---
document_id: DOC-CMP-001
title: 21 Completion — Domain Overview, Register & Precedence Rules
category: 21-completion
status: approved
version: 1.0
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-ROOT-001, DOC-OVR-003, DOC-OVR-009, DOC-OVR-011, DOC-TST-001, DOC-TST-003, DOC-RSK-003, DOC-RSK-004, DOC-BA-006, DOC-UX-001]
---

# 21 — Completion

**This domain closes the analysis.** Every other domain in `docs/` states what the system is, what it must do, and how it will be built; this domain states **how we will know it is done**. The governing methodology for the whole repository is *completion = verified completion* (`00-project-overview/success-criteria.md`, root README §10 items 36/44/46/48): nothing is complete because it was asserted — it is complete when evidence exists, is linked, and has been reviewed at a gate.

Scope of this domain:

1. **Delivery sequencing** — how work proceeds through phases and how test plans attach to that sequencing.
2. **Quality gates** — the entry/exit evidence system every other domain feeds.
3. **Assessment artifacts** — feasibility, technical debt, recommendations.
4. **Final acceptance** — the sign-off that turns `PENDING` into `ACCEPTED`.

---

## 1. File Register

Eight files are authored in this domain. The document-ID series `DOC-CMP-NNN` is allocated here (single allocator rule, root README §5 pattern).

| File | Document ID | Purpose | Source of truth |
|---|---|---|---|
| `21-completion/README.md` | `DOC-CMP-001` | Domain overview, register, precedence rules, relationship to `20-validation/` | yes |
| `core/implementation-roadmap.md` | `DOC-CMP-002` | Phased delivery plan (Phase 0 → Post-launch) — **delivery-model authority** | yes |
| `core/roadmap.md` | `DOC-CMP-003` | Sprint-cadence view derived for test planning — narrow, derived | no (derived from `DOC-CMP-002`) |
| `core/quality-gates.md` | `DOC-CMP-004` | Gate system: Gate 0 … Gate 3, evidence, participants, outcomes | yes |
| `core/feasibility-assessment.md` | `DOC-CMP-005` | Feasibility across six dimensions with conditions (root README §10 item 36) | yes |
| `core/technical-debt.md` | `DOC-CMP-006` | Debt register `TD-NN` (root README §10 item 44) | yes |
| `core/recommendations.md` | `DOC-CMP-007` | Prioritized recommendations `REC-NN` (root README §10 item 46) | yes |
| `core/final-acceptance.md` | `DOC-CMP-010` | Acceptance checklist `AC-S-01…AC-S-24`, sign-off, procedure (root README §10 item 48) | yes |

**Unused IDs:** `DOC-CMP-008` and `DOC-CMP-009` are **not allocated to any file** and must never be cited — citing them is a consistency-audit defect. The gap in the series is deliberate; IDs are never reused or back-filled (root README §5 discipline). The next free ID in this domain is `DOC-CMP-011`.

**Series minted in this domain:** `TD-NN` (technical debt, defined and allocated in `core/technical-debt.md`) and `REC-NN` (recommendations, defined and allocated in `core/recommendations.md`). No `FR`/`TC`/`BR`/`RISK`/`ASM`/`DEP`/`GAP`/`AC` ID is ever minted here — this domain only cites IDs that already exist in their owning registers.

---

## 2. Phases & Gates (overview)

Phase vocabulary is owned by `../17-risk-management/core/mitigation-plans.md` (§Phase vocabulary); gates themselves are defined in `core/quality-gates.md`.

```text
 PHASE 0              PHASE 1             PHASE 2              LAUNCH          POST-LAUNCH
 pre-implementation   core build          pilot & hardening    public          operation & review
 (no product code)    (blocks B01…B13)    (staging, load,      availability    (SLOs, review)
       │                   │               drills, pilot)
       │                   │                   │                  │                │
       ▼                   ▼                   ▼                  ▼                ▼
   Gate 0  ──────────►  Gate 1  ───────────►  Gate 2  ────────► go-live ───────► Gate 3
 sponsor owns         build exit            launch readiness                  post-launch
 (baselines,          (test evidence,       (production-readiness,            review (SLOs,
  dangerous ASMs,      money-path green,     compliance sign-offs,            residual CRITICALs,
  DEP-05/06,           coverage vs ACs,      GAP closure for                  debt register)
  GAP triage,          k6 vs NFRs,           launch blockers)
  analysis sign-off)   security triage)
       │                   │                   │                  │                │
       └───────────────────┴───────────────────┴──────────────────┴────────────────┘
                    every gate runs the phase-gate risk checklist
                    (17-risk-management/risk-review-process.md §7, G-R1…G-R7)
                    and records the outcome: PASS · PASS WITH FINDINGS · FAIL
```

Feeds into the gates:

- **Test evidence** — `../13-testing/core/test-plans.md` (PLAN-01…PLAN-18, performance, security, chaos, accessibility, localization, device-lab, migration plans) → gate evidence.
- **Risk checks** — `../17-risk-management/core/risk-review-process.md` §7 checklist runs at every gate.
- **Design completeness** — `11-ui-ux/README.md` §7 design gate "feeds `core/quality-gates.md`".
- **Operational readiness** — `../15-deployment/core/production-readiness.md` (52 checklist rows) → Gate 2.
- **Compliance evidence** — `../12-non-functional/core/compliance-and-legal.md` §5 sign-off checklist → `AC-S-24` → Gate 2.
- **Audit findings** — `20-validation/` (see §4).

---

## 3. Precedence Rule (two roadmap files)

This domain holds two differently-scoped sequencing documents. Both exist on purpose; they serve different consumers.

| | `core/implementation-roadmap.md` | `core/roadmap.md` |
|---|---|---|
| Document ID | `DOC-CMP-002` | `DOC-CMP-003` |
| Question answered | What is the delivery model — phases, entry/exit criteria, dependencies, risks owned, evidence produced? | How do test plans execute per sprint against those phases? |
| Cited by | `00-project-overview/project-charter.md` ("Delivery model — Phased (see `core/implementation-roadmap.md`)") | `../13-testing/core/test-plans.md` ("plans execute per sprint against `core/roadmap.md`") |
| Scope | Full authority: phases, gates mapping, dependencies, risks, evidence | Narrow: sprint-cadence checklist; sizing/schedule detail is deliberately out of scope |
| Status | **Authoritative** | **Derived** |

**Conflict rule:** on any conflict between the two files — phase naming, ordering, gate mapping, or what a phase contains — **`core/implementation-roadmap.md` wins**. `core/roadmap.md` is a view over it and must be regenerated from it after any change (change-management propagation, root README §9).

Neither file contains calendar dates, effort estimates, or sprint counts: schedule, staffing, and budget baselines are `INSUFFICIENT EVIDENCE` until the sponsor sets them at Gate 0 (`ASM-14`, `00-project-overview/assumptions.md`).

---

## 4. Relationship to `20-validation/`

| Direction | What moves |
|---|---|
| `20-validation/` → gates | Audit findings are **standing input** to every gate: `../20-validation/core/critical-findings.md` (open critical items must be dispositioned), `../20-validation/core/missing-information.md` (owns `GAP-NNN` — triaged at Gate 0, launch blockers closed at Gate 2), `../20-validation/core/contradiction-audit.md` (unreconciled citations block the gate that owns them), `../20-validation/core/consistency-audit.md` (register hygiene check G-R6) |
| gates → `20-validation/` | Gate outcomes are recorded in the gate document and mirrored to `../20-validation/core/analysis-validation.md` where applicable (`../17-risk-management/core/risk-review-process.md` §7) |
| `core/final-acceptance.md` ↔ `../20-validation/core/analysis-validation.md` | Root README §10 item 48 pairs them: the final quality assessment must read **PASS** or **PASS WITH FINDINGS** before acceptance can move from `PENDING` to `ACCEPTED` |
| `core/quality-gates.md` ↔ `17-risk-management/` | The phase-gate risk check (`risk-review-process.md` §7) is embedded in every gate; a gate-blocking risk unresolved means the gate does not pass |

> **Evidence status (`INSUFFICIENT EVIDENCE`):** the directories `19-traceability/` and `20-validation/` are declared in root README §2 and referenced throughout the corpus, but they are **not present in `docs/` as authored**. Every reference to them in this domain is a path reference to the canonical home, not a citation to content. Authoring them is recorded as `TD-10` in `core/technical-debt.md` and as a recommendation in `core/recommendations.md`; the gap is also reported for external editing.

---

## 5. How to Use This Domain

| Reader | Start with |
|---|---|
| Sponsor / product owner | `core/quality-gates.md` (Gate 0) → `core/final-acceptance.md` |
| Delivery / engineering | `core/implementation-roadmap.md` → `core/roadmap.md` |
| QA lead | `core/roadmap.md` → `../13-testing/core/test-plans.md` → `core/quality-gates.md` (Gate 1) |
| Anyone asking "is it ready?" | `core/feasibility-assessment.md` → `core/recommendations.md` → `core/final-acceptance.md` |
| Anyone inheriting unfinished work | `core/technical-debt.md` |

Evidence discipline for every file here: statements carry `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE` tags; gate outcomes use only `PASS · PASS WITH FINDINGS · FAIL`; findings use `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`; and no statement invents an ID or a `file:line` reference that has not been checked against `docs/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 36,44,46,48 + charter pointer |
