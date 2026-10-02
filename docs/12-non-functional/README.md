---
document_id: DOC-NFD-001
title: Non-Functional Detail Domain — Overview, Method & Target Dashboard
category: 12-non-functional
status: approved
version: 1.2
created: 2026-09-26
updated: 2026-10-03
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009, NFR-010, NFR-011, NFR-012, NFR-013, NFR-014, NFR-015, NFR-016, NFR-017, NFR-018, NFR-019, NFR-020]
related_documents: [DOC-NFR-000, DOC-REQ-001, DOC-AC-001, DOC-OVR-008, DOC-OVR-011, DOC-BA-005, DOC-ROOT-001]
---

# Non-Functional Detail Domain — Overview, Method & Target Dashboard

## 1. Purpose

This domain **elaborates** the 20 non-functional requirements (`NFR-001…NFR-020`) with the things a requirement statement alone cannot carry: numeric thresholds beyond the headline, budgets, mechanisms, operating policies, tooling, and verification hooks. It never restates requirement text — the statement of record lives in `02-requirements/` (`DOC-NFR-000` … `DOC-NFR-020`), IDs are assigned only in `02-requirements/requirements-overview.md` (`DOC-REQ-001` §2), and acceptance outcomes are registered in `02-requirements/acceptance-criteria.md` (`DOC-AC-001`).

## 2. Method — Statement → Elaboration → Verification

```text
02-requirements/core/NFR-nnn.md      "WHAT must hold"  (statement, rationale, AC refs)
        │
        ▼
12-non-functional/core/<domain>.md                  "HOW it holds at scale" (thresholds, budgets,
        │                                       mechanisms, policies, tooling, degradation)
        ▼
02-requirements/acceptance-criteria.md          "PASS/FAIL" (AC-NFR-nnn-nn, binary)
        │
        ▼
13-testing/                                     execution, evidence, TC-nnn linkage
```

Rules binding every file here:

1. **No restatement.** Reference `NFR-*` by ID; never copy the requirement's Metric/Target block wholesale — add *new* detail (per-surface splits, budgets, cadences, policies).
2. **Every elaboration is measurable**: a threshold, a ratio, a cadence or a named procedure. Qualitative claims are tagged `INFERENCE` or `INSUFFICIENT EVIDENCE`.
3. **No contradiction**: where canon fixes a number (99.99%, 10,000 users, ≥ 80% cache hit, ≥ 95% axe pass), it is inherited unchanged.
4. **AC alignment**: each file lists which `AC-NFR-*` / `AC-S-*` its detail feeds; it never invents new AC IDs.
5. Evidence tags (`VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`) per root README §8.

## 3. File Index

| # | File | document_id | Elaborates | Core content |
|---|---|---|---|---|
| 0 | `README.md` | DOC-NFD-001 | (this file) | method, dashboard, index |
| 1 | `performance.md` | DOC-NFD-002 | NFR-001, NFR-002, NFR-004 | latency budgets (API/page/OTP/image), throughput assumptions, per-surface budgets, tooling, degradation under load |
| 2 | `scalability.md` | DOC-NFD-003 | NFR-003, NFR-017, NFR-018 | capacity model, growth formulas, scaling levers under `C-22`, bottleneck order, partitioning path, k6 acceptance |
| 3 | `reliability.md` | DOC-NFD-004 | NFR-005, NFR-007, NFR-008 + `C-26` | availability math, error budgets, redundancy caveats, failure domains, degradation matrix, retry/idempotency, durability, chaos plan, SLI/SLO |
| 4 | `maintainability.md` | DOC-NFD-005 | NFR-009, NFR-010, NFR-016 | code standards, boundary enforcement, test pyramid targets, docs-as-code, lead time, environment parity, release cadence |
| 5 | `observability.md` | DOC-NFD-006 | NFR-014, NFR-020 + `INT-REQ-007` | RED/USE + business metrics, structured logs, tracing sampling, dashboards, alert severities, runbooks, telemetry retention |
| 6 | `compliance-and-legal.md` | DOC-NFD-007 | methodology §35 (legal/compliance), feeds NFR-019 | Yemen data-protection, wallet regulation, consumer rights, VAT, legal deliverables, KYC, messaging opt-in, audit retention, accessibility statement, sanctions |
| 7 | `usability-and-support.md` | DOC-NFD-008 | NFR-012, NFR-013 + support ops | task-efficiency targets, learnability, low-bandwidth mode, localization gates, human-only support model, SLAs, tooling, CSAT, feedback loop |
| 8 | `accessibility.md` | DOC-NFD-009 | NFR-011 (+ NFR-012, NFR-013) | measurable conformance targets per surface, assistive-technology matrix, CI automation thresholds, defect SLAs, Arabic/RTL accessibility specifics, verification & evidence |
| [`core/`](core/README.md) | DOC-NFD-010 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-NFD-011 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-NFD-012 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-NFD-013 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-NFD-014 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

> Note: root README §10 maps "Accessibility → `../11-ui-ux/core/accessibility.md` + `core/accessibility.md`". The UX patterns live in `../11-ui-ux/core/accessibility.md` (DOC-UX-006); the measurable NFR-011 elaboration lives in `accessibility.md` (DOC-NFD-009).

## 4. Consolidated Target Dashboard

One row per NFR — headline target only (the canonical statement remains `DOC-REQ-001` §2). "Detail" points to the elaborating file.

