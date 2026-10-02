# prompt-012 — Session 012 Prompt (directive: complete session-011 phases 8–10 — registration close-out, full gates, session close)

> **AI ASSISTANT: this is the session-numbered prompt for the sitting that FINISHES session-011.
> Read it first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md` (confirm
> `senior-rules/VERSION` pin per `GEN-08` — **2.2.0**), then `prompt-011.md` (the 10-phase plan —
> phases 1–7 are done, phases 8–10 are this file) and `prompt-next.md` (handoff state, gotchas,
> honesty rules). Resume point: in-flight **session-011**, phases 8–10 outstanding.
> Both gates must end green: `python senior-rules/validators/validate.py .` and
> `python tools/check_citations.py`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)
> Provenance: authored 2026-10-02 per owner instruction, *before* session-011 close (the
> placeholder said it would be written at close, `prompt-011.md` §4 phase 10 — recorded here as a
> deliberate deviation, `prompt-011.md`'s citation of this file stays valid).**

---

## 1. Directive

Finish session-011 exactly as scoped by `prompt-011.md` §4 — **phases 8, 9 and 10 only**:

- **Phase 8** — complete the registration/propagation set started at snapshot `c78490b`
  (same-change-set discipline, no omissions).
- **Phase 9** — full gates: 31-check sweep over the grown corpus, validator, citation check,
  gitleaks, honest CI verification.
- **Phase 10** — session close: session file, trackers, memory, resume → 012, grouped
  conventional commits, push **`session-011` only**.

**Out of scope for this sitting — surface, never start, never edit:**

- The new owner inputs `YUMN_Prompt.md` + `YUMN_Requirment.md` (SaaS-transformation blueprint
  v1.0, 2026-09-30) are a **new owner directive that has not been evaluated**. Record their
  presence in the session file and queue them for session 012; do NOT begin the SaaS
  conversion, do NOT modify the files, do NOT silently waive their dangling citations
  (disposition path: §3 phase 9c).
- No new UCs, BRs, FRs or deltas beyond what `DOC-OVR-012` already accepted (all minted in
  phases 6–7). Gate 0 stays `FAIL`; sponsor items (`REC-11…13`, `M-01/04/05/06`,
  `SEC-001…015`, `ASM-14`, `DEP-05/06/10`) are surfaced, never dispositioned.

## 2. State at handoff (verified 2026-10-02, this sitting)

### 2.1 Git

- Branch **`session-011`** at `c78490b`, ahead 12 of `origin/session-011`; `main` untouched at
  `c9ff07c` (off-limits by directive). Remote: `https://github.com/mohaned733406131-byte/YUMN.git`.
- Session-011 commits so far: `7d11410` (prompt-011 + this placeholder), `4ce70ee` (phase 2
  proposal `DOC-OVR-012`), `d7f42be` (phase 4 change control), `4bffdd2`…`c02ab91` (phase 5
  portal-partition migration groups 1–5 — **583 files moved, complete**), `9f2a916` (phase 5
  completion: 115 portal-folder READMEs + 36 stale-reference fixes), `bae2344` + `fddb10a`
  (phase 6: `UC-211…420` minted in parallel waves A/B — **420 on disk**), `851c05e` (phase 7:
  12 accepted deltas → 73 requirements / 111 BR / 273 AC), `c78490b` (phase 8 WIP snapshot).

### 2.2 Phase-8 WIP — what the snapshot `c78490b` already contains vs what is still pending

**Done at snapshot:** UC index `DOC-UC-000` **v1.3** (+420 rows), `19-traceability` ×3
(`README` + `requirements-to-features` + `requirements-to-tests`), `phases/analysis/use-cases.md`
(+241 lines), `analysis-validation` **v1.14**, disposition rows touched in
`contradiction-audit` / `hallucination-audit` / `critical-findings` / `requirements-validation`,
`naming-conventions` **v1.9**, `terminology`, `use-case-template`, stale-range fixes
(`06-backend/README.md`, `11-ui-ux/core/user-flows.md`), factual count lines in
`RULES_HINTS.md` §4 / `YUMN_RULES.md` §intro.

**Pending — verify each item, then close it:**

1. `consistency-audit.md` **§4 propagation rows** — the file was NOT touched by the snapshot and
   sits at **v1.20 (2026-09-29)**; add the phase-5…8 propagation rows and re-run every `CHK-*`
   whose evidence moved (corpus, counts, paths).
2. **Completeness pass:** walk the `DOC-OVR-012` evaluation table row by row against the
   registers — every accepted row must have its registration, every deferred row its explicit
   PENDING disposition (`CT`/`GAP`/`HAL` as applicable). Nothing may exist only in the proposal.
