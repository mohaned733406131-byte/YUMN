# plan-develop — Development, Enhancement & Expansion Plan (v1 → comprehensive platform)

> **Status:** ✅ **APPROVED 2026-09-28 (administrator) — authorized for implementation at the
> analysis layer** under [`docs/README.md`](docs/README.md) §9 change control. Approval covers the
> §8 recommendations `D1`…`D11` as written (see §8 Outcome column); items the plan itself routes to
> external review (`CT-23`, `CT-26`, `CT-27`, `CT-28`, `GAP-14`, `DEP-05/09`, `ASM-14`) remain
> **OPEN** — approval does not fabricate the evidence those gates require (`GEN-03`, `DOD-10`).
> **Author role:** Development & Planning Manager / Requirements Engineer / Business Analyst.
> **Date:** 2026-09-28 · **Session:** 007 · **Rules pin:** ADMR `2.2.0` + `YUMN_RULES.md` (94 rules).
> **Method:** approved knowledge base (24 domains, 73 requirements, 221 endpoints, 114 test cases)
> compared against (a) external multi-vendor platform / ERP research (§9 sources), and (b) the
> sponsor-provided platform specification [`describ.md`](describ.md) (registered as `CT-23`…`CT-30` /
> `GAP-13` / `GAP-14` in [`docs/20-validation/`](docs/20-validation/README.md)).

---

## 0. How to read this document (scope, honesty and ID rules)

1. **There is no running system yet.** `C-23` (greenfield) and [`development_phases_entry.md`](development_phases_entry.md)
   are explicit: Phase 0 (analysis) is COMPLETE, Phase 1 (bootstrap) is NOT STARTED, Gate 0 is `FAIL`.
   Therefore "existing system features" in §1 means **the features already specified and approved in the
   v1 knowledge base** (the 20 functional requirements `FR-001…FR-020`, 13 blocks `B01…B13`, 221 API
   endpoints, 18 registered entities). Nothing in `docs/` is `VERIFIED` (`SPE-03`).
2. **Every proposal is checked against `C-01…C-26`** ([`project-constraints.md`](docs/00-project-overview/project-constraints.md)).
   Proposals that need a constraint amended are marked **`CHG`** and route through sponsor change
   control — they are *requests*, not assumptions. The five absolute prohibitions
   ([`RULES_HINTS.md`](senior-rules/RULES_HINTS.md) §7) are never traded for feature speed.
3. **Priority definitions** used in §1 and everywhere below:
   - **HIGH** — blocks Gate 0 / the money path / statutory compliance, or is a sponsor decision that
     unlocks a whole cluster of work. Resolve before (or at the start of) Phase 1 build.
   - **MEDIUM** — required for a complete, credible v1 marketplace. Build inside Phase 1–2.
   - **LOW** — competitive/quality polish. Phase 2 or post-launch backlog (never silently promoted
     into v1 — `project-scope.md` §Scope-creep control).
4. **ID policy:** `C-*`, `FR-*`, `BR-*`, `GAP-*`, `CT-*`, `CRIT-*`, `REC-*`, `TD-*`, `SEC-*`,
   `API-*`, `DB-*`, `UC-*`, `BP-*`, `ACT-*`, `B0x` cited below are existing corpus IDs. New proposals
   carry **document-local IDs `M-nn` (modification), `P-nn` (proposed feature), `ORG-nn` (admin org),
   `ROLE-nn` (role)** — minted into their owning registers only after approval. **Minted 2026-09-28:**
   `ORG-01`…`ORG-08` and `ROLE-01`…`ROLE-07`/`ROLE-09` now live in
   [`rbac.md`](docs/09-security/core/rbac.md) §11 (`ROLE-08`/`ROLE-10`/`ROLE-11` stay document-local —
   their conditions are unmet); `M-nn`/`P-nn` convert to `FR-*` + ACs at their build wave
   (never earlier — `SPE-03`/`D-02` discipline).
5. **Evidence tags:** `VERIFIED` = confirmed in a cited corpus file this session · `INFERENCE` =
   reasoned from sources but not yet ratified · `INSUFFICIENT EVIDENCE` = needs a sponsor/owner answer.

---

## 1. Existing system features requiring modification or enhancement

### 1.1 HIGH priority

| # | Feature (spec ref) | Modification / enhancement required | Justification |
|---|---|---|---|
| `M-01` | **Wallet & account model** — `FR-013`, `DB-010 wallet`, `DB-011 wallet_transaction` | Add **multi-currency sub-accounts + platform-managed FX rate** *only if* the sponsor amends `C-04`; includes rate table, cross-currency posting type, FX gain/loss leg, statement rendering | Sponsor spec [`describ.md`](describ.md) §1/§3/§6 vs `C-04` "YER only, no USD/SAR wallets in v1" → `CT-23` (`HIGH`, `OPEN`), `GAP-13` + `GAP-14`. `VERIFIED` in [`contradiction-audit.md`](docs/20-validation/core/contradiction-audit.md). Money-path change ⇒ ADR + ledger design review (`RISK-001`) |
| `M-02` | **Top-up rails** — `FR-013`, `C-05`, `INT-REQ-001` | Register **Al-Kuraimi** and **Jeeb** as additional wallet providers behind the existing `PaymentProviderPort`; provider PIN verification callback, webhook signature, degradation matrix update | Sponsor spec §2.1 vs `C-05` fixed set (m-Floos, OneCash, bank transfer) → `CT-24` (`HIGH`, `OPEN`); also enlarges `DEP-05` (NOT STARTED, Gate-0 blocker) and needs `GAP-10` API specs. Bank-transfer half already agrees (`BR-PAY-04`, `UC-034`) |
| `M-03` | **Authentication** — `FR-001`, `C-06`, `SEC-REQ-001` | Make **email an optional, verified secondary identifier** (login + password reset), phone stays mandatory and remains the OTP factor; never an email-primary path | Sponsor spec §7 vs `C-06` "Phone + OTP only, no email-primary auth" → `CT-25` (`HIGH`, `OPEN`, `GAP-13`). Reduces account-takeover recovery dead-ends (`GAP-12` also touches recovery). Security impact (enumeration, reset flows) ⇒ threat-model delta required |
| `M-04` | **Escrow release rule** — `FR-014`, `C-12`, `BR-ESC-01…08`, `DB-012 escrow` | Replace/augment the fixed `release_at = DELIVERED + 7d` timer with **merchant-defined return-period hold + partial release of non-returned items** (per-line maturity, split release postings) | Sponsor spec §5 vs `C-12` (7-day hold) → `CT-26` (`HIGH`, `OPEN`). Merchant return policy itself already exists (`C-11`, `BR-RET-01`) — only the *escrow maturity* rule conflicts. Money-critical ⇒ ADR before any `b07` build (`ORD-08`-style gate) |
| `M-05` | **Wallet creation lifecycle** — `FR-013` vs [`docs/08-database/core/wallet.md`](docs/08-database/core/wallet.md) | Pick **one**: wallet row created at registration (after phone verification) *or* lazily on first top-up/order; align API, entity doc, ACs and tests | `CT-30` (`MEDIUM`, `OPEN`) — canon-internal contradiction surfaced by sponsor §1 ("registered **and verified**"); `FR-013.md` and the entity doc disagree today. Cheap to fix, expensive if built twice |
| `M-06` | **System money boundary** — `FR-013`, `system-context.md`, `BR-PAY-07` | Decide whether **peer-to-peer account funding** and **customer withdrawals to external wallets** become legal flows (new ledger posting types, limits, velocity/fraud controls, admin approval queue) — or are explicitly rejected | Sponsor §3.2 vs load-bearing principle "money never flows directly between actors" → `CT-27` (`HIGH`, `OPEN`); withdrawal vs `BR-PAY-07` → `CT-28` (`MEDIUM`, `OPEN`). If approved: re-opens AML/fraud scope, `SEC-*` controls and `AC-S-*` assertions |
| `M-07` | **Admin reach over customer money** — `FR-002`, `rbac.md` rows 15/16, `SEC-REQ-004` | Recommended disposition: **NO** direct balance read/write for anyone; replace with read-only *aggregate* finance dashboards + explicitly enumerated, audited support actions (freeze already exists: `API-ADM-033/034`) | Sponsor §4 ("operations … individually or **collectively** … any actions deemed appropriate") vs `rbac.md` deny rows + append-only ledger → `CT-29` (`HIGH`, `OPEN`) needs sponsor **and** security sign-off. `rbac.md` is `source_of_truth` |
| `M-08` | **Spec consistency on money/state enums** — `D-06`, `D-07`, `CRIT-03` | Reconcile API ↔ DB vocabularies (product status, KYC `IN_REVIEW`, top-up lifecycle, refund/payout/dispute states, ledger `type`, notification categories) and add the entities the API promises but the DB lacks (push device tokens, dispute evidence, support messages, vendor application, payout account) | `SPE-02/03/04` forbid coding against contradictory specs; `CRIT-03/07` (`HIGH`, `OPEN`) + `CT-06…CT-10`, `CT-18…CT-20` all `OPEN`. Must close **before** schema freeze in Phase 1 — otherwise migration churn on money tables |
| `M-09` | **FR ↔ acceptance-criteria text** — `FR-015…FR-020` | Finish the `D-02` reconciliation: the registry (`acceptance-criteria.md`) and the six FR files still diverge in wording/renumbering even though the 94 `-05` references were added | `CRIT-05` (`HIGH`, `OPEN`), `HAL-05`, `RVF-04`; ACs are the contractual test basis (273 ACs) — drift here silently invalidates Gate 1 check 1.3 |
| `M-10` | **Order state precedence** — `C-09`, `state-transitions.md` | ADR defining `COMPLETED → RETURN_REQUESTED` vs `COMPLETED → DISPUTED` precedence and the resulting fund outcome | `D-12` (`HIGH`, `OPEN`), rule `ORD-08`. One master order + one sub-order per vendor (`C-10`) makes the race money-affecting; must precede `b06` implementation |
| `M-11` | **Security design hardening** — `SEC-001…SEC-015` (all `OPEN`) | Close the design-level findings that change shipped behaviour: step-up re-authentication for privileged/money actions (`SEC-012`, `HIGH`), admin console same-origin/CSRF posture (`SEC-003`), plus the `SEC-C-*` control deltas they imply | Gate 1 check 1.7 requires **0 open CRITICAL/HIGH** security findings; `SEC-REQ-004/010` depend on them. Cheapest to fix in design now, most expensive after build |
| `M-12` | **Notification scope** — `FR-017`, `DB-017`, `GAP-03` | Decide the **email channel** (in or out of v1); if in: template family, preference centre row, provider adapter, deliverability ops. If out: strike every email claim | `GAP-03` (`OPEN`, Gate-0 check 0.5). Today the canon is "4 channels, no email v1" but the question was never dispositioned — an undecided scope item this close to build is a defect risk |

