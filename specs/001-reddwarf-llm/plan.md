# Implementation Plan: Red Dwarf Tiny LLM Implementation

**Branch**: `001-reddwarf-llm` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-reddwarf-llm/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Python-based tiny LLM implementation supporting TinyLlama-1.1B and Phi-2 models with 4-bit/8-bit quantization for consumer hardware (<8GB VRAM). All inference responses are bookended with Red Dwarf quotes. Foundation architecture for future Holly persona agent and MCP server integration. Development via devcontainer, deployment via Docker, comprehensive test suite with Red Dwarf-themed data, strict type hints, and entertainment-first approach.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: PyTorch, Transformers (HuggingFace), FastAPI, Pydantic, bitsandbytes
**Storage**: Local file system (model weights from HuggingFace Hub, JSON/YAML for quotes database)
**Testing**: pytest, pytest-cov, pytest-asyncio, mypy for type checking
**Target Platform**: Linux/macOS with CUDA/Metal GPU support, Docker containers, VS Code devcontainers
**Project Type**: Single project (Python package with CLI, library, and future API)
**Performance Goals**: <2s inference for 512-token prompts, <30s model loading, <8GB VRAM usage
**Constraints**: Consumer hardware friendly, offline-capable after initial model download, no external API dependencies
**Scale/Scope**: Single-user interactive chat, ~10 core modules, 50+ Red Dwarf quotes, 80% test coverage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Tiny & Maintainable ✅
- **Clear module separation**: model loading (`src/model/`), inference (`src/inference/`), response formatting (`src/formatting/`), quotes database (`src/quotes/`), FastAPI endpoints (`src/api/`)
- **Type hints**: All public functions and classes will have full PEP 484 type annotations
- **Single responsibility**: Each module has one purpose (e.g., `model_loader.py` only handles model initialization)
- **Composition over inheritance**: Prefer dependency injection for model/formatter/quote providers
- **Documentation**: Humorous docstrings that remain clear (e.g., "Load a tiny brain - I mean, model")

**Risk**: ⚠️ PyTorch/Transformers dependencies are large, but unavoidable for LLM inference

### II. Test Coverage & Quality ✅
- **80% coverage target**: Critical paths (model loading, inference, quote selection, API endpoints)
- **Red Dwarf test data**: Test prompts like "Calculate hyperdrive trajectory to Earth", expected responses with character-appropriate quotes
- **Unit tests**: `tests/unit/` for each module in isolation (mocked dependencies)
- **Integration tests**: `tests/integration/` for end-to-end inference with actual models
- **Contract tests**: `tests/contract/` for API endpoint behavior
- **CI enforcement**: Tests block merges, coverage reports generated

### III. User Experience Consistency ✅
- **Holly authenticity**: Quotes database curated from Red Dwarf scripts, verified for character accuracy
- **No repetition**: Session-based tracking ensures varied quotes within 20 consecutive requests (per SC-009)
- **Clear error messages**: Humorous but helpful (e.g., "Gordon Bennett! Model file missing. Run `make download-models` to fix.")
- **API documentation**: OpenAPI/Swagger with examples showing request/response format
- **Progressive enhancement**: Basic inference works excellently before adding Holly persona layer

### IV. Performance Requirements ✅
- **<2s inference target**: Achieved via 4-bit/8-bit quantization (bitsandbytes), small models (TinyLlama 1.1B, Phi-2 2.7B)
- **<8GB VRAM**: Quantization and model selection enforce this constraint
- **<30s model loading**: Lazy loading where possible, quantization reduces weight size
- **Monitoring**: Performance metrics logged (inference time, memory usage, token throughput)
- **Benchmarks**: `tests/performance/` tracks regression via automated benchmarks

**Risk**: ⚠️ Metal (macOS) quantization support less mature than CUDA - may need fallbacks

### V. Entertainment First ✅
- **Fun-first design**: Red Dwarf quotes as core feature, not afterthought
- **Humorous comments**: Code comments reference show episodes where appropriate
- **Non-commercial**: Fan content under DBAD license, respects Red Dwarf IP
- **Documentation style**: README and guides entertaining to read while remaining useful
- **Community-friendly**: Contribution guidelines welcoming, code reviews constructive

