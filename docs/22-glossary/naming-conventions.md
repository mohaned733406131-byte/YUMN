---
document_id: DOC-GL-003
title: Naming Conventions
category: 22-glossary
status: approved
version: 1.5
created: 2026-09-26
updated: 2026-09-29
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-ROOT-001, DOC-GL-001, DOC-GL-002, DOC-OVR-002, DOC-DB-001, DOC-API-002, DOC-BE-005, DOC-TPL-001]
---

# Naming Conventions — How Artifacts Are Named in yumn (DOC-GL-003)

The author-facing authority for **how things are named** across all 24 documentation domains: files, identifiers, code, database objects, API surface, queues/events, git branches, locales, dates and numerals.

**Precedence.** `root README §5 (DOC-ROOT-001)` issues the canonical ID patterns; the domain that owns a registry owns its IDs (e.g. `08-database/README.md` §1 for tables). This document is the single navigable index of those rules plus the rules that span domains. It must never contradict its cited sources; if it appears to, the cited source wins and the clash is logged in `20-validation/contradiction-audit.md`. Rules with no canonical source are tagged `INFERENCE` and flagged for the owning domain to confirm.

Two global rules override everything below (root README §5):

1. **Filenames:** `lowercase-kebab-case.md`. Never `final.md`, `latest.md`, `new-final.md`.
2. **Identifiers:** `UPPERCASE-WITH-DASHES` (`FR-013`, `BR-PAY-04`), fixed zero-padding per series, case-sensitive, never reused.

---

## 1. Documentation Files & Directories

| Kind | Convention | Examples / notes |
|---|---|---|
| Directories | Two-digit numeric prefix + kebab-case topic: `NN-topic/` | `07-api/`, `22-glossary/`, `13-testing/` |
| Domain index | Every domain directory carries a `README.md` that is its index + register of internal IDs | `17-risk-management/README.md` lists its DOC IDs and file table |
| Ordinary documents | `lowercase-kebab-case.md`, descriptive singular noun phrase | `state-transitions.md`, `security-findings.md`, `risk-register.md` |
| **Exception — ID-named files** | When the file's primary identifier *is* the content, the filename is that ID | `FR-013.md`, `UC-007.md`, `TC-021.md` (root README §5, filename exception) |
| Use cases / workflows | ID-named (`UC-NNN.md`) vs prefixed sequence (`workflow-NNN.md`) | `use-cases/UC-040.md`; `workflows/workflow-012.md` (DOC-WF-001 reserves `WF-NNN` for the concept, `README.md` for the index) |
| Entity documents | `entities/<table>.md` — file name **is** the table name (singular `snake_case`, not kebab) | `entities/wallet_transaction.md` → `DB-011` (`08-database/README.md` §1) |
| Endpoint documents | One file per group, plural resource noun | `endpoints/orders.md`, `endpoints/wallet.md` |
| Filled vs template files | Templates live only in `23-templates/` and contain `<angle-bracket placeholders>`; no other file may contain them | `23-templates/test-case-template.md` vs `13-testing/test-cases/TC-001.md` |
| Cross-links | Relative Markdown links from the linking file; reference by **ID** in prose, never by copied definition | `[terminology.md](terminology.md)`, "see `BR-ESC-02`" |
| Banned names | version/position words instead of meaning | `final.md`, `latest.md`, `draft2.md`, `Untitled.md`, `copy-of-*.md` |
| Process folders (not domains) | `phases/` holds `README.md` + `<slug>/_index.md` + the 16 CORE-03 artifacts (kebab-case); `sessions/` holds `README.md` + `session-NNN-<slug>.md` (zero-padded, sequential, never reused) | `phases/analysis/implementation-plan.md`, `sessions/session-005-rules-compliance-audit.md` (CORE-03; `senior-rules/core/02` §2.1); IDs `DOC-PHA-NNN` / `DOC-SES-NNN` |

