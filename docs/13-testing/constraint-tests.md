---
document_id: DOC-TST-004
title: Constraint Tests — Canonical Register TST-CON-01 … TST-CON-26
category: 13-testing
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-011, FR-012, FR-013, FR-015, NFR-003, NFR-005, NFR-006]
related_documents: [DOC-TST-001, DOC-TST-002, DOC-TST-003, DOC-OVR-008, DOC-AC-001, DOC-SA-010]
---

# Constraint Tests — TST-CON-01 … TST-CON-26

**The single, authoritative register of constraint tests.** Exactly one test per project constraint: `TST-CON-NN ↔ C-NN` (one-to-one, same number). **These IDs are defined nowhere else** — other documents may only reference them. Constraint canon lives in `00-project-overview/project-constraints.md` (DOC-OVR-008); acceptance conditions for the sweep in `AC-XCUT-02`; gate `AC-S-02` requires **26/26 PASS** before release.

**Status vocabulary:** `DESIGNED` (specified here) → `READY` (implementation + fixtures exist) → `EXECUTED` → `PASS` / `FAIL`. All tests are `DESIGNED` at v1.0 (no implementation exists yet).

---

## 1. Summary Register

| ID | Constraint | Assertion (one line) | Test type | Status |
|---|---|---|---|---|
| TST-CON-01 | C-01 | Every `payment_method != wallet` is rejected; zero COD paths exist | Integration + static | DESIGNED |
| TST-CON-02 | C-02 | No card fields, endpoints, or card processors anywhere | Static + API review | DESIGNED |
| TST-CON-03 | C-03 | No BNPL/installment/credit feature, flag or endpoint | Scope + code review | DESIGNED |
| TST-CON-04 | C-04 | Single fiat currency YER; no USD/SAR/crypto code paths | Unit + code audit | DESIGNED |
| TST-CON-05 | C-05 | Only m-Floos, OneCash, manual bank-transfer top-ups accepted | Integration | DESIGNED |
| TST-CON-06 | C-06 | Phone + OTP only: no email-primary auth, no social login | Integration + static | DESIGNED |
| TST-CON-07 | C-07 | No server-side biometric authentication exists | Code review | DESIGNED |
| TST-CON-08 | C-08 | Access JWT 15 min, refresh 7 days with single-use rotation | Security integration | DESIGNED |
| TST-CON-09 | C-09 | **State count == 17 and no other states exist in code** | Unit (state machine) | DESIGNED |
| TST-CON-10 | C-10 | One master per checkout, one sub-order per vendor, master = Σ subs | Integration | DESIGNED |
| TST-CON-11 | C-11 | Return eligibility honours `isReturnable` / `returnPeriodDays` from delivery | Rule integration | DESIGNED |
| TST-CON-12 | C-12 | Escrow releases no earlier than 7 days after DELIVERED | Integration (clock-shift) | DESIGNED |
| TST-CON-13 | C-13 | 15-min reservation TTL with auto-release; permanent deduction on payment | Integration + timer | DESIGNED |
| TST-CON-14 | C-14 | **Orders accepted only in 500–5,000,000 YER** | Validation boundary | DESIGNED |
| TST-CON-15 | C-15 | Cart guards: ≤50 products, ≤10 units/product, ≤5 vendors | Validation boundary | DESIGNED |
| TST-CON-16 | C-16 | **No GPS/location field anywhere + 6-digit delivery-code flow** | Static + E2E | DESIGNED |
| TST-CON-17 | C-17 | Shipping zones restricted to domestic Yemen addresses | Config integration | DESIGNED |
| TST-CON-18 | C-18 | 100% custom build — no commerce platform in the manifest | Dependency audit | DESIGNED |
| TST-CON-19 | C-19 | PostgreSQL 16 is the only relational DB in every environment | Deploy config review | DESIGNED |
| TST-CON-20 | C-20 | BullMQ is the only queue system — no RabbitMQ/Kafka | Dependency audit | DESIGNED |
| TST-CON-21 | C-21 | Modular monolith: 0 module-boundary violations | Architecture lint | DESIGNED |
| TST-CON-22 | C-22 | Docker Compose deployment only — no Kubernetes manifests | Deploy config review | DESIGNED |
| TST-CON-23 | C-23 | Greenfield — no legacy migration/coexistence code paths | Scope audit | DESIGNED |
| TST-CON-24 | C-24 | Arabic default + full English parity; exactly two locales | i18n scan + E2E | DESIGNED |
| TST-CON-25 | C-25 | **10,000 concurrent users sustained within NFR-001** | Load (k6) | DESIGNED |
| TST-CON-26 | C-26 | **99.99% availability SLO verified by probes + drill method** | Monitoring + drill | DESIGNED |

