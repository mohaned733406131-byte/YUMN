---
document_id: DOC-OVR-002
title: Project Context
category: 00-project-overview
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-020]
related_documents: [DOC-OVR-001, DOC-OVR-003]
---

# Project Context

## What Is This System?

**yumn (يُمن)** is a **multi-vendor e-commerce marketplace** connecting Yemeni merchants, customers, and delivery providers on a single platform. Vendors operate branded storefronts inside the marketplace; customers discover products, pay from an in-app wallet, and receive orders through code-confirmed home delivery.

**Tagline:** "Yemen's market in your hands."

> Classification: `VERIFIED` — project brief / charter.

## Why Does It Exist?

Yemen's retail trade is dominated by informal channels (WhatsApp/Facebook sellers, physical souqs) with no trustworthy digital infrastructure:

- Buyers have **no buyer protection** — payments are hand-to-hand with no escrow.
- Merchants have **no tooling** — no catalog, inventory, order, or finance management.
- Cash handling is risky and unscalable; digital payment adoption is rising via mobile wallets but no marketplace ties them together.
- Delivery is informal — no trackable, code-confirmed handover.

**Problem statement:** enable trusted, wallet-funded, escrow-protected commerce between Yemeni merchants and customers at national scale.

**If the system does not exist:** informal commerce continues; no escrow trust, no merchant tooling, no data-driven marketplace operations.

## Who Uses It?

Seven actors — see [actors-and-roles.md](actors-and-roles.md): Customer, Vendor, Delivery Provider, Admin, Super Admin, Moderator, System.

## Business Domain

| Aspect | Value |
|---|---|
| Domain | B2C2C multi-vendor marketplace (customer ↔ platform ↔ vendor) |
| Geography | Yemen (domestic fulfillment); MENA as future expansion |
| Currency | Yemeni Rial (`YER`) — single currency in v1 (`C-04`) |
| Languages | Arabic (primary, RTL) + English (secondary, LTR) — `C-24` |
| Payments | In-app **wallet only** — top-up via m-Floos, OneCash, bank transfer (`C-01…C-05`) |
| Fulfillment | Vendor → delivery provider → customer; **6-digit code confirmation, no GPS** (`C-16`) |
| Tax | VAT 15% applied to discounted prices (Yemeni tax regulation) |

## Project Boundaries

```text
INSIDE                          OUTSIDE
────────────────────────────    ─────────────────────────────
Customer storefront (web)       Physical retail / POS
Vendor panel (web)              Cross-border shipping
Customer & courier mobile apps  Currency exchange business
Admin / back-office console     Bank core systems (only APIs)
Marketplace domain logic        Cash-in agent networks (only via wallets)
Wallet, escrow, ledger          Card networks, BNPL, crypto
Search, notifications, CMS      Social network integrations
```

## Platform Decomposition — 13 Blocks

The system is decomposed into 13 blocks (`B01…B13`). This is the **canonical** decomposition — all architecture, data, API, and test structures align to it.

| Block | Name | Primary Responsibility |
|---|---|---|
| B01 | Identity & Access | Registration, OTP, login, sessions, roles, permissions |
| B02 | Product Catalog | Products, variants, categories, attributes, inventory, reviews |
| B03 | Store Management | Vendors, KYC, storefronts, store settings, templates |
| B04 | Search & Discovery | Search, filtering, sorting, banners, merchandising |
| B05 | Cart & Checkout | Cart, checkout sessions, order placement guards |
| B06 | Order Management | Master/sub-orders, 17-state lifecycle, timelines |
| B07 | Payment & Wallet | Wallet, top-ups, payments, escrow, ledger, payouts |
| B08 | Shipping & Delivery | Zones, shipments, delivery assignments, code confirmation |
| B09 | Returns & Refunds | Return requests, inspections, wallet refunds |
| B10 | Notifications | SMS / WhatsApp / in-app / push messaging |
| B11 | Analytics & Reporting | Dashboards, reports, operational metrics |
| B12 | Content & CMS | Pages, banners, promotions, static content |
| B13 | Platform Administration | Admin console, settings, audit logs, support tools |

> Each block maps 1:1 to a database schema (`b01…b13`) — see `../08-database/core/database-overview.md`.

## Compliance Context

| Area | Position |
|---|---|
| Data protection | Yemeni Law No. (11) of 2012 on Personal Data Protection — applicable; full regulation detail `INSUFFICIENT EVIDENCE` (legal counsel required) |
| Tax | VAT 15% charged on digital sales; invoices issued per Yemeni tax rules |
| E-invoicing mandate | Not applicable in v1 (Saudi ZATCA regime is out of scope — domestic fulfillment only, `C-17`) |
| Payment regulation | Wallet operation must comply with Central Bank of Yemen mobile payment rules — `INFERENCE`, requires legal confirmation (`ASM-12`) |
| PCI-DSS | **Not applicable** — no card data handled (`C-02`) |
| Accessibility | WCAG 2.1 AA target (see `NFR-011`) |

## Analysis Evidence Basis

This analysis was produced from the approved project brief (charter-level requirements supplied by the project sponsor). Statements are tagged `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE` throughout; unresolved items are registered in `20-validation/missing-information.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