> `INFERENCE` (filenames for entities/endpoints/workflows): stated here as a rule because it is the *observed uniform* across those directories; the owning documents define content, not the extension mechanics.

## 2. Frontmatter & Document Rules (every file)

| Rule | Value | Source |
|---|---|---|
| Required block | `document_id`, `title`, `category` (= directory name), `status`, `version`, `created`, `updated`, `author`, `source_of_truth`, `related_requirements`, `related_documents` | root README §7 |
| ID in frontmatter | `DOC-<CAT>-NNN`, e.g. `DOC-GL-003`; `<CAT>` is the domain's registered short code (`ROOT OVR BA REQ SA ARCH BE API DB DBE RSK GL TPL TST CMP VAL TRC PHA SES …` — `PHA`/`SES` registered 2026-09-28 for `phases/`/`sessions/`) | root README §5 |
| Status vocabulary | `DRAFT · UNDER_REVIEW · APPROVED · IMPLEMENTED · VERIFIED · SUPERSEDED · DEPRECATED · REJECTED` (all caps in values; frontmatter uses lowercase `approved`) | root README §6 |
| `source_of_truth` | `true` only for the authoritative document of its concept; registries of supporting detail (entity files, TC files) use `false` | root README §4, §7 |
| Change history | Every file ends with `## Change History` table `| Version | Date | Change | Reason |`; version bumps on every change, never silent edits | root README §9.1–2 |
| Evidence tags | `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`; severities `CRITICAL…INFORMATIONAL`; confidence `HIGH/MEDIUM/LOW` | root README §8 |
| Dates in prose/frontmatter | ISO `YYYY-MM-DD`; timestamps in API/data `ISO-8601 UTC` with `Z` | `07-api/api-conventions.md` §5 |
| Placeholders | `<lower-case-with-hyphens>` — allowed **only** inside `23-templates/` | DOC-TPL-001 §2 |

## 3. Identifier Series (master table)

Allocation is **append-only and sequential with fixed width**; the *Defined in* column is the only place an ID may be minted. Never renumber, never reuse, never change a pattern locally.

