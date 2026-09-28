---
document_id: DOC-PHA-016
title: Test Plan & Cases — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-TST-001, DOC-TST-003, DOC-TRC-003]
related_requirements: [AC-S-03, AC-S-09]
---

# Test Plan & Cases — analysis phase

- Phase: analysis · Rules version: ADMR `2.0.0` · Suites: unit/component/integration/system/UAT/perf/security
- Strategy (canonical): [`13-testing/testing-strategy.md`](../../13-testing/testing-strategy.md) · Registry: [`13-testing/test-cases/README.md`](../../13-testing/test-cases/README.md) (`TC-001`…`TC-114`) · Constraints: [`13-testing/constraint-tests.md`](../../13-testing/constraint-tests.md) (`TST-CON-01`…`26`)

## 1. Coverage mapping (TST-02)

| Function/component | Unit | Component | Integration | System | UAT | Perf | Security |
|---|---|---|---|---|---|---|---|
| Identity / OTP / session (`b01`) | `TC-*` unit tier | — | API tier | `TC-114` deny-by-default matrix | `AC-SR004-*` | `PERF-01` | `TC-105`–`TC-108`, `SEC-REQ-001` |
| Catalog / cart / checkout (`b02`–`b05`) | unit tier | — | `TC-104` coupon @ creation | `TST-CON-01…08`, `TST-CON-13…15` | `AC-FR*` | `PERF-02` | tampered-price / oversell negatives |
| Wallet / ledger / payments (`b07`) | money-math units | — | `TST-CON-02`…`07` | invariant suite (`PRF-05`) | `AC-FR*` | `PERF-03` | `TC-106`, `TC-109` |
| Orders / state machine (`b06`) | enum-count unit | — | `TST-CON-09` 17/17 matrix | `TC-111`, `TC-112` | `AC-FR012-*` | `PERF-04` | race + 409 tests |
| Delivery / code (`b08`) | hash unit | — | `TST-CON-16` | `TC-111` | `AC-SR005-*` | — | `SEC-REQ-005` negatives |
| Returns / disputes (`b09`) | refund-math units | — | `TST-CON-11`, `TST-CON-12` | `TC-112` | `AC-FR*` | — | audit assertions |
| Admin / settings / audit (`b13`) | — | — | `TC-110` precedence | `TC-109`, `TC-114` | `AC-SR010-*` | — | `TC-107` tamper chain |
| Health / ops | — | — | `TC-113` probes | chaos `CHAOS-01…08` | — | `PERF-05…07` | — |

Full AC → test matrix (277 rows): [`19-traceability/requirements-to-tests.md`](../../19-traceability/requirements-to-tests.md) — verdict `PASS WITH FINDINGS` (203 EXPLICIT / 42 DECLARED / 27 GAP / 5 operational).

## 2. Test cases

Canonical, full-detail cases live in `13-testing/test-cases/TC-001.md`…`TC-114.md` (114 files, locked total — never renumbered, `SPE-05`). Constraint tests: `TST-CON-01`…`TST-CON-26` (wallet-only, 17-state, return window, code confirm, cart limits, etc.).

## 3. Execution results

- **Executed: 0.** No source tree exists (phase 0 is documentation-only) → `jest --coverage --ci`, Playwright, k6, axe, ZAP are all **BLOCKED** pending Phase 1 bootstrap.
- Coverage report: **not generated** — target when running: overall ≥80%, critical paths 100% (`DOD-04`; adapter floors `b07` ≥95%, `b01` ≥90% are *looser* than the 100%-critical gate — the stricter applies unless the user approves the project numbers in writing, `RULES_HINTS.md` §6).
- Command binding status: `test:all`, dead-element scan, `k6 run`, i18n key scan are **NOT DOCUMENTED** → `BLOCKED` (core/00 §0.6); Phase 1 checklist item 2.

## 4. Bug register (TST-05)

| ID | Severity | Root cause | Fix | Regression test |
|---|---|---|---|---|
| — | — | No code executed → no defects found yet | — | — |

## Status
**PLAN COMPLETE · EXECUTION BLOCKED** (reason: no implementation exists). Reporting this as anything else would violate GEN-03/DOD-10.

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 14 / TST-01, session 005) | analysis-agent |
