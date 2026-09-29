# prompt-next — Session 010 Handoff (sponsor dispositions, CI verification, remaining 9 check FAILs)

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08` — now **2.2.0**). Resume point: `session_track.md` session 009.
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> Citation checker must end green: `python tools/check_citations.py`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-09-29, session 009 CLOSED)

Pre-gate hygiene was executed without touching any gate — session file:
[`docs/sessions/session-009-pre-gate-hygiene.md`](docs/sessions/session-009-pre-gate-hygiene.md) (DOC-SES-009, v1.0).

- **Fresh 31-check re-run** (the session-008 deferral) on the **485**-file corpus, session-local
  script (not committed): pre-fix **19 `PASS` / 2 `PWF` / 10 `FAIL`**; session 006's recorded
  "18/2/10" correlated to 19/2/10 (its own tally was 18/2/**11** + the session-008 `CHK-21` flip).
- **`CHK-05` fixed → finding 2 `RESOLVED`:** the 48 residual files (40 `UC-001…040`, 6
  `functional/FR-{005,007,016,018,019,020}`, `02-requirements/README.md`,
  `00-project-overview/README.md`) given `## Change History` + `1.0` → **`1.1`**;
  `CHK-05` **485/485**, tally **20 `PASS` / 2 `PWF` / 9 `FAIL`** — the only state change.
- **Registers:** `consistency-audit.md` **v1.17**, `analysis-validation.md` **v1.11** (roll-up
  **66 → 65 open**), consumers `phase-audit.md` **v1.6**, `implementation-plan.md` **v1.3**,
  `session-005` **v1.6**, `all_in_one_track.md`.
- **Secret scan now genuinely PASS (was BLOCKED):** gitleaks **8.30.1** installed via
  `winget install --id Gitleaks.Gitleaks`; raw findings 2 (tree) / 5 (git history, 28 commits)
  were the same two benign `Idempotency-Key` test fixtures → **`.gitleaks.toml`** (default rules
  kept, regex-scoped allowlist with written justifications) → `gitleaks dir` **exit 0**,
  `gitleaks git` **exit 0**.
- **Trackers:** `session_track.md` row 009 `CLOSED` + log + resume → 010; `sessions/README.md`
  **v1.6** (row 009); session file DOC-SES-009 v1.0; `memory.md` session-009 snapshot;
  this file → 010.

**Last states:** validator `RESULT: PASS — structure healthy` (0 broken links; 77 + 94 rule IDs);
citation check `RESULT: PASS — every cited path and ID resolves (REC-15)`
**498 files, 18,875 ID citations, 0 problems** (it earned its keep this session: the first run
after my register edits failed on one path I had invented — `` `02-requirements/functional/FR-005/007/…md` ``
— fixed at source, then green; the session file's own references to the two uncommitted
session-local scripts had to come off the path checker as plain text; re-run it before every commit).
**Git:** branch **`session-009`**: `ae2ae01` (CHK-05 remediation + registers, roll-up 65),
`d492ae3` (gitleaks allowlist), `f303c54` (session-009 close-out) — remote `origin` =
`https://github.com/mohaned733406131-byte/YUMN.git`. **`main` was not touched** — by directive
(it still sits at `c9ff07c`, the session-007 close).

## 2. Current truth (do not contradict)

- **65 open findings** across the seven audits: 13 consistency + 21 contradiction + 11 gap +
  7 hallucination + 6 critical + 7 requirement-validation (snapshot 2026-09-29,
  `analysis-validation.md` **v1.11** — register of record).
- Register versions: `consistency-audit.md` **v1.17** (13 OPEN · 15 RESOLVED; **31-check re-run
  20/2/9 on the 485-file corpus** — 9 `FAIL`s = findings 6, 7, 8, 11, 14, 15, 16, 21, 22),
  `contradiction-audit.md` **v1.6** (21 open), `missing-information.md` **v1.3** (11 open),
  `hallucination-audit.md` **v1.8** (7 open), `critical-findings.md` **v1.5** (6 open),
  `requirements-validation.md` **v1.1** (7 open), `analysis-validation.md` **v1.11** (65 open),
  `technical-debt.md` **v1.9** (**all `TD-01…TD-10` `PAID`**),
  `recommendations.md` **v1.10** (**assistant-side all `PAID`** — `REC-01…REC-10`, `REC-14`,
  `REC-15`; `REC-11…REC-13` remain sponsor-owned).
- **The 9 failing checks** and their owning findings: `CHK-12`/`CHK-13` → findings 6/7
  (`AC-S-04/12/21` + 127 `AC-UCnnn-nn` reconciliation in `02-requirements/acceptance-criteria.md`),
  `CHK-14` → finding 8, `CHK-19` → finding 11, `CHK-22`/`CHK-24` → findings 14/15
  (`22-glossary/` three term rows + the `A-07` claim), `CHK-23` → finding 16 (`seller`/`merchant`
  synonym drift — disallowed by naming conventions; counts depend on scope: 19 files/37 hits vs
  38/79 across all of `docs/`, 17/20 and 28/48 case-sensitive excluding `20-`/`21-`),
  `CHK-29` → finding 21 (`GAP-NNN` width in root README §5), `CHK-31` → finding 22
  (money-path status sets / `payout_state` domain).
- **Secret scan = PASS** (gitleaks 8.30.1, `.gitleaks.toml`, tree + 28-commit history clean).
  The raw hits were always fixtures — record it as *triaged* with evidence, not as "no findings".
