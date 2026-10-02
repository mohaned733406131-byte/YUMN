---
document_id: DOC-TST-003
title: Test Plans — Executable Verification Plans
category: 13-testing
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-001, NFR-002, NFR-004, NFR-011, NFR-013, SEC-REQ-009, SEC-REQ-011, SEC-REQ-012, DATA-REQ-004, INT-REQ-003, INT-REQ-006]
related_documents: [DOC-TST-001, DOC-TST-002, DOC-TST-004, DOC-TST-005, DOC-INT-008, DOC-UX-006]
---

# Test Plans

Executable plans for the yumn verification effort. Methodology (levels, coverage, defect lifecycle) is fixed by [testing-strategy.md](testing-strategy.md); this file defines **what runs, when, and under which entry/exit conditions**. Every plan cites its canon IDs; results are evidence for the quality gates in `../../21-completion/core/quality-gates.md`.

**Defects process (all plans):** failures are filed against the failing TC / `TST-CON-*` / AC ID with severity per [testing-strategy.md](testing-strategy.md) §10. CRITICAL/HIGH block the plan's exit; security defects additionally follow `SEC-REQ-012` (critical ≤ 7 days); anything deferred needs written risk acceptance in `17-risk-management/core/risk-register.md`.

---

## §a. Per-Domain Feature Plans

| Plan | Domain | TC range | FR / key BR / C coverage | Entry criteria | Automation |
|---|---|---|---|---|---|
| PLAN-01 | Authentication | TC-001–010 | FR-001, BR-AUTH-01…08, C-06, C-08, SEC-REQ-001/003/005 | FR-001 ACs stable; OTP mock adapter + SMS sandbox available | 95% |
| PLAN-02 | Authorization | TC-011–014 | FR-002, BR-VND-06/07, SEC-REQ-004, AC-FR002-01…05, AC-SR004-01…04 | RBAC matrix defined in `../../09-security/core/rbac.md`; ≥2 roles seeded per actor | 100% |
| PLAN-03 | Catalog | TC-015–017 | FR-004, BR-CAT-01…08, C-17 | Category tree + Arabic fixtures seeded (DOC-TST-005) | 95% |
| PLAN-04 | Inventory | TC-018–020 | FR-005, BR-CAT-07, C-13, C-14 | Timer injection harness available; concurrency runner ready | 95% |
| PLAN-05 | Reviews & ratings | TC-021–022 | FR-006, BR-REV-01…05 | DELIVERED-order fixture exists | 90% |
| PLAN-06 | Vendor onboarding & KYC | TC-023–024 | FR-007, BR-VND-01/03/04 | KYC document fixtures (masked, `MASK-03`) loaded | 90% |
| PLAN-07 | Store management | TC-025–026 | FR-008, BR-VND-02/04/05/06 | ≥2 stores with staff roles seeded | 90% |
| PLAN-08 | Search & discovery | TC-027–028 | FR-009, BR-CAT-06, AC-FR009-01…04 | ES index fixtures with Arabic diacritics/typos loaded | 90% |
| PLAN-09 | Shopping cart | TC-029–030 | FR-010, BR-CRT-01…06, C-15 | Cart limit fixtures (50/51, 5/6) present | 95% |
| PLAN-10 | Checkout, payment & wallet | TC-031–042 | FR-011, FR-013, BR-PAY-01…10, BR-CRT-06, BR-ORD-06, C-01, C-05, C-14 | Money boundary fixtures + ledger invariant harness green | 95% |
| PLAN-11 | Order lifecycle | TC-043–056 | FR-012, BR-ORD-01…10, C-09, C-10 | 17-state fixtures exist; `TST-CON-09` design reviewed | 95% |
| PLAN-12 | Escrow, commission & payouts | TC-057–064 | FR-014, BR-ESC-01…08, C-12 | Clock-shift harness for 7-day/3–7-day windows ready | 90% |
| PLAN-13 | Shipping & delivery | TC-065–074 | FR-015, BR-SHP-01…07, C-16, C-17 | Fake courier accounts + code fixtures seeded; no GPS field exists (`TST-CON-16`) | 90% |
| PLAN-14 | Returns, refunds & disputes | TC-075–084 | FR-016, BR-RET-01…07, C-11 | Return-window + 72-h inspection fixtures ready | 90% |
| PLAN-15 | Notifications | TC-085–090 | FR-017, BR-NTF-01…05, INT-REQ-003/004 | Mock SMS/WhatsApp adapters with failover injection | 95% |
| PLAN-16 | Analytics & reporting | TC-091–096 | FR-018, BR-VND-07, BR-FIN-03/04 | Closed-day dataset with ledger-consistent totals | 85% |
| PLAN-17 | Content, CMS & coupons | TC-097–104 | FR-019, BR-PRM-01…06 | Coupon edge fixtures (90%/91%, 90/91 days) seeded | 95% |
| PLAN-18 | Platform administration & audit | TC-105–114 | FR-020, BR-PLT-06, SEC-REQ-010 | Admin/Moderator accounts + audit chain verifier ready | 80% |

