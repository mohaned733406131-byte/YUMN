---
document_id: DOC-BA-002
title: Business Model
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-011, FR-013, FR-014, FR-019]
related_documents: [DOC-BA-001, DOC-BA-003, DOC-BA-005, DOC-OVR-002, DOC-OVR-005]
---

# Business Model

yumn is a **commission-based, multi-vendor marketplace** (B2C2C: customer ↔ platform ↔ vendor) for Yemen. The platform intermediates discovery, wallet-funded payment, escrow protection, and code-confirmed delivery; it does not hold inventory and does not extend credit. All figures below are anchored to canon (`BR-*`, `C-*`, `OBJ-*`); anything not fixed by canon is tagged `INFERENCE` or `INSUFFICIENT EVIDENCE`.

## 1. Value Proposition per Actor

| Actor | Value proposition | Anchored by |
|---|---|---|
| Customer (`ACT-01`) | One Arabic-first (RTL) storefront for many Yemeni stores; escrow-protected payment (money released only after delivery), code-confirmed handover, wallet refunds, merchant-configurable returns, reviews from real purchases | `C-01`, `C-11`, `C-16`, `FR-013`, `FR-016` |
| Vendor (`ACT-02`) | Turnkey store: KYC onboarding ≤48 h, catalog/inventory/order/finance tooling, customer reach without building a site, transparent tiered commission, batched wallet payouts, monthly statements | `FR-007`, `FR-008`, `FR-018`, `BR-VND-03`, `BR-ESC-03`, `BR-ESC-05`, `BR-FIN-04` |
| Delivery Provider (`ACT-03`) | Paid per-delivery assignment queue for the same zone, simple pickup → transit → 6-digit-code flow, no GPS/device tracking burden, earnings tied to completed deliveries | `FR-015`, `BR-SHP-04`, `BR-SHP-07`, `C-16` |
| Admin / Super Admin (`ACT-04`, `ACT-05`) | Full operational control with auditability: KYC, orders, finance, disputes, roles, settings — every privileged/money action logged append-only | `FR-020`, `BR-PLT-06` |
| Moderator (`ACT-06`) | Focused scope: reviews, content, support escalation — powerful enough to act, constrained by RBAC | `FR-006`, `FR-020`, `BR-REV-04` |
| Platform (owner) | Take rate on every sale, data on the whole marketplace, defensible position in an informal market with no escrow incumbent | `BR-ESC-03`, `OBJ-02`, `OBJ-11` |

## 2. Revenue Streams

| # | Stream | v1 status | Definition | Evidence |
|---|---|---|---|---|
| R1 | **Sales commission** | **Live in v1** | Per-vendor tier **5–20%, default 10%**, applied to line subtotal after coupon discount, computed at escrow release, reversed proportionally on refund | `BR-ESC-03`, `BR-ESC-04` |
| R2 | Listing fees | **None in v1** — free listings by design (no canon rule permits charging for listings; vendors must not be blocked from publishing by a fee) | — | `INFERENCE` from absence of any `BR-PRM-*`/`BR-VND-*` fee rule; contradicted only if sponsor decides otherwise |
| R3 | Promoted placements / advertising | **Future scope** — explicitly parked, never a v1 requirement | — | `project-scope.md` FUTURE SCOPE |
| R4 | Delivery/shipping fee | **Collected at checkout** — `BR-SHP-01` fee = f(zone, weight, method); free with `free_shipping` coupon. Whether the fee accrues to platform or vendor is **not defined in canon** | — | `INSUFFICIENT EVIDENCE` — product-owner decision required before finance design |
| R5 | Vendor subscription / tiered commission plans | **Open question** — could later replace or supplement R1 | — | `GAP-05` (`project-scope.md` UNCERTAIN SCOPE) |

> No stream may be introduced that violates `C-01…C-05` (no COD, cards, BNPL, crypto, or extra top-up rails). The marketplace takes **no spread on wallet balances** — wallet funds are 1:1 YER, refunds return in full to the wallet (`BR-PAY-07`).

## 3. Cost Structure (`INFERENCE`, shaped by canon)

