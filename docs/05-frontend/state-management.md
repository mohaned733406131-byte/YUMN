---
document_id: DOC-FE-004
title: State Management — Server State, UI State & Cart Strategy
category: 05-frontend
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-010, FR-011, FR-012, FR-013, NFR-001, NFR-002, NFR-004, SEC-REQ-003]
related_documents: [DOC-FE-001, DOC-FE-002, DOC-FE-006, DOC-BA-005]
---

# State Management — Server State, UI State & Cart Strategy

**Two-state model:** server state is owned by **TanStack Query (React Query)**; ephemeral UI state is owned by **Zustand**. No global "app store" holds domain data — wallet, orders and stock are always server-derived.

---

## 1. State Taxonomy

| Category | Examples | Owner | Persistence | Freshness rule |
|---|---|---|---|---|
| **Server state** | product pages, order lists, wallet balance, addresses, notifications | TanStack Query | query cache (memory; optional `sessionStorage` for restore-on-reload of non-sensitive lists) | staleTime per resource (§3) |
| **Session/auth state** | access token, user profile, roles, session list | Auth context fed by `api-sdk` | access token in **memory only**; refresh via httpOnly cookie (DOC-FE-006) | refreshed silently at 15-min expiry (`C-08`) |
| **Cart state** | items, quantities, reservation deadline, totals snapshot | Zustand cart slice + server reconciliation | `localStorage` (guest) → merged to server on login (`BR-CRT-03`) | server totals authoritative at every step (`BR-CRT-04`) |
| **UI state** | modals, active tab, form drafts, filters, toasts, step index | Zustand slices / local `useState` | memory (form drafts may use `sessionStorage`) | irrelevant to server |
| **Ephemeral server-derived UI** | OTP cooldown timers, countdown to reservation expiry | local component state driven by server timestamps | memory | server timestamp + local clock drift correction |

**Forbidden in client state:** computed money totals used for payment, "authoritative" order status, permission decisions beyond UX mirroring.

## 2. TanStack Query Policy

| Aspect | Policy |
|---|---|
| Query keys | hierarchical factory: `['products', slug]`, `['orders', { status, page }]`, `['wallet', 'balance']` — enables prefix invalidation |
| Defaults | `staleTime` 30 s for catalog; 0 for wallet/orders/status; `retry: 1` except network errors |
| Mutations | always invalidate the owning key list on success; never mutate cache optimistically for money/order data (§6) |
| Pagination | infinite query for search/order lists; cursor from API (`07-api` pagination conventions) |
| Prefetch | ISR pages prefetch below-the-fold queries (reviews, variants); dashboards prefetch on row hover |
| Error handling | normalized API errors surface through the shared error mapper (DOC-FE-005 §5); 401 triggers the refresh interceptor, not a toast |
| Polling | order detail & courier queue poll at 10–15 s while tab visible, paused when hidden (`NFR-002` battery/CPU) |
| SSR | Next.js: cache hydration via `HydrationBoundary`; only public catalog queries are hydrated server-side |

### Stale-time table (defaults)

| Resource | staleTime | Reason |
|---|---|---|
| Category tree, CMS pages | 5 min | changes rarely; server invalidates on publish |
| Product detail (price display) | 60 s | display-only; checkout revalidates (`BR-CRT-04`) |
| Search results | 30 s | volatile, facet-driven |
| Cart | 15 s + reservation countdown from server | 15-minute TTL (`C-13`) |
| Order list/detail | 0 s | state machine moves server-side (`C-09`) |
| Wallet balance | 0 s | never cached across navigation (`DOC-BE-007` non-cacheable) |
| Notifications inbox | 30 s, refetch on push receipt | push-driven invalidation (FR-017) |

## 3. Zustand Slices

| Slice | Holds | Reset triggers |
|---|---|---|
| `auth` | user profile, roles, in-memory access token | logout, session revoked, refresh-family revocation (BR-AUTH-05) |
| `cart` | items, per-store grouping, reservation deadline, guest id | checkout success, merge completion, TTL expiry |
| `checkout` | 7-step wizard index, selected address/shipping/payment drafts | order placed, abandon > TTL |
| `ui` | drawers, locale switch, toasts, filter panel state | navigation (per-route reset) |
| `search` | query text, facets, sort (mirrors URL — URL wins on load) | URL change |

Rules: slices contain **no business rules** — the cart slice enforces C-15 *pre-feedback only* (disable + message), server enforces authoritatively (`DOC-BE-009`).

## 4. Cart State — Guest Sync & Merge (`FR-010`, `BR-CRT-01…06`)

