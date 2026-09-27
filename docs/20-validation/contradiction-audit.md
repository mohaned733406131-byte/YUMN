---
document_id: DOC-VAL-004
title: AUD-02 — Contradiction Audit (CT-01…CT-20)
category: 20-validation
status: approved
version: 1.1
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [FR-007, FR-013, FR-016, FR-017, NFR-009]
related_documents: [DOC-ROOT-001, DOC-TPL-011, DOC-GL-003, DOC-OVR-008, DOC-ARCH-010, DOC-DEC-002, DOC-DPL-005, DOC-API-019, DOC-TST-001, DOC-AC-001, DOC-BE-006, DOC-ARCH-007]
---

# AUD-02 — Contradiction Audit (CT-01…CT-20)

| Field | Value |
|---|---|
| **Audit ID** | `AUD-02` |
| **Type** | contradiction |
| **Date** | 2026-09-27 |
| **Scope** | pairs of statements in different documents that cannot both be true: infrastructure ↔ API ↔ test cases, data-flow ↔ background processing, database enums ↔ API enums, glossary/naming rules ↔ the canon they index, registry claims ↔ their contents |
| **Method** | targeted value-set and path comparisons seeded by `AUD-01` failing checks; every pair re-read in full context (including the paragraph around each line) before filing; one entry per distinct conflict, both statements quoted verbatim |
| **Auditor** | analysis-agent |

**Rules (root README §9.5):** contradictions are never ignored and never silently fixed — they stay in this file until the owning document changes through §9 change management, then this entry flips to `RESOLVED` with the propagation recorded in `consistency-audit.md`. Severity: `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`.

---

## 1. Findings (summary)