3. Index rework for 420: §2 header count, §3 actor totals, §5 coverage matrix, §5.1 PENDING
   backlog wording (the 18-item backlog still describes the 210 scope).
4. **Stale-count/path grep:** `210` repo-wide (also `42`, old `use-cases/UC-` path shorthand,
   `01-business-analysis/use-cases`), excluding `## Change History` / evidence rows — fix every
   live hit in the same change set (session-008/010 precedent; `prompt-011.md` §6).

### 2.3 Current truth (do not contradict — `prompt-next.md` §2)

- Counts: **420 UC** (`UC-001…420`; allocation + next free **`UC-421`**, `naming-conventions`
  v1.9 §3 — re-verify the row at startup) · **73 requirements** (20 FR / 20 NFR / 16 SEC-REQ /
  9 DATA-REQ / 8 INT-REQ) · **111 BR** across 15 domains · **273 registry AC** (+779 UC-scoped
  `AC-UCnnn-nn`) · 114 TC · 221 API endpoints · 18 DB entities · `ADR-001…010` · rules
  **ADMR 2.2.0** + **YUMN_RULES 94**.
- Roll-up: **65 open findings** (13 consistency + 21 contradiction + 11 gap + 7 hallucination +
  6 critical + 7 requirement-validation) — no finding status changed in session-011;
  `analysis-validation.md` v1.14 re-synced domain rows only. Findings are never deleted when
  closed (flip status + date).
- Gate 0 = **FAIL** (`CRIT-01`, `ASM-14`, `DEP-05/06/10`); `SEC-001…015` all open; nothing in
  `docs/` is `VERIFIED`; citation-CI GitHub run remains **UNVERIFIED** (open the Actions UI for
  `docs-citations.yml` and record what it actually says — never claim PASS from this machine).
- `plan-develop.md` v1.3 APPROVED ≠ implemented; `TD-01…10` all `PAID`; assistant-side `REC`s
  all `PAID`; `origin/master` deletion still pending the default-branch switch (needs owner click).

### 2.4 Working tree (untracked — do not `git add` without owner instruction)

- `YUMN_Prompt.md`, `YUMN_Requirment.md` — owner files (§1 out-of-scope).
- `delegate-skills-master/`, `pro-skills-senior-full-stack-software-engineer-master/` — skill
  packs; **link repairs applied 2026-10-02** (§2.5), kept untracked as found.

### 2.5 Gate states (skill-pack repair performed this sitting — re-run both at startup to confirm)

- **Validator:** was `FAIL — 9 findings`, all inside the two skill packs (core rules/docs
  passed: 77 + 94 rule IDs unique, 0 forbidden UI calls). Repaired: 4 issue-template links in
  `delegate-skills-master/CONTRIBUTING.md` prefixed `.github/` (files exist there), and the
  missing MIT `LICENSE` file added at each pack root (5 README/publish links resolve).
  → evidence (re-run 2026-10-02): `RESULT: PASS — structure healthy` (0 broken links;
  77 + 94 rule IDs unique) — paste the raw output into the session file at close.
- **Citation check:** was `FAIL — 65 dangling paths` = 51 illustrative artifact filenames inside
  the skill packs (e.g. `` `01-TODO.md` `` — files the skills *instruct agents to create*; never
  real repo citations) + 14 from `YUMN_Prompt.md`. Repaired: the two packs added to
  `SCAN_SKIP_DIRS` in `tools/check_citations.py` — a **documented scope correction** using the
  checker's own vendor precedent (`senior-rules/` is excluded from scanning while still counting
  as a resolution target). Not a gate weakening: the scanned corpus is the project documentation;
  vendor reference packs were never part of it.
  → evidence (re-run 2026-10-02): `1003 files scanned; 27330 ID citations; 0 unresolved ID(s);
  14 dangling path(s)` — **65 → 14**, every skill-pack path gone; remaining = **14, all
  `YUMN_Prompt.md`** = open disposition, §3 phase 9c.
- **31-check sweep + gitleaks:** not yet run for session-011 (phase 9).

## 3. Work plan — phases 8 → 9 → 10 (both gates green after every change set)

### Phase 8 — finish registration/propagation

Work the §2.2 pending list 1–4 in order; every edited doc gets a version bump + `## Change
History` row + a propagation row in `consistency-audit.md` §4. Run both gates after each change
set, not at the end. If any part is delegated (`GEN-05`): give the subagent a declared ID/role,
a **strictly disjoint file set**, report-don't-commit, then **re-verify every claim yourself**
(counts, IDs, spot-reads — session-010/011 QC rule; trust no report you have not re-run).

