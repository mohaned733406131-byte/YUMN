---
document_id: DOC-BE-002
title: Backend Architecture — NestJS Modular Monolith Layout
category: 06-backend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-002, FR-004, FR-010, FR-012, FR-013, FR-017, FR-020, NFR-009, NFR-010, NFR-018]
related_documents: [DOC-BE-001, DOC-BE-005, DOC-OVR-008, DOC-OVR-002]
---

# Backend Architecture — NestJS Modular Monolith Layout

One deployable NestJS 10 application (`C-21`), split into **13 feature modules mirroring blocks `B01…B13`** plus shared infrastructure modules. Boundaries are lint- and test-enforced, not conventions-only (NFR-009).

---

## 1. Top-Level Structure

```text
api/
├─ src/
│  ├─ blocks/
│  │  ├─ b01-identity/        # FR-001…FR-003
│  │  ├─ b02-catalog/         # FR-004…FR-006
│  │  ├─ b03-store/           # FR-007…FR-008
│  │  ├─ b04-search/          # FR-009
│  │  ├─ b05-checkout/        # FR-010…FR-011
│  │  ├─ b06-order/           # FR-012
│  │  ├─ b07-wallet/          # FR-013…FR-014
│  │  ├─ b08-shipping/        # FR-015
│  │  ├─ b09-returns/         # FR-016
│  │  ├─ b10-notification/    # FR-017
│  │  ├─ b11-analytics/       # FR-018
│  │  ├─ b12-content/         # FR-019
│  │  └─ b13-platform/        # FR-020
│  ├─ shared/
│  │  ├─ auth/                # guards, decorators, session context
│  │  ├─ config/              # typed env config (validated at boot)
│  │  ├─ logging/             # structured logger + correlation ID
│  │  ├─ events/              # in-process event bus (domain events)
│  │  ├─ errors/              # error codes + exception base classes
│  │  ├─ validation/          # global pipes, common DTO constraints
│  │  ├─ idempotency/         # key storage & replay responses
│  │  ├─ pagination/          # cursor/page helpers (07-api conventions)
│  │  └─ crypto/              # hashing, encryption helpers (PII)
│  ├─ integrations/
│  │  ├─ payments/            # m-Floos, OneCash adapters (INT-REQ-001)
│  │  ├─ sms/                 # dual-provider adapter (INT-REQ-003)
│  │  ├─ whatsapp/            # templates (INT-REQ-004)
│  │  ├─ push/                # FCM/APNs
│  │  └─ webhooks/            # signed outbound webhooks (INT-REQ-006)
│  ├─ jobs/                   # BullMQ processors wiring (queues per BR-PLT-01)
│  ├─ prisma/                 # schema, migrations, client singleton
│  ├─ main.ts                 # bootstrap: pipes, filters, guards order, CORS, helmet
│  └─ app.module.ts           # root module composition
├─ test/                      # unit + integration + e2e (13-testing/)
└─ Dockerfile
```

## 2. In-Module Layering

Every `bNN-*` module follows the same layers; dependencies point downward only:

```text
Controller  →  Service  →  Domain  →  Repository (Prisma)
(HTTP/DTO)    (use-cases,   (pure      (queries,
               transactions, business    no rules)
               orchestration) logic)
```

| Layer | Responsibilities | Must not do |
|---|---|---|
| **Controller** | route binding, DTO validation pipes, idempotency-key extraction, auth/role guard application, response shaping per `07-api` | business decisions, direct Prisma access |
| **Service** | use-case orchestration, transactions/sagas, cross-module calls via public service interfaces, event emission | raw SQL outside repositories, HTTP concerns |
| **Domain** | pure business rules — pricing/VAT, state machine guards, commission, limits — unit-testable without I/O (`NFR-010`) | I/O, framework decorators, logging side effects |
| **Repository** | Prisma queries scoped by ownership keys, pagination, locking (e.g. wallet row lock) | rule enforcement, cross-schema joins outside the block |

Rule of thumb: **if it is a `BR-*` rule, it lives in Domain; if it coordinates, it lives in Service; if it speaks HTTP, it lives in Controller.**

## 3. Module ↔ Block ↔ Responsibility Map

| Module | Block | Key responsibilities | Primary FRs |
|---|---|---|---|
| `b01-identity` | B01 | registration, OTP issuance/verify, login, JWT issue/refresh, sessions, roles, profiles, addresses | FR-001, FR-002, FR-003 |
| `b02-catalog` | B02 | products, variants, categories, attributes, images, stock reservations, reviews | FR-004, FR-005, FR-006 |
| `b03-store` | B03 | vendor KYC, stores, zones, settings, staff, followers | FR-007, FR-008 |
| `b04-search` | B04 | query orchestration, facet/sort, ES index projections, banners/merchandising | FR-009 |
| `b05-checkout` | B05 | cart server state, merge, limits, checkout session, order placement saga | FR-010, FR-011 |
| `b06-order` | B06 | master/sub-orders, 17-state machine, timelines, cancellation, disputes | FR-012 |
| `b07-wallet` | B07 | balances, top-ups, payments, double-entry ledger, escrow, commission, payouts, refunds | FR-013, FR-014 |
| `b08-shipping` | B08 | zones/fees, shipments, courier assignment, 6-digit code confirmation | FR-015 |
| `b09-returns` | B09 | return requests, inspection window, refund initiation | FR-016 |
| `b10-notification` | B10 | templates, preferences, fan-out orchestration, in-app inbox | FR-017 |
| `b11-analytics` | B11 | dashboards read models, reports, exports | FR-018 |
| `b12-content` | B12 | CMS pages, banners, coupons, featured/deals | FR-019 |
| `b13-platform` | B13 | settings, audit log, roles admin, support tickets, dispute resolution | FR-020 |

