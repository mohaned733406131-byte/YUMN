---
document_id: DOC-VAL-003
title: AUD-01 — Consistency Sweep (docs/ corpus, 433 files at sweep / 444 at publication)
category: 20-validation
status: approved
version: 1.4
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, FR-002, SEC-REQ-004]
related_documents: [DOC-ROOT-001, DOC-TPL-011, DOC-GL-003, DOC-CMP-004, DOC-AC-001, DOC-BE-006, DOC-ARCH-007, DOC-DB-005, DOC-SA-010]
---

# AUD-01 — Consistency Sweep (docs/ corpus)

| Field | Value |
|---|---|
| **Audit ID** | `AUD-01` |
| **Type** | consistency |
| **Date** | 2026-09-27 |
| **Scope** | all 433 `.md` files under `docs/` at sweep time (24 directories); ID series `DOC-*`, `AC-*`, `GAP-*`, `UC/WF/TC/BR/RISK/SEC/ASM/DEP/STK/API/DB/ADR/TST-CON`; cross-file vocabularies (order states, roles, enums, queue names, health paths, terminology) |
| **Method** | scripted sweeps (frontmatter key presence, duplicate `document_id`, `category:` vs parent directory, `status` vocabulary, `## Change History` presence, path resolution of root README §10 targets, ID-existence greps per series, per-file regex counts) + manual re-read of ~38 cited files to confirm or refute each automated hit; no result recorded without reading the cited line |
| **Auditor** | analysis-agent |

**Purpose:** the baseline register-hygiene run mandated by root README §9.4 ("record affected IDs in `20-validation/consistency-audit.md`"), `21-completion/quality-gates.md` check `G-R6`, and `18-decisions/decision-log.md:77`. This run establishes the baseline against which every later propagation is diffed.

> **Corpus note (dynamic corpus):** the sweeps ran on 433 files. Four authoring passes landed *during* this run and are reflected in the findings below rather than silently ignored: `19-traceability/` (3 files, 17:34), `20-validation/hallucination-audit.md` + `critical-findings.md` (`DOC-VAL-005`, `DOC-VAL-006`, 17:34–17:35), `20-validation/requirements-validation.md` (`DOC-VAL-007`, `AUD-07`), and `20-validation/analysis-validation.md` (`DOC-VAL-008`, `AUD-06`), plus this domain's own four files. The corpus stands at 444 `.md` files at publication; a re-run of `CHK-01…CHK-31` against the published corpus is required at the next gate (root README §11).

---

## 1. Checks (30)

