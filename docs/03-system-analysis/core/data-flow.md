---
document_id: DOC-SA-005
title: Logical Data Flow (Analysis Level)
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-010, FR-011, FR-012, FR-013, FR-014, FR-017]
related_documents: [DOC-SA-002, DOC-SA-003, DOC-SA-004, DOC-SA-010, DOC-ARCH-007, DOC-BA-005]
---

# Logical Data Flow (Analysis Level)

**What data moves between actors, processes and stores — with no technology named.** Data stores here are *conceptual* (business-meaningful containers), not tables; the physical mapping (PostgreSQL schemas `b01…b13`, MinIO buckets, Elasticsearch indices, Redis keys) belongs to `08-database/` and to the technical counterpart [`../../04-architecture/core/data-flow.md`](../../04-architecture/core/data-flow.md) (DOC-ARCH-007). This document defines the flow contract; DOC-ARCH-007 documents how each flow is realized (sync call, queue job, cache write, index update).

## 1. Conceptual Data Stores

| Store | Owner block | Contains (conceptually) | Mutated by | Read by | Persistence rule |
|---|---|---|---|---|---|
| DS1 Identity & Session Store | B01 | Accounts, credentials, OTP records, sessions, roles/permissions | registration, login, OTP, admin role changes | every block (authentication), B13 (audit) | PII encrypted at rest (`SEC-REQ-006`); phones never logged (`SEC-REQ-002`) |
| DS2 Catalog Store | B02 | Products, variants, categories, attributes, images metadata | vendor listings, moderation | B04, B05, B11, storefronts | soft-delete only (`BR-CAT-06`) |
| DS3 Inventory Store | B02 | Stock levels, reservations, reservation expiries | B05 (reserve), B06 (deduct/restore), System (TTL expiry) | B05, B06, vendor panel | integer ≥0, atomic ops (`BR-CAT-07`, `C-13`) |
| DS4 Cart Store | B05 | Server-side carts, guest-merge records, checkout sessions | customer actions, TTL expiry | B05, B04 (count) | server totals are authoritative (`BR-CRT-04`) |
| DS5 Order Store | B06 | Master orders, sub-orders, status history, timelines | checkout, transitions, escalations | B07–B09, B11, all surfaces | status history append-only (`BR-ORD-03`) |
| DS6 Wallet & Ledger Store | B07 | Wallet balances, double-entry postings, top-up intents | top-ups, payments, refunds, freezes | B07, B11, statements | append-only postings (`BR-PAY-06`, `DATA-REQ-007`) |
| DS7 Escrow & Payout Store | B07 | Escrow holds, commission records, payout batches | System (release), admin, reconciliation | B07, B11, vendor finances | release only under `BR-ESC-02` guards |
| DS8 Delivery Store | B08 | Zones, shipments, assignments, codes, attempts | courier actions, System | B06, customer/vendor timelines | no location data (`BR-SHP-05`) |
| DS9 Return Store | B09 | Return requests, inspections, decisions | customer, vendor, admin, System | B06, B07, B13 | decisions carry reason + audit (`BR-RET-06`) |
| DS10 Notification Store | B10 | Templates, preferences, message records, receipts | user prefs, fan-out jobs | B13 (audit), B11 (stats) | security categories non-disableable (`BR-NTF-02`) |
| DS11 Content & Promotion Store | B12 | Pages, banners, coupons, redemptions | admin/vendor, checkout | B04, B05, storefronts | redemption counts updated transactionally (`BR-PRM-04`) |
| DS12 Analytics Store | B11 | Aggregates, report snapshots, statements | aggregation jobs | dashboards, exports | derived data — rebuildable from DS2/DS5/DS6/DS8 |
| DS13 Audit & Support Store | B13 | Audit entries, tickets, dispute records, settings | privileged/money actions, tickets | B13, compliance review | append-only, tamper-evident (`SEC-REQ-010`) |
| DS14 Search Index | B04 | Searchable product/store documents | index jobs from DS2/DS11 | B04 search | rebuildable; stale-tolerant (`NFR-007`) |
| DS15 Media Store | B02/B12 | Product, review, KYC and proof images | uploads | storefronts, panels | ≤5 MB, type-checked, EXIF stripped (`SEC-REQ-011`) |
| DS16 Work Queue | all | Pending jobs, retries, dead letters | any block | System workers | 3 retries + backoff + DLQ (`BR-PLT-01/02`) |

## 2. Flow Register (DF-NN)

Flows are logical: a flow exists whenever the data below crosses between two parties, regardless of how architecture later transports it.

