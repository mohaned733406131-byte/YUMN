---
document_id: DOC-SR-010
title: SEC-REQ-010 — Audit trail integrity
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-004, SEC-REQ-007, FR-020, NFR-019]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# SEC-REQ-010 — Audit trail integrity

> Registry summary (`requirements-overview.md` §3): append-only audit log for privileged & money actions; tamper-evident chain.

**Priority:** High · **STRIDE:** Repudiation (R), Tampering (T) · **Failure impact:** HIGH

## Description
Every privileged and money-moving action writes an append-only audit entry containing actor, action, entity, before/after state, IP, and timestamp (BR-PLT-06). The trail is tamper-evident through a hash chain and protected by database permissions so that neither the application nor an operator can silently rewrite history.

## Security rationale
Wallet, escrow, refund, payout, and dispute decisions must be provable — an admin or vendor could otherwise deny an action, or an attacker with database access could erase the evidence of fraud. Threat: denial of actions and silent log manipulation → STRIDE **Repudiation** and **Tampering**.

## Requirement statements

- R1: Audit entries are append-only: the application database role holds no UPDATE/DELETE privilege on audit tables (pattern shared with DATA-REQ-007), and entries are never edited or removed by application code.
- R2: Coverage is mandatory for: role/permission changes, KYC approve/reject/suspend (FR-007), wallet freeze/unfreeze (BR-PAY-09), refunds, payouts, top-up admin verification (BR-PAY-04), dispute and return resolutions (BR-RET-06), and platform settings changes (FR-020).
- R3: Each entry carries actor, action, entity reference, before/after values, IP, and timestamp (BR-PLT-06), with no secrets or full PII payloads embedded.
- R4: Tamper evidence — each row chains the hash of the previous row; a verification job recomputes the chain and alerts on any modification, deletion, or gap.
- R5: Financially relevant audit records are retained and exportable for at least 5 years (NFR-019, aligned with financial retention).

## Acceptance criteria

- AC-SR010-01: Permission test — direct `UPDATE`/`DELETE` against audit tables as the application role fails with a privilege error.
- AC-SR010-02: Tamper test — manually altering or deleting one audit row causes the verification job to fail the chain check and raise an alert.
- AC-SR010-03: Coverage test — an automated scenario executes each action listed in R2 and asserts exactly one complete audit row (all required fields) per action.
- AC-SR010-04: Retention test — audit records for money actions older than the current window remain queryable/exportable per the ≥5-year retention configuration.

## Related IDs

`BR-PLT-06` · `BR-PAY-04` · `BR-PAY-09` · `BR-RET-06` · `FR-007` · `FR-020` · `SEC-REQ-004` · `DATA-REQ-007` · `NFR-019`

## Verification method

Database permission test, chain-tamper injection test, scenario-based coverage integration tests, and retention/export evidence review; audit design documented in `09-security/`.

## Failure impact

**HIGH** — money actions become unprovable: disputes cannot be resolved fairly, fraud inside admin roles goes undetected, and the platform fails its ≥5-year financial record obligation (NFR-019).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
