---
document_id: DOC-IR-002
title: INT-REQ-002 — Bank transfer top-up
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-001, INT-REQ-008, FR-013, FR-020]
related_documents: [DOC-REQ-001, DOC-BA-005, DOC-OVR-008]
---

# INT-REQ-002 — Bank transfer top-up

> Registry summary (`requirements-overview.md` §5): manual admin verification flow before crediting (BR-PAY-07). Rule text of record: **BR-PAY-04** — bank-transfer top-ups credit the wallet only after admin verification of the reference.

**Dependency risk:** MEDIUM — no external API dependency; risk is verification throughput (admin backlog) and reference fraud, both mitigated by audit + alerts.

## Purpose
Provide the manual top-up rail required by C-05 (bank transfer) and the fallback when wallet-provider rails are unavailable (DEP-05), by verifying each transfer in the admin console before any wallet credit.

## Interface expectations

- **Initiate (customer):** submit amount (BR-PAY-02 bounds), bank reference, and an optional receipt image (validated per SEC-REQ-011) → creates a `PENDING` top-up request; no credit occurs at this step.
- **Verify (admin):** admin console (FR-020) lists pending requests; the admin approves or declines with a reason; approval posts balanced ledger entries idempotently (BR-PAY-06, BR-PAY-08); decline notifies the customer with the reason.
- **Poll (customer):** request status is readable by its owner only (DATA-REQ-008) until terminal.
- **Timeouts/limits:** no external call; requests persist until decided — unresolved items are visible on the admin dashboard and excluded from any silent auto-approval (`INFERENCE` — never auto-credit is `VERIFIED` from BR-PAY-04).

## Data exchanged
Amount (integer YER), bank name/reference, receipt image, customer phone, admin identity, decision + reason + timestamp; every decision writes an audit entry (BR-PLT-06, SEC-REQ-010).

## Failure behavior & fallback
Ambiguous/duplicate reference → declined with reason (no credit); admin unavailable → request stays pending and customer sees pending status (wallet funding temporarily limited to provider rails); suspected fraud → hold + support/dispute path (FR-020).

## Security
Admin approval requires the Admin/Moderator RBAC permissions (SEC-REQ-004) and is deny-by-default; receipt uploads are type/size/malware controlled (SEC-REQ-011); decisions are audit-chained (SEC-REQ-010); no secrets involved.

## Acceptance criteria

- AC-IR002-01: Credit gate — no code path credits a bank-transfer top-up before admin approval; a completed transfer without approval leaves balance unchanged.
- AC-IR002-02: Duplicate — submitting the same bank reference twice results in the second request being rejected with a stable error.
- AC-IR002-03: Decline — declining a request leaves the wallet untouched and delivers a localized (ar/en) notification with the reason (BR-NTF-04).
- AC-IR002-04: Audit — every approval and decline produces a complete audit entry (actor, entity, before/after, IP, timestamp).

## Related IDs

`C-05` · `FR-013` · `FR-020` · `BR-PAY-04` · `BR-PAY-06` · `BR-PAY-08` · `BR-PLT-06` · `SEC-REQ-004` · `SEC-REQ-010` · `SEC-REQ-011` · `INT-REQ-001` · `DATA-REQ-008`

## Verification method
Integration tests for the pending → approve/decline flow (including duplicate reference and no-auto-credit negatives), RBAC check as each role, and audit-entry assertions.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
