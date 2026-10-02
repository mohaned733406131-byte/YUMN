---
document_id: DOC-OVR-010
title: Dependencies (DEP-01 … DEP-12)
category: 00-project-overview
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-10-02
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-001, INT-REQ-002, INT-REQ-003]
related_documents: [DOC-OVR-009, DOC-INT-001]
---

# Dependencies

| ID | Dependency | Type | Needed For | Failure / Delay Impact | Owner | Status |
|---|---|---|---|---|---|---|
| DEP-01 | Node.js 20 LTS, TypeScript 5.x runtime | Technical | All backend/frontend build | No development start | Engineering | Available |
| DEP-02 | PostgreSQL 16 server | Technical | All persistence (`C-19`) | No development start | DevOps | Available |
| DEP-03 | Redis 7 server | Technical | Sessions, cache, BullMQ (`C-20`) | Queues/cache inoperable | DevOps | Available |
| DEP-04 | Elasticsearch 8 cluster | Technical | Search & discovery (`FR-009`) | Search degraded → browse-by-category fallback only | DevOps | Available |
| DEP-05 | m-Floos + OneCash merchant API access (sandbox → production) | External commercial | Wallet top-ups (`FR-013`, `C-05`) | Top-up limited to manual bank transfer | Business development | **NOT STARTED** (blocks FR-013 production) |
| DEP-06 | SMS provider contract (Telesom and/or Sabafon) + WhatsApp Business API approval | External commercial | OTP delivery, notifications (`FR-001`, `FR-017`) | **Registration blocked** — hardest blocker | Business development | **NOT STARTED** (Phase 0 gate) |
| DEP-07 | MinIO / S3-compatible object storage | Technical | Product images, review images | Media upload unavailable | DevOps | Available |
| DEP-08 | Domains, TLS certificates, CDN (Cloudflare) | External | Production launch | No public launch | DevOps | Not started |
| DEP-09 | Legal opinions: VAT treatment (ASM-10/ASM-12), data protection (ASM-13) | External professional | Compliance design | Compliance risk; possible redesign | Legal / sponsor | Not started |
| DEP-10 | Central Bank position on closed-loop wallets (ASM-12) | Regulatory | Wallet architecture legitimacy | **Existential** — wallet-only model at risk | Sponsor / legal | Not started |
| DEP-11 | Design assets: logo, brand tokens, Arabic copy | Internal input | Frontend/UI work | Design phase stalls | Design / product | Partial (brand tokens defined in `../11-ui-ux/core/design-system.md`) |
| DEP-12 | Test device lab (Android versions, iOS) + real carrier SIMs | Tooling | Mobile app testing, OTP testing | Mobile QA cannot complete | QA | Not started |

## Dependency Ordering (critical path)

```text
DEP-06 (SMS/WhatsApp) ──► FR-001 usable ──► everything else
DEP-10 (regulatory)   ──► FR-013/FR-014 design lock ──► payment build
DEP-05 (wallet rails) ──► FR-013 production top-ups
DEP-09 (legal)        ──► NFR/compliance sign-off ──► launch
DEP-11 (design)       ──► 05-frontend build
```

## Risk Linkage

DEP-05 → `RISK-003` · DEP-06 → `RISK-006` · DEP-10 → `RISK-012` · DEP-08 → `RISK-014` (see `17-risk-management/core/risk-register.md`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
