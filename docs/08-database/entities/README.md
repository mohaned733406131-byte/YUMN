---
document_id: DOC-DB-007
title: Entity Index (DB-001 … DB-018)
category: 08-database
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [DATA-REQ-001, DATA-REQ-008]
related_documents: [DOC-DB-001, DOC-DB-003, DOC-DB-005]
---

# Entity Index (DB-001 … DB-018)

**The ER overview ([DOC-DB-003](../entity-relationship.md)) is the register of the model; this file is the index of entity documents.** Each entity has exactly one file with `entity_id: DB-NNN` in its frontmatter. Entity docs are *not* source-of-truth documents (`source_of_truth: false`) — the register is.

## 1. Index

| entity_id | File | Doc ID | Purpose | Owning module |
|---|---|---|---|---|
| DB-001 | [user.md](user.md) | DOC-DBE-001 | Account: encrypted phone identity, password hash, roles, status, locale, soft-delete/anonymization markers | B01 Identity & Access |
| DB-002 | [address.md](address.md) | DOC-DBE-002 | Delivery addresses (≤10 per user): governorate/district/street, label, default flag, no GPS | B01 Identity & Access |
| DB-003 | [store.md](store.md) | DOC-DBE-003 | Vendor storefront: owner, bilingual name, unique slug, status, KYC record, commission tier, hub text, hours | B03 Store Management |
| DB-004 | [category.md](category.md) | DOC-DBE-004 | Category tree (≤5 levels): bilingual names, per-level unique slug, position, status | B02 Product Catalog |
| DB-005 | [product.md](product.md) | DOC-DBE-005 | Sellable item: Arabic-first naming, YER price, return policy, status, rating denormalization, search-sync flags | B02 Product Catalog |
| DB-006 | [inventory.md](inventory.md) | DOC-DBE-006 | Stock per product: on-hand/reserved/available (generated), 15-min reservation TTL, optimistic-lock version, no-negative CHECK | B02 Product Catalog |
| DB-007 | [cart.md](cart.md) | DOC-DBE-007 | One active cart per logged-in user; item lines in `cart_item`; C-15 guards; merge-on-login rule reference | B05 Cart & Checkout |
| DB-008 | [order.md](order.md) | DOC-DBE-008 | Master order: unique order_no, 17-state enum, money columns (C-14), wallet-only payment, sub-orders, append-only state history | B06 Order Management |
| DB-009 | [payment.md](payment.md) | DOC-DBE-009 | Order/top-up payment intents: state machine, wallet-only for orders, idempotency key, provider references, bank verification | B07 Payment & Wallet |
| DB-010 | [wallet.md](wallet.md) | DOC-DBE-010 | One wallet per user: balance ≥ 0 as ledger cache, currency YER, freeze flag | B07 Payment & Wallet |
| DB-011 | [wallet_transaction.md](wallet_transaction.md) | DOC-DBE-011 | Append-only double-entry ledger: signed amounts, balance_after, references, idempotency, immutability | B07 Payment & Wallet |
| DB-012 | [escrow.md](escrow.md) | DOC-DBE-012 | Per-sub-order hold: funded at PLACED, release_at = DELIVERED + 7 d, HELD/RELEASED/REFUNDED/FROZEN, commission at release | B07 Payment & Wallet |
| DB-013 | [shipment.md](shipment.md) | DOC-DBE-013 | Delivery execution: courier assignment, delivery-state mirror, hashed 6-digit code + attempt lock, zone text, attempt log | B08 Shipping & Delivery |
| DB-014 | [return_request.md](return_request.md) | DOC-DBE-014 | Return lifecycle: window fields (BR-RET-01), 72-h inspection due (BR-RET-05), evidence, refund link | B09 Returns & Refunds |
| DB-015 | [review.md](review.md) | DOC-DBE-015 | Verified-purchase review: rating 1–5, moderation status + hide flag, one per order item | B02 Product Catalog |
| DB-016 | [coupon.md](coupon.md) | DOC-DBE-016 | Coupon definitions: type/value, ≤90-day window, global/per-user usage limits, platform or store scope | B12 Content & CMS |
| DB-017 | [notification.md](notification.md) | DOC-DBE-017 | Outbound message record: 4 channels (no email v1 — GAP-03), template key, payload, dedup key, read state | B10 Notifications |
| DB-018 | [audit_log.md](audit_log.md) | DOC-DBE-018 | Append-only, hash-chained audit of privileged and money actions: actor, action, entity, before/after, IP/UA | B13 Platform Administration |

**Supporting tables** (`sub_order`, `order_item`, `order_status_history`, `cart_item`, `checkout_session`, `stock_reservation`, `user_role`, `session`, `otp_challenge`, `product_image`, `product_variant`, `store_member`, `kyc_document`, `store_follower`, `refund`, `payout`, `shipment_attempt`, `shipment_offer`, `shipping_zone`, `shipping_rate`, `return_item`, `return_evidence`, `review_response`, `coupon_redemption`, `notification_preference`, `banner`, `cms_page`, `dispute`, `support_ticket`, `platform_setting`, `audit_chain`, `governorate`) are specified in [../entity-relationship.md](../entity-relationship.md) and in the relationship sections of their aggregate's entity file. They receive no `DB-NNN` id.

## 2. Conventions for Entity Documents

1. **Frontmatter** — required block (root README §7) plus, on line 2, `entity_id: DB-NNN`; entity docs set `source_of_truth: false`; `related_requirements` and `related_documents` list only real IDs.
2. **Sections, in fixed order:**
   - *Overview & purpose* — what the entity is, which FR/BR/C-IDs it realizes.
   - *Field table* — `Name | Type | Null | Default | Constraints | Notes` with real columns (no placeholders).
   - *Indexes* — mirrors DOC-DB-004 for that table (names must match).
   - *Relationships* — FKs with names, cardinality, ON DELETE (mirrors DOC-DB-003).
   - *Invariants & business rules enforced* — split into **DB-enforced** vs **app-enforced**, with IDs.
   - *Example rows* — 2–3 short, realistic rows (YER amounts, Yemeni phone pattern `^7[0-9]{8}$`, Arabic names).
   - *Change History* — required table.
3. **Naming** — table/column/constraint names exactly as in DOC-DB-001 §1 (singular snake_case, `_yer` money suffix, `timestamptz`).
4. **Money** — every amount is `bigint` whole YER; never floats, never foreign currency (C-04).
5. **Cross-reference, don't copy** — rule text lives in `01-business-analysis/business-rules.md`, states in `03-system-analysis/state-transitions.md`, constraints in `00-project-overview/project-constraints.md`. Entity docs cite IDs.
6. **No contradictions with canon** — where an entity doc interprets a canon tension, it says so explicitly in its *Invariants* section.
7. **Change control** — editing an entity doc bumps `version`, adds a Change History row, and updates the register (DOC-DB-003) and this index if structure changed (root README §9).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