### 1.2 MEDIUM priority

| # | Feature (spec ref) | Modification / enhancement required | Justification |
|---|---|---|---|
| `M-13` | **Admin console & settings** — `FR-020`, `API-ADM-001…043` | Expand the settings model (5 groups today → full taxonomy §5), add department/scoped-staff navigation, feature-flag console, bulk actions, saved views | Benchmark platforms (CS-Cart, Sharetribe, Mirakl-class operators) all ship deep operator consoles; yumn's 43 admin endpoints cover **operations** but not **platform administration** (no flag API, no department model — `department` appears in **0** corpus files, `VERIFIED`). Detail in §5 |
| `M-14` | **RBAC / staff model** — `FR-002`, `rbac.md` §8 | Add scoped admin **staff profiles** (permission bundles per department) while preserving the 7-actor canonical mapping (API 7 = enum 10 − 3 staff; DB 6 = 7 − `SYSTEM`) | Today `ADMIN` is one flat role doing KYC + refunds + moderation + settings-lite. Real platform teams need separation of duties (four-eyes on money ops) — benchmark-standard and required for `M-07`/§5/§6 |
| `M-15` | **Vendor finance surface** — `BR-FIN-04`, `API-ANL-004/005`, `API-WAL-013` | Upgrade monthly statements to **document-grade artefacts**: numbered invoices/settlement documents, PDF, tax fields, payout receipts, downloadable tax summary | Statements exist (`VERIFIED`), but no invoicing document exists anywhere in the corpus (`invoice` ≈ 6 incidental hits; BP-01…BP-15 contain **no** accounting/invoicing process). Yemen tax invoicing is asserted in `project-context.md` while `ASM-10` (VAT liability) is `UNSUPPORTED` (`DEP-09`) |
| `M-16` | **Delivery providers** — `FR-015`, `INT-REQ-005`, `DeliveryProviderPort` | Add a **delivery-provider (fleet/partner) registry**: partner record, service areas, rate cards, contracts, settlement runs, SLA metrics — couriers can stay individual in v1 | `GAP-07` (`OPEN`, owned via `RISK-018`) + benchmark: operator-run marketplaces manage carriers as counterparties, not just as freelancers. Port already exists, so this is domain + admin surface, not new architecture |
| `M-17` | **Wishlist route** — [`routing.md`](docs/05-frontend/core/routing.md) §, [`information-architecture.md`](docs/11-ui-ux/core/information-architecture.md) | **Decide**: implement the saved-products list (small: `b01` relation + 3 endpoints + 2 screens) **or** delete the `/account/wishlist` route | The route and IA row cite `FR-008`/`BR-VND-05`, which only define *store following*; `FR-010.md` explicitly excludes "persistent wishlists … not specified in v1". Today it is a **candidate dead element** (`DOD-05`/`IMP-02` — 0 dead routes is a hard gate) |
| `M-18` | **Technical SEO pack** — `FR-009`, `frontend-architecture.md` | Generate `sitemap.xml`, `robots.txt`, canonical/hreflang already designed, product & breadcrumb structured data, search-console verification | ISR/SEO-friendly slugs and `hreflang` exist (`VERIFIED`), but no crawler entry-point artefacts are specified (only IA "sitemap" = navigation). Cheap, high discovery value in a marketplace |
| `M-19` | **Promotions calendar** — `FR-019`, `DB-016 coupon` | Add scheduling/period targeting for banners + coupons, campaign calendar view, per-store promotion windows | Coupons (`≤90%`, non-stackable) and banners exist; benchmark operators run *scheduled campaigns*, not hand-toggled banners. No new money semantics (stays inside `B12`) |
| `M-20` | **Review & moderation quality** — `FR-006`, `API-ADM-027…029` | Vendor right-of-reply workflow on hidden reviews, evidence attachments on reports, auto-flag heuristics tuning | Moderation queue/hide/restore exist; the *governance* around them (response, escalation, false-positive rate) is thin vs benchmark and vs `BR-REV-*` expectations |
| `M-21` | **Search & discovery analytics** — `FR-009`/`FR-018` | Zero-result search terms, filter usage, conversion by query — surfaced to admin + vendor | `search.md` explicitly notes search behavioural events are **not** covered by `FR-018` (`VERIFIED`). Needed to operate merchandising; reads only, no PII export beyond existing rules |

### 1.3 LOW priority

| # | Feature (spec ref) | Modification / enhancement required | Justification |
|---|---|---|---|
| `M-22` | **Customer engagement depth** — `FR-017` | Rich notification segmentation (category digests), quiet hours, per-store muted follow alerts | In-app inbox/preferences exist; depth is a retention lever, not a launch gate. Must respect `BR-NTF-*` (transactional-only today) |
| `M-23` | **PWA / offline shell** — `05-frontend` | PWA manifest, offline browsing of previously visited catalog | Listed as FUTURE SCOPE in `project-scope.md`; low because mobile apps (`apps/mobile-customer`) are the primary companion surface |
| `M-24` | **Analytics depth** — `FR-018` | Cohorts, funnel, LTV-by-vendor, marketing attribution | Attribution is an explicit FR-018 exclusion today; keep parked unless scope-creep control approves |
| `M-25` | **Cart abandonment follow-up** | Decide (recommended: **keep out of scope**) | The sweeper (`cart.status → ABANDONED`, reservation release) already exists; *marketing* reminders are excluded by `FR-010.md` (notifications are transactional). Record the decision so the exclusion stops being re-litigated |

---

## 2. Missing features — how to implement, what they do, why they matter

> Priority: **H** = HIGH, **M** = MEDIUM, **L** (LOW). Conditional items carry the decision that gates them.

### 2.1 Finance, accounting & invoicing (the ERP core)

**`P-01` — Invoicing engine (customer invoices, credit notes, platform fee invoices) · H**
- *Functionality:* numbered, immutable invoice documents generated from orders/payments; Arabic-first
  PDF with tax breakdown (VAT 15% per `BR-FIN-01`, shipping untaxed), invoice series/numbering,
  credit notes for refunds/cancellations, invoice register + resend/download, customer & vendor copies.
- *Implementation:* new domain inside `B07`/`B13` area — `invoice` table (series, number unique,
  order/sub-order FK, money in integer YER, VAT breakdown, hash for tamper evidence), generation via
  BullMQ job on payment/refund events (queue naming `{block}.{entity}.{action}`, register row added),
  PDF renderer in a worker (never in request path — `F10`), `GET/POST` endpoints under
  `/api/v1/...` following [`api-conventions.md`](docs/07-api/core/api-conventions.md), audit on issue/void.
  Ledger postings stay exclusively in `LedgerService.post` (`F7`).
- *Importance:* invoices are the legal artefact of every transaction; today the platform moves money
  with **no** invoice document anywhere in the spec. Required before real merchants onboard.
- *Constraint check:* none violated; tax *policy* awaits `DEP-09`/`ASM-10` (VAT opinion).

**`P-02` — Accounting sub-ledger → general-ledger bridge (chart of accounts, journal export) · H**
- *Functionality:* map every ledger posting type to a chart-of-accounts code; produce daily journal
  batches, trial balance, P&L and balance-sheet-ready exports; month-end close checklist; immutable
  link from any report row back to ledger entries.
