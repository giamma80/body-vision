.PHONY: help install dev test lint format clean

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)BodyVision - Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies with uv
	uv venv
	uv pip install -e ".[dev,test]"

dev: ## Run development server
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests with coverage
	pytest --cov=backend --cov=inference --cov-report=term-missing --cov-report=html

test-watch: ## Run tests in watch mode
	pytest --watch

lint: ## Run linters (ruff + mypy)
	ruff check .
	mypy backend/ inference/

format: ## Format code with ruff
	ruff format .
	ruff check --fix .

pre-commit: ## Install pre-commit hooks
	pre-commit install
	pre-commit run --all-files

docker-build: ## Build Docker images
	docker-compose -f infra/docker/docker-compose.dev.yml build

docker-up: ## Start Docker containers
	docker-compose -f infra/docker/docker-compose.dev.yml up -d

docker-down: ## Stop Docker containers
	docker-compose -f infra/docker/docker-compose.dev.yml down

docker-logs: ## Show Docker logs
	docker-compose -f infra/docker/docker-compose.dev.yml logs -f

clean: ## Clean cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete

redis-check: ## Check if Redis is installed
	@command -v redis-server >/dev/null 2>&1 || { \
		echo "$(BLUE)Redis is not installed.$(NC)"; \
		echo "$(BLUE)Install with:$(NC)"; \
		echo "  macOS: brew install redis"; \
		echo "  Ubuntu: sudo apt-get install redis-server"; \
		echo "  Or visit: https://redis.io/download"; \
		exit 1; \
	}
	@echo "$(GREEN)✓ Redis is installed$(NC)"

redis-status: redis-check ## Check Redis server status
	@redis-cli ping >/dev/null 2>&1 && \
		echo "$(GREEN)✓ Redis is running$(NC)" || \
		echo "$(BLUE)Redis is not running. Start with: make redis-start$(NC)"

redis-start: redis-check ## Start Redis server (auto-detects platform)
	@if redis-cli ping >/dev/null 2>&1; then \
		echo "$(GREEN)✓ Redis is already running$(NC)"; \
	elif command -v brew >/dev/null 2>&1 && brew services list | grep -q redis; then \
		echo "$(BLUE)Starting Redis via Homebrew...$(NC)"; \
		brew services start redis && sleep 1; \
	else \
		echo "$(BLUE)Starting Redis server...$(NC)"; \
		redis-server --daemonize yes && sleep 1; \
	fi
	@make redis-status

redis-stop: ## Stop Redis server (auto-detects platform)
	@if ! redis-cli ping >/dev/null 2>&1; then \
		echo "$(BLUE)Redis is not running$(NC)"; \
	elif command -v brew >/dev/null 2>&1 && brew services list | grep redis | grep -q started; then \
		echo "$(BLUE)Stopping Redis via Homebrew...$(NC)"; \
		brew services stop redis; \
	else \
		echo "$(BLUE)Stopping Redis server...$(NC)"; \
		redis-cli shutdown 2>/dev/null || true; \
	fi

redis-restart: redis-stop redis-start ## Restart Redis server

worker: ## Start Dramatiq worker for background tasks
	./scripts/start_worker.sh

db-migrate: ## Create new database migration
	alembic revision --autogenerate -m "$(MSG)"

db-upgrade: ## Apply database migrations
	alembic upgrade head

db-downgrade: ## Rollback last migration
	alembic downgrade -1

.DEFAULT_GOAL := help
