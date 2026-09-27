---
document_id: DOC-VAL-005
title: AUD-04 — Hallucination Audit (unsupported claims across docs/)
category: 20-validation
status: approved
version: 1.0
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-015, FR-016, FR-017, FR-020, NFR-015]
related_documents: [DOC-ROOT-001, DOC-REQ-001, DOC-AC-001, DOC-TST-001, DOC-TST-006, DOC-ARCH-010, DOC-BA-005, DOC-CMP-004]
---

# AUD-04 — Hallucination Audit (unsupported claims across docs/)

| Field | Value |
|---|---|
| **Audit ID** | AUD-04 |
| **Type** | hallucination (incorrect / unsupported claims) |
| **Date** | 2026-09-27 |
| **Scope** | All `*.md` files under `docs/` — 433 present when claims were extracted, 444 after `19-traceability/` and `20-validation/` landed: completeness/count/provenance claims, `every`/`all`/`zero gaps`/`not yet authored` assertions, AC/BR/TC/ADR ID inventories |
| **Method** | Claim extraction by pattern sweep; mechanical re-count of every numeric claim (file-system counts, regex ID extraction from owning registers); set-difference of ID sequences; path-resolution pass (root README §11) |
| **Auditor** | analysis-agent |

This register records statements across `docs/` that assert a fact about the document set itself (counts, emptiness, completeness, provenance, "not yet authored", "every", "zero gaps") and then checks that assertion against the artifact set on disk. It is a **write-only audit**: findings are recorded here with evidence; fixing the cited documents is left to their owning domains (root README §11: no silent changes — each fix is an explicit edit by the owning author).

Claims about cross-document *content* contradictions live in `20-validation/contradiction-audit.md` (CT-NN series); missing information lives in `20-validation/missing-information.md` (GAP-NNN series); register-wide hygiene lives in `20-validation/consistency-audit.md`. Where this audit touches those areas it cross-references instead of duplicating.

---

## 1. Method

1. **Claim extraction.** Every `*.md` in `docs/` (433 files at audit time) was scanned for absolute completeness/count claims: numbers of test cases, ADRs, requirements, rules, acceptance criteria; phrases `every`, `all`, `zero gaps`, `not yet authored`, `not yet created`, `currently empty`, `single, authoritative registry`, provenance statements (`archived under`, `structure came from`).
2. **Mechanical re-count.** Each numeric claim was recomputed from the file system or from the cited register file (file counts, ID sequences extracted by regex from the owning register, frontmatter extraction).
3. **Classification.** Each claim is tagged `VERIFIED` (re-count matches), `INFERENCE` (supported but not mechanically provable), or `INSUFFICIENT EVIDENCE` (artifact absent).
4. **No fixes.** This file never edits the cited document. Remediation is named per finding.

Evidence tags and severities follow root README §9/§10: `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`; gate outcomes `PASS · PASS WITH FINDINGS · FAIL`.

---

## 2. Findings register

