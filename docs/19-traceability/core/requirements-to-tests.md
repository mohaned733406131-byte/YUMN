---
document_id: DOC-TRC-003
title: Requirements to Tests — Requirement → Acceptance Criterion → Test Artifact Matrix
category: 19-traceability
status: approved
version: 1.5
created: 2026-09-27
updated: 2026-09-29
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-019, FR-020, NFR-009, SEC-REQ-012, DATA-REQ-002, INT-REQ-002]
related_documents: [DOC-TRC-001, DOC-TRC-002, DOC-AC-001, DOC-OVR-011, DOC-TST-001, DOC-TST-002, DOC-TST-003, DOC-TST-004, DOC-TST-005, DOC-TST-006, DOC-INT-008]
---

# 19 — Requirements to Tests

**The requirement → acceptance criterion → test-artifact matrix.** One row per acceptance criterion (277), one row per constraint (26), and the history of the test cases the corpus once declared but did not contain (§5 — all present since 2026-09-27). This is the document `02-requirements/acceptance-criteria.md` §7 and `00-project-overview/success-criteria.md` `AC-S-03` point at when they claim "requirement → AC → TC with zero gaps".

**It does not claim zero gaps.** It reports what is linked, what is merely declared, and what is missing.

---

## 1. Scope & Method

**AC universe — 277 rows:**

| Family | IDs | Count | Defined in |
|---|---|---|---|
| Functional | `AC-FR001-01 … AC-FR020-04` | 94 | `02-requirements/acceptance-criteria.md` §1 |
| Non-functional | `AC-NFR-001-01 … AC-NFR-020-02` | 40 | §2 |
| Security | `AC-SR001-01 … AC-SR012-04` | 50 | §3 |
| Data | `AC-DR001-01 … AC-DR008-04` | 32 | §4 |
| Integration | `AC-IR001-01 … AC-IR008-04` | 33 | §5 |
| Cross-cutting scenarios | `AC-XCUT-01 … AC-XCUT-04` | 4 | §6 |
| Success criteria | `AC-S-01 … AC-S-24` | 24 | `00-project-overview/success-criteria.md` |

**Test-artifact universe scanned (nothing else counts as an artifact):**

| Artifact class | IDs found | Source |
|---|---|---|
| Test cases | 114 files `TC-001 … TC-114` (locked allocation fully present) | `13-testing/test-cases/TC-*.md` §*Related requirements & rules* |
| Executable feature plans | `PLAN-01 … PLAN-18` | `../../13-testing/core/test-plans.md` §a |
| Performance / security / chaos activities | `PERF-01…07`, `SEC-P-01…09`, `CHAOS-01…08` | `../../13-testing/core/test-plans.md` §b–§d |
| Plan sections | `§b … §h` (scope + canon columns) | `../../13-testing/core/test-plans.md` |
| Constraint tests | `TST-CON-01 … TST-CON-26` | `../../13-testing/core/constraint-tests.md` |
| Test documents | `DOC-TST-001`, `DOC-TST-002`, `DOC-TST-005`, `DOC-INT-008` | `13-testing/README.md`, `testing-strategy.md`, `test-data-and-environments.md`, `../../10-integrations/core/testing-and-sandboxes.md` |

**Link status per row:**

| Status | Meaning |
|---|---|
| `EXPLICIT` | The artifact itself names the AC (`VERIFIED`) |
| `DECLARED` | Only an allocation/scope statement covers it: the locked TC-block table, a plan's scope line, or a strategy statement (`INFERENCE`) |
| `GAP` | No artifact and no declaration anywhere in the scanned set (`INSUFFICIENT EVIDENCE`) |
| `OPERATIONAL EVIDENCE` | Provable only by an operational/pilot/audit record, never by a test artifact — tracked in `21-completion/` |

Rules obeyed: shorthand citations are expanded conservatively (`AC-SR011-01/02` → both IDs; `AC-NFR-013-01/02` → both; `AC-FR009-01…04` → the range); a row is never marked `EXPLICIT` on the strength of another document's opinion about a test; and no test result (`PASS`/`FAIL`/executed) is claimed anywhere — every `TST-CON-NN` is `DESIGNED`, and execution evidence belongs to `21-completion/quality-gates.md`.

---

## 2. Coverage Summary

| AC family | Total | EXPLICIT | DECLARED only | GAP | Operational (non-test evidence) |
|---|---|---|---|---|---|
| FR | 94 | 86 | 8 | 0 | 0 |
| NFR | 40 | 29 | 5 | 6 | 0 |
| SEC | 50 | 31 | 19 | 0 | 0 |
| DATA | 32 | 10 | 6 | 16 | 0 |
| INT | 33 | 27 | 1 | 5 | 0 |
| XCUT | 4 | 4 | 0 | 0 | 0 |
| SUCCESS | 24 | 16 | 3 | 0 | 5 |
| **Total** | **277** | **203** | **42** | **27** | **5** |

**Verdict: `PASS WITH FINDINGS`.**

- Every one of the 68 requirements and all 277 ACs has a row; nothing is omitted.
- All 20 FRs have ≥1 test case of their own (the `FR-003` family rides the `TC-001–010` block, as `../../13-testing/test-cases-index.md` §2 states), so `AC-S-03`'s "≥1 test case per FR" half holds at design level.
- The **"0 gaps" half of `AC-S-03` does not hold**: 27 ACs have no artifact link and 42 more are covered only by a declaration.
- **Nothing has been executed**: 114/114 test-case files exist, all constraint tests are `DESIGNED`, and no report, dashboard or drill record exists in the corpus.

