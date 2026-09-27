---
document_id: DOC-CMP-007
title: Recommendations (REC-NN)
category: 21-completion
status: approved
version: 1.1
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-013, AC-S-03, AC-S-24]
related_documents: [DOC-ROOT-001, DOC-CMP-004, DOC-CMP-005, DOC-CMP-006, DOC-OVR-009, DOC-OVR-010, DOC-OVR-011, DOC-TST-001, DOC-RSK-001, DOC-CMP-010]
---

# Recommendations (`REC-NN`)

Methodology item 46 (root README §10): *Recommendations* — prioritized, actionable suggestions with rationale, owner, and a **testable acceptance criterion**. Every recommendation here is already surfaced by an evidence trail (`TD-NN`, `ASM-NN`, `DEP-NN`, `GAP-NN`, `RISK-NN`); nothing in this file is speculation.

**Series:** `REC-NN` (two digits, starting `REC-01`). Single allocator is this file; citations elsewhere must already exist here. IDs are never reused; next free after this revision is `REC-16`.

**Priority:** `P0` must precede Gate 0 or Gate 1 exit · `P1` precedes Gate 2 (launch) · `P2` is continuous improvement with a named trigger.

---

## 1. Register

| REC-NN | Recommendation | Rationale (evidence) | Owner | Acceptance criterion (testable) | Priority |
|---|---|---|---|---|---|
| REC-01 | Restore the Analysis Documentation Structure Specification at repository-root `archdoc.md`, or re-point `docs/README.md` §1/§3 to the structure actually enforced by root README §2/§5 | `TD-03` — the file is 0 bytes while cited as the structural authority for the 24-domain layout and navigation order | Knowledge-base maintainer | `archdoc.md` is non-empty and its domain list matches root README §2, **or** `docs/README.md` contains no reference to it and no other document cites it | P1 |
| REC-02 | Re-sync `04-architecture/architecture-decisions-reference.md` with reality: set `ADR-001…ADR-010` to `ACCEPTED`, remove the empty-directory note, verify the §3 coverage map against the ten ADR texts | `TD-02` — two canon-locked citations (`C-21`→`ADR-002`, `C-22`→`ADR-004`) currently show `RESERVED` for files that exist as `approved`; contradicts the index's own §7 lifecycle | Technical lead (architecture) | Every status in the index §1/§2 table equals the `status:` frontmatter of the corresponding `18-decisions/ADR/*.md` file, and no statement in the index claims the directory is empty | P1 |
| REC-03 | Author `TC-104`…`TC-114` under `13-testing/test-cases/` from `23-templates/test-case-template.md` — or formally retract the IDs (locked table, plan ranges, and all citations in one change set) | `TD-04` — 11 of the 114 locked TCs do not exist; `TC-105`/`TC-114` are cited by `13-testing/README.md`, `13-testing/test-plans.md`, `22-glossary/naming-conventions.md`, `22-glossary/terminology.md`; blocks the `AC-S-03` zero-gap audit | QA lead | A script counting files matching `TC-*.md` in `13-testing/test-cases/` equals the total in the §5 locked table, and every `TC-` ID cited anywhere in `docs/` resolves to a file | P0 |
| REC-04 | Close FR ↔ AC drift: add the registry-only `-05` references to the 14 requirement files, or amend `02-requirements/acceptance-criteria.md` with a version bump if an AC was meant to be withdrawn | `TD-05` — `AC-FR001-05` … `AC-FR017-05` exist only in the registry; registry §7 requires requirement files to reference their AC IDs | Product owner (requirements) | For every FR file with a registry row, each `AC-FRnnn-*` ID in the registry appears in that file — verified by an ID-citation check with zero missing references | P0 |
| REC-05 | Reconcile health paths to one canon (`/healthz` + `/readyz` per `BR-PLT-07`): fix `API-ADM-042`/`API-ADM-043` and `TC-001`, `TC-031`, `TC-057`, `TC-065`, then record the correction in `20-validation/contradiction-audit.md` | `TD-06` — the contract and four test cases specify `/health/live` + `/health/ready`, which probes, CI smoke steps, and monitoring do not call; live split that fails at first deployment | DevOps lead | A repo-wide search for `/health/live` and `/health/ready` returns zero hits outside a Change History row, and both `TC` files assert the canon paths | P0 |
| REC-06 | Declare `06-backend/background-processing.md` §1 the single queue register; rename divergent downstream names, register the orphan `b07.wallet.credit`, and make CI's naming check compare against that register | `TD-07` — `04-architecture/data-flow.md` and `10-integrations/` use different names for the same jobs (5 confirmed mismatches); `naming-conventions.md` claims CI enforces one pattern | Technical lead (backend) | Every queue name cited anywhere in `docs/` appears verbatim in the §1 register table; CI job fails on a name not present | P1 |
| REC-07 | Publish one cross-layer role mapping (actor → API role → application enum → DB value) in `09-security/rbac.md` and extend the conformance test to assert enum parity across all three layers | `TD-08` — API lists 6 roles + `SYSTEM`, application enum 10, DB enum 6, with no enforced cross-layer table (`INFERENCE`) | Security officer | The mapping table exists, and the named conformance test covers API↔enum↔DB parity (test source confirms three-layer assertion) | P1 |
| REC-08 | Replace the "not yet authored" stub rows in `03-system-analysis/README.md` and `04-architecture/README.md` with pointers to the real `07-api/`, `08-database/`, `13-testing/` registries | `TD-09` — the three domains are fully populated; stale stubs cause exactly the stop-or-invent-ID failure mode root README §5 forbids | Knowledge-base maintainer | Both READMEs contain zero "not yet authored" rows for those three domains, and each row names the registry path and ID pattern | P1 |
| REC-09 | **PAID 2026-09-27** — Author `19-traceability/` (requirements-to-tests matrix) and `20-validation/` (analysis-validation, critical-findings, missing-information, contradiction-audit, consistency-audit) **before Gate 0** | `TD-10` — gates, `AC-S-03`, `risk-review-process.md` §10, and `final-acceptance.md` all require these paths; they are declared but absent, so gate evidence has no home | Product owner (chairs risk review) | All six named files exist; `19-traceability/requirements-to-tests.md` accounts for every P0 UC and registry AC; a link pass over `docs/` yields zero references to non-existent `19-`/`20-` paths — **met: 3 + 8 files authored, validator `PASS — structure healthy` (0 broken links)** | P0 |
| REC-10 | Add a retire state and quarterly sweep cadence to the §4.1 flag lifecycle; sweep the 7 registered flags against code usage and record dead rows here before removal | `TD-01` — the lifecycle's own dead-flag rule routes to this register, but no row state or cadence exists yet; `FEATURE_FLAGS_DEFAULT_MODE=off` (fail-closed) hides leftovers | DevOps lead | Flag lifecycle defines the retire state and cadence; one completed sweep has a dated record with per-flag disposition | P2 |
| REC-11 | Establish budget, team-size, and schedule baselines and re-score `ASM-14` — and resolve `ASM-03`, `ASM-04`, `ASM-12` (or accept them in writing) as part of the same Gate 0 package | Charter L46 + `00-project-overview/assumptions.md` escalation rule; `ASM-14` `UNSUPPORTED`, `ASM-12` `DANGEROUS`; feasibility verdict for schedule/financial dimensions is `INSUFFICIENT EVIDENCE` until this lands | **Project sponsor** | Gate 0 checklist rows 0.1 and 0.2 in `21-completion/quality-gates.md` are `PASS` with linked evidence, and the four assumption rows carry re-scores + evidence links | P0 |
| REC-12 | Open `DEP-05` (sandbox from **both** m-Floos and OneCash) and `DEP-06` (SMS/WhatsApp contracts) — or record the explicit sponsor decision for bank-transfer-only funding and the `DEP-06` mitigation path — before Gate 0 | `dependencies.md`: both `NOT STARTED`; `RISK-006`/`RISK-003` kill criteria; `SEC-011` CRITICAL (sole uncontracted auth channel); registration has no fallback (`FR-001`) | Business development (sponsor decides) | Gate 0 checklist rows 0.3 `PASS` — signed contracts/approval receipts on file, or a written sponsor decision recorded in `17-risk-management/risk-register.md` status | P0 |
| REC-13 | Run the compliance evidence program: obtain the written Central Bank position (`DEP-10`) **before any B07 money build**, then the legal opinions (`DEP-09`) and the full `AC-S-24` ten-item checklist before launch claims | `RISK-012` (`DANGEROUS` assumption `ASM-12`) kill criteria; `12-non-functional/compliance-and-legal.md` §5; `GAP-07`-adjacent legal position records | Legal liaison (sponsor decides on adverse position) | Gate 0 row 0.4 `PASS` (position on file); Gate 2 row 2.4 `PASS` (all ten `AC-S-24` deliverables signed) | P0 |
| REC-14 | Enforce gate discipline formally: quality gates non-negotiable in money paths, risk acceptance only explicitly in writing with a register status change, and `20-validation/critical-findings.md` dispositioned at every gate | `00-project-overview/stakeholders.md` conflict row; STK-01; `risk-review-process.md` §4; root README §11; RISK-005 decision rule (tests/monitoring/backups never traded) | Project sponsor + product owner | Every gate record in `21-completion/quality-gates.md` §7 shows an outcome (`PASS · PASS WITH FINDINGS · FAIL`), with findings/severities and, where applicable, written acceptances linked | P1 |
| REC-15 | Make ID and path citation discipline CI-enforced: no cited `FR`/`TC`/`BR`/`RISK`/`ASM`/`DEP`/`GAP`/`AC`/`SEC`/`REC`/`TD` ID may be absent from its owning register, and every backticked `docs/` path must resolve | Root README §5 (never cite an ID not in the register) and §11 (link validation); documentation checks D-1/D-3 of `21-completion/quality-gates.md`; `22-glossary/naming-conventions.md` already claims CI enforcement for ID patterns | DevOps lead (runs) + knowledge-base maintainer (owns rule set) | CI job fails on a dangling ID or unresolved path; a full-repo run is green after REC-03…REC-06, REC-08, REC-09 are paid down | P1 |

