---
document_id: DOC-SEC-002
title: Threat Model — Assets, Trust Boundaries, STRIDE & Top Threats
category: 09-security
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-003, SEC-REQ-004, SEC-REQ-005, SEC-REQ-008, SEC-REQ-009, SEC-REQ-010, SEC-REQ-011, FR-013, FR-015]
related_documents: [DOC-SEC-001, DOC-SEC-004, DOC-SEC-007, DOC-SEC-008, DOC-BA-005, DOC-OVR-008, DOC-OVR-010]
---

# Threat Model (STRIDE)

**Scope:** the yumn modular monolith (`C-21`) with its four surfaces (customer web `Next.js 14`, vendor panel, admin console, React Native apps `0.73`), PostgreSQL 16, Redis 7, Elasticsearch 8, MinIO, BullMQ workers, and the external providers of `DEP-05`/`DEP-06`. Method: STRIDE per trust boundary, then a ranked threat register. Threat IDs `TM-NN` are stable references for `13-testing/` and `17-risk-management/`.

## 1. Assets

| ID | Asset | Sensitivity | Adversary goal | Where it lives |
|---|---|---|---|---|
| A-01 | Wallet balances (customer funds) | CRITICAL | Steal / inflate balance | PostgreSQL `b07` schema, in-memory cache is derived only |
| A-02 | Escrow-held funds & vendor payables | CRITICAL | Release early, redirect payout | PostgreSQL, escrow jobs (BullMQ) |
| A-03 | Double-entry ledger (append-only) | CRITICAL | Hide theft by rewriting history | PostgreSQL `DATA-REQ-007` |
| A-04 | Authentication material (bcrypt hashes, JWT RS256 keys, refresh sessions) | CRITICAL | Impersonate any user | PostgreSQL, Redis session registry, env secrets |
| A-05 | OTPs and delivery codes (short-lived secrets) | HIGH | Bypass verification, fake delivery | Redis (TTL), SMS/WhatsApp channels |
| A-06 | PII: phone, name, address (≈ identity graph) | HIGH | Mass doxxing, targeted SIM-swap prep | PostgreSQL, Elasticsearch, logs |
| A-07 | KYC documents & bank-transfer receipts | HIGH | Identity fraud | MinIO (`DEP-07`), PostgreSQL references |
| A-08 | Admin console capabilities (refunds, KYC decisions, role changes, payouts) | CRITICAL | Exercise privilege for money/data | `PlatformAdminModule` (`B13`) |
| A-09 | Provider credentials & webhook signing secrets (`DEP-05`, `DEP-06`) | CRITICAL | Forge callbacks, hijack OTP sending | Environment / secrets store (`SEC-REQ-007`) |
| A-10 | Platform reputation & availability (`C-26` 99.99%) | HIGH | Degrade trust, block registration | Whole system |

## 2. Trust Boundaries

```text
TB-1  Public internet ──► WAF/CDN (DEP-08) ──► Node API (NestJS)
      [customer web · vendor panel · RN apps]      │
TB-2  API / workers ──► PostgreSQL 16 · Redis 7 · Elasticsearch 8 · MinIO
TB-3  Vendor portal & Courier app ──► API   (tenant-scoped principals inside TB-1,
                                            treated as separate boundary because of
                                            cross-tenant blast radius)
TB-4  Admin console ──► API  (privileged principal; same origin today — see SEC-003)
TB-5  External providers ──► inbound webhooks / outbound calls
      (m-Floos, OneCash, SMS primary/secondary, WhatsApp Business)
```

## 3. STRIDE per Boundary

| Boundary | S — Spoofing | T — Tampering | R — Repudiation | I — Info disclosure | D — DoS | E — Elevation |
|---|---|---|---|---|---|---|
| **TB-1** public → API | Forged/fake identity via guessed OTP; session token theft | Request body tampering; price/qty manipulation before server recompute (`BR-CRT-04`) | Denied orders/refunds without trail | Token/OTP sniffing on HTTP; XSS reading data | Request floods, OTP pumping, bot scalping | Calling hidden admin endpoints from a customer token (`SEC-REQ-004`) |
| **TB-2** API → data stores | Connecting as a rogue service using leaked DB creds | UPDATE/DELETE of ledger/audit rows; injection via string-built SQL | Log rewriting to erase evidence | DB dump, backup theft, ES/MinIO bucket exposure | Connection exhaustion; Redis outage takes down rate limits/queues | A compromised app container reads all schemas (no column ACL in v1) |
| **TB-3** vendor/courier portals | Stolen vendor staff credentials; self-escalation to Owner (`BR-VND-06`) | Cross-store writes (`BR-VND-07`); fake delivery-code attempts | Vendor disputes courier/customer claims | Vendor A reads vendor B's orders/products; courier sees non-assigned deliveries | Inventory/order endpoint abuse | Staff role escalation; courier acting outside assigned shipment |
| **TB-4** admin console | Admin password/OTP theft (single origin, shared cookie — `SEC-003`) | Bulk data edits; disabling security settings | Admin denies a refund/KYC decision (`BR-PLT-06` counters) | Full PII/KYC/ledger visibility leaks | Admin actions on money endpoints without quotas | ADMIN → SUPER_ADMIN escalation; moderator exceeding content scope |
| **TB-5** providers ↔ yumn | Forged webhook claiming a payment succeeded | Altered amount/status in callback; replayed old callback | Provider and yumn disagree on a transaction | Provider credentials in logs; OTP codes in logs | Provider outage blocks registration/top-ups; callback floods | Provider-controlled data interpreted as trusted commands |

