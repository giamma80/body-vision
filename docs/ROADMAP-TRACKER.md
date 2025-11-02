# ROADMAP-TRACKER.md

## Legenda
- Status: `todo` | `in-progress` | `done`
- Priority: `high` | `medium` | `low`

## Implementation Strategy: Vertical Slice Approach

Building end-to-end functionality in phases rather than completing each component individually.

---

## FASE 1: Fondamenta Dati ✅ (COMPLETED)

### Completed Tasks

| Task | Area | Priority | Status | Date | Note |
|---|---|---|---|---|---|
| Setup monorepo struttura base | infra | high | done | 2025-11-01 | backend, frontend, inference, infra, scripts |
| Configurare uv + pyproject + lock | backend | high | done | 2025-11-01 | 122 dipendenze installate |
| Setup GitHub repository | infra | high | done | 2025-11-01 | Repo pubblico creato |
| Database Models (SQLAlchemy) | backend | high | done | 2025-11-02 | User, AnalysisSession, Measurement |
| Configurare Alembic migrations | backend | high | done | 2025-11-02 | Async support con SQLite/PostgreSQL |
| Prima migration + test DB | backend | high | done | 2025-11-02 | bodyvision.db creato con 3 tabelle |

**Files Created:**
- `backend/app/models/user.py` - User model with auth_id for Supabase
- `backend/app/models/analysis.py` - AnalysisSession & Measurement models
- `backend/app/models/base.py` - TimestampMixin for created_at/updated_at
- `backend/app/core/database.py` - Async engine + session factory
- `backend/migrations/env.py` - Alembic async configuration
- `backend/migrations/versions/5eea10b5f0bc_*.py` - Initial migration
- `.env` - Local configuration with SQLite

**Database Schema:**
```
users (id, email, full_name, auth_id, is_active, timestamps)
analysis_sessions (id, user_id, job_id, status, images, metadata, timestamps)
measurements (id, session_id, body_fat_%, volume, density, mesh_url, timestamps)
```

---

## FASE 2: Backend Funzionante ✅ (COMPLETED)

### Completed Tasks

| Task | Area | Priority | Status | Date | Note |
|---|---|---|---|---|---|
| Inference Dummy Worker | inference | high | done | 2025-11-02 | Mock worker con calcoli realistici |
| POST /predict endpoint completo | backend | high | done | 2025-11-02 | Accoda job + salva DB |
| GET /predict/{job_id} endpoint | backend | high | done | 2025-11-02 | Ritorna status + risultati |
| Redis management automation | infra | high | done | 2025-11-02 | Makefile targets + docs |
| Test unitari per endpoints | backend | high | done | 2025-11-02 | pytest con 64% coverage |

**Files Created:**
- `backend/app/core/broker.py` - Dramatiq broker with Redis
- `inference/app/tasks/body_analysis.py` - Mock analysis task (150+ lines)
- `backend/app/api/endpoints/predict.py` - Complete REST API (250+ lines)
- `scripts/start_worker.sh` - Worker startup script
- `scripts/test_api.py` - End-to-end test script
- `backend/tests/test_predict.py` - Unit tests
- `docs/REDIS-SETUP.md` - Complete Redis documentation

**API Endpoints:**
- `POST /api/predict/` - Creates job, returns job_id and session_id
- `GET /api/predict/{job_id}` - Returns status and measurements

**Worker Features:**
- Realistic body composition calculations based on BMI
- Simulates 2-5 second processing time
- Updates database with status (queued → processing → completed)
- Generates measurements: body_fat%, volume, density, lean/fat mass
- Error handling with failed status

**Make Commands:**
- `make redis-check` - Verify Redis installation
- `make redis-status` - Check if running
- `make redis-start` - Auto-start (platform-aware)
- `make redis-stop` - Stop gracefully
- `make redis-restart` - Restart
- `make worker` - Start Dramatiq worker
- `make db-migrate MSG="..."` - Create migration
- `make db-upgrade` - Apply migrations

**Test Coverage:**
- Backend: 64% (323 statements, 116 missing)
- All endpoint tests passing
- Health check, validation, 404 handling

---

## FASE 3: GraphQL Schema ✅ (COMPLETED)

### Completed Tasks

| Task | Area | Priority | Status | Date | Note |
|---|---|---|---|---|---|
| Strawberry GraphQL schema | backend | medium | done | 2025-11-02 | Complete schema con 8 queries |
| GraphQL types | backend | medium | done | 2025-11-02 | User, Session, Measurement, Stats |
| GraphQL queries implementation | backend | medium | done | 2025-11-02 | Complex queries con relationships |
| GraphQL endpoint integration | backend | medium | done | 2025-11-02 | FastAPI + GraphiQL UI |
| GraphQL documentation | docs | medium | done | 2025-11-02 | Examples + Python client |
| GraphQL tests | backend | medium | done | 2025-11-02 | Unit tests + integration |

