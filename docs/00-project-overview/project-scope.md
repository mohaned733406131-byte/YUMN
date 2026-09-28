---
document_id: DOC-OVR-005
title: Project Scope
category: 00-project-overview
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-OVR-001, DOC-OVR-008]
---

# Project Scope

## IN SCOPE (v1 — must implement)

### Platform Core
- Multi-vendor marketplace with 13-block decomposition (`B01…B13`)
- Registration/login: phone + password, SMS/WhatsApp OTP verification (`FR-001`)
- RBAC for 7 actors incl. resource-level ownership checks (`FR-002`)
- Full product catalog: products, variants (up to 5 dimensions), categories (5 levels), attributes, images, inventory with 15-minute reservation TTL (`FR-004`, `FR-005`)
- Reviews & ratings (1–5 stars, ≤5 images) (`FR-006`)
- Vendor onboarding with KYC review workflow; store profiles & settings (`FR-007`, `FR-008`)
- Search & discovery: full-text Arabic-aware search, filters, sorting, banners (`FR-009`)
- Cart with guards (≤50 items, ≤10 per product, ≤5 vendors) and 15-minute reservation countdown (`FR-010`)
- 7-step checkout → order placement with idempotency (`FR-011`)
- Order lifecycle: **exactly 17 states**, master/sub-order architecture (`FR-012`, `C-09`, `C-10`)
- Wallet: balance, top-up (m-Floos / OneCash / bank transfer), payments, double-entry ledger (`FR-013`)
- Escrow with 7-day hold, commission (5–20%, default 10%), vendor payouts (`FR-014`)
- Shipping zones, delivery assignment, **6-digit delivery-code confirmation** (`FR-015`, `C-16`)
- Returns with merchant-configurable policy; refunds strictly to wallet (`FR-016`)
- Multi-channel notifications: SMS, WhatsApp, in-app, push (`FR-017`)
- Analytics & reporting dashboards (admin, vendor) (`FR-018`)
- CMS: static pages, banners, promotions, coupon engine (`FR-019`)
- Admin console: users, vendors, catalog, orders, finance, delivery ops, settings, audit logs (`FR-020`)
- Four delivery surfaces: customer web, vendor panel, admin console, customer+courier mobile apps
- Full documentation knowledge base (this repository)

## OUT OF SCOPE (explicitly excluded — enforced by constraints)

| Excluded | Excluded By |
|---|---|
| Cash on delivery (COD) | `C-01` |
| Card payments / third-party card processors (Stripe, Moyasar, etc.) | `C-02` |
| BNPL / installments / credit | `C-03` |
| Cryptocurrency / multi-currency wallets (USD/SAR accounts) | `C-04` |
| Top-up methods beyond m-Floos, OneCash, bank transfer | `C-05` |
| Email-primary auth, social login (Google/Facebook/Apple) | `C-06` |
| Biometric authentication | `C-07` |
| GPS / real-time courier tracking | `C-16` |
| International (cross-border) fulfillment | `C-17` |
| Off-the-shelf commerce platforms (Shopify/Medusa/WooCommerce) | `C-18` |
| Non-PostgreSQL relational databases | `C-19` |
| RabbitMQ / Kafka (job processing) | `C-20` |
| Microservices architecture | `C-21` |
| Kubernetes in v1 | `C-22` |
| Legacy migration / brownfield coexistence | `C-23` |
| Additional locales beyond Arabic and English | `C-24` |
| AI chatbot / generative-AI support features | Scope decision (human ticketing only, `FR-020`) |
| Subscription products, trials, samples, rentals | Scope decision (see `01-business-analysis/business-rules.md`, `BR-CAT-05`) |
| Email as a notification channel | `INFERENCE` — not in `FR-017` channel list; confirm if needed (`GAP-03`) |
| Native desktop applications | Not requested |

## FUTURE SCOPE (explicitly NOT current requirements)

- MENA regional expansion (Saudi, Oman) with multi-currency
- Invoicing/e-invoicing integration with tax authorities
- Loyalty points program beyond simple tiers
- Marketplace advertising / sponsored placements
- Vendor multi-user advanced workflows (currently basic roles only)
- Live chat (human, async) beyond ticketing
- Progressive Web App offline shopping mode

## UNCERTAIN SCOPE (needs stakeholder clarification)

| ID | Item | Needed From | Registered In |
|---|---|---|---|
| GAP-01 | Growth/commercial targets for launch (vendor/order/GMV) | Sponsor | `20-validation/missing-information.md` |
| GAP-02 | Whether admin can override a delivery code in exceptional cases | Operations | same |
| GAP-03 | Email notification channel: include or exclude? | Product owner | same |
| GAP-04 | Loyalty program depth (tiers only vs points accrual/redemption) | Product owner | same |
| GAP-05 | Vendor subscription/tiered commission plans (vs flat 5–20%) | Finance | same |
| GAP-06 | Cash-out (wallet → bank) for vendors: automatic or admin-approved only? | Finance | same |
| GAP-07 | Logistics partners beyond individual couriers (fleet operators) | Operations lead (RISK-018 owner) | same |
| GAP-08 | Statutory data-retention obligations applicable in Yemen (exact scope) | Legal liaison | same |
| GAP-09 | Unresolved blocking legal deliverables (Central Bank wallet position, VAT opinion) | Legal liaison + sponsor | same |
| GAP-10 | Exact provider API specifications for m-Floos / OneCash (blocked by DEP-05) | Technical lead / integrations | same |
| GAP-11 | Hosting / cross-border data-location decision (Yemen Law No. 11 of 2012) | Project sponsor | same |
| GAP-12 | v2 account-recovery channel beyond SMS/WhatsApp | Security officer | same |

## Scope-Creep Control

1. Any new feature request is checked against this document first.
2. If OUT OF SCOPE (constraint-backed), it is rejected with the constraint ID.
3. If FUTURE SCOPE, it is parked in the backlog — never silently promoted.
4. If genuinely new, it requires: new/updated FR in `02-requirements/` → ADR if architectural → impact analysis across `19-traceability/` → status change here.
5. The methodology rule applies: *future enhancements must never become hidden current requirements.*

## Scope Stability Statement

Scope is baselined at v1.0. Post-baseline changes follow change management (root README §9).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | Uncertain-scope table extended with GAP-07..GAP-12 pointer rows (canonical register already carries them) | Consistency with 20-validation/missing-information.md (session 006: CHK-15) |