- **Schedule pointer:** plans execute per sprint against `../../21-completion/core/roadmap.md`; PLAN-01/02/09/10/11 are Phase-1 critical path. Sizing and sequencing detail: sprint test plan appendix maintained in CI, not in docs.
- **User acceptance:** at each release candidate, a per-surface UAT pass (`AC-S-04`) executes the P0/P1 journeys of every plan's TC range; sign-off sheets reference the plan IDs above and are filed as release evidence.
- **Entry (common):** FR + ACs stable; environment healthy; fixtures seeded (DOC-TST-005); TCs for the range exist and are READY.
- **Exit (common):** all TCs in range executed, P0/P1 100% PASS, 0 CRITICAL/HIGH open, evidence links added to the TCs, `19-traceability/` updated.

## §b. Performance Plan (k6)

Scope: prove `NFR-001/002/004`, `NFR-003` (`C-25`), `NFR-017` — against staging built from the same image digests as production.

| ID | Scenario | Pattern | Duration | Thresholds (pass = all hold) |
|---|---|---|---|---|
| PERF-01 | Steady 10K concurrent mixed | ramp → hold 10,000 VUs | 30 min (`AC-S-05`) | p95 read < 200 ms; p95 write < 500 ms; p99 write ≤ 1,000 ms; error < 0.1%; CPU < 70%; mem < 75%; pool < 80% (`AC-NFR-003-01/02`) |
| PERF-02 | Read/catalog-heavy | browse, search, product pages | 15 min | p95 read < 200 ms; cache hit ratio ≥ 80% on catalog reads (`NFR-004`, `AC-NFR-004-01`) |
| PERF-03 | Search-heavy (ES) | query mix incl. Arabic analyzer queries | 15 min | p95 < 200 ms; facet counts consistent; ES-down fallback still < 1% errors (`AC-FR009-03`) |
| PERF-04 | Checkout path mix | realistic browse→cart→checkout→wallet pay ratios | 30 min | p95 write < 500 ms; 0 duplicate orders/debits; stock never negative (`AC-FR011-02`, `AC-FR005-01`) |
| PERF-05 | Spike | burst 1k → 10k VU in 60 s, hold 5 min | 10 min | error < 0.5% during burst; recovery ≤ 60 s; no data inconsistency (`NFR-007`) |
| PERF-06 | Soak 30 min (pre-release) | steady 60% of C-25 with write traffic | 30 min | no memory growth trend; queue backlog drains ≤ 5 min (`AC-NFR-003-02`) |
| PERF-07 | Client performance | Lighthouse CI mobile/4G: home, category, product, checkout | per PR | LCP < 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1; JS < 200 KB gz (`AC-NFR-002-01/02`) |

- **Schedule:** PERF-07 per PR; PERF-01/02 weekly; PERF-03–06 pre-release and after any perf-relevant change.
- **Entry:** staging at parity; soak of synthetic data volume for `AC-NFR-017-01`; monitoring (RED metrics) live.
- **Exit:** all thresholds green on three consecutive runs; report archived; any breach filed as CRITICAL (SLO) or HIGH.
- **Defects:** perf regressions are HIGH at minimum; SLO breaches are CRITICAL and release-blocking (`AC-S-05`).

## §c. Security Plan

Scope: `SEC-REQ-001…012`, OWASP Top 10 mapping, `AC-SR001-01…AC-SR012-04`, `AC-S-12/13/16`.

| ID | Activity | Tool / method | Trigger | Pass condition |
|---|---|---|---|---|
| SEC-P-01 | SAST | GitHub Actions static analysis + ESLint security rules | every PR | 0 high/critical findings in changed code |
| SEC-P-02 | Dependency scan | npm audit / OSV-style scanner | every PR + nightly | 0 known critical CVEs; criticals fixed ≤ 7 d (`SEC-REQ-012`) |
| SEC-P-03 | Secret scanning | gitleaks-style CI scan | every PR | 0 secrets in repo (`AC-S-07`, `AC-SR007-01/03`) |
| SEC-P-04 | DAST | ZAP-style baseline + active scan on staging | weekly + pre-release | 0 exploitable high/critical (`AC-S-13`) |
| SEC-P-05 | Authz matrix | TC-011–014: cross-user, cross-store, staff escalation, direct API bypass | every PR | every case returns 404/deny, no data leak (`AC-FR002-01…05`, `AC-SR004-01…04`) |
| SEC-P-06 | Rate limiting | sustained bursts on standard, OTP, top-up endpoints | weekly | 100 req/min standard enforced; stricter OTP/top-up buckets; 429 returned (`SEC-REQ-009`, `AC-SR009-01/02`) |
| SEC-P-07 | File upload | oversized / wrong-type / SVG / EXIF payloads on catalog + KYC | every PR (API) | reject per policy, EXIF stripped, no SVG execution (`SEC-REQ-011`, `AC-SR011-01…03`) |
| SEC-P-08 | Auth abuse | lockout (5→15 min), OTP 3 attempts, refresh reuse, delivery-code 3 attempts | every PR | behavior matches BR-AUTH-04/05, `AC-SR005-01/02/03` |
| SEC-P-09 | Threat-model coverage | map `STP-*` controls to tests | pre-release | 100% covered (`AC-S-12`) |

