---
document_id: DOC-SR-012
title: SEC-REQ-012 — Vulnerability management
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-007, SEC-REQ-008, FR-020, NFR-009]
related_documents: [DOC-REQ-001, DOC-OVR-010]
---

# SEC-REQ-012 — Vulnerability management

> Registry summary (`requirements-overview.md` §3): SAST/DAST/dependency scanning in CI; critical vulns fixed ≤ 7 days.

**Priority:** High · **STRIDE:** Elevation of privilege (E), Tampering (T) · **Failure impact:** HIGH

## Description
Weaknesses are discovered continuously and closed within defined service levels: static analysis (SAST) and dependency/SCA scanning gate every CI run, dynamic scanning (DAST) runs against staging for each release, and known exploited or critical findings are fixed and verified within 7 days.

## Security rationale
The stack (Node 20, NestJS, Prisma — DEP-01) and third-party dependencies change frequently; without automated detection and a hard remediation clock, known CVEs accumulate until they are exploited against a platform holding real balances. Threat: exploitation of known weaknesses → STRIDE **Elevation of privilege** and **Tampering**.

## Requirement statements

- R1: CI executes SAST and dependency vulnerability scanning on every pull request; a build with a policy-violating finding (new critical/high exposure) fails and cannot merge.
- R2: DAST runs against the staging environment as part of the release pipeline; open critical findings block promotion to production.
- R3: Critical vulnerabilities are fixed and verified within **7 days** of confirmation (registry); non-critical severities follow a documented severity-SLA table in `09-security/` (`INFERENCE` for HIGH ≤ 30 days — exact thresholds beyond CRITICAL are a control-level policy decision).
- R4: Findings are recorded as `SEC-nnn` in `09-security/` and, where they threaten objectives, linked to `17-risk-management/risk-register.md` entries; remediation status is visible in a recurring report.
- R5: Base images and direct dependencies (DEP-01…DEP-04, DEP-07) receive a periodic upgrade review so scanning debt does not grow monotonically (`INFERENCE`).

## Acceptance criteria

- AC-SR012-01: Pipeline gate test — introducing a known-vulnerable dependency into a branch turns the CI security job red and blocks the merge.
- AC-SR012-02: Release gate test — a seeded critical DAST finding in staging prevents production promotion until resolved.
- AC-SR012-03: SLA evidence — a tracked critical finding shows confirmed date, fix date, and verification evidence, all within 7 days.
- AC-SR012-04: Reporting test — a monthly vulnerability report by severity is generated from scan output with zero silent suppressions lacking justification.

## Related IDs

`SEC-REQ-007` · `SEC-REQ-008` · `FR-020` · `NFR-009` · `NFR-010` · `C-18` · `C-21` · `DEP-01` · `RISK-003`

## Verification method

CI pipeline evidence (SAST/SCA gate runs and failure behavior), DAST scan reports per release, remediation-SLA record review, and report artifact inspection; findings catalogued in `09-security/`.

## Failure impact

**HIGH** — known vulnerabilities in the payment/auth path are directly exploitable against funded wallets; accumulated scan debt also blocks releases under the quality gate (NFR-009) and undermines the 99.99% availability target (C-26) when exploited.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
