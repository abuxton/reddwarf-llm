# Tasks: Red Dwarf Tiny LLM Implementation

**Input**: Design documents from `/specs/001-reddwarf-llm/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Feature**: Tiny LLM with Red Dwarf quote bookending, devcontainer support, Docker deployment

**Tests**: Test tasks are included as this is a serious implementation requiring comprehensive test coverage per the constitution (80%+ target).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create root project directories: src/reddwarf/, tests/unit/, tests/integration/, tests/contract/, tests/performance/, tests/fixtures/, docs/, scripts/, data/, docker/, .devcontainer/
- [ ] T002 Initialize Python project with pyproject.toml including dependencies: torch, transformers, fastapi, pydantic, bitsandbytes, pytest, pytest-cov, pytest-asyncio, mypy, black, isort, ruff, uvicorn
- [ ] T003 [P] Create setup.py for editable installs with pip install -e '.[dev]'
- [ ] T004 [P] Create requirements.txt from pyproject.toml for production dependencies
- [ ] T005 [P] Create requirements-dev.txt for development dependencies (testing, linting, formatting)
- [ ] T006 [P] Configure mypy.ini with strict=true, warn_unused_ignores=true, disallow_any_unimported=true
- [ ] T007 [P] Configure black/isort/ruff in pyproject.toml with line-length=100, target Python 3.10+
- [ ] T008 [P] Configure pytest in pyproject.toml with coverage settings and async support
- [ ] T009 [P] Create .python-version file specifying Python 3.10+
- [ ] T010 [P] Create LICENSE file with DBAD license text
- [ ] T011 [P] Create .gitignore with Python, PyTorch, model cache, and IDE entries
- [ ] T012 [P] Create src/reddwarf/__init__.py with package metadata and version
- [ ] T013 [P] Create src/py.typed marker file for PEP 561 type checking support
- [ ] T014 Create makefile with targets: help, test, lint, format, run, docker-build, docker-run, download-models, clean

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Configuration & Settings

- [ ] T015 [P] Create src/reddwarf/config/__init__.py with package exports
- [ ] T016 [P] Create src/reddwarf/config/defaults.yaml with default model settings, API config, inference parameters
- [ ] T017 [P] Create src/reddwarf/config/settings.py with Settings dataclass using Pydantic for validation, environment variable overrides

### Quote Database Foundation

- [ ] T018 [P] Create src/reddwarf/quotes/__init__.py with package exports
- [ ] T019 [P] Create Quote dataclass in src/reddwarf/quotes/database.py with fields: id, text, character, episode, season
- [ ] T020 [P] Create QuoteDatabase class in src/reddwarf/quotes/database.py with methods: from_json, get_by_id, get_by_character, validate
- [ ] T021 Create scripts/extract_quotes.py to parse subtitle files from /Users/abuxton/src/github/forks/reddwarfsubs and extract quotes with character attribution, episode/season metadata
- [ ] T022 Run quote extraction script and manually review/curate extracted quotes for accuracy
- [ ] T023 Create src/reddwarf/quotes/quotes.json with curated Red Dwarf quotes (target: 50+ quotes minimum)
- [ ] T024 Create scripts/validate-quotes.py to check quote database for duplicates, schema violations, character consistency
- [ ] T025 [P] Create Session dataclass in src/reddwarf/quotes/database.py for tracking used quote IDs per session
- [ ] T026 [P] Create QuoteSelector class in src/reddwarf/quotes/selector.py with get_random_quote method implementing no-repeat logic

### Model Management Foundation

- [ ] T027 [P] Create src/reddwarf/model/__init__.py with package exports
- [ ] T028 [P] Create ModelConfig dataclass in src/reddwarf/model/config.py with validation for quantization, device, memory limits
- [ ] T029 [P] Create model registry in src/reddwarf/model/registry.py mapping model names to HuggingFace IDs (TinyLlama, Phi-2)
- [ ] T030 Create scripts/download-models.sh to fetch TinyLlama-1.1B and Phi-2 from HuggingFace Hub to data/models/

### Monitoring & Logging Foundation

- [ ] T031 [P] Create src/reddwarf/monitoring/__init__.py with package exports
- [ ] T032 [P] Create PerformanceMetrics dataclass in src/reddwarf/monitoring/metrics.py with capture method for VRAM/RAM/timing
- [ ] T033 [P] Create StructuredLogger class in src/reddwarf/monitoring/logger.py with log_inference method outputting JSON format

### Test Infrastructure

- [ ] T034 [P] Create tests/conftest.py with pytest fixtures: mock_model, red_dwarf_quotes, test_config
- [ ] T035 [P] Create tests/fixtures/test_quotes.json with 10+ curated test quotes
- [ ] T036 [P] Create tests/fixtures/test_prompts.py with character-appropriate test scenarios (Lister, Rimmer, Cat)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Local Model Inference (Priority: P1) 🎯 MVP

**Goal**: Load a tiny LLM model on consumer hardware (<8GB VRAM) and generate text responses bookended with Red Dwarf quotes

**Independent Test**: Load TinyLlama-1.1B with 4-bit quantization, send prompt "What is the route to Earth?", receive response with opening/closing quotes, verify VRAM < 8GB and inference < 2s

### Tests for User Story 1 (TDD Approach)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T037 [P] [US1] Contract test for /infer endpoint in tests/contract/test_inference_api.py verifying request/response schemas
- [ ] T038 [P] [US1] Contract test for /health endpoint in tests/contract/test_health_api.py verifying model status reporting
- [ ] T039 [P] [US1] Integration test for end-to-end inference in tests/integration/test_end_to_end_inference.py with real model loading
- [ ] T040 [P] [US1] Performance test for inference speed in tests/performance/test_inference_speed.py verifying <2s target
- [ ] T041 [P] [US1] Performance test for memory usage in tests/performance/test_memory_usage.py verifying <8GB VRAM

### Implementation for User Story 1

#### Model Loading

- [ ] T042 [P] [US1] Create ModelLoader class in src/reddwarf/model/loader.py with load method supporting quantization (4-bit, 8-bit, none)
- [ ] T043 [P] [US1] Implement device detection (CUDA, MPS, CPU) in src/reddwarf/model/loader.py
- [ ] T044 [US1] Implement bitsandbytes quantization integration in src/reddwarf/model/loader.py with fallback for Metal
- [ ] T045 [US1] Add model caching logic to avoid re-downloads in src/reddwarf/model/loader.py using HuggingFace cache
- [ ] T046 [P] [US1] Unit test for ModelLoader in tests/unit/test_loader.py with mocked torch models

#### Inference Engine

- [ ] T047 [P] [US1] Create InferenceRequest dataclass in src/reddwarf/inference/request.py with Pydantic validation
- [ ] T048 [P] [US1] Create InferenceResponse dataclass in src/reddwarf/inference/response.py with formatted output fields
- [ ] T049 [US1] Create InferenceEngine class in src/reddwarf/inference/engine.py with generate method
- [ ] T050 [US1] Implement tokenization and generation logic in src/reddwarf/inference/engine.py using Transformers library
- [ ] T051 [US1] Add timeout handling and error recovery in src/reddwarf/inference/engine.py
- [ ] T052 [US1] Integrate PerformanceMetrics capturing in src/reddwarf/inference/engine.py
- [ ] T053 [P] [US1] Unit test for InferenceEngine in tests/unit/test_engine.py with mocked model

#### Response Formatting with Quotes

- [ ] T054 [P] [US1] Create src/reddwarf/formatting/__init__.py with package exports
- [ ] T055 [US1] Create ResponseFormatter class in src/reddwarf/formatting/response_formatter.py integrating QuoteSelector
- [ ] T056 [US1] Implement bookend logic ensuring opening_quote != closing_quote in src/reddwarf/formatting/response_formatter.py
- [ ] T057 [US1] Add formatted_response construction in src/reddwarf/formatting/response_formatter.py
- [ ] T058 [P] [US1] Unit test for ResponseFormatter in tests/unit/test_response_formatter.py

#### API Endpoints

- [ ] T059 [P] [US1] Create src/reddwarf/api/__init__.py with package exports
- [ ] T060 [P] [US1] Create InferenceRequestAPI Pydantic model in src/reddwarf/api/models.py
- [ ] T061 [P] [US1] Create InferenceResponseAPI Pydantic model in src/reddwarf/api/models.py with from_domain method
- [ ] T062 [US1] Create FastAPI app in src/reddwarf/api/main.py with CORS, OpenAPI metadata
- [ ] T063 [US1] Implement /health endpoint in src/reddwarf/api/endpoints.py returning model status
- [ ] T064 [US1] Implement /infer endpoint in src/reddwarf/api/endpoints.py with dependency injection for InferenceEngine
- [ ] T065 [US1] Add error handling middleware in src/reddwarf/api/endpoints.py for graceful failures
- [ ] T066 [P] [US1] Unit test for API endpoints in tests/unit/test_api_endpoints.py with mocked services

#### Quote Selection Tests

- [ ] T067 [P] [US1] Unit test for QuoteSelector in tests/unit/test_quote_selector.py verifying no-repeat logic within session
- [ ] T068 [P] [US1] Unit test for Session in tests/unit/test_quote_selector.py verifying reset after exhaustion

#### Integration & Validation

- [ ] T069 [US1] Run all tests for User Story 1 and verify they pass
- [ ] T070 [US1] Manually test inference with curl against /infer endpoint
- [ ] T071 [US1] Verify quotes rotate without repetition in consecutive requests
- [ ] T072 [US1] Verify inference timing meets <2s target for 512-token prompts
- [ ] T073 [US1] Verify VRAM usage stays <8GB with 4-bit quantization

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Core inference working!

---

## Phase 4: User Story 2 - Development Environment Setup (Priority: P2)

**Goal**: Provide standardized devcontainer with all dependencies pre-configured for contributors

**Independent Test**: Open project in VS Code, rebuild devcontainer, run make test, verify all tests pass and type checking/formatting tools work

### Tests for User Story 2

- [ ] T074 [P] [US2] Integration test in tests/integration/test_devcontainer.py verifying all tools available (mypy, black, pytest)
- [ ] T075 [P] [US2] Integration test verifying GPU passthrough works in devcontainer (Linux only, skip on macOS)

### Implementation for User Story 2

#### Devcontainer Configuration

- [ ] T076 [P] [US2] Create .devcontainer/devcontainer.json using mcr.microsoft.com/devcontainers/python:3.10 base image
- [ ] T077 [P] [US2] Add NVIDIA CUDA feature in .devcontainer/devcontainer.json for GPU support
- [ ] T078 [P] [US2] Add Docker-in-Docker feature in .devcontainer/devcontainer.json
- [ ] T079 [P] [US2] Configure HuggingFace cache mount in .devcontainer/devcontainer.json to avoid re-downloads
- [ ] T080 [P] [US2] Set postCreateCommand to "pip install -e '.[dev]'" in .devcontainer/devcontainer.json
- [ ] T081 [P] [US2] Add VS Code extensions in .devcontainer/devcontainer.json: Python, Pylance, Ruff

#### Pre-commit Hooks

- [ ] T082 [P] [US2] Create .pre-commit-config.yaml with black, isort, ruff, mypy hooks
- [ ] T083 [US2] Add pre-commit installation to devcontainer postCreateCommand

#### Documentation

- [ ] T084 [P] [US2] Create docs/setup-devcontainer.md with step-by-step devcontainer setup instructions
- [ ] T085 [P] [US2] Document GPU passthrough requirements for Linux in docs/setup-devcontainer.md
- [ ] T086 [P] [US2] Document macOS Metal limitations (no container GPU) in docs/setup-devcontainer.md with CPU fallback instructions

#### Validation

- [ ] T087 [US2] Build devcontainer locally and verify all dependencies install
- [ ] T088 [US2] Run make test inside devcontainer and verify 80%+ coverage
- [ ] T089 [US2] Run make lint inside devcontainer and verify no errors
- [ ] T090 [US2] Run make format inside devcontainer and verify code formatting works

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Contributors can develop locally!

---

## Phase 5: User Story 3 - Docker Deployment (Priority: P3)

**Goal**: Containerized service deployable on any Docker-compatible system with identical behavior to local development

**Independent Test**: Build Docker image, run container with GPU passthrough, make inference requests via curl, verify identical performance to local setup

### Tests for User Story 3

- [ ] T091 [P] [US3] Integration test in tests/integration/test_docker_deployment.py building and running container
- [ ] T092 [P] [US3] Integration test verifying API accessible on port 8000 in container

### Implementation for User Story 3

#### Docker Configuration

- [ ] T093 [P] [US3] Create docker/Dockerfile with multi-stage build (builder + runtime stages)
- [ ] T094 [P] [US3] Optimize Docker image by copying only necessary files in docker/Dockerfile
- [ ] T095 [P] [US3] Set TRANSFORMERS_CACHE environment variable in docker/Dockerfile
- [ ] T096 [P] [US3] Create docker/docker-compose.yml with service definition, port mapping, volume mounts
- [ ] T097 [P] [US3] Configure GPU reservation in docker/docker-compose.yml for NVIDIA GPUs
- [ ] T098 [P] [US3] Add model cache volume mount in docker/docker-compose.yml to data/models/

#### Docker Helper Scripts

- [ ] T099 [P] [US3] Add docker-build target to makefile running docker build command
- [ ] T100 [P] [US3] Add docker-run target to makefile running docker-compose up

#### Documentation

- [ ] T101 [P] [US3] Create docs/setup-docker.md with Docker setup instructions
- [ ] T102 [P] [US3] Document GPU passthrough setup for Linux (nvidia-container-toolkit) in docs/setup-docker.md
- [ ] T103 [P] [US3] Document macOS limitations (no GPU in containers) in docs/setup-docker.md
- [ ] T104 [P] [US3] Add troubleshooting section to docs/setup-docker.md for common Docker issues

#### Validation

- [ ] T105 [US3] Build Docker image locally with make docker-build
- [ ] T106 [US3] Run Docker container with make docker-run
- [ ] T107 [US3] Test /health endpoint from host machine
- [ ] T108 [US3] Test /infer endpoint from host machine and verify quotes bookend
- [ ] T109 [US3] Verify container can be stopped and restarted without data loss

**Checkpoint**: All core user stories (1-3) should now be independently functional. MVP ready for deployment!

---

## Phase 6: User Story 4 - Model Selection and Configuration (Priority: P4)

**Goal**: Enable users to select from multiple models and configure quantization to balance quality vs resources

**Independent Test**: Switch between TinyLlama and Phi-2, change quantization levels, measure memory/speed differences, verify outputs valid

### Tests for User Story 4

- [ ] T110 [P] [US4] Integration test in tests/integration/test_model_switching.py verifying model changes without restart
- [ ] T111 [P] [US4] Performance test comparing TinyLlama vs Phi-2 speed/memory in tests/performance/test_model_comparison.py

### Implementation for User Story 4

#### Model Management Endpoints

- [ ] T112 [P] [US4] Implement /models GET endpoint in src/reddwarf/api/endpoints.py listing available models
- [ ] T113 [P] [US4] Implement /models/current GET endpoint in src/reddwarf/api/endpoints.py returning current model status
- [ ] T114 [P] [US4] Create ModelStatusAPI Pydantic model in src/reddwarf/api/models.py

#### Configuration Management

- [ ] T115 [US4] Add model switching logic to InferenceEngine in src/reddwarf/inference/engine.py
- [ ] T116 [US4] Add environment variable overrides in src/reddwarf/config/settings.py for REDDWARF_MODEL_ID, REDDWARF_QUANTIZATION
- [ ] T117 [P] [US4] Unit test for configuration overrides in tests/unit/test_settings.py

#### Documentation

- [ ] T118 [P] [US4] Document model selection in README.md with performance characteristics
- [ ] T119 [P] [US4] Create docs/performance-tuning.md with guidelines for model/quantization selection
- [ ] T120 [P] [US4] Add model comparison table to docs/performance-tuning.md (memory, speed, quality trade-offs)

#### Validation

- [ ] T121 [US4] Test switching from TinyLlama to Phi-2 via environment variables
- [ ] T122 [US4] Test 4-bit vs 8-bit quantization and measure VRAM differences
- [ ] T123 [US4] Verify /models and /models/current endpoints return accurate information

**Checkpoint**: Users can now customize model behavior based on their hardware!

---

## Phase 7: User Story 5 - Foundation for Holly Agent Integration (Priority: P5)

**Goal**: Clean separation between inference and persona logic, enabling future Holly personality characteristics

**Independent Test**: Review code architecture, verify persona can be toggled without affecting inference, demonstrate clear module boundaries

### Tests for User Story 5

- [ ] T124 [P] [US5] Unit test in tests/unit/test_holly_persona.py verifying persona stub exists and is independently testable

### Implementation for User Story 5

#### Persona Foundation

- [ ] T125 [P] [US5] Create src/reddwarf/formatting/holly_persona.py with HollyPersona stub class
- [ ] T126 [P] [US5] Define PersonaConfig dataclass in src/reddwarf/formatting/holly_persona.py for future traits (IQ jokes, computer-speak)
- [ ] T127 [US5] Add optional persona parameter to ResponseFormatter in src/reddwarf/formatting/response_formatter.py
- [ ] T128 [US5] Implement persona toggle logic ensuring inference works with/without persona

#### Documentation for Future Development

- [ ] T129 [P] [US5] Create docs/holly-personality-guidelines.md documenting Holly character traits from Red Dwarf
- [ ] T130 [P] [US5] Document persona extension points in docs/holly-personality-guidelines.md
- [ ] T131 [P] [US5] Add examples of Holly-style responses in docs/holly-personality-guidelines.md

#### Validation

- [ ] T132 [US5] Verify inference works identically with persona disabled
- [ ] T133 [US5] Run all existing tests with persona stub enabled (should pass)

**Checkpoint**: Architecture ready for Holly personality layer in future phase!

---

## Phase 8: User Story 6 - MCP Server Foundation (Priority: P6)

**Goal**: API designed for MCP protocol wrapping with structured inputs/outputs and clear extension points

**Independent Test**: Review API design, verify endpoints follow RESTful patterns, confirm interfaces suitable for MCP wrapping

### Tests for User Story 6

- [ ] T134 [P] [US6] Contract test in tests/contract/test_mcp_readiness.py verifying API structure compatible with MCP protocol

### Implementation for User Story 6

#### API Structuring for MCP

- [ ] T135 [P] [US6] Add context parameter to InferenceRequestAPI in src/reddwarf/api/models.py for future conversation history
- [ ] T136 [P] [US6] Create ContextAPI Pydantic model in src/reddwarf/api/models.py (stub for MCP context management)
- [ ] T137 [P] [US6] Document MCP integration strategy in docs/api-reference.md

#### Validation

- [ ] T138 [US6] Review API endpoints and verify they accept/return structured data
- [ ] T139 [US6] Verify InferenceRequest/Response can be wrapped in MCP protocol format

**Checkpoint**: API ready for future MCP server implementation!

---

## Phase 9: Additional Endpoints & Quote Management (Priority: P4-P5)

**Goal**: Complete the API with quote browsing and statistics

**Independent Test**: Query /quotes endpoint, verify random quote returned; query /quotes/stats, verify accurate counts

### Tests for Additional Endpoints

- [ ] T140 [P] Contract test for /quotes endpoint in tests/contract/test_quotes_api.py
- [ ] T141 [P] Contract test for /quotes/stats endpoint in tests/contract/test_quotes_api.py

### Implementation

- [ ] T142 [P] Implement /quotes GET endpoint in src/reddwarf/api/endpoints.py returning random quote
- [ ] T143 [P] Implement /quotes/stats GET endpoint in src/reddwarf/api/endpoints.py returning database statistics
- [ ] T144 [P] Create QuoteAPI Pydantic model in src/reddwarf/api/models.py
- [ ] T145 [P] Create QuoteStatsAPI Pydantic model in src/reddwarf/api/models.py

### Validation

- [ ] T146 Test /quotes endpoint returns valid quote with all fields
- [ ] T147 Test /quotes/stats returns accurate counts

**Checkpoint**: API complete with all endpoints from contracts/openapi.yaml!

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, documentation, and final hardening

### Documentation

- [ ] T148 [P] Create comprehensive README.md at repository root with project overview, setup instructions, usage examples
- [ ] T149 [P] Add Red Dwarf humor to README.md while maintaining technical clarity
- [ ] T150 [P] Document all API endpoints in docs/api-reference.md with examples
- [ ] T151 [P] Create CONTRIBUTING.md with contribution guidelines and code standards
- [ ] T152 [P] Add architecture diagram to docs/ showing module relationships

### Benchmarking & Performance

- [ ] T153 [P] Create scripts/benchmark.py measuring inference speed across models/quantization levels
- [ ] T154 Run benchmark and document results in docs/performance-tuning.md
- [ ] T155 Add benchmark results to README.md

### Code Quality & Refactoring

- [ ] T156 Run make lint on entire codebase and fix any warnings
- [ ] T157 Run make format on entire codebase for consistent style
- [ ] T158 Review all docstrings for completeness and humor
- [ ] T159 [P] Add type hints to any remaining untyped functions
- [ ] T160 Verify mypy passes with --strict on all modules

### Testing & Coverage

- [ ] T161 Run make test and verify 80%+ coverage achieved
- [ ] T162 [P] Add additional unit tests for edge cases if coverage below target
- [ ] T163 [P] Add integration tests for error scenarios (model not loaded, timeout, CUDA OOM)
- [ ] T164 Create tests/fixtures/ with additional Red Dwarf themed test data

### Security & Hardening

- [ ] T165 Review error messages to ensure no sensitive data leakage
- [ ] T166 Add input validation for all API endpoints (already done via Pydantic, verify completeness)
- [ ] T167 Add rate limiting considerations to docs/api-reference.md for future multi-user deployments

### Quickstart Validation

- [ ] T168 Follow docs/setup-devcontainer.md step-by-step and verify accuracy
- [ ] T169 Follow docs/setup-docker.md step-by-step and verify accuracy
- [ ] T170 Update quickstart.md in specs/001-reddwarf-llm/ if any discrepancies found
- [ ] T171 Test all curl examples in quickstart.md and verify they work

### Final Integration Testing

- [ ] T172 Run full end-to-end test: start server, test all endpoints, verify quotes rotate, measure performance
- [ ] T173 Test graceful shutdown and restart
- [ ] T174 Test error recovery (kill model process, verify API returns appropriate errors)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - Core MVP
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) - Parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) AND US1 (needs working inference to containerize)
- **User Story 4 (Phase 6)**: Depends on US1 (extends inference with model selection)
- **User Story 5 (Phase 7)**: Depends on US1 (extends response formatting)
- **User Story 6 (Phase 8)**: Depends on US1 (extends API structure)
- **Additional Endpoints (Phase 9)**: Depends on Foundational (Phase 2) - Parallel with US1
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### Critical Path

```
Setup (Phase 1)
    ↓
