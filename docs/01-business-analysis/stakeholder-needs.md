---
document_id: DOC-BA-006
title: Stakeholder Needs
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-002, FR-013, FR-014, FR-017, FR-020]
related_documents: [DOC-BA-001, DOC-BA-004, DOC-BA-007, DOC-OVR-006, DOC-OVR-007]
---

# Stakeholder Needs

This document translates the stakeholder register (`00-project-overview/stakeholders.md`, `STK-01…STK-15`) into concrete product needs. It **does not repeat the register** — stakeholder identity, role, and goals stay there; only *what each stakeholder needs from yumn, how the platform meets it, and where needs conflict* live here. Needs are expressed as capabilities and are traced to `FR-*` / `BR-*` / `C-*` IDs, never restated definitions.

## 1. Need Translation by Stakeholder

| Stakeholder (ref) | Need from yumn | How addressed | Related IDs | Conflict / note |
|---|---|---|---|---|
| STK-01 Sponsor / platform owner | Launch on time, control cost, growth visibility, governance | Phased delivery against canon baseline; dashboards and reports; constraint envelope as non-negotiable gate | `OBJ-01`, `OBJ-12`, `FR-018`, `AC-S-01…04` | May trade quality for schedule — quality gates in money paths are non-negotiable (`21-completion/quality-gates.md` conflict resolution) |
| STK-02 Product owner | Clear scope, fast decisions on open items | Scope-creep control + explicit UNCERTAIN list | `GAP-01…GAP-06`, `project-scope.md`, `AC-S-01` | Single decision point = bottleneck risk; needs a decision cadence at weekly steering |
| STK-03 Customers | Fair prices, protected payments, reliable delivery, easy returns, Arabic UX | Escrow + wallet refunds, 6-digit code proof, return policy window, Arabic-first RTL default | `C-01`, `C-11`, `C-16`, `C-24`, `FR-013`, `FR-015`, `FR-016` | Distrust of digital payments → wallet adoption risk (`ASM-05`-class concern); trust is earned by ledger correctness (`BR-PAY-06`) and refund speed (`BR-RET-04`) |
| STK-04 Vendors | Sales growth, fast payouts, simple tools, clear fees | Vendor panel (catalog/inventory/orders/finance), tiered commission transparency, batched payouts 3–7 days, monthly statements | `FR-007`, `FR-008`, `FR-018`, `BR-ESC-03/05`, `BR-FIN-04` | Fee sensitivity + push for COD → **direct conflict with `C-01`**; resolution: constraint wins, communication is change management. Subscription tiers unresolved (`GAP-05`) |
| STK-05 Delivery providers | Fair pay, clear assignments, fast confirmation, simple flow | Zone-based offer queue (first accept wins), app-based pickup/dropoff, code entry confirmation, no GPS burden | `BR-SHP-04`, `BR-SHP-07`, `FR-015`, `C-16` | Code fraud attempts → 3-attempt limit + 24 h lock + ticket (`BR-SHP-03`); earnings disputes → admin review (`BR-SHP-06`) |
| STK-06 Platform admins / operations | Powerful but safe tools, auditability, quick issue resolution | Admin console with scoped RBAC, append-only audit on every privileged/money action, dispute & escalation views | `FR-020`, `FR-002`, `BR-PLT-06`, `BR-ORD-09` | Over-privilege risk → constrained by RBAC (`SEC-REQ-004`); admin can flag wallets but never edit the ledger (`BR-PAY-09`, `DATA-REQ-007`) |
| STK-07 Finance team | Reconciled ledger, correct commissions/payouts, payout controls | Double-entry append-only ledger, daily reconciliation, commission engine, payout gates | `BR-PAY-06`, `BR-ESC-08`, `BR-FIN-03/04/05`, `DATA-REQ-007`, `AC-S-14` | Ledger defect = existential (`RISK-001`); rounding differences posted to a platform account, never hidden (`BR-FIN-05`) |
| STK-08 Customer support | Full context to resolve cases without GPS | Order/timeline visibility per role, support tickets, auto-tickets on code lockout, evidence = code + timestamp + courier identity | `BR-ORD-09`, `FR-020`, `BR-SHP-03/06`, `BR-SHP-07` | No GPS (`C-16`) means disputes rely on code evidence — support capacity must scale with dispute rate (`BO-10`) |
| STK-09 Engineering team | Clear requirements, stable architecture, delivery pace | This knowledge base as the contract; modular monolith; ADRs | `C-21`, `C-20`, `NFR-009`, `OBJ-10` | Requirement churn from `GAP-*` items is the main ambiguity source; resolve blocking gaps before implementation gate |
| STK-10 QA team | Testable requirements, environments, test data | Every rule/requirement has a verification method; constraint test suite; traceability | `AC-S-02`, `AC-S-03`, `AC-S-08`, `AC-S-09` | Late requirement changes invalidate tests → changes go through root README §9 change management |
| STK-11 Security / compliance officer | Threat coverage, data protection, audit trail | Append-only audit, OTP/lockout controls, encryption, least-privilege RBAC | `SEC-REQ-001…012`, `BR-AUTH-04/05`, `BR-PLT-06` | PDPA detail `INSUFFICIENT EVIDENCE` (`ASM-13`, `DEP-09`) |
| STK-12 Payment partners (m-Floos, OneCash) | Correct API usage, compliant flows | Adapter abstraction, verified callbacks, reconciliation | `INT-REQ-001`, `INT-REQ-008`, `BR-PAY-03`, `DEP-05` | Outage/latency → top-up failures (`RISK-003`); fallback is admin-verified bank transfer (`BR-PAY-04`) |
| STK-13 SMS/WhatsApp providers | Template compliance, deliverability | SMS primary with automatic WhatsApp failover; bilingual templates | `INT-REQ-003`, `INT-REQ-004`, `BR-NTF-03/04`, `DEP-06` | OTP delivery failure **blocks all registration** — hardest dependency; security notices cannot be opted out (`BR-NTF-02`) |
| STK-14 Infrastructure / DevOps | Stable, observable, recoverable systems | Docker-only deployment, health gates, backups, monitoring, DLQ alerts | `C-22`, `C-26`, `NFR-005/006/014`, `BR-PLT-02/07` | Small team vs 99.99% target (`RISK-005`) — operational simplicity (`C-21`, `C-22`) is the mitigation |
| STK-15 Legal / regulatory counsel | Lawful operation: data protection, payments, tax | Compliance hooks: VAT on every order, audit retention, wallet freeze capability | `BR-FIN-01`, `NFR-019`, `BR-PAY-09`, `ASM-10/12/13` | Regulations `INSUFFICIENT EVIDENCE` — `ASM-12` (`DANGEROUS`) blocks wallet legitimacy (`DEP-10`) |

