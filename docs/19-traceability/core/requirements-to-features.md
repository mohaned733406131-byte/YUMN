---
document_id: DOC-TRC-002
title: Requirements to Features — Objective & Feature Traceability Matrix
category: 19-traceability
status: approved
version: 1.6
created: 2026-09-27
updated: 2026-10-03
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-013, FR-020, NFR-001, SEC-REQ-001, DATA-REQ-007, INT-REQ-001]
related_documents: [DOC-TRC-001, DOC-TRC-003, DOC-REQ-001, DOC-AC-001, DOC-OVR-004, DOC-BA-005, DOC-UC-000, DOC-WF-001, DOC-API-001, DOC-DB-001]
---

# 19 — Requirements to Features

**The requirement → objective → feature/asset matrix.** Two matrices: **A** traces every objective down to the requirements that realise it; **B** traces every one of the 73 requirements forward to the assets it shapes — API group, representative endpoints, database entities, use cases, workflows, business rules, priority.

This file answers methodology item 40 (`docs/README.md` §10) for the *feature* side of the chain. The *test* side lives in `requirements-to-tests.md` (`DOC-TRC-003`); domain rules, vocabulary and the coverage dashboard live in `README.md` (`DOC-TRC-001`).

---

## 1. Scope & Method

**Universe:** 73 requirements — 20 `FR-001…FR-020`, 20 `NFR-001…NFR-020`, 16 `SEC-REQ-001…016`, 9 `DATA-REQ-001…009`, 8 `INT-REQ-001…008` (count verified against `02-requirements/requirements-overview.md`) — and 12 objectives `OBJ-01…OBJ-12`.

**Every cell is read from a file, never inferred from a name.** Column sources:

| Column | Source | Basis |
|---|---|---|
| Objective(s) | `02-requirements/[<family>/]<portal>/<ID>.md` §Rationale (`OBJ-NN` mentions; present in 20/20 `FR` and 17/20 `NFR` files, absent from every `SEC-REQ`/`DATA-REQ`/`INT-REQ` file); `00-project-overview/project-objectives.md` table (explicit `FR-*`/`NFR-*` references and the `FR-001…FR-020` range) | `VERIFIED` where present |
| Block | `02-requirements/requirements-overview.md` §1 (`B01…B13`) | `VERIFIED`, FR only |
| API group(s) | `07-api/README.md` §4 Group → Requirement Mapping (FR column and Key SEC/DATA/INT column) | `VERIFIED` |
| Representative endpoints | `07-api/*.md` endpoint-table *Related IDs* column, reversed to the requirement; capped at 3 shown + remainder counted | `VERIFIED` |
| DB entities | `08-database/*.md` frontmatter `related_requirements`, reversed | `VERIFIED` |
| UC / WF | `01-business-analysis/<portal>/UC-nnn.md` and `01-business-analysis/<portal>/workflow-nnn.md` frontmatter `related_requirements`, reversed; shown as `UC-… / WF-…` | `VERIFIED`, FR only |
| Business rules | `02-requirements/functional/core/FR-nnn.md` §Business Rules Applied | `VERIFIED`, FR only |
| Priority | `02-requirements/requirements-overview.md` §1 (FR); `02-requirements/core/SEC-REQ-nnn.md` header (SEC) | `VERIFIED` where present |

**Empty cell = `INSUFFICIENT EVIDENCE`** — the column has no supporting link for that requirement. A blank is never a silently implied link (`docs/README.md` §8).

---

## 2. Matrix A — Objective → Requirements

