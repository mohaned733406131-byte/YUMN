---
document_id: DOC-UC-000
title: UC-000 — Use Case Index & Template
category: 01-business-analysis
status: approved
version: 1.2
created: 2026-09-26
updated: 2026-09-29
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

## 2. Use Case Index (210 use cases)

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
| UC-043 | Rotate Refresh Tokens and Revoke Session Families on Reuse | System | B01 | FR-001 | P0 |
| UC-044 | Lock an Account After Five Consecutive Failed Logins | System | B01 | FR-001 | P0 |
| UC-045 | Sweep Expired Sessions and Orphaned Refresh Tokens | System | B01 | FR-001 | P2 |
| UC-046 | Expire Unpaid Stock Reservations After 15 Minutes | System | B02 | FR-005 | P0 |
| UC-047 | Commit Stock Reservations on Payment Success | System | B02 | FR-005 | P0 |
| UC-048 | Restore Stock When an Order Is Cancelled | System | B02 | FR-005, FR-012 | P1 |
| UC-049 | Reconcile the Inventory Ledger Against On-Hand Stock | System | B02 | FR-005 | P1 |
| UC-050 | Recompute Store Ratings Incrementally | System | B02 | FR-006 | P2 |
| UC-051 | Release Unused Wallet Authorization Holds | System | B07 | FR-013 | P1 |
| UC-052 | Execute Scheduled Vendor Payout Batches | System | B07 | FR-014 | P0 |
| UC-053 | Roll Over Payouts Below the 1,000 YER Minimum | System | B07 | FR-014 | P2 |
| UC-054 | Run Daily Ledger and Escrow Reconciliation | System | B07 | FR-013, FR-014 | P0 |
| UC-055 | Alert Finance on Reconciliation Mismatch | System | B07 | FR-013 | P0 |
| UC-056 | Generate Monthly Vendor Statements | System | B11 | FR-018, FR-014 | P1 |
| UC-057 | Reverse Commission Proportionally on Refund | System | B07 | FR-014, FR-016 | P1 |
| UC-058 | Execute Wallet Refunds to the Customer | System | B07 | FR-013, FR-016 | P0 |
| UC-059 | Fan Out Notifications Across Channels by Preference | System | B10 | FR-017 | P0 |
| UC-060 | Honor Per-Category Notification Opt-Outs | System | B10 | FR-017 | P1 |
| UC-061 | Deliver Mandatory Security Notifications | System | B10 | FR-017, FR-001 | P0 |
| UC-062 | Retry Failed Jobs and Alert on Dead-Letter Depth | System | B13 | FR-020 | P1 |
| UC-063 | Escalate Orders Stuck at CONFIRMED After 24 Hours | System | B06 | FR-012 | P1 |
| UC-064 | Guard Escrow Release While a Dispute Is Open | System | B07 | FR-014, FR-012 | P0 |
| UC-065 | Auto-Create a Support Ticket on the Third Delivery-Code Failure | System | B13 | FR-015, FR-020 | P1 |
| UC-066 | Auto-Close Stale Support Tickets | System | B13 | FR-020 | P2 |
| UC-067 | Synchronize the Search Index on Catalog Changes | System | B04 | FR-004, FR-009 | P1 |
| UC-068 | Gate Traffic on Liveness and Readiness Probes | System | B13 | FR-020 | P0 |
| UC-069 | Normalize Slugs and Preserve Canonical URLs | System | B04 | FR-009, FR-004 | P2 |
| UC-070 | Screen and Sanitize All Uploaded Files | System | B01 | FR-007, FR-004, FR-013 | P0 |
| UC-071 | Deliver Follower Marketing Notifications on New Products | System | B10 | FR-017, FR-008 | P2 |
| UC-072 | Cascade a Store Suspension Across Catalog, Orders, and Payouts | System | B03 | FR-007, FR-008 | P0 |
| UC-073 | Escalate KYC Decisions Past the 48-Hour SLA | System | B03 | FR-007 | P1 |
| UC-074 | Compensate a Failed Checkout Saga | System | B05 | FR-011, FR-010 | P0 |
| UC-075 | Rebuild the Order Timeline Read Model | System | B06 | FR-012 | P2 |
| UC-076 | Reconcile Wallet Top-Ups Against Provider Polls and Callbacks | System | B07 | FR-013 | P1 |
| UC-077 | Broadcast Delivery Offers to Eligible Couriers | System | B08 | FR-015 | P0 |
| UC-078 | Sweep Expired Delivery Codes | System | B08 | FR-015 | P1 |
| UC-079 | Render Notification Templates Per Locale | System | B10 | FR-017 | P1 |
| UC-080 | Aggregate Dashboard Analytics Rollups | System | B11 | FR-018 | P1 |
| UC-081 | Generate Report Export Files | System | B11 | FR-018 | P2 |
| UC-082 | Deliver Signed Outbound Webhooks with Retry | System | B13 | FR-020 | P1 |
| UC-083 | Enforce Audit Log Retention and Redaction | System | B13 | FR-020 | P1 |
| UC-084 | View the Admin Operations Dashboard | Admin | B11 | FR-018, FR-020 | P1 |
| UC-085 | Run a Platform Report | Admin | B11 | FR-018 | P1 |
| UC-086 | Export a Platform Report as CSV | Admin | B11 | FR-018 | P2 |
| UC-087 | Review the Daily Reconciliation Result | Admin | B07 | FR-013, FR-020 | P0 |
| UC-088 | Monitor Platform Health Probes | Admin | B13 | FR-020 | P1 |
| UC-089 | Search the User Directory | Admin | B01 | FR-003, FR-020 | P1 |
| UC-090 | View a User's Profile and Active Sessions | Admin | B01 | FR-003 | P1 |
| UC-091 | Suspend a User Account | Admin | B01 | FR-002, FR-020 | P0 |
| UC-092 | Reactivate a Suspended User Account | Admin | B01 | FR-002 | P1 |
| UC-093 | Browse the Store Directory | Admin | B03 | FR-008, FR-020 | P1 |
| UC-094 | View Store Detail and Open Exposure | Admin | B03 | FR-008 | P1 |
| UC-095 | Approve a Newly Created Store | Admin | B03 | FR-007 | P1 |
| UC-096 | Suspend a Store | Admin | B03 | FR-007, FR-020 | P0 |
| UC-097 | Re-Activate a Suspended Store | Admin | B03 | FR-007 | P1 |
| UC-098 | Freeze a Customer Wallet | Admin | B07 | FR-013, FR-020 | P0 |
| UC-099 | Unfreeze a Customer Wallet | Admin | B07 | FR-013 | P1 |
| UC-100 | Monitor the Support Ticket Queue | Admin | B13 | FR-020 | P1 |
| UC-101 | Claim or Assign a Support Ticket | Admin | B13 | FR-020 | P1 |
| UC-102 | Reply to a Support Ticket Thread | Admin | B13 | FR-020 | P1 |
| UC-103 | Resolve a Support Ticket with a Resolution Note | Admin | B13 | FR-020 | P1 |
| UC-104 | List CMS Pages | Admin | B12 | FR-019 | P2 |
| UC-105 | Create a CMS Page Draft | Admin | B12 | FR-019 | P1 |
| UC-106 | Edit a CMS Page Draft | Admin | B12 | FR-019 | P1 |
| UC-107 | Publish a CMS Page | Admin | B12 | FR-019 | P1 |
| UC-108 | Archive a CMS Page | Admin | B12 | FR-019 | P2 |
| UC-109 | List Banners with Schedule and Targeting | Admin | B12 | FR-019 | P2 |
| UC-110 | Create a Home Banner | Admin | B12 | FR-019 | P1 |
| UC-111 | Edit Banner Content, Targeting, and Schedule | Admin | B12 | FR-019 | P1 |
| UC-112 | Remove a Banner | Admin | B12 | FR-019 | P2 |
| UC-113 | List Platform Coupons | Admin | B12 | FR-019 | P2 |
| UC-114 | Create a Platform Coupon | Admin | B12 | FR-019 | P1 |
| UC-115 | Disable a Platform Coupon | Admin | B12 | FR-019 | P1 |
| UC-116 | View the Category Tree (Admin Scope) | Admin | B02 | FR-004, FR-020 | P1 |
| UC-117 | Create a Category Node | Admin | B02 | FR-004 | P1 |
| UC-118 | Rename, Re-Slug, or Move a Category Node | Admin | B02 | FR-004 | P1 |
| UC-119 | Delete an Empty Category | Admin | B02 | FR-004 | P2 |
| UC-120 | List the Attribute Dictionary | Admin | B02 | FR-004 | P2 |
| UC-121 | Create an Attribute | Admin | B02 | FR-004 | P1 |
| UC-122 | Update or Disable an Attribute | Admin | B02 | FR-004 | P2 |
| UC-123 | Delete an Unused Attribute | Admin | B02 | FR-004 | P2 |
| UC-124 | Monitor the Platform Return Queue | Admin | B09 | FR-016, FR-020 | P1 |
| UC-125 | Decide a Stalled or Disputed Return Case | Admin | B09 | FR-016 | P0 |
| UC-126 | Oversee Refund Receipts and Statuses | Admin | B09 | FR-016, FR-013 | P1 |
| UC-127 | Review Vendor Payout Runs | Admin | B07 | FR-014, FR-020 | P1 |
| UC-128 | Monitor Frozen Wallets | Admin | B07 | FR-013 | P2 |
| UC-129 | Triage the Refund Queue | Admin | B09 | FR-016 | P1 |
| UC-130 | Run the Delivery Performance Report | Admin | B11 | FR-015, FR-018 | P2 |
| UC-131 | Run the Vendor Health Report | Admin | B11 | FR-007, FR-018 | P2 |
| UC-132 | Run the KYC Throughput Report | Admin | B11 | FR-007, FR-018 | P2 |
| UC-133 | Run the User Growth Report | Admin | B11 | FR-003, FR-018 | P2 |
| UC-134 | Restore Previously Hidden Content | Admin | B12 | FR-006, FR-019 | P1 |
| UC-135 | Handle the 24-Hour Confirmation Escalation | Admin | B06 | FR-012 | P1 |
| UC-136 | Handle the Three-Failed-Attempt Delivery Escalation | Admin | B08 | FR-015, FR-012 | P1 |
| UC-137 | Read the Orders Queue as Moderator (Read-Only) | Moderator | B06 | FR-012, FR-020 | P1 |
| UC-138 | Read the Return Queue as Moderator (Read-Only) | Moderator | B09 | FR-016 | P2 |
| UC-139 | Review a Dispute as Moderator (Advisory Input) | Moderator | B09 | FR-016, FR-020 | P1 |
| UC-140 | Handle a Support Ticket as Moderator | Moderator | B13 | FR-020 | P1 |
| UC-141 | Resend an OTP (Registration, Login, or Reset) | Customer | B01 | FR-001 | P1 |
| UC-142 | Complete Step-Up OTP Verification for a Sensitive Change | Customer | B01 | FR-001, FR-002 | P1 |
| UC-143 | Log Out of the Current Device | Customer | B01 | FR-001 | P1 |
| UC-144 | Log Out of All Devices | Customer | B01 | FR-001 | P1 |
| UC-145 | Change Password While Signed In | Customer | B01 | FR-001 | P1 |
| UC-146 | View Active Device Sessions | Customer | B01 | FR-003 | P2 |
| UC-147 | Revoke Another Device's Session | Customer | B01 | FR-003 | P1 |
| UC-148 | View and Edit Profile | Customer | B01 | FR-003 | P1 |
| UC-149 | Add and Verify an Optional Email | Customer | B01 | FR-003 | P2 |
| UC-150 | Upload a Profile Avatar | Customer | B01 | FR-003 | P2 |
| UC-151 | Manage Account Preferences | Customer | B01 | FR-003 | P2 |
| UC-152 | Switch the Interface Locale (ar/en) | Customer | B01 | FR-003 | P1 |
| UC-153 | Request Account Deletion | Customer | B01 | FR-003 | P1 |
| UC-154 | Cancel a Pending Deletion Request | Customer | B01 | FR-003 | P2 |
| UC-155 | Browse the Personalized Home Feed | Customer | B12 | FR-019, FR-009 | P1 |
| UC-156 | Use Search Suggestions (Typeahead) | Customer | B04 | FR-009 | P2 |
| UC-157 | Browse Deals and the Promotion Gallery | Customer | B12 | FR-019 | P1 |
| UC-158 | Read Static Content and Help Pages | Customer | B12 | FR-019 | P2 |
| UC-159 | Track a Guest Order via a Tokenized Link | Customer | B06 | FR-012 | P2 |
| UC-160 | Clear the Entire Cart | Customer | B05 | FR-010 | P2 |
| UC-161 | Review the Authoritative Checkout Preview | Customer | B05 | FR-010, FR-011 | P1 |
| UC-162 | Apply and Validate a Coupon at Checkout | Customer | B05 | FR-011, FR-019 | P1 |
| UC-163 | Cancel an Order Before Dispatch | Customer | B06 | FR-012 | P0 |
| UC-164 | View Wallet Balance and Status | Customer | B07 | FR-013 | P0 |
| UC-165 | Write a Product Review After Delivery | Customer | B02 | FR-006 | P1 |
| UC-166 | Edit a Review Once Within 7 Days | Customer | B02 | FR-006 | P2 |
| UC-167 | Report a Review for Moderation | Customer | B02 | FR-006, FR-020 | P2 |
| UC-168 | Request a Return for Delivered Items | Customer | B09 | FR-016 | P0 |
| UC-169 | Track Return Request Status | Customer | B09 | FR-016 | P1 |
| UC-170 | View the Return Pickup Schedule | Customer | B09 | FR-016, FR-015 | P2 |
| UC-171 | Open a Dispute on a Delivered Order | Customer | B09 | FR-016, FR-012 | P0 |
| UC-172 | Submit Dispute Evidence | Customer | B09 | FR-016 | P1 |
| UC-173 | Review the Dispute Resolution Outcome | Customer | B09 | FR-016 | P1 |
| UC-174 | View Escrow Holding Status for Own Orders | Customer | B07 | FR-014 | P2 |
| UC-175 | Open the Notification Inbox | Customer | B10 | FR-017 | P1 |
| UC-176 | Mark Notifications Read or Remove Them | Customer | B10 | FR-017 | P2 |
| UC-177 | Configure Notification Preferences | Customer | B10 | FR-017 | P1 |
| UC-178 | Register This Device for Push Notifications | Customer | B10 | FR-017 | P1 |
| UC-179 | Manage Registered Push Devices | Customer | B10 | FR-017 | P2 |
| UC-180 | View Own Support Ticket List and Status | Customer | B13 | FR-020 | P2 |
| UC-181 | Resume an Existing Session on App Launch (Mobile) | Customer | B01 | FR-001 | P1 |
| UC-182 | Receive and Open a Deep-Linked Order Push | Customer | B10 | FR-017, FR-012 | P2 |
| UC-183 | Resubmit a Rejected Vendor Application | Vendor | B03 | FR-007 | P1 |
| UC-184 | Track the KYC Case Status and SLA Age | Vendor | B03 | FR-007 | P1 |
| UC-185 | View the Follower List and Count | Vendor | B03 | FR-008 | P2 |
| UC-186 | Manage Store Staff (Invite, Change Role, Remove) | Vendor | B03 | FR-002, FR-008 | P1 |
| UC-187 | Configure the Payout Account | Vendor | B07 | FR-014 | P1 |
| UC-188 | Unpublish a Product (Withdraw from Sale) | Vendor | B02 | FR-004 | P1 |
| UC-189 | Soft-Delete a Product | Vendor | B02 | FR-004 | P1 |
| UC-190 | Remove a Product Image | Vendor | B02 | FR-004 | P1 |
| UC-191 | Inspect SKU Reservations and Expiry | Vendor | B02 | FR-005 | P2 |
| UC-192 | Review the Sub-Order Queue | Vendor | B06 | FR-012 | P1 |
| UC-193 | Cancel a Sub-Order Before Pickup | Vendor | B06 | FR-012, FR-014 | P0 |
| UC-194 | Review the Return Queue | Vendor | B09 | FR-016 | P1 |
| UC-195 | Inspect a Received Return Within 72 Hours | Vendor | B09 | FR-016 | P0 |
| UC-196 | Respond to a Dispute with Evidence | Vendor | B09 | FR-016 | P0 |
| UC-197 | Track Dispute Status | Vendor | B09 | FR-016 | P1 |
| UC-198 | Request a Payout | Vendor | B07 | FR-014 | P0 |
| UC-199 | View the Sales Dashboard | Vendor | B11 | FR-018 | P1 |
| UC-200 | Run a Store Report | Vendor | B11 | FR-018 | P2 |
| UC-201 | Export a Store Report as CSV | Vendor | B11 | FR-018 | P2 |
| UC-202 | View Store Reviews | Vendor | B02 | FR-006 | P2 |
| UC-203 | List Store Coupons | Vendor | B12 | FR-019 | P2 |
| UC-204 | Open a Support Ticket About an Order | Vendor | B13 | FR-020 | P2 |
| UC-205 | Release an Accepted Assignment Back to the Pool | Delivery Provider | B08 | FR-015 | P1 |
| UC-206 | Update Courier Profile and Served Zones | Delivery Provider | B08 | FR-015 | P2 |
| UC-207 | Toggle Availability Online/Offline | Delivery Provider | B08 | FR-015 | P1 |
| UC-208 | Handle the 24-Hour Code Lockout After Third Failure | Delivery Provider | B08 | FR-015 | P1 |
| UC-209 | Follow the Order Timeline During a Delivery | Delivery Provider | B06 | FR-012, FR-015 | P2 |
| UC-210 | Open a Support Ticket About a Delivery | Delivery Provider | B13 | FR-020 | P2 |

