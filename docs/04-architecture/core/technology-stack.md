---
document_id: DOC-ARCH-009
title: Technology Stack Register
category: 04-architecture
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-002, NFR-010, NFR-013, NFR-015, NFR-016]
related_documents: [DOC-ARCH-002, DOC-ARCH-010, DOC-OVR-008, DOC-OVR-010, DOC-REQ-001]
---

# Technology Stack Register

The authoritative register of every technology in yumn, with version, rationale, governing constraint/driver, and the alternatives that were considered and rejected. Constraint references are IDs, never restated text. Decisions are indexed in `architecture-decisions-reference.md` (DOC-ARCH-010) and written as full ADRs in `18-decisions/core/`.

## 1. Runtime & Language

| Layer | Technology | Version | Rationale | Constraint / driver | Alternatives considered |
|---|---|---|---|---|---|
| Backend runtime | Node.js | 20 LTS | LTS stability; matches full-stack TS; event I/O fits API + workers | `DEP-01` | Node 18 (older LTS), Deno/Bun (immature ecosystem) |
| Language | TypeScript | 5.x | Type safety across web/api/mobile; enables strict module boundaries | `DEP-01`, `NFR-009` | Plain JS (no static boundaries), Java/Kotlin (team/stack mismatch — `INFERENCE`) |
| Frontend runtime | Node.js (build) + browser | 20 / evergreen | Same toolchain as backend | `NFR-015` | — |

## 2. Application Frameworks

| Layer | Technology | Version | Rationale | Constraint / driver | Alternatives considered |
|---|---|---|---|---|---|
| API framework | NestJS | 10 | Module architecture maps 1:1 to blocks `B01…B13`; DI, guards, pipes; strong TS support | `C-21` (modular monolith), `ADR-003` | Express (no module discipline), Fastify-only (smaller ecosystem of structural patterns), Spring/Django (different language) |
| Customer/vendor/admin web | Next.js | 14 | SSR for discovery performance, routing, image handling; three shells in one app | `NFR-002`, `NFR-013`, `ADR-008` | SPA-only React + Vite (weaker SEO/first paint), Angular (heavier), Nuxt (Vue — stack consistency) |
| Mobile (customer + courier) | React Native | 0.73 | One codebase for two apps; shares TS/domain vocabulary with web | `NFR-015`, `ADR-008`, `DEP-12` | Flutter (second language), two native apps (double cost) |

## 3. Data & Messaging

| Layer | Technology | Version | Rationale | Constraint / driver | Alternatives considered |
|---|---|---|---|---|---|
| Relational DB | PostgreSQL | 16 | Only relational DB allowed; ACID for money/order/stock; JSON flexibility for metadata | `C-19`, `DEP-02`, `ADR-001` | MySQL (excluded by C-19), MongoDB (no relational integrity for ledger) |
| ORM | Prisma | 5 | Typed models, migrations, parameterized queries by default | `SEC-REQ-008`, `DATA-REQ-005` | TypeORM (weaker typing ergonomics), Knex/raw SQL (more boilerplate) |
| Cache / coordination | Redis | 7 | Cache, counters, TTL keys, and queue substrate — one dependency | `C-20`, `DEP-03`, `NFR-004` | Memcached (no queues/structures), Hazelcast (extra technology) |
| Job/queue system | BullMQ | current with Redis 7 | The only allowed queue: retries/backoff/DLQ, delayed jobs for timers | `C-20`, `BR-PLT-01/02`, `ADR-005` | RabbitMQ, Kafka (both excluded), SQS (cloud lock-in), cron-only (no retries/DLQ) |
| Search | Elasticsearch | 8 | Arabic-aware full-text, facets, aggregations for `FR-009` | `DEP-04`, `ADR-006` | PostgreSQL FTS (weaker Arabic handling/scale), Meilisearch/Typesense (smaller feature/aggregation surface) |
| Object storage | MinIO | current S3-compatible | Self-hosted, no cloud lock-in, S3 API portability | `DEP-07`, `NFR-016`, `ADR-007` | Local disk only (no growth path), AWS S3 (lock-in) |

## 4. Delivery & Operations

| Layer | Technology | Version | Rationale | Constraint / driver | Alternatives considered |
|---|---|---|---|---|---|
| Container runtime | Docker | current | Standard packaging; any Docker host runs it | `C-22`, `NFR-016` | Podman (fine but no gain), VM images (heavier) |
| Orchestration | Docker Compose | current | Single-host topology, layered parity across environments | `C-22`, `ADR-004` | Kubernetes (**excluded by C-22**), Nomad/Swarm (unneeded complexity) |
| CI/CD | GitHub Actions | current | Repo-native pipelines, secret scanning, OIDC to environments | `SEC-REQ-012`, `NFR-020` | GitLab CI, Jenkins (extra infra) |
| Edge/reverse proxy | Nginx (or equivalent) | current | TLS termination, routing, static delivery | `SEC-REQ-006`, `DEP-08` | Traefik (viable alternative; chosen at implementation — `INFERENCE`), cloud LB (lock-in) |
| CDN/DNS | Cloudflare | current | TLS, DDoS, asset caching in region | `DEP-08` | Self-hosted CDN (cost/complexity) |

