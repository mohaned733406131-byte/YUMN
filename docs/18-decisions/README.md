---
document_id: DOC-DEC-001
title: Decisions Domain Overview (ADR Governance)
category: 18-decisions
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-016, NFR-018]
related_documents: [DOC-ARCH-010, DOC-ARCH-009, DOC-ROOT-001, DOC-RSK-001]
---

# Decisions Domain — Overview (DOC-DEC-001)

## 1. Purpose

This domain is the **single home of decisions** for yumn (root README §4): the decision log, and the full Architecture Decision Records under `ADR/`. It is deliberately separate from `04-architecture/architecture-decisions-reference.md` (DOC-ARCH-010), which **reserves the numbering and states rationale summaries only** — per that document, decision *texts* live here and nowhere else. DOC-ARCH-010 §1 records that ADR-002 and ADR-004 are canon-locked (cited by `C-21` and `C-22`).

**Status at v1.0:** the ten reserved ADRs (ADR-001…ADR-010) are written, reviewed, and `ACCEPTED` (2026-09-26), all authored in the analysis phase before implementation exists. Their decisions bind implementation; their compliance sections are the checklist that `13-testing/` constraint tests and `20-validation/` audits verify against.

## 2. ADR Lifecycle

| Status | Meaning | Allowed transitions |
|---|---|---|
| `RESERVED` | Number + title parked in DOC-ARCH-010 §1; file not yet written | → `PROPOSED` when drafting starts |
| `PROPOSED` | ADR written, under review | → `ACCEPTED` / `REJECTED` / → `RESERVED` (withdrawn) |
| `ACCEPTED` | Approved and binding on implementation | → `SUPERSEDED` by a newer ADR |
| `SUPERSEDED` | Replaced; file kept with a pointer to the replacement | terminal |
| `REJECTED` | Considered and declined; kept so the option is not re-litigated | terminal |

Lifecycle rules (mirrors DOC-ARCH-010 §7):

1. Draft `ADR/ADR-NNN.md` using a **reserved** number from DOC-ARCH-010 §1 (or the next free number ≥ 011 for new decisions).
2. Review checks: constraint compliance (`C-01…C-26`), at least three alternatives with rejection reasons, consequences incl. linked `RISK-*`, and the list of documents to update.
3. Acceptance flips the status **in both** the ADR and DOC-ARCH-010 §1; both records bump version with a Change History row (root README §9 — no silent changes).
4. Every document impacted by the decision is listed in the ADR's compliance/related sections and propagated; the change set is recorded in `../20-validation/core/consistency-audit.md`.
5. Consistency is re-audited afterwards: **an ADR loses to a constraint** — if they conflict, the constraint wins and the ADR must be superseded (DOC-ARCH-010 §6).

## 3. Numbering Rules

1. **ADR numbers are stable and never reused.** A superseded ADR keeps its file and number; the replacement takes the **next free number** and references the old one (`supersedes` in its header).
2. **`ADR-002` and `ADR-004` are canon-locked** — their numbers are cited in `00-project-overview/project-constraints.md`; any rewrite must keep those numbers.
3. **`ADR-001…ADR-010` are reserved titles** (DOC-ARCH-010 §1); no other decision may take them. This domain has now written all ten, matching those titles exactly.
4. **Future decisions start at `ADR-011`** (candidates: DOC-ARCH-010 §4 and §"Reserved for future ADRs" in `decision-log.md`).
5. Filename convention: `ADR/ADR-NNN.md`, zero-padded three digits; `document_id: DOC-ADR-NNN`; primary identifier is the content (filename exception in root README §5 does not apply — these are kebab-case-free by convention because the ID *is* the filename stem).

## 4. Decisions Without an ADR

Not every decision warrants a full record. Small, domain-level decisions are captured **inline in `decision-log.md` §2** ("Decisions Without ADR") with: ID (`D-NN`), title, rationale, and where the decision is defined (the source-of-truth document). Examples already in canon: integer YER money representation, Arabic-Indic numeral display, no email channel in v1, the 48-hour return-approval SLA, the cursor-vs-offset pagination split, the no-MFA-in-v1 stance, the single human support hub, and the UUID v7 / singular `snake_case` database conventions.

**Promotion rule:** an inline decision that (a) shapes architecture or (b) conflicts with a future change must be promoted to a full ADR (taking the next free number ≥ 011) and its inline entry then points to the ADR. Conversely, a constraint-backed decision (`C-01…C-26`) is never re-decided here — constraints outrank ADRs.

## 5. File Index

| # | File | Document ID | Content |
|---|---|---|---|
| 1 | `README.md` | DOC-DEC-001 | This overview: lifecycle, numbering, index |
| 2 | `decision-log.md` | DOC-DEC-002 | Chronological log of ADR-001…ADR-010, inline decisions `D-01…D-10`, future ADR candidates |
| 3 | `core/ADR-001.md` | DOC-ADR-001 | PostgreSQL 16 as the sole relational database |
| 4 | `core/ADR-002.md` | DOC-ADR-002 | Modular monolith instead of microservices |
| 5 | `core/ADR-003.md` | DOC-ADR-003 | NestJS 10 as the backend framework |
| 6 | `core/ADR-004.md` | DOC-ADR-004 | Docker Compose deployment; no Kubernetes in v1 |
| 7 | `core/ADR-005.md` | DOC-ADR-005 | Redis 7 + BullMQ as the only queue/cache substrate |
| 8 | `core/ADR-006.md` | DOC-ADR-006 | Elasticsearch 8 for search & discovery |
| 9 | `core/ADR-007.md` | DOC-ADR-007 | MinIO for object storage |
| 10 | `core/ADR-008.md` | DOC-ADR-008 | React Native 0.73 + Next.js 14 for all client surfaces |
| 11 | `core/ADR-009.md` | DOC-ADR-009 | Wallet-only payments with provider adapters |
| 12 | `core/ADR-010.md` | DOC-ADR-010 | Phone + OTP authentication with short-lived JWTs |

## 6. Required Sections of Every ADR (enforced checklist)

Header (`# ADR-NNN: <reserved title>`) → **Status table** (Status, Date, Deciders, Consulted, Informed) → **Context** (forces, constraints, requirements, quality attributes, neighbouring ADRs/dependencies) → **Decision** (unambiguous) → **Alternatives Considered** (table: option · pros · cons · why rejected — minimum three) → **Consequences** (positive · negative · neutral · introduced risks with `RISK-*` links) → **Compliance** (table of every driving `C-NN` + how satisfied; `C-18` in every ADR) → **Related IDs** → **Change History**. This merges DOC-ARCH-010 §8 with this domain's format; an ADR missing any section fails review.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
