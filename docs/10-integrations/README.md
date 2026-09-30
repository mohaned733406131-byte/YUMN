---
document_id: DOC-INT-000
title: Integrations Domain — Overview & File Index
category: 10-integrations
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-001, INT-REQ-002, INT-REQ-003, INT-REQ-004, INT-REQ-005, INT-REQ-006, INT-REQ-007, INT-REQ-008]
related_documents: [DOC-ROOT-001, DOC-REQ-001, DOC-IR-000, DOC-OVR-010, DOC-SEC-001]
---

# 10 — Integrations Domain Overview & File Index

## 1. Purpose

This directory owns the **integration contracts**: concrete endpoints, payload schemas, provider-specific failure matrices, sequence detail, and degradation behavior for every external system yumn talks to. The *requirements* (provider-agnostic guarantees with `AC-IRnnn-nn`) live in `02-requirements/`; the *security policy* for shared controls lives in `09-security/`. Nothing here redefines a requirement — it expands it.

## 2. External-System Map

| System | Direction | Protocol | Purpose | References |
|---|---|---|---|---|
| m-Floos (mobile-money) | yumn → provider (initiate), provider → yumn (signed callback) + poll fallback | HTTPS REST, HMAC-SHA256 callback | Wallet top-up credit (`C-05`) | `INT-REQ-001`, `DEP-05` |
| OneCash (mobile-money) | yumn → provider, provider → yumn + poll fallback | HTTPS REST, HMAC-SHA256 callback | Wallet top-up credit (`C-05`) | `INT-REQ-001`, `DEP-05` |
| Bank transfer (customer → bank → yumn) | customer → yumn (evidence), ops → bank portal (verification) | Manual + web portal | Top-up credited only after admin verification | `INT-REQ-002`, `BR-PAY-04` |
| SMS primary (Telesom and/or Sabafon) | yumn → provider; DLR provider → yumn | HTTPS API, signed DLR webhook | OTP + transactional SMS (primary) | `INT-REQ-003`, `DEP-06` |
| SMS secondary (failover) | yumn → provider | HTTPS API | OTP/transactional failover target | `INT-REQ-003`, `DEP-06` |
| WhatsApp Business API | yumn → provider (templates); status provider → yumn | HTTPS Graph-style API, signed webhooks | Template notifications + OTP failover (`BR-NTF-03`) | `INT-REQ-004`, `DEP-06` |
| Internal courier fleet | yumn → couriers (offer/assign), courier app → yumn (scans, code) | Internal API (RN app) | Delivery orchestration v1 — no external fleet API | `INT-REQ-005`, `C-16` |
| Future external delivery fleet | yumn → provider (reserved) | behind `DeliveryProviderPort` | Substitutable later without domain changes | `INT-REQ-005`, `INT-REQ-008` |
| FCM (Google) | yumn → FCM; devices → yumn (token lifecycle) | HTTPS API | Android push delivery | `FR-017`, `DEP-01` stack |
| APNs (Apple) | yumn → APNs; devices → yumn | HTTPS API (`.p8`) | iOS push delivery | `FR-017` |
| Prometheus / Grafana / Alertmanager | services ← scrape; alerts → on-call | HTTP scrape + alert routing | Observability export, alerting | `INT-REQ-007`, `NFR-014` |
| CDN / edge / TLS (Cloudflare-class) | clients → edge → API | HTTPS | TLS termination, DDoS hygiene, cert lifecycle | `DEP-08`, `SEC-REQ-006` |

**Explicitly absent (by canon):** card processors, BNPL, crypto rails, email service providers (`C-01`–`C-04`, `BR-NTF-01`/`GAP-03`), GPS/tracking providers (`C-16`), external IAM/SSO (`FR-002` out of scope), microservice brokers (`C-20` — BullMQ only).

## 3. File Index

| # | Filename | DOC ID | Purpose | Source of truth |
|---|---|---|---|---|
| 1 | `README.md` | DOC-INT-000 | This file — domain overview, external-system map, index | Yes |
| 2 | `integration-overview.md` | DOC-INT-001 | Integration-layer architecture: ports/adapters, sync vs async, retries/idempotency/circuit breakers, degradation matrix, observability export | Yes |
| 3 | `wallet-providers.md` | DOC-INT-002 | m-Floos + OneCash top-up contract: flow, signatures, idempotency, limits, failure states, reconciliation | No |
| 4 | `bank-transfer-topup.md` | DOC-INT-003 | Manual bank-transfer top-up: evidence, admin verification queue, credit/reject paths, fraud checks | No |
| 5 | `sms-provider.md` | DOC-INT-004 | SMS integration: templates, failover, DLRs, budgets, latency and degradation modes | No |
| 6 | `whatsapp-business.md` | DOC-INT-005 | WhatsApp Business: approved templates, opt-in/out, conversation windows, OTP channel policy | No |
| 7 | `push-notifications.md` | DOC-INT-006 | FCM + APNs: token lifecycle, payload contract, topics, quiet hours, fallbacks | No |
| 8 | `webhook-reliability.md` | DOC-INT-007 | Inbound/outbound webhooks: HMAC, replay window, idempotency, retry schedule, DLQ + replay | No |
| 9 | `testing-and-sandboxes.md` | DOC-INT-008 | Provider testing strategy: sandboxes, contract tests, chaos drills, go-live checklists | No |
| [`core/`](core/README.md) | DOC-INT-009 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-INT-010 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-INT-011 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-INT-012 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-INT-013 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## 4. Requirement Coverage Map

