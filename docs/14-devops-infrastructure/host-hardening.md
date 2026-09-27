---
document_id: DOC-OPS-008
title: Single-Host Hardening & Vulnerability Management
category: 14-devops-infrastructure
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-006, SEC-REQ-007, SEC-REQ-012, SEC-REQ-009, NFR-016]
related_documents: [DOC-OPS-001, DOC-OPS-003, DOC-OPS-006, DOC-SEC-005, DOC-NFD-004, DOC-OVR-010]
---

# Single-Host Hardening & Vulnerability Management

One Docker host per environment (`C-22`) means **the host is the security perimeter** for everything not terminated at the edge. This document covers OS-level hygiene, network exposure, Docker daemon practices, TLS, log integrity, scanning cadence, and where incident response lives. Control catalogue and threat model stay in `09-security/`.

## 1. OS Patching Cadence

| Item | Policy | Owner |
|---|---|---|
| Base OS | LTS Linux (Ubuntu LTS / Debian stable class); in-place `unattended-upgrades` for security patches | ops owner |
| Security patches (OS) | **Automated within 24 h** of publication; reboot-required patches applied in the maintenance window (`DOC-DPL-003` §4) | ops owner |
| Kernel / critical CVE | **≤ 7 days** aligned with `SEC-C-24` SLA; emergency out-of-window patch allowed with a P4 deploy record | ops owner |
| Docker engine + CLI | Monthly review; upgrade in the maintenance window | ops owner |
| Container base images | Weekly digest-bump PRs (`dependency-audit.yml`); CRITICAL CVE ⇒ immediate rebuild | CI + engineering |
| Node 20 / npm packages | Weekly Dependabot/Renovate PRs; CRITICAL ≤ 7 days, HIGH ≤ 30 days (`SEC-C-24`) | engineering |
| Data-service images (PG/Redis/ES/MinIO) | Monthly patch review; **major** upgrades are planned migrations, not in-place bumps | ops owner |
| Patch evidence | Monthly record: applied packages, reboot time, downtime vs budget | ops owner |

## 2. SSH & Remote Access Policy

| Rule | Setting |
|---|---|
| Authentication | **Key-only**; `PasswordAuthentication no`, `PermitRootLogin no`, `KbdInteractiveAuthentication no` |
| Accounts | Named human accounts with individual keys; **no shared accounts**; key removed on staff departure (same trigger as secret rotation, `DOC-SEC-005` §2) |
| Production access | Via **bastion/jump host or VPN** (`INFERENCE`); direct SSH to the production host from the internet is denied at the firewall. Where a bastion is not yet deployed, SSH is restricted to a static IP allowlist as the interim control |
| Staging/dev | VPN or IP allowlist; direct exposure permitted for the engineering network only |
| Local development | No SSH — developer machines run their own Compose stack (`DOC-OPS-002`) |
| MFA | SSH certificate or hardware-key MFA at the bastion where the provider supports it; **no MFA on the admin console in v1** — see `15-deployment/production-readiness.md` §Security for the recorded decision |
| Commands | Sudo limited to the ops role; full session logging (`script`/auditd) with 90-day retention (`RC-02`) |
| Failed logins | `fail2ban`-class rate limiting; alerts on burst (feeds `SEC-REQ-009` abuse control) |
| Emergency break-glass | One sealed, offline root key held by the ops owner; use is a `BR-PLT-06`-recorded event and triggers a key rotation afterwards |

## 3. Firewall & Port Exposure

**Host firewall (ufw/iptables-class) default policy: deny inbound, allow outbound.**

| Port | Protocol | Source | Applies to | Purpose |
|---|---|---|---|---|
| 80 | TCP | 0.0.0.0/0 (redirect → 443) | staging, prod | HTTP→HTTPS redirect (`DEP-08`) |
| 443 | TCP | 0.0.0.0/0 | staging, prod | TLS traffic to `edge` (`SEC-REQ-006`) |
| 22 | TCP | VPN/bastion IP allowlist **only** | all | SSH (§2) |
| 5432 (postgres) | TCP | **internal Docker network only** — not published | all | Prisma (`C-19`) |
| 6379 (redis) | TCP | internal only | all | cache/BullMQ (`C-20`) |
| 9200 (elasticsearch) | TCP | internal only | all | search (`DEP-04`) |
| 9000/9001 (minio) | TCP | internal only | all | objects (`DEP-07`) |
| 9090/3000/9093 (prom/grafana/alertmanager) | TCP | internal + SSH tunnel / IP-allowlisted `edge` location | staging, prod | observability UI |
| 8025 (sms-sink) | TCP | dev network only | local, dev | payload inspection |
| Ephemeral (outbound) | TCP | 0.0.0.0/0 outbound | all | providers (SMS, WhatsApp, m-Floos, OneCash), registry, off-host backup |

**Invariant:** in production the only internet-facing inbound ports are **80 and 443** (`DOC-OPS-003` §7). Any new published port requires a security review and a change to this table.

Additional host controls:

