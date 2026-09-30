---
document_id: DOC-UX-001
title: UI/UX Domain — Overview, Design Principles & File Index
category: 11-ui-ux
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-011, NFR-012, NFR-013, FR-001, FR-010, FR-011, FR-013, FR-015, FR-017, FR-019, FR-020]
related_documents: [DOC-ROOT-001, DOC-REQ-001, DOC-AC-001, DOC-OVR-008, DOC-OVR-002, DOC-BA-005, DOC-UC-000, DOC-WF-001, DOC-FE-001]
---

# UI/UX Domain — Overview, Design Principles & File Index

## 1. Purpose & Scope

This domain captures the **design intent** for all yumn surfaces: what the user experiences, why, and under which rules — before any code is written. It is the bridge between the requirements (`02-requirements/`), the business behavior (`01-business-analysis/`) and the frontend implementation (`05-frontend/`).

**In scope here:** user flows, information architecture, design system (tokens, components, voice), screen states, UX accessibility patterns, content/localization rules, and feedback/engagement design.

**Out of scope here (owned elsewhere):**

| Concern | Owner |
|---|---|
| Component code, CSS mechanics (Tailwind, logical properties), routing implementation | `05-frontend/` (`DOC-FE-001`…`DOC-FE-009`) |
| i18n libraries, catalogs, locale routing mechanics | `../05-frontend/core/internationalization.md` (`DOC-FE-008`) |
| Measurable accessibility targets & metrics | `12-non-functional/` (NFR-011 elaboration) |
| Requirement statements & acceptance criteria | `02-requirements/` (`DOC-REQ-001`, `DOC-AC-001`) |
| Order state machine semantics (17 states) | `../03-system-analysis/core/state-transitions.md` (`DOC-SA-010`) |

> Evidence rule applied throughout: statements are `VERIFIED` (traceable to canon), `INFERENCE` (derived design judgment), or `INSUFFICIENT EVIDENCE` (registered as a gap). Design choices not fixed by canon are tagged `INFERENCE`.

## 2. Design Principles

These principles govern every decision in this directory. They are ordered by precedence.

### P1 — Arabic-first, RTL-native (`C-24`, `OBJ-03`) — `VERIFIED`

Arabic (`ar`) is the default locale on every surface; layout is RTL from the first pixel, not mirrored after the fact. English (`en`) is full parity, never a stripped-down fallback. Design artifacts here are authored in Arabic first; English is a translation with parity obligations (`NFR-013`). Directional elements (icons, progress, focus order, scroll edges) mirror; numeric, code and phone content stays in LTR islands (`DOC-FE-007`).

### P2 — Trust and transparency for wallet money (`C-01`, `C-12`, `OBJ-02`) — `VERIFIED` intent, `INFERENCE` on expression

yumn holds real money: prepaid wallet balances, 7-day escrow, refunds. The customer has no cash-in-hand safety net, so **every screen touching money must show where the money is, where it is going, and what happens next**: balance changes show a transaction row immediately; checkout shows the full breakdown (items − discount + VAT 15% + shipping) before confirm; escrow is explained in plain language ("your money is held safely until you receive the order") wherever payment is taken (`BR-FIN-01`, `BR-ESC-01`). Money screens never use playful tone. *(`INFERENCE`: expression of the trust requirement as microcopy and disclosure patterns.)*

### P3 — Low-bandwidth empathy (Yemen network conditions) — `INFERENCE`

The dominant access profile is a mid-tier Android on variable mobile data (`ASM-01`, NFR-002 target device class). Design consequences: skeleton-first loading (never blank screens), progressive disclosure of heavy media, images with intrinsic dimensions and lightweight placeholders, offline/degraded states that preserve user work, and copy that does not punish slow networks (no "something went wrong" for a merely slow request). Performance budgets are enforced in `12-non-functional/performance.md`; the *UX treatment* of slowness is defined here (`screen-states.md`).

### P4 — Progressive disclosure over density

Customers get one decision per checkout step (`FR-011` seven-step session); vendor and admin panels reveal detail on demand. No screen requires training to complete its primary task (`NFR-012`: registration → first order < 5 min, vendor → first listing < 10 min).

### P5 — Recovery, never dead ends

Every error state offers at least one next action (retry, edit input, contact support, go back). `NFR-012` requires **0 unrecoverable dead ends** across the 8 core tasks; `screen-states.md` is the registry of recovery affordances.

### P6 — One shared vocabulary for order states

All four surface families render the same 17 states (`C-09`, `DOC-SA-010`) with the same label, badge and icon semantics (`design-system.md` §6). Users, vendors, couriers and admins never see different words for the same state.

