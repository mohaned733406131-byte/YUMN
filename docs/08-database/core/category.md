---
document_id: DOC-DBE-004
entity_id: DB-004
title: Entity category (DB-004)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-004, FR-009, DATA-REQ-006]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-005, DOC-BA-005]
---

# Entity: `category` (DB-004) — table `b02.category`

## Overview & purpose

The classification tree that drives browse, storefront navigation, attribute scoping and search facets (FR-004, FR-009). A self-referencing parent chain with **depth ≤ 5 levels** and **slugs unique per level** (BR-CAT-03). Categories are seeded reference data (DOC-DB-006 §4) curated by admins; vendors assign products to leaf/mid categories. Bilingual names follow the Arabic-first rule (C-24).

## Field table

| Name | Type | Null | Default | Constraints | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | app-generated | PK | UUID v7 |
| `parent_id` | uuid | yes | null | FK `fk_category_parent_id` → `b02.category` ON DELETE RESTRICT | `NULL` = root; self-tree |
| `name_ar` | varchar(120) | no | — | `length(btrim(name_ar)) > 0` | Arabic primary (C-24) |
| `name_en` | varchar(120) | yes | null | — | English parity (C-24) |
| `slug` | varchar(140) | no | — | partial uniques (see below) | URL segment; unique **per level** (BR-CAT-03) |
| `level` | smallint | no | — | `ck_category_depth`: `BETWEEN 1 AND 5` | 1 = root (FR-004 five levels); maintained app-side with `parent_id` |
| `position` | smallint | no | `0` | `>= 0` | sibling ordering in navigation |
| `status` | `category_status` | no | `'ACTIVE'` | enum `ACTIVE, HIDDEN` | `HIDDEN` = removed from navigation/ browse roots; children stay addressable by direct link |
| `icon_key` | varchar(120) | yes | null | — | MinIO object key (optional) |
| `meta_title_ar` / `meta_title_en` | varchar(160) | yes | null | — | SEO/sharing text (FR-009) |
| `created_at` / `updated_at` | timestamptz | no | `now()` | trigger T1 on update | — |

Slug uniqueness (BR-CAT-03 "slugs unique per level") is expressed as **two partial unique indexes** because PostgreSQL treats `NULL` parents as distinct:

- `uq_category_root_slug` on `(slug)` WHERE `parent_id IS NULL`
- `uq_category_parent_slug` on `(parent_id, slug)` WHERE `parent_id IS NOT NULL`

## Indexes

- PK `id`
- `uq_category_root_slug`, `uq_category_parent_slug` (partial UNIQUE, above)
- `idx_category_parent_position` on `(parent_id, position)` — ordered navigation tree
- `idx_category_status_level` on `(status, level)` — tree editor + depth validation

## Relationships

| From | To | Cardinality | FK | ON DELETE |
|---|---|---|---|---|
| `category` (child) | `category` (parent) | N:0..1 | `fk_category_parent_id` | RESTRICT (re-parent or hide instead of dropping a subtree) |
| `product` (DB-005) | `category` | N:1 | `fk_product_category_id` | RESTRICT |
| `category_attribute` | `category` | N:1 | `fk_category_attribute_category_id` | CASCADE — attribute definitions per category (FR-004) |

## Invariants & business rules enforced

**DB-enforced**

1. Depth check `level BETWEEN 1 AND 5` (BR-CAT-03) — the *stored* level is validated; recomputing level/parent consistency is app-side.
2. Slug uniqueness per level via the two partial unique indexes (BR-CAT-03).
3. `parent_id` must reference an existing category; cycles prevented app-side (a parent must have `level < 5` and never be a descendant — checked before write, unit-tested).
4. `status` enum only `ACTIVE`/`HIDDEN`.

**App-enforced**

1. Re-parenting recomputes `level` and descendants' slugs/paths in one transaction (depth ≤5 validated before commit).
2. Deleting a category with products is blocked (products RESTRICT the FK) — vendors must reassign first (DATA-REQ-001).
3. Category moves emit a search reindex flag on affected products (ES is not the system of record — DOC-DB-002 §5).
4. Seeded root categories are idempotent (`ON CONFLICT DO NOTHING`, DOC-DB-006 §4).

## Example rows

```text
id=0198f900-…  parent_id=NULL          name_ar=إلكترونيات   name_en=Electronics  slug=electronics        level=1  position=1  status=ACTIVE
id=0198f944-…  parent_id=0198f900-…    name_ar=هواتف        name_en=Phones       slug=phones             level=2  position=1  status=ACTIVE
id=0198f97c-…  parent_id=0198f944-…    name_ar=أجهزة ذكية   name_en=Smartphones  slug=smartphones        level=3  position=1  status=ACTIVE
```

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
