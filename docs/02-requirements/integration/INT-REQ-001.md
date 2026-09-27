---
document_id: DOC-IR-001
title: INT-REQ-001 — Wallet top-up providers
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-002, INT-REQ-006, INT-REQ-008, FR-013, FR-014]
related_documents: [DOC-REQ-001, DOC-OVR-010, DOC-BA-005]
---

# INT-REQ-001 — Wallet top-up providers

> Registry summary (`requirements-overview.md` §5): m-Floos + OneCash: initiate → callback/poll → credit ledger; reconciliation job; sandbox before prod (DEP-05).

**Dependency risk:** HIGH — `DEP-05` is **NOT STARTED** and blocks production top-ups (FR-013); fallback is bank transfer (INT-REQ-002).

## Purpose
Fund customer wallets from Yemeni mobile-money providers (m-Floos, OneCash) per C-05, with the wallet credited only from verified provider evidence — never from a client claim — and with daily reconciliation against provider statements.

## Interface expectations

- **Initiate:** server creates a provider transaction with amount in integer YER within BR-PAY-02 bounds (1,000–5,000,000), a platform reference, and an idempotency key (BR-PAY-08); the client receives redirect/starter data only, never credit authority.
- **Callback / poll:** provider posts a signed callback; if none arrives, a poll/reconciliation job queries status. Outbound calls time out at 10 s; provider callbacks are retried 3× with exponential backoff then DLQ (BR-PLT-02).
- **Finalize:** verified success posts balanced ledger entries (BR-PAY-06) and updates wallet balance atomically (BR-PAY-05); duplicate, out-of-order, or late callbacks are idempotent.
- **Rate limits:** initiation endpoint stricter than the 100 req/min standard (SEC-REQ-009).
- **Environments:** sandbox suite must pass end-to-end before any production credential is issued (DEP-05 gate).

## Data exchanged
Merchant credentials, transaction reference, amount (integer YER), customer wallet phone, status codes, timestamps, HMAC signature. No card data exists in the flow (C-02); message/log output excludes credentials (SEC-REQ-007).

## Failure behavior & fallback
Callback lost → poll job reconciles within the daily window; amount/status mismatch → transaction held, no credit, finance alert (BR-ESC-08/BR-FIN-03); provider outage → top-up UI degrades to bank transfer (INT-REQ-002) and ops alert fires; exhausted retries → DLQ + alert (BR-PLT-01).

## Security
HMAC-SHA256 signature verification with constant-time compare, provider IP allowlist, replay window on timestamps, secrets in environment only (SEC-REQ-007), audit entry per credit (BR-PLT-06).

## Acceptance criteria

- AC-IR001-01: Sandbox E2E — initiate → signed callback → wallet credited exactly once with balanced ledger rows.
- AC-IR001-02: Idempotency — the same callback delivered 3× produces a single credit; a callback after a poll-based credit is a no-op.
- AC-IR001-03: Mismatch — a callback whose amount/status differs from the initiated transaction is rejected and alerts finance; no credit posted.
- AC-IR001-04: Forgery — unsigned, wrong-signature, or expired-timestamp callbacks return 401, are logged, and never credit.
- AC-IR001-05: Gate — production credentials remain unusable until the sandbox acceptance suite passes (DEP-05 exit criterion).

## Related IDs

`DEP-05` · `C-05` · `FR-013` · `BR-PAY-02` · `BR-PAY-03` · `BR-PAY-05` · `BR-PAY-06` · `BR-PAY-08` · `BR-ESC-08` · `BR-FIN-03` · `INT-REQ-006` · `INT-REQ-008` · `RISK-003`

## Verification method
Provider-sandbox integration tests (happy path, duplicate/mismatch/forgery negatives), reconciliation job test with seeded discrepancy, and pre-production gate review recorded in `10-integrations/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
