---
document_id: DOC-DR-009
title: DATA-REQ-009 — Search-index data protection
category: 02-requirements
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-002, DATA-REQ-003, SEC-REQ-006, FR-009]
related_documents: [DOC-REQ-001, DOC-OVR-012]
---

# DATA-REQ-009 — Search-index data protection

> Registry summary (`requirements-overview.md` §4): index field allowlist (public catalog fields only), restricted/encrypted index snapshots, index deletion wired into the account-deletion workflow, with a "PII in index" test.

## Description
The search index (Arabic-aware full-text search under `FR-009`) is a second copy of data whose protection nobody specified: `../../../09-security/core/security-findings.md` `SEC-007` (lines 91–97, severity MEDIUM) records that what is indexed, snapshot protection, and "how deletion propagates (index vs source) are all undefined" (line 94), leaving `DATA-REQ-003` "silently unmet for indexed fields" (line 95). This requirement extends data-minimization, retention and deletion guarantees to the index itself. Registration recorded in `DOC-OVR-012` §5.

## Requirement statements

- R1: Only public catalog fields are indexed — an explicit per-index field allowlist keeps PII (phone, addresses, wallet, KYC fields) out of the index entirely (`SEC-007` line 94, extends `DATA-REQ-002`).
- R2: Index snapshots/backups are access-restricted like the source data and encrypted at rest — an index snapshot is never a weaker copy of the database (`SEC-007`; encryption posture per `SEC-REQ-006`).
- R3: Index deletion is wired into the account-deletion workflow: when source PII is deleted/anonymised, the corresponding indexed content is removed or re-indexed from the scrubbed source in the same workflow, so `DATA-REQ-003` holds for indexed fields (`SEC-007` line 95).
- R4: A "PII in index" test samples indexed documents and asserts only allowlisted fields exist; it runs in CI and fails the build on a leaked field (`SEC-007` recommendation).

## Acceptance criteria

- AC-DR009-01: Given the index field allowlist, when a document is indexed, then only allowlisted public catalog fields appear — a probe for phone/address/wallet fields in the index returns zero hits.
- AC-DR009-02: Given an index snapshot, when its storage is inspected, then access is role-restricted and contents are encrypted at rest — parity with the source-data posture (SEC-REQ-006).
- AC-DR009-03: Given a completed account-deletion run, when the index is queried for the deleted user's content, then it is gone — deletion propagated source → index inside the same workflow (DATA-REQ-003).
- AC-DR009-04: Given the "PII in index" CI test, when a new indexed field is added without an allowlist entry, then the test fails and the build is blocked.

## Related IDs

`DATA-REQ-002` · `DATA-REQ-003` · `DATA-REQ-008` · `SEC-REQ-006` · `FR-009` · `NFR-019` · `SEC-007`

## Verification method

Index-content probe tests (allowlist + PII scan) in CI; snapshot storage policy inspection; account-deletion end-to-end test asserting index propagation; findings tracked in `../../../09-security/core/security-findings.md` (`SEC-007`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial requirement | Session-011 owner directive (`prompt-011.md` §4.7) — delta accepted in `DOC-OVR-012` §5 (source: `security-findings.md` `SEC-007` lines 91–97) |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration (data/ + functional/ sections) | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
