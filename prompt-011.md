# prompt-011 — Session 011 Prompt (owner directive: full system expansion — 400+ UCs, portal-partitioned docs across 23 folders)

> **AI ASSISTANT: this is the session-numbered prompt for session 011 — read it first, then
> `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md` (confirm `senior-rules/VERSION` pin per
> `GEN-08` — **2.2.0**). Resume point: `session_track.md` session 010 → 011.
> Both gates must end green: `python senior-rules/validators/validate.py .` and
> `python tools/check_citations.py`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)
> State handoff detail (registers, gotchas, honesty rules): `prompt-next.md` — this file adds the
> session-011 work directive on top of it.**

---

## 1. The directive (owner instruction, received 2026-09-30, start of session 011)

> "Expand and develop the system by scaling up its boundaries, requirements, rules, constraints,
> and processes—as well as all aspects of the analysis—to maximize its utility. Aim for a system
> of significant scope, featuring over 400 use cases, comprehensive business rules, detailed
> requirements, and thorough analysis components. Act as the project owner and manager to ensure
> the system is optimized and fully comprehensive. Begin by proposing modifications, additional
> use cases, and new requirements; then, evaluate and implement these additions. Incorporate
> shared structures or gateway components into the appropriate locations within the analysis
> documentation (spanning 23 folders). Everything related to a specific section or portal is
> placed in its own dedicated folder. For example, the `01-business-analysis` folder contains five
> subfolders—`core`, `admin`, `vendor`, `customer`, and `delivery`—with each subfolder holding all
> the business analysis materials relevant to that specific area. This structure applies to all
> subsequent folders and sections, up to `23-templates`, with a focus on parallel workflows,
> rules, and skills."

**How to treat it (honesty first — `GEN-03`/`DOD-10`/`SPE-03`):**

- It is an **owner requirement to expand the whole analysis and restructure the docs tree**, and
  it is binding work. Record it as an owner directive in the session file and the change-control
  rows — **not** as an independently verified finding. The "over 400" figure is **owner-supplied**
  (`INSUFFICIENT EVIDENCE` until your own inventory/matrix supports it); if your derivation lands
  at a different number, publish the derived number **and** the owner target, side by side, and
  say which is which (session-010 "over 350" precedent — never blend the numbers).
- **Order of work is mandated by the directive itself:** (a) *propose* modifications, additional
  UCs, and new requirements → (b) *evaluate* each proposal against the rule system → (c)
  *implement* what survives evaluation. The proposal + evaluation are artifacts of this session
  (authored, versioned, change-controlled), not internal monologue.
- **Do not fabricate content.** Every new UC must be derived from documents that already exist:
  the 68-ID requirement registry (`FR` 20 / `NFR` 20 / `SEC-REQ` 12 / `DATA-REQ` 8 / `INT-REQ` 8),
  the 104 `BR-*` rules, the 221-endpoint API register, 114 `TC-*`, 12 workflows `WF-*`, frontend
  routes/screens, state machines, `plan-develop.md` `M-*`/`P-*`, `describ.md`, constraint tests.
  New rules/requirements (BR/FR deltas) likewise need a source document or an explicit owner
  approval recorded in the proposal — otherwise they stay on a PENDING list (`AUD-04`/`SPE-03`
  territory; "approval ≠ evidence" — see `prompt-next.md` §6).
- **Structure directive = a physical migration with change-control consequences.** Every folder
  `01-…` … `23-templates` gains five portal subfolders (`core`, `admin`, `vendor`, `customer`,
  `delivery`); portal-specific material moves into its portal folder; shared/platform-wide
  material goes to `core/`; cross-portal gateways (indexes, registries, the section `README.md`)
  stay at the folder root. Working interpretation (confirm in the proposal, phase 2):
  - "23 folders" = `docs/01-business-analysis` … `docs/23-templates` (23 of the 24 numbered
    domains; `00-project-overview`, `phases/`, `sessions/` are section-level/overview and are not
    portal-partitioned — state this explicitly in the proposal).
  - For `01-business-analysis` the example is literal: the folder ends up with **five**
    subfolders — `use-cases/` (210 files) and `workflows/` (13 files) are partitioned into the
    portal folders, the UC index (`DOC-UC-000`) and `business-rules.md` are shared/gateway
    structures placed per the proposal.
  - **Change control FIRST** (path scheme registered in `22-glossary/naming-conventions.md` +
    version bump + CH row before any file moves), then scripted migration, then the citation
    gate (`tools/check_citations.py`) proves every rewritten path resolves — 0 problems is the
    acceptance bar. Never move a file without updating every citing path in the same change set.
