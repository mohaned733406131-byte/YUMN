# prompt-010 — Session 010 Prompt (owner directive: full use-case coverage, 350+ UCs)

> **AI ASSISTANT: this is the session-numbered prompt for session 010 — read it first, then
> `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md` (confirm `senior-rules/VERSION` pin per
> `GEN-08` — **2.2.0**). Resume point: `session_track.md` session 010.
> Both gates must end green: `python senior-rules/validators/validate.py .` and
> `python tools/check_citations.py`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)
> State handoff detail (registers, gotchas, honesty rules): `prompt-next.md` — this file adds the
> session-010 work directive on top of it.**

---

## 1. The directive (owner instruction, received 2026-09-29, start of session 010)

> "An analysis … revealed that over 350 use cases across the four portals are required … Although
> only 40 use cases are currently documented, create all the missing use cases to ensure the
> system covers every scenario for all portals. Furthermore, update the project analysis,
> requirements, and all related documentation to fully accommodate these workflows without any
> omissions."

**How to treat it (honesty first — `GEN-03`/`DOD-10`/`SPE-03`):**

- It is an **owner requirement to expand UC coverage**, and it is binding work. Record it as an
  owner directive in the session file and the change-control rows — **not** as an independently
  verified finding. The "over 350" figure is **owner-supplied** (`INSUFFICIENT EVIDENCE` until
  your own coverage matrix supports it); if your derivation lands at a different number, publish
  the derived number **and** the owner target, and say which is which.
- **Do not fabricate scenarios.** Every UC must be derived from documents that already exist:
  the 68-requirement registry, the 104 `BR-*` rules, the 221-endpoint API register, frontend
  screens/routes, workflows, `plan-develop.md` `M-*`/`P-*` items, `describ.md`, constraint tests.
  A UC with no source document behind it is a hallucination (`AUD-04` territory).
- **Completeness is proven, not asserted:** deliver a coverage matrix (portal × feature area → UC
  IDs) so "covers every scenario" is checkable. No zero-gap claim without the matrix
  (`AUD-01`/`D-02` precedent).
- No gate moves. Gate 0 stays `FAIL` (`CRIT-01`); nothing becomes `VERIFIED`.

## 2. State at handoff (verified 2026-09-29, session 010 startup)

- Session 009 **CLOSED** and pushed (branch `session-009`: `ae2ae01`, `d492ae3`, `f303c54`,
  `c139266`); `main` untouched at `c9ff07c`. Session file:
  [`docs/sessions/session-009-pre-gate-hygiene.md`](docs/sessions/session-009-pre-gate-hygiene.md).
- **Baseline gates green at startup:** validator `RESULT: PASS — structure healthy` (77 + 94 rule
  IDs); citation check `RESULT: PASS — 498 files, 18,875 ID citations, 0 problems`.
- **No use-case work has started yet** — the directive arrived before any UC edit. Working tree
  clean; branch `session-009` checked out (create **`session-010`** before committing).
- Current roll-up: **65 open findings** (13/21/11/7/6/7, `analysis-validation.md` v1.11); secret
  scan PASS (gitleaks 8.30.1 + `.gitleaks.toml`); citation-CI run **UNVERIFIED**.

## 3. Facts already gathered (do not re-derive)

- **Use cases today: 42 files** (`UC-001…UC-042.md`; the directive's "40" predates `UC-041`/`UC-042`
  added in session 007). Index/template: `docs/01-business-analysis/use-case-index.md`
  (**DOC-UC-000, v1.1**) — §1 is the binding UC template (9 body sections, 45–70 lines/file),
  §2 is the index titled **"Use Case Index (42 use cases)"** (hard-coded count — must be re-synced),
  and the ID rules (sequential `UC-NNN`, `DOC-UC-NNN` mirrors, no reuse/renumbering, one primary
  actor from the canonical 7, only **existing** `BR-*`/`FR-*` IDs, API touchpoints conceptual).
- **Four portals** = the four surface families of `05-frontend/README.md` (DOC-FE-001 §1 — "four
  surface families, five client applications"): **S1 Customer web, S4 Customer mobile** (one
  portal, two clients), **S2 Vendor panel**, **S3 Admin console** (Admin/Super Admin/Moderator),
  **S5 Courier app**. Actors: 7 (`DOC-OVR-007`), portals map to ACT-01/02/04-06/03; ACT-07 System
  UCs (jobs/engines) belong to the system, not a portal.
- **Requirement registry:** 68 IDs — `FR` 20 (files `02-requirements/functional/FR-001…020.md`),
  `NFR` 20, `SEC-REQ` 12, `DATA-REQ` 8, `INT-REQ` 8 (`02-requirements/requirements-overview.md`).
