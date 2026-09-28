# yumn — Mind Map (repository navigation)

Root: `E:\YUMN`

```text
E:\YUMN
├─ AGENTS.md                        AI assistant instruction (read ENTRY.md first, rules binding)
├─ architecture.md                  Canonical architecture pointer → docs/04-architecture/
├─ development_phases_entry.md      Phase status + gate state (DOC-01 entry file)
├─ all_in_one_track.md              Roll-up index of all tracking files (DOC-01 entry file)
├─ session_track.md                 Session ledger + resume points (SES-02, DOC-01 entry file)
├─ memory.md                        Durable project facts & known-defect register (DOC-01)
├─ mind_map.md                      This file
│
├─ senior-rules/                    ADMR rule system (binding — read at session start)
│  ├─ ENTRY.md                      Master rule file (read first, obey always)
│  ├─ RULES.md                      Master catalog: GEN SES DOC DOD IMP SEC TST LOG UI VCS AUD COM ADP
│  ├─ RULES_HINTS.md                yumn adapter: stack, commands, paths, overrides (ADP-01)
│  ├─ YUMN_RULES.md                 yumn rule catalog: MNY ESC ORD IDT STK SHP RET RTL API DAT OPS PRF SPE
│  ├─ core/                         Doctrine behind the catalog (DoD, security, testing, data/API…)
│  ├─ templates/                    Copy-ready artifacts (phase plan, test plan, task todo…)
│  ├─ validators/validate.py        Structural validator — run after every phase
│  ├─ CHANGELOG.md · VERSION        Rule versioning (core/00 §0.5)
│  └─ adapters/                     RULES_HINTS template (source of the filled adapter)
│
├─ senior-implementation-rules-master/   Upstream ADMR source (vendored; reinstall from here)
│
├─ docs/                            ★ Knowledge base — the analysis source of truth (24 domains)
│  ├─ README.md                     Master index, reading order, ID conventions, source-of-truth rules
│  ├─ 00-project-overview/          Charter, context, scope, constraints C-01…C-26, actors, assumptions
│  ├─ 01-business-analysis/         104 business rules, 40 use cases, 12 workflows, 15 processes
│  ├─ 02-requirements/              68 requirements (FR/NFR/SEC-REQ/DATA-REQ/INT-REQ) + 253 ACs
│  ├─ 03-system-analysis/           Boundary, components, state transitions, edge cases, failures
│  ├─ 04-architecture/              Views, tech stack, module boundaries, scalability
│  ├─ 05-frontend/  06-backend/     Client & server internals (layout, state, auth, queues, cache)
│  ├─ 07-api/                       221 endpoints in 14 groups + conventions, error model, pagination
│  ├─ 08-database/                  PostgreSQL 16 schema b01…b13, 18 entities, indexes, migrations
│  ├─ 09-security/                  Threat model, RBAC, findings SEC-001…SEC-016
│  ├─ 10-integrations/              m-Floos/OneCash, SMS, WhatsApp, push, webhook reliability
│  ├─ 11-ui-ux/                     Flows, design system, accessibility, localization
│  ├─ 12-non-functional/            Measurable NFR detail (performance, reliability, observability)
│  ├─ 13-testing/                   Strategy, plans, TC-001…TC-103 (declared …TC-114), TST-CON-01…26
│  ├─ 14-devops-infrastructure/     CI/CD gates, compose topology, environments, monitoring
│  ├─ 15-deployment/                Build/release, rollback, health checks, production readiness
│  ├─ 16-data/                      Lifecycle, retention, classification, deletion & privacy
│  ├─ 17-risk-management/           Risk register RISK-001…RISK-024 + mitigations
│  ├─ 18-decisions/                 ADR-001…ADR-010 + decision log
│  ├─ 22-glossary/                  Terminology + naming conventions (binding for code/docs)
│  └─ 23-templates/                 Templates for every document type
│
├─ command.md                       Analysis methodology (56 areas / 48-part structure)
└─ archdoc.md                       Structure spec — restored 2026-09-28 (REC-01; reconstructed, provenance noted)
```

**Navigation rule:** read a directory's `README.md` before analyzing that directory (`docs/README.md` §3). IDs are never copied across documents — always reference them (`docs/README.md` §4).
