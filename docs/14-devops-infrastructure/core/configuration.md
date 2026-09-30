---
document_id: DOC-OPS-005
title: Configuration Management & Environment Variable Inventory
category: 14-devops-infrastructure
status: approved
version: 1.1
created: 2026-09-26
updated: 2026-09-28
author: analysis-agent
source_of_truth: true
related_requirements: [NFR-020, SEC-REQ-007, DATA-REQ-003]
related_documents: [DOC-OPS-001, DOC-OPS-002, DOC-SEC-005, DOC-DTA-005, DOC-DPL-005, DOC-ARCH-005]
---

# Configuration Management & Environment Variable Inventory

Everything the platform needs to know about *where it is running* arrives as **environment configuration** — never as code, never in images, never in git (`NFR-020`, `SEC-REQ-007`). This document is the inventory of record: every variable, its purpose, its consumers, and whether it is a secret.

## 1. Configuration Hierarchy

Values resolve in this order; the **last** source wins:

```text
1. Compiled defaults        safe, non-environment defaults in code (LOG_LEVEL=info, TZ=UTC, LOCALE_DEFAULT=ar)
2. Environment file         .env.<environment> on the host, mounted via env_file (per-environment values)
3. Runtime environment      variables injected by Compose / the deployer (highest precedence for overrides)
4. Feature flags            runtime-tunable behaviour switches (§4) — read from Redis/DB, overlay the above
5. Platform settings (DB)   business configuration edited by admins in the console (FR-020) — commission tiers,
                            VAT rates, return windows, shipping costs. NOT infra config; constraints C-01…C-26
                            are never configurable (DOC-ARCH-005 §5)
```

Rules:

| # | Rule | Anchor |
|---|---|---|
| CFG-1 | Only layer 1 may be non-sensitive **and** environment-independent. Anything environment-specific lives in layer 2/3. | `ADR-004` parity |
| CFG-2 | Secrets exist only in layers 2/3, on the host, mode `0600` — never in layers 1/4/5, never in images or git. | `SEC-REQ-007` |
| CFG-3 | Layer 5 (DB settings) may never be used to change infrastructure topology, credentials, or constraint behaviour. | `FR-020`, `C-01…C-26` |
| CFG-4 | Retention periods are configuration consumed by the purge job, not code constants. | `DATA-REQ-003` R1 |

## 2. Environment Variable Inventory

Consumers: **api** (NestJS HTTP), **worker** (BullMQ), **web** (Next.js), **edge** (nginx). `Y` = secret (never logged, never echoed, host-only file).

### 2.1 Core / runtime

| Variable | Purpose | Required | Example | Secret? | Consumed by |
|---|---|---|---|---|---|
| `NODE_ENV` | runtime mode | yes | `production` | N | api, worker, web |
| `TZ` | container timezone | yes | `UTC` (storage is UTC, `BR-PAY-10`) | N | api, worker, web |
| `LOCALE_DEFAULT` | default locale for server-rendered defaults | yes | `ar` (`C-24`) | N | api, web |
| `LOG_LEVEL` | structured log verbosity | no (`info`) | `info` | N | api, worker, web |
| `LOG_FORMAT` | log output shape | yes | `json` (`DOC-NFD-006` §2) | N | api, worker, web |
| `API_BASE_URL` | public API base for web/mobile | yes | `https://api.yumn.ye/api/v1` | N | web, worker |
| `WEB_BASE_URL` | public web origin (CORS allowlist) | yes | `https://yumn.ye` | N | api, web |
| `PORT` | HTTP listen port | yes | `3000` | N | api, web |
| `TRUST_PROXY` | honour `X-Forwarded-*` from edge | yes | `true` | N | api, web |

### 2.2 Data stores

