---
document_id: DOC-UC-000
title: UC-000 — Use Case Index & Template
category: 01-business-analysis
status: approved
version: 1.3
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-011, FR-012, FR-015, FR-020]
related_documents: [DOC-BA-005, DOC-OVR-007, DOC-REQ-001, DOC-SA-010]
---

# Use Cases — Index, ID Scheme & Template

**Single index of all use cases for the yumn platform.** Use case IDs follow `UC-NNN` (zero-padded, sequential from `UC-001`); document IDs follow `DOC-UC-NNN` where the numeric part matches the UC number (`UC-017` → `DOC-UC-017`). This file itself is `UC-000` / `DOC-UC-000`. Files live in `01-business-analysis/` and are named `UC-NNN.md`.

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

## 2. Use Case Index (420 use cases)

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
| UC-211 | Enforce OTP and Login Rate-Limit Budgets With 429 and Retry-After | System | B01 | FR-001 | P1 |
| UC-212 | Evict the Oldest Device Session on the Sixth Concurrent Login | System | B01 | FR-001 | P1 |
| UC-213 | Invalidate Every Session When a Password Reset Succeeds | System | B01 | FR-001 | P1 |
| UC-214 | Expire OTP Challenges After Five Minutes and Reset Attempt Counters | System | B01 | FR-001 | P1 |
| UC-215 | Lift the Account Lock Automatically After the 15-Minute Timeout | System | B01 | FR-001 | P1 |
| UC-216 | Anonymize Profile PII for Accounts Dormant 24 Months After Notice | System | B01 | FR-003 | P2 |
| UC-217 | Serialize Contended Stock Reservations to Prevent Oversell | System | B02 | FR-005 | P0 |
| UC-218 | Resolve the Reservation-Expiry Race at Checkout Confirmation | System | B02 | FR-005 | P0 |
| UC-219 | Purge Orphaned Product Images Only When No Order References Them | System | B02 | FR-004 | P2 |
| UC-220 | Delete Superseded KYC Document Sets When a Resubmission Is Accepted | System | B03 | FR-007 | P2 |
| UC-221 | Purge KYC Objects and Metadata Five Years After Account Closure | System | B03 | FR-007 | P2 |
| UC-222 | Rebuild the Search Index From Source After an Outage | System | B04 | FR-009 | P1 |
| UC-223 | Serve Category Browse From Cache While Search Is Degraded | System | B04 | FR-009 | P1 |
| UC-224 | Alert on Search Indexing Lag Beyond the Five-Minute Delete SLO | System | B04 | FR-009 | P2 |
| UC-225 | Return the Original Order on Idempotent Checkout Replay | System | B05 | FR-011 | P0 |
| UC-226 | Reject Order Totals Outside the 500–5,000,000 YER Bounds | System | B05 | FR-011 | P0 |
| UC-227 | Expire Idempotency-Key Records After 24 Hours | System | B05 | FR-011 | P2 |
| UC-228 | Auto-Accept PLACED Orders for Stores With Auto-Accept Enabled | System | B06 | FR-012 | P2 |
| UC-229 | Roll the Master Order Up to COMPLETED When Every Sub-Order Settles | System | B06 | FR-012 | P1 |
| UC-230 | Append the State-History Backstop Row on Every Order Transition | System | B06 | FR-012 | P1 |
| UC-231 | Auto-Cancel Top-Ups Left Pending Beyond the Confirmation Window | System | B07 | FR-013 | P1 |
| UC-232 | Open a Circuit Breaker on a Failing Top-Up Provider and Degrade to Bank Transfer | System | B07 | FR-013 | P1 |
| UC-233 | Serialize Concurrent Wallet Debits to Keep Balances Non-Negative | System | B07 | FR-013 | P0 |
| UC-234 | Credit Refunds Into Frozen Wallets While Debits Stay Blocked | System | B07 | FR-013 | P1 |
| UC-235 | Drain the Escrow Release Backlog After Scheduler Recovery | System | B07 | FR-014 | P1 |
| UC-236 | Post Ledger Corrections as Compensating Entries Only | System | B07 | FR-013 | P1 |
| UC-237 | Route VAT Rounding Residuals to the Platform Rounding Account | System | B07 | FR-013 | P2 |
| UC-238 | Issue a Fresh 6-Digit Delivery Code at OUT_FOR_DELIVERY | System | B08 | FR-015 | P0 |
| UC-239 | Award a Delivery Offer to the First Courier Acceptance Only | System | B08 | FR-015 | P0 |
| UC-240 | Lift the Delivery-Code Confirmation Lock After 24 Hours | System | B08 | FR-015 | P1 |
| UC-241 | Auto-Approve Returns Left Uninspected for 72 Hours | System | B09 | FR-016 | P1 |
| UC-242 | Auto-Escalate Return Decisions Stalled Past 48 Hours | System | B09 | FR-016 | P1 |
| UC-243 | Advance the Order to COMPLETED After a Rejected Return | System | B09 | FR-016 | P1 |
| UC-244 | Deduplicate Notification Fan-Out by Event, Recipient, and Channel | System | B10 | FR-017 | P1 |
| UC-245 | Throttle Per-Channel Notification Sends to Protect Provider Quotas | System | B10 | FR-017 | P1 |
| UC-246 | Record SMS and WhatsApp Delivery Receipts per Message | System | B10 | FR-017 | P1 |
| UC-247 | Publish the Weekly Retention Purge Report | System | B11 | FR-018 | P2 |
| UC-248 | Enforce Retention Windows on Metrics, Logs, and Traces | System | B11 | FR-018 | P2 |
| UC-249 | Purge CDN and ISR Caches When Content Is Published | System | B12 | FR-019 | P1 |
| UC-250 | Invalidate the Coupon Validation Cache on Admin Disable | System | B12 | FR-019 | P2 |
| UC-251 | Verify the Audit Hash Chain Nightly and Alert on Tamper | System | B13 | FR-020 | P0 |
| UC-252 | Page On-Call When Backup Freshness Breaches Its Window | System | B13 | FR-020 | P0 |
| UC-253 | Run the Daily Retention Purge With Floor Guards and Evidence | System | B13 | FR-020 | P1 |
| UC-254 | Create Next-Month Table Partitions Ahead of Deployment | System | B13 | FR-020 | P1 |
| UC-255 | Cascade Primary-Data Deletion to Search, Cache, Queues, and Objects | System | B13 | FR-020 | P1 |
| UC-256 | Investigate Account-Lockout and OTP-Abuse Signals | Admin | B01 | FR-001, FR-020 | P1 |
| UC-257 | Execute the Incident Rotation Runbook for a Leaked Secret | Super Admin | B01 | FR-001, FR-020 | P0 |
| UC-258 | Force Session Revalidation After a Signing-Key Rotation | Super Admin | B01 | FR-001, FR-002 | P1 |
| UC-259 | Audit Four-Eyes Compliance on Money Operations | Admin | B01 | FR-002, FR-020 | P1 |
| UC-260 | Review a Target's Recent Administrative Actions Before Enforcement | Admin | B01 | FR-002, FR-020 | P2 |
| UC-261 | Sample-Verify Completed Data-Deletion Requests | Admin | B01 | FR-003, FR-020 | P1 |
| UC-262 | Deactivate a Category Node from the Storefront | Admin | B02 | FR-004 | P2 |
| UC-263 | Confirm Rating Recomputation After a Review Is Hidden | Admin | B02 | FR-006 | P2 |
| UC-264 | Confirm a Hidden Product Is Delisted From Search and Storefront | Admin | B02 | FR-004, FR-019 | P2 |
| UC-265 | Prioritize the Overdue KYC Queue Before the 48-Hour SLA | Admin | B03 | FR-007, FR-020 | P1 |
| UC-266 | Clear a KYC Blocker That Prevents Store Reactivation | Admin | B03 | FR-007, FR-019 | P1 |
| UC-267 | Verify the Cascade Effects of a Store Suspension | Admin | B03 | FR-007, FR-020 | P2 |
| UC-268 | Set the Platform Commission Tier Within the 5-20% Bound | Super Admin | B03 | FR-014, FR-019 | P1 |
| UC-269 | Cancel an Order as the Platform of Last Resort | Admin | B06 | FR-012, FR-014 | P1 |
| UC-270 | Force a Sub-Order State Correction Within the 17-State Table | Admin | B06 | FR-012, FR-020 | P0 |
| UC-271 | Assemble the Order Timeline Evidence Pack for a Dispute | Admin | B06 | FR-012, FR-016 | P1 |
| UC-272 | Trace a Master Order to Its Sub-Orders During an Investigation | Admin | B06 | FR-012 | P2 |
| UC-273 | Investigate an Escalated Illegal Order-State Transition | Admin | B06 | FR-012, FR-020 | P1 |
| UC-274 | Second-Approve a Large Bank-Transfer Top-Up | Super Admin | B07 | FR-013, FR-020 | P1 |
| UC-275 | Cross-Check Pending Top-Ups Against the Bank Statement | Admin | B07 | FR-013, FR-014 | P1 |
| UC-276 | Release an Unused Authorization Hold Manually | Admin | B07 | FR-013 | P1 |
| UC-277 | Record the Disposition of a Reconciliation Mismatch | Admin | B07 | FR-013, FR-014 | P0 |
| UC-278 | Approve the Vendor Payout Batch for Execution | Admin | B07 | FR-014, FR-020 | P0 |
| UC-279 | Freeze Payouts and Top-Up Crediting on a Ledger-Integrity Alarm | Admin | B07 | FR-013, FR-014, FR-020 | P0 |
| UC-280 | Run the Pre-Launch Money-Cycle Audit | Admin | B07 | FR-013, FR-014 | P0 |
| UC-281 | Reassign a Stalled Delivery Back to the Offer Pool | Admin | B08 | FR-015 | P1 |
| UC-282 | Pull Delivery Proof for a Dispute Review | Admin | B08 | FR-015, FR-016 | P2 |
| UC-283 | Arbitrate a Dispute and Choose the Prevailing Party | Admin | B09 | FR-016, FR-020 | P0 |
| UC-284 | Attach Platform Evidence to a Dispute Case | Admin | B09 | FR-016 | P1 |
| UC-285 | Track Open Disputes and Their Frozen Escrow Exposure | Admin | B09 | FR-014, FR-016 | P1 |
| UC-286 | Verify Refund Credits Within the 3-Business-Day SLA | Admin | B09 | FR-013, FR-016 | P1 |
| UC-287 | Run the Orders Report | Admin | B11 | FR-018, FR-020 | P2 |
| UC-288 | Run the GMV Report | Admin | B11 | FR-018, FR-020 | P2 |
| UC-289 | Run the Returns and Refunds Report | Admin | B11 | FR-016, FR-018 | P2 |
| UC-290 | Monitor Queue Depths and SLA Breaches as Moderator | Moderator | B11 | FR-018, FR-020 | P2 |
| UC-291 | Review a CMS Page's Publish History Before Republishing | Admin | B12 | FR-019 | P2 |
| UC-292 | Disable a Store Coupon for Promotion Abuse | Admin | B12 | FR-019 | P1 |
| UC-293 | Investigate Coupon-Abuse Patterns Across Orders and Refunds | Admin | B12 | FR-011, FR-019 | P2 |
| UC-294 | Hide Reported Content With a Reason as Moderator | Moderator | B13 | FR-006, FR-019 | P1 |
| UC-295 | Isolate Auto-Created Delivery-Code Tickets in the Support Queue | Admin | B13 | FR-015, FR-020 | P2 |
| UC-296 | Investigate an Audit Hash-Chain Verification Failure | Admin | B13 | FR-020 | P0 |
| UC-297 | Extract Audit Evidence for a Security Incident | Admin | B13 | FR-020 | P1 |
| UC-298 | Re-Drive a Failed Job From the Dead-Letter Queue | Admin | B13 | FR-020 | P1 |
| UC-299 | Dispose of Aged Data-Quality Quarantine Records | Admin | B13 | FR-020 | P1 |
| UC-300 | Review the Weekly Retention Purge Report | Admin | B13 | FR-020 | P2 |
| UC-301 | Investigate a Guard-Blocked Retention Purge Attempt | Admin | B13 | FR-020 | P1 |
| UC-302 | Resolve a Settings Version Conflict After a Concurrent Edit | Super Admin | B13 | FR-019, FR-020 | P2 |
| UC-303 | Track Critical Security Findings Against the 7-Day Remediation SLA | Admin | B13 | FR-020 | P1 |
| UC-304 | Audit the Evidence Entry of a Completed Purge Run | Admin | B13 | FR-020 | P2 |
| UC-305 | Review the Monthly Security Severity Report | Admin | B13 | FR-020 | P2 |
| UC-306 | Delete an Address Used by an In-Flight Checkout | Customer | B01 | FR-003, FR-011 | P2 |
| UC-307 | Hit the 10-Address Cap and Free Up a Slot | Customer | B01 | FR-003 | P2 |
| UC-308 | Keep Past Orders on Their Address Snapshot After Editing the Book | Customer | B01 | FR-003, FR-012 | P2 |
| UC-309 | Recover After a Refresh-Token Reuse Revokes the Session Family | Customer | B01 | FR-001 | P1 |
| UC-310 | Sit Through the 15-Minute Lockout Countdown After Five Failed Logins | Customer | B01 | FR-001 | P1 |
| UC-311 | Collect the OTP via WhatsApp When SMS Delivery Fails | Customer | B01 | FR-001, FR-017 | P1 |
| UC-312 | Hit the OTP Attempt Cap and Read the Blocked-Verification Notice | Customer | B01 | FR-001 | P1 |
| UC-313 | Attach Photos to a Product Review and Handle Upload Rejections | Customer | B02 | FR-006 | P2 |
| UC-314 | Attempt a Review After the 30-Day Window and Get Rejected | Customer | B02 | FR-006 | P2 |
| UC-315 | Filter a Product's Reviews by Rating | Customer | B02 | FR-006 | P2 |
| UC-316 | Read the Vendor's Published Response Beneath Your Review | Customer | B02 | FR-006 | P2 |
| UC-317 | Check the Return Policy and Window on the Product Page | Customer | B02 | FR-004, FR-016 | P2 |
| UC-318 | List the Stores You Follow | Customer | B03 | FR-008 | P2 |
| UC-319 | Unfollow a Store and Stop Its Notifications | Customer | B03 | FR-008, FR-017 | P2 |
| UC-320 | Open a Suspended Storefront and Find It Unavailable | Customer | B03 | FR-008 | P2 |
| UC-321 | Combine Search Filters and Compare Facet Counts | Customer | B04 | FR-009 | P1 |
| UC-322 | Sort Results by Relevance, Price, Rating, or Newest | Customer | B04 | FR-009 | P2 |
| UC-323 | Recover from a Zero-Result Search with Suggestions and Popular Categories | Customer | B04 | FR-009 | P1 |
| UC-324 | Fall Back to Category Browse When Search Is Unavailable | Customer | B04 | FR-009 | P1 |
| UC-325 | Add Past a Cart Guard and Leave the Cart Unchanged | Customer | B05 | FR-010 | P1 |
| UC-326 | Re-Reserve Stock When a Cart Line's 15-Minute Countdown Expires | Customer | B05 | FR-010, FR-005 | P1 |
| UC-327 | Re-Confirm a Price That Changed Since Add-to-Cart | Customer | B05 | FR-010, FR-011 | P0 |
| UC-328 | Remove an Ineligible Line That Blocks Checkout | Customer | B05 | FR-010 | P1 |
| UC-329 | Merge the Guest Cart Into the Account Cart on Login | Customer | B05 | FR-010 | P1 |
| UC-330 | Resume Checkout After Topping Up the Wallet Shortfall | Customer | B05 | FR-011, FR-013 | P0 |
| UC-331 | Retry a Duplicate Confirm and Receive the Original Order | Customer | B05 | FR-011 | P0 |
| UC-332 | Reject an Order Total Outside the 500-5,000,000 YER Bounds | Customer | B05 | FR-011 | P1 |
| UC-333 | Handle a Shipping-Zone Gap for the Selected Address | Customer | B05 | FR-011, FR-015 | P1 |
| UC-334 | Filter the Order List by Status | Customer | B06 | FR-012 | P2 |
| UC-335 | Refresh the Order Screen After a Status Conflict | Customer | B06 | FR-012 | P2 |
| UC-336 | Receive the 24-Hour Escalation Notice on a Stalled Order | Customer | B06 | FR-012, FR-017 | P2 |
| UC-337 | Get the Cancel-Window Refusal After READY_FOR_PICKUP | Customer | B06 | FR-012 | P1 |
| UC-338 | Open the Order Receipt With the Full VAT Breakdown | Customer | B06 | FR-011, FR-012 | P2 |
| UC-339 | Filter Wallet Transactions by Type and Date Range | Customer | B07 | FR-013 | P1 |
| UC-340 | Poll a Top-Up Awaiting Provider Confirmation | Customer | B07 | FR-013 | P1 |
| UC-341 | Upload a Bank-Transfer Slip for Admin Verification | Customer | B07 | FR-013 | P1 |
| UC-342 | Work With a Frozen Wallet (Pay and Top-Up Blocked, Refunds Still Received) | Customer | B07 | FR-013 | P0 |
| UC-343 | Check Refund Status and the 3-Business-Day Wallet Credit Date | Customer | B07 | FR-016, FR-013 | P1 |
| UC-344 | Reject a Top-Up Outside the 1,000-5,000,000 YER Bounds | Customer | B07 | FR-013 | P2 |
| UC-345 | Read Wallet Amounts Correctly as Arabic-Indic Numerals with a Screen Reader | Customer | B07 | FR-013 | P2 |
| UC-346 | Retrieve the Delivery Code In-App When No SMS Arrives | Customer | B08 | FR-015, FR-017 | P0 |
| UC-347 | See Failed Delivery Attempts Reflected in Your Order Timeline | Customer | B08 | FR-015, FR-012 | P2 |
| UC-348 | Open the 24-Hour Code-Lockout Notice and Its Auto-Created Ticket | Customer | B08 | FR-015, FR-020 | P1 |
| UC-349 | Follow Delivery Progress Without a Map | Customer | B08 | FR-015 | P2 |
| UC-350 | Check Return Eligibility Before Submitting a Request | Customer | B09 | FR-016 | P0 |
| UC-351 | Open a Late-Window Return on a Completed Order | Customer | B09 | FR-016 | P1 |
| UC-352 | Watch a Return Auto-Approve After the 72-Hour Inspection Timeout | Customer | B09 | FR-016 | P1 |
| UC-353 | Read the Refund Composition (Item Value Versus Shipping) | Customer | B09 | FR-016 | P2 |
| UC-354 | Resolve a Conflict Between an Open Dispute and a New Return | Customer | B09 | FR-016, FR-012 | P2 |
| UC-355 | Filter the Notification Inbox by Category and Unread State | Customer | B10 | FR-017 | P2 |
| UC-356 | Disable a Marketing Channel Without Silencing Order Alerts | Customer | B10 | FR-017 | P1 |
| UC-357 | See Locked Security Toggles in the Preference Center | Customer | B10 | FR-017 | P1 |
| UC-358 | Keep Using the App When Push Permission Is Denied | Customer | B10 | FR-017 | P1 |
| UC-359 | Add a Message and Attachment to an Open Support Ticket Thread | Customer | B13 | FR-020 | P2 |
| UC-360 | Rate the Support Resolution in the Post-Ticket Survey | Customer | B13 | FR-020 | P2 |
| UC-361 | Resolve Publish Blockers on an Incomplete Listing | Vendor | B02 | FR-004 | P1 |
| UC-362 | Upload Product Images Within Count and Format Limits | Vendor | B02 | FR-004 | P1 |
| UC-363 | Correct Price Validation Rejections on a Listing Draft | Vendor | B02 | FR-004 | P2 |
| UC-364 | Define Product Variants Within Dimension and SKU Limits | Vendor | B02 | FR-004 | P1 |
| UC-365 | Filter the Inventory Table for Low-Stock SKUs | Vendor | B02 | FR-005 | P2 |
| UC-366 | Recover From a Stock Adjustment Blocked by Active Reservations | Vendor | B02 | FR-005 | P1 |
| UC-367 | Confirm Search Visibility After a Catalog Change | Vendor | B04 | FR-004, FR-009 | P2 |
| UC-368 | Set Weekly Store Operating Hours | Vendor | B03 | FR-008 | P2 |
| UC-369 | Revise KYC Documents Rejected at Upload | Vendor | B03 | FR-007 | P2 |
| UC-370 | Block Demotion of the Last Store Owner | Vendor | B03 | FR-002 | P1 |
| UC-371 | Handle Store Suspension During Active Fulfillment | Vendor | B03 | FR-007, FR-012 | P1 |
| UC-372 | Handle Staff Invitation Rejections (Unregistered Phone or Staff Limit) | Vendor | B03 | FR-002 | P2 |
| UC-373 | Define Domestic Shipping Zones and Store Fees | Vendor | B08 | FR-008, FR-015 | P1 |
| UC-374 | Enable Auto-Accept for Incoming Sub-Orders | Vendor | B06 | FR-012 | P1 |
| UC-375 | Start Fulfillment on a Confirmed Sub-Order | Vendor | B06 | FR-012 | P0 |
| UC-376 | View the Append-Only Timeline for an Own Sub-Order | Vendor | B06 | FR-012 | P2 |
| UC-377 | Recover From a State Conflict on a Concurrent Order Action | Vendor | B06 | FR-012 | P1 |
| UC-378 | Handle a Closed Cancellation Window on a Dispatched Sub-Order | Vendor | B06 | FR-012 | P2 |
| UC-379 | Triage the Sub-Order Queue by SLA Age | Vendor | B06 | FR-012 | P2 |
| UC-380 | Track Overdue Return Decisions Before the 48-Hour Escalation | Vendor | B09 | FR-016 | P1 |
| UC-381 | Track the Return Pickup Status After Approval | Vendor | B09 | FR-016, FR-015 | P2 |
| UC-382 | Handle a Return Auto-Approved After the 72-Hour Inspection Window | Vendor | B09 | FR-016 | P1 |
| UC-383 | Raise a Dispute on an Own Sub-Order | Vendor | B09 | FR-016, FR-012 | P0 |
| UC-384 | Verify Return-Window Eligibility Before a Decision | Vendor | B09 | FR-016 | P1 |
| UC-385 | Monitor Frozen Escrow Holds on Own Sub-Orders | Vendor | B07 | FR-014 | P2 |
| UC-386 | Handle a Payout Request Below the 1,000 YER Minimum | Vendor | B07 | FR-014 | P2 |
| UC-387 | Investigate a Rejected Payout's Reason and Ledger References | Vendor | B07 | FR-014 | P2 |
| UC-388 | Resolve Payout Holds While KYC or Store Status Is Blocked | Vendor | B07 | FR-014 | P1 |
| UC-389 | Re-Verify the Payout Account After a Destination Change | Vendor | B07 | FR-014 | P1 |
| UC-390 | Compare Store Metrics Against the Previous Period | Vendor | B11 | FR-018 | P2 |
| UC-391 | Resolve a Report Export Row-Cap Rejection | Vendor | B11 | FR-018 | P2 |
| UC-392 | Adjust Schedule and Limits or Disable an Active Store Coupon | Vendor | B12 | FR-019 | P1 |
| UC-393 | Resolve Store Coupon Creation Rejections (Bounds and Duplicate Code) | Vendor | B12 | FR-011 | P2 |
| UC-394 | Configure Vendor Notification Preferences for Store Events | Vendor | B10 | FR-017 | P2 |
| UC-395 | Open a Support Ticket About a Payout or Payment Issue | Vendor | B13 | FR-020 | P2 |
| UC-396 | Decline a Delivery Offer Without Claiming It | Delivery Provider | B08 | FR-015 | P1 |
| UC-397 | Review the Shipment Attempt Log Before a Retry | Delivery Provider | B08 | FR-015 | P1 |
| UC-398 | Upload an Optional Delivery Photo as Extra Proof | Delivery Provider | B08 | FR-015 | P2 |
| UC-399 | Finish on the Proof Success Screen and Continue to the Next Job | Delivery Provider | B08 | FR-015 | P2 |
| UC-400 | Disable Code Entry When the Job Is Reassigned or Released | Delivery Provider | B08 | FR-015 | P1 |
| UC-401 | Recover from Delivery-Code Entry Rate Limiting | Delivery Provider | B08 | FR-015 | P2 |
| UC-402 | Keep Attempt and Lock Progress Across an App Restart | Delivery Provider | B08 | FR-015 | P2 |
| UC-403 | Work a Delivery Whose Attempts Are Frozen for Admin Review | Delivery Provider | B08 | FR-015 | P1 |
| UC-404 | Hear Code Attempt Feedback via Screen Reader | Delivery Provider | B08 | FR-015 | P2 |
| UC-405 | Track Personal Delivery Stats on the Courier Profile | Delivery Provider | B08 | FR-015 | P2 |
| UC-406 | Register This Courier Device for Job Push Notifications | Delivery Provider | B10 | FR-017 | P1 |
| UC-407 | Open a Delivery Job from a Push Deep Link | Delivery Provider | B10 | FR-017, FR-015 | P1 |
| UC-408 | Fall Back to the In-App Inbox When Push Delivery Fails | Delivery Provider | B10 | FR-017 | P2 |
| UC-409 | Configure Delivery Notification Channels as a Courier | Delivery Provider | B10 | FR-017 | P2 |
| UC-410 | Resume a Delivery Deep Link After Signing In | Delivery Provider | B01 | FR-001, FR-015 | P2 |
| UC-411 | Re-Authenticate When the Session Expires Mid-Job | Delivery Provider | B01 | FR-001, FR-015 | P1 |
| UC-412 | Switch the Courier App Language Between Arabic and English | Delivery Provider | B01 | FR-003 | P2 |
| UC-413 | Record Vendor Receipt of an Approved Return Package | Delivery Provider | B09 | FR-016 | P0 |
| UC-414 | Escalate a Failed Return Pickup to Operations | Delivery Provider | B09 | FR-016, FR-020 | P2 |
| UC-415 | Browse Completed Jobs in the History Tab | Delivery Provider | B08 | FR-015 | P2 |
| UC-416 | Handle Access Denied When Opening a Delivery You Do Not Own | Delivery Provider | B08 | FR-015 | P2 |
| UC-417 | Record a Failed Pickup Attempt When the Store Is Not Ready | Delivery Provider | B08 | FR-015 | P1 |
| UC-418 | Wait and Retry Later When the Customer Is Unavailable | Delivery Provider | B08 | FR-015 | P1 |
| UC-419 | Work Only with a Masked Buyer Code at the Door | Delivery Provider | B08 | FR-015 | P1 |
| UC-420 | Type the Delivery Code with Latin Digits in the Arabic Interface | Delivery Provider | B08 | FR-015 | P2 |

