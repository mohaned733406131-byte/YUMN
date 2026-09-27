# memory — Durable Project Facts & Known-Defect Register (DOC-01)

Facts that must survive context resets. Anything richer is linked, never restated (SPE-01).

## 1. What yumn is (one line)

Multi-vendor e-commerce marketplace for Yemen — Arabic-first (RTL), **wallet-only** payments with
escrow, 6-digit code-confirmed delivery, custom-built modular monolith. Source:
[docs/00-project-overview/project-charter.md](docs/00-project-overview/project-charter.md).

## 2. Immutable facts (constraints — never violate, `docs/00-project-overview/project-constraints.md`)

| ID | Absolute |
|---|---|
| `C-01…C-05` | Wallet-only payments: no COD, cards, BNPL, crypto; top-up via m-Floos/OneCash/bank transfer only |
| `C-06`/`C-07` | Phone + OTP only (no email-primary, no social, no biometrics in v1) |
| `C-08` | JWT: 15-min access / 7-day single-use refresh |
| `C-09`/`C-10` | Exactly **17** order states; one master order + one sub-order per vendor |
| `C-11`/`C-12`/`C-13` | Return window per store policy; escrow hold **7 days**; stock reservation **15 min** |
| `C-14`/`C-15` | Order total 500–5,000,000 YER; cart ≤50 products / ≤10 units / ≤5 vendors |
| `C-16` | **No GPS** anywhere — 6-digit code confirmation instead |
| `C-17`/`C-18` | Domestic Yemen fulfillment; 100% custom build (no commerce platform) |
| `C-19`/`C-20`/`C-21`/`C-22` | PostgreSQL only; BullMQ only; monolith only; Docker Compose only (no Kubernetes) |
| `C-24` | Arabic-first RTL + English, only these two locales |
| `C-25`/`C-26` | 10,000 concurrent users; 99.99% availability, RTO ≤1 h, RPO ≤15 min |

Key numbers: VAT 15% on (subtotal − discount), shipping untaxed · commission 5–20% default 10% ·
escrow release = delivered + 7 days · payout 3–7 business days, min 1,000 YER · refund ≤3 business
days · KYC decision ≤48 h · inspection ≤72 h · OTP 6-digit/5-min/3-attempts.

## 3. Where truth lives (never copy, always reference)

| Concept | Authoritative file |
|---|---|
| Constraints / scope / actors | `docs/00-project-overview/` |
| Business rules (99) | `docs/01-business-analysis/business-rules.md` |
| Requirements (68) + ACs (253) | `docs/02-requirements/requirements-overview.md`, `acceptance-criteria.md` |
| Order/state behavior | `docs/03-system-analysis/state-transitions.md` |
| API contract (221 endpoints) | `docs/07-api/` |
| Database schema | `docs/08-database/` |
| Test cases | `docs/13-testing/test-cases/` |
| Naming | `docs/22-glossary/naming-conventions.md` |
| Implementation binding (commands/paths/budgets) | `senior-rules/RULES_HINTS.md` |
| Project rules | `senior-rules/YUMN_RULES.md` |

## 4. Known defects register (rule `SPE-03` forbids claiming these done)

> **2026-09-27:** canonical defect registers now live in `docs/20-validation/` (`CRIT-01…10`, `CT-01…20`, `HAL-01…13`, `GAP-01…12`, consistency findings 1–25) and `docs/21-completion/` (`TD-01…10`, `REC-01…15`). Rows below are this repo's durable session snapshot; status per row.

