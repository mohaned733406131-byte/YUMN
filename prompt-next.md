# prompt-next — Session 003 Handoff

> **AI ASSISTANT: read this file first, then `senior-rules/ENTRY.md` + `senior-rules/RULES_HINTS.md`
> (confirm `senior-rules/VERSION` pin per `GEN-08`). Resume point: `session_track.md` session 002.
> Rules validator must end green: `python senior-rules/validators/validate.py .`
> (`python3` is NOT available; never run `senior-rules/scripts/admr-install.js` from repo root.)**

---

## 1. Where we left off (2026-09-27, session 002 CLOSED)

All three tasks of the original mandate are **done**:

1. **Knowledge base understood** — full analysis of `docs/` (24 domains, 68 requirements,
   99 BRs, 277 ACs, 221 endpoints, 18 entities) recorded across `memory.md`,
   `mind_map.md`, `all_in_one_track.md`.
2. **Rule system adopted** — `senior-rules/` installed (ADMR 2.0.0, local patches logged in
   `senior-rules/CHANGELOG.md`), adapter `RULES_HINTS.md` filled, 77 project rules in
   `YUMN_RULES.md` (13 families), root `AGENTS.md` wired.
3. **D-01/D-14 resolved** — the three missing domains were authored (user disposition: author,
   don't amend): `19-traceability/` (3 files), `20-validation/` (8), `21-completion/` (8);
   registrations synced (root `docs/README.md` §5 `AUD-NN` row, `naming-conventions.md` v1.1,
   `validation-audit-template.md` v1.1); seam findings 20/23/25 closed.

**Last validator state:** `RESULT: PASS — structure healthy` (0 broken links, 77 unique rule IDs).

## 2. Current truth (do not contradict)

- Canonical defect registers now live **inside** `docs/`:
  - `docs/20-validation/` — `AUD-01…07` files; `GAP-01…12`, `CT-01…20` (`CT-01` PASS, rest OPEN),
    `HAL-01…13`, `CRIT-01…10`, `RVF-01…07`, consistency findings 1–25 (20 OPEN, 5 RESOLVED).
  - `docs/21-completion/` — `TD-01…10` (`TD-10` PAID), `REC-01…15` (`REC-09` paid), Gates 0–3.
- **81 open findings** across the six audits (20 consistency, 19 contradiction, 12 gap,
  13 hallucination, 10 critical, 7 requirement-validation).
- **Gate 0 = `FAIL` today**: `CRIT-01` (sponsor baselines `ASM-14` unset) + `DEP-05`/`DEP-06`
  NOT STARTED. Nothing in `docs/` is `VERIFIED` — no implementation exists (`SPE-03`).
- `memory.md` §4 rows D-02…D-04, D-06…D-13 remain **OPEN** — they mirror audit findings;
  rule `SPE-03` forbids claiming any of them done without evidence.

## 3. Next work queue (in priority order)

**A. P0 knowledge-base repairs** (paired `TD-NN` → `REC-NN`, each with a testable acceptance
criterion in `docs/21-completion/recommendations.md`):

1. `REC-03` — author or retract `TC-104…TC-114` (11 absent files; unblocks `AC-S-03`).
2. `REC-04` — close FR ↔ AC drift: add 14 missing `AC-FRnnn-05` references (or amend registry).
3. `REC-05` — health-path canon: one spelling (`/healthz`+`/readyz` per `BR-PLT-07`) across
   `07-api/endpoints/admin.md`, TC-001/031/057/065; log in `CT-02`/`CT-03`.
4. `REC-06` / `REC-07` / `REC-08` — queue register merge, role cross-layer mapping,
   stale "not yet authored" stub rows.

**B. Sponsor-owned Gate 0 blockers** (cannot be done by the assistant — surface, don't fake):
`REC-11` (`ASM-14` baselines), `REC-12` (`DEP-05`/`DEP-06` or written decision), `REC-13`
(`DEP-10` Central Bank position before any B07 build).

**C. After every change set** (root README §9): version bump + `## Change History` row in each
touched doc, propagate impacted IDs, record the sweep in
`20-validation/consistency-audit.md` propagation log, re-run all seven audits, re-run the
rules validator.

**D. Then** implementation bootstrap per `development_phases_entry.md` Gate 0 (repo skeleton,
CI, Prisma schemas `b01…b13`) — only after A lands and B are dispositioned.

## 4. Commands

```text
python senior-rules/validators/validate.py .        # must end PASS
node --check senior-rules/scripts/admr-install.js   # syntax check only; do not RUN install
dir docs\13-testing\test-cases                      # verify TC inventory (103 vs 114)
```

## 5. Honesty rules in force

- Evidence tags on every non-obvious claim: `VERIFIED` / `INFERENCE` / `INSUFFICIENT EVIDENCE`.
- Findings are **never deleted** when closed — flip status + date (DOC-TPL-011 #3).
- Never cite an ID absent from its owning register (root README §11 `D-3`).
- No dates/effort/sprints until `ASM-14` baselines exist.
- End the session by updating `session_track.md` (status row + log + evidence + resume prompt)
  and `memory.md` if defects changed.
