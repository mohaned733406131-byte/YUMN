---
document_id: DOC-TST-001
title: 13 Testing — Domain Overview & Test Case Index
category: 13-testing
status: approved
version: 1.3
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-TST-002, DOC-TST-003, DOC-TST-004, DOC-TST-005, DOC-TST-006, DOC-AC-001, DOC-OVR-011]
---

# 13 — Testing

**Verification domain for the yumn platform.** Testing answers one question for every claim made elsewhere in `docs/`: *how do we know it works?* This README is the domain index; the methodology's Verification Strategy (§47) is expanded in [testing-strategy.md](core/testing-strategy.md).

Scope: all five surfaces (customer web, vendor panel, admin console, customer mobile, courier mobile), the NestJS modular monolith (C-21), background workers, and the eight external integrations — against 73 requirements, 111 business rules, 26 constraints, and 273 acceptance criteria.

---

## 1. Goals & Quality Gates

Testing exists to move requirements from `IMPLEMENTED` to `VERIFIED` with evidence, never with assertion. Every test activity in this domain feeds one of the gates defined in `../21-completion/core/quality-gates.md`:

| Gate | Question | Evidence this domain produces | Canon |
|---|---|---|---|
| G-TEST-1 | Are all FRs covered by passing tests? | 114 TCs mapped to FR families; traceability with 0 gaps | `AC-S-01`, `AC-S-03` |
| G-TEST-2 | Do all 26 constraints hold? | Constraint register 26/26 PASS | `AC-S-02`, `C-01…C-26` |
| G-TEST-3 | Is quality inside budget? | Coverage report, defect query, regression timing | `AC-S-07`, `AC-S-08`, `AC-S-09` |
| G-TEST-4 | Are SLOs met under load? | k6 reports (10,000 concurrent, 30 min) | `AC-S-05`, `C-25` |
| G-TEST-5 | Is the platform safe? | SAST/DAST/dependency scans, authz matrix | `AC-S-12`, `AC-S-13`, `AC-S-16` |
| G-TEST-6 | Is it usable by everyone, in Arabic first? | axe reports, RTL visual regression | `AC-S-10`, `AC-S-11` |
| G-TEST-7 | Is it operable? | DR drill, alert drill, rollback rehearsal | `AC-S-17`, `AC-S-18`, `AC-S-20` |

No gate is passed by opinion; each requires a report, dashboard export, or drill record referenced from the relevant test artifact.

## 2. Test Pyramid (summary)

```text
            ┌────────────┐
            │   k6 / DAST│   scheduled + pre-release (perf, security)
        ┌───┴────────────┴───┐
        │  E2E (Playwright,   │  critical journeys only, per-surface
        │  Maestro, UAT)      │
    ┌───┴─────────────────────┴───┐
    │  Integration / API tests     │  NestJS + Supertest-style, real PG/Redis
├───┴─────────────────────────────┴───┤
│  Unit tests (Jest) — domain logic   │  majority of count; offline (NFR-010)
└─────────────────────────────────────┘
```

| Level | Share of suite (target) | What it proves | Tool |
|---|---|---|---|
| Unit | ~60% | Business rules, state machine, money math in isolation | Jest |
| Integration / API | ~25% | Module + DB + queue behaviour, authz, idempotency | Jest + Supertest-style against the NestJS app |
| E2E | ~10% | Cross-surface journeys (register → order → delivery → refund) | Playwright (3 web surfaces), Maestro (2 RN apps) |
| Non-functional | ~5% | Load, security, a11y, localization | k6, ZAP-style DAST, axe-core, Lighthouse CI |

The pyramid is deliberately **unit-heavy**: `NFR-010` requires all business logic to be unit-testable without network, and `AC-S-08` sets measurable coverage floors (see [testing-strategy.md](core/testing-strategy.md) §4).

## 3. Toolchain

