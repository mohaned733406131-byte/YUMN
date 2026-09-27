---
document_id: DOC-OVR-006
title: Stakeholders
category: 00-project-overview
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-OVR-007, DOC-OVR-009]
---

# Stakeholder Register

| ID | Stakeholder | Role | Goals | Needs | Key Risks / Conflicts |
|---|---|---|---|---|---|
| STK-01 | Project sponsor / platform owner | Commissioner of the build | Launch on time, control cost, marketplace growth | Governance, transparent reporting | May trade quality for schedule |
| STK-02 | Product owner | Scope & priority authority | Correct product, clear requirements | Fast decisions on `GAP-*` items | Single point of decision bottleneck |
| STK-03 | Customers (buyers) | Primary users | Fair prices, protected payments, reliable delivery | Escrow trust, easy returns, Arabic UX | Distrust of digital payments → wallet adoption risk |
| STK-04 | Vendors (merchants) | Supply-side users | Sales growth, fast payouts, simple tools | Easy onboarding, clear fees, payout speed | Fee sensitivity; may push for COD (`C-01` conflict) |
| STK-05 | Delivery providers / couriers | Fulfillment users | Fair pay, clear assignments, fast confirmation | Simple pickup/dropoff flow, code confirmation | Code fraud attempts; earnings disputes |
| STK-06 | Platform admins / operations staff | Daily operators | Control, auditability, quick issue resolution | Powerful but safe admin tools, audit logs | Over-privilege risk → must be constrained by RBAC |
| STK-07 | Finance team | Money integrity | Reconciled ledger, correct commissions/payouts | Double-entry ledger, daily reports, payout controls | Ledger defect = existential risk (RISK-001) |
| STK-08 | Customer support team | Dispute resolution | Full context to resolve cases | Order/timeline visibility, ticket tooling | Without GPS (`C-16`), disputes rely on code evidence |
| STK-09 | Engineering team | Builders | Clear requirements, stable architecture, sane delivery pace | This knowledge base, ADRs, test strategy | Requirement churn; ambiguity in `GAP-*` items |
| STK-10 | QA team | Verification | Testable requirements, environments, test data | `TC-*` traceability, stable builds | Late requirement changes invalidate tests |
| STK-11 | Security / compliance officer | Assurance | Threat coverage, data protection, audit trail | Threat model, secrets hygiene, RBAC evidence | PDPA compliance detail `INSUFFICIENT EVIDENCE` |
| STK-12 | Payment partners (m-Floos, OneCash) | External integrators | Correct API usage, compliant flows | Stable integration contract (`10-integrations/`) | Outage/latency → top-up failures (RISK-003) |
| STK-13 | SMS/WhatsApp providers (Telesom, Sabafon, WhatsApp Business) | External integrators | Template compliance, deliverability | Failover routing (`FR-017`) | OTP delivery failure blocks all registration |
| STK-14 | Infrastructure / DevOps | Operators | Stable, observable, recoverable systems | Docker environments, monitoring, backups | Small team vs 99.99% target (RISK-005) |
| STK-15 | Legal / regulatory counsel | Compliance authority | Lawful operation (data protection, payments, tax) | Compliance opinions (`ASM-12`, `ASM-13`) | Regulations `INSUFFICIENT EVIDENCE` at analysis time |

## Conflicts of Interest

| Conflict | Resolution |
|---|---|
| Vendors want COD vs platform wallet-only (`C-01`) | Constraint wins; vendor communication is a change-management concern |
| Speed-to-market vs quality gates | `21-completion/quality-gates.md` — gates are non-negotiable for money paths |
| Feature richness vs operational simplicity (`C-21`/`C-22`) | Modular monolith enforced; simplification audit in `20-validation/` |
| Low commission (vendor attraction) vs revenue (platform) | Commission tiered 5–20%, default 10% (`BR-ESC-03`); adjust only via decision record |

## Potentially Omitted Stakeholders (identified by this analysis)

- **Payment-regulator liaison** (Central Bank oversight of wallets — `ASM-12`)
- **Tax advisor** (VAT collection/remittance obligations)
- **Logistics partners** beyond individual couriers (fleet operators) — `GAP-07`
- **Accessibility advocate / disabled-user representatives** — needed to validate `NFR-011` beyond automated checks

## Stakeholder Engagement

| Stakeholder Group | Engagement |
|---|---|
| STK-01, STK-02 | Weekly steering; approvals at quality gates |
| STK-03…STK-06 | Design reviews per prototype cycle; UAT participation |
| STK-07, STK-11 | Sign-off on ledger design & threat model before implementation |
| STK-12, STK-13 | Integration sandbox validation before staging |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
