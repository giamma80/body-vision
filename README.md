<div align="center">

# 🏋️ BodyVision

### AI-Powered Body Composition Analysis from Images

*Transform simple photos into precise 3D body metrics using state-of-the-art computer vision and parametric body models*

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120.0-009688.svg)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1-EE4C2C.svg)](https://pytorch.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Roadmap](#-roadmap) • [Contributing](#-contributing)

</div>

---

## 🎯 What is BodyVision?

**BodyVision** is a cutting-edge, full-stack system that estimates body composition metrics from standardized photos. Using advanced pose estimation and parametric 3D body models (SMPL-X, STAR, GHUM), it provides:

- **Body Fat Percentage** - Clinical-grade estimation
- **Body Density** - Volumetric analysis
- **3D Body Mesh** - Downloadable .obj file for visualization
- **Guided Photo Capture** - Real-time pose guidance for accuracy

Perfect for fitness tracking, health monitoring, virtual try-on applications, and body composition research.

---

## ✨ Features

### 🎥 Intelligent Photo Capture
- **Real-time pose guidance** using MediaPipe
- **Three-angle capture** (front, side, back)
- **Quality validation** to ensure accurate measurements
- **Browser-based** - no app installation required

### 🧠 Advanced ML Pipeline
- **Multiple body models** via feature flags (SMPL-X / STAR / GHUM)
- **GPU-accelerated** inference with CPU fallback
- **Async processing** with Dramatiq job queue
- **Model caching** for blazing-fast predictions

### 📊 Comprehensive Metrics
- Body fat percentage
- Body volume (liters)
- Body density (kg/L)
- Downloadable 3D mesh (.obj format)
- Historical tracking & trends

### 🏗️ Production-Ready Architecture
- **FastAPI** backend with Strawberry GraphQL
- **Next.js 14** frontend with App Router
- **Supabase** for storage & database
- **Docker** containerization
- **CI/CD** with GitHub Actions
- **Type-safe** with TypeScript + mypy

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Redis
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/giamma80/body-vision.git
cd body-vision

# Run the setup script
./scripts/init.sh

# Or manually:
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e ".[dev,test]"

# Copy environment variables
cp .env.example .env
# Edit .env with your Supabase credentials
```

### Run Development Server

```bash
# Start backend
make dev
# Or: uvicorn backend.app.main:app --reload

# Visit http://localhost:8000/docs for API documentation
```

### Run Tests

```bash
make test
# Or: pytest --cov=backend --cov=inference
```

---

## 🏛️ Architecture

```
┌─────────────────┐
│  Browser/Mobile │
│   (Next.js)     │
└────────┬────────┘
         │ Upload images
         ▼
┌─────────────────┐      ┌──────────────┐
│ Supabase Storage│◄────►│  PostgreSQL  │
└────────┬────────┘      └──────▲───────┘
         │                       │
         │ Image URLs            │ Metadata
         ▼                       │
┌─────────────────┐              │
│  FastAPI + GQL  │──────────────┘
└────────┬────────┘
         │ Queue job
         ▼
┌─────────────────┐
│ Dramatiq Worker │
│  (PyTorch ML)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Body Model     │
│ SMPL-X/STAR/GHUM│
└────────┬────────┘
         │
         ▼
  Results + 3D Mesh
```

### Tech Stack

#### Backend
- **FastAPI** 0.120.0 - High-performance async web framework
- **Strawberry GraphQL** 0.284.1 - Type-safe GraphQL server
- **SQLAlchemy** 2.0 + **Alembic** - Database ORM & migrations
- **Dramatiq** + **Redis** - Distributed task queue
- **Supabase** - PostgreSQL + Object Storage + Auth
- **Python 3.12** with **uv** for dependency management

#### Frontend
- **Next.js** 14+ with App Router
- **TypeScript** 5+ for type safety
- **Shadcn/UI** (Radix + Tailwind CSS)
- **React Three Fiber** for 3D visualization
- **urql** for GraphQL client

#### ML/Inference
- **PyTorch** 2.5.1 - Deep learning framework
- **MediaPipe** - Pose estimation & body landmarks
- **SMPL-X/STAR/GHUM** - Parametric 3D body models
- **trimesh** - 3D mesh processing
- **OpenCV** - Image preprocessing

#### DevOps
- **Docker** + **Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **uv** - Ultra-fast Python package management
- **ruff** - Lightning-fast linter & formatter
- **mypy** - Static type checking
- **pytest** - Testing framework

---

## 📁 Project Structure

```
body-vision/
├── backend/              # FastAPI + Strawberry GraphQL API
│   ├── app/
│   │   ├── api/         # REST endpoints & GraphQL schema
│   │   ├── core/        # Configuration & settings
│   │   ├── models/      # SQLAlchemy database models
│   │   ├── schemas/     # Pydantic request/response schemas
│   │   └── services/    # Business logic layer
│   └── tests/           # Backend tests
├── frontend/            # Next.js web application
│   ├── app/            # Next.js App Router
│   ├── components/     # React components
│   └── lib/            # Utilities & GraphQL client
├── inference/           # ML inference engine
│   ├── app/            # Worker & model code
│   │   ├── models/     # SMPL-X/STAR/GHUM adapters
│   │   ├── tasks/      # Dramatiq async tasks
│   │   └── utils/      # Preprocessing & postprocessing
│   └── tests/          # Inference tests
├── infra/              # Infrastructure as code
│   └── docker/         # Dockerfiles & compose configs
├── scripts/            # Utility scripts
├── docs/               # Project documentation
└── pyproject.toml      # Python dependencies (uv)
```

---

## 🗺️ Roadmap

### Phase 1: Foundation ✅ (Current)
- [x] Project setup & monorepo structure
- [x] Backend API skeleton (FastAPI + GraphQL)
- [x] Configuration management with feature flags
- [x] CI/CD pipeline
- [x] Development environment setup

### Phase 2: Core Features 🚧 (In Progress)
- [ ] Frontend UI (Next.js + Shadcn)
- [ ] Camera capture & pose guidance
- [ ] Image upload to Supabase Storage
- [ ] REST endpoint for prediction jobs
- [ ] GraphQL queries for results

### Phase 3: ML Pipeline 📋 (Planned)
- [ ] Dramatiq worker implementation
- [ ] MediaPipe pose estimation
- [ ] SMPL-X body model integration
- [ ] Body metrics calculation
- [ ] 3D mesh generation & export

### Phase 4: Polish & Deploy 🔮 (Future)
- [ ] User authentication (Supabase Auth)
- [ ] Historical tracking & trends
- [ ] PDF report generation
- [ ] Mobile app (React Native)
- [ ] Production deployment (Docker/K8s)

See [ROADMAP-TRACKER.md](docs/ROADMAP-TRACKER.md) for detailed task breakdown.

---

## 🧪 Development

### Available Commands

```bash
make help          # Show all available commands
make install       # Install dependencies with uv
make dev           # Run development server
make test          # Run tests with coverage
make lint          # Run linters (ruff + mypy)
make format        # Format code with ruff
make pre-commit    # Install pre-commit hooks
make clean         # Clean cache files
```

### Running Tests

```bash
# All tests with coverage
pytest --cov=backend --cov=inference --cov-report=html

# Specific test file
pytest backend/tests/test_main.py

# Watch mode
pytest --watch
```

### Code Quality

The project uses:
- **ruff** for linting & formatting (replaces black, isort, flake8)
- **mypy** for static type checking
- **pre-commit** hooks for automated quality checks

```bash
# Format code
ruff format .

# Lint
ruff check .

# Type check
mypy backend/ inference/

# Run all quality checks
make lint && make format
```

---

## 🐳 Docker

```bash
# Build containers
make docker-build

# Start all services
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Run linters (`make lint`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- Follow [PEP 8](https://pep8.org/) for Python code
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions small and focused
- Add tests for new features

See [CODE-BEST-PRACTICE.md](docs/CODE-BEST-PRACTICE.md) for detailed guidelines.

---

## 📚 Documentation

- [Architecture Design](docs/ARCHITECTURE-DESIGN.md) - System architecture & diagrams
- [Code Best Practices](docs/CODE-BEST-PRACTICE.md) - Development guidelines
- [Roadmap Tracker](docs/ROADMAP-TRACKER.md) - Development progress
- [API Documentation](http://localhost:8000/docs) - Swagger UI (run server first)

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Body Model Selection
BODYVISION_MODEL=smplx  # Options: smplx | star | ghum

# Redis
REDIS_URL=redis://localhost:6379/0

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/bodyvision
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [SMPL-X](https://smpl-x.is.tue.mpg.de/) - Expressive body model
- [MediaPipe](https://mediapipe.dev/) - Cross-platform ML solutions
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Supabase](https://supabase.com/) - Open source Firebase alternative

---

<div align="center">

**Built with ❤️ using modern AI and web technologies**

[⭐ Star this repo](https://github.com/giamma80/body-vision) • [🐛 Report Bug](https://github.com/giamma80/body-vision/issues) • [💡 Request Feature](https://github.com/giamma80/body-vision/issues)

</div>