| Concern | Tool | Notes |
|---|---|---|
| Unit / integration | **Jest 29** | Also runs contract tests against mock adapters (`../10-integrations/core/testing-and-sandboxes.md`) |
| HTTP assertion layer | **Supertest-style** in-process API tests | Hits the NestJS app without a live socket |
| Web E2E | **Playwright** | Chromium/Firefox/WebKit — covers customer web, vendor panel, admin console; also serves cross-browser checks (`AC-NFR-015-01`) |
| Mobile E2E | **Maestro** flows on RN 0.73 | Runs on the `DEP-12` device lab; see strategy §2.3 justification |
| Performance | **k6** | Steady/spike/soak scenarios for `C-25`, `NFR-001…004` |
| Security | **SAST + dependency scan in GitHub Actions; ZAP-style DAST on staging; axe-core for a11y** | `SEC-REQ-012`, `AC-SR012-01/02` |
| Accessibility | **axe-core + Lighthouse CI** | `NFR-011`, `AC-S-10` |
| Observability of tests | Prometheus/Grafana | Load-run metrics, alert drills (`INT-REQ-007`) |

## 4. File Index

| File | ID | Purpose | Source of truth |
|---|---|---|---|
| [README.md](README.md) | DOC-TST-001 | This overview, TC allocation index | yes |
| [testing-strategy.md](core/testing-strategy.md) | DOC-TST-002 | Methodology §47 verification strategy — levels, coverage, environments, defect lifecycle | yes |
| [test-plans.md](core/test-plans.md) | DOC-TST-003 | Executable plans: per-domain, performance, security, chaos, a11y, localization, mobile, migration | no |
| [constraint-tests.md](core/constraint-tests.md) | DOC-TST-004 | **Canonical register `TST-CON-01…TST-CON-26`** — one test per `C-01…C-26` | yes |
| [test-data-and-environments.md](core/test-data-and-environments.md) | DOC-TST-005 | Environment matrix, fixtures, PII masking policy for non-prod | no |
| [test-cases/README.md](test-cases-index.md) | DOC-TST-006 | TC layer anatomy, locked range table, coverage summary | no |
| `test-cases/TC-NNN.md` | `DOC-TC-NNN` | 114 individual test cases (`TC-001`…`TC-114`) | no |
| [`core/`](core/README.md) | DOC-TST-007 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-TST-008 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-TST-009 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-TST-010 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-TST-011 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

## 5. Locked Test-Case Allocation (TC-001 … TC-114)

The block allocation below is **locked**: TC IDs are never renumbered or reassigned to another domain. Individual TC files live in [`test-cases/`](test-cases-index.md).

| Range | Domain | FR | Count |
|---|---|---|---|
| TC-001–010 | Authentication (OTP, login, refresh rotation, lockout, sessions) | FR-001 | 10 |
| TC-011–014 | Authorization: cross-user access, cross-store access, staff escalation, direct API bypass — each expecting 404/deny | FR-002 | 4 |
| TC-015–017 | Catalog (products, categories, images) | FR-004 | 3 |
| TC-018–020 | Inventory (stock TTL 15 min, oversell prevention, optimistic lock) | FR-005 | 3 |
| TC-021–022 | Reviews & ratings | FR-006 | 2 |
| TC-023–024 | Vendor onboarding & KYC | FR-007 | 2 |
| TC-025–026 | Store management | FR-008 | 2 |
| TC-027–028 | Search & discovery | FR-009 | 2 |
| TC-029–030 | Shopping cart (limits, guest merge) | FR-010 | 2 |
| TC-031–042 | Checkout, payment & wallet (TC-031 = checkout wallet payment — canonical example `FR-013 → BR-PAY-04 → API-WAL-002 → TC-031`) | FR-011, FR-013 | 12 |
| TC-043–056 | Order lifecycle (17-state machine, cancellation window, master/sub) | FR-012 | 14 |
| TC-057–064 | Escrow, commission & payouts | FR-014 | 8 |
| TC-065–074 | Shipping & delivery (code verify, first-accept, failed attempts) | FR-015 | 10 |
| TC-075–084 | Returns, refunds & disputes | FR-016 | 10 |
| TC-085–090 | Notifications (SMS/WhatsApp/in-app/push) | FR-017 | 6 |
| TC-091–096 | Analytics & reporting | FR-018 | 6 |
| TC-097–104 | Content, CMS & coupons | FR-019 | 8 |
| TC-105–114 | Platform administration, moderation & audit | FR-020 | 10 |
| **Total** | | | **114** |

