---
document_id: DOC-DTA-001
title: Data Domain — README (16-data Index)
category: 16-data
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-002, DATA-REQ-003, DATA-REQ-004, DATA-REQ-005, DATA-REQ-006, DATA-REQ-007, DATA-REQ-008]
related_documents: [DOC-REQ-001, DOC-DR-000, DOC-BA-005, DOC-OVR-008, DOC-OVR-007]
---

# 16-data — Data as a System Concern

**yumn (يُمن)** — multi-vendor marketplace for Yemen; wallet-only payments (`C-01`), domestic shipping (`C-17`), phone-first identity (`C-06`, `BR-AUTH-01`).

## 1. Purpose

This domain owns the **data lifecycle policy layer**: what data exists, who owns it, how it is classified, how long it is kept, how it is deleted, and how its quality is proven. Four questions define the domain:

1. **Lifecycle** — where does each category of data come from, where does it live, who uses it, and when does it die? (`data-lifecycle.md`)
2. **Ownership** — which actor owns which data, who holds custody, and which roles may read or write it? (`data-ownership.md`)
3. **Classification** — how sensitive is each element, and what handling, encryption, masking, and logging rules follow from that? (`data-classification.md`)
4. **Retention & deletion** — how long is each class kept, how is it archived, purged, or erased on request? (`retention-and-archival.md`, `data-deletion-and-privacy.md`)

A fifth document, `data-quality.md`, defines how the platform proves its data is complete, valid, consistent, timely, and unique (`DATA-REQ-006`).

## 2. Boundary — What 16-data Owns and Does Not Own

`16-data/` is **policy and register**, not schema, not controls, not requirement prose. One authoritative document per concept (root README §4); everything else references it by ID or path.

| Domain | Owns | Does **not** own | Rule of thumb |
|---|---|---|---|
| **16-data (this)** | Lifecycle stages per category; ownership/access matrix; classification levels and the element inventory; retention schedule and purge policy; deletion/anonymization procedures; data-quality rules and reconciliation register | Table/column definitions, indexes, migrations; control implementations; requirement wording | If the question is "what policy governs this data through time?", it belongs here |
| **08-database** | Physical schema: entities (`DB-nnn`), relationships, constraints, indexes, migrations, partitioning mechanics (`DATA-REQ-001`, `DATA-REQ-005`) | Whether a field should exist, its classification, its retention period | 16-data decides *that* a phone number is CONFIDENTIAL and kept 24 months after closure; 08-database decides *how* it is stored and constrained |
| **09-security** | Controls: RBAC, authentication, encryption implementation, secrets, threat model, security findings (`SEC-NNN`) | The classification taxonomy itself and the retention/deletion schedule | Classification (16-data) *drives* control selection (09-security): CONFIDENTIAL ⇒ AES-256 at rest (`SEC-REQ-006`) |
| **02-requirements** | The requirement statements `DATA-REQ-001…008` with acceptance criteria (`AC-DRnnn-nn`) | Operational detail: actual periods, actual access rows, actual purge mechanics | Requirements say *what*; 16-data says *how, for which data, by whom* and is referenced by the requirements themselves |
| **03-system-analysis / 04-architecture** | Data flows and movement views | Ownership, classification, retention of the flowing data | Flow diagrams consume the categories defined here |
| **12-non-functional / 14-devops** | Measurable performance, observability, backup tooling | Which classes are backed up, for how long, and when purge evidence is required | Ops executes the schedule defined in `retention-and-archival.md` |

**Consistency rule:** `DATA-REQ-002` R1 requires every PII column to map to a purpose entry in `core/data-classification.md`; `DATA-REQ-003` R4/R5 and `DATA-REQ-004` R5 require retention and backup periods to be defined in `16-data/`. This domain is therefore the implementation target of four of the eight data requirements.

## 3. System-of-Record Map

