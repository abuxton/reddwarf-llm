# Phase 0: Research & Technology Decisions

**Feature**: Red Dwarf Tiny LLM Implementation
**Date**: 2025-12-22
**Status**: Complete

## Overview

This document consolidates research findings and technology decisions for the Red Dwarf tiny LLM project. All "NEEDS CLARIFICATION" items from Technical Context have been resolved through investigation of best practices, dependency evaluation, and architecture patterns.

---

## 1. Model Selection & Quantization Strategy

### Decision: TinyLlama-1.1B and Phi-2 as Primary Models

**Rationale**:
- **TinyLlama-1.1B**: 1.1B parameters, Apache 2.0 license, excellent for <8GB VRAM systems
  - Quantized 4-bit: ~600MB VRAM, ~1s inference for 512 tokens
  - Quantized 8-bit: ~1.2GB VRAM, ~0.8s inference for 512 tokens
  - Well-supported by HuggingFace Transformers and bitsandbytes
- **Phi-2**: 2.7B parameters, MIT license, higher quality responses
  - Quantized 4-bit: ~1.5GB VRAM, ~1.5s inference for 512 tokens
  - Quantized 8-bit: ~3GB VRAM, ~1.2s inference for 512 tokens
  - Microsoft Research model with excellent instruction following

**Alternatives Considered**:
- **GPT-2 Small (124M)**: Too small, poor coherence for conversational use
- **Mistral 7B**: Too large even quantized (~4GB 4-bit), exceeds 2s inference target on consumer GPUs
- **Llama-2 7B**: Same issue as Mistral, too resource-intensive for "tiny" focus

**Implementation**:
- Use `transformers.AutoModelForCausalLM.from_pretrained()` with `load_in_4bit=True` or `load_in_8bit=True`
- bitsandbytes library for quantization (CUDA) or Metal Performance Shaders fallback (macOS)
- Model registry in `src/reddwarf/model/registry.py` maps model names to HuggingFace IDs

**References**:
- TinyLlama: https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Phi-2: https://huggingface.co/microsoft/phi-2
- bitsandbytes quantization guide: https://huggingface.co/docs/transformers/main_classes/quantization

---

## 2. Python Type Hints Best Practices

### Decision: Strict Type Hints with mypy --strict

**Rationale**:
- **PEP 484/585/604**: Use modern type syntax (`list[str]` not `List[str]` for Python 3.10+)
- **mypy strict mode**: Catches all type errors including `Any` usage, untyped decorators
- **Pydantic for data validation**: Runtime validation + type checking for API models
- **Protocol for interfaces**: Define contracts without inheritance (e.g., `ModelLoader` protocol)

**Alternatives Considered**:
- **Minimal typing**: Rejected - violates constitution "Type hints mandatory for all public APIs"
- **pyright/pylance only**: Rejected - mypy has better CI integration and configuration options
- **runtime_checkable**: Considered excessive for internal code, reserved for plugin systems

**Implementation**:
```python
# Good: Strict types with Pydantic
from pydantic import BaseModel, Field
from typing import Protocol

class InferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2048)
    max_tokens: int = Field(512, ge=1, le=2048)
    temperature: float = Field(0.7, ge=0.0, le=2.0)

class ModelLoader(Protocol):
    def load(self, model_id: str, quantization: str) -> torch.nn.Module:
        ...
```

**Configuration**:
- `mypy.ini`: `strict = true`, `warn_unused_ignores = true`, `disallow_any_unimported = true`
- Pre-commit hook runs mypy on all changed files
- CI fails on type errors

**References**:
- mypy documentation: https://mypy.readthedocs.io/en/stable/
- Pydantic docs: https://docs.pydantic.dev/latest/

---

## 3. FastAPI Architecture for Future MCP Server

### Decision: FastAPI with Layered Architecture

**Rationale**:
- **FastAPI**: Async support, automatic OpenAPI docs, Pydantic integration, production-ready
- **Layered separation**: API endpoints → Service layer → Model/inference layer
- **Dependency injection**: FastAPI's `Depends()` for clean testing and modularity
- **Future MCP compatibility**: REST endpoints can wrap MCP protocol with minimal refactoring

**Alternatives Considered**:
- **Flask**: Rejected - lacks async support, less modern type integration
- **Django**: Rejected - too heavyweight for this project, violates "Tiny & Maintainable"
- **gRPC**: Rejected - overkill for single-user local deployment, complicates devcontainer setup

