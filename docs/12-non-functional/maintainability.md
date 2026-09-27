---
document_id: DOC-NFD-005
title: Maintainability Detail — Standards, Test Pyramid, Docs-as-Code & Environment Parity
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-009, NFR-010, NFR-015, NFR-016, NFR-019, FR-018, DATA-REQ-005, INT-REQ-008]
related_documents: [DOC-NFD-001, DOC-NFR-009, DOC-NFR-010, DOC-NFR-016, DOC-AC-001, DOC-OVR-008, DOC-OVR-009]
---

# Maintainability Detail — Standards, Test Pyramid, Docs-as-Code & Environment Parity

Elaborates **NFR-009 (modularity & documentation), NFR-010 (testability) and NFR-016 (deployment portability)**. Statements live in `02-requirements/non-functional/`; this file adds the concrete standards, tool inventory, coverage split, parity evidence and cadences. Acceptance: `AC-NFR-009-*`, `AC-NFR-010-*`, `AC-NFR-016-*`.

## 1. Code Standards & Enforcement

| Standard | Rule | Enforced where |
|---|---|---|
| Language/lint | TypeScript strict everywhere; ESLint + Prettier with zero-warning CI on PRs | pre-commit + CI |
| Framework | NestJS backend, Next.js web, React Native apps — versions pinned in lockfiles (`C-18`, 100% custom build) | lockfile diff gate |
| Naming | blocks `b01-…b13`, modules `<block>.<entity>.<action>` queue keys (`BR-PLT-01`), `snake_case` DB, `camelCase` API | lint rules |
| Error handling | typed error envelopes (`DOC-AC-*` contract); no swallowed catches; every catch logs or rethrows with context | lint + review checklist |
| Secrets | never in code/images — env/secrets only (`SEC-REQ-007`) | secret scanner (e.g., gitleaks-class) in CI |
| Money | integer YER only (`BR-PAY-10`); no floating-point arithmetic on balances — CI rule greps for currency-typed floats | custom lint rule (`INFERENCE`) |
| Migrations | forward-only, reviewed like code, run identically per env (`DATA-REQ-005`) | migration dry-run job |

## 2. Module Boundary Enforcement (NFR-009 / `C-21`)

The system is a **modular monolith**: one deployable, 13 bounded modules (B01–B13), packages mapped per `DOC-OVR-009`.

| Mechanism | Rule | Gate |
|---|---|---|
| Dependency-cruiser (or eslint-boundaries) rules | `block/*` may import only from `shared/*` + own module; cross-block imports = error unless via declared public interface | CI, 0 violations |
| Public interface files | each block exposes `index.ts` (or `/internal` path) as its only legal surface; deep imports (`b03/orders/src/...`) banned | lint |
| Wallet/ledger isolation | only `b07` (or blocks in `related_blocks`) posts ledger entries; enforced by import rule + table-level DB grants (`DATA-REQ-007` style append-only) | CI + DB review |
| Database ownership | tables prefixed/tagged per block; no cross-block joins without interface-layer query (`INFERENCE`) | code review |
| Tests prove boundaries | a dependency-graph test asserts allowed edge set unchanged | CI |
| Physical single process (`C-21`) | boundaries are logical — splitting services would require an ADR (`18-decisions/`); this preserves `C-22` operations | documented |

## 3. Testability & Coverage Split (NFR-010)

| Layer | Target | What it covers | Canon |
|---|---|---|---|
| Unit (pure logic, no I/O) | **≥ 80%** lines of the modules under test | wallet math, cart rules, pricing/VAT, search scoring, RTL helpers | `AC-NFR-010-01`, `AC-S-08` |
| Unit — **payments/ledger** | **≥ 95%** (tests run **offline**, no network) | double-entry, escrow release/refund, callbacks | `AC-NFR-010-01` |
| Unit — **auth** | **≥ 90%** | OTP rules (cooldown/attempt/resend), token issue/verify, roles | `AC-NFR-010-01` |
| Integration | every block's DB/Redis/queue interactions via testcontainers-or-Compose harness | saga steps, outbox, BullMQ retry→DLQ, migrations | `AC-NFR-010-02` |
| E2E (Playwright/RN) | P1 flows only (register → order → wallet → tracking) | cross-browser, both locales | `AC-NFR-015-*` |

Operational rules:

- Business logic must be **importable and testable with zero network/DB** (`NFR-010` statement) — all I/O behind injected ports/adapters.
- Suite budgets (keep CI < 10 min, `INFERENCE`): unit < 90 s, integration < 5 min, E1E smoke < 3 min.
- **Flaky policy**: a test failing 2× non-reproducibly is quarantined + ticketed same day; quarantine list reviewed weekly; 0 items at release.
- Coverage measured per changed-lines too: PRs must not reduce module coverage (CI diff gate).

## 4. Documentation-as-Code (NFR-009 second half)

