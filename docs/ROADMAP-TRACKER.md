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

## FASE 2: Backend Funzionante 🚧 (IN PROGRESS)

### Current Tasks

| Task | Area | Priority | Status | Note |
|---|---|---|---|---|
| Inference Dummy Worker | inference | high | todo | Mock worker con Dramatiq che genera risultati fake |
| POST /predict endpoint completo | backend | high | todo | Accoda job Dramatiq e salva su DB |
| GET /predict/{job_id} endpoint | backend | high | todo | Ritorna status + risultati da DB |
| Upload test a Supabase Storage | backend | medium | todo | Test integrazione storage |
| Test unitari per endpoints | backend | high | todo | pytest per API + database |

### Next Steps
1. Creare worker Dramatiq con task mock
2. Implementare POST /predict che:
   - Valida input
   - Crea record in `analysis_sessions`
   - Accoda job Dramatiq
   - Ritorna job_id
3. Implementare GET /predict/{job_id} che:
   - Recupera session + measurements da DB
   - Ritorna status e risultati

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

**Current Focus:** FASE 2 - Implementare worker Dramatiq dummy + API endpoints completi

**Database:** SQLite locale per sviluppo (`bodyvision.db`), PostgreSQL per produzione

**Next Session Goals:**
1. ✅ Worker Dramatiq mock funzionante
2. ✅ POST /predict che accoda job e salva in DB
3. ✅ GET /predict/{job_id} che ritorna risultati
4. ✅ Test end-to-end del flusso completo

---

Last Updated: 2025-11-02
