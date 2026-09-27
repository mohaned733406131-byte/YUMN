---
document_id: DOC-TST-005
title: Test Data & Environments
category: 13-testing
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [DATA-REQ-002, DATA-REQ-006, NFR-013, SEC-REQ-007]
related_documents: [DOC-TST-001, DOC-TST-002, DOC-TST-003, DOC-TST-004, DOC-DTA-004, DOC-INT-008]
---

# Test Data & Environments

Where yumn is tested, with what data, and under which PII rules. Consumes the provider sandbox rules from `10-integrations/testing-and-sandboxes.md` (DOC-INT-008) and the masking rules from `16-data/data-classification.md` (DOC-DTA-004). Produces the fixtures referenced by every plan in [test-plans.md](test-plans.md).

---

## 1. Environment Matrix

| Env | Purpose | Stack | Data | Providers | Real PII? |
|---|---|---|---|---|---|
| **local** | Developer loop; unit/API runs | `docker compose up` on a laptop (C-22): PG 16, Redis 7, ES 8, MinIO, BullMQ | seeded fixtures, resettable | mock adapters | no |
| **dev (shared)** | Branch CI integration runs, demo | same compose file, shared host | per-run isolated schema/tenant | mock adapters | no |
| **staging** | E2E, perf, DAST, chaos, drills | **prod-like**: same image digests as prod (`AC-NFR-016-01`), full observability stack | seeded fixtures + masked copies | **fake/sandbox only — no real money, no real customer messaging** (`DOC-INT-008` §2) | no (masked) |
| **prod-like (pre-release)** | Release rehearsal: load at C-25 scale, DR/rollback (plan §h) | prod digests, scaled-down replicas | masked restore of prod-shape data | sandbox credentials | masked per §6 |
| **production** | Service only — **no tests** beyond passive probes and post-release smoke | real | real | real | real |

Parity rule: staging and prod-like must use identical image digests and configuration shape so tests mean what they claim; environment drift is itself a defect (`AC-NFR-016-01`, `NFR-016`). Production secrets are unreachable from any test environment (`SEC-REQ-007`).

## 2. What Is Real vs Fake

| Dependency | CI / local | Staging | Production |
|---|---|---|---|
| PostgreSQL 16 / Redis 7 / ES 8 / MinIO / BullMQ | real containers | real containers | real |
| m-Floos / OneCash wallet top-ups | `MockPaymentAdapter` scripted fixtures | **provider sandbox only** (after `DEP-05`); mock otherwise | real |
| Bank transfer top-up | fixtures + admin-decision flows | seeded pending requests in admin console | real |
| SMS / WhatsApp OTP | `MockSmsAdapter` (delay/error injection) | provider sandbox / test number (after `DEP-06`) | real |
| Push FCM/APNs | `MockPushAdapter` | sandbox projects; real devices via `DEP-12` | real |
| Delivery couriers | fake courier accounts | fake courier accounts | internal engine (`INT-REQ-005`) |
| Email | **does not exist in v1** (GAP-03) — never configured | — | — |

**Hard rule:** no test run anywhere moves real money or messages real customers (`DOC-INT-008` §2). Money-cycle proofs (`AC-XCUT-01`) run entirely against mock/sandbox ledgers.

## 3. Seed & Fixture Strategy

1. **Fixtures are code.** Seed scripts live in the repository and run as a versioned step (`seed:test`); no hand-inserted rows on shared environments. Every seed run is deterministic (fixed RNG seed) so failures reproduce.
2. **Isolation.** Each CI run gets its own schema or tenant prefix; tests never share mutable rows.
3. **Invariant on load.** A fixture batch that violates the property it exists to protect fails the seed: ledger Σ = 0, stock ≥ 0, order totals within C-14.
4. **Two personas per role.** Every actor (Customer, Vendor, Delivery Provider, Admin, Super Admin, Moderator) has at least two seeded accounts so ownership tests (TC-011–014) always have a "me" and an "other".
5. **Bilingual by construction.** Names, addresses, product titles and review text exist in both `ar` and `en` so every journey can run in either locale (NFR-013).

**Seed pipeline (executed in this order on every environment build):**

```text
migrations → base fixtures (actors, stores, zones) → domain fixtures (products, stock, coupons)
→ money fixtures (wallets, ledger batches, escrow positions) → state fixtures (orders per state)
→ search index build (ES) → invariant assertions (Σ ledger = 0, stock ≥ 0, totals within C-14)
```

A failure at any step aborts the environment build — tests never run against a half-seeded environment.

## 4. Fixture Catalog