## 5. Quality & Observability

| Layer | Technology | Version | Rationale | Constraint / driver | Alternatives considered |
|---|---|---|---|---|---|
| Unit/integration tests | Jest | current | First-class TS/TS NestJS support; fast; mocks for ports | `NFR-010` | Mocha/Vitest (viable; Jest default for Nest) |
| E2E tests | Playwright | current | Web E2E incl. RTL assertions; cross-browser matrix | `NFR-015`, `NFR-011` | Cypress (single-tab limitations) |
| Load tests | k6 | current | Scriptable, CI-friendly concurrency scenarios | `NFR-003`, `C-25` | JMeter (heavier), Locust (Python stack) |
| Lint/format | ESLint + Prettier | current | Module-boundary lint rules are a hard gate | `NFR-009`, DOC-ARCH-006 | — |
| Metrics | Prometheus | current | Scrape-based metrics, alert rules | `INT-REQ-007`, `NFR-014` | Datadog (SaaS lock-in/cost) |
| Dashboards | Grafana | current | Metric dashboards for RED/queue/DB views | `INT-REQ-007` | — |
| Alerting | Alertmanager / Grafana alerting | current | Routes to on-call | `INT-REQ-007` | PagerDuty-only (integration possible later) |
| Accessibility checks | axe-style automated scans | current | ≥95% automated pass, zero critical | `NFR-011` | Manual-only (insufficient) |

## 6. External Provider SDKs & Protocols

| Concern | Approach | Version/notes | Constraint / driver | Alternatives considered |
|---|---|---|---|---|
| Wallet top-up (m-Floos, OneCash) | Thin REST adapters in `WalletModule`, sandbox-first | Provider-documented APIs (`DEP-05` status: not started) | `C-05`, `INT-REQ-001`, `INT-REQ-008` | Direct SDK types in domain (rejected — F8), single provider only |
| Bank transfer top-up | Manual admin verification, no bank API | Human workflow | `INT-REQ-002`, `BR-PAY-04` | Bank API integration (no access in v1) |
| SMS | Two-provider adapter with failover | Telesom/Sabafon per `DEP-06` (not started) | `INT-REQ-003` | Single provider (no failover), aggregator SaaS (to evaluate) |
| WhatsApp Business | Template messages via provider API | Approval-gated templates | `INT-REQ-004`, `DEP-06` | Unofficial APIs (policy risk — rejected) |
| Push | APNs + FCM via push adapter | Registered device tokens | `FR-017`, `BR-NTF-01` | Third-party push SaaS (optional later) |
| Auth tokens | JWT RS256, 15 min access / 7-day single-use rotating refresh | httpOnly + SameSite cookies / secure storage | `C-08`, `SEC-REQ-003`, `ADR-010` | Opaque server sessions (no stateless scale-out), social login (excluded by `C-06`) |
| Password hashing | bcrypt cost 12 | | `SEC-REQ-002`, `BR-AUTH-02` | Argon2 (viable alternative; bcrypt is the specified baseline) |
| OTP | 6-digit, 5-min, 3 attempts, 60 s cooldown, ≤3 resends/10 min | SMS primary → WhatsApp fallback | `BR-AUTH-03`, `SEC-REQ-001`, `ADR-010` | TOTP apps (out of scope), email OTP (excluded — `C-06`, `BR-AUTH-08`) |

## 7. Explicitly Excluded Technologies

| Excluded | Because | IDs |
|---|---|---|
| Shopify / Medusa / WooCommerce / Saleor / any commerce platform | Custom build mandate | `C-18` |
| Kubernetes | Compose-only v1 | `C-22`, `ADR-004` |
| Microservices frameworks, Kafka, RabbitMQ | Monolith + BullMQ only | `C-21`, `C-20` |
| Non-PostgreSQL relational databases | Single RDBMS | `C-19` |
| Card processors (Stripe, Moyasar, Tap), BNPL, crypto rails | Payment exclusions | `C-02`, `C-03`, `C-04` |
| Email delivery stack | No email channel in v1 | `BR-NTF-01`, `GAP-03` |
| Geolocation/telemetry SDKs | No GPS | `C-16`, `BR-SHP-05` |
| Cloud-vendor managed services as hard dependencies | Portability | `NFR-016` |

## 8. Register Maintenance

Changes to this register require: (1) an ADR in `18-decisions/core/` (new or superseding), (2) an update here with rationale + constraint check, (3) an update to DOC-ARCH-010, (4) impact check recorded via `../../20-validation/core/consistency-audit.md`. Versions drift with lockfile updates within the same major line without an ADR; a **major** or product change always requires one.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
