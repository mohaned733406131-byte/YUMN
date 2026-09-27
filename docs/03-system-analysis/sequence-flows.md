---
document_id: DOC-SA-007
title: Key Sequence Flows
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-007, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016]
related_documents: [DOC-SA-004, DOC-SA-010, DOC-BA-004, DOC-WF-001, DOC-BA-005]
---

# Key Sequence Flows

Five end-to-end sequences as text sequence diagrams (`SQ-01…SQ-05`), complementing the business-side walkthroughs in `01-business-analysis/workflows/` (`WF-001…WF-012`) and the state machine in `state-transitions.md` (DOC-SA-010). Participants are **logical components** (`LC-*`, DOC-SA-006), not classes or services. Alternate and failure branches are shown inline with `✗` markers; rule IDs are referenced, never restated.

## SQ-01 — Browse → Cart → Checkout → Order → Delivery → Completion

Covers `WF-002`, `WF-003`, `WF-004`, `WF-005`, `WF-006`; use cases `UC-006`, `UC-009`, `UC-011`, `UC-019`, `UC-030`, `UC-039`.

```text
Customer   LC-06      LC-02/03     LC-07/08     LC-10/12    LC-09      LC-14      LC-16     LC-23
   │        Discovery  Catalog/Inv  Cart/Checkout Wallet/Esc  Order      Delivery   Notif.    Jobs
   │          │           │            │            │          │          │          │         │
   │─search──►│           │            │            │          │          │          │         │
   │          │─docs─────►│            │            │          │          │          │         │
   │◄─results─┤           │            │            │          │          │          │         │
   │─add item─────────────────────────►│            │          │          │          │         │
   │          │           │─reserve(15m)───────────►│ (inv)    │          │          │         │
   │          │           │◄─granted / ✗conflict────┤          │          │          │         │
   │─checkout─────────────────────────►│            │          │          │          │         │
   │          │           │            │─quote fee──────────────────────►│          │         │
   │          │           │            │─validate coupon──►LC-18         │          │         │
   │          │           │            │─server totals (VAT BR-FIN-01)   │          │         │
   │◄─review/confirm──────┤            │            │          │          │          │         │
   │─confirm(key)─────────────────────►│            │          │          │          │         │
   │          │           │            │─debit(total,key)────►│          │          │         │
   │          │           │            │            │─post DR/CR + escrow funding     │         │
   │          │           │            │◄─payment OK──────────┤          │          │         │
   │          │           │            │─create master+subs(key)────────►│          │         │
   │          │           │◄─permanent deduct─────────────────┤ (paid)   │          │         │
   │          │           │            │            │          │─PLACED alert────────►│       │
   │◄─order confirmed + timeline───────┼────────────┼──────────┤          │          │         │
   │          │           │            │            │          │          │          │         │
   │          │           │            │            │  Vendor: accept → process → ready        │
   │          │           │            │            │          │─READY_FOR_PICKUP───►│         │
   │          │           │            │            │          │◄─offer zone couriers┤         │
   │          │           │            │            │          │   (Courier accepts: BR-SHP-04)│
   │          │           │            │            │          │◄─ASSIGNED/PICKED_UP/IN_TRANSIT┤
   │          │           │            │            │          │─OUT_FOR_DELIVERY───►│─code────►│
   │◄─delivery code (SMS/WhatsApp)─────┼────────────┼──────────┼─────────────────────┤         │
   │─share code with courier (out-of-band, C-16)     │          │          │          │         │
   │          │           │            │            │          │◄─verify code (≤3 attempts)────┤
   │          │           │            │            │          │─DELIVERED ─► escrow 7-day hold │
   │          │           │            │            │  LC-23: after 7d, guards pass (BR-ESC-02) │
   │          │           │            │            │          │─COMPLETED + commission release │
   │◄─completion notice───┼────────────┼───────────►│          │          │          │◄────────┘
```