| Category | Drivers | Canon anchor |
|---|---|---|
| Platform build & maintenance | 100% custom build (no platform licensing), modular monolith, small team | `C-18`, `C-21`, `C-22` |
| Infrastructure | Docker hosts, PostgreSQL 16, Redis, Elasticsearch, object storage, CDN, TLS | `C-19`, `C-20`, `DEP-02…DEP-04`, `DEP-07`, `DEP-08` |
| Third-party services | SMS/WhatsApp OTP delivery (registration is blocked without it), wallet provider fees, reconciliation | `DEP-05`, `DEP-06`, `RISK-003`, `RISK-006` |
| Operations & support | KYC review (48 h SLA), dispute/return handling without GPS (evidence-based), support ticketing (no AI chatbot) | `BR-VND-03`, `BR-RET-06`, `FR-020` |
| Quality & compliance | Automated test suites, security scanning, legal opinions (VAT, data protection, Central Bank wallet position) | `AC-S-08`, `DEP-09`, `DEP-10` |
| Payout operations | Batched vendor payouts, daily reconciliation, monthly statements | `BR-ESC-05`, `BR-FIN-03`, `BR-FIN-04` |

Availability target (99.99%, `C-26`) and scale target (10,000 concurrent users, `C-25`) are cost floors, not aspirational extras.

## 4. Key Partners

| Partner | Role | Dependency | Risk if unavailable |
|---|---|---|---|
| **m-Floos, OneCash** | Wallet top-up rails (callback/poll credit) | `DEP-05`, `INT-REQ-001`, `BR-PAY-03` | Top-ups degrade to bank transfer only (`C-05` allows no other rails) |
| **Banks (Yemen)** | Admin-verified bank-transfer top-ups; future vendor cash-out considerations | `BR-PAY-04`, `INT-REQ-002`, `GAP-06` | Manual verification becomes the only funding path |
| **Telesom / Sabafon SMS + WhatsApp Business** | OTP and notification delivery, SMS → WhatsApp failover | `DEP-06`, `INT-REQ-003`, `INT-REQ-004`, `BR-NTF-03` | **Registration blocked** — hardest single blocker |
| **Couriers (individuals / small fleets)** | Zone-based pickup & delivery; first-accept assignment | `BR-SHP-04`, `ASM-07`, `GAP-07` | Fulfillment stops; assignment model rework if a national fleet emerges |
| **Legal / tax counsel** | VAT treatment, data protection, Central Bank wallet position | `DEP-09`, `DEP-10`, `ASM-10`, `ASM-12` | `ASM-12` is `DANGEROUS` — wallet-only model at risk |
| **Infrastructure vendors** | Domains, TLS, CDN, object storage | `DEP-07`, `DEP-08` | No public launch; media uploads unavailable |

## 5. Channels

| Channel | Audience | Notes |
|---|---|---|
| Customer web (responsive, Arabic-first RTL) | Customers | Primary discovery surface; LCP < 2.5 s on 4G (`NFR-002`) |
| Customer mobile app (Android/iOS) | Customers | Push notifications, courier code handoff experience |
| Vendor panel (web) + vendor mobile app | Vendors | Catalog, orders, finance, KYC |
| Courier mobile app | Delivery Providers | Assignment queue, pickup/dropoff, code entry |
| Admin / back-office console | Admin, Super Admin, Moderator | Operations, finance, content, audit |
| SMS / WhatsApp / in-app / push | All users | Only notification channels in v1 — **no email channel** (`BR-NTF-01`, `GAP-03`) |

## 6. Key Metrics

| Metric | Definition | Target / status |
|---|---|---|
| GMV | Total value of orders placed (order totals, incl. VAT & shipping) | Baseline targets `INSUFFICIENT EVIDENCE` (`GAP-01`, `ASM-14`) |
| Take rate | Commission ÷ GMV | Governed by 5–20% tier, default 10% (`BR-ESC-03`); blended take-rate target `INSUFFICIENT EVIDENCE` |
| Active vendors | Vendors with KYC = APPROVED and ≥1 ACTIVE product | Pilot gate: ≥10 pilot vendors complete full sale → payout cycle (`AC-S-21`) |
| Repeat purchase rate | Customers with ≥2 orders ÷ customers with ≥1 order | `INSUFFICIENT EVIDENCE` — track from launch (`OBJ-11`) |
| Wallet funding success | Successful top-ups ÷ top-up attempts | No canon target; monitored via reconciliation (`BR-ESC-08`) |
| Escrow accuracy | Escrow releases exactly per `BR-ESC-*` | 100%, zero ledger imbalance (`OBJ-02`, `AC-S-14`) |
| Delivery first-attempt code success | Deliveries confirmed on 1st code attempt | ≥95% (`OBJ-07`) |
| KYC decision time | Submission → decision | ≤48 h (`BR-VND-03`, `OBJ-06`) |
| Order state integrity | Deliveries without code | 0 (`OBJ-07`, `BR-ORD-08`) |

