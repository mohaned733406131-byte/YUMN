---
document_id: DOC-NFD-007
title: Compliance & Legal Detail — Data Protection, Wallet Regulation, VAT & Legal Deliverables
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-019, NFR-017, NFR-011, FR-003, FR-020, DATA-REQ-002, DATA-REQ-003, SEC-REQ-010]
related_documents: [DOC-NFD-001, DOC-NFR-019, DOC-AC-001, DOC-OVR-003, DOC-BA-005, DOC-DTA-005, DOC-SEC-001]
---

# Compliance & Legal Detail — Data Protection, Wallet Regulation, VAT & Legal Deliverables

Elaborates the compliance domain behind **NFR-019** (PDPA-aligned controls, VAT on every order, ≥ 5-year audit retention) and its launch gate `AC-S-24`. The controlling method: **compliance is demonstrated with evidence — checklists, automated tests and sign-offs — not asserted** (`NFR-019`). Every item below is either `VERIFIED` (canon), `INFERENCE` (derived, needs confirmation) or `INSUFFICIENT EVIDENCE` (open legal position). Legal opinions arrive via **`DEP-09`**; Central Bank wallet position via **`DEP-10`** (`ASM-12`).

## 1. Legal Register (jurisdiction: Republic of Yemen)

| # | Area | Position (as canon states it) | Evidence status | Resolution |
|---|---|---|---|---|
| L1 | **Personal data protection** | Yemeni **Law No. (11) of 2012 on Personal Data Protection** — applicable; control detail `INSUFFICIENT EVIDENCE` (`project-context.md` §Compliance) | `INSUFFICIENT EVIDENCE` | `DEP-09` legal opinion → checklist completion → `ASM-13` |
| L2 | **PDPA-aligned controls** | NFR-019 mandates minimisation, purpose limitation, retention/deletion, user rights — applied "as far as evidence allows" (`DATA-REQ-002` R5) | partial `VERIFIED` (control set), detail `INSUFFICIENT EVIDENCE` | `AC-NFR-019-02` checklist 100% + `DEP-09` |
| L3 | **Closed-loop wallet regulation** | Central Bank of Yemen mobile-payment rules govern a platform-operated wallet (`C-01`, `ASM-12`) | `INFERENCE` — **DANGEROUS assumption** | **`DEP-10`**: legal opinion **before implementation**; if refused → fundamental redesign (wallet-only model at risk) |
| L4 | **VAT** | VAT collected from the buyer on **every order** (`BR-FIN-01`, `NFR-019`); rate/treatment per `ASM-10` (`UNSUPPORTED` pending legal confirmation) | rate/`REM`-mechanics `INSUFFICIENT EVIDENCE`; obligation to charge `VERIFIED` | `DEP-09` confirms rate, filing and remittance |
| L5 | **Financial record retention** | ≥ **5 years** for financial/audit records (`NFR-019`, `DATA-REQ-003`); configured 10 years as margin (`DOC-DTA-005`) | floor `VERIFIED`; exact statutory periods `INSUFFICIENT EVIDENCE` | `DEP-09` / `ASM-13`; configured period may rise, **never below 5 y** |
| L6 | **Consumer protection / returns** | 14-day return policy, escrow 7-day release (`C-11`, `C-12`) — platform policy as documented | `VERIFIED` as product rules; statutory consumer-rights baseline `INFERENCE` | confirm via `DEP-09` that policy ≥ statutory minimum |
| L7 | **Messaging/marketing consent** | OTP/transactional sends allowed as service traffic; **marketing requires opt-in**; security notices cannot be opted out (`BR-NTF-02`, `BR-NTF-05`) | `VERIFIED` as rules; telecom template compliance `INFERENCE` | provider template approval at `DEP-06` |
| L8 | **Cross-border processing / hosting** | storage location + processors (SMS, WhatsApp, wallet providers, MinIO host) must be assessed under Law 11/2012 | `INSUFFICIENT EVIDENCE` | sponsor confirmation + `DEP-09`; design change → ADR |
| L9 | **Sanctions / AML-KYC posture** | KYC exists for vendor payout eligibility (`BR-ESC-06`) and admin-triggered checks — **not** a full AML program | scope `INFERENCE` | `DEP-09` defines whether statutory AML duties attach; no claim made until opined |