| # | Defect | Severity | Evidence | Disposition needed |
|---|---|---|---|---|
| D-01 | Docs domains `19-traceability/`, `20-validation/`, `21-completion/` are linked as live by `docs/README.md` but **did not exist** (~160 references) | HIGH | `docs/README.md` §2 rows 19–21 | **RESOLVED 2026-09-27** — all three authored (3 + 8 + 8 files); validator `PASS — structure healthy` |
| D-02 | `FR-015…FR-020` restate/renumber AC IDs owned by `acceptance-criteria.md`; 14 FR files omit their 5th AC | HIGH | `docs/02-requirements/functional/` vs `acceptance-criteria.md` | Repair FR files to reference (not rewrite) registry ACs before deriving tests |
| D-03 | `TC-104…TC-114` declared (114 total) but only `TC-001…TC-103` exist | MEDIUM | `docs/13-testing/README.md` §5 | Write the 11 or correct the declared count |
| D-04 | `BR-INV-01…05` cited by `TC-018/019/020`, defined nowhere (inventory rules live under `BR-CAT-*`) | MEDIUM | `docs/13-testing/test-cases/TC-018…020` | Define or re-point the references |
| D-05 | `GAP-07` cited in 5 files; canonical register listed only `GAP-01…06` | MEDIUM | `docs/00-project-overview/project-scope.md` vs risk register | **RESOLVED 2026-09-27** — GAP-07 adopted; register now `GAP-01…GAP-12` (`docs/20-validation/missing-information.md`) |
| D-06 | API vocabularies disagree with DB enums: product status (`INACTIVE` vs `DISABLED`), KYC (`IN_REVIEW` absent), notification categories (7 vs 4), notification `severity` (no column), refund/payout/dispute/return states, ledger `type` set | HIGH | `docs/07-api/` vs `docs/08-database/constraints-and-integrity.md` §2.3 | Reconcile via ADR **before coding** (rule `SPE-04`) |
| D-07 | API promises storage that doesn't exist: push devices, review reports, dispute evidence, support-ticket messages, vendor application, top-up proof file, payout account, deletion request | HIGH | endpoint files vs `docs/08-database/entities/` | Add entities or remove endpoints before implementation |
| D-08 | Repo path spellings conflict: `apps/api` + `apps/web` + `apps/mobile/**` (ops docs) vs root `api/` + `apps/web-*` + `apps/mobile-*` (frontend/backend docs) | MEDIUM | `docs/14-devops-infrastructure/ci-cd.md` vs `docs/05-frontend/frontend-architecture.md` | Canonical = frontend/backend tree; correct ops docs (adapter §4 already pins this) |
| D-09 | Queue-name registers diverge: 25 names in `06-backend/background-processing.md` vs 17 in `04-architecture/data-flow.md`, 1 shared | MEDIUM | both files | Merge into one register (authority: background-processing.md per glossary) |
| D-10 | `archdoc.md` at repo root is **0 bytes** yet cited as the governing structure spec; `archive/` cited but absent | MEDIUM | `docs/README.md` §1 | Restore the file or drop the citation |
| D-11 | ADR index `04-architecture/architecture-decisions-reference.md` claims "no ADR files exist" though ADR-001…010 are all present & ACCEPTED; three status vocabularies in use | LOW | index vs `docs/18-decisions/ADR/` | Re-sync the index |
| D-12 | Underspecified race: `COMPLETED → RETURN_REQUESTED` vs `COMPLETED → DISPUTED` precedence (funds outcome) | HIGH | `docs/03-system-analysis/state-transitions.md` | ADR before implementation (rule `ORD-08`) |
| D-13 | Master rule set self-inconsistency: `VERSION` = 2.0.0 while `CHANGELOG.md` shows `[2.1.0]` | LOW | `senior-rules/VERSION` | Reconcile at first session per GEN-08 |
| D-14 | `docs/README.md` declares 24 domains; only 21 existed (see D-01) | LOW | directory listing | **RESOLVED 2026-09-27** — 24 domains exist (see D-01) |

## 5. Hard operational reminders

- Nothing in `docs/` is `VERIFIED` — no implementation exists. `APPROVED` = analysis only.
- `DEP-05` (wallet providers) and `DEP-06` (SMS/WhatsApp) are **NOT STARTED** — they gate launch;
  `INT-REQ-003` is CRITICAL (no OTP ⇒ no registration).
- Money rules (`MNY-*`, `ESC-*`) outrank feature speed: `RISK-001` (wallet/ledger integrity) is CRITICAL.
- Run `python senior-rules/validators/validate.py .` after every implementation phase (AGENTS.md) — **`python3` is NOT available on this machine.**
