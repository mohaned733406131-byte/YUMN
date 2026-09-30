Kimi
Co-authored with Senior Eng. Salah Alssayani — Taizz University, Alsaeed Faculty of Engineering & IT, Department of Software Engineering (eng.salahalssayani@gmail.com)
License: GPL-3.0
# RULES_HINTS — System Adapter (binds ADMR to this system)

> This is the filled adapter for **yumn**. The AI reads it at session start (ADP-01/02).
> Framework- and project-specific rules live here and in `YUMN_RULES.md` ONLY —
> core rule files under `senior-rules/core/`, `RULES.md`, `ENTRY.md` are never modified (ADP-03).

## 1. System identity
- Name: **yumn (يُمن)** — multi-vendor e-commerce marketplace for Yemen · Version: **0.1.0** (analysis complete, pre-implementation) · Rules version pinned: **2.2.0**
- Pin source: `senior-rules/VERSION` = `2.2.0`. At session start (GEN-08) confirm VERSION ↔ CHANGELOG ↔ this pin agree and re-read changed rules before working.
  - **GEN-08 reconciliation (session 003, 2026-09-27):** pin **2.0.0**. The `[2.1.0]` entry is packaging-only (`.ai-rules`→`senior-rules` reference renames, npm installer, README updates) — it changes **no rule IDs, severities, or rule text**. Defect `D-13` → `RESOLVED 2026-09-27`.
  - **GEN-08 reconciliation (session 006, 2026-09-28):** pin **2.0.0 → 2.2.0**. `[2.2.0]` (MINOR) is the F-07 amendment: `validators/validate.py` check 5 now enforces rule-ID uniqueness in **both** `RULES.md` (77) and `YUMN_RULES.md` (94). Validator/tooling change only — **no rule IDs, severities, or rule text changed**; nothing to re-read beyond `CHANGELOG.md` `[2.2.0]`. (Pre-existing `VERSION` 2.0.0 vs `[2.1.0]` drift recorded in that entry, not silently reconciled.) npm package stays `v2.0.0` (`AGENTS.md` line is the published-package fact).
- Knowledge base: `docs/` (24-domain analysis, `APPROVED` v1.0). No implementation exists yet — nothing in `docs/` is `VERIFIED`.
- Language of record: English. Product locales: `ar` (default, RTL) + `en` only.

## 2. Stack
- Language/runtime: **TypeScript 5.x** on **Node.js 20 LTS** (single runtime in v1)
- Framework (backend): **NestJS 10** — modular monolith, modules map 1:1 to blocks `B01…B13`
- Framework (frontend): **Next.js 14 App Router** (customer/vendor/admin shells in one app) + **React Native 0.73** (customer + courier apps)
- DB: **PostgreSQL 16** + **Prisma 5** (`multiSchema`, schemas `b01…b13`) — only RDBMS allowed (`C-19`)
- Cache/queue: **Redis 7** + **BullMQ** (the only queue, `C-20`); search **Elasticsearch 8**; objects **MinIO**
- Infra: **Docker + Docker Compose** (Kubernetes excluded, `C-22`), Nginx 1.27 edge, **GitHub Actions**, Cloudflare; Prometheus / Grafana / Alertmanager
- Quality: Jest 29, Playwright, k6, Maestro, axe-core + Lighthouse CI, ESLint + Prettier, CodeQL, gitleaks, Trivy, Dependabot/Renovate, ZAP, size-limit
- External: m-Floos / OneCash wallet top-up adapters, Telesom/Sabafon SMS with failover, WhatsApp Business, APNs + FCM push
- Explicitly excluded: any commerce platform (`C-18`), microservices/Kafka/RabbitMQ (`C-20`/`C-21`), cards/BNPL/crypto/COD (`C-01…C-04`), email channel (`BR-NTF-01`), GPS/geolocation (`C-16`), biometrics (`C-07`), social/email-primary login (`C-06`)

