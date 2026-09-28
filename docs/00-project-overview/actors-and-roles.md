---
document_id: DOC-OVR-007
title: Actors and Roles
category: 00-project-overview
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [FR-001, FR-002, FR-003]
related_documents: [DOC-OVR-006, DOC-OVR-008]
---

# Actors and Roles

**Canonical actor list — exactly 7 actors.** Every use case, permission matrix, API authorization rule, and test must use these names (see `22-glossary/terminology.md`).

## Actor Register

| ID | Actor | Type | Description |
|---|---|---|---|
| ACT-01 | **Customer** | Human | Browses, buys, pays from wallet, tracks, returns, reviews |
| ACT-02 | **Vendor** | Human | Manages store, KYC, catalog, inventory, orders, finances |
| ACT-03 | **Delivery Provider (Courier)** | Human | Accepts assignments, picks up, delivers, confirms with code |
| ACT-04 | **Admin** | Human | Day-to-day platform operations (scoped permissions) |
| ACT-05 | **Super Admin** | Human | Full platform control, roles/permission management, config |
| ACT-06 | **Moderator** | Human | Content moderation, review flags, support escalation |
| ACT-07 | **System** | Non-human | Background jobs, schedulers, webhooks, automated engines |

> Canonical naming rule: never use "Customer / Buyer / Shopper / User" interchangeably — **Customer** is the only term for ACT-01 (`22-glossary/terminology.md`).

## Role Hierarchy

```text
Super Admin (ACT-05)
   └── Admin (ACT-04)          — platform operations
   └── Moderator (ACT-06)      — content/support moderation
Vendor Owner ──► Vendor Staff (Viewer/Editor/Manager)   [ACT-02, scoped to own store]
Delivery Provider (ACT-03)     — scoped to own deliveries
Customer (ACT-01)              — scoped to own resources
System (ACT-07)                — service identities, no interactive login
```

## Permission Summary per Actor

| Capability | Customer | Vendor | Courier | Admin | Super Admin | Moderator | System |
|---|---|---|---|---|---|---|---|
| Browse/search/cart (guest→login gate) | ✔ | ✔ | ✖ | ✔ | ✔ | ✔ | — |
| Place order / wallet use | ✔ (own) | ✖ | ✖ | ✖ | ✖ | ✖ | — |
| Manage own store & catalog | ✖ | ✔ (own store) | ✖ | ✔ | ✔ | ✖ | — |
| View own deliveries | ✖ | ✖ | ✔ (own) | ✔ | ✔ | ✖ | — |
| KYC approval | ✖ | submit only | ✖ | ✔ | ✔ | ✖ | — |
| Order state override | ✖ | limited (own sub-orders) | delivery states | ✔ | ✔ | ✖ | ✔ (automated) |
| Refund approval (to wallet) | request | respond | ✖ | ✔ | ✔ | ✖ | auto per rule |
| Manage roles/permissions | ✖ | staff invite only | ✖ | ✖ | ✔ | ✖ | ✖ |
| Moderation (reviews, content) | report only | respond | ✖ | ✔ | ✔ | ✔ | auto-flag |
| Read audit log | ✖ | own store scope | own scope | platform scope | full | ✖ | write-only |
| System configuration | ✖ | store settings only | ✖ | limited | ✔ | ✖ | runtime config |

Full permission matrices: `09-security/rbac.md` (definitive) and `06-backend/authorization.md` (enforcement).

## Resource Ownership (cross-user access rules)

| Resource | Owner | Others |
|---|---|---|
| Wallet / transactions | Customer | No read/write ever (not even Admin — Admin can *flag*, ledger is append-only) |
| Orders | Customer (buyer) + vendor (own sub-orders) | Admin read/override per RBAC; no cross-customer access |
| Store & products | Vendor (own `store_id`) | Admin/Moderator oversight; other vendors never |
| Deliveries | Courier (assigned) | Admin dispatch view only |
| Audit logs | Platform (append-only) | Read per role scope; nobody edits |

Conceptual authorization tests (see `13-testing/test-cases/TC-011…TC-014`):
1. Can Customer A access Customer B's order? → **Must be denied** (ownership + IDOR checks)
2. Can Vendor X modify Vendor Y's product? → **Must be denied** (`store_id` scoping)
3. Can Vendor Staff escalate to Owner? → **Must be denied** (self-role-change blocked)
4. Can a banned customer call the API directly bypassing UI? → **Must be denied** (server-side enforcement)

## Consistency Rule

Changing an actor here propagates to: `01-business-analysis` (use cases) → `02-requirements` (FR-002) → `09-security/rbac.md` → `06-backend/authorization.md` → `08-database` (roles tables) → `05-frontend` (route guards) → `13-testing` → `19-traceability` → `20-validation/consistency-audit.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | Consistency-rule cite corrected: `07-api/authorization.md` (no such file) → `06-backend/authorization.md` (the actual authorization document) | `REC-15` citation-CI enforcement (session 008) — the one genuinely dangling path; `HAL-12` evidence, first clause fixed here |
