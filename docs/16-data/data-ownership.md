---
document_id: DOC-DTA-003
title: Data Ownership & Access Matrix
category: 16-data
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-008, DATA-REQ-002, DATA-REQ-007, FR-002, FR-008, SEC-REQ-004]
related_documents: [DOC-DTA-001, DOC-DTA-002, DOC-DTA-004, DOC-DR-008, DOC-BA-005, DOC-OVR-007]
---

# DOC-DTA-003 — Data Ownership & Access Matrix

## 1. Purpose

Defines **who owns which data, who holds custody, which roles may read or write it, and within what scope** — the operational form of `DATA-REQ-008` (ownership boundaries) and `BR-VND-07` (store scoping), `BR-ORD-09` (order visibility). Ownership answers three separate questions that are often conflated:

| Question | Answer pattern |
|---|---|
| **Ownership** — whose data is it in law and business terms? | An actor (or the platform) |
| **Custody** — who stores and administers it? | Always **yumn (the platform)** as legal custodian (`INFERENCE` — operator of the system of record) |
| **Access** — which roles may read/write, and scoped how? | Per-row owner keys + role grants in §4 |

**Non-negotiables:** every tenant-scoped table carries `user_id`/`store_id`/`courier_id` owner keys (`DATA-REQ-008` R1); every read/write includes the owner predicate (R2); background jobs are parameterized by owner (R4); the `System` role is never an escape hatch for unscoped reads (R3, `SEC-REQ-004` R5).

## 2. Ownership Matrix

Legend for access column: **R** = read, **W** = write, **—** = no access, **R*** = scoped read (own rows only), **W*** = scoped write (own rows only). Roles: CU = Customer, VN = Vendor (incl. staff), CO = Courier, AD = Admin, SA = Super Admin, MO = Moderator, SY = System.

| Data domain | Owner actor | Custody | CU | VN | CO | AD | SA | MO | SY | Write scope |
|---|---|---|---|---|---|---|---|---|---|---|
| Account profile (phone, name, email, locale) | Customer (ACT-01) | Platform | W* own | — | — | R masked | R | — | W job | Owner only; Admin read = support view, no edit of identity |
| Address book (≤10) | Customer (ACT-01) | Platform | RW* own | — | R assigned shipment only | R masked | R | — | W job | Owner only; never editable by staff |
| Wallet balance & transactions | Customer (ACT-01) | Platform | R* own | — | — | **—** (may flag only) | R scope | — | W postings | Append-only postings by money services only (`DATA-REQ-007`) |
| Ledger postings / escrow / commission | Platform (joint: Customer+Vendor economic interest) | Platform | R* own | R* own | — | R reports | R | — | W append-only | INSERT-only app role; corrections = compensating rows |
| Vendor payable & payout records | Vendor (ACT-02) | Platform | — | R* own | — | R platform scope | R | — | W jobs | Finance services; vendor never writes |
| Orders (master) | Customer (buyer) | Platform | R* own, W cancel | R sub-order | — | R/W override | R/W | R scoped | W state jobs | State machine + `order_status_history` append-only (`BR-ORD-03`) |
| Sub-orders & fulfillment | Vendor (own store) | Platform | R own items | W* own | R assigned | R/W | R/W | R scoped | W jobs | Vendor advances only own fulfillment steps (`BR-ORD-07`) |
| Delivery assignment & shipment fields | Courier (assigned) | Platform | R own shipment | R own shipment | R* assigned only | R dispatch | R | — | W assignment jobs | Courier writes pickup/delivery/code verification only |
| Products & images | Vendor (own `store_id`) | Platform | R (public) | RW* own | — | R/W moderation | R/W | R/W hide | W jobs | Soft-delete only (`BR-CAT-06`); moderators may hide, never edit content |
| Inventory & reservations | Vendor (own store) | Platform | — | RW* own | — | R | R | — | W reservation jobs | Atomic stock ops; System releases expired TTL holds (`C-13`) |
| Store profile, zones, settings | Vendor (own store) | Platform | R public | RW* own | — | R/W | R/W | — | W jobs | Staff roles Viewer/Editor/Manager; only Owner changes staff (`BR-VND-06`) |
| KYC documents & decision | Vendor (submit) / Platform (verify) | Platform | — | W submission, R own status | — | **R/W review** | R/W | — | W workflow | Admin/Super Admin only; 48 h SLA (`BR-VND-03`) |
| Reviews & responses | Customer (review) / Vendor (response) | Platform | RW* own | R/W response own store | — | R/W hide | R/W | **R/W moderation** | W flag jobs | One edit within 7 days (`BR-REV-02`); hide writes audit (`BR-REV-04`) |
| Coupons | Platform (global) / Vendor (store) | Platform | R apply | RW* store coupons | — | R/W all | R/W | R disable | W jobs | Admin can list/disable store coupons (`BR-PRM-03`) |
| Notifications (user inbox) | Customer / recipient actor | Platform | RW* own | R own store msgs | R own assignments | R ops view | R | — | W fan-out | Preferences per channel (`BR-NTF-05`); security notices non-disableable |
| Audit log | Platform (yumn) | Platform | — | R own-store scope | R own scope | R platform scope | R full | — | **W append-only** | Nobody updates/deletes; System writes only (`SEC-REQ-010`) |
| Support tickets & disputes | Platform + requesting party | Platform | R own | R own | R own | RW | RW | RW scoped | W workflow | Moderator handles content/support scope, not finance |
| Search index (derived) | Platform (from Vendor content) | Platform | R search | R/W reindex own | — | R/W reindex | R | R/W demote | W indexer | Indexer writes derived docs only; never PII (`DOC-DTA-002` §3.9) |
| Backups & infrastructure config | Platform | Platform | — | — | — | — | R/W ops | — | W jobs | Operations role only (`DATA-REQ-004` R3) |
| Metrics & dashboards | Platform | Platform | — | R own dashboard | — | R platform | R | R moderation metrics | W scrape | Vendor dashboards scoped to `store_id` (`FR-018`) |

