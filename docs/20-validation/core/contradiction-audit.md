---
document_id: DOC-VAL-004
title: AUD-02 — Contradiction Audit (CT-01…CT-30)
category: 20-validation
status: approved
version: 1.9
created: 2026-09-27
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [FR-007, FR-013, FR-016, FR-017, NFR-009]
related_documents: [DOC-ROOT-001, DOC-TPL-011, DOC-GL-003, DOC-OVR-008, DOC-ARCH-010, DOC-DEC-002, DOC-DPL-005, DOC-API-019, DOC-TST-001, DOC-AC-001, DOC-BE-006, DOC-ARCH-007]
---

# AUD-02 — Contradiction Audit (CT-01…CT-30)

| Field | Value |
|---|---|
| **Audit ID** | `AUD-02` |
| **Type** | contradiction |
| **Date** | 2026-09-27 |
| **Scope** | pairs of statements in different documents that cannot both be true: infrastructure ↔ API ↔ test cases, data-flow ↔ background processing, database enums ↔ API enums, glossary/naming rules ↔ the canon they index, registry claims ↔ their contents; extended 2026-09-28 to sponsor-provided input (`describ.md`) ↔ canon constraints/rules, and one canon-internal pair the input surfaced |
| **Method** | targeted value-set and path comparisons seeded by `AUD-01` failing checks; every pair re-read in full context (including the paragraph around each line) before filing; one entry per distinct conflict, both statements quoted verbatim |
| **Auditor** | analysis-agent |

**Rules (root README §9.5):** contradictions are never ignored and never silently fixed — they stay in this file until the owning document changes through §9 change management, then this entry flips to `RESOLVED` with the propagation recorded in `consistency-audit.md`. Severity: `CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`.

---

## 1. Findings (summary)