| Kind | Pattern | Example | Width | Defined in | Allocation (2026-09-26) |
|---|---|---|---|---|---|
| Documents | `DOC-<CAT>-NNN` | `DOC-GL-003` | 3 | each file's frontmatter | continuous per domain |
| Constraints | `C-NN` | `C-09` | 2 | `00-project-overview/project-constraints.md` | `C-01…C-26` |
| Objectives | `OBJ-NN` | `OBJ-11` | 2 | `00-project-overview/project-objectives.md` | append-only |
| Assumptions | `ASM-NN` | `ASM-14` | 2 | `00-project-overview/assumptions.md` | `ASM-01…ASM-15` |
| Dependencies | `DEP-NN` | `DEP-06` | 2 | `00-project-overview/dependencies.md` | `DEP-01…DEP-12` |
| Stakeholders | `STK-NN` | `STK-15` | 2 | `00-project-overview/stakeholders.md` | `STK-01…STK-15` |
| Business objectives | `BO-NN` | `BO-12` | 2 | `01-business-analysis/business-objectives.md` | `BO-01…BO-12` |
| Actors | `ACT-NN` | `ACT-03` | 2 | `00-project-overview/actors-and-roles.md` | `ACT-01…ACT-07` |
| Business processes | `BP-NN` | `BP-08` | 2 | `01-business-analysis/business-processes.md` | `BP-01…BP-15` |
| Functional requirements | `FR-NNN` | `FR-013` | 3 | `02-requirements/functional/` | `FR-001…FR-020` |
| Non-functional requirements | `NFR-NNN` | `NFR-020` | 3 | `02-requirements/non-functional/` | `NFR-001…NFR-020` |
| Security requirements | `SEC-REQ-NNN` | `SEC-REQ-007` | 3 | `02-requirements/security/` | `SEC-REQ-001…012` |
| Data requirements | `DATA-REQ-NNN` | `DATA-REQ-008` | 3 | `02-requirements/data/` | `DATA-REQ-001…008` |
| Integration requirements | `INT-REQ-NNN` | `INT-REQ-005` | 3 | `02-requirements/integration/` | `INT-REQ-001…008` |
| Business rules | `BR-<DOMAIN>-NN` | `BR-ESC-02` | 2 | `01-business-analysis/business-rules.md` | 15 domains (`AUTH CAT VND CRT ORD PAY ESC SHP RET NTF PRM REV PLT FIN INV`), 104 rules |
| Use cases | `UC-NNN` | `UC-026` | 3 | `01-business-analysis/use-cases/` | `UC-001…UC-210` (42 issued at session-010 start; `UC-043…UC-210` allocated for minting in session 010) |
| Workflows | `WF-NNN` | `WF-003` | 3 | `01-business-analysis/workflows/` | `WF-001…WF-012` |
| Blocks | `B01…B13` | `B07` | 2 (no dash) | `00-project-overview/project-context.md` | 13 blocks |
| API endpoints | `API-<GROUP>-NNN` | `API-WAL-002` | 3 | `07-api/endpoints/` | 14 groups (`ATH USR VND CAT SRC CRT ORD WAL SHP RET NTF CNT ANL ADM`), 221 endpoints |
| Database entities | `DB-NNN` (+ table name) | `DB-011` | 3 | `08-database/entities/` | `DB-001…DB-018` |
| Test cases | `TC-NNN` | `TC-031` | 3 | `13-testing/test-cases/` | allocation locked `TC-001…TC-114` (`13-testing/README.md` §5); files added incrementally — count live in `13-testing/test-cases/` |
| Constraint tests | `TST-CON-NN` | `TST-CON-09` | 2 | `13-testing/constraint-tests.md` | `TST-CON-01…26` (one per constraint) |
| Acceptance criteria | `AC-<REQID>-NN`, `AC-S-NN`, `AC-XCUT-NN` | `AC-FR013-01`, `AC-S-14` | 2 | `02-requirements/acceptance-criteria.md` | see §3.1 |
| Risks | `RISK-NNN` | `RISK-006` | 3 | `17-risk-management/risk-register.md` (DOC-RSK-002) | `RISK-001…RISK-024` |
| Decisions / ADRs | `ADR-NNN` | `ADR-011` | 3 | `18-decisions/ADR/` (index: `04-architecture/architecture-decisions-reference.md`) | `ADR-001…ADR-010` reserved; new from `ADR-011` |
| Security findings | `SEC-NNN` | `SEC-011` | 3 | `09-security/security-findings.md` | `SEC-001…SEC-015` |
| Gaps | `GAP-NN` (issued) / `GAP-NNN` (root README §5) | `GAP-03` | 2 | `20-validation/missing-information.md` | `GAP-01…GAP-12` — see §3.2 |
| Validation audits | `AUD-NN` | `AUD-01` | 2 | `20-validation/README.md` §2 | `AUD-01…AUD-07` — `VERIFIED`: series minted when `20-validation/` was authored (2026-09-27), per DOC-TPL-011 |
| Data-quality rules | `DQ-NN` | `DQ-12` | 2 | `16-data/data-quality.md` | append-only |
| Threat-model entries | `TM-NN` | `TM-04` | 2 | `09-security/threat-model.md` | append-only |
| Reconciliation jobs | `J<N>` | `J1`, `J2` | 1 | `06-backend/background-processing.md`, `16-data/data-quality.md` | `J1…J12` |
| Queues | `{block}.{entity}.{action}` | `b07.escrow.release` | — | `06-backend/background-processing.md` (`BR-PLT-01`, `C-20`) | CI enforces the pattern |
| Domain events | PascalCase past tense | `OrderConfirmed` | — | `06-backend/background-processing.md` | payload = IDs only |
| API roles | `SCREAMING_SNAKE` | `SUPER_ADMIN` | — | `07-api/api-conventions.md` §4 | `CUSTOMER VENDOR COURIER ADMIN SUPER_ADMIN MODERATOR` (+ `SYSTEM`, non-interactive) |
| Error codes | `SCREAMING_SNAKE` | `STATE_CONFLICT` | — | `07-api/error-model.md` §4 catalog | catalog-closed |