---

## 2. Sequencing & Precedence

1. **P0 items are Gate 0/Gate 1 preconditions**, not backlog: REC-03…REC-05 unblock the very evidence gates review (coverage audit, probe contract); REC-09 (gate evidence home) was paid 2026-09-27; REC-11…REC-13 are the sponsor-owned commercial/regulatory blockers.
2. **No recommendation may contradict canon.** Where a recommendation would change a locked number (114 TCs, 253 ACs, 7 flags, 52 production-readiness rows, 26 constraints) or a root README §9 item, the change set follows the root change-control process — update, version bump, Change History row in **both** affected documents.
3. **Effort, dates, and sprint placement are deliberately absent:** `ASM-14` baselines are not set, so sequencing is by dependency and priority only (see `21-completion/implementation-roadmap.md`).
4. **Pairing rule:** every `TD-NN` has exactly one pay-down `REC-NN` (TD-01→REC-10, TD-02→REC-02, TD-03→REC-01, TD-04→REC-03, TD-05→REC-04, TD-06→REC-05, TD-07→REC-06, TD-08→REC-07, TD-09→REC-08, TD-10→REC-09); REC-11…REC-15 address evidence gaps that are risks/assumptions rather than authored debt.
5. **Progress is measured** by the acceptance-criterion column, checked at Gate 0 (P0), Gate 1 (P0/P1), Gate 2 (P1), Gate 3 (all, including P2 cadence), alongside the `TD-NN` review (D-2).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 36,44,46,48 + charter pointer |
| 1.1 | 2026-09-27 | `REC-09` → paid (both domains authored; validator green); sequencing note 1 updated | Pay-down of `TD-10` → `REC-09` in the 2026-09-27 domain-authoring change set |
