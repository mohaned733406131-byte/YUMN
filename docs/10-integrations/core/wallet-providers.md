---
document_id: DOC-INT-002
title: Wallet Top-Up Providers — m-Floos & OneCash Contract
category: 10-integrations
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [INT-REQ-001, INT-REQ-006, INT-REQ-008, FR-013, FR-014]
related_documents: [DOC-INT-000, DOC-INT-001, DOC-INT-003, DOC-INT-007, DOC-IR-001, DOC-BA-005, DOC-FR-013]
---

# Wallet Top-Up Providers — m-Floos & OneCash (`INT-REQ-001`)

Contract for the two mobile-money top-up rails allowed by `C-05`. Provider-specific facts are confined to this file and the `mFloosAdapter` / `OneCashAdapter` folders (`INT-REQ-008`).

> **Evidence note:** exact provider API specifications (endpoint paths, signature header names, field names) are **not available yet** because `DEP-05` (merchant API access) is `NOT STARTED`. Everything below marked `INFERENCE` is a design assumption that must be confirmed against the providers' actual sandbox documentation when `DEP-05` opens; the *behavioral* requirements (callback-only credit, idempotency, limits, reconciliation) are `VERIFIED` from `BR-PAY-*` and `INT-REQ-001`. The open API-knowledge gap is recorded in the GAP registry (`../../20-validation/core/missing-information.md`).

## 1. End-to-End Flow

```text
1. INITIATE   customer → POST /topups {amountYER, provider}
              server validates bounds (1,000–5,000,000 BR-PAY-02), creates topup(PENDING),
              generates platform reference + idempotency key (BR-PAY-08),
              calls PaymentProviderPort.initiate()  [10 s timeout]
2. APPROVE    customer is redirected / handed starter data and approves
              inside the m-Floos or OneCash app        ← client never holds credit authority
3. CONFIRM    provider → signed webhook callback  (or: poll job queries status)
              verify HMAC + timestamp window + allowlist → persist raw → 200 fast
4. VERIFY     match provider txn id + amount + status against the PENDING topup;
              mismatch → HOLD, no credit, finance alert (BR-ESC-08 / BR-FIN-03)
5. CREDIT     one ACID transaction: balanced ledger rows (BR-PAY-06) + wallet balance
              update (BR-PAY-05) + status → CREDITED + audit entry (BR-PLT-06)
6. RECONCILE  daily job compares ledger/wallet totals vs provider statement (BR-ESC-08)
```

Sequencing rule: steps 3–5 are the **only** credit path; step 1's client response never influences balance (`BR-PAY-03`).

## 2. API Contract Assumptions (`INFERENCE` — confirm under `DEP-05`)

| Aspect | Design assumption | Basis |
|---|---|---|
| Direction | yumn-initiated charge request; provider confirms via server-to-server callback, with polling as fallback | `INT-REQ-001` "callback / poll" |
| Amount | integer YER, no floats, no currency conversion | `BR-PAY-10`, `C-04` |
| Reference | platform-generated topup reference sent to provider; echoed back in callback | `INT-REQ-001` data exchanged |
| Signature | HMAC-SHA256 over raw body with provider secret; constant-time compare; header carries timestamp | `INT-REQ-001` security, `INT-REQ-006` |
| Callback retries (provider → yumn) | providers retry; our handler is idempotent so their retries are safe | `AC-IR006-01` |
| Poll fallback | scheduled job queries pending transactions older than ~2 min; finalizes identical to callback path | `INT-REQ-001` |
| Status vocabulary | normalized to `PENDING / SUCCEEDED / FAILED / EXPIRED` inside the adapter | `INT-REQ-008` taxonomy |
| Errors | provider error strings mapped to `TIMEOUT / REJECTED / PROVIDER_DOWN / SIGNATURE_INVALID` | `INT-REQ-008` |
| Sandbox | full suite must pass before production credentials are issued | `AC-IR001-05`, `DEP-05` |

## 3. Amount Limits & Validation

| Rule | Value | Canon |
|---|---|---|
| Minimum top-up | **1,000 YER** | `BR-PAY-02` |
| Maximum top-up | **5,000,000 YER** per transaction | `BR-PAY-02` |
| Type | integer YER only | `BR-PAY-10` |
| Out-of-bounds | rejected before any provider call, stable error code | `AC-FR013-01` |
| Rate limit | stricter than the 100 req/min standard (design: 10/min per user) | `SEC-REQ-009` R2, `INT-REQ-001` |
| Wallet state | frozen wallet cannot top up (`BR-PAY-09`) — checked before initiate | `BR-PAY-09` |

## 4. Signature, Forgery & Replay Controls

- Callback accepted only if: source IP ∈ provider allowlist **and** HMAC valid (constant-time) **and** timestamp inside the replay window → else `401`, security metric, zero effect (`AC-IR001-04`, `AC-IR006-02`).
- Signature computed over the **raw body** before JSON parsing (parser differentials).
- Replay window and nonce persistence: fixed in `webhook-reliability.md` (design: ±5 min) — tracked as `SEC-005` until implemented.
- Secrets (merchant key, webhook secret) come from environment only (`SEC-REQ-007`, inventory S-04/S-05).
- Every accepted credit writes an audit entry (actor = SYSTEM, action = TOPUP_CREDIT) (`BR-PLT-06`, `SEC-REQ-010` R2).

