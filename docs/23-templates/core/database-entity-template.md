---
document_id: DOC-TPL-007
title: Database Entity Template (entities/<table>.md)
category: 23-templates
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-DB-001, DOC-DB-003, DOC-DB-007, DOC-GL-003]
---

# Database Entity Template (DOC-TPL-007)

**When to use:** a new entity document in `08-database/<table>.md`. **Authority: `08-database/README.md` §1 (naming) + §2 (keys/UUID), DOC-DB-007 (entity index), DOC-DB-003 (ER overview)** — the ER overview is the register of the model; the entity file documents one table. Exemplar: `../../08-database/core/user.md` (DB-001).

## Rules

- **Filename is the table name**: singular `snake_case` (`sub_order`, not `sub-orders.md`) — file, table and entity doc always share the name (DOC-GL-003 §1).
- **`entity_id: DB-NNN` on line 2** of the frontmatter; mint the next free `DB-NNN` only in DOC-DB-007; `document_id: DOC-DBE-NNN` mirrors it; `category: 08-database`.
- Schema `b0n` = the owning block (`b01…b13`); title states both: `` Entity: `x` (DB-NNN) — table `b0n.x` ``.
- Columns: `snake_case`, FK `<entity>_id`, timestamps `*_at` (`timestamptz`, UTC), booleans `is_*`/`has_*`, money integer `*_yer`; PK `id uuid` (UUID v7, app-generated); indexes `idx_*`, uniques `uq_*`, checks `ck_*`, FKs `fk_*` (08-database README §1).
- Enums: snake_case type, `SCREAMING_SNAKE_CASE` values; soft delete `deleted_at`; append-only tables have `created_at` only, no `updated_at` (DOC-GL-003 §5).
- State *values* never drift from the 17 canonical order states (`C-09`, DOC-SA-010); money behaviour cites the governing `BR-*`; PII columns cite `SEC-REQ-002`/`DATA-REQ-002`.
- Every invariant is classified **DB-enforced** (constraint/index) vs **App-enforced (tests cover them)** — never leave that split implicit.
- Filled entity files carry `source_of_truth: false` (the ER overview and DB README hold authority).

## Template

```text
---
document_id: DOC-DBE-<nnn>
entity_id: DB-<nnn>
title: Entity <table-name> (DB-<nnn>)
category: 08-database
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: false
related_requirements: [<fr-sec-req-data-req-ids>]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-007, DOC-BA-005]
---

# Entity: `<table-name>` (DB-<nnn>) — table `b0n.<table-name>`

## Overview & purpose

<What this table is, which actors/flows it serves, the FRs it realizes, and the shaping requirements (PII, retention, money) — citing IDs, never restating definitions.>

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 (DOC-DB-001 §2) |
| `<column>` | <type> | <yes|no> | <default|—> | <ck_/uq_/enum/NOT NULL — or —> | <why it exists, with governing IDs> |
| `created_at` | timestamptz | no | `now()` | — | — |

<One closing paragraph for any deliberate non-column design (child tables, role rows, split storage) with its reasoning IDs.>

## Indexes

- `uq_<table>_<cols>` on `<cols>` (UNIQUE) — <purpose>
- `idx_<table>_<cols>` on `(<cols>)` — <query it serves>

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `<table>` | `<parent>` (DB-nnn) | N:1 | `fk_<table>_<column>` | <CASCADE|RESTRICT> |

## Invariants & business rules enforced

**DB-enforced**

1. <constraint/index — (BR-*/C-* citation)>

**App-enforced (tests cover them)**

1. <rule the application enforces — (BR-*/SEC-REQ-* citation)>

**Canon note:** <only if an interpretation was required here — record it, never change canon.>

## Example rows

<id>=<uuid-v7>  <col>=<representative value>  <col>=<representative value>   # e.g. states: ACTIVE / DELETED, locale AR

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | <date> | Initial version | Initial analysis |
```

## Pre-Submission Checklist

1. Filename = table = singular `snake_case`; `entity_id` on line 2 matches the DOC-DB-007 allocation; title names schema `b0n`.
2. Every column type/default/constraint follows `08-database/README.md` §1–§2 (UUID v7 PK, `*_at`, `*_yer`, `is_*`, enum casing, no plaintext PII).
3. Indexes and FKs use the `idx_/uq_/ck_/fk_` prefixes; relationship table states cardinality **and** `ON DELETE` behaviour.
4. Invariants split DB-enforced vs app-enforced; every cited BR/C/SEC-REQ/DATA-REQ ID exists; no 18th order state; no leftover `<…>`.
5. Frontmatter: `category: 08-database`, `source_of_truth: false`; version + Change History row on any edit (root README §9).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
