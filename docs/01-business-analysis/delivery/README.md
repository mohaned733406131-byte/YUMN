---
document_id: DOC-BA-012
title: 01 Business Analysis — delivery/ portal folder
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

# 01 Business Analysis · `delivery/`

## Purpose

One of the five portal subfolders of `01-business-analysis/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **delivery/courier-app-specific material (couriers)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-BA-012 | This portal index — purpose, file table |
| [UC-025.md](UC-025.md) | DOC-UC-025 | UC-025 — View Available Deliveries |
| [UC-026.md](UC-026.md) | DOC-UC-026 | UC-026 — Accept Delivery Assignment |
| [UC-027.md](UC-027.md) | DOC-UC-027 | UC-027 — Confirm Package Pickup |
| [UC-028.md](UC-028.md) | DOC-UC-028 | UC-028 — Update Transit & Attempt Delivery |
| [UC-029.md](UC-029.md) | DOC-UC-029 | UC-029 — Record Failed Delivery Attempt |
| [UC-030.md](UC-030.md) | DOC-UC-030 | UC-030 — Confirm Delivery with 6-Digit Code |
| [UC-205.md](UC-205.md) | DOC-UC-205 | UC-205 — Release an Accepted Assignment Back to the Pool |
| [UC-206.md](UC-206.md) | DOC-UC-206 | UC-206 — Update Courier Profile and Served Zones |
| [UC-207.md](UC-207.md) | DOC-UC-207 | UC-207 — Toggle Availability Online/Offline |
| [UC-208.md](UC-208.md) | DOC-UC-208 | UC-208 — Handle the 24-Hour Code Lockout After Third Failure |
| [UC-209.md](UC-209.md) | DOC-UC-209 | UC-209 — Follow the Order Timeline During a Delivery |
| [UC-210.md](UC-210.md) | DOC-UC-210 | UC-210 — Open a Support Ticket About a Delivery |
| [workflow-005.md](workflow-005.md) | DOC-WF-006 | "WF-005 — Courier Assignment → Pickup → Transit → Delivery Code → DELIVERED" |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (13 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
