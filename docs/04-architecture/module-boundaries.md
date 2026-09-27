---
document_id: DOC-ARCH-006
title: Module Boundaries (Modular Monolith)
category: 04-architecture
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-009, NFR-010]
related_documents: [DOC-OVR-008, DOC-ARCH-004, DOC-ARCH-002, DOC-SA-006, DOC-REQ-001]
---

# Module Boundaries

`C-21` mandates a **modular monolith**: one deployable backend, internally partitioned so modules can be reasoned about, tested and — if the future ever requires it — extracted. Boundaries are not aspirational; they are enforced mechanically in CI (`NFR-009`). This document defines the allowed dependency rules, the enforcement mechanism, the shared kernel, and where cross-cutting concerns live.

## 1. Boundary Model

Each block `B01…B13` is one NestJS module (see DOC-ARCH-004). Every module has:

| Part | Rule |
|---|---|
| **Public surface** | Only services/DTOs exported from the module's `*.public.ts` (or Nest provider exports) may be imported by other modules |
| **Private interior** | Entities, repositories, Prisma mappers, internal helpers are invisible outside the module |
| **Own schema** | Each module owns its PostgreSQL schema `b01…b13` (1:1 block mapping, `08-database/database-overview.md`) |
| **Own queues** | Jobs are named `{block}.{entity}.{action}` and are produced/consumed only by the owning module's workers (`BR-PLT-01`) |
| **Own tests** | Unit tests cover private logic; contract tests cover the public surface (`NFR-010`) |

## 2. Allowed Dependencies (complete list)

| # | From (consumer) | To (provider) | What may be used | Why allowed |
|---|---|---|---|---|
| D1 | any module | `SharedKernel` | Prisma/transactions, idempotency, event bus, validation, locale, health, errors | Neutral infrastructure with no domain knowledge |
| D2 | Checkout (B05) | Cart, Inventory, Payment (B07), Order (B06), Shipping (B08), Content (B12) | Public ports only | Checkout orchestrates the purchase |
| D3 | Order (B06) | Payment, Inventory, Shipping, Return (B09), Notification (B10), Content? — **no Content** | Public ports + `OrderStateGuard` | Order drives lifecycle side effects |
| D4 | Cart (B05) | Inventory, Catalog (B02) | reserve/release, visibility checks | Stock guards at cart time |
| D5 | Shipping (B08) | Order, Notification, Store (B03) | state transition requests, code messages, zone data | Delivery progression |
| D6 | Return (B09) | Order, Payment, Shipping, Notification | refund request, states, pickup, alerts | Return orchestration |
| D7 | Wallet/Escrow/Payout (B07) | Ledger, Order (read), Store (read), Notification, Admin (B13) — *admin decisions only* | ledger posts, maturity guards, KYC status, payout alerts | Money flows |
| D8 | Notification (B10) | Identity (B01) — read prefs, Content (B12) — templates | preferences, template bodies | Fan-out needs recipient data |
| D9 | Search (B04) | Catalog (read), Content (read), Cart — availability flags only | published documents | Discovery |
| D10 | Review (B02) | Order (read), Catalog | delivery proof, product linkage | Post-delivery reviews |
| D11 | Store (B03) | Notification, Audit (via B13 port) | alerts, audit records | KYC & staff events |
| D12 | Admin (B13) | *everything* (read + controlled commands) | public ports, dispute/verification/ruling commands | Administration is the designated orchestrator |
| D13 | Analytics (B11) | Order, Wallet, Shipping, Catalog, Content — **read-only** | query/DTO endpoints | Reporting must not mutate domain state |
| D14 | Content (B12) | Audit | audit on coupon/disable actions | Promotion changes are privileged |
| D15 | any module | `DomainEventBus` (kernel) | publish/subscribe of domain events | Decoupled side effects (notifications, indexing) |

**Universal rules:** dependencies always point to a module's *public surface*; no module may import another module's repository/Prisma client directly; no circular module pairs (if A→B and B→A are both wanted, the pair must be joined via an event or moved into the kernel).

## 3. Forbidden Patterns

