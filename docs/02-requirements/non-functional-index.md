---
document_id: DOC-NFR-000
title: Non-Functional Requirements — Index (DOC-NFR-000)
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009, NFR-010, NFR-011, NFR-012, NFR-013, NFR-014, NFR-015, NFR-016, NFR-017, NFR-018, NFR-019, NFR-020]
related_documents: [DOC-REQ-001, DOC-REQ-002, DOC-OVR-004, DOC-OVR-008, DOC-OVR-011, DOC-BA-005, DOC-AC-001]
---

# Non-Functional Requirements — Index

## Purpose

This directory is the **source of truth for the 20 non-functional requirements `NFR-001…NFR-020`** of the yumn platform: the measurable quality attributes that gate release alongside the functional requirements. One file per NFR; every file states a precise target, a measurement method, and a pass/fail acceptance condition.

## NFR Index

IDs, titles and targets below are copied verbatim from the canonical registry `requirements-overview.md` §2 — that registry remains the only place where IDs are assigned; this index never diverges from it.

| ID | Title | Target (summary) |
|---|---|---|
| NFR-001 | API response time | p95 < 200 ms read, < 500 ms write under nominal load |
| NFR-002 | Client performance | LCP < 2.5 s on 4G mobile; JS bundle < 200 KB gzipped (customer web) |
| NFR-003 | Concurrency | 10,000 concurrent users (C-25) sustained within NFR-001 |
| NFR-004 | Caching | Read-heavy endpoints cached (Redis); cache hit ratio ≥ 80% on catalog reads |
| NFR-005 | Uptime | 99.99% monthly (C-26) |
| NFR-006 | RTO / RPO | RTO ≤ 1 h; RPO ≤ 15 min |
| NFR-007 | Fault tolerance | Graceful degradation: search/caches down → browse works; queue down → retries; no silent data loss |
| NFR-008 | Data integrity | ACID transactions; idempotency on all money/order/stock operations; zero ledger imbalance |
| NFR-009 | Modularity & standards | Monolith modules with enforced boundaries (C-21); lint/type/test gates in CI; docs current |
| NFR-010 | Testability | All business logic unit-testable without network; coverage thresholds (AC-S-08) |
| NFR-011 | WCAG 2.1 AA | ≥95% automated pass; zero critical violations; keyboard + screen-reader support |
| NFR-012 | Core-task efficiency | New customer completes registration→first order < 5 min; vendor lists product < 10 min |
| NFR-013 | Bilingual RTL/LTR | Arabic default, English parity; locale-aware dates/numbers/currency (C-24) |
| NFR-014 | Logging/metrics/tracing | Structured logs, RED metrics per endpoint, correlation IDs, alerting |
| NFR-015 | Browsers/devices | Last 2 versions Chrome/Safari/Firefox/Edge; Android 10+, iOS 15+ |
| NFR-016 | Deployment | Runs on any Docker host; no cloud-vendor lock-in in v1 |
| NFR-017 | Storage growth | Design for 10M products, 100M order-line records, 5-year retention (partitioning plan) |
| NFR-018 | Scale-out path | Stateless API replicas behind LB; DB read replicas; documented path beyond C-25 |
| NFR-019 | Legal/data | PDPA-aligned controls, VAT on every order, audit retention ≥ 5 years for financial records |
| NFR-020 | Supportability | Runbooks, config via environment, health endpoints, zero-downtime deploys |

## How NFRs Are Measured

Each `NFR-nnn.md` file carries its own **Metric / Target**, **Measurement Method** and **Verification / Acceptance** sections (the "measurability contract"). Detailed measurement plans — load-test scenarios, SLO dashboards, chaos drills, accessibility pipelines — live one domain over in **`12-non-functional/`** (`performance.md`, `reliability.md`, `scalability.md`, `accessibility.md`, `maintainability.md`, `observability.md`). This directory defines *what* must hold; `12-non-functional/` defines *how* it is measured at scale. Acceptance outcomes are registered in `02-requirements/acceptance-criteria.md` under `AC-NFR-*` IDs and executed by `13-testing/`.

## Source-of-Truth Statement

- **IDs, titles and target summaries are fixed in `requirements-overview.md` §2** (`DOC-REQ-001`). If this index or any `NFR-nnn.md` file appears to contradict the registry, the registry wins and the discrepancy goes to `../20-validation/core/contradiction-audit.md`.
- These files are the authoritative expansion of each NFR (description, rationale, method, consequences). Other documents **reference the NFR ID — never copy its definition.**
- Constraints (`C-01…C-26`), objectives (`OBJ-*`) and success criteria (`AC-S-*`) referenced here are owned by `00-project-overview/`; business rules by `01-business-analysis/business-rules.md`.

## Measurability Rule

> **Every NFR MUST have (1) at least one quantitative metric with a threshold, (2) a named measurement tool or procedure, and (3) a binary verification/acceptance condition mapped to an `AC-NFR-*` ID.**

An NFR without all three is incomplete, fails the 7-question requirement quality test in `requirements-overview.md` §6, and must not be marked `APPROVED`. Qualitative wording ("fast", "secure", "scalable") is only acceptable once quantified in the Metric / Target section.

## Naming & IDs

```text
Files:        NFR-001.md … NFR-020.md      (lowercase-safe pattern: NFR-nnn.md)
Document IDs: DOC-NFR-000 (this index) … DOC-NFR-020 (one per NFR file)
Acceptance:   AC-NFR-001-01, AC-NFR-001-02 … (registered in acceptance-criteria.md)
Categories:   Performance · Scalability · Availability · Recoverability · Reliability
              Maintainability · Accessibility · Usability · Localization · Observability
              Compatibility · Portability · Capacity · Compliance · Operability
```

## Related Directories

`02-requirements/requirements-overview.md` (registry) · `02-requirements/acceptance-criteria.md` (`AC-NFR-*`) · `12-non-functional/` (measurement detail) · `13-testing/` (verification) · `19-traceability/` (NFR → test mapping)

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial NFR index (20 NFRs) | Initial analysis |
