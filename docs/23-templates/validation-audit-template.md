---
document_id: DOC-TPL-011
title: Validation Audit Template (AUD-NN — 20-validation/)
category: 23-templates
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-ROOT-001, DOC-GL-001, DOC-GL-003]
---

# Validation Audit Template (DOC-TPL-011)

**When to use:** authoring any audit document under `20-validation/` — consistency, contradiction, missing-information, hallucination (unsupported claims), critical-findings or final quality assessment. **Authority: root README §8 (evidence tags), §9 (change/contradiction rules), §11 (quality gate); the audit files themselves are defined in root README §10** — where this template and root README disagree, root README wins (log it in `contradiction-audit.md`). No filled exemplar exists yet: `20-validation/` has not been authored.

## Rules

- **Audit-type → file map (root README §9–§10, the only sanctioned homes):**

| Audit type | File | Methodology section |
|---|---|---|
| Consistency sweep | `20-validation/consistency-audit.md` | root README §9.4 |
| Contradictions | `20-validation/contradiction-audit.md` | §10 / 42 |
| Missing information | `20-validation/missing-information.md` | §10 / 41 |
| Incorrect / unsupported claims | `20-validation/hallucination-audit.md` | §10 / 43 |
| Critical findings | `20-validation/critical-findings.md` | §10 / 45 |
| Final quality assessment | `20-validation/analysis-validation.md` | §10 / 48 |

- **Audit IDs:** `AUD-NN` (e.g. `AUD-01`) — `VERIFIED`: the series mandated by this template was minted in `20-validation/README.md` §2 (`AUD-01…AUD-07`) and registered in root README §5 when `20-validation/` was authored (2026-09-27); same width/zero-padding rule as every series.
- Audits **record**, they never fix: contradictions and gaps stay open in the audit until the owning document changes (root README §9.5) — no silent local fixes, no deletions of findings.
- Every finding carries an evidence tag (`VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`) and cites exact locations (file §section or line) plus the conflicting/absent IDs (root README §8).
- Severity for findings: `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL` (root README §8); gate outcomes: `PASS · PASS WITH FINDINGS · FAIL` (root README §11 quality gate).
- `category: 20-validation` in the filled file; `document_id` uses the domain's registered short code `VAL` (`DOC-VAL-NNN`, minted with the domain 2026-09-27); `status: approved` only after sign-off.
- English only; `<angle-bracket>` placeholders exist only in *this* template and are fully removed when the audit is filled (DOC-TPL-001 §2).

## Template

```text
---
document_id: DOC-<cat>-<nnn>
title: AUD-<nn> — <audit type> (<scope>)
category: 20-validation
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-ROOT-001, DOC-GL-003]
---

# AUD-<nn> — <audit type> (<scope>)

| Field | Value |
|---|---|
| **Audit ID** | AUD-<nn> |
| **Type** | <consistency | contradiction | missing-information | hallucination | critical-findings | final-quality> |
| **Date** | <date> |
| **Scope** | <domains / file globs / ID series examined — e.g. "all 24 domain READMEs, DOC-* frontmatter"> |
| **Method** | <how the audit was performed: sweep patterns, cross-reference checks, ID-existence greps, sample re-reads> |
| **Auditor** | <role> |

## Findings

| # | Finding | Severity | Where (file §section) | Evidence (IDs / tags) | Status |
|---|---|---|---|---|---|
| 1 | <what is wrong or unknown — one line> | <SEVERITY> | `<path>` §<section> | <conflicting or missing IDs — `VERIFIED`> | OPEN |
| 2 | <…> | <…> | <…> | <… — `INFERENCE`> | OPEN |

## Coverage & Statistics

- Files examined: <n> of <total in scope>
- Checks run: <n> — passed <n>, failed <n>
- ID references verified: <n> — missing/nonexistent: <list or "none">
- Terms/IDs in scope of this sweep: <series and counts, e.g. DOC-* 24 · ADR-* 10 · SEC-* 15>

## Verdict & Sign-off

- **Gate:** <PASS | PASS WITH FINDINGS | FAIL> (root README §11 quality gate)
- **Unresolved contradictions / gaps:** <AUD-linked IDs, `GAP-NN` — or "— none">
- **Required follow-up:** <owning documents that must change, with the §9 propagation rule — or "— none">
- **Sign-off:** <role>, <date>

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | <date> | Initial version | Initial analysis |
```

## Pre-Submission Checklist

1. File is one of the six sanctioned `20-validation/` homes (Rules table); audit ID `AUD-NN` minted in the `20-validation/` register when it exists; no findings filed into a differently-named file.
2. Scope and Method are concrete enough to reproduce the sweep; Coverage statistics are real counts, not estimates.
3. Every finding has location + IDs + evidence tag + severity; contradictions/gaps stay OPEN until canon changes (root README §9.5) — none deleted or silently resolved.
4. Gate verdict follows root README §11; follow-up names owning documents; sign-off present.
5. No `<…>` placeholders remain; `version` + Change History row on every edit (root README §9).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | `AUD-NN` registration note → `VERIFIED` (minted `AUD-01…AUD-07` in `20-validation/README.md` §2, row in root README §5); `DOC-VAL` short-code gap closed | `20-validation/` authored — pending notes executed (root README §9) |
