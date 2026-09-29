# prompt-next — Session 011 Handoff (PENDING UC backlog, AC reconciliation debt, sponsor dispositions, CI verification)

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08` — now **2.2.0**). Resume point: `session_track.md` session 010.
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> Citation checker must end green: `python tools/check_citations.py`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-09-29, session 010 CLOSED)

The owner's use-case directive was executed end to end — session file:
[`docs/sessions/session-010-uc-coverage-expansion.md`](docs/sessions/session-010-uc-coverage-expansion.md) (DOC-SES-010, v1.0).

- **UC coverage 42 → 210** (`prompt-010.md` §1): **168 `UC-043`…`UC-210`** minted in **parallel
  subagent waves** (10 + 3 agents, strictly disjoint file sets; `UC-045` re-filled for contiguity;
  4 cross-ref typos fixed), template-verbatim, only existing `BR-*`/`FR-*`. Inventory verified:
  210 files, missing 0, every file 55–75 lines.
- **Honesty (never blend the numbers):** **derived 210** published beside the **owner target
  "over 350" = `INSUFFICIENT EVIDENCE`**; coverage claimed only as far as the index §5 matrix
  proves it; an explicit **18-item PENDING backlog** (`use-cases/README.md` §5.1) lists what is
  *not* covered (with reasons) — no zero-gap claim.
- **Change control:** `naming-conventions.md` **v1.6** (§3 `UC-001…UC-210`, **210 issued**, next
  **`UC-211+`**), `terminology.md` **v1.3**, `use-case-template.md` **v1.2** — commits `c1f280d`.
- **Propagation, no omissions:** index `DOC-UC-000` **v1.2** (+168 rows, §3 totals 58/32/12/59/1/5/43
  = 210, §5 coverage matrix 43/65/58/32/12 = 210 + PENDING + numbers note), `19-traceability` ×3
  **v1.3/v1.3/v1.5** (Matrix B +213 UC→FR links = 282 pairs; `F-07`/`G-07` 121 → **779**),
  `analysis-validation` **v1.13** (domain-01 63 → **231 files**, 42 → **210 UC**),
  `consistency-audit` **v1.20**, `phases/analysis/use-cases` **v1.2** (+168 rows), stale
  `UC-001…UC-040` ranges fixed in `03-`/`11-` — commit `fc242c0`.
- **QC (orchestrator re-ran, did not trust agent reports):** **779 `AC-UCnnn-nn`, 0 collisions**;
  flagged BRs verified present in `business-rules.md`; spot-reads template-clean.
- **Full 31-check sweep** (`prompt-010` §4.4 — counts moved): **654-file corpus → 20 `PASS` /
  2 `PWF` / 9 `FAIL`, identical verdicts, no flip**; evidence cells refreshed; roll-up unchanged.
- **Trackers:** `session_track.md` row 010 `CLOSED` + log + resume → 011; `sessions/README.md`
  **v1.7** (row 010); session file DOC-SES-010 v1.0; `memory.md` session-010 snapshot;
  `all_in_one_track.md` (sessions `…010`); this file → 011 **and** `prompt-011.md`.

**Last states:** validator `RESULT: PASS — structure healthy` (0 broken links; 77 + 94 rule IDs);
citation check `RESULT: PASS — every cited path and ID resolves (REC-15)`
**669 files, 21,751 ID citations, 0 problems**; `gitleaks dir` exit 0 (session allowlist).
**Git:** branch **`session-010`**: `c1f280d` (change control), `6b0bba4` (168 UCs minted),
`fc242c0` (propagation) + sweep/close-out commits — remote `origin` =
`https://github.com/mohaned733406131-byte/YUMN.git`. **`main` was not touched** — by directive
(it still sits at `c9ff07c`, the session-007 close).

## 2. Current truth (do not contradict)

- **65 open findings** across the seven audits: 13 consistency + 21 contradiction + 11 gap +
  7 hallucination + 6 critical + 7 requirement-validation (snapshot 2026-09-29,
  `analysis-validation.md` **v1.13** — register of record; **no finding status changed in 010**).
