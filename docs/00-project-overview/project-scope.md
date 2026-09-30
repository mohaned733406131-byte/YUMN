---
document_id: DOC-OVR-005
title: Project Scope
category: 00-project-overview
status: approved
version: 1.2
created: 2026-09-26
updated: 2026-09-28
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
| Top-up methods beyond m-Floos, OneCash, Al-Kuraimi Bank, Jeeb, bank transfer (as amended 2026-09-28) | `C-05` |
| Email-primary auth, social login (Google/Facebook/Apple) — an *optional verified* email on a profile remains allowed (`C-06` as amended) | `C-06` |
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
| Email as a notification channel | **RESOLVED out of v1** 2026-09-28 (`plan-develop.md` §8 `D6`) — SMS/WhatsApp/in-app/push cover it; `GAP-03` closed |
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
| GAP-02 | Whether admin can override a delivery code in exceptional cases | Operations | same — **RESOLVED `NEVER` 2026-09-28 (`D7`)** |
| GAP-03 | Email notification channel: include or exclude? | Product owner | same — **RESOLVED `OUT OF v1` 2026-09-28 (`D6`)** |
| GAP-04 | Loyalty program depth (tiers only vs points accrual/redemption) | Product owner | same — **deferred** 2026-09-28 (`D8`), still OPEN |
| GAP-05 | Vendor subscription/tiered commission plans (vs flat 5–20%) | Finance | same — **deferred** 2026-09-28 (`D8`), still OPEN |
| GAP-06 | Cash-out (wallet → bank) for vendors: automatic or admin-approved only? | Finance | same |
| GAP-07 | Logistics partners beyond individual couriers (fleet operators) | Operations lead (RISK-018 owner) | same — fleet **registry skeleton approved** 2026-09-28 (`D8`, `P-09`) |
| GAP-08 | Statutory data-retention obligations applicable in Yemen (exact scope) | Legal liaison | same |
| GAP-09 | Unresolved blocking legal deliverables (Central Bank wallet position, VAT opinion) | Legal liaison + sponsor | same |
| GAP-10 | Exact provider API specifications for m-Floos / OneCash (blocked by DEP-05) | Technical lead / integrations | same |
| GAP-11 | Hosting / cross-border data-location decision (Yemen Law No. 11 of 2012) | Project sponsor | same |
| GAP-12 | v2 account-recovery channel beyond SMS/WhatsApp | Security officer | same |

## APPROVED BACKLOG (pointer — content never copied)

> Approved 2026-09-28 by the administrator (`plan-develop.md` v1.2 §8 `D9`/`D10`). The canonical
> text of every row lives in [`plan-develop.md`](../../plan-develop.md); this section only records
> that the plan is **approved work waiting for its build wave** — no row here is a v1 requirement
> yet (`SPE-03`/`D-02`: `M-nn`/`P-nn` convert to `FR-*` + ACs at their wave, never earlier).

| Group | IDs | Where it lands | When |
|---|---|---|---|
| Modifications (HIGH) — pre-build backlog | `M-01`…`M-14` subset in plan §1.1 | owning domains + `requirements-overview.md` | Wave 1 FR conversion |
| Modifications (MEDIUM/LOW) | plan §1.2–§1.3 | owning domains | later waves |
| Missing features — ERP/finance core | plan §2.1 (`P-01`…`P-06`), `D2`/`D3`/`D11` | `B07`+`B13`, `erp-finance-departments.md` (DOC-SA-011) | Wave 1–2 |
| Wishlist `P-11` | `D5` — implement | customer-facing surfaces | Wave 2 |
| Fleet registry skeleton `P-09` | `D8` — approved skeleton | delivery/ops (`GAP-07`) | Wave 2 |
| Admin departments + staff bundles | `ORG-01`…`ORG-08`, `ROLE-01`…`ROLE-09` | **minted** in `../09-security/core/rbac.md` §11 | as of 2026-09-28 |
| Completeness checklist (v1) | plan §3 rows 1–59 | gate evidence at each wave | ongoing |

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
| 1.2 | 2026-09-28 | `C-05`/`C-06` OUT OF SCOPE rows follow the amended constraints (Al-Kuraimi/Jeeb; optional verified email); `GAP-02` → RESOLVED `NEVER`, `GAP-03` → RESOLVED `OUT OF v1`, `GAP-04`/`GAP-05` annotated deferred, `GAP-07` skeleton annotated; new **APPROVED BACKLOG** pointer section (content stays in `plan-develop.md`) | `plan-develop.md` v1.2 §8 approval implementation (session 007, `D5`–`D9`) |
