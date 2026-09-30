---
document_id: DOC-VAL-001
title: 20-Validation — Domain Index & Audit Register
category: 20-validation
status: approved
version: 1.2
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-019]
related_documents: [DOC-ROOT-001, DOC-TPL-011, DOC-GL-003, DOC-CMP-004, DOC-CMP-006, DOC-AC-001, DOC-OVR-005]
---

# 20 — Validation (DOC-VAL-001)

**Scope of `20-validation/`:** the evidence and defect record for this knowledge base — where gaps, contradictions, unsupported claims, critical findings and the final quality verdict live. This README is the domain index, the **`AUD-NN` audit register**, and the rules of engagement for every file in this directory.

> **Audits record, they never fix.** No file here edits another document. Findings stay `OPEN` until the *owning* document changes through root README §9 change management, after which this domain records the propagation (root README §9.4) — never a silent local fix (root README §9.5, `../23-templates/core/validation-audit-template.md` §Rules).

**Authority:** root README §8 (evidence tags, severities), §9 (change/contradiction rules), §10 rows 41/42/43/45/48 (this domain's sanctioned file list), §11 (quality gate); `../23-templates/core/validation-audit-template.md` (DOC-TPL-011 — file shape, finding columns, pre-submission checklist). Where DOC-TPL-011 and root README disagree, root README wins and the disagreement is logged in `core/contradiction-audit.md`.

---

## 1. File Index (root README §10)

| # | File | document_id | Root README §10 row | Audit ID | State at 2026-09-27 |
|---|---|---|---|---|---|
| 1 | [README.md](README.md) | `DOC-VAL-001` | §2 documentation map | — | authored 2026-09-27 |
| 2 | [missing-information.md](core/missing-information.md) | `DOC-VAL-002` | 41. Missing Information | `AUD-03` | authored 2026-09-27 |
| 3 | [consistency-audit.md](core/consistency-audit.md) | `DOC-VAL-003` | §9.4 propagation record | `AUD-01` | authored 2026-09-27 (baseline sweep) |
| 4 | [contradiction-audit.md](core/contradiction-audit.md) | `DOC-VAL-004` | 42. Contradictions | `AUD-02` | authored 2026-09-27 (baseline) |
| 5 | [hallucination-audit.md](core/hallucination-audit.md) | `DOC-VAL-005` | 43. Incorrect/Unsupported Claims | `AUD-04` | authored 2026-09-27 (parallel authoring pass) |
| 6 | [critical-findings.md](core/critical-findings.md) | `DOC-VAL-006` | 45. Critical Findings | `AUD-05` | authored 2026-09-27 (parallel authoring pass) |
| 7 | [requirements-validation.md](core/requirements-validation.md) | `DOC-VAL-007` | §7 quality test (via `02-requirements/requirements-overview.md`) | `AUD-07` | authored 2026-09-27 (parallel authoring pass) |
| 8 | [analysis-validation.md](core/analysis-validation.md) | `DOC-VAL-008` | 48. Final Quality Assessment | `AUD-06` | authored 2026-09-27 (parallel authoring pass) |

`document_id` short code `VAL` and the `DOC-VAL-NNN` allocation are minted **here**, per `22-glossary/naming-conventions.md:36` ("pending — see `DOC-VAL-*` gap"). Files 5–8 were declared in this register as a forward allocation; all four have since been authored by their own authoring passes and are now `authored` above — nothing in this file asserts their content or sign-off.

---

## 2. Audit Register (`AUD-NN` — minted here)

`AUD-NN` is width 2, allocated append-only in this table only (`22-glossary/naming-conventions.md:91`, `../23-templates/core/validation-audit-template.md` §Rules). The row previously carried `INFERENCE` in DOC-GL-003 §3; with this register authored, `AUD-01…AUD-07` are `VERIFIED` allocations.

| Audit ID | Type | File | Methodology | Scope of the baseline run | Verdict (baseline) |
|---|---|---|---|---|---|
| `AUD-01` | consistency | `core/consistency-audit.md` | root README §9.4 | all 433 `.md` files in `docs/`, 2026-09-27 (corpus 443 at v1.1 re-run) | `PASS WITH FINDINGS` — 20 of 31 checks failed |
| `AUD-02` | contradiction | `core/contradiction-audit.md` | root README §9.5 | cross-layer statements (API ↔ DB ↔ UI ↔ infra ↔ glossary) | `PASS WITH FINDINGS` — `CT-01` `PASS`; `CT-02…CT-20` `OPEN` |
| `AUD-03` | missing-information | `core/missing-information.md` | root README §10/41 | every unresolved question across `docs/` | `PASS WITH FINDINGS` — `GAP-01…GAP-12` all `OPEN` |
| `AUD-04` | hallucination | `core/hallucination-audit.md` | root README §10/43 | unsupported claims presented as fact | `PASS WITH FINDINGS` — `HAL-01…HAL-13`, 1 `CRITICAL` + 4 `HIGH` |
| `AUD-05` | critical-findings | `core/critical-findings.md` | root README §10/45 | `CRITICAL`-severity defects | `FAIL` for Gate 0 / register `PASS WITH FINDINGS` — `CRIT-01…CRIT-10` |
| `AUD-06` | final-quality | `core/analysis-validation.md` | root README §10/48 | whole-corpus quality verdict | `PASS WITH FINDINGS` — 444 files scored |
| `AUD-07` | requirements-quality | `core/requirements-validation.md` | `02-requirements/requirements-overview.md` (7-question test) | `FR/NFR/SEC-REQ/DATA-REQ/INT-REQ` quality test results | `PASS WITH FINDINGS` — 68 requirement files checked |

**Audit lifecycle:** `PLANNED` → `RUN` (date + verdict recorded) → each finding carries its own status; the audit row flips to `CLOSED` only when every finding under it is `RESOLVED`/`WAIVED` and the owning documents have been version-bumped (root README §9.2).

---

## 3. Finding Series — where each ID lives

| Series | Pattern | Minted only in | Baseline allocation (2026-09-27) |
|---|---|---|---|
| Gaps | `GAP-NN` (issued) / `GAP-NNN` (root README §5 pattern) | `core/missing-information.md` | `GAP-01…GAP-07` inherited from `00-project-overview/project-scope.md`; **`GAP-08…GAP-12` minted by `AUD-03`** |
| Contradictions | `CT-NN` | `core/contradiction-audit.md` | `CT-01` (mandated PASS) … `CT-20` |
| Audits | `AUD-NN` | this file (§2) | `AUD-01…AUD-07` |
| Unsupported claims | `HAL-NN` | `core/hallucination-audit.md` | `HAL-01…HAL-13` minted by `AUD-04` |
| Critical findings | `CRIT-NN` | `core/critical-findings.md` | `CRIT-01…CRIT-10` minted by `AUD-05` |
| Cross-references (not minted here) | `SEC-NNN`, `RISK-NNN`, `TD-NN`, `DQ-NN`, `TST-CON-NN` | owning registers (`09-security/`, `17-risk-management/`, `21-completion/`, `16-data/`, `13-testing/`) | referenced only |

**Never mint an ID outside its register** (`22-glossary/naming-conventions.md` §3 *Defined in* column). This file allocates `AUD-NN`, `DOC-VAL-NNN` and — via `missing-information.md` — `GAP-NN` / (via the other audits) `CT-NN`; everything else is citation.

---

## 4. Rules of Engagement

1. **Evidence tags** on every statement: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE` (root README §8).
2. **Severity** for findings: `CRITICAL` · `HIGH` · `MEDIUM` · `LOW` · `INFORMATIONAL`; **confidence** for conclusions: `HIGH` · `MEDIUM` · `LOW`.
3. **Gate outcomes** for audits: `PASS` · `PASS WITH FINDINGS` · `FAIL` (root README §11; outcome vocabulary mirrored in `../21-completion/core/quality-gates.md` §1).
4. **Finding status:** `OPEN` → `RESOLVED` (owning document changed, version bumped) or `WAIVED` (explicit written disposition with owner). No finding is deleted (DOC-TPL-011 pre-submission checklist #3).
5. **Exact citations:** every finding names `file` + `§section` or `file:line` plus the conflicting/absent IDs. No evidence is invented; anything not read first-hand is tagged `INFERENCE`.
6. **Propagation:** when an owning document changes, run the affected sweep again and record the affected IDs in `core/consistency-audit.md` §Change-Propagation Log (root README §9.4).
7. **Re-run triggers:** any structural change (new directory, new ID series, registry renumber), any canon change in root README §5/§9, and before every gate (root README §11: "Audits … must be run after any structural change").
8. **Consumers:** `../21-completion/core/quality-gates.md` §1 lists all four of these files as *standing input to every gate*; `G-R6` (register hygiene) requires this domain to be clean; `D-1` (link validation) and `D-3` (ID discipline) are the checks this domain produces evidence for.
9. **English only**; no `<angle-bracket>` placeholders outside `23-templates/` (DOC-TPL-001 §2).

---

## 5. Register-Precedence Notes (open items owned elsewhere)

| # | Question | State at 2026-09-27 | Handled in |
|---|---|---|---|
| 1 | Where is the canonical GAP register: `core/missing-information.md` (root README §5:161, `22-glossary/naming-conventions.md:90`) or `00-project-overview/project-scope.md` §UNCERTAIN SCOPE (`../16-data/core/retention-and-archival.md:39`, `../12-non-functional/core/compliance-and-legal.md:88`)? | Conflict recorded, not resolved here | `contradiction-audit.md` `CT-15` |
| 2 | Root README §5 has no `AUD-NN` row (`naming-conventions.md:91` instructs registering it here "when `20-validation/` is authored") | Register authored; root README §5 row **not yet added** | consistency-audit finding (required edit, not made here) |
| 3 | Root README §5 pattern `GAP-NNN` vs issued width `GAP-NN` | Known defect logged against root README | `naming-conventions.md:118`, consistency-audit finding |
| 4 | `19-traceability/` (root README §10 row 40) was cited by 33 files while absent | Directory authored 2026-09-27 17:34 (3 files); consistency-audit finding 3 flipped to `RESOLVED` — but `../19-traceability/core/requirements-to-tests.md` cites an undefined `DOC-INT-010` | consistency-audit finding 3 (`RESOLVED`) + finding 23 (`OPEN`) |

---

## 6. How to Add a Finding

1. Open the **sanctioned file** for the type (§1 table — never file a contradiction into the consistency file; DOC-TPL-011 pre-submission checklist #1).
2. Append a row to `## Findings` with: one-line statement, severity, `where` (file §section or line), `evidence` (IDs + tag), `status`.
3. If the finding needs a new `GAP-NN`/`CT-NN`, allocate it in the register row of the owning file, then cross-reference.
4. Bump `version`, add a `## Change History` row (root README §9.2), and update the `updated:` frontmatter date.
5. Re-run the affected checks; record the propagation in `consistency-audit.md` §Change-Propagation Log.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring; `DOC-VAL-001…008` allocated; `AUD-01…AUD-07` registered; series-home table established | Root README §10 items 41/42/43/45/48; `DOC-TPL-011` §Rules; `naming-conventions.md:91` |
| 1.1 | 2026-09-27 | Parallel authoring pass absorbed: file index rows 5–7 → authored, row 8 still forward-allocated; audit verdicts filled for `AUD-04`/`AUD-05`/`AUD-07`; series table now records `CT-01…CT-20`, `HAL-01…HAL-13`, `CRIT-01…CRIT-10`; §5 note 4 closed with a new open item | Sibling files landed after this register was authored; DOC-TPL-011 #3 (findings never deleted) |
| 1.2 | 2026-09-27 | `analysis-validation.md` (`DOC-VAL-008`) authored → index row 8 and `AUD-06` verdict (`PASS WITH FINDINGS`, 444 files) recorded; all 8 declared files now present | Sibling authoring pass completed the domain |