## 2. Test Detail

### TST-CON-01 — Wallet-only payments
- **Constraint:** C-01 · **Status:** DESIGNED
- **Asserted:** order creation rejects every `payment_method != wallet`; no COD/cash code path exists in code, API schemas or UI flows.
- **Type / Method / Env:** integration + static · Jest/Supertest-style matrix over `POST /orders` (wallet, cod, card, bank) + repo scan for `cod`/`cash_on_delivery` identifiers · CI, staging.
- **Pass:** non-wallet methods → `PAYMENT_METHOD_NOT_ALLOWED` with 0 order rows and 0 ledger entries; static scan 0 hits. **Notes:** pairs with TC-031, `AC-FR011-05`, `BR-PAY-01`; counted in the `AC-XCUT-02` sweep.

### TST-CON-02 — No card payments
- **Constraint:** C-02 · **Status:** DESIGNED
- **Asserted:** no card fields, endpoints, processors (Stripe/Moyasar/Tap or any card network) exist anywhere.
- **Type / Method / Env:** static + API review · dependency/import scan + OpenAPI schema grep + UI form inspection · CI.
- **Pass:** 0 matches for card PAN/CVV/processor tokens in code, schemas, DB entities, and docs of the contract. **Notes:** complements TST-CON-01 (absence proof vs behavioral rejection).

### TST-CON-03 — No BNPL / installments / credit
- **Constraint:** C-03 · **Status:** DESIGNED
- **Asserted:** no BNPL, installment or credit feature, feature flag, endpoint or schedule field exists.
- **Type / Method / Env:** scope + code review · keyword scan (`installment`, `bnpl`, `credit_limit`, `pay_later`) + product-type audit · CI + review.
- **Pass:** 0 hits outside explanatory docs; product types limited to physical goods (`BR-CAT-05`). **Notes:** pairs with `project-scope.md` OUT OF SCOPE entries.

### TST-CON-04 — Single fiat currency YER
- **Constraint:** C-04 · **Status:** DESIGNED
- **Asserted:** all money is integer YER; no USD/SAR wallets, no crypto code paths.
- **Type / Method / Env:** unit + code audit · money-type tests (integer, no floats) + scan for currency codes/crypto libraries · CI.
- **Pass:** every ledger/balance/order amount is integer YER; 0 crypto/foreign-currency references in payment module. **Notes:** `BR-PAY-10`, `BR-FIN-05`.

### TST-CON-05 — Approved top-up methods only
- **Constraint:** C-05 · **Status:** DESIGNED
- **Asserted:** only m-Floos, OneCash and manual bank transfer top-ups are accepted; other instruments rejected.
- **Type / Method / Env:** integration · one happy + one reject case per method against mock adapters (`MockPaymentAdapter`) · CI, staging sandbox.
- **Pass:** each approved method credits exactly once after verification (`BR-PAY-03/04`); unknown method → validation error, 0 ledger rows. **Notes:** `AC-IR001-01`, `AC-IR002-01`, `API-WAL-003/004`.

### TST-CON-06 — Phone + OTP only
- **Constraint:** C-06 · **Status:** DESIGNED
- **Asserted:** registration/login are phone-primary with SMS/WhatsApp OTP; no email-primary auth and no social login exist.
- **Type / Method / Env:** integration + static · register/login path tests + absence scan for OAuth/social/email-login endpoints · CI.
- **Pass:** phone `^7[0-9]{8}$` + OTP flows succeed; 0 social/email-auth endpoints; email never used for login (`BR-AUTH-08`). **Notes:** `AC-FR001-01`, TC-001–010.