| Control | Setting |
|---|---|
| Network separation | Docker networks `net-edge` / `net-app`; data tier unreachable from the host (`DOC-ARCH-005` §3) |
| Rate limiting at edge | Per-IP connection and request limits in nginx; stricter on OTP/top-up routes (`SEC-REQ-009`, enforced in-app) |
| DDoS / WAF | Cloudflare in front (`DEP-08`) — origin IP locked to Cloudflare ranges where possible |
| Egress control | Default allow-out in v1; documented as a candidate tightening (`INFERENCE`) — a restricted egress allowlist would break provider flexibility until endpoint inventory stabilizes |
| IPv6 | Disabled or firewalled with the same rules (avoid bypass) |

## 4. Docker Daemon Hygiene

| Rule | Setting | Why |
|---|---|---|
| No socket to app containers | `docker.sock` is **never** mounted into `api`, `worker`, `web`, or any application-adjacent container | Socket = root on the host |
| No `privileged` containers | Forbidden in all overlays; asserted by the CI compose-policy check (`DOC-OPS-003` §10) | Kernel escape surface |
| No `host` network mode | Forbidden | Bypasses network isolation |
| Rootless where feasible | Rootless Docker (or equivalent) adopted on dev/staging first; production evaluated per distro support — **goal, not a v1 hard gate** (`INFERENCE`) | Reduces daemon compromise impact |
| Non-root app user | Final images run as UID `10001` (`yumn`); data dirs chowned accordingly | Blast radius |
| Read-only rootfs | `read_only: true` + explicit `tmpfs` for `api`/`web` where compatible | Tamper resistance |
| Capabilities | `cap_drop: [ALL]` + minimal `cap_add` per service | Least privilege |
| Seccomp/AppArmor | Default Docker seccomp profile; custom profile only with justification | Syscall surface |
| Content trust | Image digest pinning in staging/prod; only images from `ghcr.io/yumn/*` and vendor registries are pulled | Supply chain |
| Registry auth | Pull token with read-only scope, rotated 90 days (`S-13`) | `SEC-REQ-007` |
| Daemon config | `live-restore` enabled; log driver limits set globally (`DOC-OPS-003` §6) | Stability |

## 5. TLS Termination & Certificate Renewal (DEP-08)

| Aspect | Design |
|---|---|
| Public TLS | Cloudflare edge terminates TLS 1.3 for the customer domain (`DEP-08`, `SEC-REQ-006`) |
| Origin certificate | Origin certificates installed on `edge` (Cloudflare origin cert or ACME-issued), mounted read-only from the `edgecerts` volume — **never baked into images** |
| Internal traffic | HTTP on `net-edge`/`net-app`; the only TLS hop that matters externally is edge↔client and edge↔Cloudflare |
| Renewal | ACME auto-renewal where a public cert is used; Cloudflare origin certs renewed per their validity period; renewal runs as a systemd timer |
| Pre-expiry alert | Daily blackbox probe on certificate expiry → alert ≥ 14 days before expiry (`SEC-REQ-006` R4, `DOC-OPS-006` §5) |
| HSTS | `Strict-Transport-Security: max-age=31536000; includeSubDomains` on all HTTPS responses |
| Cipher/protocol | TLS 1.3 only (TLS 1.2 disabled unless a legacy mobile client forces a documented exception) |
| Private keys | Host-only files mode `0600`, backed up encrypted (`DOC-OPS-007` §3), class `S-11` |
| DNS | Cloudflare-managed DNS; zone transfer disabled; API token with minimal scope held as a CI/ops secret |

## 6. Log Integrity

| Control | Design | Canon |
|---|---|---|
| Host audit | `auditd`-class rules on auth events, sudo, and writes to `infra/` and `.env*` files; shipped off-host daily | `SEC-REQ-010` |
| Container logs | JSON to stdout with rotation (`DOC-OPS-003` §6) → Loki (`DOC-OPS-006` §6) | `NFR-014` |
| Tamper evidence | Money/privileged actions are recorded in the **database audit trail** with a hash chain — logs are diagnostic, the audit table is the system of record | `BR-PLT-06`, `SEC-REQ-010` |
| Log immutability posture | Loki retention 30 days; audit rows retained per `RC-06` (10 years, `INFERENCE`) | `DOC-DTA-005` |
| Clock sync | NTP enabled on the host — timestamps must be trustworthy for correlation and audit | `NFR-014` |
| No secrets in logs | Schema-level allowlist + daily 1,000-line audit script | `AC-NFR-014-01`, `SEC-REQ-007` R4 |
| Access to logs | Ops role only for production; no customer PII in log bodies | `DATA-REQ-002` |

## 7. CIS Baseline Checklist (pointer + local summary)

The authoritative hardening baseline is the **CIS Distribution-independent Linux Benchmark** (level 1 server profile) applied to the host image, plus the **CIS Docker Benchmark**. Execution evidence is kept in `infra/host/cis/` as a checked-in checklist + a re-scan report after every host rebuild.

