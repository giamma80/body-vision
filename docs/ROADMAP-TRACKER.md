# ROADMAP-TRACKER.md

## Legenda
- Status: todo | in-progress | done
- Priority: high | medium | low

## Backlog & Attività

| Task | Area | Priority | Status | Note |
|---|---|---|---|---|
| Setup monorepo struttura base | infra | high | todo | inizializzare backend, frontend, inference, infra |
| Configurare uv + pyproject + lock | backend | high | todo | gestione dipendenze e lockfile |
| Setup Dockerfile + docker-compose.dev.yml | infra | high | todo | container backend, frontend, worker |
| Implementare upload foto frontend → Supabase | frontend | high | todo | cattura foto, gestione signed URL |
| Implementare POST /predict | backend | high | todo | job queue e background task |
| Implementare GraphQL queries | backend | medium | todo | consultazione risultati e storico |
| Worker: download immagini, preprocessing, inferenza | inference | high | todo | gestione feature flag modelli |
| Logging strutturato e /health endpoint | backend | medium | todo | includere job_id |
| Test unitari e smoke | backend | high | todo | pytest e mock broker/storage |
| Dev mode dummy model | backend | medium | todo | scripts/create-dev-model.py |
| Frontend UI: guida pose, mesh viewer | frontend | medium | todo | Shadcn/UI + Tailwind |
| Documentazione finale | docs | medium | todo | README, ARCHITECTURE-DESIGN, CODE-BEST-PRACTICE, ROADMAP-TRACKER |