| INT-REQ | Title | Primary file | Also covered in |
|---|---|---|---|
| INT-REQ-001 | Wallet top-up providers | `wallet-providers.md` | `integration-overview.md` §4, `webhook-reliability.md` |
| INT-REQ-002 | Bank transfer top-up | `bank-transfer-topup.md` | `testing-and-sandboxes.md` §2 |
| INT-REQ-003 | SMS provider failover | `sms-provider.md` | `integration-overview.md` §4, `whatsapp-business.md` §1 |
| INT-REQ-004 | WhatsApp Business notifications | `whatsapp-business.md` | `push-notifications.md` §7 (channel fallbacks) |
| INT-REQ-005 | Delivery orchestration | `integration-overview.md` §1 (`DeliveryProviderPort`) | `testing-and-sandboxes.md` §4 |
| INT-REQ-006 | Webhook robustness | `webhook-reliability.md` | `integration-overview.md` §5, `../09-security/core/security-controls.md` |
| INT-REQ-007 | Observability export | `integration-overview.md` §7 | `webhook-reliability.md` §4 (DLQ alerting) |
| INT-REQ-008 | Provider abstraction | `integration-overview.md` §1 | every provider file + `testing-and-sandboxes.md` §3/§8 |

## 5. Who Consumes the Integration Layer

| Consumer (domain module) | Uses | Key rules it must not re-implement |
|---|---|---|
| Identity & Access (`B01`) | SMS/WhatsApp OTP ports | `BR-AUTH-03` OTP parameters, failover semantics |
| Payment & Wallet (`B07`) | payment ports, webhook credit path, bank queue | `BR-PAY-03/04/06/08` — never credit on client claim |
| Notifications (`B10`) | SMS, WhatsApp, push ports | `BR-NTF-01…05` channel/preference rules |
| Shipping & Delivery (`B08`) | `DeliveryProviderPort` | `BR-SHP-02/03/04` — code confirmation, first-accept |
| Platform Admin (`B13`) | DLQ replay UI, verification queues | `SEC-REQ-010` audit on every replay/decision |

## 6. Shared Conventions (summary — detail in `integration-overview.md`)

- **Ports & adapters:** domain code depends only on `PaymentProviderPort`, `SmsProviderPort`, `WhatsAppPort`, `DeliveryProviderPort` with normalized DTOs and an error taxonomy (`TIMEOUT`, `REJECTED`, `PROVIDER_DOWN`, `SIGNATURE_INVALID`) — no vendor type ever leaks (`INT-REQ-008`).
- **Flow:** initiate → signed callback → poll fallback → idempotent finalization.
- **Timeouts:** 10 s per outbound call. **Retries:** 3× exponential backoff → DLQ with alert (`BR-PLT-02`, `BR-PLT-01`).
- **Idempotency:** provider transaction/message ID as key; N deliveries → 1 effect (`BR-PAY-08`, `BR-PLT-03`).
- **Webhooks:** HMAC-SHA256 + constant-time compare, IP allowlist, replay window, secrets from environment only (`SEC-REQ-007`).
- **Environments:** sandbox certification before production credentials (`DEP-05`, `DEP-06` gates).
- **Correlation:** every call/callback carries a correlation ID surfaced in logs, metrics, and DLQ entries (`NFR-014`).
- **Money in integer YER** everywhere; no floats cross any boundary (`BR-PAY-10`).

## 7. Dependency Risk Snapshot (from `DOC-OVR-010`)

| DEP | Status | Integration impact |
|---|---|---|
| `DEP-05` m-Floos + OneCash merchant API | **NOT STARTED** | Blocks production top-ups; fallback = bank transfer (`INT-REQ-002`) → `RISK-003` |
| `DEP-06` SMS + WhatsApp Business approval | **NOT STARTED** (Phase 0 gate) | Blocks registration/OTP → `RISK-006` |
| `DEP-07` MinIO | Available | Uploads/media |
| `DEP-08` Domains/TLS/CDN | Not started | Launch gate for HTTPS edge |
| `DEP-12` Test device lab + carrier SIMs | Not started | E2E OTP/failover drills |

## 8. Reading Order

| Audience | Read |
|---|---|
| New engineer | DOC-INT-000 → `integration-overview.md` → the provider file you touch |
| Payments engineer | `wallet-providers.md` → `bank-transfer-topup.md` → `webhook-reliability.md` |
| Notifications engineer | `sms-provider.md` → `whatsapp-business.md` → `push-notifications.md` |
| QA / release owner | `testing-and-sandboxes.md` → provider files' failure sections |
| Security reviewer | `integration-overview.md` §6 → `webhook-reliability.md` → `09-security/` |

## 9. Domain Boundaries

**Owned here:** provider contracts, degradation behavior, webhook mechanics, integration testing strategy.
**Not owned here:** requirement statements/ACs (`02-requirements/`); job/queue mechanics of the monolith (`../06-backend/core/background-processing.md`); endpoint contracts toward yumn's own clients (`07-api/`); alert routing detail (`../12-non-functional/core/observability.md`); environment wiring (`14-devops-infrastructure/`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-INT-009…DOC-INT-013) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
