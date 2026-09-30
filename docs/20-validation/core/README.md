---
document_id: DOC-VAL-009
title: 20 Validation — core/ portal folder
category: 20-validation
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-VAL-001]
---

# 20 Validation · `core/`

## Purpose

One of the five portal subfolders of `20-validation/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-VAL-009 | This portal index — purpose, file table |
| [analysis-validation.md](analysis-validation.md) | DOC-VAL-008 | AUD-06 — Final Quality Assessment (whole corpus) |
| [consistency-audit.md](consistency-audit.md) | DOC-VAL-003 | AUD-01 — Consistency Sweep (docs/ corpus, 433 files at sweep / 444 at publication / 479 at session-006 re-run / 485 at session-009 re-run / 654 at session-010 re-run) |
| [contradiction-audit.md](contradiction-audit.md) | DOC-VAL-004 | AUD-02 — Contradiction Audit (CT-01…CT-30) |
| [critical-findings.md](critical-findings.md) | DOC-VAL-006 | AUD-05 — Critical Findings (money-path and gate-blocking) |
| [hallucination-audit.md](hallucination-audit.md) | DOC-VAL-005 | AUD-04 — Hallucination Audit (unsupported claims across docs/) |
| [missing-information.md](missing-information.md) | DOC-VAL-002 | AUD-03 — Missing Information (GAP register GAP-01…GAP-14) |
| [requirements-validation.md](requirements-validation.md) | DOC-VAL-007 | AUD-07 — Requirements Validation (73 requirements, 5 categories) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (7 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-09-30 | Contents row: AUD-07 title count 68 → **73 requirements** | Owner directive session 011 (`prompt-011.md` §4.8) — consumer of `requirements-validation.md` v1.2 (requirements 68 → 73, `requirements-overview.md` v1.2) |
