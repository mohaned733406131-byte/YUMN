---
document_id: DOC-DR-000
title: Data Requirements — README (DATA-REQ Index)
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-002, DATA-REQ-003, DATA-REQ-004, DATA-REQ-005, DATA-REQ-006, DATA-REQ-007, DATA-REQ-008]
related_documents: [DOC-REQ-001, DOC-REQ-002, DOC-BA-005, DOC-OVR-008]
---

# Data Requirements (`DATA-REQ-001` … `DATA-REQ-008`)

## Purpose

Expands the 8 data requirement IDs registered in [`requirements-overview.md` §4](../requirements-overview.md) into precise, testable statements — retention periods, backup cadence, migration rules, ledger immutability, ownership scoping. The registry is canonical: IDs and titles here never diverge from it, and no data requirement exists that is not registered.

## Index

| ID | File | Title | Core obligation |
|---|---|---|---|
| DATA-REQ-001 | [DATA-REQ-001.md](DATA-REQ-001.md) | Integrity constraints | FK/UNIQUE/CHECK/NOT NULL enforced by PostgreSQL, not just the app |
| DATA-REQ-002 | [DATA-REQ-002.md](DATA-REQ-002.md) | Personal data minimization | Collect only purposeful PII; classify per `16-data/data-classification.md` |
| DATA-REQ-003 | [DATA-REQ-003.md](DATA-REQ-003.md) | Retention & deletion | Configurable retention + deletion workflow; financial records ≥ 5 years |
| DATA-REQ-004 | [DATA-REQ-004.md](DATA-REQ-004.md) | Backup & restore | Continuous WAL + daily snapshots; quarterly restore drills (NFR-006) |
| DATA-REQ-005 | [DATA-REQ-005.md](DATA-REQ-005.md) | Schema evolution | Expand–contract migrations; backward-compatible, zero-downtime deploys |
| DATA-REQ-006 | [DATA-REQ-006.md](DATA-REQ-006.md) | Data quality validation | Write-time validation + daily reconciliation (stock, wallet, escrow) |
| DATA-REQ-007 | [DATA-REQ-007.md](DATA-REQ-007.md) | Financial immutability | Append-only ledger via DB permissions; compensating entries only |
| DATA-REQ-008 | [DATA-REQ-008.md](DATA-REQ-008.md) | Ownership boundaries | Owner keys (`user_id`/`store_id`) on every scoped row, query- and test-enforced |

## Relation to `08-database/` and `16-data/`

- `08-database/` owns the **structure** — entities (`DB-nnn`), relationships, indexes, constraint definitions, migrations. It decides *how* a constraint is modeled.
- `16-data/` owns **data as a system concern** — lifecycle, classification taxonomy, ownership model, deletion/retention policy detail.
- This directory owns the **requirements** both must satisfy, with acceptance criteria `AC-DRnnn-nn`. Never restate an entity schema or classification table here — reference those documents by ID/path.

## Naming & ID Conventions

- Files: `DATA-REQ-nnn.md`. Document IDs: `DOC-DR-000` (this index) … `DOC-DR-008`. Acceptance criteria: `AC-DRnnn-nn` (e.g. `AC-DR004-02`).
- IDs are assigned only in `requirements-overview.md`; every file carries frontmatter with `category: 02-requirements`, `status: approved`, `source_of_truth: true`.

## Severity & Evidence Conventions

- Failure impact (where stated) uses `CRITICAL` · `HIGH` · `MEDIUM` · `LOW` · `INFORMATIONAL` (root README §8).
- Statements are evidence-tagged `VERIFIED` · `INFERENCE` · `INSUFFICIENT EVIDENCE`; exact PDPA erasure periods remain `INSUFFICIENT EVIDENCE` pending `DEP-09`.

## Verification

Each requirement declares its verification method (constraint test suite, job test with seeded data, restore drill, permission test, schema audit) and maps into `13-testing/`. Requirements whose acceptance criteria cannot pass are incomplete per `02-requirements/README.md` Quality Rules.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial index (8 requirements) | Initial analysis |