- *Implementation:* read-side only — a `posting → account mapping` table (config-driven, versioned),
  nightly batch job alongside existing reconciliation jobs (`J1` balance-vs-ledger, `J2` global
  invariant, both **0 tolerance**) plus a new export job; CSV/JSON outbox for the ERP connector (§4).
  No second writer of money.
- *Importance:* turns the double-entry ledger (`BR-PAY-06`, `NFR-008`) into something an accountant
  can sign off; prerequisite for Gate-2 money-cycle evidence and for any external ERP.

**`P-03` — Tax reporting workspace (VAT return, withheld/collected, per-store tax summary) · H**
- *Functionality:* VAT 15% collected per order (`BR-FIN-01`), periodic return report, taxable-base
  reconciliation vs ledger, per-vendor tax summaries, export for filing.
- *Implementation:* aggregations over orders/payments/refunds (read models in `B11`), report families
  added to `API-ANL-007/008` pattern, exports share the existing CSV rules (UTF-8 BOM, 50k cap).
- *Importance:* Yemen VAT position is asserted but unsupported (`ASM-10`, `DEP-09` `OPEN`); a
  marketplace that cannot produce a VAT return cannot operate legally.

**`P-04` — Settlement & payout automation upgrade · M**
- *Functionality:* payout request → eligibility (KYC, min 1,000 YER, 3–7 business days) → batch →
  execution → receipt, with vendor-facing status, retry queue for failed legs, and reconciliation of
  each payout batch against provider statements.
- *Implementation:* extends the existing `PayoutModule` (`buildBatch/execute`) + `b07` payout tables;
  add a settlement-run entity, admin approval workflow (four-eyes under §5 departments), webhook
  confirmations idempotent by payout ID.
- *Importance:* benchmark platforms sell *automatic, transparent payouts*; yumn's rules already define
  the policy (`BR-ESC-05/06`) — the operational machinery and receipts are what's missing.

**`P-05` — ERP connector (see §4 for full design) · M (foundation H, full connector M)**

### 2.2 Merchants / vendors

**`P-06` — Vendor plans & contract management · M (conditional `GAP-05`)**
- *Functionality:* plan/tier definitions (commission 5–20% default 10% stays the base rule), signed
  agreement records with version history, plan-driven limits (SKU caps, category access), plan billing.
- *Implementation:* `plan` + `vendor_agreement` tables in `b03`, plan resolution alongside the
  commission-tier lookup (settings `COMMISSION` group), admin + vendor read surfaces, audit on change.
- *Importance:* monetization beyond commission is the standard second revenue lever; explicitly an
  `OPEN` gap (`GAP-05`, Gate-2 check 2.5) — **do not build until Finance answers**.

**`P-07` — Bulk catalog import/export (CSV/XML) for vendors · M**
- *Functionality:* downloadable template, validate → dry-run diff → commit, error report per row,
  bulk price/stock updates, image URL import; admin-side export of full catalog.
- *Implementation:* worker job (queue row + register update), streaming parser with row caps,
  partial-failure report stored per import run, permissions under vendor `Editor/Manager`.
- *Importance:* the single biggest onboarding-time lever — CS-Cart-style platforms treat vendor import
  as table stakes; `OBJ-06` wants first listing fast.

**`P-08` — Vendor performance & SLA scorecard · M**
- *Functionality:* on-time dispatch, delivery first-attempt success, return/dispute rate, response
  times, rating trend, ranking impact; admin view across all vendors with export.
- *Implementation:* read models in `B11` from order/shipment/return history; no new money data.
- *Importance:* marketplace quality governance (benchmark-standard); supports `OBJ-07` and the
  moderation tools in `M-20`.

### 2.3 Delivery / logistics

**`P-09` — Delivery provider (fleet) registry & settlement · M (`GAP-07`)**
- *Functionality:* provider onboarding (org record, contacts, service areas, rate card, contract),
  assignment policy (first-accept stays for individuals; provider-level assignment for partners),
  provider settlements, per-provider SLA dashboard.
- *Implementation:* new entity set in `b08`, admin endpoints beside `API-ADM` finance/logistics
  groups, `DeliveryProviderPort` gains a provider-scoped adapter (already the designed extension
  point, `INT-REQ-005`); internal fleet remains the default engine in v1.
- *Importance:* required to answer `GAP-07`/`RISK-018` before volume grows; keeps GPS prohibition
  intact (`C-16` — no coordinates anywhere).

**`P-10` — Delivery operations console additions · M**
- *Functionality:* dispatch board (zones, load, courier availability), code-attempt exception queue
  (3 attempts → 24 h lock + auto ticket already exists), delivery-code admin override (`GAP-02`
  decision), proof-of-delivery evidence gallery (photo captured by courier app, no geotag).
- *Implementation:* extends `B08` + admin endpoints; overrides are `ADMIN`-only and audited; photo
  storage via MinIO with moderation hooks.
- *Importance:* operational control is the difference between a demo and a running marketplace.

### 2.4 Customer experience

**`P-11` — Saved products / wishlist · M (paired with `M-17`)**
- *Functionality:* save/unsave from product card & PDP, saved list screen, price/stock-change notice
  (transactional), one-tap move to cart.
- *Implementation:* `b01` relation table + 3 endpoints + 2 screens; optimistic UI allowed (reversible,
  no money impact — `frontend` rules already whitelist wishlist-class mutations).
- *Importance:* conversion feature present in essentially every benchmark storefront; today it exists
  only as a **route with no requirement** — implement it or delete the route.

**`P-12` — Buy-again / reorder · L**
- *Functionality:* "reorder" from order history re-validates the previous basket (price/stock changes
  surfaced like `GET /cart/checkout-view`), drops unavailable lines, goes through normal checkout.
- *Implementation:* pure composition of existing cart/checkout APIs; no new domain state.
- *Importance:* repeat-purchase lever supporting `BO-02`; zero risk to money semantics.

**`P-13` — Back-in-stock notifications (opt-in) · L**
- *Functionality:* subscribe on out-of-stock product/variant; single-shot notification when available.
- *Implementation:* subscription table in `b02`/`b10`, inventory job emits event on stock increase,
  fan-out through the existing notification pipeline (transactional category, preferences respected).
- *Importance:* recovers demand without marketing automation (keeps `FR-017` transactional stance).

### 2.5 Platform governance & operations

**`P-14` — Feature-flag console (admin API + UI) · M**
- *Functionality:* list flags with defaults/current value/source, toggle with mandatory reason,
  immediate audit entry, environment label, "never flagged" guard list enforced server-side.
- *Implementation:* the design already exists — `platform.feature_flag` durable table + Redis cache,
  fail-closed defaults, audit on change ([`configuration.md`](docs/14-devops-infrastructure/core/configuration.md) §4);
  what is missing is the **API/UI surface** (`API-ADM` has no flag endpoint — `VERIFIED`). SUPER_ADMIN only.
- *Importance:* safe progressive delivery for the new features in this plan; already paid-down as
  `TD-01`/`REC-10` at the *register* level, so only the control plane remains.

**`P-15` — Support & trust operations tooling · M**
- *Functionality:* ticket SLA timers + breach dashboard, canned responses, macros, CSAT prompt,
  bulk moderation actions with per-item reason, evidence vault (dispute/upload files — also closes
  parts of `D-07` storage promises).
- *Implementation:* `b13` extensions (tickets exist: `API-ADM-035…041`), storage buckets in MinIO,
  moderation bulk endpoints with one audit row per item, dashboards in `B11`.
- *Importance:* support cost scales linearly without tooling; dispute evidence is currently promised
  by the API with nowhere to store it (`CRIT-07`-class defect family).

**`P-16` — Fraud & abuse controls (non-biometric) · M**
- *Functionality:* rate limiting & velocity rules (top-up, OTP, code attempts already exist),
  device/session anomaly signals, mule-pattern detection on P2P flows (only if `M-06` approved),
  admin risk queue with manual review, rule tuning console.
- *Implementation:* Redis-backed rule engine consuming existing events; detections create review items
  (never auto-mutate money); full audit; no cookies fingerprinting beyond what policy allows, no
  biometrics (`C-07`), no location (`C-16`).
- *Importance:* wallet platforms attract abuse from day one; `SEC-*` and `RISK-001` make this a
  first-class concern, and `M-06` multiplies it.

**`P-17` — Privacy & data-rights centre · M**
- *Functionality:* account deletion request flow (promised by API per `D-07`), data export request,
  retention-policy admin view, consent/version log, DSAR audit trail.
- *Implementation:* `b01`/`b13` jobs + admin queue; retention schedules driven by
  [`docs/16-data/core/retention-and-archival.md`](docs/16-data/core/retention-and-archival.md); gated on `GAP-08`
  (Yemen retention obligations, `OPEN`).
- *Importance:* `AC-S-24` compliance pack and `GAP-08`/`GAP-11` are launch-gate items.