### 3.1 Acceptance-criterion shapes

Canonical family (root README §5): `AC-<REQID>-NN` — e.g. `AC-SR004-01` — and `AC-S-NN`. Issued shapes in canon:

| Shape | Meaning | Example |
|---|---|---|
| `AC-FRnnn-nn` | AC on a functional requirement | `AC-FR013-01` |
| `AC-NFR-nnn-nn` | AC on a non-functional requirement | `AC-NFR-005-01` |
| `AC-SRnnn-nn` | Security-requirement criteria (sub-numbered since `DOC-AC-001` v1.1) | `AC-SR004-01`, `AC-SR005-01`, `AC-SR007-02` |
| `AC-DRnnn-nn`, `AC-IRnnn-nn` | Data / integration requirement criteria | `AC-DR006-02`, `AC-IR003-01` |
| `AC-S-NN` | System-level success criterion | `AC-S-14`, `AC-S-22` |
| `AC-XCUT-NN` | Cross-cutting criterion | `AC-XCUT-01` |
| `AC-UCnnn-nn`, `AC-WF-NNN-NN` | Use-case / workflow criteria (observed in `01-business-analysis/`) | `AC-UC001-01`, `AC-WF-012-01` |

### 3.2 Known deviations to respect (do not "fix" locally)

| Deviation | Where | Handling |
|---|---|---|
| `GAP-NNN` pattern vs two-digit issuance (`GAP-03`) | root README §5 vs `20-validation/`, `17-risk-management/` | Use the issued form `GAP-03`; pattern width is a documentation defect logged for root README |
| `AC-SR-nnn` (retired) vs `AC-SRnnn-nn` | pre-v1.1 registry vs requirement files | Resolved by `DOC-AC-001` v1.1 (2026-09-26) — cite only the sub-numbered `AC-SRnnn-nn`/`AC-DRnnn-nn`/`AC-IRnnn-nn` shapes; the flat `AC-SR-nnn` spelling is retired and must not be reintroduced |
| Stray flat AC IDs (`AC-SR-16`; `AC-DR-004-03`, since corrected) | `15-deployment/production-readiness.md`; historic `02-requirements/` drafts | Not present in the `DOC-AC-001` v1.1 registry — cite the registered `AC-SRnnn-nn`/`AC-DRnnn-nn` form or log the clash in `20-validation/contradiction-audit.md` |
| Security finding cited as `A-07` | `09-security/security-findings.md` (SEC-008) | The register uses `ASM-*`/`SEC-*`; `A-07` is undefined — cite `ASM-07` intent or log in `contradiction-audit.md` |
| "four surfaces" vs "five surfaces" | `C-09`/`FR-001` vs `13-testing/`/`ADR-008` | Terminology *Surface* row resolves wording; don't mint a new count |

## 4. Code Naming (`INFERENCE` for items marked ⚠)

| Kind | Convention | Example | Source |
|---|---|---|---|
| Service/deployable names | kebab-case | `api`, `worker`, `postgres` | `04-architecture/README.md` (✓) |
| Module directories (B-blocks) | kebab-case mirroring block slug | `b07-wallet/` | ⚠ observed pattern, confirm in `18-decisions/ADR/` |
| Classes / services / Nest modules | PascalCase | `EscrowService`, `OtpModule` | ⚠ `INFERENCE` (event names `OrderConfirmed` are canon PascalCase) |
| Functions / variables / DTO fields | camelCase; API DTO fields exactly as `error-model`/`api-conventions` name them | `idempotencyKey`, `subOrderIds` | ⚠ `INFERENCE` |
| Constants / env vars | SCREAMING_SNAKE | `YUMN_JWT_SECRET` — read at runtime only, `${VAR}` in Compose, no literals | env discipline ✓ (`SEC-REQ-007` R1, `C-22`); the casing itself ⚠ |
| Test files | mirror source name + spec suffix | `escrow.service.spec.ts` | ⚠ `INFERENCE` (`13-testing/` owns *what* is tested) |
| Secrets | never appear in any name or file; only env/secrets manager | — | `09-security/secrets-management.md` (✓) |