## 5. Duplicate-Credit Prevention (idempotency)

| Layer | Mechanism |
|---|---|
| 1 — Webhook level | provider transaction ID persisted on receipt; repeat deliveries short-circuit to `200` with no reprocessing (`INT-REQ-006`, `BR-PLT-03`) |
| 2 — Domain level | unique constraint on provider txn id → second credit attempt fails closed at the DB (`DATA-REQ-001`) |
| 3 — Ledger level | credit posts inside the same ACID transaction that flips topup status; status flip and ledger insert are inseparable (`BR-PLT-04`) |
| 4 — Reconciliation level | daily job flags any wallet credit without matching provider statement entry → finance alert (`BR-ESC-08`, `BR-FIN-03`) |

Test evidence: same callback delivered 3× and a callback arriving after a poll-based credit both produce exactly one credit (`AC-IR001-02`).

## 6. Failure States

| State | Trigger | Behavior | Canon |
|---|---|---|---|
| `PENDING` | initiated, awaiting provider confirm | balance untouched; customer sees pending; poll job watches | `BR-PAY-03` |
| `PENDING` too long (design: > 15 min, `INFERENCE`) | no callback, poll returns pending | topup auto-**cancelled**, hold released, customer notified with retry guidance; a *later* valid callback is evaluated against the cancelled record and — if the provider did charge — routed to reconciliation for manual credit decision (never silent) | `INFERENCE` — derived from honest-state requirement `BR-ORD-10`-style and `BR-ESC-08` |
| `SUCCEEDED` verified | callback/poll matches amount + status | credit posted once | `BR-PAY-03`, `BR-PAY-06` |
| Amount/status mismatch | provider says X, platform initiated Y | **HOLD — no credit**, finance alert, transaction visible to ops | `AC-IR001-03`, `BR-ESC-08` |
| `FAILED` / `REJECTED` | provider rejected | terminal, no credit, localized error to customer | `INT-REQ-008` taxonomy |
| Duplicate/out-of-order/late callback | replay, race | idempotent no-op or safely sequenced via status machine | `INT-REQ-001` finalize |
| Handler always fails | bug | 3 retries → DLQ → alert → admin replay after fix | `BR-PLT-02`, `BR-PLT-01` |

## 7. Reconciliation

| Aspect | Design | Canon |
|---|---|---|
| Schedule | Daily job (plus on-demand from ops) | `BR-ESC-08`, `BR-FIN-03` |
| Inputs | Ledger totals, wallet balances, topup records ↔ provider statement (file/API, `INFERENCE` on transport) | `BR-FIN-03` |
| Output | Report of matched/unmatched items; **any mismatch alerts finance immediately** | `BR-ESC-08` |
| Invariant | Σ ledger debits == Σ credits; wallet + escrow + payable totals == provider statement | `BR-ESC-08`, `NFR-008` |
| Corrections | Compensating entries only — never UPDATE/DELETE of postings | `DATA-REQ-007` |
| Silent auto-approval | Never — unmatched items require human decision | `INT-REQ-002` principle applied across top-ups (`INFERENCE`) |

## 8. Provider Outage Behavior

| Condition | Behavior |
|---|---|
| Single provider down (circuit open) | That provider's option disabled in the top-up UI; the other provider remains; no error storms (fail-fast `PROVIDER_DOWN`) |
| Both providers down | **Top-up UI degrades to bank transfer** (`INT-REQ-002`) with an ar/en explanation banner; ops alert fires; in-flight `PENDING` items still reconciled | 
| Provider slow (timeouts rising) | 10 s timeout → `TIMEOUT` → retry per adapter policy → circuit opens before user hangs | `NFR-001`, `NFR-007` |
| Recovery | circuit half-open probe; pending poll job drains backlog; reconciliation confirms no double credit | `BR-ESC-08` |
| Dependency status | `DEP-05` **NOT STARTED** → production top-ups blocked; `RISK-003` tracks the commercial risk | `DOC-OVR-010` |

## 9. Data Exchanged (privacy note)

Sent/received: platform reference, amount (integer YER), wallet phone (masked in logs), status codes, timestamps, HMAC signature. **Never exchanged:** card data (none exists, `C-02`), passwords, OTP codes. Log/trace output excludes credentials and full message bodies (`SEC-REQ-007`, `SEC-REQ-002`); metric labels carry no phone numbers (`INT-REQ-007`).

## 10. Verification

| Test | Assertion | Canon |
|---|---|---|
| Sandbox E2E | initiate → signed callback → exactly one credit with balanced ledger rows | `AC-IR001-01` |
| Idempotency | 3× callback / post-poll callback → single credit | `AC-IR001-02` |
| Mismatch | wrong amount/status → rejected + finance alert, no credit | `AC-IR001-03` |
| Forgery | unsigned/bad-signature/expired-timestamp → 401, logged, no credit | `AC-IR001-04` |
| Gate | production credentials unusable until sandbox suite passes | `AC-IR001-05` |
| Limits | 999 YER and 5,000,001 YER rejected at validation | `AC-FR013-01`, `BR-PAY-02` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
