---
document_id: DOC-PHA-006
title: Use Cases — analysis phase roll-up
category: phases
status: approved
version: 1.2
created: 2026-09-28
updated: 2026-09-29
author: analysis-agent
source_of_truth: false
related_documents: [DOC-BA-004, DOC-PHA-007]
related_requirements: []
---

# Use Cases — analysis phase roll-up

## Purpose
Index every operation the system supports, as authored during analysis. The **canonical use-case files live in [`01-business-analysis/`](../../01-business-analysis/use-case-index.md) (`UC-001`…`UC-210`)**; this roll-up (CORE-03 item 4) proves completeness against the phase boundary and links the flows artifact (item 5).

## Scope
All functionality of the four shells: customer web + customer mobile, vendor panel, admin console, courier mobile.

## Actors / roles
Canonical actor list: [`00-project-overview/actors-and-roles.md`](../../00-project-overview/actors-and-roles.md) — `customer`, `vendor`, `courier`, `support`, `moderator`, `admin`, `super admin`, `system` (7 API roles; see [permissions-matrix.md](permissions-matrix.md)).

## Inventory (210 use cases — titles verified against the files, 2026-09-29)

| Actor group | Use cases | Canonical index |
|---|---|---|
| Guest / customer — discovery & identity | `UC-001`…`UC-005` (browse as guest, register phone+OTP, login, reset password, addresses) | [`../../01-business-analysis/use-case-index.md`](../../01-business-analysis/use-case-index.md) |
| Customer — commerce | `UC-006`…`UC-014` (search, product detail, follow store, add to cart, manage cart, checkout with wallet, track order, confirm receipt with code, contact support) | same |
| Customer — money | `UC-041`, `UC-042` (top up wallet, view wallet statement) | same |
| Vendor — store & catalog | `UC-015`…`UC-024` (register+KYC, store profile, listings, inventory, incoming orders, ready for pickup, return response, finances/payouts, coupons, review responses) | same |
| Courier — delivery execution | `UC-025`…`UC-030` (view deliveries, accept assignment, confirm pickup, transit + attempts, failed attempt, 6-digit code confirmation) | same |
| Admin / platform operations | `UC-031`…`UC-040` (KYC decisions, moderation, orders & disputes, bank-transfer top-up verification, platform settings, audit log, roles, flagged content, escrow auto-release, OTP provider failover) | same |

The grouped rows above index `UC-001`…`UC-042` unchanged. The 168 use cases minted in session 010 (`prompt-010.md` §1) are indexed one row each — ID, title copied from the file H1, actor:

