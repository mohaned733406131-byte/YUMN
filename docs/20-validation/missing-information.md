---
document_id: DOC-VAL-002
title: AUD-03 — Missing Information (GAP register GAP-01…GAP-12)
category: 20-validation
status: approved
version: 1.1
created: 2026-09-27
updated: 2026-09-27
author: analysis-agent
source_of_truth: true
related_requirements: [FR-013, FR-014, FR-017, NFR-019, INT-REQ-001]
related_documents: [DOC-ROOT-001, DOC-TPL-011, DOC-OVR-005, DOC-GL-003, DOC-CMP-004, DOC-NFD-007, DOC-DTA-005, DOC-INT-002, DOC-DTA-003, DOC-SEC-008]
---

# AUD-03 — Missing Information (GAP register)

| Field | Value |
|---|---|
| **Audit ID** | `AUD-03` |
| **Type** | missing-information |
| **Date** | 2026-09-27 |
| **Scope** | every unresolved question in `docs/` that canon points at `20-validation/missing-information.md`: the `GAP-NN` series plus every "record it when that register is authored" promise found by full-text sweep of all 433 `.md` files |
| **Method** | (a) full-text sweep for `missing-information` / `GAP-` across `docs/`; (b) read each promise site and each `GAP-*` definition site; (c) reconcile against `00-project-overview/project-scope.md` §UNCERTAIN SCOPE and `22-glossary/naming-conventions.md` §3.2; (d) re-count citations per GAP ID |
| **Auditor** | analysis-agent |

**Rule:** this file is the only place a `GAP-NN` may be minted (root README §5:161; `naming-conventions.md:90`). A gap is a *missing fact*, not a defect — defects go to `consistency-audit.md`/`contradiction-audit.md`. Gaps are never silently assumed away (`22-glossary/terminology.md:71`).

---

## 1. Register

| ID | Question / missing information | Needed from (owner) | Status | Blocks (gate / phase) | Minted by — source | Evidence |
|---|---|---|---|---|---|---|
| `GAP-01` | Growth/commercial targets for launch (vendor/order/GMV) | Sponsor | `OPEN` | Gate 0 check 0.5 (triage); Gate 2 check 2.5 (launch claims) | `project-scope.md:80` | `VERIFIED` |
| `GAP-02` | Whether admin can override a delivery code in exceptional cases | Operations | `OPEN` | Gate 0 check 0.5 | `project-scope.md:81`; `11-ui-ux/user-flows.md:127` (override policy `INSUFFICIENT EVIDENCE`) | `VERIFIED` |
| `GAP-03` | Email notification channel: include or exclude? | Product owner | `OPEN` | Gate 0 check 0.5; any email-dependent claim | `project-scope.md:82`; `01-business-analysis/business-rules.md:143` (`BR-NTF-01`) | `VERIFIED` |
| `GAP-04` | Loyalty program depth (tiers only vs points accrual/redemption) | Product owner | `OPEN` | Gate 0 check 0.5 | `project-scope.md:83` | `VERIFIED` |
| `GAP-05` | Vendor subscription/tiered commission plans (vs flat 5–20%) | Finance | `OPEN` | Gate 2 check 2.5 (before tiered plans ship) | `project-scope.md:84`; `21-completion/quality-gates.md:133` | `VERIFIED` |
| `GAP-06` | Cash-out (wallet → bank) for vendors: automatic or admin-approved only? | Finance | `OPEN` | Gate 2 check 2.5 | `project-scope.md:85`; `21-completion/quality-gates.md:133` | `VERIFIED` |
| `GAP-07` | Logistics partners beyond individual couriers (fleet operators) | Operations lead (`RISK-018` owner) | `OPEN` | Post-launch mitigation (`RISK-018` action) | `00-project-overview/stakeholders.md:48`; `17-risk-management/risk-register.md:42`, `:442` — **never minted in `project-scope.md`**, registered here | `VERIFIED` (existence) / `INFERENCE` (owner) |
| `GAP-08` | Precise statutory data-retention obligations applicable in Yemen | Legal liaison, via `DEP-09` / `ASM-13` | `OPEN` | Gate 2 check 2.4 (`AC-S-24` evidence pack) | **minted by this audit** — `16-data/retention-and-archival.md:39` | `VERIFIED` |
| `GAP-09` | Unresolved blocking legal deliverables — esp. the Central Bank wallet position (`DEP-10`, `ASM-12`), plus the VAT opinion (`DEP-09`, `ASM-10`) | Legal liaison + sponsor | `OPEN` | Gate 0 check 0.4 (before money build); Gate 2 checks 2.4 and launch hard-stops | **minted by this audit** — `12-non-functional/compliance-and-legal.md:88`; `17-risk-management/risk-register.md:147`; `21-completion/quality-gates.md:79`, `:132`, `:143` | `VERIFIED` |
| `GAP-10` | Exact provider API specifications (endpoint paths, signature header names, field names) for m-Floos / OneCash — unavailable while `DEP-05` is `NOT STARTED` | Technical lead / integrations, via `DEP-05` | `OPEN` | Gate 0 check 0.3 | **minted by this audit** — `10-integrations/wallet-providers.md:19`; `10-integrations/testing-and-sandboxes.md:130` | `VERIFIED` |
| `GAP-11` | Hosting / cross-border data-location decision (whether Yemeni Law No. 11 of 2012 applies) | Project sponsor | `OPEN` | Before launch; `DEP-09` / `ASM-13`; may force an ADR | **minted by this audit** — `16-data/data-ownership.md:99` | `VERIFIED` |
| `GAP-12` | v2 account-recovery channel beyond SMS/WhatsApp (auth-channel concentration) | Security officer | `OPEN` | Post-v1 (recommendation, not a v1 gate) | **minted by this audit** — `09-security/security-findings.md:48` (`SEC-001` recommendation) | `VERIFIED` |

