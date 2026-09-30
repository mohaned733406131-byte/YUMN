---
document_id: DOC-VAL-006
title: AUD-05 — Critical Findings (money-path and gate-blocking)
category: 20-validation
status: approved
version: 1.6
created: 2026-09-27
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-014, FR-016, FR-017, FR-020, NFR-015, SEC-REQ-009, DATA-REQ-004, INT-REQ-001, INT-REQ-002]
related_documents: [DOC-ROOT-001, DOC-OVR-003, DOC-OVR-009, DOC-OVR-010, DOC-OVR-011, DOC-AC-001, DOC-TST-001, DOC-BE-006, DOC-ARCH-007, DOC-API-013, DOC-CMP-004, DOC-CMP-010]
---

# AUD-05 — Critical Findings (money-path and gate-blocking)

| Field | Value |
|---|---|
| **Audit ID** | AUD-05 |
| **Type** | critical-findings (gate-blocking / money-path) |
| **Date** | 2026-09-27 |
| **Scope** | All Gates 0–3 entry criteria and checklists in `../../21-completion/core/quality-gates.md`; every money-path document (`07-api/{wallet,orders,notifications}.md`, `../../06-backend/core/background-processing.md`, `../../04-architecture/core/data-flow.md`, `08-database/{constraints-and-integrity.md,entities/payment.md}`); prerequisite registers `00-project-overview/{dependencies,assumptions,project-charter,success-criteria}.md`; test inventory `13-testing/` |
| **Method** | Gate-criteria extraction then per-row verification against owning registers; API-contract vs DB-enum diff (3 money-path resources); dual-owner queue-inventory diff (25 vs 17); AC coverage recomputation; dependency/assumption status read from register rows |
| **Auditor** | analysis-agent |

This register lists the findings that block or endanger a quality gate (`../../21-completion/core/quality-gates.md`) or a money-path feature (checkout, top-up, payment, escrow, refund, payout, ledger, notification delivery). It is the **standing input** named at `quality-gates.md:35` and `quality-gates.md:50` (G-R6): open critical items must be dispositioned before the next gate.

Findings are **recorded, not fixed** here (root README §11 — audits never edit the audited document). Each row states the gate it blocks and the evidence that would clear it. Detailed evidence trails: `hallucination-audit.md` (HAL-NN), `requirements-validation.md` (AUD-07), `analysis-validation.md` (AUD-06), plus the sibling registers `contradiction-audit.md` (CT-NN) and `missing-information.md` (GAP-NNN), which this file cross-references instead of duplicating.

Gate vocabulary follows `quality-gates.md` §1: `PASS` / `PASS WITH FINDINGS` / `FAIL`, severities `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`.

---

## 1. Method

1. Enumerated every gate entry criterion and checklist row in `../../21-completion/core/quality-gates.md` (Gates 0–3) and every money-path document (`../../07-api/core/wallet.md`, `orders.md`, `../../06-backend/core/background-processing.md`, `../../04-architecture/core/data-flow.md`, `../../08-database/core/payment.md`, `constraints-and-integrity.md`).
2. Verified each prerequisite against its owning register (`00-project-overview/dependencies.md`, `assumptions.md`, `project-charter.md`, `success-criteria.md`) with mechanical counts and direct reads.
3. Cross-checked API contracts against DB enums (§3, CRIT-03) and queue inventories across two owners (CRIT-04).
4. Recorded each failure with evidence tag, severity, blocked gate, and clearance condition.

Evidence tags: `VERIFIED` = recomputed from the artifact; `INFERENCE` = absence-based or derived, stated as such; `INSUFFICIENT EVIDENCE` = the artifact that would settle it does not exist.

---

## 2. Findings register