### 2.6 Growth (conditional / backlog)

**`P-18` — Loyalty & rewards · L (`GAP-04` decision)** — points accrual/redemption on wallet spend;
ledger-safe (points as a *separate* non-monetary balance — never mix with YER ledger). Gated by
product-owner decision; explicitly FUTURE SCOPE today.
**`P-19` — Referral / affiliate program · L** — invite codes, attribution windows, payout rules;
would touch money ⇒ needs its own ADR; keep in backlog.
**`P-20` — Sponsored placements / advertising · L** — `R3` in the business model is future revenue;
design the *slot* inventory first (banners exist), the auction/billing later.

---

## 3. Everything needed for a fully comprehensive system (consolidated checklist)

> Type: **NEW** = net-new capability · **ENH** = enhance existing spec · **CHG** = needs change control first ·
> **COND** = gated by the listed decision. Priority H/M/L as defined in §0.3.

| # | Domain | Addition | Type | Pri | Gate / condition |
|---|---|---|---|---|---|
| 1 | Money & accounts | Multi-currency sub-accounts + platform FX rate engine | CHG | H | `GAP-13` amend `C-04`; then `GAP-14` FX mechanics |
| 2 | Money & accounts | Al-Kuraimi / Jeeb top-up adapters (+ keep m-Floos/OneCash/bank) | CHG/ENH | H | `GAP-13` amend `C-05`; `DEP-05`, `GAP-10` specs |
| 3 | Money & accounts | P2P account funding + customer external withdrawal | CHG | H | `GAP-13`; new controls under `P-16` |
| 4 | Money & accounts | Escrow maturity = merchant return period + partial release | CHG | H | `GAP-13` amend `C-12`; ADR + ledger review |
| 5 | Money & accounts | Wallet-creation timing unified (`CT-30`) | ENH | H | owner decision |
| 6 | Money & accounts | Ledger → chart-of-accounts mapping + journal exports | NEW | H | §4 foundation |
| 7 | Money & accounts | Invoicing engine (invoices, credit notes, series, PDF) | NEW | H | tax opinion `DEP-09` for mandatory fields |
| 8 | Money & accounts | VAT/tax reporting workspace + return export | NEW | H | `DEP-09`/`ASM-10` |
| 9 | Money & accounts | Settlement runs, payout receipts, provider reconciliation | ENH | M | — |
| 10 | Money & accounts | Daily/monthly financial close pack (statement pack for sponsor) | NEW | M | builds on `J1/J2`, `API-ANL-009` |
| 11 | Compliance | Data-rights/DSAR centre, consent log, retention console | NEW | M | `GAP-08`, `GAP-11` |
| 12 | Compliance | Security design deltas `SEC-001…015` (step-up auth, same-origin) | ENH | H | Gate 1 check 1.7 |
| 13 | Spec integrity | Enum/entity reconciliation (`D-06`, `D-07`, `CRIT-03/07`, `CT-06…10/18…20`) | ENH | H | before schema freeze |
| 14 | Spec integrity | FR↔AC text drift closure (`D-02`, `CRIT-05`) | ENH | H | Gate 1 check 1.3 |
| 15 | Spec integrity | Order-state precedence ADR (`D-12`) | ENH | H | before `b06` |
| 16 | Admin | Department model + scoped admin staff profiles | NEW/CHG | M | §5; `rbac.md` change control |
| 17 | Admin | Settings taxonomy expansion (§5.3) + per-store override rules | ENH | M | settings registry + optimistic locking already designed |
| 18 | Admin | Feature-flag console (API + UI, audited) | NEW | M | `configuration.md` §4 already canonical |
| 19 | Admin | Bulk/batch operations, saved views, queue dashboards, exports | NEW | M | — |
| 20 | Admin | Four-eyes approval on money ops (verify/freeze/refund/payout) | NEW | M | `rbac` separation of duties |
| 21 | Admin | Audit-log explorer (filters, hash-chain verify UI, export) | ENH | M | audit API exists; chain-verify cadence `CT-21` decision |
| 22 | Vendors | Vendor plans & signed agreements | CHG/NEW | M | `GAP-05` |
| 23 | Vendors | Bulk catalog import/export | NEW | M | — |
| 24 | Vendors | Performance/SLA scorecards + admin league table | NEW | M | — |
| 25 | Vendors | Vendor-side finance upgrades (invoice copies, tax summary) | ENH | M | ties to #7 |
| 26 | Delivery | Delivery-provider (fleet) registry, rate cards, settlements | NEW | M | `GAP-07` |
| 27 | Delivery | Dispatch console, evidence gallery, code-override policy | NEW | M | `GAP-02` decision |
| 28 | Delivery | Provider SLA dashboards (on-time, first-attempt) | NEW | M | — |
| 29 | Customer | Wishlist/saved products (or delete the route) | NEW/CHG | M | `M-17` decision |
| 30 | Customer | Buy-again/reorder | NEW | L | — |
| 31 | Customer | Back-in-stock opt-in alerts | NEW | L | — |
| 32 | Customer | Order status timeline upgrade (no GPS) + delivery ETA windows | ENH | M | `C-16` intact |
| 33 | Discovery | XML sitemap, robots, structured data | NEW | M | — |
| 34 | Discovery | Search insight reports (zero-result, filter usage) | NEW | L | — |
| 35 | Content | Promotion/campaign calendar (scheduled banners & coupons) | ENH | M | — |
| 36 | Content | Review governance (right-of-reply, evidence, flag tuning) | ENH | M | — |
| 37 | Notifications | Email channel decision + implementation or formal exclusion | CHG | H | `GAP-03` |
| 38 | Notifications | Preference centre depth, digests, quiet hours | ENH | L | `BR-NTF-*` |
| 39 | Security | Fraud/abuse rule engine + risk queue | NEW | M | grows with #3 |
| 40 | Security | Impersonation/break-glass with step-up + full audit | NEW | M | `SEC-012`; never ledger access (`M-07`) |
| 41 | Support | Ticket SLA, canned replies, CSAT, bulk moderation | NEW | M | — |
| 42 | Analytics | Finance close pack, tax reports, cohort/funnel (post-launch) | NEW | M/L | attribution stays future |
| 43 | Platform | ERP connector (outbox → ERP; ERP → read models) | NEW | M/H | §4; option decision |
| 44 | Platform | Service/integration accounts with scoped tokens for ERP & partners | NEW | H | §4 security model |
| 45 | Platform | Org "departments" for non-admin staff too (vendor roles stay as-is) | ENH | L | — |
| 46 | Growth | Loyalty/rewards | NEW | L | `GAP-04` |
| 47 | Growth | Referral/affiliate | NEW | L | backlog + ADR if money touches |
| 48 | Growth | Sponsored placements | NEW | L | `R3` future revenue |
| 49 | Growth | PWA offline shell | NEW | L | future scope |
| 50 | Ops | SLO/error-budget dashboards for the new surfaces | ENH | M | `INT-REQ-007` stack exists |
| 51 | Ops | Runbooks + admin procedures for each new department | NEW | M | Gate-2 readiness rows |
| 52 | Data | Reporting indexes/migrations for all new tables (forward-only) | ENH | H | `DATA-REQ-005`, no `migrate down` |
| 53 | ERP·Accounts | Chart of accounts + mapping registry, partner accounts, AR/AP aging (platform **and** per-merchant books) | NEW | H | §4.2 dept 1; `P-02` |
| 54 | ERP·Sales | Invoice register, credit notes, per-store sales journal & revenue reports | NEW | H | §4.2 dept 2; `P-01` |
| 55 | ERP·Purchases | Platform opex bills (queue → four-eyes approval → payment record); vendor PO → goods receipt → supplier bill | NEW | M | §4.2 dept 3; never marketplace money |
| 56 | ERP·Inventory | Stock-health views, adjustment approval; optional valuation (FIFO/AVCO) + locations for merchants | NEW | M/L | §4.2 dept 4; `b02` stays SoR |
| 57 | ERP·Reports | TB/P&L/BS/cash-flow/VAT packs (platform) + merchant statement/invoice/tax packs | NEW | H | §4.2 dept 5; `P-02`/`P-03` |
| 58 | ERP·Periods | Fiscal calendar, open/adjust/close/lock, close checklist, year-end carry-forward, report cutoffs | NEW | H | §4.2 dept 6; lock = `SUPER_ADMIN`, audited |
| 59 | ERP·Surfaces | Admin "Finance & ERP" console area + vendor-portal Finance extensions (invoices, tax, purchases) | NEW | M | §4.2 + §5.4 |

**Non-functional additions that ride along with every row above:** Arabic-first RTL rendering and
`ar`+`en` parity (`C-24`), WCAG 2.1 AA ≥95% automated pass (`NFR-011`), p95 budgets
(read <200 ms / write <500 ms), coverage floors (≥80% overall, money paths per the stricter ADMR
100%-critical gate), audit rows on every state change (`BR-PLT-06`), and 0 dead elements at DOD.

