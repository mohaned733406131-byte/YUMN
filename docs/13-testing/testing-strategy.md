---
document_id: DOC-TST-002
title: Testing Strategy — Verification Methodology (Methodology §47)
category: 13-testing
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-001, NFR-009, NFR-010, NFR-011, NFR-013, SEC-REQ-012, DATA-REQ-008]
related_documents: [DOC-TST-001, DOC-TST-003, DOC-TST-004, DOC-TST-005, DOC-REQ-001, DOC-AC-001, DOC-INT-008]
---

# Testing Strategy — Verification Methodology

**Source of truth for how yumn is verified.** This is the Verification Strategy of the analysis methodology (§47) expanded for this project: scope, test levels, coverage targets, automation policy, environments, Arabic/RTL testing, defect lifecycle, entry/exit criteria, regression, and explicit non-goals. Executable detail lives in [test-plans.md](test-plans.md); case detail in [`test-cases/`](test-cases/README.md).

---

## 1. Scope & Philosophy

**Scope:** five surfaces (customer web, vendor panel, admin console on Next.js 14; customer and courier mobile on React Native 0.73), the NestJS 10 modular monolith (13 blocks B01–B13, C-21), BullMQ workers, and the eight integrations (`INT-REQ-001…008`).

**Philosophy — five principles:**

1. **Evidence over assertion.** Every PASS carries a artifact: CI run ID, report file, dashboard export, or drill record (`AC-S-*` verification column).
2. **Rules are the oracle.** Test expectations derive from `FR-*`, `BR-*`, `C-*` and `AC-*` — never from the implementation under test. If code and canon disagree, the code fails.
3. **Shift left, but don't stop.** Unit tests carry the volume; API, E2E, load and security tests prove the seams.
4. **Fail fast in CI.** Merge-blocking gates (lint, types, unit, contract, SAST) run on every PR (`NFR-009`).
5. **Test the failure, not only the happy path.** Every plan carries negative and fault-injection cases (`AC-XCUT-04`, `NFR-007`).

## 2. Test Levels

### 2.1 Unit (Jest)

- **Covers:** pure domain logic — business rules (104 `BR-*`), the 17-state order machine (C-09), money math (integer YER, VAT `BR-FIN-01`, commission `BR-ESC-03`), validation guards, adapter contract math (retry/backoff), stateless authorization helpers.
- **Rule:** no network, no clock, no shared DB (`NFR-010`; `AC-NFR-010-01` runs the suite with outbound sockets blocked).
- **Runs:** every PR, minutes.

### 2.2 Integration / API (Jest + Supertest-style)

- **Covers:** module + PostgreSQL 16 + Redis 7 + BullMQ together; HTTP contracts from `07-api/endpoints/`; idempotency keys; RBAC/ownership enforcement on real endpoints (TC-011–014); DB-level integrity (`AC-DR001-01…04`); ledger posting inside transactions.
- **Style:** boot the NestJS app in-process, exercise `07-api` routes, assert status/body/DB state — the Supertest pattern, no separate test server.
- **Runs:** every PR; provider calls use mock adapters (`DOC-INT-008` §2).

### 2.3 End-to-End (Playwright web, Maestro mobile)

- **Covers:** cross-surface journeys — register/OTP → fund wallet → browse/search → cart → checkout → delivery code → escrow → return/refund; plus vendor fulfillment and admin dispute paths.
- **Web:** **Playwright** drives the three web surfaces in one runner, in `ar` and `en`, on last-2 versions of Chrome/Safari/Firefox/Edge (`AC-NFR-015-01`).
- **Mobile:** **Maestro** flows (YAML, user-level driving) on RN 0.73 builds from the `DEP-12` device lab. *Justification:* Maestro runs against release-like builds with no native synchronization hooks, is stable across Android 10+ / iOS 15+, and keeps the mobile E2E suite small and green; deep mobile logic is covered at unit level, and RN shares the same tested domain/TS layer as web. Detox was rejected for v1: per-platform native builds and flaky async syncing add maintenance cost disproportionate to two apps whose critical logic lives server-side (`NFR-010`).
- **Runs:** nightly full suite; per-PR smoke of P0 journeys.