| Variable | Purpose | Required | Example | Secret? | Consumed by |
|---|---|---|---|---|---|
| `DATABASE_URL` | PostgreSQL connection (Prisma, `C-19`) | **yes** | `postgresql://yumn_app@postgres:5432/yumn` | **Y** (contains password) | api, worker, migrate |
| `DATABASE_URL_MIGRATIONS` | privileged migrations role | **yes** (migrate job only) | `postgresql://yumn_migrate@postgres:5432/yumn` | **Y** | migrate |
| `DATABASE_POOL_MAX` | Prisma pool size | no (`20`) | `20` | N | api, worker |
| `REDIS_URL` | Redis for cache + BullMQ (`C-20`) | **yes** | `redis://:pass@redis:6379/0` | **Y** | api, worker |
| `REDIS_URL_CACHE` | separate logical DB for cache | no (falls back to `REDIS_URL`) | `redis://:pass@redis:6379/1` | **Y** | api |
| `REDIS_URL_QUEUE` | separate logical DB for BullMQ | no (falls back) | `redis://:pass@redis:6379/2` | **Y** | api, worker |
| `ELASTICSEARCH_URL` | ES endpoint (`DEP-04`) | **yes** | `http://elasticsearch:9200` | N | api, worker |
| `ELASTICSEARCH_API_KEY` | ES auth | yes if security enabled | `base64…` | **Y** | api, worker |
| `SEARCH_ENABLED` | allow search degradation switch | no (`true`) | `true` | N | api, worker |

### 2.3 Object storage (`DEP-07`)

| Variable | Purpose | Required | Example | Secret? | Consumed by |
|---|---|---|---|---|---|
| `MINIO_ENDPOINT` | host | yes | `http://minio:9000` | N | api, worker |
| `MINIO_PORT` | port | yes | `9000` | N | api, worker |
| `MINIO_USE_SSL` | TLS to MinIO | yes | `false` (internal network) | N | api, worker |
| `MINIO_BUCKET_MEDIA` | images bucket | yes | `yumn-media` | N | api, worker |
| `MINIO_BUCKET_KYC` | KYC documents bucket | yes | `yumn-kyc` | N | api, worker |
| `MINIO_ACCESS_KEY` | S3 access key | **yes** | `yumn-app` | **Y** | api, worker |
| `MINIO_SECRET_KEY` | S3 secret key | **yes** | *(from env file)* | **Y** | api, worker |

### 2.4 Auth & crypto

| Variable | Purpose | Required | Example | Secret? | Consumed by |
|---|---|---|---|---|---|
| `JWT_PRIVATE_KEY` | RS256 signing key (PEM, single-line `\n`) | **yes** | *(from env file)* | **Y** | api |
| `JWT_PUBLIC_KEY` | RS256 verify key / JWKS source | **yes** | *(from env file)* | N | api |
| `JWT_ACCESS_TTL` | access token lifetime | yes (`15m`) | `15m` (`C-08`) | N | api |
| `JWT_REFRESH_TTL` | refresh lifetime | yes (`7d`) | `7d` (`C-08`) | N | api |
| `DATA_ENCRYPTION_KEY` | field-level encryption for PII (`SEC-REQ-002`) | **yes** | *(from env file)* | **Y** | api, worker |
| `CSRF_SIGNING_SECRET` | CSRF token signing for cookie auth | **yes** | *(from env file)* | **Y** | api, web |

### 2.5 Provider integrations

