---
document_id: DOC-OVR-009
title: Assumptions (ASM-01 … ASM-15)
category: 00-project-overview
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: []
related_documents: [DOC-OVR-008, DOC-OVR-010]
---

# Assumptions

Each assumption: statement, source, evidence, risk if false, how to verify, status (`SUPPORTED` / `REASONABLE` / `UNSUPPORTED` / `DANGEROUS`).

| ID | Assumption | Evidence | Risk if False | How to Verify | Status |
|---|---|---|---|---|---|
| ASM-01 | Target customers own Android smartphones with data access | INFERENCE — market context (mobile-first MENA retail) | Web-only demand; app investment wasted | Market research / analytics after web launch | REASONABLE |
| ASM-02 | Majority of transactions will be in YER | VERIFIED — brief | FX flows needed earlier; pricing model changes | Pilot data after launch | SUPPORTED |
| ASM-03 | m-Floos and OneCash expose merchant top-up APIs suitable for integration | INFERENCE — known local providers | Top-ups degrade to bank-transfer-only (admin-verified) | Request sandbox credentials from both providers (pre-build gate, `DEP-05`) | UNSUPPORTED |
| ASM-04 | Telesom/Sabafon SMS and WhatsApp Business API are reachable commercially | INFERENCE | OTP delivery fails → registration blocked (RISK-006) | Provider contracting before Phase 1 (`DEP-06`) | UNSUPPORTED |
| ASM-05 | Vendors accept prepayment (no COD) as condition of listing | INFERENCE — brief states wallet-only as mandate | Vendor churn / black-market workarounds | Vendor discovery interviews before build | REASONABLE |
| ASM-06 | 6-digit code delivery confirmation is operationally acceptable (no GPS) | VERIFIED — brief | Dispute volume rises; support burden grows | Pilot with 10 vendors; measure dispute rate | SUPPORTED |
| ASM-07 | Delivery providers are individuals/Small fleets, not a single national courier | INFERENCE | Assignment model needs rework | Ops interviews before B08 build | REASONABLE |
| ASM-08 | 15-minute stock reservation matches vendor expectations | INFERENCE | Oversell complaints or inventory lock complaints | Vendor interviews; tune TTL as config (not hardcoded) | REASONABLE |
| ASM-09 | 7-day escrow hold is acceptable to vendors | INFERENCE | Vendor adoption resistance; payout disputes | Vendor interviews; make hold period a platform config with default 7 days | REASONABLE |
| ASM-10 | VAT 15% applies to marketplace sales and platform is responsible for charging | INFERENCE — regional norm | Tax exposure; repricing | Legal/tax opinion before launch (`DEP-09`) | UNSUPPORTED |
| ASM-11 | 10,000 concurrent users is the correct launch scale target | VERIFIED — brief (`C-25`) | Over/under-provisioning | Sponsor confirmation at Gate 0 | SUPPORTED |
| ASM-12 | Central Bank of Yemen permits platform-operated closed-loop wallets | INFERENCE | Wallet feature illegal → fundamental redesign | Legal opinion before implementation (`DEP-10`) | DANGEROUS |
| ASM-13 | Yemeni Personal Data Protection Law (2012) obligations are implementable by the planned controls | INFERENCE | Compliance gaps; penalties | Legal gap assessment (`DEP-09`) | UNSUPPORTED |
| ASM-14 | Budget, team size, and schedule baselines will be set by sponsor at Gate 0 | INSUFFICIENT EVIDENCE | Planning impossible; roadmap floats | Sponsor decision — blocking for `../21-completion/core/quality-gates.md` Gate 0 | UNSUPPORTED |
| ASM-15 | Arabic search quality is achievable with Elasticsearch Arabic analyzer (stemming) without custom NLP | INFERENCE | Poor search → discovery fails (FR-009) | Search relevance spike in Phase 1 with real product data | REASONABLE |

## Escalation Rule

`DANGEROUS` and `UNSUPPORTED` assumptions blocking critical paths (ASM-03, ASM-04, ASM-12, ASM-14) must be resolved before the quality gate that precedes implementation (`../21-completion/core/quality-gates.md`). They are also registered as risks (`RISK-006`, `RISK-012`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