- "Focus on parallel workflows, rules, and skills" = use **parallel subagent waves with strictly
  disjoint file sets** for authoring/migration (session-010 precedent, `prompt-next.md` §5), and
  keep `BR-*` rules, `YUMN_RULES.md`, and workflow docs aligned with the portal split.
- No gate moves: Gate 0 stays `FAIL` (`CRIT-01`, `ASM-14`, `DEP-05/06/10`); nothing becomes
  `VERIFIED`; sponsor-owned items (`REC-11…13`, `M-01/04/05/06`, `SEC-001…015`) are surfaced, not
  dispositioned by the assistant.

## 2. State at handoff (verified 2026-09-30, session 011 startup)

- Session **010 CLOSED** (branch `session-010`: `c1f280d`, `6b0bba4`, `fc242c0`, `451d55d`,
  `8f89ef3`, `cbda26a`); `main` untouched at `c9ff07c` by directive. Session file:
  [`docs/sessions/session-010-uc-coverage-expansion.md`](docs/sessions/session-010-uc-coverage-expansion.md).
  Session 011 runs on branch **`session-011`** (created at startup; `main` stays off-limits).
- **Baseline gates green at startup:** validator `RESULT: PASS — structure healthy` (77 + 94 rule
  IDs, 0 broken links); citation check `RESULT: PASS — 669 files, 21,751 ID citations, 0
  problems`. Working tree clean except untracked `prompt-010.md` (committed `cbda26a`) and this
  file.
- **Current truth (do not contradict — `prompt-next.md` §2):** **210 UCs** derived (`UC-001…210`,
  index `DOC-UC-000` v1.2, 18-item PENDING backlog, next free ID **`UC-211`**); **65 open
  findings** (13 consistency + 21 contradiction + 11 gap + 7 hallucination + 6 critical + 7
  requirement-validation; `analysis-validation.md` **v1.13**); `consistency-audit.md` **v1.20**
  (31-check sweep **20/2/9**, the 9 FAILs mapped to findings 6/7/8/11/14/15/16/21/22); BR
  **104/15 domains**; constraints **`C-01…C-26`**; requirements **68 IDs**; TC **114**; API
  **221**; rules **ADMR 2.2.0 + 94**; `plan-develop.md` **v1.2 APPROVED** (≠ implemented);
  `TD-01…10` all `PAID`; assistant-side `REC`s all `PAID`.
- **Still open regardless of this directive:** citation-CI run **UNVERIFIED** (open the GitHub
  Actions UI for `docs-citations.yml`, record what it actually says); `SEC-001…015` all open;
  `origin/master` deletion pending default-branch switch; Gate 0 `FAIL`.

## 3. Resume point

- `session_track.md` row 010 → **session 011**; handoff queue in `prompt-next.md` §3:
  (A) sponsor dispositions — surface only; (B) UC backlog toward the owner target — **absorbed
  and superseded by §1** (target now "over 400", not "over 350"); (C) verify the pushed CI
  honestly; (D) work the 9 FAIL checks via their owning findings; (E) bootstrap only after
  Gate 0 evidence exists (it does not — stays `FAIL`).
- This directive adds the **structure migration** (new work, no queue predecessor) and the
  **proposal → evaluate → implement** cycle on top of queue B.

## 4. Work plan (phases — both gates green after every change set)

1. **Startup:** read ENTRY + RULES_HINTS (VERSION pin 2.2.0), run both gates (done: PASS/PASS),
   branch `session-011` (done), then this file.
2. **Proposal (directive: begin here — no writes to existing docs yet):** author the session
   proposal artifact (new file under `docs/00-project-overview/`, registered DOC ID, frontmatter
   + CH per root README §7/§9) with: (a) boundary/scope modifications, (b) the full additional-UC
   list (ID, title, actor, portal, block, FR/BR refs, priority, **source document** per UC) from
   `UC-211` to the target (≥ 401 files; plan allocation e.g. `UC-211…UC-420`, registered BEFORE
   minting), (c) proposed new requirements (FR/… deltas) and new business rules, (d) proposed
   constraint/process/rule changes (`C-NN` via root README §9; `YUMN_RULES.md` only via `core/00`
   §0.5 — likely "propose, defer"), (e) the target folder structure for `01…23` with a per-folder
   placement table (root / `core/` / portal) and migration cost (files moved × citing paths).