Foundational (Phase 2) ← CRITICAL BLOCKER
    ↓
    ├─→ User Story 1 (Phase 3) ← MVP CORE
    │       ↓
    │       ├─→ User Story 3 (Phase 5)
    │       ├─→ User Story 4 (Phase 6)
    │       ├─→ User Story 5 (Phase 7)
    │       └─→ User Story 6 (Phase 8)
    │
    ├─→ User Story 2 (Phase 4)
    └─→ Additional Endpoints (Phase 9)
    
    ↓ (after all user stories)
Polish (Phase 10)
```

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories ← **START HERE FOR MVP**
- **User Story 2 (P2)**: Can start after Foundational - Independent (devcontainer setup)
- **User Story 3 (P3)**: Requires US1 complete (Docker packages working inference)
- **User Story 4 (P4)**: Requires US1 complete (extends model management)
- **User Story 5 (P5)**: Requires US1 complete (extends response formatting)
- **User Story 6 (P6)**: Requires US1 complete (extends API structure)

### Within Each User Story

1. Tests (TDD) MUST be written and FAIL before implementation
2. Foundational components (dataclasses, configs) before logic
3. Core logic before API endpoints
4. Unit tests before integration tests
5. Story complete and validated before moving to next priority

### Parallel Opportunities

**Within Phase 1 (Setup)**: Tasks T003-T013 can all run in parallel (different files)

**Within Phase 2 (Foundational)**: 
- Configuration tasks (T015-T017) parallel
- Quote tasks (T018-T020, T024-T026) parallel
- Model tasks (T027-T029) parallel
- Monitoring tasks (T031-T033) parallel
- Test fixture tasks (T034-T036) parallel

**Within User Story 1**:
- All test tasks (T037-T041) parallel
- Model loading tasks (T042-T043) parallel with T046
- Request/Response dataclasses (T047-T048) parallel
- Unit test tasks (T046, T053, T058, T066-T068) parallel after their dependencies

**Across User Stories** (if team capacity allows):
- After Foundational complete: US1, US2, and Additional Endpoints (Phase 9) can start in parallel
- After US1 complete: US3, US4, US5, US6 can all proceed in parallel

---

## Parallel Example: Foundational Phase

```bash
# After Setup phase completes, launch all foundational components together:

# Configuration Team:
Task: "Create src/reddwarf/config/__init__.py"
Task: "Create src/reddwarf/config/defaults.yaml"
Task: "Create src/reddwarf/config/settings.py"

# Quote Database Team:
Task: "Create src/reddwarf/quotes/__init__.py"
Task: "Create Quote dataclass in src/reddwarf/quotes/database.py"
Task: "Create QuoteDatabase class in src/reddwarf/quotes/database.py"

# Model Team:
Task: "Create src/reddwarf/model/__init__.py"
Task: "Create ModelConfig dataclass in src/reddwarf/model/config.py"
Task: "Create model registry in src/reddwarf/model/registry.py"

# All can proceed simultaneously - no conflicts
```

---

## Parallel Example: User Story 1 - Testing

```bash
# Write all tests for User Story 1 together (TDD approach):

Task: "Contract test for /infer endpoint in tests/contract/test_inference_api.py"
Task: "Contract test for /health endpoint in tests/contract/test_health_api.py"
Task: "Integration test for end-to-end inference in tests/integration/test_end_to_end_inference.py"
Task: "Performance test for inference speed in tests/performance/test_inference_speed.py"
Task: "Performance test for memory usage in tests/performance/test_memory_usage.py"

# All tests will FAIL initially - this is expected and correct for TDD
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - Recommended Start

