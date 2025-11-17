.PHONY: help install install-dev clean clean-pyc clean-build lint format type-check test test-cov test-unit test-integration run run-env-gen build check pre-commit upgrade-deps

.DEFAULT_GOAL := help

# Color output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)GenAI 3D Virtual Reality & Augmented Reality Platform$(NC)"
	@echo "$(BLUE)Author: Ruslan Magana | Website: ruslanmv.com$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: ## Install the project dependencies using uv
	@echo "$(BLUE)Installing dependencies with uv...$(NC)"
	uv pip install -e .
	@echo "$(GREEN)✓ Installation complete!$(NC)"

install-dev: ## Install the project with development dependencies
	@echo "$(BLUE)Installing development dependencies with uv...$(NC)"
	uv pip install -e ".[dev,test,docs]"
	@echo "$(GREEN)✓ Development installation complete!$(NC)"

upgrade-deps: ## Upgrade all dependencies to latest versions
	@echo "$(BLUE)Upgrading dependencies...$(NC)"
	uv pip install --upgrade -e ".[dev,test,docs]"
	@echo "$(GREEN)✓ Dependencies upgraded!$(NC)"

##@ Development

run: ## Run the Gradio web application
	@echo "$(BLUE)Starting Gradio web application...$(NC)"
	python genai_3d_vr_ar/app.py

run-env-gen: ## Run the environment generator (CLI)
	@echo "$(BLUE)Starting environment generator...$(NC)"
	python genai_3d_vr_ar/generate_environment.py

##@ Code Quality

lint: ## Run linting with ruff
	@echo "$(BLUE)Running ruff linter...$(NC)"
	ruff check .
	@echo "$(GREEN)✓ Linting complete!$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code with black...$(NC)"
	black .
	@echo "$(BLUE)Sorting imports with isort...$(NC)"
	isort .
	@echo "$(GREEN)✓ Code formatting complete!$(NC)"

format-check: ## Check code formatting without making changes
	@echo "$(BLUE)Checking code format...$(NC)"
	black --check .
	isort --check-only .
	@echo "$(GREEN)✓ Format check complete!$(NC)"

type-check: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks with mypy...$(NC)"
	mypy genai_3d_vr_ar
	@echo "$(GREEN)✓ Type checking complete!$(NC)"

check: lint format-check type-check ## Run all code quality checks
	@echo "$(GREEN)✓ All checks passed!$(NC)"

##@ Testing

test: ## Run all tests
	@echo "$(BLUE)Running all tests...$(NC)"
	pytest
	@echo "$(GREEN)✓ Tests complete!$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest --cov=genai_3d_vr_ar --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest -m unit
	@echo "$(GREEN)✓ Unit tests complete!$(NC)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest -m integration
	@echo "$(GREEN)✓ Integration tests complete!$(NC)"

test-verbose: ## Run tests with verbose output
	@echo "$(BLUE)Running tests (verbose)...$(NC)"
	pytest -vv
	@echo "$(GREEN)✓ Tests complete!$(NC)"

##@ Git & Pre-commit

pre-commit: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✓ Pre-commit hooks installed!$(NC)"

pre-commit-run: ## Run pre-commit on all files
	@echo "$(BLUE)Running pre-commit on all files...$(NC)"
	pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit checks complete!$(NC)"

##@ Build & Distribution

build: ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	uv build
	@echo "$(GREEN)✓ Build complete! Check dist/ directory$(NC)"

##@ Cleanup

clean: clean-pyc clean-build clean-test ## Remove all build, test, and Python artifacts

clean-pyc: ## Remove Python file artifacts
	@echo "$(BLUE)Cleaning Python artifacts...$(NC)"
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Python artifacts cleaned!$(NC)"

clean-build: ## Remove build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Build artifacts cleaned!$(NC)"

clean-test: ## Remove test and coverage artifacts
	@echo "$(BLUE)Cleaning test artifacts...$(NC)"
	rm -rf .tox/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	@echo "$(GREEN)✓ Test artifacts cleaned!$(NC)"

##@ Docker (Future)

docker-build: ## Build Docker image (placeholder)
	@echo "$(YELLOW)Docker support coming soon...$(NC)"

docker-run: ## Run Docker container (placeholder)
	@echo "$(YELLOW)Docker support coming soon...$(NC)"

##@ Documentation

docs-serve: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation...$(NC)"
	mkdocs serve

docs-build: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	mkdocs build
	@echo "$(GREEN)✓ Documentation built in site/ directory$(NC)"

##@ Environment

env-create: ## Create .env file from template
	@if [ ! -f .env ]; then \
		echo "$(BLUE)Creating .env file from template...$(NC)"; \
		cp .env.example .env; \
		echo "$(GREEN)✓ .env file created! Please update with your credentials.$(NC)"; \
	else \
		echo "$(YELLOW)⚠ .env file already exists!$(NC)"; \
	fi

env-check: ## Check if .env file exists and has required variables
	@echo "$(BLUE)Checking environment configuration...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(RED)✗ .env file not found! Run 'make env-create' first.$(NC)"; \
		exit 1; \
	fi
	@if grep -q "<your" .env; then \
		echo "$(YELLOW)⚠ Warning: .env contains placeholder values!$(NC)"; \
		echo "$(YELLOW)  Please update PROJECT_ID and API_KEY with your credentials.$(NC)"; \
	else \
		echo "$(GREEN)✓ Environment configuration looks good!$(NC)"; \
	fi

##@ CI/CD

ci: clean install-dev check test ## Run full CI pipeline locally
	@echo "$(GREEN)✓ CI pipeline complete!$(NC)"

##@ Info

info: ## Display project information
	@echo "$(BLUE)╔═══════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║  GenAI 3D Virtual Reality & Augmented Reality Platform   ║$(NC)"
	@echo "$(BLUE)╚═══════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Author:$(NC)   Ruslan Magana"
	@echo "$(GREEN)Website:$(NC)  ruslanmv.com"
	@echo "$(GREEN)License:$(NC)  Apache 2.0"
	@echo "$(GREEN)Version:$(NC)  1.0.0"
	@echo ""
	@echo "$(BLUE)Description:$(NC)"
	@echo "  Production-ready GenAI platform for 3D VR/AR content generation"
	@echo "  with IBM WatsonX.ai integration and Stable Diffusion support."
	@echo ""
	@echo "$(BLUE)Features:$(NC)"
	@echo "  • AI-powered 360° image generation"
	@echo "  • WatsonX.ai prompt enrichment"
	@echo "  • Meta Quest 3 & Apple Vision Pro support"
	@echo "  • Unreal Engine 5 smart NPC integration"
	@echo ""
	@echo "$(GREEN)Quick Start:$(NC)"
	@echo "  1. make install-dev"
	@echo "  2. make env-create"
	@echo "  3. Edit .env with your credentials"
	@echo "  4. make run"
	@echo ""
