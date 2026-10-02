# prompt-next — Session 012 Handoff (queue-only: owner SaaS-blueprint directive first, post-push CI observation, carried FAIL findings)

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08` — now **2.2.0**). Resume point: `session_track.md` session 011 (CLOSED).
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> Citation checker must end green: `python tools/check_citations.py`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-10-03, session 011 CLOSED)

Phases 5–10 executed end to end — close file:
[docs/sessions/session-011-portal-uc420-section-grouping.md](docs/sessions/session-011-portal-uc420-section-grouping.md) (DOC-SES-011, v1.0, raw gate outputs).

- **Phases 5–7 (committed):** portal partition **583 files → `docs/<nn>/<portal>/`** (5 groups, +**115 portal READMEs**,
  36 stale directory refs fixed — commits `4bffdd2`…`9f2a916`); **UC 210 → 420** (`UC-211`…`UC-420` minted from
  `DOC-OVR-012`, waves `bae2344`/`fddb10a`, template-verbatim, existing FR/BR only); accepted deltas →
  **73 requirements / 111 BR / 273 AC** (`851c05e`, proposal scope only) + WIP snapshot `c78490b`.
- **Phase 8 (session-013 owner directive — section-grouping, `command.md` style):** **39 renames** flat → section
  `core/`/family folders; **7 parallel fix agents** (A/B/C/M1/M2/M3/M4; M3 85 files; M2 70 files/81 replacements —
  incident disclosed + recovered byte-provenance from git blobs, agents ran no git) with **orchestrator re-verification
  of every claim** + the moved files' **own outbound links** completed directly (M2's blind spot); 15-file leftover
  sweep; **Wave-D `GAP-15`/`GAP-16` → roll-up 65 → 67** (8 consumers; GAP register 16 issued / 13 open);
  `test-plan` v1.2 (297 = 203/42/47/5); citation scope corrections `f58759b`/`f7762bc`.
- **Phase 9:** fresh 31-check on **986 files → 20/2/9 identical** (no flip, no regression); UC-420 contiguous
  (0 gaps / 0 dupes); AC↔UC **1591 published** (1594 raw − 3 cross-cites); gitleaks dir + git **exit 0**
  (triaged fixtures); CI record `docs-citations` **#1–#13 `failure`**; **phase 9c — 17 pairs registered in
  `PHANTOM_PATHS` (14 owner-surface / 1 deleted-pack / 2 dated-evidence) → citation 0/0**.
- **Phase 10 trackers:** `session_track.md` row 011 `CLOSED` + resume → 012; `sessions/README.md` **v1.8** (row 011);
  session file DOC-SES-011; `memory.md` session-011 snapshot + §3 counts (73/273/111); `consistency-audit` **v1.23**;
  `all_in_one_track.md` (sessions `…011`); this file → 012.

**Last states:** validator `RESULT: PASS — structure healthy` (0 broken links; 77 + 94 rule IDs);
citation `RESULT: PASS — every cited path and ID resolves (REC-15)` — **0 unresolved / 0 dangling** (raw totals in
the session file's evidence block); `gitleaks dir/git` exit 0 (triaged). **Git:** branch **`session-011`**
(`main` untouched — still at `c9ff07c`); history = phases 5–8 `4bffdd2`…`c78490b` + close `53c8127`/`f58759b`/`f7762bc`
+ phase-9/10 grouped commits (governing IDs in each message) — see `git log`; remote `origin` =
`https://github.com/mohaned733406131-byte/YUMN.git`; **push = `session-011` only**. PR #3 open (owner-created);
`origin/master` still GitHub's default branch (deletion pending).

## 2. Current truth (do not contradict)

- **67 open findings**: 13 consistency + 21 contradiction + **13 gap** + 7 hallucination + 6 critical +
  7 requirement-validation (snapshot 2026-10-03; `analysis-validation.md` **v1.15** register of record; Wave-D added
  `GAP-15`/`GAP-16` only — no other finding changed in session 011).
