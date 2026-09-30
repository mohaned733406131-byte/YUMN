# architecture — canonical pointer (DOC-01 entry file)

**Source of truth:** the analysis knowledge base. Do not restate architecture here — link to it.

| Question | Authoritative document |
|---|---|
| Architecture style & C4 views | [docs/04-architecture/core/architecture-overview.md](docs/04-architecture/core/architecture-overview.md) |
| Containers / processes | [docs/04-architecture/core/container-view.md](docs/04-architecture/core/container-view.md) |
| Components & module boundaries | [docs/04-architecture/core/component-view.md](docs/04-architecture/core/component-view.md) · [docs/04-architecture/core/module-boundaries.md](docs/04-architecture/core/module-boundaries.md) |
| Deployment topology & environments | [docs/04-architecture/core/deployment-view.md](docs/04-architecture/core/deployment-view.md) · [docs/14-devops-infrastructure/environments.md](docs/14-devops-infrastructure/environments.md) |
| Technology stack (versions) | [docs/04-architecture/core/technology-stack.md](docs/04-architecture/core/technology-stack.md) |
| Data flow | [docs/04-architecture/core/data-flow.md](docs/04-architecture/core/data-flow.md) |
| Scalability path | [docs/04-architecture/core/scalability.md](docs/04-architecture/core/scalability.md) |
| Decisions (ADRs 001–010) | [docs/18-decisions/README.md](docs/18-decisions/README.md) · [decision log](docs/18-decisions/decision-log.md) |
| System behavior / state machines | [docs/03-system-analysis/core/state-transitions.md](docs/03-system-analysis/core/state-transitions.md) |
| Backend internals | [docs/06-backend/core/backend-architecture.md](docs/06-backend/core/backend-architecture.md) |
| Frontend internals | [docs/05-frontend/core/frontend-architecture.md](docs/05-frontend/core/frontend-architecture.md) |

## One-paragraph summary (implementation binding in `senior-rules/RULES_HINTS.md` §2)

yumn is a **modular monolith**: NestJS 10 (TypeScript / Node 20) serving 13 modules `B01…B13`
that map 1:1 to PostgreSQL 16 schemas `b01…b13` (Prisma 5), with Redis 7 + BullMQ as the only
queue, Elasticsearch 8 for Arabic-aware search, MinIO for objects, a Next.js 14 web app
(customer/vendor/admin shells) and two React Native 0.73 apps — all deployed as **Docker Compose
services on a single host per environment** (no Kubernetes, `C-22`), fronted by Nginx/Cloudflare.

**Note:** this file must stay a pointer. When architecture changes, change
`docs/04-architecture/` first (DOC-05: same commit as the code), then update this table if the
link target changes.