## 3. Totals per Actor

| Actor | Use Cases | Range |
|---|---|---|
| Customer (ACT-01) | 113 | UC-001 … UC-014, UC-041 … UC-042, UC-141 … UC-182, UC-306 … UC-360 |
| Vendor (ACT-02) | 67 | UC-015 … UC-024, UC-183 … UC-204, UC-361 … UC-395 |
| Delivery Provider (ACT-03) | 37 | UC-025 … UC-030, UC-205 … UC-210, UC-396 … UC-420 |
| Admin (ACT-04) | 102 | UC-031 … UC-036, UC-084 … UC-136, UC-256, UC-259 … UC-267, UC-269 … UC-273, UC-275 … UC-289, UC-291 … UC-293, UC-295 … UC-301, UC-303 … UC-305 |
| Super Admin (ACT-05) | 6 | UC-037, UC-257 … UC-258, UC-268, UC-274, UC-302 |
| Moderator (ACT-06) | 7 | UC-038, UC-137 … UC-140, UC-290, UC-294 |
| System (ACT-07) | 88 | UC-039 … UC-040, UC-043 … UC-083, UC-211 … UC-255 |
| **Total** | **420** | UC-001 … UC-420 |

Priority totals: P0 = 73, P1 = 205, P2 = 142 (420 total). Block coverage (all 420 rows): B01 (50), B02 (42), B03 (29), B04 (13), B05 (19), B06 (32), B07 (49), B08 (40), B09 (36), B10 (24), B11 (21), B12 (25), B13 (40) — 420 total. The Block column is populated for every row: `UC-001`…`UC-210` from the UC files themselves, `UC-211`…`UC-420` per the registered per-UC assignments in `00-project-overview/system-expansion-proposal.md` §4 (the session-011 UC files carry no Block field, so the proposal §4 value is the value of record).