| Rule | Detail |
|---|---|
| This documentation set (`00…21`) is the primary artifact | every module owns entries in `00-project-overview/project-context.md` (B01–B13, S1–S5 decomposition) and `01-business-analysis/` domain docs |
| ADRs for structural decisions | `18-decisions/ADR/` — adoption of sharding, multi-host HA, service split all require ADRs (referenced from `DOC-NFD-003` §5.3, `DOC-NFD-004` §3) |
| Runbooks accompany features | anything alerting (`DOC-NFD-006`) ships with a runbook section; top-10 incidents per `NFR-020` |
| Freshness audit | quarterly scan flags docs untouched > 90 days that reference changed code paths; owner updates or marks `draft`; **0 broken relative links** at audit end (`AC-NFR-009-02`) |
| In-code docs | README per package (purpose, run, test, env vars); OpenAPI generated from Nest decorators and diffed in CI |
| Evidence tag | docs carry `VERIFIED`/`INFERENCE`/`INSUFFICIENT EVIDENCE` per root README §8 |

## 5. Environment Parity & Portability (NFR-016 / `C-22`)

| Parity axis | Rule | Evidence |
|---|---|---|
| Images | same release tag → **identical image digests** in dev/staging/prod; 0 env-specific rebuilds | CI digest-comparison job (`AC-NFR-016-01`) |
| Config | **100% env vars/secrets**; 0 host-specific config baked into images (`SEC-REQ-007`) | config audit in dependency script |
| Cloud lock-in | **0** cloud SDKs/managed services in runtime graph (`@aws-sdk/*`, `@google-cloud/*`, `@azure/*` banned); storage only via S3-compatible MinIO (`DEP-07`); provider adapters keep integrations swappable (`INT-REQ-008`) | dependency audit (`AC-NFR-016-02`) |
| Bring-up | fresh Docker Engine ≥ 24 host → healthy stack + green smoke in **≤ 30 min** from `git clone` + `docker compose up` | timed drill in `15-deployment/` (`AC-NFR-016-01`) |
| Relocation | portability drill on a second, differently-provisioned host with **zero code changes**: pre-launch, then annually | drill record |
| Migrations | identical migration artifacts per env (`DATA-REQ-005`) | migration job output |

## 6. Change & Release Discipline

| Practice | Rule |
|---|---|
| Branching | trunk-based with short-lived branches; every PR: lint + unit + integration + coverage-diff + dependency-boundary + secret-scan |
| Review | 1 approval minimum; payments/auth/ledger paths require 2 approvals (`INFERENCE`) |
| Versioning | semver on images/tags; changelog derived from merged PR labels |
| Backward compatibility | breaking API changes need versioned routes or coordinated FE change (`10-integrations`/`07-api` contract diff) |
| Dependency updates | Renovate/Dependabot-class weekly PRs; security patches within SLA (`DOC-NFD-007` §8) |
| Feature flags | env-gated flags for risky flows (checkout, wallet) enabling kill without rollback — ops-owned, documented (`INFERENCE`) |

## 7. Lead Time & Cadence (operationalizing `AC-NFR-009-01`)

| Signal | Target/trigger |
|---|---|
| PR → production | < 2 days median (goal, `INFERENCE`); blocking failures raise a ticket within 1 business day |
| Breaking change detection | CI contract-diff job fails the build → same-day ticket |
| Release cadence | weekly routine; hotfixes any time; every release passes the full gate set (`AC-XCUT-01`), including NFR sweeps `AC-S-05…AC-S-10` |
| Module split recommendation | raised when a block changes > 2×/week with > 30% overlap onto another block (heuristic, `INFERENCE`) — recorded as ticket, ADR only if adopted |
| Doc/ADR freshness | quarterly audit (§4) — stale docs escalate to owner, not auto-deleted |

## 8. Verification Hooks

| Detail | Feeds AC |
|---|---|
| §2 boundary rules = 0 violations | `AC-NFR-009-01` (boundaries, coupling) |
| §4 freshness audit = 0 broken links, stale set cleared | `AC-NFR-009-02` (docs current) |
| §3 coverage report per build (80/95/90) | `AC-NFR-010-01`, `AC-S-08` |
| §3 offline unit proof for wallet/auth logic | `AC-NFR-010-01` |
| §3 integration suite green in CI | `AC-NFR-010-02` |
| §5 digest parity + 30-min drill + 0 lock-in findings | `AC-NFR-016-01`, `AC-NFR-016-02` |
| §6 every release passes gates | `AC-XCUT-01` |

## 9. Out of Scope Here

Multi-host HA decisions (see `DOC-NFD-004` §3 residual-risk note), test execution plans (`13-testing/`), infrastructure sizing (`14-devops-infrastructure/`), release pipeline wiring (`15-deployment/`), debt tracking (`21-completion/`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
