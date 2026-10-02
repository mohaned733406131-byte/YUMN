---
document_id: DOC-BA-010
title: 01 Business Analysis — vendor/ portal folder
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

# 01 Business Analysis · `vendor/`

## Purpose

One of the five portal subfolders of `01-business-analysis/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **vendor-portal-specific material (sellers)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-BA-010 | This portal index — purpose, file table |
| [UC-015.md](UC-015.md) | DOC-UC-015 | UC-015 — Register as Vendor & Submit KYC |
| [UC-016.md](UC-016.md) | DOC-UC-016 | UC-016 — Manage Store Profile |
| [UC-017.md](UC-017.md) | DOC-UC-017 | UC-017 — Create / Edit Product Listing |
| [UC-018.md](UC-018.md) | DOC-UC-018 | UC-018 — Manage Inventory |
| [UC-019.md](UC-019.md) | DOC-UC-019 | UC-019 — View & Accept Incoming Order |
| [UC-020.md](UC-020.md) | DOC-UC-020 | UC-020 — Mark Order Ready for Pickup |
| [UC-021.md](UC-021.md) | DOC-UC-021 | UC-021 — Respond to Return Request |
| [UC-022.md](UC-022.md) | DOC-UC-022 | UC-022 — View Finances & Payouts |
| [UC-023.md](UC-023.md) | DOC-UC-023 | UC-023 — Create Store Coupon |
| [UC-024.md](UC-024.md) | DOC-UC-024 | UC-024 — Respond to Customer Review |
| [UC-183.md](UC-183.md) | DOC-UC-183 | UC-183 — Resubmit a Rejected Vendor Application |
| [UC-184.md](UC-184.md) | DOC-UC-184 | UC-184 — Track the KYC Case Status and SLA Age |
| [UC-185.md](UC-185.md) | DOC-UC-185 | UC-185 — View the Follower List and Count |
| [UC-186.md](UC-186.md) | DOC-UC-186 | UC-186 — Manage Store Staff (Invite, Change Role, Remove) |
| [UC-187.md](UC-187.md) | DOC-UC-187 | UC-187 — Configure the Payout Account |
| [UC-188.md](UC-188.md) | DOC-UC-188 | UC-188 — Unpublish a Product (Withdraw from Sale) |
| [UC-189.md](UC-189.md) | DOC-UC-189 | UC-189 — Soft-Delete a Product |
| [UC-190.md](UC-190.md) | DOC-UC-190 | UC-190 — Remove a Product Image |
| [UC-191.md](UC-191.md) | DOC-UC-191 | UC-191 — Inspect SKU Reservations and Expiry |
| [UC-192.md](UC-192.md) | DOC-UC-192 | UC-192 — Review the Sub-Order Queue |
| [UC-193.md](UC-193.md) | DOC-UC-193 | UC-193 — Cancel a Sub-Order Before Pickup |
| [UC-194.md](UC-194.md) | DOC-UC-194 | UC-194 — Review the Return Queue |
| [UC-195.md](UC-195.md) | DOC-UC-195 | UC-195 — Inspect a Received Return Within 72 Hours |
| [UC-196.md](UC-196.md) | DOC-UC-196 | UC-196 — Respond to a Dispute with Evidence |
| [UC-197.md](UC-197.md) | DOC-UC-197 | UC-197 — Track Dispute Status |
| [UC-198.md](UC-198.md) | DOC-UC-198 | UC-198 — Request a Payout |
| [UC-199.md](UC-199.md) | DOC-UC-199 | UC-199 — View the Sales Dashboard |
| [UC-200.md](UC-200.md) | DOC-UC-200 | UC-200 — Run a Store Report |
| [UC-201.md](UC-201.md) | DOC-UC-201 | UC-201 — Export a Store Report as CSV |
| [UC-202.md](UC-202.md) | DOC-UC-202 | UC-202 — View Store Reviews |
| [UC-203.md](UC-203.md) | DOC-UC-203 | UC-203 — List Store Coupons |
| [UC-204.md](UC-204.md) | DOC-UC-204 | UC-204 — Open a Support Ticket About an Order |
| [workflow-004.md](workflow-004.md) | DOC-WF-005 | "WF-004 — Vendor Order Acceptance → Fulfillment → READY_FOR_PICKUP" |
| [workflow-011.md](workflow-011.md) | DOC-WF-012 | "WF-011 — Vendor Onboarding: Register → KYC Submit → Approve → First Listing" |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (34 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