### 2.4 Performance (k6)

- **Covers:** `NFR-001` (p95 read < 200 ms / write < 500 ms), `NFR-002`, `NFR-003` (10,000 concurrent — C-25), `NFR-004` (cache hit ≥ 80%), `NFR-017` (volume). Scenarios and thresholds: [test-plans.md](test-plans.md) §b.
- **Runs:** weekly on staging + pre-release; soak 30 minutes per `AC-S-05`.

### 2.5 Security

- **Covers:** SAST + dependency + secret scanning in GitHub Actions; ZAP-style DAST (baseline + active scan) against staging; the authz matrix (TC-011–014); rate limits (`SEC-REQ-009`), upload hardening (`SEC-REQ-011`), token/OTP/lockout behavior (`SEC-REQ-001/003/005`), OWASP Top 10 mapping. Detail: [test-plans.md](test-plans.md) §c.
- **Runs:** SAST/secrets every PR; DAST weekly and pre-release (`SEC-REQ-012`, `AC-SR012-01/02`).

### 2.6 Accessibility

- **Covers:** WCAG 2.1 AA (`NFR-011`) — axe-core scans of every customer page in `ar` and `en` (≥ 95% automated pass, 0 critical/0 serious), keyboard-only journeys, TalkBack/VoiceOver passes.
- **Runs:** per PR (automated scan) + manual pass per release ([test-plans.md](test-plans.md) §e).

## 3. Level Selection Rule

| Change type | Minimum level required |
|---|---|
| Pure domain logic (`BR-*`) | Unit + at least one API test |
| New/changed endpoint | Unit + API contract + authz negative (TC-011 style) |
| UI change on a surface | Component/unit + Playwright (web) or Maestro (mobile) smoke |
| Money/stock/order path | Unit + API + idempotency/concurrency case + reconciliation fixture |
| Constraint-affecting change | Associated `TST-CON-*` must run and pass |
| Infra/config change | Smoke suite + chaos/regression subset |

## 4. Coverage Targets

| Target | Value | Justification |
|---|---|---|
| Overall line coverage (unit) | **≥ 80%** | `AC-S-08` / `AC-NFR-009-02` — the CI quality gate |
| Payment module line coverage | **≥ 95%** | `AC-S-08`; money is the highest-trust path (`C-01`, `BR-PAY-*`, `RISK-001` ledger invariant) |
| Auth module line coverage | **≥ 90%** | `AC-S-08`; single authentication channel (`SEC-001`) leaves no fallback |
| Branch coverage on domain logic (state machine, money, stock, coupon math) | **≥ 90%** | Local hardening (`INFERENCE`): these modules have asymmetric blast radius — a missed branch is a lost refund or an oversell; cheap to reach because the logic is pure (`NFR-009` testability, `NFR-010`) |
| E2E P0 journey pass rate | 100% to merge/release | `AC-S-07` |

Coverage is a **floor, not a goal**: a covered line that asserts nothing is reported as such in review. Thresholds are enforced as merge gates in CI (`14-devops-infrastructure/ci-cd.md`), matching `NFR-009`'s lint/type/test gates.

## 5. Automation Policy & CI Gating

| Suite | Trigger | Gate |
|---|---|---|
| Lint + types + unit + contract | every PR | merge-blocking |
| API/integration (mock adapters) | every PR | merge-blocking |
| SAST, dependency scan, secret scan, i18n key scan | every PR | merge-blocking (`SEC-REQ-007`, `SEC-REQ-012`) |
| Coverage thresholds (80/95/90) | every PR to a release branch | merge-blocking (`AC-S-08`) |
| Playwright P0 smoke + Maestro smoke | nightly | release-blocking |
| Full E2E (all journeys, both locales) | nightly | release-blocking for open defects |
| k6 performance, ZAP DAST | weekly + pre-release | release-blocking |
| Device-lab (`DEP-12`), UAT, DR/rollback drills | per release cycle | release gate |

