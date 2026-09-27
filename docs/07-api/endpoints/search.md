---
document_id: DOC-API-010
title: API-SRC — Search & Discovery (FR-009)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-009, FR-004, FR-005, FR-019, NFR-001, NFR-004, NFR-007, NFR-013, BR-CAT-03, BR-CAT-06, BR-PLT-01, BR-PLT-02]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-009, DOC-BA-005, DOC-OVR-008]
---

# API-SRC — Search & Discovery

**Group:** `API-SRC` · **FR-009** · **Endpoints:** `API-SRC-001…003` · **Base:** `/api/v1`

Arabic-aware full-text search over Elasticsearch (`DEP-04`): alef/ya/ta-marbuta normalization and diacritic handling server-side, bilingual indexed fields, filters, facets, and 5 sort modes. Only ACTIVE, non-deleted products of in-stock availability appear (`BR-CAT-06`, FR-005). Response shape is fixed by `pagination.md` §6.

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-SRC-001 | `GET /search/products` | Public | Full-text product search with filters, sort, facets, highlights (cursor feed) | `?q&category&store&priceMin&priceMax&ratingMin&inStock&sort&limit&cursor` → `200 { items: [ { …product, highlights: { nameEn, description } } ], page: { limit, nextCursor, hasMore, total: { value, relation } }, facets: { category[], price[], store[], rating[], inStock[] }, meta: { query, tookMs, degraded, locale } }` — `sort ∈ relevance\|price_asc\|price_desc\|newest\|rating` | `QUERY_TOO_SHORT`, `FACET_INVALID`, `VALIDATION_ERROR`, `SEARCH_UNAVAILABLE`, `NOT_FOUND` (bad cursor) | FR-009, `C-24`, `BR-CAT-06`, `pagination.md` §6, `AC-FR009-01/04` |
| API-SRC-002 | `GET /search/facets` | Public | Facet counts for the current query/filters **without** returning items — powers the filter sidebar without refetching the list | `?q&category&store&priceMin&priceMax&ratingMin&inStock` → `200 { facets: { …same keys as API-SRC-001 }, meta: { tookMs, degraded } }` — counts computed in the same filter context as the result list | `FACET_INVALID`, `VALIDATION_ERROR`, `SEARCH_UNAVAILABLE` | FR-009, `NFR-004`, `AC-FR009-04` |
| API-SRC-003 | `GET /search/suggest` | Public | Typeahead suggestions (products, categories, stores) | `?q&limit≤10` → `200 { suggestions: [ { text, type: "product"\|"category"\|"store", slug, count? } ], meta: { tookMs, degraded } }` — prefix-oriented, Arabic-normalized, no facets/cursor | `QUERY_TOO_SHORT`, `VALIDATION_ERROR`, `SEARCH_UNAVAILABLE` | FR-009, `NFR-001` |

## 2. Behavior Notes

- **Zero-result behavior** (`200 with empty `items``): the response still includes `facets` (so the UI can offer "relax filters") plus `meta.didYouMean` — the best suggestion from the suggest endpoint — and `meta.popularCategories` (top 5 by product count) as fallback navigation. Zero results are **never** an error status.
- **Degradation** (`NFR-007`): if Elasticsearch is unreachable the gateway attempts a cached-query replay for `relevance`/`newest` sorts and sets `meta.degraded = true`; when no cached answer exists the endpoint returns **503 `SEARCH_UNAVAILABLE`** and clients fall back to category browse (`GET /categories/{slug}`, `API-CAT-002`) — browsing never depends on ES.
- **Index synchronization** (`BR-PLT-01/02`): catalog writes enqueue `b02.product.index` jobs (3 retries, exponential backoff, DLQ alert) — freshness is eventually consistent; `newest` sort reflects index time.
- **Arabic analysis** (`C-24`, `AC-FR009-01`): `q` is passed verbatim; normalization (variant letters, diacritics, stemming) happens in the ES analyzer — clients must not pre-normalize or transliterate.
- **Visibility**: `BR-CAT-06` ACTIVE-only and `BR-VND-04` suspended-store exclusion are enforced at index time **and** re-checked at query time (belt-and-braces for `AC-FR009-02`).
- **Performance** (`NFR-001`, `C-25`): p95 < 200 ms at 10,000 concurrent users; aggregations cached in Redis keyed by `(query, filters, locale)` for ≥ 80% hit ratio (`NFR-004`).
- **Merchandising injection** (`FR-019`): featured/deal banners sourced from CMS are **not** part of the search response — clients fetch them from `GET /home` / `GET /promotions` (`content.md`) and render above/beside results.
- **Search analytics events**: FR-018 covers dashboards/reports over order, finance and operations data — it does **not** specify behavioral event tracking (search clicks, query logs). No search-analytics endpoint exists in v1; queries are retained only as privacy-minimized server logs for relevance tuning (`DATA-REQ-002`).

## 3. Pagination / Idempotency / Caching

All three endpoints are GETs (side-effect free, idempotent). `API-SRC-001` uses **cursor** pagination (default 24, max 50); `API-SRC-002/003` are single-shot. `Cache-Control: max-age=30` on suggest/facets; search results may be cached only when `sort=newest` and no user context is present.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