| Objective | Priority | Requirements traced (evidence basis) | Notes |
|---|---|---|---|
| OBJ-01 | Critical | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008 +12 more — objectives table range; objectives table; requirement file | All `FR-001…FR-020` IMPLEMENTED + VERIFIED |
| OBJ-02 | Critical | FR-005, FR-006, FR-011, FR-012, FR-013, FR-014, FR-016, FR-018 +3 more — requirement file | 100% of orders paid from wallet; escrow releases exactly per `BR-ESC-*`; zero ledger imbalance in audit reports |
| OBJ-03 | Critical | FR-003, FR-004, FR-008, FR-009, FR-017, FR-019, NFR-002, NFR-011 +2 more — requirement file | WCAG 2.1 AA pass ≥ 95%; RTL defects = 0 at release; Arabic is the default locale |
| OBJ-04 | Critical | FR-009, FR-010, NFR-001, NFR-002, NFR-003, NFR-004 — objectives table; requirement file | p95 API latency < 200 ms at 10,000 concurrent users (`NFR-001`, `NFR-003`) |
| OBJ-05 | Critical | NFR-005, NFR-006, NFR-007 — objectives table; requirement file | 99.99% monthly availability; RTO ≤ 1 h, RPO ≤ 15 min (`NFR-005`, `NFR-006`) |
| OBJ-06 | High | FR-004, FR-007, NFR-012 — requirement file | First vendor goes live (KYC approved → first listing) within 48 h of application; KYC decision SLA ≤ 48 h |
| OBJ-07 | High | FR-015, FR-017 — requirement file | ≥ 95% of deliveries confirmed within first code attempt; 0 successful deliveries without code |
| OBJ-08 | High | FR-012, FR-018, FR-020, NFR-008, NFR-014, NFR-019 — requirement file | 100% of state-changing admin actions audited; daily financial reconciliation reports available next morning |
| OBJ-09 | High | NFR-009, NFR-010 — requirement file | Automated test suites gate every release; regression suite < 30 min; defect escape rate to production < 5% of found defects |
| OBJ-10 | Medium | NFR-009 — requirement file | A new developer ships a validated change within 5 working days using this knowledge base alone |
| OBJ-11 | Medium | FR-004, FR-006, FR-007, FR-008, FR-009, FR-018, FR-019, NFR-012 +2 more — requirement file | Growth targets (vendors, listings, orders, GMV) defined and tracked from launch — baseline targets `INSUFFICIENT EVIDENCE` until sponsor sets them (`ASM-14`) |
| OBJ-12 | Critical | FR-001, FR-002, FR-004, FR-005, FR-010, FR-011, FR-012, FR-013 +3 more — requirement file | Zero violations of `C-01…C-26` verified by constraint tests (`../../13-testing/core/testing-strategy.md` §Constraint Tests) |

Notes on Matrix A:

- The *evidence basis* suffix states where the link came from; an objective referenced by no requirement file and not by the objectives table would show `INSUFFICIENT EVIDENCE` — none of the 12 does.
- `OBJ-01` is expanded from the objectives table's own range `All FR-001…FR-020`.
- `OBJ-04`/`OBJ-05` are the only objectives whose table rows name requirements directly (`NFR-001`, `NFR-003`, `NFR-005`, `NFR-006`); every other link comes from a requirement file's own `OBJ-NN` mention.
- `OBJ-09` and `OBJ-10` are reachable only from `NFR-009`/`NFR-010` — no `FR-*`, use case, workflow or test case names them (see §5 T-05).
- The five session-011 requirements (`SEC-REQ-013`…`SEC-REQ-016`, `DATA-REQ-009`) name no `OBJ-NN` in their own files and are absent from the objectives table, so they appear in **no** row above — unlinked by evidence, not by omission (they are part of `T-01`).

---

## 3. Matrix B — Requirement → Feature Assets