1. **Complete Phase 1: Setup** (Tasks T001-T014) - ~4 hours
2. **Complete Phase 2: Foundational** (Tasks T015-T036) - ~12 hours
   - CRITICAL: Quote extraction from reddwarfsubs (T021-T022) - ~2 hours
   - CRITICAL: Model download setup (T030) - ~1 hour
3. **Complete Phase 3: User Story 1** (Tasks T037-T073) - ~20 hours
   - Tests first (T037-T041) - ~4 hours
   - Model loading (T042-T046) - ~4 hours
   - Inference engine (T047-T053) - ~4 hours
   - Response formatting (T054-T058) - ~2 hours
   - API endpoints (T059-T066) - ~4 hours
   - Validation (T069-T073) - ~2 hours
4. **STOP and VALIDATE**: Test User Story 1 independently, demo inference with quotes
5. **Deploy/demo if ready** - Working MVP!

**Estimated Time: ~36 hours of focused development**

### Incremental Delivery (MVP + Devcontainer + Docker)

1. Complete Setup + Foundational → Foundation ready (~16 hours)
2. Add User Story 1 → Test independently → MVP working! (~20 hours)
3. Add User Story 2 → Devcontainer setup for contributors (~8 hours)
4. Add User Story 3 → Docker deployment ready (~8 hours)
5. Each story adds value without breaking previous stories

