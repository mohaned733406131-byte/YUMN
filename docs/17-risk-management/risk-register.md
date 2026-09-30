---
document_id: DOC-RSK-002
title: Risk Register (RISK-001 … RISK-024)
category: 17-risk-management
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-008, NFR-005, FR-013, FR-001, SEC-REQ-012, INT-REQ-001, INT-REQ-003, DATA-REQ-007]
related_documents: [DOC-RSK-001, DOC-RSK-003, DOC-RSK-004, DOC-OVR-003, DOC-OVR-009, DOC-OVR-010, DOC-SEC-008]
---

# Risk Register — RISK-001 … RISK-024 (DOC-RSK-002)

Canonical register for yumn. Scoring model, categories, ranking rule and response strategies are defined in `README.md` (DOC-RSK-001) and are not repeated here. **All 24 risks are `OPEN`** — no implementation exists yet, so no mitigation has produced evidence. Rows are listed in ID order; ranking for "top N" purposes uses score ↓ → impact ↓ → ID ↑ (DOC-RSK-001 §3.3).

The first three rows are the entries mirrored in `00-project-overview/project-charter.md` §Summary of Major Risks (titles and severities identical by design).

## 1. Summary Table

| ID | Title | Category | P | I | Score | Severity | Response | Owner role | Status | Linked DEP / ASM / SEC / REQ IDs |
|---|---|---|---|---|---|---|---|---|---|---|
| RISK-001 | Wallet/ledger data integrity defect | Data | 4 | 5 | 20 | **CRITICAL** | Mitigate | Technical lead + Finance (Admin) | OPEN | NFR-008, DATA-REQ-006/007, SEC-002, SEC-015, AC-S-14/15, BR-PAY-06 |
| RISK-002 | Vendor adoption slower than plan | Business/Adoption | 4 | 4 | 16 | **HIGH** | Mitigate | Product owner | OPEN | OBJ-06, FR-007, ASM-05/09, GAP-05, AC-S-21 |
| RISK-003 | Third-party wallet provider outage / commercial failure (`DEP-05`) | External/Provider | 3 | 5 | 15 | **HIGH** | Mitigate + Transfer | Business development | OPEN | DEP-05, ASM-03, C-05, FR-013, INT-REQ-001/002/008, SEC-REQ-012 |
| RISK-004 | VAT treatment ambiguity and tax exposure | Regulatory | 3 | 4 | 12 | **HIGH** | Mitigate + Transfer | Legal liaison (sponsor) | OPEN | DEP-09, ASM-10, BR-FIN-01, NFR-019 |
| RISK-005 | Infrastructure/operational complexity vs. small team | Operational | 3 | 4 | 12 | **HIGH** | Mitigate | DevOps lead | OPEN | C-21, C-22, C-26, NFR-005/014/020, STK-14, ADR-002/004 |
| RISK-006 | SMS/WhatsApp provider outage or non-contracting → OTP delivery fails → registration blocked | External/Provider | 4 | 5 | 20 | **CRITICAL** | Avoid + Mitigate | Business development | OPEN | DEP-06, ASM-04, SEC-011, FR-001, INT-REQ-003/004, BR-NTF-03 |
| RISK-007 | Search/Elasticsearch degradation or Arabic relevance failure | Technical | 3 | 3 | 9 | **MEDIUM** | Mitigate | Technical lead | OPEN | DEP-04, FR-009, ASM-15, NFR-001/004/007, ADR-006 |
| RISK-008 | Performance shortfall vs. 10K concurrency target | Technical | 3 | 5 | 15 | **HIGH** | Mitigate | Technical lead | OPEN | C-25, NFR-001/003, AC-S-05, ADR-005 |
| RISK-009 | Data breach / PII leak (KYC documents, phone data) | Security | 2 | 5 | 10 | **MEDIUM** | Mitigate | Security officer | OPEN | SEC-003/007/008/014, SEC-REQ-002/006/007, DATA-REQ-002, NFR-019 |
| RISK-010 | Payment fraud and false-dispute abuse (SIM swap, fake delivery claims) | Financial | 3 | 4 | 12 | **HIGH** | Mitigate | Finance (Admin) + Security officer | OPEN | SEC-004, BR-SHP-02/03, BR-PAY-03, SEC-REQ-005/009, C-16 |
| RISK-011 | Scope creep from unresolved gaps and stakeholder requests | Operational | 3 | 3 | 9 | **MEDIUM** | Avoid | Product owner | OPEN | GAP-01…GAP-07, OBJ baseline, `project-scope.md` scope-creep control |
| RISK-012 | Central Bank position on closed-loop wallets (existential for wallet-only model) | Regulatory | 4 | 5 | 20 | **CRITICAL** | Mitigate | Project sponsor | OPEN | DEP-10, ASM-12, C-01, C-05, FR-013/014, ADR-009 |
| RISK-013 | Coupon and promotion abuse (stacking, refund gaming) | Financial | 3 | 2 | 6 | **MEDIUM** | Mitigate | Finance (Admin) | OPEN | BR-PRM-01…06, FR-019, DQ-12, BR-ESC-04 |
| RISK-014 | Launch infrastructure not ready (domains, TLS, CDN) | Operational | 3 | 4 | 12 | **HIGH** | Mitigate | DevOps lead | OPEN | DEP-08, NFR-005, SEC-REQ-006, NFR-020 |
| RISK-015 | Arabic-first UX quality shortfall (RTL defects, weak Arabic copy) | Business/Adoption | 3 | 4 | 12 | **HIGH** | Mitigate | Product owner + Design | OPEN | C-24, NFR-012/013, AC-S-11, FR-004, DQ-02 |
| RISK-016 | Mobile device/OS fragmentation breaks customer or courier apps | Technical | 2 | 3 | 6 | **MEDIUM** | Mitigate | QA lead | OPEN | DEP-12, NFR-015, ADR-008 |
| RISK-017 | Key-person / team concentration (baselines unset, `ASM-14`) | Operational | 3 | 4 | 12 | **HIGH** | Mitigate | Project sponsor | OPEN | ASM-14, DEP-11, NFR-009/010, OBJ set |
| RISK-018 | Courier supply shortage in launch zones | External/Provider | 3 | 4 | 12 | **HIGH** | Mitigate | Operations lead | OPEN | ASM-07, GAP-07, FR-015, BR-SHP-04, C-17 |
| RISK-019 | Single-host failure domain vs. 99.99% availability | Operational | 3 | 4 | 12 | **HIGH** | Mitigate | DevOps lead | OPEN | C-26, NFR-005/006, ADR-004, DEP-08 |
| RISK-020 | Data-protection law (PDPA 2012) obligations not implementable as designed | Regulatory | 3 | 4 | 12 | **HIGH** | Mitigate + Transfer | Security officer + Legal liaison | OPEN | ASM-13, DEP-09, SEC-REQ-006, NFR-019, DATA-REQ-003 |
| RISK-021 | Dependency/supply-chain compromise of the build | Security | 1 | 4 | 4 | **LOW** | Mitigate | Technical lead | OPEN | SEC-REQ-012, DEP-01, NFR-009/010 |
| RISK-022 | Escrow hold and payout terms drive vendor churn/disputes | Business/Adoption | 3 | 3 | 9 | **MEDIUM** | Mitigate | Product owner | OPEN | C-11, C-12, BR-ESC-01/02/05, ASM-09, FR-016 |
| RISK-023 | Redis/queue state loss (jobs, counters, OTP codes) | Data | 3 | 3 | 9 | **MEDIUM** | Mitigate | DevOps lead | OPEN | C-20, DEP-03, NFR-007, BR-PLT-01/02, ADR-005 |
| RISK-024 | Competitor response and price pressure at launch | Business/Adoption | 3 | 2 | 6 | **MEDIUM** | Accept | Product owner | OPEN | OBJ-01, `business-model.md`, BO-01…BO-06 |

**Distribution:** CRITICAL 3 · HIGH 12 · MEDIUM 8 · LOW 1 = 24. **No risk has been scored below MEDIUM+LOW combined visibility; none is closed.**

