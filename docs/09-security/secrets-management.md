---
document_id: DOC-SEC-005
title: Secrets Management Policy
category: 09-security
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: false
related_requirements: [SEC-REQ-002, SEC-REQ-006, SEC-REQ-007, SEC-REQ-012]
related_documents: [DOC-SEC-001, DOC-SEC-006, DOC-SEC-007, DOC-SR-007, DOC-OVR-008, DOC-OVR-010]
---

# Secrets Management (`SEC-REQ-007`)

Policy for every secret yumn holds: what exists, where it lives, who may read it, how often it rotates, and what happens when one leaks. Requirement statements and acceptance criteria are in `../02-requirements/core/SEC-REQ-007.md`; this is the design.

## 1. Principles

1. **Runtime injection only** — every secret is read from environment variables / `env_file` at process start; no literal appears in source code, fixtures, Docker images, or committed Compose files (`${VAR}` indirection only) (`SEC-REQ-007` R1, `C-22`).
2. **Fail fast, fail quiet** — missing required secret ⇒ startup aborts with a non-sensitive error; no default, fallback, or example credential is ever used (R3).
3. **Never echo** — secrets never reach logs, errors, traces, client bundles, or `/metrics` labels (R4, cross `SEC-REQ-002` R2, `SEC-REQ-006` R5).
4. **Scan the repo** — CI secret scanning on every change; a seeded credential fails the pipeline and blocks merge (R2, `AC-SR007-01`).
5. **Rotate deliberately** — periodic rotation plus immediate rotation on suspected compromise or staff departure (R5).

## 2. Secret Inventory

| # | Secret class | Examples | Storage (v1) | Rotation cadence | Compromise impact |
|---|---|---|---|---|---|
| S-01 | JWT signing material | RS256 private key (+ public JWKS) | env file, host-only permissions | **90 days** (`INFERENCE`) + immediate on suspicion | Forged access tokens → impersonation (`SEC-REQ-003`) |
| S-02 | Database credentials | PostgreSQL app role, migrations role | env file per service | **90 days** (`INFERENCE`) | Full data read; write limited by append-only privileges |
| S-03 | Redis credentials | cache/session/queue ACL password | env file | **90 days** (`INFERENCE`) | Session registry & rate-limit manipulation |
| S-04 | Wallet provider merchant credentials | m-Floos / OneCash merchant key + secret (`DEP-05`) | env file, adapter-scoped | per provider contract; review **quarterly** (`INFERENCE`) | Initiate/verify fraudulent top-ups; forge API calls |
| S-05 | Webhook HMAC signing secrets | provider callback secret, DLR secret, WhatsApp verify token (`INT-REQ-006`) | env file | **on rotation of provider secret**; dual-secret grace period if supported (`INFERENCE`) | Forge "payment success" → fake wallet credit (`TM-08`) |
| S-06 | SMS provider API keys | primary + secondary provider keys (`DEP-06`) | env file | per contract; review **quarterly** (`INFERENCE`) | OTP hijack, SMS fraud, OTP interception at volume |
| S-07 | WhatsApp Business credentials | Business API token, template webhook secret (`DEP-06`) | env file | per Meta policy; review **quarterly** (`INFERENCE`) | Notification hijack, brand abuse |
| S-08 | Push credentials | FCM service account, APNs `.p8` key | env file | **yearly** (Apple key limit) / per Google policy (`INFERENCE`) | Spam/fake push to users; low financial impact |
| S-09 | Object-storage credentials | MinIO root + app access/secret keys (`DEP-07`) | env file | **90 days** (`INFERENCE`) | KYC document / image exposure (`A-07`) |
| S-10 | Bank-transfer portal credentials | bank web-portal login for statement checks (`INT-REQ-002` reconciliation) | env file (ops-only) | per bank policy; **on staff departure** | Statement access → PII/amount exposure; no credit authority |
| S-11 | TLS private keys | CDN/edge certificate (`DEP-08`) | edge/CDN config, never in repo | per certificate expiry, monitored with pre-expiry alert (`SEC-REQ-006` R4) | MITM of OTP/token traffic |
| S-12 | Encryption keys (at-rest / field-level) | data keys, key-encryption key | env / key service outside DB (`SEC-REQ-002` R3) | **annually** or on algorithm change (`INFERENCE`) | Readable PII/financial columns (see `data-protection.md`) |
| S-13 | CI/CD secrets | registry tokens, scan-tool tokens, deployment SSH keys | GitHub Actions secrets | **90 days** + on personnel change (`INFERENCE`) | Pipeline compromise → supply chain (`SEC-REQ-012`) |
| S-14 | Observability credentials | Grafana/Alertmanager admin, Prometheus remote-write token | env file | **90 days** (`INFERENCE`) | Alert suppression, metric tampering |

No other secret classes may be introduced without adding a row here (inventory completeness is checked at review).

## 3. Storage Model — v1 Under `C-22` and the Roadmap

**v1 (chosen): Docker Compose `env_file` + host filesystem permissions.**

| Aspect | Design |
|---|---|
| Layout | `.env` / `env.<environment>` files on the host, referenced by Compose as `${VAR}` / `env_file:` — never copied into images, never committed |
| Git hygiene | `.gitignore` blocks `.env*`, `*.pem`, `*.key`, `*.p12`, `credentials.json`, `service-account*.json`; CI secret scan backstops any miss (`SEC-REQ-007` R2) |
| File mode | `0600`, owned by the deployment user; secrets directory excluded from backups that are shared broadly |
| Separation | Distinct values per environment — `dev`, `staging`, `production` share **no** credential; sandbox provider keys are never valid in production and vice versa |
| Justification | `C-22` mandates Docker Compose with **no Kubernetes in v1**, and `NFR-016` forbids cloud-vendor lock-in; a vault product would add an unowned service, new failure mode, and secret-injection complexity disproportionate to a single-host deployment. Secrets remain outside code, images, and git — the core of `SEC-REQ-007` — while the deployment stays inside its constraints |