```text
Guest adds item ──► Zustand cart + localStorage (guestId)
        │
Login/Register success
        │
POST /cart/merge (idempotency key) ──► server merges guest cart into user cart
        │                                conflict → server quantity wins (BR-CRT-03)
        ▼
Server cart becomes source of truth; local guest cart cleared
        │
Every add/qty change ──► mutation → server response replaces local cart
        │                  (client pre-checks C-15 limits for instant feedback)
        ▼
Checkout entry ──► server revalidation (items active? in stock? price changed?)
```

| Concern | Client behavior | Server behavior (authoritative) |
|---|---|---|
| Limits (≤50 products, ≤10 units/product, ≤5 vendors — `C-15`) | block + localized message at add-time | rejects with `LIMIT_EXCEEDED` (DOC-BE-009) |
| 15-min reservation countdown (`C-13`, `BR-CRT-02`) | countdown from server-provided deadline; on 0 → refetch cart, mark items released | TTL expiry job releases stock (DOC-BE-006) |
| Price change since add (`BR-CRT-04`) | show delta banner, require re-confirm | recalculates at checkout regardless |
| Inactive/OOS item (`BR-CRT-05`) | highlight + "remove to continue" | blocks order creation |
| Wallet balance < total (`BR-CRT-06`) | show shortfall in review step | rejects at confirmation |
| Merge conflicts (`BR-CRT-03`) | display merged result | server value wins |

Cart state is **never** ISR/SSR-cached and is cleared on logout (guest carts survive; user carts remain server-side).

## 5. Session Refresh Handling (15-min access token, `C-08`)

| Step | Behavior |
|---|---|
| Storage | access token in memory (module scope); refresh token in httpOnly cookie set by server — nothing in `localStorage` (`SEC-REQ-003`) |
| Proactive refresh | `api-sdk` schedules refresh at ~80% of TTL (≈12 min) when the tab is active |
| Reactive refresh | on `401 TOKEN_EXPIRED`, single-flight refresh promise — all concurrent requests await it, then retry once |
| Refresh failure | auth slice cleared; user stays on route; next guarded action prompts re-login (DOC-FE-003 §9) |
| Rotation | each refresh response replaces in-memory access token; server rotates the refresh cookie (single-use, `BR-AUTH-05`) |
| Reuse detection (alert) | server revokes the session family → next request 401 → client shows "session ended on another device" toast + login |
| Multi-tab (web) | one tab refreshes and shares the new access token via `BroadcastChannel`; avoids rotation races |
| RN | same interceptor; token persisted in Keychain/Keystore-backed storage (encrypted), never plaintext (`SEC-REQ-006`) |

## 6. Optimistic Updates — Allowed vs Forbidden

| Interaction | Optimistic? | Rationale |
|---|---|---|
| Wishlist add/remove, store follow | **Allowed** | reversible, no money impact; roll back on error |
| Cart quantity increment (pre-limit) | **Allowed with rollback** | must roll back to server truth on `LIMIT_EXCEEDED` |
| Review draft, notification prefs, profile fields | **Allowed** | cosmetic, revalidated server-side |
| **Wallet balance / top-up** | **Forbidden** | money display must never be locally invented (`BR-PAY-05`, `BR-PAY-06`) |
| **Order placement / cancellation** | **Forbidden** | idempotent server transaction is the only truth (`BR-ORD-06`, `BR-PLT-04`) |
| **Order state changes** | **Forbidden** | 17-state machine guarded server-side; invalid transition = `409 STATE_CONFLICT` (`03-system-analysis/state-transitions.md`) |
| **Refund / return status** | **Forbidden** | financial + SLA-driven (BR-RET-04, BR-RET-05) |
| **Stock availability** | **Forbidden** | atomic reservation server-side (`BR-CAT-07`) |

Pattern for allowed cases: `mutationFn` → `onMutate` (cancel queries, snapshot, patch) → `onError` (restore snapshot + toast) → `onSettled` (invalidate).

## 7. Cross-Surface State Rules

| Surface | Notes |
|---|---|
| web-customer | cart + checkout slices persist across route changes; cleared on locale switch? No — locale-independent |
| web-vendor / web-admin | filters & tables URL-synced (shareable, back-button correct); no client-side copies of order/wallet data beyond query cache |
| mobile apps | same query keys as web (shared `api-sdk`); cart persists in device storage for offline viewing, revalidated on foreground |
| all | logout clears query cache (`queryClient.clear()`) + auth slice; sensitive screens are excluded from app-switcher snapshots on RN |

## 8. Verification

- Unit tests: cart merge conflict resolution (server wins), limit pre-check, optimistic rollback.
- Integration: silent refresh under 8 concurrent requests results in exactly one refresh call (single-flight).
- Negative tests: no code path writes a refresh token to `localStorage`/`sessionStorage` (static scan).
- E2E (`13-testing/`): guest cart → login → merged cart → checkout; wallet balance never changes before server response.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
