---
document_id: DOC-PHA-009
title: Non-Functional Requirements (metrics per function) — analysis phase
category: phases
status: approved
version: 1.1
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-NFR-001, DOC-NFD-001, DOC-PHA-010]
related_requirements: [NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, NFR-010, NFR-011, NFR-013, NFR-017, NFR-020]
---

# Non-Functional Requirements (metrics per function) — analysis phase

## Purpose
CORE-03 item 7: measurable NFR budgets for every function class. Canonical requirement text: [`02-requirements/non-functional/`](../../02-requirements/non-functional/README.md) (`NFR-001`…`NFR-020`, 20 files); domain detail: [`12-non-functional/`](../../12-non-functional/README.md). This artifact rolls the budgets up and pins the **binding numbers** the adapter tightened ([`RULES_HINTS.md`](../../../senior-rules/RULES_HINTS.md) §6 — stricter than core defaults; may tighten, never loosen without written user approval).

## Scope
All user-facing and internal function classes: browse/search, cart/checkout, wallet/ledger, order lifecycle, notifications, admin operations, background jobs.

## Metrics per function class

| Function class | Metric | Budget | Canon |
|---|---|---|---|
| API reads | latency p95 | **< 200 ms** | `NFR-001`, `PRF-01` |
| API writes | latency p95 | **< 500 ms** | `NFR-001`, `PRF-01` |
| API error rate | errors/requests | **< 0.1%** | `NFR-003`, `PRF-01` |
| Concurrency | sustained load | **10,000 users × 30 min** | `C-25`, `NFR-003` |
| Web (all shells) | LCP / INP / CLS | **< 2.5 s / ≤ 200 ms / ≤ 0.1**; JS **< 200 KB gzipped**, vendor chunk ≤ 100 KB | `NFR-002`, `PRF-02` |
| Availability | uptime | **99.99%** (≤ 4.32 min / 30 d) | `C-26`, `NFR-005` |
| Recovery | RTO / RPO | **≤ 1 h / ≤ 15 min**, WAL ship ≤ 5 min | `NFR-006`, `PRF-03` |
| Cache | hit ratio / staleness | **≥ 80% / ≤ 5 s**; wallet, order, ledger, escrow, session responses **never cached** | `NFR-004`, `MNY-12` |
| Fault tolerance | degradation / recovery | ES/Redis down → browse works, recovery ≤ 60 s; queue 3 retries → DLQ alert ≤ 1 min; SMS→WhatsApp keeps OTP ≥ 99% | `NFR-007`, `PRF-04` |
| Data invariants | counts | **0** ledger imbalance, **0** negative balances/stock, **0** orphan rows, **100%** idempotency coverage | `NFR-008`, `PRF-05` |
| Test suite | duration / flakes | regression **< 30 min**, **0 flakes across 10 runs**; unit **< 3 min**; no wall-clock dependence | `NFR-010`, `AC-S-09`, `PRF-06` |
| Accessibility | automated pass | **WCAG 2.1 AA**, ≥ 95% automated pass, 0 critical/serious axe findings | `NFR-011` |
| Localization | locales | exactly `ar` (default, RTL) + `en`; no third locale; Arabic-Indic numerals for money in `ar` | `C-24`, `NFR-013` |
| Growth | volume | 10,000,000 products / 100,000,000 order lines / 5-year retention without re-architecture | `NFR-017`, `PRF-07` |
| Health | probe latency | `/healthz` + `/readyz` respond < 1 s; unhealthy instance removed ≤ 30 s | `NFR-020`, `OPS-07` |

## Preconditions for measurement
Benchmarks run on **staging only** (`OPS-06`); k6 scenarios `PERF-01`…`PERF-07` — exact invocation **NOT DOCUMENTED**, to be bound in Phase 1 bootstrap (`RULES_HINTS.md` §3).

## Postconditions
Every budget above has a named verification (k6 / size-limit / Lighthouse CI / uptime dashboard / invariant suite) — all **BLOCKED until code exists** (DOD-07).

## Open questions (COM-01)
1. Which NFR rows (registry has 20) inherit adapter-tightened numbers vs. corpus defaults — adapter §6 is authoritative; any loosening needs written user approval.

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 7, session 005) | analysis-agent |
| 2026-09-28 | 1.1 | Phantom citation DOC-REQ-010 replaced with DOC-NFD-001 in related_documents (session 006: CHK-07) | analysis-agent |