| Store | Role | Source of truth? | Data held | Consistency model |
|---|---|---|---|---|
| PostgreSQL 16 (`C-19`, `DEP-02`) | **System of record** | **Yes** | Users, addresses, catalog, orders, ledger, escrow, audit trail, KYC metadata | ACID; referential integrity in DB (`DATA-REQ-001`) |
| Redis 7 (`DEP-03`) | Cache, rate limits, BullMQ queues (`C-20`), short-lived OTP/session state | **No** | Cache entries, counters, job payloads, OTP codes (TTL-bound) | Disposable — rebuildable from Postgres; never queried for business truth |
| Elasticsearch 8 (`DEP-04`) | Search index (derived) | **No** | Product/store/review documents for Arabic-aware search (`FR-009`) | Rebuilt from Postgres; deleted documents must be purged from it (`data-lifecycle.md` §6) |
| MinIO (`DEP-07`) | Object storage | **Yes, for objects** | Product images, review images, return evidence images, KYC documents | Object metadata keyed to Postgres rows; deletion cascades |
| BullMQ on Redis (`C-20`) | Async work | **No** | Job payloads (`{block}.{entity}.{action}`, `BR-PLT-01`) | At-least-once with idempotency (`BR-PLT-03`) |
| Prometheus / Grafana (`INT-REQ-007`) | Metrics | **No** | Aggregated counters/histograms | No PII in metric labels (`SEC-REQ-006` R5) |
| Backups (WAL + snapshots, `DATA-REQ-004`) | Recovery copies | **No** | Full Postgres state + object store | Retention window documented in `retention-and-archival.md` §6 |

**Never a source of truth:** Redis, Elasticsearch, BullMQ payloads, Prometheus, logs, caches (canon: Redis is cache/queues, ES is derived).

## 4. Requirement Coverage Map

| Requirement | 16-data owner document | What this domain contributes |
|---|---|---|
| `DATA-REQ-001` Integrity constraints | `data-quality.md` | Rule register with enforcement point per rule (DB CHECK vs app vs batch); 08-database owns DDL |
| `DATA-REQ-002` Personal data minimization | `data-classification.md`, `data-ownership.md` | Purpose-tagged element inventory; forbidden-field list (no card data `C-02`, no GPS `C-16`/`BR-SHP-05`) |
| `DATA-REQ-003` Retention & deletion | `retention-and-archival.md`, `data-deletion-and-privacy.md` | Retention schedule, purge mechanics, deletion flow, evidence entries |
| `DATA-REQ-004` Backup & restore | `retention-and-archival.md` §6, `data-deletion-and-privacy.md` §5 | Backup retention window and residual-copy aging-out policy |
| `DATA-REQ-005` Schema evolution | `data-lifecycle.md` §7 (interaction only) | Archive-compatible expand–contract note; migration detail stays in 08-database |
| `DATA-REQ-006` Data quality validation | `data-quality.md` | Dimensions, rules, reconciliation jobs, quarantine, quality SLOs |
| `DATA-REQ-007` Financial immutability | `data-lifecycle.md` §4, `data-ownership.md` §3, `retention-and-archival.md` | Append-only lifecycle stage, write-scope denial, 10-year retention class |
| `DATA-REQ-008` Ownership boundaries | `data-ownership.md` | Owner × custody × access × write-scope matrix; enforcement pointers |

## 5. File Index

| # | File | Document ID | Content | Source of truth |
|---|---|---|---|---|
| 1 | [README.md](README.md) | `DOC-DTA-001` | Domain charter, boundaries, store map, requirement coverage, index | Yes |
| 2 | [data-lifecycle.md](core/data-lifecycle.md) | `DOC-DTA-002` | CREATE → STORE → USE → SHARE → ARCHIVE → DELETE per data category; derived-data invalidation | No (supporting) |
| 3 | [data-ownership.md](core/data-ownership.md) | `DOC-DTA-003` | Ownership matrix: owner actor, platform custody, per-role access, write scope; storage-location assumption | Yes |
| 4 | [data-classification.md](core/data-classification.md) | `DOC-DTA-004` | 4-level scheme + full element inventory with encryption, retention class, masking, access | Yes |
| 5 | [retention-and-archival.md](core/retention-and-archival.md) | `DOC-DTA-005` | Retention classes `RC-01…RC-09`, retention schedule, purge & archive mechanics, legal-evidence gap | Yes |
| 6 | [data-deletion-and-privacy.md](core/data-deletion-and-privacy.md) | `DOC-DTA-006` | Deletion/anonymization procedures, cascade, verification, export, non-production masking | No (supporting) |
| 7 | [data-quality.md](core/data-quality.md) | `DOC-DTA-007` | Quality dimensions, rule register `DQ-01…DQ-18`, reconciliation jobs, quarantine, SLOs | No (supporting) |
| [`core/`](core/README.md) | DOC-DTA-008 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-DTA-009 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-DTA-010 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-DTA-011 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-DTA-012 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## 6. Governing Principles

