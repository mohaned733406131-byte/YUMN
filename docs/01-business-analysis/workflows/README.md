---
document_id: DOC-WF-001
title: Workflows — Index & Format
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-011, FR-012, FR-013, FR-015, FR-016]
related_documents: [DOC-BA-001, DOC-BA-004, DOC-BA-005]
---

# End-to-End Workflows — Index & Format

**12 end-to-end workflows `WF-001…WF-012`** spanning the yumn marketplace from registration to settlement. Each workflow crosses actor and block boundaries and names its branches and failure paths — not just the happy path. The 17-state order machine they operate on is authoritative in `03-system-analysis/state-transitions.md` (`C-09`); rule definitions are authoritative in `business-rules.md`.

## 1. Workflow Index

| ID | File | document_id | Purpose (one line) | Primary actors |
|---|---|---|---|---|
| WF-001 | [workflow-001.md](workflow-001.md) | DOC-WF-002 | Customer registration & login — phone + OTP, lockout and session branches | Customer, System |
| WF-002 | [workflow-002.md](workflow-002.md) | DOC-WF-003 | Product search → PDP → add to cart, with guest gating and cart guards | Customer (guest/registered) |
| WF-003 | [workflow-003.md](workflow-003.md) | DOC-WF-004 | Cart → 7-step checkout → wallet payment → order `PLACED`, incl. insufficient-balance → top-up branch | Customer, System |
| WF-004 | [workflow-004.md](workflow-004.md) | DOC-WF-005 | Vendor order acceptance → fulfillment → `READY_FOR_PICKUP` with SLA escalation | Vendor, System |
| WF-005 | [workflow-005.md](workflow-005.md) | DOC-WF-006 | Courier assignment → pickup → transit → 6-digit code → `DELIVERED`, incl. failed-attempt branches | Delivery Provider, Customer, System |
| WF-006 | [workflow-006.md](workflow-006.md) | DOC-WF-007 | Escrow: `DELIVERED` → 7-day hold → `COMPLETED` → commission → payout | System, Finance/Admin |
| WF-007 | [workflow-007.md](workflow-007.md) | DOC-WF-008 | Return request → approval → pickup → inspection → `REFUNDED` | Customer, Vendor, Courier, System |
| WF-008 | [workflow-008.md](workflow-008.md) | DOC-WF-009 | Dispute → escrow freeze → admin resolution | Customer/Vendor, Admin |
| WF-009 | [workflow-009.md](workflow-009.md) | DOC-WF-010 | Wallet top-up: m-Floos/OneCash callback and bank transfer admin verification | Customer, System, Admin |
| WF-010 | [workflow-010.md](workflow-010.md) | DOC-WF-011 | Customer cancellation (pre-dispatch) → stock restore → wallet refund | Customer, System |
| WF-011 | [workflow-011.md](workflow-011.md) | DOC-WF-012 | Vendor onboarding: register → KYC submit → approve → first listing | Vendor, Admin |
| WF-012 | [workflow-012.md](workflow-012.md) | DOC-WF-013 | Coupon creation (admin/vendor) → redemption at checkout | Admin/Vendor, Customer, System |

> **Numbering rule:** the file number is the workflow ID (`workflow-007.md` = `WF-007`); the `document_id` runs one ahead of the workflow number because `DOC-WF-001` is reserved for this index (`workflow-001.md` = `WF-001` = `DOC-WF-002`, … `workflow-012.md` = `WF-012` = `DOC-WF-013`). Never reference a workflow by document_id when a `WF-NNN` ID exists.

## 2. Workflow File Format

Every workflow file uses the same anatomy (in this order):

1. **Frontmatter** — `document_id`, title, category, status, version, dates, author, `related_requirements` (`FR-*`), `related_documents`.
2. **Header + metadata block** — Trigger · Actors · Scope (blocks `B01…B13` touched) · Preconditions · Final state.
3. **ASCII arrow flow** — one code block, `→` happy path, branch labels on arrows, failure exits marked `✗`.
4. **Step table** — columns: `Step | Actor | Action | System | Rules applied (BR IDs) | Data changes | Failure / branch handling`.
5. **Alternatives** — named variant paths (e.g. WhatsApp OTP failover, bank-transfer top-up).
6. **Exceptions** — explicit failure/edge handling with rule IDs.
7. **Rules applied** — the full list of `BR-*` IDs exercised (references only — never restated definitions).
8. **Data touched** — entities/tables in narrative form (no schema copy — `08-database/` owns schema).
9. **Systems** — blocks `B01…B13` involved.
10. **Final state** — the resulting order/wallet/etc. state and notifications sent.
11. **Change History** — `1.0 | 2026-09-26 | Initial version | Initial analysis`.

## 3. Conventions

- **Naming:** `WF-NNN` for references; files `workflow-NNN.md` (zero-padded, `lowercase-kebab-case`).
- **Rules:** cite `BR-*` IDs only; definitions live in `business-rules.md` (DOC-BA-005).
- **States:** the 17 canonical states only (`C-09`); never invent transitional states — "escalation to admin review" is an escalation, not a state (`BR-SHP-06`, `BR-ORD-10`).
- **Actors:** the canonical 7 (`ACT-01…ACT-07`).
- **Money:** wallet-only (`C-01`); refunds always to wallet (`BR-PAY-07`); amounts integer YER (`BR-PAY-10`).
- **Evidence:** anything not fixed by canon is tagged `INFERENCE`; unknown targets are `INSUFFICIENT EVIDENCE`.

## 4. Dependencies

Consumes: `00-project-overview/` (actors, constraints), `business-rules.md`, `03-system-analysis/state-transitions.md`, `02-requirements/` (FR registry). Feeds: `03-system-analysis/` (behavioral analysis), `07-api/` (endpoint choreography), `13-testing/` (E2E test cases), `19-traceability/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial index (12 workflows) | Initial analysis |
