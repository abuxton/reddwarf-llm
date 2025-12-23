# https://github.com/krisnova/Makefile/blob/main/Makefile
# GitHub Specify: https://github.com/specify/specify

-include .env

REPO_TOP=$(shell git rev-parse --show-toplevel)
MK_DIR=${REPO_TOP}/common/mk

.PHONY: help-reddwarf setup venv test lint format run docker-build docker-run download-models clean

setup:  ## Initial setup - Install deps, download models, prep environment
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "  🚀 Red Dwarf Tiny LLM - Initial Setup"
	@echo "  \"I'm going to eat you, little fishy...\""
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🐍 Step 0: Checking for virtual environment..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "⚠️  No virtual environment detected!"; \
		echo "   Please create and activate a venv first:"; \
		echo "   python3 -m venv .venv"; \
		echo "   source .venv/bin/activate"; \
		echo "   Then run 'make setup' again"; \
		exit 1; \
	fi
	@echo "✅ Virtual environment active: $$VIRTUAL_ENV"
	@echo ""
	@echo "📦 Step 1: Installing Python dependencies..."
	pip install -e '.[dev]'
	@echo ""
	@echo "🧠 Step 2: Downloading models from HuggingFace..."
	@if [ -f scripts/download-models.sh ]; then \
		bash scripts/download-models.sh; \
	else \
		echo "⚠️  Model download script not found - skipping for now"; \
	fi
	@echo ""
	@echo "🪝 Step 3: Installing pre-commit hooks (optional)..."
	@if command -v pre-commit >/dev/null 2>&1; then \
		pre-commit install; \
	else \
		echo "⚠️  pre-commit not available - skipping hooks"; \
	fi
	@echo ""
	@echo "✅ Setup complete! Ready to run:"
	@echo "   - 'make test' to run tests"
	@echo "   - 'make run' to start the FastAPI server"
	@echo "   - 'make help-reddwarf' for all available commands"
	@echo ""

venv:  ## Create virtual environment
	@echo "🐍 Creating virtual environment..."
	python3 -m venv .venv
	@echo "✅ Virtual environment created!"
	@echo "   Activate it with: source .venv/bin/activate"
	@echo "   Then run: make setup"

help-reddwarf:  ## Show this help message - Red Dwarf style!
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "  Red Dwarf Tiny LLM - Available Commands"
	@echo "  \"Everybody's dead, Dave. Everybody's dead, Dave.\""
	@echo "═══════════════════════════════════════════════════════════════"
# 	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MK_DIR)/reddwarf.mk) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

test:  ## Run tests with coverage (Holly's IQ test equivalent)
	@echo "🚀 Running tests - hoping for better than IQ 6000..."
	pytest --cov=src/reddwarf --cov-report=html --cov-report=term-missing tests/

test-unit:  ## Run only unit tests
	@echo "🧪 Running unit tests..."
	pytest tests/unit/

test-integration:  ## Run only integration tests
	@echo "🔗 Running integration tests..."
	pytest tests/integration/

test-contract:  ## Run only contract tests
	@echo "📋 Running contract tests..."
	pytest tests/contract/

test-performance:  ## Run only performance tests
	@echo "⚡ Running performance tests..."
	pytest tests/performance/

lint:  ## Run linters (mypy, ruff) - Channel your inner Rimmer
	@echo "🔍 Running type checking with mypy..."
	mypy src/ tests/
	@echo "🔍 Running linter with ruff..."
	ruff check src/ tests/

format:  ## Format code (black, isort) - Make it prettier than Cat
	@echo "💅 Formatting code with black..."
	black src/ tests/ scripts/
	@echo "📦 Sorting imports with isort..."
	isort src/ tests/ scripts/

run:  ## Run FastAPI server locally - Fire up Holly's brain!
	@echo "🚀 Starting Red Dwarf LLM server..."
	@echo "   API docs at: http://localhost:8000/docs"
	uvicorn reddwarf.api.main:app --reload --host 0.0.0.0 --port 8000

docker-build:  ## Build Docker image - Construct the mining ship
	@echo "🐋 Building Docker image..."
	docker build -f docker/Dockerfile -t reddwarf-llm:latest .

docker-run:  ## Run Docker container - Launch into deep space!
	@echo "🚀 Launching Red Dwarf container..."
	docker-compose -f docker/docker-compose.yml up

download-models:  ## Download models from HuggingFace - Fetch Holly's brain!
	@echo "🧠 Downloading models from HuggingFace..."
	@if [ -f scripts/download-models.sh ]; then \
		bash scripts/download-models.sh; \
	else \
		echo "❌ scripts/download-models.sh not found - creating it first..."; \
		echo "Run this makefile target again after quote extraction is complete."; \
	fi

clean:  ## Clean cache and build artifacts - Smeg it all!
	@echo "🧹 Cleaning cache and build artifacts..."
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/ dist/ build/ src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✨ Clean as Lister's laundry (which is... not very clean)"

install:  ## Install package in editable mode with dev dependencies
	@echo "📦 Installing Red Dwarf LLM in editable mode..."
	pip install -e '.[dev]'

install-prod:  ## Install package in production mode (no dev dependencies)
	@echo "📦 Installing Red Dwarf LLM (production)..."
	pip install -e .

pre-commit-install:  ## Install pre-commit hooks
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install

pre-commit-run:  ## Run pre-commit hooks on all files
	@echo "🪝 Running pre-commit hooks..."
	pre-commit run --all-files
