---
document_id: DOC-ARCH-004
title: Component View — NestJS Modules (B01–B13)
category: 04-architecture
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-012, FR-013, FR-020, NFR-009, NFR-010]
related_documents: [DOC-ARCH-002, DOC-ARCH-006, DOC-SA-006, DOC-OVR-002, DOC-BA-005]
---

# Component View — Internal Modules

The internals of the NestJS API container (CNT-04): one module per block (`B01…B13`) plus a shared kernel. This is the technology-bound realization of the logical components in `03-system-analysis/logical-components.md` (DOC-SA-006); the rules governing how these modules may depend on each other are in `module-boundaries.md` (DOC-ARCH-006).

## 1. Module Map

| Module | Block | Realizes (LC) | Provides (interfaces consumed by other modules) | Depends on (allowed) |
|---|---|---|---|---|
| `IdentityModule` | B01 | LC-01, LC-20 | `AuthService` (register/login/OTP/refresh), `SessionService`, `PermissionService.evaluate()`, `ProfileService`, `AddressService` | kernel, `NotificationPort`, `AuditPort` |
| `CatalogModule` | B02 | LC-02 | `CatalogService` (products/variants/categories), `PublicationPort` (visibility) | kernel, `StorePort`, `ModerationPort` |
| `InventoryModule` | B02 | LC-03 | `InventoryService.reserve()/release()/deduct()/restore()`, `ExpirySchedulePort` | kernel, `CatalogPort` |
| `ReviewModule` | B02 | LC-04 | `ReviewService.submit/respond/hide`, `RatingQueryPort` | kernel, `OrderReadPort`, `ModerationPort` |
| `StoreModule` | B03 | LC-05 | `StoreService` (profile/zones/staff/followers), `KycService`, `VendorStatusPort` | kernel, `AuditPort`, `NotificationPort` |
| `SearchModule` | B04 | LC-06 | `SearchService.search/browse/suggest`, `IndexWriterPort` (used by workers) | kernel, `CatalogReadPort`, `PromotionReadPort` |
| `CartModule` | B05 | LC-07 | `CartService.add/change/merge/validate`, `ServerTotalsPort` | kernel, `InventoryPort`, `CatalogReadPort` |
| `CheckoutModule` | B05 | LC-08 | `CheckoutService.quote/applyCoupon/confirm` | kernel, `CartPort`, `InventoryPort`, `PaymentPort`, `OrderPort`, `ShippingPort`, `PromotionPort` |
| `OrderModule` | B06 | LC-09 | `OrderService.place/transition/cancel/timeline/aggregate`, `OrderStateGuard`, `OrderEventsPort` | kernel, `PaymentPort`, `InventoryPort`, `ShippingPort`, `ReturnPort`, `DisputePort`, `NotificationPort`, `SchedulePort` |
| `WalletModule` | B07 | LC-10 | `WalletService.balance/topUp/debit/credit/freeze/statement`, `TopUpPort` | kernel, `PaymentProviderPort`, `LedgerPort`, `AuditPort` |
| `LedgerModule` | B07 | LC-11 | `LedgerService.post/assertBalanced/reconcile` (called only via Wallet/Escrow/Payout/Refund paths) | kernel |
| `EscrowModule` | B07 | LC-12 | `EscrowService.fund/checkMaturity/release/freeze/reverseCommission`, `MaturitySchedulePort` | kernel, `LedgerPort`, `OrderReadPort`, `AuditPort` |
| `PayoutModule` | B07 | LC-13 | `PayoutService.accumulate/buildBatch/execute`, `BatchSchedulePort` | kernel, `LedgerPort`, `StorePort`, `EscrowReadPort` |
| `ShippingModule` | B08 | LC-14 | `ShippingService.quoteFee/offer/accept/progress`, `DeliveryCodeService.issue/verify`, `AttemptService` | kernel, `OrderPort`, `NotificationPort`, `StorePort`, `AuditPort` |
| `ReturnModule` | B09 | LC-15 | `ReturnService.open/decide/receive/inspect/autoApprove`, `RefundRequestPort` | kernel, `OrderPort`, `PaymentPort`, `ShippingPort`, `NotificationPort`, `AuditPort` |
| `NotificationModule` | B10 | LC-16, LC-22 | `NotificationService.send/preference/render/receipts`, `MessageProviderPort`, `TemplateService` | kernel, `IdentityReadPort` |
| `AnalyticsModule` | B11 | LC-17 | `AnalyticsService.aggregate/dashboards/statement/export` (read-only) | kernel, read ports from Order/Wallet/Shipping/Catalog |
| `ContentModule` | B12 | LC-18 | `ContentService` (pages/banners), `CouponService.create/validate/disable`, `MerchandisingPort` | kernel, `AuditPort` |
| `AdminModule` | B13 | LC-19, LC-24 | `SettingsService`, `TicketService`, `DisputeService.open/rule`, `RoleService`, `AuditService.query`, `ModerationService` | kernel, `OrderPort`, `EscrowPort`, `PaymentPort`, `CatalogPort`, `ReviewPort`, `KycPort` |
| `SharedKernel` | — | cross-cutting | Prisma/transaction helper, `IdempotencyService`, `DomainEventBus`, `ValidationPipe` config, locale/time/currency helpers, health (`BR-PLT-07`), error model | (no module deps) |

## 2. Provided Interfaces in Detail (selected)