| # | Contradiction | Severity | Where (file §section) | Evidence (IDs / tags) | Status |
|---|---|---|---|---|---|
| `CT-01` | Constraint pairwise review: no constraint conflicts with another | — (`PASS`) | `00-project-overview/project-constraints.md:89` | mandated entry; 26 `C-NN` reviewed pairwise, 0 conflicts — `VERIFIED` | **`PASS`** |
| `CT-02` | Two health-probe path spellings are both declared canonical | `MEDIUM` | `15-deployment/health-checks.md:23-24` vs `07-api/endpoints/admin.md:115-116` | `API-ADM-042/043`, `BR-PLT-07` — `VERIFIED` | `OPEN` |
| `CT-03` | `health-checks.md` cites `TC-001` as authority for `/healthz`, but `TC-001` asserts `/health/ready` | `LOW` | `15-deployment/health-checks.md:36` vs `13-testing/test-cases/TC-001.md:27` | `TC-001`, `API-ADM-043` — `VERIFIED` | `OPEN` |
| `CT-04` | Queue register disagrees with its consumer document (1 of 17 names match) | `HIGH` | `04-architecture/data-flow.md:54-70` vs `06-backend/background-processing.md:25-49` | `BR-PLT-01`, `C-20` — `VERIFIED` | `OPEN` |
| `CT-05` | Naming document's own queue example names a non-existent queue | `LOW` | `22-glossary/naming-conventions.md:167` vs `06-backend/background-processing.md:48` | `b03.platform.webhook.send` vs `b13.platform.webhook.send` — `VERIFIED` | `OPEN` |
| `CT-06` | Notification `category` vocabulary: 4 DB values vs 7 API values, no shared mapping | `HIGH` | `08-database/entities/notification.md:29` vs `07-api/endpoints/notifications.md:27` | `notification_category`, `BR-NTF-05`, `AC-FR017-01` — `VERIFIED` | `OPEN` |
| `CT-07` | KYC status: API has `IN_REVIEW`, the database enum does not | `MEDIUM` | `08-database/entities/store.md:33` + `constraints-and-integrity.md:91` vs `07-api/endpoints/admin.md:38`, `:40`, `07-api/error-model.md:150` | `kyc_status`, `KYC_IN_REVIEW`, `BR-VND-03` — `VERIFIED` | `OPEN` |
| `CT-08` | Top-up status has three incompatible vocabularies (API / adapter / DB) | `MEDIUM` | `07-api/endpoints/wallet.md:29-30` vs `10-integrations/wallet-providers.md:51` vs `08-database/constraints-and-integrity.md:85` | `API-WAL-003/004`, `INT-REQ-008`, `payment_state` — `VERIFIED` | `OPEN` |
| `CT-09` | Wallet ledger `type`: API offers 5 values, DB enum defines 8 | `MEDIUM` | `07-api/endpoints/wallet.md:28` vs `08-database/constraints-and-integrity.md:100` | `API-WAL-002`, `ledger_type`, `BR-PAY-06` — `VERIFIED` | `OPEN` |
| `CT-10` | Return inspection outcome `PASS/FAIL` vs stored `PASSED/FAILED`, no mapping documented | `LOW` | `07-api/endpoints/returns.md:35` vs `08-database/entities/return_request.md:44` | `API-RET-009`, `inspection_outcome`, `BR-RET-05` — `VERIFIED` | `OPEN` |
| `CT-11` | AC registry claims to be the single authority but omits `AC-S-04/12/21` | `HIGH` | `02-requirements/acceptance-criteria.md:17` vs `00-project-overview/success-criteria.md` | 16 citing files — `VERIFIED` | `OPEN` |
| `CT-12` | AC registry claims every AC, yet 121 `AC-UCnnn-nn` sit outside it and `AC-WF-012-01` is undefined | `MEDIUM` | `acceptance-criteria.md:17` vs `01-business-analysis/use-cases/*`; `naming-conventions.md:112` | `DOC-AC-001` — `VERIFIED` | `OPEN` |
| `CT-13` | Flat AC ID `AC-SR-16` used although the registry has no such row | `LOW` | `15-deployment/production-readiness.md:66` | pre-flagged at `naming-conventions.md:120` — `VERIFIED` | `OPEN` |
| `CT-14` | ADR index states the ADR directory is empty while 10 approved ADRs exist | `MEDIUM` | `04-architecture/architecture-decisions-reference.md:19`, `:25-34` vs `18-decisions/ADR/ADR-001…010.md`, `18-decisions/decision-log.md:23-30` | `ADR-001…ADR-010` — `VERIFIED` | `OPEN` |
| `CT-15` | Two documents each claim to be the canonical GAP register | `MEDIUM` | root README §5:161 + `naming-conventions.md:90` vs `16-data/retention-and-archival.md:39`, `12-non-functional/compliance-and-legal.md:88` | `GAP-01…GAP-12` — `VERIFIED` | `OPEN` |
| `CT-16` | Glossary bans "seller"/"merchant" while canon rows use them | `LOW` | `naming-conventions.md:210` (§11) vs `00-project-overview/project-charter.md:42`, `project-constraints.md:43`, `02-requirements/requirements-overview.md` | `C-11`, `FR-016` — `VERIFIED` | `OPEN` |
| `CT-17` | Naming document declares `A-07` undefined, but the threat model defines asset `A-07` | `LOW` | `naming-conventions.md:121` vs `09-security/threat-model.md:29` | asset series `A-01…A-10` — `VERIFIED` | `OPEN` |
| `CT-18` | Payment release returns `status: "RELEASED"`, a value outside the `payment_state` enum the same payment row must hold | `MEDIUM` | `07-api/endpoints/wallet.md:34` vs `08-database/entities/payment.md:33`, `constraints-and-integrity.md:85` | `payment_state {PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED}`; `RELEASED` exists only as `escrow_state` (`entities/escrow.md:32`); no mapping documented — `VERIFIED` (statement) + `INFERENCE` (which domain is meant) | `OPEN` |
| `CT-19` | Refund receipt status set differs from the stored `refund.state` enum, with no documented mapping | `MEDIUM` | `07-api/endpoints/wallet.md:40` vs `08-database/entities/payment.md:60` | API `PENDING\|COMPOSED\|CREDITED` vs DB `{PENDING, PROCESSING, COMPLETED, FAILED}`; only `PENDING` is shared — `VERIFIED` | `OPEN` |
| `CT-20` | Payout `state` column has no declared enum, and its only documented value (`ELIGIBLE`) is absent from the API status set | `MEDIUM` | `07-api/endpoints/wallet.md:37-38` vs `08-database/indexes-and-performance.md:138-139`; `constraints-and-integrity.md:84-100` | no `payout_state` row in the enum register (unlike `payment_state:85`, `escrow_state:87`); partial index `WHERE state='ELIGIBLE'` vs API `REQUESTED\|SCHEDULED\|EXECUTED\|REJECTED\|ROLLED_OVER` — `VERIFIED` | `OPEN` |

