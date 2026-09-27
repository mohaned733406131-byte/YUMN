Kimi
Co-authored with Senior Eng. Salah Alssayani — Taizz University, Alsaeed Faculty of Engineering & IT, Department of Software Engineering (eng.salahalssayani@gmail.com)
License: GPL-3.0
# YUMN_RULES — Project-Specific Rule Catalog

Every rule: stable ID · severity · requirement · mechanical verification.
Severity: **CRITICAL** = blocks completion · **HIGH** = pass or justify in writing · **MEDIUM** = expected · **LOW** = guidance.

These rules bind the stack-agnostic master catalog (`RULES.md`) to the yumn domain, derived from the
approved knowledge base in `docs/` (`C-01…C-26`, 99 `BR-*`, 68 requirements, `SEC-REQ-*`, `NFR-*`).
IDs are stable: never renumbered, never reused. Precedence: see `RULES_HINTS.md` §7.
Verification commands are listed in `RULES_HINTS.md` §3.

---

## MNY — Money, Wallet & Ledger

| ID | Sev | Rule | Verification |
|---|---|---|---|
| MNY-01 | CRITICAL | Orders are paid **wallet-only**; COD, cards, BNPL and crypto are rejected everywhere (`C-01…C-04`, `BR-PAY-01`). | `TST-CON-01` + contract test: non-wallet method ⇒ `400 PAYMENT_METHOD_NOT_ALLOWED`; DB CHECK `ck_payment_method_wallet_only`. |
| MNY-02 | CRITICAL | All money is **integer YER** (bigint) — no floats, no decimals, no currency conversion (`BR-PAY-10`). Percentages are basis points. | DTO gates `@IsInt()`; unit tests on money math; CI grep for float money types. |
| MNY-03 | CRITICAL | Every balance change posts **balanced double-entry rows**; Σ `amount_yer` per `entry_group_id` = 0, global Σ ledger = 0 (`BR-PAY-06`, `NFR-008`). | CI seed assertion "Σ ledger = 0"; invariant test; daily reconciliation job alert on mismatch. |
| MNY-04 | CRITICAL | Ledger tables are **append-only** (`wallet_transaction`, `order_status_history`, `audit_log`): no UPDATE/DELETE ever; corrections are compensating `ADJUSTMENT` rows (`DATA-REQ-007`). | DB role grants = `SELECT, INSERT` only; immutability negative test in CI. |
| MNY-05 | CRITICAL | Wallet balance **never goes negative** — row-level lock + atomic check inside the transaction (`BR-PAY-05`). | Concurrency test (parallel debits) ⇒ zero negative rows, zero deadlocks (`NFR-003`). |
| MNY-06 | CRITICAL | **`Idempotency-Key` is mandatory** on order create, top-up, payment authorize/capture, refund, payout, coupon validate, cart merge; replay returns the stored response verbatim, fingerprint mismatch ⇒ `409` (`BR-PLT-03`). | Contract tests per endpoint; key storage TTL 24 h; 409-on-conflict test. |
| MNY-07 | CRITICAL | Top-ups credit **only** on verified provider callback / reconciled poll (m-Floos, OneCash) or **admin verification** of a bank reference — never from a client claim (`BR-PAY-03/04`). | Integration test: forged client "credited" claim rejected; webhook signature + replay-window tests. |
| MNY-08 | CRITICAL | Amount bounds enforced at every layer: order **500–5,000,000 YER**, top-up **1,000–5,000,000 YER** (`C-14`, `BR-PAY-02`). | DB CHECKs + DTO validation + boundary tests at ±1. |
| MNY-09 | HIGH | VAT **15% × (subtotal − coupon discount)**, shipping untaxed, half-up rounding to whole YER **per sub-order**, remainder to `ROUNDING_ACCOUNT` (`BR-FIN-01/02/05`). | Golden-number tests (e.g. 100,000 → 15,000 VAT, total 117,000 with 2,000 shipping). |
| MNY-10 | HIGH | Refunds credit the **wallet only** (no external cash-out except vendor payouts) within **3 business days** of `REFUNDED` (`BR-PAY-07`, `BR-RET-04`). | Return-flow test asserts wallet credit + timestamp; no payout created for buyer refunds. |
| MNY-11 | HIGH | A **frozen** wallet can neither pay nor top up, but **does** receive refunds (`BR-PAY-09`). | Test matrix: frozen ⇒ pay/top-up denied, refund credited. |
| MNY-12 | HIGH | Money, order, ledger, escrow and session responses are never cached or SSR'd: `Cache-Control: no-store`, deny-list enforced (`docs/06-backend/caching.md`). | Response-header test + deny-list CI check (a cache decorator on a denied route fails CI). |
| MNY-13 | HIGH | Provider secrets, callback HMACs and card-like data never touch logs; webhook verification uses constant-time compare + IP allowlist + replay window (`INT-REQ-006`). | Log-sampling test (0 secrets/PII in 1,000-line extract); webhook negative tests. |

