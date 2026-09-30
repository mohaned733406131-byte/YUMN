---
document_id: DOC-DEC-002
title: Decision Log
category: 18-decisions
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-016, NFR-018, FR-009, FR-013, FR-001]
related_documents: [DOC-DEC-001, DOC-ARCH-010, DOC-ARCH-009, DOC-ROOT-001]
---

# Decision Log (DOC-DEC-002)

Chronological record of every decision in the project: full ADRs (§1), decisions captured inline because they do not warrant an ADR (§2), and parked candidates (§3). ADR *texts* live in `ADR/`; this log is the index with one-line outcomes and driving IDs. Titles match `04-architecture/architecture-decisions-reference.md` §1 exactly.

## 1. Architecture Decision Records (ADR-001 … ADR-010)

| ADR | Title | Date | Status | Deciders | One-line outcome | Driving IDs | Record |
|---|---|---|---|---|---|---|---|
| ADR-001 | PostgreSQL 16 as the sole relational database | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | One ACID store holds money, stock and order state in a single consistency boundary; no other RDBMS permitted | `C-19`, `DEP-02`, `NFR-006`, `NFR-008` | [ADR/ADR-001.md](core/ADR-001.md) |
| ADR-002 | Modular monolith instead of microservices | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | One deployable NestJS app with tool-enforced module boundaries for `B01…B13`; no distributed transactions in money paths | `C-21`, `NFR-009`, `NFR-010` | [ADR/ADR-002.md](core/ADR-002.md) |
| ADR-003 | NestJS 10 as the backend framework | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | NestJS module/DI structure mirrors the block model; guards/pipes carry RBAC and validation; full TypeScript fit with web/mobile | `DEP-01`, `C-21`, `NFR-009` | [ADR/ADR-003.md](core/ADR-003.md) |
| ADR-004 | Docker Compose deployment; no Kubernetes in v1 | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | Single-host Compose topology with layered environment parity satisfies `C-25`; images stay orchestrator-portable for v2 | `C-22`, `NFR-016`, `NFR-018` | [ADR/ADR-004.md](core/ADR-004.md) |
| ADR-005 | Redis 7 + BullMQ as the only queue/cache substrate | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | One dependency covers cache, counters, TTL state and durable jobs (retries/DLQ/delayed) — no Kafka/RabbitMQ ever | `C-20`, `DEP-03`, `BR-PLT-01/02`, `NFR-004` | [ADR/ADR-005.md](core/ADR-005.md) |
| ADR-006 | Elasticsearch 8 for search & discovery | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | Arabic-aware analysis plus facets/aggregations deliver `FR-009` quality relational FTS cannot at target scale; index is rebuildable | `DEP-04`, `FR-009`, `NFR-007` | [ADR/ADR-006.md](core/ADR-006.md) |
| ADR-007 | MinIO for object storage | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | Self-hosted S3-compatible storage avoids cloud lock-in while keeping the S3 API portable inside the Compose topology | `DEP-07`, `NFR-016`, `C-22` | [ADR/ADR-007.md](core/ADR-007.md) |
| ADR-008 | React Native 0.73 + Next.js 14 for all client surfaces | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | One language across five surfaces: RN for customer + courier apps, Next.js SSR for the three web shells with structural RTL | `NFR-002`, `NFR-013`, `NFR-015`, `DEP-12` | [ADR/ADR-008.md](core/ADR-008.md) |
| ADR-009 | Wallet-only payments with provider adapters | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | Pre-funded wallet + escrow is the only payment model; providers sit behind adapters so custody/ rails can change without domain rework | `C-01…C-05`, `INT-REQ-001/008`, `FR-013` | [ADR/ADR-009.md](core/ADR-009.md) |
| ADR-010 | Phone + OTP authentication with short-lived JWTs | 2026-09-26 | ACCEPTED | project sponsor + architecture (analysis phase) | Phone is the sole identity; SMS/WhatsApp OTP verifies events; 15-min access + 7-day single-use rotating refresh tokens give stateless scale-out | `C-06…C-08`, `SEC-REQ-001/003`, `FR-001` | [ADR/ADR-010.md](core/ADR-010.md) |

All ten were decided together during the analysis phase (2026-09-26), consultatively with DOC-ARCH-010 (index) and `technology-stack.md` (stack register) — those two documents and these ADRs must always agree; on conflict, **the ADR carries the text, the constraint outranks them both** (DOC-ARCH-010 §6).

## 2. Decisions Without ADR

Smaller decisions that are binding but do not shape architecture enough for a full record. Each is defined once (source of truth cited) and referenced by ID elsewhere.

