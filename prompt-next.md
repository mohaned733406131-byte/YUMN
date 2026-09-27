# prompt-next — Session 006 Handoff (the sweep + F-07 amendment)

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08`). Resume point: `session_track.md` session 005.
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-09-28, session 005 CLOSED)

The **rules-compliance audit** ran and its findings were remediated — `F-01…F-10` canonical table
in [`docs/phases/analysis/phase-audit.md`](docs/phases/analysis/phase-audit.md):

- **F-01** `docs/sessions/` created — `README.md` (DOC-SES-000) + session-001…004 reconstructed
  with provenance notes + session-005 authored.
- **F-02** all work from sessions 001–005 committed and pushed (grouped conventional commits,
  hashes in session-005 `# Commit evidence` + `session_track.md` row 005).
- **F-03** branch `master` → **`main`**; work branch **`session-005`** (both pushed;
  `origin/master` deleted).
- **F-04 / D-15** `docs/phases/` created — 16/16 CORE-03 artifacts + `_index.md` + `README.md`
  (`DOC-PHA-001…018`). This **reversed** the earlier "leave phase folder as-is" decision per the
  user's "create all folder or file that require" instruction (logged in `memory.md` §4).
- **F-05 / D-10** PARTIAL — `docs/README.md` v1.2 citations made honest; `archdoc.md` content
  still absent (sponsor: restore or drop). New related defect **`D-16`**: 0-byte `describ.md`.
- **F-06** rule-count claims 77 → **94** corrected in `all_in_one_track.md` + `session_track.md`.
- **F-07** **OPEN** — validator checks ID uniqueness only in `RULES.md` (77), not
  `YUMN_RULES.md` (94). Amendment proposed via `core/00` §0.5; manual check 94/94 unique.
- **F-08** terminal sessions now named (`session-005`).
- **F-09 / F-10** unchanged: `SEC-001…015` all open; 69 audit findings; Gate 0 `FAIL`.

**Last validator state:** `RESULT: PASS — structure healthy` (0 broken links, 77 rules).
**Registrations landed:** `naming-conventions.md` v1.3 (`PHA`/`SES` codes + process-folder row),
`consistency-audit.md` v1.10 (§4 propagation row for the session-005 change set),
`RULES_HINTS.md` §4 `SEC-001…SEC-016` → `SEC-001…SEC-015` (factual correction, pin stays 2.0.0).

## 2. Current truth (do not contradict)

- **69 open findings** across the seven audits (unchanged by session 005):
  16 consistency + 15 contradiction + 12 gap + 11 hallucination + 8 critical + 7 requirement-validation.
- Register versions: `consistency-audit.md` **v1.10** (15/2/14 checks; 16 OPEN · 9 RESOLVED),
  `contradiction-audit.md` **v1.3**, `critical-findings.md` **v1.3**, `analysis-validation.md`
  **v1.4**, `hallucination-audit.md` **v1.2**, `requirements-validation.md` **v1.1**,
  `requirements-to-tests.md` **v1.3**, `technical-debt.md` **v1.7** (`TD-07…10` PAID;
  `TD-01…03` OPEN), `recommendations.md` **v1.7** (`REC-03…09` PAID; `REC-01/02/10…15` remain).
- The full 31-check re-run was **explicitly deferred** in `consistency-audit.md` §4 (row
  2026-09-28) — it is part of this session's sweep, not silently skipped.
- Queue register = 30 rows; names `{block}.{entity}.{action}` (BR-PLT-01).
- **Gate 0 = `FAIL` today**: `CRIT-01` (`ASM-14` unset) + `DEP-05`/`DEP-06` NOT STARTED.
  Nothing in `docs/` is `VERIFIED` — no implementation exists (`SPE-03`).
- `memory.md` §4: D-01/D-03/D-05/D-09/D-13/D-14/D-15 RESOLVED; D-02 PARTIAL; D-10 PARTIAL;
  D-04, D-06…D-08, D-11, D-12, D-16 OPEN.
- Phase 0 artifacts now exist: `docs/phases/analysis/_index.md` (16/16);
  `development_phases_entry.md` phase-0 evidence points there.

## 3. Next work queue (in priority order)

**A. THE SWEEP (carried over — root README §9.4/§9.5 + `20-validation/README.md` §4 rule 7):**

1. **Re-run all seven audits fresh** — counts are snapshots and have drifted (session 005 added
   24 files: `docs/sessions/` 6, `docs/phases/` 18). Take new numbers from the files.
2. **Add the six deferred findings** (evidence-tagged, severity, owner, `OPEN`, version bump +
   `## Change History` row in each owning register; never delete when later closed — DOC-TPL-011 #3):
   - (a) Moderator read conflict: `07-api/endpoints/admin.md` `API-ADM-024` / `API-ADM-022` vs
     `09-security/rbac.md` rows 22/24 (Moderator denied) + `UC-036`.
   - (b) J10 audit-chain cadence: "Hourly" vs "nightly" (grep `J10`).
   - (c) `BR-PRM-07` orphan citation at `02-requirements/…/content.md:59` (no such rule ID).
   - (d) `ipHash` vs `ip` ambiguity: `admin.md:125` vs `audit_log` entity.
   - (e) `API-TOP` phantom group — 4 files (real group: `API-WAL-003`).
   - (f) D-02 AC text-drift half — `HAL-05`/`RVF-04`/`CRIT-05` already open; re-verify only.
3. **Re-sync cross-references** + propagation row + `python senior-rules/validators/validate.py .` → PASS.

**B. F-07 amendment:** extend `senior-rules/validators/validate.py` ID-uniqueness to also scan
`YUMN_RULES.md` (or add an adapter-level check) via `core/00` §0.5 amendment procedure —
log it in the amendment log; do not hot-patch silently.

**C. Remaining assistant-side recommendations:** `REC-01`, `REC-02`, `REC-10`, `REC-14`, `REC-15`
(`TD-01…03` open; `REC-15` = CI enforcement — no CI exists yet).

**D. Sponsor-owned Gate 0 blockers** (surface, don't fake): `REC-11` (`ASM-14`),
`REC-12` (`DEP-05`/`DEP-06`), `REC-13` (`DEP-10`); plus `D-10`/`D-16` (restore vs drop) and
`SEC-001…015` dispositions.

**E. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 → create
`docs/phases/bootstrap/` with the full artifact set — only after B/C dispositioned.

## 4. Commands

```text
python senior-rules/validators/validate.py .          # must end PASS; run after EVERY change set
# queue-name acceptance scan (must stay 0 violations): parse register from
#   docs/06-backend/background-processing.md §1 first column (expect 30 entries), then scan
#   Get-ChildItem docs -Recurse -Filter *.md  excluding \20-validation\ + \21-completion\,
#   cut each file at its "## Change History" line, regex (?<![\w.-])b\d{2}\.[a-z0-9_]+(?:[._-][a-z0-9_]+)+,
#   SKIP tokens containing "_" (DB column refs), flag the rest if absent from the register.
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -10                                 # commit history (session-005 evidence)
```

## 5. PowerShell / editing gotchas (they cost real time — re-read before scripting)

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
- End the session by updating `session_track.md` (log + evidence + resume prompt) and `memory.md`
  if defects changed; author the session work file under `docs/sessions/` (SES-01).