- Register versions: `consistency-audit.md` **v1.23** (**31-check re-run 20/2/9 on the 986-file corpus** — same 9
  `FAIL`s = findings 6, 7, 8, 11, 14, 15, 16, 21, 22; §4 carries the session-011 wave row + phase-9c note),
  `contradiction-audit.md` **v1.9** (21 open), `missing-information.md` **v1.5** (13 open, **16 issued**),
  `hallucination-audit.md` **v1.8** (7 open), `critical-findings.md` **v1.5** (6 open),
  `requirements-validation.md` **v1.1** (7 open), `technical-debt.md` **v1.9** (**all `TD-01…TD-10` `PAID`**),
  `recommendations.md` **v1.10** (**assistant-side all `PAID`** — `REC-01…REC-10`, `REC-14`, `REC-15`;
  `REC-11…REC-13` remain sponsor-owned).
- **Use cases: 420** (`UC-001…UC-420`, **all 420 issued**; next free **`UC-421+`** per `naming-conventions.md` §3);
  index `DOC-UC-000` **v1.3**. Owner "over 350": **derived 420 ≥ 350 by count** — coverage claims only as far as the
  index §5 matrix proves; residual PENDING rows live in the index (re-read it before citing a number).
- **Counts of truth:** 420 UC · 73 requirements · 111 BR (15 domains) · 273 AC (269 + 4 XCUT) · 114 TC ·
  221 endpoints · 18 entities · ADR 10 · traceability matrix 297 rows (203/42/47/5) · rules ADMR **2.2.0** +
  `YUMN_RULES.md` 94 · constraints `C-01…C-26`.