No legal claim in this file may be repeated as fact downstream; unresolved rows are launch blockers under `AC-S-24`.

## 2. Data-Protection Controls (PDPA-aligned, implementable today)

| Control | Implementation | Canon |
|---|---|---|
| **Data minimisation** | never collect: card PAN (`C-02`), GPS/coordinates (`C-16`), biometrics (`C-07`), email as identity (`BR-AUTH-08`); national ID only if legally compelled — currently not collected | `DATA-REQ-002` R3, `16-data/data-classification.md` |
| **Purpose limitation** | each data category mapped to a purpose/owner in the data inventory; secondary use requires inventory update | `16-data/data-ownership.md` |
| **Retention & deletion** | retention classes `RC-01…RC-09`; customer deletion run leaves financial/audit records intact (legal-hold exemption) | `DATA-REQ-003`, `FR-003` privacy tests |
| **User rights** | export of personal data (audited admin export, `UC-036`); erasure where no legal hold applies | `FR-003`, `BR-PLT-06` |
| **Security of processing** | encryption at rest for PII columns (`SEC-REQ-006`), TLS in transit, RBAC least privilege, append-only audit (`SEC-REQ-010`) | `DOC-SEC-*` |
| **Breach readiness** | security-incident runbook (observability §7 item 10); audit trail enables impact scoping | `NFR-020`, `SEC-REQ-010` |
| **Evidence** | checklist mapped to implemented features + tests, signed by compliance owner (STK-11) | `AC-NFR-019-02` |

## 3. Wallet & Payment Regulation (existential lane)

| Obligation | Mechanism | Gate |
|---|---|---|
| Legitimacy of closed-loop wallet | legal opinion on Central Bank position | **`DEP-10` before implementation**; negative result triggers redesign decision + ADR |
| Client money segregation | escrow + ledger model: platform holds funds in trust-like sub-ledgers per customer/vendor; daily reconciliation to provider statements (`BR-ESC-08`, `BR-FIN-03`) | `AC-S-14`, `AC-S-15` |
| Ledger integrity for regulators | double-entry, append-only, before/after audit on every money op (`BR-PLT-06`), ≥ 5-y (configured 10-y) retention | `SEC-REQ-010`, `OBJ-08` |
| Wallet freeze powers | admin freeze for legal/security reasons; frozen wallet still receives refunds (`BR-PAY-09`, `EC-23`) | `FR-020` |
| Provider terms | m-Floos, OneCash, bank-transfer partner contracts at `DEP-05` | launch dependency |
| No card data ever | `C-02`: wallet/top-up rails only — eliminates card-scope compliance entirely | `C-02` |

## 4. VAT — Boundary Matrix & Evidence (feeds `AC-NFR-019-01`)

| Flow | VAT treatment (as canon requires) | Rule source |
|---|---|---|
| Product subtotal | **15% VAT on (subtotal − discount)**; shipping **not** taxed | business-rules (BR-FIN family), `DOC-UX-008` money examples |
| Displayed price | order confirmation and all money screens show subtotal, discount, VAT, shipping, total as **separate lines** in integer YER, Arabic-Indic digits in `ar` | `BR-PAY-10`, `DOC-UX-007` §4 |
| Every order | VAT calculated server-side on every order — checkout cannot bypass | `BR-FIN-01`, `NFR-019` |
| Escrow split | escrow/release amounts derive from the already-taxed total; refunds reverse the same figures | `C-12`, ledger rules |
| Vendor payout | payout = vendor's share of taxed totals less commission; VAT line remains platform-visible | `BR-ESC-*` family |
| Top-up | wallet top-up itself is not a sale — not VAT-charged (`INFERENCE`) | confirm in `DEP-09` |
| Remittance liability | collected VAT held for remittance per tax rules; model as payable until remitted | `business-model.md` §3 (`ASM-10` `UNSUPPORTED`) |
| Reporting | admin finance reports expose VAT collected per period (exact figures from ledger, not estimates) | `07-api/endpoints/analytics.md` `totalsMeta` rule |