| # | Contradiction | Severity | Where (file §section) | Evidence (IDs / tags) | Status |
|---|---|---|---|---|---|
| `CT-01` | Constraint pairwise review: no constraint conflicts with another | — (`PASS`) | `00-project-overview/project-constraints.md:89` | mandated entry; 26 `C-NN` reviewed pairwise, 0 conflicts — `VERIFIED` | **`PASS`** |
| `CT-02` | Two health-probe path spellings are both declared canonical | `MEDIUM` | `../../15-deployment/core/health-checks.md:23-24` vs `../../07-api/admin/admin.md:115-116` | `API-ADM-042/043`, `BR-PLT-07` — `VERIFIED` | **`RESOLVED` 2026-09-27** (`REC-05`) |
| `CT-03` | `health-checks.md` cites `TC-001` as authority for `/healthz`, but `TC-001` asserts `/health/ready` | `LOW` | `../../15-deployment/core/health-checks.md:36` vs `../../13-testing/core/TC-001.md:27` | `TC-001`, `API-ADM-043` — `VERIFIED` | **`RESOLVED` 2026-09-27** (`REC-05`) |
| `CT-04` | Queue register disagrees with its consumer document (1 of 17 names match) | `HIGH` | `../../04-architecture/core/data-flow.md:54-70` vs `../../06-backend/core/background-processing.md:25-49` | `BR-PLT-01`, `C-20` — `VERIFIED` | **`RESOLVED` 2026-09-27** (`REC-06` — both queue owners now use the single register: `data-flow.md` v1.1, `background-processing.md` v1.1, register 25 → 30 rows) |
| `CT-05` | Naming document's own queue example names a non-existent queue | `LOW` | `22-glossary/core/naming-conventions.md:167` vs `../../06-backend/core/background-processing.md:48` | `b03.platform.webhook.send` vs `b13.platform.webhook.send` — `VERIFIED` | **`RESOLVED` 2026-09-27** (`REC-06` — `naming-conventions.md` v1.2 §7 example now `b13.platform.webhook.send`) |
| `CT-06` | Notification `category` vocabulary: 4 DB values vs 7 API values, no shared mapping | `HIGH` | `../../08-database/core/notification.md:29` vs `../../07-api/core/notifications.md:27` | `notification_category`, `BR-NTF-05`, `AC-FR017-01` — `VERIFIED` | `OPEN` |
| `CT-07` | KYC status: API has `IN_REVIEW`, the database enum does not | `MEDIUM` | `../../08-database/core/store.md:33` + `constraints-and-integrity.md:91` vs `../../07-api/admin/admin.md:38`, `:40`, `../../07-api/core/error-model.md:150` | `kyc_status`, `KYC_IN_REVIEW`, `BR-VND-03` — `VERIFIED` | `OPEN` |
| `CT-08` | Top-up status has three incompatible vocabularies (API / adapter / DB) | `MEDIUM` | `../../07-api/core/wallet.md:29-30` vs `../../10-integrations/core/wallet-providers.md:51` vs `../../08-database/core/constraints-and-integrity.md:85` | `API-WAL-003/004`, `INT-REQ-008`, `payment_state` — `VERIFIED` | `OPEN` |
| `CT-09` | Wallet ledger `type`: API offers 5 values, DB enum defines 8 | `MEDIUM` | `../../07-api/core/wallet.md:28` vs `../../08-database/core/constraints-and-integrity.md:100` | `API-WAL-002`, `ledger_type`, `BR-PAY-06` — `VERIFIED` | `OPEN` |
| `CT-10` | Return inspection outcome `PASS/FAIL` vs stored `PASSED/FAILED`, no mapping documented | `LOW` | `../../07-api/core/returns.md:35` vs `../../08-database/core/return_request.md:44` | `API-RET-009`, `inspection_outcome`, `BR-RET-05` — `VERIFIED` | `OPEN` |
| `CT-11` | AC registry claims to be the single authority but omits `AC-S-04/12/21` | `HIGH` | `02-requirements/acceptance-criteria.md:17` vs `00-project-overview/success-criteria.md` | 16 citing files *(→ 20 on the 2026-09-30 re-count; registry total 253 → **273** since session 011)* — `VERIFIED` | `OPEN` |
| `CT-12` | AC registry claims every AC, yet 121 `AC-UCnnn-nn` sit outside it *(→ **1591** across 420 UC files since session 011, 2026-09-30)* and `AC-WF-012-01` is undefined | `MEDIUM` | `acceptance-criteria.md:17` vs `01-business-analysis/*`; `naming-conventions.md:112` | `DOC-AC-001` — `VERIFIED` | `OPEN` |
| `CT-13` | Flat AC ID `AC-SR-16` used although the registry has no such row | `LOW` | `../../15-deployment/core/production-readiness.md:66` | pre-flagged at `naming-conventions.md:120` — `VERIFIED` | `OPEN` |
| `CT-14` | ADR index states the ADR directory is empty while 10 approved ADRs exist | `MEDIUM` | `04-architecture/core/architecture-decisions-reference.md:19`, `:25-34` vs `18-decisions/ADR/ADR-001…010.md`, `18-decisions/core/decision-log.md:23-30` | `ADR-001…ADR-010` — `VERIFIED` | **`RESOLVED` 2026-09-28** (`REC-02` — index v1.1: empty-directory note removed, ten statuses re-synced to `ACCEPTED`) |
| `CT-15` | Two documents each claim to be the canonical GAP register | `MEDIUM` | root README §5:161 + `naming-conventions.md:90` vs `../../16-data/core/retention-and-archival.md:39`, `../../12-non-functional/core/compliance-and-legal.md:88` | `GAP-01…GAP-16` — `VERIFIED` | `OPEN` |
| `CT-16` | Glossary bans "seller"/"merchant" while canon rows use them | `LOW` | `naming-conventions.md:210` (§11) vs `00-project-overview/project-charter.md:42`, `project-constraints.md:43`, `02-requirements/requirements-overview.md` | `C-11`, `FR-016` — `VERIFIED` | `OPEN` |
| `CT-17` | Naming document declares `A-07` undefined, but the threat model defines asset `A-07` | `LOW` | `naming-conventions.md:121` vs `../../09-security/core/threat-model.md:29` | asset series `A-01…A-10` — `VERIFIED` | `OPEN` |
| `CT-18` | Payment release returns `status: "RELEASED"`, a value outside the `payment_state` enum the same payment row must hold | `MEDIUM` | `../../07-api/core/wallet.md:34` vs `../../08-database/core/payment.md:33`, `constraints-and-integrity.md:85` | `payment_state {PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED}`; `RELEASED` exists only as `escrow_state` (`../../08-database/core/escrow.md:32`); no mapping documented — `VERIFIED` (statement) + `INFERENCE` (which domain is meant) | `OPEN` |
| `CT-19` | Refund receipt status set differs from the stored `refund.state` enum, with no documented mapping | `MEDIUM` | `../../07-api/core/wallet.md:40` vs `../../08-database/core/payment.md:60` | API `PENDING\|COMPOSED\|CREDITED` vs DB `{PENDING, PROCESSING, COMPLETED, FAILED}`; only `PENDING` is shared — `VERIFIED` | `OPEN` |
| `CT-20` | Payout `state` column has no declared enum, and its only documented value (`ELIGIBLE`) is absent from the API status set | `MEDIUM` | `../../07-api/core/wallet.md:37-38` vs `../../08-database/core/indexes-and-performance.md:138-139`; `constraints-and-integrity.md:84-100` | no `payout_state` row in the enum register (unlike `payment_state:85`, `escrow_state:87`); partial index `WHERE state='ELIGIBLE'` vs API `REQUESTED\|SCHEDULED\|EXECUTED\|REJECTED\|ROLLED_OVER` — `VERIFIED` | `OPEN` |
| `CT-21` | `J10` audit-chain verification cadence declared three different ways (hourly vs nightly vs daily) | `MEDIUM` | `../../16-data/core/data-quality.md:84` (job register: **Hourly**) vs `../../17-risk-management/core/mitigation-plans.md:46` + `../../21-completion/core/implementation-roadmap.md:188` (**Nightly**) vs `17-risk-management/core/risk-register.md:79` (**daily**) | `J10`, `SEC-REQ-010` R4, `SEC-002` residual-risk acceptance; `implementation-roadmap.md:174` defers cadence to `data-quality.md` while `:188` asserts nightly — `VERIFIED` (four lines re-read) | `OPEN` (deferred item (b), logged at sweep 2026-09-28) |
| `CT-22` | API audit-log projection and privacy claim promise `ipHash`, but the schema stores a raw `ip` address | `MEDIUM` | `../../07-api/admin/admin.md:77` (`API-ADM-024` response field `ipHash`) + `admin.md:125` ("audit entries store `ipHash`, not raw IPs", `SEC-REQ-008`) vs `../../08-database/core/audit_log.md:40` (`ip` column, `inet`, "client address (`BR-PLT-06`)") | corroborating projections at `../../13-testing/core/TC-036.md:53`, `TC-053.md:46`, `TC-109.md:57`; no documented hash-on-read step, no `ip_hash` column — `VERIFIED` | `OPEN` (deferred item (d), logged at sweep 2026-09-28) |
| `CT-23` | Sponsor spec: multi-currency sub-accounts + platform FX vs `C-04` "Fiat YER only — no USD/SAR wallets in v1" | `HIGH` | `describ.md:19` ("sub-accounts denominated in various currencies"), `:38-40` (SAR order vs YER balance, "standard exchange rate"), `:63-64` ("platform … controls the exchange rate") vs `docs/00-project-overview/project-constraints.md:26` (`C-04`) | `C-04`, `FR-013:29` ("YER-only per-user wallet"), `wallet.md` `currency=YER` column — `VERIFIED` | `OPEN` (`GAP-13` resolved 2026-09-28 as mixed, but `D1`/`M-01` stays OPEN pending finance review — `C-04` not amended) |
| `CT-24` | Sponsor spec: top-up via Al-Kuraimi/Jeeb with provider PIN vs `C-05` fixed three methods (m-Floos, OneCash, bank transfer) | `HIGH` | `describ.md:28-30` ("payment ID and the PIN generated within their external wallet (such as **Al-Kuraimi** or **Jeeb**)") vs `project-constraints.md:27` (`C-05` "No other instruments") | `C-05`, `BR-PAY-04:94` (spec §2.2 admin-verified transfer **agrees**), `INT-REQ-008` — `VERIFIED` | **`RESOLVED` 2026-09-28** (`GAP-13` disposition `D1`/`M-02` — `C-05` amended v1.1: Al-Kuraimi Bank + Jeeb added to the instrument set; both statements now stand) |
| `CT-25` | Sponsor spec: email+password as a second login option vs `C-06` "No email-primary auth" + canon phone+password / phone+OTP paths | `HIGH` | `describ.md:68` ("phone number **and/or** email; … email is optional"), `:74` ("Email and password") vs `project-constraints.md:33` (`C-06`); `FR-001` register paths | `C-06`, `SEC-REQ-001` — `VERIFIED` (phone-mandatory half of the spec **agrees**) | **`RESOLVED` 2026-09-28** (`GAP-13` disposition `D1`/`M-03` — `C-06` amended v1.1: optional *verified* profile email allowed as contact data; the email-as-login leg stays rejected, spec re-scoped) |
| `CT-26` | Sponsor spec: escrow held for the merchant-defined return period vs `C-12` fixed 7-day hold | `HIGH` | `describ.md:57-59` ("held in an escrow account for the duration of the merchant-defined return period … Funds … not returned are released directly") vs `project-constraints.md:44` (`C-12` "funds held 7 days from DELIVERED") | `C-12`, `BR-RET-01` (merchant returnable designation **agrees**), `escrow.md` `escrow_state` — `VERIFIED` | `OPEN` (`GAP-13` resolved 2026-09-28 as mixed, but `D1`/`M-04` stays OPEN pending finance review — `C-12` not amended) |
| `CT-27` | Sponsor spec: person-to-person account funding vs canon "Money never flows directly between actors" | `HIGH` | `describ.md:33` ("Another person transfers funds from their own account to this user's account"), `:41-42` ("deposit funds into another person's account") vs `../../03-system-analysis/core/system-context.md:96` ("**Money never flows directly between actors.** Customer funds enter only via top-up (`C-05`)…") | `system-context.md:96`, `C-05`, `FR-013` (top-up enumeration has no P2P leg) — `VERIFIED` | `OPEN` (`GAP-13` resolved 2026-09-28 as mixed, but `D1`/`M-06` stays OPEN — P2P is a system-boundary change routed to security review, not amended) |
| `CT-28` | Sponsor spec: customer withdrawal to an external wallet vs `BR-PAY-07` "never external cash-out" | `MEDIUM` | `describ.md:41-42` ("request a withdrawal to an external wallet, subject to the options available in the system") vs `01-business-analysis/business-rules.md:97` (`BR-PAY-07`) | `BR-PAY-07`, `BR-ESC-05` (vendor-payout exception does not cover customers), `GAP-06` (vendor cash-out is itself an open question) — `VERIFIED` | `OPEN` (`GAP-13` resolved 2026-09-28 as mixed, but `D1`/`M-05` stays OPEN pending owner review — `BR-PAY-07` not amended) |
| `CT-29` | Sponsor spec: admin "operations on accounts — individually or collectively" incl. "any actions deemed appropriate" vs `rbac.md` rows 15–16 (no role may adjust ledgers; no role but the customer reads a wallet) | `HIGH` | `describ.md:52-53` vs `../../09-security/core/rbac.md:51` (row 15 `Direct ledger / balance adjustment` — ADMIN `✖`, SUPER_ADMIN `✖`, SYSTEM `✖ (compensating entries only)`) and `:52` (row 16 `Read a customer's wallet balance` — ADMIN `✖`, SUPER_ADMIN `✖`) | `rbac.md` §2 rows 15–16, `SEC-REQ-004`, `FR-002` — `VERIFIED` | **`RESOLVED`-NO 2026-09-28** (`GAP-13` disposition `D1`/`M-07` = **NO** — canon stands: rbac rows 15–16 unchanged and absolute; spec leg rejected) |
| `CT-30` | Canon-internal: wallet row creation timing — `FR-013` "created at registration" vs `wallet.md` "created lazily on first top-up/order attempt" (sponsor spec §1 asserts account-on-verification) | `MEDIUM` | `../../02-requirements/functional/core/FR-013.md:45` vs `../../08-database/core/wallet.md:34`; `describ.md:18-19` | `FR-013`, `wallet.md` `created_at` note, `UC-041` flow (top-up assumes a wallet row) — `VERIFIED` | `OPEN` (canon-internal — owning docs `FR-013.md` / `../../08-database/core/wallet.md` decide) |