---

## 4. ERP integration (merchants, management, delivery, accounting, invoicing, …)

### 4.1 What "ERP" means here — scope map

| Requested ERP area | Capability | System of record (recommended) | Where it lives |
|---|---|---|---|
| **Merchants** | Vendor master data, KYC status, agreements, commission plans, payable balances | **yumn** (master), ERP as consumer | `b03` + `b07` → ERP partner ledger |
| **Management (platform ops)** | Dashboards, approvals, SLAs, staffing by department | **yumn** | §5 admin console |
| **Delivery providers** | Provider registry, rate cards, settlements, SLA | **yumn** (master) | `b08` (new `P-09`) → ERP expense entries |
| **Accounting** | Chart of accounts, journals, trial balance, P&L, close | **ERP** (master) fed by yumn ledger | `P-02` outbox → ERP |
| **Invoicing** | Statutory invoices, credit notes, numbering, tax fields | **yumn issues** (transactional truth); ERP stores/registers | `P-01` |
| **Tax** | VAT 15% computation & collection | **yumn**; reporting to ERP / filing tool | `P-03` |
| **Inventory** | Stock per product (marketplace, vendor-owned) | **yumn** (`b02`) — ERP only if a vendor separately runs one | optional sync |
| **Payouts/settlements** | Escrow release → payout batch → execution | **yumn** | `P-04` → ERP payment records |
| **Purchases (AP)** | Platform operating bills (infra, SMS/WhatsApp, provider fees); vendor supplier procurement (PO → receipt → bill) | **ERP / new domain** — never marketplace money | §4.2 department plan |
| **HR/payroll, manufacturing, POS** | — | out of scope v1 | explicitly excluded |

**Non-negotiable integrity rule:** the append-only double-entry ledger stays the single writer of
marketplace money (`BR-PAY-06`, `NFR-008`, `LedgerService.post` = only money writer, forbidden
pattern `F7` in [`module-boundaries.md`](docs/04-architecture/core/module-boundaries.md)). The ERP **never
writes** to `b07`; it receives postings and returns nothing money-shaped. Reconciliation is one-way
asserted: `J1`/`J2` inside yumn, plus a new daily "ledger ↔ ERP journal" diff report.

### 4.2 Departmental coverage — accounts, sales, purchases, inventory, reports & periods (platform **and** merchants)

**Operating model — two sets of books, one ledger of truth.** yumn keeps a *platform book* plus one
*merchant book per store* as sub-ledgers of the same append-only ledger; the ERP (in-platform core
under Option A, satellite under Option B) holds the general ledger those sub-ledgers post into.
Every department below is therefore **multi-tenant by construction**: platform administrators see and
operate the whole book; each merchant sees only their own slice (ownership rules `DATA-REQ-008`,
`BR-ORD-09` — foreign data ⇒ 404, never 403-leak).

| ERP department | Platform administrator scope | Merchant scope | Core objects / sources | Phase |
|---|---|---|---|---|
| **1. Accounts (CoA, AR/AP, partner accounts)** | Chart of accounts + account mapping (`P-02`), platform receivables (commission, fees, VAT collected), platform payables (vendor payouts, delivery-provider settlements, supplier bills), partner master (vendors, couriers, providers), AR/AP aging | Receivable from the platform = released escrow − commission − refunds (the "payable balance" already surfaced in `API-ANL-004`); own supplier AP **iff** purchases module enabled | mapping tables, ledger postings, `payout`, `escrow` | Phase 1 |
| **2. Sales** | Master/sub-orders, invoices & credit notes (`P-01`), refunds, GMV & commission revenue reports, invoice register, VAT collected | Own sub-orders, invoices issued on their behalf (downloadable copy), returns → credit notes, per-store sales journal | `b06` orders, `P-01` documents, `b09` returns | Phase 1 |
| **3. Purchases (AP)** | Platform operating procurement: bill for infra/hosting, SMS/WhatsApp credits, provider fees, partner services → approval → bill → payment record | Supplier procurement: purchase order → goods receipt → supplier bill → payment status (their money moves **outside** yumn; yumn only records it) | **new** `purchase_order`, `goods_receipt`, `supplier_bill`, `vendor_bill_payment` (ERP domain — not marketplace money, no `b07` writes) | Platform AP Phase 1–2 · merchant procurement Phase 2 (or native if Option B) |
| **4. Inventory** | None as stock (the platform holds no inventory — `business-model.md`); aggregate stock-health metrics only | yumn `b02.inventory` stays the operational source of truth (on-hand/reserved/available, 15-min TTL `C-13`, no-negative checks); ERP layer adds locations, valuation (FIFO/AVCO), adjustments/losses, stock-move history and its journal impact | `b02` (SoR) → optional snapshot sync to ERP; **never** ERP → yumn availability (prevents oversell) | Snapshot Phase 1–2; valuation Phase 2 |
| **5. Accounting reports** | Trial balance, P&L, balance sheet, cash flow, VAT return (`P-03`), commission/fee revenue, payout & provider reconciliation, month-end close pack | Monthly statement (`BR-FIN-04`, `API-ANL-004/005`), invoice register, tax summary, AR/AP aging (if purchases on), inventory valuation report | read models over ledger + documents (`B11` pattern) | Phase 1 |
| **6. Periods & close** | Fiscal calendar (12 periods + year), open → adjust → close → lock, cutoff rules, close checklist with an owner per department, year-end carry-forward, period-boundary report locks | Statement period aligned to platform period; their books "close" read-only when the platform period closes (they may still download) | **new** `fiscal_period`, `close_checklist_item`, `period_lock` (SUPER_ADMIN action, audited `BR-PLT-06`) | Phase 1 |

**Department ↔ staff mapping** (keeps §5.2 `ORG-*` org-departments as the *permission* model and this
table as the *module* model — they compose, they do not duplicate):

| ERP department | Owning org (platform) | Merchant-facing role | Guard |
|---|---|---|---|
| Accounts | `ORG-01` Finance (+ `ROLE-02` read-only auditor) | Vendor **Owner/Manager** | no ledger writes for anyone (`rbac` rows 15/16) |
| Sales | `ORG-01` (finance views) + `ORG-02` (merchant ops views) | Owner/Manager | invoices immutable once issued; void = credit note + audit |
| Purchases | `ORG-01` (opex approval) | Owner/Manager (`Editor` read) | payment is a **record**, never executed through yumn |
| Inventory | `ORG-02` oversight | Owner/Editor | `b02` stays operational SoR; valuation ≠ availability |
| Reports | `ORG-01`, `ORG-08` Executive (read-only) | Owner (own store only) | exports obey CSV rules; totals carry `totalsMeta` |
| Periods & close | `ORG-01` proposes, **`SUPER_ADMIN` locks** | — (read-only) | lock is audited; late entries only via adjustment journals |

**Administration surfaces**

- *Platform admin console (new "Finance & ERP" area):* tabs for **Accounts** (CoA mapping, partners,
  aging), **Sales** (invoice register, credit notes), **Purchases** (bill queue with four-eyes
  approval, PO list), **Inventory** (read-only stock health + adjustments approval), **Reports**
  (run/export, scheduled delivery), **Periods** (calendar, checklist, lock), **Sync monitor**
  (outbox depth, held/review/resolved exceptions, mapping drift) — every mutation returns an
  `auditId`, actions stay inside §5.5 UX guardrails.
- *Vendor portal:* extend the existing Finance area (`UC-022`) with **Invoices**, **Tax summary**,
  and — when enabled — **Purchases** (PO/bill entry) and **Stock valuation**; statements and
  balance/escrow/payout views already exist.
- *Interfaces:* admin endpoints follow the `API-ADM` group conventions; merchant endpoints follow
  `API-ANL`/`API-WAL` scoping (own store, foreign ⇒ 404).

**Period-close mechanics (non-negotiables):** ledger stays append-only — corrections are
compensating entries only (`DATA-REQ-007`, `LedgerService.post` = single writer, forbidden pattern
`F7`); a locked period rejects connector journals (queue them as adjustment-period entries, never
overwrite); close cadence settles together with the open `CT-21` decision (hourly vs nightly vs
daily chain/`J10` verification) so one answer drives all batch timings; `J1`/`J2` must be green
**before** a period may be locked.

**Phasing:** Phase 1 = departments 1, 2, 5, 6 skeleton + platform purchase-bill capture ·
Phase 1–2 = department 3 approval flow + inventory snapshots (`P-10` ops view) ·
Phase 2 = merchant procurement & valuation depth (or adopt Option B ERP natively) · all of it stays
behind the connector port so switching Option A → B is configuration, not re-platform.

### 4.3 Options considered

