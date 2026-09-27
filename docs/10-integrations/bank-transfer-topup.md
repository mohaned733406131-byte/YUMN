---
document_id: DOC-INT-003
title: Bank Transfer Top-Up — Manual Admin Verification Flow
category: 10-integrations
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [INT-REQ-002, INT-REQ-001, FR-013, FR-020]
related_documents: [DOC-INT-000, DOC-INT-001, DOC-INT-002, DOC-IR-002, DOC-BA-005, DOC-FR-013]
---

# Bank Transfer Top-Up (`INT-REQ-002`)

The manual top-up rail required by `C-05` and the standing fallback when the wallet-provider rails are unavailable (`DEP-05`/`DEP-01` outage). Rule of record: **`BR-PAY-04` — bank-transfer top-ups credit the wallet only after admin verification of the reference.** There is no external provider API: the "integration" is between the customer's evidence, the admin console (`FR-020`), and the ledger.

## 1. Flow

```text
1. SUBMIT    customer → POST /topups/bank-transfer {amountYER, bankName, reference, receiptImage?}
             validates bounds (1,000–5,000,000 YER, BR-PAY-02) + upload rules (SEC-REQ-011)
             → creates topup_request(PENDING)          ← NO credit at this step
2. QUEUE     request appears in the admin verification queue (FR-020), sorted by age
3. DECIDE    ADMIN/SUPER_ADMIN approves or declines with a reason
             APPROVE → one ACID tx: balanced ledger rows (BR-PAY-06) + balance update
                        + status CREDITED + idempotency guard (BR-PAY-08) + audit (BR-PLT-06)
             DECLINE → no ledger effect; status DECLINED + reason; customer notified (ar/en, BR-NTF-04)
4. POLL      customer reads own request status until terminal (DATA-REQ-008 owner scoping)
```

No code path exists that credits before approval (`AC-IR002-01`); unresolved items simply remain `PENDING` — **never auto-approved** (`VERIFIED` from `BR-PAY-04`, mirrored by `INT-REQ-002`).

## 2. Evidence Fields

| Field | Type | Validation | Notes |
|---|---|---|---|
| `amountYER` | integer | 1,000–5,000,000 (`BR-PAY-02`) | must match the transferred amount for approval |
| `bankName` | enum/controlled list | known Yemeni banks (config list, `INFERENCE`) | free text rejected to keep matching reliable |
| `reference` | string | normalized (trim/upper), length-bounded, **unique across requests** | duplicate → stable error (`AC-IR002-02`); uniqueness checked on hash (`data-protection.md` §5) |
| `receiptImage` | optional jpg/png/webp ≤5 MB | type + magic bytes + EXIF strip + malware scan | `SEC-REQ-011`, `BR-CAT-08` discipline |
| `customerPhone` | derived from session | `^7[0-9]{8}$` | requester identity comes from the authenticated principal, never the body |
| `createdAt` | timestamp | server | drives queue age and SLA reporting |
| Decision: `approverId`, `decision`, `reason`, `decidedAt`, `ip` | — | required on decide | feeds the audit entry (§5) |

## 3. Admin Verification Queue

| Aspect | Design | Canon |
|---|---|---|
| Access | ADMIN + SUPER_ADMIN only; MODERATOR explicitly denied (finance scope) | `09-security/rbac.md` row 14, `DOC-OVR-007` |
| Visibility | pending list with age; every decision writes an audit row (actor, entity, before/after, IP, timestamp) | `SEC-REQ-010` R2/R3, `BR-PLT-06` |
| Approval effect | balanced ledger credit + wallet balance update, idempotent | `BR-PAY-06`, `BR-PAY-08` |
| Rejection effect | zero ledger effect; localized reason to customer | `AC-IR002-03`, `BR-NTF-04` |
| Backlog surfacing | age-of-request visible on the admin dashboard; oldest-first | `INT-REQ-002` (dashboard visibility) |
| Fraud suspicion | hold + support/dispute path instead of approve/decline | `FR-020` |

## 4. Credit / Rejection Paths

| Path | Precondition | Effect |
|---|---|---|
| **Credit** | amount within bounds ∧ unique reference ∧ admin approval ∧ wallet not frozen (`BR-PAY-09`) | one transaction: ledger rows + balance + `CREDITED` + audit |
| **Reject — duplicate reference** | reference already used | request never created / second submit rejected (`AC-IR002-02`) |
| **Reject — admin decline** | mismatch, ambiguity, suspected fraud | `DECLINED` + reason; wallet untouched; customer notified (`AC-IR002-03`) |
| **Reject — policy** | amount < 1,000 or > 5,000,000 | validation error before row creation (`BR-PAY-02`, `AC-FR013-01`) |
| **Pending forever** | no admin decision | stays `PENDING`; visible on dashboard; customer sees pending; no silent expiry (`INFERENCE` — never-auto-credit is `VERIFIED`) |
| **Idempotent re-approve** | same request approved twice (double-click/retry) | second attempt returns the original result, single ledger credit (`BR-PAY-08`) |

