---
document_id: DOC-TST-007
title: 13 Testing — core/ portal folder
category: 13-testing
status: approved
version: 1.1
created: 2026-09-30
updated: 2026-10-02
author: analysis-agent
source_of_truth: false
related_requirements: []
related_documents: [DOC-TST-001]
---

# 13 Testing · `core/`

## Purpose

One of the five portal subfolders of `13-testing/` (portal partition — `22-glossary/core/naming-conventions.md` §1):
holds **shared, platform-wide material for this domain (not specific to a single portal)** for this domain. Cross-portal registries, gateways and index
files stay at the domain root; shared material lives in `core/`.

## Contents

| File | document_id | Title |
|---|---|---|
| [README.md](README.md) | DOC-TST-007 | This portal index — purpose, file table |
| [TC-001.md](TC-001.md) | DOC-TC-001 | TC-001 — Registration with a valid phone dispatches a 5-minute OTP |
| [TC-002.md](TC-002.md) | DOC-TC-002 | TC-002 — Correct OTP verification activates the account and issues a session |
| [TC-003.md](TC-003.md) | DOC-TC-003 | TC-003 — Wrong-OTP attempts, expiry, resend cooldown and resend limit |
| [TC-004.md](TC-004.md) | DOC-TC-004 | TC-004 — Login issues a 15-minute access token and a 7-day refresh token |
| [TC-005.md](TC-005.md) | DOC-TC-005 | TC-005 — Five consecutive failed logins lock the account for 15 minutes |
| [TC-006.md](TC-006.md) | DOC-TC-006 | TC-006 — Refresh rotation is single-use and reuse revokes the session family |
| [TC-007.md](TC-007.md) | DOC-TC-007 | TC-007 — Sixth device login succeeds by evicting the oldest of five sessions |
| [TC-008.md](TC-008.md) | DOC-TC-008 | TC-008 — Authenticated password change invalidates every existing session |
| [TC-009.md](TC-009.md) | DOC-TC-009 | TC-009 — Password reset via OTP revokes all sessions and forbids reuse |
| [TC-010.md](TC-010.md) | DOC-TC-010 | TC-010 — Logout revokes one session; logout-all revokes every session |
| [TC-011.md](TC-011.md) | DOC-TC-011 | TC-011 — Cross-user access to another customer's order or address is denied |
| [TC-012.md](TC-012.md) | DOC-TC-012 | TC-012 — Vendor A cannot read or mutate vendor B's product or sub-order |
| [TC-013.md](TC-013.md) | DOC-TC-013 | TC-013 — Privilege escalation attempts by Moderator, Customer and vendor staff are refused |
| [TC-014.md](TC-014.md) | DOC-TC-014 | TC-014 — Direct API bypass with forged tokens or tampered clients is denied server-side |
| [TC-015.md](TC-015.md) | DOC-TC-015 | TC-015 — Publishing a product requires an Arabic name and complete catalog data |
| [TC-016.md](TC-016.md) | DOC-TC-016 | TC-016 — Image upload security limits and the publish/unpublish lifecycle |
| [TC-017.md](TC-017.md) | DOC-TC-017 | TC-017 — Category structure preserves unique names within a parent |
| [TC-018.md](TC-018.md) | DOC-TC-018 | TC-018 — Checkout reserves stock atomically and the 15-minute TTL releases it |
| [TC-019.md](TC-019.md) | DOC-TC-019 | TC-019 — Inventory mutations validate stock and reject writes below reservations |
| [TC-020.md](TC-020.md) | DOC-TC-020 | TC-020 — Concurrent checkout never oversells the last unit of a product |
| [TC-021.md](TC-021.md) | DOC-TC-021 | TC-021 — Review eligibility: only the purchaser after DELIVERED, within 30 days, once per item |
| [TC-022.md](TC-022.md) | DOC-TC-022 | TC-022 — Moderation hide/restore excludes a review from ratings and every response is audited |
| [TC-023.md](TC-023.md) | DOC-TC-023 | TC-023 — Vendor application creates one PENDING_KYC store and publishing stays blocked until approval |
| [TC-024.md](TC-024.md) | DOC-TC-024 | TC-024 — KYC decisions: reject with reason, resubmit restarts the 48-hour SLA, approval unlocks publishing |
| [TC-025.md](TC-025.md) | DOC-TC-025 | TC-025 — Store configuration: commission is read-only, zones must be domestic, suspension locks writes |
| [TC-026.md](TC-026.md) | DOC-TC-026 | TC-026 — Staff role matrix is enforced by the Owner, and followers receive new-product notifications |
| [TC-027.md](TC-027.md) | DOC-TC-027 | TC-027 — Arabic search normalization matches variant forms and never returns inactive products |
| [TC-028.md](TC-028.md) | DOC-TC-028 | TC-028 — Filter/sort results stay consistent with facet counts, and search degradation falls back to category browse |
| [TC-029.md](TC-029.md) | DOC-TC-029 | TC-029 — Cart guard ladder rejects the 6th vendor, 11th unit and 51st product without partial mutation |
| [TC-030.md](TC-030.md) | DOC-TC-030 | TC-030 — Reservation expiry, price changes and ineligible items block checkout; guest cart merges with server value winning |
| [TC-031.md](TC-031.md) | DOC-TC-031 | TC-031 — Wallet checkout happy path: debit, escrow funding and PLACED order with visible VAT math |
| [TC-032.md](TC-032.md) | DOC-TC-032 | TC-032 — Insufficient balance and non-wallet payment method create no order and no ledger entry |
| [TC-033.md](TC-033.md) | DOC-TC-033 | TC-033 — Order total boundaries 499 / 500 / 5,000,000 / 5,000,001 YER enforced at confirmation |
| [TC-034.md](TC-034.md) | DOC-TC-034 | TC-034 — VAT math: 15 % on (subtotal − discount), shipping untaxed, half-up rounding and master sum |
| [TC-035.md](TC-035.md) | DOC-TC-035 | TC-035 — m-Floos top-up credits exactly once on a verified callback; replayed callback is a no-op |
| [TC-036.md](TC-036.md) | DOC-TC-036 | TC-036 — Bank-transfer top-up stays PENDING until admin verification, then credits once; rejection posts nothing |
| [TC-037.md](TC-037.md) | DOC-TC-037 | TC-037 — Top-up amount boundaries 999 / 1,000 / 5,000,000 / 5,000,001 YER rejected before any provider call |
| [TC-038.md](TC-038.md) | DOC-TC-038 | TC-038 — Wallet ledger is append-only: UPDATE/DELETE rejected, corrections are compensating entries |
| [TC-039.md](TC-039.md) | DOC-TC-039 | TC-039 — Coupon math at checkout plus stacking, expiry, over-usage and under-minimum rejections |
| [TC-040.md](TC-040.md) | DOC-TC-040 | TC-040 — Multi-vendor checkout splits into one master and three sub-orders with per-vendor totals |
| [TC-041.md](TC-041.md) | DOC-TC-041 | TC-041 — Stock reservation TTL expiry during checkout blocks the order and never funds escrow |
| [TC-042.md](TC-042.md) | DOC-TC-042 | TC-042 — Concurrent checkout race on the last unit: one winner, clean loser, zero oversell, zero orphan hold |
| [TC-043.md](TC-043.md) | DOC-TC-043 | TC-043 — Full lifecycle walk PLACED → COMPLETED with one immutable history row per transition |
| [TC-044.md](TC-044.md) | DOC-TC-044 | TC-044 — Vendor cancellation at CONFIRMED moves the sub-order to CANCELLED and starts the refund path |
| [TC-045.md](TC-045.md) | DOC-TC-045 | TC-045 — Customer cancellation at PLACED inside the window → CANCELLED → REFUNDED with wallet credit |
| [TC-046.md](TC-046.md) | DOC-TC-046 | TC-046 — Cancellation attempts at/after READY_FOR_PICKUP are refused with 409 CANCEL_WINDOW_CLOSED |
| [TC-047.md](TC-047.md) | DOC-TC-047 | TC-047 — Invalid transitions (PLACED → DELIVERED and other forbidden moves) return 409 STATE_CONFLICT |
| [TC-048.md](TC-048.md) | DOC-TC-048 | TC-048 — 24-hour vendor SLA breach raises an escalation alert and queue flag but never auto-cancels |
| [TC-049.md](TC-049.md) | DOC-TC-049 | TC-049 — Master completes only when every sub-order settles; a dispute blocks only its own sub-order |
| [TC-050.md](TC-050.md) | DOC-TC-050 | TC-050 — Order status history is append-only: no mutation API, no in-place row rewrites |
| [TC-051.md](TC-051.md) | DOC-TC-051 | TC-051 — Customer order status and timeline API shape per state with correct visibility scoping |
| [TC-052.md](TC-052.md) | DOC-TC-052 | TC-052 — Vendor force-actions on a DELIVERED order are denied with no state, money or history change |
| [TC-053.md](TC-053.md) | DOC-TC-053 | TC-053 — Admin force-cancel at PROCESSING writes an append-only audit entry; Moderator is refused |
| [TC-054.md](TC-054.md) | DOC-TC-054 | TC-054 — Saga failure after wallet capture: compensating release, idempotent retry, single net charge |
| [TC-055.md](TC-055.md) | DOC-TC-055 | TC-055 — BR-ORD-10 escalation timing boundary: silent at 23:59, fires exactly once at 24:00 |
| [TC-056.md](TC-056.md) | DOC-TC-056 | TC-056 — DISPUTED opened before COMPLETED freezes escrow and blocks the 7-day release |
| [TC-057.md](TC-057.md) | DOC-TC-057 | TC-057 — Escrow funded at PLACED on wallet payment |
| [TC-058.md](TC-058.md) | DOC-TC-058 | TC-058 — Escrow releases exactly once 7 days after DELIVERED |
| [TC-059.md](TC-059.md) | DOC-TC-059 | TC-059 — Commission base excludes VAT and shipping at release |
| [TC-060.md](TC-060.md) | DOC-TC-060 | TC-060 — Commission tier change applies to the next escrow release only |
| [TC-061.md](TC-061.md) | DOC-TC-061 | TC-061 — An open dispute freezes escrow until admin ar0itration |
| [TC-062.md](TC-062.md) | DOC-TC-062 | TC-062 — An in-window return suppresses escrow release until it settles |
| [TC-063.md](TC-063.md) | DOC-TC-063 | TC-063 — Payouts honor the 1,000 YER floor, idempotency and the 3–7 0usiness-day window |
| [TC-064.md](TC-064.md) | DOC-TC-064 | TC-064 — Daily reconciliation proves the ledger 0alances and flags mismatch without silent fixes |
| [TC-065.md](TC-065.md) | DOC-TC-065 | TC-065 — Available job list shows only same-zone offers with zone-priced fees |
| [TC-066.md](TC-066.md) | DOC-TC-066 | TC-066 — First accept wins the delivery assignment; the losing courier gets 409 |
| [TC-067.md](TC-067.md) | DOC-TC-067 | TC-067 — Courier release returns the assignment to READY_FOR_PICKUP |
| [TC-068.md](TC-068.md) | DOC-TC-068 | TC-068 — Pickup → transit → out-for-delivery issues the 6-digit code to the buyer |
| [TC-069.md](TC-069.md) | DOC-TC-069 | TC-069 — Correct 6-digit code delivers the sub-order and starts the 7-day escrow hold |
| [TC-070.md](TC-070.md) | DOC-TC-070 | TC-070 — First two wrong code entries report remaining attempts without delivering |
| [TC-071.md](TC-071.md) | DOC-TC-071 | TC-071 — Third wrong code locks confirmation for 24 hours and auto-creates a support ticket |
| [TC-072.md](TC-072.md) | DOC-TC-072 | TC-072 — Three courier-recorded failed attempts escalate to admin review |
| [TC-073.md](TC-073.md) | DOC-TC-073 | TC-073 — Shipping contract and data store contain no GPS/location coordinates |
| [TC-074.md](TC-074.md) | DOC-TC-074 | TC-074 — Return request accepted inside the window (day 0, deadline instant, and 14-day policy from COMPLETED) |
| [TC-075.md](TC-075.md) | DOC-TC-075 | TC-075 — Return request rejections: elapsed window, non-returnable, wrong state, open dispute, duplicate |
| [TC-076.md](TC-076.md) | DOC-TC-076 | TC-076 — Vendor decides a return inside the 48-hour SLA: approve schedules pickup, reject requires a reason |
| [TC-077.md](TC-077.md) | DOC-TC-077 | TC-077 — Undecided return past 48 hours auto-escalates to the admin queue and the admin decision is audited |
| [TC-078.md](TC-078.md) | DOC-TC-078 | TC-078 — Inspection PASS moves RETURN_RECEIVED to REFUNDED; FAIL routes to admin review as DISPUTED |
| [TC-079.md](TC-079.md) | DOC-TC-079 | TC-079 — Uninspected return auto-approves after 72 hours and a late inspection is refused |
| [TC-080.md](TC-080.md) | DOC-TC-080 | TC-080 — Refund composition, wallet credit within 3 business days, and idempotent execution |
| [TC-081.md](TC-081.md) | DOC-TC-081 | TC-081 — Opening a dispute freezes only the affected sub-order's escrow |
| [TC-082.md](TC-082.md) | DOC-TC-082 | TC-082 — Admin resolves a dispute for the buyer: escrow unfreezes into the audited refund flow |
| [TC-083.md](TC-083.md) | DOC-TC-083 | TC-083 — Admin resolves a dispute for the vendor: sub-order completes and escrow releases once |
| [TC-084.md](TC-084.md) | DOC-TC-084 | TC-084 — Notification channel set is locked to SMS/WhatsApp/in-app/push with no email anywhere |
| [TC-085.md](TC-085.md) | DOC-TC-085 | TC-085 — Security notifications survive a fully opted-out user while optional categories stay silent |
| [TC-086.md](TC-086.md) | DOC-TC-086 | TC-086 — OTP delivery fails over from SMS to WhatsApp within the request window |
| [TC-087.md](TC-087.md) | DOC-TC-087 | TC-087 — Templates follow the user locale (Arabic default) and deep links stay server-generated |
| [TC-088.md](TC-088.md) | DOC-TC-088 | TC-088 — Marketing opt-out silences only the chosen channel and category |
| [TC-089.md](TC-089.md) | DOC-TC-089 | TC-089 — In-app inbox pagination, read-state idempotency, owner scoping and device tokens |
| [TC-090.md](TC-090.md) | DOC-TC-090 | TC-090 — Vendor dashboard shows exact own-store metrics and never another store's |
| [TC-091.md](TC-091.md) | DOC-TC-091 | TC-091 — Store report families paginate, reconcile to totals and reject unknown families |
| [TC-092.md](TC-092.md) | DOC-TC-092 | TC-092 — CSV exports carry BOM, formula-injection guards, the row cap and role gates |
| [TC-093.md](TC-093.md) | DOC-TC-093 | TC-093 — Monthly statement arithmetic ties to the ledger and reports payout rollovers |
| [TC-094.md](TC-094.md) | DOC-TC-094 | TC-094 — Admin dashboard aggregates the platform with role-scoped access |
| [TC-095.md](TC-095.md) | DOC-TC-095 | TC-095 — Admin report families and daily reconciliation expose mismatches to admins only |
| [TC-096.md](TC-096.md) | DOC-TC-096 | TC-096 — CMS page lifecycle: draft, atomic publish, duplicate slug and archive |
| [TC-097.md](TC-097.md) | DOC-TC-097 | TC-097 — Content admin APIs enforce Moderator read-only and Admin-only writes |
| [TC-098.md](TC-098.md) | DOC-TC-098 | TC-098 — Banners honour targeting, schedule windows and the home surface |
| [TC-099.md](TC-099.md) | DOC-TC-099 | TC-099 — Public home and promotions payloads are cached, localized and privacy-aware |
| [TC-100.md](TC-100.md) | DOC-TC-100 | TC-100 — Server-side coupon validation computes discounts and rejects every invalid issue |
| [TC-101.md](TC-101.md) | DOC-TC-101 | TC-101 — Coupon creation enforces bounds, uniqueness, idempotency and immutability |
| [TC-102.md](TC-102.md) | DOC-TC-102 | TC-102 — Coupon disable flow and store-coupon scoping behave as documented |
| [TC-103.md](TC-103.md) | DOC-TC-103 | TC-103 — Public page rendering is bilingual and cached; admin page list filters and pages through drafts |
| [TC-104.md](TC-104.md) | DOC-TC-104 | TC-104 — Coupon redemption at order creation computes type-specific discounts, enforces limits and books exactly one redemption row |
| [TC-105.md](TC-105.md) | DOC-TC-105 | TC-105 — Audit rows are append-only: application role cannot UPDATE/DELETE and the API refuses every write |
| [TC-106.md](TC-106.md) | DOC-TC-106 | TC-106 — Manual alteration or deletion of an audit row fails the chain verification and raises an alert |
| [TC-107.md](TC-107.md) | DOC-TC-107 | TC-107 — Every privileged and money action leaves exactly one complete audit row — zero gaps |
| [TC-108.md](TC-108.md) | DOC-TC-108 | TC-108 — Money-action audit rows older than the hot window stay queryable and exportable for at least 5 years |
| [TC-109.md](TC-109.md) | DOC-TC-109 | TC-109 — Privileged and money actions record actor, action, entity, before/after, IP and timestamp — denials included |
| [TC-110.md](TC-110.md) | DOC-TC-110 | TC-110 — Platform settings take effect per documented precedence and role changes apply immediately, audited |
| [TC-111.md](TC-111.md) | DOC-TC-111 | TC-111 — Third failed delivery-code attempt locks confirmation and surfaces an AUTO ticket with the full timeline in the support console |
| [TC-112.md](TC-112.md) | DOC-TC-112 | TC-112 — An open dispute freezes escrow release for the affected sub-order and the admin resolution is written exactly once to the audit log |
| [TC-113.md](TC-113.md) | DOC-TC-113 | TC-113 — Health gating: /healthz ignores dependencies, /readyz gates on required checks and degrades without failing |
| [TC-114.md](TC-114.md) | DOC-TC-114 | TC-114 — Admin surface is deny-by-default: low-privilege tokens are refused server-side, failures are audited, nothing persists |
| [constraint-tests.md](constraint-tests.md) | DOC-TST-004 | Constraint Tests — Canonical Register TST-CON-01 … TST-CON-26 |
| [test-data-and-environments.md](test-data-and-environments.md) | DOC-TST-005 | Test Data & Environments |
| [test-plans.md](test-plans.md) | DOC-TST-003 | Test Plans — Executable Verification Plans |
| [testing-strategy.md](testing-strategy.md) | DOC-TST-002 | Testing Strategy — Verification Methodology (Methodology §47) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-30 | Initial portal-folder index (118 file(s)) | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` |
| 1.1 | 2026-10-02 | Reference paths updated for the section-grouping migration | Session-013 owner directive (prompt-013 clarification) — section-grouping migration |