## 3. Totals per Actor

| Actor | Use Cases | Range |
|---|---|---|
| Customer (ACT-01) | 58 | UC-001 … UC-014, UC-041 … UC-042, UC-141 … UC-182 |
| Vendor (ACT-02) | 32 | UC-015 … UC-024, UC-183 … UC-204 |
| Delivery Provider (ACT-03) | 12 | UC-025 … UC-030, UC-205 … UC-210 |
| Admin (ACT-04) | 59 | UC-031 … UC-036, UC-084 … UC-136 |
| Super Admin (ACT-05) | 1 | UC-037 |
| Moderator (ACT-06) | 5 | UC-038, UC-137 … UC-140 |
| System (ACT-07) | 43 | UC-039 … UC-040, UC-043 … UC-083 |
| **Total** | **210** | UC-001 … UC-210 |

Priority totals: P0 = 47, P1 = 107, P2 = 56. Block coverage: B01 (28), B02 (25), B03 (15), B04 (5), B05 (7), B06 (13), B07 (23), B08 (14), B09 (17), B10 (12), B11 (13), B12 (18), B13 (20).

## 4. Related Documents

- `00-project-overview/actors-and-roles.md` (DOC-OVR-007) — the 7 actors
- `01-business-analysis/business-rules.md` (DOC-BA-005) — all `BR-*` referenced here
- `02-requirements/requirements-overview.md` (DOC-REQ-001) — all `FR-*` referenced here
- `03-system-analysis/state-transitions.md` (DOC-SA-010) — the 17-state machine used in postconditions