**Branches:** `✗` stock conflict at reserve → cart error, no order (`BR-CRT-05`); insufficient balance → top-up branch `SQ-04` (`BR-CRT-06`); price changed since add → re-confirm (`BR-CRT-04`); duplicate confirm with same key → original order returned (`BR-ORD-06`); payment OK but order write fails → compensation refunds the debit (`BR-PLT-04`, see `failure-modes.md`); 3rd bad code → 24-h lock + ticket (`BR-SHP-03`); dispute before day 7 → escrow frozen (`BR-ORD-05`).

## SQ-02 — Return Flow

Covers `WF-007`; use cases `UC-012`, `UC-021`.

```text
Customer   LC-09       LC-15        LC-14/LC-09   Vendor     LC-10        LC-19      LC-16
   │        Order       Returns      Delivery      (ACT-02)   Wallet       Admin      Notif.
   │─open return (reason, photos)──►│              │          │            │          │
   │          │◄─window check: delivery date + returnPeriodDays (BR-RET-01, C-11)     │
   │          │   ✗ window elapsed / !isReturnable → reject, notify ◄────────────────┤
   │─RETURN_REQUESTED───────────────►│              │          │            │          │
   │          │                      │─────────────►│ decision request ─────────────►│
   │          │◄── 48h SLA; after 48h auto-escalate to admin (DOC-SA-010) ───────────┤
   │          │   ◄── RETURN_APPROVED (pickup scheduled) or RETURN_REJECTED (reason) ─┘
   │          │◄─────────────── return pickup via LC-14 ──────────────│          │
   │          │─RETURN_RECEIVED─────────────────────►│ inspect ≤72h (BR-RET-05)      │
   │          │   ✗ no decision in 72h → auto-approve (System)                     │
   │          │─REFUNDED───────────────────────────────────────────►│              │
   │          │                      │              │   credit item value (+shipping if platform fault, BR-RET-03)
   │          │                      │              │   ≤3 business days (BR-RET-04) │
   │          │─commission reversal + escrow adjustment (BR-RET-07, BR-ESC-04/07) ──►│
   │◄─refund notice + wallet statement update─────────────────────────────────────────┤
```

**Branches:** `✗` dispute opened during return → admin is final arbiter (`BR-RET-06`), audit entry written (`BR-PLT-06`); escrow insufficient for refund → vendor payable draw (`BR-ESC-07`); master order completes only after all sub-orders settle (`BR-ORD-07`).

## SQ-03 — Vendor Onboarding

Covers `WF-011`; use cases `UC-015`, `UC-017`, `UC-031`.

```text
Vendor     LC-01       LC-05        LC-19/LC-24   Admin      LC-02        LC-16
 (ACT-02)  Identity    Store/Vendor Audit         (ACT-04)   Catalog      Notif.
   │─register phone + password──────►│             │          │            │
   │◄─OTP request────────────────────┼────────────────────────────────────►│
   │─verify OTP (6d/5m/3 tries, BR-AUTH-03)───────►│          │            │
   │◄─verified account + JWT (15m/7d, C-08)────────┤          │            │
   │─store profile + KYC documents────────────────►│          │            │
   │          │             │─validate type/size/malware (SEC-REQ-011)    │
   │          │             │─queue KYC decision + audit entry───────────►│
   │◄───────────────────────┼──────────────────────┤          │            │
   │          │             │   KYC decided ≤48h (BR-VND-03): APPROVED / REJECTED (resubmit allowed)
   │          │◄───────────┤ APPROVED (BR-VND-01 gate opens)  │            │
   │─create product (Arabic name, price, category, image, stock)─────────►│
   │          │             │   ✗ not approved → rejected (BR-VND-01)      │
   │          │             │   validations BR-CAT-01…05, BR-CAT-08        │
   │◄─product ACTIVE───────────────────────────────────────────┤─index doc─►LC-06
   │─orders now routable; store visible in discovery ─────────────────────►│
```

**Branches:** `✗` suspension later (`BR-VND-04`) hides products, blocks new orders, freezes existing, holds payouts; staff invite limited to Owner (`BR-VND-06`); one store per vendor (`BR-VND-02`).

## SQ-04 — Wallet Top-Up (mobile wallet and bank transfer)