FR-003 (profile/addresses) is exercised within TC-001–010 (registration/profile setup) and via AC-FR003-* acceptance tests; no dedicated TC block.

## 6. Constraint Tests (TST-CON)

The canonical register **`TST-CON-01 … TST-CON-26`** — exactly one test per constraint `C-01 … C-26` — is defined **only** in [constraint-tests.md](core/constraint-tests.md). Highlights required by canon:

| Test | Constraint | Assertion |
|---|---|---|
| `TST-CON-09` | C-09 | State count == 17 and no other states exist in code |
| `TST-CON-14` | C-14 | Order total accepted only in 500–5,000,000 YER |
| `TST-CON-16` | C-16 | No GPS/location field anywhere + 6-digit delivery-code flow (3 attempts → 24 h lock) |
| `TST-CON-25` | C-25 | 10,000 concurrent users sustained within NFR-001 |
| `TST-CON-26` | C-26 | 99.99% availability SLO verification method |

`AC-S-02` requires 26/26 PASS as a release gate.

## 7. How Testing Satisfies the Success Criteria (`AC-S-*`)

| Success criterion | Satisfied by |
|---|---|
| AC-S-01 (20 FRs VERIFIED) | TC evidence per FR block + requirement status audit |
| AC-S-02 (26/26 constraints) | [constraint-tests.md](core/constraint-tests.md) register, executed per plan |
| AC-S-03 (0 traceability gaps) | `../19-traceability/core/requirements-to-tests.md` — AC → TC / plan / TST-CON |
| AC-S-04 (4 surfaces deliver UC set) | Per-surface E2E + UAT sign-off (test-plans §a) |
| AC-S-05 (p95 under 10k concurrent) | k6 steady-state plan (test-plans §b), 30-minute window |
| AC-S-06 (99.99% availability) | `TST-CON-26` + post-launch probes (`AC-NFR-005-01`) |
| AC-S-07 (0 CRITICAL/HIGH defects) | Defect lifecycle severity gate (strategy §10) |
| AC-S-08 (coverage 80/95/90) | Coverage thresholds enforced in CI (strategy §5) |
| AC-S-09 (regression < 30 min) | Impact-based regression + nightly full E2E (strategy §12) |
| AC-S-10 / AC-S-11 (a11y, RTL) | Accessibility plan (test-plans §e) and localization/RTL plan (§f) |
| AC-S-12 / AC-S-13 (threats, vulns) | Security plan (test-plans §c) |
| AC-S-14 / AC-S-15 (ledger, idempotency) | Payment TC suite + reconciliation fixtures (test-data §4) |
| AC-S-16 (no secrets in repo) | CI secret scanning (security plan) |
| AC-S-17 / AC-S-18 / AC-S-20 | Restore drill, alert drill, rollback rehearsal (test-plans §d, §h) |

## 8. Navigation

- QA engineer: this file → [testing-strategy.md](core/testing-strategy.md) → [test-plans.md](core/test-plans.md) → [test-cases/README.md](test-cases-index.md).
- Implementer needing a constraint's pass criteria → [constraint-tests.md](core/constraint-tests.md).
- Anything about test data, environments, fixture phones → [test-data-and-environments.md](core/test-data-and-environments.md).
- Upstream canon: `02-requirements/acceptance-criteria.md` (AC), `00-project-overview/project-constraints.md` (C), `01-business-analysis/business-rules.md` (BR).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | Scope line count sync: 99 → **104 business rules** (`BR-INV-01…05` registered) | `CRIT-06`/`HAL-04` pay-down (session 008) — consumer of `business-rules.md` v1.1 (root README §9.4) |
| 1.2 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-TST-007…DOC-TST-011) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
| 1.3 | 2026-09-30 | Scope-line count sync: 68 → **73 requirements**, 104 → **111 business rules**, 253 → **273 acceptance criteria** (`requirements-overview.md` v1.2, `business-rules.md` v1.2, `acceptance-criteria.md` v1.2) | Owner directive session 011 (`prompt-011.md` §4.7) — three count consumers re-synced in same change set |
