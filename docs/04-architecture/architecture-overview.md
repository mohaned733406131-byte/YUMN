---
document_id: DOC-ARCH-002
title: Architecture Overview
category: 04-architecture
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-001, NFR-003, NFR-005, NFR-007, NFR-009, NFR-016, NFR-018]
related_documents: [DOC-OVR-008, DOC-SA-002, DOC-SA-003, DOC-ARCH-003, DOC-ARCH-010, DOC-REQ-001]
---

# Architecture Overview (Source of Truth)

This document is the **authoritative statement of yumn's technical architecture**: principles, the C4 level-1 context and container views, the quality attributes that drive decisions, and the major technology choices with their constraint references. Detail views expand from here: containers (DOC-ARCH-003), components (DOC-ARCH-004), deployment (DOC-ARCH-005), data flow (DOC-ARCH-007), stack (DOC-ARCH-009), decisions (DOC-ARCH-010).

## 1. Architecture Principles

| # | Principle | Origin | What it means in practice |
|---|---|---|---|
| P1 | Custom build | `C-18` | No Shopify/Medusa/WooCommerce/Saleor. All domain logic is purpose-built; dependencies are libraries, not platforms. |
| P2 | Modular monolith | `C-21` (`ADR-002`) | One deployable backend composed of strongly separated modules (`B01…B13`); no network calls between domain parts; boundaries enforced by tooling (`module-boundaries.md`). |
| P3 | Single relational store | `C-19` | PostgreSQL 16 is the only RDBMS; money and order state live in one ACID transaction boundary (`NFR-008`). |
| P4 | One job system | `C-20` | BullMQ on Redis for all background work — no Kafka/RabbitMQ; queue naming `{block}.{entity}.{action}` (`BR-PLT-01`). |
| P5 | Single-host container deployment | `C-22` (`ADR-004`) | Docker Compose only in v1; no Kubernetes; environment parity via compose layers. |
| P6 | Wallet-only money | `C-01…C-05` (`ADR-009`) | Payments are ledger movements; provider adapters sit at the edge (`INT-REQ-008`). |
| P7 | Arabic-first, two locales | `C-24` | RTL is a structural property of the frontend architecture, not a stylesheet afterthought (`NFR-013`). |
| P8 | Stateless application tier | `NFR-018` | API replicas scale horizontally; session state lives in tokens (`C-08`), cache state is disposable. |
| P9 | Degrade, never corrupt | `NFR-007`/`NFR-008` | Optional subsystems (search, cache, notifications) may fail; money/stock invariants must hold. |
| P10 | Greenfield, no coexistence | `C-23` | No adapters for legacy systems; schemas designed cleanly for `b01…b13`. |

## 2. C4 Level 1 — System Context

Identical in meaning to the analysis context (DOC-SA-003), expressed with the technical actors and provider endpoints:

```text
        Customer web/mobile · Vendor panel · Admin console · Courier app
                                    │ HTTPS (TLS 1.3)
                                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          y u m n  (يُمن)                            │
│   Multi-vendor marketplace — modular monolith + companion clients   │
│   B01 Identity · B02 Catalog · B03 Store · B04 Search · B05 Cart    │
│   B06 Orders · B07 Wallet/Escrow · B08 Shipping · B09 Returns       │
│   B10 Notifications · B11 Analytics · B12 CMS · B13 Administration  │
└───────────────┬──────────────────────────────────┬───────────────────┘
                │ egress via adapters              │ inbound webhooks
                ▼                                  ▼
   SMS providers · WhatsApp Business · m-Floos/OneCash · push services
                (INT-REQ-001/003/004/006, INT-REQ-008)
```

## 3. C4 Level 1 — Containers

```text
 ┌────────────┐   ┌───────────────────┐   ┌───────────────────┐
 │ Web app    │   │ Customer mobile   │   │ Courier mobile    │
 │ Next.js 14 │   │ React Native 0.73 │   │ React Native 0.73 │
 │ (storefront│   └─────────┬─────────┘   └─────────┬─────────┘
 │  vendor    │             │                       │
 │  admin)    │             │        HTTPS/JSON (REST, JWT 15m/7d)
 └─────┬──────┘             │                       │
       └────────────────────┴───────────┬───────────┘
                                       ▼
                          ┌─────────────────────────┐
                          │ NestJS API (modular      │
                          │ monolith) — synchronous   │
                          │ domain logic, B01…B13     │
                          └───┬───────────┬──────────┘
                Prisma 5      │           │ enqueue / consume
                              ▼           ▼
 ┌──────────────┐   ┌──────────────────┐   ┌────────────────────┐
 │ PostgreSQL 16│   │ Redis 7          │   │ BullMQ workers     │
 │ system of    │   │ cache, locks,    │   │ (same codebase,    │
 │ record       │   │ sessions-adj.,   │   │  separate process) │
 └──────────────┘   │ job queues       │   └─────────┬──────────┘
                    └──────────────────┘             │
 ┌──────────────────┐  ┌──────────────────┐          │
 │ Elasticsearch 8  │  │ MinIO (S3)       │◄─────────┘
 │ search/discovery │  │ images & media   │   (index writes, uploads)
 └──────────────────┘  └──────────────────┘
```

