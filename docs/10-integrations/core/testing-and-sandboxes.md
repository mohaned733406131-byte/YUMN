---
document_id: DOC-INT-008
title: Integration Testing Strategy — Sandboxes, Contract Tests & Go-Live
category: 10-integrations
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: [INT-REQ-001, INT-REQ-002, INT-REQ-003, INT-REQ-004, INT-REQ-005, INT-REQ-006, INT-REQ-007, INT-REQ-008]
related_documents: [DOC-INT-000, DOC-INT-001, DOC-INT-002, DOC-INT-003, DOC-INT-004, DOC-INT-005, DOC-INT-007, DOC-IR-000]
---

# Integration Testing Strategy & Sandboxes

How each external integration is proven before it touches production traffic — and how the abstraction (`INT-REQ-008`) keeps swapping or adding providers cheap. Test cases live in `13-testing/`; this file defines the strategy, environments, drills, and go-live gates.

## 1. Test Pyramid for Integrations

| Layer | What it proves | Runs where | Network |
|---|---|---|---|
| **Unit** | Adapter mapping, error taxonomy normalization, retry math | CI | none (`NFR-010`) |
| **Contract tests** | Every adapter satisfies the *same* port contract | CI against **mock adapters** | none |
| **Sandbox integration** | Real provider behavior: happy path + negatives | staging, provider sandbox | provider sandbox only |
| **Chaos/drill** | Failover, outage, DLQ, replay behavior | staging with fault injection | simulated failures |
| **E2E (lab)** | Carrier-real SMS/OTP, real devices | test-device lab (`DEP-12`) | real carriers, non-prod |

## 2. Environments & Mocks per Provider

| Integration | Mock (CI) | Sandbox (staging) | Production gate |
|---|---|---|---|
| m-Floos / OneCash (`INT-REQ-001`) | `MockPaymentAdapter` — scripted success/fail/duplicate/mismatch/forged-callback fixtures | provider sandbox credentials (issue only after `DEP-05` opens) | `AC-IR001-05`: sandbox acceptance suite must pass **before** production credentials are used |
| Bank transfer (`INT-REQ-002`) | none needed (no external API) — fixtures for queue/decision flows | staging admin console with seeded pending requests | admin SOP + audit review |
| SMS primary/secondary (`INT-REQ-003`) | `MockSmsAdapter` with delay/error injection to trigger failover | provider sandbox/shortcode certification; DLR webhook replay fixtures | both providers pass the failover suite; `DEP-06` certification |
| WhatsApp (`INT-REQ-004`) | `MockWhatsAppAdapter` incl. template-rejection responses | Business API test number | template approval evidence for every catalog entry |
| Push FCM/APNs (`FR-017`) | `MockPushAdapter` (invalid-token scenarios) | sandbox FCM project / APNs sandbox topic | real-device lab verification (`DEP-12`) |
| Delivery orchestration (`INT-REQ-005`) | `MockDeliveryAdapter` / internal engine | staging with fake courier accounts | race + code-lock tests green |
| Observability (`INT-REQ-007`) | — | staging Prometheus/Grafana live | alert fire drill passed |

**Hard rule:** staging and CI run **fake providers only — no real money, no real customer messaging** (`INFERENCE` operational rule; sandbox-before-production is `VERIFIED` for `DEP-05`/`DEP-06`). Production credentials exist only in the production environment and are unreachable from CI (`secrets-management.md` §3, env separation).

## 3. Contract Tests (the abstraction proof)

One shared suite, executed against **every** adapter implementation (`AC-IR008-04`):

| Contract clause | Assertion |
|---|---|
| Port signatures | initiate/send/poll functions accept only normalized DTOs (integer YER, phone, reference) |
| Error taxonomy | each injected vendor failure maps to exactly one of `TIMEOUT / REJECTED / PROVIDER_DOWN / SIGNATURE_INVALID`; unknown errors → `PROVIDER_DOWN`, never an escaping exception |
| Timeout discipline | adapter honors the 10 s budget (injected slow response) |
| Idempotency | duplicate callback/txn ID → single effect at every layer |
| No leakage | static scan: zero vendor identifiers in domain code, API schemas, log statements (`AC-IR008-03`) |
| Boundary | import/lint rule fails build if a vendor SDK is referenced outside its adapter folder (`AC-IR008-01`) |
| Substitution | mock ↔ sandbox swap with **zero domain edits** (`AC-IR008-02`) |

## 4. Chaos Drills (provider DOWN simulations)

| Drill | Injection | Expected outcome | Canon |
|---|---|---|---|
| SMS primary timeout | primary adapter latency > 10 s | automatic secondary send inside OTP window; no duplicate on primary success | `AC-IR003-01/02` |
| Both SMS providers down | both adapters error | WhatsApp OTP fallback; if that fails → honest unavailable state + on-call alert | `AC-IR003-04` |
| Wallet provider circuit open | repeated `PROVIDER_DOWN` | top-up option disabled, bank-transfer path offered, no worker pile-up | `INT-REQ-001` failure, `NFR-007` |
| Callback storm | replay one callback 10× fast | one credit; 200s all round; no alert fatigue | `AC-IR001-02`, `AC-IR006-01` |
| Forged callback | bad signature + expired timestamp | 401, security metric, zero effect | `AC-IR001-04`, `AC-IR006-02` |
| Handler poison | always-failing domain handler | 3 retries with increasing backoff → DLQ → alert → admin replay works | `AC-IR006-03` |
| Queue backlog | suspend workers | user-facing read paths unaffected; backlog drains after resume; DLQ depth alert fires | `BR-PLT-02`, `NFR-007` |
| Observability down | stop Prometheus scrape | zero user impact; `up == 0` alert | `INT-REQ-007` |
| Delivery race | two couriers accept simultaneously | exactly one assignment, other gets conflict | `AC-IR005-01` |
| Push provider down | FCM/APNs error | messages present in in-app center; DLQ alert if persistent | `FR-017`, `BR-PLT-02` |