**Implementation**:
```python
# src/reddwarf/api/main.py
from fastapi import FastAPI, Depends
from .endpoints import router as inference_router

app = FastAPI(title="Red Dwarf Tiny LLM", version="0.1.0")
app.include_router(inference_router, prefix="/api/v1")

# src/reddwarf/api/endpoints.py
@router.post("/infer", response_model=InferenceResponseAPI)
async def infer(
    request: InferenceRequestAPI,
    engine: InferenceEngine = Depends(get_inference_engine)
) -> InferenceResponseAPI:
    # Service layer call, no business logic in endpoint
    result = await engine.generate(request)
    return InferenceResponseAPI.from_domain(result)
```

**MCP Integration Path**:
- Current: REST endpoints for HTTP inference
- Future: MCP server wraps same service layer, adds tool use and context management
- Service layer remains unchanged, only API layer adapts to MCP protocol

**References**:
- FastAPI docs: https://fastapi.tiangolo.com/
- MCP specification: https://modelcontextprotocol.io/

---

## 4. Testing Strategy with Red Dwarf Themed Data

### Decision: Pytest with Fixtures for Character Scenarios

**Rationale**:
- **pytest**: Industry standard, excellent fixture system, async support
- **pytest-cov**: Coverage reporting integrated into test runs
- **Character-themed fixtures**: Create reusable test scenarios tied to Red Dwarf episodes
- **Parameterized tests**: Test multiple models/quantization levels with same scenarios

**Alternatives Considered**:
- **unittest**: Rejected - more verbose, less expressive than pytest
- **nose2**: Rejected - less active development than pytest
- **Hypothesis property-based testing**: Considered for future fuzz testing, not MVP

**Implementation**:
```python
# tests/fixtures/test_prompts.py
LISTER_SCENARIOS = [
    {"prompt": "What's for dinner?", "expected_theme": "vindaloo"},
    {"prompt": "Calculate route to Earth", "expected_theme": "navigation"}
]

RIMMER_SCENARIOS = [
    {"prompt": "List my achievements", "expected_theme": "none"},
    {"prompt": "Explain risk assessment", "expected_theme": "bureaucracy"}
]

# tests/conftest.py
@pytest.fixture
def mock_model():
    """Holly's IQ 6000 brain - I mean, mock model"""
    return MockTinyLLM()

@pytest.fixture
def red_dwarf_quotes():
    """Curated quotes database for testing"""
    return QuoteDatabase.from_json("tests/fixtures/test_quotes.json")

# tests/integration/test_end_to_end_inference.py
@pytest.mark.parametrize("scenario", LISTER_SCENARIOS)
def test_lister_scenarios(scenario, mock_model, red_dwarf_quotes):
    engine = InferenceEngine(model=mock_model, formatter=ResponseFormatter(quotes=red_dwarf_quotes))
    response = engine.generate(InferenceRequest(prompt=scenario["prompt"]))
    assert scenario["expected_theme"] in response.text.lower()
    assert response.opening_quote is not None
    assert response.closing_quote is not None
```

**Coverage Targets**:
- Unit tests: 90%+ for core logic (model loading, inference, quote selection)
- Integration tests: 70%+ for end-to-end flows
- Contract tests: 100% for API endpoints
- Overall: 80%+ as per constitution

**References**:
- pytest documentation: https://docs.pytest.org/
- pytest-cov: https://pytest-cov.readthedocs.io/

---

## 5. Devcontainer Configuration Best Practices

### Decision: Python 3.10+ with CUDA/Metal GPU Passthrough

**Rationale**:
- **Base image**: `mcr.microsoft.com/devcontainers/python:3.10` (official Microsoft image)
- **GPU support**: NVIDIA Container Toolkit for CUDA passthrough (Linux)
- **macOS limitation**: Metal GPU not accessible in containers, document CPU fallback
- **Pre-installed tools**: black, isort, mypy, pytest, pre-commit
- **HuggingFace cache**: Mount local cache to avoid re-downloading models

**Alternatives Considered**:
- **Custom Dockerfile**: Rejected - base images maintained by Microsoft more reliable
- **PyTorch Docker**: Considered but too heavyweight, includes unnecessary tools
- **Conda environment**: Rejected - pip is sufficient, Conda adds complexity

**Implementation**:
```json
// .devcontainer/devcontainer.json
{
  "name": "Red Dwarf LLM Dev",
  "image": "mcr.microsoft.com/devcontainers/python:3.10",
  "features": {
    "ghcr.io/devcontainers/features/nvidia-cuda:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "mounts": [
    "source=${localEnv:HOME}/.cache/huggingface,target=/root/.cache/huggingface,type=bind"
  ],
  "postCreateCommand": "pip install -e '.[dev]'",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff"
      ]
    }
  }
}
```

