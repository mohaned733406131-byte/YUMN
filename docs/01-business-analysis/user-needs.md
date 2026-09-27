---
document_id: DOC-BA-007
title: User Needs (per Actor)
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-003, FR-007, FR-009, FR-010, FR-011, FR-015, FR-016, FR-020]
related_documents: [DOC-BA-001, DOC-BA-004, DOC-BA-006, DOC-OVR-007]
---

# User Needs (per Actor)

A jobs-to-be-done view of the canonical actors (`ACT-01…ACT-07`, `00-project-overview/actors-and-roles.md`). For each actor: **jobs to be done, pains today, how yumn addresses them (`FR-*` refs), and success signals**. The customer section separates **guest vs registered** needs, because guest gating is a deliberate design point (`BR-CRT-03`, `FR-010`). Stakeholder-level needs live in `stakeholder-needs.md` (`STK-*`); this document is about the *users of the product*.

## 1. Customer (`ACT-01`)

### 1a. Guest customer (unauthenticated)

| Aspect | Detail |
|---|---|
| Jobs to be done | Discover products (Arabic search, category browse, filters); compare prices; open product detail pages; build a cart; check out-of-stock/availability signals — all **before** creating an account |
| Pains today | Informal WhatsApp/Facebook sellers have no catalog, no prices until you message, no stock truth |
| How addressed | `FR-009` (Arabic-aware search, filters, sorting), `FR-004` (catalog/PDP data), `FR-010` (client-side guest cart), `BR-CAT-06` (only ACTIVE products shown), `BR-CRT-01` (guards apply to guests too) |
| Gating rule | Browsing and cart are open; **placing an order and other account actions require login** — guest cart merges on login, server value wins on quantity conflict (`BR-CRT-03`, permission matrix `actors-and-roles.md`) |
| Success signals | Guest reaches PDP without friction; guest cart survives login merge; zero dead-end prompts before checkout |

### 1b. Registered customer

| Aspect | Detail |
|---|---|
| Jobs to be done | Register/login fast with phone (no email); fund wallet; place orders across multiple vendors; track order state; confirm delivery with a 6-digit code; cancel pre-dispatch; request returns; get refunds to wallet; write reviews; manage addresses (≤10) and sessions (≤5 devices) |
| Pains today | Paying cash with no buyer protection; no delivery proof; returns are personal negotiations; no order history/records |
| How addressed | `FR-001` (phone + OTP auth), `FR-003` (profile, addresses, sessions), `FR-013` (wallet/top-ups), `FR-011` (7-step checkout), `FR-012` (17-state tracking + timeline), `FR-015` (code confirmation, `C-16`), `FR-016` (returns, `C-11`), `FR-006` (reviews), `BR-PAY-07` (refunds always to wallet) |
| Trust needs | Escrow hold before vendor release (`BR-ESC-01`); never negative balance (`BR-PAY-05`); visible VAT and totals recalculated server-side (`BR-CRT-04`, `BR-FIN-01`); Arabic-first UI (`C-24`, `BR-PLT-05`) |
| Success signals | Registration → first order < 5 min (`NFR-012`); refund credited ≤3 business days (`BR-RET-04`); ≥95% deliveries confirmed on first code attempt (`OBJ-07`); repeat purchase rate tracked from launch (`BO-02`) |

## 2. Vendor (`ACT-02`)

| Aspect | Detail |
|---|---|
| Jobs to be done | Open a store with minimal paperwork; get KYC approved fast; list products in Arabic with images/variants; keep stock accurate; accept/fulfill orders on time; see money clearly (sales, commission, payouts); respond to reviews; handle returns; invite staff with bounded roles |
| Pains today | Selling via chat apps: no catalog, no inventory control, manual order bookkeeping, no finance records, cash-handling risk |
| How addressed | `FR-007` (onboarding + KYC ≤48 h), `FR-008` (storefront config, follower feature `BR-VND-05`), `FR-004`/`FR-005` (catalog + inventory, 15-min reservation), `FR-012` (sub-order actions, timeline), `FR-014` (escrow/commission/payout), `FR-018` (dashboards), `FR-006` (vendor response `BR-REV-04`), `BR-VND-06` (staff roles) |
| Constraints they work within | One store per account (`BR-VND-02`); store_id scoping on every query (`BR-VND-07`); no publish before KYC approval (`BR-VND-01`); suspension freezes products/orders/payouts (`BR-VND-04`); return policy is theirs to configure (`C-11`) |
| Success signals | Time-to-first-listing < 10 min (`NFR-012`); KYC decision ≤48 h (`BR-VND-03`); payout 3–7 business days after release (`BR-ESC-05`); monthly statement received (`BR-FIN-04`); ≥10 pilot vendors complete full sale → payout (`AC-S-21`) |

## 3. Delivery Provider / Courier (`ACT-03`)