| Area | Applied controls (level-1 highlights) |
|---|---|
| Filesystem | Mount options (`nodev,nosuid,noexec`) on `/tmp`, `/var/tmp`, `/dev/shm`; no world-writable system dirs |
| Services | Unused services/ports disabled; chrony/NTP configured; mail transfer agent removed |
| Auth | SSH hardening (§2), password aging policy for human accounts, umask `027` |
| Logging | journald persistent storage with size caps; auditd enabled (§6) |
| Container | Docker daemon config (§4); `/etc/docker` mode `0750`; user namespace remapping where supported |
| Kernel | Reverse-path filtering, ICMP ignore, suspicious packet logging (sysctl profile in `infra/host/`) |

Re-verification: re-run the CIS scan after each OS upgrade and after any host rebuild; findings triaged as `SEC-nnn`-style issues in the security register (`09-security/`).

## 8. Vulnerability Scanning Cadence (`SEC-REQ-012`)

| Scan | Tool (class) | When | Gate |
|---|---|---|---|
| Dependency (npm) | Dependabot / Renovate + `npm audit` | every PR + weekly schedule | CRITICAL blocks merge; remediation SLA CRITICAL ≤ 7 d, HIGH ≤ 30 d (`SEC-C-24`) |
| SAST | CodeQL-class | every PR + weekly | CRITICAL/HIGH block (§`SEC-C-23`) |
| Secret scan | gitleaks-class | every PR | **zero tolerance** (`AC-SR007-01`) |
| Container image scan | Trivy-class on built images | every image build + weekly full re-rescan | CRITICAL CVE ⇒ rebuild before promotion |
| Base-image re-scan | Trivy on pinned digests | weekly | Digest-bump PR |
| DAST | ZAP-style baseline + active | against **staging**, per release | Open critical ⇒ no production promotion (`AC-SR012-02`) |
| IaC/compose misconfig | Checkov/Trivy-config class | every PR | Misconfiguration blocks merge |
| Host/CIS | CIS scanner | after every rebuild + monthly | Findings triaged with SLA |
| Reporting | Monthly severity report; no silent suppressions | monthly | `AC-SR012-03/04` |

## 9. Incident Response — Where It Lives

This document **hardens** the host; it does not define incident process.

| Topic | Authoritative location |
|---|---|
| Runbooks for the top-10 operational incidents (symptom → diagnosis → mitigation → escalation) | `12-non-functional/observability.md` §7 |
| Availability math, error-budget policy, degradation matrix, game-day drills | `12-non-functional/reliability.md` §2, §4, §8 |
| Risk register (incl. RISK-005 small-team-vs-99.99%, RISK-014 edge/DNS) | `17-risk-management/risk-register.md` |
| Secret-leak rotation runbook | `09-security/secrets-management.md` §7 |
| Backup/restore under disaster | `14-devops-infrastructure/backup-recovery.md` §6 |
| Rollback decision tree | `15-deployment/rollback.md` |
| Go-live evidence that these exist and were rehearsed | `15-deployment/production-readiness.md` |

Host-specific escalation inputs: P1 alerts from `DOC-OPS-006` §4 page the on-call; on-call ack ≤ 15 min; anything exceeding the error-budget burn threshold triggers the freeze policy of `DOC-NFD-004` §2.

## 10. Backup of Host Configuration

| Item | Where it lives | Backed up how |
|---|---|---|
| Compose files, nginx templates, monitoring rules, systemd units, sysctl profile, firewall rules | **Git repo** under `infra/` | Git is the backup; protected branch + required reviews |
| `.env.<environment>` (secrets) | Host filesystem, mode `0600` | Encrypted archive off-host, on change + weekly (`DOC-OPS-007` §4) |
| TLS private keys | `edgecerts` volume | Encrypted archive with config (`S-11`) |
| Host provisioning script | `infra/host/bootstrap.sh` in repo | Git; re-running it on a clean host is step 1 of disaster recovery (`DOC-OPS-007` §6) |
| CIS scan reports & patch logs | `infra/host/cis/` (repo) + off-host archive | Git + weekly config archive |
| Manual/break-glass notes | Sealed runbook copy held by ops owner | Physical/offline copy |

**Rule:** any change that exists only on the host is a defect — reproduce it in `infra/` within the same change window.

## 11. Verification

| Check | Method | Cadence |
|---|---|---|
| Only 80/443 exposed | External port scan + CI compose assertion | weekly + every PR |
| No docker.sock / privileged in any service | CI compose-policy check | every PR |
| SSH policy enforced | Config audit (`sshd -T`) | monthly |
| CIS re-scan | CIS scanner after rebuild/upgrade | per rebuild + monthly |
| Scan SLAs met | Monthly severity report | monthly (`AC-SR012-03/04`) |
| Cert expiry headroom | Blackbox probe alert ≥ 14 days out | daily |
| Host config in git | Drift diff: `infra/` vs running host | weekly |
| Incident runbooks rehearsed | Rehearsal log | per `AC-NFR-020-01` |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