- Other source inventory: `BR-*` 104/15 domains, `API-*` 221 (14 endpoint groups),
  `DB-*` 18 entities, `TC-*` 114, workflows `WF-*` 12, plan `M-01…M-25`/`P-01…P-20`
  (`plan-develop.md` v1.2), `describ.md` §1–§8, constraint tests `TST-CON-*` 26.
- Count consumers that hard-code **42 UC** (session-008/009 precedent — grep `42` repo-wide
  before declaring the set done): `docs/01-business-analysis/use-case-index.md` §2 header, `analysis-validation.md`
  domain-01 row (63 files / 42 UC), `19-traceability/README.md` §5 dashboard, `requirements-to-features.md`
  `T-03` evidence, `phases/analysis/use-cases.md` (42-file roll-up), `memory.md` §3-era counts,
  `all_in_one_track.md`.

## 4. Work plan (phases — gates green after every change set)

1. **Discovery / gap analysis (no writes yet):** read ENTRY + RULES_HINTS (startup), then build
   the portal × feature-area matrix from the source inventory in §3 — for each area, list which
   UCs exist and which scenarios have none. Sources: FR registry, `07-api` endpoint register
   (14 groups), `docs/05-frontend/core/routing.md` routes/screens, `03-system-analysis` workflows/state
   machines, `plan-develop.md`, `describ.md`, `13-testing` coverage. Output: the target UC list
   (ID, title, primary actor, portal, block `B01…B06`, FR refs, priority, source document).
2. **Change control before minting IDs:** UC-series allocation grows 42 → target (root README §5
   ID-series row, `22-glossary/naming-conventions.md` §3 allocation, index header/§2 count) —
   follow the session-008 `BR` 99→104 precedent exactly (version bump + CH row + repo-wide grep
   for the old number). New UCs start at **UC-043**; never touch UC-001…042 content except where
   a real inconsistency is found (then its own CH row).
3. **Authoring:** one file per UC in `01-business-analysis/use-cases/UC-NNN.md`, template §1
   verbatim (frontmatter keys incl. `related_requirements`/`related_documents`, 9 sections,
   `AC-UCnnn-01/02/03…`). Batch by portal; each batch → run both gates before the next. Only
   existing `BR-*`/`FR-*` (and other registered) IDs; conceptual API paths only.
4. **Registration / propagation (no omissions):** README index rows for every new UC;
   `requirements-to-features.md` UC column; `requirements-to-tests.md`/test coverage pointers;
   `phases/analysis/use-cases.md` roll-up; `19-traceability/README.md` §5 dashboard;
   `analysis-validation.md` domain row + roll-up; `docs/20-validation/core/consistency-audit.md` §4
   propagation row + re-run the affected checks (`CHK-01`, `CHK-05`, `CHK-06`, `CHK-08`,
   `CHK-11`, `CHK-15`, `CHK-27`) — full 31-check sweep if counts/registries moved.
5. **Coverage proof:** publish the matrix (portal × area → UC IDs, gaps explicitly listed as
   `PENDING`/backlog with reasons) — this is the evidence for "covers every scenario".
6. **Session close:** session file `docs/sessions/session-010-*.md` (DOC-SES-010), registry row,
   `session_track.md` row 010 + resume → 011, `memory.md` snapshot, `prompt-next.md` → 011 **and**
   `prompt-011.md`; grouped commits on branch **`session-010`** only, push (`main` untouched).

## 5. Commands

```text
python senior-rules/validators/validate.py .     # must end PASS; run after EVERY change set
python tools/check_citations.py                  # must end PASS — it rejects invented IDs/paths
gitleaks dir E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner   # expect exit 0
# UC inventory:  Get-ChildItem docs\01-business-analysis\use-cases -Filter 'UC-*.md'
# old-count grep: Select-String over docs (exclude 20-/21- CH rows) for "42 use cases|42 UC|UC 42"
git log --oneline -10
```

## 6. Rules and gotchas in force

- Everything in `prompt-next.md` §5 (PowerShell traps: backticks in PS strings, alias-named
  functions deleting files, BOM handling, exact-string matching) and §6 (honesty rules) applies
  unchanged.
- UC file gotchas: index count "42 use cases" is hard-coded in at least the index §2 header;
  frontmatter must carry **all** keys (CHK-01/CHK-05); each new file needs `## Change History`
  (CHK-05 is now `PASS` 485/485 — do not regress it); `AC-UCnnn-*` IDs must not collide with the
  253-row AC registry (`AC-UCnnn-nn` series is UC-scoped — 127 exist today).
- Findings never deleted when closed; register flips carry dates; roll-up totals recomputed from
  the registers, never hand-waved.
- **Only push `session-010`** — `main` is off-limits by directive.