| Requirement | Objective(s) | Block | API group(s) | Representative endpoints | DB entities | UC / WF | Business rules | Priority |
|---|---|---|---|---|---|---|---|---|
| FR-001 | OBJ-01, OBJ-12 | B01 | API-ATH | API-ATH-001, API-ATH-002, API-ATH-003 +9 more | DB-001 user | UC-002, UC-003, UC-004, UC-040 +24 more / WF-001, WF-011 | BR-AUTH-01, BR-AUTH-02, BR-AUTH-03, BR-AUTH-04, BR-AUTH-05 +6 more | Critical |
| FR-002 | OBJ-01, OBJ-12 | B01 | API-ADM | API-ADM-002, API-ADM-025, API-ADM-026 +6 more | DB-001 user | UC-037, UC-091, UC-092, UC-142 +6 more | BR-ORD-09, BR-PLT-06, BR-VND-06, BR-VND-07 | Critical |
| FR-003 | OBJ-01, OBJ-03 | B01 | API-USR | API-ATH-007, API-ATH-010, API-ATH-011 +16 more | DB-001 user, DB-002 address | UC-002, UC-004, UC-005, UC-089 +17 more / WF-001 | BR-AUTH-01, BR-AUTH-06, BR-AUTH-07, BR-AUTH-08 | High |
| FR-004 | OBJ-01, OBJ-03, OBJ-06, OBJ-11, OBJ-12 | B02 | API-CAT | API-ADM-014, API-ADM-015, API-ADM-016 +18 more | DB-004 category, DB-005 product | UC-001, UC-007, UC-017, UC-067 +22 more / WF-002, WF-011 | BR-CAT-01, BR-CAT-02, BR-CAT-03, BR-CAT-04, BR-CAT-05 +5 more | Critical |
| FR-005 | OBJ-02, OBJ-12 | B02 | API-CAT | API-CAT-004, API-CAT-014, API-CAT-015 +1 more | DB-005 product, DB-006 inventory | UC-009, UC-018, UC-046, UC-047 +8 more / WF-003, WF-004, WF-010 | BR-CAT-07, BR-CRT-02, BR-PLT-01, BR-PLT-02, BR-PLT-03 +1 more | Critical |
| FR-006 | OBJ-01, OBJ-02, OBJ-11 | B02 | API-CAT | API-CAT-017, API-CAT-018, API-CAT-019 +3 more | DB-005 product, DB-015 review | UC-007, UC-024, UC-032, UC-038 +12 more | BR-REV-01, BR-REV-02, BR-REV-03, BR-REV-04, BR-REV-05 | High |
| FR-007 | OBJ-01, OBJ-06, OBJ-11 | B03 | API-VND | API-ADM-005, API-ADM-006, API-ADM-007 +10 more | DB-003 store | UC-015, UC-017, UC-019, UC-031 +17 more / WF-011 | BR-ESC-06, BR-PLT-06, BR-VND-01, BR-VND-02, BR-VND-03 +2 more | Critical |
| FR-008 | OBJ-01, OBJ-03, OBJ-11 | B03 | API-VND | API-CNT-002, API-VND-006, API-VND-007 +8 more | DB-003 store | UC-008, UC-016, UC-071, UC-072 +9 more / WF-011 | BR-CAT-06, BR-REV-05, BR-SHP-01, BR-VND-02, BR-VND-04 +3 more | High |
| FR-009 | OBJ-01, OBJ-03, OBJ-04, OBJ-11 | B04 | API-SRC | API-CAT-002, API-CAT-003, API-SRC-001 +2 more | DB-004 category, DB-005 product | UC-001, UC-006, UC-067, UC-069 +10 more / WF-002 | BR-CAT-03, BR-CAT-06, BR-PLT-01, BR-PLT-02 | High |
| FR-010 | OBJ-01, OBJ-04, OBJ-12 | B05 | API-CRT | API-CRT-001, API-CRT-002, API-CRT-003 +4 more | DB-007 cart | UC-009, UC-010, UC-011, UC-074 +7 more / WF-002, WF-003 | BR-CRT-01, BR-CRT-02, BR-CRT-03, BR-CRT-04, BR-CRT-05 +1 more | Critical |
| FR-011 | OBJ-01, OBJ-02, OBJ-12 | B05 | API-ORD | API-CNT-003, API-CNT-004, API-CNT-015 +10 more | DB-007 cart, DB-008 order, DB-009 payment | UC-011, UC-074, UC-161, UC-162 +12 more / WF-003, WF-012 | BR-CRT-04, BR-CRT-05, BR-CRT-06, BR-FIN-01, BR-FIN-02 +9 more | Critical |
| FR-012 | OBJ-01, OBJ-02, OBJ-08, OBJ-12 | B06 | API-ORD | API-ORD-003, API-ORD-004, API-ORD-005 +10 more | DB-008 order | UC-012, UC-013, UC-019, UC-020 +41 more / WF-004, WF-005, WF-007, WF-008 +1 more | BR-ORD-01, BR-ORD-10 | Critical |
| FR-013 | OBJ-02, OBJ-12 | B07 | API-WAL | API-ADM-030, API-ADM-031, API-ADM-032 +11 more | DB-009 payment, DB-010 wallet, DB-011 wallet_transaction | UC-011, UC-034, UC-041, UC-042 +33 more / WF-003, WF-009, WF-010, WF-012 | BR-PAY-01, BR-PAY-02, BR-PAY-03, BR-PAY-04, BR-PAY-05 +5 more | Critical |
| FR-014 | OBJ-02, OBJ-12 | B07 | API-WAL | API-ANL-004, API-ANL-009, API-VND-020 +6 more | DB-011 wallet_transaction, DB-012 escrow | UC-022, UC-039, UC-052, UC-053 +23 more / WF-006, WF-008 | BR-ESC-01, BR-ESC-02, BR-ESC-03, BR-ESC-04, BR-ESC-05 +5 more | Critical |
| FR-015 | OBJ-01, OBJ-07 | B08 | API-SHP | API-ORD-010, API-RET-008, API-SHP-001 +16 more | DB-013 shipment | UC-013, UC-020, UC-025, UC-026 +47 more / WF-005 | BR-ORD-08, BR-ORD-09, BR-SHP-01, BR-SHP-02, BR-SHP-03 +4 more | Critical |
| FR-016 | OBJ-01, OBJ-02, OBJ-12 | B09 | API-RET | API-RET-001, API-RET-002, API-RET-003 +15 more | DB-014 return_request | UC-021, UC-033, UC-057, UC-058 +40 more / WF-007 | BR-PAY-06, BR-PAY-07, BR-PAY-08, BR-RET-01, BR-RET-02 +5 more | Critical |
| FR-017 | OBJ-01, OBJ-03, OBJ-07 | B10 | API-NTF | API-NTF-001, API-NTF-002, API-NTF-003 +11 more | DB-017 notification | UC-008, UC-012, UC-029, UC-038 +29 more / WF-001, WF-004, WF-005, WF-007 +1 more | BR-NTF-01, BR-NTF-02, BR-NTF-03, BR-NTF-04, BR-NTF-05 +2 more | High |
| FR-018 | OBJ-01, OBJ-02, OBJ-08, OBJ-11 | B11 | API-ANL | API-ANL-001, API-ANL-002, API-ANL-003 +3 more | INSUFFICIENT EVIDENCE | UC-022, UC-056, UC-080, UC-081 +18 more / WF-006 | BR-ESC-08, BR-FIN-03, BR-FIN-04, BR-PAY-10, BR-PLT-01 +2 more | Medium |
| FR-019 | OBJ-01, OBJ-03, OBJ-11 | B12 | API-CNT | API-ADM-009, API-ADM-010, API-ADM-012 +29 more | DB-016 coupon | UC-023, UC-104, UC-105, UC-106 +26 more / WF-012 | BR-FIN-01, BR-PLT-03, BR-PLT-05, BR-PRM-01, BR-PRM-02 +5 more | High |
| FR-020 | OBJ-01, OBJ-08, OBJ-12 | B13 | API-ADM | API-ADM-001, API-ADM-002, API-ADM-003 +19 more | DB-018 audit_log | UC-014, UC-031, UC-032, UC-033 +70 more / WF-006, WF-008, WF-009 | BR-ORD-05, BR-ORD-10, BR-PAY-04, BR-PAY-09, BR-PLT-06 +7 more | Critical |
| NFR-001 | OBJ-04OBJ-04 | INSUFFICIENT EVIDENCE | API-ANL | API-SRC-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-002 | OBJ-03, OBJ-04 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-003 | OBJ-04OBJ-04 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-004 | OBJ-04 | INSUFFICIENT EVIDENCE | API-ANL, API-SRC | API-CAT-001, API-SRC-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-005 | OBJ-05OBJ-05 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-006 | OBJ-05OBJ-05 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-007 | OBJ-02, OBJ-05 | INSUFFICIENT EVIDENCE | API-SRC | API-ADM-042, API-ADM-043 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-008 | OBJ-02, OBJ-08 | INSUFFICIENT EVIDENCE | API-CRT, API-ORD | API-WAL-007 | DB-006 inventory, DB-008 order, DB-010 wallet, DB-011 wallet_transaction +1 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-009 | OBJ-09, OBJ-10 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-010 | OBJ-02, OBJ-09 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-011 | OBJ-03 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-012 | OBJ-03, OBJ-06, OBJ-11 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-013 | OBJ-03 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-014 | OBJ-08 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-015 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-016 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-017 | OBJ-11 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | DB-008 order, DB-011 wallet_transaction | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-018 | OBJ-11 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-019 | OBJ-08 | INSUFFICIENT EVIDENCE | API-ADM | API-USR-012, API-WAL-012 | DB-011 wallet_transaction, DB-018 audit_log | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| NFR-020 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| SEC-REQ-001 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ATH, API-USR | API-ATH-001, API-ATH-002, API-ATH-003 +5 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Critical |
| SEC-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ATH-001, API-ATH-010 | DB-001 user, DB-002 address, DB-003 store, DB-013 shipment +2 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Critical |
| SEC-REQ-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ATH | API-ATH-005, API-ATH-006, API-ATH-007 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Critical |
| SEC-REQ-004 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ADM, API-CRT, API-ORD | API-ADM-001, API-ADM-002, API-ADM-023 +4 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Critical |
| SEC-REQ-005 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ATH | API-ADM-003, API-ATH-003, API-ATH-004 +1 more | DB-013 shipment | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | High |
| SEC-REQ-006 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-USR | API-USR-001, API-VND-021 | DB-010 wallet | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Critical |
| SEC-REQ-007 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Critical |
| SEC-REQ-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ADM-043 | DB-009 payment | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Critical |
| SEC-REQ-009 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ATH, API-NTF, API-ORD, API-WAL | API-ATH-001, API-ATH-002, API-NTF-008 +2 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | High |
| SEC-REQ-010 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ADM | API-ADM-024, API-CNT-009, API-CNT-010 +2 more | DB-011 wallet_transaction, DB-018 audit_log | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | High |
| SEC-REQ-011 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-CAT, API-RET, API-SHP, API-USR, API-VND | API-ADM-006, API-ADM-035, API-CAT-012 +8 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | High |
| SEC-REQ-012 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ADM-016, API-CNT-001 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | High |
| SEC-REQ-013 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | High |
| SEC-REQ-014 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Medium |
| SEC-REQ-015 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Medium |
| SEC-REQ-016 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | Medium |
| DATA-REQ-001 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | DB-008 order, DB-016 coupon | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-USR | INSUFFICIENT EVIDENCE | DB-001 user, DB-002 address, DB-017 notification | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-USR | API-USR-012, API-USR-013 | DB-001 user, DB-018 audit_log | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-004 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-005 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-006 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-ANL-002, API-ANL-003, API-ANL-007 +1 more | DB-004 category, DB-005 product, DB-006 inventory, DB-011 wallet_transaction +2 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-007 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-RET, API-WAL | API-ADM-024, API-ANL-004, API-WAL-002 | DB-008 order, DB-009 payment, DB-010 wallet, DB-011 wallet_transaction +2 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-CAT, API-VND | API-ADM-001, API-ADM-036, API-ADM-038 +8 more | DB-003 store, DB-007 cart, DB-008 order, DB-010 wallet +3 more | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| DATA-REQ-009 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-001 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-WAL | API-WAL-003, API-WAL-004 | DB-009 payment | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-002 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-WAL | API-WAL-003, API-WAL-004, API-WAL-005 | DB-009 payment | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-003 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-NTF | API-ATH-002 | DB-017 notification | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-004 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-NTF | API-ATH-002 | DB-017 notification | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-005 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | API-SHP | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-006 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | DB-009 payment, DB-017 notification | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-007 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |
| INT-REQ-008 | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE | INSUFFICIENT EVIDENCE |

