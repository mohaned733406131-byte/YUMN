---
document_id: DOC-REQ-001
title: Requirements Overview (Canonical ID Registry)
category: 02-requirements
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-OVR-004, DOC-OVR-008]
---

# Requirements Overview — Canonical ID Registry

**This document is the single registry of every requirement ID in the project.** Individual requirement files (`functional/FR-nnn.md`, etc.) expand each entry; they must never contradict this registry. Never invent a requirement ID that is not listed here.

Total: **20 FR + 20 NFR + 12 SEC-REQ + 8 DATA-REQ + 8 INT-REQ = 68 requirements.**

---

## 1. Functional Requirements (`FR-001…FR-020`)

Each expands to `02-requirements/functional/FR-nnn.md`.

| ID | Title | Block | Priority | Summary |
|---|---|---|---|---|
| FR-001 | Identity, Authentication & Session Management | B01 | Critical | Registration/login by phone + password; SMS/WhatsApp OTP verification; session & token lifecycle (C-06, C-08) |
| FR-002 | Roles, Permissions & Access Control | B01 | Critical | RBAC for 7 actors; resource ownership; server-side enforcement on every endpoint |
| FR-003 | User & Profile Management | B01 | High | Profiles, addresses (≤10), password change, account deletion, session management (≤5 devices) |
| FR-004 | Product Catalog Management | B02 | Critical | Products, variants (≤5 dimensions), categories (5 levels), attributes, images, pricing |
| FR-005 | Inventory Management | B02 | Critical | Stock levels, 15-min reservation TTL (C-13), deduction on payment, restoration on cancel |
| FR-006 | Reviews & Ratings | B02 | High | 1–5 star reviews with ≤5 images, only for delivered orders, vendor responses, moderation |
| FR-007 | Vendor Onboarding & KYC | B03 | Critical | Vendor registration, document submission, KYC review (≤48 h), approval/rejection/suspension |
| FR-008 | Store Management & Storefront Configuration | B03 | High | Store profiles, branding, zones, operating settings, follower feature |
| FR-009 | Search & Discovery | B04 | High | Arabic-aware full-text search, filters, sorting, category browse, banners/merchandising |
| FR-010 | Shopping Cart | B05 | Critical | Multi-vendor cart, guards (50/10/5 — C-15), 15-min reservation countdown, server reconciliation |
| FR-011 | Checkout & Order Placement | B05 | Critical | 7-step checkout, address → shipping → wallet payment → review → confirm; idempotent order creation |
| FR-012 | Order Lifecycle Management | B06 | Critical | Exactly 17 states (C-09), master/sub-orders (C-10), transitions, timelines, customer/vendor/admin actions |
| FR-013 | Wallet & Payment Processing | B07 | Critical | Balance, top-ups (C-05), payments, double-entry ledger, freezes; wallet-only enforcement (C-01) |
| FR-014 | Escrow, Commission & Vendor Payouts | B07 | Critical | 7-day escrow hold (C-12), commission 5–20% (default 10%), payout scheduling, refund flows |
| FR-015 | Shipping & Delivery | B08 | Critical | Shipping zones/costs, courier assignment, pickup → transit → delivery, 6-digit code confirmation (C-16) |
| FR-016 | Returns & Refunds | B09 | Critical | Merchant return policy (C-11), return request → inspection → wallet refund |
| FR-017 | Notifications & Messaging | B10 | High | SMS, WhatsApp, in-app, push fan-out; templates; preferences; security notices mandatory |
| FR-018 | Analytics & Reporting | B11 | Medium | Admin & vendor dashboards, sales/finance/ops reports, export |
| FR-019 | Content & Promotions (CMS + Coupons) | B12 | High | Static pages, banners, coupon engine (non-stackable, ≤90%), featured/deal merchandising |
| FR-020 | Platform Administration, Settings & Audit | B13 | Critical | Admin console, platform settings, audit logs, support tickets, dispute handling, role management |

---

## 2. Non-Functional Requirements (`NFR-001…NFR-020`)

Expands to `02-requirements/non-functional/NFR-nnn.md`; measurement detail in `12-non-functional/`.