| Fixture set | Values | Protects |
|---|---|---|
| **Reserved test phones** | block **`79xxxxxxx`** (`790000000`–`799999999`) for all seeded/fixture accounts; every test phone must match `^7[0-9]{8}$` (BR-AUTH-01). Ad-hoc steps in individual TCs may use any syntactically compliant number registered inside the test environment, provided it does not collide with the reserved block | `BR-AUTH-01`, `C-06` |
| **Arabic + English content** | paired product titles/descriptions, store names, addresses (governate/district/street), review text, notification templates; Arabic-Indic numerals for money display | `C-24`, `NFR-013`, `BR-NTF-04` |
| **Money boundaries (orders)** | `499` (reject), `500` (accept), `5,000,000` (accept), `5,000,001` (reject) YER | `C-14`, `TST-CON-14`, `AC-FR011-01` |
| **Money boundaries (top-ups)** | `999` (reject), `1,000` (accept), `5,000,000` (accept), `5,000,001` (reject) YER | `BR-PAY-02`, `AC-FR013-01` |
| **Cart limits** | `50` products (accept) / `51` (reject); `10` units (accept) / `11` (reject); `5` vendors (accept) / `6` (reject) | `C-15`, `TST-CON-15`, `AC-FR010-01/02` |
| **17 order-state fixtures** | one order (master + sub) per canonical state — PLACED … DISPUTED — with correct history rows, escrow position and wallet position for that state | `C-09`, `TST-CON-09`, plans §a/§d |
| **Wallet ledger fixtures** | balanced batches (Σ debit = Σ credit = 0), zero-balance wallet, frozen wallet, escrow-held funds, payable below/above 1,000 YER; invariant **RISK-001 (zero ledger imbalance)** asserted after every seed and reconciliation run | `BR-PAY-05/06`, `AC-S-14`, `RISK-001` |
| **Coupon edges** | discount `90%` (accept) / `91%` (reject); validity `90` days (accept) / `91` days (reject); expired, fully-used, min-amount-not-met, second-coupon-on-order | `BR-PRM-01/02/06`, `AC-FR019-01/02/03` |
| **OTP timing** | valid-within-5-min code; expired code; attempt counter at 2 (allowed) and 3 (blocked); resend at 59 s (blocked) and 61 s (allowed); third resend inside 10 minutes (blocked) | `BR-AUTH-03`, `AC-FR001-05`, `SEC-REQ-005` |
| **ES index content** | Arabic queries with alef variants (أ/إ/ا), diacritics, common typos, mixed ar/en tokens; soft-deleted and inactive products that must never surface | `AC-FR009-01/02`, `BR-CAT-06` |
| **Delivery codes** | correct 6-digit code; wrong codes for the 3-attempt lockout; codes near TTL; courier + buyer pairs for first-accept race | `C-16`, `BR-SHP-02/03/04` |
| **KYC documents** | masked sample identity documents (never real IDs), oversized/malformed/SVG uploads for negative cases | `SEC-REQ-011`, `AC-SR011-01/02` |

Timer-dependent fixtures (stock TTL 15 min, OTP 5 min, escrow 7 days, return inspection 72 h, refund ≤ 3 business days) are driven by an injectable clock — tests never sleep through wall-clock windows ([testing-strategy.md](testing-strategy.md) §9).

### 4.1 Load & volume datasets

| Dataset | Shape | Used by |
|---|---|---|
| Nominal staging data | ~50k products, ~5k users, ~10k orders — realistic ar/en mix | PERF-01…06, E2E, DAST (plan §b/§c) |
| Synthetic volume | 10M products, 100M order-line records for capacity checks | `AC-NFR-017-01` volume load + EXPLAIN review |
| k6 parameter files | user/phone/credential pools drawn from the reserved `79xxxxxxx` block; per-VU carts and wallets pre-funded | all k6 scenarios |
| Concurrency pools | ≥ 30 distinct wallet-funded customers and ≥ 10 courier accounts for 10k-VU runs | `TST-CON-25`, first-accept race (`BR-SHP-04`) |

## 5. Fixture Ownership & Refresh Cadence

| Item | Owner | Refresh cadence |
|---|---|---|
| Seed scripts & fixture data files | QA lead (testing domain), reviewed with the owning domain author | on change of schema or rule; reviewed each release |
| Environment parity (digests) | DevOps (`14-devops-infrastructure/`) | every release + weekly drift check |
| Masked prod-shape restore (prod-like) | Data owner (`16-data/`) | quarterly, or before any DR/rollback rehearsal; always re-masked per §6 |
| ES index fixtures | Search domain owner | on analyzer/settings change; otherwise per seed run |
| Adapter mock fixtures (payment/SMS) | Integrations owner (`10-integrations/`) | on provider contract change (`DEP-05`/`DEP-06` status changes) |
| Device-lab builds & SIM inventory | QA (`DEP-12`) | per release candidate |

Refresh is a **versioned event**: seed script bump → CI re-seed → invariant assertions run → failure blocks the pipeline (a broken fixture is a broken test gate, not a warning). Fixture deprecation follows the same change-management rules as documents (root README §9).

**Reset & cleanup:** local/dev environments are disposable — reset by full re-seed, never by surgical row edits. Staging is re-seeded nightly after E2E runs and on demand before perf/DAST windows; prod-like is reset only together with a masked restore (§6). Test-created entities (orders, tickets, reviews) carry a `seeded_by`/run-ID marker so cleanup and defect triage can separate fixture noise from real state.

## 6. PII Policy in Non-Production

| Rule | Detail |
|---|---|
| No production PII by default | Non-prod is built from synthetic fixtures (§4); production rows never enter CI/local |
| Masked restores | Any restore of prod-shaped data into prod-like is masked first, per `16-data/data-classification.md`: phone/email → **MASK-02**, names/addresses/free text → **MASK-04**, OTP/document bytes/secrets → **MASK-03**, financial identifiers → **MASK-05** (amounts kept only where a test needs them), provider/JWT keys → **MASK-06** (never copied) |
| Logs & reports | Test runs assert no secrets/PII in logs (`AC-NFR-014-01`); test reports and defect attachments use masked screenshots/values |
| Secrets | Sandbox credentials only; production secrets exist only in production (`SEC-REQ-007`) |
| Deletion | Non-prod PII-like data is ephemeral; environments are reset rather than archived; retention class RC-01/RC-03 applies (`retention-and-archival.md`) |
| Compliance | The policy implements `DATA-REQ-002` (minimization) and is auditable against the MASK rules (`AC-DR002-*`) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