---

## 2. Exact conflicting statements

### `CT-01` — Constraint pairwise review · **`PASS`**

- **Statement:** `00-project-overview/project-constraints.md:89` — "No constraint conflicts with another (`VERIFIED` by pairwise review — recorded in `20-validation/contradiction-audit.md`, entry CT-01: PASS). Apparent legacy conflicts (COD allowed, Kubernetes, microservices) do not exist in this analysis — they are OUT OF SCOPE."
- **Check performed:** all 26 `C-NN` read against `naming-conventions.md:65` allocation and the constraint conflict-check section; no second document asserts a conflicting constraint pair.
- **Outcome:** `PASS` — the mandated entry exists with the mandated outcome. Status `CLOSED`.

### `CT-02` — Health-probe paths · `MEDIUM` · `OPEN`

- **Statement A:** `15-deployment/health-checks.md:23-24` — "`GET /healthz` | Is the process alive? …" / "`GET /readyz` | Should this instance serve requests? …"; and `:36` — "Infrastructure probes use **`/healthz`** and **`/readyz`** — the paths fixed by `BR-PLT-07`, `NFR-005`, `NFR-020` … The API therefore serves **both** path spellings during v1; a single spelling must be chosen by a canon reconciliation before implementation (`20-validation/contradiction-audit.md`)."
- **Statement B:** `07-api/endpoints/admin.md:115-116` — "API-ADM-042 | `GET /health/live` | Public | Liveness …" / "API-ADM-043 | `GET /health/ready` | Public | Readiness …"
- **Why both cannot stand:** the same two probes are specified under different paths in two `source_of_truth` documents, with no mapping row; `health-checks.md:36` already defers the decision to this file.
- **Owning document(s):** `15-deployment/health-checks.md` and `07-api/endpoints/admin.md` (one spelling + one mapping row, then `BR-PLT-07` re-cited).

### `CT-03` — Miscited test case · `LOW` · `OPEN`

- **Statement A:** `15-deployment/health-checks.md:36` — the paths are "fixed by … and `13-testing/test-cases/TC-001.md`."
- **Statement B:** `13-testing/test-cases/TC-001.md:27` — "`GET /health/ready` returns 200 on the API base `/api/v1`."
- **Why both cannot stand:** the cited test case does not exercise `/healthz`; it exercises the API spelling. Either the citation or the test case is wrong.
- **Owning document:** `15-deployment/health-checks.md` (citation) — resolve together with `CT-02`.

### `CT-04` — Queue registers · `HIGH` · `OPEN`

- **Statement A (canonical allocator):** `06-backend/background-processing.md:21-49` — "## 1. Queue Register (by block)" with 25 rows: `b01.auth.session.sweep`, `b02.inventory.expire`, `b02.catalog.index`, `b02.review.rating-recompute`, `b03.vendor.kyc.sla`, `b04.search.banner-refresh`, `b05.checkout.saga-compensate`, `b06.order.sla.check`, `b06.order.timeline-project`, `b07.wallet.topup.reconcile`, `b07.escrow.release`, `b07.payout.batch`, `b07.ledger.daily-reconcile`, `b08.shipping.assign-offer`, `b08.shipping.code-expire`, `b08.shipping.failed-attempt-sla`, `b09.return.inspect-check`, `b09.return.refund-credit`, `b10.notification.fanout`, `b10.notification.template-render`, `b11.analytics.rollup`, `b11.analytics.export`, `b12.content.publish`, `b13.platform.webhook.send`, `b13.platform.audit.retention`.
- **Statement B (consumer):** `04-architecture/data-flow.md:52-70` — 17 rows: `b05.inventory.release`, `b05.checkout.compensate`, `b06.order.escalate`, `b06.order.notify`, `b07.wallet.topup-reconcile`, `b07.escrow.release`, `b07.payout.execute`, `b07.ledger.reconcile`, `b08.delivery.code`, `b08.delivery.attempt-timeout`, `b09.return.inspect-timeout`, `b09.return.decision-escalate`, `b10.notification.send`, `b04.search.index`, `b02.review.recompute`, `b11.analytics.aggregate`, `b13.ticket.auto-close`.
- **Diff:** exactly one identical name (`b07.escrow.release`); block assignment also disagrees (`b05.inventory.release` vs `b02.inventory.expire`, `b04.search.index` vs `b02.catalog.index`). A third instance exists: `07-api/endpoints/search.md:35` — "catalog writes enqueue `b02.product.index` jobs". Intra-file corroboration: the same document's §2 introduces per-channel child queues `b10.notification.delivery.{sms|whatsapp|push}` (`06-backend/background-processing.md:59`) that its own §1 register (`:25-49`, which lists only `b10.notification.fanout` and `b10.notification.template-render`) does not contain — cross-graded `CRIT-04`.
- **Owning document:** `04-architecture/data-flow.md` (restate from the allocator; `naming-conventions.md:95` makes `06-backend/background-processing.md` the *Defined in* authority for queues).