## 5. Audit Trail (`SEC-REQ-010`)

Every approval and decline produces exactly one complete audit entry: actor, action (`TOPUP_BANK_APPROVE` / `TOPUP_BANK_DECLINE`), entity reference, before/after status, IP, timestamp — no secrets or full PII payloads (`AC-IR002-04`, `AC-SR010-03`). Audit rows are append-only and hash-chained; the application role cannot UPDATE/DELETE them (`AC-SR010-01`). Financially relevant entries are retained ≥ 5 years (`NFR-019`).

## 6. Fraud Checks

| Check | Mechanism | Rationale |
|---|---|---|
| Amount match | approver compares request amount vs receipt/bank statement evidence | prevents "I transferred 1,000, claimed 100,000" |
| Reference match | exact normalized reference; uniqueness platform-wide | prevents reuse of one transfer to credit twice (`AC-IR002-02`) |
| Duplicate submission | unique-hash constraint at write time | race-proof, not just UI-level |
| Evidence integrity | receipt images pass `SEC-REQ-011` (type, size, no active content, EXIF stripped) | forged HTML/SVG "receipts" are unrepresentable — SVG/HTML rejected |
| Velocity (design, `INFERENCE`) | alerts on many requests from one account/reference pattern | complements rate limits (`SEC-REQ-009`) |
| Two-person control (design, `INFERENCE`) | optional: large amounts (> configured threshold) require SUPER_ADMIN second approval | strongest mitigation for insider credit fraud; threshold to be set with finance |
| Statement verification | ops cross-checks the platform bank account (portal credentials S-10) when evidence is unclear | `secrets-management.md` §2 |

## 7. SLA

| Metric | Target | Evidence |
|---|---|---|
| Decision time | **≤ 1 business day** (design target, `INFERENCE`) | no canon value exists; chosen to keep the fallback rail usable during provider outages; comparable to the 48 h KYC decision rule (`BR-VND-03`) |
| Escalation | requests pending > 1 business day flagged on dashboard; > 2 business days alert ops lead (`INFERENCE`) | supports `C-26` operability, `NFR-020` |
| Auto-approval | **never** — no timeout converts `PENDING` into `CREDITED` | `VERIFIED` (`BR-PAY-04`) |
| Customer comms | pending status readable at any time; decline arrives with reason in ar/en | `AC-IR002-03`, `DATA-REQ-008` |

## 8. Failure Behavior

| Condition | Behavior |
|---|---|
| Admin unavailable / backlog | requests remain pending; wallet funding temporarily limited to provider rails (`INT-REQ-001`); customer sees honest pending state |
| Ambiguous or duplicate reference | declined with reason; no credit |
| Suspected fraud | hold + support/dispute path (`FR-020`); possible wallet freeze (`BR-PAY-09`) |
| Receipt upload malicious | rejected/quarantined by the upload pipeline; request may still be submitted without receipt (`AC-SR011-01…04`) |
| Platform outage during decide | idempotency key ensures the retried decision credits exactly once (`BR-PAY-08`) |

## 9. Security Summary

- **Authorization:** ADMIN/SUPER_ADMIN only, deny-by-default, server-side (`SEC-REQ-004`); MODERATOR has no finance authority (`09-security/rbac.md` §4).
- **Uploads:** `SEC-REQ-011` pipeline for receipts (`SEC-C-22`).
- **Audit:** append-only, chained, 5-year retention (`SEC-REQ-010`, `NFR-019`).
- **Privacy:** request status owner-scoped (`DATA-REQ-008`); no bank credentials involved in the customer flow; portal credentials (S-10) are human-held, ops-only.
- **Rate limits:** submission on the standard/top-up budgets (`SEC-REQ-009`).

## 10. Verification

| Test | Assertion | Canon |
|---|---|---|
| Credit gate | completed transfer without approval leaves balance unchanged | `AC-IR002-01` |
| Duplicate | same reference twice → second rejected with stable error | `AC-IR002-02` |
| Decline | wallet untouched; localized reason delivered | `AC-IR002-03` |
| Audit | every approve/decline → one complete audit row | `AC-IR002-04` |
| RBAC | MODERATOR/CUSTOMER/VENDOR calls to the decide endpoint → 403 | `AC-SR004-01` |
| Limits | 999 YER submit rejected | `BR-PAY-02` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
