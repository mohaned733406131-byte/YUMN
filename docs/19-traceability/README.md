---
document_id: DOC-TRC-001
title: Traceability — Domain Overview, Chain Rules & Coverage Dashboard
category: 19-traceability
status: approved
version: 1.2
created: 2026-09-27
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-020, NFR-009]
related_documents: [DOC-ROOT-001, DOC-REQ-001, DOC-AC-001, DOC-OVR-004, DOC-OVR-011, DOC-BA-005, DOC-API-001, DOC-DB-001, DOC-TST-001, DOC-TST-003, DOC-TST-004, DOC-TST-006]
---

# 19 — Traceability

**Owns the requirement → artifact matrices of the yumn knowledge base.** This domain answers, for every requirement, objective, acceptance criterion and constraint: *where is it realised, and where is it proven?* It is the deliverable of methodology item **40. Traceability Matrix** (`docs/README.md` §10) and it is what gate `AC-S-03` ("every FR has ≥1 passing test case and satisfied acceptance criteria — `19-traceability/requirements-to-tests.md`, 0 gaps") is measured against.

This domain **records links, never creates canon**. Requirement text, AC text, rules, endpoints, entities and test cases are owned by `02-requirements/`, `01-business-analysis/`, `07-api/`, `08-database/` and `13-testing/`; this domain only reads them and reports what the corpus actually supports.

---

## 1. Purpose & Audience

| Question | Answered here | Owned elsewhere |
|---|---|---|
| Which objectives does a requirement serve? | `requirements-to-features.md` Matrix A | `00-project-overview/project-objectives.md` |
| Which API group, endpoint, entity, use case, workflow and rule does a requirement touch? | `requirements-to-features.md` Matrix B | `07-api/`, `08-database/`, `01-business-analysis/` |
| Which test artifact proves each acceptance criterion? | `requirements-to-tests.md` | `13-testing/` |
| Did any test actually execute and pass? | **No** — this domain is design-time linkage only | `21-completion/quality-gates.md` |
| Is a claim inconsistent or unsupported elsewhere? | Reported as a finding only | `20-validation/` |

Audience: the validation domain (`20-validation/`), the completion domain (`21-completion/`), and any reviewer checking `AC-S-01`, `AC-S-02`, `AC-S-03`.

---

## 2. The Canonical Chain

Repository-wide example (`docs/README.md` §5):

```text
FR-013 → BR-PAY-04 → UC-021 → API-WAL-002 → wallet → TC-031 → AC-FR013-01
```

Each hop was re-verified against the corpus while authoring this domain (`VERIFIED` unless marked otherwise):

| Hop | Evidence checked | Result |
|---|---|---|
| `FR-013 → BR-PAY-04` | `02-requirements/functional/FR-013.md` §Business Rules Applied | Holds |
| `BR-PAY-04 → UC-021` | `01-business-analysis/business-rules.md` row `BR-PAY-04`; `use-cases/UC-021.md` | **Fails** — `BR-PAY-04` is exercised by `UC-034` (Verify Bank-Transfer Top-Up); `UC-021` (Respond to Return Request) cites `BR-RET-*`/`BR-ORD-05`, not `BR-PAY-04` |
| `UC-021 → API-WAL-002` | `07-api/endpoints/wallet.md`, `returns.md` | **Fails** — `UC-021` is cited by `API-RET-*` and `API-WAL-014`; `API-WAL-002` cites only `FR-013`, `BR-PAY-06/10`, `DATA-REQ-007/008` |
| `API-WAL-002 → wallet` | `07-api/endpoints/wallet.md`, `08-database/entities/wallet.md` (`DB-010`, related `FR-013`) | Holds (ledger view over `DB-010`/`DB-011`) |
| `wallet → TC-031` | `13-testing/test-cases/TC-031.md` §Related IDs (`API-WAL-001/002/007/009`, `FR-013`) | Holds |
| `TC-031 → AC-FR013-01` | `TC-031.md` §Related IDs | Holds |

The five-hop form used by `TC-031` — `FR-013 → BR-PAY-04 → API-WAL-002 → TC-031 → AC-FR013-01` — holds at every hop. The two failing hops above are recorded as findings (§7, F-05) for `20-validation/contradiction-audit.md`; they are not silently corrected here because `docs/README.md` is not mine to edit.