**Files Created:**
- `backend/app/graphql/types.py` - GraphQL types (110+ lines)
- `backend/app/graphql/queries.py` - 8 queries (315+ lines)
- `backend/app/graphql/schema.py` - Schema definition
- `backend/app/api/endpoints/graphql_endpoint.py` - FastAPI integration
- `docs/GRAPHQL-EXAMPLES.md` - Complete query examples (400+ lines)
- `scripts/test_graphql.py` - Test script
- `backend/tests/test_graphql.py` - Unit tests

**GraphQL Queries Implemented:**
1. `user(email)` - Get user by email
2. `userById(id)` - Get user by ID
3. `analysisSession(jobId)` - Get session with measurements
4. `userSessions(email, status, limit, offset)` - Get user's sessions with filters
5. `userWithSessions(email, limit)` - User + recent sessions combined
6. `userStats(email)` - Statistics (total, avg body fat, processing time)
7. `latestMeasurements(email, limit)` - Latest measurements only

**GraphQL Features:**
- Fully typed schema with Strawberry
- Automatic enum conversion (AnalysisStatus, Gender)
- Relationship resolution (Session → Measurement)
- Pagination support (limit/offset)
- Filtering (by status)
- Aggregations (count, avg)
- GraphiQL UI at /graphql
- Introspection enabled

**Documentation:**
- Complete query examples
- Variables usage
- Error handling
- Performance tips
- Python client example
- curl examples

---

## FASE 4: Frontend (Next.js) 📋 (PLANNED)

| Task | Area | Priority | Status | Note |
|---|---|---|---|---|
| Next.js 14 setup | frontend | high | todo | App Router + TypeScript |
| Shadcn/UI components | frontend | medium | todo | UI library setup |
| Upload 3 foto interface | frontend | high | todo | Drag & drop o file picker |
| GraphQL client setup | frontend | medium | todo | urql o Apollo Client |
| Visualizzazione risultati | frontend | medium | todo | Tabella semplice (no 3D per ora) |

---

## FASE 4: ML Pipeline Reale 🔮 (FUTURE)

| Task | Area | Priority | Status | Note |
|---|---|---|---|---|
| MediaPipe pose estimation | inference | high | todo | Estrazione landmark corporei |
| SMPL-X body model integration | inference | high | todo | Fitting modello parametrico |
| Calcolo metriche reali | inference | high | todo | Body fat %, volume, densità |
| 3D mesh generation | inference | medium | todo | Export .obj file |
| 3D viewer (React Three Fiber) | frontend | medium | todo | Visualizzazione mesh |

---

## Completed Earlier

| Task | Area | Priority | Status | Date | Note |
|---|---|---|---|---|---|
| Logging strutturato e /health endpoint | backend | medium | done | 2025-11-01 | Endpoint /health già implementato |
| README promozionale | docs | medium | done | 2025-11-01 | Badges, architecture, features |
| GitHub Actions CI/CD | infra | medium | done | 2025-11-01 | Lint + test workflow |
| Pre-commit hooks | backend | medium | done | 2025-11-01 | ruff + mypy |

---

## Future Enhancements

| Task | Area | Priority | Status | Note |
|---|---|---|---|---|
| Supabase Auth integration | backend | medium | todo | User authentication |
| Setup Dockerfile + docker-compose | infra | medium | todo | Containerizzazione |
| Historical tracking dashboard | frontend | low | todo | Grafici evoluzione metriche |
| PDF report generation | backend | low | todo | Export report analisi |
| Mobile app (React Native) | frontend | low | todo | App nativa iOS/Android |
| Production deployment | infra | low | todo | Docker/K8s deployment |

---

## Notes

**Current Focus:** FASE 4 - Frontend Setup (Next.js)

**Database:** SQLite locale per sviluppo (`bodyvision.db`), PostgreSQL per produzione

**Completed (FASE 1, 2 & 3):**
- ✅ Database models + migrations (FASE 1)
- ✅ Worker Dramatiq mock funzionante (FASE 2)
- ✅ POST /predict che accoda job e salva in DB (FASE 2)
- ✅ GET /predict/{job_id} che ritorna risultati (FASE 2)
- ✅ Test end-to-end del flusso completo (FASE 2)
- ✅ Redis automation con Makefile (FASE 2)
- ✅ GraphQL schema completo con Strawberry (FASE 3)
- ✅ 8 GraphQL queries con relationships (FASE 3)
- ✅ GraphiQL UI + documentation (FASE 3)

**Next Session Goals:**
1. Setup Next.js 14 con App Router
2. Shadcn/UI + Tailwind configuration
3. GraphQL client (urql o Apollo)
4. Upload interface + results display

**Backend Status:** COMPLETO! 🎉🎉
- ✅ REST API con job queue
- ✅ GraphQL API con query complesse
- ✅ Database persistence
- ✅ Worker background con mock results
- ✅ Redis automation
- ✅ Complete testing + documentation
- 🚀 **Ready per frontend integration!**

**API Endpoints:**
- REST: `/api/predict/` (POST/GET)
- GraphQL: `/graphql` (POST) con GraphiQL UI
- Health: `/health`
- Docs: `/docs` (Swagger)

---

Last Updated: 2025-11-02
