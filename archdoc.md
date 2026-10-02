# archdoc — Analysis Documentation Structure Specification

| Field | Value |
|---|---|
| Document | `archdoc.md` (repository root) |
| Status | **RECONSTRUCTED** — content authored 2026-09-28 (session 008, `REC-01`/`TD-03`) |
| Provenance (honest) | The file existed as a **0-byte placeholder whose content never existed in git history** (defect `D-10`, finding `HAL-03`). This specification was **reconstructed from the structure as actually implemented and validated** by [`docs/README.md`](docs/README.md) §2–§5 and `docs/20-validation/core/consistency-audit.md`. It did **not** precede the knowledge base — it records it. The earlier claim that an original copy was archived under `archive/` is unverifiable: `archive/` does not exist in this repository (`SPE-03`). |
| Authority split | This file owns the **structure contract**: the domain list, the per-file metadata contract, and the navigation rules. [`docs/README.md`](docs/README.md) remains the operational index: domain map with per-domain source-of-truth columns (§2), reading order (§3), source-of-truth table (§4), ID series (§5), change control (§9), quality gate (§11). **Where the two disagree, `docs/README.md` wins** until reconciled here under root README §9 change control. |

---

## 1. Domain structure — 24 numbered analysis domains

The knowledge base under `docs/` consists of **exactly 24 analysis domains**, numbered `00`–`23`.
Each domain is a directory containing a `README.md` index (the entry point for that domain) and its
documents. The canonical directory names are:

| # | Directory | # | Directory |
|---|---|---|---|
| 00 | `project-overview` | 12 | `non-functional` |
| 01 | `business-analysis` | 13 | `testing` |
| 02 | `requirements` | 14 | `devops-infrastructure` |
| 03 | `system-analysis` | 15 | `deployment` |
| 04 | `architecture` | 16 | `data` |
| 05 | `frontend` | 17 | `risk-management` |
| 06 | `backend` | 18 | `decisions` |
| 07 | `api` | 19 | `traceability` |
| 08 | `database` | 20 | `validation` |
| 09 | `security` | 21 | `completion` |
| 10 | `integrations` | 22 | `glossary` |
| 11 | `ui-ux` | 23 | `templates` |

This list is the structural contract only (names + numbers). **What each domain contains and which
document is authoritative for which concept** lives in `docs/README.md` §2 and §4 — that table is
the authority; this list must track it, never lead it.

**Process folders (not domains):** `docs/phases/` (per-phase artifact sets, `DOC-PHA-*`) and
`docs/sessions/` (session work files, `DOC-SES-*`). They are registered in `docs/README.md` §2 so no
document is an orphan (`SPE-05`).

## 2. Per-file metadata contract

Every document under `docs/` carries:

1. **YAML frontmatter with exactly the 11 keys** — `document_id`, `title`, `category`, `status`,
   `version`, `created`, `updated`, `author`, `source_of_truth`, `related_requirements`,
   `related_documents` (enforced by `validate.py` + `docs/20-validation/core/consistency-audit.md` `CHK-01`;
   the literal `^related_requirements:` example inside code fences in root README §9.2 must not be
   counted as a key occurrence).
2. **`status` vocabulary** as defined in `22-glossary/core/naming-conventions.md` (never invent ad-hoc
   status words; `VERIFIED` is reserved for implementation evidence — analysis documents are
   `draft`/`approved` only, see `SPE-03`).
3. **A `## Change History` section** with a `| Version | Date | Change | Reason |` table; every edit
   bumps `version:` and appends a row in the same change (root README §9.2; `CHK-05`).
4. **One `document_id` per file**, unique across the corpus, minted by the owning domain's register
   (`DOC-<CAT>-NNN`; codes in `22-glossary/core/naming-conventions.md`).

Root-level entry files (`session_track.md`, `memory.md`, `mind_map.md`, `architecture.md`,
`development_phases_entry.md`, `all_in_one_track.md`, this file) are exempt from frontmatter and are
validated by `validate.py`'s entry-file checks instead.

## 3. Source-of-truth and cross-referencing

- **One authoritative document per concept**; everywhere else **reference the ID — never copy the
  definition** (`SPE-01`; authority table in `docs/README.md` §4).
- **Never cite an ID absent from its owning register** (`SPE-05`/root README §11 `D-3`): the ID
  series and their allocating registers are listed in root README §5; mint IDs only in the allocator.
- **Findings are never deleted** when closed — status flips with date and resolution note
  (`DOC-TPL-011` #3).
- **Evidence tags** on every non-obvious claim: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`.

## 4. Navigation rules (human and AI)

1. Start at [`docs/README.md`](docs/README.md); follow its §3 reading order for a full pass.
2. **Read a directory's `README.md` before analyzing that directory** — never assume one directory
   yields complete knowledge; cross-domain claims must be checked against the owning domain.
3. For per-file shape, copy the matching file from `23-templates/` (not a neighbour document).
4. Route new work through the tracker set: `session_track.md` (resume points), `memory.md`
   (durable facts), `prompt-next.md` (next-session handoff), `all_in_one_track.md` (roll-up index).

## 5. Validation of this structure

- Structure validator: `python senior-rules/validators/validate.py .` (entry files, markdown links,
  rule-ID uniqueness, forbidden calls) — must be run after every change set.
- Content audits: the seven registers under `docs/20-validation/` (consistency, contradiction, gap,
  hallucination, critical, requirements-validation, roll-up) — re-run before every gate claim
  (root README §11; `20-validation/README.md` §4 rule 7).
- Gates: `docs/21-completion/core/quality-gates.md` (Gate 0–3) — gates stay `FAIL`/`BLOCKED` until real
  evidence exists (`DOD-10`); approval of analysis artifacts never flips a gate (`GEN-03`).

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-28 | Initial reconstruction of the structure specification: 24-domain contract (names + numbers), per-file metadata contract (11 frontmatter keys, status vocabulary, `## Change History`, `DOC-*` minting), source-of-truth/cross-referencing rules, navigation rules, validation pointers; provenance stated honestly (0-byte history, `archive/` absent) | `REC-01`/`TD-03` pay-down (session 008) — restore the cited structural authority; `HAL-03`/`CRIT-08` closure evidence |
