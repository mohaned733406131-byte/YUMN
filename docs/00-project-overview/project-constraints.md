---
document_id: DOC-OVR-008
title: Project Constraints (C-01 … C-26)
category: 00-project-overview
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [FR-020]
related_documents: [DOC-OVR-005, DOC-OVR-010]
---

# Project Constraints

**26 non-negotiable constraints (`C-01…C-26`).** These override all other considerations — no recommendation, design, or request may violate them. Every constraint has a verification method; constraint tests live in `13-testing/constraint-tests.md`.

## Payment Constraints

| ID | Constraint | Rationale | Verification |
|---|---|---|---|
| C-01 | **Wallet-only payments.** Cash on Delivery (COD) is prohibited in all flows. | Trust model: escrow requires pre-funding; COD has no buyer protection & high RTO | Integration test: order creation rejects `payment_method != wallet` (`TST-CON-01`) |
| C-02 | **No card payments.** No credit/debit card processing, no card networks, no third-party card processors (Stripe, Moyasar, Tap, etc.). | Regulatory/licensing risk; no PCI scope | Static scan + API test: no card fields/endpoints exist |
| C-03 | **No BNPL / installments / credit.** | Avoid credit risk & regulation | Requirement + code review |
| C-04 | **No cryptocurrency; single currency.** Fiat YER only — no USD/SAR wallets in v1. | Regulatory & volatility risk; operational simplicity | Code review of payment module |
| C-05 | **Wallet top-up methods:** mobile wallet (m-Floos, OneCash, **Al-Kuraimi Bank, Jeeb** — amended 2026-09-28) and bank transfer (manual admin verification). No other instruments. | Local rails reality | Integration tests per method (`API-WAL-003/004`) |

## Authentication Constraints

| ID | Constraint | Rationale | Verification |
|---|---|---|---|
| C-06 | **Phone + OTP only.** Primary identifier is the phone number; verification via SMS or WhatsApp. No email-primary auth, no social login. An **optional, verified email address** may exist on a profile (contact/notification only — never identifier, never OTP channel; amended 2026-09-28). | Yemeni market reality — phone is universal, email is not | Integration tests: register/login paths |
| C-07 | **No biometrics** in v1 (device-level biometrics may unlock the app locally only, never as server auth). | Simplicity / coverage | Code review |
| C-08 | **JWT lifetimes:** access token 15 minutes, refresh token 7 days with single-use rotation. | Security baseline | Security test `SEC-REQ-003` |

## Order & Commerce Constraints

| ID | Constraint | Rationale | Verification |
|---|---|---|---|
| C-09 | **Exactly 17 order states** — the canonical list in `03-system-analysis/state-transitions.md`. | Shared vocabulary across 4 surfaces | State-machine unit tests (17/17 states covered) |
| C-10 | **Master/Sub-order architecture.** One master order per checkout; one sub-order per vendor. Payment & escrow at master level; fulfillment & payout per sub-order. | Multi-vendor settlement reality | Integration tests for split orders |
| C-11 | **Merchant-configurable return policy** (`isReturnable`, `returnPeriodDays` per product/store); return window starts at delivery confirmation. | Merchant autonomy + buyer clarity | Rule tests `BR-RET-01…03` |
| C-12 | **Escrow:** funds held 7 days from DELIVERED before release to vendor (unless dispute freezes). | Buyer protection window | Escrow engine tests |
| C-13 | **Stock reservation:** 15-minute TTL hold at checkout; auto-release on expiry; permanent deduction on payment. | Prevent oversell without prepayment | Timer + concurrency tests |
| C-14 | **Order value bounds:** minimum 500 YER, maximum 5,000,000 YER per order. | Operational/risk bounds | Validation tests at both boundaries |
| C-15 | **Cart guards:** ≤50 products, ≤10 units per product, ≤5 vendors per cart. | Checkout/payoff clarity | Validation tests |

## Delivery Constraints

| ID | Constraint | Rationale | Verification |
|---|---|---|---|
| C-16 | **No GPS / no real-time tracking.** Delivery completion is confirmed by a **6-digit code** (3 attempts → 24 h lock + support ticket). | Device/network realities; privacy | E2E delivery flow tests; no location APIs in contract |
| C-17 | **Domestic Yemen fulfillment only** in v1. | Scope | Shipping zone config tests |

## Technical Constraints

| ID | Constraint | Rationale | Verification |
|---|---|---|---|
| C-18 | **100% custom build** — no Shopify/Medusa/WooCommerce/Saleor or other commerce platforms. | Control & differentiation | Dependency audit |
| C-19 | **PostgreSQL 16** is the only relational database. | Consistency | Deployment config review |
| C-20 | **BullMQ** is the only job/queue system (Redis-backed). No RabbitMQ, no Kafka. | Operational simplicity | Dependency audit |
| C-21 | **Modular monolith** — no microservices. | Team size & operability (`ADR-002`) | Architecture review |
| C-22 | **Docker + Docker Compose deployment; no Kubernetes in v1.** | Simplicity (`ADR-004`) | Deployment config review |
| C-23 | **Greenfield** — no legacy system migration or coexistence. | Clean start | Scope audit |
| C-24 | **Arabic-first RTL**, full English parity; only these two locales. | Market | i18n tests; RTL visual regression |

## Business & Quality Constraints

| ID | Constraint | Rationale | Verification |
|---|---|---|---|
| C-25 | **10,000 concurrent users** must be supported within NFR targets. | Scale target | Load test (`NFR-003`) |
| C-26 | **99.99% availability** (≤ 4.32 min downtime/month), RTO ≤ 1 h, RPO ≤ 15 min. | Trust & operations | Monitoring + DR drill |

> Note: three exclusions are governed by scope decisions rather than numbered constraints, to keep this register at exactly 26 items: **no AI chatbot** (human ticketing support only, `FR-020`), **no subscription products**, and **no trial/sample/rental products**. All three are recorded in `project-scope.md` OUT OF SCOPE and are just as binding as constraints for v1.

## Constraint Interaction Map (selected)

```text
C-01 (wallet-only) ──requires──► C-05 (top-up rails), C-12 (escrow), FR-013/FR-014
C-09 (17 states)   ──drives────► C-10 (master/sub), C-16 (code confirm), FR-012
C-16 (no GPS)      ──drives────► code lockout rule (BR-SHP-03), support tooling (FR-020)
C-21 (monolith)    ──drives────► C-20 (BullMQ), C-22 (Docker), ADR-002/ADR-004
C-24 (Arabic)      ──drives────► NFR-012, frontend RTL design, ES Arabic analyzer
```

## Conflict Check

No constraint conflicts with another (`VERIFIED` by pairwise review — recorded in `20-validation/contradiction-audit.md`, entry CT-01: PASS). Apparent legacy conflicts (COD allowed, Kubernetes, microservices) do not exist in this analysis — they are OUT OF SCOPE.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial 26 constraints | Initial analysis |
| 1.1 | 2026-09-28 | **Amended `C-05`** (+Al-Kuraimi Bank, Jeeb wallets) and **`C-06`** (optional *verified* email on profile — never identifier/OTP); `C-05` verification citation fixed from phantom `API-TOP-*` to `API-WAL-003/004` (`HAL-15`) | `plan-develop.md` §8 `D1` approval (administrator, 2026-09-28) — `GAP-13` mixed disposition: `CT-24`/`CT-25` → RESOLVED, `HAL-15` → RESOLVED; count stays 26 (amendments, not new constraints) |
