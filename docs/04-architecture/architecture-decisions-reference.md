---
document_id: DOC-ARCH-010
title: Architecture Decisions Reference (ADR Index)
category: 04-architecture
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-009, NFR-016, NFR-018]
related_documents: [DOC-ARCH-002, DOC-ARCH-009, DOC-OVR-008, DOC-ROOT-001, DOC-REQ-001]
---

# Architecture Decisions Reference (ADR Index)

Index of the architectural decisions that shape yumn, each with a rationale summary and a pointer to its full ADR in `18-decisions/core/`. **This file does not contain decision texts** — it reserves the numbering, records the status, and states which constraint or quality attribute drives each choice. ADRs are authored, approved and superseded only in `18-decisions/` (root README §9).

> **Status note (re-synced 2026-09-28, `REC-02`):** all ten ADR files exist in `18-decisions/core/` and are authored, approved, and binding on implementation. Every status below equals the `status: approved` frontmatter of the corresponding file (`approved` ≡ `ACCEPTED` in the §7 lifecycle vocabulary). Two numbers are canon-locked and must be honored: `C-21` references **`ADR-002`** (modular monolith) and `C-22` references **`ADR-004`** (Docker Compose / no K8s).

## 1. ADR Register (ADR-001 … ADR-010)

| ADR | Title | Status | Rationale summary | Driving IDs | Detailed in |
|---|---|---|---|---|---|
| `ADR-001` | PostgreSQL 16 as the sole relational database | `ACCEPTED` | One ACID store keeps money, stock and order state in a single consistency boundary; JSON flexibility for metadata; mature backup/WAL story meets RPO | `C-19`, `DEP-02`, `NFR-008`, `NFR-006` | `../18-decisions/core/ADR-001.md` |
| `ADR-002` | Modular monolith instead of microservices | `ACCEPTED` — canon-locked by `C-21` | Team size and operability: one deployable, module boundaries enforced by tooling, no distributed transactions; keeps money flows simple | `C-21`, `NFR-009`, `DEP-*` team | `../18-decisions/core/ADR-002.md` |
| `ADR-003` | NestJS 10 as the backend framework | `ACCEPTED` | Module/DI structure mirrors blocks `B01…B13`; guards/pipes support RBAC and validation; full TypeScript fit with web/mobile | `DEP-01`, `C-21`, `NFR-009` | `../18-decisions/core/ADR-003.md` |
| `ADR-004` | Docker Compose deployment; no Kubernetes in v1 | `ACCEPTED` — canon-locked by `C-22` | Single-host topology is sufficient for `C-25`; Compose gives environment parity and low operational burden; containers remain orchestrator-portable | `C-22`, `NFR-016`, `NFR-018` | `../18-decisions/core/ADR-004.md` |
| `ADR-005` | Redis 7 + BullMQ as the only queue/cache substrate | `ACCEPTED` | One dependency covers cache, counters, TTL keys and durable jobs with retries/backoff/DLQ; delayed jobs power all business timers | `C-20`, `DEP-03`, `BR-PLT-01/02`, `NFR-004` | `../18-decisions/core/ADR-005.md` |
| `ADR-006` | Elasticsearch 8 for search & discovery | `ACCEPTED` | Arabic-aware analysis plus facets/aggregations deliver `FR-009` quality that relational FTS cannot at target scale; index is rebuildable so failure degrades gracefully | `DEP-04`, `FR-009`, `NFR-007` | `../18-decisions/core/ADR-006.md` |
| `ADR-007` | MinIO for object storage | `ACCEPTED` | Self-hosted S3-compatible storage avoids cloud lock-in while keeping the S3 API portable; fits Docker Compose deployment | `DEP-07`, `NFR-016`, `C-22` | `../18-decisions/core/ADR-007.md` |
| `ADR-008` | React Native 0.73 + Next.js 14 for all client surfaces | `ACCEPTED` | One language across five surfaces; RN covers customer + courier apps with shared domain vocabulary; Next.js SSR meets `NFR-002` and carries RTL structure | `NFR-002`, `NFR-013`, `NFR-015`, `DEP-12` | `../18-decisions/core/ADR-008.md` |
| `ADR-009` | Wallet-only payments with provider adapters | `ACCEPTED` | Escrow trust model requires pre-funding; excludes cards/BNPL/crypto to avoid regulatory scope; adapters keep providers out of domain code | `C-01…C-05`, `INT-REQ-001/008`, `FR-013` | `../18-decisions/core/ADR-009.md` |
| `ADR-010` | Phone + OTP authentication with short-lived JWTs | `ACCEPTED` | Phone is universal in the market; SMS/WhatsApp OTP covers verification; 15-min/7-day rotating JWTs give stateless scale-out with strong session control | `C-06…C-08`, `SEC-REQ-001/003`, `FR-001` | `../18-decisions/core/ADR-010.md` |

## 2. Numbering Rules

1. **ADR numbers are stable and never reused.** A superseded ADR keeps its file with status `SUPERSEDED`; the replacement takes the next free number and references the old one.
2. **`ADR-002` and `ADR-004` are canon-locked** — their numbering is cited in `00-project-overview/project-constraints.md`; any rewrite must keep those numbers.
3. **The ten numbers above are allocated**: no other decision may take `ADR-001…ADR-010`, so future authors must start at `ADR-011`.
4. Additional future decisions (candidates listed in §4) take `ADR-011` and above.

