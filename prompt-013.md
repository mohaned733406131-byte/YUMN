# Session-013 continuation prompt — finish session-011 phases 8–10, then stand by for session-012

> **DO NOT run `sudo node senior-rules/scripts/admr-install.js`** — it installs to `/root` and is unusable.
> Read `ENTRY.md` → `AGENTS.md` → `RULES_HINTS.md` first. Load relevant skills before substantive work
> (at minimum `documentation-knowledge-base`; add `05_quality_assurance`, `09_risk_management`,
> `master-entry-orchestrator` / `stakeholder-communication-reporter` as the phase fits).

This prompt continues **session-011** (prompt-012 phases 8–10) from a verified handoff. Everything in
§2 was re-verified in the session that produced this file. Everything in §3–§5 is unfinished.

---

## 1. Binding scope (inherited from prompt-012 — read `prompt-012.md` in full before starting)

- **Primary mission:** advance session-011 per `prompt-012.md` §1–§6 through phases 8, 9, 10.
  Prompt-012's phase plans (its §3 item 4, §4, §5) and the deferred §7 ("queue session-012") are
  superseded **only** by the concrete inventories below, which are more current.
- **session-012 SaaS-blueprint analysis: queue only, do NOT start.** Owner files
  YUMN_Prompt.md / YUMN_Requirment.md remain read-only and surface-inspected only.
- Hard rules unchanged: gates green after every change set (`python senior-rules/validators/validate.py .`
  and `python tools/check_citations.py` — **`python3` is not available**); same-change-set discipline
  (version bump + `## Change History` row + `consistency-audit.md` §4 row per edited doc);
  Gate 0 stays FAIL; no new UCs/BRs/FRs beyond DOC-OVR-012; sponsor items surfaced, never
  dispositioned; dangling citations get an explicit phase-9 disposition, never a silent waiver;
  report red gates red; commit `session-011` only — never `main`; never `git add` skill packs or
  owner files without explicit owner instruction; **multi-agent work uses parallel subagents with
  declared IDs, disjoint file sets, report-don't-commit, and every claim re-verified by the
  orchestrator.**

---

## 2. Verified handoff state (re-verified 2026-10-02 — trust these numbers; re-check if you doubt them)

### 2.1 Git

- Branch `session-011` @ `f58759b`, ahead of origin by 14 commits. `main` untouched at `c9ff07c`.
- Working tree at handoff: modified `docs/20-validation/core/consistency-audit.md` (**v1.21, phase-8
  item 1 — UNCOMMITTED**) plus untracked `prompt-013.md` (this file), `YUMN_Prompt.md`,
  `YUMN_Requirment.md`, `pro-skills-senior-full-stack-software-engineer-master/`.
  `delegate-skills-master/` is gone from disk (never tracked).

### 2.2 Gates at handoff (raw output, verbatim)

```
=== validator ===
=== Structure & gate validation ===
Scanning: .
...
RESULT: PASS — structure healthy
```

```
=== check_citations ===
(citation gate output: FAIL — 17 dangling paths; 1003 files scanned;
 27345 ID citations, 0 unresolved IDs)
dangling list (17): 14 owner paths in YUMN_Prompt.md, 1 prompt-012.md →
delegate-skills-master/CONTRIBUTING.md, 2 consistency-audit.md:144/:147
evidence quotes (test-cases/README.md, user-fills.md)
```

Full raw citation output (with exact file:line tokens) is preserved in `prompt-012.md` §2.2 —
**re-run the gate to regenerate it; do not treat any PASS/FAIL above as memory-backed evidence for
your session file.** Expected steady state before phase 9c: validator PASS, citation FAIL with
exactly these 17 dangling paths (this file adds none: dead paths above appear only as plain text,
never backticked — the checker only path-checks backticked `.md`/`.py` tokens).

### 2.3 Counts (re-verified this sitting)

| Metric | Truth |
|---|---|
| UC files | **420**, contiguous; next free = UC-421 (per UC Inventory) |
| Requirements | **73** (20/20/16/9/8 — `requirements-overview.md:19`) |
| Business rules | **111** rows (15 domains) |
| AC registry | **273** = 269 rows + 4 XCUT |
| Test cases | **114** |
| Endpoints / entities / ADRs | 221 / 18 / ADR-001…010 all ACCEPTED |
| Rules | ADMR 2.2.0, YUMN_RULES 94 |
| docs markdown | 986 `docs/**/*.md` (checker scans 1003) |
| Findings | **65 open**, Gate 0 = FAIL, nothing VERIFIED, citation-CI UNVERIFIED |