**Assessment**: All core principles satisfied. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
reddwarf-llm/
├── src/
│   ├── reddwarf/
│   │   ├── __init__.py
│   │   ├── model/
│   │   │   ├── __init__.py
│   │   │   ├── loader.py          # Model loading with quantization
│   │   │   ├── config.py          # ModelConfig dataclass
│   │   │   └── registry.py        # Supported models registry (TinyLlama, Phi-2)
│   │   ├── inference/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py          # Core inference logic
│   │   │   ├── request.py         # InferenceRequest dataclass
│   │   │   └── response.py        # InferenceResponse dataclass
│   │   ├── formatting/
│   │   │   ├── __init__.py
│   │   │   ├── response_formatter.py  # Bookend responses with quotes
│   │   │   └── holly_persona.py   # Future: Holly personality layer (stub)
│   │   ├── quotes/
│   │   │   ├── __init__.py
│   │   │   ├── database.py        # Quote collection management
│   │   │   ├── selector.py        # Random selection with no-repeat logic
│   │   │   └── quotes.json        # Red Dwarf quotes database
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py            # FastAPI app initialization
│   │   │   ├── endpoints.py       # Inference HTTP endpoints
│   │   │   └── models.py          # API request/response models
│   │   ├── monitoring/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py          # Performance logging
│   │   │   └── metrics.py         # Memory/timing metrics collection
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   └── main.py            # CLI interface (future)
│   │   └── config/
│   │       ├── __init__.py
│   │       ├── settings.py        # Application configuration
│   │       └── defaults.yaml      # Default configuration values
│   └── py.typed                   # PEP 561 marker for type checking
├── tests/
│   ├── unit/
│   │   ├── test_loader.py
│   │   ├── test_engine.py
│   │   ├── test_response_formatter.py
│   │   ├── test_quote_selector.py
│   │   └── test_api_endpoints.py
│   ├── integration/
│   │   ├── test_end_to_end_inference.py
│   │   └── test_model_loading.py
│   ├── contract/
│   │   └── test_api_contracts.py
│   ├── performance/
│   │   ├── test_inference_speed.py
│   │   └── test_memory_usage.py
│   ├── fixtures/
│   │   ├── test_quotes.json       # Red Dwarf themed test data
│   │   └── test_prompts.py        # Character-appropriate test scenarios
│   └── conftest.py                # Pytest configuration and shared fixtures
├── docs/
│   ├── setup-devcontainer.md
│   ├── setup-docker.md
│   ├── api-reference.md
│   ├── holly-personality-guidelines.md  # Future: Character consistency guide
│   └── performance-tuning.md
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile.dev
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/
│   ├── download-models.sh         # Fetch models from HuggingFace
│   ├── benchmark.py               # Performance benchmarking
│   └── validate-quotes.py         # Verify quote database integrity
├── data/                          # Model cache directory (gitignored)
├── makefile                       # Common commands (test, run, docker-build, etc.)
├── pyproject.toml                 # Python packaging + dependencies
├── setup.py                       # Legacy setup for editable installs
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Development dependencies
├── .python-version                # Python 3.10+
├── mypy.ini                       # Type checking configuration
├── .flake8 or pyproject.toml      # Linting configuration (black, isort)
├── pytest.ini or pyproject.toml   # Test configuration
├── LICENSE                        # DBAD license
└── README.md                      # Project overview with humor
```

**Structure Decision**: Single project (Option 1) selected. This is a focused Python library/application with API endpoints, not a distributed web app. All code lives under `src/reddwarf/` as a proper Python package, enabling both `import reddwarf` usage and CLI/API execution. Clear module boundaries support clean architecture: model management, inference engine, response formatting, and API layer are completely separate. Tests mirror source structure for easy navigation. Docker and devcontainer configs at root for discoverability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Large dependencies (PyTorch, Transformers) | Essential for LLM inference - no alternatives exist for model loading/execution | Custom implementation would require years of work and violate "Tiny & Maintainable" |
| Metal/CUDA quantization complexity | Required to meet <8GB VRAM constraint on consumer hardware | Without quantization, models require 16-32GB VRAM, making project inaccessible to target audience |

**Justification**: Both complexities are externalized (dependencies) and unavoidable for the core requirement. Our code remains tiny; we leverage battle-tested libraries for heavy lifting.

---

## Phase Completion Status

### ✅ Phase 0: Research (Complete)
- **Deliverable**: `research.md`
- **Content**: All "NEEDS CLARIFICATION" items resolved with technology decisions, best practices, and implementation patterns
- **Key Decisions**:
  - Model selection: TinyLlama-1.1B + Phi-2 with bitsandbytes quantization
  - Type system: Strict mypy with Pydantic for API validation
  - FastAPI with layered architecture for MCP compatibility
  - pytest with Red Dwarf themed fixtures
  - Devcontainer + Docker deployment strategies
  - JSON quotes database with session-based selection

### ✅ Phase 1: Design & Contracts (Complete)
- **Deliverable 1**: `data-model.md` - Core entities defined
  - ModelConfig, InferenceRequest, InferenceResponse, Quote, QuoteDatabase, Session, PerformanceMetrics
  - Full type specifications, validation rules, relationships, state transitions
  - Testing strategy and serialization formats documented

- **Deliverable 2**: `contracts/` - API contracts defined
  - `openapi.yaml`: Complete OpenAPI 3.0 specification with 7 endpoints
  - `/health`, `/infer`, `/models`, `/models/current`, `/quotes`, `/quotes/stats`
  - Request/response schemas, error handling, examples

- **Deliverable 3**: `quickstart.md` - User onboarding documentation
  - Three setup paths: devcontainer, Docker, local Python
  - Configuration examples, common commands, troubleshooting
  - API usage examples and performance tuning tips

- **Deliverable 4**: Agent context updated
  - `.github/agents/copilot-instructions.md` created/updated with Python 3.10+, PyTorch, FastAPI technologies

### 🔄 Phase 2: Task Breakdown (NOT STARTED - per instructions)
- **Next Command**: `/speckit.tasks` (separate execution, not part of `/speckit.plan`)
- **Output**: `tasks.md` breaking implementation into actionable tickets
- **Scope**: Code generation tasks, test implementation, Docker/devcontainer setup, documentation

---

## Constitution Check - Post Phase 1 Re-evaluation

*Re-checking all principles after design phase completion*

### I. Tiny & Maintainable ✅
- **Architecture**: Clean separation verified in `data-model.md` and `contracts/openapi.yaml`
- **Module count**: ~10 core modules as planned (model, inference, formatting, quotes, api, monitoring, config)
- **Type safety**: All entities designed with full type hints (Pydantic + dataclasses)
- **No feature creep**: Scope limited to MVP inference + quotes, Holly persona/MCP server deferred

**Status**: PASS - Design maintains tiny, focused codebase

### II. Test Coverage & Quality ✅
- **Coverage**: 80% target documented in `data-model.md` with unit/integration/contract test split
- **Red Dwarf data**: Test fixtures defined (Lister curry scenarios, Rimmer bureaucracy scenarios)
- **Test structure**: Mirrors source structure (`tests/unit/`, `tests/integration/`, `tests/contract/`)

**Status**: PASS - Test strategy comprehensive and achievable

### III. User Experience Consistency ✅
- **Holly authenticity**: Quote database design ensures character attribution per episode/season
- **No repetition**: Session entity tracks used quote IDs with reset logic (20+ consecutive unique)
- **Error messages**: Documented in `contracts/README.md` with humorous but helpful examples
- **API docs**: OpenAPI spec provides interactive Swagger UI at `/docs` endpoint

**Status**: PASS - UX consistency preserved in design

### IV. Performance Requirements ✅
- **<2s inference**: Research confirms 4-bit quantization achieves target with TinyLlama/Phi-2
- **<8GB VRAM**: ModelConfig enforces `max_memory_mb` constraint
- **Monitoring**: PerformanceMetrics entity captures inference_time_ms, vram_mb, tokens_per_second
- **Benchmarks**: Documented in `quickstart.md` with performance tuning tips

**Status**: PASS - Performance targets achievable with chosen architecture

### V. Entertainment First ✅
- **Fun-first**: Entire API responses bookended with Red Dwarf quotes (core feature, not addon)
- **Humor in docs**: `quickstart.md` includes Red Dwarf references while remaining useful
- **API descriptions**: OpenAPI spec includes character humor ("Smeg off", "Holly's IQ")
- **Non-commercial**: Documented as fan content respecting Red Dwarf IP

**Status**: PASS - Entertainment value integrated throughout

**Final Assessment**: ✅ ALL CONSTITUTION PRINCIPLES SATISFIED POST-DESIGN

No violations introduced in Phase 1. Architecture, testing, UX, performance, and entertainment goals all maintained in detailed design. Ready for Phase 2 task breakdown (separate command).

---

## Next Steps

The implementation plan is complete. To proceed:

1. **Generate tasks**: Run `/speckit.tasks` to break implementation into actionable tickets
2. **Assign work**: Distribute tasks across contributors or sprints
3. **Implement**: Follow `research.md` technology decisions and `data-model.md` entity specifications
4. **Test**: Maintain 80% coverage per test strategy in `data-model.md`
5. **Document**: Use `quickstart.md` as template for README and user guides

**Branch**: `001-reddwarf-llm` (already created)
**Artifacts Location**: `/specs/001-reddwarf-llm/`
**Status**: ✅ PLAN COMPLETE - Ready for task generation
