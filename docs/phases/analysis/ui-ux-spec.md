---
document_id: DOC-PHA-015
title: UI/UX Specification — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-UX-001, DOC-FE-001]
related_requirements: [NFR-002, NFR-011, NFR-013]
---

# UI/UX Specification — analysis phase

## Purpose
CORE-03 item 13: HCI-conformant UI/UX specification for the phase's user-facing scope. Canonical design docs: [`11-ui-ux/`](../../11-ui-ux/README.md) (flows, IA, design system, screen states, accessibility, localization, feedback) + [`05-frontend/`](../../05-frontend/README.md) (architecture, routing, state, forms, RTL).

## Scope
Five shells: customer web (`apps/web-customer`), vendor panel (`apps/web-vendor`), admin console (`apps/web-admin`), customer mobile (`apps/mobile-customer`), courier mobile (`apps/mobile-courier`).

## Actors / roles
The 7 actors ([`actors-and-roles.md`](../../00-project-overview/actors-and-roles.md)) — each shell exposes only its role's capabilities (never relying on hidden UI for security, P1/`SEC-02`).

## Main flow (user journeys)
End-to-end journeys: [`11-ui-ux/user-flows.md`](../../11-ui-ux/user-flows.md) + `WF-001`…`WF-012`. Information architecture and navigation: [`information-architecture.md`](../../11-ui-ux/information-architecture.md). Screen states (loading/empty/error/offline): [`screen-states.md`](../../11-ui-ux/screen-states.md).

## Design system & styling constraints
- Tokens/components: [`design-system.md`](../../11-ui-ux/design-system.md) + `packages/design-tokens`, `packages/ui`.
- **Arabic-first RTL:** `ar` default, logical CSS properties only — `ml-*/mr-*/pl-*/pr-*/left-*/right-*/text-left/text-right/float` fail CI (`RTL-03`); money as `ر.ي` with Arabic-Indic numerals in `ar` (`RTL-04`).
- No hardcoded strings — shared catalogs only, i18n lint fails CI (`RTL-02`).
- Confirmations use the reusable modal component — never `alert/confirm/prompt` (`IMP-04`; validator §6 = 0 today).

## Alternate flows / exception flows
Server error, validation failure, network failure and offline paths are specified per form ([`forms-and-validation.md`](../../05-frontend/forms-and-validation.md)) and screen state; every operation handles success/failure branches (`IMP-05`).

## Postconditions (quality bar)
- Accessibility: **WCAG 2.1 AA**, ≥95% automated pass, 0 critical/serious axe findings (`UI-02`, `NFR-011`).
- Performance: LCP <2.5 s, INP ≤200 ms, CLS ≤0.1, JS <200 KB gzipped (`PRF-02`).
- Responsive across supported breakpoints (`UI-04`).
- Money/order/permission data never stored in client state or SSR'd (`RTL-06`); optimistic updates forbidden for wallet, order placement/state, refund/return, stock (`RTL-07`).

## Data entities touched
Read-models only on the client — authoritative values (wallet balance, order status, totals) always come from the API (`RTL-06`).

## Invariants
Exactly two locales, no machine translation (`C-24`) · no GPS/map UI anywhere (`C-16`) · payment UI shows wallet-only methods (`C-01…C-04`).

## Open questions (COM-01)
1. Courier app proof-photo flow: photo is optional and never required (`BR-SHP-05`) — UI must not nudge it as mandatory; confirm copy in `11-ui-ux/feedback-and-engagement.md` at design time.

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 13, session 005) | analysis-agent |
