# CODE-BEST-PRACTICE.md

## Scopo
Linee guida pratiche e snippet per sviluppare, testare e mantenere BodyVision (monorepo).

## Struttura della monorepo
```
/ (root)
├─ backend/
├─ frontend/
├─ inference/
├─ infra/
├─ scripts/
└─ README.md
```

## Naming & Style
- Python: snake_case per funzioni/variabili, CamelCase per classi
- Frontend (TSX/JSX): PascalCase per componenti, camelCase per props
- Linters & Formatting: black, ruff, mypy, pre-commit hooks

## Dependency Management
- uv per installazione e lock delle dipendenze
- separazione dev/test groups

## Config & Feature Flags
- `backend/app/core/config.py` con Pydantic BaseSettings
- BODYVISION_MODEL = smplx|smpl|ghum|light

## API Design
- REST per mutazioni (POST /predict)
- GraphQL per query complesse
- Idempotenza tramite job_id

## Worker & Background Jobs
- RQ o Dramatiq
- Scarica immagini da Supabase e calcola metriche
- Salva risultati in DB e Storage

## Storage & Supabase
- Upload diretto dal browser
- Backend scarica solo URL firmati
- Pulizia temp files

## Logging & Observability
- structlog o loguru con job_id correlation
- /health endpoint

## Error Handling & Security
- Validazione Pydantic
- SECURE_LOAD flag per joblib/pickle
- HTTPS in produzione

## Testing
- pytest unit + smoke
- Mock per broker e storage

## CI / Quality Gates
- GitHub Actions: ruff, black, mypy, pytest
- Pre-commit hooks

## Snippets
- FastAPI health endpoint
- Worker progress update
- Dev mode dummy model