## 3. Commands (must all exist and run green)
| Purpose | Command |
|---|---|
| Install (clean) | `npm ci` |
| Build (api) | `nest build` |
| Build (web) | `next build` |
| Lint | `eslint . --max-warnings=0` (includes module-boundary rules — a hard gate) |
| Format check | `prettier --check .` |
| Typecheck | `tsc --noEmit` (strict) |
| Unit tests | `jest --coverage --ci` |
| Full test suite | **NOT DOCUMENTED** as one command — regression budget is `< 30 min`, 0 flakes (`AC-S-09`). Bind a `test:all` script in bootstrap; until bound, this rule is `BLOCKED` (core/00 §0.6) |
| Coverage report | `jest --coverage --ci` (gates: overall ≥80%, `b07` ≥95%, `b01` ≥90% — see §6) |
| Migration run (dev) | `npx prisma migrate dev --name <descriptive_name>` |
| Migration run (deploy) | `npx prisma migrate deploy` (compose service `migrate`, forward-only) |
| Migration rollback | **No `migrate down` in production — forbidden.** Rollback = forward fix; rehearsal = restore drill (`docker compose up -d postgres redis minio elasticsearch`) + PITR |
| Migration lint / drift | `prisma validate` + `prisma migrate diff --from-migrations migrations/ --to-schema-datamodel schema.prisma --exit-code` |
| Seed | `npm run seed` (local); `seed:test` (versioned test fixtures); prod: `seed --only=reference` |
| Compose render | `docker compose config -q` |
| Secret scan | `gitleaks detect --redact --no-banner` |
| Dependency vulnerability scan | `npm audit --audit-level=high` (+ Trivy on images, CodeQL for SAST) |
| Dead-element scan | **NOT DOCUMENTED** — closest is the route-inventory test (`docs/05-frontend/core/routing.md` §10) plus CI boundary/queue-name/i18n gates. A real dead-route/dead-transaction inventory test must be created in bootstrap; until then DOD-05/IMP-02 verification is `BLOCKED` |
| Benchmark | k6 scenarios `PERF-01…PERF-07` on **staging** only — exact `k6 run …` invocation **NOT DOCUMENTED**; bind it in bootstrap |
| i18n key scan | Named as merge-blocking (`docs/13-testing/core/testing-strategy.md` §5) — command **NOT DOCUMENTED**; bind in bootstrap |
| Rules validator | `python3 senior-rules/validators/validate.py .` |

## 4. Paths
- Base dirs: backend `api/src/blocks/b01-identity … b13-platform/`, `api/src/shared/`, `api/src/integrations/`, `api/src/jobs/`, `api/src/prisma/` · tests `api/test/` · web `apps/web-customer/`, `apps/web-vendor/`, `apps/web-admin/` · mobile `apps/mobile-customer/`, `apps/mobile-courier/` · shared `packages/{api-sdk,ui,validation,i18n,design-tokens,config-eslint,config-ts}` · docs `docs/<NN-domain>/` · rules `senior-rules/`
- **Canonical repo tree = `05-frontend/frontend-architecture.md` §1 + `06-backend/backend-architecture.md` §1** (root `api/`, `apps/<shell>/`, `packages/*`). ⚠ Ops documents cite a different spelling (`apps/api`, `apps/web`, `apps/mobile/**`) — treat those as defects to correct (rule `SPE-04`), not as authority.
- Entry files present: `senior-rules/ENTRY.md`, `senior-rules/RULES.md`, `senior-rules/RULES_HINTS.md` (this file), `senior-rules/YUMN_RULES.md`, `senior-rules/CHANGELOG.md`, `senior-rules/VERSION`, root `AGENTS.md`. Root `session_track.md`, `development_phases_entry.md`, `all_in_one_track.md`, `architecture.md`, `mind_map.md`, `memory.md` are required by DOC-01 and are **pending creation** — status honesty: validator will report them `FAIL` until they exist.
- Main security spec: `docs/09-security/` (`threat-model.md`, `security-controls.md`, `rbac.md`, `security-findings.md` = `SEC-001…SEC-015` — corrected from `…SEC-016` on 2026-09-28, session 005: the register holds 15 findings, `SEC-016` is only a forward-sequence note; factual correction, no rule text/severity changed, pin stays `2.0.0`)
- Main architecture file: `docs/04-architecture/core/architecture-overview.md` (ADRs in `docs/18-decisions/ADR/ADR-001…010`)
- Requirements/source IDs: `docs/02-requirements/` (68 reqs), `docs/01-business-analysis/business-rules.md` (104 `BR-*` — count corrected 2026-09-28, session 008: `BR-INV-01…05` registered), `docs/00-project-overview/project-constraints.md` (`C-01…C-26`)

