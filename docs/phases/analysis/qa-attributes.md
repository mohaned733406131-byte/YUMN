---
document_id: DOC-PHA-010
title: QA File (quality attributes met) — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-TST-001, DOC-TST-002, DOC-PHA-014]
related_requirements: []
---

# QA File (quality attributes) — analysis phase

## Purpose
CORE-03 item 8 / `TST-04`: each quality attribute with a **metric and a result**. Results are stated honestly for a documentation-only phase: *designed and specified = met; executed = BLOCKED* (DOD-10).

## Scope
The seven QA attributes for phase 0 deliverables (knowledge base + rule system), plus their projected verification for later phases.

## QA attributes

| # | Attribute | Metric (target) | Result at phase 0 | Verification vehicle |
|---|---|---|---|---|
| 1 | **Correctness** | 0 broken links; every ID resolves; registries reconcile (68 req / 99 BR / 253 AC / 114 TC / 26 constraint tests) | **MET** — validator `markdown links (0 broken)`; sweeps in `20-validation/` | `validate.py`, consistency audit `CHK` series |
| 2 | **Reliability** | Reproducible resume from `session_track.md` + session files (SES-05); 0 flakes (later) | **MET for docs** — sessions 001–004 now reconstructible from `docs/sessions/` | SES-01/02/05 |
| 3 | **Usability** | WCAG 2.1 AA, ≥95% automated pass, 0 serious axe findings | **DESIGNED only** — spec in `11-ui-ux/`, `12-non-functional/accessibility.md`; BLOCKED until UI exists | axe-core + Lighthouse CI |
| 4 | **Performance** | p95 read <200 ms / write <500 ms; LCP <2.5 s; 10k concurrent | **BLOCKED** — k6 invocation not yet bound (bootstrap item) | k6 `PERF-01…07` on staging |
| 5 | **Security** | 0 open CRITICAL/HIGH findings; 0 secrets in repo | **NOT MET (design)** — `SEC-001…015` all OPEN (1 CRITICAL, 4 HIGH); secrets scan clean (no `.env`/keys in tree, `.gitignore` correct), gitleaks binary unavailable → scan BLOCKED | `docs/09-security/security-findings.md`, `gitleaks detect --redact --no-banner` |
| 6 | **Maintainability** | Module boundaries enforceable by lint; one source of truth per concept (`SPE-01`) | **MET for docs** — `SPE-01` reference-not-copy sweep; boundary lint = Phase 1 command binding | `eslint . --max-warnings=0` (module-boundary rules) |
| 7 | **Portability** | Compose-only, single-host reproducibility (`C-22`) | **DESIGNED** — `14-devops-infrastructure/docker-compose.md`; `docker compose config -q` BLOCKED (no compose file yet) | compose render + Trivy |

## Preconditions
Gate 0 (sponsor sign-off, `ASM-14`, `DEP-05/06`) before any attribute moves from DESIGNED → EXECUTED.

## Postconditions
Phase closes with attribute rows 1, 2, 6 MET; 3, 4, 5, 7 explicitly BLOCKED/NOT MET with the owning gate named.

## Open questions (COM-01)
1. Security attribute cannot reach MET until `SEC-011` (auth channel) and the four HIGH findings are resolved — owners and ETAs needed (sponsor item).

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 8 / TST-04, session 005) | analysis-agent |
