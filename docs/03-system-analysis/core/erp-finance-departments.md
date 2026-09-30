---
document_id: DOC-SA-011
title: ERP & Finance Departments — accounts, sales, purchases, inventory, reports, periods
category: 03-system-analysis
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-014, FR-020]
related_documents: [DOC-OVR-008, DOC-SEC-004, DOC-VAL-004, DOC-VAL-002]
---

# ERP & Finance Departments — accounts, sales, purchases, inventory, reports, periods

This document is the **analysis-level design of the platform's finance/ERP department surface**: the six
departments (accounts, sales, purchases, inventory, reports, periods), the scope each book gives its
operators, the surfaces through which those departments are used, and the period-close mechanics that
govern them. It records the departmental coverage of [`plan-develop.md`](../../../plan-develop.md) §4.1,
§4.2 and §4.5 as approved through that plan's §8 decisions `D2`, `D3` and `D11` — the department model
is therefore approved scope, not a brainstorm.

It is **not** an implementation. Phase 1 has not started, no endpoint, table, job or test exists for
any department below, and nothing here is `VERIFIED` (`SPE-03`). The document is a design contract for
the build that follows approval, and it mints no new identifiers: every `FR-*`, `BR-*`, `API-*`, `DB-*`
and decision ID cited here already exists in the knowledge base.

## Operating model

**Two sets of books, one ledger of truth.** yumn keeps a **platform book** plus one **merchant book per
store** as sub-ledgers of the single append-only double-entry ledger; the ERP — the in-platform core
under Option A, a satellite under Option B — holds the general ledger those sub-ledgers post into.

- **Multi-tenant by construction.** Every department below is scoped twice: platform administrators
  see and operate the whole book, each merchant sees only their own slice of it.
- **Ownership rule `DATA-REQ-008`** (with `BR-ORD-09`): foreign data ⇒ **404**, never a 403 that leaks
  existence. The enforcement table lives in [`rbac.md`](../../09-security/core/rbac.md) §6.
- **Integrity rule:** `LedgerService.post` remains the **only** money writer — `BR-PAY-06`, `NFR-008`,
  and forbidden pattern `F7` ("money writes outside B07") in
  [`module-boundaries.md`](../../04-architecture/core/module-boundaries.md).
- **The ERP never writes `b07`.** It receives postings and returns nothing money-shaped, so
  reconciliation stays one-way: yumn's own `J1`/`J2` invariants plus a ledger↔ERP journal diff.
- **Inventory is symmetric:** `b02` stays the operational source of truth; the ERP layer never writes
  availability back into yumn (that direction would permit oversell).

## Departments

The six departments of `plan-develop.md` §4.2, each row scoped per book and pinned to its phase:

| ERP department | Platform administrator scope | Merchant scope | Core objects / sources | Phase |
|---|---|---|---|---|
| **1. Accounts** (CoA, AR/AP, partner accounts) | Chart of accounts + account mapping (`P-02`), platform receivables (commission, fees, VAT collected), platform payables (vendor payouts, delivery-provider settlements, supplier bills), partner master (vendors, couriers, providers), AR/AP aging | Receivable from the platform = released escrow − commission − refunds (the payable balance already surfaced in `API-ANL-004`); own supplier AP **iff** purchases module enabled | mapping tables, ledger postings, `payout`, `escrow` | Phase 1 |
| **2. Sales** | Master/sub-orders, invoices & credit notes (`P-01`), refunds, GMV & commission revenue reports, invoice register, VAT collected | Own sub-orders, invoices issued on their behalf (downloadable copy), returns → credit notes, per-store sales journal | `b06` orders, `P-01` documents, `b09` returns | Phase 1 |
| **3. Purchases** (AP) | Platform operating procurement: bill for infra/hosting, SMS/WhatsApp credits, provider fees, partner services → approval → bill → payment record | Supplier procurement: purchase order → goods receipt → supplier bill → payment status (their money moves **outside** yumn; yumn only records it) | `purchase_order`, `goods_receipt`, `supplier_bill`, `vendor_bill_payment` (ERP domain — not marketplace money, no `b07` writes) | Platform AP Phase 1–2 · merchant procurement Phase 2 |
| **4. Inventory** | None as stock (the platform holds no inventory); aggregate stock-health metrics only | `b02.inventory` stays the operational source of truth (on-hand/reserved/available, 15-min TTL `C-13`, no-negative checks); the ERP layer adds locations, valuation (FIFO/AVCO), adjustments/losses, stock-move history and their journal impact | `b02` (SoR) → optional snapshot sync to ERP; **never** ERP → yumn availability (prevents oversell) | Snapshots Phase 1–2; valuation Phase 2 |
| **5. Accounting reports** | Trial balance, P&L, balance sheet, cash flow, VAT return (`P-03`), commission/fee revenue, payout & provider reconciliation, month-end close pack | Monthly statement (`BR-FIN-04`, `API-ANL-004/005`), invoice register, tax summary, AR/AP aging (if purchases on), inventory valuation report | read models over ledger + documents (`B11` pattern) | Phase 1 |
| **6. Periods & close** | Fiscal calendar (12 periods + year), open → adjust → close → lock, cutoff rules, close checklist with an owner per department, year-end carry-forward, period-boundary report locks | Statement period aligned to the platform period; their books go read-only when the platform period closes (downloads remain available) | `fiscal_period`, `close_checklist_item`, `period_lock` (`SUPER_ADMIN` action, audited `BR-PLT-06`) | Phase 1 |

## Department ↔ staff mapping

