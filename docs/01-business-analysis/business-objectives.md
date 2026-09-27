---
document_id: DOC-BA-003
title: Business Objectives (BO-01 … BO-12)
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-014, FR-018, FR-020]
related_documents: [DOC-BA-001, DOC-BA-002, DOC-OVR-004, DOC-OVR-011]
---

# Business Objectives

**Business-side objectives `BO-01…BO-12`** — the marketplace outcomes the business must achieve. These are deliberately **distinct from the project objectives `OBJ-01…OBJ-12`** (`00-project-overview/project-objectives.md`), which govern the *build* (launch coverage, performance, availability, test velocity). `BO-*` govern the *operation* once live: liquidity, vendor retention, payment trust, and operational efficiency. Where canon fixes a number, it is cited; where it does not, the target is tagged `INFERENCE` or `INSUFFICIENT EVIDENCE` — never invented as fact.

**Objective families:** Liquidity (`BO-01…BO-03`) · Vendor retention (`BO-04…BO-06`) · Payment trust (`BO-07…BO-09`) · Operational efficiency (`BO-10…BO-12`).

## 1. Marketplace Liquidity

| ID | Objective | Owner | Metric | Target | Evidence |
|---|---|---|---|---|---|
| BO-01 | Grow supply so every search returns buyable results | Product owner | Active vendors (KYC approved + ≥1 ACTIVE product) and ACTIVE listings per category | Pilot gate: ≥10 pilot vendors complete sale → payout (`AC-S-21`); steady-state counts `INSUFFICIENT EVIDENCE` until sponsor sets them (`GAP-01`) | `AC-S-21`, `GAP-01` |
| BO-02 | Grow demand and transaction volume | Product owner / sponsor | Orders placed per week; GMV per month | Launch targets `INSUFFICIENT EVIDENCE` (`GAP-01`, `ASM-14`); tracking instrumented from day one (`OBJ-11`) | `GAP-01`, `OBJ-11` |
| BO-03 | Convert browsing into completed, code-confirmed purchases | Product owner | Funnel: search → add-to-cart → checkout → `DELIVERED` conversion; abandonment at the 7-step checkout | `INFERENCE`: checkout is the highest-leverage step; numeric target `INSUFFICIENT EVIDENCE` (no baseline) | `FR-009`, `FR-010`, `FR-011` |

## 2. Vendor Retention

| ID | Objective | Owner | Metric | Target | Evidence |
|---|---|---|---|---|---|
| BO-04 | Onboard vendors fast enough to keep supply momentum | Operations | Time from KYC submission → decision; vendor time-to-first-listing | KYC decision ≤48 h (`BR-VND-03`); first vendor live within 48 h of application (`OBJ-06`); product listed <10 min (`NFR-012`) | `BR-VND-03`, `OBJ-06`, `NFR-012` |
| BO-05 | Keep vendors paid and trusting the money flow | Finance | Payout cycle time from release → execution; % payouts below minimum rolled over; monthly statement delivery | Payouts batched 3–7 business days after escrow release, min 1,000 YER (`BR-ESC-05`); statement monthly (`BR-FIN-04`); zero payout without KYC approval (`BR-ESC-06`) | `BR-ESC-05`, `BR-FIN-04` |
| BO-06 | Keep commission terms transparent and competitive | Product owner / Finance | Effective take rate per vendor tier; vendor disputes over fees | Tiered 5–20%, default 10%, computed at release and reversed proportionally on refund (`BR-ESC-03`, `BR-ESC-04`); changes to tiers require a decision record per `stakeholders.md` conflict resolution; subscription tiers remain `GAP-05` | `BR-ESC-03`, `GAP-05` |

> **Known tension:** vendors may push for COD and resist the 7-day escrow hold (`STK-04`, `ASM-09`). Resolution: constraints win (`C-01`); hold period is a platform config with default 7 days (`ASM-09`), and vendor communication is a change-management activity, not a requirement change.

## 3. Payment Trust