⚠ **Known count conflict:** AC↔UC raw grep this sitting = **1594** occurrences vs sweep cell
**1591** (delta likely CH/evidence rows). Reconcile in phase 9 and publish ONE number everywhere.

### 2.4 Checker mechanics (tools/check_citations.py — verified)

- Path check: only backticked tokens ending `.md`/`.py`; skips NNN, globs, `<`/`{`/`http`.
  Tail-boundary fallback for prefix matches. Existence = repo-relative resolution, untracked files
  appear absent to it in practice (owner-file tokens dangle).
- ID check scans **every line, including code fences**; only "next free" FORWARD_LINE lines are
  exempt. Never write a not-yet-minted ID (e.g. a GAP row you have not created yet).
- Disposition hook: `PHANTOM_PATHS` at ~line 103 = set of `(citing-file-relpath, token)` pairs,
  each needing a justifying comment. Phase 9c registers the true-phantom pairs here (or documents
  an owner-surface justification) — never a silent waiver.

### 2.5 Sweep (chk31) + phase-8 walk status

- chk31_v3.py ran over 986 files: **20 PASS / 2 PWF / 9 FAIL** → findings 6,7,8,11,14,15,16,21,22
  (already written into consistency-audit §4 as v1.21). Script lives in the temp opencode dir
  (temp path, un-backticked on purpose): if it is gone, rebuild from the session-009/010 pattern —
  31 checks, accept exactly 10 verdicts (9 FAIL + 1 PWF), re-run after the fix wave for a fresh
  verdict and re-map any FAIL that no longer reproduces.
- Phase-8 item 2 walk (BETA) found these **unclosed** gaps — all verified:
  1. **C-27** appears only in `system-expansion-proposal.md` (live hits :415/:422/:477/:478/:493;
     :170–179/:213 = UC-27x false positives) — no register row. Decide mint-vs-alternative.
  2. **YUMN_RULES §7 rule-text defer** — no PENDING row in missing-information.
  3. `system-expansion-proposal.md:412` claims a webhook reliability doc that **EXISTS**
     (`docs/10-integrations/core/webhook-reliability.md`) — stale negative claim; proposal
     frontmatter is v1.0 → bump to 1.1 + CH row when fixed.
  4. Phase-8 item 3 done (use-case-index v1.3 @ `c78490b`); item 4 survey done — inventory below.
  5. `docs/sessions/README.md` has no 011 row yet — expected, phase 10.

---

## 3. Remaining work — Phase 8 closure (the fix wave)

Apply the four waves below as **parallel subagents with declared IDs, strictly disjoint file sets,
report-don't-commit**; the orchestrator re-verifies every claim, edits `consistency-audit.md`
(v1.21 → v1.22 + §4 row) and runs gates after each change set. Every edited doc gets version bump +
`## Change History` row in the same change set.

### Wave A — domain READMEs (agent A)

- `docs/01-business-analysis/README.md` :34/:35/:36/:45/:48/:73 — stale `use-cases/`/`workflows/`
  refs → correct portal paths; "104 BR" → **111**; :73 index-maintenance numbers.
- `docs/13-testing/README.md` :85/:86/:95/:156 — stale counts/paths.
- `docs/18-decisions/README.md` :19/:35/:47 — stale paths/counts.

### Wave B — traceability + validation (agent B; largest item)

- `docs/19-traceability/core/requirements-to-tests.md` — **65 stale-path occurrences**
  (21+17+27 blocks; mostly plain text, which is why the gate never caught them) → rewrite to live
  paths; verify each target exists before/after.
- `docs/20-validation/core/requirements-validation.md:36` — stale path.
- `docs/20-validation/core/missing-information.md:101` — stale path.

### Wave C — decisions housekeeping (agent C)

- `docs/18-decisions/core/decision-log.md` :17 — bare `ADR/` prose → concrete ADR paths (ADRs live in
  `docs/18-decisions/` — verify actual filenames first).
- `decision-log.md:78` stale RESERVED note — re-sync proven against
  `docs/04-architecture/core/architecture-decisions-reference.md:110`.

### Wave D — orchestrator-only (cross-file decisions, do NOT delegate)

- `system-expansion-proposal.md:412` stale webhook claim + v1.0→1.1 bump (item 2.3 above).
- **C-27 disposition:** decide mint-two-GAP-rows vs documented alternative. If minted, roll up the
  open-findings total 65 → 67 with full propagation (consistency-audit, session file, memory);
  re-check every roll-up site listed in prompt-012 §6 before choosing.
