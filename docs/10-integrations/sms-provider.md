---
document_id: DOC-INT-004
title: SMS Integration — Templates, Failover & Degradation
category: 10-integrations
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [INT-REQ-003, INT-REQ-004, INT-REQ-006, INT-REQ-008, FR-001, FR-017]
related_documents: [DOC-INT-000, DOC-INT-001, DOC-INT-005, DOC-IR-003, DOC-BA-005, DOC-FR-001, DOC-FR-017]
---

# SMS Integration (`INT-REQ-003`, `DEP-06`)

SMS is the **primary delivery channel for OTPs and transactional messages** — and therefore an authentication-critical dependency (`SEC-REQ-001` R5). Dependency risk is **CRITICAL**: `DEP-06` is `NOT STARTED` and is a Phase 0 gate (`RISK-006`).

## 1. Interface

```text
domain (auth, orders, delivery, security notices)
   │  SmsProviderPort.send(templateId, phone, locale, purpose, correlationId)
   ▼
SmsAdapter ── attempt primary (Telesom and/or Sabafon, DEP-06) ── 10 s timeout
   │              │ timeout / error
   │              ▼
   │         attempt secondary provider  (inside the OTP's 5-min window, BR-AUTH-03)
   ▼
DLR webhook (signed, HMAC + allowlist, INT-REQ-006) → status recorded per message
```

- Single port for all sends — provider choice/failover is configuration, never domain logic (`INT-REQ-008`).
- Transient failures: 3 retries with exponential backoff → DLQ + alert (`BR-PLT-02`, `BR-PLT-01`); **user-triggered** resend attempts remain governed by `BR-AUTH-03` (60 s cooldown, ≤3 resends/10 min).
- Failover fires **only** on timeout/error — a successful primary send never produces a duplicate message (`AC-IR003-02`).

## 2. Templates (ar/en)

| Template class | Purpose | Channel rules | Localization |
|---|---|---|---|
| `otp_registration` | Registration verification | Security — cannot be disabled (`BR-NTF-02`) | ar default + en (`BR-NTF-04`, `C-24`) |
| `otp_password_reset` | Password reset | Security — mandatory | ar/en |
| `otp_sensitive_change` | Phone/payout-sensitive change confirmation | Security — mandatory | ar/en |
| `login_alert` / `password_changed` / `account_locked` | Security notices | Mandatory (`BR-NTF-02`) | ar/en |
| `order_placed` / `order_confirmed` / `order_shipped` / `order_delivered` | Transactional order lifecycle | Opt-out **not** applied to transactional | ar/en |
| `delivery_code` | 6-digit delivery code to buyer at OUT_FOR_DELIVERY | Security-class; code excluded from logs (`INT-REQ-005`) | ar/en |
| `topup_result` / `refund_processed` | Money notices | Transactional | ar/en |
| `payout_released` (vendor) | Finance notice | Transactional | ar/en |
| `marketing_*` | Promotions | **Opt-out honored per channel** (`BR-NTF-05`) | ar/en |

Rules: message bodies with OTP codes are **never written to logs** (`INFERENCE`, extends `SEC-REQ-002` never-logged discipline); templates carry only the minimum parameters (order reference, status — no full PII); every template exists in both locales and follows the user's locale with Arabic default (`AC-IR003`-adjacent, `AC-IR004-04` pattern).

## 3. Sender IDs & Numbers

| Aspect | Design | Canon |
|---|---|---|
| Sender ID | Per-template/per-purpose sender identity where the provider allows (e.g., branded sender for OTP vs transactional) — `INFERENCE`, exact sender registry depends on `DEP-06` carrier agreements | `DEP-06`, `INT-REQ-003` |
| Destination validation | `^7[0-9]{8}$` only — non-Yemeni numbers rejected (`AC-IR003` scope, `BR-AUTH-01`) | `BR-AUTH-01` |
| DLR | Signed delivery-receipt webhook logs sent/delivered/failed per message with correlation ID | `INT-REQ-003` receipts |

## 4. Failover Behavior (primary → secondary)

| Condition | Action | Window |
|---|---|---|
| Primary timeout (> 10 s) | Switch to secondary immediately | must still land inside the OTP's 5-minute validity (`AC-IR003-01`) |
| Primary error response | Switch to secondary | same |
| Primary success | **No** secondary attempt (no duplicates) | `AC-IR003-02` |
| Secondary also fails | WhatsApp fallback for OTP (`BR-NTF-03`); transactional traffic queues and retries | `AC-IR004-01` |
| Both SMS + WhatsApp fail | Registration/verification unavailable; honest localized error with retry guidance; immediate on-call alert | `AC-IR003-04`, `RISK-006` |
| Failover metrics | `sms_failover_total{reason}` exported; alert on rising rate | `INT-REQ-007` |

