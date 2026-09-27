---
document_id: DOC-SR-009
title: SEC-REQ-009 — Rate limiting & abuse control
category: 02-requirements
status: approved
version: 1.0
created: 2026-09-26
updated: 2026-09-26
author: analysis-agent
source_of_truth: true
related_requirements: [SEC-REQ-005, SEC-REQ-008, FR-013, NFR-003]
related_documents: [DOC-REQ-001, DOC-OVR-008]
---

# SEC-REQ-009 — Rate limiting & abuse control

> Registry summary (`requirements-overview.md` §3): per-IP and per-user limits (100 req/min standard); stricter on OTP/top-up endpoints.

**Priority:** High · **STRIDE:** Denial of service (D) · **Failure impact:** HIGH

## Description
Server-side rate limits protect the platform from automated abuse and resource exhaustion: a standard limit of 100 requests/minute per IP and per user, with stricter thresholds on OTP, login, and top-up initiation endpoints, enforced centrally (Redis) and independent of any client behavior.

## Security rationale
Without quotas, bots farm OTPs, scrape catalogs, brute-force at scale (SEC-REQ-005), and hammer money endpoints until partial failures appear — degrading the 10,000-concurrency target (C-25) and the 99.99% availability target (C-26). Threat: application-layer denial of service and automation abuse → STRIDE **Denial of service**.

## Requirement statements

- R1: Standard limit is 100 requests/minute per IP and per user; exceeding it returns 429 with a `Retry-After` header, applied before expensive business logic runs.
- R2: OTP resend/verify, login, and top-up initiation endpoints enforce limits stricter than the standard (OTP is additionally bounded by BR-AUTH-03: 60 s cooldown, ≤3 resends per 10 minutes).
- R3: Counters are server-side (Redis, DEP-03) and shared across replicas behind the load balancer; removing or disabling client-side throttling has no effect (NFR-018 stateless replicas).
- R4: Legitimate traffic at the C-25 target of 10,000 concurrent users stays within NFR-001 latency targets; limiting must not become the bottleneck.
- R5: 429 bursts and limiter-triggered patterns are exported as metrics and alert on suspected abuse (NFR-014).

## Acceptance criteria

- AC-SR009-01: Limit test — request 101 within a 60-second window from one IP or user receives 429 + `Retry-After`; the next window succeeds normally.
- AC-SR009-02: Endpoint-specific test — measured thresholds for OTP resend/verify, login, and top-up initiation are strictly below the 100 req/min standard and enforced per account and per IP.
- AC-SR009-03: Bypass test — spoofed/removed client headers and disabled client-side throttling do not raise the effective server-side limit.
- AC-SR009-04: Load test (C-25) — 10,000 concurrent legitimate users hold p95 within NFR-001 while a scripted abusive client is throttled with 429s.

## Related IDs

`FR-013` · `BR-AUTH-03` · `BR-PAY-02` · `SEC-REQ-005` · `SEC-REQ-008` · `NFR-001` · `NFR-003` · `NFR-014` · `C-25` · `C-26`

## Verification method

Integration tests asserting per-endpoint thresholds and 429 semantics, plus the NFR-003 load test with an abusive client profile; limiter configuration review in `09-security/`.

## Failure impact

**HIGH** — OTP farming and automated credential attacks defeat SEC-REQ-001/005; sustained request floods exhaust Node/DB capacity, breaching C-25/C-26 targets and causing revenue-blocking outages.

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-26 | Initial requirement | Initial analysis |