## ESC — Escrow, Commission & Payouts

| ID | Sev | Rule | Verification |
|---|---|---|---|
| ESC-01 | CRITICAL | Escrow hold starts at `DELIVERED` and lasts **7 days**; release requires elapsed time AND no active dispute AND state ∉ {`DISPUTED`,`RETURN_*`,`REFUNDED`} (`C-12`, `BR-ESC-01/02`). | `TST-CON-12`; release-job tests for each blocking condition. |
| ESC-02 | CRITICAL | Commission = (line subtotal after coupon) × per-vendor rate **500–2000 bps (default 1000)**, computed **at release**; later refund ⇒ proportional reversal (`BR-ESC-03/04`). | Golden tests at 5%/10%/20% + reversal math; DB CHECK `ck_escrow_rate_band`. |
| ESC-03 | CRITICAL | Refunds draw **escrow first, then vendor payable** — vendor liability, never platform float (`BR-ESC-07`). | Refund test asserts ledger posting order and balances. |
| ESC-04 | HIGH | Payouts execute in batches **3–7 business days** after release, minimum **1,000 YER** (below ⇒ `ROLLED_OVER`), only for `KYC=APPROVED`, non-suspended stores (`BR-ESC-05/06`). | Payout batch tests: minimum, rollover, KYC/suspension gating. |
| ESC-05 | HIGH | **Daily reconciliation**: ledger vs wallet vs escrow vs payable vs provider statements; any mismatch alerts finance (`BR-ESC-08`, `BR-FIN-03`, `API-ANL-009`). | Reconciliation job test + induced-mismatch alert test. |
| ESC-06 | HIGH | A dispute freezes escrow **only for its own sub-orders**; master `COMPLETED` waits for every sub-order ∈ {`COMPLETED`,`REFUNDED`} (`BR-ORD-05/07`). | Dispute test: unaffected sub-orders still release. |
| ESC-07 | HIGH | Payout and ledger operations are covered by the ≥95% `b07` coverage floor and the 100% critical-path rule (`DOD-04`). | Coverage report per module. |

## ORD — Order Lifecycle & State Machine