## 2. Cross-Cutting Need Groups

| Need group | Stakeholders | Requirement anchors | Notes |
|---|---|---|---|
| **Money integrity** (never lose or mis-count funds) | STK-03, STK-04, STK-07, STK-11 | `FR-013`, `FR-014`, `BR-PAY-05/06`, `BR-ESC-08` | Highest-priority group; any conflict with schedule/feature needs resolves toward integrity |
| **Trust without cash** (wallet-only acceptance) | STK-03, STK-04 | `C-01`, `BR-CRT-06`, `BR-PAY-01` | Adoption is a communication problem, not a configurability one — no setting may enable COD |
| **Operational visibility** (see what is happening) | STK-06, STK-08, STK-01, STK-07 | `FR-018`, `FR-020`, `BR-ORD-09`, `OBJ-08` | Scoped by role; never cross-customer access |
| **Localization & accessibility** (usable by the actual market) | STK-03, STK-04, STK-01 | `C-24`, `NFR-011`, `NFR-013`, `BR-PLT-05` | Arabic default with English parity |
| **Predictable external dependencies** | STK-12, STK-13, STK-14 | `DEP-05`, `DEP-06`, `INT-REQ-006`, `BR-PLT-02` | Failover + retries + DLQ so partner outages degrade, not crash |

## 3. Conflict Notes (need vs need)

| Conflict | Parties | Resolution (canon) |
|---|---|---|
| Vendors want COD vs customers wanting buyer protection | STK-04 vs STK-03 | Wallet-only wins — `C-01`; escrow is the trust substitute (`BR-ESC-01`) |
| Fast payouts vs refund/dispute protection | STK-04 vs STK-03 | 7-day escrow hold (`C-12`) then batched payout (`BR-ESC-05`); hold configurable with 7-day default (`ASM-09`) |
| Low commission (attract vendors) vs platform revenue | STK-04 vs STK-01/STK-07 | Tiered 5–20% default 10% (`BR-ESC-03`); changes only via decision record |
| Growth speed vs compliance certainty | STK-01 vs STK-11/STK-15 | Blocking assumptions (`ASM-12`, `ASM-04`) resolved before implementation gate |
| Feature richness vs operational simplicity | STK-01 vs STK-06/STK-14 | Modular monolith + Docker (`C-21`, `C-22`); simplification audit in `20-validation/` |
| Rich notifications vs provider cost/deliverability | STK-03 vs STK-13 | Category-level opt-out for marketing (`BR-NTF-05`); security notices always on (`BR-NTF-02`) |

## 4. Omitted Stakeholders (needs not yet served)

The register lists potentially omitted parties: payment-regulator liaison, tax advisor, fleet-operator logistics partners (`GAP-07`), accessibility advocates. Their needs are recorded but unaddressed in v1 — do not treat their absence as a resolved need.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
