---
document_id: DOC-NFD-008
title: Usability & Support Detail — Task Efficiency, Localization Gates & Human Support Ops
category: 12-non-functional
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [NFR-012, NFR-013, NFR-011, NFR-002, FR-020, FR-001, FR-004, FR-007, FR-011, BR-ORD-10, BR-SHP-03, BR-SHP-06]
related_documents: [DOC-NFD-001, DOC-NFR-012, DOC-NFR-013, DOC-AC-001, DOC-UX-005, DOC-UX-006, DOC-UX-007, DOC-UX-008, DOC-FE-008]
---

# Usability & Support Detail — Task Efficiency, Localization Gates & Human Support Ops

Elaborates **NFR-012 (core-task efficiency), NFR-013 (bilingual UX)** and the operational support model behind **`AC-S-23`** / **`NFR-020`** (support resolves issues with tooling, not code changes). Requirement statements stay in `02-requirements/`; UX patterns live in `11-ui-ux/` (DOC-UX-005/006/007). This file adds the task matrix, device/bandwidth envelope, locale quality gates, support SLAs and the feedback loop.

## 1. Task-Efficiency Matrix (measures behind NFR-012)

| # | Task (persona) | Target (median, `ar`, mid-tier Android on 4G) | Success gate | AC |
|---|---|---|---|---|
| T1 | Register → OTP verified (customer) | ≤ 90 s (`INFERENCE` split) | part of T2 chain | `AC-NFR-012-01` |
| T2 | Registration → **first paid order** (customer) | **< 5 min** | ≥ 90% success | `AC-NFR-012-01` |
| T3 | Wallet top-up via available rail (customer) | ≤ 2 min (`INFERENCE`) | ≥ 90% success | `AC-NFR-012-01` |
| T4 | Search → open product (customer) | ≤ 45 s (`INFERENCE`) | ≥ 90% success | `AC-NFR-012-01` |
| T5 | Add to cart → checkout (customer) | ≤ 90 s (`INFERENCE`) | ≥ 90% success | `AC-NFR-012-01` |
| T6 | Track order status (customer) | ≤ 30 s (`INFERENCE`) | ≥ 90% success | `AC-NFR-012-01` |
| T7 | Request return (customer) | ≤ 3 min (`INFERENCE`) | ≥ 90% success | `AC-NFR-012-01` |
| T8 | Account → **first published listing** (vendor, incl. image upload + pricing) | **< 10 min** | ≥ 90%; SUS ≥ 78 | `AC-NFR-012-02` |
| T9 | Admin: resolve a dispute with full context (admin) | ≤ 3 min (`INFERENCE`) | SUS ≥ 78 per persona | `AC-NFR-012-02` |

Method: moderated sessions, **≥ 5 participants per persona**, real devices, stopwatch timing recorded in `13-testing/`; Arabic round is the **measured default** (`C-24`); post-launch funnel analytics (registration → first top-up → first order event gaps) monitor continuously after release.

Cross-cutting gates:

- **Dead-end rule:** every rejected input and failed state offers a next action — 0 unrecoverable dead ends, in both locales (`AC-NFR-012-01`).
- **Inline validation:** 100% of rejected inputs on money/address forms explained in the user's locale **before** submission fails — pattern set in `DOC-UX-005` §4, schemas in `../../05-frontend/core/forms-and-validation.md`.
- **Perceived speed:** each task step's wait states follow `DOC-UX-005` (optimistic cart updates, skeletons < 800 ms, no double-submit) so NFR-001/NFR-002 latency does not surface as friction inside the timed tasks.

## 2. Learnability — no-training operation

| Mechanism | Detail |
|---|---|
| First-run guidance | one-time inline hints (not modals) on wallet, cart, checkout; dismissible, locale-correct, never blocks (`INFERENCE`, consistent with `DOC-UX-008` voice rules) |
| Progressive disclosure | advanced admin/vendor options collapsed until context demands them (contract tiers, notification prefs) |
| Consistent conventions | one navigation model across S1–S5 (`DOC-UX-003`); shared design system (`DOC-UX-004`) means learn-one-learn-all |
| Error teachability | every error message states what happened + what to do next in plain Arabic (`DOC-UX-004` §8 voice table) |
| Assist path | human support reachable from within every flow (§5) — abandoning to WhatsApp is always a visible exit (`GAP-03`: no email) |

## 3. Device & Low-Bandwidth Envelope (Yemen context)

| Constraint | Operating rule |
|---|---|
| Reference device | mid-tier Android (2–4 GB RAM), 360 px width, **4G** — the measured default for all NFR-012 sessions and NFR-002 LCP gates |
| Responsive floor | 320 px usable, **no horizontal scroll at 360 px**, up to ≥ 1440 px (`NFR-015`) |
| Data-saver mode | auto-serve WebP/AVIF with ≤ 200 KB per catalog image (`INFERENCE` bounds), lazy-load below the fold, defer non-critical video — LCP budget in `DOC-NFD-002` §2 still applies |
| Flaky network | 3G-threshold degradation drill: browse + cart must remain operable with 500 ms RTT / 40% packet loss (`INFERENCE`); OTP retry UX handles SMS delay (cooldown UI in `DOC-UX-005`) |
| Offline/partial | connection-loss states per `DOC-UX-005` §5; money forms never silently drop input |
| Out-of-support devices | graceful message on critical flows, **0 data-corrupting failures** (`NFR-015`) |

## 4. Localization Quality Gates (detail beyond NFR-013)