## 5. Coverage Matrix (portal × feature area → UC IDs)

Feature areas are derived from blocks `B01…B13` (`06-backend/backend-architecture.md` §3). Portal = the surface the primary actor uses. Every UC appears in exactly one portal group, so the matrix accounts for all **210** use cases (completeness proof, AUD-01/D-02). Admin console includes Super Admin (`UC-037`) and Moderator (`UC-038`, `UC-137 … UC-140`); Shared/System includes the automated jobs `UC-039 … UC-040`.

| Portal | Feature area | UC IDs | Count |
|---|---|---|---|
| **Shared/System (ACT-07)** | **Portal subtotal** | UC-039 … UC-040, UC-043 … UC-083 | **43** |
| | Identity, auth & profiles (B01) | UC-043 … UC-045, UC-070 | 4 |
| | Catalog, stock & reviews (B02) | UC-046 … UC-050 | 5 |
| | Stores & vendors (B03) | UC-072 … UC-073 | 2 |
| | Search & discovery (B04) | UC-067, UC-069 | 2 |
| | Cart & checkout (B05) | UC-074 | 1 |
| | Orders & timelines (B06) | UC-063, UC-075 | 2 |
| | Wallet, escrow & payouts (B07) | UC-039, UC-051 … UC-055, UC-057 … UC-058, UC-064, UC-076 | 10 |
| | Delivery & shipping (B08) | UC-077 … UC-078 | 2 |
| | Notifications (B10) | UC-040, UC-059 … UC-061, UC-071, UC-079 | 6 |
| | Analytics & reports (B11) | UC-056, UC-080 … UC-081 | 3 |
| | Platform, support & moderation (B13) | UC-062, UC-065 … UC-066, UC-068, UC-082 … UC-083 | 6 |
| **Admin console (ACT-04/05/06)** | **Portal subtotal** | UC-031 … UC-038, UC-084 … UC-140 | **65** |
| | Identity, auth & profiles (B01) | UC-037, UC-089 … UC-092 | 5 |
| | Catalog, stock & reviews (B02) | UC-116 … UC-123 | 8 |
| | Stores & vendors (B03) | UC-031, UC-093 … UC-097 | 6 |
| | Orders & timelines (B06) | UC-033, UC-135, UC-137 | 3 |
| | Wallet, escrow & payouts (B07) | UC-034, UC-087, UC-098 … UC-099, UC-127 … UC-128 | 6 |
| | Delivery & shipping (B08) | UC-136 | 1 |
| | Returns & disputes (B09) | UC-124 … UC-126, UC-129, UC-138 … UC-139 | 6 |
| | Analytics & reports (B11) | UC-084 … UC-086, UC-130 … UC-133 | 7 |
| | Content, banners & coupons (B12) | UC-104 … UC-115, UC-134 | 13 |
| | Platform, support & moderation (B13) | UC-032, UC-035 … UC-036, UC-038, UC-088, UC-100 … UC-103, UC-140 | 10 |
| **Customer web + mobile (ACT-01)** | **Portal subtotal** | UC-001 … UC-014, UC-041 … UC-042, UC-141 … UC-182 | **58** |
| | Identity, auth & profiles (B01) | UC-002 … UC-005, UC-141 … UC-154, UC-181 | 19 |
| | Catalog, stock & reviews (B02) | UC-007, UC-165 … UC-167 | 4 |
| | Stores & vendors (B03) | UC-008 | 1 |
| | Search & discovery (B04) | UC-001, UC-006, UC-156 | 3 |
| | Cart & checkout (B05) | UC-009 … UC-011, UC-160 … UC-162 | 6 |
| | Orders & timelines (B06) | UC-012, UC-159, UC-163 | 3 |
| | Wallet, escrow & payouts (B07) | UC-041 … UC-042, UC-164, UC-174 | 4 |
| | Delivery & shipping (B08) | UC-013 | 1 |
| | Returns & disputes (B09) | UC-168 … UC-173 | 6 |
| | Notifications (B10) | UC-175 … UC-179, UC-182 | 6 |
| | Content, banners & coupons (B12) | UC-155, UC-157 … UC-158 | 3 |
| | Platform, support & moderation (B13) | UC-014, UC-180 | 2 |
| **Vendor panel (ACT-02)** | **Portal subtotal** | UC-015 … UC-024, UC-183 … UC-204 | **32** |
| | Catalog, stock & reviews (B02) | UC-017 … UC-018, UC-024, UC-188 … UC-191, UC-202 | 8 |
| | Stores & vendors (B03) | UC-015 … UC-016, UC-183 … UC-186 | 6 |
| | Orders & timelines (B06) | UC-019 … UC-020, UC-192 … UC-193 | 4 |
| | Wallet, escrow & payouts (B07) | UC-022, UC-187, UC-198 | 3 |
| | Returns & disputes (B09) | UC-021, UC-194 … UC-197 | 5 |
| | Analytics & reports (B11) | UC-199 … UC-201 | 3 |
| | Content, banners & coupons (B12) | UC-023, UC-203 | 2 |
| | Platform, support & moderation (B13) | UC-204 | 1 |
| **Courier app (ACT-03)** | **Portal subtotal** | UC-025 … UC-030, UC-205 … UC-210 | **12** |
| | Orders & timelines (B06) | UC-209 | 1 |
| | Delivery & shipping (B08) | UC-025 … UC-030, UC-205 … UC-208 | 10 |
| | Platform, support & moderation (B13) | UC-210 | 1 |
| | **Total** | UC-001 … UC-210 | **210** |