---

## 2. Exact conflicting statements

### `CT-01` — Constraint pairwise review · **`PASS`**

- **Statement:** `00-project-overview/project-constraints.md:89` — "No constraint conflicts with another (`VERIFIED` by pairwise review — recorded in `contradiction-audit.md`, entry CT-01: PASS). Apparent legacy conflicts (COD allowed, Kubernetes, microservices) do not exist in this analysis — they are OUT OF SCOPE."
- **Check performed:** all 26 `C-NN` read against `naming-conventions.md:65` allocation and the constraint conflict-check section; no second document asserts a conflicting constraint pair.
- **Outcome:** `PASS` — the mandated entry exists with the mandated outcome. Status `CLOSED`.

### `CT-02` — Health-probe paths · `MEDIUM` · **`RESOLVED` 2026-09-27**

- **Statement A:** `../../15-deployment/core/health-checks.md:23-24` — "`GET /healthz` | Is the process alive? …" / "`GET /readyz` | Should this instance serve requests? …"; and `:36` — "Infrastructure probes use **`/healthz`** and **`/readyz`** … The API therefore serves **both** path spellings during v1; a single spelling must be chosen by a canon reconciliation before implementation (`contradiction-audit.md`)."
- **Statement B:** `../../07-api/admin/admin.md:115-116` — "API-ADM-042 | `GET /health/live` | Public | Liveness …" / "API-ADM-043 | `GET /health/ready` | Public | Readiness …"
- **Why both could not stand:** the same two probes were specified under different paths in two `source_of_truth` documents, with no mapping row; `health-checks.md:36` deferred the decision to this file.
- **Owning document(s):** `../../15-deployment/core/health-checks.md` and `../../07-api/admin/admin.md`.
- **Resolution (`REC-05`, `TD-06`, 2026-09-27):** canon fixed at `/healthz` + `/readyz` per `BR-PLT-07`. `../../07-api/admin/admin.md` **v1.1** — `API-ADM-042/043` rows repathed; `../../15-deployment/core/health-checks.md` **v1.1** — §1.1 rewritten from "open reconciliation" to the declared canon; `TC-001`, `TC-031`, `TC-057`, `TC-065` **v1.1** — preconditions repathed. Repo-wide re-search for `/health/live` + `/health/ready` returns zero platform hits (only MinIO's vendor probe `/minio/health/live` remains, explicitly excluded from the `REC-05` acceptance criterion). Propagation logged in `consistency-audit.md` §4.

### `CT-03` — Miscited test case · `LOW` · **`RESOLVED` 2026-09-27**

- **Statement A:** `../../15-deployment/core/health-checks.md:36` — the paths are "fixed by … and `../../13-testing/core/TC-001.md`."
- **Statement B:** `../../13-testing/core/TC-001.md:27` — "`GET /health/ready` returns 200 on the API base `/api/v1`."
- **Why both could not stand:** the cited test case did not exercise `/healthz`; it exercised the retired API spelling.
- **Owning document:** `../../15-deployment/core/health-checks.md` (citation) — resolved together with `CT-02`.
- **Resolution (`REC-05`, 2026-09-27):** `TC-001` **v1.1** now asserts the canon readiness gate `GET /readyz`, and `health-checks.md` v1.1 §1.1 cites it precisely as the readiness assertion while attributing both paths to `BR-PLT-07`/`NFR-005`/`NFR-020` — citation and test case now agree.

### `CT-04` — Queue registers · `HIGH` · `OPEN`

- **Statement A (canonical allocator):** `../../06-backend/core/background-processing.md:21-49` — "## 1. Queue Register (by block)" with 25 rows: `b01.auth.session.sweep`, `b02.inventory.expire`, `b02.catalog.index`, `b02.review.rating-recompute`, `b03.vendor.kyc.sla`, `b04.search.banner-refresh`, `b05.checkout.saga-compensate`, `b06.order.sla.check`, `b06.order.timeline-project`, `b07.wallet.topup.reconcile`, `b07.escrow.release`, `b07.payout.batch`, `b07.ledger.daily-reconcile`, `b08.shipping.assign-offer`, `b08.shipping.code-expire`, `b08.shipping.failed-attempt-sla`, `b09.return.inspect-check`, `b09.return.refund-credit`, `b10.notification.fanout`, `b10.notification.template-render`, `b11.analytics.rollup`, `b11.analytics.export`, `b12.content.publish`, `b13.platform.webhook.send`, `b13.platform.audit.retention`.
- **Statement B (consumer):** `../../04-architecture/core/data-flow.md:52-70` — 17 rows: `b05.inventory.release`, `b05.checkout.compensate`, `b06.order.escalate`, `b06.order.notify`, `b07.wallet.topup-reconcile`, `b07.escrow.release`, `b07.payout.execute`, `b07.ledger.reconcile`, `b08.delivery.code`, `b08.delivery.attempt-timeout`, `b09.return.inspect-timeout`, `b09.return.decision-escalate`, `b10.notification.send`, `b04.search.index`, `b02.review.recompute`, `b11.analytics.aggregate`, `b13.ticket.auto-close`.
- **Diff:** exactly one identical name (`b07.escrow.release`); block assignment also disagrees (`b05.inventory.release` vs `b02.inventory.expire`, `b04.search.index` vs `b02.catalog.index`). A third instance exists: `../../07-api/core/search.md:35` — "catalog writes enqueue `b02.product.index` jobs". Intra-file corroboration: the same document's §2 introduces per-channel child queues `b10.notification.delivery.{sms|whatsapp|push}` (`../../06-backend/core/background-processing.md:59`) that its own §1 register (`:25-49`, which lists only `b10.notification.fanout` and `b10.notification.template-render`) does not contain — cross-graded `CRIT-04`.
- **Owning document:** `../../04-architecture/core/data-flow.md` (restate from the allocator; `naming-conventions.md:95` makes `../../06-backend/core/background-processing.md` the *Defined in* authority for queues).

### `CT-05` — Naming example vs register · `LOW` · `OPEN`

- **Statement A:** `22-glossary/core/naming-conventions.md:167` — "Queue: **`{block}.{entity}.{action}`** — `b02.inventory.expire`, `b07.escrow.release`, `b03.platform.webhook.send`".
- **Statement B:** `../../06-backend/core/background-processing.md:48` — "`b13.platform.webhook.send` | B13 | events | signed outbound webhooks (`INT-REQ-006`)".
- **Owning document:** `22-glossary/core/naming-conventions.md` §7.

### `CT-06` — Notification categories · `HIGH` · `OPEN`

- **Statement A (DB):** `../../08-database/core/notification.md:29` — "`category` | `notification_category` | … enum `SECURITY, ORDER, MARKETING, SYSTEM` | preference granularity (BR-NTF-05)".
- **Statement B (API):** `../../07-api/core/notifications.md:27` — "`category: "SECURITY"|"ORDER"|"DELIVERY"|"RETURN"|"PROMOTION"|"STORE_FOLLOW"|"SYSTEM"`"; reinforced by `:32` (`API-NTF-006` per-category matrix) and `:33` (`API-NTF-007`).
- **Why both cannot stand:** the API returns/stores four categories the enum cannot hold (`DELIVERY`, `RETURN`, `PROMOTION`, `STORE_FOLLOW`) and omits `MARKETING`; `notification_preference.category` (`notification.md:46`) inherits the same 4-value enum, so preference writes for `PROMOTION` cannot be persisted as specified.
- **Owning document:** `../../08-database/core/notification.md` (+ `constraints-and-integrity.md` if the enum is restated there) — or `../../07-api/core/notifications.md`, decided by `BR-NTF-05`.

### `CT-07` — KYC `IN_REVIEW` · `MEDIUM` · `OPEN`

- **Statement A (DB):** `../../08-database/core/store.md:33` — "`kyc_status` | `kyc_status` | no | `'PENDING'` | enum `PENDING, APPROVED, REJECTED`"; `../../08-database/core/constraints-and-integrity.md:91` repeats the same three values.
- **Statement B (API):** `../../07-api/admin/admin.md:38` — "status: `"PENDING"|"IN_REVIEW"`"; `admin.md:40` — "Approve KYC — `PENDING/IN_REVIEW → APPROVED`"; `../../07-api/core/error-model.md:150` — "`KYC_IN_REVIEW` | 409 | yes | New submission while a case is under review".
- **Why both cannot stand:** no column can hold `IN_REVIEW`, so the queue filter `?status=IN_REVIEW` and the error code have nothing to read from; `BR-VND-03` resubmission resets to `PENDING` (`store.md:37`) — a second, unstated path.
- **Owning document:** `../../07-api/admin/admin.md` + `../../07-api/core/error-model.md`, or the DB enum (owner: `08-database/`).

### `CT-08` — Top-up status vocabularies · `MEDIUM` · `OPEN`

- **Statement A (API):** `../../07-api/core/wallet.md:29-30` — "`status: "PENDING_PROVIDER"|"PENDING_VERIFICATION"`" on create, "`status: "PENDING_PROVIDER"|"PENDING_VERIFICATION"|"CREDITED"|"REJECTED"`" on poll (`API-WAL-003/004`).
- **Statement B (adapter contract):** `../../10-integrations/core/wallet-providers.md:51` — "Status vocabulary | normalized to `PENDING / SUCCEEDED / FAILED / EXPIRED` inside the adapter | `INT-REQ-008` taxonomy" (while `:35` in the same file describes "status → CREDITED").
- **Statement C (DB):** `../../08-database/core/constraints-and-integrity.md:85` — "`payment_state` | `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED`" (top-ups are `payment.kind='TOPUP'`; there is no top-up table — `../../08-database/core/payment.md:27`).
- **Why all three cannot stand:** none of `PENDING_PROVIDER`, `PENDING_VERIFICATION`, `CREDITED`, `REJECTED`, `SUCCEEDED`, `EXPIRED` exists in the only state column a top-up can occupy.
- **Owning document:** `../../07-api/core/wallet.md` (or `../../08-database/core/payment.md`), with `../../10-integrations/core/wallet-providers.md` §6 as the mapping owner.

### `CT-09` — Ledger `type` cardinality · `MEDIUM` · `OPEN`

- **Statement A (API):** `../../07-api/core/wallet.md:28` — "`type: "TOPUP"|"ORDER_PAYMENT"|"REFUND"|"ESCROW_HOLD"|"PAYOUT"`" (`API-WAL-002`, filter `?type`).
- **Statement B (DB):** `../../08-database/core/constraints-and-integrity.md:100` — "`ledger_type` | `TOPUP, ORDER_HOLD, ORDER_CAPTURE, RELEASE, REFUND, PAYOUT, COMMISSION, ADJUSTMENT`"; `../../08-database/core/wallet_transaction.md:29` repeats it.
- **Why both cannot stand:** three DB values (`ORDER_HOLD`, `ORDER_CAPTURE`, `COMMISSION`, `ADJUSTMENT` — four, minus `ORDER_PAYMENT`) have no API spelling, and `ORDER_PAYMENT` has no enum member; `?type=ORDER_PAYMENT` cannot be evaluated against the index.
- **Owning document:** `../../07-api/core/wallet.md`.

### `CT-10` — Inspection outcome spelling · `LOW` · `OPEN`

- **Statement A (API):** `../../07-api/core/returns.md:35` — "`{ outcome: "PASS"|"FAIL", notes, imageFileIds? }`" (`API-RET-009`).
- **Statement B (DB):** `../../08-database/core/return_request.md:44` — "`inspection_outcome` … enum `PASSED, FAILED`"; sample row `:90` shows `inspection_outcome=PASSED`.
- **Note:** a request→storage mapping is plausible but is not documented anywhere; per `root README §8` an undocumented mapping stays a contradiction, not an assumption.
- **Owning document:** `../../07-api/core/returns.md` (state the mapping) or `../../08-database/core/return_request.md`.

### `CT-11` — AC registry authority · `HIGH` · `OPEN`

- **Statement A:** `02-requirements/acceptance-criteria.md:17` — "**This document is the single, authoritative registry of every acceptance criterion (`AC-*`) in the yumn project.** … No other document may invent, redefine or contradict an AC listed here … The registry defines **253 ACs**". *(Quote as recorded at audit — since superseded: the same line now reads **273 ACs** — `acceptance-criteria.md` **v1.2**, registered session 011, 2026-09-30 (+16 `AC-SR` for `SEC-REQ-013`…`016`, +4 `AC-DR` for `DATA-REQ-009`).)*
- **Statement B:** `00-project-overview/success-criteria.md` defines `AC-S-01…AC-S-24`, including `AC-S-04`, `AC-S-12`, `AC-S-21` — **none of which appear in the registry** (registry holds 21 of 24; re-verified against `acceptance-criteria.md` **v1.2** on 2026-09-30 — all three IDs are still absent).
- **Impact:** 16 files cite the three missing IDs (e.g. `../../01-business-analysis/vendor/workflow-011.md:59` cites `AC-S-21`; `../../21-completion/core/quality-gates.md:134` gate 2.6 requires `AC-S-21/22/23`), so gate evidence cannot be traced through the declared registry. *(File count since superseded: **20** files cite at least one of the three on the 2026-09-30 re-count.)*
- **Still holds after session 011?** **Yes** — the count moved (253 → 273) and the external family table `../../19-traceability/core/requirements-to-tests.md` now carries **297** AC rows (277 → 297 in the same change set = 273 registry ACs + 24 `AC-S-*`), but the registry itself still omits `AC-S-04`/`AC-S-12`/`AC-S-21`; the contradiction is registry-vs-`AC-S-*`, not a numeric drift. Only the reconcile target changes (253 → 273). Status stays `OPEN` — not flipped (the rows are still not imported).
- **Owning document:** `02-requirements/acceptance-criteria.md` (import the three rows and reconcile the **273** total — 253 when this row was filed; session 011 raised the registry to 273 and the traceability family table to 297) — owner decision per root README §4.

### `CT-12` — AC shapes outside the registry · `MEDIUM` · `OPEN`

- **Statement A:** `02-requirements/acceptance-criteria.md:17` — "single, authoritative registry of **every** acceptance criterion".
- **Statement B:** 121 distinct `AC-UCnnn-nn` IDs are defined in `01-business-analysis/*.md` (e.g. `UC-001.md:60-62`) and appear in no registry row; `22-glossary/core/naming-conventions.md:112` documents the shapes "`AC-UCnnn-nn`, `AC-WF-NNN-NN` … observed in `01-business-analysis/`" with example `AC-WF-012-01`, which has **zero** occurrences anywhere and no workflow file contains an acceptance-criteria section. *(Counts as recorded at audit — since superseded: session 011 (2026-09-30) minted `UC-211`…`UC-420`, so the corpus now holds **420** UC files (portal-partitioned under `01-business-analysis/{core,admin,vendor,customer,delivery}/`); re-count returns **1591** distinct `AC-UCnnn-nn` IDs across those 420 files — still in no registry row, `AC-WF-012-01` still has zero occurrences. The contradiction widens, status unchanged.)*
- **Owning document:** `02-requirements/acceptance-criteria.md` + `22-glossary/core/naming-conventions.md` §3.1 (either register the UC/WF criteria or restate the claim).

### `CT-13` — Flat AC ID · `LOW` · `OPEN`

- **Statement A:** `../../15-deployment/core/production-readiness.md:66` — row S-4 "Secret scan clean on repo and images | … | `AC-SR007-01/03` results | NOT DONE | **`AC-SR-16`**".
- **Statement B:** `22-glossary/core/naming-conventions.md:120` — "Stray flat AC IDs (`AC-SR-16` …) | `../../15-deployment/core/production-readiness.md` | Not present in the `DOC-AC-001` v1.1 registry — cite the registered `AC-SRnnn-nn` … form or log the clash in `contradiction-audit.md`".
- **Owning document:** `../../15-deployment/core/production-readiness.md` (this entry satisfies the "log the clash" option; the file must still be corrected).

### `CT-14` — ADR index status · `MEDIUM` · `OPEN`

- **Statement A:** `04-architecture/core/architecture-decisions-reference.md:19` — "**Status note:** none of the ADR files listed below exist yet in `18-decisions/core/` — the directory is currently empty." and `:25-34` — ten rows reading "RESERVED — not yet written".
- **Statement B:** `../../18-decisions/core/ADR-001.md` … `ADR-010.md` all exist with `status: approved`; `18-decisions/core/decision-log.md:23-30` records the same ten as `ACCEPTED` dated 2026-09-26; `decision-log.md:17` states titles "match `04-architecture/core/architecture-decisions-reference.md` §1 exactly".
- **Self-acknowledged:** `decision-log.md:77` — "update `04-architecture/core/architecture-decisions-reference.md` §1 status from RESERVED to ACCEPTED (it currently shows RESERVED — the index must be re-synced and version-bumped when this authoring lands), then run `consistency-audit.md`."
- **Owning document:** `04-architecture/core/architecture-decisions-reference.md`.

### `CT-15` — Canonical GAP register · `MEDIUM` · `OPEN`

- **Statement A:** root `README.md:161` — "| Gaps | `GAP-NNN` | `GAP-03` | **`missing-information.md`** |"; `22-glossary/core/naming-conventions.md:90` — "Defined in | `missing-information.md`".
- **Statement B:** `../../16-data/core/retention-and-archival.md:39` — "No new `GAP-NNN` ID is minted here — gap IDs are assigned only in the canonical GAP register (**`00-project-overview/project-scope.md` §Open items**)"; `../../12-non-functional/core/compliance-and-legal.md:88` — "recorded in `missing-information.md` when that register is authored (**no new gap IDs minted outside the canonical GAP register, per `DOC-DTA-005` convention**)"; `../../21-completion/core/quality-gates.md:80` cites `00-project-overview/project-scope.md` as the Gate-0 GAP source.
- **Consequence:** `GAP-08…GAP-12` had to be minted somewhere; this audit records that `missing-information.md` did so under root README precedence while `project-scope.md` still carries only six rows.
- **Owning documents:** `../../16-data/core/retention-and-archival.md`, `../../12-non-functional/core/compliance-and-legal.md` (and `../../21-completion/core/quality-gates.md:80` once decided).

### `CT-16` — Disallowed synonyms · `LOW` · `OPEN`

- **Statement A:** `22-glossary/core/naming-conventions.md:210` — "**Seller** is a **disallowed synonym** … "\"Seller\"/\"merchant\" anywhere in documents (only inside quotations of external text); never name a table `seller` or a route `/sellers/...`\"".
- **Statement B (canon uses them):** `00-project-overview/project-charter.md:42`, `00-project-overview/project-constraints.md:43` (`C-11`), `02-requirements/requirements-overview.md` (`FR-016` commission wording) — plus 17 files containing `seller` and 30 containing `merchant`.
- **Owning document:** `22-glossary/core/naming-conventions.md` §11 (narrow the ban to identifiers) or the canon rows (renaming), decided by the glossary owner; neither may be changed unilaterally (root README §9.4).

### `CT-17` — `A-07` claim · `LOW` · `OPEN`

- **Statement A:** `22-glossary/core/naming-conventions.md:121` — "Security finding cited as `A-07` | `../../09-security/core/security-findings.md` (SEC-008) | The register uses `ASM-*`/`SEC-*`; **`A-07` is undefined** — cite `ASM-07` intent or log in `contradiction-audit.md`".
- **Statement B:** `../../09-security/core/threat-model.md:29` — "| `A-07` | KYC documents & bank-transfer receipts | HIGH | Identity fraud | MinIO (`DEP-07`), PostgreSQL references |" — an asset row inside the `A-01…A-10` asset table (`threat-model.md:21-32`), also cited at `../../09-security/core/data-protection.md:37`, `secrets-management.md:39`, `../../18-decisions/core/ADR-007.md:94`.
- **Why both cannot stand:** the ID is defined; what is actually missing is an `A-NN` row in `naming-conventions.md` §3 (*Defined in* column), not the asset.
- **Owning document:** `22-glossary/core/naming-conventions.md` §3 + §3.2.

---

### `CT-18` — Payment release status · `MEDIUM` · `OPEN`

- **Statement A:** `../../07-api/core/wallet.md:34` (API-WAL-008 `POST /wallet/payments/{id}/release`) — "`{ reason }` → `200 { paymentId, status: "RELEASED" }`".
- **Statement B:** `../../08-database/core/payment.md:33` — "`state` | `payment_state` | … enum `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED`" and `constraints-and-integrity.md:85` — "`payment_state` | `PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED` | `payment.state`".
- **Why both cannot stand:** the response is keyed by `paymentId` and names a `status` the payment column cannot hold; `RELEASED` is a legal value only of `escrow_state` (`../../08-database/core/escrow.md:32` — `HELD, RELEASED, REFUNDED, FROZEN`), and no document states that API-WAL-008 reports an escrow/hold status under a payment-scoped field. A client reading `{ paymentId, status }` cannot map it to `payment.state`.
- **Owning document:** `../../07-api/core/wallet.md` (declare the response status domain) — cross-graded `CRIT-03`.

---

### `CT-19` — Refund status vocabulary · `MEDIUM` · `OPEN`

- **Statement A:** `../../07-api/core/wallet.md:40` (API-WAL-014 `GET /orders/{id}/refund`) — "`status: "PENDING"|"COMPOSED"|"CREDITED"` … wallet credit within 3 business days of `REFUNDED`".
- **Statement B:** `../../08-database/core/payment.md:60` — "`refund` (supporting) … `state ∈ {PENDING, PROCESSING, COMPLETED, FAILED}`".
- **Why both cannot stand:** only `PENDING` is in both sets; `COMPOSED` and `CREDITED` have no stored representation, while `PROCESSING`, `COMPLETED` and `FAILED` are never exposed on a customer-facing receipt, and no mapping table exists in `07-api/` or `08-database/`.
- **Owning document:** `../../07-api/core/wallet.md` + `../../08-database/core/payment.md` (pick one vocabulary and map) — cross-graded `CRIT-03`.

---

### `CT-20` — Payout state domain · `MEDIUM` · `OPEN`

- **Statement A:** `../../07-api/core/wallet.md:37-38` — API-WAL-011 returns `status: "REQUESTED"`; API-WAL-012 filters/returns `status: "REQUESTED"|"SCHEDULED"|"EXECUTED"|"REJECTED"|"ROLLED_OVER"`.
- **Statement B:** `../../08-database/core/indexes-and-performance.md:138-139` — "`payout` | `idx_payout_store_state` on `(store_id, state, created_at DESC)`" and "`payout` | `idx_payout_state` on `(state, eligible_at)` WHERE `state='ELIGIBLE'`", while `constraints-and-integrity.md:84-100` declares `payment_state` and `escrow_state` but **no `payout_state`** (0 documents define one).
- **Why both cannot stand:** the schema's only documented payout `state` value — `ELIGIBLE`, indexed and driven by `eligible_at` for the ≥1,000 YER / 3–7 business-day batch job — is unreachable through the API's five-value status set, and the five API values have no declared storage domain. Vendors cannot filter for eligible payouts; `ROLLED_OVER` (wallet.md:38) has no counterpart anywhere in `08-database/`.
- **Owning document:** `../../08-database/core/constraints-and-integrity.md` (declare `payout_state`) + `../../07-api/core/wallet.md` (align status set).

---

### `CT-21` — `J10` cadence · `MEDIUM` · `OPEN`

- **Statement A (job register — the owner):** `../../16-data/core/data-quality.md:84` — "`J10` | Audit hash-chain verification | All audit partitions | **Hourly** | Chain intact | Alert + freeze privileged writes for investigation".
- **Statement B (post-launch cadence):** `../../17-risk-management/core/mitigation-plans.md:46` — "Post-launch | **Nightly** `J1`/`J2`/`J10` forever; monthly invariant attestation; any money-path incident triggers re-score"; repeated at `../../21-completion/core/implementation-roadmap.md:188` — "`RISK-001` (nightly `J1`/`J2`/`J10` forever, monthly attestation)".
- **Statement C (risk acceptance):** `17-risk-management/core/risk-register.md:79` — "…accepted with **daily** chain verification `J10` + signed…".
- **Why all cannot stand:** the residual-risk acceptance for `SEC-002`/`SEC-REQ-010` R4 is granted *in exchange for* a stated verification cadence, and three documents name three different cadences (hourly / nightly / daily); `implementation-roadmap.md:174` defers to `data-quality.md` while `:188` of the same file asserts nightly. An operator cannot tell which cadence is the binding control — hourly would satisfy every other claim, but "daily/nightly" acceptance language would be falsified by an hourly-only job in a future re-tuning.
- **Owning document:** `../../16-data/core/data-quality.md` (job register decides); `mitigation-plans.md`, `risk-register.md:79`, `implementation-roadmap.md:188` must then be re-worded to the single cadence. Deferred item (b); logged at sweep 2026-09-28, re-searched from `J10` grep (5 occurrence sites re-read).

---

### `CT-22` — `ipHash` (API) vs raw `ip` (schema) · `MEDIUM` · `OPEN`

- **Statement A (API + privacy claim):** `../../07-api/admin/admin.md:77` (`API-ADM-024` response) — "`{ id, at, actorId, actorRole, action, targetType, targetId, reason?, ipHash, correlationId }`"; `admin.md:125` — "**No PHI/secret leakage**: … audit entries store `ipHash`, not raw IPs (`SEC-REQ-008`)"; test projections repeat the field name (`TC-036.md:53`, `TC-053.md:46`, `TC-109.md:57`).
- **Statement B (schema):** `../../08-database/core/audit_log.md:40` — "`ip` | `inet` | yes | null | — | client address (`BR-PLT-06`)" — a raw client address column; the entity defines no `ip_hash`.
- **Why both cannot stand:** either the API hashes on read (an undocumented transformation, violating the "schema is the contract" convention of `08-database/README.md`) or the privacy claim at `admin.md:125` is false while a raw `ip` sits in an append-only, exportable table; either way `SEC-REQ-008`'s "no raw IPs" statement and the schema disagree. A third option — store the hash — requires a schema change neither document mentions.
- **Owning document:** `../../08-database/core/audit_log.md` + `../../07-api/admin/admin.md` (pick storage-vs-hash-on-read and document it once). Deferred item (d); logged at sweep 2026-09-28.

---

### `CT-23` — Multi-currency sub-accounts vs `C-04` · `HIGH` · `OPEN`

- **Statement A (sponsor spec, 2026-09-28):** `describ.md:19` — "this account includes **sub-accounts denominated in various currencies**"; `:38-40` — "if the user holds a balance in Yemeni currency but places an order in Saudi Riyals, the system displays the equivalent deduction based on the system's standard exchange rate, or deducts the amount from an account holding the same currency as the order"; `:63-64` — "**Currency management is handled by the platform**, which controls the **exchange rate** and updates it across the entire system."
- **Statement B (canon):** `00-project-overview/project-constraints.md:26` — "`C-04` | **No cryptocurrency; single currency.** Fiat YER only — no USD/SAR wallets in v1."; corroborated by `../../02-requirements/functional/core/FR-013.md:29` ("a YER-only per-user wallet") and the `../../08-database/core/wallet.md` `currency=YER` column.
- **Why both cannot stand:** sub-accounts denominated in USD/SAR, cross-currency deduction at a "standard exchange rate", and a platform-set FX rate are exactly what `C-04` forbids in v1; the canon's ledger, wallet row, and order money path have no second currency, no rate table, and no FX posting type.
- **Owning document:** constraint amendment via root `docs/README.md` §9 change control (sponsor-owned) — or the spec is re-scoped to YER-only (`GAP-13`). Never fixed by editing `C-04` locally.

---

### `CT-24` — Al-Kuraimi/Jeeb + provider PIN vs `C-05` · `HIGH` · `RESOLVED` 2026-09-28

- **Statement A (sponsor spec):** `describ.md:28-30` — "**Via external wallets integrated with the system via API.** The user enters the payment ID and the PIN generated within their external wallet (such as **Al-Kuraimi** or **Jeeb**). The system verifies the transaction through the connected API and adds the amount to the balance."
- **Statement B (canon):** `00-project-overview/project-constraints.md:27` — "`C-05` | **Wallet top-up methods:** mobile wallet (m-Floos, OneCash) and bank transfer (manual admin verification). No other instruments."
- **Agreement noted:** spec §2.2 ("submits proof of payment, which an administrator then verifies before adding the funds") matches `business-rules.md:94` `BR-PAY-04` exactly; only the first funding leg (named providers + PIN instrument) conflicts.
- **Why both cannot stand:** `C-05` enumerates the complete instrument set; Al-Kuraimi and Jeeb are not in it, and adding them amends a constraint that also drives the `DEP-05` integration scope and the `C-05` constraint-test row.
- **Owning document:** §9 change control (sponsor) if the providers are intended; otherwise the spec leg is dropped (`GAP-13`).
- **Resolution (`D1`/`M-02`, administrator, 2026-09-28):** `project-constraints.md` **v1.1** amends `C-05` to include Al-Kuraimi Bank and Jeeb (verification citation fixed to `API-WAL-003/004`); `project-scope.md` v1.2 OUT OF SCOPE row follows. Both statements now stand — conflict closed. `DEP-05`/`GAP-10` (provider API specs) remain OPEN on their own merits.

---

### `CT-25` — Email login option vs `C-06` · `HIGH` · `RESOLVED` 2026-09-28

- **Statement A (sponsor spec):** `describ.md:68` — "Login is performed using a **phone number and/or email**; the **phone number is mandatory**, while the **email is optional**."; `:74` — "2. **Email and password.**"
- **Statement B (canon):** `00-project-overview/project-constraints.md:33` — "`C-06` | **Phone + OTP only.** Primary identifier is the phone number; verification via SMS or WhatsApp. No email-primary auth, no social login."; canon login paths are phone+password (primary) and phone+OTP (alternate) per `FR-001`.
- **Agreement noted:** the spec's phone-mandatory rule and phone-verified-at-registration match `C-06` and `FR-001`; the conflict is email as a second login identifier.
- **Why both cannot stand:** an email+password path introduces a second primary identifier the auth design, user entity, and `SEC-REQ-001` flows never modelled; `C-06` was granted on market grounds (phone universal, email is not).
- **Owning document:** §9 change control (sponsor) if email login is intended; otherwise the spec option 2 is dropped (`GAP-13`).
- **Resolution (`D1`/`M-03`, administrator, 2026-09-28):** `project-constraints.md` **v1.1** amends `C-06` to permit an **optional, verified email on the profile** (contact/notification data only — never identifier, never OTP channel); the spec's option-2 login leg ("Email and password") stays rejected and `describ.md` is re-scoped there. Phone remains the sole primary identifier (`FR-001`, `SEC-REQ-001` untouched).

---

### `CT-26` — Merchant-defined escrow period vs `C-12` · `HIGH` · `OPEN`

- **Statement A (sponsor spec):** `describ.md:57-59` — "**Returnable products are designated by the merchant**; the value of these items is held in an **escrow account for the duration of the merchant-defined return period**. Funds for items that are **not returned are released directly**."
- **Statement B (canon):** `00-project-overview/project-constraints.md:44` — "`C-12` | **Escrow:** funds held 7 days from DELIVERED before release to vendor (unless dispute freezes)."
- **Agreement noted:** merchant designation of returnable products matches `BR-RET-01`; only the hold duration semantics conflict (fixed 7-day clock vs per-merchant window).
- **Why both cannot stand:** the escrow engine's release timer, the delayed-job `b07.escrow.release` schedule, and `C-12`'s constraint test all encode one fixed delay; a merchant-defined period makes release time an unbounded per-store parameter with no canon default, cap, or timezone rule.
- **Owning document:** §9 change control (sponsor) if merchant-defined windows are intended; otherwise the spec is re-scoped to the 7-day clock (`GAP-13`).

---

### `CT-27` — P2P account funding vs "money never flows between actors" · `HIGH` · `OPEN`

- **Statement A (sponsor spec):** `describ.md:33` — "**Via account funding.** Another person transfers funds from their own account to this user's account."; repeated `:41-42` — "Users can **deposit funds into another person's account**…"
- **Statement B (canon):** `../../03-system-analysis/core/system-context.md:96` — "**Money never flows directly between actors.** Customer funds enter only via top-up (`C-05`); vendor exit is only the platform payout (`BR-ESC-05`); refunds credit the wallet (`BR-PAY-07`)."
- **Why both cannot stand:** P2P wallet-to-wallet transfers are a direct actor-to-actor money flow — the invariant the system-context document names as one of its load-bearing principles (`FR-013`'s top-up enumeration has no P2P leg, and `ledger_type` has no transfer posting type); granting it would also reopen fraud/laundering controls the risk register assumed closed.
- **Owning document:** §9 change control (sponsor) — this is a system-boundary change, not a wording fix (`GAP-13`).

---

### `CT-28` — Customer withdrawal vs `BR-PAY-07` · `MEDIUM` · `OPEN`

- **Statement A (sponsor spec):** `describ.md:41-42` — "Users can … **request a withdrawal to an external wallet**, subject to the options available in the system."
- **Statement B (canon):** `01-business-analysis/business-rules.md:97` — "`BR-PAY-07` | Refunds always credit the wallet — never external cash-out to cards/banks (except vendor payouts, BR-ESC-05)."
- **Why both cannot stand:** a customer-facing "withdrawal to an external wallet" is external cash-out; `BR-ESC-05`'s exception covers vendor payouts only. (Vendor cash-out is itself undecided — `GAP-06` — but the spec's §3.2 subject is the customer account.)
- **Owning document:** §9 change control (sponsor) if customer cash-out is in v1; otherwise the spec leg is dropped (`GAP-13`).

---

### `CT-29` — Admin collective account actions vs RBAC rows 15–16 · `HIGH` · `RESOLVED`-NO 2026-09-28

- **Statement A (sponsor spec):** `describ.md:52-53` — "The **management function** (administration) enables operations on and the viewing of accounts — either individually or **collectively** — as well as **any actions deemed appropriate for account management**."
- **Statement B (canon):** `../../09-security/core/rbac.md:51` — row 15 `Direct ledger / balance adjustment (manual write)`: CUSTOMER `✖` … ADMIN `✖` … SYSTEM `✖ (compensating entries only)`; `:52` — row 16 `Read a customer's wallet balance / transactions`: ADMIN `✖`, SUPER_ADMIN `✖`.
- **Why both cannot stand:** the matrix grants **no role** manual ledger writes (only `SYSTEM` compensating entries) and denies admin wallet reads entirely, while the spec promises collective admin operations and viewing "as … appropriate" — an open-ended grant that `SEC-REQ-004`/`FR-002` never modelled, and "collectively" implies bulk balance operations the append-only ledger design has no API for.
- **Owning document:** `../../09-security/core/rbac.md` is the definitive matrix (`DOC-OVR-007`); changing it requires §9 change control with security sign-off (`GAP-13`).
- **Resolution (`D1`/`M-07` = **NO**, administrator, 2026-09-28):** canon stands — `rbac.md` rows 15–16 remain absolute (no role adjusts ledgers; no role but the customer reads a wallet); the spec leg is rejected. `rbac.md` §11 (minted the same day) restates the guardrail in the department/permission model. Closed as `RESOLVED`-NO — no canon edit, spec re-scoped.

---

### `CT-30` — Wallet row creation timing (canon-internal) · `MEDIUM` · `OPEN`

- **Statement A:** `../../02-requirements/functional/core/FR-013.md:45` — "User account exists (FR-001) with a **wallet row created at registration**."; the sponsor spec asserts the same shape at `describ.md:18-19` ("Once a customer or merchant is registered **and verified**, a financial account is created for them").
- **Statement B:** `../../08-database/core/wallet.md:34` — `created_at` … "created **lazily on first top-up/order attempt**".
- **Why both cannot stand:** either a wallet row exists for every registered user (statement A) or it appears only on first money attempt (statement B); they cannot both be true, and downstream behaviour differs (zero-balance rows in the table, `UC-041` top-up flow, wallet-freeze preconditions). This one is canon-internal — the sponsor spec merely surfaced it.
- **Owning document:** `../../02-requirements/functional/core/FR-013.md` and `../../08-database/core/wallet.md` (owner decision; `GAP` not minted — the answer exists in canon, the two rows just disagree).

---

## 3. Coverage & Statistics

- Files examined: **~56** directly cited files (each quoted line re-read in context), out of 480 in scope at the 2026-09-28 re-run (479 at session-006, 433 at original sweep) plus the root sponsor file `describ.md`; seeded by `AUD-01` failing checks `CHK-16`, `CHK-19`, `CHK-20`, `CHK-21`, `CHK-22`, `CHK-23`, `CHK-24`, `CHK-25`, `CHK-12`, `CHK-13`, `CHK-14`, `CHK-31`, plus deferred sweep items (b)/(d), plus the session-007 sponsor-input reconciliation.
- Checks run: **30** — passed 1 (`CT-01`), failed 19 at audit; 2026-09-27 re-run: `CT-04`/`CT-05` conditions now pass → passed 3, 15 recorded `OPEN`; 2026-09-28 session-006 sweep: `CT-21`/`CT-22` added → issued 22, 17 `OPEN`; 2026-09-28 session-007 sponsor reconciliation: `CT-23`…`CT-30` opened (8) and `CT-14` → `RESOLVED` (`REC-02`) → issued 30, 24 `OPEN`; 2026-09-28 `GAP-13` disposition (`plan-develop.md` §8 `D1`): `CT-24`/`CT-25` → `RESOLVED` (constraints amended), `CT-29` → `RESOLVED`-NO → issued 30, **21 `OPEN`**.
- ID references verified: 30 statement pairs, every one with `file:line` (sponsor quotes cite `describ.md` line numbers); **0** fabricated or assumed citations.
- Contradictions by severity (issued): `CRITICAL` 0 · `HIGH` 9 (`CT-04`, `CT-24`, `CT-25`, `CT-29` resolved — `CT-06`, `CT-11`, `CT-23`, `CT-26`, `CT-27` open) · `MEDIUM` 14 (`CT-14` resolved, 13 open) · `LOW` 6 (`CT-05` resolved) · `PASS` 1.
- Series in scope: `CT-NN` issued 30 · open 21 · resolved 8 (`CT-02`, `CT-03` — `REC-05`; `CT-04`, `CT-05` — `REC-06`, all 2026-09-27; `CT-14` — `REC-02`, 2026-09-28; `CT-24`, `CT-25` — `D1` constraint amendments, `CT-29` — `D1`/`M-07` NO, all 2026-09-28) · passed 1.
- Cross-graded against the sibling audits: `CT-18` = `CRIT-03(a)`, `CT-19` = `CRIT-03(c)`, `CT-08` = `CRIT-03(b)`, `CT-04` = `CRIT-04`, `CT-11`/`CT-12` adjacent to `CRIT-05` (`critical-findings.md:51-53`). Severities here grade the *document conflict*; `critical-findings.md` grades gate impact. `CT-20` (payout state domain) is not covered by any `CRIT-*` row. Sponsor-input conflicts `CT-23`…`CT-29` are graded here only; their gate impact routes through `GAP-13` (change-control decision), not a `CRIT-*` row; `CT-30` is canon-internal.

---

## 4. Verdict & Sign-off

- **Gate:** `PASS WITH FINDINGS` (root README §11) — the audit ran to completion with every conflict evidenced; 21 remain `OPEN` because fixing them is the owning document's job (root README §9.5 forbids local fixes here). `CT-02`/`CT-03` were closed under `REC-05`, `CT-04`/`CT-05` under `REC-06`, by the owning documents' change sets on 2026-09-27; `CT-14` closed under `REC-02` on 2026-09-28 (ADR index v1.1); `CT-21`/`CT-22` were added by the session-006 sweep on 2026-09-28 from the deferred backlog; `CT-23`…`CT-30` were opened by the session-007 sponsor-input reconciliation on 2026-09-28; `CT-24`/`CT-25` closed by the `C-05`/`C-06` amendments and `CT-29` closed `RESOLVED`-NO under the `GAP-13`/`D1` disposition on 2026-09-28.
- **Unresolved contradictions / gaps:** `CT-06`…`CT-13`, `CT-15`…`CT-23`, `CT-26`…`CT-28`, `CT-30` (`OPEN`); `CT-01` `PASS`/`CLOSED`; `CT-02`, `CT-03`, `CT-04`, `CT-05`, `CT-14`, `CT-24`, `CT-25`, `CT-29` `RESOLVED`. Cross-links: `GAP-01…GAP-16` (`missing-information.md`) — `GAP-13` `RESOLVED` 2026-09-28 (mixed disposition), `GAP-02`/`GAP-03` `RESOLVED` same day (`D7`/`D6`); findings 6–11, 13, 14, 15, 16, 17, 22, 24, 26 (`consistency-audit.md`) — finding 12 closed alongside `CT-02`/`CT-03`; `HAL-15` (`hallucination-audit.md`) cross-links the `API-TOP` group defect (`RESOLVED` 2026-09-28); `HAL-02` `RESOLVED` alongside `CT-14`.
- **Required follow-up — owning documents that must change, in propagation order (root README §9.4), edits NOT made by this audit:** ~~`../../15-deployment/core/health-checks.md` + `../../07-api/admin/admin.md` (`CT-02`, `CT-03`)~~ **done 2026-09-27 (`REC-05`, both docs v1.1 + `TC-001/031/057/065` v1.1)** · ~~`../../04-architecture/core/data-flow.md` + `../../06-backend/core/background-processing.md` + `10-integrations/*` + `13-testing/TC-061/063/064/107` (`CT-04`)~~ **done 2026-09-27 (`REC-06`)** · ~~`04-architecture/core/architecture-decisions-reference.md` (`CT-14`)~~ **done 2026-09-28 (`REC-02`, index v1.1)** · `../../07-api/core/notifications.md` + `../../08-database/core/notification.md` (`CT-06`) · `02-requirements/acceptance-criteria.md` (`CT-11`, `CT-12`) · `../../07-api/core/wallet.md` (`CT-08`, `CT-09`, `CT-18`, `CT-19`, `CT-20`) + `../../08-database/core/payment.md` (`CT-18`, `CT-19`) + `../../08-database/core/constraints-and-integrity.md` (`CT-20`) · `../../16-data/core/retention-and-archival.md` + `../../12-non-functional/core/compliance-and-legal.md` (`CT-15`) · `../../07-api/admin/admin.md` + `../../07-api/core/error-model.md` (`CT-07`) · `22-glossary/core/naming-conventions.md` (~~`CT-05`~~ done 2026-09-27; `CT-16`, `CT-17`) · `../../15-deployment/core/production-readiness.md` (`CT-13`) · `../../07-api/core/returns.md` (`CT-10`) · `../../16-data/core/data-quality.md` + `../../17-risk-management/core/mitigation-plans.md` + `risk-register.md` + `../../21-completion/core/implementation-roadmap.md` (`CT-21` cadence) · `../../08-database/core/audit_log.md` + `../../07-api/admin/admin.md` (`CT-22` `ipHash`) · ~~**sponsor change control, root `docs/README.md` §9 — `CT-23`…`CT-29`**~~ **decided 2026-09-28 (`GAP-13` disposition `D1`, mixed): `CT-24`/`CT-25` → `RESOLVED` via `C-05`/`C-06` amendments (`project-constraints.md` v1.1), `CT-29` → `RESOLVED`-NO (canon stands); `CT-23` (`M-01`), `CT-26` (`M-04`), `CT-27`/`CT-28` (`M-05`/`M-06`) remain `OPEN` — finance/security/owner review before any `C-04`/`C-12`/`BR-PAY-07` edit; FX mechanics stays `GAP-14`** · `../../02-requirements/functional/core/FR-013.md` + `../../08-database/core/wallet.md` (`CT-30` wallet-row timing). After each change: bump `version`, add the §9.2 row, re-run the linked `AUD-01` checks, log the propagation.
- **Sign-off:** analysis-agent, 2026-09-27; amended by session 007, 2026-09-28.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial baseline: `CT-01` recorded `PASS`; `CT-02…CT-17` opened with exact conflicting statements | Root README §9.5 / §10 item 42; `project-constraints.md:89` (`CT-01` mandate); `DOC-TPL-011` |
| 1.1 | 2026-09-27 | `CT-18` (`payment` `RELEASED`), `CT-19` (refund status set), `CT-20` (payout state domain) opened after the money-path re-read; `CT-04` gains the intra-file `b10.notification.delivery.*` evidence; statistics re-issued (20 checks: 1 pass / 19 open) and cross-grades to `CRIT-03(a)(c)` / `CRIT-04` / `CRIT-05` recorded | `AUD-01` check `CHK-31`; cross-ref `critical-findings.md` `CRIT-03`; root README §9.5 |
| 1.2 | 2026-09-27 | `CT-02`, `CT-03` → `RESOLVED` (health-path canon `/healthz` + `/readyz` applied in `admin.md` v1.1, `health-checks.md` v1.1, `TC-001/031/057/065` v1.1); statistics re-issued (open 17 / resolved 2); follow-up list updated | `REC-05` / `TD-06` pay-down; root README §9.5 (resolution recorded, rows kept) |
| 1.3 | 2026-09-27 | `CT-04`, `CT-05` → `RESOLVED` (single 30-row queue register adopted: `data-flow.md` v1.1, `background-processing.md` v1.1, `naming-conventions.md` v1.2, `search.md`, `10-integrations/*`, `TC-061/063/064/107`); statistics re-issued (open 15 / resolved 4); follow-up list updated | `REC-06` / `TD-07` pay-down; root README §9.5 (resolution recorded, rows kept) |
| 1.4 | 2026-09-28 | Session-006 sweep: `CT-21` (`J10` hourly vs nightly vs daily cadence) and `CT-22` (`ipHash` API field vs raw `ip` schema column) opened from the deferred backlog items (b)/(d) with re-read evidence; title/range → `CT-01…CT-22`; statistics re-issued (issued 22, open 17); follow-up list extended | Deferred sweep findings must land in their owning register (session-006 mandate); root README §9.5 |
| 1.5 | 2026-09-28 | Session-007 sponsor-input reconciliation: `CT-23`…`CT-30` opened (8 conflicts between `describ.md` and canon: `C-04`, `C-05`, `C-06`, `C-12`, system-context actor-flow principle, `BR-PAY-07`, RBAC rows 15–16, plus canon-internal wallet-creation timing), each with verbatim quotes and §9 change-control routing via `GAP-13`/`GAP-14`; `CT-14` → `RESOLVED` (`REC-02`); title/range → `CT-01…CT-30`; statistics re-issued (issued 30, open 24) | Sponsor spec `describ.md` (session 007, `D-16` resolved) must be reconciled against canon — contradictions registered, never silently absorbed (root README §9.5); findings kept, never deleted (DOC-TPL-011 #3) |
| 1.6 | 2026-09-28 | `GAP-13` disposition (`plan-develop.md` §8 `D1`, administrator): `CT-24` → `RESOLVED` (`C-05` amended +Al-Kuraimi/Jeeb), `CT-25` → `RESOLVED` (`C-06` amended, optional verified profile email), `CT-29` → `RESOLVED`-NO (`M-07` = NO, rbac rows 15–16 absolute); `CT-23`/`CT-26`/`CT-27`/`CT-28` annotated (`M-01`/`M-04`/`M-05`/`M-06` stay OPEN on their own merits); statistics re-issued (issued 30, open 21, resolved 8); verdict + follow-up re-scoped | Approval implementation (session 007) — owning documents changed under `docs/README.md` §9; findings flipped, never deleted (DOC-TPL-011 #3) |
| 1.7 | 2026-09-30 | Session-011 count refresh, **annotation only** — no status, severity or roll-up change: `CT-11` annotated (registry 253 → **273**, `acceptance-criteria.md` v1.2; external family table 277 → **297**; citing files 16 → 20; reconcile target 253 → 273; contradiction re-checked 2026-09-30 and **still holds** — `AC-S-04`/`AC-S-12`/`AC-S-21` remain absent from the registry), `CT-12` annotated (121 → **1591** distinct `AC-UCnnn-nn` across the **420** UC files minted through `UC-420`, `AC-WF-012-01` still undefined); both summary rows updated to match | Owner directive session 011 `prompt-011.md` §4.8 — proposal/disposition rows in the relevant registers (`CT`/`GAP`/`HAL` as applicable) |
| 1.8 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
| 1.9 | 2026-10-02 | GAP range consumers refreshed (annotation only — no CT status/severity change): `CT-15` evidence `GAP-01…GAP-12` → `GAP-01…GAP-16`; §6 cross-links `GAP-01…GAP-14` → `GAP-01…GAP-16` | Root README §9.4 consumer re-sync — `missing-information.md` v1.5 mint (session-013 wave D) |
