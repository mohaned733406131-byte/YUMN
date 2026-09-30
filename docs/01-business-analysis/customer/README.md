---
document_id: DOC-BA-011
title: 01 Business Analysis — customer/ portal folder
category: 01-business-analysis
status: approved
version: 1.0
created: 2026-09-30
updated: 2026-09-30
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-BA-001]
---

# 01 Business Analysis · `customer/`

## Purpose

One of the five portal subfolders of `01-business-analysis/` (portal partition — `22-glossary/naming-conventions.md` §1):
holds **customer-app-specific material (buyers)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-BA-011 | This portal index — purpose, file table |
| [UC-001.md](UC-001.md) | DOC-UC-001 | UC-001 — Browse Marketplace as Guest |
| [UC-002.md](UC-002.md) | DOC-UC-002 | UC-002 — Register with Phone + OTP |
| [UC-003.md](UC-003.md) | DOC-UC-003 | UC-003 — Login with Phone & Password |
| [UC-004.md](UC-004.md) | DOC-UC-004 | UC-004 — Reset Password via OTP |
| [UC-005.md](UC-005.md) | DOC-UC-005 | UC-005 — Manage Addresses |
| [UC-006.md](UC-006.md) | DOC-UC-006 | UC-006 — Search Products |
| [UC-007.md](UC-007.md) | DOC-UC-007 | UC-007 — View Product Detail |
| [UC-008.md](UC-008.md) | DOC-UC-008 | UC-008 — Follow a Store |
| [UC-009.md](UC-009.md) | DOC-UC-009 | UC-009 — Add Product to Cart |
| [UC-010.md](UC-010.md) | DOC-UC-010 | UC-010 — Manage Cart |
| [UC-011.md](UC-011.md) | DOC-UC-011 | UC-011 — Checkout with Wallet Payment |
| [UC-012.md](UC-012.md) | DOC-UC-012 | UC-012 — Track Order |
| [UC-013.md](UC-013.md) | DOC-UC-013 | UC-013 — Confirm Receipt with Delivery Code |
| [UC-014.md](UC-014.md) | DOC-UC-014 | UC-014 — Contact Support |
| [UC-041.md](UC-041.md) | DOC-UC-041 | UC-041 — Top Up Wallet |
| [UC-042.md](UC-042.md) | DOC-UC-042 | UC-042 — View Wallet Statement |
| [UC-141.md](UC-141.md) | DOC-UC-141 | UC-141 — Resend an OTP (Registration, Login, or Reset) |
| [UC-142.md](UC-142.md) | DOC-UC-142 | UC-142 — Complete Step-Up OTP Verification for a Sensitive Change |
| [UC-143.md](UC-143.md) | DOC-UC-143 | UC-143 — Log Out of the Current Device |
| [UC-144.md](UC-144.md) | DOC-UC-144 | UC-144 — Log Out of All Devices |
| [UC-145.md](UC-145.md) | DOC-UC-145 | UC-145 — Change Password While Signed In |
| [UC-146.md](UC-146.md) | DOC-UC-146 | UC-146 — View Active Device Sessions |
| [UC-147.md](UC-147.md) | DOC-UC-147 | UC-147 — Revoke Another Device's Session |
| [UC-148.md](UC-148.md) | DOC-UC-148 | UC-148 — View and Edit Profile |
| [UC-149.md](UC-149.md) | DOC-UC-149 | UC-149 — Add and Verify an Optional Email |
| [UC-150.md](UC-150.md) | DOC-UC-150 | UC-150 — Upload a Profile Avatar |
| [UC-151.md](UC-151.md) | DOC-UC-151 | UC-151 — Manage Account Preferences |
| [UC-152.md](UC-152.md) | DOC-UC-152 | UC-152 — Switch the Interface Locale (ar/en) |
| [UC-153.md](UC-153.md) | DOC-UC-153 | UC-153 — Request Account Deletion |
| [UC-154.md](UC-154.md) | DOC-UC-154 | UC-154 — Cancel a Pending Deletion Request |
| [UC-155.md](UC-155.md) | DOC-UC-155 | UC-155 — Browse the Personalized Home Feed |
| [UC-156.md](UC-156.md) | DOC-UC-156 | UC-156 — Use Search Suggestions (Typeahead) |
| [UC-157.md](UC-157.md) | DOC-UC-157 | UC-157 — Browse Deals and the Promotion Gallery |
| [UC-158.md](UC-158.md) | DOC-UC-158 | UC-158 — Read Static Content and Help Pages |
| [UC-159.md](UC-159.md) | DOC-UC-159 | UC-159 — Track a Guest Order via a Tokenized Link |
| [UC-160.md](UC-160.md) | DOC-UC-160 | UC-160 — Clear the Entire Cart |
| [UC-161.md](UC-161.md) | DOC-UC-161 | UC-161 — Review the Authoritative Checkout Preview |
| [UC-162.md](UC-162.md) | DOC-UC-162 | UC-162 — Apply and Validate a Coupon at Checkout |
| [UC-163.md](UC-163.md) | DOC-UC-163 | UC-163 — Cancel an Order Before Dispatch |
| [UC-164.md](UC-164.md) | DOC-UC-164 | UC-164 — View Wallet Balance and Status |
| [UC-165.md](UC-165.md) | DOC-UC-165 | UC-165 — Write a Product Review After Delivery |
| [UC-166.md](UC-166.md) | DOC-UC-166 | UC-166 — Edit a Review Once Within 7 Days |
| [UC-167.md](UC-167.md) | DOC-UC-167 | UC-167 — Report a Review for Moderation |
| [UC-168.md](UC-168.md) | DOC-UC-168 | UC-168 — Request a Return for Delivered Items |
| [UC-169.md](UC-169.md) | DOC-UC-169 | UC-169 — Track Return Request Status |
| [UC-170.md](UC-170.md) | DOC-UC-170 | UC-170 — View the Return Pickup Schedule |
| [UC-171.md](UC-171.md) | DOC-UC-171 | UC-171 — Open a Dispute on a Delivered Order |
| [UC-172.md](UC-172.md) | DOC-UC-172 | UC-172 — Submit Dispute Evidence |
| [UC-173.md](UC-173.md) | DOC-UC-173 | UC-173 — Review the Dispute Resolution Outcome |
| [UC-174.md](UC-174.md) | DOC-UC-174 | UC-174 — View Escrow Holding Status for Own Orders |
| [UC-175.md](UC-175.md) | DOC-UC-175 | UC-175 — Open the Notification Inbox |
| [UC-176.md](UC-176.md) | DOC-UC-176 | UC-176 — Mark Notifications Read or Remove Them |
| [UC-177.md](UC-177.md) | DOC-UC-177 | UC-177 — Configure Notification Preferences |
| [UC-178.md](UC-178.md) | DOC-UC-178 | UC-178 — Register This Device for Push Notifications |
| [UC-179.md](UC-179.md) | DOC-UC-179 | UC-179 — Manage Registered Push Devices |
| [UC-180.md](UC-180.md) | DOC-UC-180 | UC-180 — View Own Support Ticket List and Status |
| [UC-181.md](UC-181.md) | DOC-UC-181 | UC-181 — Resume an Existing Session on App Launch (Mobile) |
| [UC-182.md](UC-182.md) | DOC-UC-182 | UC-182 — Receive and Open a Deep-Linked Order Push |
| [workflow-001.md](workflow-001.md) | DOC-WF-002 | "WF-001 — Customer Registration & Login" |
| [workflow-002.md](workflow-002.md) | DOC-WF-003 | "WF-002 — Search → PDP → Add to Cart (guest gating)" |
| [workflow-003.md](workflow-003.md) | DOC-WF-004 | "WF-003 — Cart → 7-Step Checkout → Wallet Payment → Order Placed" |
| [workflow-009.md](workflow-009.md) | DOC-WF-010 | "WF-009 — Wallet Top-Up (m-Floos/OneCash Callback, Bank Transfer Admin Verification)" |
| [workflow-010.md](workflow-010.md) | DOC-WF-011 | "WF-010 — Cancellation (Customer Pre-Dispatch) → Refund" |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (63 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
