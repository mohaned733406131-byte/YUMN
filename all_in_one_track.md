# all_in_one_track — Roll-up Index (DOC-04)

Every tracking file in one place. No orphan documents: each row links to a live file; if a link
dies, fix it in the same commit (DOC-04/DOC-05).

## Rule system (binding)

| File | Purpose |
|---|---|
| [senior-rules/ENTRY.md](senior-rules/ENTRY.md) | Master rule file — read first, always |
| [senior-rules/RULES.md](senior-rules/RULES.md) | Master rule catalog (GEN…ADP) |
| [senior-rules/RULES_HINTS.md](senior-rules/RULES_HINTS.md) | yumn adapter: stack, commands, paths, overrides |
| [senior-rules/YUMN_RULES.md](senior-rules/YUMN_RULES.md) | yumn project rules (MNY…SPE, **94** rules — count corrected 2026-09-28, session 005) |
| [senior-rules/CHANGELOG.md](senior-rules/CHANGELOG.md) · [VERSION](senior-rules/VERSION) | Rule version control |
| [AGENTS.md](AGENTS.md) | AI instruction to read ENTRY.md before work |

## Session & phase tracking

| File | Purpose |
|---|---|
| [session_track.md](session_track.md) | Session ledger, resume points, resume prompts (SES-02/04) |
| [docs/sessions/](docs/sessions/README.md) | Session work files `session-001…007` with evidence (SES-01) |
| [development_phases_entry.md](development_phases_entry.md) | Phase status, Gate 0 state (DOC-01/02) |
| [memory.md](memory.md) | Durable facts + known-defect register (DOC-01) |
| [mind_map.md](mind_map.md) | Repository navigation (DOC-01) |
| [architecture.md](architecture.md) | Canonical architecture pointer (DOC-01) |
| [docs/phases/](docs/phases/README.md) | Per-phase artifact sets — **phase 0 `analysis/` 16/16 created 2026-09-28 (session 005)**; Phase 1 folder when scheduled |

## Knowledge base (analysis source of truth)

| File | Purpose |
|---|---|
| [docs/README.md](docs/README.md) | Master index, reading order, ID conventions, source-of-truth map |
| [docs/00-project-overview/project-charter.md](docs/00-project-overview/project-charter.md) | Executive summary, constraints baseline |
| [docs/02-requirements/requirements-overview.md](docs/02-requirements/requirements-overview.md) | Canonical registry of all 68 requirement IDs |
| [docs/01-business-analysis/business-rules.md](docs/01-business-analysis/business-rules.md) | Canonical registry of 99 `BR-*` rules |
| [docs/07-api/README.md](docs/07-api/README.md) | API contract (221 endpoints) |
| [docs/08-database/database-overview.md](docs/08-database/database-overview.md) | Database structure (schemas `b01…b13`) |
| [docs/13-testing/README.md](docs/13-testing/README.md) | Testing strategy + test cases |

## Open items that gate the next phase

Tracked in [memory.md](memory.md) §Known defects and — canonically — in
[docs/20-validation/](docs/20-validation/README.md) (`CRIT-NN`, `CT-NN`, `HAL-NN`, `GAP-01…GAP-14`)
plus [docs/21-completion/recommendations.md](docs/21-completion/recommendations.md) (`REC-NN`).
Domains `19/20/21` were authored 2026-09-27 (resolved); `TC-104…114` authored (resolved, session 003);
FR↔AC `-05` references added (resolved, session 004 — AC *text-drift* half still open under `HAL-05`/`RVF-04`).
Change-control sweep completed (session 006): 31-check re-run 18/2/11 on 479 files, deferred findings
(a)–(f) filed (finding 26, `CT-21`, `CT-22`, `HAL-15` new), F-07 fixed (`validate.py` covers both rule
catalogs, `VERSION` 2.2.0). `describ.md` reconciled + `plan-develop.md` **v1.2 APPROVED** and propagated
at the analysis layer (session 007): constraint amendments `C-05`/`C-06`, `DOC-SA-011`, rbac §11,
register dispositions (`CT-24`/`CT-25`/`GAP-02`/`GAP-03`/`GAP-13`/`HAL-15` → `RESOLVED`), roll-up
**72 open**.
Still open: money-path enum drift (`D-06`/`SPE-04`), API-promised storage (`D-07`), the `ORD-08` race (`D-12`),
72 audit findings, plan items `M-01`/`M-04`/`M-05`/`M-06` (`CT-23`/`CT-26`/`CT-27`/`CT-28`, `GAP-14`),
sponsor baselines (`ASM-14`), `DEP-05`/`DEP-06`, Gate 0 (`CRIT-01`).
Rule `SPE-03` forbids claiming any of these as done.