## 7. Unit Economics — Worked Example (100,000 YER order)

A single-customer cart containing one vendor's items, no coupon:

| Line | Calculation | Amount (YER) | Rule |
|---|---|---|---|
| Cart subtotal (items) | given | 100,000 | `BR-FIN-01` base |
| Coupon discount | none applied | 0 | `BR-PRM-02` (one coupon max) |
| VAT | 15% × (100,000 − 0) | **15,000** | `BR-FIN-01` (shipping not taxed) |
| Shipping fee | example zone/weight fee | 2,000 | `BR-SHP-01` |
| **Order total charged to wallet** | 100,000 + 15,000 + 2,000 | **117,000** | `BR-FIN-02`; debited at `PLACED`, balance never negative (`BR-PAY-05`) |
| Escrow funding | full order total held on `PLACED`; hold clock starts at `DELIVERED` | 117,000 | `C-10`, `BR-ESC-01` |
| Commission base | line subtotal after coupon discount | 100,000 | `BR-ESC-03` |
| **Commission (default 10%)** | 100,000 × 10% | **10,000** | `BR-ESC-03` (tier may range 5–20%: 5,000–20,000) |
| **Vendor payable after release** | 100,000 − 10,000 | **90,000** | `BR-ESC-02`; released after 7 days from `DELIVERED`, no dispute |
| Payout execution | batched, ≥1,000 YER minimum | 90,000 paid 3–7 business days after release | `BR-ESC-05`, `BR-ESC-06` |
| VAT liability | collected from buyer at checkout | 15,000 held for remittance per tax rules | `ASM-10` (`UNSUPPORTED` — legal confirmation via `DEP-09`) |
| Shipping fee destination | — | **not defined in canon** | `INSUFFICIENT EVIDENCE` — decision needed before finance design |

**Refund variant:** if the order is refunded later, commission is reversed proportionally (`BR-ESC-04`) and refunds draw from escrow-held funds first, then vendor payable (`BR-ESC-07`); the buyer is credited 117,000 to wallet within 3 business days of `REFUNDED` (`BR-RET-04`, `BR-PAY-07`).

**Scale of the model (`INFERENCE`):** break-even depends on GMV × blended take rate vs. fixed platform + SMS + infrastructure costs; no budget/GMV baseline exists yet (`ASM-14`), so break-even GMV is `INSUFFICIENT EVIDENCE` until the sponsor sets Gate 0 figures.

## 8. Lean Canvas Summary

| Canvas block | yumn answer |
|---|---|
| Problem | No buyer protection, no merchant tooling, informal cash delivery in Yemen (`project-context.md`) |
| Customer segments | Primary: Yemeni customers (mobile-first) and merchants; secondary: couriers; segment sizes `INSUFFICIENT EVIDENCE` (`GAP-01`) |
| Unique value proposition | "Yemen's market in your hands" — escrow-protected, wallet-funded, code-confirmed, Arabic-first commerce |
| Solution | 13-block custom platform: wallet + escrow + ledger, 17-state orders, code delivery, Arabic search, vendor OS |
| Channels | Web + 3 panels/apps + SMS/WhatsApp/push (§5) |
| Revenue streams | Commission R1 (§2); R2–R5 parked/undefined |
| Cost structure | §3 — custom build, infra, SMS, ops, compliance |
| Key metrics | §6 — GMV, take rate, active vendors, escrow accuracy, first-attempt delivery |
| Unfair advantage | First escrow-backed marketplace built for Yemeni rails (wallets, Arabic RTL, no-GPS code model); regulatory clearance (`DEP-10`) still pending |
| Early risks | Wallet adoption distrust (`STK-03`), vendor COD push vs `C-01` (`STK-04`), provider outages (`RISK-003`) |

## 9. Business-Model Constraints Check

Every stream and flow above was checked against `C-01…C-26`: no COD, no cards, no BNPL, no crypto, single currency YER, phone-only auth, domestic fulfillment only, code-based delivery. The model intentionally avoids credit and float-based revenue (no interest, no lending) — `C-03`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
