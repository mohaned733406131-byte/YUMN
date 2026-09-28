# prompt-next — Session 007 Handoff (REC pay-downs, then bootstrap)

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08` — now **2.2.0**). Resume point: `session_track.md` session 006.
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-09-28, session 006 CLOSED)

The **change-control sweep** ran and F-07 was amended — session file:
[`docs/sessions/session-006-change-control-sweep.md`](docs/sessions/session-006-change-control-sweep.md) (DOC-SES-006).

- **31-check scripted re-run** on the **479**-file corpus → **18 PASS · 2 PWF · 11 FAIL**
  (flips: `CHK-01`, `CHK-06`, `CHK-15`; `CHK-05` 49 → **48** files still missing `## Change History`).
- **Sweep fixes:** `related_requirements: []` + `## Change History` on session files/READMEs → finding 1
  `RESOLVED`; `GAP-07…12` pointer rows in `project-scope.md` v1.1 → finding 9 `RESOLVED`; `DOC-REQ-010`
  → `DOC-NFD-001` (finding 28); queue token → `b10.notification.delivery` (finding 27).
- **Deferred findings (a)–(f) filed in owning registers:** (a) → consistency **finding 26** (`HIGH`,
  `OPEN` — Moderator read conflict), (b) → **`CT-21`**, (c) **disproved** → **`HAL-14` `RESOLVED`**,
  (d) → **`CT-22`**, (e) → **`HAL-15`**, (f) re-verified `HAL-05`/`RVF-04`/`CRIT-05` still `OPEN`.
- **Registers now:** `consistency-audit.md` **v1.11** (28 findings, 15 `OPEN`/13 `RESOLVED`), `contradiction-audit.md`
  **v1.4** (`CT-01…CT-22`, 17 open), `hallucination-audit.md` **v1.3** (`HAL-01…HAL-15`, 12 open),
  `analysis-validation.md` **v1.5** (**71 open** roll-up), `critical-findings.md` v1.3, `requirements-validation.md` v1.1.
- **F-07 FIXED** via `core/00` §0.5: `validate.py` check 5 covers `RULES.md` (77) **and** `YUMN_RULES.md`
  (94) + zero-IDs guard; `VERSION` → **2.2.0**; `CHANGELOG.md` `[2.2.0]`; `RULES_HINTS.md` §1 pin → 2.2.0.
- **Operational incident logged:** a PS function named `RD` resolved to the `rd` alias (`Remove-Item`)
  and deleted 10 files — recovered with `git restore`; never name a PS function after an alias (§5).

**Last validator state:** `RESULT: PASS — structure healthy` (0 broken links; 77 + 94 rule IDs).
**Trackers updated:** `session_track.md` row 006 + resume → 007; `memory.md` session-006 snapshot;
`docs/sessions/README.md` v1.2 (row 006); `all_in_one_track.md` (`session-001…006`, 71 open).

## 2. Current truth (do not contradict)

- **71 open findings** across the seven audits: 15 consistency + 17 contradiction + 12 gap +
  12 hallucination + 8 critical + 7 requirement-validation (snapshot 2026-09-28, `analysis-validation.md` v1.5).
- Register versions: `consistency-audit.md` **v1.11** (18/2/11 checks; 15 OPEN · 13 RESOLVED),
  `contradiction-audit.md` **v1.4** (17 open), `critical-findings.md` **v1.3** (8 open),
  `analysis-validation.md` **v1.5**, `hallucination-audit.md` **v1.3** (12 open),
  `requirements-validation.md` **v1.1** (7 open), `requirements-to-tests.md` **v1.3**,
  `technical-debt.md` **v1.7** (`TD-07…10` PAID; `TD-01…03` OPEN), `recommendations.md` **v1.7**
  (`REC-03…09` PAID; `REC-01/02/10…15` remain).
- Rules: **ADMR 2.2.0** (pin in `RULES_HINTS.md` §1; rule text unchanged since 2.0.0) + `YUMN_RULES.md` 94.
- Queue register = 30 rows; names `{block}.{entity}.{action}` (BR-PLT-01); repo scan 0 violations.
- **Gate 0 = `FAIL` today**: `CRIT-01` (`ASM-14` unset) + `DEP-05`/`DEP-06` NOT STARTED.
  Nothing in `docs/` is `VERIFIED` — no implementation exists (`SPE-03`).
- `memory.md` §4: D-01/D-03/D-05/D-09/D-13/D-14/D-15 RESOLVED; D-02 PARTIAL; D-10 PARTIAL;
  D-04, D-06…D-08, D-11, D-12, D-16 OPEN. D-13 note: pin now 2.2.0 (superseded 2026-09-28).
