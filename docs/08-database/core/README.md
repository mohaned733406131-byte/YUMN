---
document_id: DOC-DB-008
title: 08 Database — core/ portal folder
category: 08-database
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-DB-001]
---

# 08 Database · `core/`

## Purpose

One of the five portal subfolders of `08-database/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-DB-008 | This portal index — purpose, file table |
| [address.md](address.md) | DOC-DBE-002 | Entity address (DB-002) |
| [audit_log.md](audit_log.md) | DOC-DBE-018 | Entity audit_log (DB-018) |
| [cart.md](cart.md) | DOC-DBE-007 | Entity cart (DB-007) |
| [category.md](category.md) | DOC-DBE-004 | Entity category (DB-004) |
| [constraints-and-integrity.md](constraints-and-integrity.md) | DOC-DB-005 | Constraints and Integrity Enforcement |
| [coupon.md](coupon.md) | DOC-DBE-016 | Entity coupon (DB-016) |
| [database-overview.md](database-overview.md) | DOC-DB-002 | Database Architecture Overview (PostgreSQL 16 + Prisma 5) |
| [entity-relationship.md](entity-relationship.md) | DOC-DB-003 | Entity-Relationship Register |
| [escrow.md](escrow.md) | DOC-DBE-012 | Entity escrow (DB-012) |
| [indexes-and-performance.md](indexes-and-performance.md) | DOC-DB-004 | Indexes and Performance Strategy |
| [inventory.md](inventory.md) | DOC-DBE-006 | Entity inventory (DB-006) |
| [migrations-and-evolution.md](migrations-and-evolution.md) | DOC-DB-006 | Migrations and Schema Evolution |
| [notification.md](notification.md) | DOC-DBE-017 | Entity notification (DB-017) |
| [order.md](order.md) | DOC-DBE-008 | Entity order (DB-008) |
| [payment.md](payment.md) | DOC-DBE-009 | Entity payment (DB-009) |
| [product.md](product.md) | DOC-DBE-005 | Entity product (DB-005) |
| [return_request.md](return_request.md) | DOC-DBE-014 | Entity return_request (DB-014) |
| [review.md](review.md) | DOC-DBE-015 | Entity review (DB-015) |
| [shipment.md](shipment.md) | DOC-DBE-013 | Entity shipment (DB-013) |
| [store.md](store.md) | DOC-DBE-003 | Entity store (DB-003) |
| [user.md](user.md) | DOC-DBE-001 | Entity user (DB-001) |
| [wallet.md](wallet.md) | DOC-DBE-010 | Entity wallet (DB-010) |
| [wallet_transaction.md](wallet_transaction.md) | DOC-DBE-011 | Entity wallet_transaction (DB-011) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (23 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