## 5. Conventions
- Branch prefix: `main` only long-lived; short-lived `feat/<ID>-<slug>`, `fix/<ID>-<slug>`, `chore/…`, `docs/<topic>`; PR-only; linear history (squash/rebase); force-push blocked on `main`
- Commits: conventional `type(scope): subject` carrying the governing ID — e.g. `feat(WAL): enforce top-up cap (BR-PAY-04)` (adopted here; the corpus records no canon commit standard)
- Module boundaries: blocks `B01…B13` ↔ DB schemas `b01…b13`; cross-schema **reads/FKs allowed, writes forbidden**; in-module layering `Controller → Service → Domain → Repository` — **`BR-*` rule ⇒ Domain, coordination ⇒ Service, HTTP ⇒ Controller**
- Naming: `docs/22-glossary/naming-conventions.md` is source of truth (kebab-case files, `UPPERCASE-DASH` IDs, singular snake_case tables, `<col>_yer` money, UUIDv7 PKs, `/api/v1` + plural kebab resources, queue pattern `{block}.{entity}.{action}`)
- Env/config: `SCREAMING_SNAKE_CASE`; hierarchy compiled defaults → `.env.<environment>` → runtime → feature flags → platform settings; secrets host-only, mode `0600`, fail-fast `CONFIG_MISSING: <name>` (name never value); no secrets under `NEXT_PUBLIC_`; no `if (env === 'production')` literals in app code

## 6. Overrides (may tighten, may NOT loosen without user approval)
- Coverage: ADMR `DOD-04` governs — **≥80% overall, 100% on critical paths**. Project floors (`docs/13-testing/core/testing-strategy.md` §4): overall ≥80%, payment/`b07` ≥95%, auth/`b01` ≥90%. ⚠ 95%/90% is **looser** than ADMR's 100%-critical gate: the stricter (100%) applies unless the user approves the project numbers in writing in the session log.
- Perf budgets (tighter than core defaults — permitted):
  - API p95 read **< 200 ms**, write **< 500 ms**; error rate **< 0.1%**; **10,000** concurrent users × 30 min (`NFR-001`, `NFR-003`, `C-25`)
  - Web **LCP < 2.5 s**, INP ≤ 200 ms, CLS ≤ 0.1; JS **< 200 KB gzipped** (`NFR-002`)
  - Availability **99.99%** (≤ 4.32 min/30 d), **RTO ≤ 1 h, RPO ≤ 15 min** (`C-26`, `NFR-005/006`)
  - Cache hit ratio ≥ 80%, staleness ≤ 5 s; wallet/order/ledger responses never cached (`NFR-004`)
  - Regression **< 30 min** with **0 flakes across 10 runs**; unit suite **< 3 min** (`AC-S-09`, `NFR-010`)
- Supported locales/RTL: exactly `ar` (default, RTL) + `en`; no third locale, no machine translation; Arabic-Indic numerals for money in `ar` (`C-24`, `NFR-013`)
- Accessibility target: **WCAG 2.1 AA** with ≥95% automated pass and 0 critical/serious axe findings (`NFR-011`) — tighter than the default

## 7. System-specific rules (stack-level only)
- **Full catalog: `senior-rules/YUMN_RULES.md`.** IDs are domain-prefixed (instead of the template's illustrative `SYS-NN`) so rules group by area: `MNY` money/ledger · `ESC` escrow/payout · `ORD` order state machine · `IDT` identity/OTP/session · `STK` stock/cart/checkout · `SHP` delivery/code · `RET` returns/disputes · `RTL` Arabic-first/i18n · `API` contract conformance · `DAT` database/migrations · `OPS` infrastructure/deploy · `PRF` performance/NFR · `SPE` spec-consistency. Stable IDs — never renumbered, never reused.
- Precedence (GEN-07 extended): `SEC` > `DOD` > `GEN-03` > `IMP` > **YUMN CRITICAL** > `DOC`/`AUD` > `TST`/`LOG`/`UI` > `VCS` > `COM` > MEDIUM/LOW. Where a YUMN rule is stricter than its core counterpart, the stricter text applies.
- The five absolute project prohibitions (each backed by a constraint, never overridden by feature pressure):
  1. **Wallet-only payments** — no COD, cards, BNPL, crypto (`C-01…C-04`)
  2. **No GPS / no real-time tracking** anywhere — no coordinate columns, no location SDKs (`C-16`)
  3. **Arabic-first, RTL, two locales only** (`C-24`)
  4. **Compose-only, monolith + BullMQ** — no Kubernetes, no microservices, no other RDBMS (`C-19…C-22`)
  5. **Ledger integrity is non-negotiable** — append-only double-entry, integer YER, zero imbalance (`BR-PAY-06`, `NFR-008`)
- Note: the template's flat `SYS-01…` numbering was replaced by domain prefixes for navigability; this is an adapter-level choice and does not modify any core file (ADP-03).

## 8. Sign-off
- Prepared by: analysis-agent (AI assistant, opencode) · Date: 2026-09-27 · Reviewed by: **PENDING** (project sponsor / technical lead)
- Reviewed-by sign-off is required before this adapter may be treated as binding for a phase gate (AUD-05).