| Option | Description | Pros | Cons | Verdict |
|---|---|---|---|---|
| **A. In-platform ERP foundation** | Build `P-01…P-04` inside the monolith (new domain area; if it grows, propose block **B14 "finance & ERP"** via change control) + an ERP **connector port** | Respects `C-18` (custom build), `C-19` (PostgreSQL only), `C-20/21` (BullMQ, monolith), `C-22` (Compose); zero new runtime; money path stays single-writer | Accounting depth is home-grown; accountant UX weaker than mature ERPs | **RECOMMENDED for v1** |
| **B. Self-hosted ERP satellite (Odoo / ERPNext)** | Add one Compose service; yumn talks to it through a dedicated adapter module | Mature accounting/invoicing/CoA; Odoo uses PostgreSQL (aligns with `C-19`); ERPNext/MariaDB would clash with the "PostgreSQL only" rule of record; both are self-hostable | Second system to secure, back up, upgrade; dual UIs for staff; 99.99% availability target (`C-26`) now covers it; data-residency question `GAP-11` applies; staff training | **v2 option** — keep the connector port ready (Option A already includes it) |
| **C. SaaS/enterprise ERP via iPaaS (NetSuite, Dynamics, …)** | Cloud ERP + integration platform | Fastest accounting maturity | Cross-border data (`GAP-11`), connectivity/cost realities in Yemen, violates the spirit of self-hosted `C-22` operations, no offline tolerance | **Not viable for v1** |

### 4.4 Integration mechanics (applies to A and B)

- **Pattern:** transactional outbox table written **in the same DB transaction** as the domain change
  (order placed, escrow released, payout executed, invoice issued) → BullMQ job publishes to the
  connector → idempotent `POST` keyed by `outbox.id` + event ID → provider ack stored. Follows the
  existing ports/adapters design (`INT-REQ-008`) and webhook-reliability rules (`INT-REQ-006`:
  10 s timeouts, 3 retries → DLQ + alert, correlation IDs, HMAC + constant-time verification,
  sandbox before production).
- **Sync modes:** near-real-time for state that must not lag (order events, invoice issuance,
  payout status); scheduled batch for financial aggregates (journal batches, tax summaries —
  hourly/nightly; the `CT-21` cadence decision should settle "hourly vs nightly vs daily" once).
- **Direction & payload map:**

| Flow | Direction | Trigger | Payload (essence) | Idempotency key |
|---|---|---|---|---|
| Vendor master | yumn → ERP | KYC approved / profile change | vendor id, legal name, KYC status, commission tier, IBAN/wallet payout account | `vendor.id@version` |
| Sales documents | yumn → ERP | order `PLACED` / `REFUNDED` | master order + sub-orders, lines, VAT breakdown, coupon, shipping | `order.id@state` |
| Journal batch | yumn → ERP | nightly + month-end | ledger postings grouped by account mapping, balanced to 0 | `batch.date#seq` |
| Invoice / credit note | yumn → ERP | invoice issued/voided | document number, series, hash, totals | `invoice.number` |
| Escrow release / commission | yumn → ERP | release event | per-sub-order release, commission bps, payable delta | `escrow.id@event` |
| Payout batch | yumn → ERP | batch executed | payout rows, provider refs, fees | `payout.batch@run` |
| Delivery settlement | yumn → ERP | provider run closed | provider id, deliveries, amounts | `delivery.settlement@id` |
| Tax summary | yumn → ERP | daily/monthly | taxable base, VAT collected, refunds | `tax.report@period` |
| Item/stock (optional) | yumn → ERP | catalog change | SKU, price YER, on-hand | `product.id@version` |
| Chart of accounts / mapping | ERP → yumn | mapping change | account codes (read-only reference) | `mapping.version` |
| Close status | ERP → yumn | month closed | close period lock flag (blocks late journals) | `period.key` |

- **Security:** dedicated **service accounts** (non-human, `SYSTEM`-class, no interactive login,
  scoped tokens rotated from host-only secrets, mode 0600, `CONFIG_MISSING` fail-fast — no secrets in
  repos or `NEXT_PUBLIC_*`); mTLS or HMAC signing with IP allowlist where the ERP is external;
  every connector action audited (`BR-PLT-06`) with `outcome` captured.
- **Failure handling:** exception queue surfaced in the admin console (held/review/resolved counts),
  replay after mapping fixes, never silent "Uncategorized" postings, DLQ alerts per the retry schedule.
- **Verification:** contract tests against a sandbox ERP, seeded-mismatch detection (same discipline as
  `J1`/`J2`), and a Gate-2 end-to-end "money cycle audit" that includes the ERP journal diff.

### 4.5 Sequencing

1. **Phase 0 (now):** decide Option A vs B (§8), settle `GAP-13` (it changes what must be journalized
   at all), open `DEP-09` (VAT opinion) — invoicing fields depend on it.
2. **Phase 1:** department skeleton for **accounts, sales, reports, periods** (§4.2 depts 1/2/5/6) +
   `P-01` invoicing + `P-02` account mapping + outbox infrastructure (the connector spine) + platform
   purchase-bill capture (dept 3 start).
3. **Phase 1–2:** purchase-bill approval flow + inventory snapshots (depts 3/4), `P-03` tax reports,
   `P-04` settlement runs, ERP journal diff report, admin "Finance & ERP" console + vendor-portal
   finance extensions.
4. **Phase 2 / v2:** merchant procurement & stock-valuation depth (dept 3/4 full), then full ERP
   satellite (Option B) if accounting volume justifies it — connector port already in place, no
   re-platform.

---

## 5. Full administrative control over the platform

### 5.1 What exists today (verified)

[`docs/07-api/admin/admin.md`](docs/07-api/admin/admin.md) defines `API-ADM-001…043` across
10 sections: users & moderation, KYC review, store lifecycle, category/attribute taxonomy, platform
settings (`GET /admin/settings` groups `GENERAL, PAYMENT, LOGISTICS, COMMISSION, SECURITY` +
`PUT /admin/settings/{key}` = `SUPER_ADMIN` + `SETTINGS_VERSION_CONFLICT` optimistic locking), audit &
role management, content moderation, finance ops (bank top-up verify/reject, wallet freeze/unfreeze),
support tickets, health probes. Around it: `API-ORD-014` forced state override, dispute arbitration
(`API-RET-014`), reconciliation (`API-ANL-009`), reports/exports (`API-ANL-007/008`).
**Absent (`VERIFIED`):** any "department" concept (0 corpus hits), a feature-flag endpoint, bulk
operations, approval workflows, per-department scoping, an audit explorer UI contract, and ERP/invoice
administration.

### 5.2 Department model (`ORG-01…ORG-08`, proposed)

Keep the **7 canonical actors** (`ACT-01…ACT-07`) and the four-way mapping invariant in
[`rbac.md`](docs/09-security/core/rbac.md) §8. Departments are **permission bundles + queue scopes inside
`ADMIN`**, not new actors (§6 explains the alternative).

| ID | Department | Owns (existing endpoints) | Must NOT touch |
|---|---|---|---|
| `ORG-01` | **Finance & Payments** | bank top-ups (`API-ADM-030…032`), freeze/unfreeze, payout ops, reconciliation, invoices, tax reports | ledger rows (append-only), role management |
| `ORG-02` | **Vendor Success / Merchant Ops** | KYC queue (`API-ADM-005…008`), stores (`API-ADM-009…013`), vendor plans/agreements | KYC *policy* changes, money |
| `ORG-03` | **Catalog & Content** | categories/attributes (`API-ADM-014…021`), moderation (`API-ADM-027…029`), CMS/banners/coupons | settings, roles |
| `ORG-04` | **Logistics & Delivery** | zones/rates, dispatch, delivery-code override (pending `GAP-02`), provider registry | payouts (org-01 executes) |
| `ORG-05` | **Customer Support** | tickets (`API-ADM-035…041`), return/dispute intake, refunds *initiation* (org-01 approves) | top-up verification, roles |
| `ORG-06` | **Trust & Safety / Compliance** | audit read, risk queue, retention/DSAR, fraud rules | ledger, settings writes |
| `ORG-07` | **Platform Engineering** | settings (group-scoped), feature flags, integrations/webhooks, health, feature releases | finance ops, moderation |
| `ORG-08` | **Executive (read-only)** | dashboards, reports, exports, KPI views | every state-changing endpoint |

Guardrails: deny-by-default (`SEC-REQ-004`), every privileged change returns `auditId`, four-eyes on
money actions (org-01 initiator ≠ approver), and **`rbac.md` rows 15/16 remain absolute** — no
department grants balance read/write (`M-07`/`CT-29` disposition pending).

### 5.3 Detailed settings (expansion of the 5 current groups)

Settings registry columns already designed (key, type, default, scope, version) — extend the taxonomy:

