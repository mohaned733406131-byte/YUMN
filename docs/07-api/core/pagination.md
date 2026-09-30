---
document_id: DOC-API-004
title: API Pagination, Filtering, Sorting & Search Result Shape
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-004, FR-009, FR-012, FR-013, FR-017, FR-018, FR-020, NFR-001, NFR-004, NFR-014]
related_documents: [DOC-API-001, DOC-API-002, DOC-API-003, DOC-REQ-001, DOC-BA-005]
---

# Pagination, Filtering, Sorting & Search Result Shape

Rules for **every** list/read-collection endpoint in `07-api/`. Endpoint files state only which mode applies (`cursor` or `offset`).

---

## 1. Decision: Cursor vs Offset

| Family | Mode | Endpoints (examples) | Justification |
|---|---|---|---|
| Catalog / discovery feeds | **cursor** | `GET /products`, `GET /search/products`, `GET /categories/{slug}` products, storefront listings | Append-heavy, high-volume feeds read under `C-25` load (10,000 concurrent users); offset re-scans `OFFSET+n` rows, gets unstable while products are indexed/soft-deleted concurrently, and degrades past deep pages. Cursor (keyset on `(sortKey, id)`) is O(page), stable under concurrent indexing (`FR-009` requirement: "pagination remains stable under concurrent indexing"), and caches cleanly (`NFR-004`) |
| Orders / activity feeds | **cursor** | `GET /orders`, `GET /store/orders`, `GET /wallet/transactions`, `GET /notifications`, `GET /deliveries/mine`, `GET /support/tickets` (customer view) | Append-only streams sorted by `createdAt DESC`; customers page forward only; cursors survive inserts without the shift/duplicate artifacts of offset; `wallet/transactions` is append-only ledger — cursor guarantees no row is skipped (`DATA-REQ-007`) |
| Admin tables / queues | **offset** (default) | `GET /admin/users`, `GET /admin/vendors`, `GET /admin/kyc`, `GET /admin/moderation`, `GET /admin/topups`, `GET /admin/orders`, `GET /admin/coupons`, `GET /store/products`, `GET /store/reviews`, `GET /store/payouts`, `GET /returns`, `GET /admin/roles` | Operator queues are bounded (thousands, not millions of rows), demand **"page 7 of 12"** jumps, SLA-age sorting, and bulk review across pages; offset with a stable `sort=updatedAt,id` tie-break is simple, cacheable, and matches admin-console UX |
| Audit log | **cursor** (documented exception) | `GET /admin/audit-log` | Append-only, unbounded, 5-year retention (`NFR-019`); strictly `createdAt DESC` scan with server-side filters — matches `UC-036` (cursor pagination) and avoids O(n) offset scans on a partitioned table |
| Export | **neither** | `GET /store/reports/{family}/export` | Streams the full filtered result set as CSV with a hard row cap (100,000) — no paging params accepted |

**Rule:** a collection endpoint uses exactly one mode; accepting both is forbidden (ambiguity in `total` semantics). The mode is declared per group in `endpoints/`.

## 2. Envelopes

### 2.1 Cursor mode

Request: `?limit=<n>&cursor=<opaque>`

```json
{
  "items": [ { "id": "…", "…": "…" } ],
  "page": {
    "limit": 20,
    "nextCursor": "eyJpZCI6MTIzfQ",
    "hasMore": true,
    "total": { "value": 1284, "relation": "eq" }
  }
}
```

- `cursor` is an **opaque** base64 token (server encodes `sortKey` + `id`); clients must not parse or fabricate it.
- Invalid/stale cursor ⇒ 400 `VALIDATION_ERROR` with `details[].issue = CURSOR_INVALID`; client restarts from page 1.
- `nextCursor: null` + `hasMore: false` = end of feed.

### 2.2 Offset mode

Request: `?page=<n>&pageSize=<n>` (page is 1-based)

```json
{
  "items": [ { "id": "…", "…": "…" } ],
  "page": {
    "page": 3,
    "pageSize": 25,
    "total": 412,
    "totalPages": 17,
    "hasPrev": true,
    "hasNext": true
  }
}
```

- `page` beyond the last page ⇒ **200 with empty `items`** (not 404) — admin UIs probe pages speculatively.
- `pageSize` requested above the max ⇒ silently clamped to the max (never an error).

## 3. Page Sizes

| Mode / family | Default | Max | Notes |
|---|---|---|---|
| Cursor feeds (catalog, search, orders, notifications, transactions) | 20 | 50 | search default 24 (grid alignment); cart-adjacent feeds never exceed 50 |
| Offset admin tables | 25 | 100 | operator bulk review |
| Small reference lists (roles, devices, addresses, staff, categories) | 50 | 100 | usually fully returned on page 1 |
| Dashboard/timeseries responses | n/a | n/a | bounded by the date range, not paged |
| Export CSV | all rows | 100,000 | exceeds ⇒ 413 `PAYLOAD_TOO_LARGE` with guidance to narrow the range |

## 4. Filter Syntax

| Filter style | Syntax | Applies to |
|---|---|---|
| Equality | `?store=shoe-city-hadramaut` (slug) or `?storeId=<uuid>` | store, category, vendor, courier |
| Multi-equality | repeated key: `?status=PLACED&status=CANCELLED` | order/return/ticket states |
| Numeric range | `?priceMin=1000&priceMax=50000` (integer YER, inclusive) | products, wallet amounts |
| Date range | `?from=2026-09-01&to=2026-09-26` (ISO date, inclusive) | reports, audit log, dashboards |
| Boolean | `?inStock=true`, `?isReturnable=true` | product filters |
| Free text | `?q=<string>` (search endpoints only) | `GET /search/products`, `GET /search/suggest` |
| Arbitrary text | `?actor=<uuid>&action=order.cancel` | audit log, admin lists |
| Delimited | `?category=electronics,phones` — comma = OR within one filter key | facets |
| Unknown filter key | 400 `VALIDATION_ERROR` (`details[].issue = UNKNOWN_FILTER`) — never silently ignored (a dropped filter silently widens results = data exposure) |
| Empty value | `?status=` ⇒ 400 `VALIDATION_ERROR` |