Reading rules:

- **`INSUFFICIENT EVIDENCE` is a finding, not a placeholder.** Section 4 counts them; section 5 lists what they imply.
- *Representative endpoints* are truncated (`+N more`) — the full set is derivable from `07-api/*.md`; truncation is presentation only, no link is dropped silently.
- *UC / WF* are shown together because neither source file cross-references the other: no `UC-*` file cites a `WF-*` ID and no workflow file cites a `UC-*` ID (both verified by search), so the two halves are independent frontmatter evidence.
- *UC / WF* cells are truncated after the first four `UC-` IDs (`+N more`), exactly like *Representative endpoints*: presentation only, no link is dropped silently. The full set is derivable from the `related_requirements` frontmatter of the portal-folder files under `../../01-business-analysis/` (glob `*/UC-*.md` and `*/workflow-*.md` across `core`, `admin`, `customer`, `delivery`, `vendor`), catalogued by `../../01-business-analysis/use-case-index.md` and `../../01-business-analysis/workflow-index.md`.
- *Business rules* are only defined for FR files — no `NFR`/`SEC-REQ`/`DATA-REQ`/`INT-REQ` file has a *Business Rules Applied* section, so those cells read `INSUFFICIENT EVIDENCE` by construction, not by omission.
- *Block* is inherently FR-only: blocks `B01…B13` partition the product, while NFR/SEC/DATA/INT requirements are cross-cutting (`INFERENCE`, consistent with `02-requirements/requirements-overview.md` §2–§5 structure).