**Roadmap (`INFERENCE`, not a v1 commitment):** when the platform moves beyond single-host (allowed by `NFR-018`'s scale-out path), adopt an OS-level secrets manager (e.g., Docker secrets / a self-hosted vault) with automated rotation. Until then, rotation is a documented manual runbook (§7) executed by the ops owner.

## 4. No Secrets in Logs / Errors / Client

| Rule | Enforcement design |
|---|---|
| Structured logging allowlist | Log payloads are built from whitelisted fields; credentials, OTP codes, password material, HMAC signatures, and full tokens are excluded by construction (`SEC-REQ-002` R4, `SEC-REQ-007` R4) |
| Error responses | API error model never includes internal messages or headers; stack traces are internal-only (`07-api` error model, `SEC-REQ-008`) |
| Metrics labels | Label allowlist — service/endpoint/status/queue only; no phone numbers, no secrets (`INT-REQ-007` security section) |
| Provider adapters | The only code allowed to hold provider signing logic (`INT-REQ-008`); normalized errors never echo credential material |
| Client bundles | Server-side rendering + env exposure whitelist — `NEXT_PUBLIC_*`-style prefixed vars are forbidden for any secret (`INFERENCE`, framework convention) |
| Verification | Automated log/trace scrub test across a full auth + top-up run (`AC-SR007-04`) |

## 5. Access-to-Secrets Matrix

| Secret class | App (api/worker) | DevOps / ops owner | Engineering (repo) | Provider (external) |
|---|---|---|---|---|
| S-01 JWT signing key | ✔ (private key, api only) | ✔ (issues/rotates) | ✖ (never in repo) | — |
| S-02 / S-03 DB & Redis | ✔ (app role only) | ✔ | ✖ | — |
| S-04 wallet provider keys | ✔ (payment adapter only) | ✔ | ✖ | holds counterpart |
| S-05 webhook secrets | ✔ (webhook verifier only) | ✔ | ✖ | holds counterpart |
| S-06 / S-07 SMS/WhatsApp keys | ✔ (notification adapter only) | ✔ | ✖ | holds counterpart |
| S-08 push credentials | ✔ (notification adapter only) | ✔ | ✖ | FCM/APNs console |
| S-09 MinIO keys | ✔ (media module) | ✔ | ✖ | — |
| S-10 bank portal creds | ✖ (ops task, human) | ✔ | ✖ | bank portal |
| S-11 TLS keys | ✖ (edge terminates) | ✔ | ✖ | CA/CDN (`DEP-08`) |
| S-12 encryption keys | ✔ (via key service, not raw) | ✔ (custody) | ✖ | — |
| S-13 CI/CD secrets | ✖ | ✔ (GitHub settings) | ✖ | GitHub |
| S-14 observability creds | ✖ (internal network) | ✔ | ✖ | — |

Rules: least privilege per adapter (a compromise of the notification module must not yield payment keys); human-held secrets (S-10) are never pasted into tickets, chat, or code review (`INFERENCE`).

## 6. CI Enforcement

| Gate | Behavior | Canon |
|---|---|---|
| Secret scanning on every PR | Seeded canary credential ⇒ build fails, merge blocked | `AC-SR007-01`, `SEC-REQ-007` R2 |
| Repository audit scan | Zero credential literals in code, Compose files, fixtures, docs | `AC-SR007-03` |
| Startup fail-fast test | Removing a required env var ⇒ non-sensitive startup failure | `AC-SR007-02` |
| Dependency/SAST scan | Complements secret scan; critical findings block merge | `SEC-REQ-012` R1 |

## 7. Incident Rotation Runbook (outline)

Trigger: leaked credential, suspected compromise, personnel departure, or scheduled cadence breach.

1. **Detect** — CI scan hit, provider anomaly alert, or report. Record time and suspected exposure scope.
2. **Contain** — revoke/rotate the exposed secret **first**, verify old value is rejected (provider-side revoke where available).
3. **Issue** — generate new value; distribute via host env files only; restart affected services rolling (health-gated, `BR-PLT-07`).
4. **Verify** — smoke test the dependent flow (auth refresh, top-up initiate, OTP send) on staging then production.
5. **Assess** — for S-04/S-05/S-06: check provider logs for abuse since suspected exposure; for S-01: force session revalidation if key retired; freeze wallet activity if money paths are implicated (`BR-PAY-09`).
6. **Audit** — write a `BR-PLT-06` audit entry (secret class, reason, operator — never the value) and note it in the vulnerability/finding report (`SEC-REQ-012` R4).
7. **Review** — post-incident: was the cadence sufficient, was logging clean, did CI catch it? Update this document (version bump + Change History).

## 8. Verification Summary

| Control check | Method |
|---|---|
| No credential in repo | CI scan + repository audit (`AC-SR007-01/03`) |
| Fail-fast startup | Deployment-pipeline startup test (`AC-SR007-02`) |
| No secret in logs/traces | Automated scrub test over auth + top-up run (`AC-SR007-04`) |
| Environment separation | Config review: dev/staging/prod credential sets are disjoint |
| Rotation runbook works | Tabletop drill per rotation class (planned in `13-testing/`) |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