**Top 8 by ranking rule (drives `mitigation-plans.md`):** RISK-001 (20) · RISK-006 (20) · RISK-012 (20) · RISK-002 (16) · RISK-003 (15) · RISK-008 (15) · RISK-004 (12) · RISK-005 (12).

---

## 2. Risk Details

### RISK-001 — Wallet/ledger data integrity defect (zero-imbalance invariant broken)

**Category:** Data (secondary: Financial) · **P** 4 · **I** 5 · **Score** 20 · **Severity:** CRITICAL · **Response:** Mitigate · **Owner:** Technical lead with Finance (Admin) · **Status:** OPEN

- **Description:** A defect in `LedgerService.post`, the escrow engine, refund/commission paths, or a migration allows ledger postings that do not balance, a wallet balance that drifts from its ledger, or an idempotency failure that double-credits. This breaks the zero-imbalance invariant that the whole trust model rests on (`NFR-008`, `BR-PAY-06`, `DATA-REQ-007`, charter Critical Success Factors). Cited by STK-07 ("ledger defect = existential"), `workflow-006`, and `AC-S-14`.
- **Trigger / early-warning indicators:** reconciliation `J1`/`J2` mismatch (even 1 YER); quarantine depth rising on money rules (`DQ-08`, `DQ-09`); increase in idempotency-key collisions or `DUPLICATE_KEY` retries on payment paths; ledger rows written outside the normal post path (audit anomaly, `SEC-REQ-010`); any production hotfix touching `b07` schema; `SEC-015` (escrow/dispute TOCTOU) left unmitigated.
- **Impact if realized:** money loss for customers/vendors; loss of trust in escrow (the product's core promise); financial restatement impossible without compensation entries; regulatory attention amplified by RISK-012; existential per `stakeholder-needs.md` STK-07.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Append-only DB privileges: application role has no UPDATE/DELETE on ledger tables (`DATA-REQ-007`, `SEC-002`) | DevOps + Technical lead | Phase 0 |
| Nightly reconciliation jobs `J1` (balance vs ledger) and `J2` (global invariant) with 0-tolerance alerts (`16-data/data-quality.md` §5) | Technical lead | Phase 1 |
| Property-based and invariant tests: every operation sequence leaves Σ debits = Σ credits; fuzz refunds/commissions | QA lead | Phase 1 |
| Idempotency keys mandatory on payment/order/reservation/coupon/refund (`BR-PLT-03`); saga compensation (`BR-PLT-04`) | Technical lead | Phase 1 |
| Architecture test "only `LedgerService` writes ledger" (F7 in `module-boundaries.md`) as CI gate | Technical lead | Phase 1 |
| Concurrency fix + test for escrow-release vs dispute race (`SEC-015`) | Technical lead | Phase 1 |
| Seeded-mismatch drill: deliberately corrupt a row and prove detection ≤ one run (`AC-DR006-02`) | QA lead | Phase 2 |
| Pre-launch money-cycle audit: top-up → order → escrow → commission → payout → refund (`AC-S-22`) | Finance (Admin) | Launch |

- **Contingency plan:** freeze payouts and top-up crediting (wallet freeze path `BR-PAY-09` semantics for affected accounts), page on-call, stop affected release jobs, reconstruct state from append-only postings + audit chain, publish compensating entries only via Finance-approved procedure (`DATA-REQ-007` — never UPDATE/DELETE), notify STK-07/STK-01, write incident report feeding `15-deployment/` runbooks.
- **Residual risk:** insider/superuser tampering is not prevented by privileges alone (`SEC-002`, accepted with daily chain verification `J10` + signed checkpoints); human-approved compensation entries remain a control point.
- **Linked IDs:** NFR-008, DATA-REQ-006/007, BR-PAY-05/06/08, BR-PLT-03/04, BR-ESC-08, BR-FIN-03/05, AC-S-14, AC-S-15, AC-S-22, SEC-002, SEC-015, DQ-08/09, J1/J2/J10, WF-006.

### RISK-002 — Vendor adoption slower than plan

**Category:** Business/Adoption · **P** 4 · **I** 4 · **Score** 16 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** Product owner · **Status:** OPEN

- **Description:** Vendors are the supply side and the marketplace's critical path (`OBJ-11`). Adoption may lag because of wallet-only prepayment (`ASM-05`, `C-01` conflict raised by STK-04), commission sensitivity (`BR-ESC-03`), 7-day escrow hold (`ASM-09`, `C-12`), KYC friction (`FR-007`), or simple distrust of a new platform. Charter lists this as a top-three risk.
- **Trigger / early-warning indicators:** KYC application→approval conversion below plan; first-listing time > 10 min target (`NFR-012`); pilot vendors dropping before first sale (`AC-S-21` gate < 10 vendors); vendor interviews rejecting prepayment (`ASM-05` verification fails); COD pressure escalating (STK-04 conflict); churn after first payout cycle.
- **Impact if realized:** thin catalog → weak customer experience → weak demand → vicious cycle; schedule and revenue targets missed; sponsor pressure to violate `C-01` (COD) — a constraint breach.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Vendor discovery interviews to verify `ASM-05`/`ASM-09` before build | Product owner | Phase 0 |
| KYC ≤ 48 h SLA with escalation (`BR-VND-03`, `OBJ-06`) operational before pilot | Operations lead | Phase 1 |
| Onboarding UX: product listed < 10 min (`NFR-012`), Arabic-first vendor panel | Design / Product | Phase 1 |
| Transparent fee communication: tiered commission 5–20% default 10% (`BR-ESC-03`), monthly statements (`BR-FIN-04`) | Finance (Admin) | Phase 1 |
| Pilot program ≥ 10 vendors completing sale → payout (`AC-S-21`) with weekly feedback loop | Product owner | Phase 2 |
| Configurable escrow hold (default 7 days per `ASM-09`) rather than a hardcode, pending evidence | Technical lead | Phase 2 |
| Pricing/commission flexibility prepared against `GAP-05` (tiered plans) without pre-committing | Product owner | Post-launch |

- **Contingency plan:** if pilot conversion < 50% of target, pause growth spend, run qualitative exit interviews, adjust the *configurable* levers (hold period, payout batching `BR-ESC-05`, onboarding assistance), escalate to sponsor; commission changes only via decision record (`stakeholders.md` conflict resolution) — never by violating `C-01`.
- **Residual risk:** market distrust of digital payments is structural; some vendors will refuse prepayment regardless (`ASM-05` may prove false → recorded as scope input, not a constraint change).
- **Linked IDs:** OBJ-06, OBJ-11, FR-007, FR-008, ASM-05, ASM-09, GAP-05, AC-S-21, NFR-012, BR-VND-01/03, BR-ESC-03/05, STK-04.

### RISK-003 — Third-party wallet provider outage / commercial failure (`DEP-05`)

**Category:** External/Provider · **P** 3 · **I** 5 · **Score** 15 · **Severity:** HIGH · **Response:** Mitigate (primary) + Transfer · **Owner:** Business development · **Status:** OPEN

- **Description:** m-Floos and OneCash (`DEP-05`, **NOT STARTED**) may delay sandbox access, degrade in production, change APIs, impose unaccept-able commercial terms, or exit the market — removing the primary top-up rails that `C-05`/`FR-013` depend on. `ASM-03` (provider APIs are suitable) is `UNSUPPORTED`. Cited by dependencies, stakeholders (STK-12), business-model, INT-REQ-001, SEC-REQ-012, `10-integrations/`, threat-model.
- **Trigger / early-warning indicators:** `DEP-05` not converted to contract by Gate 0; sandbox credentials not issued; callback latency/error-rate metrics above SLO; reconciliation `J6` mismatches (provider statement vs ledger); provider fee/term changes; provider incident announcements.
- **Impact if realized:** production top-ups unavailable → wallet funding collapses to manual bank transfer (`INT-REQ-002`, `BR-PAY-04`) → lower conversion, support load, revenue shortfall; if *both* providers fail and bank transfer is slow, checkout stalls (wallet-only, `C-01`).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Commercial close with **both** providers (dual-rail from day one, not single-provider) | Business development | Phase 0 |
| Adapter abstraction so providers never touch domain code (`INT-REQ-008`, ADR-009) — swap cost stays low | Technical lead | Phase 1 |
| Circuit breakers + degraded-mode banner "top-up via bank transfer" (`integration-overview.md`) | Technical lead | Phase 1 |
| Daily provider-statement reconciliation `J6` with top-up hold on mismatch | Finance (Admin) | Phase 1 |
| Bank-transfer top-up flow fully built and staffed (`INT-REQ-002`, `BR-PAY-04`) as first-class fallback | Operations lead | Phase 1 |
| Contractual commitments sought: SLA, sandbox retention, 30-day API-change notice (transfer element) | Business development | Phase 0 → Launch |
| Sandbox test suite green before production credentials (`AC-IR001-05`) | QA lead | Phase 2 |

- **Contingency plan:** open-circuit both provider adapters → top-up UI degrades to admin-verified bank transfer with honest localized messaging (already specified in `integration-overview.md`); continue serving orders funded by existing balances; if commercial failure (not outage), activate the second provider or renegotiate; only if *no* rail remains, sponsor decides on temporary top-up limits — **cards/BNPL remain prohibited (`C-02`/`C-03`)**.
- **Residual risk:** bank transfer is slow and admin-bound — capacity of Finance (Admin) becomes the throttle; provider market concentration in Yemen remains.
- **Linked IDs:** DEP-05, ASM-03, C-05, FR-013, INT-REQ-001/002/008, SEC-REQ-012, BR-PAY-02/03/04/08, BR-ESC-08, J6, STK-12, ADR-009.

### RISK-004 — VAT treatment ambiguity and tax exposure

**Category:** Regulatory · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate + Transfer · **Owner:** Legal liaison (sponsor) · **Status:** OPEN

- **Description:** `ASM-10` (VAT 15% applies and yumn is responsible for charging) is `UNSUPPORTED`. If the platform is not the taxable person, or the rate/base differs, computed VAT (`BR-FIN-01`), displayed breakdowns, and remittance obligations are wrong — with retrospective exposure.
- **Trigger / early-warning indicators:** `DEP-09` legal opinion not received before launch; tax-authority guidance changing; pilot order audits showing wrong VAT on mixed baskets (coupon + shipping); vendor invoices conflicting with platform VAT lines.
- **Impact if realized:** back-taxes/penalties; repricing at launch (trust damage); restatement of historical orders; possible redesign of the commission/invoice model.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Written tax opinion before launch (`DEP-09`) covering who charges, base, and evidence | Legal liaison | Phase 0 |
| VAT as configuration (rate, applicability) — not compiled in — while keeping `BR-FIN-01` as default | Technical lead | Phase 1 |
| Separate VAT line on every money screen and statement (`compliance-and-legal.md`, `BR-FIN-02`) | Product owner | Phase 1 |
| Reconciliation `J5` (order totals vs line items + VAT) with escalation on mismatch | Finance (Admin) | Phase 1 |
| Monthly statement + audit retention ≥ 5 years (`BR-FIN-04`, `NFR-019`) to evidence collections | Finance (Admin) | Launch |

- **Contingency plan:** if opinion contradicts `ASM-10`, sponsor approves a decision record adjusting calculation/remittance, `BR-FIN-01` is superseded through change management (root README §9), and back-calculation tooling is built for the affected window.
- **Residual risk:** tax law can change after launch; retroactive application windows remain possible.
- **Linked IDs:** DEP-09, ASM-10, BR-FIN-01/02/04, NFR-019, FR-014, FR-018, GAP registry (`20-validation/missing-information.md`).

### RISK-005 — Infrastructure/operational complexity vs. small team

**Category:** Operational · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** DevOps lead · **Status:** OPEN

- **Description:** STK-14 states the core tension: a small operations team against a 99.99% target (`C-26`). Every extra technology, environment, or manual runbook multiplies on-call load. Canon mitigates this deliberately through operational simplicity — modular monolith (`C-21`, ADR-002), Docker Compose (`C-22`, ADR-004), a single queue system (`C-20`, ADR-005) — but the team must *hold that line* and still run the monitoring/backup discipline the SLOs require.
- **Trigger / early-warning indicators:** new infra components proposed without an ADR; manual steps appearing in deploy runbooks; alert volume exceeding on-call tolerance; MTTR trending up; missed backup/reconciliation windows (`DQM-02`); team headcount not confirmed at Gate 0 (`ASM-14`).
- **Impact if realized:** missed `C-26` windows, failed DR drill (`AC-S-17`), alert fatigue, incident burnout, quality/schedule trade-offs under pressure (STK-01 conflict).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Enforce the stack register: any new technology requires an ADR (`technology-stack.md` §8) | Technical lead | Phase 0 |
| Single Compose topology with layered parity (`deployment-view.md`) — same images across environments | DevOps lead | Phase 1 |
| Observability from day one: RED metrics, dashboards, alert routes (`INT-REQ-007`, `NFR-014`) | DevOps lead | Phase 1 |
| Runbooks for top 10 incidents + DR drill within RTO 1 h / RPO 15 min (`AC-S-17`, `AC-S-19`) | DevOps lead | Phase 2 |
| Health/readiness gates and graceful degradation (`BR-PLT-07`, `NFR-007`) verified in staging | QA lead | Phase 2 |
| On-call rotation sized to team; alert severity definitions per `../12-non-functional/core/observability.md` | DevOps lead | Launch |

- **Contingency plan:** if ops load exceeds capacity, reduce *scope* (features) rather than controls — cut launch scope via product owner, never monitoring/backups; sponsor may add ops capacity (`ASM-14` decision).
- **Residual risk:** single-host topology concentrates failure (see RISK-019); 99.99% on one host is inherently harder than on redundant fleets.
- **Linked IDs:** C-21, C-22, C-26, NFR-005/006/014/020, ADR-002, ADR-004, ADR-005, STK-14, AC-S-17…AC-S-20, DEP-01…DEP-04.

### RISK-006 — SMS/WhatsApp provider outage or non-contracting → OTP delivery fails → registration blocked

**Category:** External/Provider · **P** 4 · **I** 5 · **Score** 20 · **Severity:** CRITICAL · **Response:** Avoid (close `DEP-06` first) + Mitigate · **Owner:** Business development · **Status:** OPEN

- **Description:** Phone + OTP is the *only* authentication channel (`C-06`, ADR-010); there is no email fallback (`BR-NTF-01`, `GAP-03`). If `DEP-06` (Telesom/Sabafon SMS contract + WhatsApp Business API approval) is not closed — it is **NOT STARTED and is the Phase 0 gate** — or providers later outage simultaneously, OTP delivery fails and **registration, password reset, and sensitive changes are blocked** (`workflow-001`). `ASM-04` is `UNSUPPORTED`. `SEC-011` rates the finding CRITICAL. Cited by dependencies, assumptions, INT-REQ-003/004, workflow-001, threat-model, security-findings, `10-integrations/`.
- **Trigger / early-warning indicators:** `DEP-06` status still NOT STARTED 30 days before Phase 1; WhatsApp template approval delayed (days, per `whatsapp-business.md`); OTP send-failure rate rising; failover drill `AC-IR003-01…04` not passing in sandbox; both-provider outage events; DLR gaps.
- **Impact if realized:** no new user registration, no password reset, no delivery-code SMS → platform cannot onboard or confirm deliveries (`sms-provider.md` §critical path) → launch blocked; SIM-swap and lockout support load compound (`SEC-004`, `SEC-001`).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Sign **two** SMS providers before Phase 1 (avoid single-provider dependency) + WhatsApp Business approval submitted in Phase 0 | Business development | Phase 0 (gate) |
| Written no-log guarantees for message bodies; sender-ID/shortcode certification | Business development | Phase 0 |
| Two-provider failover + WhatsApp OTP fallback (`INT-REQ-003`, `BR-NTF-03`) implemented and drill-tested (`AC-IR003-01…04`) | Technical lead | Phase 1 |
| OTP delivery treated as authentication SLO: send-failure metric + alert (`SEC-001` recommendation) | DevOps lead | Phase 1 |
| Per-destination rate guards to protect SMS budget and victims (`SEC-006`) | Security officer | Phase 1 |
| Carrier SIM/lab testing with real SIMs (`DEP-12`) before launch | QA lead | Phase 2 |
| Honest localized outage messaging and support tooling for lockouts (`SEC-REQ-005` R5) | Product owner | Phase 2 |

- **Contingency plan:** both SMS providers down → automatic WhatsApp fallback (`BR-NTF-03`); WhatsApp also down → registration/verification **unavailable**, surfaced honestly with retry guidance and immediate on-call alert (`AC-IR003-04`) — **no bypass of OTP exists** (`SEC-REQ-001`); operations pause growth campaigns until recovery.
- **Residual risk:** all channels share the same underlying carriers and Meta approval; a prolonged regional outage still blocks onboarding (`SEC-001` — no third recovery path in v1).
- **Linked IDs:** DEP-06, ASM-04, SEC-011, SEC-001, SEC-006, FR-001, FR-017, INT-REQ-003/004, BR-AUTH-03, BR-NTF-01/02/03, SEC-REQ-001/005/009, C-06, DEP-12, ADR-010, workflow-001.

### RISK-007 — Search/Elasticsearch degradation or Arabic relevance failure

**Category:** Technical · **P** 3 · **I** 3 · **Score** 9 · **Severity:** MEDIUM · **Response:** Mitigate · **Owner:** Technical lead · **Status:** OPEN

- **Description:** Discovery (`FR-009`) depends on Elasticsearch 8 (`DEP-04`, ADR-006). Two failure modes: (a) cluster/index degradation — lag, mapping errors, single-node loss; (b) Arabic relevance failure — `ASM-15` (analyzer stemming is enough without custom NLP) proves false, so search returns poor results and browse-by-category becomes the only path. `RISK-007` is the ID used as the register example in root README §5.
- **Trigger / early-warning indicators:** index lag `DQM-01` p95 > 5 min; `J8` drift persisting > 1 run; search relevance spike in Phase 1 (per `ASM-15` verification) scoring below baseline; zero-result rate rising; ES memory pressure in load tests; fallback traffic share to category browse increasing.
- **Impact if realized:** customers cannot find products → conversion and GMV drop; `NFR-001`/`NFR-004` targets missed on search endpoints; pressure to ship custom NLP late (schedule risk).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Search relevance spike with real Arabic product data in Phase 1 (`ASM-15` verification) | Product owner + Technical lead | Phase 1 |
| Graceful degradation contract: ES down → category browse works (`NFR-007`, readiness unaffected) | Technical lead | Phase 1 |
| Nightly + on-demand reindex `J8`; index rebuildable from catalog (no backup needed) | DevOps lead | Phase 1 |
| k6 search scenarios inside the `NFR-003` load test | QA lead | Phase 2 |
| Documented escalation path to multi-node ES (candidate ADR-011 per DOC-ARCH-010 §4) if `NFR-001` not met | Technical lead | Post-launch |

- **Contingency plan:** serve cached/category browse while reindexing; if relevance fails the spike, prioritize analyzer tuning and merchandising rules before considering a search-as-a-service evaluation (future ADR).
- **Residual risk:** Arabic morphology is genuinely hard; long-tail queries may stay below ideal without NLP investment (accepted for v1).
- **Linked IDs:** DEP-04, FR-009, ASM-15, NFR-001/004/007, ADR-006, DQM-01, J8, C-24.

### RISK-008 — Performance shortfall vs. 10K concurrency target

**Category:** Technical · **P** 3 · **I** 5 · **Score** 15 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** Technical lead · **Status:** OPEN

- **Description:** `C-25` requires 10,000 concurrent users within `NFR-001` (p95 < 200 ms read / < 500 ms write) and `AC-S-05` demands a sustained 30-minute k6 proof. Single-host deployment (`ADR-004`), PostgreSQL connection limits, deep pagination, ES query cost, and N+1 patterns are plausible causes of shortfall.
- **Trigger / early-warning indicators:** staging load tests trending > 80% of latency budget at half target concurrency; p95 drifting during integration tests; DB CPU/connections saturated; cache hit ratio < 80% (`NFR-004`); rate-limit budgets throttling legit users (`SEC-013`).
- **Impact if realized:** `C-25`/`AC-S-05` breach → gate failure at final acceptance; poor UX in peak sales; rushed vertical scaling that strains `C-26` (see RISK-019).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Performance budgets in CI: bundle < 200 KB gzipped, query-shape review per endpoint | Technical lead | Phase 1 |
| Redis read cache for catalog with ≥ 80% hit target (`NFR-004`, ADR-005); cursor pagination for deep lists (`../07-api/core/pagination.md`) | Technical lead | Phase 1 |
| Connection pooling + statement/index review against `10M products / 100M rows` capacity plan (`NFR-017`) | Technical lead | Phase 1 |
| k6 suites at 2× target concurrency before launch; fix regressions, not budgets | QA lead | Phase 2 |
| Documented scale-out path (API replicas, read replicas) per `NFR-018`/`scalability.md` ready if single host tops out | DevOps lead | Phase 2 |

- **Contingency plan:** activate `NFR-018` stage S2 (stateless API replicas behind LB, PG read replica) — all within Compose (`C-22` preserved); reduce non-essential background work; cache more aggressively.
- **Residual risk:** headroom on one host is finite; sustained growth beyond target eventually needs the multi-host decision (candidate ADR, requires `C-22` change).
- **Linked IDs:** C-25, NFR-001/003/004/017/018, AC-S-05, ADR-004, ADR-005, ADR-006, SEC-013, `../12-non-functional/core/performance.md`.

### RISK-009 — Data breach / PII leak (KYC documents, phone data)

**Category:** Security · **P** 2 · **I** 5 · **Score** 10 · **Severity:** MEDIUM · **Response:** Mitigate · **Owner:** Security officer · **Status:** OPEN

- **Description:** yumn stores KYC identity documents, bank receipts, phone numbers, addresses, and financial history. Open findings `SEC-007` (PII may reach the ES index unprotected), `SEC-008` (MinIO bucket/presigned-URL exposure), `SEC-014` (key rotation undefined), `SEC-003` (admin console origin) are concrete leak paths identified during analysis — none fixed.
- **Trigger / early-warning indicators:** bucket-policy review failures; presigned URLs with long TTL observed; index containing non-allowlisted fields; secret scan hits; access anomalies on `b01`/KYC tables; penetration test findings; unkeyed audit gaps.
- **Impact if realized:** identity disclosure of real Yemeni users and vendors; PDPA exposure (`ASM-13`, RISK-020); irrecoverable trust loss killing vendor onboarding (compounds RISK-002).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Resolve `SEC-007`: index field allowlist (public catalog only), encrypted/restricted snapshots, deletion wired into account deletion | Technical lead | Phase 1 |
| Resolve `SEC-008`: deny anonymous listing, short presigned TTLs, server-generated keys, separate media origin | Security officer | Phase 1 |
| AES-256 at rest for PII/financial fields; keys outside DB; rotation runbook (`SEC-014`) | Security officer | Phase 1 |
| RBAC + ownership scoping on every endpoint; cross-tenant leakage test (`AC-DR008-02`) | Security officer | Phase 1 |
| SAST/DAST/dependency/secret scanning in CI; critical vulns ≤ 7 days (`SEC-REQ-012`) | Technical lead | Phase 1 |
| Incident-response playbook + breach-notification path via existing channels (no email, `GAP-03`) | Security officer | Phase 2 |

- **Contingency plan:** revoke credentials/buckets, rotate keys, isolate affected stores, preserve audit chain (`J10`), notify affected users via SMS/WhatsApp/in-app, regulator notification per legal advice (`DEP-09`), forensic review before re-enabling.
- **Residual risk:** insider + host compromise (no WORM anchor yet, `SEC-002`); user phone numbers are inherently exposed to SMS delivery.
- **Linked IDs:** SEC-003, SEC-007, SEC-008, SEC-014, SEC-REQ-002/006/007/011, DATA-REQ-002/003, NFR-019, ASM-13, RISK-020.

### RISK-010 — Payment fraud and false-dispute abuse

**Category:** Financial · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** Finance (Admin) with Security officer · **Status:** OPEN

- **Description:** Fraud vectors specific to this design: SIM-swap takeover of funded wallets and delivery codes (`SEC-004`), replayed/forged provider callbacks (`SEC-005`), false non-delivery claims against the 6-digit-code model (`C-16`), refund/return abuse (BR-RET + BR-ESC-04 commission reversal), and collusion between courier and buyer. No chargebacks exist (wallet-only) but disputes are the equivalent lever.
- **Trigger / early-warning indicators:** refund rate spikes per store/courier; code-lockout events clustering per courier (`BR-SHP-03`); delivery-confirmation anomalies (code attempts, timestamps); provider callback replay rejects rising; dispute volume above pilot baseline (`ASM-06` verification); wallet-freeze actions (`BR-PAY-09`) increasing.
- **Impact if realized:** direct money loss (escrow released wrongly, refunds granted fraudulently), courier network destabilization, support cost explosion, erosion of the trust promise.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Callback signature + replay window + nonce store (`SEC-005` fix, `webhook-reliability.md`) | Technical lead | Phase 1 |
| Idempotent money operations + reconciliation `J6` hold on mismatch | Finance (Admin) | Phase 1 |
| Wallet freeze capability (`BR-PAY-09`) and admin dispute tooling (`FR-020`) with full audit (`BR-PLT-06`) | Operations lead | Phase 1 |
| Rate limits/abuse controls on OTP, top-up, refund endpoints (`SEC-REQ-009`) validated under load (`SEC-013`) | Security officer | Phase 2 |
| Courier performance signals (per-courier dispute rate) feeding assignment eligibility (`BR-SHP-04`) | Operations lead | Phase 2 |
| Pilot dispute-rate measurement against `ASM-06` before scale | Product owner | Phase 2 |

- **Contingency plan:** freeze affected wallets/orders, halt affected payout batch (`J4`), admin ruling with audit entry (`BR-RET-06`), compensating ledger entries only, courier suspension, pattern review feeding `threat-model.md` updates.
- **Residual risk:** SIM-swap is carrier-level and outside platform control (`SEC-004` accepted residual); without GPS, delivery proof remains code-based (`C-16`).
- **Linked IDs:** SEC-004, SEC-005, SEC-013, BR-PAY-03/09, BR-SHP-02/03/04, BR-RET-06, BR-ESC-04/07, SEC-REQ-005/009, C-16, ASM-06, FR-016, FR-020.

### RISK-011 — Scope creep from unresolved gaps and stakeholder requests

**Category:** Operational · **P** 3 · **I** 3 · **Score** 9 · **Severity:** MEDIUM · **Response:** Avoid · **Owner:** Product owner · **Status:** OPEN

- **Description:** Seven open gaps (`GAP-01…GAP-07`), three scope-exclusion debates (`GAP-03` email, `GAP-04` loyalty, `GAP-05` tiers), eager stakeholders (STK-01 speed vs quality, STK-09 ambiguity), and future-scope items create constant pressure to promote backlog items into current requirements — the methodology's explicit prohibition.
- **Trigger / early-warning indicators:** new FR requests without impact analysis; `GAP-*` items unresolved at Gate 0; ADRs appearing for convenience rather than substance; requirement churn invalidating tests (STK-10); documents drifting from baselines (consistency-audit entries).
- **Impact if realized:** schedule slip, diluted quality on money paths, test invalidation, constraint pressure (features that imply COD/cards/K8s are the danger pattern).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Enforce `project-scope.md` scope-creep control (check document first; reject with constraint ID) | Product owner | Phase 0 |
| Resolve `GAP-01…GAP-06` decisions before Gate 0 (owners listed in scope register) | Product owner + Sponsor | Phase 0 |
| Every change follows root README §9: version bump, change history, impacted IDs into `20-validation/consistency-audit.md` | Technical lead | Continuous |
| Future-scope items parked, never promoted silently; ADR required for architectural change | Architecture | Continuous |
| Phase-gate scope audit in `21-completion/quality-gates.md` | Sponsor | Each gate |

- **Contingency plan:** if creep has already consumed float, sponsor re-baselines schedule or cuts launch scope; never reduce test/observability coverage to absorb creep.
- **Residual risk:** sponsor-level deadline pressure (STK-01) can override process; the mitigation is transparency of register/gate status, not authority.
- **Linked IDs:** GAP-01…GAP-07, OBJ set, `project-scope.md`, root README §9, `20-validation/consistency-audit.md`, `21-completion/quality-gates.md`.

### RISK-012 — Central Bank position on closed-loop wallets (existential for wallet-only model)

**Category:** Regulatory · **P** 4 · **I** 5 · **Score** 20 · **Severity:** CRITICAL · **Response:** Mitigate · **Owner:** Project sponsor · **Status:** OPEN

- **Description:** The entire money model (wallet-only `C-01`, escrow `C-12`, top-ups `C-05`, refunds `BR-PAY-07`) assumes the Central Bank of Yemen permits a platform-operated closed-loop wallet. `ASM-12` is **`DANGEROUS`** (Inference, unverified) and `DEP-10` (regulatory position) is **NOT STARTED**; dependencies.md marks the impact **"Existential — wallet-only model at risk"**. Cited by dependencies and assumptions as the regulatory counterpart of RISK-003/RISK-006.
- **Trigger / early-warning indicators:** `DEP-10` still open at Gate 0; legal counsel unable to confirm; any Central Bank notice on e-money/wallet operators; provider partners reporting regulatory queries; `DEP-09` legal opinion raising payment-scope questions.
- **Impact if realized:** the flagship feature could be unlawful or require licensing → fundamental redesign (ADR-009 alternatives: escrow-by-bank-transfer, partnership with a licensed wallet operator, or market exit); sunk build cost on B07, launch delay, investor/partner loss. **This is the single existential regulatory risk.**
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Obtain written Central Bank position **before implementation** (`DEP-10`, `ASM-12` verification) — Gate 0 blocking item | Project sponsor + Legal | Phase 0 |
| Map licensing/registration options with counsel; document permitted operational limits (caps, KYC tiers) | Legal liaison | Phase 0 |
| Keep wallet mechanics behind ADR-009 adapter/port boundaries so a licensed-partner model can replace self-custody with bounded rework | Technical lead | Phase 1 |
| Track regulator signals via provider partners (m-Floos/OneCash compliance channels) | Business development | Continuous |
| Legal sign-off recorded in `AC-S-24` before public launch | Project sponsor | Launch |

- **Contingency plan / kill criteria:** **if the Central Bank rejects or restricts the model, implementation does not start (or is re-scoped at the gate).** Redesign options, in order of preference: (1) operate as a *pass-through* to a licensed wallet/bank partner, keeping yumn's ledger as an internal accounting layer (ADR-009 alternative: "partner-custodied wallet"); (2) admin-verified bank-transfer-only escrow (`BR-PAY-04`, `INT-REQ-002`) with slower funding — changes `C-05` scope, therefore requires sponsor-approved constraint change and a **new superseding ADR** (root README §9, DOC-ARCH-010 §6); (3) if no lawful variant exists, v1 launch is cancelled pending regulation. Cards/BNPL/crypto remain excluded regardless (`C-02`/`C-03`/`C-04`).
- **Residual risk:** regulatory timelines are outside platform control; even a favorable opinion may come with conditions (caps, reporting) that raise operating cost.
- **Linked IDs:** DEP-10, ASM-12, C-01, C-04, C-05, FR-013, FR-014, ADR-009, BR-PAY-04/07, AC-S-24, DEP-09.

### RISK-013 — Coupon and promotion abuse

**Category:** Financial · **P** 3 · **I** 2 · **Score** 6 · **Severity:** MEDIUM · **Response:** Mitigate · **Owner:** Finance (Admin) · **Status:** OPEN

- **Description:** Coupon engine abuse: stacking attempts (`BR-PRM-02` bans stacking), expired/fully-used codes racing at checkout, discount > 90% errors, platform-vs-store coupon privilege misuse, and refund-gaming (buy with coupon → refund → keep discount economics). Impact is bounded by `BR-PRM-01` caps and `DQ-12`.
- **Trigger / early-warning indicators:** coupon-attempt rejection spikes; per-user/global usage-limit hits; refund-with-coupon rate per account; discount share of GMV drifting above plan; admin coupon actions without audit (`BR-PLT-06` gap).
- **Impact if realized:** margin erosion, unfair pricing perception, payout math disputes; aggregate losses scalable via automated scripts.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Enforce `BR-PRM-01…06` server-side; reject before order row exists (`BR-PRM-06`) | Technical lead | Phase 1 |
| `DQ-12` constraints: unique code, ≤ 90-day window, ≤ 90% discount | Technical lead | Phase 1 |
| Idempotent coupon application (`BR-PLT-03`); per-user + global usage limits (`BR-PRM-04`) | Technical lead | Phase 1 |
| Commission reversal on refund handled in one transaction (`BR-ESC-04`, `BR-RET-07`) | Finance (Admin) | Phase 1 |
| Fraud-pattern report: refund rate × coupon usage per user (feeds `FR-018`) | Finance (Admin) | Phase 2 |

- **Contingency plan:** disable offending coupon (admin action, audited), block abuser's coupon eligibility, claw back via wallet adjustments with audit entries.
- **Residual risk:** coordinated abuse across fresh accounts remains possible; bounded by top-up/KYC friction.
- **Linked IDs:** FR-019, BR-PRM-01…06, BR-ESC-04, BR-RET-07, BR-PLT-03/06, DQ-12, C-14, FR-018.

### RISK-014 — Launch infrastructure not ready (domains, TLS, CDN)

**Category:** Operational · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** DevOps lead · **Status:** OPEN

- **Description:** `DEP-08` (domains, TLS certificates, Cloudflare CDN) is **Not started** and is a hard precondition for public launch: no domain/TLS/CDN → no public site, no certificate automation, no DDoS protection, no edge caching supporting `NFR-002`.
- **Trigger / early-warning indicators:** `DEP-08` not started 60 days before target launch; DNS/TLS renewal automation unproven; certificate expiry alerts; CDN cache rules untested with RTL assets; edge config drift between staging and prod.
- **Impact if realized:** launch delayed (I4 — all other work ready but unreachable); TLS misconfiguration risks `SEC-REQ-006` violations; no CDN → mobile LCP budget (`NFR-002`) missed in-region.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Register domains + validate DNS ownership early; document ownership (naming, renewal) with sponsor | DevOps lead | Phase 0 |
| Cloudflare zone + TLS 1.3 at edge (`SEC-REQ-006`), origin protection, WAF basics | DevOps lead | Phase 2 |
| Edge caching tuned for Next.js assets + invalidation strategy for `ar`/`en` variants | DevOps lead | Phase 2 |
| Staging runs on the same edge config (parity rule, `deployment-view.md` §9) | DevOps lead | Phase 2 |
| Pre-launch smoke: external uptime probe from inside Yemen region + certificate expiry alerting | DevOps lead | Launch |

- **Contingency plan:** if CDN unavailable, serve directly from the edge proxy with valid certs (`deployment-view.md` `edge` service) — degraded performance but functional launch; if domain transfer delayed, launch under provider subdomain temporarily (decision recorded).
- **Residual risk:** regional reachability to global CDN edges varies in Yemen; edge latency must be measured, assumed not proven.
- **Linked IDs:** DEP-08, NFR-002, NFR-005, SEC-REQ-006, BR-PLT-07, ADR-004, ADR-007, RISK-019.

### RISK-015 — Arabic-first UX quality shortfall

**Category:** Business/Adoption · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** Product owner with Design · **Status:** OPEN

- **Description:** The market is Arabic; charter states poor RTL = product failure. Shortfall modes: RTL layout defects, Latin-digits leaking into Arabic screens, untranslated strings, culturally wrong copy, or onboarding friction (`NFR-012` 5-minute registration target). `DEP-11` (Arabic copy/design assets) is only **Partial**.
- **Trigger / early-warning indicators:** RTL visual-regression defects > 0; locale-coverage checks failing (`AC-NFR-013-01`); mixed-locale strings found; Arabic copy review backlog; usability sessions missing the 5-min registration target; DQ-02 rejections (missing Arabic product names) high at pilot.
- **Impact if realized:** customers churn before first order; vendors see low conversion; brand trust damaged in a word-of-mouth market; `AC-S-11` gate fails.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Close `DEP-11`: native Arabic copy review for all user-facing strings and templates (`BR-NTF-04`, `BR-PLT-05`) | Design / Product | Phase 0 → Phase 1 |
| RTL as structural architecture: logical properties, RTL regression suite, zero hardcoded strings (`AC-S-11`) | Technical lead | Phase 1 |
| Arabic-Indic numerals via `Intl.NumberFormat('ar-YE')`, input normalization (decisions log entries D-01/D-02) | Technical lead | Phase 1 |
| Arabic usability testing with target users on registration→first order (`NFR-012`) | Product owner | Phase 2 |
| Arabic search relevance spike (works with RISK-007) | Product owner | Phase 2 |

- **Contingency plan:** freeze new visual features before launch to burn down RTL defects; hire native copy review; delay a surface rather than ship broken Arabic (per-surface launch is possible — web first).
- **Residual risk:** dialect and literacy variance across governorates cannot be fully validated pre-launch.
- **Linked IDs:** C-24, NFR-012/013, AC-S-11, FR-004, BR-PLT-05, BR-NTF-04, DEP-11, DQ-02, ASM-01, ADR-008.

### RISK-016 — Mobile device/OS fragmentation breaks apps

**Category:** Technical · **P** 2 · **I** 3 · **Score** 6 · **Severity:** MEDIUM · **Response:** Mitigate · **Owner:** QA lead · **Status:** OPEN

- **Description:** React Native 0.73 apps (customer + courier) must run on Android 10+/iOS 15+ (`NFR-015`) across low-end devices common in the market; `DEP-12` (test device lab + carrier SIMs) is **Not started**. Without the lab, crashes/ANRs on old Android versions and OTP delivery differences across carriers go undetected.
- **Trigger / early-warning indicators:** device-lab procurement slipping past Phase 2 start; crash-rate on internal testing devices; app-store review mentions of specific OS versions; RN/dependency upgrades causing regressions; carrier-specific OTP delays in field tests.
- **Impact if realized:** courier app failure blocks deliveries (operational), customer app crashes block purchases; poor store ratings compound adoption risk (RISK-002).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Stand up `DEP-12` device lab + real SIMs before mobile QA exit | QA lead | Phase 0 → Phase 2 |
| Device matrix aligned to `NFR-015`; smoke suite per OS version | QA lead | Phase 2 |
| Crash reporting wired for both apps from first build | Technical lead | Phase 1 |
| Avoid native modules beyond necessity; keep RN core stable within 0.73 line | Technical lead | Continuous |
| Low-end device performance pass on registration→checkout journey | QA lead | Phase 2 |

- **Contingency plan:** narrow supported versions to the `NFR-015` floor with honest store listings; web fallback (Next.js storefront) covers customers if app fails on a device class; courier operations can use the web panel temporarily.
- **Residual risk:** long-tail devices outside the matrix will exist; support burden accepted.
- **Linked IDs:** DEP-12, NFR-015, ADR-008, FR-001, FR-015, RISK-006 (OTP testing), `13-testing/`.

### RISK-017 — Key-person / team concentration

**Category:** Operational · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** Project sponsor · **Status:** OPEN

- **Description:** Budget, team size, and schedule baselines are `INSUFFICIENT EVIDENCE` (`ASM-14`, `UNSUPPORTED`); the analysis itself is authored by a single agent, and delivery risks concentrating in one or two individuals (architecture, money paths, ops). Departure or unavailability of a key person stalls Gate 0 or the money-critical path.
- **Trigger / early-warning indicators:** `ASM-14` unresolved at Gate 0; bus-factor = 1 modules (ledger, escrow) with no second reviewer; documentation gaps; single-person deployments/rollbacks; hiring not started vs roadmap.
- **Impact if realized:** schedule slip (I4), knowledge loss on money code, incident response degraded, quality trade-offs under pressure.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Sponsor sets budget/team/schedule baseline at Gate 0 (`ASM-14` verification) | Project sponsor | Phase 0 |
| Knowledge base as the onboarding path (this repo) + ADRs capturing rationale | Technical lead | Continuous |
| Mandatory peer review for money-path changes; no single-person merges in `b07` | Technical lead | Phase 1 |
| Runbooks + architecture tests reduce tribal knowledge (works with RISK-005) | DevOps lead | Phase 1 |
| Cross-train QA/DevOps on deploy, restore, and reconciliation procedures | DevOps lead | Phase 2 |

- **Contingency plan:** sponsor re-baselines timeline or adds contract capacity; freeze non-critical feature work to protect money-path delivery; sequence work so no single person blocks a gate.
- **Residual risk:** Yemen's constrained tech talent market limits replacement options.
- **Linked IDs:** ASM-14, DEP-11, NFR-009/010, OBJ set, `21-completion/quality-gates.md` Gate 0, STK-09.

### RISK-018 — Courier supply shortage in launch zones

**Category:** External/Provider · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** Operations lead · **Status:** OPEN

- **Description:** Delivery depends on individuals/small fleets (`ASM-07`), zone-based first-accept assignment (`BR-SHP-04`), and no GPS fallback (`C-16`). If couriers are insufficient in a launch zone, orders stall in OUT_FOR_DELIVERY, escrow never matures, and customers lose trust. `GAP-07` (fleet-operator logistics partners) is unresolved; no national courier exists (STK-15 omitted stakeholder).
- **Trigger / early-warning indicators:** assignment-accept time rising; unassigned shipments aging; delivery attempts > 3 escalating (`BR-SHP-06`); courier churn; zone coverage map showing gaps; courier earnings disputes (STK-05).
- **Impact if realized:** delivery SLA breach, order cancellations, escrow/dispute pile-up, launch-zone reputation damage.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Courier recruitment ≥ coverage target per launch zone before opening sales (`AC-S-21` companion) | Operations lead | Phase 2 |
| Ops interviews to verify `ASM-07` before B08 build | Operations lead | Phase 0 |
| Assignment queue with clear economics (fees, batching) and first-accept + optimistic lock correctness (`BR-SHP-04`) | Technical lead | Phase 1 |
| Escalation paths: 3 failed attempts → admin review (`BR-SHP-06`); manual reassignment tooling | Operations lead | Phase 1 |
| Evaluate `GAP-07` fleet partners as a supply hedge (decision record if contracted) | Product owner | Post-launch |

- **Contingency plan:** restrict shipping zones to covered areas at launch (config lever, respects `C-17`); pause promotions in uncovered zones; temporary earnings incentives; admin-managed manual assignment during shortage.
- **Residual risk:** courier supply is a labor-market constraint no platform control can guarantee.
- **Linked IDs:** ASM-07, GAP-07, FR-015, BR-SHP-04/06, C-16, C-17, STK-05, AC-S-21, RISK-002.

### RISK-019 — Single-host failure domain vs. 99.99% availability

**Category:** Operational · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate · **Owner:** DevOps lead · **Status:** OPEN

- **Description:** `ADR-004`/`C-22` deliberately choose Docker Compose on a single host (or tightly coupled host set) for operability. That topology makes `C-26` (99.99% ≈ 4.32 min/month) hard: host loss, disk failure, or network partition exceed the downtime budget, and RTO ≤ 1 h depends on restore speed (`NFR-006`).
- **Trigger / early-warning indicators:** uptime dashboard approaching monthly budget; host hardware SMART/volume warnings; restore drill exceeding 30 min; backup job failures (`DATA-REQ-004`); readiness gaps during deploys; `J2` freshness breaches after restarts.
- **Impact if realized:** `C-26`/`AC-S-06` breach; extended outage erodes wallet trust; DR drill failure blocks `AC-S-17`/final acceptance.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| WAL archiving + daily snapshots; quarterly restore drills within RTO 1 h / RPO 15 min (`AC-S-17`) | DevOps lead | Phase 1 → continuous |
| Health/readiness gates, graceful shutdown, rolling restart of stateless API replicas (`BR-PLT-07`, `NFR-020`) | DevOps lead | Phase 1 |
| Redundant power/network at host site; monitored capacity; off-host backup copy | DevOps lead | Phase 2 |
| Maintenance windows scheduled against budget; alert on budget consumption (4.32 min scale) | DevOps lead | Launch |
| Keep the multi-host path documented (`NFR-018`, candidate ADR) so escalation needs no redesign | Technical lead | Post-launch |

- **Contingency plan:** restore from WAL/snapshot to replacement host within RTO (documented in `15-deployment/` runbooks); switch DNS/edge to standby if pre-provisioned; if repeated host failures occur, sponsor approves the multi-host ADR (requires formal `C-22` review per DOC-ARCH-010 §6).
- **Residual risk:** true N+1 redundancy is consciously not built in v1 — accepted against `C-22`; single-region dependence remains.
- **Linked IDs:** C-22, C-26, NFR-005/006/018/020, ADR-004, DATA-REQ-004, AC-S-06/17/20, DEP-08, RISK-005.

### RISK-020 — Data-protection law (PDPA 2012) obligations not implementable as designed

**Category:** Regulatory · **P** 3 · **I** 4 · **Score** 12 · **Severity:** HIGH · **Response:** Mitigate + Transfer · **Owner:** Security officer with Legal liaison · **Status:** OPEN

- **Description:** `ASM-13` (Yemeni Personal Data Protection Law obligations are implementable with planned controls) is `UNSUPPORTED`; `DEP-09` (data-protection legal opinion) not started. Unknowns: consent model, cross-border processing (global CDN/SMS providers), retention limits, breach-notification duties, data-subject rights implementation.
- **Trigger / early-warning indicators:** `DEP-09` opinion revealing obligations beyond design (e.g., deletion of financial records vs 5-year retention conflict); CDN/SMS processing flagged as cross-border; regulator inquiry; retention job conflicts with evidentiary retention (`NFR-019`).
- **Impact if realized:** penalties, forced redesign of retention/deletion (`DATA-REQ-003`), notification obligations without an email channel (`GAP-03` pressure), launch delay.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Legal gap assessment before launch (`DEP-09`), mapped to `SEC-REQ-006` + `16-data/` controls | Legal liaison | Phase 0 |
| Data minimization + classification already specified (`DATA-REQ-002`, `data-classification.md`) implemented as designed | Security officer | Phase 1 |
| Retention/deletion workflows with audit evidence (`DATA-REQ-003`, `16-data/data-deletion-and-privacy.md`) | Technical lead | Phase 1 |
| Provider data-processing terms reviewed (SMS/WhatsApp/CDN) for lawful transfer | Legal liaison | Phase 1 |
| Breach-notification playbook using available channels (SMS/WhatsApp/in-app) | Security officer | Phase 2 |

- **Contingency plan:** if opinion requires controls not yet built, sponsor prioritizes compliance items ahead of feature scope (works with RISK-011); worst case, restrict processing (e.g., disable optional PII collection) rather than launch non-compliant.
- **Residual risk:** legal environment is `INSUFFICIENT EVIDENCE` at analysis time; interpretation may change.
- **Linked IDs:** ASM-13, DEP-09, SEC-REQ-002/006/007, DATA-REQ-002/003, NFR-019, AC-S-24, GAP-03, RISK-009.

### RISK-021 — Dependency/supply-chain compromise of the build

**Category:** Security · **P** 1 · **I** 4 · **Score** 4 · **Severity:** LOW · **Response:** Mitigate · **Owner:** Technical lead · **Status:** OPEN

- **Description:** A malicious or compromised npm package (or CI action) could execute during build and reach money-path code. Scored **LOW by probability** (rare, mitigations already mandated) with **high impact** — the classic low-probability/high-impact profile that must keep a contingency despite the band.
- **Trigger / early-warning indicators:** dependency-scan alerts (`SEC-REQ-012`); typosquat/new-dep PRs without review; lockfile drift; unexpected CI failures or outbound calls from build; secret-scan hits.
- **Impact if realized:** backdoor in API/worker → ledger manipulation (compounds RISK-001), secret exfiltration; supply-chain incidents are hard to bound.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| SAST + dependency + secret scanning on every PR; critical vulns fixed ≤ 7 days (`SEC-REQ-012`) | Technical lead | Phase 1 |
| Lockfile committed; pinned action versions; no floating `latest` in CI | DevOps lead | Phase 1 |
| Review required for new dependencies; minimal dependency policy (stack register) | Technical lead | Continuous |
| Reproducible builds with commit-SHA image tags (`deployment-view.md` §7) | DevOps lead | Phase 1 |
| Post-incident ledger reconciliation (`J1`, `J2`) as detection backstop | Finance (Admin) | Continuous |

- **Contingency plan:** rotate secrets, rebuild from known-good lockfile, revoke tokens, run full reconciliation before resuming payouts, incident report under `SEC-REQ-012`.
- **Residual risk:** transitive dependencies remain beyond direct control; zero-day exploitation possible.
- **Linked IDs:** SEC-REQ-007/012, DEP-01, NFR-009/010, C-18, RISK-001.

### RISK-022 — Escrow hold and payout terms drive vendor churn/disputes

**Category:** Business/Adoption · **P** 3 · **I** 3 · **Score** 9 · **Severity:** MEDIUM · **Response:** Mitigate · **Owner:** Product owner · **Status:** OPEN

- **Description:** Vendors must accept prepayment (`ASM-05`), a 7-day escrow hold (`C-12`, `ASM-09`), batched payouts 3–7 business days after release with a 1,000 YER floor (`BR-ESC-05`), and commission reversals on refunds (`BR-ESC-04`). If perceived as slow/unfair relative to informal trade, vendors dispute or leave.
- **Trigger / early-warning indicators:** payout dispute tickets per vendor; vendor churn after first cycle; support themes around hold period; pilot interviews rejecting `ASM-09`; requests for instant payouts.
- **Impact if realized:** vendor attrition (compounds RISK-002), support cost, negative word-of-mouth; pressure to shorten escrow → weakens buyer protection (`C-12` is a constraint — pressure becomes a constraint-conflict case).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Verify `ASM-09` via vendor interviews before build; keep hold period platform-configurable with 7-day default | Product owner | Phase 0 → Phase 1 |
| Transparent payout timeline + monthly statements (`BR-FIN-04`) shown in vendor panel | Product owner | Phase 1 |
| Clear return/dispute explanation at listing time (why escrow protects the sale) | Design / Product | Phase 1 |
| Payout batch reliability monitored (`J4`, 0-tolerance mismatch) | Finance (Admin) | Phase 1 |
| Pilot measures dispute/churn rate (`AC-S-21`) before scaling recruitment | Product owner | Phase 2 |

- **Contingency plan:** adjust configurable levers (hold period within sponsor-approved bounds, payout cadence, minimum amount) via decision record; improve communication before any policy change; never violate `C-12` to stem churn.
- **Residual risk:** market norms (instant cash) vs escrow protection — inherent tension accepted as part of the trust model.
- **Linked IDs:** ASM-05, ASM-09, C-11, C-12, FR-014, FR-016, BR-ESC-01…05, BR-FIN-04, GAP-05, GAP-06, STK-04.

### RISK-023 — Redis/queue state loss (jobs, counters, OTP codes)

**Category:** Data · **P** 3 · **I** 3 · **Score** 9 · **Severity:** MEDIUM · **Response:** Mitigate · **Owner:** DevOps lead · **Status:** OPEN

- **Description:** Redis 7 is the sole substrate for cache, BullMQ queues, rate-limit counters, OTP storage (5-min TTL), and session registry acceleration (`C-20`, `ADR-005`, `DEP-03`). Data loss (misconfigured persistence, failover without AOF) or exhaustion (memory, stuck queues) silently drops scheduled jobs — reconciliation, escrow maturity, notification fan-out, TTL releases — degrading correctness signals rather than corrupting Postgres directly.
- **Trigger / early-warning indicators:** AOF/RDB save failures; queue depth/DLQ depth rising (`DQM-03`, `BR-PLT-02`); `J11` outbox staleness > 15 min; reconciliation freshness breaches (`DQM-02`); rate-limit counter anomalies; OTP delivery failures despite healthy SMS.
- **Impact if realized:** missed escrow releases or payouts (late money = trust damage), notification loss, lost TTL stock releases (oversell risk until `J7` corrects), degraded abuse controls.
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| AOF persistence enabled; volume backed up; documented restore (deployment-view §4) | DevOps lead | Phase 1 |
| Jobs idempotent + retry 3× + DLQ with depth alerts (`BR-PLT-01/02`) so replays are safe | Technical lead | Phase 1 |
| Postgres as durable session record so cache loss cannot strand revocations (`authentication.md` §4) | Technical lead | Phase 1 |
| Critical invariants owned by Postgres + nightly jobs, not by Redis state (`DQ-08`, `J1–J6`) | Technical lead | Phase 1 |
| Memory limits, queue monitoring panels, stuck-job alerts per `../12-non-functional/core/observability.md` | DevOps lead | Phase 1 |

- **Contingency plan:** flush cache (safe by design — it is disposable); replay/re-run jobs idempotently; if queue data lost, trigger reconciliation and manual re-enqueue of escrow/payout batches; OTP codes simply re-requested (60 s cooldown).
- **Residual risk:** in-flight non-idempotent external sends (SMS) may duplicate or be lost — bounded by provider DLR logs.
- **Linked IDs:** C-20, DEP-03, NFR-007, BR-PLT-01/02/03, ADR-005, DQM-02/03, J11, SEC-REQ-009, SEC-006.

### RISK-024 — Competitor response and price pressure at launch

**Category:** Business/Adoption · **P** 3 · **I** 2 · **Score** 6 · **Severity:** MEDIUM · **Response:** Accept (monitor) · **Owner:** Product owner · **Status:** OPEN

- **Description:** Existing informal commerce, social-marketplace selling, and any formal competitors can respond with price cuts, fee reductions, or faster delivery. Impact is limited because yumn's differentiators are escrow trust, Arabic-first tooling, and wallet protection rather than price alone.
- **Trigger / early-warning indicators:** vendor reports of competitor fee changes; signup conversion drops by cohort; price-parity gaps on key categories; competitor launches in launch governorates.
- **Impact if realized:** slower growth (moderate), vendor price demands (margin pressure on commission `BR-ESC-03`).
- **Mitigation actions:**

| Action | Owner | Phase |
|---|---|---|
| Quarterly competitive scan recorded in business review (no canon document claims market share) | Product owner | Post-launch |
| Differentiation messaging: escrow protection, code-confirmed delivery, vendor tooling | Design / Product | Launch |
| Commission levers prepared (already tiered 5–20%) — any change via decision record | Product owner | Post-launch |
| Track vendor/customer acquisition metrics vs `GAP-01` targets once sponsor sets them | Product owner | Post-launch |

- **Contingency plan:** deliberate pricing review by sponsor using tiered commission capability; prioritize retention of active vendors over price matching; accept short-term share loss if fee war threatens unit economics.
- **Residual risk:** market pricing dynamics are uncontrollable; `GAP-01` (growth targets) remains unresolved, so impact measurement is approximate.
- **Linked IDs:** OBJ-01, BR-ESC-03, GAP-01, `../01-business-analysis/core/business-model.md`, BO-01…BO-06, STK-03/STK-04.

---

## 3. Register Rules

1. New risks continue the sequence `RISK-025`…; IDs are **never reused**, even after closure.
2. Score/severity changes require a rationale note and a version bump (no silent changes — root README §9).
3. Closing a risk requires evidence (test, drill, contract, sign-off) linked from the detail section; the entry stays visible with status `CLOSED` (never deleted).
4. The charter's Summary of Major Risks mirrors RISK-001/002/003; if those rows change, `00-project-overview/project-charter.md` must be updated in the same change set (consistency rule, `20-validation/consistency-audit.md`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