Covers `WF-009`; use cases `UC-034`, plus top-up step inside `UC-011`.

```text
Customer   LC-10       LC-21          Provider      LC-11      Admin      LC-19      LC-16
           Wallet      PayProvider    (m-Floos/     Ledger     (ACT-04)   Audit      Notif.
   │─start top-up(amount, method)──►│               OneCash)    │          │          │
   │          │  ✗ amount ∉ [1,000 … 5,000,000] YER → error (BR-PAY-02)    │          │
   │          │─initiate(amount, ref)─────────────►│             │          │          │
   │◄─redirect / prompt─────────────┤              │             │          │          │
   │───customer pays at provider──────────────────►│             │          │          │
   │          │              │─signed callback / reconciled poll──────────►│          │
   │          │◄─verified credit (BR-PAY-03)───────┤             │          │          │
   │          │   ✗ no callback → reconciliation job retries (INT-REQ-001) │          │
   │          │─post balanced pair (credit wallet)─►│             │─audit───►│          │
   │◄─balance updated + receipt──────────────────────────────────────────────────────►│
   │                                                                   │          │
   │  — bank transfer variant (INT-REQ-002) —                          │          │
   │─submit transfer reference───────────────────────────────────────►│          │
   │          │◄─admin verifies reference (BR-PAY-04)─────────────────┤          │
   │          │─post credit only after approval───►│                 │─audit───►│
   │◄─credited notice────────────────────────────────────────────────────────────┤
```

**Branches:** `✗` duplicate callback with same reference → no-op (idempotency, `BR-PAY-08`); frozen wallet cannot top up (`BR-PAY-09`); provider outage → intent stays pending, reconciliation closes it; client claim of success without callback → rejected (`BR-PAY-03`).

## SQ-05 — Dispute

Covers `WF-008`; use cases `UC-033`, `UC-012`.

```text
Customer/Vendor  LC-09       LC-12        LC-19       Admin      LC-10      LC-16
   │              Order       Escrow       Audit       (ACT-04)   Wallet     Notif.
   │─raise dispute(evidence)──────────►│              │          │          │
   │              │─DISPUTED (before COMPLETED; BR-ORD-05)       │          │
   │              │─freeze escrow────────►│           │          │          │
   │              │   ✗ release timer fires during dispute → blocked (BR-ESC-02)
   │              │───────────audit entry (actor, reason)───────►│          │
   │◄─────────────┼───────────────────────┤──────────────────────┤─notice──►│
   │              │              │         │◄─review evidence + timeline────┤
   │              │              │         │   rules: BR-ORD-05, BR-RET-06 (policy vs dispute)
   │              │─resolution: for vendor → COMPLETED ──────────┤          │
   │              │        or  for buyer  → REFUNDED ───────────►│ credit wallet
   │              │              │─unfreeze / release or unwind──►│          │
   │              │───────────audit (before/after)──────────────►│          │
   │◄─outcome notice + timeline update───────────────────────────────────────┤
```

**Branches:** `✗` dispute on one sub-order freezes only that sub-order (`state-transitions.md` §4); post-COMPLETED dispute allowed within policy, admin-only after release; refund draws escrow first then vendor payable (`BR-ESC-07`); commission reversed proportionally (`BR-ESC-04`).

## Sequence Conventions

1. Every sequence starts from a precondition of `01-business-analysis/` (`UC-*`, `WF-*`) and ends in one of the 17 states or an unchanged state — no invented states (`C-09`).
2. Arrows labelled `✗` are failure exits; each names the governing `BR-*` or constraint.
3. Time-based steps (15-min reservation, 48-h KYC/decision SLA, 72-h inspection, 24-h escalation, 7-day escrow, 3–7-day payout) are driven by LC-23 jobs, never by a client timer.
4. Notifications appear as the last leg of every user-visible transition; security notifications are never suppressible (`BR-NTF-02`).
5. Physical-level realizations (endpoints, queues, transactions) are documented in `07-api/`, `04-architecture/data-flow.md` and `06-backend/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