| Variable | Purpose | Required | Example | Secret? | Consumed by |
|---|---|---|---|---|---|
| `SMS_PROVIDER_PRIMARY` | primary adapter id | yes | `telesom` (`DEP-06`) | N | worker |
| `SMS_PRIMARY_API_KEY` | primary provider key | **yes** | *(env file)* | **Y** | worker |
| `SMS_PROVIDER_SECONDARY` | failover adapter id | yes | `sabafon` (`INT-REQ-003`) | N | worker |
| `SMS_SECONDARY_API_KEY` | secondary provider key | **yes** | *(env file)* | **Y** | worker |
| `SMS_SENDER_ID` | alphanumeric sender | yes | `yumn` | N | worker |
| `WHATSAPP_API_TOKEN` | WhatsApp Business token (`DEP-06`) | **yes** | *(env file)* | **Y** | worker |
| `WHATSAPP_VERIFY_TOKEN` | webhook verify token (`INT-REQ-006`) | **yes** | *(env file)* | **Y** | api |
| `WHATSAPP_WEBHOOK_SECRET` | HMAC secret for inbound messages | **yes** | *(env file)* | **Y** | api |
| `WALLET_PROVIDER_MFLOOS_BASE_URL` | m-Floos endpoint (`DEP-05`) | yes | `https://api.mfloos.example` | N | api, worker |
| `WALLET_PROVIDER_MFLOOS_MERCHANT_KEY` | merchant key | **yes** (prod) | *(env file)* | **Y** | api, worker |
| `WALLET_PROVIDER_MFLOOS_SECRET` | merchant secret | **yes** (prod) | *(env file)* | **Y** | api, worker |
| `WALLET_PROVIDER_ONECASH_BASE_URL` | OneCash endpoint | yes | `https://api.onecash.example` | N | api, worker |
| `WALLET_PROVIDER_ONECASH_MERCHANT_KEY` | merchant key | **yes** (prod) | *(env file)* | **Y** | api, worker |
| `WALLET_PROVIDER_ONECASH_SECRET` | merchant secret | **yes** | *(env file)* | **Y** | api, worker |
| `PAYMENT_WEBHOOK_SECRET` | inbound top-up callback HMAC | **yes** | *(env file)* | **Y** | api |
| `PUSH_FCM_CREDENTIALS_JSON` | FCM service account (JSON as env) | **yes** | *(env file)* | **Y** | worker |
| `PUSH_APNS_KEY_P8` | APNs signing key (`.p8` content) | **yes** | *(env file)* | **Y** | worker |
| `PUSH_APNS_TEAM_ID` / `PUSH_APNS_KEY_ID` / `PUSH_APNS_TOPIC` | APNs identifiers | yes | `TEAM123456` | N | worker |

Provider sets are **disjoint per environment**: sandbox base URLs + sandbox keys in dev/staging, production URLs + production keys in prod — never mixed (`DOC-OPS-002` PAR-4).

### 2.6 Observability & ops

| Variable | Purpose | Required | Example | Secret? | Consumed by |
|---|---|---|---|---|---|
| `METRICS_ENABLED` | expose Prometheus `/metrics` | yes (`true`) | `true` (`INT-REQ-007`) | N | api, worker |
| `OTEL_EXPORTER_ENDPOINT` | trace export (OTel-compatible) | no | `http://prometheus:9090` | N | api, worker |
| `ALERT_SMTP_URL` / `ALERT_WEBHOOK_URL` | Alertmanager receivers | staging/prod | `https://hooks…` | **Y** (webhook URL may carry token) | alertmanager |
| `BACKUP_ENCRYPTION_PASSPHRASE` | backup at-rest encryption | **yes** (prod) | *(env file)* | **Y** | backup job |
| `BACKUP_OFFHOST_TARGET` | off-host copy destination | **yes** (prod) | `s3://yumn-backups/prod` | N | backup job |
| `HEALTH_READY_ES_POLICY` | readiness treatment of ES | yes (`degraded`) | `degraded` (`DOC-DPL-005`) | N | api |

### 2.7 Feature flags (runtime, §4)

| Variable | Purpose | Required | Example | Secret? | Consumed by |
|---|---|---|---|---|---|
| `FEATURE_FLAGS_BACKEND` | where flags are read from | yes | `redis` | N | api, worker |
| `FEATURE_FLAGS_TTL_SECONDS` | cache TTL for flag values | no (`30`) | `30` | N | api, worker |
| `FEATURE_FLAGS_DEFAULT_MODE` | behaviour for unknown flags | yes | `off` (fail-closed) | N | api, worker |

## 3. Fail-Fast Validation on Boot