| Group | New keys (examples) | Owner dept |
|---|---|---|
| `GENERAL` (exists) | platform name, support channels, legal pages, locale pair (`ar`,`en` only) | `ORG-07` |
| `PAYMENT` (exists) | enabled top-up providers, per-provider limits, min/max order (`C-14`), wallet freeze policy | `ORG-01` |
| `LOGISTICS` (exists) | zones, rates, code attempt/lock rules, ETA windows, provider assignment policy | `ORG-04` |
| `COMMISSION` (exists) | tier table 5–20% (default 10%), release policy (7 d vs merchant window if `M-04` approved) | `ORG-01` |
| `SECURITY` (exists) | OTP length/TTL/attempts, session lifetimes (`C-08` — *read-only*: never tunable), step-up rules | `ORG-06` |
| **`FINANCE`** (new) | statement day, payout min (`1,000 YER`) & window, rounding, adjustment policy | `ORG-01` |
| **`TAX`** (new) | VAT rate (15% default), tax-inclusive display, tax IDs, fiscal period | `ORG-01` |
| **`INVOICING`** (new) | series/numbering, mandatory legal fields, PDF language, logo, QR/hash policy | `ORG-01` |
| **`ERP`** (new) | connector mode (off/one-way/batch), endpoint, mapping version, schedule, dry-run | `ORG-07` |
| **`NOTIFICATIONS`** (new) | template versions, quiet hours, provider preference order (`BR-NTF-03`), channel enablement incl. email if `GAP-03` = in | `ORG-07` |
| **`CONTENT`** (new) | banner slots, moderation auto-approve mode, review auto-approve | `ORG-03` |
| **`SEARCH`** (new) | reindex cadence, synonyms, boost rules | `ORG-03` |
| **`RISK`** (new) | velocity limits, top-up review thresholds, P2P limits (if approved) | `ORG-06` |
| **`AUDIT`** (new) | retention years, chain-verify cadence (`CT-21` decision), export policy | `ORG-06` |
| **`FX`** (new, conditional) | rate source, spread, update cadence, rounding | `ORG-01` — only if `GAP-14` |

Precedence stays as designed (compiled defaults → `.env.<env>` → runtime → feature flags → platform
settings); `SETTINGS_VERSION_CONFLICT` on every write; flag changes remain separate and never encode
business values ([`configuration.md`](docs/14-devops-infrastructure/core/configuration.md) §4).

### 5.4 Component inventory the admin must control

Entities/settings the console must administer end-to-end: users & roles, stores & staff, KYC
documents, categories/attributes/slug redirects, products (override/unlist), coupons, banners/CMS
pages, notification templates, shipping zones/rates, delivery providers (new), wallets (freeze only),
top-ups, escrow views, payouts, invoices (new), tax config (new), ERP mappings (new), integrations
(webhook endpoints, provider credentials), feature flags, audit log, tickets, disputes, moderation
queue, risk rules, retention jobs, health/metrics links, **plus the ERP department surface:**
chart-of-accounts mapping, partner accounts, invoice register & credit notes, purchase-bill queue,
inventory adjustments, fiscal periods (open/close/lock), close checklist, report runs, connector
sync monitor (§4.2).

### 5.5 Admin UX requirements (all screens)

Arabic-first RTL with `en` parity; WCAG 2.1 AA (0 critical/serious axe findings); server-side
authorization on every action (UI hiding is never security); confirmation via the system modal (never
`alert/confirm/prompt`); every mutation shows its `auditId`; bulk actions with per-item audit rows;
CSV/UTF-8 exports consistent with existing rules; cursor pagination except where offset is documented.

---

## 6. Potential user roles and additional role-based features

### 6.1 Canonical today (unchanged unless change control says otherwise)

7 actors (`ACT-01 Customer`, `ACT-02 Vendor`, `ACT-03 Courier`, `ACT-04 Admin`, `ACT-05 Super Admin`,
`ACT-06 Moderator`, `ACT-07 System`) + vendor staff profiles Viewer/Editor/Manager inside `VENDOR`,
enum 10, DB 6 login roles ([`rbac.md`](docs/09-security/core/rbac.md) §8).

### 6.2 Proposed role additions

| ID | Role | Type | Scope & capabilities | Condition |
|---|---|---|---|---|
| `ROLE-01` | **Finance Officer** | staff profile under `ADMIN` (`ORG-01`) | verify top-ups, payout batches, invoices, tax reports, reconciliation views; no role changes, no ledger writes | approved with §5 |
| `ROLE-02` | **Accountant / Auditor (read-only)** | staff profile, read-only | journals, close pack, exports, audit read; zero mutations | with `P-02` |
| `ROLE-03` | **KYC / Compliance Officer** | staff profile (`ORG-02`/`ORG-06`) | KYC decisions, document vault, sanctions checks | with §5 |
| `ROLE-04` | **Support Agent** | staff profile (`ORG-05`) | ticket queue, canned replies, return intake, refund *initiation* | with `P-15` |
| `ROLE-05` | **Logistics Coordinator** | staff profile (`ORG-04`) | dispatch, provider assignment, code-override (if `GAP-02` = yes) | with `P-09/P-10` |
| `ROLE-06` | **Content Editor / Category Manager** | staff profile (`ORG-03`), narrower than `MODERATOR` | CMS, banners, category tree, review moderation | with §5 |
| `ROLE-07` | **Risk Analyst** | staff profile (`ORG-06`) | risk queue, velocity rules, freeze *requests* | with `P-16` |
| `ROLE-08` | **Delivery Partner Admin** | new external role under `ACT-03` umbrella | manage own fleet couriers, rates, settlements, SLA views | `GAP-07` = yes |
| `ROLE-09` | **Integration / Service Account** | non-human (`SYSTEM`-class) | ERP connector, partner APIs; scoped tokens, no login, write-only audit | with §4 |
| `ROLE-10` | **Vendor Franchise HQ (multi-store owner)** | new actor **only if** change control approves | one owner, many stores (today `BR-VND-02` = one store per vendor) | future; currently excluded by `BR-VND-02` |
| `ROLE-11` | **Corporate / B2B buyer** | future customer profile | org accounts, PO-based ordering, credit (**conflicts `C-03`**) | out of scope v1 — backlog only |

**Recommendation:** ship `ROLE-01…ROLE-07`, `ROLE-09` as **permission bundles** (no new `ACT` rows) —
this preserves the documented cardinality invariants and avoids a corpus-wide role-mapping rewrite.
`ROLE-08`, `ROLE-10`, `ROLE-11` require explicit change control (`ACT` + `rbac` + `actors-and-roles`
propagation).

### 6.3 Role-specific feature additions

- **Customer:** wishlist (`P-11`), buy-again (`P-12`), stock alerts (`P-13`), richer order timeline,
  statement/invoice download (`P-01`), privacy centre (`P-17`).
- **Vendor:** bulk import (`P-07`), scorecard (`P-08`), invoice copies + tax summary (`M-15`),
  plan/agreement view (`P-06`), payout receipts, promotion calendar participation (`M-19`).
- **Courier:** proof-of-delivery photo upload, earnings view, availability toggle (all no-GPS, `C-16`).
- **Admin staff (per department):** §5.2 capabilities + bulk ops, saved views, approval inboxes,
  audit explorer.
- **Super Admin:** role/permission management, settings (all groups), flags, ERP switch, integrations.
- **System:** new jobs for invoicing, journal export, ERP outbox, retention, scorecards — each added
  as a row to the 30-row queue register before any code names it.

---

## 7. Prioritization & sequencing (aligned to the phase model)

Per [`implementation-roadmap.md`](docs/21-completion/core/implementation-roadmap.md): schedule floats; no
dates until `ASM-14` baselines exist; each phase exits only through its gate.

| Wave | Contents | Gate |
|---|---|---|
| **Wave 0 — decisions (sponsor/owner)** | `GAP-13` (amend vs re-scope `C-04/05/06/12`, P2P, admin access) → unblocks `M-01…M-07` + `GAP-14`; `GAP-03` email; `GAP-02` code override; `M-17` wishlist; ERP Option A/B; department model sign-off | **Gate 0** (currently `FAIL`: `CRIT-01`, `DEP-05`, `DEP-06`, `DEP-10`, charter sign-off) |
| **Wave 0 — spec integrity (analyst, no code)** | `M-05`, `M-08`, `M-09`, `M-10` + remaining `CT-*`/`CRIT-*` dispositions | Gate 0 checks 0.5–0.7 |
| **Wave 1 — build (Phase 1)** | all HIGH rows; ERP spine (`P-01`,`P-02`); admin foundations (§5); `SEC-012`/`SEC-003` | **Gate 1** |
| **Wave 2 — completeness (Phase 1–2)** | MEDIUM rows: `P-03`,`P-04`,`P-06…P-10`,`P-14…P-17`, vendor tooling, SEO, campaigns | **Gate 2** |
| **Wave 3 — growth (Phase 2 / post-launch)** | LOW rows: loyalty, referral, PWA, analytics depth, ERP satellite (Option B) | **Gate 3** |

Dependencies that must not be inverted: money features (`M-01`, `M-04`, `P-01`, `P-02`) wait for
`DEP-10` (Central Bank position) per Gate 0 check 0.4; anything OTP-dependent waits for `DEP-06`;
provider adapters wait for `DEP-05` + `GAP-10`; tax outputs wait for `DEP-09`/`ASM-10`.

---

## 8. Approval request — decisions needed before this plan becomes work

