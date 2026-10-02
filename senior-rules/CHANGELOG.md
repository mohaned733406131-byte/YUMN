Kimi
Co-authored with Senior Eng. Salah Alssayani — Taizz University, Alsaeed Faculty of Engineering & IT, Department of Software Engineering (eng.salahalssayani@gmail.com)
License: GPL-3.0
# CHANGELOG — AI Development Master Rules

Follows SemVer per core/00_meta_rules.md §0.5.

## [2.2.0] — 2026-09-28
- **Amendment F-07 (MINOR)**: `validators/validate.py` check 5 extended — rule-ID
  uniqueness is now enforced in **both** `RULES.md` (master catalog, 77 IDs) **and**
  `YUMN_RULES.md` (project catalog, 94 IDs across MNY/ESC/ORD/IDT/STK/SHP/RET/RTL/
  API/DAT/OPS/PRF/SPE). The check now also fails if zero IDs parse (silent-0 guard).
  Rationale: session-005 audit finding F-07 ("Validator checks ID uniqueness only in
  RULES.md") — proposed in the session-005 log, applied via this amendment, never a
  mid-task hot-patch. No rule text changed; `RULES.md` untouched.
- **Note (pre-existing drift, recorded not silently reconciled)**: `VERSION` read
  `2.0.0` while this changelog's latest entry was `[2.1.0]` — bumped straight to
  `2.2.0` above `[2.1.0]` rather than renumbering either record.

## [2.1.0] — 2026-09-24
- **Renamed**: all `.ai-rules` references replaced with `senior-rules` across all files (docs, validators, scripts, templates, package.json).
- **Added**: npm package `@salahalssayani/ai-development-master-rules` with automated installer (`npx admr-install`) — works with any AI model (Claude, GPT, Cursor, Gemini, Copilot, Windsurf, etc.).
- **Updated**: README.md and README.ar.md with npm installation section.

## [2.0.0] — 2026-09-20
Complete professional rebuild of the original rule set (Taizz University, Eng. Salah Alssayani).
- **Fixed**: all typos and garbled phrases ("flow of eb=vents", "sull testing", "wold ever",
  "CEM"); unified the rule voice to address the AI as "You".
- **Added**: numeric Definition of Done (DOD-01..10) with 9 gates; version-control
  discipline (VCS-01..05); secrets management (SEC-01); CI/CD gate enforcement;
  data migration + rollback (IMP-06); API versioning (IMP-07); dependency supply-chain
  scanning (SEC-06); backup/DR (SEC-09); PII redaction + retention in logs (LOG-02);
  fail-safe logging (LOG-03); performance budgets (DOD-07); rule versioning + amendment
  procedure + precedence order (GEN-07, core/00); BLOCKED-not-fake-done protocol (GEN-03);
  adapter pattern for framework-agnostic adoption (ADP-01..03, adapters/);
  automated validator (validators/validate.py); copy-ready templates (templates/).
- **Preserved**: every original rule intent — sessions & recovery, per-phase artifact set
  (a–u), no-dead-elements, real-backend CRUD, permissions matrices, relational activity
  logging, confirmation-modal-only UI, audit waves, ask-first clarification, doc roll-up
  linkage, technology recommendations, five-role completion review.

---

## Local patches (yumn repo — applied to this installed copy)

> No rule IDs, severities, or rule text were changed. These are tooling/signature fixes so the
> system's own validator can validate its own shipped files. Re-apply after any reinstall from
> `senior-implementation-rules-master/` (reinstall overwrites `senior-rules/`).

## [2026-09-27] — install-time fixes
- **Fixed** `scripts/admr-install.js`: unescaped backticks inside its AGENTS.md template literal broke parsing (SyntaxError) — escaped them; upstream defect.
- **Fixed** `scripts/admr-install.js`: first line now `// Kimi` (authorship signature); shebang converted to a comment — execute as `node scripts/admr-install.js`.
- **Extended** `validators/validate.py` `has_signature()`: accepts `// Kimi` for `.js/.mjs/.cjs/.ts` and `# Kimi` for `.gitignore/.gitattributes` (mirrors the existing `# Kimi` carve-out for `.py`). Stricter coverage, not looser.
- **Signed** `.gitignore` / `.gitattributes` with the `# Kimi` first line.
- **Caution**: never run `scripts/admr-install.js` with the working directory equal to the rules source directory (it renames `senior-rules/` to a backup before copying — source and target must differ).
