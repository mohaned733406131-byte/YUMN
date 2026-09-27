---
document_id: DOC-WF-012
title: "WF-011 — Vendor Onboarding: Register → KYC Submit → Approve → First Listing"
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-004, FR-007, FR-008]
related_documents: [DOC-WF-001, DOC-BA-004, DOC-BA-005]
---

# WF-011 — Vendor Onboarding: Register → KYC Submit → Approve → First Listing

| Field | Value |
|---|---|
| **Trigger** | Prospective merchant applies to sell on yumn |
| **Actors** | Vendor (`ACT-02`), System (`ACT-07` — OTP, SLA timer, notifications), Admin (`ACT-04` — KYC decision) |
| **Blocks** | B01 Identity · B03 Store Management · B13 Admin · B02 Product Catalog · B10 Notifications |
| **Preconditions** | Phone reachable for OTP (`DEP-06`); KYC document upload available (object storage `DEP-07`) |
| **Final state** | KYC = APPROVED, one store live, first product `ACTIVE` — or rejection with resubmission; SLA ≤48 h |

```text
[Register as vendor: phone + password + OTP] ──► account created (BR-AUTH-01…03)
        │
        ▼
[Create store] ── one store per account (BR-VND-02) ──► store DRAFT
        │
        ▼
[Submit KYC documents] ──► PENDING ──► SLA timer starts (≤48 h, BR-VND-03)
        │                                    │
        │                                    ├── Admin approves ──► KYC = APPROVED ──► store LIVE
        │                                    │                            │
        │                                    │                            ▼
        │                                    │                 [Create first product] ── publishable checks
        │                                    │                            │ ok
        │                                    │                            ▼
        │                                    │                 [ACTIVE product] ──► visible in search (BR-CAT-06)
        │                                    │
        │                                    └── Admin rejects ──► REJECTED + reason ──► resubmission allowed
        │                                                              (BR-VND-03, audit BR-PLT-06)
        ▼
 attempt to publish before approval ──► ✗ BLOCKED (BR-VND-01)
```

| Step | Actor | Action | System | Rules applied | Data changes | Failure / branch handling |
|---|---|---|---|---|---|---|
| 1 | Vendor | Register (phone + password) with OTP | B01 | `BR-AUTH-01…03` | user row, sessions | Same auth branches as WF-001 (lockout, OTP attempts) |
| 2 | Vendor | Create store (profile, branding, zones) | B03 | `BR-VND-02`, `FR-008` | store row (one per account) | Second store attempt → rejected (`BR-VND-02`) |
| 3 | Vendor | Submit KYC documents | B03 | `BR-VND-03` | KYC submission, status = PENDING, SLA deadline | Upload validation: type/size, no SVG execution (`SEC-REQ-011`) |
| 4 | System | Start 48 h decision SLA timer; notify admins | B03, B13 | `BR-VND-03` | SLA timer | SLA breach → escalation notice (no canon penalty value — `INSUFFICIENT EVIDENCE`) |
| 5 | Admin | Review and approve/reject | B13 | `BR-VND-03`, `BR-PLT-06` | KYC status APPROVED/REJECTED + audit entry | Rejection requires reason; resubmission allowed (`BR-VND-03`) |
| 6 | System | On approval: activate store; notify vendor | B03, B10 | `BR-VND-01`, `BR-NTF-04` | store active flag, notification | Rejection → vendor notified with reason and resubmit path |
| 7 | Vendor | Create first product (Arabic name, price, category, image, stock) | B02 | `BR-CAT-01`, `BR-CAT-04/05/08` | product draft | Missing mandatory field / non-physical type / bad image → validation error |
| 8 | Vendor | Publish | B02, B04 | `BR-VND-01`, `BR-CAT-06` | product → ACTIVE, index updated | Before KYC approval → blocked (`BR-VND-01`); suspended vendor → blocked (`BR-VND-04`) |
| 9 | Vendor | (Optional) invite staff (Viewer/Editor/Manager) | B03 | `BR-VND-06`, `BR-VND-07` | staff memberships | Only Owner invites/changes/removes staff; all queries store-scoped |
| 10 | System | Register first listing for onboarding metrics | B11 | `OBJ-06`, `AC-S-21` | onboarding events | First vendor live ≤48 h of application is the objective measure (`OBJ-06`) |

**Alternatives**
- **Bank/alternative KYC evidence:** document set defined by ops (`FR-007`); format details are implementation-level — no canon list exists (`INSUFFICIENT EVIDENCE` at analysis level).
- **Resubmission loop:** rejected → fix → resubmit → back to step 4; SLA restarts on resubmission (`BR-VND-03`).
- **Store suspension later:** `BR-VND-04` hides products, blocks new orders, freezes existing orders, holds payouts — reverses to active only via admin review.

**Exceptions**
- OTP/SMS unreachable → onboarding blocked at step 1 (hard dependency, `DEP-06`).
- Duplicate person/store attempt → phone uniqueness `BR-AUTH-01`; one store per account `BR-VND-02`.
- Publish attempts while PENDING → blocked (`BR-VND-01`); no bypass for Owner or staff.
- Cross-store data access by staff → denied at service layer (`BR-VND-07`).

**Rules applied:** `BR-AUTH-01/02/03`, `BR-VND-01…04/06/07`, `BR-CAT-01/04/05/06/08`, `BR-NTF-04`, `BR-PLT-05/06` · Constraints: `C-06`, `C-24` · Objectives: `OBJ-06`.

**Data touched:** users, stores, staff memberships, KYC submissions (status + SLA), audit entries, products (draft → ACTIVE), search index, onboarding metrics.

**Systems:** B01 Identity & Access · B03 Store Management · B13 Platform Administration · B02 Product Catalog · B04 Search & Discovery · B10 Notifications · B11 Analytics.

**Final state:** KYC APPROVED, store live with ≥1 ACTIVE product discoverable in search; vendor ready to receive orders (WF-004); full audit trail of the KYC decision.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