| Rule | Behaviour | Evidence |
|---|---|---|
| Schema-validated at startup | A Zod/class-validator schema enumerates **every required variable**; the process logs `CONFIG_MISSING: <name>` (name only, never a value) and exits non-zero | `AC-SR007-02` |
| No defaults for secrets | Missing secret ⇒ startup abort. No fallback, no example credential, no "dev default" in production mode | `SEC-REQ-007` R3 |
| Cross-field checks | e.g. `WALLET_PROVIDER_*_BASE_URL` set ⇒ its key/secret set; `PUSH_APNS_KEY_P8` present ⇒ `PUSH_APNS_KEY_ID` present | Boot validation suite |
| Range/format checks | TTLs parse as durations; URLs parse; PEM contains `BEGIN`; pool sizes are integers > 0 | Boot validation suite |
| Web startup | Next.js validates `NEXT_PUBLIC_*` allowlist at build **and** runtime; **no secret may use the `NEXT_PUBLIC_` prefix** | `SEC-REQ-007` R4 |
| Migrate job | `prisma migrate deploy` fails loudly and halts the deploy — never partially rolls forward (`DOC-DB-006` §2) | Deploy log |
| Negative test in CI | A pipeline step boots the API **without** `DATABASE_URL` and asserts a non-zero exit with a non-sensitive message | `AC-SR007-02` |

## 4. Feature-Flag Design

Flags are **operational switches**, not configuration of business rules. Business values (commission %, VAT rate, return windows) belong to platform settings in the DB (`FR-020`), not to flags.

| Aspect | Design |
|---|---|
| Storage | Redis key `feature:{flag}` (string `"0"`/`"1"`, optional JSON payload) with TTL; a DB table `platform.feature_flag` is the durable source re-synced to Redis at boot (`INFERENCE`) |
| Read path | Cached in-process for `FEATURE_FLAGS_TTL_SECONDS` (default 30 s), then re-read; a flag is never read from disk or hardcoded |
| Scope | Global by default; optional per-locale or per-store override for UI experiments |
| Default mode | **Fail-closed (`off`)** for risky flags; unknown flag ⇒ default value, never an exception |
| Change control | Changing a flag writes a `BR-PLT-06` audit entry (actor, flag, old→new) and emits a P4 dashboard marker (`DOC-NFD-006` §6) |
| Never flagged | Anything that would violate `C-01…C-26`, alter the 17 order states (`C-09`), change JWT lifetimes (`C-08`), or disable audit writing |

### 4.1 v1 flag register

| Flag | Default | Purpose | Related canon |
|---|---|---|---|
| `search_suggestions_enabled` | on | Autosuggest/typeahead; turning it off leaves full search + category browse intact | `FR-009`, `NFR-007` (search degradation) |
| `auto_accept_orders_enabled` | **off** | Auto-move `PLACED → CONFIRMED` for stores meeting a KYC+standing condition; off until the rule is proven | `FR-012`, `C-09`, `BR-ORD-01` |
| `reviews_bulk_moderation_enabled` | off | Batch moderation UI/API surface for the moderator role | `FR-006`, `FR-020` |
| `bank_topup_enabled` | on | Manual bank-transfer rail (`BR-PAY-04`) — may be disabled during reconciliation backlog | `INT-REQ-002`, `C-05` |
| `instant_topup_enabled` | on | Provider-backed top-ups; off ⇒ degrade to bank transfer only | `INT-REQ-001`, `10-integrations` degradation matrix |
| `maintenance_mode` | off | Routes non-critical traffic to the maintenance page; health endpoints stay live | `NFR-020`, `DOC-DPL-003` |
| `new_vendor_registration_enabled` | on | Throttle intake during KYC backlog | `FR-007` |

