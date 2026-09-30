---
document_id: DOC-PHA-007
title: Use Case Descriptions & Flows — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-BA-005, DOC-PHA-006, DOC-SA-006]
related_requirements: []
---

# Use Case Descriptions & Flows — analysis phase

## Purpose
CORE-03 item 5: descriptions + **flow of actions** + **flow of events** for all phase functionality. Canonical flows live in [`01-business-analysis/`](../../01-business-analysis/workflow-index.md) (`WF-001`…`WF-012`) and [`../../03-system-analysis/core/sequence-flows.md`](../../03-system-analysis/core/sequence-flows.md) (`SQ-01`…`SQ-05`); this artifact indexes them and states the flow conventions.

## Scope
Every end-to-end journey spanning ≥2 use cases across actors.

## Actors / roles
`customer`, `vendor`, `courier`, `admin`, `moderator`, `support`, `system` — see [`actors-and-roles.md`](../../00-project-overview/actors-and-roles.md).

## Flow-of-actions index (12 workflows)

| ID | Flow of actions | Primary states touched |
|---|---|---|
| `WF-001` | Customer registration & login (OTP, lockout branches) | session, `OTP` lifecycle |
| `WF-002` | Search → PDP → add to cart (guest gating) | cart reservation |
| `WF-003` | Cart → 7-step checkout → wallet payment → order placed | `PLACED` |
| `WF-004` | Vendor order acceptance → fulfillment → ready for pickup | `CONFIRMED`…`READY_FOR_PICKUP` |
| `WF-005` | Courier assignment → pickup → transit → delivery code → delivered | `OUT_FOR_DELIVERY` → `DELIVERED` |
| `WF-006` | Escrow: delivered → 7-day hold → completed → commission → payout | `COMPLETED`, escrow |
| `WF-007` | Return request → approval → pickup → inspection → refunded | `RETURN_*` → `REFUNDED` |
| `WF-008` | Dispute → escrow freeze → admin resolution | `DISPUTED` |
| `WF-009` | Wallet top-up (m-Floos/OneCash callback; bank transfer admin verification) | `wallet_transaction` |
| `WF-010` | Cancellation (customer pre-dispatch) → refund | `CANCELLED` |
| `WF-011` | Vendor onboarding: register → KYC → approve → first listing | KYC states |
| `WF-012` | Coupon creation (admin/vendor) → redemption at checkout | coupon state |

## Flow of events (sequence level)
`SQ-01` browse→cart→checkout→order→delivery→completion · `SQ-02` return · `SQ-03` vendor onboarding · `SQ-04` wallet top-up · `SQ-05` dispute — mermaid sequence diagrams per convention in [`sequence-flows.md`](../../03-system-analysis/core/sequence-flows.md); phase roll-up in [sequence-diagrams.md](sequence-diagrams.md).

## Alternate flows
Per workflow files: OTP failover SMS→WhatsApp (`WF-001`, `BR-NTF-03`), payment insufficient funds (`WF-003`, `BR-CRT-06`), 3rd failed delivery lock (`WF-005`, `BR-SHP-03`), dispute freezes escrow only for its own sub-orders (`WF-008`, `BR-ORD-05/07`).

## Exception flows
Provider callback never arrives → reconciliation job (`BR-ESC-08`, `ESC-05`); queue exhaustion → DLQ + alert ≤1 min (`NFR-007`); ES/Redis down → browse degrades, recovers ≤60 s (`NFR-007`).

## Postconditions
Each flow terminates in exactly one terminal state or a documented rollback with wallet credit (`MNY-10`); every state change appends `order_status_history` (`ORD-05`).

## Data entities touched
`user`, `cart`, `order`, `sub_order`, `payment`, `wallet`, `wallet_transaction`, `escrow`, `shipment`, `return_request`, `review`, `coupon` — [`08-database/entities/`](../../08-database/entities/README.md).

## Invariants
Wallet-only payment (`C-01…C-04`) · `DELIVERED` only via 6-digit code (`ORD-04`) · zero ledger imbalance (`MNY-03`) · no GPS anywhere (`C-16`).

## Open questions (COM-01)
1. `ORD-08`/`D-12`: precedence when `COMPLETED → RETURN_REQUESTED` races `COMPLETED → DISPUTED` — ADR required before implementing (funds outcome undefined).

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 5, session 005) | analysis-agent |
