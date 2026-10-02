---
document_id: DOC-PHA-006
title: Use Cases — analysis phase roll-up
category: phases
status: approved
version: 1.3
created: 2026-09-28
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_documents: [DOC-BA-004, DOC-PHA-007]
related_requirements: []
---

# Use Cases — analysis phase roll-up

## Purpose
Index every operation the system supports, as authored during analysis. The **canonical use-case files live in [`01-business-analysis/`](../../01-business-analysis/use-case-index.md) (`UC-001`…`UC-420`)**; this roll-up (CORE-03 item 4) proves completeness against the phase boundary and links the flows artifact (item 5).

## Scope
All functionality of the four shells: customer web + customer mobile, vendor panel, admin console, courier mobile.

## Actors / roles
Canonical actor list: [`00-project-overview/actors-and-roles.md`](../../00-project-overview/actors-and-roles.md) — `customer`, `vendor`, `courier`, `support`, `moderator`, `admin`, `super admin`, `system` (7 API roles; see [permissions-matrix.md](permissions-matrix.md)).

## Inventory (420 use cases — titles verified against the files, 2026-09-30)

| Actor group | Use cases | Canonical index |
|---|---|---|
| Guest / customer — discovery & identity | `UC-001`…`UC-005` (browse as guest, register phone+OTP, login, reset password, addresses) | [`../../01-business-analysis/use-case-index.md`](../../01-business-analysis/use-case-index.md) |
| Customer — commerce | `UC-006`…`UC-014` (search, product detail, follow store, add to cart, manage cart, checkout with wallet, track order, confirm receipt with code, contact support) | same |
| Customer — money | `UC-041`, `UC-042` (top up wallet, view wallet statement) | same |
| Vendor — store & catalog | `UC-015`…`UC-024` (register+KYC, store profile, listings, inventory, incoming orders, ready for pickup, return response, finances/payouts, coupons, review responses) | same |
| Courier — delivery execution | `UC-025`…`UC-030` (view deliveries, accept assignment, confirm pickup, transit + attempts, failed attempt, 6-digit code confirmation) | same |
| Admin / platform operations | `UC-031`…`UC-040` (KYC decisions, moderation, orders & disputes, bank-transfer top-up verification, platform settings, audit log, roles, flagged content, escrow auto-release, OTP provider failover) | same |