**GPU Passthrough**:
- Linux: Requires `nvidia-container-toolkit` on host, Docker 19.03+
- macOS: Not supported - document fallback to CPU inference or local (non-container) development
- Windows: WSL2 + CUDA passthrough documented separately

**References**:
- VS Code devcontainers: https://code.visualstudio.com/docs/devcontainers/containers
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/

---

## 6. Docker Deployment Strategy

### Decision: Multi-stage Build with Model Caching

**Rationale**:
- **Multi-stage build**: Separate build and runtime stages to minimize image size
- **Model caching**: Option 1: Bake models into image (large but offline-capable)
- **Model caching**: Option 2: Volume mount for models (smaller image, requires download)
- **Default: Option 2** - More flexible, users can update models without rebuilding image

**Alternatives Considered**:
- **Single-stage build**: Rejected - results in bloated images with build tools
- **Baked models**: Rejected as default - 1-2GB per model makes images huge
- **Docker Compose with external services**: N/A - single-container deployment sufficient

**Implementation**:
```dockerfile
# docker/Dockerfile
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY makefile pyproject.toml setup.py ./
ENV PATH=/root/.local/bin:$PATH
ENV TRANSFORMERS_CACHE=/app/models

# Install package
RUN pip install --no-cache-dir -e .

EXPOSE 8000
CMD ["uvicorn", "reddwarf.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  reddwarf-llm:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./data/models:/app/models  # Model cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

**References**:
- Docker best practices: https://docs.docker.com/develop/dev-best-practices/
- Multi-stage builds: https://docs.docker.com/build/building/multi-stage/

---

## 7. Red Dwarf Quotes Database Design

### Decision: JSON File with Category Metadata

**Rationale**:
- **Format**: JSON for simplicity, readability, and easy manual curation
- **Structure**: List of quote objects with `text`, `character`, `episode`, `season` fields
- **Session tracking**: In-memory set of used quote IDs per session, reset on restart
- **No external database**: Overkill for ~50-200 quotes, violates "Tiny & Maintainable"

**Alternatives Considered**:
- **SQLite**: Rejected - adds complexity for minimal benefit with small dataset
- **YAML**: Rejected - JSON parsing faster, better Python stdlib support
- **Hardcoded Python dict**: Rejected - less maintainable, harder for non-coders to contribute

**Implementation**:
```json
// src/reddwarf/quotes/quotes.json
[
  {
    "id": 1,
    "text": "Everybody's dead, Dave.",
    "character": "Holly",
    "episode": "The End",
    "season": 1
  },
  {
    "id": 2,
    "text": "I'm going to eat you little fishie.",
    "character": "Cat",
    "episode": "Confidence and Paranoia",
    "season": 1
  },
  {
    "id": 3,
    "text": "Smoke me a kipper, I'll be back for breakfast.",
    "character": "Ace Rimmer",
    "episode": "Dimension Jump",
    "season": 4
  }
]
```

```python
# src/reddwarf/quotes/selector.py
class QuoteSelector:
    def __init__(self, database: QuoteDatabase):
        self._db = database
        self._used_ids: set[int] = set()

    def get_random_quote(self) -> Quote:
        available = [q for q in self._db.quotes if q.id not in self._used_ids]
        if not available:
            self._used_ids.clear()  # Reset after exhausting all quotes
            available = self._db.quotes
        quote = random.choice(available)
        self._used_ids.add(quote.id)
        return quote
```

**Curation Process**:
- Manual review of Red Dwarf transcripts for iconic quotes
- Verify quotes are show-accurate, avoid misattributions
- Prioritize Holly, Lister, Rimmer, Cat, Kryten for character balance
- Script: `scripts/validate-quotes.py` checks JSON schema and duplicates

**References**:
- Red Dwarf transcripts: http://www.reddwarf.co.uk/ (fan community resource)

---

## 8. Performance Monitoring & Logging

### Decision: Python logging Module with Structured Logs

**Rationale**:
- **stdlib logging**: No external dependencies, well-understood, sufficient for single-user deployment
- **Structured format**: JSON logs for easy parsing/analysis if needed
- **Metrics tracked**: Inference time, memory usage (VRAM/RAM), token throughput, errors
- **Log levels**: DEBUG for development, INFO for production, ERROR for failures

**Alternatives Considered**:
- **Prometheus/Grafana**: Rejected - overkill for single-user local deployment
- **OpenTelemetry**: Rejected - adds complexity, no distributed tracing needed
- **Custom metrics library**: Rejected - stdlib logging + simple metrics module sufficient

**Implementation**:
```python
# src/reddwarf/monitoring/logger.py
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def log_inference(
        self,
        prompt_length: int,
        response_length: int,
        inference_time_ms: float,
        memory_mb: float,
        model: str
    ) -> None:
        self.logger.info(json.dumps({
            "event": "inference",
            "timestamp": datetime.utcnow().isoformat(),
            "prompt_tokens": prompt_length,
            "response_tokens": response_length,
            "inference_ms": inference_time_ms,
            "memory_mb": memory_mb,
            "model": model
        }))