| # | Forbidden | Example | Consequence if found |
|---|---|---|---|
| F1 | Cross-schema SQL joins in application code | `OrderModule` issuing `SELECT … FROM b07.wallet` | CI lint failure; must use `PaymentPort` |
| F2 | Direct Prisma access to another module's models | Cart code calling `prisma.order.update` | CI lint failure |
| F3 | Module reaching into private internals | `Checkout` importing `wallet/internal/ledger.service` | Import boundary lint failure |
| F4 | Two modules owning the same table | Any table outside its block schema | Migration review rejection |
| F5 | Business logic in controllers/DTOs | Validation beyond transport shape in a controller | Code review + unit-test gate (`NFR-010`) |
| F6 | State mutation outside the owning module | Any module writing order state except `OrderModule` | Test failure: only `OrderService.transition` may change state (`C-09`, `BR-ORD-01`) |
| F7 | Money writes outside B07 | Any module touching `b07` postings directly | Test failure: only `LedgerService.post` writes ledger (`DATA-REQ-007`) |
| F8 | Provider SDK types crossing module edges | `m-floos` types appearing outside `WalletModule` | Boundary lint failure (`INT-REQ-008`) |
| F9 | Synchronous cross-module DB transactions spanning schemas | One giant transaction locking `b05` and `b07` from Checkout | Saga + idempotency instead (`BR-PLT-04`) — *money ops are the documented exception where wallet debit + order creation are coordinated by the saga pattern, not by one implicit transaction* |
| F10 | Blocking calls in request path to slow providers | Sending SMS inline during checkout confirm | Enqueue notification job instead (`BR-PLT-01`) |

## 4. Enforcement Mechanism

| Layer | Tooling (`INFERENCE` — the concrete tool is chosen at implementation) | What it checks | Gate |
|---|---|---|---|
| Static import rules | ESLint `no-restricted-imports` plus per-module lint rules matching module paths | F1, F3, F8 | Every push (lint stage) |
| Dependency graph | Import-graph checker (e.g. dependency-cruiser style) with allowlist = §2 table | Whole-graph violations, cycles (F3) | Every push |
| Schema ownership | Prisma schema foldering per block + migration review | F4 | PR review + CI |
| Architecture tests | Jest tests asserting "only `OrderModule` mutates order state", "only `LedgerService` writes ledger", etc. | F6, F7 | Unit test stage |
| Runtime belt-and-braces | Ports/facades are the only exported providers; deep imports fail to resolve | F2 | Typecheck |
| Review checklist | PR template item: "module boundary respected; no cross-schema SQL" | Everything | PR review |

Failing any architectural gate blocks the merge — this is what makes `NFR-009` ("monolith modules with enforced boundaries") measurable.

## 5. Shared Kernel

Small, stable, domain-agnostic. Anything here must be usable by all modules without knowing business rules.

| Kernel item | Contents | Must NOT contain |
|---|---|---|
| Data access | Prisma client bootstrap, transaction helper, unit-of-work | Domain entities of any block |
| Idempotency | Key storage/lookup (`BR-PLT-03`) | Money logic |
| Domain event bus | In-process pub/sub + outbox-to-queue bridge (`INFERENCE` pattern) | Business routing decisions |
| Validation primitives | DTO pipe config, common validators (phone regex, YER amount bounds helper) | Rule definitions that belong to `BR-*` owners |
| Localization | Locale resolution, ar/en message keys | Hardcoded user-facing strings (`BR-PLT-05`) |
| Errors & codes | Error taxonomy used by `07-api/` (e.g. `STATE_CONFLICT`) | Per-domain error texts |
| Health/metrics/logging | `/healthz`, `/readyz` (`BR-PLT-07`), RED metrics, correlation IDs (`NFR-014`) | Provider-specific instrumentation |
| Auth middleware | JWT verification, rate-limit middleware | RBAC *decisions* — those belong to `IdentityModule` (`SEC-REQ-004`) |

## 6. Cross-Cutting Concern Placement

| Concern | Owning module | Why there |
|---|---|---|
| RBAC & sessions | B01 Identity | Single authority on actors (`FR-002`) |
| Audit trail | B13 Admin (`AuditService`) behind `AuditPort` | Audit is a platform function; append-only (`SEC-REQ-010`) |
| Notifications fan-out | B10 Notification | One template/preferences/channel authority (`FR-017`) |
| Idempotency, transactions, events | SharedKernel | Domain-agnostic mechanics |
| Scheduling/retries | SharedKernel queue API + per-module queue names | `C-20`, `BR-PLT-01/02` |
| Dispute freeze of escrow | B13 issues command → B06/B07 apply | Admin orchestrates; state owners execute (rules `BR-ORD-05`, `BR-ESC-02`) |
| Reconciliation | B07 (money) + B13 (alerting) | Finance authority (`BR-ESC-08`, `BR-FIN-03`) |
| Moderation | B13 command surface; content owners (B02/B12) apply | Moderator role separation (`ACT-06`) |

## 7. Evolution Path (why boundaries matter)

Boundaries are drawn so that a future extraction (if `C-21` were ever relaxed — not planned for v1) would follow existing seams: `SearchModule` (index already separate), `NotificationModule` (already behind provider ports), `AnalyticsModule` (already read-only). Until then, extraction is **out of scope**; the enforcement above exists to keep the monolith maintainable (`NFR-009`), not to enable microservices.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
