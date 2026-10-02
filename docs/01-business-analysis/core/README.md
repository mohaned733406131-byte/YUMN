---
document_id: DOC-BA-008
title: 01 Business Analysis — core/ portal folder
category: 01-business-analysis
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-BA-001]
---

# 01 Business Analysis · `core/`

## Purpose

One of the five portal subfolders of `01-business-analysis/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-BA-008 | This portal index — purpose, file table |
| [UC-039.md](UC-039.md) | DOC-UC-039 | UC-039 — Auto-Release Escrow After 7 Days |
| [UC-040.md](UC-040.md) | DOC-UC-040 | UC-040 — Send OTP with Provider Failover |
| [UC-043.md](UC-043.md) | DOC-UC-043 | UC-043 — Rotate Refresh Tokens and Revoke Session Families on Reuse |
| [UC-044.md](UC-044.md) | DOC-UC-044 | UC-044 — Lock an Account After Five Consecutive Failed Logins |
| [UC-045.md](UC-045.md) | DOC-UC-045 | UC-045 — Sweep Expired Sessions and Orphaned Refresh Tokens |
| [UC-046.md](UC-046.md) | DOC-UC-046 | UC-046 — Expire Unpaid Stock Reservations After 15 Minutes |
| [UC-047.md](UC-047.md) | DOC-UC-047 | UC-047 — Commit Stock Reservations on Payment Success |
| [UC-048.md](UC-048.md) | DOC-UC-048 | UC-048 — Restore Stock When an Order Is Cancelled |
| [UC-049.md](UC-049.md) | DOC-UC-049 | UC-049 — Reconcile the Inventory Ledger Against On-Hand Stock |
| [UC-050.md](UC-050.md) | DOC-UC-050 | UC-050 — Recompute Store Ratings Incrementally |
| [UC-051.md](UC-051.md) | DOC-UC-051 | UC-051 — Release Unused Wallet Authorization Holds |
| [UC-052.md](UC-052.md) | DOC-UC-052 | UC-052 — Execute Scheduled Vendor Payout Batches |
| [UC-053.md](UC-053.md) | DOC-UC-053 | UC-053 — Roll Over Payouts Below the 1,000 YER Minimum |
| [UC-054.md](UC-054.md) | DOC-UC-054 | UC-054 — Run Daily Ledger and Escrow Reconciliation |
| [UC-055.md](UC-055.md) | DOC-UC-055 | UC-055 — Alert Finance on Reconciliation Mismatch |
| [UC-056.md](UC-056.md) | DOC-UC-056 | UC-056 — Generate Monthly Vendor Statements |
| [UC-057.md](UC-057.md) | DOC-UC-057 | UC-057 — Reverse Commission Proportionally on Refund |
| [UC-058.md](UC-058.md) | DOC-UC-058 | UC-058 — Execute Wallet Refunds to the Customer |
| [UC-059.md](UC-059.md) | DOC-UC-059 | UC-059 — Fan Out Notifications Across Channels by Preference |
| [UC-060.md](UC-060.md) | DOC-UC-060 | UC-060 — Honor Per-Category Notification Opt-Outs |
| [UC-061.md](UC-061.md) | DOC-UC-061 | UC-061 — Deliver Mandatory Security Notifications |
| [UC-062.md](UC-062.md) | DOC-UC-062 | UC-062 — Retry Failed Jobs and Alert on Dead-Letter Depth |
| [UC-063.md](UC-063.md) | DOC-UC-063 | UC-063 — Escalate Orders Stuck at CONFIRMED After 24 Hours |
| [UC-064.md](UC-064.md) | DOC-UC-064 | UC-064 — Guard Escrow Release While a Dispute Is Open |
| [UC-065.md](UC-065.md) | DOC-UC-065 | UC-065 — Auto-Create a Support Ticket on the Third Delivery-Code Failure |
| [UC-066.md](UC-066.md) | DOC-UC-066 | UC-066 — Auto-Close Stale Support Tickets |
| [UC-067.md](UC-067.md) | DOC-UC-067 | UC-067 — Synchronize the Search Index on Catalog Changes |
| [UC-068.md](UC-068.md) | DOC-UC-068 | UC-068 — Gate Traffic on Liveness and Readiness Probes |
| [UC-069.md](UC-069.md) | DOC-UC-069 | UC-069 — Normalize Slugs and Preserve Canonical URLs |
| [UC-070.md](UC-070.md) | DOC-UC-070 | UC-070 — Screen and Sanitize All Uploaded Files |
| [UC-071.md](UC-071.md) | DOC-UC-071 | UC-071 — Deliver Follower Marketing Notifications on New Products |
| [UC-072.md](UC-072.md) | DOC-UC-072 | UC-072 — Cascade a Store Suspension Across Catalog, Orders, and Payouts |
| [UC-073.md](UC-073.md) | DOC-UC-073 | UC-073 — Escalate KYC Decisions Past the 48-Hour SLA |
| [UC-074.md](UC-074.md) | DOC-UC-074 | UC-074 — Compensate a Failed Checkout Saga |
| [UC-075.md](UC-075.md) | DOC-UC-075 | UC-075 — Rebuild the Order Timeline Read Model |
| [UC-076.md](UC-076.md) | DOC-UC-076 | UC-076 — Reconcile Wallet Top-Ups Against Provider Polls and Callbacks |
| [UC-077.md](UC-077.md) | DOC-UC-077 | UC-077 — Broadcast Delivery Offers to Eligible Couriers |
| [UC-078.md](UC-078.md) | DOC-UC-078 | UC-078 — Sweep Expired Delivery Codes |
| [UC-079.md](UC-079.md) | DOC-UC-079 | UC-079 — Render Notification Templates Per Locale |
| [UC-080.md](UC-080.md) | DOC-UC-080 | UC-080 — Aggregate Dashboard Analytics Rollups |
| [UC-081.md](UC-081.md) | DOC-UC-081 | UC-081 — Generate Report Export Files |
| [UC-082.md](UC-082.md) | DOC-UC-082 | UC-082 — Deliver Signed Outbound Webhooks with Retry |
| [UC-083.md](UC-083.md) | DOC-UC-083 | UC-083 — Enforce Audit Log Retention and Redaction |
| [business-model.md](business-model.md) | DOC-BA-002 | Business Model |
| [business-objectives.md](business-objectives.md) | DOC-BA-003 | Business Objectives (BO-01 … BO-12) |
| [business-processes.md](business-processes.md) | DOC-BA-004 | Business Processes (BP-01 … BP-15) |
| [stakeholder-needs.md](stakeholder-needs.md) | DOC-BA-006 | Stakeholder Needs |
| [user-needs.md](user-needs.md) | DOC-BA-007 | User Needs (per Actor) |
| [workflow-006.md](workflow-006.md) | DOC-WF-007 | "WF-006 — Escrow: DELIVERED → 7-Day Hold → COMPLETED → Commission → Payout" |
| [workflow-007.md](workflow-007.md) | DOC-WF-008 | "WF-007 — Return Request → Approval → Pickup → Inspection → REFUNDED" |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (50 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
