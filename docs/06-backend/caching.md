---
document_id: DOC-BE-007
title: Caching — Redis Strategy, TTLs, Invalidation & Non-Cacheable Data
category: 06-backend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-004, NFR-007, NFR-018, FR-009, FR-013]
related_documents: [DOC-BE-001, DOC-BE-002, DOC-BE-006, DOC-BA-005]
---

# Caching — Redis Strategy

Redis 7 serves four distinct roles: **application cache**, **session/OTP/rate-limit state**, **BullMQ backend**, and **hot read-model storage**. Elasticsearch handles full-text search; Redis never does. Cache hit ratio target on catalog reads: **≥ 80%** (`NFR-004`).

---

## 1. What Is Cached (with TTLs)

| Key pattern | Content | TTL | Pattern | Owner module |
|---|---|---|---|---|
| `cat:tree:v{n}` | category tree (5 levels max) | 10 min | cache-aside | b04-search |
| `cat:{slug}:v{n}` | category node | 10 min | cache-aside | b04-search |
| `prod:{id}:v{n}` | product detail projection (price display, images, attrs) | 60 s | cache-aside + version bump on write | b02-catalog |
| `store:{id}:profile` | store profile/follower count | 5 min | cache-aside | b03-store |
| `search:suggest:{q}` | autocomplete suggestions | 5 min | TTL-only | b04-search |
| `cms:page:{slug}` | published CMS content | 10 min | cache-aside, purge on publish | b12-content |
| `banner:home:{locale}` | home banners/merchandising | 5 min | write-through on publish | b12-content |
| `cart:{userId}` | server cart snapshot | 15 min (= reservation window) | write-through | b05-checkout |
| `sess:{sid}` / `sessions:{userId}` | session registry, refresh rotation markers | 7 d / sliding | write-through (authoritative) | b01-identity |
| `otp:{phone}:{ctx}` | OTP + attempt counters | 5 min | write-through (authoritative) | b01-identity |
| `rl:{scope}:{id}` | rate-limit counters (SEC-REQ-009) | window-sized | write-through (authoritative) | shared/auth |
| `lock:fail:{phone}` | login failure/lockout counter | 15 min | write-through (authoritative) | b01-identity |
| `idem:{key}` | idempotency replay records | 24 h | write-through | shared/idempotency |
| `price:ship:{zone}:{method}` | shipping fee rates | 30 min | cache-aside | b08-shipping |
| `coupon:{code}` | coupon definition (validation fast path) | 60 s | cache-aside | b12-content |
| `perm:matrix` | RBAC permission matrix snapshot | 5 min | version-keyed | shared/auth |

Versioning pattern: `…:v{n}` where `n` is a per-entity version counter bumped on write → invalidation is a single `INCR`, not key enumeration.

## 2. Cache Patterns

| Pattern | Used for | Mechanics |
|---|---|---|
| **Cache-aside** | catalog, CMS, shipping rates | read: miss → DB → SET with TTL; write: bump version (invalidate) |
| **Write-through** | cart, sessions, OTP, rate limits, idempotency | Redis is updated in the same operation as the business event; TTL enforces lifecycle |
| **Read-through with stampede control** | product detail (hot) | see §4 |
| **Not used: write-back** | — | Redis is never a durability layer for money or stock (`NFR-008`) |

## 3. Invalidation Events

| Event | Invalidation action |
|---|---|
| Product create/update/price/stock change | `INCR prod:{id}:v` (+ ES sync via `b02.catalog.index`) |
| Product soft-delete/deactivate | version bump + storefront 404 path (`BR-CAT-06`) |
| Category tree change | bump `cat:tree:v` (all node keys carry same tree version) |
| Store profile/suspension change | bump store profile key; suspension also hides products (`BR-VND-04`) |
| CMS publish / banner change | purge `cms:page:*`, `banner:*` + notify CDN/ISR revalidation (`b12.content.publish`) |
| Coupon create/disable | short TTL (60 s) does most work; explicit bump on admin disable |
| Locale content change | keys are locale-suffixed where content differs |
| RBAC matrix change | bump `perm:matrix` + revoke affected sessions (DOC-BE-004 §2) |

