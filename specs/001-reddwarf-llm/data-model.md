# Phase 1: Data Model

**Feature**: Red Dwarf Tiny LLM Implementation
**Date**: 2025-12-22
**Status**: Complete

## Overview

This document defines the core entities, relationships, and data structures for the Red Dwarf LLM system. All entities are designed as Python dataclasses or Pydantic models with full type hints, supporting clean serialization, validation, and testing.

---

## Core Entities

### 1. ModelConfig

Represents configuration for loading and running a language model.

**Fields**:
- `model_id: str` - HuggingFace model identifier (e.g., "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
- `quantization: Literal["none", "4bit", "8bit"]` - Quantization level for memory optimization
- `device: Literal["cuda", "mps", "cpu"]` - Target compute device
- `max_memory_mb: int | None` - Maximum memory allocation (None = no limit)
- `torch_dtype: str` - Data type for model weights (e.g., "float16", "bfloat16")
- `trust_remote_code: bool` - Allow execution of remote code from model repo (default: False)

**Validation Rules**:
- `model_id` must not be empty
- `quantization` incompatible with `device="cpu"` (requires GPU)
- `max_memory_mb` must be > 0 if specified
- `torch_dtype` must be valid PyTorch dtype string

**State Transitions**:
- Created → Validated → Used for model loading
- Immutable after creation (frozen dataclass)

**Example**:
```python
config = ModelConfig(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    quantization="4bit",
    device="cuda",
    max_memory_mb=8000,
    torch_dtype="float16",
    trust_remote_code=False
)
```

---

### 2. InferenceRequest

Represents a user's request for text generation.

**Fields**:
- `prompt: str` - Input text to generate from (1-2048 chars)
- `max_tokens: int` - Maximum tokens to generate (default: 512, range: 1-2048)
- `temperature: float` - Sampling temperature (default: 0.7, range: 0.0-2.0)
- `top_p: float | None` - Nucleus sampling parameter (range: 0.0-1.0)
- `top_k: int | None` - Top-k sampling parameter (range: 1-100)
- `do_sample: bool` - Enable sampling vs greedy decoding (default: True)
- `session_id: str | None` - Session identifier for quote tracking (optional)
- `timestamp: datetime` - Request creation time (auto-generated)

**Validation Rules**:
- `prompt` length: 1-2048 characters
- `max_tokens`: 1-2048
- `temperature`: 0.0-2.0 (0.0 = deterministic, higher = more random)
- `top_p`: 0.0-1.0 if specified
- `top_k`: 1-100 if specified
- `session_id`: UUID format if specified

**Relationships**:
- References `session_id` → Session (for quote tracking)
- Produces one InferenceResponse

**Example**:
```python
request = InferenceRequest(
    prompt="Calculate the route back to Earth from deep space",
    max_tokens=256,
    temperature=0.8,
    session_id="550e8400-e29b-41d4-a716-446655440000"
)
```

---

### 3. InferenceResponse

Represents the generated response from the model, bookended with Red Dwarf quotes.

**Fields**:
- `request_id: str` - Unique identifier for this response (UUID)
- `opening_quote: Quote` - Red Dwarf quote prepended to response
- `generated_text: str` - Raw model output (before formatting)
- `closing_quote: Quote` - Red Dwarf quote appended to response
- `formatted_response: str` - Final text with quotes bookended
- `model_id: str` - Model used for generation
- `inference_time_ms: float` - Generation duration in milliseconds
- `tokens_generated: int` - Number of tokens in generated text
- `tokens_per_second: float` - Generation throughput
- `finish_reason: Literal["length", "eos_token", "stop_sequence"]` - Why generation stopped
- `timestamp: datetime` - Response creation time (auto-generated)

**Validation Rules**:
- `request_id` must be valid UUID
- `inference_time_ms` > 0
- `tokens_generated` > 0
- `tokens_per_second` > 0
- `formatted_response` must contain both quotes and generated text

**Relationships**:
- Consumes one InferenceRequest (not stored, request_id for correlation)
- Includes two Quote entities (opening, closing)
- References `model_id` from ModelConfig

**Derived Fields**:
- `formatted_response = f"{opening_quote.text}\n\n{generated_text}\n\n{closing_quote.text}"`

**Example**:
```python
response = InferenceResponse(
    request_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    opening_quote=Quote(id=1, text="Everybody's dead, Dave.", character="Holly"),
    generated_text="The navigation computer indicates we are 3 million years from Earth...",
    closing_quote=Quote(id=42, text="Smoke me a kipper!", character="Ace Rimmer"),
    formatted_response="<full formatted text>",
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    inference_time_ms=1250.5,
    tokens_generated=78,
    tokens_per_second=62.4,
    finish_reason="eos_token"
)
```

---

### 4. Quote

Represents a single quote from Red Dwarf series.

**Fields**:
- `id: int` - Unique identifier for quote
- `text: str` - Quote text (1-500 chars)
- `character: str` - Character who said it (Holly, Lister, Rimmer, Cat, Kryten, etc.)
- `episode: str` - Episode name
- `season: int` - Season number (1-12)

**Validation Rules**:
- `id` must be unique within database
- `text` length: 1-500 characters
- `character` must be non-empty
- `season`: 1-12 (valid Red Dwarf seasons)

**Relationships**:
- Many quotes belong to one QuoteDatabase
- Two quotes used per InferenceResponse (opening, closing)

**Example**:
```python
quote = Quote(
    id=7,
    text="I'm going to eat you little fishie!",
    character="Cat",
    episode="Confidence and Paranoia",
    season=1
)
```

---

### 5. QuoteDatabase

Collection of Red Dwarf quotes with management functionality.

**Fields**:
- `quotes: list[Quote]` - All available quotes
- `total_count: int` - Number of quotes in database (derived from len(quotes))

**Methods**:
- `from_json(path: str) -> QuoteDatabase` - Load quotes from JSON file
- `get_by_id(quote_id: int) -> Quote | None` - Retrieve specific quote
- `get_by_character(character: str) -> list[Quote]` - Filter by character
- `validate() -> list[str]` - Check for duplicates, invalid data (returns error list)

**Validation Rules**:
- All quote IDs must be unique
- Must contain at least 10 quotes (reasonable minimum for variety)
- Character names must be consistent (case-sensitive)

**Example**:
```python
db = QuoteDatabase.from_json("src/reddwarf/quotes/quotes.json")
assert db.total_count >= 50
assert len(db.validate()) == 0  # No errors
```

---

### 6. Session

Tracks quote usage within a user session to prevent repetition.

**Fields**:
- `session_id: str` - Unique session identifier (UUID)
- `used_quote_ids: set[int]` - IDs of quotes already used in this session
- `created_at: datetime` - Session start time
- `last_activity: datetime` - Most recent inference request time

**Methods**:
- `mark_quote_used(quote_id: int) -> None` - Add quote ID to used set
- `reset_if_exhausted(total_quotes: int) -> None` - Clear used set if all quotes consumed
- `is_expired(timeout_minutes: int = 60) -> bool` - Check if session should be cleaned up

**Validation Rules**:
- `session_id` must be valid UUID
- `used_quote_ids` cannot exceed total available quotes
- `last_activity >= created_at`

**State Transitions**:
- Created → Active (quote selections) → Exhausted (all quotes used) → Reset → Active
- Or: Created → Active → Expired (cleanup)

**Example**:
```python
session = Session(session_id="550e8400-e29b-41d4-a716-446655440000")
session.mark_quote_used(1)
session.mark_quote_used(42)
assert len(session.used_quote_ids) == 2
```

---

### 7. PerformanceMetrics

Captures resource usage and timing for monitoring.

**Fields**:
- `timestamp: datetime` - Measurement time
- `inference_time_ms: float` - Generation duration
- `vram_mb: float` - GPU memory usage (0 if CPU)
- `ram_mb: float` - System RAM usage
- `tokens_per_second: float` - Throughput metric
- `model_id: str` - Model being measured
- `quantization: str` - Quantization level used

**Methods**:
- `capture(model_id: str, quantization: str) -> PerformanceMetrics` - Static method to measure current state
- `to_log_dict() -> dict[str, Any]` - Convert to structured log format

**Validation Rules**:
- All numeric fields must be >= 0
- `inference_time_ms` > 0 for valid measurements

**Example**:
```python
metrics = PerformanceMetrics.capture(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    quantization="4bit"
)
logger.info(metrics.to_log_dict())
```

---

## Entity Relationships

```
ModelConfig (1) ──> LoadedModel (1)
                         │
                         │ uses
                         ▼
InferenceRequest (1) ──> InferenceEngine ──> InferenceResponse (1)
        │                     │
        │ references          │ selects
        ▼                     ▼
    Session (1)          QuoteDatabase (1)
        │                     │
        │ tracks usage        │ contains
        ▼                     ▼
    used_quote_ids       Quote (many)

InferenceResponse includes:
  - opening_quote: Quote
  - closing_quote: Quote

PerformanceMetrics captured per InferenceResponse
```

---

## Data Persistence

### Files
- **quotes.json**: Quote database (src/reddwarf/quotes/quotes.json)
- **config.yaml**: Application settings (optional, defaults in code)
- **models/**: Cached model weights (data/models/, gitignored)

### In-Memory
- **Session**: Active sessions stored in dict (session_id → Session)
- **LoadedModel**: Single loaded model instance (singleton pattern)
- **PerformanceMetrics**: Logged to stdout/file, not persisted in database

### No Database
- SQLite/PostgreSQL not needed - all data is either configuration files or runtime state
- Model weights managed by HuggingFace Transformers cache
- Quote database is read-only after load

---

## Serialization Formats

### JSON
- Quote database (`quotes.json`)
- API request/response payloads
- Structured logs (`PerformanceMetrics.to_log_dict()`)

### YAML (optional)
- Configuration file (`config.yaml`)
- Environment-specific overrides

### Python Pickle (HuggingFace internal)
- Model weights (managed by Transformers library, not our concern)

---

## Validation Strategy

### At Creation (Pydantic)
```python
from pydantic import BaseModel, Field, validator

class InferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2048)
    max_tokens: int = Field(512, ge=1, le=2048)
    temperature: float = Field(0.7, ge=0.0, le=2.0)

    @validator("prompt")
    def prompt_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be whitespace only")
        return v
```

### At Runtime (Business Logic)
```python
def validate_model_config(config: ModelConfig) -> list[str]:
    errors = []
    if config.quantization != "none" and config.device == "cpu":
        errors.append("Quantization requires GPU (cuda or mps)")
    if config.max_memory_mb and config.max_memory_mb < 500:
        errors.append("max_memory_mb too low for any model")
    return errors
```

### At Load (Quote Database)
```python
def validate_quote_database(db: QuoteDatabase) -> list[str]:
    errors = []
    ids = [q.id for q in db.quotes]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate quote IDs found")
    if db.total_count < 10:
        errors.append("Quote database must have at least 10 quotes")
    return errors
```

---

## Type Hierarchy

```python
# Domain models (business logic)
@dataclass(frozen=True)
class ModelConfig: ...

@dataclass(frozen=True)
class Quote: ...

# Mutable runtime state
@dataclass
class Session: ...

@dataclass
class PerformanceMetrics: ...

# API models (Pydantic for validation + JSON serialization)
class InferenceRequestAPI(BaseModel):
    prompt: str
    max_tokens: int = 512
    ...

    def to_domain(self) -> InferenceRequest:
        """Convert API model to domain model"""
        return InferenceRequest(...)

class InferenceResponseAPI(BaseModel):
    request_id: str
    formatted_response: str
    ...

    @classmethod
    def from_domain(cls, response: InferenceResponse) -> "InferenceResponseAPI":
        """Convert domain model to API model"""
        return cls(...)
```

**Separation Rationale**:
- Domain models: Business logic, frozen/immutable where possible
- API models: Pydantic validation, JSON serialization, HTTP concerns
- Conversion methods: Translate between layers, maintain clean boundaries

---

## Testing Strategy

### Unit Tests (Mocked Dependencies)
```python
def test_quote_selector_no_repeat():
    db = QuoteDatabase(quotes=[Quote(id=i, ...) for i in range(5)])
    selector = QuoteSelector(db)
    session = Session(session_id="test-123")

    quotes = [selector.get_random_quote(session) for _ in range(5)]
    assert len(set(q.id for q in quotes)) == 5  # All unique

    # After exhausting all quotes, should reset
    sixth_quote = selector.get_random_quote(session)
    assert sixth_quote.id in [0, 1, 2, 3, 4]
    assert len(session.used_quote_ids) == 1  # Reset happened
```

### Integration Tests (Real Data)
```python
def test_end_to_end_inference_with_quotes():
    config = ModelConfig(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", ...)
    engine = InferenceEngine(config=config)
    request = InferenceRequest(prompt="What's the route to Earth?")

    response = engine.generate(request)

    assert response.opening_quote is not None
    assert response.closing_quote is not None
    assert response.opening_quote.id != response.closing_quote.id
    assert response.inference_time_ms < 2000  # < 2s target
    assert "Earth" in response.generated_text or "route" in response.generated_text
```

### Contract Tests (API Validation)
```python
def test_api_request_validation():
    # Valid request
    valid = InferenceRequestAPI(prompt="Test prompt")
    assert valid.max_tokens == 512  # Default

    # Invalid: prompt too long
    with pytest.raises(ValidationError):
        InferenceRequestAPI(prompt="x" * 2049)

    # Invalid: temperature out of range
    with pytest.raises(ValidationError):
        InferenceRequestAPI(prompt="Test", temperature=3.0)
```

---

## Phase 1 Data Model Complete

All entities defined with:
- ✅ Field specifications and types
- ✅ Validation rules
- ✅ State transitions where applicable
- ✅ Relationships between entities
- ✅ Serialization formats
- ✅ Testing strategy

**Next**: Generate API contracts (OpenAPI specification)