| ID | Objective | Owner | Metric | Target | Evidence |
|---|---|---|---|---|---|
| BO-07 | Make the wallet safe enough that customers pre-fund it | Product owner | Wallet adoption: % of orders paid from wallet; top-up success rate; negative-balance incidents | 100% of orders paid from wallet (enforced, `C-01`/`BR-PAY-01`); balance never negative (`BR-PAY-05`); top-up credit only on verified callback/admin verification (`BR-PAY-03`, `BR-PAY-04`) | `OBJ-02`, `BR-PAY-01`, `BR-PAY-05` |
| BO-08 | Keep the ledger provably correct | Finance | Daily reconciliation result: Σ ledger entries balance; wallet + escrow + payable = provider statements | **Zero imbalance**, reported next morning (`BR-ESC-08`, `BR-FIN-03`, `AC-S-14`, `OBJ-08`); corrections only via compensating entries (`DATA-REQ-007`) | `BR-ESC-08`, `AC-S-14` |
| BO-09 | Protect buyers so they keep buying | Product owner / Support | Dispute rate; refund cycle time; escrow releases with active dispute (must be 0) | Escrow releases only when 7 days elapsed and no dispute (`BR-ESC-02`); wallet credit ≤3 business days from `REFUNDED` (`BR-RET-04`); dispute outcomes resolved by admin with audit (`BR-RET-06`) | `BR-ESC-02`, `BR-RET-04` |

## 4. Operational Efficiency

| ID | Objective | Owner | Metric | Target | Evidence |
|---|---|---|---|---|---|
| BO-10 | Resolve delivery exceptions without GPS | Operations / Support | First-attempt code success; locked confirmations; escalations to admin review | ≥95% confirmed on first code attempt (`OBJ-07`); 0 successful deliveries without code (`OBJ-07`, `BR-ORD-08`); 3rd failure → 24 h lock + ticket (`BR-SHP-03`) and admin review (`BR-SHP-06`) | `OBJ-07`, `BR-SHP-03`, `BR-SHP-06` |
| BO-11 | Run the platform with a small operations team | Admin lead / Super Admin | % of state-changing admin actions audited; support ticket resolution time; manual rework per 1,000 orders | 100% of privileged/money actions audited (`OBJ-08`, `BR-PLT-06`); ticket flow live at launch (`AC-S-23`); ticket SLA `INSUFFICIENT EVIDENCE` (no canon value) | `BR-PLT-06`, `AC-S-23` |
| BO-12 | Detect and contain financial/operational defects fast | Finance / Engineering | Reconciliation lag; alert time to DLQ depth / ledger mismatch; incident MTTR | Daily reconciliation available next morning (`OBJ-08`); DLQ depth alerts (`BR-PLT-02`); MTTR within RTO ≤1 h (`NFR-006`, `C-26`) | `BR-PLT-02`, `NFR-006` |

## 5. Relationship to Project Objectives

| | Project objectives `OBJ-*` | Business objectives `BO-*` |
|---|---|---|
| Scope | The **build**: coverage, performance, availability, quality velocity, constraint envelope | The **operation**: liquidity, retention, trust, efficiency |
| Owner | Project sponsor / technical lead | Product owner / platform owner / finance |
| Example | `OBJ-04` p95 < 200 ms at 10k users | `BO-03` search → checkout conversion |
| Overlap | `OBJ-02` (trust-safe payments) underpins `BO-07…BO-09`; `OBJ-06` (vendor onboarding) underpins `BO-04`; `OBJ-11` (liquidity) is the project-side shadow of `BO-01…BO-03` |

No `BO-*` may be satisfied by violating a constraint; no `BO-*` restates an `OBJ-*` definition — where they align, only `OBJ-*` carries the canonical measure.

## 6. Target-Setting Rule

Launch growth targets (vendors, listings, orders, GMV) are `INSUFFICIENT EVIDENCE` until the sponsor sets them at Gate 0 (`GAP-01`, `ASM-14`). This document must not be patched with invented numbers; when targets arrive, `BO-01`, `BO-02`, and `BO-03` are updated via change management with a version bump.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version (12 business objectives) | Initial analysis |