---

## 4. Summary Statistics

**Matrix A:** 12 objectives · all 12 carry at least one requirement link (20 `FR` + 17 `NFR` files declare an `OBJ-NN`) · `OBJ-09` (quality velocity) and `OBJ-10` (maintainability) are reached only through `NFR-009`/`NFR-010` · `OBJ-11` carries links but its measurable is itself `INSUFFICIENT EVIDENCE` pending `ASM-14`.

**Matrix B:** 73 requirement rows × 9 columns = 657 cells · **327 cells (49.8%) are `INSUFFICIENT EVIDENCE`** · 54 of 73 requirements carry at least one empty cell.

| Column | Rows with evidence | Rows `INSUFFICIENT EVIDENCE` |
|---|---|---|
| Objective(s) | 37 | 36 |
| Block | 20 | 53 |
| API group(s) | 42 | 31 |
| Representative endpoints | 44 | 29 |
| DB entities | 38 | 35 |
| UC / WF | 20 | 53 |
| Business rules | 20 | 53 |
| Priority | 36 | 37 |

Interpretation: the functional spine (20 FRs) is fully linked to use cases, workflows, rules, blocks and priority, and 17 of the 20 NFRs name their objective; the cross-cutting families (`NFR`, `SEC-REQ`, `DATA-REQ`, `INT-REQ`) are linked mainly through API groups, endpoints and entities. What is systematically absent is a UC/WF, block and business-rule trace for every non-FR requirement (53 + 53 + 53 `INSUFFICIENT EVIDENCE` cells), a priority trace for the 37 `NFR`/`DATA-REQ`/`INT-REQ` requirements, and **any objective at all for all 16 `SEC-REQ`, all 9 `DATA-REQ` and all 8 `INT-REQ` requirements** plus `NFR-015`, `NFR-016`, `NFR-020`.

