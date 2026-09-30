---
document_id: DOC-NFD-009
title: Accessibility — Measurable Targets & Verification
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-011, NFR-012, NFR-013]
related_documents: [DOC-NFD-001, DOC-NFR-011, DOC-AC-001, DOC-UX-004, DOC-UX-006, DOC-UX-007, DOC-TST-003, DOC-DTA-007, DOC-NFD-002, DOC-NFD-007]
---

# Accessibility — Measurable Targets & Verification

Measurable elaboration of **NFR-011** (WCAG 2.1 AA) for the yumn platform: per-surface conformance targets, numeric criteria, assistive-technology coverage, tooling thresholds, defect policy and evidence hooks. The requirement statement of record stays in `../../02-requirements/core/NFR-011.md`; design patterns stay in `../../11-ui-ux/core/accessibility.md`. Nothing here is implemented yet — status of every activity below is **DESIGNED** (root README §6).

## 1. Purpose & Relationship to NFR-011 / 11-ui-ux

This file answers the question the requirement statement and the UX patterns file cannot: *how is NFR-011 measured, on which surface, how often, with which tool, and what happens when a number misses*. It follows the `12-non-functional/` method (`DOC-NFD-001` §2): reference requirements by ID, add thresholds/cadences/policies only, never restate the requirement text, and never invent AC IDs.

| Concern | Authoritative location | This file's role |
|---|---|---|
| What must hold (WCAG 2.1 AA, ≥95% pass, 0 critical) | `../../02-requirements/core/NFR-011.md` (`DOC-NFR-011`) | inherits numbers unchanged; adds splits & cadences |
| PASS/FAIL outcomes | `02-requirements/acceptance-criteria.md` (`DOC-AC-001`) — `AC-NFR-011-01/02`, `AC-S-10` | lists which detail feeds which AC (§8) |
| What users see (patterns, contrast table, checklist) | `../../11-ui-ux/core/accessibility.md` (`DOC-UX-006`) | measures the patterns; does not re-describe them |
| How it is executed | `../../13-testing/core/test-plans.md` §e (`DOC-TST-003`) | feeds thresholds & defect mapping to the plan |
| Related quality claims | NFR-012 (usability), NFR-013 (locale parity — a11y runs per locale) | cross-cutting gates only |

## 2. Conformance Targets by Surface

Conformance level is **WCAG 2.1 Level AA on every surface** — matching NFR-011 exactly (AAA is explicitly not targeted, `DOC-UX-006` §7). NFR-011's normative scope is the *customer-facing web* flows (registration, catalog, cart, checkout, wallet, orders, support); mobile screens are named in its own metric (TalkBack/VoiceOver core journeys); vendor/admin/courier coverage is an elaboration aligned with `DOC-UX-006` §5 and `FR-020` (accessible admin UI).

| Surface | Scope in v1 (prioritized by usage) | Level | Target phase | Evidence type |
|---|---|---|---|---|
| S1 customer web (Next.js 14) | Full NFR-011 flow set: registration, catalog, cart, checkout, wallet, orders, support — both `ar` and `en` | WCAG 2.1 AA | **v1 must** | axe scan per locale + manual audit report + SR session log |
| S4 customer mobile (RN 0.73) | Core journeys FL-01…FL-03 (register → browse/buy → tracking/code) per NFR-011 metric | WCAG 2.1 AA (RN-adapted) | **v1 must** | SR session log (TalkBack/VoiceOver recordings) + automated RN scan |
| S2 vendor panel (web) | Listing creation, order inbox, payout views — dense tables and row actions (highest-risk per `DOC-UX-006` §5) | WCAG 2.1 AA | v1 should | automated scan + sampled manual audit |
| S3 admin console (web) | Money-action modals, KYC/dispute queues, confirm-focus-on-safe (`FR-020`) | WCAG 2.1 AA | v1 should | automated scan + spot audit of dialogs |
| S5 courier mobile (RN 0.73) | FL-06: job offer → code verify incl. attempts announcements | WCAG 2.1 AA (RN-adapted) | v1 should | SR session log + automated RN scan |