## 4. Threat Register — Top Threats & Mitigations

| ID | Threat | STRIDE | Boundary | Mitigation (design) | Mapped to | Residual risk |
|---|---|---|---|---|---|---|
| **TM-01** | Account takeover via SIM swap + OTP interception, or password reset abuse | S, I | TB-1, TB-5 | OTP bound to purpose/session, 5-min expiry, 3 attempts, single-use (`SEC-REQ-001` R1–R3); reset invalidates all sessions (`BR-AUTH-07`); security notices mandatory (`BR-NTF-02`) so victim is alerted | `SEC-REQ-001`, `BR-AUTH-03`, `BR-AUTH-07`, `FR-001` | **HIGH residual:** platform cannot detect carrier-level SIM swap — mitigated only by mandatory post-reset alert + device-session cap (`BR-AUTH-06`); see `SEC-004` |
| **TM-02** | OTP bombing / SMS pumping (attacker triggers OTPs to victim numbers or burns SMS budget) | D | TB-1, TB-5 | Resend cooldown 60 s, ≤3 resends/10 min (`BR-AUTH-03`); per-IP + per-account budgets stricter than standard (`SEC-REQ-009`); failover must not multiply sends (`AC-IR003-02`) | `SEC-REQ-009`, `SEC-REQ-005`, `INT-REQ-003` | **MEDIUM residual:** budget cap is per design (`INFERENCE`, `security-controls.md` §5); multi-IP distributed pumping needs per-destination limits — accepted |
| **TM-03** | Wallet double-spend / double-credit: race on balance debit, or duplicate provider callback crediting twice | T, E | TB-2, TB-5 | Row-level locking + never-negative atomic check (`BR-PAY-05`); idempotency keys on money ops (`BR-PAY-08`, `BR-PLT-03`); credit only on verified callback/poll (`BR-PAY-03`); callback idempotency (`AC-IR001-02`) | `SEC-REQ-010`, `FR-013`, `BR-PAY-05/06/08`, `DATA-REQ-006` | **LOW residual:** depends on correct transaction scoping in code — verified by concurrency + Σdebits=Σcredits tests (`NFR-008`) |
| **TM-04** | Ledger / audit tampering to hide theft (UPDATE/DELETE of postings or audit rows) | T, R | TB-2, TB-4 | Append-only enforced by DB privileges — app role holds no UPDATE/DELETE on ledger & audit tables (`DATA-REQ-007`, `SEC-REQ-010` R1); hash-chained audit verified by job (`SEC-REQ-010` R4); corrections only as compensating entries | `SEC-REQ-010`, `DATA-REQ-007`, `BR-PAY-06`, `BR-PLT-06` | **MEDIUM residual:** a host-level DBA (superuser) can still rewrite rows — no external WORM/anchor in v1; see `SEC-002` |
| **TM-05** | Vendor data snooping: vendor A reads vendor B's products/orders/finances | I, E | TB-3 | `store_id` scoping at service layer (`BR-VND-07`); ownership on every query (`DATA-REQ-008`); deny-by-default matrix (`SEC-REQ-004`); cross-tenant tests `AC-FR002-01/02` | `SEC-REQ-004`, `BR-VND-07`, `DATA-REQ-008`, `FR-002` | **LOW residual:** requires every repository method to carry the scope — enforced by matrix test suite (`AC-SR004-01`) |
| **TM-06** | Delivery-code fraud: courier or bystander guesses/observes the 6-digit code and fakes delivery | S, E | TB-3 | Code issued only at OUT_FOR_DELIVERY (`BR-SHP-02`); 3 attempts → 24 h lock + auto support ticket (`BR-SHP-03`, `SEC-REQ-005` R3); stored hashed (`INT-REQ-005`); proof = code + timestamp + courier identity (`BR-SHP-07`) | `SEC-REQ-005`, `C-16`, `FR-015`, `BR-SHP-02/03` | **HIGH residual:** no GPS to corroborate; SMS interception (SIM swap) defeats the code — see `SEC-004`; lockout converts guessing to an observable event |
| **TM-07** | Admin privilege abuse: rogue ADMIN issues refunds, approves fraudulent KYC, changes roles, freezes wallets | E, R, T | TB-4 | ADMIN/SUPER_ADMIN separation — role & permission management is SUPER_ADMIN only (`rbac.md`, `DOC-OVR-007`); every privileged/money action audit-chained (`BR-PLT-06`, `SEC-REQ-010` R2); deny-by-default + route-level guard | `SEC-REQ-004`, `SEC-REQ-010`, `FR-020`, `BR-PLT-06` | **MEDIUM residual:** no second factor beyond password+session at admin login (canon tension — `SEC-012`); same-origin console (`SEC-003`) |
| **TM-08** | Webhook spoofing: attacker POSTs a forged "payment success" or DLR to credit a wallet / manipulate status | S, T | TB-5 | HMAC-SHA256 signature with constant-time compare, IP allowlist, replay window on timestamp (`INT-REQ-001`, `INT-REQ-006`); invalid signature → 401 + security metric (`AC-IR006-02`); secrets env-only (`SEC-REQ-007`) | `SEC-REQ-007`, `INT-REQ-006`, `BR-PAY-03` | **LOW residual:** window length and nonce store are design-level choices — recorded `INFERENCE` in `10-integrations/webhook-reliability.md` (`SEC-005`) |
| **TM-09** | Stored XSS in Arabic/RTL content (product names, reviews, store profiles) stealing admin/customer sessions | T, E, I | TB-1 | Context-aware output encoding regardless of locale/RTL (`SEC-REQ-008` R2); CSP without `unsafe-inline` (R3); upload validation blocks SVG/HTML (`SEC-REQ-011` R4); JSON API + React escaping by default | `SEC-REQ-008`, `SEC-REQ-011`, `C-24`, `FR-006` | **LOW residual:** correctness depends on never using `dangerouslySetInnerHTML`/`innerHTML` for UGC — enforced by lint rule + browser-driven test `AC-SR008-02` |
| **TM-10** | Promotion/coupon abuse: coupon stacking, over-discount, self-dealing via fake accounts | T, E | TB-1 | One coupon per order, never stack (`BR-PRM-02`); ≤90% discount bound (`BR-PRM-01`); validation before order row exists (`BR-PRM-06`); server-side recompute of totals (`BR-CRT-04`); usage limits per-user/global (`BR-PRM-04`) | `SEC-REQ-004`, `FR-019`, `BR-PRM-01…06` | **MEDIUM residual:** mass-account farming for per-user limits is only throttled by OTP rate limits (`TM-02`); monitoring metric on new-account coupon use |
| **TM-11** | Bot scalping / automation: inventory grabbing, catalog scraping, quota abuse | D | TB-1 | Rate limits 100 req/min standard, stricter on checkout/top-up (`SEC-REQ-009`); 15-min reservation TTL (`C-13`) bounds hoarding; cart guards (`C-15`) | `SEC-REQ-009`, `C-13`, `C-15`, `FR-010` | **MEDIUM residual:** no bot management/WAF rules beyond `DEP-08` CDN in v1 — accepted for launch, revisit via `SEC-008` register |