## 5. Database Naming (binding — `08-database/README.md` §1)

| Kind | Convention | Example |
|---|---|---|
| Schemas | `b01…b13`, one per block | `b07.wallet` |
| Tables | **singular** `snake_case` | `sub_order`, `wallet_transaction` (reserved words `user`, `order` quoted in DDL) |
| Columns | `snake_case`; FK `<entity>_id`; timestamps `*_at` (`timestamptz`, UTC); booleans `is_*`/`has_*` | `buyer_user_id`, `released_at`, `is_frozen` |
| Money | integer YER with `_yer` suffix | `price_yer`, `balance_yer`, `amount_yer` |
| Primary keys | `id uuid` (UUID v7, app-generated); partitioned tables add `created_at` composite | `08-database/README.md` §2 |
| Indexes / constraints | `idx_<table>_<cols>`, `uq_<table>_<cols>`, `ck_<table>_<rule>`, `fk_<table>_<column>` | `fk_sub_order_order_id` |
| Enums | snake_case **type**, `SCREAMING_SNAKE_CASE` **values** | `order_state = 'OUT_FOR_DELIVERY'` |
| Soft delete / append-only | `deleted_at` where soft; append-only tables have `created_at` only, no `updated_at` | `wallet_transaction`, `audit_log` |
| Entity doc file | `entities/<table>.md` with `entity_id: DB-NNN` | `entities/return_request.md` |

## 6. API Naming (`07-api/api-conventions.md`)

| Kind | Rule | Example |
|---|---|---|
| Base path | `/api/v1` under `https://api.yumn.ye`, never locale-prefixed | breaking change ⇒ `/api/v2`, v1 lives ≥6 months |
| Resources | lowercase kebab-case **plural** nouns | `/orders`, `/support/tickets` |
| Ownership prefixes | vendor ⇒ `/store/...`, admin ⇒ `/admin/...`, customer ⇒ root | `/store/orders/{id}/confirm` |
| Nesting | max 2 levels; deeper via query params / linked IDs | — |
| Verbs | nouns in paths; actions via method or terminal POST segment | `POST /orders/{id}/confirm` |
| IDs | lowercase opaque UUID in path; slugs for public reads | `/products/{slug}` |
| Error codes | `SCREAMING_SNAKE_CASE` from the closed catalog | `409 IDEMPOTENCY_CONFLICT` |
| Header names | HTTP canonical casing | `Authorization`, `X-Session-Id`, `Accept-Language` |
| JSON field names | camelCase; money fields `*Amount`/`price`/`balance`/`total` as integers; timestamps end `At` | `2026-09-26T14:03:22Z` |
| Endpoint IDs | `API-<GROUP>-NNN` per group file | `API-WAL-002` |

## 7. Queues, Jobs & Events (`06-backend/background-processing.md`)

- Queue: **`{block}.{entity}.{action}`** — `b02.inventory.expire`, `b07.escrow.release`, `b13.platform.webhook.send` (lowercase, dot-separated; CI check per `BR-PLT-01`).
- Domain event type: **PascalCase past tense** — `OrderConfirmed`, `OtpRequested`, `WalletCredited`; payload carries **IDs only**, never amounts or PII.
- Job/reconciliation identifiers: `J1` … `J12` (allocation: `06-backend/background-processing.md`, `16-data/data-quality.md`).
- Retries: 3× exponential backoff → **DLQ** + alert; job names never encode secrets.