---

## 5. Findings & Documents Needing Update

| # | Finding | Severity | Evidence |
|---|---|---|---|
| T-01 | **36 requirements serve no objective in the matrix**: every `SEC-REQ`, `DATA-REQ`, `INT-REQ` (33) plus `NFR-015`, `NFR-016`, `NFR-020` are referenced by no objective row and by no `OBJ-NN` mention in their own file | MEDIUM | Matrix B *Objective(s)* column |
| T-02 | **37 requirements define no priority**: all `NFR-*`, `DATA-REQ-*`, `INT-REQ-*` files lack a priority field (only FR registry §1 and `SEC-REQ-*` headers carry one) | LOW | Matrix B *Priority* column; `02-requirements/*.md` |
| T-03 | **No UC/WF trace exists for cross-cutting requirements**: all 420 UC and all 12 workflow frontmatters list `FR-*` only | LOW | frontmatter scan of the portal folders of `../../01-business-analysis/` — re-verified 2026-09-30 (session 011): 420/420 `UC-*.md`, every `related_requirements` entry is an `FR-*` ID; count 210 → 420, finding unchanged (LOW `OPEN`) |
| T-04 | **31 requirements touch no registered API group and 29 touch no endpoint** — including `SEC-REQ-007`, `SEC-REQ-012`, `DATA-REQ-004/005`, `INT-REQ-006/007/008`, which are verified elsewhere by plans/drills but not by an endpoint link, and all five session-011 requirements (`SEC-REQ-013`…`016`, `DATA-REQ-009`), which no `07-api/` document references at all | MEDIUM | Matrix B; `07-api/README.md` §4 |
| T-05 | **Two objectives have no functional or verification trace**: `OBJ-09` (quality velocity) and `OBJ-10` (maintainability) are named only by `NFR-009`/`NFR-010` — no `FR-*`, use case, workflow or test case cites them, although `OBJ-09`'s measurable (a release-gating test suite) is a testing concern; `OBJ-11`'s measurable is `INSUFFICIENT EVIDENCE` (`ASM-14`) | LOW | Matrix A; search of `13-testing/` for `OBJ-09`/`OBJ-10` returns nothing |
| T-06 | **No stakeholder → objective/requirement map exists** in `00-project-overview/stakeholders.md` (table has `STK-01…STK-15` with goals, no `OBJ-*`/`FR-*` column), so a stakeholder trace cannot be built without inventing links | LOW | file read |