Flag lifecycle: **add** = new row + default in the register · **active** = row in force · **retire** = remove code usage first, then remove the row (a dead flag is technical debt and is recorded in `21-completion/technical-debt.md` **before** the row disappears) · **retired** = row removed; the flag name is never reused. **Sweep cadence: quarterly** — every flag in §4.1 is checked against code usage; any dead row is dispositioned in `21-completion/technical-debt.md` before removal (`REC-10`, `TD-01`).

### 4.2 Flag sweep record (dated, per-flag disposition)

| Date | Flag (§4.1) | Disposition | Evidence |
|---|---|---|---|
| 2026-09-28 | `search_suggestions_enabled` | `RETAIN` — pre-implementation baseline; no code usage exists to remove | no `api/`, `apps/`, or `packages/` tree in the repo (`SPE-03`); re-sweep at first code, then quarterly |
| 2026-09-28 | `auto_accept_orders_enabled` | `RETAIN` — pre-implementation baseline; no code usage exists to remove | as above |
| 2026-09-28 | `reviews_bulk_moderation_enabled` | `RETAIN` — pre-implementation baseline; no code usage exists to remove | as above |
| 2026-09-28 | `bank_topup_enabled` | `RETAIN` — pre-implementation baseline; no code usage exists to remove | as above |
| 2026-09-28 | `instant_topup_enabled` | `RETAIN` — pre-implementation baseline; no code usage exists to remove | as above |
| 2026-09-28 | `maintenance_mode` | `RETAIN` — pre-implementation baseline; no code usage exists to remove | as above |
| 2026-09-28 | `new_vendor_registration_enabled` | `RETAIN` — pre-implementation baseline; no code usage exists to remove | as above |

Sweep result: **0 dead rows** (nothing to remove); next sweep due at first implementation code, then on the quarterly cadence (`REC-10` acceptance evidence).

## 5. Config Drift Prevention

| Mechanism | Detail | Cadence |
|---|---|---|
| Files-in-repo | `compose*.yaml`, nginx templates, Prometheus rules, Grafana dashboards, alert routes are **code** — changed only by PR | every change |
| Env files off-repo | `.env.<environment>` lives on the host only; `.gitignore` blocks `.env*`, `*.pem`, `*.key`, `credentials.json` | enforced by CI secret scan |
| Drift detection | On each deploy, the running `docker compose config` is rendered and diffed against the committed base + overlay; unexpected difference ⇒ deploy aborts | every deploy |
| Required-variable audit | A script lists every variable referenced by the code and asserts it appears in each environment's env file with a value | weekly (`dependency-audit.yml`) |
| Config review | Secrets/credentials set reviewed for disjointness across environments and rotation cadence (`DOC-SEC-005` §2) | quarterly |
| Infrastructure as code | Host-level config (systemd units, firewall rules, cert renewal) tracked under `infra/host/` in the repo | every change |
| One source per concept | Platform settings live in the DB console; nothing duplicates them in env files (e.g. commission tier is **not** an env var) | review |

## 6. Verification

| Check | Method | Evidence |
|---|---|---|
| Missing required var ⇒ non-sensitive failure | CI negative-boot job | `AC-SR007-02` |
| No secret in repo | `gitleaks` over the whole tree | `AC-SR007-01/03` |
| No secret in logs | Automated scrub test over auth + top-up run | `AC-SR007-04` |
| Inventory completeness | Every env var in code appears in §2 and vice versa (script) | weekly audit job |
| Environment disjointness | Config review of `.env.*` values | `DOC-SEC-005` §8 |
| Parity of variable sets across envs | Same variable **names** in dev/staging/prod; only values differ | `ADR-004` parity check |

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial version | Initial analysis |
| 1.1 | 2026-09-28 | §4.1 flag lifecycle gains explicit **retire/retired** states and a **quarterly sweep cadence**; new §4.2 dated sweep record with per-flag dispositions (baseline: 0 dead rows, pre-implementation) | `REC-10` / `TD-01` pay-down — the lifecycle's dead-flag rule needed a home, state, and cadence (`FEATURE_FLAGS_DEFAULT_MODE=off` fail-closed hides leftovers) |
