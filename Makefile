.PHONY: help install dev test lint format clean

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
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

redis-start: ## Start Redis server
	redis-server --daemonize yes

redis-stop: ## Stop Redis server
	redis-cli shutdown

.DEFAULT_GOAL := help
