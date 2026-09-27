---
document_id: DOC-SA-003
title: System Context View
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-012, FR-013, FR-015, FR-017, FR-020]
related_documents: [DOC-OVR-002, DOC-OVR-007, DOC-SA-002, DOC-REQ-001, DOC-BA-005]
---

# System Context View

The context view answers: **who interacts with yumn, and what crosses the boundary in each direction?** It shows yumn as a single black box surrounded by the 7 canonical actors (`ACT-01…ACT-07`) and the external entities defined in `system-boundary.md` (DOC-SA-002). It corresponds to C4 level 1; the technical C4 context with containers is in `04-architecture/architecture-overview.md` (DOC-ARCH-002).

## 1. Context Diagram (text form)

```text
                          ┌───────────────────────────────────────────────┐
        ACT-02 Vendor ───►│                                               │
        (panel: KYC,      │                y u m n  (يُمن)                │
         catalog, orders, │                                               │
         finances)        │   Identity & Access · Catalog · Store ·       │
                          │   Search · Cart/Checkout · Orders ·           │
        ACT-01 Customer ─►│   Wallet/Escrow · Shipping · Returns ·        │
        (web + mobile:    │   Notifications · Analytics · CMS · Admin     │
         browse, wallet,  │                                               │
         orders, returns) │   Marketplace domain — B01 … B13              │
                          │                                               │
        ACT-03 Delivery ─►│                                               │
        Provider (courier │                                              │
        app: accept,      │        ▲ callback / webhook (signed)         │
        pickup, code)     │        │                                      │
                          │        │                                      │
        ACT-04 Admin ────►│        │        ACT-07 System                 │
        ACT-05 Super Adm.►│        │        (jobs, schedulers, engines    │
        ACT-06 Moderator ►│        │         — originates INSIDE)         │
                          └────────┼──────────────────────┬───────────────┘
                                   │                      │ egress (adapters)
        External entities          │                      ▼
        ─────────────────          │        SMS primary/secondary (INT-REQ-003)
        m-Floos / OneCash ◄────────┘        WhatsApp Business  (INT-REQ-004)
        (top-up credit)                     Push services       (FR-017)
        Bank (manual transfer               Cloudflare / CDN    (DEP-08)
             via admin verify)
             (INT-REQ-002)
```

## 2. Actors — Responsibilities, Inputs, Outputs

| Actor | ID | Responsibility in the context | Inputs to yumn | Outputs from yumn | Primary blocks | Use cases |
|---|---|---|---|---|---|---|
| Customer | `ACT-01` | Discovers products, funds wallet, buys, receives, returns, reviews | Phone + OTP, profile & addresses, search queries, cart changes, wallet payments, delivery code shared with courier, return/dispute requests, reviews | Catalog & prices, cart/order totals with VAT, order status timeline, wallet balance & statements, notifications | B04, B05, B06, B07, B09 | `UC-001…UC-014` |
| Vendor | `ACT-02` | Runs a store: KYC, listings, stock, fulfillment, finances | KYC documents, product/variant data, stock levels, prices, coupons, order accept/ready actions, return decisions, review responses | Assigned orders, sales/finance/payout reports, follower counts, moderation outcomes | B02, B03, B06, B07, B12 | `UC-015…UC-024` |
| Delivery Provider | `ACT-03` | Moves packages; proves handover with the 6-digit code | Assignment accept/release, pickup/transit/out-for-delivery updates, failed-attempt records, delivery code entry | Available assignments in zone, pickup addresses, attempt counts, payout statements | B08 | `UC-025…UC-030` |
| Admin | `ACT-04` | Day-to-day platform operations with scoped permissions | KYC decisions, bank top-up verification, order/dispute/return rulings, settings, support-ticket replies | Queues (KYC, top-ups, disputes, tickets), dashboards, audit trail | B03, B06, B07, B13 | `UC-031…UC-036` |
| Super Admin | `ACT-05` | Full control: roles, permissions, platform configuration | Role/permission grants and revocations, configuration changes | Updated RBAC model, configuration state | B01, B13 | `UC-037` |
| Moderator | `ACT-06` | Content and review moderation, escalation handling | Hide/restore decisions on products, reviews, banners; escalation dispositions | Moderation queue, hidden-content state, audit entries | B13, B02, B12 | `UC-038` |
| System | `ACT-07` | Non-human actor: timers, background jobs, provider callbacks, automated engines | Scheduled triggers, queue jobs, signed webhooks, stock TTL expiries, escrow maturity | State transitions, notifications, ledger postings, escalations, reconciliation alerts | all (`B01…B13`) | `UC-039`, `UC-040` |