# src/reddwarf/monitoring/metrics.py
import torch
from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
    inference_time_ms: float
    vram_mb: float
    ram_mb: float
    tokens_per_second: float

    @staticmethod
    def capture() -> "PerformanceMetrics":
        if torch.cuda.is_available():
            vram = torch.cuda.memory_allocated() / 1024**2
        else:
            vram = 0.0
        # RAM measurement via psutil if needed
        return PerformanceMetrics(...)
```

**References**:
- Python logging: https://docs.python.org/3/library/logging.html
- PyTorch memory management: https://pytorch.org/docs/stable/notes/cuda.html

---

## 9. Code Quality Tools Configuration

### Decision: Black + isort + mypy + ruff

**Rationale**:
- **black**: Opinionated formatter, zero-config, 100-char line length (readable for modern screens)
- **isort**: Import sorting compatible with black profile
- **mypy**: Strict type checking as discussed in section 2
- **ruff**: Fast linter replacing flake8/pylint, catches bugs black doesn't format

**Alternatives Considered**:
- **yapf/autopep8**: Rejected - black more consistent, less configuration
- **pylint**: Rejected - ruff faster and sufficient for this codebase
- **flake8**: Rejected - ruff is drop-in replacement with better performance

**Implementation**:
```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py310']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
strict = true
warn_unused_ignores = true
disallow_any_unimported = true
exclude = ["tests/fixtures/"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]
target-version = "py310"
```

**Pre-commit Hooks**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-requests]
```

**References**:
- black: https://black.readthedocs.io/
- ruff: https://docs.astral.sh/ruff/

---

## 10. Makefile Helpers Design

### Decision: Make Targets for Common Workflows

**Rationale**:
- **Makefile**: Universal, familiar to developers, no additional dependencies
- **Common commands**: `make test`, `make lint`, `make run`, `make docker-build`
- **Help target**: `make help` lists all commands with descriptions
- **Phony targets**: All targets are `.PHONY` (no file outputs)

**Implementation**:
```makefile
# makefile
.PHONY: help test lint format run docker-build docker-run download-models clean

help:  ## Show this help message
	@echo "Red Dwarf Tiny LLM - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

test:  ## Run tests with coverage
	pytest --cov=src/reddwarf --cov-report=html --cov-report=term tests/

lint:  ## Run linters (mypy, ruff)
	mypy src/ tests/
	ruff check src/ tests/

format:  ## Format code (black, isort)
	black src/ tests/
	isort src/ tests/

run:  ## Run FastAPI server locally
	uvicorn reddwarf.api.main:app --reload

docker-build:  ## Build Docker image
	docker build -f docker/Dockerfile -t reddwarf-llm:latest .

docker-run:  ## Run Docker container
	docker-compose -f docker/docker-compose.yml up

download-models:  ## Download models from HuggingFace
	python scripts/download-models.sh

clean:  ## Clean cache and build artifacts
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/ dist/ build/
```

**References**:
- GNU Make: https://www.gnu.org/software/make/manual/

---

## Research Complete

All "NEEDS CLARIFICATION" items from Technical Context have been resolved. Key decisions documented:

1. ✅ Model selection: TinyLlama-1.1B + Phi-2 with 4-bit/8-bit quantization
2. ✅ Type hints: Strict mypy with Pydantic for runtime validation
3. ✅ API framework: FastAPI with layered architecture for MCP compatibility
4. ✅ Testing: pytest with Red Dwarf themed fixtures, 80% coverage target
5. ✅ Devcontainer: Python 3.10+ base image with GPU passthrough (Linux)
6. ✅ Docker: Multi-stage builds, volume-mounted models
7. ✅ Quotes database: JSON format with session-based no-repeat selection
8. ✅ Monitoring: stdlib logging with structured JSON logs
9. ✅ Code quality: black + isort + mypy + ruff with pre-commit hooks
10. ✅ Makefile: Common commands for test/lint/run/docker workflows

**Next Phase**: Phase 1 - Design & Contracts (data-model.md, contracts/, quickstart.md)