### `CT-05` — Naming example vs register · `LOW` · `OPEN`

- **Statement A:** `22-glossary/naming-conventions.md:167` — "Queue: **`{block}.{entity}.{action}`** — `b02.inventory.expire`, `b07.escrow.release`, `b03.platform.webhook.send`".
- **Statement B:** `06-backend/background-processing.md:48` — "`b13.platform.webhook.send` | B13 | events | signed outbound webhooks (`INT-REQ-006`)".
- **Owning document:** `22-glossary/naming-conventions.md` §7.

### `CT-06` — Notification categories · `HIGH` · `OPEN`

- **Statement A (DB):** `08-database/entities/notification.md:29` — "`category` | `notification_category` | … enum `SECURITY, ORDER, MARKETING, SYSTEM` | preference granularity (BR-NTF-05)".
- **Statement B (API):** `07-api/endpoints/notifications.md:27` — "`category: "SECURITY"|"ORDER"|"DELIVERY"|"RETURN"|"PROMOTION"|"STORE_FOLLOW"|"SYSTEM"`"; reinforced by `:32` (`API-NTF-006` per-category matrix) and `:33` (`API-NTF-007`).
- **Why both cannot stand:** the API returns/stores four categories the enum cannot hold (`DELIVERY`, `RETURN`, `PROMOTION`, `STORE_FOLLOW`) and omits `MARKETING`; `notification_preference.category` (`notification.md:46`) inherits the same 4-value enum, so preference writes for `PROMOTION` cannot be persisted as specified.
- **Owning document:** `08-database/entities/notification.md` (+ `constraints-and-integrity.md` if the enum is restated there) — or `07-api/endpoints/notifications.md`, decided by `BR-NTF-05`.

### `CT-07` — KYC `IN_REVIEW` · `MEDIUM` · `OPEN`

- **Statement A (DB):** `08-database/entities/store.md:33` — "`kyc_status` | `kyc_status` | no | `'PENDING'` | enum `PENDING, APPROVED, REJECTED`"; `08-database/constraints-and-integrity.md:91` repeats the same three values.
- **Statement B (API):** `07-api/endpoints/admin.md:38` — "status: `"PENDING"|"IN_REVIEW"`"; `admin.md:40` — "Approve KYC — `PENDING/IN_REVIEW → APPROVED`"; `07-api/error-model.md:150` — "`KYC_IN_REVIEW` | 409 | yes | New submission while a case is under review".
- **Why both cannot stand:** no column can hold `IN_REVIEW`, so the queue filter `?status=IN_REVIEW` and the error code have nothing to read from; `BR-VND-03` resubmission resets to `PENDING` (`store.md:37`) — a second, unstated path.
- **Owning document:** `07-api/endpoints/admin.md` + `07-api/error-model.md`, or the DB enum (owner: `08-database/`).

### `CT-08` — Top-up status vocabularies · `MEDIUM` · `OPEN`