**Rule:** invalidation is emitted from the **service layer** (after commit), never from controllers — so job-driven updates invalidate too.

## 4. Stampede / Thundering-Herd Protection

| Layer | Technique |
|---|---|
| Single hot key | **soft TTL + hard TTL**: store `expires_at` inside the value; stale-but-usable for 5 s while only the first requester queries the DB behind a Redis `SET NX` lock (500 ms lease) |
| Negative caching | "not found / inactive" cached 10 s to absorb bot sweeps (still 404 semantics) |
| Enumeration storms | category tree served as **one** key, not per-node fan-out |
| ES outage | cached catalog remains servable; misses fall back to DB, not to ES (NFR-007) |
| Cold start / deploy | warm-up job pre-loads category tree, home banners, shipping rates into Redis |

## 5. Non-Cacheable (always fresh)

| Data | Why never cached |
|---|---|
| **Wallet balance** | money display must be exact (`BR-PAY-05/06`) — read from DB in the request |
| **Order status / timeline** | 17-state machine moves continuously (`C-09`); stale state causes wrong UX and 409 loops |
| **Ledger / transactions** | financial truth, append-only (DATA-REQ-007) |
| **Escrow / payable balances** | settlement-critical (`BR-ESC-*`) |
| **Stock counts at checkout** | atomic reservation is authoritative (`BR-CAT-07`) |
| **Session/permission checks** | security-relevant — Redis is *used* here, but as authoritative state, not as a disposable cache |
| **Any personalized/admin page** | dashboards query DB/read models per request |

Middleware enforces this: a deny-list of route prefixes fails CI if wrapped in cache decorators.

## 6. Redis vs Elasticsearch vs DB

| Need | Store | Reason |
|---|---|---|
| Full-text Arabic search, facets, ranking | **Elasticsearch 8** | analyzers, relevance (`FR-009`, `C-24` drives ES Arabic analyzer) |
| Hot key-value reads, counters, locks, queues | **Redis 7** | latency, TTL, atomic ops |
| Authoritative transactional state | **PostgreSQL 16** | ACID (`C-19`, `NFR-008`) |
| Trending/hot analytics aggregates | Redis read-model → DB rollups (`b11.analytics.rollup`) | dashboards without DB hammering |
| Derived search docs consistency | DB → event → ES (idempotent) (`DOC-BE-006` §6) | DB always wins |

## 7. Degradation (NFR-007)

| Failure | Behavior |
|---|---|
| Redis cache down | **bypass mode**: reads go to DB (higher latency, correct data); writes unaffected except sessions/OTP/rate limits which are Redis-authoritative → auth endpoints return explicit 503 `DEPENDENCY_UNAVAILABLE` with retry (never silent security bypass) |
| ES down | browse by category + ISR pages continue; search shows localized fallback (NFR-007) |
| Stampede during recovery | soft-TTL warm-up; DB connection pool protected by queueing |
| Memory pressure | `allkeys-lru` for **cache** DB; separate Redis logical DB/instance for authoritative state (sessions/OTP/rate limits/queues) so eviction never destroys security state |
| Monitoring | hit ratio, memory, evictions, latency exported to Prometheus; hit ratio < 80% on catalog reads alerts (NFR-004) |

## 8. Client-Facing Caching Interaction

| Surface | Behavior |
|---|---|
| Next.js ISR pages | CDN caches HTML for catalog/CMS routes; purge on publish (`05-frontend/frontend-performance.md` §3) |
| HTTP caching | static assets immutable hashed; API responses `no-store` unless explicitly cacheable (money routes always `no-store`) |
| Clients | TanStack Query stale-times per `05-frontend/state-management.md` §2 — aligned with these TTLs but never exceeding them for catalog data |

## 9. Verification

| Test | Coverage |
|---|---|
| Unit | TTL values from a single constants module; version-bump invalidation logic |
| Integration | write → immediate read reflects change; stampede test (100 concurrent misses → 1 DB query) |
| Load | cache hit ratio ≥80% on catalog reads under k6 suite (NFR-004) |
| Negative | deny-list routes never cached; Redis flush → correct bypass behavior |
| Constraint | wallet/order endpoints return `Cache-Control: no-store` (checked in API tests) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
