---
document_id: DOC-TST-006
title: Test Cases — Layer Index, Anatomy & Locked Allocation
category: 13-testing
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: [FR-001, FR-002, FR-011, FR-012, FR-013]
related_documents: [DOC-TST-001, DOC-TST-002, DOC-TST-003, DOC-TST-004, DOC-TST-005, DOC-AC-001]
---

# Test Cases — Layer Index (TC-001 … TC-114)

Index and authoring standard for the individual test-case files in this directory. The **allocation below is locked**: TC IDs are never renumbered, reused, or reassigned to another domain. Strategy, plans and constraints are in the parent files ([testing-strategy.md](testing-strategy.md), [test-plans.md](test-plans.md), [constraint-tests.md](constraint-tests.md)).

**Files:** one test case per file, named **`TC-NNN.md`** (zero-padded, e.g. `TC-031.md`), with frontmatter `document_id: DOC-TC-NNN`, `category: 13-testing`, `status: approved`, `version: 1.0`, `source_of_truth: false`, and `related_requirements` listing the IDs the case exercises. This README (DOC-TST-006) is the only index of the layer.

---

## 1. Anatomy of a TC File

Every `TC-NNN.md` contains these sections, in this order:

| # | Section | Content rule |
|---|---|---|
| 1 | **Objective** | One or two sentences: the single behavior being proven, phrased as a verifiable claim |
| 2 | **Level** | `unit` \| `integration` \| `e2e` \| `performance` \| `security` \| `a11y` — chosen per strategy §3 (level selection rule) |
| 3 | **Preconditions** | Environment, accounts, seed state, provider mode — must be re-creatable from [test-data-and-environments.md](test-data-and-environments.md) |
| 4 | **Test data** | Table of exact values (phones from the reserved `79xxxxxxx` block, boundary amounts, locale) — never vague sample entries such as a generic user |
| 5 | **Steps** | Numbered, executable actions (endpoint + payload, UI path, or tool command) |
| 6 | **Expected result** | Observable, binary outcomes: status codes, row states, ledger effects — PASS/FAIL with no interpretation |
| 7 | **Related requirements & rules** | `FR/NFR/SEC-REQ/DATA-REQ/INT-REQ`, `BR-*`, `AC-*`, API endpoint IDs |
| 8 | **Constraints** | `C-*` (and `TST-CON-*` when the case feeds one) |
| 9 | **Priority** | P0 (release-blocking journey), P1 (core), P2 (secondary) |
| 10 | **Automation** | `Yes — <tool>` or `No — <reason>` (device-lab/manual judgment) |
| 11 | **Change History** | Standard table (root README §9) |

**Authoring rules:** expectations cite canon (AC/BR/C), never the implementation; every case must map to ≥1 AC or rule (`AC-S-03`); negative cases state the error code and the "nothing persisted" assertion; timing cases use injectable clocks; Arabic-first journeys default to `ar`.

## 2. Locked TC Allocation

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

## 3. Special Semantics

**TC-011–014 — the four authorization concept cases.** These IDs are cited across the repository as the canonical negative-access cases; their meaning is fixed:

| ID | Concept | Expected outcome |
|---|---|---|
| TC-011 | **Cross-user access** — Customer A requests Customer B's resource by ID | 404/403 deny, zero data disclosed (`AC-FR002-01`, SEC-REQ-004) |
| TC-012 | **Cross-store access** — Vendor X's staff acts on Vendor Y's product/store | deny at service layer via `store_id` scoping (`BR-VND-07`, `AC-FR002-02`) |
| TC-013 | **Staff escalation** — vendor staff attempts to change their own role to Owner (or any privileged self-elevation) | rejected; only the Owner changes staff roles (`BR-VND-06`, `AC-FR002-03`) |
| TC-014 | **Direct API bypass** — a Viewer/low-privilege caller calls a write endpoint directly, bypassing the UI | server responds 403/404 — frontend guards are never the security boundary (`AC-FR002-05`, `AC-SR004-03`) |

All four are **P0, automated, and merge-blocking**; they run under security plan §c (SEC-P-05) as well as feature plan PLAN-02.