| Use case | Title | Actor |
|---|---|---|
| `UC-043` | Rotate Refresh Tokens and Revoke Session Families on Reuse | System |
| `UC-044` | Lock an Account After Five Consecutive Failed Logins | System |
| `UC-045` | Sweep Expired Sessions and Orphaned Refresh Tokens | System |
| `UC-046` | Expire Unpaid Stock Reservations After 15 Minutes | System |
| `UC-047` | Commit Stock Reservations on Payment Success | System |
| `UC-048` | Restore Stock When an Order Is Cancelled | System |
| `UC-049` | Reconcile the Inventory Ledger Against On-Hand Stock | System |
| `UC-050` | Recompute Store Ratings Incrementally | System |
| `UC-051` | Release Unused Wallet Authorization Holds | System |
| `UC-052` | Execute Scheduled Vendor Payout Batches | System |
| `UC-053` | Roll Over Payouts Below the 1,000 YER Minimum | System |
| `UC-054` | Run Daily Ledger and Escrow Reconciliation | System |
| `UC-055` | Alert Finance on Reconciliation Mismatch | System |
| `UC-056` | Generate Monthly Vendor Statements | System |
| `UC-057` | Reverse Commission Proportionally on Refund | System |
| `UC-058` | Execute Wallet Refunds to the Customer | System |
| `UC-059` | Fan Out Notifications Across Channels by Preference | System |
| `UC-060` | Honor Per-Category Notification Opt-Outs | System |
| `UC-061` | Deliver Mandatory Security Notifications | System |
| `UC-062` | Retry Failed Jobs and Alert on Dead-Letter Depth | System |
| `UC-063` | Escalate Orders Stuck at CONFIRMED After 24 Hours | System |
| `UC-064` | Guard Escrow Release While a Dispute Is Open | System |
| `UC-065` | Auto-Create a Support Ticket on the Third Delivery-Code Failure | System |
| `UC-066` | Auto-Close Stale Support Tickets | System |
| `UC-067` | Synchronize the Search Index on Catalog Changes | System |
| `UC-068` | Gate Traffic on Liveness and Readiness Probes | System |
| `UC-069` | Normalize Slugs and Preserve Canonical URLs | System |
| `UC-070` | Screen and Sanitize All Uploaded Files | System |
| `UC-071` | Deliver Follower Marketing Notifications on New Products | System |
| `UC-072` | Cascade a Store Suspension Across Catalog, Orders, and Payouts | System |
| `UC-073` | Escalate KYC Decisions Past the 48-Hour SLA | System |
| `UC-074` | Compensate a Failed Checkout Saga | System |
| `UC-075` | Rebuild the Order Timeline Read Model | System |
| `UC-076` | Reconcile Wallet Top-Ups Against Provider Polls and Callbacks | System |
| `UC-077` | Broadcast Delivery Offers to Eligible Couriers | System |
| `UC-078` | Sweep Expired Delivery Codes | System |
| `UC-079` | Render Notification Templates Per Locale | System |
| `UC-080` | Aggregate Dashboard Analytics Rollups | System |
| `UC-081` | Generate Report Export Files | System |
| `UC-082` | Deliver Signed Outbound Webhooks with Retry | System |
| `UC-083` | Enforce Audit Log Retention and Redaction | System |
| `UC-084` | View the Admin Operations Dashboard | Admin |
| `UC-085` | Run a Platform Report | Admin |
| `UC-086` | Export a Platform Report as CSV | Admin |
| `UC-087` | Review the Daily Reconciliation Result | Admin |
| `UC-088` | Monitor Platform Health Probes | Admin |
| `UC-089` | Search the User Directory | Admin |
| `UC-090` | View a User's Profile and Active Sessions | Admin |
| `UC-091` | Suspend a User Account | Admin |
| `UC-092` | Reactivate a Suspended User Account | Admin |
| `UC-093` | Browse the Store Directory | Admin |
| `UC-094` | View Store Detail and Open Exposure | Admin |
| `UC-095` | Approve a Newly Created Store | Admin |
| `UC-096` | Suspend a Store | Admin |
| `UC-097` | Re-Activate a Suspended Store | Admin |
| `UC-098` | Freeze a Customer Wallet | Admin |
| `UC-099` | Unfreeze a Customer Wallet | Admin |
| `UC-100` | Monitor the Support Ticket Queue | Admin |
| `UC-101` | Claim or Assign a Support Ticket | Admin |
| `UC-102` | Reply to a Support Ticket Thread | Admin |
| `UC-103` | Resolve a Support Ticket with a Resolution Note | Admin |
| `UC-104` | List CMS Pages | Admin |
| `UC-105` | Create a CMS Page Draft | Admin |
| `UC-106` | Edit a CMS Page Draft | Admin |
| `UC-107` | Publish a CMS Page | Admin |
| `UC-108` | Archive a CMS Page | Admin |
| `UC-109` | List Banners with Schedule and Targeting | Admin |
| `UC-110` | Create a Home Banner | Admin |
| `UC-111` | Edit Banner Content, Targeting, and Schedule | Admin |
| `UC-112` | Remove a Banner | Admin |
| `UC-113` | List Platform Coupons | Admin |
| `UC-114` | Create a Platform Coupon | Admin |
| `UC-115` | Disable a Platform Coupon | Admin |
| `UC-116` | View the Category Tree (Admin Scope) | Admin |
| `UC-117` | Create a Category Node | Admin |
| `UC-118` | Rename, Re-Slug, or Move a Category Node | Admin |
| `UC-119` | Delete an Empty Category | Admin |
| `UC-120` | List the Attribute Dictionary | Admin |
| `UC-121` | Create an Attribute | Admin |
| `UC-122` | Update or Disable an Attribute | Admin |
| `UC-123` | Delete an Unused Attribute | Admin |
| `UC-124` | Monitor the Platform Return Queue | Admin |
| `UC-125` | Decide a Stalled or Disputed Return Case | Admin |
| `UC-126` | Oversee Refund Receipts and Statuses | Admin |
| `UC-127` | Review Vendor Payout Runs | Admin |
| `UC-128` | Monitor Frozen Wallets | Admin |
| `UC-129` | Triage the Refund Queue | Admin |
| `UC-130` | Run the Delivery Performance Report | Admin |
| `UC-131` | Run the Vendor Health Report | Admin |
| `UC-132` | Run the KYC Throughput Report | Admin |
| `UC-133` | Run the User Growth Report | Admin |
| `UC-134` | Restore Previously Hidden Content | Admin |
| `UC-135` | Handle the 24-Hour Confirmation Escalation | Admin |
| `UC-136` | Handle the Three-Failed-Attempt Delivery Escalation | Admin |
| `UC-137` | Read the Orders Queue as Moderator (Read-Only) | Moderator |
| `UC-138` | Read the Return Queue as Moderator (Read-Only) | Moderator |
| `UC-139` | Review a Dispute as Moderator (Advisory Input) | Moderator |
| `UC-140` | Handle a Support Ticket as Moderator | Moderator |
| `UC-141` | Resend an OTP (Registration, Login, or Reset) | Customer |
| `UC-142` | Complete Step-Up OTP Verification for a Sensitive Change | Customer |
| `UC-143` | Log Out of the Current Device | Customer |
| `UC-144` | Log Out of All Devices | Customer |
| `UC-145` | Change Password While Signed In | Customer |
| `UC-146` | View Active Device Sessions | Customer |
| `UC-147` | Revoke Another Device's Session | Customer |
| `UC-148` | View and Edit Profile | Customer |
| `UC-149` | Add and Verify an Optional Email | Customer |
| `UC-150` | Upload a Profile Avatar | Customer |
| `UC-151` | Manage Account Preferences | Customer |
| `UC-152` | Switch the Interface Locale (ar/en) | Customer |
| `UC-153` | Request Account Deletion | Customer |
| `UC-154` | Cancel a Pending Deletion Request | Customer |
| `UC-155` | Browse the Personalized Home Feed | Customer |
| `UC-156` | Use Search Suggestions (Typeahead) | Customer |
| `UC-157` | Browse Deals and the Promotion Gallery | Customer |
| `UC-158` | Read Static Content and Help Pages | Customer |
| `UC-159` | Track a Guest Order via a Tokenized Link | Customer |
| `UC-160` | Clear the Entire Cart | Customer |
| `UC-161` | Review the Authoritative Checkout Preview | Customer |
| `UC-162` | Apply and Validate a Coupon at Checkout | Customer |
| `UC-163` | Cancel an Order Before Dispatch | Customer |
| `UC-164` | View Wallet Balance and Status | Customer |
| `UC-165` | Write a Product Review After Delivery | Customer |
| `UC-166` | Edit a Review Once Within 7 Days | Customer |
| `UC-167` | Report a Review for Moderation | Customer |
| `UC-168` | Request a Return for Delivered Items | Customer |
| `UC-169` | Track Return Request Status | Customer |
| `UC-170` | View the Return Pickup Schedule | Customer |
| `UC-171` | Open a Dispute on a Delivered Order | Customer |
| `UC-172` | Submit Dispute Evidence | Customer |
| `UC-173` | Review the Dispute Resolution Outcome | Customer |
| `UC-174` | View Escrow Holding Status for Own Orders | Customer |
| `UC-175` | Open the Notification Inbox | Customer |
| `UC-176` | Mark Notifications Read or Remove Them | Customer |
| `UC-177` | Configure Notification Preferences | Customer |
| `UC-178` | Register This Device for Push Notifications | Customer |
| `UC-179` | Manage Registered Push Devices | Customer |
| `UC-180` | View Own Support Ticket List and Status | Customer |
| `UC-181` | Resume an Existing Session on App Launch (Mobile) | Customer |
| `UC-182` | Receive and Open a Deep-Linked Order Push | Customer |
| `UC-183` | Resubmit a Rejected Vendor Application | Vendor |
| `UC-184` | Track the KYC Case Status and SLA Age | Vendor |
| `UC-185` | View the Follower List and Count | Vendor |
| `UC-186` | Manage Store Staff (Invite, Change Role, Remove) | Vendor |
| `UC-187` | Configure the Payout Account | Vendor |
| `UC-188` | Unpublish a Product (Withdraw from Sale) | Vendor |
| `UC-189` | Soft-Delete a Product | Vendor |
| `UC-190` | Remove a Product Image | Vendor |
| `UC-191` | Inspect SKU Reservations and Expiry | Vendor |
| `UC-192` | Review the Sub-Order Queue | Vendor |
| `UC-193` | Cancel a Sub-Order Before Pickup | Vendor |
| `UC-194` | Review the Return Queue | Vendor |
| `UC-195` | Inspect a Received Return Within 72 Hours | Vendor |
| `UC-196` | Respond to a Dispute with Evidence | Vendor |
| `UC-197` | Track Dispute Status | Vendor |
| `UC-198` | Request a Payout | Vendor |
| `UC-199` | View the Sales Dashboard | Vendor |
| `UC-200` | Run a Store Report | Vendor |
| `UC-201` | Export a Store Report as CSV | Vendor |
| `UC-202` | View Store Reviews | Vendor |
| `UC-203` | List Store Coupons | Vendor |
| `UC-204` | Open a Support Ticket About an Order | Vendor |
| `UC-205` | Release an Accepted Assignment Back to the Pool | Delivery Provider |
| `UC-206` | Update Courier Profile and Served Zones | Delivery Provider |
| `UC-207` | Toggle Availability Online/Offline | Delivery Provider |
| `UC-208` | Handle the 24-Hour Code Lockout After Third Failure | Delivery Provider |
| `UC-209` | Follow the Order Timeline During a Delivery | Delivery Provider |
| `UC-210` | Open a Support Ticket About a Delivery | Delivery Provider |

