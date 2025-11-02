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

## FASE 3: GraphQL + Frontend Minimale 📋 (PLANNED)

| Task | Area | Priority | Status | Note |
|---|---|---|---|---|
| Strawberry GraphQL schema | backend | medium | todo | Query per sessioni e misurazioni |
| Next.js 14 setup | frontend | high | todo | App Router + TypeScript |
| Shadcn/UI components | frontend | medium | todo | UI library setup |
| Upload 3 foto interface | frontend | high | todo | Drag & drop o file picker |
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

**Current Focus:** FASE 3 - Frontend Setup o GraphQL Schema

**Database:** SQLite locale per sviluppo (`bodyvision.db`), PostgreSQL per produzione

**Completed (FASE 1 & 2):**
- ✅ Database models + migrations
- ✅ Worker Dramatiq mock funzionante
- ✅ POST /predict che accoda job e salva in DB
- ✅ GET /predict/{job_id} che ritorna risultati
- ✅ Test end-to-end del flusso completo
- ✅ Redis automation con Makefile
- ✅ Complete documentation

**Next Session Goals:**
1. Setup GraphQL schema con Strawberry
2. Oppure: Setup Next.js 14 frontend
3. Oppure: Supabase integration setup

**MVP Status:** Backend completo e funzionante! 🎉
- API REST con job queue
- Database persistence
- Worker background con mock results
- Ready per frontend integration

---

Last Updated: 2025-11-02