### TST-CON-07 — No server-side biometrics
- **Constraint:** C-07 · **Status:** DESIGNED
- **Asserted:** no biometric data is received, stored or used as server authentication.
- **Type / Method / Env:** code review · scan for biometric endpoints/fields (fingerprint/face) in API + DB schema · CI.
- **Pass:** 0 biometric references server-side; any device-local unlock remains client-only. **Notes:** device biometric may gate local app access only.

### TST-CON-08 — JWT lifetimes & rotation
- **Constraint:** C-08 · **Status:** DESIGNED
- **Asserted:** access token 15 minutes, refresh token 7 days, refresh single-use with rotation; reuse revokes the session family.
- **Type / Method / Env:** security integration · decode issued tokens; replay a used refresh token; clock-shift expiry checks · staging.
- **Pass:** expired access → 401 at 15 min; refresh valid ≤ 7 days; second use of same refresh → family revoked + user alert (`BR-AUTH-05`). **Notes:** `SEC-REQ-003`, `AC-SR003-01/02/03`, ≤5 devices (C-08).

### TST-CON-09 — Exactly 17 order states
- **Constraint:** C-09 · **Status:** DESIGNED
- **Asserted:** **state count == 17 and no other states exist in code** — the enumeration equals `03-system-analysis/state-transitions.md` §1 exactly.
- **Type / Method / Env:** unit (state machine) · enumerate the `OrderState` enum/constant at runtime and diff against the canonical list; assert DB CHECK constraint contains the same 17 values; assert 17/17 state-machine tests exist and pass · CI.
- **Pass:** set equality (17 expected, 0 extra, 0 missing), DB constraint matches, all transitions from the canonical table pass and forbidden transitions return `409 STATE_CONFLICT`. **Notes:** `AC-FR012-01` demands 17/17 coverage; an 18th state anywhere = CRITICAL.

### TST-CON-10 — Master / sub-order architecture
- **Constraint:** C-10 · **Status:** DESIGNED
- **Asserted:** one master order per checkout, one sub-order per vendor; master total = Σ sub-order totals; payment/escrow at master level, fulfillment/payout per sub-order.
- **Type / Method / Env:** integration · 3-vendor cart checkout; assert row structure and totals; dispute one sub-order and observe scoped freeze · CI, staging.
- **Pass:** 1 master + N subs created atomically; totals reconcile exactly; master completes only when all subs settle (`BR-ORD-07`). **Notes:** `AC-FR011-04`, `BR-ORD-02`.

### TST-CON-11 — Merchant return policy
- **Constraint:** C-11 · **Status:** DESIGNED
- **Asserted:** `isReturnable=false` or elapsed `returnPeriodDays` (measured from delivery confirmation) rejects the return request.
- **Type / Method / Env:** rule integration · boundary fixtures: not-returnable product; day N-1 vs day N+1 after delivery · CI.
- **Pass:** eligible request accepted; ineligible rejected with policy error and 0 return rows; window start = delivery confirmation timestamp. **Notes:** `AC-FR016-01`, `BR-RET-01`.

### TST-CON-12 — 7-day escrow hold
- **Constraint:** C-12 · **Status:** DESIGNED
- **Asserted:** escrow releases to vendor payable no earlier than 7 days after DELIVERED, and never while a dispute or return is open.
- **Type / Method / Env:** integration with clock-shift harness · run release job at day 6.99 (no release), day 7.0 (release), day 7 with dispute (no release) · staging.
- **Pass:** single release, exactly once, only under allowed conditions; DISPUTED blocks release (`BR-ESC-02`, `BR-ORD-05`). **Notes:** `AC-FR014-01/02`.

### TST-CON-13 — Stock reservation TTL
- **Constraint:** C-13 · **Status:** DESIGNED
- **Asserted:** checkout hold lasts 15 minutes then auto-releases; permanent deduction happens only on payment; never below zero.
- **Type / Method / Env:** integration + timer + concurrency · seed reservation at t0; advance timer to 15:01; concurrent last-unit checkouts · CI.
- **Pass:** release restores availability at TTL+1 s; paid order deducts exactly once (idempotent replay); stock ≥ 0 always. **Notes:** `AC-FR005-01/02/03`, `BR-CAT-07`.