**Estimated Time: ~52 hours to production-ready deployment**

### Full Feature Set

1. Complete Phases 1-3 → MVP (~36 hours)
2. Add Phases 4-5 → Devcontainer + Docker (~16 hours)
3. Add Phases 6-8 → Model selection + Agent/MCP foundations (~12 hours)
4. Add Phase 9 → Additional API endpoints (~4 hours)
5. Add Phase 10 → Polish, documentation, benchmarks (~12 hours)

**Estimated Time: ~80 hours for complete feature implementation**

### Parallel Team Strategy (3 developers)

With multiple developers after Foundational phase:

1. **Team completes Setup + Foundational together** (~16 hours)
2. **Once Foundational done, split:**
   - Developer A: User Story 1 (Core inference) - ~20 hours
   - Developer B: User Story 2 (Devcontainer) - ~8 hours, then helps with US1 tests
   - Developer C: Additional Endpoints (Phase 9) - ~4 hours, then helps with US1 validation
3. **After US1 complete, parallel work:**
   - Developer A: User Story 4 (Model selection) - ~6 hours
   - Developer B: User Story 3 (Docker) - ~8 hours
   - Developer C: User Story 5+6 (Agent/MCP foundations) - ~8 hours
4. **Final sprint: Polish together** (~12 hours)