- **Statement A (API):** `07-api/endpoints/wallet.md:29-30` — "`status: "PENDING_PROVIDER"|"PENDING_VERIFICATION"`" on create, "`status: "PENDING_PROVIDER"|"PENDING_VERIFICATION"|"CREDITED"|"REJECTED"`" on poll (`API-WAL-003/004`).
- **Statement B (adapter contract):** `10-integrations/wallet-providers.md:51` — "Status vocabulary | normalized to `PENDING / SUCCEEDED / FAILED / EXPIRED` inside the adapter | `INT-REQ-008` taxonomy" (while `:35` in the same file describes "status → CREDITED").
- **Statement C (DB):** `08-database/constraints-and-integrity.md:85` — "`payment_state` | `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED`" (top-ups are `payment.kind='TOPUP'`; there is no top-up table — `08-database/entities/payment.md:27`).
- **Why all three cannot stand:** none of `PENDING_PROVIDER`, `PENDING_VERIFICATION`, `CREDITED`, `REJECTED`, `SUCCEEDED`, `EXPIRED` exists in the only state column a top-up can occupy.
- **Owning document:** `07-api/endpoints/wallet.md` (or `08-database/entities/payment.md`), with `10-integrations/wallet-providers.md` §6 as the mapping owner.

### `CT-09` — Ledger `type` cardinality · `MEDIUM` · `OPEN`

- **Statement A (API):** `07-api/endpoints/wallet.md:28` — "`type: "TOPUP"|"ORDER_PAYMENT"|"REFUND"|"ESCROW_HOLD"|"PAYOUT"`" (`API-WAL-002`, filter `?type`).
- **Statement B (DB):** `08-database/constraints-and-integrity.md:100` — "`ledger_type` | `TOPUP, ORDER_HOLD, ORDER_CAPTURE, RELEASE, REFUND, PAYOUT, COMMISSION, ADJUSTMENT`"; `entities/wallet_transaction.md:29` repeats it.
- **Why both cannot stand:** three DB values (`ORDER_HOLD`, `ORDER_CAPTURE`, `COMMISSION`, `ADJUSTMENT` — four, minus `ORDER_PAYMENT`) have no API spelling, and `ORDER_PAYMENT` has no enum member; `?type=ORDER_PAYMENT` cannot be evaluated against the index.
- **Owning document:** `07-api/endpoints/wallet.md`.

### `CT-10` — Inspection outcome spelling · `LOW` · `OPEN`

- **Statement A (API):** `07-api/endpoints/returns.md:35` — "`{ outcome: "PASS"|"FAIL", notes, imageFileIds? }`" (`API-RET-009`).
- **Statement B (DB):** `08-database/entities/return_request.md:44` — "`inspection_outcome` … enum `PASSED, FAILED`"; sample row `:90` shows `inspection_outcome=PASSED`.
- **Note:** a request→storage mapping is plausible but is not documented anywhere; per `root README §8` an undocumented mapping stays a contradiction, not an assumption.
- **Owning document:** `07-api/endpoints/returns.md` (state the mapping) or `08-database/entities/return_request.md`.

### `CT-11` — AC registry authority · `HIGH` · `OPEN`

- **Statement A:** `02-requirements/acceptance-criteria.md:17` — "**This document is the single, authoritative registry of every acceptance criterion (`AC-*`) in the yumn project.** … No other document may invent, redefine or contradict an AC listed here … The registry defines **253 ACs**".
- **Statement B:** `00-project-overview/success-criteria.md` defines `AC-S-01…AC-S-24`, including `AC-S-04`, `AC-S-12`, `AC-S-21` — **none of which appear in the registry** (registry holds 21 of 24).
- **Impact:** 16 files cite the three missing IDs (e.g. `01-business-analysis/workflows/workflow-011.md:59` cites `AC-S-21`; `21-completion/quality-gates.md:134` gate 2.6 requires `AC-S-21/22/23`), so gate evidence cannot be traced through the declared registry.
- **Owning document:** `02-requirements/acceptance-criteria.md` (import the three rows and reconcile the 253 total) — owner decision per root README §4.

### `CT-12` — AC shapes outside the registry · `MEDIUM` · `OPEN`

- **Statement A:** `02-requirements/acceptance-criteria.md:17` — "single, authoritative registry of **every** acceptance criterion".
- **Statement B:** 121 distinct `AC-UCnnn-nn` IDs are defined in `01-business-analysis/use-cases/*.md` (e.g. `UC-001.md:60-62`) and appear in no registry row; `22-glossary/naming-conventions.md:112` documents the shapes "`AC-UCnnn-nn`, `AC-WF-NNN-NN` … observed in `01-business-analysis/`" with example `AC-WF-012-01`, which has **zero** occurrences anywhere and no workflow file contains an acceptance-criteria section.
- **Owning document:** `02-requirements/acceptance-criteria.md` + `22-glossary/naming-conventions.md` §3.1 (either register the UC/WF criteria or restate the claim).

