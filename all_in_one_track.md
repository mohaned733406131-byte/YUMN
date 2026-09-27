# all_in_one_track — Roll-up Index (DOC-04)

Every tracking file in one place. No orphan documents: each row links to a live file; if a link
dies, fix it in the same commit (DOC-04/DOC-05).

## Rule system (binding)

| File | Purpose |
|---|---|
| [senior-rules/ENTRY.md](senior-rules/ENTRY.md) | Master rule file — read first, always |
| [senior-rules/RULES.md](senior-rules/RULES.md) | Master rule catalog (GEN…ADP) |
| [senior-rules/RULES_HINTS.md](senior-rules/RULES_HINTS.md) | yumn adapter: stack, commands, paths, overrides |
| [senior-rules/YUMN_RULES.md](senior-rules/YUMN_RULES.md) | yumn project rules (MNY…SPE, 77 rules) |
| [senior-rules/CHANGELOG.md](senior-rules/CHANGELOG.md) · [VERSION](senior-rules/VERSION) | Rule version control |
| [AGENTS.md](AGENTS.md) | AI instruction to read ENTRY.md before work |

## Session & phase tracking

| File | Purpose |
|---|---|
| [session_track.md](session_track.md) | Session ledger, resume points, resume prompts (SES-02/04) |
| [development_phases_entry.md](development_phases_entry.md) | Phase status, Gate 0 state (DOC-01/02) |
| [memory.md](memory.md) | Durable facts + known-defect register (DOC-01) |
| [mind_map.md](mind_map.md) | Repository navigation (DOC-01) |
| [architecture.md](architecture.md) | Canonical architecture pointer (DOC-01) |
| `docs/phases/<slug>/` | Per-phase artifact set — **not yet created** (begins Phase 1) |

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
[docs/20-validation/](docs/20-validation/README.md) (`CRIT-NN`, `CT-NN`, `HAL-NN`, `GAP-01…GAP-12`)
plus [docs/21-completion/recommendations.md](docs/21-completion/recommendations.md) (`REC-NN`).
Domains `19/20/21` were authored 2026-09-27 (resolved); open: FR↔AC rewrites,
declared-but-absent test cases (`TC-104…114`), money-path enum drift, sponsor baselines (`ASM-14`).
Rule `SPE-03` forbids claiming any of these as done.