| Aspect | Detail |
|---|---|
| Jobs to be done | See delivery offers for their zone; accept quickly (first accept wins); pick up packages; move through transit states; confirm handover with the buyer's 6-digit code; release an assignment when needed; see their earnings scope |
| Pains today | Verbal/informal delivery jobs, no proof of handover, disputes over "did it arrive", no tracking burden (and none wanted) |
| How addressed | `FR-015` (zones, assignment, pickup → transit → delivery), `BR-SHP-04` (zone offer, first accept, optimistic lock), `BR-SHP-02/03` (code issue + attempts), `BR-SHP-07` (proof = code + timestamp + identity), `C-16` (no GPS ever requested/stored `BR-SHP-05`) |
| Boundaries | Scoped to own deliveries only (permission matrix); assignment can return to `READY_FOR_PICKUP` if released; 3rd code failure locks confirmation for 24 h and creates a ticket (`BR-SHP-03`) |
| Success signals | Assignment accepted without double-assignment conflicts (`BR-SHP-04`); ≥95% first-attempt code success (`OBJ-07`); zero deliveries completed without a code (`OBJ-07`) |

## 4. Admin (`ACT-04`)

| Aspect | Detail |
|---|---|
| Jobs to be done | Run daily operations: approve KYC; review escalated orders (SLA breaches, failed deliveries); verify bank-transfer top-ups; resolve disputes; approve/deny returns; freeze wallets; manage content and coupons oversight; handle support tickets; read audit trail |
| Pains today | Manual coordination across chat threads; no single record of who did what; risk of over-reaching into user money |
| How addressed | `FR-020` (admin console: users, vendors, catalog, orders, finance, delivery ops, settings, audit, tickets, disputes), `FR-007` (KYC decisions), `FR-012` (state overrides where permitted), `BR-PAY-04` (bank top-up verification), `BR-PAY-09` (freeze — flag only, ledger untouchable), `BR-RET-06` (final arbiter), `BR-PLT-06` (audit entries) |
| Boundaries | Scoped permissions, never full control (that is Super Admin, `ACT-05`); no wallet/ledger edit rights ever (`actors-and-roles.md` resource ownership) |
| Success signals | 100% of state-changing admin actions audited (`OBJ-08`); escalation queues cleared within SLA (`BR-ORD-10`, `BR-SHP-06`); daily reconciliation available next morning (`OBJ-08`) |

## 5. Moderator (`ACT-06`)

| Aspect | Detail |
|---|---|
| Jobs to be done | Review flagged/reported reviews and content; hide abusive/inappropriate content with an audit entry; respond to review disputes; escalate support cases to Admin |
| Pains today | Unstructured moderation in group chats; inconsistent decisions with no record |
| How addressed | `FR-006` (moderation of reviews), `FR-019` (content/CMS oversight), `FR-020` (support escalation), `BR-REV-04` (hide with audit; vendor may respond once), `BR-PLT-06` (audit), `BR-PLT-05` (Arabic/English copy) |
| Boundaries | Cannot approve KYC, change roles, or touch money (permission matrix); store-scoped awareness only |
| Success signals | Flag → decision recorded with audit entry; store rating recomputed after moderation (`BR-REV-05`); no unlogged moderation actions |

## 6. Super Admin (`ACT-05`) and System (`ACT-07`) — brief

- **Super Admin:** needs full platform control: role/permission management, platform configuration, unlimited read scope. Addressed by `FR-002`/`FR-020`; bounded by `BR-PLT-06` audit and `SEC-REQ-004` server-side enforcement. Success signal: every role change audited; no self-role-escalation by Vendor Staff (`actors-and-roles.md` test 3).
- **System:** needs to execute jobs deterministically — timers (escrow, reservation TTL, inspection SLA), retries, webhook handling, automated state moves. Addressed by `FR-012`/`BR-PLT-01/02/03`. Success signal: zero ledger imbalances (`AC-S-14`), no silent data loss (`NFR-007`).

## 7. Cross-Actor Need Summary

| Actor | Top need | Top success signal | Anchor |
|---|---|---|---|
| Guest customer | Discover before committing | Frictionless browse + cart merge | `FR-009`, `BR-CRT-03` |
| Registered customer | Protected purchase and easy money-back | Refund ≤3 business days | `BR-RET-04`, `BR-ESC-01` |
| Vendor | Fast onboarding and dependable payouts | KYC ≤48 h, payout 3–7 days | `BR-VND-03`, `BR-ESC-05` |
| Courier | Simple, fair assignment + confirmation | First-accept, no double assign | `BR-SHP-04` |
| Admin | Control with audit | 100% audited actions | `OBJ-08`, `BR-PLT-06` |
| Moderator | Bounded, recorded decisions | Zero unlogged actions | `BR-REV-04` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
