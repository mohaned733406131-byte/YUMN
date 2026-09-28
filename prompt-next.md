# prompt-next — Session 009 Handoff (sponsor dispositions, CI verification, pre-gate hygiene)

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08` — now **2.2.0**). Resume point: `session_track.md` session 008.
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> Citation checker must end green: `python tools/check_citations.py`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-09-28, session 008 CLOSED)

The assistant-side recommendation queue is **empty**: `REC-01`, the owner-approved `BR-INV-01…05`
registration, and `REC-15` citation CI were paid and propagated — session file:
[`docs/sessions/session-008-archdoc-brinv-citation-ci.md`](docs/sessions/session-008-archdoc-brinv-citation-ci.md) (DOC-SES-008, v1.0).

- **`REC-01` → PAID:** `archdoc.md` **v1.0** restored as an explicitly **RECONSTRUCTED** 24-domain
  structure spec (0-byte history + absent `archive/` disclosed, `SPE-03`); `docs/README.md` v1.4 §1;
  `TD-03`/`REC-01` PAID, `HAL-03`/`CRIT-08`/`AVF-08`/finding 13/`F-05`/`D-10` closed → 69 open.
- **`BR-INV-01…05` registered:** `business-rules.md` **v1.1** new `## INV` section — **104 rules /
  15 domains** — 8 count consumers re-synced; `CRIT-06`/`HAL-04`/`AVF-05` → `RESOLVED`,
  `CHK-08` re-counted 104/104 → 67 open.
- **`REC-15` → PAID:** `tools/check_citations.py` (12-series ID + path check, tail-boundary rule)
  + `.github/workflows/docs-citations.yml`; full repo green (496 files, 18,607 citations, 0 problems),
  failure mode proven (`exit 1`); two real dangling cites fixed at source
  (`actors-and-roles.md` v1.1, `requirements-to-tests.md` v1.4 `AC-FR020-05` → `-04`);
  `HAL-12`/`AVF-11`/`REC-15` closed → **66 open**.
- **Close-out catch-up:** 7 missed `99`→`104` BR consumers fixed (`01` README v1.2 incl. the
  `INV` domain list, `testing-strategy` v1.1, `qa-attributes` v1.1, `RULES_HINTS`/`YUMN_RULES`
  factual corrections, `memory`/`all_in_one_track`) + UC/TC dashboard drift (`analysis-validation`
  v1.10 domain-01 = 63 files/42 UC, `requirements-to-features` v1.2, `19-traceability/README` v1.2
  §5 re-count + `F-02`/`F-03` → `RESOLVED`); `consistency-audit` **v1.16**.
- **Trackers:** `session_track.md` row 008 `CLOSED` + log + resume → 009; `sessions/README.md`
  **v1.5** (row 008); session file DOC-SES-008 v1.0; `memory.md` session-008 snapshot + **`D-04`
  → `RESOLVED`**; this file → 009.

**Last states:** validator `RESULT: PASS — structure healthy` (0 broken links; 77 + 94 rule IDs);
citation check `RESULT: PASS — every cited path and ID resolves (REC-15)`.
**Git:** branch **`session-008`**, commits `e28a9f1`, `81da89d`, `38961c9`, `506c740`, `55ecd83`
(+ closing evidence commit) pushed to `origin`
(`https://github.com/mohaned733406131-byte/YUMN.git`). **`main` was not touched** — by directive.

## 2. Current truth (do not contradict)

- **66 open findings** across the seven audits: 14 consistency + 21 contradiction + 11 gap +
  7 hallucination + 6 critical + 7 requirement-validation (snapshot 2026-09-28,
  `analysis-validation.md` **v1.10** — register of record).