| ID | Sev | Rule | Verification |
|---|---|---|---|
| ORD-01 | CRITICAL | **Exactly 17 order states**; transitions only per `docs/03-system-analysis/state-transitions.md`; any other transition ⇒ `409 STATE_CONFLICT` — never 500 (`C-09`, `BR-ORD-01`). | `TST-CON-09` (17/17), enum-count test, full transition-matrix test. |
| ORD-02 | CRITICAL | One **master order** per checkout, one **sub-order per vendor**; master total = Σ sub-totals; payment and escrow are master-level, allocated per sub-order (`C-10`, `BR-ORD-02`). | Deferred constraint `ct_order_totals_match_suborders` + service tests. |
| ORD-03 | CRITICAL | Order creation requires an **idempotency key**; duplicates return the original order (`BR-ORD-06`). | Duplicate-POST test returns same `order_no`. |
| ORD-04 | CRITICAL | `DELIVERED` is reachable **only** through successful 6-digit code verification (`C-16`, `BR-ORD-08`). | `TST-CON-16`; no admin/courier shortcut test. |
| ORD-05 | HIGH | Every state change appends to `order_status_history` with actor, timestamp, reason (`BR-ORD-03`). | Timeline endpoint test; backstop trigger test. |
| ORD-06 | HIGH | Cancellation windows: customer at `PLACED`/`CONFIRMED`; vendor/admin until `READY_FOR_PICKUP`; any cancellation triggers the wallet refund flow (`BR-ORD-04`). | Window tests per role; refund asserted on every cancel path. |
| ORD-07 | HIGH | Concurrent transitions use optimistic `version` locking: first valid wins, loser gets `409` (`docs/03-system-analysis/state-transitions.md` §5). | Race test (two simultaneous transitions) ⇒ one 200, one 409. |
| ORD-08 | HIGH | ⚠ **Unspecified today:** semantic precedence when `COMPLETED → RETURN_REQUESTED` races `COMPLETED → DISPUTED` (funds outcome undefined). Decide and record it (ADR + state table) **before** implementing that path — do not invent a rule in code. | ADR exists; transition row added; race test added. |
| ORD-09 | MEDIUM | Still `CONFIRMED` 24 h after confirmation escalates to admin review with notification — never a silent auto-cancel (`BR-ORD-10`). | SLA job test. |

## IDT — Identity, OTP & Sessions

| ID | Sev | Rule | Verification |
|---|---|---|---|
| IDT-01 | CRITICAL | Primary identifier is phone matching **`^7[0-9]{8}$`**, unique platform-wide; no email-primary or social login (`BR-AUTH-01`, `C-06`). | DTO regex test; uniqueness test; no login-by-email endpoint test. |
| IDT-02 | CRITICAL | Passwords: **≥8 chars, bcrypt cost 12**, never logged; PII (phone/email/street) AES-256 encrypted at rest with hash for lookup (`SEC-REQ-002`, `DB-001/002`). | Password-policy test; log-scan test; ciphertext-at-rest assertion. |
| IDT-03 | CRITICAL | OTP: **6 digits, 5-min expiry, 3 attempts, 60-s cooldown, ≤3 resends/10 min**; SMS primary with automatic WhatsApp failover inside the validity window (`BR-AUTH-03`, `BR-NTF-03`). | `SEC-REQ-001` ACs; failover test; 4th-attempt-rejected test. |
| IDT-04 | CRITICAL | JWT **RS256**, access **15 min**, refresh **7 days single-use** rotation; refresh reuse revokes the whole session family; max **5** devices (`C-08`, `BR-AUTH-05/06`). | Token-expiry boundary tests (14:59 pass / 15:00 fail); reuse-revocation test; 6th-login evicts oldest. |
| IDT-05 | CRITICAL | Server-side, **deny-by-default** authorization on every non-public endpoint; ownership violation on another tenant's resource ⇒ **404**, in-scope but forbidden ⇒ 403 (`SEC-REQ-004`). | Role × endpoint matrix tests for all 7 roles; IDOR suite. |
| IDT-06 | HIGH | **5** consecutive failed logins ⇒ **15-minute** lock (`423`), lock events logged; password reset invalidates all sessions (`BR-AUTH-04/07`). | Lockout test; post-reset session test. |
| IDT-07 | HIGH | Delivery/OTP codes and passwords never appear in logs, URLs, analytics, or error messages; generic responses on auth entry points prevent enumeration (`SEC-REQ-002`, error-model §5). | Log-sampling review; enumeration test. |

## STK — Stock, Cart & Checkout Guards