---

## 3. Matrix C — Acceptance Criterion → Test Artifact

Columns: `AC` · `Requirement` (parent ID) · `Test artifact(s)` · `Link basis` (what was read) · `Status`.

| AC | Requirement | Test artifact(s) | Link basis | Status |
|---|---|---|---|---|
| AC-DR001-01 | DATA-REQ-001 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-DR001-02 | DATA-REQ-001 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-DR001-03 | DATA-REQ-001 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-DR001-04 | DATA-REQ-001 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-DR002-01 | DATA-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR002-02 | DATA-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR002-03 | DATA-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR002-04 | DATA-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR003-01 | DATA-REQ-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR003-02 | DATA-REQ-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR003-03 | DATA-REQ-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR003-04 | DATA-REQ-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR004-01 | DATA-REQ-004 | scope: test-plans.md §d | plan scope declaration — test-plans.md §d | DECLARED |
| AC-DR004-02 | DATA-REQ-004 | scope: test-plans.md §d | plan scope declaration — test-plans.md §d | DECLARED |
| AC-DR004-03 | DATA-REQ-004 | scope: test-plans.md §d | plan scope declaration — test-plans.md §d | DECLARED |
| AC-DR004-04 | DATA-REQ-004 | scope: test-plans.md §d | plan scope declaration — test-plans.md §d | DECLARED |
| AC-DR005-01 | DATA-REQ-005 | §h | plan section — test-plans.md §h | EXPLICIT |
| AC-DR005-02 | DATA-REQ-005 | scope: test-plans.md §h | plan scope declaration — test-plans.md §h | DECLARED |
| AC-DR005-03 | DATA-REQ-005 | §h | plan section — test-plans.md §h | EXPLICIT |
| AC-DR005-04 | DATA-REQ-005 | scope: test-plans.md §h | plan scope declaration — test-plans.md §h | DECLARED |
| AC-DR006-01 | DATA-REQ-006 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR006-02 | DATA-REQ-006 | TC-064 | TC file — Related requirements & rules | EXPLICIT |
| AC-DR006-03 | DATA-REQ-006 | TC-064 | TC file — Related requirements & rules | EXPLICIT |
| AC-DR006-04 | DATA-REQ-006 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR007-01 | DATA-REQ-007 | TC-064 | TC file — Related requirements & rules | EXPLICIT |
| AC-DR007-02 | DATA-REQ-007 | TC-064 | TC file — Related requirements & rules | EXPLICIT |
| AC-DR007-03 | DATA-REQ-007 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR007-04 | DATA-REQ-007 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR008-01 | DATA-REQ-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR008-02 | DATA-REQ-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR008-03 | DATA-REQ-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-DR008-04 | DATA-REQ-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-FR001-01 | FR-001 | TC-001, TST-CON-06 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR001-02 | FR-001 | TC-004, TC-005 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR001-03 | FR-001 | TC-006 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR001-04 | FR-001 | TC-007 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR001-05 | FR-001 | DOC-TST-005, TC-002, TC-003 | TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR002-01 | FR-002 | §c, PLAN-02, SEC-P-05, TC-011 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-FR002-02 | FR-002 | §c, PLAN-02, SEC-P-05, TC-012 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-FR002-03 | FR-002 | §c, PLAN-02, SEC-P-05, TC-013 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-FR002-04 | FR-002 | §c, PLAN-02, SEC-P-05, TC-107, TC-109, TC-110 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-FR002-05 | FR-002 | §c, PLAN-02, SEC-P-05, TC-014, TC-114 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-FR003-01 | FR-003 | DOC-TST-006 §4; TC-001–010 (shared) | allocation declaration — 13-testing/test-cases/README.md §4; TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR003-02 | FR-003 | TC-008, TC-009 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR003-03 | FR-003 | TC-010 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR003-04 | FR-003 | DOC-TST-006 §4; TC-001–010 (shared) | allocation declaration — 13-testing/test-cases/README.md §4; TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR003-05 | FR-003 | DOC-TST-006 §4; TC-001–010 (shared) | allocation declaration — 13-testing/test-cases/README.md §4; TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR004-01 | FR-004 | TC-015 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR004-02 | FR-004 | TC-015 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR004-03 | FR-004 | TC-016 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR004-04 | FR-004 | TC-016 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR004-05 | FR-004 | TC-015, TC-017 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR005-01 | FR-005 | §b, PERF-04, TC-019, TST-CON-13 | constraint register — constraint-tests.md; plan activity — test-plans.md §b; plan section — test-plans.md §b; TC file — Related requirements & rules | EXPLICIT |
| AC-FR005-02 | FR-005 | TC-020, TST-CON-13 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR005-03 | FR-005 | TST-CON-13 | constraint register — constraint-tests.md | EXPLICIT |
| AC-FR005-04 | FR-005 | TC-018–020 | TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR006-01 | FR-006 | TC-021 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR006-02 | FR-006 | TC-021 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR006-03 | FR-006 | TC-021 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR006-04 | FR-006 | TC-022 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR006-05 | FR-006 | TC-022 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR007-01 | FR-007 | TC-024 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR007-02 | FR-007 | TC-023 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR007-03 | FR-007 | TC-023–024 | TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR007-04 | FR-007 | TC-024 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR008-01 | FR-008 | TC-025–026 | TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR008-02 | FR-008 | TC-026 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR008-03 | FR-008 | TC-025 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR008-04 | FR-008 | TC-025, TST-CON-17 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR008-05 | FR-008 | TC-026 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR009-01 | FR-009 | DOC-TST-002, DOC-TST-005, PLAN-08, TC-027 | executable plan row — test-plans.md §a; TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md; test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-FR009-02 | FR-009 | DOC-TST-005, PLAN-08, TC-027 | executable plan row — test-plans.md §a; TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR009-03 | FR-009 | §b, §d, CHAOS-05, PERF-03, PLAN-08, TC-028 | executable plan row — test-plans.md §a; plan activity — test-plans.md §b; plan activity — test-plans.md §d; plan section — test-plans.md §b; plan section — test-plans.md §d; TC file — Related requirements & rules | EXPLICIT |
| AC-FR009-04 | FR-009 | PLAN-08, TC-028 | executable plan row — test-plans.md §a; TC file — Related requirements & rules | EXPLICIT |
| AC-FR009-05 | FR-009 | TC-027–028 | TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR010-01 | FR-010 | DOC-TST-005, TC-029, TST-CON-15 | constraint register — constraint-tests.md; TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR010-02 | FR-010 | DOC-TST-005, TC-029, TST-CON-15 | constraint register — constraint-tests.md; TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR010-03 | FR-010 | TC-030 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR010-04 | FR-010 | TC-030 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR010-05 | FR-010 | TC-030 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR011-01 | FR-011 | DOC-TST-005, TC-033, TST-CON-14 | constraint register — constraint-tests.md; TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR011-02 | FR-011 | §b, PERF-04, TC-039, TC-042, TC-054, TC-104 | plan activity — test-plans.md §b; plan section — test-plans.md §b; TC file — Related requirements & rules | EXPLICIT |
| AC-FR011-03 | FR-011 | TC-032, TC-041 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR011-04 | FR-011 | TC-034, TC-040, TC-057, TST-CON-10 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR011-05 | FR-011 | TC-032, TST-CON-01 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR012-01 | FR-012 | TC-043, TST-CON-09 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR012-02 | FR-012 | TC-047, TC-052 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR012-03 | FR-012 | TC-046, TC-052 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR012-04 | FR-012 | TC-043, TC-049 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR012-05 | FR-012 | TC-043, TC-044, TC-045, TC-048, TC-050, TC-051, TC-053, TC-055, TC-056 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR013-01 | FR-013 | DOC-TST-005, TC-031, TC-037 | TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR013-02 | FR-013 | TC-035 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR013-03 | FR-013 | TC-032 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR013-04 | FR-013 | TC-032 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR013-05 | FR-013 | TC-031, TC-036, TC-038, TC-057 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR014-01 | FR-014 | TC-058, TST-CON-12 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR014-02 | FR-014 | TC-061, TST-CON-12 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR014-03 | FR-014 | TC-059, TC-060 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR014-04 | FR-014 | DOC-TST-006 §4; TC-057–064 | allocation declaration — 13-testing/test-cases/README.md §4; TC block declaration — 13-testing/test-cases/README.md §2/§4 | DECLARED |
| AC-FR014-05 | FR-014 | TC-063 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR015-01 | FR-015 | TC-065 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR015-02 | FR-015 | TC-068, TC-069, TC-070, TC-072, TST-CON-16 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR015-03 | FR-015 | TC-071, TST-CON-16 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR015-04 | FR-015 | TC-066, TC-067 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR015-05 | FR-015 | TC-073, TST-CON-16 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR016-01 | FR-016 | TC-062, TC-074, TC-075, TST-CON-11 | constraint register — constraint-tests.md; TC file — Related requirements & rules | EXPLICIT |
| AC-FR016-02 | FR-016 | TC-062, TC-076, TC-078 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR016-03 | FR-016 | TC-079 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR016-04 | FR-016 | TC-062, TC-080 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR017-01 | FR-017 | TC-084, TC-089 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR017-02 | FR-017 | TC-085 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR017-03 | FR-017 | TC-086 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR017-04 | FR-017 | TC-087 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR017-05 | FR-017 | TC-085, TC-088 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR018-01 | FR-018 | TC-090, TC-091, TC-094 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR018-02 | FR-018 | TC-064, TC-090, TC-091, TC-093, TC-094, TC-095 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR018-03 | FR-018 | TC-092, TC-093 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR018-04 | FR-018 | TC-095 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR019-01 | FR-019 | DOC-TST-005, TC-101 | TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR019-02 | FR-019 | DOC-TST-005, TC-100 | TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR019-03 | FR-019 | DOC-TST-005, TC-100, TC-102, TC-104 | TC file — 
Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-FR019-04 | FR-019 | TC-096, TC-097, TC-098, TC-099, TC-103 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR020-01 | FR-020 | TC-060, TC-077, TC-082, TC-083, TC-096, TC-097, TC-098, TC-102, TC-109, TC-110 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR020-02 | FR-020 | TC-071, TC-111 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR020-03 | FR-020 | TC-061, TC-081, TC-082, TC-112 | TC file — Related requirements & rules | EXPLICIT |
| AC-FR020-04 | FR-020 | TC-060, TC-110 | TC file — Related requirements & rules | EXPLICIT |
| AC-IR001-01 | INT-REQ-001 | DOC-INT-008, TST-CON-05 | constraint register — constraint-tests.md; test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR001-02 | INT-REQ-001 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR001-03 | INT-REQ-001 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR001-04 | INT-REQ-001 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR001-05 | INT-REQ-001 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR002-01 | INT-REQ-002 | TST-CON-05 | constraint register — constraint-tests.md | EXPLICIT |
| AC-IR002-02 | INT-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-IR002-03 | INT-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-IR002-04 | INT-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-IR003-01 | INT-REQ-003 | §d, CHAOS-01, DOC-INT-008 | plan activity — test-plans.md §d; plan section — test-plans.md §d; test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR003-02 | INT-REQ-003 | §d, CHAOS-01, DOC-INT-008 | plan activity — test-plans.md §d; plan section — test-plans.md §d; test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR003-03 | INT-REQ-003 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR003-04 | INT-REQ-003 | §d, CHAOS-01, DOC-INT-008 | plan activity — test-plans.md §d; plan section — test-plans.md §d; test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR004-01 | INT-REQ-004 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR004-02 | INT-REQ-004 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR004-03 | INT-REQ-004 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR004-04 | INT-REQ-004 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR005-01 | INT-REQ-005 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR005-02 | INT-REQ-005 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-IR005-03 | INT-REQ-005 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-IR005-04 | INT-REQ-005 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR006-01 | INT-REQ-006 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR006-02 | INT-REQ-006 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR006-03 | INT-REQ-006 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR006-04 | INT-REQ-006 | scope: test-plans.md §d | plan scope declaration — test-plans.md §d | DECLARED |
| AC-IR007-01 | INT-REQ-007 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR007-02 | INT-REQ-007 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR007-03 | INT-REQ-007 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR007-04 | INT-REQ-007 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR008-01 | INT-REQ-008 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR008-02 | INT-REQ-008 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR008-03 | INT-REQ-008 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-IR008-04 | INT-REQ-008 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-NFR-001-01 | NFR-001 | scope: test-plans.md §b | plan scope declaration — test-plans.md §b | DECLARED |
| AC-NFR-001-02 | NFR-001 | scope: test-plans.md §b | plan scope declaration — test-plans.md §b | DECLARED |
| AC-NFR-002-01 | NFR-002 | §b, PERF-07 | plan activity — test-plans.md §b; plan section — test-plans.md §b | EXPLICIT |
| AC-NFR-002-02 | NFR-002 | §b, PERF-07 | plan activity — test-plans.md §b; plan section — test-plans.md §b | EXPLICIT |
| AC-NFR-003-01 | NFR-003 | §b, PERF-01 | plan activity — test-plans.md §b; plan section — test-plans.md §b | EXPLICIT |
| AC-NFR-003-02 | NFR-003 | §b, PERF-01, PERF-06, TST-CON-25 | constraint register — constraint-tests.md; plan activity — test-plans.md §b; plan section — test-plans.md §b | EXPLICIT |
| AC-NFR-004-01 | NFR-004 | §b, PERF-02 | plan activity — test-plans.md §b; plan section — test-plans.md §b | EXPLICIT |
| AC-NFR-004-02 | NFR-004 | scope: test-plans.md §b | plan scope declaration — test-plans.md §b | DECLARED |
| AC-NFR-005-01 | NFR-005 | TST-CON-26 | constraint register — constraint-tests.md | EXPLICIT |
| AC-NFR-005-02 | NFR-005 | TST-CON-26 | constraint register — constraint-tests.md | EXPLICIT |
| AC-NFR-006-01 | NFR-006 | §d, CHAOS-06, TST-CON-26 | constraint register — constraint-tests.md; plan activity — test-plans.md §d; plan section — test-plans.md §d | EXPLICIT |
| AC-NFR-006-02 | NFR-006 | scope: test-plans.md §d | plan scope declaration — test-plans.md §d | DECLARED |
| AC-NFR-007-01 | NFR-007 | scope: test-plans.md §d, TC-113 | plan scope declaration — test-plans.md §d; TC file — Related requirements & rules | EXPLICIT |
| AC-NFR-007-02 | NFR-007 | §d, CHAOS-04 | plan activity — test-plans.md §d; plan section — test-plans.md §d | EXPLICIT |
| AC-NFR-008-01 | NFR-008 | TC-064 | TC file — Related requirements & rules | EXPLICIT |
| AC-NFR-008-02 | NFR-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-NFR-009-01 | NFR-009 | TST-CON-21 | constraint register — constraint-tests.md | EXPLICIT |
| AC-NFR-009-02 | NFR-009 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-NFR-010-01 | NFR-010 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-NFR-010-02 | NFR-010 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-NFR-011-01 | NFR-011 | §e | plan section — test-plans.md §e | EXPLICIT |
| AC-NFR-011-02 | NFR-011 | §e | plan section — test-plans.md §e | EXPLICIT |
| AC-NFR-012-01 | NFR-012 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-NFR-012-02 | NFR-012 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-NFR-013-01 | NFR-013 | §f, TST-CON-24 | constraint register — constraint-tests.md; plan section — test-plans.md §f | EXPLICIT |
| AC-NFR-013-02 | NFR-013 | §f, TST-CON-24 | constraint register — constraint-tests.md; plan section — test-plans.md §f | EXPLICIT |
| AC-NFR-014-01 | NFR-014 | DOC-TST-005 | test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-NFR-014-02 | NFR-014 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-NFR-015-01 | NFR-015 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-NFR-015-02 | NFR-015 | §g | plan section — test-plans.md §g | EXPLICIT |
| AC-NFR-016-01 | NFR-016 | §h, DOC-TST-002, DOC-TST-005, TST-CON-22 | constraint register — constraint-tests.md; plan section — test-plans.md §h; test document citation — 13-testing/test-data-and-environments.md; test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-NFR-016-02 | NFR-016 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-NFR-017-01 | NFR-017 | §b, DOC-TST-005 | plan section — test-plans.md §b; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-NFR-017-02 | NFR-017 | scope: test-plans.md §b | plan scope declaration — test-plans.md §b | DECLARED |
| AC-NFR-018-01 | NFR-018 | §d, CHAOS-07 | plan activity — test-plans.md §d; plan section — test-plans.md §d | EXPLICIT |
| AC-NFR-018-02 | NFR-018 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-NFR-019-01 | NFR-019 | TC-059 | TC file — Related requirements & rules | EXPLICIT |
| AC-NFR-019-02 | NFR-019 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | GAP |
| AC-NFR-020-01 | NFR-020 | scope: test-plans.md §h, TC-113 | plan scope declaration — test-plans.md §h; TC file — Related requirements & rules | EXPLICIT |
| AC-NFR-020-02 | NFR-020 | §h | plan section — test-plans.md §h | EXPLICIT |
| AC-SR001-01 | SEC-REQ-001 | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-SR001-02 | SEC-REQ-001 | scope: test-plans.md §c; TC block TC-001–010 | plan scope declaration — test-plans.md §c; TC block declaration — 13-testing/test-cases/README.md §4 | DECLARED |
| AC-SR001-03 | SEC-REQ-001 | scope: test-plans.md §c; TC block TC-001–010 | plan scope declaration — test-plans.md §c; TC block declaration — 13-testing/test-cases/README.md §4 | DECLARED |
| AC-SR001-04 | SEC-REQ-001 | scope: test-plans.md §c; TC block TC-001–010 | plan scope declaration — test-plans.md §c; TC block declaration — 13-testing/test-cases/README.md §4 | DECLARED |
| AC-SR001-05 | SEC-REQ-001 | scope: test-plans.md §c; TC block TC-001–010 | plan scope declaration — test-plans.md §c; TC block declaration — 13-testing/test-cases/README.md §4 | DECLARED |
| AC-SR002-01 | SEC-REQ-002 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR002-02 | SEC-REQ-002 | DOC-INT-008 | test document citation — 10-integrations/testing-and-sandboxes.md | EXPLICIT |
| AC-SR002-03 | SEC-REQ-002 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR002-04 | SEC-REQ-002 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR003-01 | SEC-REQ-003 | TST-CON-08 | constraint register — constraint-tests.md | EXPLICIT |
| AC-SR003-02 | SEC-REQ-003 | TST-CON-08 | constraint register — constraint-tests.md | EXPLICIT |
| AC-SR003-03 | SEC-REQ-003 | TST-CON-08 | constraint register — constraint-tests.md | EXPLICIT |
| AC-SR003-04 | SEC-REQ-003 | scope: test-plans.md §c; TC block TC-001–010 | plan scope declaration — test-plans.md §c; TC block declaration — 13-testing/test-cases/README.md §4 | DECLARED |
| AC-SR003-05 | SEC-REQ-003 | scope: test-plans.md §c; TC block TC-001–010 | plan scope declaration — test-plans.md §c; TC block declaration — 13-testing/test-cases/README.md §4 | DECLARED |
| AC-SR004-01 | SEC-REQ-004 | §c, PLAN-02, SEC-P-05 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR004-02 | SEC-REQ-004 | §c, PLAN-02, SEC-P-05 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR004-03 | SEC-REQ-004 | §c, PLAN-02, SEC-P-05, TC-014, TC-114 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-SR004-04 | SEC-REQ-004 | §c, PLAN-02, SEC-P-05, TC-114 | executable plan row — test-plans.md §a; plan activity — test-plans.md §c; plan section — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-SR005-01 | SEC-REQ-005 | §c, SEC-P-08 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR005-02 | SEC-REQ-005 | §c, SEC-P-08 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR005-03 | SEC-REQ-005 | §c, SEC-P-08 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR005-04 | SEC-REQ-005 | scope: test-plans.md §c; TC block TC-001–010 | plan scope declaration — test-plans.md §c; TC block declaration — 13-testing/test-cases/README.md §4 | DECLARED |
| AC-SR006-01 | SEC-REQ-006 | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-SR006-02 | SEC-REQ-006 | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-SR006-03 | SEC-REQ-006 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR006-04 | SEC-REQ-006 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR007-01 | SEC-REQ-007 | §c, SEC-P-03 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR007-02 | SEC-REQ-007 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR007-03 | SEC-REQ-007 | §c, SEC-P-03 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR007-04 | SEC-REQ-007 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR008-01 | SEC-REQ-008 | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-SR008-02 | SEC-REQ-008 | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-SR008-03 | SEC-REQ-008 | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-SR008-04 | SEC-REQ-008 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR009-01 | SEC-REQ-009 | §c, SEC-P-06 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR009-02 | SEC-REQ-009 | §c, SEC-P-06 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR009-03 | SEC-REQ-009 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR009-04 | SEC-REQ-009 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR010-01 | SEC-REQ-010 | scope: test-plans.md §c, TC-105 | plan scope declaration — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-SR010-02 | SEC-REQ-010 | scope: test-plans.md §c, TC-106 | plan scope declaration — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-SR010-03 | SEC-REQ-010 | scope: test-plans.md §c, TC-107 | plan scope declaration — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-SR010-04 | SEC-REQ-010 | scope: test-plans.md §c, TC-108 | plan scope declaration — test-plans.md §c; TC file — Related requirements & rules | EXPLICIT |
| AC-SR011-01 | SEC-REQ-011 | §c, DOC-TST-005, SEC-P-07 | plan activity — test-plans.md §c; plan section — test-plans.md §c; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-SR011-02 | SEC-REQ-011 | §c, DOC-TST-005, SEC-P-07 | plan activity — test-plans.md §c; plan section — test-plans.md §c; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-SR011-03 | SEC-REQ-011 | §c, SEC-P-07 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-SR011-04 | SEC-REQ-011 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR012-01 | SEC-REQ-012 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-SR012-02 | SEC-REQ-012 | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-SR012-03 | SEC-REQ-012 | scope: test-plans.md §c | plan scope declaration — test-plans.md §c | DECLARED |
| AC-SR012-04 | SEC-REQ-012 | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-XCUT-01 | cross-cutting | DOC-TST-005 | test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-XCUT-02 | cross-cutting | DOC-TST-002, TST-CON-01, TST-CON-26 | constraint register — constraint-tests.md; test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-XCUT-03 | cross-cutting | §e, §f, DOC-TST-002 | plan section — test-plans.md §e; plan section — test-plans.md §f; test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-XCUT-04 | cross-cutting | §d, CHAOS-03, CHAOS-05, DOC-TST-002 | plan activity — test-plans.md §d; plan section — test-plans.md §d; test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-S-01 | success-criteria | DOC-TST-001 | test document citation — 13-testing/README.md | DECLARED |
| AC-S-02 | success-criteria | DOC-TST-004 | constraint register — constraint-tests.md | EXPLICIT |
| AC-S-03 | success-criteria | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-S-04 | success-criteria | DOC-TST-001 | test document citation — 13-testing/README.md | DECLARED |
| AC-S-05 | success-criteria | §b, DOC-TST-002, PERF-01, TST-CON-25 | constraint register — constraint-tests.md; plan activity — test-plans.md §b; plan section — test-plans.md §b; test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-S-06 | success-criteria | DOC-TST-001 | test document citation — 13-testing/README.md | DECLARED |
| AC-S-07 | success-criteria | §c, DOC-TST-002, SEC-P-03 | plan activity — test-plans.md §c; plan section — test-plans.md §c; test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-S-08 | success-criteria | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-S-09 | success-criteria | DOC-TST-002 | test document citation — 13-testing/testing-strategy.md | EXPLICIT |
| AC-S-10 | success-criteria | §e | plan section — test-plans.md §e | EXPLICIT |
| AC-S-11 | success-criteria | §f | plan section — test-plans.md §f | EXPLICIT |
| AC-S-12 | success-criteria | §c, SEC-P-09 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-S-13 | success-criteria | §c, SEC-P-04 | plan activity — test-plans.md §c; plan section — test-plans.md §c | EXPLICIT |
| AC-S-14 | success-criteria | DOC-TST-005, TC-038 | TC file — Related requirements & rules; test document citation — 13-testing/test-data-and-environments.md | EXPLICIT |
| AC-S-15 | success-criteria | TC-042, TC-054 | TC file — Related requirements & rules | EXPLICIT |
| AC-S-16 | success-criteria | §c | plan section — test-plans.md §c | EXPLICIT |
| AC-S-17 | success-criteria | §d, CHAOS-06, TST-CON-26 | constraint register — constraint-tests.md; plan activity — test-plans.md §d; plan section — test-plans.md §d | EXPLICIT |
| AC-S-18 | success-criteria | §d, CHAOS-08 | plan activity — test-plans.md §d; plan section — test-plans.md §d | EXPLICIT |
| AC-S-19 | success-criteria | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE — evidence type is an operational/pilot record, not a test artifact | OPERATIONAL EVIDENCE |
| AC-S-20 | success-criteria | §h | plan section — test-plans.md §h | EXPLICIT |
| AC-S-21 | success-criteria | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE — evidence type is an operational/pilot record, not a test artifact | OPERATIONAL EVIDENCE |
| AC-S-22 | success-criteria | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE — evidence type is an operational/pilot record, not a test artifact | OPERATIONAL EVIDENCE |
| AC-S-23 | success-criteria | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE — evidence type is an operational/pilot record, not a test artifact | OPERATIONAL EVIDENCE |
| AC-S-24 | success-criteria | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE — evidence type is an operational/pilot record, not a test artifact | OPERATIONAL EVIDENCE |