**Automation rule:** any test executed twice manually must be automated in the next sprint unless it requires a physical device, a human judgment (usability), or a real provider certification window. Target: **≥ 90% of TCs automated**; the remainder (device-lab, UAT, moderation judgment calls) are listed in [test-plans.md](test-plans.md) with manual procedure.

## 6. Test Data Policy

Owned by [test-data-and-environments.md](test-data-and-environments.md) (DOC-TST-005): reserved phone block, Arabic/English fixtures, boundary fixtures (money, cart, coupons, 17 states, OTP timing), ledger fixtures with zero-imbalance invariant, and PII masking (`MASK-01…MASK-06`) for non-prod. Summary of the hard rules:

- No production data in non-prod; restored backups are masked before use (`16-data/data-classification.md`).
- Fixtures are code (seed scripts), versioned in the repo — never hand-inserted rows on shared environments.
- Every fixture asserts the invariant it exists to protect (e.g., Σ ledger = 0) on load.

## 7. Environments

| Env | Purpose | Providers | Real PII? |
|---|---|---|---|
| local | Developer loop, `docker compose up` (C-22, C-19) | mock adapters | no |
| dev (shared) | Branch CI integration runs | mock adapters | no (masked) |
| staging | Prod-like: full stack, E2E/perf/DAST, drills | **fake/sandbox only — no real money** (`DOC-INT-008` §2) | no (masked) |
| prod-like (pre-release) | DR/rollback rehearsal, load at C-25 scale | sandbox credentials | masked per `MASK-*` |
| production | **No tests beyond passive probes and smoke** | real | real |

Environment parity is a test asset: image digests must match across envs (`AC-NFR-016-01`). Full matrix: [test-data-and-environments.md](test-data-and-environments.md) §1.

## 8. Arabic / RTL Testing

Arabic-first is a functional requirement, not a cosmetic one (`C-24`, `NFR-013`):

1. **Default locale:** every journey is authored with `ar` as the primary path; `en` is the parity run (both always executed).
2. **Visual regression:** core journeys at 320/768/1280 px in `ar` — mirrored layout, icon flipping, drawer/focus order (0 RTL defects, `AC-XCUT-03`).
3. **Formatting:** integer YER with Arabic-Indic numerals, locale dates, `ar-YE` (BR-PAY-10).
4. **Search:** Arabic-aware analyzer — alef variants, diacritics, common typos (`AC-FR009-01`).
5. **Templates:** every notification template asserted in both locales (BR-NTF-04).
6. **Screen reader:** TalkBack/VoiceOver announce Arabic correctly; focus follows visual RTL order (NFR-011).

## 9. Environments for Determinism

Flakiness is treated as a defect class: no test depends on wall-clock time (timer injection for the 15-min stock TTL, 5-min OTP, 7-day escrow, 72-h inspection), no test shares mutable state (per-test schema/tenant), and random data is seeded (reproducible failures). `AC-NFR-010-02` requires 0 flakes across 10 consecutive regression runs.

## 10. Defect Lifecycle & Severity

| Severity | Definition | Examples | Target fix |
|---|---|---|---|
| **CRITICAL** | Money loss/imbalance, security breach, data loss, constraint broken, total flow blocked | ledger Σ ≠ 0; COD path exists; 18th order state | immediate; release-blocking |
| **HIGH** | Core journey blocked or wrong result, no workaround | OTP never delivers; cross-user data visible (TC-011 fail) | ≤ 48 h; release-blocking |
| **MEDIUM** | Wrong behavior with workaround, or secondary flow broken | wrong VAT rounding on free-shipping coupon; stale cache > 5 s | next sprint |
| **LOW** | Cosmetic, minor copy, non-blocking UX | label overflow in `ar` at 320 px | backlog |
| **INFORMATIONAL** | Observation, tech-debt note, test gap | duplicate assertion in suite | backlog |

