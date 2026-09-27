---
document_id: DOC-WF-003
title: "WF-002 — Search → PDP → Add to Cart (guest gating)"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-004, FR-009, FR-010]
related_documents: [DOC-WF-001, DOC-BA-005, DOC-OVR-008]
---

# WF-002 — Search → PDP → Add to Cart (guest gating)

| Field | Value |
|---|---|
| **Trigger** | User (guest or registered) opens the storefront or submits a search query |
| **Actors** | Customer as guest or registered (`ACT-01`), System (`ACT-07` — search index, reservation timers) |
| **Blocks** | B04 Search & Discovery · B02 Product Catalog · B05 Cart |
| **Preconditions** | Product data indexed; at least one ACTIVE product exists (bootstrap: empty-state UI) |
| **Final state** | Cart holds validated lines with a live 15-minute reservation countdown, ready for checkout (WF-003) |

```text
[Search query / category browse / banner tap]
      │
      ▼
Arabic-aware search + filters + sort ──► results (ACTIVE products only, BR-CAT-06)
      │ no results                              │
      ▼                                         ▼
✗ EMPTY STATE (refine query)          [Open PDP: price, stock, images, store, return policy]
                                                  │
                                        sold out / inactive / non-shippable
                                                  ▼
                                          ✗ BUY DISABLED (BR-CAT-07, BR-CRT-05)
                                                  │ available
                                                  ▼
                                     [Add to cart] ── guest? ──► client-side cart (BR-CRT-03)
                                                  │                    │ login later
                                                  │ registered         ▼
                                                  ▼            merge on login (server wins)
                                          server cart created
                                                  │
                                                  ▼
                                    guard check (50 / 10 / 5 — C-15) ──► ✓ reserved, 15-min countdown
                                                  │ exceed limits
                                                  ▼
                                        ✗ CART_LIMIT_EXCEEDED (BR-CRT-01)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Customer | Enter search text / pick category / filter / sort | B04 | `FR-009`, `BR-CAT-06` | query log (no PII) | No results → Arabic empty state with suggestions; search down → category browse fallback (`NFR-007`) |
| 2 | System | Return matching ACTIVE products (Arabic stemming) | B04, B02 | `BR-CAT-06`, `BR-PLT-05` | none | Inactive/soft-deleted products excluded (`BR-CAT-06`) |
| 3 | Customer | Open product detail page (PDP) | B02 | `BR-CAT-01`, `BR-CAT-04` | none | Missing publishable data → not surfaced (`BR-CAT-01`) |
| 4 | System | Evaluate buy eligibility (stock, store status, shippable) | B02, B03 | `BR-CAT-07`, `BR-VND-04` | none | Stock 0 or store suspended → add disabled (`BR-CRT-05`) |
| 5 | Guest | Add to cart (pre-login) | B05 (client) | `BR-CRT-03` | local cart state | Guest cart persists client-side only; merges on login (WF-001) |
| 6 | Registered | Add to cart | B05 | `BR-CRT-01` | cart line inserted | ≤50 products, ≤10 units/product, ≤5 vendors — violation → `CART_LIMIT_EXCEEDED` |
| 7 | System | Start/refresh 15-minute stock reservation | B02, B05 | `BR-CRT-02`, `BR-CAT-07`, `C-13` | reserved quantity, reservation expiry | Countdown restarts on each add; expiry releases reserved stock |
| 8 | System | Recompute price/stock server-side | B05 | `BR-CRT-04` | line price snapshot | Price changed since add → flagged for re-confirmation at checkout |
| 9 | Customer | Repeat or proceed to checkout (WF-003) | B05 | `BR-CRT-05` | none | Inactive/OOS/out-of-policy lines block checkout until removed |

**Alternatives**
- **Category browse without search:** same eligibility rules; banner/merchandising taps route into PDP (`FR-009`).
- **Storefront entry:** customer follows a store (`BR-VND-05`) and browses its ACTIVE products only.
- **Login mid-guest-session:** cart merges, server value wins on quantity conflict (`BR-CRT-03`).

**Exceptions**
- Reservation expiry mid-browse → reserved stock released, PDP shows fresh stock (`BR-CRT-02`).
- Concurrent oversell attempt → atomic deduction; oversell prohibited (`BR-CAT-07`).
- Search index unavailable → degrade to category browse; never block ordering (`NFR-007`).
- Prices/pricing anomalies (≤0, sale ≥ original) → product not publishable (`BR-CAT-04`).

**Rules applied:** `BR-CAT-01/04/06/07`, `BR-CRT-01…05`, `BR-VND-04/05/07`, `BR-PLT-05` · Constraints: `C-13`, `C-15`, `C-24` · Non-functional: `NFR-007`, `NFR-012`.

**Data touched:** product search index, products/variants/stock, reservations (15-min TTL), cart lines (guest local / server), price snapshots, browse logs.

**Systems:** B04 Search & Discovery · B02 Product Catalog · B05 Cart & Checkout · B03 Store Management (suspension state) · B10 Notifications (optional back-in-stock later — v1 signals only via catalog refresh).

**Final state:** cart populated within all guards, each line reserved with an active 15-minute countdown; guest carts remain client-side until login merges them.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
