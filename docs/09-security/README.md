---
document_id: DOC-SEC-001
title: Security Domain — Overview, Posture & File Index
category: 09-security
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-30
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-001, SEC-REQ-002, SEC-REQ-003, SEC-REQ-004, SEC-REQ-005, SEC-REQ-006, SEC-REQ-007, SEC-REQ-008, SEC-REQ-009, SEC-REQ-010, SEC-REQ-011, SEC-REQ-012]
related_documents: [DOC-ROOT-001, DOC-REQ-001, DOC-SR-000, DOC-BA-005, DOC-OVR-007, DOC-OVR-008]
---

# 09 — Security Domain Overview & File Index

## 1. Purpose

This directory is the **design response** to the 12 security requirements (`SEC-REQ-001…SEC-REQ-012`) registered in `02-requirements/requirements-overview.md` §3. The requirement files state *what must hold, testably*; this domain states *how the design makes it hold*: threat model, authentication design, authorization matrix, secrets policy, encryption design, control catalog, and the findings register (`SEC-001…SEC-015`).

Nothing here is implemented yet — every control carries status `DESIGNED`. Implementation placement lives in `06-backend/` (`DOC-BE-003` authentication, `DOC-BE-004` authorization); environment/CI specifics live in `14-devops-infrastructure/`.

---

## 2. Security Posture Summary

yumn is a **custodial wallet platform for real money** (YER) inside a modular monolith (`C-21`) deployed with Docker Compose (`C-22`), Arabic-first (`C-24`), with no card rails (`C-02`) and no email channel (`BR-NTF-01`, `GAP-03`). That shape drives the posture:

| Posture driver | Consequence for security design |
|---|---|
| Wallet-only payments + escrow (`C-01`, `C-12`) | **Financial fraud is the primary threat class** — double-credit, ledger tampering, refund abuse, and account takeover end in money movement that cannot be clawed back (BR-PAY-07 refunds are wallet-internal only) |
| Phone is the sole identity anchor (`C-06`, `BR-AUTH-01`) | SIM-swap, OTP interception and OTP pumping are first-class threats; SMS availability is an authentication availability property (`SEC-REQ-001` R5) |
| Single deployment host, no WAF/K8s in v1 (`C-22`) | Rate limiting and abuse control must live in the application (Redis, `DEP-03`), not in infrastructure |
| One codebase, 7 roles, 4 surfaces (`FR-002`) | Server-side deny-by-default authorization (`SEC-REQ-004`) is the single most leveraged control |
| Append-only ledger (`DATA-REQ-007`) | Immutability is enforced by database permissions + hash-chained audit (`SEC-REQ-010`), not by convention |
| Third-party providers hold money/OTP paths (`DEP-05`, `DEP-06`) | Webhook authenticity (`INT-REQ-006`) and secrets custody (`SEC-REQ-007`) are security-critical, not just integration concerns |

### Threat priority ranking (design focus)

| # | Threat class | Why it ranks here | Primary controls |
|---|---|---|---|
| 1 | Account takeover (OTP/SIM/reset paths) | Direct route to funded wallets | `SEC-REQ-001`, `SEC-REQ-003`, `SEC-REQ-005` — `authentication.md` |
| 2 | Wallet double-credit / ledger tampering | Irreversible money loss | `SEC-REQ-010`, `BR-PAY-03/05/06/08`, `DATA-REQ-007` — `threat-model.md` TM-03/TM-04 |
| 3 | Privilege escalation / admin abuse | Refunds, KYC, payouts, role changes | `SEC-REQ-004`, `SEC-REQ-010` — `rbac.md` |
| 4 | Forged or replayed provider webhooks | Forged callback = fake credit | `INT-REQ-006`, `SEC-REQ-007` — `webhook-reliability.md` |
| 5 | OTP/SMS pumping and app-layer DoS | Cost + availability (`C-25`, `C-26`) | `SEC-REQ-009`, `SEC-REQ-005` — `security-controls.md` |
| 6 | Stored XSS in Arabic/RTL user content | Session theft, admin compromise | `SEC-REQ-008`, `SEC-REQ-011` — `security-controls.md` |
| 7 | Delivery-code fraud (no-GPS flow) | Theft of delivered goods | `SEC-REQ-005`, `C-16`, `BR-SHP-03` — `threat-model.md` TM-06 |
| 8 | Secrets exposure in git/logs/images | Game-over regardless of other controls | `SEC-REQ-007` — `secrets-management.md` |
| 9 | PII/KYC leakage (PDPA-aligned, `DEP-09`) | Reportable breach, loss of trust | `SEC-REQ-002`, `SEC-REQ-006` — `data-protection.md` |
| 10 | Known-vulnerability accumulation | Exploitable against funded wallets | `SEC-REQ-012` — `security-controls.md` |