| # | Check | Method | Result |
|---|---|---|---|
| `CHK-01` | All 11 required frontmatter keys present (root README §7) on every file | parse frontmatter block; 433 × 11 = 4,763 assertions | **FAIL** — 1 miss (finding 1) |
| `CHK-02` | `category:` equals parent directory name | compare per file | **PASS** — 432/432 directory files; root `README.md` uses `category: root` by design (root README §7: `<directory name>` has no directory at root) |
| `CHK-03` | `document_id` uniqueness | hash all 433 | **PASS** — 433 unique, 0 duplicates |
| `CHK-04` | `status:` vocabulary (root README §6) | value histogram | **PASS** — 433/433 `approved`, consistent with §6 ("all approved at v1.0") |
| `CHK-05` | `## Change History` present | raw-text regex per file | **FAIL** — 64 files missing (finding 2) |
| `CHK-06` | Path resolution of root README §2/§10 targets | `Test-Path` on 38 declared targets | **FAIL** (as swept) — `19-traceability/` absent (finding 3, since `RESOLVED`); 3 of 6 `20-validation/` files absent (finding 4, since `RESOLVED` — all 8 present at publication) |
| `CHK-07` | Every cited `DOC-*` has a `document_id` definition | 437 distinct cited vs 433 defined at sweep; re-run 449 vs 444 at publication; 448 vs 444 post-change-set | **PASS** (2026-09-27 change set) — at sweep: 4 hits, all meta (`21-completion/README.md:43` "must never be cited", `23-templates/use-case-template.md:22` illustrative), 0 real orphans. At publication: 5 undefined (4 meta + **`DOC-INT-010`**, finding 23). After `DOC-INT-010` → `DOC-INT-008`: 4 meta hits only, **0 real orphans** — finding 23 `RESOLVED` |
| `CHK-08` | ID series completeness vs `naming-conventions.md` §3 allocation | per-series count + contiguity | **PASS** — `UC-001…040` 40 · `WF-001…012` 12 · `BR-*` 99/99 across 14 domains · `RISK-001…024` 24 · `SEC-001…015` 15 · `ASM-01…15` 15 · `DEP-01…12` 12 · `STK-01…15` 15 · API 221 endpoints in 14 groups · entities `DB-001…018` 18 · ADR files 10 · `TST-CON-01…26` 26 |
| `CHK-09` | Test cases vs locked allocation `TC-001…TC-114` (`naming-conventions.md:84`) and vs the counts asserted in `13-testing/` | file count vs prose | **FAIL** — 103 files vs asserted "114 individual test cases" (`13-testing/README.md:86`, `:112` total row, `:29` G-TEST-1) (finding 5 → `HAL-01`, `CRIT-02`) |
| `CHK-10` | `TST-CON-NN` ↔ `C-NN` pairing | join both lists | **PASS** — 26/26 paired, 0 mismatches |
| `CHK-11` | `DOC-AC-001` declared total vs counted families | family counts | **PASS** — 94 FR + 40 NFR + 50 SR + 32 DR + 33 IR + 4 XCUT = 253 = declared |
| `CHK-12` | `AC-S-NN` coverage of the claimed "single, authoritative registry of every AC" | set difference | **FAIL** — `AC-S-04`, `AC-S-12`, `AC-S-21` absent from `DOC-AC-001` (finding 6 → `CT-11`) |
| `CHK-13` | `AC-UCnnn-nn` / `AC-WF-NNN-NN` shapes vs registry | cross-grep | **FAIL** — 121 `AC-UCnnn-nn` defined only in use-case files; `AC-WF-012-01` has 0 definitions (finding 7 → `CT-12`) |
| `CHK-14` | Flat/retired AC spellings (`naming-conventions.md:119-120`) | regex `AC-[A-Z]+-\d{2}\b` | **FAIL** — `AC-SR-16` at `15-deployment/production-readiness.md:66` (finding 8 → `CT-13`) |
| `CHK-15` | Every cited `GAP-NN` has a mint site | citation sweep vs `project-scope.md:80-85` | **FAIL** — `GAP-07` cited in 16 files, never minted (finding 9; adopted by `AUD-03`) |
| `CHK-16` | Queue-name agreement: canonical register vs consumers | name-set diff | **FAIL** — 1 of 17 consumer names matches (`finding 10 → CT-04`) |
| `CHK-17` | Order-state vocabulary (17 values) across DB, API, state machine | value-set compare | **PASS** — `constraints-and-integrity.md:84`, `03-system-analysis/state-transitions.md`, `07-api/endpoints/orders.md` agree |
| `CHK-18` | Role vocabulary across RBAC, API, data ownership | value-set compare | **PASS** — 7 identities (`CUSTOMER VENDOR COURIER ADMIN SUPER_ADMIN MODERATOR SYSTEM`) agree at `rbac.md:35`, `api-conventions.md:67`, `naming-conventions.md:97` |
| `CHK-19` | Shared enums: DB vs API (5 domains) | value-set compare | **FAIL** — 5 mismatches (finding 11 → `CT-06…CT-10`) |
| `CHK-20` | Health-probe paths vs API register vs test case | path compare | **FAIL** — 2 spellings + 1 miscitation (finding 12 → `CT-02`, `CT-03`) |
| `CHK-21` | ADR index status vs `18-decisions/ADR/` contents | file/status compare | **FAIL** — index says "directory is currently empty" (finding 13 → `CT-14`) |
| `CHK-22` | Single declared location for the GAP register | citation compare | **FAIL** — two claimed locations (finding 14 → `CT-15`) |
| `CHK-23` | Disallowed synonyms (`naming-conventions.md` §11) | `\bsellers?\b`, `\bmerchants?\b` | **FAIL** — 17 files / 30 files (finding 15 → `CT-16`) |
| `CHK-24` | `naming-conventions.md` §3.2 deviation claims vs reality | spot-verify each claim | **FAIL** — `A-07` is defined (finding 16 → `CT-17`) |
| `CHK-25` | Naming document's own examples vs canonical register | example check | **FAIL** — `b03.platform.webhook.send` vs `b13.…` (finding 17 → `CT-05`) |
| `CHK-26` | Terminology spot check (15 sampled domain terms vs `22-glossary/terminology.md`) | sample lookup | **PASS WITH FINDINGS** — 12/15 present (finding 18) |
| `CHK-27` | `<angle-bracket>` tokens outside `23-templates/` (DOC-TPL-001 §2.1) | token extraction, HTML tags excluded | **PASS WITH FINDINGS** — 88 tokens in 35 files, notation vs placeholder ambiguous (finding 19) |
| `CHK-28` | `AUD-NN` row present in root README §5 (instructed by `naming-conventions.md:91`) | read §5 | **PASS** (2026-09-27 — row added, root README v1.1; finding 20 `RESOLVED`) — at sweep: no row (finding 20) |
| `CHK-29` | `GAP-NNN` pattern width vs issued `GAP-NN` | compare §5 vs issued IDs | **FAIL** — known defect, still open (finding 21) |
| `CHK-30` | Citation volume of this directory (does the corpus expect these files?) | path-count | **PASS** — 26 / 27 / 19 / 2 / 5 / 7 / 1 files cite missing-information / contradiction / consistency / hallucination / critical-findings / analysis-validation / requirements-validation |
| `CHK-31` | Money-path status vocabularies: API values vs `payment`/`refund` enums; declared DB domain for every state column the API exposes | value-set compare + enum-register cross-check | **FAIL** — 3 defects (finding 22 → `CT-18`, `CT-19`; finding 24 → `CT-20`) |