| ID | From → To | Data moved | Trigger | Key rules |
|---|---|---|---|---|
| DF-01 | Customer → Identity process | Phone, password, OTP response | register / login | `BR-AUTH-01…04`, `C-06` |
| DF-02 | Identity process → DS1 | Account, session family | successful auth | `BR-AUTH-05/06`, `SEC-REQ-003` |
| DF-03 | Identity process → Notification process | OTP code request (6 digits) | registration, reset, sensitive change | `BR-AUTH-03`, `SEC-REQ-001` |
| DF-04 | Notification process → SMS/WhatsApp providers | Template payload | message dispatch | `INT-REQ-003/004`, `BR-NTF-03` |
| DF-05 | Customer → Discovery process | Query, filters, locale | search / browse | `FR-009`, `C-24` |
| DF-06 | Catalog/Media stores → Discovery process → Customer | Product documents, images, prices, availability | search result render | `BR-CAT-06`, `NFR-007` |
| DF-07 | Customer → Cart process | Product ID, quantity | add / update cart | `BR-CRT-01/02`, `C-15` |
| DF-08 | Cart process → Inventory store | Reservation request (items, 15-min expiry) | cart add/refresh | `BR-CRT-02`, `C-13` |
| DF-09 | Inventory store → Cart/Order processes | Reservation grant or conflict | reservation check | `BR-CAT-07` |
| DF-10 | Customer → Checkout process | Address, shipping choice, coupon, payment intent | checkout confirm | `BR-CRT-04…06`, `BR-PRM-06` |
| DF-11 | Checkout process → Wallet process | Debit request (order total, idempotency key) | payment step | `BR-PAY-01/05/08`, `C-01` |
| DF-12 | Wallet process → DS6 | Debit posting + escrow funding posting | payment success | `BR-PAY-06`, `BR-ESC-01`, `DATA-REQ-007` |
| DF-13 | Checkout process → Order process | Master + sub-order payload (idempotency key) | payment success | `BR-ORD-02/06`, `C-10`, `BR-PLT-03/04` |
| DF-14 | Order process → Vendor panel / Notification process | New-order alert per sub-order | order `PLACED` | `BR-ORD-10`, `BR-NTF-04` |
| DF-15 | Vendor → Order process | Accept / start / ready actions | fulfillment steps | `BR-ORD-04`, transition table |
| DF-16 | Order process → Delivery process | Ready shipment (zone, weight, package) | `READY_FOR_PICKUP` | `BR-SHP-01/04` |
| DF-17 | Delivery process → Courier app | Assignment offer (address, no GPS data) | offer broadcast | `C-16`, `BR-SHP-05` |
| DF-18 | Courier → Delivery process | Accept, pickup, transit, out-for-delivery updates | courier actions | transition table (DOC-SA-010) |
| DF-19 | Delivery process → Notification process | 6-digit code issuance to buyer | `OUT_FOR_DELIVERY` | `BR-SHP-02`, `SEC-REQ-005` |
| DF-20 | Courier ↔ Customer | Code shared out-of-band (verbal/physical) | handover | `C-16` — platform observes only the entry |
| DF-21 | Courier → Delivery process | Code entry + attempt result | confirmation attempt | `BR-SHP-03`, `BR-ORD-08` |
| DF-22 | Delivery process → Order process | `DELIVERED` event | code verified | transition table |
| DF-23 | System → Escrow process | Matured hold (7 days elapsed, guard check) | daily/hourly timer | `BR-ESC-01/02`, `C-12` |
| DF-24 | Escrow process → DS7 | Release posting + commission record | release success | `BR-ESC-03`, `BR-ESC-04` |
| DF-25 | Escrow process → Payout process | Released amounts per vendor | release success | `BR-ESC-05/06` |
| DF-26 | Payout process → Vendor / DS7 | Payout batch execution (3–7 business days, ≥1,000 YER) | batch run | `BR-ESC-05` |
| DF-27 | Customer → Return process | Return request (items, reason, photos) | return open | `BR-RET-01/02`, `C-11` |
| DF-28 | Return process → Vendor/Admin | Decision request | `RETURN_REQUESTED` | 48 h decision SLA (DOC-SA-010) |
| DF-29 | Return process → Wallet process | Refund instruction | `RETURN_RECEIVED` passed / 72 h auto | `BR-RET-03/04/05` |
| DF-30 | Wallet process → DS6 | Refund credit posting | refund execution | `BR-PAY-07`, `BR-ESC-07`, `DATA-REQ-007` |
| DF-31 | Customer → Wallet process | Top-up intent (method, amount) | top-up start | `BR-PAY-02`, `C-05` |
| DF-32 | Wallet process ↔ m-Floos/OneCash | Initiate + signed callback/poll | top-up lifecycle | `BR-PAY-03`, `INT-REQ-001` |
| DF-33 | Customer → Admin queue | Bank transfer reference | bank top-up | `INT-REQ-002`, `BR-PAY-04` |
| DF-34 | Admin → Wallet process | Verification decision | admin approves reference | `BR-PAY-04`, `BR-PLT-06` |
| DF-35 | Customer/Vendor → Dispute process | Dispute payload + evidence | dispute open | `BR-ORD-05` |
| DF-36 | Dispute process → Escrow process | Freeze instruction | dispute open | `BR-ORD-05`, `BR-ESC-02` |
| DF-37 | Admin → Dispute process → Order process | Ruling (for-vendor / for-buyer) | resolution | transition table; audit `BR-PLT-06` |
| DF-38 | Content process → Discovery process | Banners, featured/deal boosts, coupons | publish | `FR-019`, `BR-PRM-03` |
| DF-39 | Checkout process → Content process | Coupon validation + redemption increment | coupon apply | `BR-PRM-01/04/06` |
| DF-40 | Customer → Review process | Rating, text, images | post-delivery review | `BR-REV-01…03` |
| DF-41 | Review process → Moderation queue → DS2 | Flag / hide decisions | moderation | `BR-REV-04`, `BR-PLT-06` |
| DF-42 | Order/Wallet/Delivery processes → Analytics process | Domain events for aggregation | scheduled / streaming | `BR-FIN-03/04`, `BR-ESC-08` |
| DF-43 | Analytics process → Vendor/Admin | Dashboards, statements, exports | request / schedule | `FR-018`, scoping `BR-VND-07` |
| DF-44 | Every privileged/money action → DS13 | Audit entry (actor, action, entity, before/after, IP, timestamp) | action commit | `BR-PLT-06`, `SEC-REQ-010` |
| DF-45 | Worker failures → DS16 → alerting | Failed job + DLQ depth | retry exhaustion | `BR-PLT-02`, `INT-REQ-006/007` |