## 8. Frontend, Routing & i18n (`05-frontend/`, `11-ui-ux/`)

| Kind | Convention | Example | Source |
|---|---|---|---|
| Route segments | lowercase kebab-case only | `/orders/UC-…` → `/account/returns` | `05-frontend/routing.md` (✓) |
| i18n keys | `feature.section.key` dotted, camelCase leaf | `checkout.review.vatLabel` | `05-frontend/internationalization.md` (✓) |
| Locale codes | exactly `ar` (default, RTL) and `en` (LTR); formatting locale `ar-YE` | `Accept-Language: ar \| en` | `C-24`, `11-ui-ux/localization.md` |
| CSS physical props | banned; logical `ms/me/ps/pe` only | `padding-inline-start` | `05-frontend/rtl-and-styling.md` (enforced by CI lint) |
| UI term strings | canonical term from `terminology.md` in both locales | "Customer" ⇒ `عميل` | DOC-GL-002 |

## 9. Git Branches & Commits

| Kind | Convention | Example | Source |
|---|---|---|---|
| Schema/PR branches | `feat/<ticket>` — one schema change set per PR | `feat/FR-013-topup-limits` | `08-database/migrations-and-evolution.md` (✓ for migrations) |
| Other branches | `feat/<ID>-short-desc`, `fix/<ID>-short-desc`, `docs/<topic>` | `feat/UC-017-checkout-idempotency`, `fix/RISK-006-otp-fallback` | ⚠ `INFERENCE` — no canon repo standard exists yet; proposed so IDs stay greppable in history |
| Commits | imperative subject referencing the governing ID where relevant | `feat(WAL): enforce top-up cap (BR-PAY-04)` | ⚠ `INFERENCE` — no canon commit standard; register the final rule in `18-decisions/ADR/` when the implementation repo starts |
| Never | force-push to main, commit secrets, `.env` literals | — | `SEC-REQ-007`, `C-22` (✓) |

## 10. Dates, Numbers & Money

| Surface | Rule | Example |
|---|---|---|
| API/storage timestamps | ISO-8601 **UTC** with `Z`; field names end `At` | `2026-09-26T14:03:22Z` |
| UI display time zone | `Asia/Aden` (UTC+3), single display zone | `INFERENCE` (terminology row *Asia/Aden*) |
| Documents (frontmatter) | `YYYY-MM-DD` | `created: 2026-09-26` |
| Money transport/storage | integer YER, no floats, no separators; DB columns `_yer`, API fields integers | `15000` ⇒ `15,000 YER` (en) / `١٥٬٠٠٠ ر.ي` (ar) |
| Digits in code/DB/API | **Western** `0-9` always | `balance_yer = 15000` |
| Digits in `ar` UI | **Arabic-Indic** `٠-٩` via `Intl.NumberFormat('ar-YE')` | `١٥٬٠٠٠ ر.ي` |
| Dates in `ar` UI | Gregorian via `Intl`, `ar-YE` formatting | — |
| Phone numbers | stored/transported as strings matching `^7[0-9]{8}$` (Yemeni mobile, no `+967` in the raw value) | `731234567` (`BR-AUTH-01`, `SEC-REQ-001` R3) |

## 11. Naming Disambiguation

Pairs and clusters that are routinely confused. The glossary row (DOC-GL-002) is authoritative for meaning; this section is the usage rule for **names** — IDs, filenames, API paths, table names, prose.