---

## 4. Constraint → Constraint Test Matrix

Every constraint `C-01…C-26` has exactly one register entry with the same number (one-to-one, `../../13-testing/core/constraint-tests.md` §1); the AC column shows which acceptance criteria the register detail itself cites.

| Constraint | Constraint test | Status | ACs cited in the register detail | Related plan activity |
|---|---|---|---|---|
| C-01 | TST-CON-01 | DESIGNED | AC-FR011-05, AC-XCUT-02 | TC-031 |
| C-02 | TST-CON-02 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-03 | TST-CON-03 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-04 | TST-CON-04 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-05 | TST-CON-05 | DESIGNED | AC-IR001-01, AC-IR002-01 | — |
| C-06 | TST-CON-06 | DESIGNED | AC-FR001-01 | TC-001 |
| C-07 | TST-CON-07 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-08 | TST-CON-08 | DESIGNED | AC-SR003-01, AC-SR003-02, AC-SR003-03 | — |
| C-09 | TST-CON-09 | DESIGNED | AC-FR012-01 | — |
| C-10 | TST-CON-10 | DESIGNED | AC-FR011-04 | — |
| C-11 | TST-CON-11 | DESIGNED | AC-FR016-01 | — |
| C-12 | TST-CON-12 | DESIGNED | AC-FR014-01, AC-FR014-02 | — |
| C-13 | TST-CON-13 | DESIGNED | AC-FR005-01, AC-FR005-02, AC-FR005-03 | — |
| C-14 | TST-CON-14 | DESIGNED | AC-FR011-01 | — |
| C-15 | TST-CON-15 | DESIGNED | AC-FR010-01, AC-FR010-02 | — |
| C-16 | TST-CON-16 | DESIGNED | AC-FR015-02, AC-FR015-03, AC-FR015-05 | — |
| C-17 | TST-CON-17 | DESIGNED | AC-FR008-04 | — |
| C-18 | TST-CON-18 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-19 | TST-CON-19 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-20 | TST-CON-20 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-21 | TST-CON-21 | DESIGNED | AC-NFR-009-01 | — |
| C-22 | TST-CON-22 | DESIGNED | AC-NFR-016-01 | — |
| C-23 | TST-CON-23 | DESIGNED | INSUFFICIENT EVIDENCE | — |
| C-24 | TST-CON-24 | DESIGNED | AC-NFR-013-01, AC-NFR-013-02 | — |
| C-25 | TST-CON-25 | DESIGNED | AC-NFR-003-02, AC-S-05 | — |
| C-26 | TST-CON-26 | DESIGNED | AC-NFR-005-01, AC-NFR-005-02, AC-NFR-006-01, AC-S-17, AC-XCUT-02 | — |