### `CT-13` — Flat AC ID · `LOW` · `OPEN`

- **Statement A:** `15-deployment/production-readiness.md:66` — row S-4 "Secret scan clean on repo and images | … | `AC-SR007-01/03` results | NOT DONE | **`AC-SR-16`**".
- **Statement B:** `22-glossary/naming-conventions.md:120` — "Stray flat AC IDs (`AC-SR-16` …) | `15-deployment/production-readiness.md` | Not present in the `DOC-AC-001` v1.1 registry — cite the registered `AC-SRnnn-nn` … form or log the clash in `20-validation/contradiction-audit.md`".
- **Owning document:** `15-deployment/production-readiness.md` (this entry satisfies the "log the clash" option; the file must still be corrected).

### `CT-14` — ADR index status · `MEDIUM` · `OPEN`

- **Statement A:** `04-architecture/architecture-decisions-reference.md:19` — "**Status note:** none of the ADR files listed below exist yet in `18-decisions/ADR/` — the directory is currently empty." and `:25-34` — ten rows reading "RESERVED — not yet written".
- **Statement B:** `18-decisions/ADR/ADR-001.md` … `ADR-010.md` all exist with `status: approved`; `18-decisions/decision-log.md:23-30` records the same ten as `ACCEPTED` dated 2026-09-26; `decision-log.md:17` states titles "match `04-architecture/architecture-decisions-reference.md` §1 exactly".
- **Self-acknowledged:** `decision-log.md:77` — "update `04-architecture/architecture-decisions-reference.md` §1 status from RESERVED to ACCEPTED (it currently shows RESERVED — the index must be re-synced and version-bumped when this authoring lands), then run `20-validation/consistency-audit.md`."
- **Owning document:** `04-architecture/architecture-decisions-reference.md`.

### `CT-15` — Canonical GAP register · `MEDIUM` · `OPEN`

- **Statement A:** root `README.md:161` — "| Gaps | `GAP-NNN` | `GAP-03` | **`20-validation/missing-information.md`** |"; `22-glossary/naming-conventions.md:90` — "Defined in | `20-validation/missing-information.md`".
- **Statement B:** `16-data/retention-and-archival.md:39` — "No new `GAP-NNN` ID is minted here — gap IDs are assigned only in the canonical GAP register (**`00-project-overview/project-scope.md` §Open items**)"; `12-non-functional/compliance-and-legal.md:88` — "recorded in `20-validation/missing-information.md` when that register is authored (**no new gap IDs minted outside the canonical GAP register, per `DOC-DTA-005` convention**)"; `21-completion/quality-gates.md:80` cites `00-project-overview/project-scope.md` as the Gate-0 GAP source.
- **Consequence:** `GAP-08…GAP-12` had to be minted somewhere; this audit records that `20-validation/missing-information.md` did so under root README precedence while `project-scope.md` still carries only six rows.
- **Owning documents:** `16-data/retention-and-archival.md`, `12-non-functional/compliance-and-legal.md` (and `21-completion/quality-gates.md:80` once decided).

### `CT-16` — Disallowed synonyms · `LOW` · `OPEN`

- **Statement A:** `22-glossary/naming-conventions.md:210` — "**Seller** is a **disallowed synonym** … "\"Seller\"/\"merchant\" anywhere in documents (only inside quotations of external text); never name a table `seller` or a route `/sellers/...`\"".
- **Statement B (canon uses them):** `00-project-overview/project-charter.md:42`, `00-project-overview/project-constraints.md:43` (`C-11`), `02-requirements/requirements-overview.md` (`FR-016` commission wording) — plus 17 files containing `seller` and 30 containing `merchant`.
- **Owning document:** `22-glossary/naming-conventions.md` §11 (narrow the ban to identifiers) or the canon rows (renaming), decided by the glossary owner; neither may be changed unilaterally (root README §9.4).

### `CT-17` — `A-07` claim · `LOW` · `OPEN`