OWASP mapping: injection → SEC-P-04 + Prisma parameterization tests; broken auth → SEC-P-08; broken access control → SEC-P-05; misconfig/secrets → SEC-P-03 + env review; crypto failures → TLS 1.3/AES-256 checks (`AC-SR006-01/02`); injection/XSS/CSRF → `AC-SR008-01…03` attack suite.
- **Entry:** staging reachable; scan targets seeded with authenticated sessions; test accounts per role.
- **Exit:** all SEC-P-* green; 0 open CRITICAL/HIGH security defects; scan reports archived.
- **Defects:** exploitable CRITICAL/HIGH → immediate ticket, release blocked (`AC-S-13`).

## §d. Reliability & Chaos Plan

Scope: `NFR-006/007`, `INT-REQ-003/006`, `DATA-REQ-004`, `AC-XCUT-04`, drills catalogued in `../../10-integrations/core/testing-and-sandboxes.md` §4.

| ID | Drill | Injection | Expected outcome | Canon |
|---|---|---|---|---|
| CHAOS-01 | SMS provider DOWN | primary adapter timeout/error | automatic failover (second provider or WhatsApp) delivers OTP inside its 5-min window; no duplicate sends | `INT-REQ-003`, `AC-IR003-01/02/04` |
| CHAOS-02 | Webhook retry storm | replay one webhook 10×; poison handler | signature check holds; idempotent single effect; 3 retries → DLQ → alert ≤ 1 min; admin replay works | `BR-PLT-02`, `INT-REQ-006` |
| CHAOS-03 | Redis restart | restart Redis under load | catalog falls back to DB, stricter rate limits, error < 1%, sessions survive on access tokens | `NFR-007`, `AC-XCUT-04` |
| CHAOS-04 | Queue workers stopped | suspend BullMQ workers | jobs persist and resume; 0 lost/duplicated jobs; backlog drains ≤ 5 min | `BR-PLT-02`, `AC-NFR-007-02` |
| CHAOS-05 | Elasticsearch down | stop ES container | browse/product pages serve from DB/cache; search shows fallback; recovery ≤ 60 s | `AC-FR009-03`, `AC-XCUT-04` |
| CHAOS-06 | DB failover / restore drill | declare DR, restore on clean host | write-ready ≤ 1 h (RTO), ≤ 15 min data loss (RPO), ledger reconciles with 0 lost money | `DATA-REQ-004`, `AC-NFR-006-01`, `AC-S-17` |
| CHAOS-07 | API replica kill | kill replica mid-load | LB drains ≤ 30 s; 0 failed sessions; error < 0.1% | `AC-NFR-018-01` |
| CHAOS-08 | Alert fire drill | stage a trigger | page ≤ 1 min, ack ≤ 15 min | `INT-REQ-007`, `AC-S-18` |

- **Schedule:** CHAOS-01/02 weekly (integration cadence); CHAOS-03/04/05 nightly-triggered in staging; CHAOS-06 quarterly (`AC-S-17`) and pre-launch; CHAOS-07/08 pre-release.
- **Entry:** staging with fault-injection access; snapshot/backup verified fresh; on-call rota notified for drills touching shared envs.
- **Exit:** all drill PASS conditions met and recorded; zero silent data loss proven by reconciliation run after each drill.
- **Defects:** any lost/duplicated job or money inconsistency → CRITICAL; degraded-but-correct behavior → HIGH if user-facing error ≥ 1%.

## §e. Accessibility Plan

Scope: `NFR-011`, `AC-NFR-011-01/02`, `AC-S-10`, patterns in `../../11-ui-ux/core/accessibility.md`.