### TST-CON-14 — Order value bounds
- **Constraint:** C-14 · **Status:** DESIGNED
- **Asserted:** **orders accepted only in the inclusive range 500–5,000,000 YER**; 499 and 5,000,001 are rejected.
- **Type / Method / Env:** validation boundary · API matrix: 499 (reject), 500 (accept), 5,000,000 (accept), 5,000,001 (reject), plus non-integer/negative amounts · CI.
- **Pass:** boundary values behave exactly as above with 0 order rows for rejects and a specific validation error code; totals computed server-side (BR-CRT-04). **Notes:** `AC-FR011-01`, `BR-CAT-04`; fixture pair in DOC-TST-005 §4.

### TST-CON-15 — Cart guards
- **Constraint:** C-15 · **Status:** DESIGNED
- **Asserted:** ≤50 distinct products, ≤10 units per product, ≤5 vendors per cart — each limit rejects at +1.
- **Type / Method / Env:** validation boundary · fixture carts at 50/51 products, 10/11 units, 5/6 vendors · CI.
- **Pass:** at-limit carts proceed to checkout; +1 attempts rejected with limit errors and 0 cart mutation. **Notes:** `AC-FR010-01/02`, `BR-CRT-01`.

### TST-CON-16 — No GPS + 6-digit delivery code
- **Constraint:** C-16 · **Status:** DESIGNED
- **Asserted:** **no GPS/location field is requested, stored or returned anywhere**; delivery completes only via 6-digit code, 3 failures → 24 h lock + support ticket.
- **Type / Method / Env:** static + E2E · schema/API/log scan for `lat`, `lng`, `location`, `geo`, `gps` fields + full delivery journey E2E (correct code; then 3 wrong codes) · staging.
- **Pass:** 0 location fields in API contract, DB schema, payloads, logs and mobile builds; OUT_FOR_DELIVERY → DELIVERED only via valid code; 3rd failure locks confirmation 24 h and auto-creates a ticket. **Notes:** `AC-FR015-02/03/05`, `BR-SHP-02/03/05`, `BR-ORD-08`; courier photo proof (BR-SHP-07) contains no geodata.

### TST-CON-17 — Domestic-only shipping zones
- **Constraint:** C-17 · **Status:** DESIGNED
- **Asserted:** shipping zones cover only Yemeni governorates/districts; foreign destinations cannot be configured or delivered.
- **Type / Method / Env:** config integration · attempt zone configs for domestic (accept) and foreign addresses (reject) · staging.
- **Pass:** foreign zone/address rejected; checkout with non-Yemeni address impossible. **Notes:** `AC-FR008-04`.

### TST-CON-18 — 100% custom build
- **Constraint:** C-18 · **Status:** DESIGNED
- **Asserted:** no commerce platform (Shopify/Medusa/WooCommerce/Saleor or similar) dependency exists in the manifest.
- **Type / Method / Env:** dependency audit · scan `package.json` + lockfile + licenses for platform packages · CI.
- **Pass:** 0 platform packages; marketplace logic is first-party. **Notes:** overlaps TST-CON-20 (queue) — this test covers commerce engines only.

### TST-CON-19 — PostgreSQL 16 only
- **Constraint:** C-19 · **Status:** DESIGNED
- **Asserted:** PostgreSQL 16 is the only relational database in every environment.
- **Type / Method / Env:** deploy config review · inspect compose files, Prisma datasource, CI services · CI + staging.
- **Pass:** single `postgres:16` datasource everywhere; 0 other RDBMS images/clients. **Notes:** `C-19`, `ADR` consistency.

### TST-CON-20 — BullMQ only queue
- **Constraint:** C-20 · **Status:** DESIGNED
- **Asserted:** BullMQ (Redis-backed) is the only job/queue system; no RabbitMQ, Kafka, or other broker.
- **Type / Method / Env:** dependency audit · scan manifest + infra for broker packages/images; queue names follow `{block}.{entity}.{action}` · CI.
- **Pass:** 0 foreign broker references; all queues BullMQ. **Notes:** `BR-PLT-01`.