**Results: 31 checks — 11 `PASS`, 2 `PASS WITH FINDINGS`, 18 `FAIL` (post-change-set; at sweep 9/2/20 — `CHK-07` and `CHK-28` flipped when findings 23 and 20 were fixed).**

---

## 2. Findings

| # | Finding | Severity | Where (file §section) | Evidence (IDs / tags) | Status |
|---|---|---|---|---|---|
| 1 | Required frontmatter key `related_requirements:` missing | `LOW` | `README.md` (root) frontmatter | 1 of 4,763 assertions fails; 432 other files carry the key — `VERIFIED` | `OPEN` |
| 2 | `## Change History` section absent | `MEDIUM` | 64 files: 40 use cases (`01-business-analysis/use-cases/`), 21 `functional/FR-001…FR-020.md` + `02-requirements/README.md` + `02-requirements/functional/README.md`, root `README.md`, `00-project-overview/README.md` | required by root README §9.2 and by the owning templates (`23-templates/use-case-template.md:96`) — `VERIFIED` | `OPEN` |
| 3 | Root README §10 row 40 target `19-traceability/` did not exist at sweep time | `MEDIUM` | `README.md` §10 row 40; `02-requirements/acceptance-criteria.md:17`; `00-project-overview/project-scope.md:92` | 33 files cited the path; `Test-Path` false at sweep; directory authored 2026-09-27 17:34 (`README.md`, `requirements-to-features.md`, `requirements-to-tests.md`) — `VERIFIED` | `RESOLVED` 2026-09-27 (row kept, never deleted) |
| 4 | This domain's 8 declared files were incomplete at sweep time | `INFORMATIONAL` | root README §10 rows 43/45/48 + `20-validation/README.md` §1 | `DOC-VAL-005`/`DOC-VAL-006` landed 17:34–17:35, `DOC-VAL-007` (`requirements-validation.md`, `AUD-07`) and `DOC-VAL-008` (`analysis-validation.md`, `AUD-06`) landed after the sweep — all 8 files now present (444-file corpus) — `VERIFIED` | `RESOLVED` 2026-09-27 (row kept, never deleted) |
| 5 | Test inventory asserted as 114 while 103 case files exist | `MEDIUM` | `13-testing/README.md:86`, `:112`, `:29` vs `13-testing/test-cases/` | 103 `TC-*.md` files; allocation itself is locked at 114 (`naming-conventions.md:84`, "files added incrementally"), so the *prose count* — not the allocation — is wrong; cross-graded `HAL-01` (`CRITICAL`) and `CRIT-02` (`CRITICAL`) by the sibling audits for gate impact — `VERIFIED` | `OPEN` → `HAL-01`, `CRIT-02` |
| 6 | Registry claims to be the single source of every AC but omits three `AC-S-NN` | `HIGH` | `02-requirements/acceptance-criteria.md:17` vs `00-project-overview/success-criteria.md` | `AC-S-04`, `AC-S-12`, `AC-S-21` defined only in `success-criteria.md`; 16 files cite them — `VERIFIED` | `OPEN` → `CT-11` |
| 7 | 121 `AC-UCnnn-nn` IDs live outside the registry, and the documented `AC-WF-NNN-NN` shape has no instance | `MEDIUM` | `acceptance-criteria.md:17` vs `01-business-analysis/use-cases/`; `naming-conventions.md:112` | 121 distinct `AC-UCnnn-nn` in use-case files; `AC-WF-012-01` appears once (naming doc) and never in `workflows/` (no AC section in any workflow file) — `VERIFIED` | `OPEN` → `CT-12` |
| 8 | Flat AC spelling `AC-SR-16` in production readiness | `LOW` | `15-deployment/production-readiness.md:66` (row S-4) | not present in `DOC-AC-001` v1.1 registry; pre-flagged at `naming-conventions.md:120` — `VERIFIED` | `OPEN` → `CT-13` |
| 9 | `GAP-07` cited but never minted | `MEDIUM` | `00-project-overview/project-scope.md:80-85` | 16 citing files incl. `stakeholders.md:48`, `risk-register.md:42`; now registered in `missing-information.md` §1 — `VERIFIED` | `OPEN` (source register still shows 6 rows) |
| 10 | Queue register disagrees with its consumer: 16 of 17 names unmatched | `HIGH` | `04-architecture/data-flow.md:54-70` vs `06-backend/background-processing.md:25-49` | only `b07.escrow.release` matches; block assignments also differ (`b05.inventory.release` vs `b02.inventory.expire`) — `VERIFIED` | `OPEN` → `CT-04` |
| 11 | Five DB↔API enum domains do not share a value set | `HIGH` | `08-database/constraints-and-integrity.md:85`, `:91`, `:100`, `entities/notification.md:29`, `entities/return_request.md:44` vs `07-api/endpoints/*` | `kyc_status`, `notification_category`, `ledger_type`, top-up status, `inspection_outcome` — `VERIFIED` | `OPEN` → `CT-06…CT-10` |
| 12 | Two health-probe path spellings, plus a test-case miscitation | `MEDIUM` | `15-deployment/health-checks.md:23-24`, `:36` vs `07-api/endpoints/admin.md:115-116` vs `13-testing/test-cases/TC-001.md:27` | `/healthz`+`/readyz` vs `/health/live`+`/health/ready`; `TC-001` asserts `/health/ready` although cited as the `/healthz` authority — `VERIFIED` | `OPEN` → `CT-02`, `CT-03` |
| 13 | ADR index describes an empty directory while 10 approved ADRs exist | `MEDIUM` | `04-architecture/architecture-decisions-reference.md:19`, `:25-34` vs `18-decisions/ADR/ADR-001…010.md` + `18-decisions/decision-log.md:23-30` | all 10 ADR files `status: approved`; log rows `ACCEPTED`; log itself defers re-sync to this audit — `VERIFIED` | `OPEN` → `CT-14` |
| 14 | Two documents claim to be the canonical GAP register | `MEDIUM` | root README §5:161 + `naming-conventions.md:90` vs `retention-and-archival.md:39` + `compliance-and-legal.md:88` | both claims `VERIFIED`; no precedence rule resolves them | `OPEN` → `CT-15` |
| 15 | Disallowed synonyms "seller"/"merchant" in active use | `LOW` | `naming-conventions.md:210` (§11) vs `00-project-overview/project-charter.md:42`, `project-constraints.md:43` (`C-11`), `02-requirements/requirements-overview.md` (`FR-016`) | 17 files contain `seller`, 30 contain `merchant` (includes canon rows) — `VERIFIED` | `OPEN` → `CT-16` |
| 16 | Naming document declares `A-07` undefined, but an asset register defines it | `LOW` | `naming-conventions.md:121` vs `09-security/threat-model.md:29` | `A-07` = "KYC documents & bank-transfer receipts", asset row `A-01…A-10`; series `A-NN` is absent from `naming-conventions.md` §3 — `VERIFIED` | `OPEN` → `CT-17` |
| 17 | Naming document's queue example contradicts the queue register | `LOW` | `naming-conventions.md:167` vs `06-backend/background-processing.md:48` | `b03.platform.webhook.send` vs `b13.platform.webhook.send` — `VERIFIED` | `OPEN` → `CT-05` |
| 18 | 3 of 15 sampled terms have no glossary row | `LOW` | `22-glossary/README.md:46` vs `22-glossary/terminology.md` (147 lines) | `outbox`, `saga`, `anonymization` absent; 12 present — `VERIFIED` for the sample, full-term sweep `INFERENCE` | `OPEN` |
| 19 | 88 `<angle-bracket>` tokens outside `23-templates/` (35 files) | `LOW` | DOC-TPL-001 §2.1-§2.3 | top files: `14-devops-infrastructure/backup-recovery.md` 11, `07-api/pagination.md` 9, `naming-conventions.md` 9 — `VERIFIED` count; classification as notation `INFERENCE` | `OPEN` |
| 20 | Root README §5 has no `AUD-NN` row although `naming-conventions.md:91` instructs adding one | `MEDIUM` | `README.md` §5:139-163 | series minted in `20-validation/README.md` §2 but not in the ID table — `VERIFIED` | `RESOLVED` (2026-09-27 — row added, root README v1.1) |
| 21 | `GAP-NNN` pattern (root README §5) vs issued `GAP-NN` width | `LOW` | `README.md` §5:161 vs issued IDs `GAP-01…GAP-12` | pre-logged at `naming-conventions.md:118` for root README — `VERIFIED` | `OPEN` |
| 22 | Money-path status values do not reconcile between API and schema (payment release, refund receipt) | `MEDIUM` | `07-api/endpoints/wallet.md:34`, `:40` vs `08-database/entities/payment.md:33`, `:60` | `status: "RELEASED"` ∉ `payment_state {PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED}` (`constraints-and-integrity.md:85`) — though it *is* a legal `escrow_state` (`entities/escrow.md:32`), and no mapping is documented for a `paymentId`-keyed response; refund `status PENDING\|COMPOSED\|CREDITED` ∉ `refund.state {PENDING, PROCESSING, COMPLETED, FAILED}` — `VERIFIED` | `OPEN` → `CT-18`, `CT-19` |
| 23 | Cited document ID `DOC-INT-010` is never defined | `MEDIUM` | `19-traceability/requirements-to-tests.md:46`, `:215-247`, `:294` vs `10-integrations/*.md` | 29 citations of `DOC-INT-010` (linked to `10-integrations/testing-and-sandboxes.md`) but the highest defined integration ID is `DOC-INT-008` (`testing-and-sandboxes.md` itself); breaks root README §11 check `D-3` "No cited ID absent from its owning register" — `VERIFIED` | `RESOLVED` (2026-09-27 — 29 citations corrected to `DOC-INT-008`, `requirements-to-tests.md` v1.1) |
| 24 | `payout` state column has no declared enum domain while the API publishes a five-value status set | `MEDIUM` | `07-api/endpoints/wallet.md:37-38` vs `08-database/indexes-and-performance.md:138-139`; `constraints-and-integrity.md:84-100` | `constraints-and-integrity.md` declares `payment_state` (:85) and `escrow_state` (:87) but no `payout_state`; the only documented payout `state` value anywhere is the partial index `WHERE state='ELIGIBLE'`, which the API status set (`REQUESTED\|SCHEDULED\|EXECUTED\|REJECTED\|ROLLED_OVER`) cannot express — `VERIFIED` | `OPEN` → `CT-20` |
| 25 | Sibling audit cites baseline statistics that the v1.1 re-run superseded | `MEDIUM` | `20-validation/analysis-validation.md:89` (AVF-10), `:109` (AUD-01 row) vs this file §2/§5 | `AVF-10` states "`CT-02`…`CT-17` contradictions, … consistency sweep 17/30 checks failed"; `:109` states "17 of 30 checks failed" — current: `CT-02…CT-20`, 20 of 31 failed — `VERIFIED` | `RESOLVED` (2026-09-27 — `analysis-validation.md` v1.1 re-synced: `CT` range, 18/31, open-findings total) |