Phase tags (`v1 must` / `v1 should`) are `INFERENCE`: NFR-011 fixes the level and the customer scope, not a per-surface rollout order; `must` = release gate via `AC-S-10`, `should` = audited before launch, defects triaged under §6.

## 3. Measurable Criteria

Canon numbers (≥95% axe pass, 0 critical/serious) are inherited from NFR-011 / `AC-NFR-011-01` unchanged; everything else is new, measurable detail. Token pairs cited are the approved values in `DOC-UX-004` §1–2 and `DOC-UX-006` §1.1.

| # | Criterion | Target | Verification |
|---|---|---|---|
| 1 | Body text contrast | ≥ **4.5:1** (e.g. `#475467` on `#FFFFFF` = 7.7:1; `#667085` muted = 5.0:1) | axe + live-render spot check |
| 2 | Large text (≥24 px, or ≥18.66 px bold) & UI components (borders, icons, focus ring `#175CD3`) | ≥ **3:1** (control border `#667085` = 5.0:1) | axe + token audit |
| 3 | Touch targets (all surfaces) | ≥ **44 × 44 CSS px**; inputs ≥ 48 px height; adjacent targets ≥ 8 px apart | measurement pass at 320 px (`DOC-UX-006` §2.1) |
| 4 | Text resize / reflow | 200% zoom with **no loss of content or functionality**; no horizontal scroll at 320 px (WCAG 1.4.4/1.4.10) | manual resize pass, both directions |
| 5 | Keyboard reachability | **100%** of core journeys (FL-01…FL-04) completable keyboard-only; ≥95% of interactive controls on audited pages in natural tab order; 0 `tabindex > 0` (`INFERENCE` split) | manual keyboard run per release |
| 6 | Focus visibility | **100%** of focusable elements show a visible ring (≥3:1, never clipped in RTL); modals trap + restore focus | manual + axe |
| 7 | Alt-text coverage | **100%** of platform-owned images (CMS banners: alt required, `FR-019`) and **100%** non-empty localized alt on vendor product images — enforced by upload prompt + automated non-empty check at the publish gate (ties to `DQ-02`, §9); decorative images 100% `aria-hidden` | axe + publish-gate check |
| 8 | Order-state announcements | **17/17** states render icon + localized text (never color alone) and are announced as text; status *changes* announced via polite live region | SR session + checklist item 8 (`DOC-UX-006` §10) |
| 9 | Form error association | **100%** of validated fields carry `aria-invalid` + `aria-describedby` pointing at the error; focus moves to first invalid field | axe + manual form pass |
| 10 | Arabic RTL reading order | **0** reading-order/focus-order defects across core journeys in `ar` (SR order = visual RTL order) | SR session in `ar` (also `AC-XCUT-03` step 6) |
| 11 | Motion | `prefers-reduced-motion: reduce` / OS reduce-motion honored by **100%** of animated components (shimmer, shake, transitions → static) | reduced-motion pass |
| 12 | Automated pass | ≥ **95%** axe pass on every customer page, **0 critical, 0 serious** — in both locales (inherited, `AC-NFR-011-01`) | CI axe scan |
| 13 | Captions / audio description | **Out of scope in v1** — no video or audio content ships; becomes mandatory on adoption (`DOC-UX-006` §7) | n/a |

## 4. Assistive-Technology Support Matrix

NFR-011's manual metric names **TalkBack and VoiceOver**; desktop NVDA coverage is an `INFERENCE` extension for web surfaces (the vendor/admin personas work on desktop).

