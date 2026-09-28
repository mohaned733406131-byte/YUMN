---
document_id: DOC-UC-000
title: UC-000 — Use Case Index & Template
category: 01-business-analysis
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-011, FR-012, FR-015, FR-020]
related_documents: [DOC-BA-005, DOC-OVR-007, DOC-REQ-001, DOC-SA-010]
---

# Use Cases — Index, ID Scheme & Template

**Single index of all use cases for the yumn platform.** Use case IDs follow `UC-NNN` (zero-padded, sequential from `UC-001`); document IDs follow `DOC-UC-NNN` where the numeric part matches the UC number (`UC-017` → `DOC-UC-017`). This file itself is `UC-000` / `DOC-UC-000`. Files live in `01-business-analysis/use-cases/` and are named `UC-NNN.md`.

Rules:
- IDs are never reused or renumbered; a retired use case keeps its file with status `SUPERSEDED`.
- Every UC names exactly one primary actor from the canonical 7 (`DOC-OVR-007`); supporting actors are listed in the scenario steps.
- Every UC references only **existing** `BR-*` IDs from `business-rules.md` (DOC-BA-005) and **existing** `FR-*` IDs from `requirements-overview.md` (DOC-REQ-001). Never invent IDs.
- API touchpoints in scenarios are conceptual (`POST /orders`) — the authoritative contract is `07-api/`.

## 1. UC Template (applies to every UC-NNN.md)

Each file = YAML frontmatter + body. Frontmatter keys: `document_id`, `title`, `category: 01-business-analysis`, `status: approved`, `version`, `created`, `updated`, `author`, `source_of_truth`, `related_requirements`, `related_documents`.

Body sections, in fixed order (45–70 lines per file):

| # | Section | Content |
|---|---|---|
| 1 | Header info | Use Case ID, Title, Actor (ID + name), Trigger, Priority (P0/P1/P2), Goal (1 sentence), Preconditions |
| 2 | Main Scenario | Numbered steps 1…n; actor action ↔ system response, with conceptual API touchpoints |
| 3 | Alternative Scenarios | `A1`, `A2`, … — legitimate alternate paths (insufficient balance, OTP lockout, stock conflict) |
| 4 | Exception Scenarios | `E1`, `E2`, … — failures (network error, provider outage, concurrent modification) |
| 5 | Postconditions | Success/failure end states, incl. state-machine effects (17 states, `DOC-SA-010`) |
| 6 | Business Rules Applied | Exact `BR-*` IDs from DOC-BA-005 (no new IDs) |
| 7 | Related Requirements | Exact `FR-*` IDs from DOC-REQ-001 |
| 8 | Permissions / Data / Dependencies | Actor permissions, entities touched, external systems |
| 9 | Acceptance Criteria | `AC-UCnnn-01/02/03…` — testable one-liners (given/when/then style) |

Priority scale: **P0** = must-have for launch (core money/fulfillment path), **P1** = important, **P2** = valuable but deferrable.

## 2. Use Case Index (42 use cases)