All 26 rows are `DESIGNED` at v1.0 — status vocabulary `DESIGNED → READY → EXECUTED → PASS/FAIL` comes from the register itself, and gate `AC-S-02` requires 26/26 `PASS` before release. Several register details (`TST-CON-02`, `-03`, `-04`, `-07`, `-18`, `-19`, `-20`, `-23`) cite no AC at all: their *Related plan activity* and AC cells read `INSUFFICIENT EVIDENCE` rather than an assumed link.

---

## 5. Declared-but-Absent Test Cases

`../../13-testing/test-cases-index.md` §2 locks an allocation of **114** cases. All **114** files exist (the 11 cases `TC-104`…`TC-114` were authored 2026-09-27 under `REC-03`). Historical status rows are kept and flipped, never deleted (DOC-TPL-011 #3):

| TC ID | Declared in | FR block | Status |
|---|---|---|---|
| `TC-104` | `../../13-testing/test-cases-index.md` §2 (range `TC-097–104`) | `FR-019` content & coupons | `declared but file absent` → `present (2026-09-27)` |
| `TC-105` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-106` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-107` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-108` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-109` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-110` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-111` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-112` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-113` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| `TC-114` | `../../13-testing/test-cases-index.md` §2 (range `TC-105–114`) | `FR-020` administration & audit | `declared but file absent` → `present (2026-09-27)` |
| **11 declared, 11 present in this range** | | | |

Consequences (re-verified 2026-09-27 after the `REC-03` pay-down): the locked-block claim in `../../13-testing/test-cases-index.md` §2/§4 — each family has "≥1 case per AC of that FR inside the block" — is now checkable for `FR-019` (`TC-104`) and `FR-020` (`TC-105`…`TC-114`); the four rows that rested on the block alone (`AC-SR010-01…04`) are `EXPLICIT` against `TC-105`…`TC-108`; and the counts behind `13-testing/README.md` gate `G-TEST-1` ("114 TCs mapped to FR families") are satisfiable from disk (114 files, every cited `TC-` ID resolves). Remaining open findings are tracked in §7 — chiefly `G-01` (27 ACs with no artifact), not file absence.

---

## 6. Gaps — 27 Acceptance Criteria With No Test Artifact

| Parent requirement | ACs with no test artifact | Note |
|---|---|---|
| `DATA-REQ-002` | `AC-DR002-01, AC-DR002-02, AC-DR002-03, AC-DR002-04` | data minimisation — no TC/plan/register cites its ACs |
| `DATA-REQ-003` | `AC-DR003-01, AC-DR003-02, AC-DR003-03, AC-DR003-04` | retention & deletion — same |
| `DATA-REQ-006` | `AC-DR006-01, AC-DR006-04` | referential integrity — partial family (only `AC-DR006-02/03` linked) |
| `DATA-REQ-007` | `AC-DR007-03, AC-DR007-04` | append-only financial data — partial family (only `AC-DR007-01/02` linked) |
| `DATA-REQ-008` | `AC-DR008-01, AC-DR008-02, AC-DR008-03, AC-DR008-04` | query performance & pagination constraints — whole family unlinked |
| `INT-REQ-002` | `AC-IR002-02, AC-IR002-03, AC-IR002-04` | bank-transfer verification — only `AC-IR002-01` is linked (`TST-CON-05`) |
| `INT-REQ-005` | `AC-IR005-02, AC-IR005-03` | delivery-provider integration — partial family |
| `NFR-008` | `AC-NFR-008-02` | idempotency & transactions — only `AC-NFR-008-01` linked (`TC-064`) |
| `NFR-012` | `AC-NFR-012-01, AC-NFR-012-02` | maintainability — whole family unlinked |
| `NFR-014` | `AC-NFR-014-02` | observability & alert quality — only `AC-NFR-014-01` linked |
| `NFR-016` | `AC-NFR-016-02` | environment parity — only `AC-NFR-016-01` linked |
| `NFR-019` | `AC-NFR-019-02` | audit retention & reporting — only `AC-NFR-019-01` linked |
| **12 requirements** | **27 ACs** | see §3 for per-row status |

Reading: each group lists ACs whose parent requirement is covered by **no** `TC`, plan row, plan section, constraint-register entry or test document citation anywhere in the scanned set. `DATA-REQ-002` (data minimisation), `DATA-REQ-003` (retention), `DATA-REQ-008` (query/performance constraints), `INT-REQ-002` (bank-transfer verification), `NFR-012` (maintainability), `NFR-019` (audit/reporting retention) and `NFR-014` (observability alert quality) are the most exposed families.

---

## 7. Findings & Documents Needing Update

| # | Finding | Severity | Evidence |
|---|---|---|---|
| G-01 | 27 ACs have no test-artifact link (`GAP` rows in §3, listed in §6) | HIGH | §3, §6 |
| G-02 | ~~11 declared test-case files are missing — `TC-104…TC-114` (103 files exist against a locked allocation of 114)~~ **RESOLVED 2026-09-27** — all 11 files authored; 114/114 present, every cited `TC-` ID resolves (`REC-03` pay-down) | HIGH (was) → **RESOLVED** | §5 |
| G-03 | 48 ACs are covered only by an allocation/scope declaration, not by an artifact naming them | MEDIUM | §3 rows with status `DECLARED` |
| G-04 | `AC-S-03` ("zero gaps") and `13-testing/README.md` `G-TEST-1` cannot be demonstrated from the corpus as it stands — file-absence cause cleared 2026-09-27, but `G-01`/`G-03` (27 unlinked + 42 declared-only ACs) and zero execution evidence still block the claim | HIGH | §2 verdict; `02-requirements/acceptance-criteria.md` §7 |
| G-05 | ~~14 FR files list only `AC-FRnnn-01…04` while the registry defines `AC-FRnnn-05` (`FR-001, 002, 003, 004, 006, 008, 009, 010, 011, 012, 013, 014, 015, 017`)~~ **RESOLVED 2026-09-27** — all 14 references added; 94/94 registry `AC-FR*` IDs present (`REC-04`/`TD-05` paid) | MEDIUM (was) → **RESOLVED** | `02-requirements/*.md` vs `acceptance-criteria.md` |
| G-06 | 5 success criteria (`AC-S-19`, `AC-S-21`…`AC-S-24`) are operational/pilot/sign-off records — no test artifact can ever satisfy them here | INFORMATIONAL | §3 rows marked `OPERATIONAL EVIDENCE` |
| G-07 | 779 `AC-UCnnn-nn` criteria exist in `01-business-analysis/*.md` outside the registry that claims to be the single registry of every `AC-*` | MEDIUM | count of unique `AC-UC*` strings — 779 re-counted 2026-09-29 after session 010 grew the corpus to 210 UCs (was 121 at v1.2; finding unchanged, MEDIUM `OPEN`) |
| G-08 | 8 constraint-register details cite no AC | LOW | §4 |
| G-09 | Execution status: 0 tests executed, 0 reports; all `TST-CON-NN` `DESIGNED` | INFORMATIONAL (expected at v1.0) | `../../13-testing/core/constraint-tests.md` |

**Documents needing update (reported, not edited):** `02-requirements/acceptance-criteria.md` §7 (G-04 — qualify the zero-gap claim until the gaps close); `01-business-analysis/*.md` or the registry wording (G-07); `00-project-overview/success-criteria.md` (G-06 — mark the five operational criteria as non-test evidence). *(G-02 clause retired 2026-09-27 — `TC-104`…`TC-114` now exist; G-05 clause retired 2026-09-27 — the 14 `-05` references now exist.)*

---

## 8. Maintenance

Follow `README.md` §6: any AC, `TC`, `PLAN`, `TST-CON`, plan-section or test-document change is reflected here in the **same change set**; sweep results go to `../../20-validation/core/consistency-audit.md`; anything contradictory (missing files, competing AC ID spaces, broken gate claims) goes to `../../20-validation/core/contradiction-audit.md`.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 item 40 |
| 1.1 | 2026-09-27 | 29 citations of undefined `DOC-INT-010` corrected to `DOC-INT-008` (`../../10-integrations/core/testing-and-sandboxes.md`) | `../../20-validation/core/consistency-audit.md` finding 23 — no cited ID absent from its owning register (root README §11 `D-3`) |
| 1.2 | 2026-09-27 | `REC-03` pay-down: `TC-104`…`TC-114` authored — §1 artifact count 114, §2 NFR/SEC counts re-run (203/42), 6 rows `DECLARED`→`EXPLICIT` (`AC-SR010-01…04`, `AC-NFR-007-01`, `AC-NFR-020-01`), 10 rows gain new TC links, §5 statuses flipped to present, `G-02` → `RESOLVED`, `G-04` re-scoped | Root README §9.4 same-change-set propagation for a `13-testing/` change (`21-completion/recommendations.md` `REC-03`) |
| 1.3 | 2026-09-27 | `REC-04` pay-down: `G-05` → `RESOLVED` (14 `AC-FRnnn-05` references added, 94/94 cited); "documents needing update" re-scoped | Root README §9.4 same-change-set propagation for an `02-requirements/functional/` change (`REC-04`) |
| 1.4 | 2026-09-28 | §1 Functional range end corrected `AC-FR020-05` → `AC-FR020-04` (registry tops at `-04`; FR-020 defines four ACs — count 94 unchanged) | `REC-15` citation-CI enforcement (session 008) — `tools/check_citations.py` caught the dangling range end |
| 1.5 | 2026-09-29 | `G-07` evidence re-counted: 121 → **779** unique `AC-UC*` IDs across the now-210 `use-cases/UC-*.md` (finding severity/status unchanged, MEDIUM `OPEN`) | `prompt-010.md` §1 session-010 UC-coverage directive — UC corpus grown 42 → 210, UC-derived evidence re-synced in the same change set (root README §9 rule 4) |