## 3. End-to-End Flow Chains (narrative)

**Purchase chain:** DF-05 → DF-06 → DF-07 → DF-08/DF-09 → DF-10 → DF-11 → DF-12 → DF-13 → DF-14. Failure at DF-11/DF-12 stops the chain before DF-13; compensation releases the DF-08 reservation (`BR-PLT-04`).

**Settlement chain:** DF-18 → DF-21 → DF-22 → DF-23 → DF-24 → DF-25 → DF-26. Any dispute (DF-35/DF-36) interrupts between DF-22 and DF-23 by freezing the hold.

**Money-in chain:** DF-31 → DF-32 (or DF-33 → DF-34) → DF-12-style ledger credit → balance visible in DF-43 statements.

**Return chain:** DF-27 → DF-28 → (pickup via DF-16-style flow) → DF-29 → DF-30 → DF-42 reporting, with DF-44 audit on admin decisions.

## 4. Flow Invariants

1. **No flow carries a raw provider payload into a domain store** — provider data is normalized at the adapter (`INT-REQ-008`) before DF-32 processing.
2. **No money flow is one-directional without a ledger pair** — every DF-12/DF-24/DF-30 movement posts balanced debit+credit (`BR-PAY-06`).
3. **No flow trusts the client for amounts** — totals are recomputed server-side (DF-10, `BR-CRT-04`).
4. **Code and OTP flows (DF-03, DF-19, DF-21) never write the secret to logs or analytics** (`SEC-REQ-002`, `SEC-REQ-005`).
5. **Notification content (DF-04) is generated from owned stores only**, in the user's locale (`BR-NTF-04`).
6. **Analytics flows (DF-42) are read-only with respect to DS1–DS11.**

## 5. Handoff to Architecture

| This document (behavior contract) | Realized in DOC-ARCH-007 (technical) |
|---|---|
| Conceptual store DS1…DS16 | PostgreSQL schemas `b01…b13`, Redis structures, ES index, MinIO buckets |
| Flow DF-08/DF-09 reservation | TTL/expiry job mechanics, locking strategy |
| DF-11/DF-12/DF-13 payment+order | Transaction boundary, saga steps, idempotency keys |
| DF-16/DF-17/DF-18 delivery | Queue fan-out, optimistic locking implementation |
| DF-23 escrow maturity | BullMQ delayed jobs and schedules |
| DF-45 failures | Retry/backoff/DLQ configuration and alert routes (`INT-REQ-007`) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
