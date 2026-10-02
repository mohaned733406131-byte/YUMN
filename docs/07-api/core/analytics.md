---
document_id: DOC-API-018
title: API-ANL — Vendor Analytics, Statements & Admin Reports (FR-018, FR-020)
category: 07-api
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [FR-018, FR-019, FR-014, FR-020, FR-012, NFR-019, DATA-REQ-006, DATA-REQ-007, DATA-REQ-008, BR-FIN-01, BR-FIN-02, BR-FIN-03, BR-FIN-04, BR-ESC-03, BR-ESC-08, BR-VND-07, BR-PLT-06]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-FR-018, DOC-FR-020, DOC-BA-005, DOC-OVR-008]
---

# API-ANL — Vendor Analytics, Statements & Admin Reports

**Group:** `API-ANL` · **FR-018 (vendor insights), FR-020 (admin monitoring)** · **Endpoints:** `API-ANL-001…009` · **Base:** `/api/v1`

Dashboard/report data is computed from the append-only ledger and order history — no endpoint mutates data. Vendor exports are **CSV with UTF-8 BOM** and formula-injection hardening (cells starting `= + - @` prefixed with `'`) capped at **50,000 rows**; amounts are whole YER with the exact `.total` metadata alongside any estimate. Monthly statements (`BR-FIN-04`) are settlement documents: gross sales − refunds − commission + payouts, downloadable as PDF or CSV. Daily reconciliation (`BR-ESC-08`, `BR-FIN-03`) compares ledger/wallet/escrow/payable totals against provider statements and exposes mismatches to admins only.

---

## 1. Endpoint Table

### 1.1 Vendor

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ANL-001 | `GET /store/dashboard` | `VENDOR` | FR-018 core screen: sales/orders/fulfillment/payment metrics with trend series | `?from&to&compare=prev_period\|none` → `200 { period, totals: { salesYER, orders, avgBasketYER, refundRatePercent, onTimeDeliveryPercent, views?, conversionPercent? }, trend: [ { date, salesYER, orders } ], topProducts: [ { productId, name, units, revenueYER } ], breakdown: { paidByWallet: {...} } , totalsMeta: { sales: { value, relation: "exact" } } }` — every estimate is annotated | `NOT_FOUND`, `STORE_SUSPENDED`, `VALIDATION_ERROR` | FR-018, `BR-VND-07`, `BR-FIN-01/02`, `UC-022` |
| API-ANL-002 | `GET /store/reports/{family}` | `VENDOR` | Tabular report — families: `sales`, `orders`, `returns`, `payouts` | `?family&from&to&page&pageSize` → `200 { family, columns: [...], rows: [...], page: {…}, total: { value, relation } }` | `VALIDATION_ERROR` (unknown family), `NOT_FOUND`, `STORE_SUSPENDED` | FR-018, DATA-REQ-006 |
| API-ANL-003 | `GET /store/reports/{family}/export` | `VENDOR` (Manager/Owner) | CSV download of the same report, streamed inline | `?family&from&to` → `200 text/csv` (≤50,000 rows; UTF-8 BOM; Excel formula injection guarded by `'`-prefixing cells starting `= + - @`) | `LIMIT_EXCEEDED` (row cap), `VALIDATION_ERROR`, `NOT_FOUND`, `STORE_SUSPENDED` | FR-018, DATA-REQ-006, NFR (CSV export rules), `UC-022` |
| API-ANL-004 | `GET /store/statements/{month}` | `VENDOR` (Owner) | Monthly settlement statement: gross − refunds − commission ± adjustments = payable, with payout history | `month=YYYY-MM` → `200 { month, grossSalesYER, refundsYER, commissionYER, adjustmentsYER, netPayableYER, payout: { requested, executed, rolledOver }, ledgerRefs: [...], pdfUrl? }` — figures tie to the append-only ledger (`DATA-REQ-007`) | `VALIDATION_ERROR` (bad month), `NOT_FOUND`, `STORE_SUSPENDED` | FR-018, FR-014, `BR-FIN-04`, `BR-ESC-03`, `UC-022` |
| API-ANL-005 | `GET /store/statements/{month}/export` | `VENDOR` (Owner) | Statement export streamed inline (CSV obeys the same 50k/BOM/formula rules) | `?format=pdf\|csv` → `200` (`text/csv` or `application/pdf`) | `LIMIT_EXCEEDED`, `VALIDATION_ERROR`, `NOT_FOUND` | FR-018, `BR-FIN-04` |