### TST-CON-21 — Modular monolith, zero boundary violations
- **Constraint:** C-21 · **Status:** DESIGNED
- **Asserted:** the system is a modular monolith; 0 cross-module boundary violations; no microservices deployment units.
- **Type / Method / Env:** architecture lint · dependency rules between the 13 block modules fail the build on violation · CI.
- **Pass:** 0 violations in module graph; single deployable unit. **Notes:** `AC-NFR-009-01`, `ADR-002`.

### TST-CON-22 — Docker Compose only
- **Constraint:** C-22 · **Status:** DESIGNED
- **Asserted:** deployment is Docker + Docker Compose; no Kubernetes manifests or helm charts exist.
- **Type / Method / Env:** deploy config review · scan repo for `kind: Deployment`, Helm charts, k8s manifests · CI.
- **Pass:** 0 k8s artifacts; `docker compose up` healthy in ≤ 30 min (`AC-NFR-016-01`). **Notes:** `ADR-004`.

### TST-CON-23 — Greenfield
- **Constraint:** C-23 · **Status:** DESIGNED
- **Asserted:** no legacy-system migration, ETL-for-coexistence, or compatibility shims exist.
- **Type / Method / Env:** scope audit · search for legacy adapters/`from_legacy`/dual-write paths + schema-migration review · CI + review.
- **Pass:** migrations are forward-only schema evolution (`DATA-REQ-005`), never legacy sync. **Notes:** expand-contract is not "migration" — see plan §h.

### TST-CON-24 — Arabic-first, exactly two locales
- **Constraint:** C-24 · **Status:** DESIGNED
- **Asserted:** `ar` is the default locale, `en` full parity; exactly two locales exist; RTL applied by default.
- **Type / Method / Env:** i18n scan + E2E · locale inventory (exactly `ar`, `en`), key-parity scan, default-locale E2E on all surfaces, RTL assertions · CI + staging.
- **Pass:** 100% key parity, 0 hardcoded strings, default `ar` with `dir=rtl`, English switch complete. **Notes:** `AC-NFR-013-01/02`, plan §f.

### TST-CON-25 — 10,000 concurrent users
- **Constraint:** C-25 · **Status:** DESIGNED
- **Asserted:** **10,000 concurrent users are sustained within NFR-001 budgets.**
- **Type / Method / Env:** load (k6) · PERF-01 steady hold at 10,000 VUs for 30 minutes + PERF-04 checkout mix on prod-like staging · staging (prod-like digests).
- **Pass:** p95 read < 200 ms, p95 write < 500 ms, error < 0.1% across the whole window; CPU/mem/pool thresholds (`AC-NFR-003-02`). **Notes:** `AC-S-05`, `NFR-003`, plan §b.

### TST-CON-26 — 99.99% availability SLO
- **Constraint:** C-26 · **Status:** DESIGNED
- **Asserted:** availability ≥ 99.99% monthly (≤ 4.32 min downtime), with RTO ≤ 1 h and RPO ≤ 15 min.
- **Type / Method / Env:** monitoring + drill (verification method, not a single test) · (1) external 60-s probes on critical routes with availability computed over rolling 30 days post-launch (`AC-NFR-005-01`); (2) staging simulated outage → alert within 1 min (`AC-NFR-005-02`); (3) quarterly DR restore drill timed to RTO 1 h / RPO 15 min (`AC-NFR-006-01`, `AC-S-17`, plan §d CHAOS-06).
- **Pass:** probe availability ≥ 99.99% over any rolling 30 days; alerting fires per spec; drill report shows RTO/RPO met with ledger reconciling 0 lost money. **Notes:** pre-launch the SLO is verified by method readiness (probes + drill green); the numeric SLO is proven in production windows.

## 3. Execution Rules

1. All 26 tests run as an automated sweep (`AC-XCUT-02`) before every release candidate; results attach to `19-traceability/`.
2. Any FAIL of TST-CON-01…16 or 18…22 is a CRITICAL defect (constraint violation) — release blocked.
3. A constraint change requires a new constraint document version **and** an update here; IDs are never reused.
4. Test-level detail (method, environment) may be refined as implementations appear; the asserted outcome may only change if `project-constraints.md` changes first.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial register (26 tests) | Initial analysis |