Severity distribution: `HIGH` 3 · `MEDIUM` 13 · `LOW` 8 · `INFORMATIONAL` 1 (25 findings; 20 `OPEN`, 5 `RESOLVED` — findings 3, 4, 20, 23, 25).

---

## 3. What passed (so the baseline is not read as uniformly broken)

Frontmatter presence (4,762/4,763), ID uniqueness, status vocabulary, ID-series completeness (12 series, all contiguous to their allocation), constraint-test pairing (26/26), AC registry arithmetic (253), order-state vocabulary (17), role vocabulary (7), `DOC-*` citation integrity *at sweep time* (4 hits, all meta — overturned at publication by finding 23, since `RESOLVED`), endpoint count vs allocation (221/221), and this directory's citation volume (19–27 files per file expected).

---

## 4. Change-Propagation Log (root README §9.4)

| Date | Owning document changed | Affected IDs | Re-run of | Result |
|---|---|---|---|---|
| 2026-09-27 | — (baseline run; no owning document edited by this audit) | `AUD-01`, findings 1–22 | all 31 checks | baseline recorded |
| 2026-09-27 17:34 | `19-traceability/` authored (3 files); `20-validation/hallucination-audit.md` + `critical-findings.md` authored in parallel | finding 3 → `RESOLVED`; finding 4 narrowed to 2 files; `HAL-01…HAL-13`, `CRIT-01…CRIT-10` minted by the sibling audits and cross-linked from findings 5, 11, 13 | `CHK-06` re-run | `19-traceability/` resolves; `20-validation/` 6 of 8 files present |
| 2026-09-27 (post-publication) | `20-validation/requirements-validation.md` (`DOC-VAL-007` / `AUD-07`) authored; `19-traceability/requirements-to-tests.md` cites `DOC-INT-010` | finding 4 → 1 file absent (`DOC-VAL-008`); new finding 23 (`DOC-INT-010` undefined) | `CHK-06`, `CHK-07` re-run | `CHK-06` 7 of 8 present; `CHK-07` flips `PASS` → `FAIL` (1 real orphan) |
| 2026-09-27 (post-publication) | `20-validation/analysis-validation.md` (`DOC-VAL-008` / `AUD-06`) authored — all 8 domain files present | finding 4 → `RESOLVED`; `DOC-VAL-008` no longer a forward-only citation | `CHK-06`, `CHK-07` re-run | corpus 444; `CHK-07` undefined set = 4 meta + `DOC-INT-010` |
| 2026-09-27 (post-publication) | this file bumped 1.0 → 1.1 (statistics) and 1.1 → 1.2 (domain completion) | finding 25 raised: `analysis-validation.md:89`, `:109` quote the superseded 17/30 baseline | cross-reference read | stale statistics recorded, owning file not edited here |
| 2026-09-27 (registration change set) | root `README.md` v1.1 (§5 `AUD-NN` row); `22-glossary/naming-conventions.md` v1.1; `23-templates/validation-audit-template.md` v1.1; `19-traceability/requirements-to-tests.md` v1.1 (`DOC-INT-010` → `DOC-INT-008`, 29 citations); `20-validation/analysis-validation.md` v1.1 (statistics re-synced); `21-completion/technical-debt.md` v1.1 (`TD-10` → `PAID`); `21-completion/recommendations.md` v1.1 (`REC-09` paid) | findings 20, 23, 25 → `RESOLVED`; `TD-10`/`REC-09` closed | `CHK-07`, `CHK-28` re-run | both flip to `PASS`; results now 11/2/18; finding count 20 `OPEN` |