| ID | Sev | Rule | Verification |
|---|---|---|---|
| STK-01 | CRITICAL | **No oversell**: atomic stock deduction, generated `qty_available`, `ck_inventory_no_negative`, `FOR UPDATE` row lock (`BR-CAT-07`). | Concurrent-checkout test ⇒ zero oversell; constraint-presence test. |
| STK-02 | HIGH | Cart limits **≤50 products, ≤10 units each, ≤5 vendors**; reservation TTL **15 minutes**, expiry releases stock (`C-15`, `C-13`, `BR-CRT-01/02`). | Boundary tests at 50/10/5; TTL expiry test. |
| STK-03 | HIGH | Totals are **always recomputed server-side** at checkout; a price change forces customer re-confirmation (`BR-CRT-04`). | Tampered-price POST test; re-confirmation flow test. |
| STK-04 | HIGH | Checkout requires **wallet balance ≥ order total** at confirmation (`BR-CRT-06`, `C-01`). | Insufficient-funds test ⇒ `422 INSUFFICIENT_FUNDS`, no order row. |
| STK-05 | HIGH | Inactive / out-of-stock / out-of-policy lines **block checkout** until removed (`BR-CRT-05`). | Blocked-checkout test per condition. |
| STK-06 | MEDIUM | Guest cart merges on login with server-wins conflict resolution; merge is idempotency-keyed (`BR-CRT-03`). | Merge conflict test; duplicate-merge test. |

## SHP — Delivery & Code Confirmation

| ID | Sev | Rule | Verification |
|---|---|---|---|
| SHP-01 | CRITICAL | **No GPS / no location data anywhere**: no coordinate columns, no location SDK, no geofencing; optional proof photo is never required (`C-16`, `BR-SHP-05`). | `TST-CON-16`; schema scan (no lat/lng columns); dependency audit for geolocation SDKs. |
| SHP-02 | CRITICAL | 6-digit code issued at `OUT_FOR_DELIVERY`; attempts 1–2 show remaining, **3rd failure locks confirmation 24 h** and auto-creates a support ticket (`BR-SHP-02/03`). | `SEC-REQ-005` ACs; attempt-counter test; lock + ticket test. |
| SHP-03 | CRITICAL | Code stored only as **hash ≥32 bytes + nonce**, never plaintext; never logged (`DB-013`, `ck_shipment_code_hash`). | DB constraint test; log-scan test. |
| SHP-04 | HIGH | Courier assignment: same-zone offers, **first accept wins** via optimistic locking (`BR-SHP-04`). | Race test: two couriers accept ⇒ one wins, one 409. |
| SHP-05 | HIGH | **3 failed delivery attempts** ⇒ escalate to admin with full timeline; delivery proof = code + timestamp + courier identity (`BR-SHP-06/07`). | Escalation job test; proof-assertion test. |

## RET — Returns, Refunds & Disputes

| ID | Sev | Rule | Verification |
|---|---|---|---|
| RET-01 | HIGH | Return window = delivery confirmation + `returnPeriodDays`; `isReturnable=false` or window elapsed ⇒ rejected (`C-11`, `BR-RET-01`). | `TST-CON-11`; boundary tests at exactly on/off the window. |
| RET-02 | HIGH | Vendor inspection after `RETURN_RECEIVED` must conclude within **72 h**, else auto-approve (`BR-RET-05`). | SLA job test with frozen clock (no wall-clock dependence, `NFR-010`). |
| RET-03 | HIGH | Refund = item value; shipping refunded only for platform/vendor fault; triggers proportional commission reversal and escrow adjustment (`BR-RET-03/07`). | Refund-math golden tests. |
| RET-04 | CRITICAL | Admin is final arbiter on policy/dispute conflicts; every privileged money decision writes an audit-log entry (`BR-RET-06`, `BR-PLT-06`). | Audit-row assertion on each admin money action. |
| RET-05 | HIGH | Dispute vocabulary must be single-sourced: the API (`OPEN/RESOLVED_BUYER/RESOLVED_VENDOR`) and DB (`OPEN/UNDER_REVIEW/RESOLVED` + resolution enum) currently disagree — reconcile before coding (`SPE-04`). | ADR/decision recorded; mapping test; no ad-hoc translation layer. |

