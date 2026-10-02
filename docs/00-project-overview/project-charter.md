---
document_id: DOC-OVR-003
title: Project Charter (Executive Summary)
category: 00-project-overview
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-OVR-001, DOC-OVR-002, DOC-OVR-004]
---

# Project Charter — yumn

## Executive Summary

yumn is a **100% custom-built, multi-vendor e-commerce marketplace for Yemen**. It provides customers a trustworthy shopping experience (escrow-protected payments, code-confirmed delivery, wallet-based money flow), vendors a complete merchant operating system (catalog, inventory, orders, finance, storefront branding), and the platform operator full administrative, financial, and analytical control.

The platform is **Arabic-first (RTL)** with full English support, **wallet-only** (no cash on delivery, no cards, no BNPL, no crypto), and delivered as a **modular monolith** on a proven, operationally simple stack (Node.js/NestJS + PostgreSQL + Redis + Docker).

| Item | Value |
|---|---|
| Project name | yumn (يُمن) |
| Type | Greenfield product build |
| Market | Yemen (MENA expansion = future scope) |
| Primary actors | Customer, Vendor, Delivery Provider, Admin, Super Admin, Moderator, System |
| Decomposition | 13 blocks `B01…B13` |
| Functional baseline | 20 functional requirements `FR-001…FR-020` |
| Constraint baseline | 26 constraints `C-01…C-26` |
| Scale target | 10,000 concurrent users (`C-25`) |
| Availability target | 99.99% (`C-26`) |
| Delivery model | Phased (see `../21-completion/core/implementation-roadmap.md`) |

## Vision

Become Yemen's trusted digital marketplace — the default place to buy and sell online.

## Mission

Give every Yemeni merchant professional selling tooling and every customer protected, wallet-powered commerce with transparent delivery and returns.

## Authority

This charter authorizes the analysis, design, and implementation of the yumn platform within the scope and constraints defined in `project-scope.md` and `project-constraints.md`. Budget, staffing, and schedule baselines are `INSUFFICIENT EVIDENCE` at this stage (see `ASM-14`) — they must be established before implementation kickoff (`../21-completion/core/quality-gates.md`, Gate 0).

## High-Level Deliverables

1. **Customer experience** — Arabic-first storefront (responsive web + mobile apps), search, cart, 7-step checkout, order tracking, wallet, returns.
2. **Vendor experience** — vendor panel + mobile app: KYC onboarding, catalog, inventory, orders, finance, storefront configuration.
3. **Delivery experience** — courier mobile app: assignment queue, pickup/dropoff, 6-digit code confirmation.
4. **Platform operations** — admin console: users, vendors, catalog oversight, orders, finance, content, delivery ops, analytics, audit.
5. **Core platform services** — wallet with double-entry ledger, escrow engine, commission engine, 17-state order machine, notification fan-out (SMS/WhatsApp/in-app/push), search index.
6. **Quality foundation** — automated test suites, CI/CD, monitoring, backups, documentation (this knowledge base).

## Top-Level Success Statement

The project succeeds when: production is live at 99.99% availability, 10K concurrent users are supported within SLOs, all `C-01…C-26` constraints are verified, all `FR-001…FR-020` pass acceptance criteria with tests, and the first vendor completes a full sale → escrow → payout cycle end-to-end.

## Critical Success Factors

- Wallet trust (ledger integrity is non-negotiable — money bugs are existential)
- Arabic-first UX quality (the market is Arabic; poor RTL = product failure)
- Vendor onboarding simplicity (supply side drives the marketplace)
- Operational simplicity of infrastructure (small ops team, no Kubernetes, `C-22`)
- Discipline on constraints — every "convenient" deviation (COD, cards, microservices) is explicitly rejected by `C-01…C-26`

## Summary of Major Risks

Full register: `17-risk-management/core/risk-register.md`. Top three:

| ID | Risk | Severity |
|---|---|---|
| RISK-001 | Wallet/ledger data integrity defect | CRITICAL |
| RISK-002 | Vendor adoption slower than plan | HIGH |
| RISK-003 | Third-party wallet provider outage / commercial failure (`DEP-05`) | HIGH |

## Charter Approval

| Role | Status | Date |
|---|---|---|
| Project sponsor | PENDING | — |
| Product owner | PENDING | — |
| Technical lead | PENDING | — |

> Sign-off status: analysis produced; formal sponsor sign-off pending (`../21-completion/core/final-acceptance.md`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