3. **Evaluation (in the same artifact):** for every proposal row — accept / reject / defer with
   the governing rule cited (`SPE-03`, `D-02`, `AUD-04`, `SEC-*`, precedence rules); rejected or
   unsourced items go to an explicit PENDING list, never to silence; owner targets stay marked
   `INSUFFICIENT EVIDENCE` until derived.
4. **Change control BEFORE minting IDs or moving files:** `naming-conventions.md` (UC allocation
   210 → target, next `UC-211`; **new folder-path scheme row**), `terminology.md`,
   `use-case-template.md` (file location), root README §5/§9 if ID series/constraints changed —
   session-008 BR 99→104 precedent: version bump + CH row + repo-wide grep for the old count/path.
5. **Structure migration:** create the five portal subfolders in `01…23`; partition existing
   files per the approved placement table (scripted move + scripted path rewrite across the
   corpus); then `python tools/check_citations.py` → **0 problems** is the acceptance gate.
   Do it folder-group by folder-group, gates after each group.
6. **UC minting (parallel waves):** `UC-211…` in subagent waves with **strictly disjoint file
   sets** (one portal/folder group per agent, report-don't-commit, orchestrator re-verifies
   counts/IDs/spot-reads — session-010 QC rule), template v1.2 verbatim, only existing/
   newly-registered `BR-*`/`FR-*`, files land in their portal folder. Gates after each wave.
7. **New requirements / rules (only what phase 3 accepted):** register in
   `02-requirements/requirements-overview.md` / `01-business-analysis/business-rules.md`
   (+ FR files/BR sections), then grep every count consumer (`prompt-next.md` §5 last bullet)
   and re-sync in the same change set.
8. **Registration / propagation (no omissions):** index rows + §2 count + §3 actor totals + §5
   coverage matrix + §5.1 backlog rework; `19-traceability` ×3 (Matrix B, dashboards);
   `phases/analysis/use-cases.md` inventory; `analysis-validation.md` domain rows + roll-up;
   `consistency-audit.md` §4 propagation row + affected `CHK-*` re-runs; proposal/disposition
   rows in the relevant registers (`CT`/`GAP`/`HAL` as applicable).
9. **Full gates:** 31-check sweep (rebuild the session-local script per session-009/010 pattern),
   validator, citation check, `gitleaks dir` + `gitleaks git` — all green or honestly reported.
10. **Session close:** session file `docs/sessions/session-011-*.md` (DOC-SES-011), `sessions/README`
    row, `session_track.md` row 011 + log + resume → 012, `memory.md` snapshot (defects changed?),
    `prompt-next.md` → 012 **and** `prompt-012.md` placeholder, grouped conventional commits on
    branch **`session-011`** only, push (`main` untouched).

## 5. Commands

```text
python senior-rules/validators/validate.py .     # must end PASS; run after EVERY change set
python tools/check_citations.py                  # must end PASS (0 problems); migration safety net
gitleaks dir E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner   # expect exit 0
gitleaks git  E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner   # expect exit 0
# UC inventory (paths change with the migration — expect 400+, contiguous, no gaps):
Get-ChildItem docs\01-business-analysis -Recurse -Filter 'UC-*.md'
# old-count / old-path grep after any count or move (exclude 20-/21- CH rows — only history may remain):
#   Select-String over docs for "210 use cases", "use-cases/UC-", "01-business-analysis"
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -10
```

## 6. Rules and gotchas in force

- Everything in `prompt-next.md` §5 (PowerShell traps: alias-named functions deleting files,
  backticks in PS strings/here-strings, BOM handling, exact-string/em-dash matching, CRLF,
  depth-≥3 globs, frontmatter parsed only from the YAML block, disjoint subagent file sets,
  under-done propagation) and §6 (honesty rules) applies unchanged.
- Counts move in pairs: index header `## 2. Use Case Index (210 use cases)` is hard-coded; grep
  `210` repo-wide after the expansion (session-010 did the same for `42`).
- CHK-05 (`## Change History` everywhere) and CHK-01 (all 11 frontmatter keys) are `PASS` today —
  every touched/new file must carry both or they regress; findings are never deleted when closed.
- AC IDs: `AC-UCnnn-nn` are UC-scoped and must not collide with the 253-row AC registry; new
  requirement ACs follow the registry series rules.
- Constraint amendments only via root README §9; rule text only via `core/00` §0.5 (bump VERSION
  + CHANGELOG); factual prose corrections don't move the pin (session 005/008 precedent).
- No dates/effort/sprints until `ASM-14` baselines exist; approval ≠ evidence; pushed ≠ running;
  coverage claims require the matrix.
- **Only push `session-011`** — `main` (and `session-010`) are off-limits for new work by directive.