| ID | Severity | Finding | Evidence | Blocks | Status |
|---|---|---|---|---|---|
| CRIT-01 | CRITICAL | Gate 0 prerequisites unmet: no baseline, no wallet-provider access, no SMS/WhatsApp contract, no regulatory position | `assumptions.md:34` `ASM-14` = `INSUFFICIENT EVIDENCE`/UNSUPPORTED; `dependencies.md:23` `DEP-05` = **NOT STARTED**, `:24` `DEP-06` = **NOT STARTED** ("Registration blocked"), `:28` `DEP-10` = Not started ("Existential"); `project-charter.md:46` baselines `INSUFFICIENT EVIDENCE`, `:87` sign-off pending; `quality-gates.md:76`–`:79` show checks 0.1/0.3/0.4 all red, `:177` Gate 0 = `PENDING` | **Gate 0** → Phase 1 start | OPEN |
| CRIT-02 | CRITICAL | Test inventory overstated: locked allocation promises 114 TCs, 103 exist — FR-020 has zero mapped cases, PLAN-18 range is fictitious | `13-testing/README.md:29,86,88,111,112` and `../../13-testing/test-cases-index.md:15,64,65,86,102` claim `TC-001…TC-114`; directory holds 104 files (`README` + `TC-001…TC-103`); `../../13-testing/core/test-plans.md:44` PLAN-18 → `TC-105–114`; full evidence in HAL-01 | **Gate 1** check `1.1`/`1.3`, `AC-S-01`/`AC-S-03` | RESOLVED (2026-09-27 — `TC-104`…`TC-114` authored; directory now holds 114 `TC-*.md` files against the locked 114; PLAN-18 range real; HAL-01 `RESOLVED`) |
| CRIT-03 | HIGH | API↔DB status drift on money-path resources: three API status vocabularies have no matching DB enum | (a) `wallet.md:34` API-WAL-008 returns payment `status: "RELEASED"` — `payment_state` = `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED` (`constraints-and-integrity.md:85`, `../../08-database/core/payment.md:33`); (b) top-up status `PENDING_PROVIDER\|PENDING_VERIFICATION\|CREDITED\|REJECTED` (`wallet.md:29`–`:30`) has no enum/column anywhere in `08-database` (top-ups are `payment` rows `kind='TOPUP'`); (c) `wallet.md:40` API-WAL-014 refund status `PENDING\|COMPOSED\|CREDITED` vs DB `refund.state ∈ {PENDING, PROCESSING, COMPLETED, FAILED}` (`../../08-database/core/payment.md:60`) | **Gate 1** (`1.3`, `1.4` money-path suites); contract-first build would encode values the schema rejects. Cross-ref: `contradiction-audit.md` (CT-NN series) | OPEN |
| CRIT-04 | HIGH | Queue inventory disagrees between its two owners: 25 queues vs 17, with divergent names, plus three delivery queues outside the backend's own register | `../../06-backend/core/background-processing.md` §1 register = 25 queues; `../../04-architecture/core/data-flow.md` §2 table = 17; name mismatches include `b02.inventory.expire` vs `b05.inventory.release`, `b07.wallet.topup.reconcile` vs `b07.wallet.topup-reconcile`, `b07.payout.batch` vs `b07.payout.execute`; backend §2 adds `b10.notification.delivery.{sms\|whatsapp\|push}` not listed in its §1 register (money-adjacent: top-up reconciliation, payout, notification delivery) | **Gate 1** (`1.4`); monitoring/DLQ design in `06-backend`/`14-devops-infrastructure`. Cross-ref: `contradiction-audit.md` (CT-NN series) | RESOLVED (2026-09-27 — single 30-row register at `../../06-backend/core/background-processing.md` §1 adopted by both owners: `data-flow.md` v1.1 restates all 17 consumer rows from it, `background-processing.md` v1.1 adds the 5 missing entries incl. `b07.wallet.credit` and `b10.notification.delivery.*`; `CT-04` `RESOLVED`) |
| CRIT-05 | HIGH | Requirements and AC registry disagree on what FR-015…FR-020 are accepted on; 14 registry FR ACs are orphaned | 16 of 24 cited AC entries in `FR-015`…`FR-020` describe different criteria than the registry row of the same ID (HAL-05); 94 `AC-FR*` defined vs 80 cited — the `-05` row of 14 FRs is never cited by its own file (HAL-07, `../../02-requirements/functional-index.md:61` codifies four) | **Gate 1** check `1.3` (coverage measured against `acceptance-criteria.md` cannot match the requirement text) | OPEN (partial 2026-09-27 — the 14 `-05` orphans are cited, `HAL-07` `RESOLVED`; the FR-015…FR-020 text divergence `HAL-05` remains) |
| CRIT-06 | HIGH | Money-adjacent tests assert business rules that do not exist: `BR-INV-01`…`BR-INV-05` | Cited in `../../13-testing/core/TC-018.md:51,61,62`, `TC-019.md:50,52,61,62`, `TC-020.md:49,61`; `01-business-analysis/business-rules.md` defines 99 rules across 14 prefixes, none `BR-INV-*` (HAL-04) | **Gate 1** check `1.9` / every gate via `D-3` ID discipline (`quality-gates.md:59`) | `RESOLVED` 2026-09-28 (first clearance branch: `business-rules.md` **v1.1** registers `BR-INV-01`…`BR-INV-05` under a new `INV` domain — 104 rules / 15 domains — wording derived from approved sources; owner-approved registration, session 008; count consumers re-synced; *(count since superseded — `business-rules.md` **v1.2**, session 011 (2026-09-30): **111 rules / 15 domains**, `BR-AUTH-09/10`, `BR-PAY-11`, `BR-ESC-09`, `BR-RET-08`, `BR-REV-06`, `BR-PLT-08` added in existing domains; status and clearance unchanged)*) |
| CRIT-07 | HIGH | Push device-token API resource has no storage model (INFERENCE — absence-based) | `../../07-api/core/notifications.md` API-NTF-008/009/010 define `POST/GET/DELETE /devices` with `{deviceId, platform, token}`; `08-database` schema map b10 lists only `notification`, `notification_preference`; no `device_token\|push_token\|fcm` table exists anywhere in `08-database`; supporting-table list in `../../08-database/entities-index.md` omits it. `notification_channel` includes `PUSH` (`constraints-and-integrity.md:95`) | **Gate 1** design completeness; FR-017 push delivery cannot persist registrations | OPEN |
| CRIT-08 | MEDIUM | Provenance and decision-record chain broken on a gate-evidence path | `docs/README.md:33,35` claim an `archdoc.md` origin and an `archive/` copy: `E:\YUMN\archdoc.md` = 0 bytes, `E:\YUMN\archive\` absent (HAL-03); `04-architecture/architecture-decisions-reference.md:19` still says the ADR directory is empty while `18-decisions/core/` holds ADR-001…ADR-010 (HAL-02) | **Gate 0** check `0.7` (link/ID pass), `D-3` at every gate; `../../21-completion/core/technical-debt.md:34`–`:35` depends on both | `RESOLVED` 2026-09-28 (both clearance conditions met: ADR index re-synced `architecture-decisions-reference.md` v1.1 session 007 `REC-02`; provenance lines corrected + `archdoc.md` v1.0 restored session 008 `REC-01` — `archive/` absence kept explicitly annotated in `docs/README.md` §1; `HAL-02`/`HAL-03` `RESOLVED`, `TD-02`/`TD-03` `PAID`) |
| CRIT-09 | MEDIUM | Launch-blocking dependencies unstarted ahead of Gate 2 | `dependencies.md:27` `DEP-09` legal opinions (VAT, data protection) = Not started; `:26` `DEP-08` domains/TLS/CDN = Not started; `:30` `DEP-12` test-device lab = Not started; `:28` `DEP-10` Central Bank position = Not started ("Existential"); `quality-gates.md:143` names unresolved `DEP-09`/`DEP-10` as **launch hard stops**, `:132` makes `AC-S-24` evidence mandatory | **Gate 2** (`2.4`, hard stop); `AC-S-24` | OPEN |
| CRIT-10 | MEDIUM | Gate inputs that `quality-gates.md` mandates did not exist at audit time; 19 non-validation links broken corpus-wide | `quality-gates.md:35` declares `critical-findings.md`, `missing-information.md`, `contradiction-audit.md`, `consistency-audit.md` standing inputs with evidence status `INSUFFICIENT EVIDENCE`; at scan time `docs/19-traceability/` and `docs/20-validation/` were absent (8 citations to `19-traceability/*` + 11 unresolvable path citations elsewhere; counts in `analysis-validation.md`) | **Gate 0** check `0.7` / `D-1` link validation; partially self-healing as domains land | OPEN |

Severity totals: **CRITICAL 1 (`CRIT-01`) · HIGH 3 (`CRIT-03`, `CRIT-05`, `CRIT-07`) · MEDIUM 2 (`CRIT-09`, `CRIT-10`) = 6 open findings** (`CRIT-02` resolved `REC-03` and `CRIT-04` resolved `REC-06`, both 2026-09-27; `CRIT-08` resolved 2026-09-28 `REC-01`; `CRIT-06` resolved 2026-09-28 `BR-INV` registration).

---

## 3. Money-path drift detail (CRIT-03)

| # | API says (07-api) | DB says (08-database) | Impact |
|---|---|---|---|
| a | `API-WAL-008` → `status: "RELEASED"` (`wallet.md:34`) | `payment_state` enum has no `RELEASED` (`constraints-and-integrity.md:85`; `../../08-database/core/payment.md:33`) | A client-visible response value the schema cannot store; release flow (`FR-013`, hold expiry) cannot round-trip |
| b | Top-up lifecycle `PENDING_PROVIDER → PENDING_VERIFICATION → CREDITED\|REJECTED` (`wallet.md:29`–`:31`) | No top-up status enum/column; top-ups are `payment` rows with `payment_state` and `provider_status_raw` jsonb (`../../08-database/core/payment.md:20,33,37`) | The documented verification workflow (bank-transfer proof, admin approval, `FR-013`/`INT-REQ-002`) has no state field to live in |
| c | `API-WAL-014` refund status `PENDING\|COMPOSED\|CREDITED` (`wallet.md:40`) | `refund.state ∈ {PENDING, PROCESSING, COMPLETED, FAILED}` (`../../08-database/core/payment.md:60`) | Two of three API values unrepresentable; two DB values unobservable; `FR-016`/`BR-PAY-07` reporting ambiguous |

Cross-reference: the same drift class (order/escrow/notification statuses, health paths) is owned by `contradiction-audit.md` (CT-NN series) — this register does not duplicate those rows, it only rolls their money-path severity up to CRIT-03.

---

## 4. Clearance conditions

| ID | Clears when |
|---|---|
| CRIT-01 | Sponsor records budget/team/schedule baselines and re-scores `ASM-14` with evidence; `DEP-05` granted from both m-Floos and OneCash (or written sponsor decision for bank-transfer-only); `DEP-06` signed; `DEP-10` written Central Bank position on file — i.e. every red cell in `quality-gates.md:74`–`:89` turns green |
| CRIT-02 | `13-testing/` re-syncs its count and locked allocation to the 103 cases that exist (or authors the missing 11), and `test-plans.md:44` PLAN-18 is re-based |
| CRIT-03 | One owner amends the other: DB adds the missing status values **or** `07-api` responses are re-mapped onto existing enums; re-verified by the payment suite (`quality-gates.md:106`) |
| CRIT-04 | A single queue register of record (name, block, purpose) is adopted by `06-backend` and `04-architecture`, including the `b10.notification.delivery.*` producers |
| CRIT-05 | `FR-015`…`FR-020` and `acceptance-criteria.md` are reconciled ID-by-ID, and either the 14 orphaned `-05` ACs are cited by their FR files or retired from the registry |
| CRIT-06 | ~~`BR-INV-*` IDs are defined in `01-business-analysis/business-rules.md` **or** the three TCs are re-pointed at the real rule IDs (owner decides; audit does not)~~ **MET 2026-09-28** — first branch taken: `BR-INV-01`…`BR-INV-05` registered (`business-rules.md` v1.1) |
| CRIT-07 | A `device_token`-style supporting table (or an explicit `INFERENCE`-tagged decision not to persist) is recorded in `08-database` |
| CRIT-08 | `docs/README.md` provenance lines are corrected (or `archdoc.md`/`archive/` are produced), and the ADR index statuses are re-synced with `18-decisions/core/` — **met 2026-09-28:** index v1.1 (session 007) + `archdoc.md` v1.0 restored with honest provenance and `docs/README.md` v1.4 §1 corrected (session 008) |
| CRIT-09 | `DEP-09`/`DEP-10` written opinions received; `AC-S-24` evidence pack assembled per `../../12-non-functional/core/compliance-and-legal.md` §5 |
| CRIT-10 | `19-traceability/` and `20-validation/` complete, then a fresh link pass shows 0 unresolvable citations (root README §11) |

**Gate 0 stance (as of 2026-09-27):** with CRIT-01 open, Gate 0 is a **`FAIL`** by its own criteria (`quality-gates.md:89`: if `DEP-06` is unsigned, Gate 0 `FAIL`). No implementation should start on the strength of this analysis alone; CRIT-03…CRIT-10 additionally require disposition before Gates 1–2 (CRIT-02 disposed 2026-09-27). Recorded outcomes belong in `../../21-completion/core/quality-gates.md` §7 when the sponsor convenes the review — not here.

---

## Coverage & Statistics

- **Files examined:** 18 of 18 in scope (`quality-gates.md`, `dependencies.md`, `assumptions.md`, `project-charter.md`, `success-criteria.md`, `risk-review-process.md` excerpts, both queue owners, 6 API/DB money-path documents, `13-testing/README.md`, `../../13-testing/test-cases-index.md`, `../../13-testing/core/test-plans.md`, `02-requirements/acceptance-criteria.md`, `FR-015`…`FR-020`); corroborating reads from AUD-04 (`hallucination-audit.md`)
- **Checks run:** 10 — passed 0, failed 10 at audit time (every finding is an open condition; none of the failures are disputed by the audited documents); 2026-09-27 re-scans: `CRIT-02` condition passes (114/114 TCs, `REC-03`), `CRIT-04` condition passes (single 30-row queue register adopted, `REC-06`); 2026-09-28 re-scans: `CRIT-08` condition passes (ADR index re-synced + `archdoc.md` restored, `REC-01`), `CRIT-06` condition passes (`BR-INV-01`…`05` registered in `business-rules.md` v1.1, owner-approved); 6 remain open
- **ID references verified:** `DEP-*` 12 rows read (05/06/08/09/10/11/12 statuses quoted verbatim) · `ASM-14` `INSUFFICIENT EVIDENCE` · `AC-S-*` 24 defined, all `PENDING` · `BR-INV-*` 5 cited / 0 defined at audit → **5/5 defined 2026-09-28** (`business-rules.md` v1.1; register now **v1.2 — 111 rules / 15 domains** since session 011, 2026-09-30, `BR-INV-*` still 5/5) · `TC-*` 103/114 at audit → **114/114 (2026-09-27)** · `payment_state` 5 values vs 3 API vocabularies · queues 25 vs 17 → single 30-row register (2026-09-27) · `API-NTF-008/009/010` 3 endpoints / 0 storage tables
- **Terms/IDs in scope:** money-path series `AC-FR011/013/014/015/016/017/020-*`, `BR-PAY-*`, `BR-ESC-*`, `BR-RET-*`, `BR-NTF-*`, `PLAN-10`/`PLAN-18`, `SEC-011`/`SEC-015` (security blockers owned by `../../09-security/core/security-findings.md`, referenced not re-audited)

## Verdict & Sign-off

- **Gate:** `FAIL` for Gate 0 as of 2026-09-27 (`quality-gates.md:89`: `DEP-06` unsigned ⇒ Gate 0 `FAIL` — CRIT-01); the register itself is complete: `PASS WITH FINDINGS` as an audit artifact. Gates 1–2 each carry ≥ 1 open CRIT row that must be dispositioned before presentation
- **Unresolved contradictions / gaps:** CRIT-01, CRIT-03, CRIT-05, CRIT-07, CRIT-09, CRIT-10 `OPEN`; CRIT-02, CRIT-04 `RESOLVED` 2026-09-27, CRIT-06, CRIT-08 `RESOLVED` 2026-09-28; cross-referenced into `contradiction-audit.md` (CT-NN series — enum/queue drift detail) and `missing-information.md` (GAP-NNN series — `GAP-01`…`GAP-07` decisions feed CRIT-09 clearance); no CT/GAP IDs are minted in this file
- **Required follow-up:** sponsor (`CRIT-01`, `CRIT-09`), ~~`13-testing/` (`CRIT-02`)~~ done 2026-09-27, one owner of `07-api`/`08-database` (`CRIT-03`), ~~`06-backend` + `04-architecture` (`CRIT-04`)~~ done 2026-09-27 (`REC-06`), `02-requirements` + `acceptance-criteria.md` (`CRIT-05`), ~~`01-business-analysis` + `13-testing` (`CRIT-06`)~~ done 2026-09-28 (`BR-INV-01`…`05` registered, `business-rules.md` v1.1), `08-database` (`CRIT-07`), ~~`docs/README.md` + `04-architecture` (`CRIT-08`)~~ done 2026-09-28 (`REC-01`/`REC-02`), `19-traceability/` + `20-validation/` owners (`CRIT-10`); dispositions recorded per finding before the next gate (root README §9.5)
- **Sign-off:** analysis-agent (author), 2026-09-27 — gate outcome recorded by the project sponsor at the Gate 0 review, not by this audit

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 items 43,45,48 + DOC-REQ-001 |
| 1.1 | 2026-09-27 | `CRIT-02` → `RESOLVED` (114/114 TCs on disk; PLAN-18 real); checks/ID stats annotated; Gate stance re-scoped to CRIT-03…CRIT-10 | `REC-03` pay-down change set (session 003) — roll-up of `HAL-01`/`TD-04` |
| 1.2 | 2026-09-27 | `CRIT-05` annotated partial: `-05` orphan clause cleared (`HAL-07` `RESOLVED`), text-drift clause (`HAL-05`) open | `REC-04` pay-down change set (session 003) — roll-up honesty, row kept `OPEN` |
| 1.3 | 2026-09-27 | `CRIT-04` → `RESOLVED` (single 30-row queue register adopted by both owners); severity totals 10 → 8 open; verdict/follow-up/ID stats re-scoped | `REC-06` pay-down change set (session 003) — roll-up of `TD-07`/`CT-04` |
| 1.4 | 2026-09-28 | `CRIT-08` → `RESOLVED` (both clearance conditions met: ADR index v1.1 session 007; `archdoc.md` v1.0 restored + `docs/README.md` v1.4 §1 corrected session 008); severity totals 8 → **7 open**, checks/verdict/follow-up re-scoped | `REC-01`/`TD-03` pay-down change set (session 008) — finding flipped, never deleted (DOC-TPL-011 #3) |
| 1.5 | 2026-09-28 | `CRIT-06` → `RESOLVED` (`BR-INV-01`…`05` registered in `business-rules.md` v1.1 — owner-approved first clearance branch; count consumers re-synced 99 → 104); severity totals 7 → **6 open**, checks/verdict/follow-up/ID stats re-scoped; session-008 cleanup also removed an erroneous duplicate `1.3` row that had been inserted earlier this session (the genuine `1.3` row — `CRIT-04`, 2026-09-27 — is kept above in date order) | `BR-INV` registration change set (session 008, `CRIT-06`/`HAL-04`) — findings flipped, never deleted (DOC-TPL-011 #3) |
| 1.6 | 2026-09-30 | Session-011 count refresh, **annotation only** — no status, severity, totals or roll-up change: `CRIT-06` evidence/ID-stat supersession chains extended 104 → **111 rules / 15 domains** (`business-rules.md` v1.2, session 011) with the 99-rule at-audit evidence and the 104-rule session-008 record both kept visible; `BR-INV-*` re-verified 5/5 | Owner directive session 011 `prompt-011.md` §4.8 — proposal/disposition rows in the relevant registers (`CT`/`GAP`/`HAL` as applicable) |