| ID | Title | Actor | Block | FR refs | Priority |
|---|---|---|---|---|---|
| UC-001 | Browse Marketplace as Guest | Customer | B04 | FR-004, FR-009 | P1 |
| UC-002 | Register with Phone + OTP | Customer | B01 | FR-001, FR-003 | P0 |
| UC-003 | Login with Phone & Password | Customer | B01 | FR-001 | P0 |
| UC-004 | Reset Password via OTP | Customer | B01 | FR-001, FR-003 | P1 |
| UC-005 | Manage Addresses | Customer | B01 | FR-003 | P1 |
| UC-006 | Search Products | Customer | B04 | FR-009 | P1 |
| UC-007 | View Product Detail | Customer | B02 | FR-004, FR-006 | P1 |
| UC-008 | Follow a Store | Customer | B03 | FR-008, FR-017 | P2 |
| UC-009 | Add Product to Cart | Customer | B05 | FR-010, FR-005 | P0 |
| UC-010 | Manage Cart | Customer | B05 | FR-010 | P1 |
| UC-011 | Checkout with Wallet Payment | Customer | B05 | FR-011, FR-013, FR-010 | P0 |
| UC-012 | Track Order | Customer | B06 | FR-012, FR-017 | P1 |
| UC-013 | Confirm Receipt with Delivery Code | Customer | B08 | FR-015, FR-012 | P0 |
| UC-014 | Contact Support | Customer | B13 | FR-020 | P2 |
| UC-015 | Register as Vendor & Submit KYC | Vendor | B03 | FR-007 | P0 |
| UC-016 | Manage Store Profile | Vendor | B03 | FR-008 | P1 |
| UC-017 | Create / Edit Product Listing | Vendor | B02 | FR-004, FR-007 | P0 |
| UC-018 | Manage Inventory | Vendor | B02 | FR-005 | P1 |
| UC-019 | View & Accept Incoming Order | Vendor | B06 | FR-012, FR-007 | P0 |
| UC-020 | Mark Order Ready for Pickup | Vendor | B06 | FR-012, FR-015 | P0 |
| UC-021 | Respond to Return Request | Vendor | B09 | FR-016, FR-012 | P1 |
| UC-022 | View Finances & Payouts | Vendor | B07 | FR-014, FR-018 | P1 |
| UC-023 | Create Store Coupon | Vendor | B12 | FR-019 | P2 |
| UC-024 | Respond to Customer Review | Vendor | B02 | FR-006 | P2 |
| UC-025 | View Available Deliveries | Delivery Provider | B08 | FR-015 | P1 |
| UC-026 | Accept Delivery Assignment | Delivery Provider | B08 | FR-015 | P0 |
| UC-027 | Confirm Package Pickup | Delivery Provider | B08 | FR-015 | P0 |
| UC-028 | Update Transit & Attempt Delivery | Delivery Provider | B08 | FR-015 | P1 |
| UC-029 | Record Failed Delivery Attempt | Delivery Provider | B08 | FR-015, FR-017 | P1 |
| UC-030 | Confirm Delivery with 6-Digit Code | Delivery Provider | B08 | FR-015, FR-012 | P0 |
| UC-031 | Approve / Reject Vendor KYC | Admin | B03 | FR-007, FR-020 | P0 |
| UC-032 | Moderate Product or Review | Admin | B13 | FR-006, FR-020 | P1 |
| UC-033 | Manage Orders & Disputes | Admin | B06 | FR-012, FR-016, FR-020 | P0 |
| UC-034 | Verify Bank-Transfer Top-Up | Admin | B07 | FR-013, FR-020 | P1 |
| UC-035 | Manage Platform Settings | Admin | B13 | FR-020 | P1 |
| UC-036 | View Audit Log | Admin | B13 | FR-020 | P2 |
| UC-037 | Manage Roles & Permissions | Super Admin | B01 | FR-002, FR-020 | P0 |
| UC-038 | Review Flagged Content | Moderator | B13 | FR-006, FR-017, FR-020 | P1 |
| UC-039 | Auto-Release Escrow After 7 Days | System | B07 | FR-014 | P0 |
| UC-040 | Send OTP with Provider Failover | System | B10 | FR-001, FR-017 | P0 |
| UC-041 | Top Up Wallet | Customer | B07 | FR-013, FR-017 | P0 |
| UC-042 | View Wallet Statement | Customer | B07 | FR-013 | P1 |

## 3. Totals per Actor

| Actor | Use Cases | Range |
|---|---|---|
| Customer (ACT-01) | 16 | UC-001 … UC-014, UC-041 … UC-042 |
| Vendor (ACT-02) | 10 | UC-015 … UC-024 |
| Delivery Provider (ACT-03) | 6 | UC-025 … UC-030 |
| Admin (ACT-04) | 6 | UC-031 … UC-036 |
| Super Admin (ACT-05) | 1 | UC-037 |
| Moderator (ACT-06) | 1 | UC-038 |
| System (ACT-07) | 2 | UC-039, UC-040 |
| **Total** | **42** | UC-001 … UC-042 |

Priority totals: P0 = 18, P1 = 19, P2 = 5. Block coverage: B01 (5), B02 (4), B03 (4), B04 (2), B05 (3), B06 (4), B07 (5), B08 (7), B09 (1), B10 (1), B11 (0 — covered via `FR-018` reporting inside UC-022), B12 (1), B13 (5).

## 4. Related Documents

- `00-project-overview/actors-and-roles.md` (DOC-OVR-007) — the 7 actors
- `01-business-analysis/business-rules.md` (DOC-BA-005) — all `BR-*` referenced here
- `02-requirements/requirements-overview.md` (DOC-REQ-001) — all `FR-*` referenced here
- `03-system-analysis/state-transitions.md` (DOC-SA-010) — the 17-state machine used in postconditions

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial index (40 use cases) | Initial analysis |
| 1.1 | 2026-09-28 | `UC-041` (Top Up Wallet, customer funding leg) and `UC-042` (View Wallet Statement) added; totals → 42 use cases (Customer 16, P0 18, P1 19, B07 5) | Session-007 UC gap from `describ.md` §8: only the admin top-up half (`UC-034`) existed and `FR-013`'s statement had no use case to trace to (root README §10) |