| # | Principle | Anchor |
|---|---|---|
| P1 | One system of record: Postgres; caches and indexes are disposable | `C-19`, `DATA-REQ-001` |
| P2 | Collect only purposeful PII; no field without an inventory entry | `DATA-REQ-002` |
| P3 | Classify before you store; classification determines encryption, masking, access, retention | `DATA-REQ-002`, `SEC-REQ-006` |
| P4 | Money data is append-only and immutable; corrections are compensating entries | `DATA-REQ-007`, `BR-PAY-06` |
| P5 | Every tenant-scoped row carries owner keys; access is always scoped | `DATA-REQ-008`, `BR-VND-07` |
| P6 | Deleting primary data invalidates derived data (ES, cache, queues) in the same operation | `FR-009`, `DATA-REQ-003` |
| P7 | No secrets, OTPs, or PII in logs, metrics labels, or error payloads | `SEC-REQ-002` R4, `SEC-REQ-006` R5, `SEC-REQ-007` R4, `SEC-REQ-010` R3 |
| P8 | Retention periods are configuration consumed by a scheduled purge job, not code | `DATA-REQ-003` R1 |
| P9 | Every deletion and purge writes evidence (actor, scope, counts, timestamp) | `DATA-REQ-003` R5 |
| P10 | Non-production environments never contain unmasked production PII | `DATA-REQ-002`, `SEC-REQ-006` |
| P11 | Never collect excluded categories at all: card data (`C-02`), GPS/location (`C-16`, `BR-SHP-05`) | `DATA-REQ-002` R3 |
| P12 | Data is never sold; sharing is limited to purpose-bound processors | `DATA-REQ-002`, `data-lifecycle.md` §5 |

## 7. Conventions Used in This Domain

- **Evidence tags:** `VERIFIED` · `INFERENCE` · `INSUFFICIENT EVIDENCE` (root README §8). Every non-obvious period or assumption carries a tag.
- **Retention classes:** `RC-01…RC-09`, defined authoritatively in `retention-and-archival.md` §3 and referenced everywhere else by class ID.
- **Quality rules:** `DQ-01…DQ-18`, defined in `data-quality.md` §3.
- **Classification levels:** PUBLIC · INTERNAL · CONFIDENTIAL · RESTRICTED, defined in `data-classification.md` §2.
- **Cross-references** are by requirement/rule/constraint ID (`DATA-REQ-`, `FR-`, `BR-`, `SEC-REQ-`, `NFR-`, `C-`) and by `DOC-DTA-nnn`. Never restate a definition that lives elsewhere.
- **Masking notation:** `⟨MASK-…⟩` rules are enumerated in `data-classification.md` §5.
- **Actor names** are the canonical 7: Customer, Vendor, Delivery Provider (Courier), Admin, Super Admin, Moderator, System (`00-project-overview/actors-and-roles.md`, ACT-01…ACT-07).

## 8. Reading Order & Verification

**Reading order:** this README → `data-classification.md` (the inventory everything references) → `data-ownership.md` → `data-lifecycle.md` → `retention-and-archival.md` → `data-deletion-and-privacy.md` → `data-quality.md`.

**Verification:** this domain is verified through the acceptance criteria of `DATA-REQ-002…008` (`AC-DRnnn-nn` in `02-requirements/`), the cross-tenant suite of `DATA-REQ-008`, purge/evidence tests of `DATA-REQ-003`, and reconciliation tests of `DATA-REQ-006`; test design lands in `13-testing/`, traceability in `19-traceability/`. Policy changes here trigger the change-management rules of root README §9 and an entry in `../20-validation/core/consistency-audit.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-DTA-008…DOC-DTA-012) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