### 1.2 Admin

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-ANL-006 | `GET /admin/dashboard` | `ADMIN`, `MODERATOR` | Platform health: GMV, orders by state, SLA breaches, top vendors, KYC queue depth, delivery success | `?from&to` → `200 { gmvYER, orders: { byState: {...} }, sla: { sla24hEscalations, overdueDecisions }, fulfillment: { onTimePercent, failedAttempts }, queues: { kyc, returns, disputes, topups }, topVendors: [...], totalsMeta: {...} }` | `FORBIDDEN` (Moderator subset), `VALIDATION_ERROR` | FR-020, `BR-ORD-10`, `UC-033` |
| API-ANL-007 | `GET /admin/reports/{family}` | `ADMIN`, `MODERATOR` | Platform report — families: `orders`, `gmv`, `vendors`, `delivery`, `returns`, `kyc`, `users` | `?family&from&to&page&pageSize&groupBy?` → `200 { family, columns, rows, page: {…}, total: { value, relation } }` | `VALIDATION_ERROR`, `FORBIDDEN` | FR-020, DATA-REQ-006 |
| API-ANL-008 | `GET /admin/reports/{family}/export` | `ADMIN` | CSV export of an admin report streamed inline (Moderator excluded) | `?family&from&to` → `200 text/csv` (same CSV safeguards, 50k cap) | `LIMIT_EXCEEDED`, `FORBIDDEN`, `VALIDATION_ERROR` | FR-020, DATA-REQ-006 |
| API-ANL-009 | `GET /admin/reconciliation` | `ADMIN` | Daily reconciliation result: ledger vs wallet vs escrow vs payable vs provider statements (`BR-ESC-08`, `BR-FIN-03`) | `?date&status` → `200 { items: [ { date, source: "MFLOOS"\|"ONECASH"\|"BANK"\|"INTERNAL", ledgerTotal, providerTotal, deltaYER, status: "MATCHED"\|"MISMATCH", resolvedBy?, note? } ], totals: { mismatches, unresolvedYER } }` | `VALIDATION_ERROR`, `FORBIDDEN` | FR-014, FR-020, `BR-ESC-08`, `BR-FIN-03`, `BR-PLT-06` |

## 2. Behavior Notes

- **Exact vs estimated** (`NFR` reporting rules): money and count totals carry `totalsMeta` with `relation: "exact" | "estimate"`; only legally relevant money is exact (from the ledger), trend/sampling outputs may be estimates and are labeled.
- **Payout eligibility** (`BR-ESC-05`): `netPayableYER` below 1,000 YER appears as `belowMinimumRollover` — visible here and in `wallet.md` `GET /store/finance/overview`.
- **Commission** (`BR-ESC-03`): reports show `commissionRatePercent` (5–20%, default 10%) applied at release; statements never invent fees not in the ledger.
- **Role scoping** (`BR-ORD-09`, `DATA-REQ-008`): vendor endpoints return only own-store rows (foreign ⇒ 404); Moderators see platform aggregates without finance exports.
- **Idempotent reads**: all endpoints are `GET`; exports are pure reads of the same dataset as CSV/PDF — repeated downloads always return the current figures.
- **Performance** (`NFR`): dashboards served ≤ 1 s p95 via pre-aggregated rollups refreshed on state transitions + nightly backfill; heavy families (`gmv`, `delivery`) may return `relation: "estimate"` before the nightly job lands.
- **Reconciliation outputs** feed `GET /admin/audit-log` (`admin.md`) — resolution always writes an audit entry (`BR-PLT-06`).

## 3. Pagination / Idempotency / Caching

| Endpoint(s) | Mode |
|---|---|
| `API-ANL-002`, `API-ANL-007` (tables) | offset |
| `API-ANL-001`, `API-ANL-006` (dashboards) | n/a (single object) |
| `API-ANL-004`, `API-ANL-009` | single resource / bounded list |

Exports stream inline (`Content-Disposition: attachment`) and are capped at 50,000 rows (`LIMIT_EXCEEDED` beyond that). Dashboard responses: `Cache-Control: max-age=30`; everything else `no-store`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