## 3. Role Scope Definitions

### 3.1 Customer (ACT-01)
Own profile, addresses, orders, wallet, reviews, tickets, notifications. Read-only on public catalog. **No** access to any other customer's rows — enforced by ownership + IDOR tests (`actors-and-roles.md` Q1). The phone is the immutable identity anchor (`C-06`, `BR-AUTH-01`).

### 3.2 Vendor (ACT-02) and staff (Viewer / Editor / Manager)
Everything scoped to **own `store_id`** — products, inventory, sub-orders, store coupons, payable ledger, follower list (`BR-VND-05`), analytics (`FR-018`). Cross-store access denied at the service layer (`BR-VND-07`) and proven by the cross-tenant suite (`AC-DR008-02`). Staff capability is a subset of Owner; only the Owner invites/removes/changes staff (`BR-VND-06`). **Vendor never sees:** buyer profile history, buyer wallet, other vendors' data, courier identity beyond the assignment, KYC reviewer notes.

### 3.3 Delivery Provider / Courier (ACT-03)
Sees **only the assigned shipment's delivery fields**: pickup instructions, drop address (governorate/district/street + notes), recipient name, recipient contact phone, delivery window, and the 6-digit confirmation flow (`BR-SHP-02`). Own delivery history only; no catalog economics, no wallet data, no other courier's queue.

**Contact-phone decision (scoping vs `C-16`):** *Decision — the courier sees the full recipient phone only after accepting the assignment, and it is masked to last-4 in all views before acceptance and after delivery completion.*
- *Justification for full number during delivery:* the platform is phone-only (`C-06`); SMS/WhatsApp are the sole contact channels (`BR-NTF-01`), and failed-contact deliveries are the platform's main cost driver. Without the number the courier cannot complete the delivery contract, so necessity under `DATA-REQ-002` is satisfied for that window.
- *Justification for masking elsewhere:* minimization applies by **time and assignment scoping** — pre-acceptance there is no delivery necessity (an unaccepted offer leaks customer data to the whole zone, `BR-SHP-04`); post-delivery the contact purpose ends and the last-4 suffices for support reference. `C-16` forbids **location/GPS collection** (`BR-SHP-05`), not delivery contact — no location field exists anywhere, so there is no tension with `C-16`. Delivery proof remains code + timestamp + courier identity (`BR-SHP-07`).
- Evidence: this decision is a purpose entry in `data-classification.md` (phone → courier view) and is tested by `AC-DR008-02`-style field assertions.

### 3.4 Admin (ACT-04) — day-to-day operations
Scoped permissions, not blanket read: KYC review, order overrides, refund approval, wallet **freeze** (never balance edit — postings are append-only, `BR-PAY-09`), support tickets, moderation oversight, limited config (`FR-020`). Read on audit log = platform scope. **Cannot** read raw wallet/ledger contents beyond reporting aggregates (`actors-and-roles.md`: Admin may *flag* only).

