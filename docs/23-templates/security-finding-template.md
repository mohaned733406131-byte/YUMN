---
document_id: DOC-TPL-010
title: Security Finding Template (SEC-NNN)
category: 23-templates
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-SEC-008, DOC-SEC-002, DOC-GL-003]
---

# Security Finding Template (DOC-TPL-010)

**When to use:** appending a new finding **entry** to `09-security/security-findings.md` (DOC-SEC-008) — findings are entries in the register, never separate files. **Authority: DOC-SEC-008 (register format, severity rule), DOC-SEC-002 (threat model the finding may cite), root README §8 (severity vocabulary)**. Exemplar entries: `SEC-001`, `SEC-002` in `security-findings.md`.

## Rules

- **Mint the next ID in `security-findings.md` only:** allocation is `SEC-001…SEC-015`; the next finding is **`SEC-016`** (DOC-GL-003 §3).
- **Severity** = impact × likelihood *if the gap is exploited as designed today* (register rule); vocabulary `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL` (root README §8). Reclassify only with evidence, bumping the version and adding a Change History row.
- Every finding updates **both** places in the same change: a row in `## Summary` (`| ID | Title | Severity | Affected area | Status |`) and a detail block (`## SEC-NNN — Title`).
- Four bullets only — `Description · Impact · Recommendation · Related` — each citing existing IDs (`SEC-REQ-*`, `BR-*`, `C-*`, `TM-NN`, `SEC-C-*`, `GAP-NN`, `DEP-nn`); never restate a rule, cite it (root README §4).
- Status vocabulary: `OPEN · IN_PROGRESS · MITIGATED · ACCEPTED (with expiry)`; a finding closes only with evidence in canon — never by deletion.
- A finding is a *gap in this design or its implementation posture*, not a vulnerability scan result: no CVE inventing, no tool output pasted as fact (root README §8 evidence tags).
- Register and its entries carry `source_of_truth: true` (DOC-SEC-008 is the authority for findings).

## Template

```text
<!-- 1. Summary Table row — insert in ID order under ## Summary in security-findings.md -->

| SEC-<nnn> | <one-line title — the gap, plainly stated> | <CRITICAL|HIGH|MEDIUM|LOW|INFORMATIONAL> | <affected area(s), comma-separated> | OPEN |

<!-- 2. Detail block — append after the last finding, before its Change History -->

## SEC-<nnn> — <one-line title>

**Severity:** <SEVERITY> · **Area:** <area(s)> · **Status:** OPEN

- **Description:** <what the gap is and why it exists in the current design — mechanism first, then the canon IDs that make it a gap (missing requirement, undefined value, shared surface).>
- **Impact:** <what an adversary or failure achieves because of the gap — the assets, flows and constituencies affected, with IDs.>
- **Recommendation:** <the concrete fix or control — named mechanism, where the spec lives, which AC/test proves it; mark genuinely open design choices as `INFERENCE` or `GAP-NN` rather than deciding them here.>
- **Related:** `<SEC-REQ-*>, <FR-*>, <BR-*>, <C-*>, <TM-NN / threat-model.md §…>, <docs §section>.`

<!-- 3. Same change: bump security-findings.md version + Change History row -->
```

## Pre-Submission Checklist

1. ID is `SEC-016` (or next free) minted only in `security-findings.md`; title states the gap, not a scare phrase.
2. Severity justified by the exploit-today rule and matched to the vocabulary; area(s) use existing domain/flow names; status valid.
3. Summary row **and** detail block both added; exactly the four bullets; every cited ID (`SEC-REQ-*`, `TM-NN`, `SEC-C-*`, `GAP-*`) exists in canon.
4. Recommendation names a verifiable mechanism — no "should be more secure"; open questions tagged `INFERENCE`/`GAP-NN`, never silently decided.
5. `security-findings.md` version bumped + Change History row (root README §9); severity distribution counts updated if present.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