**Estimated Time: ~36 hours wall-clock time with 3 developers (vs 80 hours solo)**

---

## Task Count Summary

- **Phase 1 (Setup)**: 14 tasks
- **Phase 2 (Foundational)**: 22 tasks (CRITICAL PATH)
- **Phase 3 (User Story 1 - MVP)**: 37 tasks (CORE VALUE)
- **Phase 4 (User Story 2 - Devcontainer)**: 17 tasks
- **Phase 5 (User Story 3 - Docker)**: 19 tasks
- **Phase 6 (User Story 4 - Model Selection)**: 14 tasks
- **Phase 7 (User Story 5 - Holly Foundation)**: 10 tasks
- **Phase 8 (User Story 6 - MCP Foundation)**: 6 tasks
- **Phase 9 (Additional Endpoints)**: 8 tasks
- **Phase 10 (Polish)**: 27 tasks

**Total: 174 tasks**

**Parallelizable tasks: ~60 marked with [P]**

**MVP Scope (Phases 1-3): 73 tasks (~36 hours)**

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] labels**: Maps task to specific user story for traceability (US1-US6)
- **TDD approach**: All tests written before implementation (should FAIL initially)
- **Constitution compliance**: 80%+ test coverage, full type hints, Red Dwarf humor maintained
- **Quote extraction**: Critical task (T021) parses /Users/abuxton/src/github/forks/reddwarfsubs for subtitle data
- **MVP focus**: User Story 1 delivers immediate value - core inference with quotes
- **Independent stories**: Each story completable and testable on its own
- **Commit strategy**: Commit after each task or logical group for clean history
- **Checkpoints**: Stop at any checkpoint to validate story independently before proceeding

---

## Acceptance Criteria Checklist

Before marking this feature complete, verify:

- [ ] All 174 tasks completed (or explicitly deferred)
- [ ] Test coverage ≥80% across all modules
- [ ] mypy --strict passes with zero errors
- [ ] All API endpoints documented in OpenAPI spec
- [ ] Quote database contains 50+ curated Red Dwarf quotes from reddwarfsubs
- [ ] Inference speed <2s for 512-token prompts on target hardware
- [ ] VRAM usage <8GB with 4-bit quantization
- [ ] Model loading <30s
- [ ] No quote repetition within 20 consecutive requests per session
- [ ] Devcontainer builds and runs successfully
- [ ] Docker container builds and runs successfully
- [ ] All quickstart.md examples work as documented
- [ ] README.md complete with setup instructions and usage examples
- [ ] Holly persona foundation implemented (stub ready for future work)
- [ ] MCP server foundation implemented (API ready for future wrapping)

---

**Remember**: This is a community project for entertainment. Have fun, write clean code, and may your curry always be vindaloo! 🚀