The grouped rows above index `UC-001`…`UC-042` unchanged. Session 010 minted 168 use cases (`UC-043`…`UC-210`, `prompt-010.md` §1) and session 011 minted 210 more (`UC-211`…`UC-420`, `prompt-011.md` §1); all 378 are indexed one row each — ID, title copied from the file H1, actor:

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
| `UC-211` | Enforce OTP and Login Rate-Limit Budgets With 429 and Retry-After | System |
| `UC-212` | Evict the Oldest Device Session on the Sixth Concurrent Login | System |
| `UC-213` | Invalidate Every Session When a Password Reset Succeeds | System |
| `UC-214` | Expire OTP Challenges After Five Minutes and Reset Attempt Counters | System |
| `UC-215` | Lift the Account Lock Automatically After the 15-Minute Timeout | System |
| `UC-216` | Anonymize Profile PII for Accounts Dormant 24 Months After Notice | System |
| `UC-217` | Serialize Contended Stock Reservations to Prevent Oversell | System |
| `UC-218` | Resolve the Reservation-Expiry Race at Checkout Confirmation | System |
| `UC-219` | Purge Orphaned Product Images Only When No Order References Them | System |
| `UC-220` | Delete Superseded KYC Document Sets When a Resubmission Is Accepted | System |
| `UC-221` | Purge KYC Objects and Metadata Five Years After Account Closure | System |
| `UC-222` | Rebuild the Search Index From Source After an Outage | System |
| `UC-223` | Serve Category Browse From Cache While Search Is Degraded | System |
| `UC-224` | Alert on Search Indexing Lag Beyond the Five-Minute Delete SLO | System |
| `UC-225` | Return the Original Order on Idempotent Checkout Replay | System |
| `UC-226` | Reject Order Totals Outside the 500–5,000,000 YER Bounds | System |
| `UC-227` | Expire Idempotency-Key Records After 24 Hours | System |
| `UC-228` | Auto-Accept PLACED Orders for Stores With Auto-Accept Enabled | System |
| `UC-229` | Roll the Master Order Up to COMPLETED When Every Sub-Order Settles | System |
| `UC-230` | Append the State-History Backstop Row on Every Order Transition | System |
| `UC-231` | Auto-Cancel Top-Ups Left Pending Beyond the Confirmation Window | System |
| `UC-232` | Open a Circuit Breaker on a Failing Top-Up Provider and Degrade to Bank Transfer | System |
| `UC-233` | Serialize Concurrent Wallet Debits to Keep Balances Non-Negative | System |
| `UC-234` | Credit Refunds Into Frozen Wallets While Debits Stay Blocked | System |
| `UC-235` | Drain the Escrow Release Backlog After Scheduler Recovery | System |
| `UC-236` | Post Ledger Corrections as Compensating Entries Only | System |
| `UC-237` | Route VAT Rounding Residuals to the Platform Rounding Account | System |
| `UC-238` | Issue a Fresh 6-Digit Delivery Code at OUT_FOR_DELIVERY | System |
| `UC-239` | Award a Delivery Offer to the First Courier Acceptance Only | System |
| `UC-240` | Lift the Delivery-Code Confirmation Lock After 24 Hours | System |
| `UC-241` | Auto-Approve Returns Left Uninspected for 72 Hours | System |
| `UC-242` | Auto-Escalate Return Decisions Stalled Past 48 Hours | System |
| `UC-243` | Advance the Order to COMPLETED After a Rejected Return | System |
| `UC-244` | Deduplicate Notification Fan-Out by Event, Recipient, and Channel | System |
| `UC-245` | Throttle Per-Channel Notification Sends to Protect Provider Quotas | System |
| `UC-246` | Record SMS and WhatsApp Delivery Receipts per Message | System |
| `UC-247` | Publish the Weekly Retention Purge Report | System |
| `UC-248` | Enforce Retention Windows on Metrics, Logs, and Traces | System |
| `UC-249` | Purge CDN and ISR Caches When Content Is Published | System |
| `UC-250` | Invalidate the Coupon Validation Cache on Admin Disable | System |
| `UC-251` | Verify the Audit Hash Chain Nightly and Alert on Tamper | System |
| `UC-252` | Page On-Call When Backup Freshness Breaches Its Window | System |
| `UC-253` | Run the Daily Retention Purge With Floor Guards and Evidence | System |
| `UC-254` | Create Next-Month Table Partitions Ahead of Deployment | System |
| `UC-255` | Cascade Primary-Data Deletion to Search, Cache, Queues, and Objects | System |
| `UC-256` | Investigate Account-Lockout and OTP-Abuse Signals | Admin |
| `UC-257` | Execute the Incident Rotation Runbook for a Leaked Secret | Super Admin |
| `UC-258` | Force Session Revalidation After a Signing-Key Rotation | Super Admin |
| `UC-259` | Audit Four-Eyes Compliance on Money Operations | Admin |
| `UC-260` | Review a Target's Recent Administrative Actions Before Enforcement | Admin |
| `UC-261` | Sample-Verify Completed Data-Deletion Requests | Admin |
| `UC-262` | Deactivate a Category Node from the Storefront | Admin |
| `UC-263` | Confirm Rating Recomputation After a Review Is Hidden | Admin |
| `UC-264` | Confirm a Hidden Product Is Delisted From Search and Storefront | Admin |
| `UC-265` | Prioritize the Overdue KYC Queue Before the 48-Hour SLA | Admin |
| `UC-266` | Clear a KYC Blocker That Prevents Store Reactivation | Admin |
| `UC-267` | Verify the Cascade Effects of a Store Suspension | Admin |
| `UC-268` | Set the Platform Commission Tier Within the 5-20% Bound | Super Admin |
| `UC-269` | Cancel an Order as the Platform of Last Resort | Admin |
| `UC-270` | Force a Sub-Order State Correction Within the 17-State Table | Admin |
| `UC-271` | Assemble the Order Timeline Evidence Pack for a Dispute | Admin |
| `UC-272` | Trace a Master Order to Its Sub-Orders During an Investigation | Admin |
| `UC-273` | Investigate an Escalated Illegal Order-State Transition | Admin |
| `UC-274` | Second-Approve a Large Bank-Transfer Top-Up | Super Admin |
| `UC-275` | Cross-Check Pending Top-Ups Against the Bank Statement | Admin |
| `UC-276` | Release an Unused Authorization Hold Manually | Admin |
| `UC-277` | Record the Disposition of a Reconciliation Mismatch | Admin |
| `UC-278` | Approve the Vendor Payout Batch for Execution | Admin |
| `UC-279` | Freeze Payouts and Top-Up Crediting on a Ledger-Integrity Alarm | Admin |
| `UC-280` | Run the Pre-Launch Money-Cycle Audit | Admin |
| `UC-281` | Reassign a Stalled Delivery Back to the Offer Pool | Admin |
| `UC-282` | Pull Delivery Proof for a Dispute Review | Admin |
| `UC-283` | Arbitrate a Dispute and Choose the Prevailing Party | Admin |
| `UC-284` | Attach Platform Evidence to a Dispute Case | Admin |
| `UC-285` | Track Open Disputes and Their Frozen Escrow Exposure | Admin |
| `UC-286` | Verify Refund Credits Within the 3-Business-Day SLA | Admin |
| `UC-287` | Run the Orders Report | Admin |
| `UC-288` | Run the GMV Report | Admin |
| `UC-289` | Run the Returns and Refunds Report | Admin |
| `UC-290` | Monitor Queue Depths and SLA Breaches as Moderator | Moderator |
| `UC-291` | Review a CMS Page's Publish History Before Republishing | Admin |
| `UC-292` | Disable a Store Coupon for Promotion Abuse | Admin |
| `UC-293` | Investigate Coupon-Abuse Patterns Across Orders and Refunds | Admin |
| `UC-294` | Hide Reported Content With a Reason as Moderator | Moderator |
| `UC-295` | Isolate Auto-Created Delivery-Code Tickets in the Support Queue | Admin |
| `UC-296` | Investigate an Audit Hash-Chain Verification Failure | Admin |
| `UC-297` | Extract Audit Evidence for a Security Incident | Admin |
| `UC-298` | Re-Drive a Failed Job From the Dead-Letter Queue | Admin |
| `UC-299` | Dispose of Aged Data-Quality Quarantine Records | Admin |
| `UC-300` | Review the Weekly Retention Purge Report | Admin |
| `UC-301` | Investigate a Guard-Blocked Retention Purge Attempt | Admin |
| `UC-302` | Resolve a Settings Version Conflict After a Concurrent Edit | Super Admin |
| `UC-303` | Track Critical Security Findings Against the 7-Day Remediation SLA | Admin |
| `UC-304` | Audit the Evidence Entry of a Completed Purge Run | Admin |
| `UC-305` | Review the Monthly Security Severity Report | Admin |
| `UC-306` | Delete an Address Used by an In-Flight Checkout | Customer |
| `UC-307` | Hit the 10-Address Cap and Free Up a Slot | Customer |
| `UC-308` | Keep Past Orders on Their Address Snapshot After Editing the Book | Customer |
| `UC-309` | Recover After a Refresh-Token Reuse Revokes the Session Family | Customer |
| `UC-310` | Sit Through the 15-Minute Lockout Countdown After Five Failed Logins | Customer |
| `UC-311` | Collect the OTP via WhatsApp When SMS Delivery Fails | Customer |
| `UC-312` | Hit the OTP Attempt Cap and Read the Blocked-Verification Notice | Customer |
| `UC-313` | Attach Photos to a Product Review and Handle Upload Rejections | Customer |
| `UC-314` | Attempt a Review After the 30-Day Window and Get Rejected | Customer |
| `UC-315` | Filter a Product's Reviews by Rating | Customer |
| `UC-316` | Read the Vendor's Published Response Beneath Your Review | Customer |
| `UC-317` | Check the Return Policy and Window on the Product Page | Customer |
| `UC-318` | List the Stores You Follow | Customer |
| `UC-319` | Unfollow a Store and Stop Its Notifications | Customer |
| `UC-320` | Open a Suspended Storefront and Find It Unavailable | Customer |
| `UC-321` | Combine Search Filters and Compare Facet Counts | Customer |
| `UC-322` | Sort Results by Relevance, Price, Rating, or Newest | Customer |
| `UC-323` | Recover from a Zero-Result Search with Suggestions and Popular Categories | Customer |
| `UC-324` | Fall Back to Category Browse When Search Is Unavailable | Customer |
| `UC-325` | Add Past a Cart Guard and Leave the Cart Unchanged | Customer |
| `UC-326` | Re-Reserve Stock When a Cart Line's 15-Minute Countdown Expires | Customer |
| `UC-327` | Re-Confirm a Price That Changed Since Add-to-Cart | Customer |
| `UC-328` | Remove an Ineligible Line That Blocks Checkout | Customer |
| `UC-329` | Merge the Guest Cart Into the Account Cart on Login | Customer |
| `UC-330` | Resume Checkout After Topping Up the Wallet Shortfall | Customer |
| `UC-331` | Retry a Duplicate Confirm and Receive the Original Order | Customer |
| `UC-332` | Reject an Order Total Outside the 500-5,000,000 YER Bounds | Customer |
| `UC-333` | Handle a Shipping-Zone Gap for the Selected Address | Customer |
| `UC-334` | Filter the Order List by Status | Customer |
| `UC-335` | Refresh the Order Screen After a Status Conflict | Customer |
| `UC-336` | Receive the 24-Hour Escalation Notice on a Stalled Order | Customer |
| `UC-337` | Get the Cancel-Window Refusal After READY_FOR_PICKUP | Customer |
| `UC-338` | Open the Order Receipt With the Full VAT Breakdown | Customer |
| `UC-339` | Filter Wallet Transactions by Type and Date Range | Customer |
| `UC-340` | Poll a Top-Up Awaiting Provider Confirmation | Customer |
| `UC-341` | Upload a Bank-Transfer Slip for Admin Verification | Customer |
| `UC-342` | Work With a Frozen Wallet (Pay and Top-Up Blocked, Refunds Still Received) | Customer |
| `UC-343` | Check Refund Status and the 3-Business-Day Wallet Credit Date | Customer |
| `UC-344` | Reject a Top-Up Outside the 1,000-5,000,000 YER Bounds | Customer |
| `UC-345` | Read Wallet Amounts Correctly as Arabic-Indic Numerals with a Screen Reader | Customer |
| `UC-346` | Retrieve the Delivery Code In-App When No SMS Arrives | Customer |
| `UC-347` | See Failed Delivery Attempts Reflected in Your Order Timeline | Customer |
| `UC-348` | Open the 24-Hour Code-Lockout Notice and Its Auto-Created Ticket | Customer |
| `UC-349` | Follow Delivery Progress Without a Map | Customer |
| `UC-350` | Check Return Eligibility Before Submitting a Request | Customer |
| `UC-351` | Open a Late-Window Return on a Completed Order | Customer |
| `UC-352` | Watch a Return Auto-Approve After the 72-Hour Inspection Timeout | Customer |
| `UC-353` | Read the Refund Composition (Item Value Versus Shipping) | Customer |
| `UC-354` | Resolve a Conflict Between an Open Dispute and a New Return | Customer |
| `UC-355` | Filter the Notification Inbox by Category and Unread State | Customer |
| `UC-356` | Disable a Marketing Channel Without Silencing Order Alerts | Customer |
| `UC-357` | See Locked Security Toggles in the Preference Center | Customer |
| `UC-358` | Keep Using the App When Push Permission Is Denied | Customer |
| `UC-359` | Add a Message and Attachment to an Open Support Ticket Thread | Customer |
| `UC-360` | Rate the Support Resolution in the Post-Ticket Survey | Customer |
| `UC-361` | Resolve Publish Blockers on an Incomplete Listing | Vendor |
| `UC-362` | Upload Product Images Within Count and Format Limits | Vendor |
| `UC-363` | Correct Price Validation Rejections on a Listing Draft | Vendor |
| `UC-364` | Define Product Variants Within Dimension and SKU Limits | Vendor |
| `UC-365` | Filter the Inventory Table for Low-Stock SKUs | Vendor |
| `UC-366` | Recover From a Stock Adjustment Blocked by Active Reservations | Vendor |
| `UC-367` | Confirm Search Visibility After a Catalog Change | Vendor |
| `UC-368` | Set Weekly Store Operating Hours | Vendor |
| `UC-369` | Revise KYC Documents Rejected at Upload | Vendor |
| `UC-370` | Block Demotion of the Last Store Owner | Vendor |
| `UC-371` | Handle Store Suspension During Active Fulfillment | Vendor |
| `UC-372` | Handle Staff Invitation Rejections (Unregistered Phone or Staff Limit) | Vendor |
| `UC-373` | Define Domestic Shipping Zones and Store Fees | Vendor |
| `UC-374` | Enable Auto-Accept for Incoming Sub-Orders | Vendor |
| `UC-375` | Start Fulfillment on a Confirmed Sub-Order | Vendor |
| `UC-376` | View the Append-Only Timeline for an Own Sub-Order | Vendor |
| `UC-377` | Recover From a State Conflict on a Concurrent Order Action | Vendor |
| `UC-378` | Handle a Closed Cancellation Window on a Dispatched Sub-Order | Vendor |
| `UC-379` | Triage the Sub-Order Queue by SLA Age | Vendor |
| `UC-380` | Track Overdue Return Decisions Before the 48-Hour Escalation | Vendor |
| `UC-381` | Track the Return Pickup Status After Approval | Vendor |
| `UC-382` | Handle a Return Auto-Approved After the 72-Hour Inspection Window | Vendor |
| `UC-383` | Raise a Dispute on an Own Sub-Order | Vendor |
| `UC-384` | Verify Return-Window Eligibility Before a Decision | Vendor |
| `UC-385` | Monitor Frozen Escrow Holds on Own Sub-Orders | Vendor |
| `UC-386` | Handle a Payout Request Below the 1,000 YER Minimum | Vendor |
| `UC-387` | Investigate a Rejected Payout's Reason and Ledger References | Vendor |
| `UC-388` | Resolve Payout Holds While KYC or Store Status Is Blocked | Vendor |
| `UC-389` | Re-Verify the Payout Account After a Destination Change | Vendor |
| `UC-390` | Compare Store Metrics Against the Previous Period | Vendor |
| `UC-391` | Resolve a Report Export Row-Cap Rejection | Vendor |
| `UC-392` | Adjust Schedule and Limits or Disable an Active Store Coupon | Vendor |
| `UC-393` | Resolve Store Coupon Creation Rejections (Bounds and Duplicate Code) | Vendor |
| `UC-394` | Configure Vendor Notification Preferences for Store Events | Vendor |
| `UC-395` | Open a Support Ticket About a Payout or Payment Issue | Vendor |
| `UC-396` | Decline a Delivery Offer Without Claiming It | Delivery Provider |
| `UC-397` | Review the Shipment Attempt Log Before a Retry | Delivery Provider |
| `UC-398` | Upload an Optional Delivery Photo as Extra Proof | Delivery Provider |
| `UC-399` | Finish on the Proof Success Screen and Continue to the Next Job | Delivery Provider |
| `UC-400` | Disable Code Entry When the Job Is Reassigned or Released | Delivery Provider |
| `UC-401` | Recover from Delivery-Code Entry Rate Limiting | Delivery Provider |
| `UC-402` | Keep Attempt and Lock Progress Across an App Restart | Delivery Provider |
| `UC-403` | Work a Delivery Whose Attempts Are Frozen for Admin Review | Delivery Provider |
| `UC-404` | Hear Code Attempt Feedback via Screen Reader | Delivery Provider |
| `UC-405` | Track Personal Delivery Stats on the Courier Profile | Delivery Provider |
| `UC-406` | Register This Courier Device for Job Push Notifications | Delivery Provider |
| `UC-407` | Open a Delivery Job from a Push Deep Link | Delivery Provider |
| `UC-408` | Fall Back to the In-App Inbox When Push Delivery Fails | Delivery Provider |
| `UC-409` | Configure Delivery Notification Channels as a Courier | Delivery Provider |
| `UC-410` | Resume a Delivery Deep Link After Signing In | Delivery Provider |
| `UC-411` | Re-Authenticate When the Session Expires Mid-Job | Delivery Provider |
| `UC-412` | Switch the Courier App Language Between Arabic and English | Delivery Provider |
| `UC-413` | Record Vendor Receipt of an Approved Return Package | Delivery Provider |
| `UC-414` | Escalate a Failed Return Pickup to Operations | Delivery Provider |
| `UC-415` | Browse Completed Jobs in the History Tab | Delivery Provider |
| `UC-416` | Handle Access Denied When Opening a Delivery You Do Not Own | Delivery Provider |
| `UC-417` | Record a Failed Pickup Attempt When the Store Is Not Ready | Delivery Provider |
| `UC-418` | Wait and Retry Later When the Customer Is Unavailable | Delivery Provider |
| `UC-419` | Work Only with a Masked Buyer Code at the Door | Delivery Provider |
| `UC-420` | Type the Delivery Code with Latin Digits in the Arabic Interface | Delivery Provider |