## 4. Related Documents

- `00-project-overview/actors-and-roles.md` (DOC-OVR-007) — the 7 actors
- `01-business-analysis/business-rules.md` (DOC-BA-005) — all `BR-*` referenced here
- `02-requirements/requirements-overview.md` (DOC-REQ-001) — all `FR-*` referenced here
- `../03-system-analysis/core/state-transitions.md` (DOC-SA-010) — the 17-state machine used in postconditions

## 5. Coverage Matrix (portal × feature area → UC IDs)

Feature areas are derived from blocks `B01…B13` (`../06-backend/core/backend-architecture.md` §3). Portal = the surface the primary actor uses, fixed by each UC's file location in the five portal subfolders of `01-business-analysis/`. Every UC appears in exactly one portal group, so the matrix accounts for all **420** use cases (completeness proof, AUD-01/D-02). Admin console includes Super Admin (`UC-037`, `UC-257`, `UC-258`, `UC-268`, `UC-274`, `UC-302`) and Moderator (`UC-038`, `UC-137 … UC-140`, `UC-290`, `UC-294`); Shared/System includes the automated jobs `UC-039 … UC-040` and the session-011 system rows `UC-211 … UC-255`. The 210 session-011 files (`UC-211`…`UC-420`) carry no Block field in the UC file itself, so their feature area is taken from the registered assignments — blocks assigned per `../00-project-overview/system-expansion-proposal.md` §4 — and each of them is classified into its B01…B13 cell below.