| ID | Category | Title | Target (summary) |
|---|---|---|---|
| NFR-001 | Performance | API response time | p95 < 200 ms read, < 500 ms write under nominal load |
| NFR-002 | Performance | Client performance | LCP < 2.5 s on 4G mobile; JS bundle < 200 KB gzipped (customer web) |
| NFR-003 | Scalability | Concurrency | 10,000 concurrent users (C-25) sustained within NFR-001 |
| NFR-004 | Performance | Caching | Read-heavy endpoints cached (Redis); cache hit ratio ≥ 80% on catalog reads |
| NFR-005 | Availability | Uptime | 99.99% monthly (C-26) |
| NFR-006 | Recoverability | RTO / RPO | RTO ≤ 1 h; RPO ≤ 15 min |
| NFR-007 | Reliability | Fault tolerance | Graceful degradation: search/caches down → browse works; queue down → retries; no silent data loss |
| NFR-008 | Reliability | Data integrity | ACID transactions; idempotency on all money/order/stock operations; zero ledger imbalance |
| NFR-009 | Maintainability | Modularity & standards | Monolith modules with enforced boundaries (C-21); lint/type/test gates in CI; docs current |
| NFR-010 | Maintainability | Testability | All business logic unit-testable without network; coverage thresholds (AC-S-08) |
| NFR-011 | Accessibility | WCAG 2.1 AA | ≥95% automated pass; zero critical violations; keyboard + screen-reader support |
| NFR-012 | Usability | Core-task efficiency | New customer completes registration→first order < 5 min; vendor lists product < 10 min |
| NFR-013 | Localization | Bilingual RTL/LTR | Arabic default, English parity; locale-aware dates/numbers/currency (C-24) |
| NFR-014 | Observability | Logging/metrics/tracing | Structured logs, RED metrics per endpoint, correlation IDs, alerting (see `12-non-functional/observability.md`) |
| NFR-015 | Compatibility | Browsers/devices | Last 2 versions Chrome/Safari/Firefox/Edge; Android 10+, iOS 15+ |
| NFR-016 | Portability | Deployment | Runs on any Docker host; no cloud-vendor lock-in in v1 |
| NFR-017 | Capacity | Storage growth | Design for 10M products, 100M order-line records, 5-year retention (partitioning plan) |
| NFR-018 | Scalability | Scale-out path | Stateless API replicas behind LB; DB read replicas; documented path to scale beyond C-25 |
| NFR-019 | Compliance | Legal/data | PDPA-aligned controls, VAT calculation on every order, audit retention ≥ 5 years for financial records |
| NFR-020 | Operability | Supportability | Runbooks, config via environment, health endpoints, zero-downtime deploys (expand-contract migrations) |

---

## 3. Security Requirements (`SEC-REQ-001…SEC-REQ-012`)

Expands to `02-requirements/security/SEC-REQ-nnn.md`; controls detailed in `09-security/`.

| ID | Title | Summary |
|---|---|---|
| SEC-REQ-001 | Strong phone-based verification | OTP required for registration, password reset, sensitive changes (6 digits, 5 min, 3 attempts) |
| SEC-REQ-002 | Credential storage | Passwords bcrypt (cost 12); never store plaintext; phone numbers encrypted at rest |
| SEC-REQ-003 | Token security | JWT RS256; access 15 min; refresh 7 days single-use rotation; httpOnly + SameSite cookies; ≤5 devices (C-08) |
| SEC-REQ-004 | Server-side authorization | RBAC + ownership checks on every endpoint; frontend guards are UX only, never security |
| SEC-REQ-005 | Brute-force protection | Account lockout 5 failures → 15 min; OTP 3 attempts; delivery code 3 attempts → 24 h lock |
| SEC-REQ-006 | Transport & data encryption | TLS 1.3 enforced; AES-256 at rest for PII/financial fields |
| SEC-REQ-007 | Secrets management | All secrets via environment/secrets manager; CI secret scanning; no keys in repo |
| SEC-REQ-008 | Injection/XSS/CSRF defense | Parameterized queries (Prisma), output encoding, CSP, CSRF tokens for cookie auth |
| SEC-REQ-009 | Rate limiting & abuse control | Per-IP and per-user limits (100 req/min standard); stricter on OTP/top-up endpoints |
| SEC-REQ-010 | Audit trail integrity | Append-only audit log for privileged & money actions; tamper-evident chain |
| SEC-REQ-011 | File upload security | Type/size validation, EXIF strip, malware scan, no SVG execution; ≤5 MB images |
| SEC-REQ-012 | Vulnerability management | SAST/DAST/dependency scanning in CI; critical vulns fixed ≤ 7 days |