---

## 3. File Register

| File | Document ID | Owns | Rows |
|---|---|---|---|
| `README.md` | `DOC-TRC-001` | Domain index, chain rules, vocabulary, coverage dashboard, findings | — |
| `requirements-to-features.md` | `DOC-TRC-002` | Objective → requirement matrix; requirement → feature/asset matrix | 12 objectives, 68 requirements |
| `requirements-to-tests.md` | `DOC-TRC-003` | Requirement → AC → test-artifact matrix; constraint → `TST-CON-NN` matrix | 277 ACs, 26 constraints |

No other file may be added to this domain without a matching row in `docs/README.md` §2 and a new `DOC-TRC-*` ID.

---

## 4. Evidence & Link-Basis Vocabulary

Statement tags follow `docs/README.md` §8: `VERIFIED` · `INFERENCE` · `INSUFFICIENT EVIDENCE`. Matrix rows add a **link status** that says how strong a requirement↔artifact link is:

| Link status | Meaning | Evidence class |
|---|---|---|
| `EXPLICIT` | An artifact names the ID itself: a `TC-NNN` *Related requirements & rules* row, a `PLAN-NN`/`PERF-NN`/`SEC-P-NN`/`CHAOS-NN` row, a plan-section canon column, a `TST-CON-NN` register detail, or a test document citing the AC | `VERIFIED` |
| `DECLARED` | Coverage is asserted only at allocation/scope level: the locked TC block table, a plan's scope line, or a strategy statement | `INFERENCE` |
| `GAP` | No artifact and no declaration found anywhere in `13-testing/` or the integration test drill catalogue | `INSUFFICIENT EVIDENCE` |
| `OPERATIONAL EVIDENCE` | The criterion is provable only by an operational/pilot/audit record, not by a test artifact | Out of test-artifact scope — tracked in `21-completion/` |

An empty matrix cell always means `INSUFFICIENT EVIDENCE` — never an implied link. Cells are never guessed (`docs/README.md` §8).

---

## 5. Coverage Dashboard (as of 2026-09-28)

**Corpus under trace (all `VERIFIED` by direct count):**

| Object | Count | Source |
|---|---|---|
| Objectives `OBJ-01…OBJ-12` | 12 | `00-project-overview/project-objectives.md` |
| Requirements | 68 (20 `FR`, 20 `NFR`, 12 `SEC-REQ`, 8 `DATA-REQ`, 8 `INT-REQ`) | `02-requirements/requirements-overview.md` |
| Business rules | 104 | `01-business-analysis/business-rules.md` |
| Constraints `C-01…C-26` | 26 | `00-project-overview/project-constraints.md` |
| Acceptance criteria | 253 in `02-requirements/acceptance-criteria.md` (94 FR + 40 NFR + 50 SR + 32 DR + 33 IR + 4 XCUT) + 24 `AC-S-NN` in `00-project-overview/success-criteria.md` = **277 traceable AC rows** | both files |
| Use cases / workflows / blocks | 42 `UC` / 12 `WF` / 13 blocks | `01-business-analysis/` , `00-project-overview/project-context.md` |
| API groups / endpoints | 14 / 221 | `07-api/README.md` §4 |
| Database entities | 18 (`DB-001…DB-018`) | `08-database/entities/` |
| Test artifacts | 114 `TC` files present (114 declared), 18 `PLAN`, 7 `PERF`, 9 `SEC-P`, 8 `CHAOS`, 8 plan sections `§a…§h`, 26 `TST-CON` | `13-testing/` |

