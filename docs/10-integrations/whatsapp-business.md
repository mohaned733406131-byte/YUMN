---
document_id: DOC-INT-005
title: WhatsApp Business — Template Notifications Contract
category: 10-integrations
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [INT-REQ-004, INT-REQ-003, INT-REQ-006, FR-001, FR-017]
related_documents: [DOC-INT-000, DOC-INT-001, DOC-INT-004, DOC-IR-004, DOC-BA-005, DOC-FR-017]
---

# WhatsApp Business Notifications (`INT-REQ-004`)

Transactional notification delivery over the WhatsApp Business API using **pre-approved templates** in Arabic and English. Dependency risk **HIGH**: `DEP-06` WhatsApp Business approval is `NOT STARTED`; mitigated because SMS remains the primary channel for OTP (`BR-NTF-03`).

## 1. Channel Position in the Notification Policy

| Channel | Role in v1 | Canon |
|---|---|---|
| SMS | Primary for OTP + delivery codes; transactional workhorse | `BR-NTF-03`, `INT-REQ-003` |
| WhatsApp | Template notifications (order status, security notices) **+ automatic OTP failover when SMS fails** | `BR-NTF-03`, `AC-IR004-01` |
| In-app | Notification center with read/unread state | `FR-017` |
| Push (FCM/APNs) | App engagement, deep links | `FR-017`, `07-api` notifications |
| Email | **Not a channel in v1** (`GAP-03`) | `BR-NTF-01` |

**OTP channel policy (stated decision):** routine OTP delivery is **SMS-only**. WhatsApp is never used to *initiate* an OTP flow; it participates solely as the **automatic failover** mandated by `BR-NTF-03` (SMS primary → failover to WhatsApp on provider timeout/failure, `AC-IR004-01`, `AC-FR017-02`). There is no third OTP channel and no email path (`GAP-03`) — so OTP reliability is exactly the SMS-failover chain described in `sms-provider.md` §7.

## 2. Template Catalog (approval-gated)

| Template | Category | Trigger | Parameters (min. PII) | Opt-out applies? |
|---|---|---|---|---|
| `order_status_update` | Utility | order state change (17-state machine) | order ref, status label, store name | No (transactional) |
| `delivery_ready` | Utility | OUT_FOR_DELIVERY | order ref | No |
| `delivery_code` | Utility | code issued to buyer | order ref, 6-digit code | No — security class (`BR-NTF-02`) |
| `otp_failover` | Authentication | SMS primary failed | code, expiry minutes | No — security |
| `security_alert` | Utility | login, password change, lockout, family revocation | event type, timestamp | No — security |
| `topup_result` / `refund_processed` | Utility | money events | order/topup ref, amount (YER) | No — transactional |
| `kyc_decision` | Utility | KYC approved/rejected | status, reason code | No |
| `payout_released` | Utility | vendor payout batch | amount, period | No |
| `marketing_offer` | Marketing | promotions, follower offers (`BR-VND-05`) | campaign, discount | **Yes** (`BR-NTF-05`) |

Rules:
- **Every template must be registered and approved before use**; an unapproved/rejected template ID fails the job to DLQ with an alert — never a silent substitution (`AC-IR004-02`).
- Template names and parameter lists are versioned in this document/file set (`INT-REQ-004` interface expectations).
- Messages carry order references, statuses and amounts — **never** full PII dumps, passwords, OTP-beyond-code, or credentials; no marketing template may carry financial data (`INT-REQ-004` security).
- Bilingual: every template renders in ar and en, following user locale with Arabic default (`BR-NTF-04`, `C-24`, `AC-IR004-04`).

## 3. Sending Path

```text
domain event → BullMQ job (b10.notification.send, BR-PLT-01)
   → WhatsAppPort.sendTemplate(name, phone, params, locale)   [10 s timeout]
   → adapter calls Business API  (credentials: env only, S-07)
   → status callbacks arrive as signed webhooks (INT-REQ-006)
   → retries: 3× exponential backoff → DLQ + alert (BR-PLT-02)
```

- Queue-based so notification traffic never blocks order/payment transactions.
- Delivery status per message logged with correlation ID (`INT-REQ-004` status).
- Failures are normalized (`TIMEOUT / REJECTED / PROVIDER_DOWN / SIGNATURE_INVALID`) — domain code never sees vendor errors (`INT-REQ-008`).