| Portal | Feature area | UC IDs | Count |
|---|---|---|---|
| **Shared/System (ACT-07)** | **Portal subtotal** | UC-039 … UC-040, UC-043 … UC-083, UC-211 … UC-255 | **88** |
| | Identity, auth & profiles (B01) | UC-043 … UC-045, UC-070, UC-211 … UC-216 | 10 |
| | Catalog, stock & reviews (B02) | UC-046 … UC-050, UC-217 … UC-219 | 8 |
| | Stores & vendors (B03) | UC-072 … UC-073, UC-220 … UC-221 | 4 |
| | Search & discovery (B04) | UC-067, UC-069, UC-222 … UC-224 | 5 |
| | Cart & checkout (B05) | UC-074, UC-225 … UC-227 | 4 |
| | Orders & timelines (B06) | UC-063, UC-075, UC-228 … UC-230 | 5 |
| | Wallet, escrow & payouts (B07) | UC-039, UC-051 … UC-055, UC-057 … UC-058, UC-064, UC-076, UC-231 … UC-237 | 17 |
| | Delivery & shipping (B08) | UC-077 … UC-078, UC-238 … UC-240 | 5 |
| | Returns & disputes (B09) | UC-241 … UC-243 | 3 |
| | Notifications (B10) | UC-040, UC-059 … UC-061, UC-071, UC-079, UC-244 … UC-246 | 9 |
| | Analytics & reports (B11) | UC-056, UC-080 … UC-081, UC-247 … UC-248 | 5 |
| | Content, banners & coupons (B12) | UC-249 … UC-250 | 2 |
| | Platform, support & moderation (B13) | UC-062, UC-065 … UC-066, UC-068, UC-082 … UC-083, UC-251 … UC-255 | 11 |
| **Admin console (ACT-04/05/06)** | **Portal subtotal** | UC-031 … UC-038, UC-084 … UC-140, UC-256 … UC-305 | **115** |
| | Identity, auth & profiles (B01) | UC-037, UC-089 … UC-092, UC-256 … UC-261 | 11 |
| | Catalog, stock & reviews (B02) | UC-116 … UC-123, UC-262 … UC-264 | 11 |
| | Stores & vendors (B03) | UC-031, UC-093 … UC-097, UC-265 … UC-268 | 10 |
| | Orders & timelines (B06) | UC-033, UC-135, UC-137, UC-269 … UC-273 | 8 |
| | Wallet, escrow & payouts (B07) | UC-034, UC-087, UC-098 … UC-099, UC-127 … UC-128, UC-274 … UC-280 | 13 |
| | Delivery & shipping (B08) | UC-136, UC-281 … UC-282 | 3 |
| | Returns & disputes (B09) | UC-124 … UC-126, UC-129, UC-138 … UC-139, UC-283 … UC-286 | 10 |
| | Analytics & reports (B11) | UC-084 … UC-086, UC-130 … UC-133, UC-287 … UC-290 | 11 |
| | Content, banners & coupons (B12) | UC-104 … UC-115, UC-134, UC-291 … UC-293 | 16 |
| | Platform, support & moderation (B13) | UC-032, UC-035 … UC-036, UC-038, UC-088, UC-100 … UC-103, UC-140, UC-294 … UC-305 | 22 |
| **Customer web + mobile (ACT-01)** | **Portal subtotal** | UC-001 … UC-014, UC-041 … UC-042, UC-141 … UC-182, UC-306 … UC-360 | **113** |
| | Identity, auth & profiles (B01) | UC-002 … UC-005, UC-141 … UC-154, UC-181, UC-306 … UC-312 | 26 |
| | Catalog, stock & reviews (B02) | UC-007, UC-165 … UC-167, UC-313 … UC-317 | 9 |
| | Stores & vendors (B03) | UC-008, UC-318 … UC-320 | 4 |
| | Search & discovery (B04) | UC-001, UC-006, UC-156, UC-321 … UC-324 | 7 |
| | Cart & checkout (B05) | UC-009 … UC-011, UC-160 … UC-162, UC-325 … UC-333 | 15 |
| | Orders & timelines (B06) | UC-012, UC-159, UC-163, UC-334 … UC-338 | 8 |
| | Wallet, escrow & payouts (B07) | UC-041 … UC-042, UC-164, UC-174, UC-339 … UC-345 | 11 |
| | Delivery & shipping (B08) | UC-013, UC-346 … UC-349 | 5 |
| | Returns & disputes (B09) | UC-168 … UC-173, UC-350 … UC-354 | 11 |
| | Notifications (B10) | UC-175 … UC-179, UC-182, UC-355 … UC-358 | 10 |
| | Content, banners & coupons (B12) | UC-155, UC-157 … UC-158 | 3 |
| | Platform, support & moderation (B13) | UC-014, UC-180, UC-359 … UC-360 | 4 |
| **Vendor panel (ACT-02)** | **Portal subtotal** | UC-015 … UC-024, UC-183 … UC-204, UC-361 … UC-395 | **67** |
| | Catalog, stock & reviews (B02) | UC-017 … UC-018, UC-024, UC-188 … UC-191, UC-202, UC-361 … UC-366 | 14 |
| | Stores & vendors (B03) | UC-015 … UC-016, UC-183 … UC-186, UC-368 … UC-372 | 11 |
| | Search & discovery (B04) | UC-367 | 1 |
| | Orders & timelines (B06) | UC-019 … UC-020, UC-192 … UC-193, UC-374 … UC-379 | 10 |
| | Wallet, escrow & payouts (B07) | UC-022, UC-187, UC-198, UC-385 … UC-389 | 8 |
| | Delivery & shipping (B08) | UC-373 | 1 |
| | Returns & disputes (B09) | UC-021, UC-194 … UC-197, UC-380 … UC-384 | 10 |
| | Notifications (B10) | UC-394 | 1 |
| | Analytics & reports (B11) | UC-199 … UC-201, UC-390 … UC-391 | 5 |
| | Content, banners & coupons (B12) | UC-023, UC-203, UC-392 … UC-393 | 4 |
| | Platform, support & moderation (B13) | UC-204, UC-395 | 2 |
| **Courier app (ACT-03)** | **Portal subtotal** | UC-025 … UC-030, UC-205 … UC-210, UC-396 … UC-420 | **37** |
| | Identity, auth & profiles (B01) | UC-410 … UC-412 | 3 |
| | Orders & timelines (B06) | UC-209 | 1 |
| | Delivery & shipping (B08) | UC-025 … UC-030, UC-205 … UC-208, UC-396 … UC-405, UC-415 … UC-420 | 26 |
| | Returns & disputes (B09) | UC-413 … UC-414 | 2 |
| | Notifications (B10) | UC-406 … UC-409 | 4 |
| | Platform, support & moderation (B13) | UC-210 | 1 |
| | **Total** | UC-001 … UC-420 | **420** |