| ID | Decision | Rationale | Where defined (source of truth) |
|---|---|---|---|
| D-01 | **Money is stored as integer YER — no floats, no minor units, single currency (`C-04`)** | Floating point cannot represent money safely; Yemen has no sub-unit circulation; rounding is explicit half-up at sub-order level with differences posted to a platform rounding account | `01-business-analysis/business-rules.md` `BR-PAY-10`, `BR-FIN-05`; enforced `DQ-09` in `../16-data/core/data-quality.md` |
| D-02 | **Arabic-Indic numerals (`٠١٢٣٤٥٦٧٨٩`) for user-facing money and counts in `ar`; Latin digits in `en`; inputs accept both and normalize to Latin integers** | Arabic-first market expectation for `ar-YE`; server must never pre-format money — APIs return raw integers and clients format via `Intl.NumberFormat('ar-YE')` | `../05-frontend/core/rtl-and-styling.md` §Digit style; `../07-api/core/api-conventions.md` §Locale display; `BR-PAY-10` |
| D-03 | **No email channel in v1 — SMS, WhatsApp, in-app and push only** | Email penetration is low in the target market (`C-06` rationale); removing it deletes an entire delivery stack from scope; consciously accepted as a gap, not an oversight | `01-business-analysis/business-rules.md` `BR-NTF-01`; scope exclusions in `00-project-overview/project-scope.md`; open question tracked as `GAP-03` |
| D-04 | **Return approval SLA: vendor/admin decision within 48 hours, then auto-escalation to admin; inspection concludes within 72 h else auto-approve** | Unattended return requests are the main trust killer in marketplaces; escalation beats silence, and time-boxed auto-decisions keep the 17-state machine moving without support intervention | `../03-system-analysis/core/state-transitions.md` (RETURN_REQUESTED → RETURN_APPROVED), `BR-RET-05`, `../03-system-analysis/core/edge-cases.md` `EC-39`; KYC's parallel 48-h rule is `BR-VND-03` |
| D-05 | **Pagination split: cursor (keyset) for catalog/search feeds, activity streams and the audit log; offset only where page depth is bounded** | Cursor pages stay stable under concurrent indexing and append-heavy streams and avoid O(n) offset scans on 100M-row tables; offset remains acceptable for shallow admin lists | `../07-api/core/pagination.md` (mode table + rationale per endpoint family) |
| D-06 | **No additional MFA factor in v1 — password login plus OTP for registration, reset and sensitive changes only** | OTP already acts as a second factor on high-risk events; TOTP/hardware keys would add a secret store and recovery path the market does not require; the privileged-role gap is consciously tracked as `SEC-012` for the first post-launch review | `../09-security/core/authentication.md` §7 (decision), `C-07`, `C-06` |
| D-07 | **OTP delivery: SMS primary, automatic WhatsApp fallback; a failed send never falls back to any other channel (never email, never in-app display)** | Registration cannot be bypassed (`SEC-REQ-001`); a two-channel chain covers provider failure without inventing an insecure third path (`AC-IR003-*`) | `01-business-analysis/business-rules.md` `BR-NTF-03`; `../02-requirements/core/INT-REQ-003.md` |
| D-08 | **Bank-transfer top-ups are credited only after admin verification of the reference — no bank API in v1** | No bank API access exists in the market context; human verification keeps the credit path trustworthy and doubles as the fallback rail when mobile-wallet providers are down | `../02-requirements/core/INT-REQ-002.md`; `BR-PAY-04`; `../10-integrations/core/bank-transfer-topup.md` |
| D-09 | **Single support hub: in-app tickets (primary) answered by human agents, with resolutions executed through admin-console tooling — no AI chatbot, no email, no code changes for common issues** | One queue keeps every issue auditable end-to-end; admin tooling (verify top-up, freeze wallet, resolve dispute, unlock code lockout, KYC decisions, state override within `C-09`) makes support an operations capability (`NFR-020`) rather than a release dependency; auto-created escalation tickets carry the full order timeline so agents never re-collect context | `../12-non-functional/core/usability-and-support.md` §5; `FR-020` (out-of-scope note); scope exclusions in `00-project-overview/project-scope.md`; `AC-FR020-04` |
| D-10 | **UUID v7 primary keys generated in the application layer, and singular `snake_case` table/column naming** | UUID v7 needs no coordination across stateless replicas (`NFR-018`) and workers, stays index-local on 100M-row tables (`NFR-017`), and ranges well with composite `(id, created_at)` partition keys; singular table names keep entity file = table = Prisma `@@map` and avoid irregular plurals — CI asserts no v4 IDs enter tables | `08-database/README.md` §1 (naming) and §2 (ID strategy) |
| D-11 | **ERP/finance strategy: build in-platform (Option A) with a connector port reserved for a later self-hosted satellite (Option B); block placement starts inside `B07`+`B13` (no `B14` until size forces it); v1 department depth is core+ (accounts, sales, purchases, inventory snapshots, reports, periods)** | Keeps `C-18`/`C-21`/`C-22` untouched for v1 while the seam (ports/adapters, per `ADR-009`'s pattern) preserves a no-rework exit to Option B; extending existing blocks avoids a change-control event today, and core+ depth answers the sponsor's departmental requirement without Phase-2 merchant procurement | `plan-develop.md` §4 (`D2`, `D3`, `D11` approval 2026-09-28); operating model in `../03-system-analysis/core/erp-finance-departments.md` (`DOC-SA-011`); permission model in `../09-security/core/rbac.md` §11 |

## 3. Reserved for Future ADRs (from ADR-011)

Candidates parked so numbering stays collision-free (merged from DOC-ARCH-010 §4 and this domain's own backlog). Each becomes an ADR only when its trigger fires; until then no number is consumed.

| Candidate | Likely number | Trigger to write it |
|---|---|---|
| Multi-host deployment / orchestrator (requires formal `C-22` change) | ADR-011 | Single-host ceiling proven in load tests, or repeated host-level outages vs `C-26` (feeds RISK-019) |
| E-mail channel (if `GAP-03` resolves to "include") | ADR-012 | Product-owner decision + `BR-NTF-01` scope change |
| MFA / step-up for privileged roles | ADR-013 | Resolution of `SEC-012` (admin login factor ambiguity) |
| Cloud migration or managed-service adoption (vs `NFR-016` portability) | ADR-014 | Sponsor decision to leave self-hosted deployment |
| Search-as-a-service / managed Elasticsearch alternative | ADR-015 | RISK-007 relevance or capacity not solvable self-hosted |
| PostgreSQL read-replica topology | ADR-011+ | `NFR-018` stage S2 activated (`../12-non-functional/core/scalability.md`) |
| Table partitioning scheme | ADR-011+ | `NFR-017` growth thresholds approached |
| Multi-node Elasticsearch cluster topology | ADR-011+ | Single-node ES no longer meets `NFR-001` |
| CDN vendor / edge strategy beyond `DEP-08` | ADR-011+ | Edge configuration hardens in production |
| Push provider strategy (APNs/FCM vs aggregator) | ADR-011+ | Mobile push implementation begins (`FR-017`) |
| Outbox pattern formalization | ADR-011+ | Enqueue-after-commit races observed in practice |
| External delivery fleet API integration (vs the internal assignment engine) | ADR-011+ | A courier/fleet provider is contracted — v1 keeps the internal engine behind the delivery abstraction (`../03-system-analysis/core/system-boundary.md`, `INT-REQ-005`) |
| Subscription / tiered products and vendor plans (vs flat commission) | ADR-011+ | `BR-CAT-05` and `GAP-05` revisited — product types or commission tiers are formally extended (`01-business-analysis/business-rules.md`, `../02-requirements/core/FR-014.md`) |

**Numbering note:** the table shows relative order only; the actual number is always *the next free* ≥ 011 at time of writing (rule 3.4, DOC-DEC-001 §3).

## 4. Log Maintenance

1. Adding an ADR: append/extend §1, update `README.md` §5 index, update `04-architecture/architecture-decisions-reference.md` §1 status from RESERVED to ACCEPTED (it currently shows RESERVED — the index must be re-synced and version-bumped when this authoring lands), then run `../20-validation/core/consistency-audit.md`.
2. Superseding: new ADR takes the next free number; the old file flips to `SUPERSEDED` with a pointer; §1 keeps both rows.
3. Inline decisions (`D-NN`): edit the row where defined, bump the log version — promotion to ADR follows DOC-DEC-001 §4.
4. Never delete a row; statuses are `ACCEPTED`/`SUPERSEDED`/`REJECTED` only.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | §2 `D-11` added: ERP/finance strategy (in-platform + connector port, `B07`/`B13` placement, core+ department depth) — inline decision, no ADR (ADR-011 stays reserved for multi-host per §3) | `plan-develop.md` §8 approval implementation (session 007, `D2`/`D3`/`D11`) — decision recorded in the decision register, not copied anywhere else (SPE-05) |