**Acceptance-criterion → test-artifact linkage (this domain's headline number):**

| Link status | ACs | Share |
|---|---|---|
| `EXPLICIT` | 203 | 73.3% |
| `DECLARED` (allocation/scope only) | 42 | 15.2% |
| `GAP` | 27 | 9.7% |
| `OPERATIONAL EVIDENCE` | 5 | 1.8% |
| **Total** | **277** | 100% |

By family: FR 86/94 `EXPLICIT` + 8 `DECLARED`; NFR 29/40 `EXPLICIT` + 5 `DECLARED`; SEC 31/50 `EXPLICIT` + 19 `DECLARED`; DATA 10/32 `EXPLICIT` + 6 `DECLARED`; INT 27/33 `EXPLICIT` + 1 `DECLARED`; XCUT 4/4 `EXPLICIT`; `AC-S` 16/24 `EXPLICIT` + 3 `DECLARED` (+5 `OPERATIONAL`).

**Verdict for `requirements-to-tests.md`: `PASS WITH FINDINGS`** — every requirement and every AC has a row, and all 20 FRs have ≥1 `TC`, but 27 ACs have no test-artifact link (F-01; the 11 formerly absent `TC` files were authored in session 003, F-02 `RESOLVED`). Nothing is executed yet: all 26 `TST-CON-NN` are `DESIGNED`, and no test result is claimed anywhere in this domain.

---

## 6. Maintenance Rules

1. **Same change set.** If an `FR`, `NFR`, `SEC-REQ`, `DATA-REQ`, `INT-REQ`, `AC`, `BR`, `C-NN`, endpoint, entity, `UC`, `WF`, `OBJ` or `TC` is added, renamed or removed, the matrices in `requirements-to-features.md` and `requirements-to-tests.md` are updated in the **same change set** — never in a later commit (`docs/README.md` §9 rule 4).
2. **Canon wins.** This domain never invents IDs, never redefines AC text, never renumbers a `TC`. If a matrix row and a source file disagree, the source file is right and the disagreement becomes a finding.
3. **Sweep.** After any structural change to requirements or testing, re-run the sweep that produces the counts in §5 and record affected IDs in `20-validation/consistency-audit.md`.
4. **Contradictions.** Anything that cannot be resolved inside a matrix (duplicate ID spaces, broken chain hops, allocation mismatches) is recorded in `20-validation/contradiction-audit.md` — never ignored (`docs/README.md` §9 rule 5).
5. **Versioning.** Any row change bumps `version` and adds a `## Change History` row (`docs/README.md` §9 rules 1–3).
6. **No execution claims.** Status such as `PASS`/`FAIL`/`VERIFIED-by-test` may not appear in this domain; execution evidence belongs to `13-testing/` artifacts and `21-completion/quality-gates.md`.

---

## 7. Known Gaps & Findings (hand-off to `20-validation/`)

Severity uses `docs/README.md` §8 classes; confidence noted where it matters.

| # | Finding | Severity | Evidence |
|---|---|---|---|
| F-01 | **27 ACs have no test-artifact link at all**: `AC-DR002-01…04`, `AC-DR003-01…04`, `AC-DR006-01/04`, `AC-DR007-03/04`, `AC-DR008-01…04`, `AC-IR002-02/03/04`, `AC-IR005-02/03`, `AC-NFR-008-02`, `AC-NFR-012-01/02`, `AC-NFR-014-02`, `AC-NFR-016-02`, `AC-NFR-019-02` | HIGH | `requirements-to-tests.md` rows with status `GAP` |
| F-02 | **11 declared TC files are absent**: `13-testing/test-cases/README.md` §2 locks an allocation of **114** cases, only **103** files exist — `TC-104` (tail of the `FR-019` block) and `TC-105…TC-114` (the whole `FR-020` block) have no file — **`RESOLVED` 2026-09-27** (session 003 authored all 11; `TC-*.md` count now **114/114**, `REC-03`/`TD-04` `PAID`, matrix `G-02` closed) | HIGH | count of `13-testing/test-cases/TC-*.md` = 103 → 114 |
| F-03 | **FR files understate their own ACs**: every `02-requirements/functional/FR-nnn.md` lists exactly `AC-FRnnn-01…04`, but `02-requirements/acceptance-criteria.md` defines `AC-FRnnn-05` for 14 FRs (`FR-001, 002, 003, 004, 006, 008, 009, 010, 011, 012, 013, 014, 015, 017`) — **`RESOLVED` 2026-09-27** (session 004 `REC-04`: all 94 registry `AC-FR*` now cited, `TD-05` `PAID`, `HAL-07` `RESOLVED`) | MEDIUM | 20 files × 4 IDs vs 94 registry IDs → 94/94 cited |
| F-04 | **`AC-S-03` zero-gap claim not yet demonstrable**: `02-requirements/acceptance-criteria.md` §7 states this domain "records requirement → AC → TC with zero gaps"; measured state is 27 `GAP` + 42 `DECLARED`-only rows | HIGH | §5 dashboard |
| F-05 | **Broken chain hops in the repository's own example**: `docs/README.md` §5 chain uses `BR-PAY-04 → UC-021 → API-WAL-002`; corpus shows `BR-PAY-04 → UC-034` and `UC-021 → API-RET-*`/`API-WAL-014` | MEDIUM | §2 hop table |
| F-06 | **Unknown API group cited**: `03-system-analysis/functional-analysis.md` cites `API-TOP-*` for the top-up group; `07-api/` registers 14 groups and top-ups live in `API-WAL` — no `API-TOP` group exists — **`RESOLVED` 2026-09-28** (all three consumer sites now cite `API-WAL-003/004`; `HAL-15` `RESOLVED`) | MEDIUM | `07-api/README.md` §4 |
| F-07 | **Parallel AC ID space**: 121 `AC-UCnnn-nn` criteria are defined in `01-business-analysis/use-cases/*.md`, while `02-requirements/acceptance-criteria.md` declares itself the single registry of every `AC-*` | MEDIUM | count of unique `AC-UC*` strings in `use-cases/` |
| F-08 | **No priority on 36 requirements**: only `FR-*` (registry §1) and `SEC-REQ-*` (file header) carry a priority; all `NFR`, `DATA-REQ`, `INT-REQ` files define none → `INSUFFICIENT EVIDENCE` in Matrix B | LOW | `02-requirements/non-functional/*.md` et al. |
| F-09 | **Two objectives have no functional or verification trace**: `OBJ-09` (quality velocity) and `OBJ-10` (maintainability) are named only by `NFR-009`/`NFR-010` — no `FR-*`, use case, workflow or test case cites them; `OBJ-11`'s measurable is itself `INSUFFICIENT EVIDENCE` (`ASM-14`) | LOW | `requirements-to-features.md` Matrix A; search of `13-testing/` for `OBJ-09`/`OBJ-10` returns nothing |
| F-10 | **No stakeholder → objective/requirement mapping exists**: `00-project-overview/stakeholders.md` contains no `STK-* → OBJ-*`/`FR-*` table, so no stakeholder trace can be built without inventing links | LOW | file read, no such table |
| F-11 | **Design-time only**: all 26 `TST-CON-NN` are `DESIGNED`; no test result, report or dashboard exists anywhere in the corpus | INFORMATIONAL (expected at v1.0) | `13-testing/constraint-tests.md` status column |

**Documents that need updating (not edited by this domain):** ~~`13-testing/test-cases/README.md` (F-02)~~ done 2026-09-27, ~~`02-requirements/functional/FR-001…FR-020.md` for the 14 IDs in F-03~~ done 2026-09-27, `02-requirements/acceptance-criteria.md` §7 (F-04), ~~`03-system-analysis/functional-analysis.md` (F-06)~~ done 2026-09-28, `01-business-analysis/use-cases/*.md` or the registry wording (F-07), `00-project-overview/stakeholders.md` (F-10).

**Documents that become valid by this domain existing:** `docs/README.md` §2 already links `19-traceability/README.md`; that link resolves as of 2026-09-27.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 item 40 |
| 1.1 | 2026-09-28 | `F-06` → `RESOLVED` (phantom `API-TOP` citations replaced by `API-WAL-003/004` in the three consumer documents; `HAL-15` flipped in the same change set) | `plan-develop.md` §8 approval implementation (session 007) — hand-off row re-synced after the owning documents changed |
| 1.2 | 2026-09-28 | §5 dashboard re-run by direct count (BR 99 → **104**, UC 40 → **42**, TC 103 → **114 present**, linkage 197/48 → **203/42** per `requirements-to-tests.md` §2, family line re-synced, verdict clause dropped); §7 `F-02`/`F-03` → `RESOLVED` (sessions 003/004 — never flipped here), `F-04` evidence 48 → 42 `DECLARED`, "needs updating" list struck for F-02/F-03 | Count/dashboard propagation catch-up (session 008 close) — the dashboard claimed `VERIFIED` by direct count but predated sessions 003/004/007/008 |