| NFR | Headline target (registry) | Elaborated here | Key added detail |
|---|---|---|---|
| NFR-001 | p95 < 200 ms read, < 500 ms write under nominal load | `performance.md` | p50/p99 splits, per-endpoint-class budgets, DB query p95, tooling (k6) |
| NFR-002 | LCP < 2.5 s on 4G; JS < 200 KB gzipped | `performance.md` | INP/CLS, per-surface budgets, font budget, RN metrics, Lighthouse CI gates |
| NFR-003 | 10,000 concurrent sustained within NFR-001 | `scalability.md` | request-rate model, headroom rules, drain criteria, mixed-profile composition |
| NFR-004 | cache hit ratio ≥ 80% on catalog reads | `performance.md` | per-route hit targets, staleness ceilings, cache-tier budgets |
| NFR-005 | 99.99% monthly (`C-26`) | `reliability.md` | 4.32 min/month budget math, probe design, burn-rate policy |
| NFR-006 | RTO ≤ 1 h; RPO ≤ 15 min | `reliability.md` | WAL cadence, drill design, backup freshness alerts, retention |
| NFR-007 | graceful degradation; no silent data loss | `reliability.md` | degradation matrix (ES/Redis/queue/SMS/MinIO/provider), recovery SLAs |
| NFR-008 | ACID + idempotency; zero ledger imbalance | `reliability.md` | idempotency key standard, reconciliation cadence, integrity invariants |
| NFR-009 | module boundaries enforced; CI gates; docs current | `maintainability.md` | dependency-cruiser rules, gate inventory, doc-freshness audit |
| NFR-010 | business logic unit-testable offline; coverage thresholds | `maintainability.md` | pyramid targets (80/95/90), suite budgets, flake policy |
| NFR-011 | WCAG 2.1 AA; ≥95% automated pass; 0 critical | `accessibility.md` + `../11-ui-ux/core/accessibility.md` | per-surface conformance matrix, AT support, CI thresholds, defect SLAs, RTL a11y (see DOC-NFD-009) |
| NFR-012 | registration→first order < 5 min; vendor listing < 10 min | `usability-and-support.md` | task matrix, SUS ≥ 78, dead-end rule, error-path audits |
| NFR-013 | Arabic default, English parity, locale-aware formats | `usability-and-support.md` | locale quality gates, template inventory, RTL regression set |
| NFR-014 | structured logs, RED metrics, correlation IDs, alerting | `observability.md` | field schema, sampling policy, dashboard list, alert severities, retention |
| NFR-015 | last-2 browsers; Android 10+, iOS 15+ | `performance.md` (device matrix) + `usability-and-support.md` | matrix expansion, device-lab cadence |
| NFR-016 | any Docker host; no cloud lock-in | `maintainability.md` | parity evidence, image digest equality, host baseline |
| NFR-017 | 10M products, 100M order lines, 5-year retention | `scalability.md` | partition plan, forecast variance, volume-test design |
| NFR-018 | stateless replicas; read replicas; documented scale path | `scalability.md` | scaling efficiency ≥ 80%, 10k→50k runbook steps, lag bounds |
| NFR-019 | PDPA-aligned controls, VAT on every order, ≥5 y audit retention | `compliance-and-legal.md` | VAT boundary matrix, legal deliverables, sign-off checklist |
| NFR-020 | runbooks, env config, health endpoints, zero-downtime deploys | `reliability.md` + `observability.md` | top-10 runbook list, health probe timings, rollback budget |

## 5. Cross-Cutting Numeric Invariants (inherited, never re-derived here)

| Invariant | Value | Canon |
|---|---|---|
| Concurrency acceptance | 10,000 VUs / 30 min | `C-25`, `AC-NFR-003-01` |
| Availability | 99.99% (≤ 4.32 min/month) | `C-26`, `AC-NFR-005-01` |
| RTO / RPO | ≤ 1 h / ≤ 15 min | `C-26`, `AC-NFR-006-01` |
| Latency | read p95 < 200 ms; write p95 < 500 ms | `AC-NFR-001-01/02` |
| Coverage | 80% overall / 95% payment / 90% auth | `AC-S-08`, `AC-NFR-010-01` |
| Accessibility | ≥ 95% automated pass; 0 critical/serious | `AC-NFR-011-01`, `AC-S-10` |
| Cache hit | ≥ 80% catalog reads; staleness ≤ 5 s | `AC-NFR-004-01/02` |
| Retention | financial/audit ≥ 5 years | `NFR-019`, `DATA-REQ-003` |
| Storage horizon | 10M products; 100M order lines | `NFR-017` |
| Locale set | exactly `ar` + `en` | `C-24` |

## 6. Reading Order

`performance` → `scalability` → `reliability` → `observability` → `maintainability` → `compliance-and-legal` → `usability-and-support`. Upstream: `02-requirements/` (statements), `00-project-overview/project-constraints.md` (`C-25`, `C-26`), `00-project-overview/success-criteria.md` (`AC-S-05…AC-S-10`, `AC-S-17…AC-S-20`). Downstream: `13-testing/` (execution), `14-devops-infrastructure/` + `15-deployment/` (wiring), `19-traceability/` (NFR → AC → TC).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-NFD-010…DOC-NFD-014) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
| 1.2 | 2026-10-03 | Fence flow-diagram ref +`core/` segment: `12-non-functional/<domain>.md` → `12-non-functional/core/<domain>.md` (all 9 NFR-domain docs live in `core/`) | Session-011 section-grouping rename follow-up (prompt-013 §2 leftover sweep) — moved-file outbound links / stale pre-portal path claims |