---

## 4. Data Requirements (`DATA-REQ-001…DATA-REQ-008`)

Expands to `02-requirements/data/DATA-REQ-nnn.md`; detail in `16-data/`.

| ID | Title | Summary |
|---|---|---|
| DATA-REQ-001 | Integrity constraints | FKs, unique/check constraints, NOT NULL where required; referential integrity enforced in DB not just app |
| DATA-REQ-002 | Personal data minimization | Collect only needed PII; classify per `16-data/data-classification.md` |
| DATA-REQ-003 | Retention & deletion | Configurable retention; account deletion workflow; financial records ≥ 5 years (NFR-019) |
| DATA-REQ-004 | Backup & restore | Continuous WAL + daily snapshots; quarterly restore drills (NFR-006) |
| DATA-REQ-005 | Schema evolution | Expand-contract migrations; backward-compatible deploys (NFR-020) |
| DATA-REQ-006 | Data quality validation | Validation at write time + reconciliation jobs (stock, wallet, escrow) |
| DATA-REQ-007 | Financial immutability | Ledger append-only: corrections via compensating entries, never UPDATE/DELETE of postings |
| DATA-REQ-008 | Ownership boundaries | Every tenant-scoped row carries owner keys (user_id/store_id) enforced by queries + tests |

---

## 5. Integration Requirements (`INT-REQ-001…INT-REQ-008`)

Expands to `02-requirements/integration/INT-REQ-nnn.md`; contracts in `10-integrations/`.

| ID | Title | Summary |
|---|---|---|
| INT-REQ-001 | Wallet top-up providers | m-Floos + OneCash: initiate → callback/poll → credit ledger; reconciliation job; sandbox before prod (DEP-05) |
| INT-REQ-002 | Bank transfer top-up | Manual admin verification flow before crediting (BR-PAY-04) |
| INT-REQ-003 | SMS provider failover | Two providers; primary → failover on timeout/error; delivery receipts logged |
| INT-REQ-004 | WhatsApp Business notifications | Template messages for OTP fallback, order updates; approval-gated templates |
| INT-REQ-005 | Delivery orchestration | Internal assignment engine; abstraction allows future external fleet APIs |
| INT-REQ-006 | Webhook robustness | Signed webhooks, idempotent handlers, 3 retries + exponential backoff + DLQ (BR-PLT-02) |
| INT-REQ-007 | Observability export | Prometheus scrape, Grafana dashboards, alert routes to on-call |
| INT-REQ-008 | Provider abstraction | Payment/SMS interfaces behind adapters — no vendor types leak into domain code |

---

## 6. Requirement Quality Statement

Every requirement file must pass the 7-question quality test (clarity, completeness, consistency, feasibility, testability, necessity, traceability) and carry: description, source, priority, rationale, dependencies, preconditions, expected result, acceptance criteria, verification method. Weak entries are flagged in `20-validation/requirements-validation.md`.

## 7. Approved Backlog (pointer — not yet `FR-*`)

> Approved 2026-09-28 by the administrator (`plan-develop.md` v1.2 §8 `D9`/`D10`). The canonical
> rows live in [`plan-develop.md`](../../plan-develop.md): modifications `M-01…M-25` (§1),
> proposed features `P-01…P-20` (§2), the 59-row completeness checklist (§3), and the
> admin/role/ERP decisions (§4–§6). **Nothing in this backlog is a requirement yet** — each row
> converts to an `FR-*` (or `NFR-*`/`INT-REQ-*`) with acceptance criteria **at its build wave**,
> never earlier (`SPE-03` / `D-02` / `plan-develop.md` §0.4). Coverage mapping after conversion
> belongs in `19-traceability/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial registry (68 requirements) | Initial analysis |
| 1.1 | 2026-09-28 | New §7 approved-backlog pointer to `plan-develop.md` (no `FR-*` minted — wave discipline) | `plan-develop.md` v1.2 §8 approval implementation (session 007, `D9`/`D10`) |