Status vocabulary for this register: `OPEN` → `RESOLVED` (answer recorded here + owning document changed, version bumped, root README §9.2) or `WAIVED` (sponsor writes an explicit decision that the question stays unanswered for v1). All twelve rows are `OPEN` at 2026-09-27.

---

## 2. Gap Notes (evidence, not answers)

- **`GAP-01…GAP-06` are inherited verbatim** — ID, item wording, and "Needed From" owner are copied from `00-project-overview/project-scope.md:80-85`; this file does not restate or reinterpret them (root README §4: cite, don't restate).
- **`GAP-07` was promised but never minted.** `risk-register.md:284` and `:299` speak of "seven open gaps (`GAP-01…GAP-07`)" and `stakeholders.md:48` tags the fleet-operator omission `GAP-07`, yet `project-scope.md` lists only six rows. Registering it here closes the numbering hole; the owner is taken from `risk-register.md:42` (`RISK-018`, Operations lead) → `INFERENCE`.
- **`GAP-03` has hard evidence behind its two sides:** `08-database/constraints-and-integrity.md` (`notification_channel` = `SMS, WHATSAPP, IN_APP, PUSH`, explicitly "**no `EMAIL` value**") and `BR-NTF-01` (`business-rules.md:143`) vs the email rows still described in `12-non-functional/` messaging prose. The gap stays the *decision*, not the channel inventory.
- **`GAP-08…GAP-12` are minted here because canon promised them to this register:** each source sentence explicitly defers "record it in `20-validation/missing-information.md`" (and, for `GAP-08`/`GAP-09`, forbids minting the ID anywhere else — `retention-and-archival.md:39`: "No new `GAP-NNN` ID is minted here — gap IDs are assigned only in the canonical GAP register"). One gap per promise site; no promise was merged or dropped.
- **Why `GAP-09` and `GAP-11` are separate rows:** `compliance-and-legal.md:88` is a *deliverables* gap (ten sign-off items, esp. item 2), while `data-ownership.md:99` is a *design-forcing* location decision that "must be confirmed by the sponsor before launch and … if it changes the design, in an ADR". They have different owners and different gate checks, so they are tracked separately.

---

## 3. Findings

| # | Finding | Severity | Where (file §section) | Evidence (IDs / tags) | Status |
|---|---|---|---|---|---|
| 1 | Canonical GAP register location is claimed twice — this file vs `project-scope.md` §UNCERTAIN SCOPE | `MEDIUM` | root README §5:161 + `naming-conventions.md:90` vs `retention-and-archival.md:39` + `compliance-and-legal.md:88` | `CT-15` in `contradiction-audit.md` — `VERIFIED` | `OPEN` |
| 2 | `GAP-07` is cited (16 files) but was never minted in the source register | `MEDIUM` | `00-project-overview/project-scope.md:80-85` | cited by `stakeholders.md:48`, `risk-register.md:42`, `risk-register.md:442`, `17-risk-management/README.md:109`, `21-completion/quality-gates.md:80` — `VERIFIED` | `OPEN` (row added here; source register still shows six rows) |
| 3 | `21-completion/quality-gates.md:80` requires "`GAP-01…GAP-07` dispositioned with owners" while `risk-register.md:35` action says "Resolve `GAP-01…GAP-06` decisions before Gate 0" | `LOW` | `21-completion/quality-gates.md:80` vs `17-risk-management/risk-register.md:35` | scope of the Gate-0 GAP set differs by one ID — `VERIFIED` | `OPEN` |
| 4 | Twelve promised-but-unregistered gaps existed at sweep time (register had 0 rows) | `MEDIUM` | all promise sites listed §1 | `GAP-08…GAP-12` minted by this run; `GAP-07` adopted — `VERIFIED` | `RESOLVED` by this document (register now populated) |
| 5 | Glossary rule says a term with no `22-glossary/terminology.md` row is "a missing-information finding for `20-validation/missing-information.md`" — 3 of 15 sampled terms have no row | `LOW` | `22-glossary/README.md:46` | sampled terms `outbox`, `saga`, `anonymization` absent from `terminology.md` (147 lines) — `VERIFIED`; full sweep not run → scope `INFERENCE` | `OPEN` (see §4 — not minted) |

---

## 4. Considered, deliberately **not** minted

| Candidate | Why no `GAP-NN` |
|---|---|
| 88 `<angle-bracket>` tokens outside `23-templates/` (35 files) | DOC-TPL-001 §2.3 makes *leftover template placeholders* a validation finding here; manual sample shows these are notation (`<column>`, `<n>`, `<uuid>`, `<encoded>`), not unfilled placeholders — so the trigger condition is not established. Recorded as a consistency finding instead; owner `23-templates/`/root README to disambiguate notation from placeholder. |
| "Pre-recorded captions if video/audio is ever added" (`11-ui-ux/accessibility.md:148`, `12-non-functional/accessibility.md:137`) | Conditional rule, not an open question — no v1 decision is pending. |
| `A-07` "undefined" claim (`naming-conventions.md:121`) | Not a gap: the asset exists (`09-security/threat-model.md:29`), so this is a **contradiction** — `CT-17` in `contradiction-audit.md`. |
| Missing `related_requirements:` on root README; missing `## Change History` on 64 files | Documentation defects → `consistency-audit.md` findings 1–2, not missing information. (`19-traceability/` sat in this cell at v1.0 as a path-existence defect; it was authored 2026-09-27 and finding 3 flipped to `RESOLVED`.) |

---

## 5. Coverage & Statistics

- Files examined: **433 of 433** `.md` files swept for `missing-information` / `GAP-` (26 files cite the register by path; `hallucination-audit.md` 2, `critical-findings.md` 5, `analysis-validation.md` 7, `requirements-validation.md` 1).
- Checks run: **4** — passed 1 (`GAP-01…GAP-06` wording/owner fidelity), failed 3 (register location, `GAP-07` never minted, Gate-0 set size).
- ID references verified: **all `GAP-*` citations in `docs/`** resolve after this run; before it, `GAP-07` had **0 definition sites**.
- Series in scope: `GAP-NN` issued 12 · open 12 · resolved 0 · waived 0.
- New IDs minted by this audit: **`GAP-08`, `GAP-09`, `GAP-10`, `GAP-11`, `GAP-12`** (5). No other series touched.

---

## 6. Verdict & Sign-off

- **Gate:** `PASS WITH FINDINGS` (root README §11) — the register now exists and every promised item is recorded; five questions remain unanswered and are owners' work, not documentation defects.
- **Unresolved contradictions / gaps:** `GAP-01…GAP-12` all `OPEN`; `CT-15` (register location) `OPEN` in `contradiction-audit.md`.
- **Required follow-up (edits NOT made here):** `00-project-overview/project-scope.md` §UNCERTAIN SCOPE needs a `GAP-07` row (and, if the location conflict is resolved in favour of this file, an `→ 20-validation/missing-information.md` pointer for `GAP-08…GAP-12`); `21-completion/quality-gates.md:80` / `risk-register.md:35` need one agreed GAP set for Gate 0; `22-glossary/terminology.md` needs rows for the three sampled terms or a recorded decision that they stay out.
- **Sign-off:** analysis-agent, 2026-09-27 (document authorship; gate sign-off remains with the roles named above).

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-27 | Initial authoring; `AUD-03` run; `GAP-01…GAP-07` registered from canon sources; `GAP-08…GAP-12` minted for promised-but-unregistered items | Root README §10 item 41; `naming-conventions.md:90`; `DOC-TPL-011` |
| 1.1 | 2026-09-27 | §4 "considered, not minted" cell corrected: `19-traceability/` was authored after the run — moved out with a pointer to consistency-audit finding 3 (`RESOLVED`) | Findings never deleted; sibling authoring pass landed after v1.0 |