**TC-031 — canonical cross-reference example.** The repository-wide traceability chain example is `FR-013 → BR-PAY-04 → API-WAL-002 → TC-031 → AC-FR013-01`: bank-transfer top-up credited only after admin verification (`BR-PAY-04`, `AC-IR002-01`). TC-031 anchors the checkout/payment block (TC-031–042) and demonstrates the expected citation density of every TC.

## 4. Coverage Summary

**114 TCs → FR families** (each FR covered by exactly one locked block, ≥ 1 case per AC of that FR inside the block):

| FR family | TC block | Cases | Primary AC evidence |
|---|---|---|---|
| FR-001 Authentication | TC-001–010 | 10 | AC-FR001-01…05, AC-SR001-*, AC-SR003-*, AC-SR005-* |
| FR-002 Authorization | TC-011–014 | 4 | AC-FR002-01…05, AC-SR004-* |
| FR-003 Profile/addresses | (within TC-001–010) + AC execution | — | AC-FR003-01…05 |
| FR-004…FR-010 (catalog → cart) | TC-015–030 | 16 | AC-FR004…AC-FR010 families |
| FR-011 + FR-013 checkout/payment | TC-031–042 | 12 | AC-FR011-01…05, AC-FR013-01…05, AC-S-14/15 |
| FR-012 order lifecycle | TC-043–056 | 14 | AC-FR012-01…05 (17-state coverage with TST-CON-09) |
| FR-014 escrow/commission/payouts | TC-057–064 | 8 | AC-FR014-01…05 |
| FR-015 shipping/delivery | TC-065–074 | 10 | AC-FR015-01…05 (C-16 with TST-CON-16) |
| FR-016 returns/refunds | TC-075–084 | 10 | AC-FR016-01…04 |
| FR-017 notifications | TC-085–090 | 6 | AC-FR017-01…05, AC-IR003-*, AC-IR004-* |
| FR-018 analytics | TC-091–096 | 6 | AC-FR018-01…04 |
| FR-019 content/coupons | TC-097–104 | 8 | AC-FR019-01…04 |
| FR-020 administration/audit | TC-105–114 | 10 | AC-FR020-01…04, AC-SR010-* |

**Non-FR ACs.** `AC-NFR-*`, `AC-SRnnn-*`, `AC-DRnnn-*`, `AC-IRnnn-*` and `AC-XCUT-*` are executed through the executable plans ([test-plans.md](test-plans.md) §b–§h) and the constraint register ([constraint-tests.md](constraint-tests.md)); where a TC also exercises one, the TC cites it in *Related requirements & rules*. `../../19-traceability/core/requirements-to-tests.md` records the full AC → artifact matrix with zero gaps (`AC-S-03`); total TC count remains **114**.

## 5. Writing Workflow

1. A TC is authored only inside its locked range — if the range is full, the case competes for priority within the block; IDs never shift.
2. Draft (`status: draft` is not used at v1.0 — files are `approved` on creation) → peer review against §1 anatomy → automation implemented in CI → linked from `19-traceability/`.
3. If canon changes (AC/BR/C edited), the TC must be updated in the same change set or recorded as a defect against the plan.
4. Failing behavior discovered while writing a TC is filed as a defect with the TC ID — the TC itself is never weakened to make code pass.

**Citation skeleton (every TC follows this shape):**

```text
Related requirements & rules: FR-0NN, SEC-REQ-0NN, BR-XXX-nn, AC-FR0NN-nn, API-<GRP>-NNN
Constraints: C-NN (+ TST-CON-NN when the case feeds the constraint register)
Priority: P0 | P1 | P2        Automation: Yes — <tool> | No — <reason>
```

**Layer boundaries:** a TC never restates what [constraint-tests.md](constraint-tests.md) defines (it may cite `TST-CON-NN`), never duplicates a plan's schedule ([test-plans.md](test-plans.md)), and never redefines fixture values ([test-data-and-environments.md](test-data-and-environments.md)) — it references them. Each layer has exactly one owner: TC files own case-level detail only.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