| Gate | Check | When |
|---|---|---|
| Locale default | browser/app locale decides; default `ar` (`C-24`); manual switch persists (`DOC-UX-003` §5) | release |
| Parity inventory | **every user-facing string** resolved in both locales — 0 fallback-to-`en` visible in `ar` QA pass | release (`AC-NFR-013-*`) |
| Numeric formats | Arabic-Indic digits rendered in `ar`, Latin in `en`; normalization at input (`DOC-UX-007` §4, `BR-PAY-10`) | automated + spot QA |
| Currency | integer YER everywhere, `ر.ي` / `YER` suffix by locale; no floating point | contract tests |
| Dates/times | locale calendars, day-month order, 24 h (`DOC-UX-007` §5) | spot QA |
| RTL regression | mirroring correctness set: forms, tables, modals, chips, timeline, maps-to-code — run against `../../05-frontend/core/rtl-and-styling.md` (`DOC-FE-007`) | every PR (visual) + release |
| Layout integrity | Arabic text expansion ≥ 30% must not clip/overlap any component (`INFERENCE` bound) | visual QA pass |
| Legal/tax text | translated; authoritative version noted on page (`DOC-FE-008`) | release |
| Template coverage | notification templates (SMS/WhatsApp/push) complete in both locales, provider-approved (`BR-NTF-04`, `DEP-06`) | before launch |
| Accessibility × locale | WCAG checks run **per locale** (`NFR-011` depends on `NFR-013`) | axe pass per locale |

Evidence lands in `13-testing/` locale suites and the pre-release QA checklist; acceptance: `AC-NFR-013-*`.

## 5. Support Model — human-only operations

| Element | Spec | Canon |
|---|---|---|
| Channels | in-app ticket (primary) + WhatsApp/SMS replies (existing channels); **no email** (`GAP-03`), **no AI chatbot in v1** | project scope; `FR-020` out-of-scope note; `DOC-UX-008` §2 |
| Ticket subjects | order dispute, return, payment/top-up, delivery/code lockout, account/KYC, listing/catalog, other — bilingual templates | `FR-020` |
| Agent tooling | admin console (S3) resolves: verify top-up, freeze wallet, resolve dispute, unlock code lockout, KYC decisions, order state override **within the 17-state table** — **0 code changes for common issues** (operability objective of `NFR-020`) | `FR-020`, `C-09` |
| Auto-created escalation tickets | 24 h CONFIRMED SLA breach (`BR-ORD-10`), 3rd failed delivery-code attempt (`BR-SHP-03` → 24 h lock), 3 failed delivery attempts (`BR-SHP-06`) — each carries the **full order timeline** | `FR-020`, `AC-FR020-04` |
| Audit | every support/admin decision writes an append-only audit entry (actor, action, before/after, IP, timestamp) | `BR-PLT-06`, `SEC-REQ-010` |
| Escalation ladder | agent → senior agent → admin (dispute arbiter, `BR-RET-06`) → sponsor for policy gaps | `INFERENCE` |
| Privacy in tickets | agents see masked PII consistent with classification; no full wallet numbers in free text | `16-data/data-classification.md`, `SEC-REQ-007` |

### Support SLAs

| Severity | Definition | First response | Resolution target | Route |
|---|---|---|---|---|
| S1 | money stuck / payment debited without order / locked wallet | ≤ 30 min (`INFERENCE`) | ≤ 4 h, escalate if not | on-call + finance admin |
| S2 | order failure, delivery dispute, code lockout, KYC blocking listing | ≤ 2 h | ≤ 24 h (KYC decision ≤ 48 h, `BR-VND-03`) | ticket queue |
| S3 | catalog, account, how-to questions | ≤ 8 h | ≤ 48 h | ticket queue |
| S4 | feature feedback / improvement ideas | next business day | backlog triage | → §6 feedback loop |

Targets are `INFERENCE` (not canon) and must be confirmed against sponsor capacity at launch readiness; `BR-VND-03`'s 48-hour KYC SLA is `VERIFIED` and never exceeded.

## 6. CSAT & Continuous-Improvement Loop

| Signal | Collection | Action |
|---|---|---|
| Post-resolution CSAT (1–5) | in-ticket rating after close (`INFERENCE` persona: ≥ 4.0 target) | monthly report; S1/S2 < 4.0 → incident review |
| Task-time funnel | analytics: registration → top-up → first-order timestamps | watch vs §1 targets post-launch; breach → UX ticket |
| Abandon points | funnel drop-offs per step + error-message clicks | routed to `../../11-ui-ux/core/screen-states.md` gaps |
| Ticket taxonomy trends | top-10 ticket reasons per month | product fix if systemic (e.g., OTP confusion → copy fix in `DOC-UX-004` §8) |
| SUS re-run | moderated sessions each minor release or quarterly (`INFERENCE`) | regression below 78 blocks release |
| Usability findings register | session notes filed in `13-testing/` with linked UX-doc updates | docs updated with version bump, never silently |

## 7. Verification Hooks

| Detail | Feeds |
|---|---|
| §1 task matrix timings + ≥ 90% success + 0 dead ends (`ar` round) | `AC-NFR-012-01` |
| §1 vendor task < 10 min + SUS ≥ 78 per persona | `AC-NFR-012-02` |
| §4 locale parity, formats, RTL, per-locale accessibility | `AC-NFR-013-*` |
| §5 support flows operable by staff; auto-escalation tickets with timeline | `AC-S-23`, `AC-FR020-03/04`, `NFR-020` |
| §2/§3 error-path audit + low-bandwidth drill | `AC-NFR-012-01` dead-end rule; supports `AC-NFR-002-01` |
| §3 matrix breadth vs supported devices | `AC-NFR-015-01/02` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