1. **Automated:** axe-core scan of every customer-facing page in `ar` and `en` — per PR on changed routes, full sweep weekly. Pass = ≥ 95% automated, 0 critical, 0 serious violations.
2. **Contrast/token audit:** design-token contrast pairs verified against the approved table (`../../11-ui-ux/core/accessibility.md` §1.1).
3. **Keyboard-only journey:** register → browse → cart → checkout → track order, executed without a mouse; visible focus, logical order, no traps (per PR can't cover this → per release, manual).
4. **Screen reader:** TalkBack (Android) + VoiceOver (iOS) core journeys in both locales; RTL focus order and announcements checked (`AC-XCUT-03` step 6).
5. **Structural checks:** landmarks/headings/alt text/form labels asserted in Playwright a11y assertions on P0 pages.

- **Entry:** stable UI for the page set; both locales rendered; axe rule set pinned.
- **Exit:** thresholds met (`AC-S-10`); manual passes recorded with screenshots/screen-reader logs; 0 open critical a11y defects.
- **Defects:** zero-tolerance for critical violations (release-blocking); serious → HIGH; moderate → MEDIUM.

## §f. Localization Plan

Scope: `NFR-013`, `C-24`, `BR-PLT-05`, `AC-NFR-013-01/02`, `AC-XCUT-03`.

1. **Key coverage:** CI scan — 100% of i18n keys present in `ar`/`en`, 0 hardcoded user-facing strings (per PR).
2. **Template inventory:** every SMS/WhatsApp/in-app/push template exists in both locales; delivery asserted per locale (`BR-NTF-04`).
3. **Formatting:** Arabic-Indic currency numerals, `ar-YE` dates/numbers, integer YER display (`BR-PAY-10`) — locale-format unit tests.
4. **RTL visual regression:** core journeys at 320/768/1280 px in `ar` — mirrored layout, drawers, icons, focus order; 0 RTL defects (`AC-S-11`).
5. **Parity walk:** English switch — no missing labels, no untranslated keys, `dir=ltr` correct (`AC-XCUT-03` step 4).
6. **Mixed-locale scan:** automated assertion that no string mixes `ar`/`en` fragments in one sentence.

- **Entry:** locale files frozen for the release; screenshots baselines approved.
- **Exit:** all six checks green; 0 RTL defects on core journeys; reports archived.
- **Defects:** missing translation/key = MEDIUM (HIGH if it blocks a core journey); RTL layout break = HIGH on P0 flows.

## §g. Mobile Device-Lab Plan (`DEP-12`)

Scope: RN 0.73 customer + courier apps on real devices — `AC-NFR-015-02`, `NFR-015` (Android 10+, iOS 15+), push verification, carrier-real OTP.

| Activity | Devices | What is proven |
|---|---|---|
| Maestro P0 smoke (both apps) | ≥ 6 physical devices: Android 10/12/14, iOS 15/17 (`NFR-015`) | register/OTP, browse, cart, checkout, delivery-code entry, order tracking in `ar` + `en` |
| Push delivery | one Android + one iOS | FCM/APNs tokens register; notifications arrive; invalid-token handling (`FR-017`) |
| Carrier-real OTP | SIMs per carrier | real SMS delivery, sender ID, p95 delivery time, failover to WhatsApp (`DEP-06`, `INT-REQ-003`) |
| Viewport/responsive | 320–1440 px | no blocking defects at small widths (`AC-NFR-015-02`) |
| Accessibility | TalkBack/VoiceOver devices | screen-reader pass from §e |

- **Schedule:** per release candidate; carrier-real pass only during `DEP-12` lab windows (dependency is Not Started — see `00-project-overview/dependencies.md`).
- **Entry:** signed debug builds installed; device farm online; test SIMs topped up; mock mode for provider-free runs.
- **Exit:** 0 blocking defects across the device matrix; push + OTP evidence recorded; failures filed per TC.
- **Defects:** app crash on a supported OS version = CRITICAL; flow-blocked on one device = HIGH; layout-only = LOW/MEDIUM.

## §h. Migration & Rollback Rehearsal

Scope: `15-deployment/` release process, `NFR-020`, `DATA-REQ-005`, `AC-NFR-020-02`, `AC-S-20`.

1. **Expand-contract migration:** apply migration while old app version still runs; assert both versions coexist without errors (`AC-DR005-01/03`).
2. **Deploy rehearsal:** staging deploy under synthetic traffic — 0 failed customer requests (< 0.1% 5xx) during window.
3. **Rollback drill:** deliberate bad release → rollback completes ≤ 15 min; data changes from the release are reverted or forward-fixed per runbook (`AC-S-20`).
4. **Seed/fixture re-baseline:** verify fixture refresh (DOC-TST-005 §5) survives schema change.
5. **Image parity:** identical digests across envs after promote (`AC-NFR-016-01`).

- **Schedule:** every release candidate; quarterly full DR variant merged with CHAOS-06.
- **Entry:** runbook exists (`15-deployment/`); migration dry-run passed on a copy of prod-like data (masked); rollback script tested once already.
- **Exit:** deploy + rollback timings recorded; 0 customer-visible errors; evidence filed for `AC-S-20`.
- **Defects:** failed rollback or data loss = CRITICAL; slow but clean rollback (> 15 min) = HIGH.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