Container responsibilities and communication protocols: `container-view.md` (DOC-ARCH-003).

## 4. Quality Attributes Driving Decisions

| Driver | Target | Architectural consequence | Decision |
|---|---|---|---|
| Concurrency (`C-25`, `NFR-003`) | 10,000 concurrent users within `NFR-001` latency | Stateless API behind load balancer, Redis read cache, connection pooling, ES query offload | `scalability.md`, `ADR-002`, `ADR-005` |
| Availability (`C-26`, `NFR-005`) | 99.99%/month; RTO ≤1 h, RPO ≤15 min | Readiness gates, health endpoints, WAL + snapshots, Compose-level restart policies, graceful degradation | `BR-PLT-07`, `NFR-006`, `deployment-view.md` |
| Performance (`NFR-001`, `NFR-004`) | p95 < 200 ms read / < 500 ms write; catalog cache hit ≥ 80% | Redis cache layer, ES for search, static/CDN delivery of assets | `data-flow.md`, `ADR-006` |
| Reliability (`NFR-007`, `NFR-008`) | No silent data loss; idempotent money/order/stock ops | BullMQ retries + DLQ, idempotency keys, ACID transactions, saga with compensation | `BR-PLT-02/03/04`, DOC-SA-009 |
| Maintainability (`NFR-009`, `NFR-010`) | Enforced module boundaries; unit-testable business logic | Modular monolith with lint-enforced imports; pure domain services | `module-boundaries.md`, `ADR-002` |
| Operability (`C-22`, `NFR-016`, `NFR-020`) | Any Docker host, no vendor lock-in, zero-downtime deploys | Compose parity across environments; expand-contract migrations | `deployment-view.md`, `ADR-004` |
| Scale-out path (`NFR-018`) | Documented path beyond `C-25` | Read replicas, partitioning, more API/worker replicas — all within Compose | `scalability.md` |
| Capacity (`NFR-017`) | 10M products, 100M order-line records, 5-year retention | Schema/index design + partition plan for order/ledger history | `08-database/`, `scalability.md` |
| Security (`SEC-REQ-003/004/009`) | 15-min access JWT, server-side authz, rate limits | JWT verification at API edge; RBAC guard per request | `ADR-010`, `09-security/` |

## 5. Major Technology Choices (summary; full register in DOC-ARCH-009)

| Concern | Choice | Constraint / driver | Decision |
|---|---|---|---|
| Backend framework | NestJS 10 (Node 20, TypeScript 5) | `DEP-01`; module structure suits monolith | `ADR-003` |
| Relational database | PostgreSQL 16 via Prisma 5 | `C-19`, `DEP-02` | `ADR-001` |
| Cache + queues | Redis 7 + BullMQ | `C-20`, `DEP-03` | `ADR-005` |
| Search | Elasticsearch 8 | `FR-009` Arabic-aware search, `DEP-04` | `ADR-006` |
| Object storage | MinIO (S3-compatible) | `DEP-07`, `NFR-016` (no cloud lock-in) | `ADR-007` |
| Customer/vendor/admin web | Next.js 14 | `NFR-002`, `NFR-013` RTL, SSR for discovery | `ADR-008` |
| Mobile (customer + courier) | React Native 0.73 | One codebase, two surfaces, `NFR-015` | `ADR-008` |
| Deployment | Docker + Docker Compose | `C-22` | `ADR-004` |
| Payments | Wallet-only with provider adapters | `C-01…C-05` | `ADR-009` |
| Authentication | Phone + OTP, JWT 15 min / 7-day rotating refresh | `C-06…C-08`, `SEC-REQ-001/003` | `ADR-010` |
| CI / testing | GitHub Actions; Jest, Playwright, k6 | `NFR-010`, root ID conventions | — (process, not ADR) |
| Observability | Prometheus + Grafana | `INT-REQ-007`, `NFR-014` | — (integrates via `INT-REQ-007`) |

## 6. Architecture Shape in One Paragraph

A **single NestJS modular monolith** exposes a REST API consumed by three web surfaces (customer storefront, vendor panel, admin console — one Next.js 14 application with separate shells, `INFERENCE`) and two React Native 0.73 apps. **PostgreSQL 16 is the system of record** for identity, catalog, orders, wallet/ledger, escrow, delivery, returns, content and audit (schemas `b01…b13`); **Redis 7** provides caching, optimistic-lock coordination support and BullMQ queues; **BullMQ workers** (same codebase, separate process) execute background work — notification fan-out, escrow maturity, payouts, TTL expiry, search indexing, reconciliation; **Elasticsearch 8** serves search/discovery; **MinIO** stores images. External providers (SMS, WhatsApp, m-Floos/OneCash, push) are reached only through adapters, and webhooks enter only through verified, idempotent handlers. Everything deploys via **Docker Compose** on any Docker host.

## 7. What This Document Does Not Cover

Behavioral specification (states, rules, sequences, edge cases) — `03-system-analysis/`. Endpoint contracts — `07-api/`. Schema DDL — `08-database/`. Security control catalog — `09-security/`. Environment/pipeline mechanics — `14-devops-infrastructure/`. Decision texts — `18-decisions/ADR/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
