---
document_id: DOC-SA-002
title: System Boundary
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-013, FR-015, FR-017]
related_documents: [DOC-OVR-002, DOC-OVR-005, DOC-OVR-008, DOC-OVR-010, DOC-SA-003, DOC-IR-001, DOC-IR-003]
---

# System Boundary

**What yumn owns, what it merely talks to, and where the trust boundaries sit.** The boundary is drawn from the approved scope (`DOC-OVR-005`), the constraint register (`DOC-OVR-008`) and the integration requirements (`02-requirements/`). `C-18` requires a 100% custom build: everything inside the boundary is purpose-built — no commerce platform is adopted to sit in the middle of it.

## 1. Inside the System

Everything below is built, owned and operated by the yumn team. Each element maps to blocks `B01…B13` (`DOC-OVR-002`).

| Inside element | Block(s) | Why it is inside |
|---|---|---|
| Customer storefront (web) | B04, B05 | Discovery and conversion surface — core to the product |
| Vendor panel (web) | B02, B03, B06, B07 | Merchant tooling; no third-party seller SaaS in v1 |
| Admin / back-office console | B13 | Platform operations, settings, audit, support, disputes |
| Customer mobile app | B04, B05, B06, B10 | Primary purchase surface for the market |
| Courier mobile app | B08 | Assignment, pickup, transit, code confirmation |
| Marketplace domain logic | B01–B13 | The differentiating logic; `C-18` forbids buying it |
| Wallet, escrow, double-entry ledger | B07 | Trust core; `C-01`, `C-12`, `DATA-REQ-007` |
| Inventory reservation engine (15-min TTL) | B02, B05 | Oversell prevention (`C-13`, `BR-CAT-07`) |
| Search index maintenance | B04 | Arabic-aware discovery (`FR-009`) |
| Notification composition, templating, fan-out | B10 | Channel orchestration is platform logic (`FR-017`) |
| CMS, banners, coupons, merchandising | B12 | Revenue and content control (`FR-019`) |
| Analytics aggregation and reporting | B11 | Dashboards over owned data (`FR-018`) |
| Audit log, RBAC, settings, support tickets | B01, B13 | Security and governance (`SEC-REQ-004`, `SEC-REQ-010`) |
| Background job scheduling and retries | all | `C-20` — BullMQ is the only queue system |

> Internal persistence, caching, queues, search and object storage (PostgreSQL, Redis, Elasticsearch, MinIO) are **infrastructure inside the boundary** — they are operated by yumn, not consumed as vendor SaaS. Their placement is a technical matter for `../../04-architecture/core/container-view.md`.

## 2. Outside the System

| Outside element | Relationship to yumn | Governing IDs |
|---|---|---|
| Physical souqs, WhatsApp/Facebook sellers | The status quo yumn competes with — not integrated | `DOC-OVR-002` |
| Cross-border shipping, MENA fulfillment | Excluded in v1 | `C-17`, scope FUTURE |
| Cash-in agent networks | Reached only *through* wallet providers, never integrated directly | `C-05` |
| Card networks, card processors, BNPL, crypto rails | Excluded entirely | `C-02`, `C-03`, `C-04` |
| Bank core systems | No direct connection; bank transfer tops up via admin-verified manual flow | `INT-REQ-002`, `BR-PAY-04` |
| Email delivery infrastructure | Not a v1 channel — `GAP-03` pending confirmation | `BR-NTF-01` |
| External delivery fleet APIs | Not integrated in v1 — internal assignment engine behind an abstraction | `INT-REQ-005` |
| Social login / identity providers | Excluded; phone + OTP only | `C-06` |
| GPS / location services | Never requested or stored | `C-16`, `BR-SHP-05` |
| Loyalty, subscription, trial/rental product engines | Out of scope for v1 | `project-scope.md`, `BR-CAT-05` |
| AI chatbot support | Excluded — human ticketing only | `FR-020`, scope note |

## 3. Actors Crossing the Boundary

All 7 actors (`ACT-01…ACT-07`, `DOC-OVR-007`) interact across the boundary; six are human and authenticate through it, one (`System`) originates inside it and crosses only to reach external providers.

| Actor | Direction of crossing | Surfaces used | Data brought in | Data taken out |
|---|---|---|---|---|
| Customer (`ACT-01`) | Inbound requests, outbound content | Web, mobile app | Phone + OTP, addresses, cart, orders, reviews | Catalog, order status, wallet balance, notifications |
| Vendor (`ACT-02`) | Inbound requests, outbound content | Vendor panel | KYC documents, products, stock, prices, coupons | Orders, sales/finance reports, follower list |
| Delivery Provider (`ACT-03`) | Inbound requests, outbound updates | Courier app | Accept/pickup/transit events, 6-digit code entry | Assignments, pickup addresses, payout statements |
| Admin (`ACT-04`) | Inbound privileged requests | Admin console | KYC decisions, settings, bank top-up verification, dispute rulings | Audit log, dashboards, tickets |
| Super Admin (`ACT-05`) | Inbound privileged requests | Admin console | Role/permission changes, platform configuration | Full platform state |
| Moderator (`ACT-06`) | Inbound privileged requests | Admin console | Content/review moderation decisions | Flag queues, audit entries |
| System (`ACT-07`) | Originates inside; egress to providers | No UI | Timers, queue jobs, provider callbacks/webhooks | Provider API calls, webhook responses |