- Register versions: `consistency-audit.md` **v1.16** (14 OPEN · 14 RESOLVED; 31-check re-run still
  18/2/10 on the **479-file** session-006 snapshot — a fresh re-run is due before any gate claim),
  `contradiction-audit.md` **v1.6** (21 open), `missing-information.md` **v1.3** (11 open),
  `hallucination-audit.md` **v1.8** (7 open), `critical-findings.md` **v1.5** (6 open),
  `requirements-validation.md` **v1.1** (7 open), `analysis-validation.md` **v1.10** (66 open),
  `technical-debt.md` **v1.9** (**all `TD-01…TD-10` `PAID`**),
  `recommendations.md` **v1.10** (**assistant-side all `PAID`** — `REC-01…REC-10`, `REC-14`,
  `REC-15`; `REC-11…REC-13` remain sponsor-owned).
- Business rules: **104** across **15** domains (`business-rules.md` v1.1, `## INV` added);
  citation CI enforces ID/path discipline on every push/PR.
- Constraints: `C-01…C-26` (amended `C-05`/`C-06` as of session 007 — any further amendment only
  via `docs/README.md` §9 change control). Rules: **ADMR 2.2.0** + `YUMN_RULES.md` 94.
- Plan: `plan-develop.md` **v1.2 APPROVED** — `M-01…M-25` / `P-01…P-20` are **backlog items**, not
  `FR-*`; they convert only at their build wave (`SPE-03`/`D-02`). Approved ≠ implemented.
- Plan items deliberately **OPEN after approval**: `M-01` (`CT-23`/`GAP-14`), `M-04` (`CT-26`),
  `M-05` (`CT-28`), `M-06` (`CT-27`) — finance/security/owner review (`GEN-03`/`DOD-10`).
- **Gate 0 = `FAIL`**: `CRIT-01` (`ASM-14` unset) + `DEP-05`/`DEP-06`/`DEP-10` NOT STARTED.
  Nothing in `docs/` is `VERIFIED` — no implementation exists (`SPE-03`).
- `memory.md` §4: D-01/D-03/D-04/D-05/D-09/D-10/D-13/D-14/D-15/D-16 **RESOLVED**; D-02 PARTIAL;
  D-04 resolved session 008 (`BR-INV` registered); D-06, D-07, D-08, D-11, D-12 OPEN
  (D-11 = decision made, ADR deferred by design).
- `CHK-05` residual: 48 files without `## Change History` (40 UC, 6 `functional/FR-*`,
  `02-requirements/README.md`, `00-project-overview/README.md`) — re-verified session 008
  (UC-041/042 carry CH).
- `SEC-001…015` all open; secret scan BLOCKED (gitleaks absent); `origin/master` deletion pending
  default-branch switch on GitHub (needs a click or `gh` CLI — not available here).
- **Citation CI run UNVERIFIED:** the workflow is pushed, but the repo is private, the Actions page
  returns 404 unauthenticated, and no `gh` CLI exists here — the first real run must be confirmed in
  the GitHub UI and recorded honestly (never claimed PASS from this machine).

## 3. Next work queue (in priority order)

**A. Sponsor/finance/security dispositions (surface, never fake):** `REC-11` (`ASM-14` baselines,
re-score `ASM-03`/`ASM-04`/`ASM-12`), `REC-12` (`DEP-05` m-Floos/OneCash sandbox, `DEP-06`
SMS/WhatsApp contracts), `REC-13` (`DEP-10` Central Bank position before any B07 build); plan
items `M-01` (`CT-23` + `GAP-14`), `M-04` (`CT-26` pricing), `M-05` (`CT-28` security review),
`M-06` (`CT-27` payout cadence); `SEC-001…015` dispositions; `origin/master` deletion.

**B. Verify the pushed CI (honestly):** open the GitHub Actions UI for `docs-citations.yml` after
this push; record the first run's result in the session-009 work file (PASS/FAIL/UNVERIFIED —
whatever it actually is). Locally both checks are green; the runner is not.