**Evidence**: boundary-matrix test suite (100% green) + sampled production-like orders with correct breakdowns = `AC-NFR-019-01`. Rate, filing cadence and remittance mechanics remain `INSUFFICIENT EVIDENCE` until `DEP-09`/`ASM-10` resolve — tests use the canon-configured rate constant, not a hardcoded assumption.

## 5. Legal Deliverables & Sign-Off Checklist (launch gate `AC-S-24`)

| # | Deliverable | Owner | Depends on | Status |
|---|---|---|---|---|
| 1 | Data-protection opinion (Law 11/2012) + completed PDPA checklist | STK-11 / external counsel | `DEP-09` | open |
| 2 | Central Bank wallet-position opinion | sponsor / counsel | `DEP-10` | open (**blocking**, `ASM-12`) |
| 3 | VAT treatment opinion (rate, remittance, filing) | counsel / finance | `DEP-09` / `ASM-10` | open |
| 4 | Retention-period opinion (statutory floors vs configured 10 y) | counsel | `DEP-09` / `ASM-13` | open |
| 5 | Processor/DPA set: SMS, WhatsApp, wallet providers, hosting/MinIO host | STK-11 + procurement | `DEP-05`, `DEP-06` | open |
| 6 | Terms of service + privacy notice, bilingual, authoritative version noted | counsel + `DOC-UX-007` §6 tone rules | items 1–4 | open |
| 7 | Return/refund policy statement vs statutory consumer rights | counsel | `C-11`, `C-12` | `INFERENCE` confirm |
| 8 | Messaging-consent wording (marketing opt-in; security non-opt-out) | counsel + product | `BR-NTF-02/05` | `INFERENCE` confirm |
| 9 | Accessibility statement (WCAG 2.1 AA claim scope) | product | `NFR-011`, `DOC-UX-006` | draft |
| 10 | Evidence pack: VAT tests, retention guard test, audit-trail sample, checklist sign-off | STK-11 | `AC-NFR-019-01/02` | assembled at gate |

All ten recorded as sign-off evidence for `AC-S-24`; unresolved blocking items (esp. 2) stop implementation — recorded in `20-validation/missing-information.md` when that register is authored (no new gap IDs minted outside the canonical GAP register, per `DOC-DTA-005` convention).

## 6. Accessibility, Localization & Ethics Overlap

| Topic | Compliance hook | Where the detail lives |
|---|---|---|
| Accessibility claim | WCAG 2.1 Level AA (`NFR-011`), ≥ 95% automated pass, 0 critical | `DOC-UX-006` §9, `NFR-011` |
| Bilingual legal text | legal/tax labels translated; **authoritative version noted on the page** | `DOC-FE-008`, `DOC-UX-007` §6 |
| Arabic-first consumer fairness | prominent-display rules for material terms (order confirmation screens show full breakdown) | `DOC-UX-005`, `DOC-UX-008` |
| No dark patterns | engagement channels respect preference center; marketing gated by opt-in | `DOC-UX-008` §3, `BR-NTF-05` |

## 7. Verification Hooks

| Detail | Feeds |
|---|---|
| §4 VAT boundary-matrix tests + sampled orders | `AC-NFR-019-01` |
| §2 checklist 100% + §5 sign-offs on file + §3 retention evidence (≥ 5 y, guard test) | `AC-NFR-019-02`, `AC-S-24` |
| §1 rows L1–L9 remain open with owners | `ASM-09…ASM-13`, `DEP-09`, `DEP-10` register |
| §3 wallet opinion | `ASM-12` (DANGEROUS) resolution |
| §6 accessibility/localization claims | `AC-NFR-011-*`, `NFR-013` |

## 8. Evidence Discipline

- Rows are re-reviewed at every launch gate; a status may only improve with the referenced dependency landing.
- `INFERENCE` rows must not be quoted downstream as facts (root README §8).
- This file is **not** legal advice; it is the operational checklist that binds counsel opinions to implementation evidence.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
