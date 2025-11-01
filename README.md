# BodyVision

Sistema full-stack per la stima della composizione corporea tramite analisi di immagini standardizzate (fronte, lato, retro) o acquisizione da fotocamera in tempo reale.

## Obiettivo

- Guidare l'utente nell'assunzione di pose corrette
- Estrarre struttura corporea tramite pose estimation
- Approssimare volume, densità e body fat %
- Generare una mesh 3D scaricabile

## Stack Tecnologico

### Backend
- **FastAPI** 0.120.0 - Modern web framework
- **Strawberry GraphQL** 0.284.1 - GraphQL server
- **SQLAlchemy** 2.0 + **Alembic** - ORM e migrations
- **Dramatiq** + **Redis** - Background job processing
- **Supabase** - PostgreSQL + Object Storage
- **Python** 3.12+ con **uv** per dependency management

### Frontend
- **Next.js** 14+ (App Router)
- **TypeScript** 5+
- **Shadcn/UI** (Radix + Tailwind CSS)
- **React Three Fiber** - 3D mesh visualization

### ML/Inference
- **PyTorch** 2.5+
- **MediaPipe** - Pose estimation
- **SMPL-X/STAR/GHUM** - Parametric body models (feature flag)
- **trimesh** - Mesh generation

## Struttura Progetto

```
body-vision/
├── backend/              # FastAPI + Strawberry GraphQL
│   ├── app/
│   │   ├── api/         # REST endpoints
│   │   ├── core/        # Configuration
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   └── tests/
├── frontend/            # Next.js application
├── inference/           # ML inference engine + workers
│   ├── app/
│   └── tests/
├── infra/              # Docker, docker-compose
├── scripts/            # Utility scripts
└── docs/               # Documentation
```

## Setup Sviluppo

### Prerequisiti

- Python 3.12+
- Node.js 20+
- Redis
- PostgreSQL (o Supabase account)
- uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installazione Backend

```bash
# Crea virtual environment
uv venv

# Attiva venv
source .venv/bin/activate  # Linux/macOS
# oppure
.venv\Scripts\activate     # Windows

# Installa dipendenze
uv pip install -e ".[dev,test]"

# Copia e configura .env
cp .env.example .env
# Modifica .env con le tue credenziali Supabase

# Avvia il server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Installazione Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker (Opzionale)

```bash
docker-compose -f infra/docker/docker-compose.dev.yml up
```

## API Endpoints

### REST
- `GET /health` - Health check
- `POST /api/predict` - Queue body composition analysis
- `GET /api/predict/{job_id}` - Get job status

### GraphQL
- `/graphql` - GraphQL Playground (dev mode)

## Configurazione

Il progetto utilizza variabili d'ambiente per la configurazione. Vedi `.env.example` per tutte le opzioni disponibili.

### Feature Flag Modelli

Seleziona il modello parametrico tramite:
```bash
BODYVISION_MODEL=smplx  # Options: smplx | star | ghum
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=backend --cov=inference --cov-report=html

# Run specific test file
pytest backend/tests/test_predict.py
```

## Code Quality

```bash
# Format code
ruff format .

# Lint
ruff check .

# Type check
mypy backend/ inference/

# Pre-commit hooks (auto-setup on first commit)
pre-commit install
pre-commit run --all-files
```

## Deployment

TBD - Docker + Kubernetes / Railway / Vercel

## Roadmap

Vedi [ROADMAP-TRACKER.md](docs/ROADMAP-TRACKER.md) per il piano di sviluppo completo.

## Architettura

Vedi [ARCHITECTURE-DESIGN.md](docs/ARCHITECTURE-DESIGN.md) per i dettagli architetturali.

## Best Practices

Vedi [CODE-BEST-PRACTICE.md](docs/CODE-BEST-PRACTICE.md) per le linee guida di sviluppo.

## License

MIT

## Contributors

- [Il tuo nome]