- **Statement A:** `22-glossary/naming-conventions.md:121` — "Security finding cited as `A-07` | `09-security/security-findings.md` (SEC-008) | The register uses `ASM-*`/`SEC-*`; **`A-07` is undefined** — cite `ASM-07` intent or log in `contradiction-audit.md`".
- **Statement B:** `09-security/threat-model.md:29` — "| `A-07` | KYC documents & bank-transfer receipts | HIGH | Identity fraud | MinIO (`DEP-07`), PostgreSQL references |" — an asset row inside the `A-01…A-10` asset table (`threat-model.md:21-32`), also cited at `09-security/data-protection.md:37`, `secrets-management.md:39`, `18-decisions/ADR/ADR-007.md:94`.
- **Why both cannot stand:** the ID is defined; what is actually missing is an `A-NN` row in `naming-conventions.md` §3 (*Defined in* column), not the asset.
- **Owning document:** `22-glossary/naming-conventions.md` §3 + §3.2.

---

### `CT-18` — Payment release status · `MEDIUM` · `OPEN`

- **Statement A:** `07-api/endpoints/wallet.md:34` (API-WAL-008 `POST /wallet/payments/{id}/release`) — "`{ reason }` → `200 { paymentId, status: "RELEASED" }`".
- **Statement B:** `08-database/entities/payment.md:33` — "`state` | `payment_state` | … enum `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED`" and `constraints-and-integrity.md:85` — "`payment_state` | `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED` | `payment.state`".
- **Why both cannot stand:** the response is keyed by `paymentId` and names a `status` the payment column cannot hold; `RELEASED` is a legal value only of `escrow_state` (`entities/escrow.md:32` — `HELD, RELEASED, REFUNDED, FROZEN`), and no document states that API-WAL-008 reports an escrow/hold status under a payment-scoped field. A client reading `{ paymentId, status }` cannot map it to `payment.state`.
- **Owning document:** `07-api/endpoints/wallet.md` (declare the response status domain) — cross-graded `CRIT-03`.

---

### `CT-19` — Refund status vocabulary · `MEDIUM` · `OPEN`

- **Statement A:** `07-api/endpoints/wallet.md:40` (API-WAL-014 `GET /orders/{id}/refund`) — "`status: "PENDING"|"COMPOSED"|"CREDITED"` … wallet credit within 3 business days of `REFUNDED`".
- **Statement B:** `08-database/entities/payment.md:60` — "`refund` (supporting) … `state ∈ {PENDING, PROCESSING, COMPLETED, FAILED}`".
- **Why both cannot stand:** only `PENDING` is in both sets; `COMPOSED` and `CREDITED` have no stored representation, while `PROCESSING`, `COMPLETED` and `FAILED` are never exposed on a customer-facing receipt, and no mapping table exists in `07-api/endpoints/` or `08-database/`.
- **Owning document:** `07-api/endpoints/wallet.md` + `08-database/entities/payment.md` (pick one vocabulary and map) — cross-graded `CRIT-03`.

---

### `CT-20` — Payout state domain · `MEDIUM` · `OPEN`

- **Statement A:** `07-api/endpoints/wallet.md:37-38` — API-WAL-011 returns `status: "REQUESTED"`; API-WAL-012 filters/returns `status: "REQUESTED"|"SCHEDULED"|"EXECUTED"|"REJECTED"|"ROLLED_OVER"`.
- **Statement B:** `08-database/indexes-and-performance.md:138-139` — "`payout` | `idx_payout_store_state` on `(store_id, state, created_at DESC)`" and "`payout` | `idx_payout_state` on `(state, eligible_at)` WHERE `state='ELIGIBLE'`", while `constraints-and-integrity.md:84-100` declares `payment_state` and `escrow_state` but **no `payout_state`** (0 documents define one).
- **Why both cannot stand:** the schema's only documented payout `state` value — `ELIGIBLE`, indexed and driven by `eligible_at` for the ≥1,000 YER / 3–7 business-day batch job — is unreachable through the API's five-value status set, and the five API values have no declared storage domain. Vendors cannot filter for eligible payouts; `ROLLED_OVER` (wallet.md:38) has no counterpart anywhere in `08-database/`.
- **Owning document:** `08-database/constraints-and-integrity.md` (declare `payout_state`) + `07-api/endpoints/wallet.md` (align status set).