### P7 — Accessibility is a design output, not a build step

Keyboard order, focus visibility, contrast and screen-reader semantics are specified in `accessibility.md` and are part of the design deliverable, per `NFR-011` (WCAG 2.1 Level AA).

## 3. Surface Register (who this design serves)

| ID | Surface | Client | Primary actors | UX character |
|---|---|---|---|---|
| S1 | Customer web storefront | Next.js 14 | ACT-01 (+ guest) | Mobile-first, transactional, trust-forward |
| S2 | Vendor panel | Next.js 14 | ACT-02 (Owner/Editor/Manager/Viewer) | Dense operational dashboard |
| S3 | Admin console | Next.js 14 | ACT-04, ACT-05, ACT-06 | Data-heavy queues, auditable actions |
| S4 | Customer mobile app | RN 0.73 | ACT-01 | One-handed, thumb-zone primary actions |
| S5 | Courier mobile app | RN 0.73 | ACT-03 | Field-usable: large targets, 6-digit code entry |

`System` (ACT-07) has no UI; it drives notifications and jobs consumed by the other surfaces.

## 4. File Index

| # | File | document_id | Content | source_of_truth |
|---|---|---|---|---|
| 0 | `README.md` | DOC-UX-001 | This file: principles, surface register, index | true |
| 1 | `user-flows.md` | DOC-UX-002 | 9 critical flows, numbered steps + decision points, mapped to `UC-*`/`WF-*` | false |
| 2 | `information-architecture.md` | DOC-UX-003 | Sitemaps, navigation, account/vendor/admin structures, URL↔screen map, B0x mapping | true |
| 3 | `design-system.md` | DOC-UX-004 | Tokens (color/type/spacing/elevation), core components, 17-state badge map, voice & tone | true |
| 4 | `screen-states.md` | DOC-UX-005 | Loading/empty/error/offline/partial/validation/success states per screen type; wallet, OTP and delivery-code state machines | false |
| 5 | `accessibility.md` | DOC-UX-006 | UX accessibility patterns for WCAG 2.1 AA (`NFR-011`), touch targets, contrast table, testing checklist | false |
| 6 | `localization.md` | DOC-UX-007 | Content & translation rules: what is translated, numerals, dates, currency, plurals, tone | false |
| 7 | `feedback-and-engagement.md` | DOC-UX-008 | Notification preference UX, notification center, promotions, review solicitation, trust signals, support entry points | false |

## 5. How This Domain Connects

```text
01-business-analysis (UC/WF/BR) ──► 11-ui-ux (flows, states, screens) ──► 05-frontend (code)
02-requirements (FR/NFR)        ──► 11-ui-ux (design intent)          ──► 13-testing (UX checks)
11-ui-ux/design-system.md       ──► DEP-11 brand tokens (feeds frontend build)
11-ui-ux/accessibility.md       ──► checklist executed by 13-testing + NFR-011 measurement in 12-non-functional
```

- **Upstream inputs (read, never modified here):** `DOC-REQ-001` (FR/NFR IDs), `DOC-BA-005` (BR IDs), `DOC-OVR-008` (C-01…C-26), `DOC-UC-000` / `DOC-WF-001` (flows), `DOC-SA-010` (17 states), `DOC-AC-001` (AC IDs).
- **Downstream consumers:** `05-frontend/` (implements what is specified here), `13-testing/` (visual regression, RTL sweeps, accessibility checklist), `19-traceability/` (design → FR/BR → test mapping).

## 6. Rules for Authors of Files in This Domain

1. Cross-reference by ID (`FR-*`, `NFR-*`, `BR-*`, `C-*`, `UC-*`, `WF-*`, `AC-*`) — never restate a definition owned elsewhere.
2. No placeholders: every statement is a concrete, testable design decision or an explicitly tagged `INFERENCE`/`INSUFFICIENT EVIDENCE` item.
3. Never contradict canon. If canon and a design wish conflict, canon wins and the wish is recorded as a gap in `20-validation/missing-information.md`.
4. Arabic-first: any example string shows the `ar` wording with its `en` counterpart.
5. New screens must appear in `information-architecture.md` and their states in `screen-states.md` in the same change (consistency rule, root README §9).

## 7. Design Completeness Gate

A screen is design-complete only when it has: (a) an IA location and URL (`DOC-UX-003`), (b) a flow entry (`DOC-UX-002`), (c) all states specified (`DOC-UX-005`), (d) component/token usage only (`DOC-UX-004`), (e) accessibility attributes (`DOC-UX-006`), (f) `ar` and `en` copy (`DOC-UX-007`). This gate feeds `21-completion/quality-gates.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