> **Outcomes recorded 2026-09-28 (administrator approval, session 007).** `OPEN` items stay open
> until their own evidence lands — approval never fabricates a gate (`GEN-03`).

| # | Decision | Options | Recommended | Outcome (2026-09-28) |
|---|---|---|---|---|
| D1 | `GAP-13` — does `describ.md` **amend** `C-04/05/06/12`, the no-P2P principle and `rbac` rows 15/16, or is the spec **re-scoped** to canon? | amend / re-scope / mixed (per-row) | **Mixed:** accept `M-02` (extra wallets) and `M-03` (optional email); decide `M-01`/`M-04`/`M-06`/`M-07` on their own merits with security & finance review | **APPROVED mixed.** `C-05` amended (+Al-Kuraimi Bank, Jeeb wallets), `C-06` amended (optional *verified* email) — `CT-24`/`CT-25` → RESOLVED, `HAL-15` → RESOLVED. `M-07` = **NO** → `CT-29` RESOLVED-NO (rbac rows 15/16 absolute). `M-01`/`M-04`/`M-05`/`M-06` remain **OPEN** (finance/security/owner review), `GAP-14` stays OPEN |
| D2 | ERP strategy | A in-platform · B self-hosted satellite · C SaaS | **A now, connector-port ready for B later** (§4.3) | **APPROVED — Option A + connector port.** Recorded in `decision-log.md` §2 (ADR-011 is pre-reserved for multi-host); propagation: `erp-finance-departments.md` DOC-SA-011 |
| D3 | ERP block placement | extend `B07`+`B13` vs new block **B14** | start inside existing boundaries; promote to `B14` only when size forces it (both paths need change control) | **APPROVED — start in `B07`/`B13`**; `B14` promotion is a change-control event |
| D4 | Departments & staff profiles | bundles inside `ADMIN` vs new actors | **bundles inside `ADMIN`** (§6.2) | **APPROVED.** `ORG-01`…`ORG-08` + `ROLE-01`…`ROLE-07`/`ROLE-09` minted in `rbac.md` §11 |
| D5 | Wishlist | implement (`P-11`) vs delete route (`M-17`) | **implement** (small, removes a dead-element DOD risk) | **APPROVED — implement** (`P-11`, scheduled Wave 2) |
| D6 | Email channel `GAP-03` | in v1 / out of v1 | **out of v1**, document the exclusion (SMS/WhatsApp/in-app/push already cover it) | **APPROVED — OUT of v1** → `GAP-03` RESOLVED (documented exclusion) |
| D7 | `GAP-02` delivery-code admin override | allow audited override / never | **never** in v1 (keeps `AC-S-*` "0 deliveries without code" absolute) | **APPROVED — NEVER** → `GAP-02` RESOLVED |
| D8 | `GAP-05` vendor plans · `GAP-04` loyalty · `GAP-07` fleets | defer / include | **defer plans & loyalty**; build the **fleet registry skeleton** (`P-09`) since ops needs it | **APPROVED — defer `GAP-04`/`GAP-05`** (stay OPEN, annotated deferred); **`P-09` fleet skeleton included** (`GAP-07` annotated approved-skeleton) |
| D9 | Approve §1 HIGH set as the pre-build backlog and §3 as the v1 completeness checklist | yes / amend | — | **APPROVED** — §1 HIGH rows + §3 59-row checklist = the pre-build backlog |
| D10 | On approval, authorize register propagation (FR registry, `rbac.md`, `project-scope.md`, constraints, ADRs) under change control | yes | — | **APPROVED.** Propagation executed 2026-09-28 under §9 change control: `rbac.md` §11, `project-constraints.md` (`C-05`/`C-06`), `project-scope.md`, `requirements-overview.md`, `decision-log.md` §2, validation registers |
| D11 | ERP department depth for v1: accounts/sales/reports/periods only, **or** also platform purchases + inventory snapshots | core-only / core+ (recommended) | **core+ (§4.2 phasing)** — merchant procurement & valuation stay Phase 2 | **APPROVED — core+** |

---

## 9. Sources

**Project canon (internal, `VERIFIED` reads this session):**
[`project-scope.md`](docs/00-project-overview/project-scope.md) ·
[`project-constraints.md`](docs/00-project-overview/project-constraints.md) ·
[`actors-and-roles.md`](docs/00-project-overview/actors-and-roles.md) ·
[`business-model.md`](docs/01-business-analysis/core/business-model.md) ·
[`business-processes.md`](docs/01-business-analysis/core/business-processes.md) ·
[`business-rules.md`](docs/01-business-analysis/business-rules.md) ·
[`requirements-overview.md`](docs/02-requirements/requirements-overview.md) ·
[`docs/02-requirements/functional/index.md`](docs/02-requirements/functional/index.md) ·
[`admin.md`](docs/07-api/admin/admin.md) · [`analytics.md`](docs/07-api/core/analytics.md) ·
[`rbac.md`](docs/09-security/core/rbac.md) ·
[`module-boundaries.md`](docs/04-architecture/core/module-boundaries.md) ·
[`backend-architecture.md`](docs/06-backend/core/backend-architecture.md) ·
[`docs/08-database/core/entities-index.md`](docs/08-database/core/entities-index.md) ·
[`integration-overview.md`](docs/10-integrations/core/integration-overview.md) ·
[`configuration.md`](docs/14-devops-infrastructure/core/configuration.md) ·
[`data-quality.md`](docs/16-data/core/data-quality.md) ·
[`missing-information.md`](docs/20-validation/core/missing-information.md) ·
[`contradiction-audit.md`](docs/20-validation/core/contradiction-audit.md) ·
[`critical-findings.md`](docs/20-validation/core/critical-findings.md) ·
[`recommendations.md`](docs/21-completion/core/recommendations.md) ·
[`implementation-roadmap.md`](docs/21-completion/core/implementation-roadmap.md) ·
[`quality-gates.md`](docs/21-completion/core/quality-gates.md) ·
[`technical-debt.md`](docs/21-completion/core/technical-debt.md) ·
[`describ.md`](describ.md) (sponsor input, `CT-23`…`CT-30` / `GAP-13` / `GAP-14`).

**External research (benchmark & ERP — consulted 2026-09-28):**
- Multi-vendor feature benchmarks: https://virtocommerce.com/blog/best-multi-vendor-marketplace-platforms ·
  https://www.cs-cart.com/multi-vendor-functions · https://docs.cs-cart.com/latest/user_guide/users/vendors/account_balance.html ·
  http://sharetribe.com/features · https://www.sharetribe.com/features/marketplace-essentials ·
  https://www.wcvendors.com/wc-vendors-pro · https://multivendorsuite.com/features
- ERP ↔ commerce integration patterns: https://www.netsuite.com/portal/resource/articles/erp/erp-ecommerce-integration.shtml ·
  https://www.shopify.com/il/enterprise/blog/ecommerce-erp-integration ·
  https://www.truecommerce.com/en-gb/blog/integrating-amazon-marketplace-with-your-erp-business-system ·
  https://www.cbh.com/insights/articles/why-centralized-ecommerce-erp-integration-matters-for-cfos
- ERP module surfaces: https://www.odoo.com/documentation/16.0/applications/finance/accounting.html ·
  https://www.odoo.com/app/purchase-features · https://docs.erpnext.com/homepage ·
  https://github.com/stevenyaga/erpnext-api-docs

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-28 | Initial draft: modification register `M-01…M-25`, proposals `P-01…P-20`, 52-row completeness checklist, ERP integration design, admin/department model, role proposals, approval decisions D1–D10 | Session 007 — development & planning manager deliverable requested by the sponsor for review before any work |
| 1.1 | 2026-09-28 | ERP section expanded: new §4.2 departmental coverage (accounts, sales, purchases, inventory, accounting reports, periods & close — platform **and** merchant books), dept↔staff map, admin/vendor surfaces, close mechanics; scope map +Purchases row; checklist rows 53–59; §5.4 components; decision D11; §4.3–4.5 renumbered | Sponsor request: ERP must manage all departments for merchants and platform administrators |
| 1.2 | 2026-09-28 | **APPROVED** by administrator. Status header rewritten; §0.4 mint record (`ORG-*`/`ROLE-*` → `rbac.md` §11); §8 table gains an Outcome column recording `D1`…`D11` dispositions with register consequences (`CT-24`/`CT-25`/`CT-29`/`GAP-02`/`GAP-03`/`GAP-13` resolutions, deferred annotations, honest OPEN carry-overs) | Session 007 — plan approved for analysis-layer implementation under `docs/README.md` §9 change control |
| 1.3 | 2026-09-30 | Count sync: §Method 68 → **73 requirements**, `M-09` parenthetical 253 → **273 ACs** (factual count corrections only — no approved content, `D1`…`D11` disposition or scope line changed) | Owner directive session 011 (`prompt-011.md` §4.7): `requirements-overview.md` v1.2 registered `SEC-REQ-013`…`016` + `DATA-REQ-009`, `acceptance-criteria.md` v1.2 registered 20 new ACs; consumer re-synced in same change set |