---

## 3. File Index

| # | Filename | DOC ID | Purpose | Source of truth |
|---|---|---|---|---|
| 1 | `README.md` | DOC-SEC-001 | This file — posture, index, conventions | Yes |
| 2 | `threat-model.md` | DOC-SEC-002 | Assets, trust boundaries, STRIDE per boundary, top threats TM-01…TM-11 with mitigations and residual risk | Yes |
| 3 | `authentication.md` | DOC-SEC-003 | Security design of FR-001: OTP lifecycle, password policy, JWT architecture, sessions, lockout, MFA decision | No |
| 4 | `rbac.md` | DOC-SEC-004 | Definitive role × capability permission matrix for the 7 actors; ownership and admin-console controls | Yes |
| 5 | `secrets-management.md` | DOC-SEC-005 | Secret inventory, storage under `C-22`, rotation cadences, access matrix, incident rotation runbook | No |
| 6 | `data-protection.md` | DOC-SEC-006 | TLS, at-rest and field-level encryption, hashing, OTP/delivery-code storage, log masking, backup encryption | No |
| 7 | `security-controls.md` | DOC-SEC-007 | Control catalog `SEC-C-01…SEC-C-24` × SEC-REQ × layer × status × verification; rate-limit budgets | Yes |
| 8 | `security-findings.md` | DOC-SEC-008 | Findings register `SEC-001…SEC-015`, all status OPEN | Yes |
| [`core/`](core/README.md) | DOC-SEC-009 | Core portal folder — shared, platform-wide material for this domain (not specific to a single portal) |
| [`admin/`](admin/README.md) | DOC-SEC-010 | Admin portal folder — admin-console-specific material (platform operators) |
| [`vendor/`](vendor/README.md) | DOC-SEC-011 | Vendor portal folder — vendor-portal-specific material (sellers) |
| [`customer/`](customer/README.md) | DOC-SEC-012 | Customer portal folder — customer-app-specific material (buyers) |
| [`delivery/`](delivery/README.md) | DOC-SEC-013 | Delivery portal folder — delivery/courier-app-specific material (couriers) |

---

## 4. Coverage Map — SEC-REQ → Primary Document

| Requirement | Primary design document(s) | Supporting |
|---|---|---|
| SEC-REQ-001 Strong phone verification | `authentication.md` | `threat-model.md` TM-01/TM-02, `security-controls.md` |
| SEC-REQ-002 Credential storage | `data-protection.md` | `authentication.md`, `security-controls.md` |
| SEC-REQ-003 Token security | `authentication.md` | `threat-model.md` TM-01, `security-controls.md` |
| SEC-REQ-004 Server-side authorization | `rbac.md` | `threat-model.md` TM-05/TM-07, `security-findings.md` |
| SEC-REQ-005 Brute-force protection | `authentication.md` | `security-controls.md` (rate budgets), `threat-model.md` |
| SEC-REQ-006 Transport & data encryption | `data-protection.md` | `security-controls.md` |
| SEC-REQ-007 Secrets management | `secrets-management.md` | `data-protection.md` (keys), `security-controls.md` |
| SEC-REQ-008 Injection/XSS/CSRF | `security-controls.md` | `threat-model.md` TM-09 |
| SEC-REQ-009 Rate limiting & abuse | `security-controls.md` | `authentication.md`, `10-integrations/` |
| SEC-REQ-010 Audit trail integrity | `security-controls.md` | `rbac.md`, `threat-model.md` TM-04 |
| SEC-REQ-011 File upload security | `security-controls.md` | `data-protection.md`, `../10-integrations/core/bank-transfer-topup.md` |
| SEC-REQ-012 Vulnerability management | `security-controls.md` | this register, `17-risk-management/` |