Both providers must pass the failover suite in sandbox/shortcode certification before production (`DEP-06` gate).

## 5. Rate, Backoff & Cost Controls

| Control | Value | Basis |
|---|---|---|
| User resend cooldown | 60 s | `BR-AUTH-03` |
| User resend cap | ≤3 per 10 min per phone | `BR-AUTH-03` |
| Per-IP OTP request budget | 10 per 10 min (`INFERENCE`) | `SEC-REQ-009`, pump defense (`TM-02`) |
| Per-destination guard | cooldown/caps keyed on hashed destination, globally | `SEC-006` recommendation |
| Send pipeline | queue-based (BullMQ) with 3 retries + backoff → DLQ | `BR-PLT-02` |
| Cost budget | Monthly SMS spend ceiling with alert at 80% (`INFERENCE` — provider cost data arrives with `DEP-06`) | operational control |
| Budget anomaly alert | Sudden spike in send volume → abuse alert (pumping indicator) | `SEC-REQ-009` R5 |

## 6. Latency Budget

| Target | Value | Evidence |
|---|---|---|
| OTP delivery (send → handset) | **< 10 seconds p95** | `INFERENCE` — design target; chosen because the OTP window is 5 min (`BR-AUTH-03`) and `NFR-012` caps registration→first-order at < 5 min; not a canon number |
| Failover decision | ≤ 10 s (primary timeout) + secondary send | `INT-REQ-003` |
| DLR receipt logging | best-effort; recorded when provider delivers it | `INT-REQ-003` |
| Measurement | `sms_send_duration_seconds` histogram + DLR latency correlation in Prometheus | `INT-REQ-007` |

## 7. Degradation Modes & Decisions

| Question | Decision | Rationale |
|---|---|---|
| In-app OTP fallback (show code inside the app)? | **No.** SMS is required for first login and every verification — an in-app code would be visible to anyone holding an unverified device/session and defeats the purpose of out-of-band verification | First-login UX already assumes the handset owns the SIM; an in-app channel for an *unverified* account has no authenticated principal to bind to |
| Email OTP? | **No** — excluded by `C-06`, `BR-AUTH-08`, `GAP-03` | canon |
| WhatsApp as routine OTP channel? | **No** — WhatsApp is only the **automatic failover** when SMS providers fail (`BR-NTF-03`); it is never the primary OTP path | `BR-NTF-03`, `AC-IR004-01` |
| Security notices during user opt-out? | Still sent — opt-out applies to marketing categories only (`BR-NTF-05` vs `BR-NTF-02`) | canon |
| Both providers down | Registration/verification **unavailable**; surfaced honestly with retry guidance; on-call alerted; tracked `RISK-006` | `AC-IR003-04` |

**Impact of provider DOWN on the critical path:** no SMS ⇒ no registration, no password reset, no sensitive-change confirmation, no delivery code delivery — i.e., **the platform cannot onboard or complete deliveries**. This is why `DEP-06` is the Phase 0 gate and why failover + WhatsApp fallback are first-class requirements rather than nice-to-haves.

## 8. Security

| Control | Design |
|---|---|
| Provider API keys | environment only, per-adapter injection (`SEC-REQ-007`, inventory S-06) |
| DLR webhooks | HMAC + constant-time compare + IP allowlist + replay window (`INT-REQ-006`) |
| Abuse prevention | per-IP/per-destination budgets; SMS pumping metrics (`SEC-REQ-009`) |
| Log hygiene | OTP bodies and phone numbers excluded from logs/metrics (`SEC-REQ-002`, `SEC-REQ-006` R5) |
| Compliance posture | written no-log guarantee requested from provider during `DEP-06` contracting (`SEC-011` recommendation) |

## 9. Verification

| Test | Assertion | Canon |
|---|---|---|
| Failover | simulated primary timeout → secondary delivers inside the OTP window | `AC-IR003-01` |
| Selectivity | no duplicate message on primary success | `AC-IR003-02` |
| Receipts | every message has a status attributable by correlation ID | `AC-IR003-03` |
| Total outage | both providers failing → alert reaches on-call; WhatsApp fallback attempted | `AC-IR003-04` |
| Carrier reality | E2E OTP on real SIMs via the test-device lab | `DEP-12`, `FR-001` verification |
| Log hygiene | zero OTP codes in logs across the auth suite | `AC-SR002-02` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