Drills run on a cadence before launch and after any provider/adapter change; results recorded in `13-testing/`.

## 5. Reconciliation Job Testing

| Test | Seed | Assertion | Canon |
|---|---|---|---|
| Balanced books | randomized operation sequence | Σ debits == Σ credits at every checkpoint | `NFR-008`, `BR-PAY-06` |
| Clean match | provider statement == ledger | report shows zero mismatches | `BR-ESC-08` |
| Amount mismatch | statement entry differs from ledger | mismatch flagged, finance alert, **no silent correction** | `BR-ESC-08`, `BR-FIN-03` |
| Missing credit | provider charged, platform has no credit | surfaced for manual decision (never auto-credit) | `INT-REQ-002` principle, `INFERENCE` |
| Duplicate guard | replayed callback fixture after credit | still exactly one credit | `AC-IR001-02` |
| Compensating entry path | forced imbalance | correction only via compensating posting — raw UPDATE/DELETE rejected | `DATA-REQ-007` |
| Escrow/stock invariants | escrow release + dispute fixtures | release never beats an active dispute (targets `SEC-015`) | `BR-ESC-02`, `BR-ORD-05` |

## 6. SMS Failover Drill (dedicated)

1. Stub primary to time out → assert secondary send occurs **and** the OTP verifies within its 5-minute window (`AC-IR003-01`).
2. Stub primary to succeed → assert **no** secondary attempt (`AC-IR003-02`).
3. Stub both to fail → assert WhatsApp fallback attempt + alert reaches on-call (`AC-IR003-04`).
4. Replay DLR fixtures → assert per-message status recorded with correlation ID (`AC-IR003-03`).
5. Real-carrier pass (`DEP-12` lab): send to test SIMs on each carrier, measure p95 delivery (target < 10 s, `INFERENCE`), verify sender ID and content in ar and en.

## 7. Go-Live Checklist per Integration

| # | Gate | Evidence required |
|---|---|---|
| 1 | Contract suite green against the production-bound adapter | CI run |
| 2 | Sandbox E2E green (happy + all negative fixtures) | `AC-IR001-01…04`, `AC-IR004-01…04` equivalents |
| 3 | Chaos drills executed (failover, forged callback, DLQ/replay) | drill report in `13-testing/` |
| 4 | Secrets provisioned in production env only; rotation owner named | `SEC-REQ-007` audit |
| 5 | Webhook endpoints reachable over TLS; allowlists + replay window configured | config review (`SEC-REQ-006`, `SEC-005`) |
| 6 | Rate budgets active on integration-facing routes | `SEC-REQ-009` config |
| 7 | Metrics, dashboards, DLQ alerts live and fire-drilled | `AC-IR007-01/02/04` |
| 8 | Reconciliation scheduled and seeded with a known-clean day | `BR-FIN-03` |
| 9 | Provider commercial certification complete (`DEP-05`/`DEP-06` status → Available) | `DOC-OVR-010` |
| 10 | Runbook entry: outage → degradation banner → recovery → post-check | `NFR-020`, `15-deployment/` |
| 11 | Privacy check: no PII/OTP/secrets in logs/metrics of the new path | `AC-SR002-02`, `AC-IR007-03` |
| 12 | Rollback: adapter can be disabled by config (circuit-open) without redeploy | `NFR-007` |

## 8. Why the Abstraction Keeps Swaps Cheap (`INT-REQ-008`)

| Change | Work required | Work avoided |
|---|---|---|
| Replace one SMS provider | new adapter + contract suite run + config change | zero edits to auth/notification domain code |
| Add a third wallet provider | new `PaymentProviderPort` implementation + fixtures + go-live checklist | no changes to wallet/ledger/order modules |
| Move sandbox → production | credential + endpoint swap in env | no code change |
| Future external delivery fleet | `DeliveryProviderPort` implementation | shipping domain untouched (`INT-REQ-005`, `AC-IR005-04`) |
| Provider API version bump | adapter-internal change only | domain, API contracts, and clients unaffected |

Proof is enforced, not assumed: architecture lint (`AC-IR008-01`), substitution test (`AC-IR008-02`), leak scan (`AC-IR008-03`), contract parity (`AC-IR008-04`) — all merge-blocking in CI (`NFR-009`).

## 9. Related Findings & Risks

| ID | Topic |
|---|---|
| `SEC-011` | `DEP-06` uncontracted — the whole SMS/WhatsApp test plan is blocked until it opens |
| `SEC-005` | replay-window parameters must be pinned before webhook drills are meaningful |
| `RISK-003` / `RISK-006` | provider commercial risks tracked in `17-risk-management/core/risk-register.md` |
| `GAP` registry | provider API specifics pending `DEP-05` documentation access (`../../20-validation/core/missing-information.md`) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