Portal subtotals: 43 + 65 + 58 + 32 + 12 = **210** = §3 actor total.

### 5.1 PENDING / backlog (not minted)

Recorded as INSUFFICIENT EVIDENCE — deliberately excluded from the 210; never counted as use cases.

| PENDING item | Reason — not minted (spec §F) |
|---|---|
| `M-01` FX rates display | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-02` Al-Kuraimi / Jeeb payment rails | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-03` Email login | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-04` Escrow maturity vendor note | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-13` Flags console | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-14` Departments | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-15` Invoices | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-16` Provider registry | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-17` Wishlist | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-19` Calendar | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-21` Search analytics UI | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-22` Engagement stats | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-23` PWA install | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-24` Analytics UI | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| `M-25` Cart abandonment | Owner M-* backlog item; INSUFFICIENT EVIDENCE |
| Re-open an existing support ticket | No API exists (spec §F) |
| Moderator audit-log access | Security finding 26 unresolved (spec §F) |
| `M-20` Vendor right-of-reply to a hidden review | Owner M-* backlog item; INSUFFICIENT EVIDENCE |

### 5.2 Numbers honesty note (derived vs owner-supplied)

- **Derived: 210 use cases.** Countable from the `UC-NNN.md` files in this directory (42 pre-existing + 168 minted by session 010) and reproduced by the §2 index (210 rows), §3 totals, and the §5 matrix above. This is the repository-derived number.
- **Owner-supplied: "over 350".** Target stated by the owner in `prompt-010.md` §1 — owner-supplied, **INSUFFICIENT EVIDENCE**, not derivable from this repository.
- The two numbers are published separately and never blended. The likely basis for the owner figure is **scenario-level counting**: across the 210 UCs, main + alternative + exception scenarios total ≈ **1,400+** scenarios — a different unit of count than use-case files.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial index (40 use cases) | Initial analysis |
| 1.1 | 2026-09-28 | `UC-041` (Top Up Wallet, customer funding leg) and `UC-042` (View Wallet Statement) added; totals → 42 use cases (Customer 16, P0 18, P1 19, B07 5) | Session-007 UC gap from `describ.md` §8: only the admin top-up half (`UC-034`) existed and `FR-013`'s statement had no use case to trace to (root README §10) |
| 1.2 | 2026-09-29 | §2 index 42 → **210 use cases** (+168 rows UC-043…UC-210), §3 actor totals/priority/block recompute, new §5 coverage matrix + PENDING backlog + derived-vs-owner numbers note | Session-010 owner directive (prompt-010.md §1) — full portal use-case coverage; completeness proven by matrix (AUD-01/D-02) |