- **The 9 failing checks** and their owning findings: `CHK-12` → finding 6 (`AC-S-04/12/21` absent from registry),
  `CHK-13` → finding 7 (**1591** `AC-UCnnn-nn` outside the 273-row registry — the gap grew because coverage grew;
  evidence re-counted, status untouched), `CHK-14` → finding 8, `CHK-19` → finding 11 (`CT-06…CT-10` enum domains),
  `CHK-22` → finding 14 (`CT-15` canonical-GAP claim sites), `CHK-23` → finding 15 (`CT-16` `seller`/`merchant`
  synonym drift), `CHK-24` → finding 16 (`CT-17` `A-07` claim), `CHK-29` → finding 21 (`GAP-NNN` width in root
  README §5), `CHK-31` → finding 22 (`CT-18`/`CT-19` money-path status sets) + finding 24 (`CT-20`
  `payout_state`). PWF: `CHK-26`/`CHK-27` → finding 19. **Never delete a finding — flip status + date (DOC-TPL-011 #3).**
- **Secret scan = PASS (triaged):** gitleaks 8.30.1 + `.gitleaks.toml`, tree + history exit 0 — record it as
  *triaged* (2 benign `Idempotency-Key` test fixtures) with evidence, never as "0 findings".
- **Citation CI on GitHub = 13/13 `failure` (recorded fact)** — after the session-011 push the new run is
  **UNVERIFIED until seen**. Local parity is green. Open the Actions UI and record what the run actually says
  (never claim PASS from this machine).
- **Phase-9c is a registration, not a waiver:** the 17 pre-close dangling pairs live in
  `tools/check_citations.py` `PHANTOM_PATHS` with per-pair justification (14 owner-surface `YUMN_Prompt.md` /
  1 deleted-pack quote / 2 dated-evidence rows). New danglers get **fixed at source** first; only irreducible
  owner-surface or historical quotes get registered — never silently.
- **Gate 0 = `FAIL`**: `CRIT-01` (`ASM-14` unset) + `DEP-05`/`DEP-06`/`DEP-10` NOT STARTED.
  Nothing in `docs/` is `VERIFIED` — no implementation exists (`SPE-03`).
- `memory.md` §4: D-01/D-03/D-04/D-05/D-09/D-10/D-13/D-14/D-15/D-16 **RESOLVED**; D-02 PARTIAL;
  D-06, D-07, D-08, D-11, D-12 OPEN (D-11 = decision made, ADR deferred by design).
- `SEC-001…015` all open; sponsor/owner items surfaced unchanged (`REC-11`/`REC-12`/`REC-13`,
  `M-01`/`M-04`/`M-05`/`M-06`); `origin/master` deletion pending default-branch switch on GitHub.

## 3. Next work queue (in priority order)

**A. Queue-only rule (`prompt-012.md` §6) — session 012 works the queue, not new scope.** First item: **owner
SaaS-blueprint directive** (`YUMN_Prompt.md` + `YUMN_Requirment.md`) — surface the disposition, then evaluate.
These files are read-only, staged, **never committed**, and their workflow-artifact tokens are the registered
owner-surface phantoms (fix at source is impossible without owner edits).

**B. Push + observe CI honestly:** commit the remaining session-011 phase-9/10 work as grouped conventional commits
(governing IDs; explicit pathspec; never owner files/skill packs), push **`session-011`** only, then record the
actual `docs-citations` run (13 prior failures — never predict PASS; UNVERIFIED until observed).

**C. Work the 9 FAIL checks via their owning findings** (map in section 2): AC reconciliation (findings 6/7/8 —
`CHK-13` evidence now **1591**), enum-domain mapping (11 → `CT-06…CT-10`), canonical-GAP claim sites (14),
glossary `seller`/`merchant` (15), `A-07` claim (16), `GAP-NNN` width (21), money-path status sets +
`payout_state` (22 + 24). Each fix = owning file version bump + CH row + register flip + **re-run the 31-check
sweep** (session-local script pattern is documented in the session-009/010/011 files — rebuild it if gone;
`C:\Users\Mohanned\AppData\Local\Temp\opencode\chk31_v2.py` may still exist but is not a repo artifact)
+ validator + citation check.

**D. Sponsor/finance/security dispositions (surface, never fake):** `REC-11` (`ASM-14` baselines, re-score
`ASM-03`/`ASM-04`/`ASM-12`), `REC-12` (`DEP-05` m-Floos/OneCash sandbox, `DEP-06` SMS/WhatsApp contracts),
`REC-13` (`DEP-10` Central Bank position before any B07 build); plan items `M-01` (`CT-23` + `GAP-14`),
`M-04` (`CT-26` pricing), `M-05` (`CT-28` security review), `M-06` (`CT-27` payout cadence);
`SEC-001…015` dispositions; `origin/master` deletion.

**E. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 → create `docs/phases/bootstrap/`
with the full artifact set — only after Gate 0 evidence exists. Gate 0 stays `FAIL` (`CRIT-01`, `ASM-14`,
`DEP-05/06/10`) until then.

## 4. Commands

```text
python senior-rules/validators/validate.py .     # must end PASS (77 + 94 rule IDs); run after EVERY change set
python tools/check_citations.py                  # must end PASS (REC-15 CI parity); run after EVERY change set
# secret scan (gitleaks 8.30.1; winget alias may need a restarted shell):
gitleaks dir E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner     # expect: no leaks found, exit 0
gitleaks git  E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner     # expect: no leaks found, exit 0
# UC inventory: Get-ChildItem docs\01-business-analysis -Recurse -Filter 'UC-*.md'   # expect 420 (contiguous UC-001…UC-420)
# old-count grep (after any UC/BR/AC/TC count change): Select-String over docs for the OLD value,
#   excluding 20-/21- CH rows — only historical Change History rows may remain.
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -15                                 # commit history (session-011 evidence)
```

## 5. PowerShell / editing gotchas (they cost real time — re-read before scripting)

- **NEVER name a PS function after an alias.** `function RD {…}` collided with `rd` (= `Remove-Item`) and
  **deleted 10 files** (session 006; recovered only because everything was committed). Use alias-safe names
  (`GetRaw`, `OutRaw`) and guard whole-file writes against `$null` content.
- **PS array flattening corrupts multi-line content** (session 011, agent M2): rebuilding content through
  `Where-Object`/`+=` pipelines collapsed two README files during a rename batch — recovery was a byte-provenance
  replay from `.git/objects` blobs. Prefer the Edit tool or scalar exact-string replaces; count-assert after every
  scripted write; agents never run git.
- **Double-quoted PS strings AND here-strings `@"…"@` consume backticks** — a `## Change History` row written
  through one lost its `` ` `` characters. Use **single-quoted here-strings** `@'…'@` / single-quoted patterns for
  markdown; scan for `CTRL[7]` after scripted writes. Inline `python -c "…` with backticks in the pattern silently
  fails the match — write a `.py` file or use the Edit tool instead.
- **`Set-Content -Encoding utf8` (PS 5.1) writes a BOM** — gitleaks rejects a BOM'd config; write config TOML with
  `[IO.File]::WriteAllText($p, $s, (New-Object Text.UTF8Encoding($false)))`.
- **`.Replace()` silently no-ops on mismatch** → wrap with `.Contains()` check; collect `$fail`.
- **`-like '*`X`*'` treats backtick as escape** → use `.Contains()`.
- **Exact-string matches must copy the file's real characters** — em-dash `—` (U+2014) vs ASCII `-`.
- **`-replace 'pattern\r?$'` fails on CRLF** → edit via the Edit tool or match explicit `` `r`n ``.
- **`Select-String -Path docs\**\*.md` misses depth ≥ 3** → `Get-ChildItem docs -Recurse -Filter *.md`.
- **Never backtick a concrete dead path in a new CH/evidence row** (session 011: 8 new danglers from well-meant
  old-path quotes — the checker path-checks single-backticked `.md`/`.py` tokens; angle-bracket/`…`/brace tokens are
  skipped). Quote old paths **un-backticked** in history rows (same-session precedent).
- **Frontmatter checks must parse only the YAML block** — `docs/README.md` §9.2 contains a literal
  `^related_requirements:` inside a code-fence example (whole-file regex gives a false "key exists").
- Insert table rows into the **correct table** (a propagation row once landed in Change History).
- Files are UTF-8 with BOM at root, no BOM in `docs/` — keep encodings as found.
- **Parallel subagents need strictly disjoint file sets** (sessions 010/011): two agents editing one file lose each
  other's writes; give each agent its own folder, have it **report (not commit, no gates)**, and **re-verify its
  claims yourself** — session 011's M2 report passed its own sweep yet missed the moved files' own outbound links
  (the orchestrator completed them).
- **Same-change-set propagation is easy to under-do:** after any count/registry/path change, grep the *old* value
  repo-wide (excluding CH/evidence rows) **and** run both gates before calling the set done.

## 6. Honesty rules in force

- Evidence tags on every non-obvious claim: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`.
- **Owner-supplied numbers are never republished as derived** (session 010/011: owner "over 350" beside derived 210
  then 420 — publish both, say which is which; count ≥ target ≠ coverage — the matrix decides).
- Findings are **never deleted** when closed — flip status + date (DOC-TPL-011 #3).
- Never cite an ID absent from its owning register (root README §11 `D-3`) — CI-enforced by
  `tools/check_citations.py` on every push/PR (local runs still required before each commit).
- No dates/effort/sprints until `ASM-14` baselines exist (plan approval does not lift this).
- **Approval ≠ evidence:** `plan-develop.md` v1.2 being APPROVED never makes a gate PASS, never mints `FR-*`,
  never flips a finding to `VERIFIED` (DOD-10 / SPE-03 / GEN-03).
- **Pushed ≠ running ≠ seen:** record the CI run's actual result; 13 prior failures make a green claim doubly
  suspect — UNVERIFIED until observed.
- **Installed ≠ clean:** the secret scan is PASS only because raw findings were triaged (2 benign fixtures) and the
  allowlist is scoped + justified — say exactly that; never say "0 findings".
- **Phantom registration is a disposition, not a waiver:** each `PHANTOM_PATHS` pair carries per-pair justification
  (23 pairs total); fix new danglers at source first.
- **Coverage claims require the matrix** (AUD-01/D-02 precedent; index §5) — gaps go to an explicit PENDING list,
  never to silence.
- Every edited doc: version bump + `## Change History` row; propagation logged in `consistency-audit.md` §4;
  re-run the 31-check sweep when counts move, plus the validator and the citation checker after every change set.
- Constraint amendments (`C-NN`) only via `docs/README.md` §9 change control (v bump + CH row + propagate).
- Rule changes: `core/00` §0.5 only (propose → edit → bump `VERSION` → `CHANGELOG` → validator) — never hot-patch.
  Factual corrections to adapter prose (counts, path spellings) do not change the pin (session 005/008 precedent).
- End the session by updating `session_track.md` (log + evidence + resume prompt) and `memory.md`
  if defects changed; author the session work file under `docs/sessions/` (SES-01).
- **Only push the session-named branch** — `session-011` now (close-out), then `session-012` for new work —
  `main` is off-limits by directive.