| Cluster | Say / use | Means | Do not use for this | Where the distinction bites |
|---|---|---|---|---|
| Vendor vs Store vs Seller | **Vendor** = actor `ACT-02`, tables/users with the vendor role; **Store** = the vendor's storefront entity (slug, branding, zones; `DB-003`, `BR-VND-01`) and the API ownership prefix `/store/...` (vendor-owned surface, `07-api/api-conventions.md` §2); **Seller** is a **disallowed synonym** | Vendor = who, Store = what they own / their API scope | "Seller"/"merchant" anywhere in documents (only inside quotations of external text); never name a table `seller` or a route `/sellers/...` | `00-project-overview/actors-and-roles.md`, `07-api/api-conventions.md`, `08-database/entities/` |
| Courier vs Delivery Provider | **Delivery Provider** = canonical actor `ACT-03` (role `COURIER`); **Courier** = accepted short form in prose only | Who physically moves the package; same person in both words | Never two different entities; never use "courier" as a company name — an external logistics **company** is an *integration* (`INT-REQ-005`), not ACT-03 | terminology rows *Delivery provider*/*Courier*, `07-api` role `COURIER` |
| Master order vs Sub-order | **Master order** = one per checkout (`orders` / `DB-008`): payment, escrow funding, buyer timeline, master total = Σ sub-orders; **Sub-order** = per-vendor slice (`sub_order`): fulfillment, commission, escrow release, payout, drives the 17-state machine | Grouping level of the order hierarchy (C-10, `BR-ORD-02`) | Never "order" alone when the level matters — qualify it; never put vendor-scoped state on the master or payment state on a sub-order | terminology rows *Master order*/*Sub-order*, `DOC-SA-010` §4 |

Author rule: pick the term from the left column, keep it identical across `ar`/`en` UI strings (terminology `Arabic` column), IDs and links. If new jargon appears, add the glossary row first (checklist item 4), then name things after it.

## 12. Author's Pre-Flight Checklist

Before adding a file, ID, table, endpoint or queue:

1. Filename `lowercase-kebab-case.md` — unless it is an ID-named file (`FR/UC/TC`) or `entities/<table>.md`.
2. Frontmatter complete, `document_id` fresh from the domain's register, `category` = directory name.
3. New ID? Mint it **only** in its *Defined in* registry, next number, same width.
4. New term? Add the row to `terminology.md` first (DOC-GL-001 §2.2).
5. References cite IDs, not copies of definitions (root README §4).
6. Every claim tagged `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`; silence ⇒ gap, not invention.
7. Changed an approved doc ⇒ bump `version` + Change History row + propagate (root README §9).
8. Suspected canon clash ⇒ `20-validation/contradiction-audit.md`, never a silent local fix.

Enforcement points in canon: CI lint for RTL/logical CSS (`05-frontend/rtl-and-styling.md`), CI check that every queue matches `BR-PLT-01` (`06-backend/background-processing.md` §Test checklist), validation audits in `20-validation/`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-27 | `AUD-NN` row → `VERIFIED` (minted in `20-validation/README.md` §2); gap range → `GAP-01…GAP-12`; short-code list gains `VAL`, `TRC` | `19-traceability/`, `20-validation/`, `21-completion/` authored — pending registrations executed (root README §9) |
| 1.2 | 2026-09-27 | §7 queue example corrected: `b03.platform.webhook.send` → `b13.platform.webhook.send` (matches the register) | `REC-06`/`TD-07` pay-down — closes `CT-05`/consistency finding 17 (`CHK-25`) |
| 1.3 | 2026-09-28 | §1 process-folder naming row (`phases/`, `sessions/`); §2 short codes gain `PHA`, `SES` | SES-01/DOC-02 remediation — `docs/sessions/` + `docs/phases/` created, IDs registered (SPE-05, session 005) |
| 1.4 | 2026-09-28 | §3 `BR` row: 14 → **15 domains** (+`INV`), 99 → **104 rules** | `CRIT-06`/`HAL-04` pay-down (session 008) — `business-rules.md` v1.1 registered `BR-INV-01…05`; ID-series allocation row kept in sync (SPE-05) |
| 1.5 | 2026-09-29 | §3 `UC` row: allocation `UC-001…UC-040` → **`UC-001…UC-210`** (42 issued + `UC-043…UC-210` allocated; also fixes the stale `…UC-040` range) | Owner directive session 010 (`prompt-010.md` §1): full portal use-case coverage — change control before minting (SPE-05, GEN-03) |