### 3.5 Super Admin (ACT-05)
Full platform control: role/permission management, platform settings, unrestricted reporting read. Same immutability limits as everyone else — no `UPDATE`/`DELETE` on ledger or audit rows (`DATA-REQ-007`, `SEC-REQ-010`). Every Super Admin action is itself audited (`BR-PLT-06`).

### 3.6 Moderator (ACT-06)
Content/support scope **only**: reviews (hide/respond with audit, `BR-REV-04`), flagged content, support escalation, coupon disable in abuse cases. **No** access to financial records, KYC documents, or identity PII beyond what a support reply requires (masked phone reference).

### 3.7 System (ACT-07)
Service identities: indexers, reconcilers, purge jobs, webhooks, state-machine automation. Authenticate through internal mechanisms only, never interactively, never as a bypass around ownership checks (`SEC-REQ-004` R5). Each job is parameterized by owner and touches only that owner's rows (`AC-DR008-03`).

## 4. Enforcement Mechanisms

| Layer | Mechanism | Ref |
|---|---|---|
| Schema | Owner key columns (`user_id`, `store_id`, `courier_id`) + FK + supporting indexes | `DATA-REQ-008` R1, `DATA-REQ-001` |
| Query | Owner predicate mandatory in repository/service layer; RBAC + ownership check on **every** endpoint | `SEC-REQ-004`, `DATA-REQ-008` R2 |
| Jobs | BullMQ payloads carry owner keys; worker asserts scope | `DATA-REQ-008` R4, `C-20` |
| Tests | Cross-tenant suite per entity + CI coverage gate for new entities | `AC-DR008-01…04` |
| API | Per-endpoint PII allowlists; response fields limited to purpose | `DATA-REQ-002` R4, `AC-DR002-04` |
| Frontend | Route guards are UX only — never security | `SEC-REQ-004` |

## 5. Storage Location & Cross-Border Assumption

**`INFERENCE` (assumption — flagged):** production data (Postgres, Redis, ES, MinIO, backups) is hosted **inside the region** (Yemen/MENA data center or an in-country facility operated under yumn's control), so no routine cross-border transfer of PII occurs. **Evidence status: `INSUFFICIENT EVIDENCE`** — hosting location is not fixed by any constraint (`C-01…C-26`) or dependency (`DEP-01…DEP-12`); the stack is deliberately cloud-vendor-agnostic and Docker-host portable (`NFR-016`, `C-22`).

Consequences if the assumption fails: cross-border processing must be assessed under Yemeni Law No. (11) of 2012 on Personal Data Protection (`project-context.md` §Compliance), which remains detail-`INSUFFICIENT EVIDENCE` pending the legal opinion in `DEP-09` / `ASM-13`. The hosting decision must be confirmed by the sponsor before launch and recorded in `20-validation/missing-information.md` and, if it changes the design, in an ADR (`18-decisions/ADR/`). Processor list (SMS, WhatsApp, wallet providers, MinIO host) must be re-checked against the same question at `DEP-06`/`DEP-05` contract signing.

## 6. Conflict Rules

1. Ownership beats role: a Moderator's role grant never overrides row ownership (`DATA-REQ-008` R3).
2. Custody never transfers: even on account deletion, the platform controls the deletion procedure (`DOC-DTA-006`) and the retained financial record.
3. Immutability beats administrative power: no role, including Super Admin, can `UPDATE`/`DELETE` ledger or audit rows.
4. Fulfillment necessity beats minimization only inside a bounded scope/time (courier phone rule §3.3); every such exception must appear as a purpose entry in `data-classification.md`.
5. Derived stores (ES, Redis) inherit ownership of their source rows — scoping applies to index and cache access too.

## 7. Verification

- Cross-tenant suite green for every entity; coverage gate fails CI on new entities (`AC-DR008-04`).
- Field-level assertion for the courier visibility windows (pre-accept masked / active full / post-delivery last-4).
- Role-scope matrix diff-tested against `../09-security/core/rbac.md` (definitive RBAC) whenever either document changes — divergence logged in `20-validation/consistency-audit.md`.
- Storage-location assumption reviewed at each launch gate (`AC-S-24` legal sign-offs).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