| Interface | Operations (contract level) | Called from | Guarantees |
|---|---|---|---|
| `PermissionService.evaluate` | `(actor, action, resource) → allow/deny` | global request guard in every module | Server-side; ownership + role (`SEC-REQ-004`, `FR-002`) |
| `InventoryService.reserve` | `(lines, ttlSeconds, idempotencyKey)` | Cart, Checkout | Atomic; stock ≥0; 15-min TTL (`C-13`, `BR-CAT-07`) |
| `OrderService.place` | `(master, subs, idempotencyKey)` | Checkout | Exactly 17 states (`C-09`); append-only history (`BR-ORD-03`); master/sub split (`C-10`) |
| `OrderService.transition` | `(orderId, from, to, actor, reason)` | Vendor/Courier/Admin flows, workers | Guard table from `state-transitions.md`; optimistic lock → conflict error |
| `WalletService.debit` | `(orderId, amountYER, idempotencyKey)` | Checkout | Balance ≥ amount or fail; paired ledger post (`BR-PAY-05/06`) |
| `EscrowService.checkMaturity` | `(orderId, now)` | Worker timer | 7 days elapsed AND no dispute/return/refund (`BR-ESC-02`, `C-12`) |
| `DeliveryCodeService.verify` | `(shipmentId, code, attemptRef)` | Courier flow | ≤3 attempts, 24-h lock + ticket on 3rd (`BR-SHP-03`); idempotent success |
| `CouponService.validate` | `(code, cart, actor)` | Checkout | Non-stackable, ≤90%, window/limits (`BR-PRM-01…04`); invalid ⇒ no order (`BR-PRM-06`) |
| `NotificationService.send` | `(template, recipientRef, data, channels)` | every module | Locale render (`BR-NTF-04`), preference filter (`BR-NTF-05`), security bypass (`BR-NTF-02`) |
| `AuditService.record` | `(actor, action, entity, before, after, ip)` | `AuditPort` from privileged/money paths | Append-only, tamper-evident (`SEC-REQ-010`, `BR-PLT-06`) |
| `IdempotencyService.run` | `(scope, key, fn)` | payment, order creation, reservation, coupon, refund (`BR-PLT-03`) | Exactly-once effect per key |

## 3. Dependency Diagram (allowed direction)

```text
                    ┌────────────── SharedKernel ───────────────┐
                    │ Prisma · Idempotency · DomainEventBus ·   │
                    │ Validation · Locale · Health · ErrorModel  │
                    └───────▲──────────────────────▲─────────────┘
                            │ (all use)            │ (all use)
   Clients ──► Identity ◄───┴── Store ──► Catalog ◄─┴── Search
                  │            │            │  ▲         ▲
                  │            │            │  │         │ (documents)
                  ▼            │            ▼  │      Content ──► Merchandising
             Notification ◄────┴─────  Inventory ◄─ Cart ─► Checkout
                  ▲                                     │        │
                  │                                     ▼        ▼
   Shipping ◄─────┴────── Order ◄──────────────────► Wallet ► Ledger
      ▲                   │  ▲                        │  ▲
      │                   │  │                        ▼  │
   Returns ───────────────┘  │                      Escrow ► Payout
      │                      │                        │
      └──────► Refund/Payment ┘                        │
                                                       ▼
   Admin (disputes, settings, tickets, roles) ──► Audit
   Analytics ──read-only──► Order/Wallet/Shipping/Catalog
```

Arrows show **allowed** dependency direction only; reverse and lateral shortcuts are blocked by the rules in DOC-ARCH-006. Notably:
- `Checkout` orchestrates but never talks to `Inventory`/`Ledger` internals — it uses their ports.
- `Ledger` has no outgoing domain dependencies: it is a leaf reached only through money operations.
- `Analytics` is read-only: no write path into any domain module.
- `Search` reads published documents; it does not write catalog state.

## 4. Cross-Cutting Concerns and Where They Live

| Concern | Home | Mechanism | IDs |
|---|---|---|---|
| Authentication | `IdentityModule` + global guard | JWT verification, session/refresh validation | `SEC-REQ-003`, `C-08` |
| Authorization | `IdentityModule` (`PermissionService`) | RBAC + ownership evaluated per request | `SEC-REQ-004`, `FR-002` |
| Idempotency | `SharedKernel` | Key store consulted by money/order/stock ops | `BR-PLT-03` |
| Audit | `AdminModule` (`AuditService`) via `AuditPort` | Interceptor/service hook on privileged & money actions | `SEC-REQ-010`, `BR-PLT-06` |
| Localization | `SharedKernel` locale helpers + client i18n | ar default, en parity, no hardcoded strings | `C-24`, `BR-PLT-05` |
| Validation | `SharedKernel` pipes/filters | Boundary validation before domain logic | `SEC-REQ-008`, rule guards |
| Rate limiting | Edge + API middleware | Per-IP/per-user counters (Redis) | `SEC-REQ-009` |
| Health/readiness | `SharedKernel` | `/healthz`, `/readyz` gates traffic | `BR-PLT-07` |
| Metrics/logging | `SharedKernel` | Structured logs, RED metrics, correlation IDs | `NFR-014`, `INT-REQ-007` |
| Job scheduling | each module declares schedules; executed by worker | BullMQ queues `{block}.{entity}.{action}` | `BR-PLT-01`, `C-20` |
| Errors | `SharedKernel` error model | Stable error codes (e.g. `STATE_CONFLICT`, `PAYMENT_METHOD_NOT_ALLOWED`) | `07-api/` contract |

## 5. Testing Surface (`NFR-010`)

Each module exposes pure domain services with injected ports, so business logic unit-tests run without network or database (`NFR-010`); ports are faked in unit tests, exercised for real in integration tests against PostgreSQL/Redis. Module boundary rules (DOC-ARCH-006) are themselves tested by lint/dependency checks in CI.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