- **Citation CI run = UNVERIFIED:** `.github/workflows/docs-citations.yml` is pushed; the repo is
  private, the Actions page 404s unauthenticated, no `gh` CLI here. Local parity is green. Open
  the GitHub UI and record what the run actually says (never claim PASS from this machine).
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

**B. Verify the pushed CI (honestly):** open the GitHub Actions UI for `docs-citations.yml`;
record the run's actual result in the session-010 work file (PASS/FAIL/UNVERIFIED — whatever it
is). Locally both checks are green; the runner is not proven until seen.

**C. Work the 9 remaining `FAIL` checks via their owning findings** (section 2 lists the
check → finding map): AC reconciliation (findings 6/7/8), glossary term rows (14/15),
`seller`/`merchant` synonym normalization (16), `GAP-NNN` width (21), money-path status sets +
`payout_state` (22). Each fix = owning file version bump + CH row + register flip + **re-run the
31-check sweep** (the session-local script pattern is documented in the session-009 file —
rebuild it if gone) + validator + citation check.

**D. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 → create
`docs/phases/bootstrap/` with the full artifact set — only after Gate 0 evidence exists.
Gate 0 stays `FAIL` (`CRIT-01`, `ASM-14`, `DEP-05/06/10`) until then.

## 4. Commands

```text
python senior-rules/validators/validate.py .     # must end PASS (77 + 94 rule IDs); run after EVERY change set
python tools/check_citations.py                  # must end PASS (REC-15 CI parity); run after EVERY change set
# secret scan (now available — gitleaks 8.30.1 at %LOCALAPPDATA%\Microsoft\WinGet\Links\gitleaks.exe;
#   the winget alias is on PATH only in a restarted shell):
gitleaks dir E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner     # expect: no leaks found, exit 0
gitleaks git  E:\YUMN --config E:\YUMN\.gitleaks.toml --redact --no-banner     # expect: no leaks found, exit 0
# queue-name acceptance scan (must stay 0 violations): parse register from
#   docs/06-backend/background-processing.md §1 first column (expect 30 entries), then scan
#   Get-ChildItem docs -Recurse -Filter *.md  excluding \20-validation\ + \21-completion\,
#   cut each file at its "## Change History" line, regex (?<![\w.-])b\d{2}\.[a-z0-9_]+(?:[._-][a-z0-9_]+)+,
#   SKIP tokens containing "_" (DB column refs), flag the rest if absent from the register.
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -10                                 # commit history (session-009 evidence)
```

## 5. PowerShell / editing gotchas (they cost real time — re-read before scripting)

- **NEVER name a PS function after an alias.** `function RD {…}` collided with `rd` (= `Remove-Item`)
  and **deleted 10 files** (session 006; recovered only because everything was committed).
  Use alias-safe names (`GetRaw`, `OutRaw`) and guard whole-file writes against `$null` content.
- **Double-quoted PS strings AND here-strings `@"…"@` consume backticks** — a `## Change History`
  row written through one lost its `` ` `` characters (`` `a `` became a BEL byte, U+0007), and a
  search pattern `` '99 `BR' `` written in double quotes becomes an unterminated-string parse error.
  Use **single-quoted here-strings** `@'…'@` / single-quoted patterns for markdown; scan for
  `CTRL[7]` after scripted writes. This session: inline `python -c "…` with backticks in the
  pattern silently failed the match — write a `.py` file or use the Edit tool instead.
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
- **Same-change-set propagation is easy to under-do:** session 008 found 7 count consumers of
  `business-rules.md` that the registration set missed; session 009's own new path shorthand
  failed the citation checker until reworded. After any count/registry/path change, grep for the
  *old* value repo-wide (excluding CH/evidence rows) **and** run both gates before calling the set done.

## 6. Honesty rules in force

- Evidence tags on every non-obvious claim: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`.
- Findings are **never deleted** when closed — flip status + date (DOC-TPL-011 #3).
- Never cite an ID absent from its owning register (root README §11 `D-3`) — CI-enforced by
  `tools/check_citations.py` on every push/PR (local runs still required before each commit).
- No dates/effort/sprints until `ASM-14` baselines exist (plan approval does not lift this).
- **Approval ≠ evidence:** `plan-develop.md` v1.2 being APPROVED never makes a gate PASS,
  never mints `FR-*`, never flips a finding to `VERIFIED` (DOD-10 / SPE-03 / GEN-03).
- **Pushed ≠ running:** the citation workflow's GitHub run is UNVERIFIED until seen in the UI.
- **Installed ≠ clean:** the secret scan is PASS only because raw findings were triaged (2 benign
  fixtures) and the allowlist is scoped + justified — say exactly that; never say "0 findings".
- Every edited doc: version bump + `## Change History` row; propagation logged in
  `consistency-audit.md` §4; re-run the 31-check sweep, the validator, and the citation checker.
- Constraint amendments (`C-NN`) only via `docs/README.md` §9 change control (v bump + CH row + propagate).
- Rule changes: `core/00` §0.5 only (propose → edit → bump `VERSION` → `CHANGELOG` → validator) — never hot-patch.
  Factual corrections to adapter prose (counts, path spellings) do not change the pin (session 005/008 precedent).
- End the session by updating `session_track.md` (log + evidence + resume prompt) and `memory.md`
  if defects changed; author the session work file under `docs/sessions/` (SES-01).
- **Only push the session-named branch** (`session-010` next) — `main` is off-limits by directive.