Actor totals across all 210 use cases (allocation `UC-001`…`UC-210`, naming-conventions v1.5):

| Actor | Use cases |
|---|---|
| Customer | 58 |
| Vendor | 32 |
| Delivery Provider | 12 |
| Admin | 59 |
| Super Admin | 1 |
| Moderator | 5 |
| System | 43 |
| **Total** | **210** |

## Preconditions
Each `UC-NNN` file carries its own preconditions, main/alternate/exception flows, postconditions and related IDs per [`23-templates/use-case-template.md`](../../23-templates/use-case-template.md).

## Main flow
Requirement → use case → workflow → API endpoint → entity → test: `FR-013 → BR-PAY-04 → UC-021 → API-WAL-002 → wallet → TC-031 → AC-FR013-01` (cross-referencing example, root README §5).

## Postconditions
210/210 use cases present; traceability matrices in [`19-traceability/`](../../19-traceability/README.md) cover every use case (`UC-*` 210 registered, consistency check `CHK` series).

## Invariants
No use case may describe a forbidden capability: COD/cards/BNPL/crypto (`C-01…C-04`), GPS/real-time tracking (`C-16`), email-primary/social login (`C-06`), third locale (`C-24`).

## Open questions (COM-01)
1. `UC-036` (Moderator) conflicts with `07-api/endpoints/admin.md` `API-ADM-022/024` on settings/audit-read — deferred sweep item (session 004 backlog).

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 4, session 005) | analysis-agent |
| 2026-09-28 | 1.1 | Inventory → 42 use cases: `UC-041`/`UC-042` added (customer money row), ranges/totals re-synced | Session-007 UC gap from `describ.md` §8 |
| 2026-09-29 | 1.2 | Inventory → **210 use cases**: `UC-043`…`UC-210` appended (168 rows, titles from the file H1s); header `42` → `210`, `42/42` → `210/210`, `UC-*` `42` → `210` registered, canonical range → `UC-001`…`UC-210`; actor totals table added (sums to 210) | `prompt-010.md` §1 (session 010 owner directive) |