Each later row must name the file that changed, its new `version`, the finding/CT IDs it closes, and the checks re-run. Findings are never deleted when closed — status flips to `RESOLVED` with the closing date (DOC-TPL-011 checklist #3).

---

## 5. Coverage & Statistics

- Files examined: **433 of 433** at sweep time (100% automated sweeps) · **~38** manually re-read for evidence confirmation · corpus **444** files at publication (see corpus note).
- Checks run: **31** — passed 11, passed-with-findings 2, failed 18 (post-change-set; at sweep 9/2/20).
- Findings: **25** — `HIGH` 3 · `MEDIUM` 13 · `LOW` 8 · `INFORMATIONAL` 1; 20 `OPEN`, 5 `RESOLVED`.
- ID references verified: **448** distinct `DOC-*` cited / **444** defined post-change-set — 4 undefined, all meta (was 4 meta + `DOC-INT-010`; finding 23 `RESOLVED`) · **24** `AC-S-*` cited, 21 inside the registry · **12** `GAP-*` registered (was 6 mint sites) · 0 undefined `FR/NFR/SEC-REQ/DATA-REQ/INT-REQ/BR/C/ASM/DEP/RISK/ADR` citations found in the sampled series.
- Terms/IDs in scope: `DOC-*` 449 cited · `UC-*` 40 · `WF-*` 12 · `TC-*` 103 files (114 asserted) · `BR-*` 99 · `RISK-*` 24 · `SEC-*` 15 · `ASM-*` 15 · `DEP-*` 12 · `STK-*` 15 · `API-*` 221 · `DB-*` 18 · `ADR-*` 10 · `TST-CON-*` 26 · `GAP-*` 12 · `AUD-*` 7 · `AC-*` 253 + 121 UC-scoped.

---

## 6. Verdict & Sign-off

- **Gate:** `PASS WITH FINDINGS` (root README §11) — no `CRITICAL` finding; every finding has owner, severity, evidence tag and a named owning document, so the corpus is usable and each defect is dispositionable. It is **not** `FAIL` because no finding blocks the analysis itself; it is **not** `PASS` because 18 of 31 checks failed (post-change-set; 20 at sweep).
- **Unresolved contradictions / gaps:** `CT-02…CT-20` (`contradiction-audit.md`), `GAP-01…GAP-12` (`missing-information.md`), findings 1–25 above (20 `OPEN`, 5 `RESOLVED`).
- **Required follow-up — edits needed elsewhere, NOT made by this audit:** (a) root README §5 — `AUD-NN` row added 2026-09-27 (finding 20 `RESOLVED`); `GAP-NNN` width still open (finding 21); (b) root README §7 example — add `related_requirements: []` (finding 1); (c) root `README.md` §10 row 40 — `19-traceability/` now exists, verify the row (finding 3, `RESOLVED`); (d) `02-requirements/acceptance-criteria.md` — reconcile `AC-S-04/12/21` and the 121 `AC-UCnnn-nn` (findings 6, 7); (e) `04-architecture/data-flow.md` — restate queues from the canonical register (finding 10); (f) `04-architecture/architecture-decisions-reference.md` §1 — re-sync statuses (finding 13); (g) the 64 files missing `## Change History` (finding 2); (h) `22-glossary/` — three term rows + the `A-07` claim (findings 16, 18); (i) `13-testing/README.md:29`, `:86`, `:112` — correct the asserted TC count (finding 5); (j) `19-traceability/requirements-to-tests.md` — `DOC-INT-010` corrected to `DOC-INT-008` (finding 23, `RESOLVED`); (k) `07-api/endpoints/wallet.md` + `08-database/entities/payment.md` + `constraints-and-integrity.md` — reconcile the money-path status sets and declare a `payout_state` domain (findings 22, 24); (l) `20-validation/analysis-validation.md:89`, `:109` — statistics re-synced in v1.1 (finding 25, `RESOLVED`).
- **Sign-off:** analysis-agent, 2026-09-27.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Baseline sweep: 30 checks, 21 findings, propagation log opened | Root README §9.4; `quality-gates.md` check `G-R6`; root README §10 |
| 1.1 | 2026-09-27 | Post-publication re-run: corpus 433 → 443; `CHK-07` flips to `FAIL`; `CHK-09` promoted to `FAIL`; `CHK-31` added (31 checks: 9/2/20); finding 3 → `RESOLVED`; finding 4 narrowed; finding 5 re-graded `MEDIUM` + cross-links `HAL-01`/`CRIT-02`; findings 22–24 added; verdict/follow-up re-issued | Findings never deleted (DOC-TPL-011 #3); sibling authoring passes landed during the run |
| 1.2 | 2026-09-27 | `analysis-validation.md` (`DOC-VAL-008`) authored: finding 4 → `RESOLVED`; corpus 444; `CHK-07` undefined set reduced to 4 meta + `DOC-INT-010`; propagation log row added | Sibling authoring pass completed the domain's 8 declared files |
| 1.3 | 2026-09-27 | Finding 25 added: `analysis-validation.md:89`, `:109` still quote the v1.0 baseline (17/30, `CT-02…CT-17`) | §9.4 propagation — consumer statistics superseded by the v1.1 re-run; owning file not edited here |
| 1.4 | 2026-09-27 | Registration change set: findings 20, 23, 25 → `RESOLVED`; `CHK-07`, `CHK-28` → `PASS` (results 11/2/18); stats re-run (448 cited, 4 undefined meta-only); propagation row added | Owning files changed in the same set: root README v1.1, naming-conventions v1.1, template v1.1, requirements-to-tests v1.1, analysis-validation v1.1, technical-debt v1.1, recommendations v1.1 |