---

## 5. ID & Naming Conventions

| Kind | Pattern | Example | Meaning |
|---|---|---|---|
| Security requirements | `SEC-REQ-NNN` | `SEC-REQ-005` | Owned by `02-requirements/` — never redefined here |
| Security controls | `SEC-C-NN` | `SEC-C-07` | Design controls catalogued in `security-controls.md` |
| Security findings | `SEC-NNN` | `SEC-004` | Register entries in `security-findings.md` — status `OPEN` until verified closed |
| Threats | `TM-NN` | `TM-03` | Threat-model entries in `threat-model.md` |
| Business rules cited | `BR-<DOMAIN>-NN` | `BR-AUTH-04` | Defined only in `01-business-analysis/business-rules.md` |

**Severity scale** (root README §8): `CRITICAL` · `HIGH` · `MEDIUM` · `LOW` · `INFORMATIONAL`.
**Control status:** `DESIGNED` for every control in v1.0 — *no control is `IMPLEMENTED` or `VERIFIED` because no code exists yet* (root README §6).
**Evidence tags:** `VERIFIED` (direct project evidence) · `INFERENCE` (logically derived) · `INSUFFICIENT EVIDENCE` (pending — e.g., PDPA detail awaiting `DEP-09`).

---

## 6. Reading Order

| Audience | Read |
|---|---|
| Security engineer | DOC-SEC-001 → `threat-model.md` → `rbac.md` → `security-controls.md` → `security-findings.md` |
| Backend developer | `authentication.md` → `../06-backend/core/authentication.md` (`DOC-BE-003`) → `rbac.md` → `../06-backend/core/authorization.md` (`DOC-BE-004`) |
| Payments engineer | `threat-model.md` TM-03/TM-04 → `data-protection.md` → `../10-integrations/core/webhook-reliability.md` |
| Ops / DevOps | `secrets-management.md` → `data-protection.md` (keys, backups) → `14-devops-infrastructure/` |
| Auditor / reviewer | `security-controls.md` (coverage vs all 12 SEC-REQs) → `security-findings.md` → `13-testing/` |

---

## 7. Domain Boundaries

**Owned here:** security design, control catalog, RBAC matrix (definitive), secrets policy, encryption design, findings register.
**Not owned here:** requirement statements and acceptance criteria (`02-requirements/`, `AC-SRnnn-nn`); code-level enforcement placement (`06-backend/`); endpoint contracts (`07-api/`); CI pipeline mechanics (`14-devops-infrastructure/`); test cases (`13-testing/`); risk linkage (`17-risk-management/risk-register.md`, `RISK-nnn`).
**Cross-domain contracts:** integration security controls are specified jointly with `10-integrations/` (webhook HMAC, provider secrets, SMS abuse limits) — requirements stay in `02-requirements/`, contracts in `10-integrations/`, security policy here.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-30 | Portal partition: registered five portal-folder READMEs (`core/` `admin/` `vendor/` `customer/` `delivery/`, DOC-SEC-009…DOC-SEC-013) in Contents | Owner directive session 011 (`prompt-011.md` §4 phase 5): five portal subfolders in every `01…23` (naming-conventions §1 portal partition) |