**Documents needing update (outside this domain, reported not edited):** `02-requirements/`, `02-requirements/`, `02-requirements/` (add priority and objective references if the sponsor wants them traced — T-01, T-02); `00-project-overview/stakeholders.md` (add an `OBJ-*` column — T-06); `07-api/README.md` §4 (review the 31 unlinked requirements — T-04).

Nothing in this file contradicts canon; where the corpus is silent the matrix says so.

---

## 6. Maintenance

Follow `README.md` §6: any change to an objective, requirement, endpoint, entity, use case, workflow or rule is reflected in both matrices **in the same change set**, with a `version` bump and a `## Change History` row here.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring | Root README §10 item 40 |
| 1.1 | 2026-09-28 | FR-013 UC column gains `UC-041`, `UC-042` (new session-007 use cases) | Session-007 UC gap — traceability must cover every UC (`CHK` series); root README §9 change management |
| 1.2 | 2026-09-28 | `T-03` evidence re-synced: 40 → **42 UC** (session-008 count) → **210 UC** (session 010 re-count, 2026-09-29) (`UC-041`/`UC-042` added session 007 — finding status unchanged, LOW `OPEN`) | Count/dashboard propagation catch-up (session 008 close) — direct count of `use-cases/UC-*.md` = 42, then 210 |
| 1.3 | 2026-09-29 | Matrix B *UC / WF* cells rebuilt from all 210 UC frontmatters: 213 new `UC-043`…`UC-210` → `FR-*` links added across the 20 FR rows (cells keep the 4-shown + `+N more` convention; WF half untouched); reading rule added for UC/WF truncation; `T-03` count 42 → **210** (severity/status unchanged) | `prompt-010.md` §1 session-010 UC-coverage directive — 42 → 210 UCs grown under `01-business-analysis/use-cases/`, traceability re-synced same change set (root README §9 rule 4) |
| 1.4 | 2026-09-30 | Universe 68 → **73** requirements (`SEC-REQ-013`…`SEC-REQ-016`, `DATA-REQ-009`); Matrix B gains 5 rows in ID position, cells derived from the new files only (no objective/block/API/endpoint/DB/UC/WF/rule link exists in the corpus; priority `High`/`Medium`/`Medium`/`Medium` on the four SEC rows, `INSUFFICIENT EVIDENCE` on `DATA-REQ-009`); Matrix A reading note added — the 5 new requirements declare no `OBJ-NN` and are unlinked there; *UC / WF* cells rebuilt from all 420 UC frontmatters (+269 `UC-211`…`UC-420` → `FR-*` links, 4-shown + `+N more` convention, WF half untouched); §4 re-run: 657 cells, **327 (49.8%) `INSUFFICIENT EVIDENCE`**, 54 of 73 rows; `T-01` 31 → 36, `T-02` 36 → 37, `T-03` 210 → **420 UC** (severity/status unchanged), `T-04` 26/24 → 31/29; stale `use-cases/` wording → portal folders | `prompt-011.md` §4.8 owner directive session 011 — requirements grew 68 → 73 and the UC corpus 210 → 420, traceability re-synced in the same change set (root README §9 rule 4) |
| 1.5 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
| 1.6 | 2026-10-03 | §Objective(s) source path corrected: `02-requirements/<family>/<ID>.md` → `02-requirements/[<family>/]<portal>/<ID>.md` (FR/DATA-REQ files sit `<family>/core/<ID>.md`; NFR/SEC-REQ/INT-REQ sit `core/<ID>.md` — no requirement file is directly under a family folder) | Session-013 leftover sweep (prompt-013 §2) — stale pre-portal path claim |