## 3. Decision → Constraint Coverage Map

| Constraint group | Decisions covering it |
|---|---|
| `C-18` custom build | Implied by all of `ADR-001…ADR-010` (no platform adopted); explicit constraint check in each ADR's compliance section |
| `C-19` PostgreSQL | `ADR-001` |
| `C-20` BullMQ | `ADR-005` |
| `C-21` modular monolith | `ADR-002`, supported by `ADR-003` |
| `C-22` Docker Compose, no K8s | `ADR-004`, `ADR-007` (self-hosted storage), `ADR-008` (client packaging) |
| `C-01…C-05` wallet-only | `ADR-009` |
| `C-06…C-08` auth | `ADR-010` |
| `C-16` no GPS / code confirm | No ADR needed — behavior fixed by canon; noted as a *rejected-option* inside `ADR-008` (no location SDK) |
| `C-24` Arabic-first | `ADR-008` (RTL structure, ES Arabic analysis in `ADR-006`) |
| `C-25` / `C-26` quality | `ADR-002` (stateless monolith scaling), `ADR-004` (restart/health topology), `ADR-005` (durable async) |
| `NFR-016` portability | `ADR-004`, `ADR-007` |

## 4. Candidate Future ADRs (reserved from `ADR-011`)

| Candidate | Trigger to write it |
|---|---|
| Multi-node Elasticsearch / cluster topology | When single-node ES no longer meets `NFR-001` |
| PostgreSQL read-replica topology | When `NFR-018` stage S2 is activated (`scalability.md`) |
| Table partitioning scheme | When `NFR-017` growth thresholds are approached |
| Multi-host deployment / orchestrator | Only if `C-22` is formally changed (v2 scope) |
| CDN vendor / edge strategy beyond `DEP-08` | When edge configuration hardens |
| Push provider strategy (APNs/FCM vs aggregator) | When mobile push is implemented |
| E-mail channel (if `GAP-03` resolves to "include") | Requires scope + `BR-NTF-01` change first |
| Outbox pattern formalization | If enqueue-after-commit races are observed in practice |

## 5. How to Write an ADR (pointer)

Full ADR format (context, decision, alternatives, consequences, compliance with `C-*`, status, supersession) is defined by the templates in `23-templates/` and the decision log in `18-decisions/README.md`. Every ADR must: cite its driving constraints, list alternatives rejected with reasons, state the impact on `04-architecture/` documents that must be updated, and be cross-referenced back from this index with an updated status.

## 6. Consistency Rule

If any document in `04-architecture/` conflicts with an approved ADR, the ADR wins and the conflict is logged in `../20-validation/core/contradiction-audit.md`; if an ADR conflicts with a constraint (`C-01…C-26`), the constraint wins and the ADR must be superseded.

## 7. ADR Status Vocabulary & Lifecycle

| Status | Meaning | Allowed transitions |
|---|---|---|
| `RESERVED` | Number and title parked in this index; file not yet written | → `PROPOSED` when drafting starts |
| `PROPOSED` | ADR written, under review | → `ACCEPTED` / `REJECTED` / → `RESERVED` (withdrawn) |
| `ACCEPTED` | Approved and binding on implementation | → `SUPERSEDED` by a newer ADR |
| `SUPERSEDED` | Replaced; kept for history with pointer to the replacement | terminal |
| `REJECTED` | Considered and declined; kept so the option is not re-litigated | terminal |

Lifecycle rules: (1) an ADR is drafted in `18-decisions/ADR/ADR-NNN.md` using the reserved number from §1; (2) review checks constraint compliance (`C-01…C-26`), alternatives and consequences; (3) acceptance flips the status in both the ADR and this index; (4) any document updated as a consequence is listed inside the ADR's "Documents to update" section; (5) consistency is re-audited in `../20-validation/core/consistency-audit.md`.

## 8. Required Sections of Every ADR (checklist)

| # | Section | Must contain |
|---|---|---|
| 1 | Metadata | ADR number, title, status, date, author, superseded-by/supersedes if any |
| 2 | Context | The problem, the driving `NFR-*`/`SEC-REQ-*`/`INT-REQ-*` and constraints |
| 3 | Decision | The choice, stated unambiguously in one paragraph |
| 4 | Alternatives considered | At least two, with rejection reasons (mirrors `technology-stack.md` §1–6) |
| 5 | Constraint compliance | Explicit check against every applicable `C-*` (e.g. `C-18`, `C-19`, `C-20`, `C-21`, `C-22`) |
| 6 | Consequences | Positive, negative, and risks (linked to `17-risk-management/` if material) |
| 7 | Documents to update | The `04-architecture/`, `06-backend/`, `14-devops-infrastructure/` files affected |
| 8 | Verification | How the decision is enforced/tested (lint rule, dependency audit, deploy config review) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | Stale empty-directory status note removed; `ADR-001…ADR-010` statuses re-synced from `RESERVED` to `ACCEPTED` (verified against each file's `status: approved` frontmatter); §1 retitled "ADR Register"; §2 rule 3 wording aligned | `REC-02` / `TD-02` pay-down — canon-locked citations (`C-21`→`ADR-002`, `C-22`→`ADR-004`) and the §7 lifecycle now match reality (`HAL-02` → `RESOLVED`) |