---

## 3. Coverage & Statistics

- Files examined: **~40** directly cited files (each quoted line re-read in context), out of 433 in scope at sweep time; seeded by `AUD-01` failing checks `CHK-16`, `CHK-19`, `CHK-20`, `CHK-21`, `CHK-22`, `CHK-23`, `CHK-24`, `CHK-25`, `CHK-12`, `CHK-13`, `CHK-14`, `CHK-31`.
- Checks run: **20** — passed 1 (`CT-01`), failed 19 (all recorded `OPEN`).
- ID references verified: 20 statement pairs, every one with `file:line`; **0** fabricated or assumed citations.
- Contradictions by severity: `CRITICAL` 0 · `HIGH` 3 (`CT-04`, `CT-06`, `CT-11`) · `MEDIUM` 10 · `LOW` 6 · `PASS` 1.
- Series in scope: `CT-NN` issued 20 · open 19 · resolved 0 · passed 1.
- Cross-graded against the sibling audits: `CT-18` = `CRIT-03(a)`, `CT-19` = `CRIT-03(c)`, `CT-08` = `CRIT-03(b)`, `CT-04` = `CRIT-04`, `CT-11`/`CT-12` adjacent to `CRIT-05` (`critical-findings.md:51-53`). Severities here grade the *document conflict*; `critical-findings.md` grades gate impact. `CT-20` (payout state domain) is not covered by any `CRIT-*` row.

---

## 4. Verdict & Sign-off

- **Gate:** `PASS WITH FINDINGS` (root README §11) — the audit ran to completion with every conflict evidenced; 19 remain `OPEN` because fixing them is the owning documents' job (root README §9.5 forbids local fixes here).
- **Unresolved contradictions / gaps:** `CT-02`…`CT-20` (`OPEN`); `CT-01` `PASS`/`CLOSED`. Cross-links: `GAP-01…GAP-12` (`missing-information.md`), findings 6–17, 22, 24 (`consistency-audit.md`).
- **Required follow-up — owning documents that must change, in propagation order (root README §9.4), edits NOT made by this audit:** `04-architecture/data-flow.md` (`CT-04`) · `07-api/endpoints/notifications.md` + `08-database/entities/notification.md` (`CT-06`) · `02-requirements/acceptance-criteria.md` (`CT-11`, `CT-12`) · `15-deployment/health-checks.md` + `07-api/endpoints/admin.md` (`CT-02`, `CT-03`) · `07-api/endpoints/wallet.md` (`CT-08`, `CT-09`, `CT-18`, `CT-19`, `CT-20`) + `08-database/entities/payment.md` (`CT-18`, `CT-19`) + `08-database/constraints-and-integrity.md` (`CT-20`) · `04-architecture/architecture-decisions-reference.md` (`CT-14`) · `16-data/retention-and-archival.md` + `12-non-functional/compliance-and-legal.md` (`CT-15`) · `07-api/endpoints/admin.md` + `07-api/error-model.md` (`CT-07`) · `22-glossary/naming-conventions.md` (`CT-05`, `CT-16`, `CT-17`) · `15-deployment/production-readiness.md` (`CT-13`) · `07-api/endpoints/returns.md` (`CT-10`). After each change: bump `version`, add the §9.2 row, re-run the linked `AUD-01` checks, log the propagation.
- **Sign-off:** analysis-agent, 2026-09-27.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial baseline: `CT-01` recorded `PASS`; `CT-02…CT-17` opened with exact conflicting statements | Root README §9.5 / §10 item 42; `project-constraints.md:89` (`CT-01` mandate); `DOC-TPL-011` |
| 1.1 | 2026-09-27 | `CT-18` (`payment` `RELEASED`), `CT-19` (refund status set), `CT-20` (payout state domain) opened after the money-path re-read; `CT-04` gains the intra-file `b10.notification.delivery.*` evidence; statistics re-issued (20 checks: 1 pass / 19 open) and cross-grades to `CRIT-03(a)(c)` / `CRIT-04` / `CRIT-05` recorded | `AUD-01` check `CHK-31`; cross-ref `critical-findings.md` `CRIT-03`; root README §9.5 |
