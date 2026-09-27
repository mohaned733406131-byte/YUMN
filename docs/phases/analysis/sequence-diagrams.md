---
document_id: DOC-PHA-013
title: Sequence Diagrams — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-SA-006, DOC-PHA-014]
related_requirements: []
---

# Sequence Diagrams — analysis phase

## Purpose
CORE-03 item 11 (separate file): interaction sequences for the phase's functionality, as Mermaid. Canonical detailed flows: [`03-system-analysis/sequence-flows.md`](../../03-system-analysis/sequence-flows.md) (`SQ-01`…`SQ-05`); this file holds the phase-level diagrams and indexes them.

## Scope
Cross-actor, cross-layer interactions spanning API → domain → repository → queue → external providers.

## Index

| ID | Sequence | Canonical detail |
|---|---|---|
| `SQ-01` | Browse → cart → checkout → order → delivery → completion | `sequence-flows.md` §SQ-01 |
| `SQ-02` | Return flow | §SQ-02 |
| `SQ-03` | Vendor onboarding (KYC) | §SQ-03 |
| `SQ-04` | Wallet top-up (provider callback + bank-transfer admin verification) | §SQ-04 |
| `SQ-05` | Dispute (escrow freeze → resolution) | §SQ-05 |

## Representative sequence — checkout with wallet payment (`WF-003`, `SQ-01` head)

```mermaid
sequenceDiagram
  autonumber
  actor C as Customer
  participant W as Web/Mobile shell
  participant API as API /api/v1 (B07 commerce)
  participant DB as PostgreSQL
  participant Q as BullMQ
  participant N as Notification (B10)

  C->>W: submit checkout
  W->>API: POST /orders (Idempotency-Key required, MNY-06)
  API->>API: recompute totals server-side (STK-03), validate cart limits (STK-02)
  API->>DB: BEGIN — order + sub_orders + stock deduction (FOR UPDATE) + wallet debit + ledger rows (MNY-03/05, STK-01)
  alt balance < total
    DB-->>API: rollback
    API-->>W: 422 INSUFFICIENT_FUNDS (STK-04)
  else commit
    DB-->>API: committed (single unit)
    API-->>W: 201 order_no + Cache-Control: no-store (MNY-12)
    API->>Q: b07.order.confirmation.enqueue
    Q->>N: notify customer + vendor (2/2 locales, RTL-05)
  end
```

## Representative sequence — wallet top-up credit (`MNY-07`, `WF-009`)

```mermaid
sequenceDiagram
  autonumber
  actor C as Customer
  participant API as API (B07 wallet)
  participant P as Provider (m-Floos/OneCash)
  participant DB as PostgreSQL
  C->>API: POST /wallet/topups (Idempotency-Key, 1,000–5,000,000 YER)
  API-->>C: 201 PENDING
  API->>P: create top-up request
  P-->>API: verified callback (HMAC, constant-time, replay window — MNY-13)
  API->>DB: BEGIN — credit wallet + balanced ledger rows (append-only)
  DB-->>API: committed
  API-->>P: 200 ack
  Note over API,DB: client "already credited" claims are rejected — credit never comes from the client (MNY-07)
```

## Invariants visible in every sequence
`Idempotency-Key` on money/order endpoints (`MNY-06`, `API-05`) · `Cache-Control: no-store` on money/order/session (`MNY-12`) · server-side authorization (`IDT-05`) · errors from the closed catalog in both locales (`API-03`).

## Open questions (COM-01)
1. Bank-transfer top-up verification path (admin, `UC-034`) needs its own sequence before implementation — `SEC-005`/`WF-009` cover the provider path only.

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 11, session 005) | analysis-agent |