- Register versions: `consistency-audit.md` **v1.20** (13 OPEN · 15 RESOLVED; **31-check re-run
  20/2/9 on the 654-file corpus** — same 9 `FAIL`s = findings 6, 7, 8, 11, 14, 15, 16, 21, 22),
  `contradiction-audit.md` **v1.6** (21 open), `missing-information.md` **v1.3** (11 open),
  `hallucination-audit.md` **v1.8** (7 open), `critical-findings.md` **v1.5** (6 open),
  `requirements-validation.md` **v1.1** (7 open), `analysis-validation.md` **v1.13** (65 open),
  `technical-debt.md` **v1.9** (**all `TD-01…TD-10` `PAID`**),
  `recommendations.md` **v1.10** (**assistant-side all `PAID`** — `REC-01…REC-10`, `REC-14`,
  `REC-15`; `REC-11…REC-13` remain sponsor-owned).
- **Use cases: 210** (`UC-001…UC-210`); allocation **210 issued**, next free **`UC-211+`**
  (`naming-conventions.md` v1.6 §3). Index `DOC-UC-000` **v1.2**. **Owner "over 350" target is
  still open** — the honest path to it is the index §5.1 **18-item PENDING backlog** (mint only
  from sources; matrix first; never fabricate scenarios — `AUD-04` territory).
- **The 9 failing checks** and their owning findings: `CHK-12`/`CHK-13` → findings 6/7
  (`AC-S-04/12/21` absent + **779** `AC-UCnnn-nn` outside the 253-row registry — the gap *grew*
  because coverage grew; evidence re-counted, status untouched), `CHK-14` → finding 8, `CHK-19` →
  finding 11, `CHK-22`/`CHK-24` → findings 14/15 (`22-glossary/` three term rows + the `A-07`
  claim), `CHK-23` → finding 16 (`seller`/`merchant` synonym drift — disallowed by naming
  conventions; counts depend on scope), `CHK-29` → finding 21 (`GAP-NNN` width in root README §5),
  `CHK-31` → finding 22 (money-path status sets / `payout_state` domain).
- **Secret scan = PASS** (gitleaks 8.30.1, `.gitleaks.toml`, tree + history clean). Record it as
  *triaged* (2 benign test fixtures) with evidence, never as "no findings".
- **Citation CI run = UNVERIFIED:** workflow is pushed; the repo is private, the Actions page 404s
  unauthenticated, no `gh` CLI here. Local parity is green. Open the GitHub UI and record what the
  run actually says (never claim PASS from this machine).
- Business rules: **104** across **15** domains; constraints `C-01…C-26`; rules **ADMR 2.2.0** +
  `YUMN_RULES.md` 94.
- Plan: `plan-develop.md` **v1.2 APPROVED** — `M-01…M-25` / `P-01…P-20` are **backlog items**, not
  `FR-*`; they convert only at their build wave (`SPE-03`/`D-02`). Approved ≠ implemented.
  Plan items deliberately **OPEN after approval**: `M-01` (`CT-23`/`GAP-14`), `M-04` (`CT-26`),
  `M-05` (`CT-28`), `M-06` (`CT-27`) — finance/security/owner review (`GEN-03`/`DOD-10`).
- **Gate 0 = `FAIL`**: `CRIT-01` (`ASM-14` unset) + `DEP-05`/`DEP-06`/`DEP-10` NOT STARTED.
  Nothing in `docs/` is `VERIFIED` — no implementation exists (`SPE-03`).
- `memory.md` §4: D-01/D-03/D-04/D-05/D-09/D-10/D-13/D-14/D-15/D-16 **RESOLVED**; D-02 PARTIAL;
  D-06, D-07, D-08, D-11, D-12 OPEN (D-11 = decision made, ADR deferred by design).
- `SEC-001…015` all open; `origin/master` deletion pending default-branch switch on GitHub
  (needs a click or `gh` CLI — not available here).