## RTL — Arabic-First, RTL & Localization

| ID | Sev | Rule | Verification |
|---|---|---|---|
| RTL-01 | CRITICAL | **Arabic is the default locale, full RTL**; exactly `ar` + `en`, no third locale, no machine translation (`C-24`, `NFR-013`). | i18n key scan: 0 missing keys in either locale; locale-config test. |
| RTL-02 | HIGH | **No hardcoded strings** in components — every string comes from the shared catalogs (`BR-PLT-05`). | i18n lint rule fails CI on literals. |
| RTL-03 | HIGH | **No physical CSS properties** — `ml-*/mr-*/pl-*/pr-*/left-*/right-*/text-left/text-right/float` fail CI; logical properties only (`docs/05-frontend/rtl-and-styling.md`). | ESLint `no-physical-properties` rule in CI. |
| RTL-04 | HIGH | Money displays as integer **YER** (`ر.ي`) with **Arabic-Indic numerals** in `ar` (`BR-PAY-10`). | Formatter unit tests per locale. |
| RTL-05 | HIGH | Every notification template exists in **2/2 locales**, language follows user locale, Arabic default (`BR-NTF-04`). | Template-completeness check. |
| RTL-06 | HIGH | Wallet balance, order state and personalized pages are **never SSR/ISR/optimized-cached**; forbidden in client state: computed money totals, authoritative order status, permission decisions (`docs/05-frontend/state-management.md`). | Route-class test; client-state lint/review checklist. |
| RTL-07 | MEDIUM | Optimistic updates are forbidden for: wallet balance/top-up, order placement/cancellation, order state changes, refund/return status, stock availability. | Component review + state-machine test. |

## API — Contract Conformance

| ID | Sev | Rule | Verification |
|---|---|---|---|
| API-01 | CRITICAL | All endpoints live under **`/api/v1`**; breaking change ⇒ `/api/v2` with ≥6-month overlap; error envelope, pagination envelope, auth header and money representation are never versioned. | Contract tests; version manifest check. |
| API-02 | HIGH | Each collection endpoint uses **exactly one** pagination mode (cursor XOR offset); wallet transactions always return exact totals. | Per-endpoint pagination tests; no dual-mode endpoint. |
| API-03 | HIGH | Error responses match the envelope exactly (`code`, localized `message`, `messageKey`, `details[]`, `correlationId`, `retryable`) and use codes from the **closed catalog** in both locales. | Error-contract test suite; no free-text server errors. |
| API-04 | HIGH | Rate limits enforced: **100 req/min** standard; OTP 5/min/IP, login 10/min/IP, top-up and order creation 10/min/user; 429 carries `Retry-After` (`SEC-REQ-009`). | Rate-limit tests per tier. |
| API-05 | HIGH | Every money/order/coupon/refund endpoint requires `Idempotency-Key` and returns `Cache-Control: no-store`. | Header + missing-key ⇒ `400 IDEMPOTENCY_KEY_REQUIRED` tests. |
| API-06 | HIGH | Uploads: jpg/png/webp (PDF for KYC/proofs) ≤5 MB, magic-byte check, AV scan, EXIF/GPS stripped, re-encoded, **no SVG**; counts ≤10 product / ≤5 review / ≤1 proof (`SEC-REQ-011`). | Upload negative tests (413/415/422); EXIF-strip assertion. |
| API-07 | MEDIUM | `X-Correlation-Id` accepted, echoed everywhere and propagated into BullMQ jobs; access logs never contain tokens/OTPs/passwords. | Correlation propagation test; log-scan test. |

## DAT — Database & Migrations