Server-side filtering only: clients never receive the full result set to filter (`NFR-001`, `SEC-REQ-004`).

## 5. Sorting

| Endpoint family | Allowed `sort` values | Default |
|---|---|---|
| Product catalog/search | `relevance`, `price_asc`, `price_desc`, `newest`, `rating` | `relevance` (search), `newest` (browse) |
| Orders / returns / tickets | `createdAt_asc`, `createdAt_desc`, `status` | `createdAt_desc` |
| Admin queues | `updatedAt_desc`, `slaAge_desc`, `createdAt_asc` | `updatedAt_desc` (KYC/returns: `slaAge_desc`) |
| Wallet transactions | `createdAt_desc` only | `createdAt_desc` |
| Audit log | `createdAt_desc` only | `createdAt_desc` |
| Reviews | `createdAt_desc`, `rating_desc` | `createdAt_desc` |

- Syntax: `?sort=<field>_<dir>` or `?sort=relevance`; unknown value ⇒ 400 `VALIDATION_ERROR`.
- Every sort is **deterministic**: the server appends `,id` (or the cursor key) as tie-break — same query never yields shuffled pages (`FR-009` acceptance `AC-FR009-04`).
- Default direction is descending for time fields, ascending for price.

## 6. Elasticsearch-Backed Search Result Shape (FR-009)

`GET /search/products` response:

```json
{
  "items": [
    {
      "id": "…", "slug": "…", "nameAr": "…", "nameEn": "…",
      "price": 12500, "salePrice": null, "currency": "YER",
      "store": { "slug": "…", "nameAr": "…" },
      "categoryPath": ["electronics", "phones"],
      "rating": 4, "reviewCount": 31, "inStock": true,
      "highlights": { "nameEn": "<em>iPhone</em> case", "description": "…" }
    }
  ],
  "page": { "limit": 24, "nextCursor": "…", "hasMore": true, "total": { "value": 318, "relation": "eq" } },
  "facets": {
    "category": [ { "key": "electronics", "count": 210 }, { "key": "home", "count": 108 } ],
    "price":   [ { "key": "0-5000", "count": 40 }, { "key": "5000-20000", "count": 130 } ],
    "store":   [ { "key": "shoe-city-hadramaut", "count": 66 } ],
    "rating":  [ { "key": "4", "count": 190 } ],
    "inStock": [ { "key": "true", "count": 300 } ]
  },
  "meta": { "query": "هاتف", "tookMs": 38, "degraded": false, "locale": "ar" }
}
```

| Element | Rule |
|---|---|
| `items[].highlights` | ES `highlight` fragments with `<em>` tags; field names match indexed fields (name, description); absent when no match inside the hit |
| `facets` | computed on the **same** filter context as `items` (post-filtering via ES facets) — facet counts must equal what selecting that facet would return (`AC-FR009-04`) |
| facet pagination | facets are never paged; a facet key list > 100 entries is truncated with `truncated: true` |
| `meta.tookMs` | server-side query duration for observability (`NFR-014`) |
| `meta.degraded` | `true` when served from cache/category fallback while ES is warming; `SEARCH_UNAVAILABLE` (503) is returned only when no fallback exists (`NFR-007`) |
| Arabic analysis | normalization (alef/ya/ta-marbuta variants, diacritics) happens server-side; `q` is sent verbatim, never transformed by the client (`C-24`, `FR-009`) |
| Index freshness | products reflect index lag; `newest` sort uses index `createdAt` — eventual consistency is acceptable and documented to clients (`BR-PLT-01` jobs) |
| Caching | facet/aggregation responses cache in Redis keyed by `(query, filters, locale)` — target cache-hit ratio ≥ 80% (`NFR-004`) |

`GET /search/suggest` returns `{ "suggestions": [ { "text": "…", "type": "product|category|store", "slug": "…", "count": 12 } ] }` — at most 10 entries, no facets, no cursor (single-shot typeahead).

## 7. Total-Count Policy

| Mode | `total` semantics |
|---|---|
| Offset admin tables | **exact** integer — operators need "412 results" for SLA/bulk work |
| Cursor catalog/orders | `total.value` is an **estimate above 10,000 rows** with `relation: "gte"`; exact (`"eq"`) below it — counting millions of rows on every feed page violates `NFR-001` |
| Search (ES) | ES `total.value` with `relation` `eq` ≤ 10,000, `gte` above — mirrors ES track_total_hits behavior |
| Cached aggregates | `total` older than 30 s is acceptable for catalog/search (cache), never for wallet/ledger or admin queues |
| Wallet transactions | exact always — money views are not estimated (`DATA-REQ-007` integrity) |
| Export | row count in the CSV trailer comment matches the ledger exactly (`FR-018` `AC-FR018-03`) |

## 8. Cross-Endpoint Rules

- Every list endpoint accepts `limit`/`pageSize` within §3 and rejects non-integer values with 400 `VALIDATION_ERROR`.
- Pagination params are **read-only**: they never change server state (safe on GET per `api-conventions.md` §2).
- `X-Total-Count` header is emitted alongside offset envelopes for admin table headers.
- Collections that must reflect live state (order list, notification list) send `Cache-Control: no-store`; catalog/search feeds may send `Cache-Control: max-age=30`.
- Where a group mixes modes, the endpoint table in the group file names the mode explicitly.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