**C. Pre-gate hygiene:** fresh **31-check consistency re-run** (corpus has grown past the
479-file snapshot; last result 18/2/10) before any gate claim; `CHK-05` residual is owned by the
48 documents themselves; install/locate gitleaks for the secret scan (still BLOCKED).

**D. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 → create
`docs/phases/bootstrap/` with the full artifact set — only after Gate 0 evidence exists.
Gate 0 stays `FAIL` (`CRIT-01`, `ASM-14`, `DEP-05/06/10`) until then.

## 4. Commands

```text
python senior-rules/validators/validate.py .     # must end PASS (77 + 94 rule IDs); run after EVERY change set
python tools/check_citations.py                  # must end PASS (REC-15 CI parity); run after EVERY change set
# queue-name acceptance scan (must stay 0 violations): parse register from
#   docs/06-backend/background-processing.md §1 first column (expect 30 entries), then scan
#   Get-ChildItem docs -Recurse -Filter *.md  excluding \20-validation\ + \21-completion\,
#   cut each file at its "## Change History" line, regex (?<![\w.-])b\d{2}\.[a-z0-9_]+(?:[._-][a-z0-9_]+)+,
#   SKIP tokens containing "_" (DB column refs), flag the rest if absent from the register.
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -10                                 # commit history (session-008 evidence)
```

## 5. PowerShell / editing gotchas (they cost real time — re-read before scripting)

- **NEVER name a PS function after an alias.** `function RD {…}` collided with `rd` (= `Remove-Item`)
  and **deleted 10 files** (session 006; recovered only because everything was committed).
  Use alias-safe names (`GetRaw`, `OutRaw`) and guard whole-file writes against `$null` content.
- **Double-quoted PS strings AND here-strings `@"…"@` consume backticks** — a `## Change History`
  row written through one lost its `` ` `` characters (`` `a `` became a BEL byte, U+0007), and a
  search pattern `` '99 `BR' `` written in double quotes becomes an unterminated-string parse error.
  Use **single-quoted here-strings** `@'…'@` / single-quoted patterns for markdown; scan for
  `CTRL[7]` after scripted writes.
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
- **Same-change-set propagation is easy to under-do:** session 008 found 7 count consumers of
  `business-rules.md` that the registration set missed, plus a traceability dashboard that predated
  sessions 003/004/007. After any count/registry change, grep for the *old* number repo-wide
  (excluding CH/evidence rows) before calling the set done.

## 6. Honesty rules in force

- Evidence tags on every non-obvious claim: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`.
- Findings are **never deleted** when closed — flip status + date (DOC-TPL-011 #3).
- Never cite an ID absent from its owning register (root README §11 `D-3`) — now CI-enforced by
  `tools/check_citations.py` on every push/PR (local runs still required before each commit).
- No dates/effort/sprints until `ASM-14` baselines exist (plan approval does not lift this).
- **Approval ≠ evidence:** `plan-develop.md` v1.2 being APPROVED never makes a gate PASS,
  never mints `FR-*`, never flips a finding to `VERIFIED` (DOD-10 / SPE-03 / GEN-03).
- **Pushed ≠ running:** the citation workflow's GitHub run is UNVERIFIED until seen in the UI.
- Every edited doc: version bump + `## Change History` row; propagation logged in
  `consistency-audit.md` §4; re-run audits, the validator, and the citation checker.
- Constraint amendments (`C-NN`) only via `docs/README.md` §9 change control (v bump + CH row + propagate).
- Rule changes: `core/00` §0.5 only (propose → edit → bump `VERSION` → `CHANGELOG` → validator) — never hot-patch.
  Factual corrections to adapter prose (counts, path spellings) do not change the pin (session 005/008 precedent).
- End the session by updating `session_track.md` (log + evidence + resume prompt) and `memory.md`
  if defects changed; author the session work file under `docs/sessions/` (SES-01).
- **Only push the session-named branch** (`session-009` next) — `main` is off-limits by directive.