| ID | Sev | Rule | Verification |
|---|---|---|---|
| DAT-01 | CRITICAL | **PostgreSQL 16 only**, Prisma Migrate only, 13 schemas `b01…b13`; module roles may read/FK across schemas but **never write** across schemas (`C-19`). | Schema audit test; cross-schema write attempt fails. |
| DAT-02 | CRITICAL | **No `migrate down` in production**; rollback = forward fix; every change follows **expand→contract** across 3 releases; destructive DDL needs the `contract:` label + backup confirmation. | CI gates M1–M9 (`prisma validate`, drift, destructive scan). |
| DAT-03 | CRITICAL | PKs are **UUIDv7** app-generated; money columns `<name>_yer` bigint; timestamps `*_at` timestamptz; soft delete via `deleted_at`; append-only tables have `created_at` only. | Constraint-presence snapshot tests. |
| DAT-04 | HIGH | Every schema change ships **migration + updated docs in the same commit** (`IMP-06`, `DOC-05`); rollback is rehearsed via restore drill (RTO ≤1 h, RPO ≤15 min). | PR diff contains migration + doc; quarterly drill evidence. |
| DAT-05 | HIGH | Partitioning maintained on `order_item`, `wallet_transaction`, `order_status_history`, `audit_log`; **never `VACUUM FULL`** on financial tables; partition jobs run dry-run first. | Partition maintenance job test; ops runbook check. |
| DAT-06 | HIGH | FK policy: **RESTRICT** for financial/history, CASCADE for owned children, SET NULL for optional lookbacks (`docs/08-database/entity-relationship.md` §2). | FK-register snapshot test (48 relations). |
| DAT-07 | HIGH | App-layer guards that the DB deliberately does not enforce must have tests: return window, 17-state matrix, cart/session/SLA limits, KYC 48-h SLA (`docs/08-database/constraints-and-integrity.md` §5). | Named test IDs mapped in `docs/13-testing/`. |

## OPS — Infrastructure & Deployment

| ID | Sev | Rule | Verification |
|---|---|---|---|
| OPS-01 | CRITICAL | **Docker Compose only** — no Kubernetes, no microservices frameworks, no Kafka/RabbitMQ, no cloud-vendor SDK as a hard dependency (`C-21`, `C-22`, `NFR-016`, ADR-004). | Dependency audit; compose topology test. |
| OPS-02 | CRITICAL | **No secrets in repo, images, or logs**: `.env*` gitignored, secrets host-only mode `0600`, fail-fast on missing var (name only), gitleaks pre-commit + CI = 0 findings (`SEC-REQ-007`). | Secret scan output; image-layer scan; `CONFIG_MISSING` test. |
| OPS-03 | HIGH | Production publishes **exactly ports 80 and 443**; any new published port is a review-blocking change. | Compose diff gate in release checklist. |
| OPS-04 | HIGH | No container gets the Docker socket, `privileged`, or `host` network mode — asserted in CI. | Compose policy assertion test. |
| OPS-05 | HIGH | Deploys are readiness-gated (one replica at a time, `/readyz` green before the next); images digest-pinned in staging/prod; rollback = pull previous tag ≤15 min (`docs/15-deployment/rollback.md`). | Deploy pipeline gate + rollback rehearsal evidence. |
| OPS-06 | HIGH | **E2E never runs against production**; no seeded users in prod; no load tests in prod; staging uses sandbox/fake providers only — no real money (`docs/14-devops-infrastructure/environments.md`). | Workflow permissions review; env-credential separation check. |
| OPS-07 | HIGH | Health: `/healthz` liveness + `/readyz` readiness gate traffic; unhealthy instances removed ≤30 s (`BR-PLT-07`, `NFR-020`). | Health-endpoint test; failure-injection drill. |
| OPS-08 | MEDIUM | Feature flags default **fail-closed (off)**; platform settings can never alter infra topology or constraints `C-01…C-26` (`docs/14-devops-infrastructure/configuration.md`). | Flag-default test; settings-guard test. |

## PRF — Performance & Non-Functional Budgets