- `CHK-05` residual: 48 files without `## Change History` (40 UC, 6 `functional/FR-*`,
  `02-requirements/README.md`, `00-project-overview/README.md`) — owning documents fix this (§9.5).

## 3. Next work queue (in priority order)

**A. Assistant-side recommendations:** `REC-01`, `REC-02`, `REC-10`, `REC-14`, `REC-15`
(`TD-01…03` open; `REC-15` = CI enforcement — no CI exists yet). Read each row's acceptance criteria
in `docs/21-completion/recommendations.md` before starting; same-change-set propagation every time.

**B. Surface sponsor-owned blockers (never fake, never fix here):** `REC-11` (`ASM-14`),
`REC-12` (`DEP-05`/`DEP-06`), `REC-13` (`DEP-10`); `D-10`/`D-16` (restore vs drop);
`SEC-001…015` dispositions; `origin/master` deletion (needs default-branch switch on GitHub).

**C. Re-audit rule (every gate):** re-run the seven audits / 31 checks before claiming any gate
(root README §11; `20-validation/README.md` §4 rule 7) — counts drift; take fresh numbers from files.

**D. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 → create
`docs/phases/bootstrap/` with the full artifact set — only after B dispositioned and Gate 0 evidence exists.

## 4. Commands

```text
python senior-rules/validators/validate.py .          # must end PASS (77 + 94 rule IDs); run after EVERY change set
# queue-name acceptance scan (must stay 0 violations): parse register from
#   docs/06-backend/background-processing.md §1 first column (expect 30 entries), then scan
#   Get-ChildItem docs -Recurse -Filter *.md  excluding \20-validation\ + \21-completion\,
#   cut each file at its "## Change History" line, regex (?<![\w.-])b\d{2}\.[a-z0-9_]+(?:[._-][a-z0-9_]+)+,
#   SKIP tokens containing "_" (DB column refs), flag the rest if absent from the register.
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -10                                 # commit history (session-006 evidence)
```

## 5. PowerShell / editing gotchas (they cost real time — re-read before scripting)

- **NEVER name a PS function after an alias.** `function RD {…}` collided with `rd` (= `Remove-Item`)
  and **deleted 10 files** (session 006; recovered only because everything was committed).
  Use alias-safe names (`GetRaw`, `OutRaw`) and guard whole-file writes against `$null` content.
- **Double-quoted PS strings AND here-strings `@"…"@` consume backticks** — a `## Change History`
  row written through one lost its `` ` `` characters (`` `a `` became a BEL byte, U+0007).
  Use **single-quoted here-strings** `@'…'@` for markdown; scan for `CTRL[7]` after scripted writes.
- **`Set-Content`/`Get-Content` round-trips safely only because these files carry a BOM** — verify
  with `git diff` after any whole-file rewrite (look for mojibake in Arabic/`§`/`—`).
- **`.Replace()` silently no-ops on mismatch** → wrap with `.Contains()` check; collect `$fail`.
- **`-like '*`X`*'` treats backtick as escape** → use `.Contains()`.
- **Exact-string matches must copy the file's real characters** — em-dash `—` (U+2014) vs ASCII `-`.
- **`-replace 'pattern\r?$'` fails on CRLF** → edit via the Edit tool or match explicit `` `r`n ``.
- **`Select-String -Path docs\**\*.md` misses depth ≥ 3** → `Get-ChildItem docs -Recurse -Filter *.md`.
- **Frontmatter checks must parse only the YAML block** — `docs/README.md` §9.2 contains a literal
  `^related_requirements:` inside a code-fence example (whole-file regex gives a false "key exists").
- Insert table rows into the **correct table** (a propagation row once landed in Change History).
- Files are UTF-8 with BOM at root, no BOM in `docs/` — keep encodings as found.

## 6. Honesty rules in force

- Evidence tags on every non-obvious claim: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`.
- Findings are **never deleted** when closed — flip status + date (DOC-TPL-011 #3).
- Never cite an ID absent from its owning register (root README §11 `D-3`).
- No dates/effort/sprints until `ASM-14` baselines exist.
- Every edited doc: version bump + `## Change History` row; propagation logged in
  `consistency-audit.md` §4; re-run audits and the validator.
- Gate 0 / DOD gates stay `BLOCKED`/`FAIL` until real evidence exists (DOD-10) — never green-wash.
- Rule changes: `core/00` §0.5 only (propose → edit → bump `VERSION` → `CHANGELOG` → validator) — never hot-patch.
- End the session by updating `session_track.md` (log + evidence + resume prompt) and `memory.md`
  if defects changed; author the session work file under `docs/sessions/` (SES-01).