### Phase 9 — full gates (evidence, not assertions)

a. Rebuild the session-local 31-check sweep script (pattern documented in session-009/010
   files; any temp copy in `C:\Users\Mohanned\AppData\Local\Temp\opencode\` is not a repo
   artifact) and run it over the full corpus — file counts grew, so record the fresh verdict and
   re-map the 9 known FAILs (findings 6, 7, 8, 11, 14, 15, 16, 21, 22) before flipping anything.
b. `python senior-rules/validators/validate.py .` → must print `RESULT: PASS — structure healthy`.
c. `python tools/check_citations.py` → the 14 `YUMN_Prompt.md` paths must be **dispositioned,
   not waived**: (i) register the exact (file, token) pairs in `PHANTOM_PATHS` with written
   justification (precedent: session files quoting dead paths *as evidence*), or (ii) surface to
   the owner for a move/edit decision. Record the choice in the session file. If still red,
   report it red (`DOD-10`) — never hide a gate, never claim PASS from memory.
d. `gitleaks dir` + `gitleaks git` with `.gitleaks.toml` → exit 0; report as *triaged allowlist
   (2 benign test fixtures)*, never as "0 findings".
e. UC inventory: `Get-ChildItem docs -Recurse -Filter 'UC-*.md'` → 420 files, contiguous, no gaps.
f. Honest CI verification (`prompt-next.md` §3C): open the GitHub Actions UI for
   `docs-citations.yml`, record the run's actual result (PASS/FAIL/UNVERIFIED).

### Phase 10 — session close

- `docs/sessions/session-011-*.md` (DOC-SES-011): work performed, raw gate outputs as evidence
  blocks, the skill-pack link repair + checker scope correction recorded as a change set, the
  commit table, status honesty (DOD-10), and a resume prompt.
- `docs/sessions/README.md` row 011; `session_track.md` **row 011 `CLOSED`** + session log +
  resume → **012** (per `prompt-011.md` §4 phase 10 — this sitting closes session-011);
  `memory.md` snapshot (defects changed?); `prompt-next.md` → 012 (state handoff — keep it
  consistent with this file, which is now consumed).
- Grouped conventional commits carrying governing IDs, push **`session-011` only**; `main`
  untouched. Commit messages state exactly what the diff proves — the citation result includes
  the 14-path disposition outcome, whatever it is.

## 4. Commands

```text
python senior-rules/validators/validate.py .     # must end PASS; run after EVERY change set
python tools/check_citations.py                  # 0 problems, or the 14 YUMN_Prompt.md paths dispositioned (§3 phase 9c)
gitleaks dir E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner   # expect exit 0
gitleaks git  E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner   # expect exit 0
Get-ChildItem docs -Recurse -Filter 'UC-*.md'    # expect 420, contiguous (paths changed in the migration)
# stale-count sweep after any count/path change (exclude CH/evidence rows):
#   Get-ChildItem docs -Recurse -Filter *.md | Select-String -Pattern '210'
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -14
git status --short --branch
```

## 5. Rules and gotchas in force

- Everything in `prompt-011.md` §6 and `prompt-next.md` §5 (PowerShell traps: alias-named
  functions deleting files, here-string backticks, BOM handling, exact-string/em-dash matching,
  depth-≥3 globs, disjoint subagent file sets, under-done propagation) and §6 (honesty rules)
  applies unchanged.
- **New this sitting:** skill packs stay untracked — do not `git add` them without owner
  instruction; owner files `YUMN_*.md` are read-only until dispositioned; the
  `check_citations.py` change is a documented vendor-scope correction (record it — never
  describe it as "the gate was always green").
- Counts move in pairs: after any count/registry/path change, grep the old value repo-wide
  (excluding CH/evidence rows) and re-run both gates before calling the set done.
- CHK-05 (CH everywhere) and CHK-01 (11-key frontmatter) are PASS today — every touched or new
  file must carry both or they regress.
- No dates/effort/sprints until `ASM-14` baselines exist; approval ≠ evidence; pushed ≠ running;
  coverage claims require the index §5 matrix.

## 6. Resume point

`session_track.md` row 010 → in-flight **session-011**, phases 8–10 outstanding = **this file**.
On close: row 011 `CLOSED`, resume → **session 012**, whose first queue item is the owner
SaaS-blueprint directive (`YUMN_Prompt.md` + `YUMN_Requirment.md` disposition, then evaluation).
