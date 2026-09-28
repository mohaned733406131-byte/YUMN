---
document_id: DOC-PHA-014
title: Activity Diagrams — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-SA-004, DOC-PHA-013]
related_requirements: []
---

# Activity Diagrams — analysis phase

## Purpose
CORE-03 item 12 (separate file): activity (decision-heavy) flows as Mermaid. Canonical behavioral detail lives in [`state-transitions.md`](../../03-system-analysis/state-transitions.md) and the workflows `WF-001`…`WF-012`; this file carries the phase-level activity diagrams.

## Scope
Two decision-dense flows that drive most branch logic: delivery-code confirmation and escrow release.

## 1. Delivery confirmation with 6-digit code (`BR-SHP-02/03`, `ORD-04`, `UC-013`/`UC-030`)

```mermaid
flowchart TD
  A[Order reaches OUT_FOR_DELIVERY] --> B[6-digit code issued & sent:<br/>SMS primary, WhatsApp failover inside validity window]
  B --> C{Code entered?}
  C -->|correct & attempts < 3| D[Order → DELIVERED<br/>escrow 7-day hold starts]
  C -->|wrong| E[Attempts = attempts + 1]
  E --> F{attempts < 3?}
  F -->|yes| G[Show remaining attempts<br/>customer/courier informed]
  G --> C
  F -->|no — 3rd failure| H[Lock confirmation 24 h<br/>auto-create support ticket (SHP-02)]
  H --> I[Escalate to admin with full timeline after 3 failed attempts (SHP-05)]
  D --> J[order_status_history appended with actor/time/reason (ORD-05)]
```

**Invariants:** code stored only as hash ≥ 32 bytes + nonce, never plaintext, never logged (`SHP-03`) · no admin/courier shortcut to `DELIVERED` (`ORD-04`) · no GPS anywhere (`C-16`).

## 2. Escrow hold → release (`BR-ESC-01/02`, `ESC-01`, `UC-039`)

```mermaid
flowchart TD
  A[DELIVERED] --> B[Escrow hold starts — 7 days]
  B --> C{7 days elapsed?}
  C -->|no| B
  C -->|yes| D{Active dispute<br/>or state in DISPUTED / RETURN_* / REFUNDED?}
  D -->|yes| E[Release job no-ops this sub-order<br/>only disputed sub-orders frozen (ESC-06)]
  E --> F{Admin resolves dispute?}
  F -->|resolved for vendor| G[Resume release path]
  F -->|resolved for buyer| H[Refund path: escrow first, then vendor payable (ESC-03)]
  D -->|no| I[Release: commission computed at release (bps 500–2000, default 1000)<br/>ledger postings balanced, Σ = 0 (MNY-03)]
  I --> J[Payout batch scheduled 3–7 business days,<br/>min 1,000 YER else ROLLED_OVER, KYC=APPROVED only (ESC-04)]
  G --> I
```

## Invariants
Zero ledger imbalance (`MNY-03`, `NFR-008`) · refund draws escrow first, then vendor payable (`ESC-03`) · privileged money decisions write an audit row (`RET-04`) · daily reconciliation job alerts finance on any mismatch (`ESC-05`).

## Open questions (COM-01)
1. `ORD-08`/`D-12`: release-vs-return/dispute race at `COMPLETED` — ADR required before implementing the release job's dispute check.

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 12, session 005) | analysis-agent |