| Assistive technology | Surfaces | Support level | Test cadence |
|---|---|---|---|
| TalkBack + Chrome/Android | S4, S5 (and S1 in Chrome Android) | **must** (NFR-011 metric) | per release — core journeys, both locales, recorded |
| VoiceOver + Safari/iOS | S4, S5 (and S1 in Safari iOS) | **must** (NFR-011 metric) | per release — core journeys, both locales, recorded |
| VoiceOver + Safari/macOS | S1, S2, S3 | should (`INFERENCE`) | pre-launch + quarterly |
| NVDA + Firefox/Chrome (Windows) | S1, S2, S3 | should (`INFERENCE`) | pre-launch + quarterly |
| Screen-reader parity check after locale switch | S1 | must (`DOC-UX-006` §4) | every release that touches i18n plumbing |

No surface claims support for an AT outside this matrix without a new row here (version bump required).

## 5. Automation & Tooling

| Tool | Scope & trigger | Threshold / gate | Wiring |
|---|---|---|---|
| **axe-core** in Playwright e2e on P0 paths | per PR (changed routes) + full page sweep weekly; both locales | fail pipeline on **0 critical / 0 serious**; overall ≥95% (`AC-NFR-011-01`) | `../../14-devops-infrastructure/core/ci-cd.md` (root README §10 map) |
| **Lighthouse accessibility** on the four core pages (home, category, product, checkout) | per PR, mobile preset | score ≥ **90** (secondary signal — NFR-011 names Lighthouse as such) | CI artifact, same job family as Lighthouse CI perf gates (`DOC-NFD-002` §6) |
| **RN accessibility checks** (React Native accessibility inspector / axe-android) in Maestro device-lab runs | per release candidate on `DEP-12` devices | 0 unlabeled interactive controls; 0 touch target < 44 px on S4/S5 flows | `../../13-testing/core/test-plans.md` §g |
| **Contrast/token audit** vs `DOC-UX-006` §1.1 table | every release | every token pair AA on live render | manual, checklist item 5 |
| **Manual audits** (keyboard + SR + checklist) | public/customer flows **per release**; **full audit pre-launch and quarterly** thereafter | checklist 10/10 green (`DOC-UX-006` §10); recordings archived | QA, evidence per §8 |

Automated coverage is knowingly partial (axe exercises rules, not comprehension) — the manual cadence is the real gate for `AC-NFR-011-02` (`INFERENCE` on tool coverage share).

## 6. Defect Management

Severity mapping reuses the project scale (`DOC-TST-002` §10) and the axe→defect mapping already fixed in `../../13-testing/core/test-plans.md` §e:

| axe impact | Defect severity | Fix target | Release effect |
|---|---|---|---|
| critical (blocks a core task) | **CRITICAL** | immediate | **release-blocking** (zero tolerance) |
| serious (core task degraded, no workaround) | **HIGH** | ≤ 48 h | **release-blocking** (`AC-S-07`: 0 open CRITICAL/HIGH) |
| moderate (workaround exists) | **MEDIUM** | next sprint | non-blocking |
| minor/cosmetic | **LOW** | backlog | non-blocking |

- States, ownership and closure evidence follow `DOC-TST-002` §10 (NEW → TRIAGED → … → CLOSED; closure requires a re-run of the failing check).
- **Waivers:** any deferred a11y defect needs written risk acceptance in `17-risk-management/risk-register.md`, naming the AC it delays, the affected surface and a remediation date; a waiver **expires** at the earlier of 90 days or the next minor release (`INFERENCE`), then either re-waived explicitly or the defect re-enters the blocking state. Silent suppressions in scan output are forbidden (pattern of `AC-SR012-04`).
- Accessibility regressions are release blockers by canon (`DOC-UX-006` §8.5).

## 7. Arabic / RTL Accessibility Specifics

Design rules live in `../../11-ui-ux/core/localization.md` (`DOC-UX-007`) and `../../05-frontend/core/rtl-and-styling.md` (`DOC-FE-007`); this file only fixes what gets *tested*:

| Aspect | Measurable check |
|---|---|
| Arabic-Indic numerals in `ar` UI (canon: `BR-PAY-10`) | TalkBack/VoiceOver must pronounce display digits as numbers — sample strings such as "١٥٬٠٠٠ ريال يمني" read correctly in SR sessions; no digit pronounced as isolated glyphs |
| Mixed `ar`/`en` strings (product names, phone `^7[0-9]{8}$`) | LTR islands (`dir="ltr"`) keep SR reading order intact; 0 bidi-broken labels on audited pages |
| Logical CSS / mirrored focus | focus ring, dropdowns and scrollers open from the logical start edge; SR focus order = visual RTL order (0 defects, §3 #10) |
| Locale switch mid-session | `lang` attribute updates; SR pronunciation switches on the same screen (checklist per `DOC-UX-006` §4) |

## 8. Verification & Evidence

| Element | Reference |
|---|---|
| Executable plan | `../../13-testing/core/test-plans.md` §e (Accessibility Plan, `DOC-TST-003`) — automation, contrast audit, keyboard run, SR pass, structural checks |
| Manual checklist | `../../11-ui-ux/core/accessibility.md` §10 (`DOC-UX-006`), executed per locale per surface |
| AC links (verified IDs) | `AC-NFR-011-01` (automated report: ≥95%, 0 critical/serious, both locales) · `AC-NFR-011-02` (keyboard + SR completion with recordings) · both roll up to `AC-S-10`; RTL reading-order evidence also serves `AC-S-11` / `AC-XCUT-03` step 6; defect gate `AC-S-07` |
| Evidence artifacts | axe JSON/HTML reports and Lighthouse a11y scores as CI artifacts; SR session recordings + keyboard-run notes filed with the `13-testing/` release report (same convention as k6 reports, `DOC-NFD-002` §6); audit report for full audits |
| External claim | accessibility statement (WCAG 2.1 AA claim scope) is a legal deliverable — `DOC-NFD-007` §5 row 9, worded strictly from the evidence above |
| Status | **DESIGNED** — no code, no CI job, no scan or recording exists yet (pre-implementation project, root README §6) |

## 9. Known Limitations & Risks

| # | Limitation / risk | Impact | Handling |
|---|---|---|---|
| 1 | Vendor-generated alt-text quality: the `DQ-01…DQ-18` register (`16-data/data-quality.md`, `DOC-DTA-007`) has **no alt-text rule** — only `DQ-02`'s "≥1 image" | screen-reader users get empty or meaningless product descriptions | platform prompts vendors at upload + automated non-empty check at publish (§3 #7); propose a completeness rule to the DQ register owner as a candidate extension (`INFERENCE` — no rule assigned yet); moderation/sampling as backstop |
| 2 | RN third-party components (bottom sheets, keyboards, carousels) may ship inaccessible defaults | S4/S5 gaps invisible to axe-web | wrapper components own `accessibilityRole`/`accessibilityLabel`; per-release SR pass (`DOC-UX-006` §4 RN parity row) |
| 3 | Admin-console (S3) internal-tool pressure: dense audit tables and bulk actions are expensive to make fully operable | scope-creep exemptions becoming permanent | **no blanket exemption** — `FR-020` requires an accessible admin UI; only low-priority affordances inside `should`-phase flows may be waived, and only per §6 waiver with expiry |
| 4 | NVDA/desktop ATs are not named in NFR-011 | a `should`, not a gate | `INFERENCE` extension (§4); reclassify to `must` only via NFR change |
| 5 | Low-bandwidth interplay: Arabic webfonts are a shared budget item (Arabic + Latin ≤ **150 KB** combined, `DOC-NFD-002` §2 / `AC-NFR-002-02`) | pressure to trim/subset fonts can degrade Arabic legibility and contrast fallbacks | a11y font rules (≥12 px min, Arabic line-height 1.7) hold; `font-display: swap` FOUT checked in the contrast/resize passes — never traded away for bytes |
| 6 | Video/audio absent in v1 → captions (SC 1.2) untested | criterion silently unmaintained if media is added | explicit out-of-scope row (§3 #13); adoption requires a missing-information entry first (`DOC-UX-006` §7) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
