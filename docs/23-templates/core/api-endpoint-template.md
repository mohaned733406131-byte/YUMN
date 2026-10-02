---
document_id: DOC-TPL-006
title: API Endpoint Group Template (endpoints/<group>.md)
category: 23-templates
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-013]
related_documents: [DOC-TPL-001, DOC-API-002, DOC-API-003, DOC-API-004, DOC-API-005, DOC-GL-003]
---

# API Endpoint Group Template (DOC-TPL-006)

**When to use:** a new group file in `07-api/<group>.md`. **Authority: DOC-API-005 (group index + allocation), `../../07-api/core/api-conventions.md` (naming, roles, headers), `../../07-api/core/error-model.md` (closed error catalog), `../../07-api/core/pagination.md`** — mirror them exactly; disagreements are logged in `../../20-validation/core/contradiction-audit.md`. Exemplar: `../../07-api/core/wallet.md` (API-WAL).

## Rules

- **Group code** `API-<GRP>` comes from the DOC-API-005 allocation (14 groups: `ATH USR VND CAT SRC CRT ORD WAL SHP RET NTF CNT ANL ADM`); a genuinely new group is minted in DOC-API-005 first, never inside the file.
- **Endpoint IDs** are `API-<GRP>-NNN`, zero-padded, next free number in the group; never renumber, never reuse (DOC-GL-003 §3).
- Paths: `/api/v1` base, lowercase plural kebab-case resources, ownership prefixes `/store/…` (vendor) and `/admin/…` (admin), max 2 nesting levels, nouns in paths with actions as method or terminal POST segment (api-conventions §2).
- Roles are drawn only from the closed set `CUSTOMER VENDOR COURIER ADMIN SUPER_ADMIN MODERATOR` + `SYSTEM` (internal); every row states role **and** ownership scope.
- Errors come only from the `error-model.md` §4 catalog (`409 IDEMPOTENCY_CONFLICT`, `VALIDATION_ERROR`, …) — never coin a code in an endpoint row.
- Money fields are integer YER, JSON keys camelCase, timestamps ISO-8601 UTC ending `At` (DOC-GL-003 §6); responses are `Cache-Control: no-store` unless a documented exception exists.
- Money/state-changing POSTs declare `Idempotency-Key` mandatory (`BR-PLT-03`); list endpoints declare cursor vs offset per DOC-API-004; rate-limited endpoints cite the tier (`SEC-REQ-009`).
- Filled group files carry `source_of_truth: false`; `related_requirements` lists every FR/NFR/SEC-REQ/DATA-REQ/INT-REQ **and** `BR-*` the group exercises.

## Template

```text
---
document_id: DOC-API-<nnn>
title: API-<GRP> — <Group name> (<FR-nnn, …>)
category: 07-api
status: approved
version: 1.0
created: <date>
updated: <date>
author: analysis-agent
source_of_truth: false
related_requirements: [<fr-nfr-sec-req-ids>, <br-ids>]
related_documents: [DOC-API-002, DOC-API-003, DOC-API-004, DOC-API-005, DOC-BA-005]
---

# API-<GRP> — <Group name>

**Group:** `API-<GRP>` · <FR-ids the group implements> · **Endpoints:** `API-<GRP>-001…<nnn>` · **Base:** `/api/v1`

<One paragraph of hard scope rules: the money/state/limits guarantees this group makes, each with its governing IDs; then the exclusions ("no X exists anywhere in this group" with the forbidding constraint ID).>

---

## 1. Endpoint Table

| ID | Method & Path | Roles | Purpose | Key request → response | Key errors | Related IDs |
|---|---|---|---|---|---|---|
| API-<GRP>-001 | `GET /<resource>` | `<ROLE>` (<scope>) | <what one call achieves> | → `200 { <exact key fields with shapes/enums> }` | `<ERROR_CODE>` | <FR-*, BR-*, C-*> |
| API-<GRP>-002 | `POST /<resource>` | `<ROLE>` | <purpose — **requires `Idempotency-Key`** if money/state-changing> | `{ <exact request fields> }` → `201 { <exact response fields> }` | `<ERROR_CODE>`, `<ERROR_CODE>` | <FR-*, AC-*, BR-*> |

## 2. Behavior Notes

- **<Lifecycle/flow>** (<INT-REQ-*>, <BR-*>): <how the endpoint fits the end-to-end behaviour — callbacks, sagas, jobs — in 1–3 sentences with IDs.>
- **<Invariant enforcement>** (<BR-*>): <what the server guarantees, and the exact error code on violation (AC linkage).>
- **<Authorization/ownership rule>** (<role>, <RBAC IDs>): <who may call and how ownership is checked.>

## 3. Pagination / Idempotency / Caching

| Endpoint(s) | Mode |
|---|---|
| `API-<GRP>-002` | cursor (exact totals) / offset / single resource |

<Mandatory idempotency-key list with its BR citation; caching statement (`Cache-Control: no-store` unless documented otherwise).>

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | <date> | Initial version | Initial analysis |
```

## Pre-Submission Checklist

1. Group code exists in DOC-API-005; endpoint IDs are the next free `API-<GRP>-NNN`; no endpoint defined outside this group's file.
2. Every path/method/role/header follows `api-conventions.md`; every error code exists in `error-model.md` §4 — grep before writing.
3. Money/state-changing POSTs declare `Idempotency-Key`; list endpoints state cursor/offset; no invented pagination or caching modes.
4. Every ID cited (FR/BR/C/AC/INT-REQ/SEC-REQ) exists in canon; no coined terms (DOC-GL-002); no leftover `<…>` placeholders.
5. Frontmatter complete with `category: 07-api`, `source_of_truth: false`, `related_requirements` covering both directions; version + Change History row on any edit (root README §9).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
