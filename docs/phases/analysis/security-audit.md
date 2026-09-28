---
document_id: DOC-PHA-011
title: Security Audit & Specifications — analysis phase
category: phases
status: approved
version: 1.0
created: 2026-09-28
updated: 2026-09-28
author: analysis-agent
source_of_truth: false
related_documents: [DOC-SEC-001, DOC-SEC-004, DOC-SEC-005]
related_requirements: [SEC-REQ-001, SEC-REQ-004, SEC-REQ-007, SEC-REQ-011]
---

# Security Audit & Specifications — analysis phase

## Purpose
CORE-03 item 9 / `SEC-04`: threat model, attack surface, findings, mitigations for the phase. Canonical spec: [`docs/09-security/`](../../09-security/README.md) — this artifact is the **phase-level roll-up**, not a copy (`SPE-01`).

## Scope
Analysis-phase attack surface = the *designed* system: 221 endpoints (`07-api/`), 18 entities (`08-database/`), 4 external integrations (`10-integrations/`), 5 shells (web ×3, mobile ×2).

## Threat model (roll-up)
- Canonical: [`threat-model.md`](../../09-security/threat-model.md) (STRIDE-classified, per-entry-point).
- Controls catalogue: [`security-controls.md`](../../09-security/security-controls.md); requirements: `SEC-REQ-001`…`SEC-REQ-012` (`02-requirements/security/`).
- Secrets: [`secrets-management.md`](../../09-security/secrets-management.md) — host-only, mode `0600`, fail-fast `CONFIG_MISSING: <name>` (`SEC-REQ-007`, `OPS-02`).

## Findings (phase security audit)

Register: [`security-findings.md`](../../09-security/security-findings.md) — **`SEC-001`…`SEC-015`, every one `OPEN`** (design-level, raised during this analysis):

| Severity | Count | IDs |
|---|---|---|
| CRITICAL | 1 | `SEC-011` (sole auth channel uncontracted — `DEP-06`) |
| HIGH | 4 | `SEC-001` (SMS-only recovery), `SEC-004` (SIM-swap on OTP/delivery code), `SEC-012` (single-factor privileged login), `SEC-015` (escrow release TOCTOU) |
| MEDIUM | 8 | `SEC-002`, `SEC-003`, `SEC-005`, `SEC-006`, `SEC-007`, `SEC-008`, `SEC-010`, `SEC-014` |
| LOW | 2 | `SEC-009`, `SEC-013` |

**DOD-06 status: NOT MET for this phase** — 1 CRITICAL + 4 HIGH open. Honest reporting per DOD-10: phase 0 closes with these findings *tracked and owned*, not dismissed; they are Gate-0/Gate-1 blockers (`phase-audit.md` §2).

## Mitigations (design commitments, enforced in code later)
- Deny-by-default, server-side authorization (`IDT-05`, P2), ownership → 404/403 (`SEC-REQ-004`).
- Constant-time webhook compare + IP allowlist + replay window (`MNY-13`, `INT-REQ-006`).
- Rate limits per tier (`API-04`), OTP/lockout policy (`IDT-03/06`), upload hardening (`API-06`).
- Append-only financial/audit stores with DB-role grants (`MNY-04`, `AC-SR010-01`).
- PII AES-256 at rest + lookup hash; log redaction (`IDT-02`, `LOG-02`, `SEC-05`).

## Preconditions / postconditions
Preconditions: `DEP-05`/`DEP-06` contracts (Gate 0). Postconditions: findings resolved to 0 open CRITICAL/HIGH **before** the phase that implements auth/payments closes (`AUD-02`: zero CRITICAL/HIGH open at phase close).

## Dead-element / secrets check (analysis-phase surface)
- Secrets in repo: **0** (no `.env*`, `*.pem`, `*.key` in tree; `.gitignore` covers `.env`/`.env.*` with `!.env.example`).
- Forbidden UI calls: **0** (validator §6).

## Open questions (COM-01)
1. `SEC-010` (CORS unspecified) and `SEC-014` (key rotation) need owner + ADR before implementation.
2. `SEC-012`: is OTP-at-login mandated for privileged roles? Canon ambiguity — decide before coding `b01` auth.

## Change History

| Date | Version | Change | Author |
|---|---|---|---|
| 2026-09-28 | 1.0 | Initial creation (CORE-03 item 9 / SEC-04, session 005) | analysis-agent |