| ERP department | Owning org (platform) | Merchant-facing role | Guard |
|---|---|---|---|
| Accounts | `ORG-01` Finance (+ `ROLE-02` read-only auditor) | Vendor **Owner/Manager** | no ledger writes for anyone (`rbac` rows 15/16) |
| Sales | `ORG-01` (finance views) + `ORG-02` (merchant ops views) | Owner/Manager | invoices immutable once issued; void = credit note + audit |
| Purchases | `ORG-01` (opex approval) | Owner/Manager (`Editor` read) | payment is a **record**, never executed through yumn |
| Inventory | `ORG-02` oversight | Owner/Editor | `b02` stays operational SoR; valuation ≠ availability |
| Reports | `ORG-01`, `ORG-08` Executive (read-only) | Owner (own store only) | exports obey CSV rules; totals carry `totalsMeta` |
| Periods & close | `ORG-01` proposes, **`SUPER_ADMIN` locks** | — (read-only) | lock is audited; late entries only via adjustment journals |

- **No new actors.** Departments are permission bundles and queue scopes **inside `ADMIN`** — plan
  decision `D4`. The seven canonical actors and the cross-layer mapping invariant of
  [`rbac.md`](../../09-security/core/rbac.md) §8 are unchanged.
- **Org-departments `ORG-01`…`ORG-08` and staff bundles `ROLE-01`…`ROLE-09`** are specified in
  [`rbac.md`](../../09-security/core/rbac.md) §11 (minted 2026-09-28 via `plan-develop.md` §8 `D10`
  propagation). This table is the *module* model; it composes with that *permission* model rather
  than duplicating it.
- **`rbac.md` rows 15/16 stay absolute:** no department grants direct ledger/balance write (row 15) or
  another party's balance/transaction read (row 16). Recommended disposition `M-07` = **NO** — replace
  with read-only aggregate finance dashboards plus explicitly enumerated, audited support actions.

## Administration surfaces

- *Platform admin console — new "Finance & ERP" area:* tabs for **Accounts** (CoA mapping, partners,
  aging), **Sales** (invoice register, credit notes), **Purchases** (bill queue with four-eyes
  approval, PO list), **Inventory** (read-only stock health + adjustments approval), **Reports**
  (run/export, scheduled delivery), **Periods** (calendar, checklist, lock) and **Sync monitor**
  (outbox depth, held/review/resolved exceptions, mapping drift). Every mutation returns an `auditId`.
- *Vendor portal:* extend the existing Finance area (`UC-022`) with **Invoices**, **Tax summary**, and —
  when enabled — **Purchases** (PO/bill entry) and **Stock valuation**; statements and the
  balance/escrow/payout views already exist.
- *Interfaces:* admin endpoints follow the `API-ADM` group conventions documented in
  [`admin.md`](../../07-api/admin/admin.md); merchant endpoints follow `API-ANL`/`API-WAL` scoping
  (own store only, foreign ⇒ 404).

## Periods & close mechanics

- **Append-only corrections.** The ledger is never edited — corrections are compensating entries only
  (`DATA-REQ-007`; `LedgerService.post` = single writer, forbidden pattern `F7`). No back-dating, no
  row updates, no deletes.
- **A locked period rejects connector journals.** Late postings are queued as adjustment-period entries
  and replayed after the period opens again — never written over a closed period.
- **Close cadence** settles together with the still-open `CT-21` decision (hourly vs nightly vs daily
  chain/`J10` verification); one answer drives all batch, export and connector timings.
- **`J1`/`J2` must be green before lock.** `J1` (balance-vs-ledger) and `J2` (global invariant) gate the
  lock — a red invariant blocks locking rather than being reconciled away.
- **The lock is a `SUPER_ADMIN` action** and is audited (`BR-PLT-06`); `ORG-01` proposes the close, and
  merchant books become read-only when the platform period closes.

## Integration pointer

Connector mechanics — the transactional outbox written in the same DB transaction as the domain change,
the direction/payload map with per-flow idempotency keys, `SYSTEM`-class service accounts with scoped
rotated tokens, the held/review/resolved exception queue and the sandbox verification discipline — live
in `plan-develop.md` §4.4 and remain pending an integration-domain document under
[`10-integrations/`](../../10-integrations/README.md). From this document's viewpoint the connector is a
**read-side consumer**: postings, documents and close status flow outward only, and no connector job may
ever become a second money writer.

## Phasing

- **Phase 1:** department skeleton for accounts, sales, reports and periods (departments 1/2/5/6), plus
  `P-01` invoicing, `P-02` account mapping, the outbox spine (the connector backbone) and platform
  purchase-bill capture — department 3 starts here.
- **Phase 1–2:** purchase-bill approval flow + inventory snapshots (departments 3/4), `P-03` tax
  reports, `P-04` settlement runs, the ERP journal diff report, the admin "Finance & ERP" console and
  the vendor-portal finance extensions.
- **Phase 2:** merchant procurement and stock-valuation depth (departments 3/4 full).
- **ERP satellite (Option B)** stays a v2 option behind the connector port — decision `D2` chose
  **Option A now**, so a later switch is configuration, not re-platform.

## Decisions

| # | Decision | Outcome | Approved |
|---|---|---|---|
| `D2` | ERP strategy | **Option A** — in-platform ERP foundation + connector port (Option B satellite remains a v2 option) | 2026-09-28 (administrator) |
| `D3` | ERP block placement | Start inside existing `B07`/`B13` boundaries; promote to a new block only when size forces it | 2026-09-28 (administrator) |
| `D11` | ERP department depth for v1 | **core+** — accounts/sales/reports/periods plus platform purchases and inventory snapshots | 2026-09-28 (administrator) |

Source for all three rows: [`plan-develop.md`](../../../plan-develop.md) §8.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-28 | Initial authoring | plan-develop.md §4 approval implementation (session 007) |