Actor totals across all 420 use cases (allocation `UC-001`…`UC-420`, naming-conventions v1.9):

| Actor | Use cases |
|---|---|
| Customer | 113 |
| Vendor | 67 |
| Delivery Provider | 37 |
| Admin | 102 |
| Super Admin | 6 |
| Moderator | 7 |
| System | 88 |
| **Total** | **420** |

## Preconditions
Each `UC-NNN` file carries its own preconditions, main/alternate/exception flows, postconditions and related IDs per [`../../23-templates/core/use-case-template.md`](../../23-templates/core/use-case-template.md).

## Main flow
Requirement → use case → workflow → API endpoint → entity → test: `FR-013 → BR-PAY-04 → UC-021 → API-WAL-002 → wallet → TC-031 → AC-FR013-01` (cross-referencing example, root README §5).

## Postconditions
420/420 use cases present; traceability matrices in [`19-traceability/`](../../19-traceability/README.md) cover every use case (`UC-*` 420 registered, consistency check `CHK` series).

## Invariants
No use case may describe a forbidden capability: COD/cards/BNPL/crypto (`C-01…C-04`), GPS/real-time tracking (`C-16`), email-primary/social login (`C-06`), third locale (`C-24`).

## Open questions (COM-01)
1. `UC-036` (Moderator) conflicts with `../../07-api/admin/admin.md` `API-ADM-022/024` on settings/audit-read — deferred sweep item (session 004 backlog).

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 4, session 005) | analysis-agent |
| 2026-09-28 | 1.1 | Inventory → 42 use cases: `UC-041`/`UC-042` added (customer money row), ranges/totals re-synced | Session-007 UC gap from `describ.md` §8 |
| 2026-09-29 | 1.2 | Inventory → **210 use cases**: `UC-043`…`UC-210` appended (168 rows, titles from the file H1s); header `42` → `210`, `42/42` → `210/210`, `UC-*` `42` → `210` registered, canonical range → `UC-001`…`UC-210`; actor totals table added (sums to 210) | `prompt-010.md` §1 (session 010 owner directive) |
| 2026-09-30 | 1.3 | Inventory → **420 use cases**: `UC-211`…`UC-420` appended (210 rows, titles from the file H1s); header `210` → `420`, `210/210` → `420/420`, `UC-*` `210` → `420` registered, canonical range → `UC-001`…`UC-420`; actor totals recomputed (sums to 420) | Owner directive session 011 (`prompt-011.md` §4.8) |