## 3. Next work queue (in priority order)

**A. Sponsor/finance/security dispositions (surface, never fake):** `REC-11` (`ASM-14` baselines,
re-score `ASM-03`/`ASM-04`/`ASM-12`), `REC-12` (`DEP-05` m-Floos/OneCash sandbox, `DEP-06`
SMS/WhatsApp contracts), `REC-13` (`DEP-10` Central Bank position before any B07 build); plan
items `M-01` (`CT-23` + `GAP-14`), `M-04` (`CT-26` pricing), `M-05` (`CT-28` security review),
`M-06` (`CT-27` payout cadence); `SEC-001…015` dispositions; `origin/master` deletion.

**B. Work the 18-item PENDING UC backlog (`UC-211+`) if the owner wants the "over 350" target:**
source list = index `use-cases/README.md` §5.1 (each item has its reason). Every new UC needs the
same discipline as session 010: source document behind it, template `use-case-template.md` v1.2,
existing `BR-*`/`FR-*` only, then the same-change set (index row + §3 totals + §5 matrix +
`phases` inventory + consumers grep + both gates + full sweep if counts move). Next free ID is
`UC-211`; never reuse/renumber.

**C. Verify the pushed CI (honestly):** open the GitHub Actions UI for `docs-citations.yml`;
record the run's actual result in the session-011 work file (PASS/FAIL/UNVERIFIED — whatever it
is). Locally both checks are green; the runner is not proven until seen.

**D. Work the 9 remaining `FAIL` checks via their owning findings** (section 2 has the map):
AC reconciliation (findings 6/7/8 — note `CHK-13` evidence is now **779**), glossary term rows
(14/15), `seller`/`merchant` synonym normalization (16), `GAP-NNN` width (21), money-path status
sets + `payout_state` (22). Each fix = owning file version bump + CH row + register flip +
**re-run the 31-check sweep** (session-local script pattern is documented in the session-009/010
files — rebuild it if gone; `C:\Users\Mohanned\AppData\Local\Temp\opencode\chk31_v2.py` may still
exist but is not a repo artifact) + validator + citation check.

**E. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 → create
`docs/phases/bootstrap/` with the full artifact set — only after Gate 0 evidence exists.
Gate 0 stays `FAIL` (`CRIT-01`, `ASM-14`, `DEP-05/06/10`) until then.

## 4. Commands

```text
python senior-rules/validators/validate.py .     # must end PASS (77 + 94 rule IDs); run after EVERY change set
python tools/check_citations.py                  # must end PASS (REC-15 CI parity); run after EVERY change set
# secret scan (gitleaks 8.30.1; winget alias may need a restarted shell):
gitleaks dir E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner     # expect: no leaks found, exit 0
gitleaks git  E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner     # expect: no leaks found, exit 0
# UC inventory:  Get-ChildItem docs\01-business-analysis\use-cases -Filter 'UC-*.md'   # expect 210+ (contiguous)
# old-count grep (after any UC/BR/TC count change): Select-String over docs for the OLD value,
#   excluding 20-/21- CH rows — only historical Change History rows may remain.
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -10                                 # commit history (session-010 evidence)
```

## 5. PowerShell / editing gotchas (they cost real time — re-read before scripting)

- **NEVER name a PS function after an alias.** `function RD {…}` collided with `rd` (= `Remove-Item`)
  and **deleted 10 files** (session 006; recovered only because everything was committed).
  Use alias-safe names (`GetRaw`, `OutRaw`) and guard whole-file writes against `$null` content.
- **Double-quoted PS strings AND here-strings `@"…"@` consume backticks** — a `## Change History`
  row written through one lost its `` ` `` characters (`` `a `` became a BEL byte, U+0007), and a
  search pattern `` '99 `BR' `` written in double quotes becomes an unterminated-string parse error.
  Use **single-quoted here-strings** `@'…'@` / single-quoted patterns for markdown; scan for
  `CTRL[7]` after scripted writes. Inline `python -c "…` with backticks in the
  pattern silently fails the match — write a `.py` file or use the Edit tool instead.
