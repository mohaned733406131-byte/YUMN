---
document_id: DOC-BE-008
title: Error Handling — Exception Filters, Error Codes & Structured Logging
category: 06-backend
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-03
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-007, NFR-014, SEC-REQ-008, SEC-REQ-010, FR-012, FR-013]
related_documents: [DOC-BE-001, DOC-BE-002, DOC-BE-005, DOC-BA-005]
---

# Error Handling

One global error pipeline produces the contract defined in **`../../07-api/core/error-model.md`** (that document owns the canonical codes and envelope; this file describes backend implementation). Clients map codes to localized text (`../../05-frontend/core/forms-and-validation.md` §5). Errors never leak internals (`SEC-REQ-008`).

---

## 1. Pipeline

```text
throw (typed exception from service/domain)
  → GlobalExceptionFilter (single filter)
      ├─ known domain error   → status + code + messageKey + details
      ├─ Prisma known errors  → mapped (unique violation → 409, FK → 409/400, timeout → 503)
      ├─ validation errors    → 400 VALIDATION_ERROR + field map
      └─ unknown error        → 500 INTERNAL_ERROR (opaque) + full log + correlationId
  → structured log (JSON) + metric increment + alert hook (severity-based)
  → response envelope per 07-api/core/error-model.md
```

| Rule | Detail |
|---|---|
| Single filter | `shared/errors/http-exception.filter.ts` — no ad-hoc `res.json({error})` in controllers |
| Exception types | base `AppException(code, status, details, options)`; subclasses per domain (`StateConflictException`, `InsufficientFundsException`, …) |
| Message keys | responses carry machine `code` + i18n `messageKey`, not English prose — localization client-side (`C-24`, `NFR-013`) |
| Correlation | every error response includes `correlationId` (`NFR-014`) |
| Retries | `retryable` flag in envelope drives client/SDK backoff |

## 2. Domain-Specific Errors (implementation)

| Code | HTTP | Thrown where | Triggered by |
|---|---|---|---|
| `STATE_CONFLICT` | 409 | `OrderService.transition()` (optimistic lock loss or illegal from→to) | C-09 machine, state doc §5 |
| `INSUFFICIENT_FUNDS` | 422 | `PaymentService` / `WalletService` (balance < total) | `BR-PAY-05`, `BR-CRT-06` |
| `STOCK_UNAVAILABLE` | 422 | `InventoryService.reserve()/deduct()` | `BR-CAT-07`, C-13 |
| `LIMIT_EXCEEDED` | 422 | `CartService`, `TopUpService` (C-15 guards, `BR-PAY-02` bounds) | C-15, BR-PAY-02 |
| `OTP_MAX_ATTEMPTS` | 422 | `OtpService.verify()` on 3rd failure | `BR-AUTH-03` |
| `ACCOUNT_LOCKED` | 423 | `AuthService.login()` after 5 failures | `BR-AUTH-04`, SEC-REQ-005 |
| `TOKEN_EXPIRED` / `AUTH_INVALID` | 401 | `JwtAuthGuard` / refresh path | C-08, SEC-REQ-003 |
| `FORBIDDEN` | 403 | guards / ownership interceptor | SEC-REQ-004, FR-002 |
| `NOT_FOUND` | 404 | repository lookups + ownership miss (foreign resource → 404, not 403) | IDOR hygiene |
| `VALIDATION_ERROR` | 400 | global validation pipe | DOC-BE-009 §1 |
| `DUPLICATE_RESOURCE` | 409 | unique constraint (phone, SKU, slug) | BR-AUTH-01, BR-CAT-02 |
| `IDEMPOTENCY_KEY_CONFLICT` | 409 | idempotency middleware (same key, different payload) | BR-PAY-08, BR-PLT-03 |
| `PAYMENT_METHOD_NOT_ALLOWED` | 400 | checkout (must be unreachable in v1) | BR-PAY-01, C-01 |
| `RATE_LIMITED` | 429 | rate-limit guard (+`Retry-After`) | SEC-REQ-009 |
| `DELIVERY_CODE_LOCKED` | 423 | `DeliveryCodeService` (3 failures → 24 h) | BR-SHP-03, C-16 |
| `RETURN_WINDOW_CLOSED` | 422 | `ReturnService.request()` | BR-RET-01, C-11 |
| `COUPON_INVALID` | 422 | `CouponService.apply()` | BR-PRM-04/06 |
| `DEPENDENCY_UNAVAILABLE` | 503 | Redis/ES/provider adapter down | NFR-007 degradation |
| `INTERNAL_ERROR` | 500 | filter catch-all | — |