Every crossing is a controlled interface: human crossings go through authenticated, rate-limited endpoints (`SEC-REQ-004`, `SEC-REQ-009`); `System` crossings go through provider adapters that hide vendor types from domain code (`INT-REQ-008`).

## 4. External Systems Across the Boundary

| # | External system | Direction | Data exchanged | Requirement | Failure behavior |
|---|---|---|---|---|---|
| E1 | SMS provider primary (e.g. Telesom/Sabafon per `DEP-06`) | Outbound | OTP codes, transactional alerts | `INT-REQ-003` | Timeout/error → automatic failover to second provider, then WhatsApp (`BR-NTF-03`) |
| E2 | SMS provider secondary | Outbound | Same payloads | `INT-REQ-003` | If both fail → in-app/push delivery + queued retry |
| E3 | WhatsApp Business API | Outbound | Approved templates: OTP fallback, order updates | `INT-REQ-004`, `DEP-06` | Template not approved → channel unavailable; SMS remains primary |
| E4 | m-Floos | Outbound initiate, inbound callback/poll | Top-up intent, amount, verified credit confirmation | `INT-REQ-001`, `C-05` | No callback → reconciliation poll job; never credit on client claim (`BR-PAY-03`) |
| E5 | OneCash | Outbound initiate, inbound callback/poll | Same as E4 | `INT-REQ-001`, `C-05` | Same as E4 |
| E6 | Bank transfer (customer → platform account) | Inbound, human-verified | Transfer reference submitted by customer | `INT-REQ-002` | Credits wallet only after admin verification (`BR-PAY-04`) |
| E7 | Push notification services (APNs/FCM — `INFERENCE`) | Outbound | Push payloads for order/offer events | `FR-017`, `BR-NTF-01` | Delivery unconfirmed → fall back to in-app record |
| E8 | CDN / edge proxy (Cloudflare, `DEP-08`) | Inbound termination | TLS termination, static asset delivery | `DEP-08` | Origin serves directly if CDN unavailable |
| E9 | Provider webhooks (top-up, messaging receipts) | Inbound | Signed event payloads | `INT-REQ-006` | Signature invalid → reject; valid but unprocessed → 3 retries + backoff + DLQ (`BR-PLT-02`) |

Providers are never allowed to leak into domain logic: each of E1–E5 and E7 sits behind an adapter interface (`INT-REQ-008`), so swapping a vendor changes one adapter, not the wallet or notification domain.

## 5. Trust Zones

Five zones, ordered from least to most trusted. Zone crossings are the only places where validation, authentication or verification is allowed to be skipped — everywhere else, input is untrusted.

```text
Z1  Public / Client zone      Customer web, mobile apps, courier app, vendor panel, admin console
      │  TLS 1.3 (SEC-REQ-006) — rate limits (SEC-REQ-009)
Z2  Edge zone                 Reverse proxy / CDN termination, request size limits (SEC-REQ-011)
      │  JWT verification, RBAC + ownership checks (SEC-REQ-003, SEC-REQ-004)
Z3  Application zone          Domain logic for B01–B13, background workers, job queue
      │  Parameterized queries only (SEC-REQ-008); append-only audit (SEC-REQ-010)
Z4  Data zone                 PostgreSQL, Redis, Elasticsearch, MinIO — private network, no public route
Z5  Provider zone             E1–E7 outside yumn's control; reachable only via egress adapters,
                              secrets from environment (SEC-REQ-007), webhooks verified (INT-REQ-006)
```

| Crossing | What is enforced | IDs |
|---|---|---|
| Z1 → Z2 | TLS 1.3, request body limits, image type/size validation | `SEC-REQ-006`, `SEC-REQ-011` |
| Z2 → Z3 | JWT access token (15 min), RBAC + resource ownership, per-IP/user rate limits (100 req/min standard) | `SEC-REQ-003`, `SEC-REQ-004`, `SEC-REQ-009` |
| Z3 → Z4 | Prisma parameterized queries, row-level locking on money/stock, ACID transactions | `SEC-REQ-008`, `BR-PAY-05`, `BR-PLT-04` |
| Z3 → Z5 (egress) | Provider abstraction, secrets in environment, idempotent callbacks | `INT-REQ-008`, `SEC-REQ-007`, `BR-PLT-03` |
| Z5 → Z3 (ingress) | Webhook signature verification, idempotent handlers, retry/DLQ policy | `INT-REQ-006`, `BR-PLT-02` |

**Cross-zone data classification:** PII (phone, name, address) and financial values are encrypted at rest (`SEC-REQ-006`) and classified per `16-data/data-classification.md`; OTP codes and delivery codes never persist in logs (`BR-AUTH-02`, `SEC-REQ-002`).

## 6. Boundary Change Control

The boundary is fixed for v1 by scope and constraints. Any proposed addition (new payment method, email channel, external fleet API, second currency) must first change `00-project-overview/` scope/constraints through change management (root README §9), then this document, then `04-architecture/`. Silent boundary creep is recorded as a contradiction in `20-validation/contradiction-audit.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
