---
document_id: DOC-IR-007
title: INT-REQ-007 — Observability export
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [INT-REQ-006, FR-020, NFR-014, NFR-005]
related_documents: [DOC-REQ-001, DOC-OVR-008]
---

# INT-REQ-007 — Observability export

> Registry summary (`requirements-overview.md` §5): Prometheus scrape, Grafana dashboards, alert routes to on-call.

**Dependency risk:** MEDIUM — tooling failure degrades detection and response (MTTD/MTTR), not request serving; directly affects the ability to hold C-26 (99.99%).

## Purpose
Export metrics, logs, and health signals from the modular monolith (C-21), workers, PostgreSQL, Redis/BullMQ, Elasticsearch, and MinIO to Prometheus for storage, Grafana for visualization, and alert routing to the on-call rotation — satisfying NFR-014.

## Interface expectations

- **Scrape:** each service exposes a `/metrics` endpoint on an internal-only port; Prometheus scrapes at a fixed interval with targets for API, worker, database, queue, and search (target list in `10-integrations/` / `12-non-functional/observability.md`).
- **Metrics:** RED metrics per endpoint (rate, errors, duration), queue depth and DLQ depth (BR-PLT-02), reconciliation mismatch counters (DATA-REQ-006), rate-limit 429 counters (SEC-REQ-009).
- **Health:** liveness/readiness endpoints gate traffic and are themselves monitored (BR-PLT-07, NFR-005).
- **Alerts:** alert rules route through Alertmanager-style routing to on-call by severity; DLQ depth, reconciliation mismatch, WAL gap, and provider outage are alerted, not just graphed (10 s webhook/alert transport timeouts and 3 retries + DLQ apply to alert notifications too — BR-PLT-02 pattern).

## Data exchanged
Metric names/labels (service, endpoint, status, queue), structured logs with correlation IDs, health status, alert events. **No PII, phone numbers, tokens, or secrets in labels/log payloads** (SEC-REQ-002, SEC-REQ-007).

## Failure behavior & fallback
Scrape gap → Prometheus records target-down and alerts; alert-pipeline failure → secondary notification channel (per `12-non-functional/observability.md`); label-cardinality blowup → guarded by label allowlist; observability outage never blocks user traffic (NFR-007 graceful degradation).

## Security
Metrics endpoints bound to internal networks only (never publicly routed); Grafana/Alertmanager access authenticated and role-scoped (SEC-REQ-004); no secrets in scrape configs — env-driven (SEC-REQ-007); log/metric export reviewed for PII leakage.

## Acceptance criteria

- AC-IR007-01: Scrape test — all defined targets are up (`up == 1`) and RED metrics for each endpoint are queryable in Prometheus after traffic runs.
- AC-IR007-02: Alert routing — a simulated error spike (and a simulated DLQ depth increase) fires an alert that reaches the on-call destination within the window defined in `12-non-functional/observability.md`.
- AC-IR007-03: PII scrub — an automated scan of a sampled metrics export and log stream finds zero phone numbers, tokens, or secret values.
- AC-IR007-04: Dashboards — Grafana dashboards exist for RED per endpoint, queue/DLQ depth, database health, and reconciliation status, and render from live data.

## Related IDs

`NFR-014` · `NFR-005` · `NFR-007` · `C-21` · `C-26` · `BR-PLT-02` · `BR-PLT-07` · `SEC-REQ-002` · `SEC-REQ-004` · `SEC-REQ-007` · `SEC-REQ-009` · `DATA-REQ-004` · `DATA-REQ-006` · `FR-020`

## Verification method
Prometheus target/query assertions in a staging environment, alert-routing fire drill, PII scan of exported metrics/logs, and dashboard existence/render review; detail in `12-non-functional/observability.md`.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