**Alignment rule:** if `../../07-api/core/error-model.md` names a code differently, that document wins and this table is updated (never invent parallel codes).

## 3. Status-Code Conventions

| Family | Usage |
|---|---|
| 400 | malformed/schema-invalid input |
| 401 | missing/expired/invalid credentials |
| 403 | authenticated but not permitted (role/permission) |
| 404 | missing **or** foreign-owned resource |
| 409 | state conflict, duplicate, idempotency payload mismatch |
| 413 | payload too large (DOC-BE-009 §4), upload >5 MB (SEC-REQ-011) |
| 422 | semantically invalid (funds, stock, limits, window) |
| 423 | locked (account, delivery code) |
| 429 | rate limited |
| 500 | unexpected (opaque) |
| 503 | dependency degraded (graceful degradation, NFR-007) |

## 4. Structured Logging (NFR-014)

| Property | Value |
|---|---|
| Format | single-line JSON per event |
| Mandatory fields | `ts`, `level`, `msg`, `correlationId` (request/job), `service`, `module`, `actor` (id+role when present), `route`, `method`, `status`, `durationMs` |
| Job fields | `queue`, `jobId`, `attemptsMade` |
| Money events | `entity`, `amountYER` (integer), `currency: YER` — never card-like data (none exists, C-02) |
| PII policy | phone masked (`79***432`); passwords/OTPs/tokens **never** logged (SEC-REQ-002, SEC-REQ-007) |
| Correlation propagation | inbound header → request-scoped logger child → outgoing HTTP/job payloads (`NFR-014`) |
| Sampling | debug/info sampled under load; warn/error always kept |
| Transport | stdout → collected by the observability stack → Prometheus/Grafana/alert routes (`INT-REQ-007`) |

## 5. Alerting Hooks

| Severity | Examples | Route |
|---|---|---|
| Critical | 5xx rate > 1%, DLQ depth > 0, ledger mismatch (`BR-ESC-08`), reconciliation failure | on-call page (`../../12-non-functional/core/observability.md`) |
| High | `STATE_CONFLICT` spike (client/server drift), auth failure spike, Redis down | team channel + dashboard annotation |
| Medium | rate-limit surge, `DEPENDENCY_UNAVAILABLE` from a provider | ticket + dashboard |
| Info | routine domain errors (`VALIDATION_ERROR`, 404) | metrics only |

Metrics emitted alongside logs: per-endpoint RED metrics, error-code counters, p95/p99 latency — asserted against `NFR-001` budgets.

## 6. Security Rules (SEC-REQ-008, SEC-REQ-010)

1. **No internals leak:** stack traces, SQL, Prisma errors, file paths, dependency versions never cross the wire — only in server logs.
2. Unknown errors become generic `INTERNAL_ERROR` with correlationId for support ("copy details" UX).
3. Authorization failures don't reveal whether a foreign resource exists (404 policy).
4. Validation errors echo field names, not values of sensitive fields (password/OTP masked in details).
5. Privileged-action failures and money-action failures produce audit entries (`BR-PLT-06`, SEC-REQ-010).
6. Error responses are cached nowhere — `Cache-Control: no-store`.

## 7. Error Handling by Caller

| Caller | Behavior |
|---|---|
| Web/mobile clients | map code → localized message; `retryable` drives auto-retry; 401 → refresh (DOC-FE-004 §5) |
| BullMQ consumers | classify: retryable (network/dep) → BullMQ retry; permanent (validation/logic) → immediate DLQ (`DOC-BE-006` §8) |
| Outbound webhooks | receiver failures follow INT-REQ-006 (3× backoff + DLQ) |
| Health endpoints | liveness/readiness report dependency states without details (`BR-PLT-07`) |

## 8. Verification

| Test | Coverage |
|---|---|
| Unit | each typed exception maps to expected status/code |
| Filter tests | unknown error → 500 opaque + log contains full detail; no stack in body |
| Contract tests | responses match `../../07-api/core/error-model.md` envelope exactly |
| Log tests | JSON schema validation; PII redaction assertions (no OTP/password/phone in clear) |
| Load | error-code metrics visible in Grafana during k6 runs (NFR-014) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-03 | Fence-diagram ref 07-api/error-model.md → `07-api/core/error-model.md` (portal scheme) | Session-011 section-grouping rename follow-up (prompt-013 §2 leftover sweep) — moved-file outbound links / stale pre-portal path claims |