- Severity scale matches the project-wide finding classes (`CRITICAL · HIGH · MEDIUM · LOW · INFORMATIONAL`, root README §8) used by `09-security/security-findings.md` (`SEC-nnn`) and the risk severity classes in `17-risk-management/risk-register.md` (`RISK-nnn`).
- **States:** NEW → TRIAGED → IN_PROGRESS → FIXED → VERIFY → CLOSED / DEFERRED (with risk acceptance) / REJECTED (not a defect, with reason).
- **Release gate:** zero open CRITICAL/HIGH (`AC-S-07`). Security defects follow `SEC-REQ-012`: critical vulnerabilities fixed ≤ 7 days.
- Every defect references the failing TC / `TST-CON-*` / AC ID; closure requires re-run evidence.

## 11. Entry / Exit Criteria

**Entry (a suite may start):** ACs and rules for the scope are stable in `02-requirements`; the build deploys to the target environment healthy (`/healthz`); fixtures seed cleanly; test data ready; dependencies (e.g., `DEP-05`/`DEP-06` sandboxes) available or mock adapters in place; test cases exist for the scope (TC or TST-CON, status DESIGNED → READY).

**Exit (a scope is verified):** 100% of planned tests executed; all P0/P1 PASS; coverage thresholds met; 0 open CRITICAL/HIGH; every AC has linked evidence; defects deferred are risk-accepted in writing; results recorded and traceability updated (`AC-S-03`, `AC-S-07`).

## 12. Regression Strategy

1. **Impact-based selection (per PR):** map changed modules → their test sets (FR → TC block, constraint → `TST-CON-*`, API group → contract tests); run that subset plus the P0 smoke. Keeps PR feedback inside minutes.
2. **Nightly full E2E:** all journeys, both locales, all surfaces — catches cross-module drift.
3. **Weekly non-functional:** performance, DAST, coverage audit.
4. **Constraint sweep:** automated pass over all 26 `TST-CON-*` (`AC-XCUT-02`) before every release candidate.
5. **Budget:** full regression < 30 minutes with 0 flakes (`AC-S-09`, `AC-NFR-010-02`).

## 13. What Is NOT Tested in v1

| Excluded | Why | Reference |
|---|---|---|
| Live real-money movement | Sandbox/fake providers only in CI/staging; production credentials unreachable from tests | `10-integrations/testing-and-sandboxes.md` §2, `DOC-INT-008` |
| Email channels | No email in v1 (GAP-03) — no positive email tests exist | `BR-NTF-01`, GAP-03 |
| GPS / real-time tracking | Feature does not exist; only *absence* is asserted | `C-16`, `TST-CON-16` |
| Card, BNPL, COD, crypto paths | Prohibited; only negative/absence scans | `C-01…C-04`, `TST-CON-01…04` |
| Kubernetes / multi-cloud | Docker Compose only | `C-22` |
| Real carrier SMS at scale | Limited to `DEP-12` device-lab windows | `DEP-12` |
| Biometrics as server auth | Does not exist (device-local only) | `C-07` |
| Load beyond C-25 (10k) as a requirement | 50k path is a rehearsed runbook, not an acceptance gate | `AC-NFR-018-02` |

## 14. Traceability Requirement

Every TC cites its `FR/NFR/SEC-REQ/DATA-REQ/INT-REQ`, `BR-*`, `C-*` and `AC-*` IDs; every `TST-CON-*` cites its `C-*` and AC; every plan cites its AC/NFR group. `19-traceability/` maintains requirement → rule → component → API → DB → test matrices with **zero gaps** (`AC-S-03`) and is the release evidence index. A test with no upstream ID is deleted or the ID is added first — tests never exist "just in case" without canon.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | §2.1 unit-scope count sync: 99 → **104 `BR-*`** | BR-count propagation catch-up (session 008 close) — consumer of `business-rules.md` v1.1 (`BR-INV-01…05` registered; root README §9.4) |