## 4. Opt-In / Opt-Out Handling

| Rule | Behavior | Canon |
|---|---|---|
| Marketing opt-in | Explicit opt-in required before any marketing template; consent recorded with timestamp and source (`INFERENCE` on the exact consent record shape) | `BR-NTF-05` |
| Marketing opt-out | Per-channel, per-category; honored immediately; opted-out categories produce **zero sends** | `BR-NTF-05`, `AC-IR004-03` |
| Security/transactional | **Cannot be disabled** by the user — delivered regardless of marketing preferences | `BR-NTF-02`, `AC-IR004-03` |
| OTP failover | Sent even when all marketing channels are off (it is a security message) | `BR-NTF-02`, `AC-FR017-01` |
| Channel-level toggle | User may disable WhatsApp as a marketing channel while security messages still attempt delivery (`INFERENCE` — aligns with `BR-NTF-05` per-channel wording) | `BR-NTF-05` |

## 5. Conversation Windows & Template Classes (`INFERENCE`)

Exact Business API commercial mechanics arrive with `DEP-06`; design assumptions to confirm:

| Aspect | Assumption | Note |
|---|---|---|
| Outbound contact | Only approved templates may start a conversation outside a customer-service window | standard Business API behavior |
| Customer-service window | Free-form replies allowed within the window opened by a customer message; yumn sends templates only | no free-form marketing blasts |
| Template approval lead time | Days — submission happens in Phase 0, before launch (`DEP-06` gate) | `DOC-OVR-010` |
| Conversation category | Utility/Authentication vs Marketing — security + transactional must be filed in non-marketing categories so opt-out logic stays correct | `BR-NTF-02`/`BR-NTF-05` split |

## 6. Failure Behavior & Fallbacks

| Condition | Behavior |
|---|---|
| Template rejected by provider | Job → DLQ + alert; **no silent substitution** with another template (`AC-IR004-02`) |
| API timeout/outage | Queued retries (3× backoff) → DLQ if persistent |
| WhatsApp down during OTP failover | If SMS primary already succeeded, user is unaffected; if SMS *also* failed → verification unavailable, honest error + alert (`AC-IR003-04`) |
| Status webhook delayed | Final state still converges via reconciliation of message records (`INFERENCE`) |
| Marketing opt-out violated | Treated as a defect — counted by an assertion test (`AC-IR004-03`) |

Fallback direction: **WhatsApp never falls back "up" to become primary**; the only sanctioned fallback chain for OTP is SMS → WhatsApp (`BR-NTF-03`). For ordinary transactional notifications, failure falls back to **in-app** (always recorded) and, for time-critical security notices, to SMS.

## 7. Security

| Control | Design | Canon |
|---|---|---|
| Webhook verification | HMAC-SHA256, constant-time compare, IP allowlist, replay window | `INT-REQ-006`, `INT-REQ-004` |
| Credentials | Business API token + webhook secret in environment only | `SEC-REQ-007` (S-07) |
| Consent state | Enforced per channel/category before send | `BR-NTF-05` |
| Log hygiene | Message bodies containing OTP codes stay out of logs | `INFERENCE`, `SEC-REQ-002` discipline |
| Phone validation | `^7[0-9]{8}$` before send | `BR-AUTH-01` |

## 8. Data Exchanged

Recipient phone, approved template name + parameters (order reference, status, amount in YER), locale `ar`/`en`, correlation ID, delivery status. No card data exists (`C-02`); email is never an identity or destination (`BR-AUTH-08`, `C-06`); no location data (`C-16`).

## 9. Verification

| Test | Assertion | Canon |
|---|---|---|
| Failover | SMS primary fails → OTP delivered via WhatsApp inside validity window | `AC-IR004-01` |
| Approval gate | unapproved template → DLQ + alert, zero sends | `AC-IR004-02` |
| Preferences | marketing opt-out still receives OTP/security; opted-out categories send nothing | `AC-IR004-03` |
| Localization | ar + en rendering per locale, Arabic default | `AC-IR004-04` |
| Sandbox | provider sandbox/test-number certification before production | `DEP-06` gate |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