- **`Set-Content -Encoding utf8` (PS 5.1) writes a BOM** — gitleaks rejects a BOM'd config
  (`invalid character at start of key`); write config TOML with
  `[IO.File]::WriteAllText($p, $s, (New-Object Text.UTF8Encoding($false)))`.
- **`.Replace()` silently no-ops on mismatch** → wrap with `.Contains()` check; collect `$fail`.
- **`-like '*`X`*'` treats backtick as escape** → use `.Contains()`.
- **Exact-string matches must copy the file's real characters** — em-dash `—` (U+2014) vs ASCII `-`.
- **`-replace 'pattern\r?$'` fails on CRLF** → edit via the Edit tool or match explicit `` `r`n ``.
- **`Select-String -Path docs\**\*.md` misses depth ≥ 3** → `Get-ChildItem docs -Recurse -Filter *.md`.
- **Frontmatter checks must parse only the YAML block** — `docs/README.md` §9.2 contains a literal
  `^related_requirements:` inside a code-fence example (whole-file regex gives a false "key exists").
- Insert table rows into the **correct table** (a propagation row once landed in Change History).
- Files are UTF-8 with BOM at root, no BOM in `docs/` — keep encodings as found.
- **Parallel subagents need strictly disjoint file sets** (session 010): two agents editing one
  file lose each other's writes; give each agent its own folder, have it report (not commit), and
  **re-verify its claims yourself** — counts, IDs, and spot-reads (session 010 QC caught nothing
  wrong only because it re-ran every check instead of trusting reports).
- **Same-change-set propagation is easy to under-do:** session 008 found 7 count consumers of
  `business-rules.md` that the registration set missed; session 009's own new path shorthand
  failed the citation checker until reworded. After any count/registry/path change, grep for the
  *old* value repo-wide (excluding CH/evidence rows) **and** run both gates before calling the set done.

## 6. Honesty rules in force

- Evidence tags on every non-obvious claim: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`.
- **Owner-supplied numbers are never republished as derived** (session 010: "over 350" stays
  `INSUFFICIENT EVIDENCE` beside the derived 210 — publish both, say which is which).
- Findings are **never deleted** when closed — flip status + date (DOC-TPL-011 #3).
- Never cite an ID absent from its owning register (root README §11 `D-3`) — CI-enforced by
  `tools/check_citations.py` on every push/PR (local runs still required before each commit).
- No dates/effort/sprints until `ASM-14` baselines exist (plan approval does not lift this).
- **Approval ≠ evidence:** `plan-develop.md` v1.2 being APPROVED never makes a gate PASS,
  never mints `FR-*`, never flips a finding to `VERIFIED` (DOD-10 / SPE-03 / GEN-03).
- **Pushed ≠ running:** the citation workflow's GitHub run is UNVERIFIED until seen in the UI.
- **Installed ≠ clean:** the secret scan is PASS only because raw findings were triaged (2 benign
  fixtures) and the allowlist is scoped + justified — say exactly that; never say "0 findings".
- **Coverage claims require the matrix** (AUD-01/D-02 precedent; session 010 index §5) — gaps go
  to an explicit PENDING list, never to silence.
- Every edited doc: version bump + `## Change History` row; propagation logged in
  `consistency-audit.md` §4; re-run the 31-check sweep, the validator, and the citation checker.
- Constraint amendments (`C-NN`) only via `docs/README.md` §9 change control (v bump + CH row + propagate).
- Rule changes: `core/00` §0.5 only (propose → edit → bump `VERSION` → `CHANGELOG` → validator) — never hot-patch.
  Factual corrections to adapter prose (counts, path spellings) do not change the pin (session 005/008 precedent).
- End the session by updating `session_track.md` (log + evidence + resume prompt) and `memory.md`
  if defects changed; author the session work file under `docs/sessions/` (SES-01).
- **Only push the session-named branch** (`session-011` next) — `main` is off-limits by directive.