| ID | Sev | Rule | Verification |
|---|---|---|---|
| PRF-01 | HIGH | API p95 read **<200 ms**, write **<500 ms**, error rate **<0.1%**, sustained at **10,000** concurrent users for 30 min (`NFR-001/003`, `C-25`). | k6 `PERF-01…07` on staging; report attached to session log. |
| PRF-02 | HIGH | Web **LCP <2.5 s**, INP ≤200 ms, CLS ≤0.1; JS **<200 KB gzipped**, no vendor chunk >100 KB (`NFR-002`). | size-limit + Lighthouse CI fail on exceed. |
| PRF-03 | HIGH | Availability **99.99%** (≤4.32 min/30 d); **RTO ≤1 h, RPO ≤15 min**; WAL ship ≤5 min (`C-26`, `NFR-005/006`). | Uptime SLO dashboard; quarterly restore-drill evidence. |
| PRF-04 | HIGH | Fault tolerance: ES/Redis down ⇒ browse still works, recovery ≤60 s; queue 3 retries ⇒ DLQ with alert ≤1 min; SMS→WhatsApp failover keeps OTP delivery ≥99% (`NFR-007`). | Chaos suite `CHAOS-01…08`. |
| PRF-05 | HIGH | **Zero ledger imbalance, zero negative balances/stock, zero orphan rows, 100% idempotency coverage** (`NFR-008`). | Invariant suite run in CI on seeded data. |
| PRF-06 | MEDIUM | Regression **<30 min** with **0 flakes across 10 consecutive runs**; unit suite **<3 min**; no test depends on wall-clock time (`NFR-010`, `AC-S-09`). | Timed CI runs; 10-run flake report. |
| PRF-07 | MEDIUM | Growth model: 10,000,000 products / 100,000,000 order lines / 5-year retention without re-architecture (`NFR-017`). | Capacity forecast + disk alert at 70%. |

## SPE — Spec Consistency (knowledge-base hygiene)

| ID | Sev | Rule | Verification |
|---|---|---|---|
| SPE-01 | CRITICAL | One source of truth per concept; everywhere else **reference the ID, never copy the definition** (`docs/README.md` §4). | Link check passes; no duplicated rule text in code comments/docs. |
| SPE-02 | CRITICAL | `02-requirements/acceptance-criteria.md` owns all `AC-*` text; requirement files may condense but **never renumber/rewrite AC IDs**. ⚠ Currently violated by `FR-015…FR-020` — fix before deriving tests from FR files. | AC-ID audit: file IDs ≡ registry IDs for all 20 FR files. |
| SPE-03 | HIGH | Never claim an artifact exists without checking the tree. ⚠ Known stale/absent items: `19/20/21` domains referenced but missing, `TC-104…TC-114` declared but absent, `BR-INV-01…05` cited but undefined, `GAP-07` unregistered, "not yet authored" notes for `07-api`/`08-database` that are false. | Existence check script over all referenced IDs/paths; findings logged before any phase closes. |
| SPE-04 | HIGH | When API vocabulary and DB enums disagree (product status, KYC states, notification categories, refund/payout/dispute/return states, ledger types), **stop and reconcile via ADR before writing code** — no ad-hoc mapping layers. | ADR recorded; single vocabulary test for each contested field. |
| SPE-05 | HIGH | Every new ID is registered in its canonical registry **in the same change** (requirements, business rules, endpoints README, entities README, test-cases README). | Registry count assertions in CI/validator. |
| SPE-06 | MEDIUM | Constraints, business rules and NFRs are implemented as tests (`TST-CON-01…26`, `AC-*`) — implementing a feature without its linked `TC-*` is incomplete (`AC-S-03`, DOD-08). | Traceability check: FR → AC → TC, 0 gaps. |

---

## Change Control

Amendments follow `core/00_meta_rules.md` §0.5: propose in the session log → edit here (append/modify, never silently renumber) → bump the adapter version note in `RULES_HINTS.md` §1 → record in `senior-rules/CHANGELOG.md` → re-run `python3 senior-rules/validators/validate.py .`.
Rules exist to catch *you* — never edit a rule mid-task to make a violation disappear.