Guest visitors (unregistered browsers) interact as **unauthenticated customers**: they may browse and search (`UC-001`) and build a client-side cart (`BR-CRT-03`), but registration gateways appear at checkout, reviews, follows and wallet actions (`FR-001`).

## 3. External Entities — Inputs and Outputs

| External entity | Inputs to yumn | Outputs from yumn | Requirement | Verification of trust |
|---|---|---|---|---|
| m-Floos / OneCash | Signed top-up callback or poll response confirming credit | Top-up initiate request (amount, reference) | `INT-REQ-001` | Callback signature + reference match; credit only after verification (`BR-PAY-03`) |
| Bank (via customer) | Transfer reference submitted in-app | Verification request to admin; credit posting after approval | `INT-REQ-002` | Human admin verification of the reference (`BR-PAY-04`) |
| SMS providers (primary, secondary) | Delivery receipts, failure responses | OTP payloads, transactional notification text | `INT-REQ-003` | Failover on timeout/error; receipts logged |
| WhatsApp Business | Template send receipts | Approved template messages (OTP fallback, order updates) | `INT-REQ-004` | Approval-gated templates only |
| Push services (`INFERENCE` — APNs/FCM) | Delivery receipts | Push payloads for opted-in categories | `FR-017`, `BR-NTF-05` | Security pushes cannot be opted out (`BR-NTF-02`) |
| Cloudflare / CDN | TLS termination, cache hits | Static assets, origin requests | `DEP-08` | TLS 1.3 at edge (`SEC-REQ-006`) |
| Provider webhook senders | Signed event payloads (top-up, receipts) | Acknowledgement; retry on failure | `INT-REQ-006` | Signature check, idempotent handling, 3 retries + DLQ (`BR-PLT-02`) |

## 4. Context-Level Interactions (what each pairing is for)

| # | From → To | Interaction | Rules / requirements |
|---|---|---|---|
| I1 | Customer → yumn | Register/login with phone + OTP, manage profile & addresses | `FR-001`, `FR-003`, `BR-AUTH-01…08` |
| I2 | Customer → yumn | Browse/search catalog, add to cart, 7-step checkout, pay from wallet | `FR-009`–`FR-011`, `FR-013`, `BR-CRT-01…06` |
| I3 | yumn → Customer | Order timeline, delivery code issuance, wallet statements, notifications | `FR-012`, `FR-017`, `BR-SHP-02` |
| I4 | Vendor → yumn | Submit KYC, publish products, manage stock, accept and fulfill orders | `FR-004`–`FR-008`, `FR-012`, `BR-VND-01…07` |
| I5 | yumn → Vendor | Assigned orders, sales/finance reports, payout notifications, follower list | `FR-014`, `FR-018`, `BR-ESC-05` |
| I6 | Delivery Provider → yumn | Accept assignment, pickup/transit updates, delivery-code entry | `FR-015`, `BR-SHP-04`, `BR-SHP-03` |
| I7 | yumn → Delivery Provider | Zone-matched offers, pickup/drop details, attempt history | `FR-015`, `C-16` (no location data) |
| I8 | Admin / Super Admin / Moderator → yumn | KYC decisions, dispute rulings, settings, moderation, audit review | `FR-002`, `FR-007`, `FR-020`, `SEC-REQ-010` |
| I9 | System → yumn internal | TTL expiry, SLA escalations, escrow release, payouts, reconciliation | `C-13`, `BR-ORD-10`, `BR-ESC-02`, `BR-ESC-05`, `BR-FIN-03` |
| I10 | yumn → Providers | OTP/notification sends, top-up initiate, webhook acks | `INT-REQ-001`, `INT-REQ-003`, `INT-REQ-004`, `INT-REQ-006` |

## 5. Boundary Rules Implied by the Context

1. **No actor talks to another actor through yumn as a chat pipe** — communication is mediated: notifications are templated (`BR-NTF-04`), support is ticket-based (`FR-020`), and phone numbers are not exposed between customers and couriers beyond delivery necessity (`DATA-REQ-002`).
2. **Money never flows directly between actors.** Customer funds enter only via top-up (`C-05`); vendor exit is only the platform payout (`BR-ESC-05`); refunds credit the wallet (`BR-PAY-07`).
3. **All yumn→external calls go through adapters** (`INT-REQ-008`); all external→yumn calls are verified (`INT-REQ-006`, `BR-PAY-03`).
4. **`System` is the only actor that acts without a human initiator**, and every automated action writes an audit or history entry (`BR-ORD-03`, `BR-PLT-06`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
