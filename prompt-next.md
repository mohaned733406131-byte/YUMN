# prompt-next — Session 008 Handoff (plan items disposition, then remaining pay-downs)

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08` — now **2.2.0**). Resume point: `session_track.md` session 007.
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-09-28, session 007 CLOSED)

`describ.md` was reconciled, `plan-develop.md` was **APPROVED**, and the approval was implemented at
the **analysis layer only** — session file:
[`docs/sessions/session-007-describ-reconciliation.md`](docs/sessions/session-007-describ-reconciliation.md) (DOC-SES-007, v1.1).

- **`describ.md` reconciliation:** sponsor §1–§8 checked against canon → contradictions **`CT-23`…`CT-30`**,
  gaps **`GAP-13`/`GAP-14`** registered; `describ.md` restored from 0-byte → **`D-16` `RESOLVED`**;
  `UC-041`/`UC-042` authored + registered.
- **REC pay-downs:** `REC-02`, `REC-10`, `REC-14` → **PAID** (`recommendations.md` **v1.8**,
  `technical-debt.md` **v1.8**).
- **`plan-develop.md` → v1.2 APPROVED (2026-09-28, administrator).** Decisions `D1`…`D11` recorded with
  Outcome column; §0.4 mint record; ERP departmental coverage §4.2; inline decision **`D-11`** in
  `decision-log.md` v1.1 (ADR-011 stays reserved for multi-host deployment).
- **Analysis-layer implementation of the approval:** `project-constraints.md` **v1.1** (`C-05`
  +Al-Kuraimi Bank/Jeeb → verify `API-WAL-003/004`; `C-06` +optional *verified* profile email — never
  identifier/OTP), `project-scope.md` **v1.2** (OUT rows, GAP dispositions, **APPROVED BACKLOG** pointer),
  `requirements-overview.md` **v1.1** (§7 pointer — **no `FR-*` minted**, `SPE-03`/`D-02`), new
  **`docs/03-system-analysis/erp-finance-departments.md` (`DOC-SA-011`)** + 03 README **v1.2**,
  `rbac.md` **v1.2 §11** (`ORG-01…08`, `ROLE-01…07`+`ROLE-09` minted; `ROLE-08`/`10`/`11` document-local),
  `19-traceability/README.md` **v1.1** (`F-06` → `RESOLVED`), phantom `API-TOP` → `API-WAL-003/004` at
  `functional-analysis.md:167` + `constraint-tests.md:84` (**`HAL-15` 3-site fix**, → `RESOLVED`).
- **Register dispositions + roll-up:** `contradiction-audit.md` **v1.6** (`CT-24`/`CT-25` → `RESOLVED`,
  `CT-29` → `RESOLVED`-NO; `CT-23`/`CT-26`/`CT-27`/`CT-28` stay OPEN annotated → **21 open**),
  `missing-information.md` **v1.3** (`GAP-02`/`GAP-03`/`GAP-13` → `RESOLVED` → **11 open**),
  `hallucination-audit.md` **v1.5** (`HAL-15` → `RESOLVED` → **10 open**),
  `consistency-audit.md` **v1.12** (§4 propagation row), `analysis-validation.md` **v1.6** → **72 open**.
- **Trackers:** `session_track.md` row 007 `CLOSED` + log + resume → 008; `sessions/README.md` **v1.4**
  (row 007 `CLOSED`); session file **v1.1**; `memory.md` session-007 snapshot; this file → 008.

**Last validator state:** `RESULT: PASS — structure healthy` (0 broken links; 77 + 94 rule IDs).
**Git:** branch **`session`**, remote `origin` = `https://github.com/mohaned733406131-byte/YUMN.git`
(commits pushed with governing IDs).

## 2. Current truth (do not contradict)

- **72 open findings** across the seven audits: 15 consistency + 21 contradiction + 11 gap +
  10 hallucination + 8 critical + 7 requirement-validation (snapshot 2026-09-28, `analysis-validation.md` **v1.6**).
- Register versions: `consistency-audit.md` **v1.12** (15 OPEN · 13 RESOLVED; 31-check re-run still
  18/2/11 on 479 files — a fresh re-run is due before any gate claim), `contradiction-audit.md`
  **v1.6** (21 open), `missing-information.md` **v1.3** (11 open), `hallucination-audit.md` **v1.5**
  (10 open), `critical-findings.md` **v1.3** (8 open), `requirements-validation.md` **v1.1** (7 open),
  `analysis-validation.md` **v1.6** (72 open), `technical-debt.md` **v1.8** (`TD-01…03` OPEN),
  `recommendations.md` **v1.8** (`REC-01`, `REC-11…13`, `REC-15` remain).