Portal subtotals: 88 + 115 + 113 + 67 + 37 = **420** = §3 actor total.

### 5.1 PENDING / backlog (not minted)

Recorded as INSUFFICIENT EVIDENCE — deliberately excluded from the 420; never counted as use cases. Re-checked 2026-09-30 against the 210 files minted in session 011 (`UC-211`…`UC-420` — titles, goals and FR refs grepped item by item): none of the 18 items is covered by a new use case, so all remain pending. Next free use-case ID: `UC-421+`.

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

- **Derived: 420 use cases.** Countable from the `UC-NNN.md` files in this directory and its five portal subfolders (42 pre-existing + 168 minted by session 010 + 210 minted by session 011) and reproduced by the §2 index (420 rows), §3 totals, and the §5 matrix above. This is the repository-derived number.
- **Owner-supplied: "over 350"** (`prompt-010.md` §1), superseded by **"over 400"** (`prompt-011.md` §1) — owner-supplied, **INSUFFICIENT EVIDENCE**, not derivable from this repository; on a file-count basis the derived 420 now exceeds both targets (420 > 350, 420 > 400).
- The two kinds of numbers are published separately and never blended. The likely basis for the owner figure is **scenario-level counting**: across the 420 UCs, main + alternative + exception scenarios total ≈ **2,955** scenarios (420 main + 1,221 alternative + 1,314 exception, script-counted; the same method yields ≈ 1,461 across the first 210) — a different unit of count than use-case files.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial index (40 use cases) | Initial analysis |
| 1.1 | 2026-09-28 | `UC-041` (Top Up Wallet, customer funding leg) and `UC-042` (View Wallet Statement) added; totals → 42 use cases (Customer 16, P0 18, P1 19, B07 5) | Session-007 UC gap from `describ.md` §8: only the admin top-up half (`UC-034`) existed and `FR-013`'s statement had no use case to trace to (root README §10) |
| 1.2 | 2026-09-29 | §2 index 42 → **210 use cases** (+168 rows UC-043…UC-210), §3 actor totals/priority/block recompute, new §5 coverage matrix + PENDING backlog + derived-vs-owner numbers note | Session-010 owner directive (prompt-010.md §1) — full portal use-case coverage; completeness proven by matrix (AUD-01/D-02) |
| 1.3 | 2026-09-30 | §2 +210 rows (UC-211…UC-420), header 210 → 420, §3 totals/priority/block recompute, §5 matrix recompute to 420, §5.1 backlog rework, §5.2 derived 210 → 420 | Owner directive session 011 (prompt-011.md §4.8) — registration of the session-011 mint in the same change set (root README §9) |