## 4. Shared Modules

| Shared module | Provides | Used by |
|---|---|---|
| `shared/auth` | `JwtAuthGuard`, `RolesGuard`, `@CurrentUser()`, `@RequirePermissions()` | all controllers |
| `shared/config` | env schema validated at boot (fail-fast), feature flags | root wiring |
| `shared/logging` | structured JSON logger with correlation ID; child loggers per request/job | everywhere (`NFR-014`) |
| `shared/events` | in-process domain event bus (`OrderDelivered`, `WalletCredited`) → job producers | services that trigger side effects |
| `shared/errors` | error code registry (aligned with `../../07-api/core/error-model.md`) + typed exceptions | services, filters (`error-handling.md`) |
| `shared/validation` | global `ValidationPipe`, common constraints (phone, integer money) | controllers (`validation.md`) |
| `shared/idempotency` | Redis-backed key store + replay cache | payment, order, stock, coupon, refund paths (`BR-PLT-03`) |
| `shared/crypto` | bcrypt wrapper (cost 12), AES-256 for PII fields, HMAC for webhooks | identity, integrations |

**Cross-module rule:** a block may call another block only through its **exported service interface** — never through its Prisma models or repositories. Violations fail lint (`no-restricted-imports`) and a boundary test (NFR-009).

## 5. Prisma Data-Access Rules

| Rule | Detail |
|---|---|
| One schema, 13 client namespaces | schema organized by block (`b01…b13` — `../../08-database/core/database-overview.md`); each module touches only its own namespace's models |
| Ownership columns | every tenant-scoped row carries `user_id`/`store_id`; repositories require an ownership filter parameter (DATA-REQ-008) |
| Transactions | money/state/stock changes run in `prisma.$transaction` with explicit isolation; row locks where the rule requires (`BR-PAY-05`) |
| No raw SQL by default | `queryRaw` only with review + parameterization (SEC-REQ-008); Prisma parameterizes everything else |
| Migrations | expand-contract only, backward compatible (`DATA-REQ-005`, NFR-020) |
| Ledger immutability | no `update`/`delete` on ledger entries — corrections via compensating rows (DATA-REQ-007) |
| Soft delete | catalog uses soft delete; only ACTIVE rows visible (`BR-CAT-06`) |
| Client lifecycle | one Prisma client per process; graceful shutdown on SIGTERM (deploys, `NFR-020`) |
| Read replicas | repository layer isolates reads so replica routing can be added without touching services (NFR-018) |

## 6. Boundary Enforcement (NFR-009)

| Mechanism | What it catches |
|---|---|
| ESLint import boundaries | block → other block's internals; shared → blocks |
| Architecture test (Jest) | repository classes instantiated only inside their block; controllers never import Prisma |
| Public API files | each block exposes `index.ts` with allowed symbols only |
| Codeowners + review | changes to `shared/` require platform-team review |
| CI gates | lint, typecheck, unit tests, boundary tests on every PR |

## 7. FR → Module Placement Summary

| FR | Module | FR | Module |
|---|---|---|---|
| FR-001 | b01-identity | FR-011 | b05-checkout → b06-order, b07-wallet |
| FR-002 | b01-identity (+ shared/auth) | FR-012 | b06-order |
| FR-003 | b01-identity | FR-013 | b07-wallet |
| FR-004 | b02-catalog | FR-014 | b07-wallet (escrow/payout) |
| FR-005 | b02-catalog | FR-015 | b08-shipping |
| FR-006 | b02-catalog | FR-016 | b09-returns |
| FR-007 | b03-store | FR-017 | b10-notification |
| FR-008 | b03-store | FR-018 | b11-analytics |
| FR-009 | b04-search | FR-019 | b12-content |
| FR-010 | b05-checkout | FR-020 | b13-platform |

## 8. Process & Scaling Model

| Topic | Decision (canon) |
|---|---|
| Runtime | Node 20, single codebase; horizontally scaled stateless replicas behind a load balancer (NFR-018) |
| Jobs | BullMQ workers run in the same image, separate process entrypoint; scale by queue depth (C-20) |
| Health | liveness/readiness endpoints gate traffic (`BR-PLT-07`) |
| Deploy | Docker Compose, no K8s (`C-22`); expand-contract migrations keep replicas compatible (`NFR-020`) |
| Load | validated against 10,000 concurrent users within NFR-001 (`C-25`, k6 in `13-testing/`) |

## 9. Verification

- Boundary tests + lint run in CI (§6).
- Architecture decision record for monolith choice referenced as `ADR-002` (`C-21`).
- Unit tests per domain class without network (`NFR-010`).
- Module import graph checked for cycles in CI.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
