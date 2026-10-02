---
document_id: DOC-INT-009
title: 10 Integrations — core/ portal folder
category: 10-integrations
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-INT-000]
---

# 10 Integrations · `core/`

## Purpose

One of the five portal subfolders of `10-integrations/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-INT-009 | This portal index — purpose, file table |
| [bank-transfer-topup.md](bank-transfer-topup.md) | DOC-INT-003 | Bank Transfer Top-Up — Manual Admin Verification Flow |
| [integration-overview.md](integration-overview.md) | DOC-INT-001 | Integration Layer Architecture (Ports, Async, Degradation) |
| [push-notifications.md](push-notifications.md) | DOC-INT-006 | Push Notifications — FCM & APNs Integration |
| [sms-provider.md](sms-provider.md) | DOC-INT-004 | SMS Integration — Templates, Failover & Degradation |
| [testing-and-sandboxes.md](testing-and-sandboxes.md) | DOC-INT-008 | Integration Testing Strategy — Sandboxes, Contract Tests & Go-Live |
| [wallet-providers.md](wallet-providers.md) | DOC-INT-002 | Wallet Top-Up Providers — m-Floos & OneCash Contract |
| [webhook-reliability.md](webhook-reliability.md) | DOC-INT-007 | Webhook Reliability — Inbound & Outbound Contract |
| [whatsapp-business.md](whatsapp-business.md) | DOC-INT-005 | WhatsApp Business — Template Notifications Contract |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (8 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