> Note: threats are cross-referenced in `security-findings.md` where the design itself leaves an open gap (`SEC-001…SEC-015`), and in `17-risk-management/risk-register.md` where a business risk exists (`RISK-003`, `RISK-006`).

## 5. Out-of-Scope Threats (explicitly excluded by canon)

| Excluded threat | Why excluded |
|---|---|
| Card-data theft / PCI scope | No cards accepted anywhere (`C-02`) — no PAN exists to steal |
| Cryptocurrency wallet draining | No crypto (`C-04`) |
| GPS/location tracking abuse | Platform never requests or stores courier location (`C-16`, `BR-SHP-05`) |
| Email phishing for account recovery | No email channel for auth (`C-06`, `BR-AUTH-08`) |
| Microservice lateral movement | Modular monolith, single trust domain (`C-21`) |
| Supply-chain compromise of a commerce platform | 100% custom build (`C-18`); dependency supply chain is handled by `SEC-REQ-012` scanning instead |

## 6. Residual Risk Summary

| Residual risk | Level | Owner follow-up |
|---|---|---|
| SIM-swap defeats OTP + delivery code (TM-01, TM-06) | HIGH | `SEC-004`; consider carrier-level binding signals post-launch |
| No MFA/step-up for privileged accounts (TM-07) | HIGH | `SEC-012`; resolve login-OTP ambiguity before implementation |
| Ledger immutability bounded by DB privilege model (TM-04) | MEDIUM | `SEC-002`; periodic chain verification job + restricted superuser access |
| Admin console same-origin with public API (TM-07) | MEDIUM | `SEC-003`; separate origin or hardened cookie scoping |
| SMS/WhatsApp dependency uncontracted (`DEP-06` NOT STARTED) | CRITICAL (delivery) | `SEC-011`, `RISK-006` — Phase 0 gate |
| Webhook replay window parameters unspecified | MEDIUM | `SEC-005`; fix ±5 min window + nonce store at implementation |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