| ID | Severity | Claim under audit | Re-count result | Evidence | Status |
|---|---|---|---|---|---|
| HAL-01 | CRITICAL | "114 test cases (`TC-001`…`TC-114`)" — `13-testing/README.md:86`, `:88`, `:111`, `:112`, `:29`; `13-testing/test-cases/README.md:15`, `:64`, `:65`, `:86`, `:102` | **False**: `13-testing/test-cases/` holds 104 files = `README.md` + `TC-001.md`…`TC-103.md` (103 test cases) | VERIFIED (mechanical directory count, 2026-09-27) | OPEN |
| HAL-02 | HIGH | "none of the ADR files listed below exist yet … the directory is currently empty" — `04-architecture/architecture-decisions-reference.md:19`; §1 statuses `RESERVED — not yet written` (`:25`–`:34`) | **False**: `18-decisions/ADR/` holds `ADR-001.md`…`ADR-010.md` (10 files); `18-decisions/decision-log.md:77` already records that the index "must be re-synced" | VERIFIED | OPEN |
| HAL-03 | HIGH | Provenance: structure "came from `archdoc.md`" and content was "archived … under `archive/` at the repository root" — `docs/README.md:33`, `docs/README.md:35`; repeated in `21-completion/recommendations.md:29` and `21-completion/technical-debt.md:35` | **Unsupported**: `E:\YUMN\archdoc.md` is 0 bytes; `E:\YUMN\archive\` does not exist | INSUFFICIENT EVIDENCE (source artifact empty, archive absent) | OPEN |
| HAL-04 | HIGH | Test cases cite business rules `BR-INV-01`…`BR-INV-05` — `13-testing/test-cases/TC-018.md:51,61,62`, `TC-019.md:50,52,61,62`, `TC-020.md:49,61` | **Undefined IDs**: `01-business-analysis/business-rules.md` defines 99 rules across 14 prefixes (`AUTH, CAT, CRT, ESC, FIN, NTF, ORD, PAY, PLT, PRM, RET, REV, SHP, VND`); no `BR-INV-*` domain exists | VERIFIED (regex over owning register) | OPEN |
| HAL-05 | HIGH | `FR-015`…`FR-020` acceptance criteria carry the same IDs as the registry but **different text** — files vs `02-requirements/acceptance-criteria.md` | **16 of 24** cited AC entries disagree with the registry row of the same ID (FR-015 4/4, FR-017 4/4, FR-018 3/4, FR-019 2/4, FR-020 2/4, FR-016 1/4). Example: `FR-015.md` `AC-FR015-01` = code→DELIVERED; registry `AC-FR015-01` = fee computation (fee criterion dropped entirely) | VERIFIED (ID-by-ID text comparison) | OPEN |
| HAL-06 | MEDIUM | "single, authoritative registry of every acceptance criterion (`AC-*`)" — `02-requirements/acceptance-criteria.md:17` | **Incomplete**: the registry never mentions `AC-S-04`, `AC-S-12`, `AC-S-21` (21 of 24 success criteria referenced). `AC-S-04` (UAT sign-off) is consumed as a gate criterion by `21-completion/quality-gates.md:139` and cited by `02-requirements/non-functional/NFR-015.md` — neither of which the registry covers | VERIFIED (set difference of ID sequences) | OPEN |
| HAL-07 | MEDIUM | Registry defines 5 ACs for 14 functional requirements; every FR file cites exactly 4 (`02-requirements/functional/README.md:61` codifies `-01 … -04`) | **14 registry ACs never cited**: 94 `AC-FR*` rows defined vs 80 distinct cited across the 20 FR files (the `-05` row of FR001, 002, 003, 004, 006, 008, 009, 010, 011, 012, 013, 014, 015, 017) | VERIFIED (regex counts, both sides) | OPEN |
| HAL-08 | MEDIUM | Requirement files restate the registry's parenthetical rule ID: `02-requirements/integration/INT-REQ-006.md:17` quotes `(BR-PLT-05)`; `INT-REQ-002.md:17` quotes `(BR-PAY-07)` | **Misquotes**: `02-requirements/requirements-overview.md:130` says `(BR-PLT-02)` and `:126` says `(BR-PAY-04)`. (`BR-PLT-05` is the Arabic-localisation rule; `BR-PAY-07` is the refund-credit rule.) Both files carry a corrective "Rule text of record" line — the summary and the quote still disagree | VERIFIED | OPEN |
| HAL-09 | MEDIUM | "`07-api/` — not yet authored", "`08-database/` — not yet authored", "`13-testing/` — not yet authored" — `04-architecture/README.md:70`, `:71`, `:72` and `03-system-analysis/README.md:82`, `:83`, `:84` | **Stale**: those domains hold 19, 25 and 109 files respectively; `API-*` (221 IDs), `DB-*` and `TC-*` registries all exist | VERIFIED | OPEN |
| HAL-10 | MEDIUM | Completeness assertions computed over a domain that does not exist: "traceability with 0 gaps" — `13-testing/README.md:29` (G-TEST-1); "`114 TCs → FR families` … traceability" — `13-testing/test-cases/README.md:86`, `:104`; "`19-traceability/`" citations in `02-requirements/acceptance-criteria.md:502`, `00-project-overview/success-criteria.md:25` | **Unsupported at audit time**: `docs/19-traceability/` absent (0 files), so no matrix exists that could establish "0 gaps" | INSUFFICIENT EVIDENCE (asserted about a non-existent artifact) | OPEN |
| HAL-11 | LOW | "…when that register is authored" phrasings for `20-validation/` — `16-data/retention-and-archival.md:39`, `12-non-functional/compliance-and-legal.md:88`, `22-glossary/naming-conventions.md:91` ("`20-validation/` (domain not yet created)"), `23-templates/validation-audit-template.md:32`, `21-completion/quality-gates.md:35` ("declared in root README §2 but not yet authored") | **Self-expiring**: `20-validation/` is being authored in parallel with this audit; these sentences become false the moment the domain lands and must be re-checked at the next gate (root README §11 link pass) | VERIFIED at audit time (domain empty when scanned) | OPEN |
| HAL-12 | LOW | Path citations that cannot resolve: `00-project-overview/actors-and-roles.md:81` cites `07-api/authorization.md` (no such file — the domain has `07-api/endpoints/auth.md` and `06-backend/authorization.md`); `22-glossary/naming-conventions.md:36,37,38,148` cite `use-cases/UC-040.md`, `workflows/workflow-012.md`, `entities/wallet_transaction.md`, `endpoints/orders.md`, `endpoints/wallet.md`, `entities/return_request.md` without a domain prefix; `23-templates/{requirement,test-case,use-case,workflow}-template.md:17` cite `functional/FR-013.md`, `test-cases/TC-001.md`, `use-cases/UC-001.md`, `workflows/workflow-001.md` the same way | **11 citations broken** under root README §11 ("every path cited … resolves") | VERIFIED (path resolution pass, 2026-09-27) | OPEN |
| HAL-13 | LOW | "Documentation Status: APPROVED — analysis complete" — `docs/README.md:22`, alongside a domain map that lists `19-traceability/` and `20-validation/` (`docs/README.md:62`, `:63`) as if present | **Premature at audit time**: both domains were absent when scanned (their README links broken); status is only defensible once the two domains land | VERIFIED at audit time | OPEN |

Severity totals: **CRITICAL 1 · HIGH 4 · MEDIUM 5 · LOW 3 = 13 open findings.**

---

## 3. Finding detail

### HAL-01 — Test-case count "114" vs 103 on disk (CRITICAL)

- **Claim:** `13-testing/README.md:29` ("114 TCs mapped to FR families; traceability with 0 gaps"), `:86` ("114 individual test cases (`TC-001`…`TC-114`)"), `:88` (§5 "Locked Test-Case Allocation (`TC-001 … TC-114`)"), `:111`–`:112` (row `TC-105–114`, total `114`); mirrored in `13-testing/test-cases/README.md:15`, `:64`–`:65`, `:86`, `:102`; consumed by `13-testing/test-plans.md:44` (PLAN-18 targets `TC-105–114`).
- **Evidence:** directory listing of `13-testing/test-cases/` = 104 files (1 `README.md` + `TC-001.md` … `TC-103.md`). No `TC-104.md`…`TC-114.md` exists.
- **Why it matters:** the locked allocation assigns FR-020 (platform administration/moderation/audit) a block `TC-105–114` that does not exist, so FR-020's ACs have **zero** test cases in the locked plan; PLAN-18 has no cases to execute; `AC-S-01`/`AC-S-03` (0-gap traceability) cannot be evidenced from an overstated inventory.
- **Remediation owner:** author of `13-testing/`. Recorded, not fixed, here (see `20-validation/critical-findings.md` CRIT-02 for the gate impact).

### HAL-02 — ADR index says "currently empty" while 10 ADRs exist (HIGH)

- **Claim:** `04-architecture/architecture-decisions-reference.md:19` ("none of the ADR files listed below exist yet … the directory is currently empty") and every §1 row status `RESERVED — not yet written` / `RESERVED — cited by …` (`:25`–`:34`), plus the lifecycle note at `:40` ("no other decision may take `ADR-001…ADR-010` … start at `ADR-011`").
- **Evidence:** `18-decisions/ADR/` contains `ADR-001.md` … `ADR-010.md` (10 files). `18-decisions/decision-log.md:77` and `18-decisions/README.md:61`–`:70` already list them.
- **Note:** `18-decisions/decision-log.md:77` self-reports the drift ("the index shows RESERVED — the index must be re-synced"), so the contradiction is known but unresolved.

### HAL-03 — `archdoc.md` / `archive/` provenance unsupported (HIGH)

- **Claim:** `docs/README.md:33` (structure came from `archdoc.md`), `docs/README.md:35` (earlier content "archived … under `archive/` at the repository root"), `21-completion/recommendations.md:29` and `21-completion/technical-debt.md:35` (both cite `archdoc.md` as a live artifact).
- **Evidence:** `E:\YUMN\archdoc.md` = 0 bytes; `E:\YUMN\archive\` does not exist. The provenance chain is asserted but the referenced artifacts carry no content.

### HAL-04 — `BR-INV-01…05` cited but never defined (HIGH)

- **Claim:** three money-adjacent test cases assert business rules `BR-INV-01`…`BR-INV-05`.
- **Evidence:** `01-business-analysis/business-rules.md` defines 99 rules; grep of the register returns zero `BR-INV-*`. The owning register has no inventory-rule domain at all.
- **Gate angle:** violates `21-completion/quality-gates.md:59` (D-3: "No cited `FR`/`TC`/`BR`/`RISK`/`ASM`/`DEP`/`GAP`/`AC`/`SEC` ID is absent from its owning register").

### HAL-05 — FR-015…FR-020 acceptance criteria rewritten vs the registry (HIGH)

Six requirement files cite AC IDs whose text no longer matches `02-requirements/acceptance-criteria.md`:

| FR file | Mismatched AC entries | Detail |
|---|---|---|
| `FR-015.md` | 4 / 4 | file `AC-FR015-01` = code→DELIVERED; registry `AC-FR015-01` = fee computation — the fee criterion is not cited anywhere in the file |
| `FR-017.md` | 4 / 4 | all four renumbered; registry `AC-FR017-05` (opt-out) never cited |
| `FR-018.md` | 3 / 4 | file `AC-FR018-04` = DLQ alert; that criterion is absent from the registry |
| `FR-019.md` | 2 / 4 | — |
| `FR-020.md` | 2 / 4 | file `AC-FR020-02` = moderator denial (not in registry); registry `AC-FR020-04` = settings precedence (not cited) |
| `FR-016.md` | 1 / 4 | file `AC-FR016-02` = period elapsed; registry `AC-FR016-02` = state flow |

- **Consequence:** the same ID denotes two different tests depending on which document you read — coverage measured against the registry (Gate 1 check `1.3`, `21-completion/quality-gates.md:105`) will not match what the requirement file asks for.

### HAL-06 — "registry of every acceptance criterion" omits three success criteria (MEDIUM)

- `02-requirements/acceptance-criteria.md:17` claims to be the single authoritative registry of every `AC-*`.
- Mechanical counts (VERIFIED): 253 ACs = 94 `AC-FR` + 40 `AC-NFR` + 50 `AC-SR` + 32 `AC-DR` + 33 `AC-IR` + 4 `AC-XCUT` — the count claim itself is **true**.
- But `00-project-overview/success-criteria.md` defines `AC-S-01`…`AC-S-24`, and the registry references only 21 of them: **`AC-S-04`, `AC-S-12`, `AC-S-21` never appear.** `AC-S-04` is a Gate 2 evidence item (`quality-gates.md:139`) and is cited by `NFR-015.md` as though it were registry-covered.

### HAL-07 — 14 registry FR acceptance criteria are orphaned (MEDIUM)

- Defined vs cited (both sides regex-counted): **94 defined / 80 distinct cited**; every FR file cites exactly 4 ACs; `02-requirements/functional/README.md:61` codifies the `-01 … -04` pattern as house style, which is why the `-05` rows of FR001, FR002, FR003, FR004, FR006, FR008, FR009, FR010, FR011, FR012, FR013, FR014, FR015, FR017 are never cited by their own requirement file.
- NFR (40/40), SR (50/50), DR (32/32) and IR (33/33) citation counts **match** their registry sections exactly — the gap is functional-only.

### HAL-08 — Requirement files misquote the registry's rule IDs (MEDIUM)

`INT-REQ-006.md:17` presents `(BR-PLT-05)` as the registry parenthetical (registry `requirements-overview.md:130` = `(BR-PLT-02)`); `INT-REQ-002.md:17` presents `(BR-PAY-07)` (registry `:126` = `(BR-PAY-04)`). Both files carry a corrective "Rule text of record" line, so the correction exists but the summary line still misquotes its own registry — a reader skimming headers gets the wrong rule.

### HAL-09 — "not yet authored" stale across three domains (MEDIUM)

`04-architecture/README.md:70`–`:72` and `03-system-analysis/README.md:82`–`:84` still describe `07-api/`, `08-database/` and `13-testing/` registries as not authored, while those domains hold 19 / 25 / 109 files and the registries are actively cited (221 `API-*` IDs, `DB-*` entity set, `TC-*` cases). The same sentences also warn never to cite an endpoint ID "that is not in that registry" — advice anchored to a domain the text says does not exist.

### HAL-10 — "zero gaps" computed over an absent domain (MEDIUM)

`13-testing/README.md:29` reports G-TEST-1 as "traceability with 0 gaps"; `test-cases/README.md:104`, `acceptance-criteria.md:502` and `success-criteria.md:25` point at `19-traceability/*` for the underlying matrix. At audit time `19-traceability/` had zero files, so no artifact supports the "0 gaps" figure. (If the matrix later exists and is green, this finding closes; re-check at the gate.)

### HAL-11 — Self-expiring "not yet authored" phrasing (LOW)

Five documents phrase `20-validation/` as a future event (`retention-and-archival.md:39`, `compliance-and-legal.md:88`, `naming-conventions.md:91`, `validation-audit-template.md:32`, `quality-gates.md:35`). This audit is authored in parallel with `20-validation/README.md`, `missing-information.md`, `consistency-audit.md` and `contradiction-audit.md`; on completion these sentences are stale and must be swept in the next link/consistency pass.

### HAL-12 — Eleven path citations that never resolve (LOW)

Verified broken (root README §11 rule): `actors-and-roles.md:81` → `07-api/authorization.md`; `naming-conventions.md:36` ×2, `:37` ×2, `:38` ×2, `:148` (six domain-less example paths); `requirement-template.md:17`, `test-case-template.md:17`, `use-case-template.md:17`, `workflow-template.md:17` (four domain-less example paths). Full link-pass numbers live in `20-validation/analysis-validation.md`.

### HAL-13 — "APPROVED — analysis complete" while two domains are empty (LOW)

`docs/README.md:22` declares the documentation set complete and ready for implementation planning while `19-traceability/` and `20-validation/` are (at audit time) absent — the map rows at `docs/README.md:62`–`:63` link to files that do not yet exist. Re-check after both domains land.

---

## 4. What this audit does not cover

- **Content contradictions between documents** (enum drift, queue drift, status mismatches) → `20-validation/contradiction-audit.md` (CT-NN series). CRITICAL money-path instances are rolled up in `20-validation/critical-findings.md`.
- **Missing information / open product decisions** → `20-validation/missing-information.md` (GAP-NNN series; seed list in `00-project-overview/project-scope.md:80`–`:85` + `GAP-07` in `00-project-overview/stakeholders.md:48`).
- **Register hygiene and silent changes** → `20-validation/consistency-audit.md`.
- **Requirement quality (7-question test)** → `20-validation/requirements-validation.md` (AUD-07).
- **Whole-corpus readiness scorecard** → `20-validation/analysis-validation.md` (AUD-06).

---

## Coverage & Statistics

- **Files examined:** 433 of 433 `docs/**/*.md` at extraction time (100% pattern sweep; corpus is 444 after this domain + `19-traceability/` landed); deep reads: `13-testing/` (both READMEs + `test-cases/` inventory), `18-decisions/ADR/` (10 files), `04-architecture/architecture-decisions-reference.md`, `02-requirements/acceptance-criteria.md`, `00-project-overview/success-criteria.md`, `01-business-analysis/business-rules.md`, `FR-015`…`FR-020`, `INT-REQ-002/006`, `NFR-015`, root `README.md`
- **Checks run:** 13 claim checks + 2 path-resolution passes — 13 claim checks **all failed** (that is what this register records); link pass #1 (before this domain existed): 1,397 citations, 131 broken (112 → then-absent `20-validation/*`, 19 elsewhere); link pass #2 (final, after this domain landed): **1,728 citations, 30 broken — 12 are the evidence strings quoted verbatim in HAL-12 below, 5 belong to sibling `20-validation/` files, 13 elsewhere** (of which 11 are HAL-12's original locations and 2 are `19-traceability/README.md` internal paths). Breakdown of record in `20-validation/analysis-validation.md`
- **ID references verified:** `AC-FR*` 94 defined / 80 cited · `AC-NFR*` 40/40 · `AC-SR*` 50/50 · `AC-DR*` 32/32 · `AC-IR*` 33/33 · `AC-XCUT*` 4/4 · `AC-S-*` 24 defined / 21 referenced · `BR-*` 99 defined, `BR-INV-*` 5 cited / 0 defined · `TC-*` 114 claimed / 103 exist · `ADR-*` 10 claimed-written / 10 exist · `SEC-*` 15 defined (claim of 15 in `17-risk-management/README.md:21` is correct — checked, no finding)
- **Terms/IDs in scope:** `TC-*` 114/103 · `ADR-*` 10 · `AC-*` 253 (+24 `AC-S-*`) · `BR-*` 99 · `FR-*` 20 · `AUD-NN` 6 sanctioned (DOC-TPL-011) · 26 `C-*` constraints · 24 `RISK-*` · 12 `GAP-*` (`GAP-01`…`GAP-07` seeded in `00-project-overview/`, `GAP-08`…`GAP-12` minted by AUD-03 in `20-validation/missing-information.md`)

## Verdict & Sign-off

- **Gate:** `PASS WITH FINDINGS` (root README §11) — the audit itself is complete and reproducible; 13 findings are open in the audited corpus, 1 of them CRITICAL (HAL-01) and 4 HIGH
- **Unresolved contradictions / gaps:** HAL-01…HAL-13 all `OPEN`; CRIT roll-ups at `20-validation/critical-findings.md` (CRIT-02, CRIT-05, CRIT-06, CRIT-08); GAP series owned by `20-validation/missing-information.md` — no GAP rows minted here
- **Required follow-up:** `13-testing/` (HAL-01), `04-architecture/` (HAL-02, HAL-09), `docs/README.md` + `21-completion/` (HAL-03), `01-business-analysis/` + `13-testing/test-cases/` (HAL-04), `02-requirements/functional/` + `acceptance-criteria.md` (HAL-05, HAL-06, HAL-07), `02-requirements/integration/` (HAL-08), `03-system-analysis/` (HAL-09), `13-testing/` + `00-project-overview/` (HAL-10), domain authors named in HAL-11…HAL-13 — root README §9.5: fixes are propagated by the owning document, never locally
- **Sign-off:** analysis-agent (author), 2026-09-27 — sponsor/QA countersignature recorded with the Gate 0 review (`21-completion/quality-gates.md` §3)

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 43,45,48 + DOC-REQ-001 |