- Constraints: `C-01…C-26` (amended `C-05`/`C-06` as of session 007 — any further amendment only via
  `docs/README.md` §9 change control).
- Rules: **ADMR 2.2.0** (pin in `RULES_HINTS.md` §1) + `YUMN_RULES.md` 94.
- Plan: `plan-develop.md` **v1.2 APPROVED** — `M-01…M-25` / `P-01…P-20` are **backlog items**, not
  `FR-*`; they convert only at their build wave (`SPE-03`/`D-02`). Approved ≠ implemented.
- Plan items deliberately **OPEN after approval**: `M-01` (`CT-23`/`GAP-14`), `M-04` (`CT-26`),
  `M-05` (`CT-28`), `M-06` (`CT-27`) — finance/security/owner review (`GEN-03`/`DOD-10`).
- **Gate 0 = `FAIL`**: `CRIT-01` (`ASM-14` unset) + `DEP-05`/`DEP-06`/`DEP-10` NOT STARTED.
  Nothing in `docs/` is `VERIFIED` — no implementation exists (`SPE-03`).
- `memory.md` §4: D-01/D-03/D-05/D-09/D-13/D-14/D-15/D-16 RESOLVED; D-02 PARTIAL; D-10 PARTIAL;
  D-04, D-06…D-08, D-11, D-12 OPEN (D-11 = decision made, ADR deferred by design).
- `CHK-05` residual: 48 files without `## Change History` (40 UC, 6 `functional/FR-*`,
  `02-requirements/README.md`, `00-project-overview/README.md`).
- `SEC-001…015` all open; secret scan BLOCKED (gitleaks absent); `origin/master` deletion pending
  default-branch switch on GitHub (needs a click or `gh` CLI — not available here).

## 3. Next work queue (in priority order)

**A. Sponsor/finance/security dispositions (surface, never fake):** `M-01` (`CT-23` + `GAP-14` —
Al-Kuraimi API/merchant-of-record legal review), `M-04` (`CT-26` — pricing/discounts sign-off),
`M-05` (`CT-28` — security review of KYC/OTP/deletion), `M-06` (`CT-27` — payout-minimum/cadence
owner decision). Also still sponsor-owned: `REC-11` (`ASM-14`), `REC-12` (`DEP-05`/`DEP-06`),
`REC-13` (`DEP-10`); `SEC-001…015` dispositions; `origin/master` deletion.

**B. Remaining assistant-side:** `REC-01`, `REC-15` (`TD-01…03`; `REC-15` = CI enforcement — **no CI
exists**, must be built or honestly marked blocked); optional `docs/10-integrations` settings /
`configuration.md` §5.3 settings groups (finance/tax/invoice/ERP — plan §8 `D3`).

**C. Pre-gate hygiene:** fresh 31-check consistency re-run before any gate claim (drift since 479-file
snapshot — corpus has grown); `CHK-05` residual is owned by the 48 documents themselves.

**D. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 → create
`docs/phases/bootstrap/` with the full artifact set — only after Gate 0 evidence exists.
Gate 0 stays `FAIL` (`CRIT-01`, `ASM-14`, `DEP-05/06/10`) until then.

## 4. Commands

```text
python senior-rules/validators/validate.py .          # must end PASS (77 + 94 rule IDs); run after EVERY change set
# queue-name acceptance scan (must stay 0 violations): parse register from
#   docs/06-backend/background-processing.md §1 first column (expect 30 entries), then scan
#   Get-ChildItem docs -Recurse -Filter *.md  excluding \20-validation\ + \21-completion\,
#   cut each file at its "## Change History" line, regex (?<![\w.-])b\d{2}\.[a-z0-9_]+(?:[._-][a-z0-9_]+)+,
#   SKIP tokens containing "_" (DB column refs), flag the rest if absent from the register.
node --check senior-rules/scripts/admr-install.js     # syntax check only; do NOT run install
git log --oneline -10                                 # commit history (session-007 evidence)
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
- No dates/effort/sprints until `ASM-14` baselines exist (plan approval does not lift this).
- **Approval ≠ evidence:** `plan-develop.md` v1.2 being APPROVED never makes a gate PASS,
  never mints `FR-*`, never flips a finding to `VERIFIED` (DOD-10 / SPE-03 / GEN-03).
- Every edited doc: version bump + `## Change History` row; propagation logged in
  `consistency-audit.md` §4; re-run audits and the validator.
- Constraint amendments (`C-NN`) only via `docs/README.md` §9 change control (v bump + CH row + propagate).
- Rule changes: `core/00` §0.5 only (propose → edit → bump `VERSION` → `CHANGELOG` → validator) — never hot-patch.
- End the session by updating `session_track.md` (log + evidence + resume prompt) and `memory.md`
  if defects changed; author the session work file under `docs/sessions/` (SES-01).