- **§7 rule-text defer** → PENDING row in missing-information (same roll-up decision).
- The 2 evidence-quote dangling paths at consistency-audit :144/:147 → phase 9c disposition.

### Cross-cutting count/range fixes (after waves A–C, orchestrator)

- `docs/22-glossary/core/naming-conventions.md:92` — stale GAP-01…GAP-12 range → current register range;
  `:150` entities path.
- `docs/phases/analysis/test-plan.md:33` — "277 rows" claim vs **114 TC** truth — verify what it
  actually counts before editing.
- Group B leftovers from the survey (≈126 live stale hits total across the waves — re-grep to
  confirm closure; do not declare done on agent say-so).

---

## 4. Phase 9 — verification & closure

1. Re-run chk31 (or rebuilt equivalent) → fresh verdict table; re-map the 9 FAILs (close or carry
   with explicit disposition; findings are never deleted when closed).
2. Gates: validator must PASS; citation gate — run full, then **phase 9c disposition of the 17
   dangling paths**: register true-phantom `(file, token)` pairs in `PHANTOM_PATHS` with
   justifications and/or mark owner-file tokens as owner-surface; record the split in the session
   file. Target: citation gate green with a documented, non-silent disposition — if it stays red,
   report it red with the reason.
3. Reconcile 1594 vs 1591 AC↔UC count; publish one number.
4. gitleaks: directory scan + `gitleaks git` — report as "triaged allowlist, 2 benign fixtures".
5. UC inventory spot check = 420 files contiguous.
6. CI check: run honestly, record actual result, else leave **UNVERIFIED** (never upgrade).
7. Re-run both gates after every change set (DOD-10).

---

## 5. Phase 10 — session close

1. `docs/sessions/session-011-*.md` (DOC-SES-011) with **raw** gate outputs — run the gates to
   capture them; never quote from memory (DOD-10).
2. `docs/sessions/README.md` row 011 (v1.7 → v1.8 + CH row).
3. `session_track.md` row 011 → CLOSED, resume pointer → 012.
4. `memory.md` snapshot: 420 UC / 73 requirements / 111 BR / 273 AC / 114 TC / Gate 0 FAIL /
   65 (or 67, if Wave D mints) open findings / citation-CI status as measured.
5. `prompt-next.md` → session-012 uses `prompt-012.md` (SaaS-blueprint analysis, queue-only rule).
6. Grouped conventional commits on `session-011` with governing IDs; push `session-011` only.
   Do not commit owner files or skill packs.

---

## 6. Gotchas (carry-overs — these bit previous sessions)

- `python3` does not exist; use `python`. PowerShell: no `grep`/`import` in execute code; wrong
  `Select-String -Path` throws — locate with `Get-ChildItem docs -Recurse -Filter <name>` first.
- Portal layout traps: `business-rules.md`, `acceptance-criteria.md`, `requirements-overview.md`
  live at **domain root, not `core/`**; `architecture-decisions-reference.md` is at
  `docs/04-architecture/core/`, not `18-decisions/`.
- Temp dir for scratch: `C:\Users\Mohanned\AppData\Local\Temp\opencode` (approved).
- CRLF/here-string/backtick traps in PowerShell; alias-named function hazard.
- Same-change-set discipline and gates-after-every-change-set are non-negotiable (§1).
- Honesty: red gates red, PASS only from fresh output, findings carried not deleted, sponsor items
  surfaced, no new UCs/BRs/FRs beyond DOC-OVR-012.






When carrying out the work, I also need you to follow `prompt-013.md`. Additionally, I want to clarify the following:
1- The work should follow the style used in the `command.md` file.
2- The structure—including folders and subfolders—should remain the same. Regarding files, please group them by section within a folder named after that section (e.g., place administration-related files in an "administration" folder, core system files in a "core" folder, and client-related files in a "client" folder).
 03-requirements 
  data
    core
    admin
    vinder
    customer
    delevery
    shared
    index.md
  funictional   
    admin
    vinder
    customer
    delevery
    shared
    index.md

This ensures the analysis is structured and organized, with each section containing the relevant files or associated information. Additionally, focus on implementing the specifications outlined in the `YUMN_Prompt.md` and `YUMN_Requirment.md` files, while adhering to the established plan, phased approach, and `senior-rules` guidelines. (Filename fix session-013: the original owner text used hyphenated names YUMN-Prompt.md and YUMN-Requirment.md; the files on disk use underscores. Citation gate corrected to the real names.)
