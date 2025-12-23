"""Pytest configuration and shared fixtures for Red Dwarf LLM tests."""

import json
from pathlib import Path
from typing import Any, Generator

import pytest

from reddwarf.config.settings import Settings
from reddwarf.quotes.database import Quote, QuoteDatabase


@pytest.fixture
def test_quotes() -> list[Quote]:
    """Minimal set of test quotes."""
    return [
        Quote(id=1, text="Test quote 1", character="Lister", episode="Test", season=1),
        Quote(id=2, text="Test quote 2", character="Rimmer", episode="Test", season=1),
        Quote(id=3, text="Test quote 3", character="Holly", episode="Test", season=1),
        Quote(id=4, text="Test quote 4", character="Cat", episode="Test", season=1),
        Quote(id=5, text="Test quote 5", character="Kryten", episode="Test", season=1),
    ]


@pytest.fixture
def red_dwarf_quotes(tmp_path: Path) -> Generator[QuoteDatabase, None, None]:
    """Red Dwarf quotes database for testing.

    Uses actual test quotes file if available, otherwise creates minimal set.
    """
    # Try to load from fixtures directory
    fixtures_path = Path("tests/fixtures/test_quotes.json")
    if fixtures_path.exists():
        yield QuoteDatabase.from_json(fixtures_path)
    else:
        # Create temporary quotes file
        test_quotes_data = [
            {
                "id": 1,
                "text": "Everybody's dead, Dave.",
                "character": "Holly",
                "episode": "The End",
                "season": 1,
            },
            {
                "id": 2,
                "text": "Smoke me a kipper!",
                "character": "Ace Rimmer",
                "episode": "Dimension Jump",
                "season": 4,
            },
            {
                "id": 3,
                "text": "Smegging hell!",
                "character": "Lister",
                "episode": "Various",
                "season": 1,
            },
            {
                "id": 4,
                "text": "What a guy!",
                "character": "Various",
                "episode": "Dimension Jump",
                "season": 4,
            },
            {
                "id": 5,
                "text": "I'm going to eat you little fishie!",
                "character": "Cat",
                "episode": "Confidence and Paranoia",
                "season": 1,
            },
        ]

        temp_quotes_file = tmp_path / "test_quotes.json"
        with open(temp_quotes_file, "w") as f:
            json.dump(test_quotes_data, f)

        yield QuoteDatabase.from_json(temp_quotes_file)


@pytest.fixture
def test_config() -> Settings:
    """Test configuration with safe defaults."""
    return Settings(
        model={
            "model_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "quantization": "4bit",
            "device": "cpu",  # Safe for CI/testing
            "max_memory_mb": 8000,
            "torch_dtype": "float16",
            "trust_remote_code": False,
        },
        inference={
            "max_tokens": 128,  # Shorter for tests
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
            "do_sample": True,
            "timeout_seconds": 30,  # Longer for CI
        },
        api={"host": "127.0.0.1", "port": 8001, "log_level": "debug", "reload": False},
        cache={
            "transformers_cache": "./data/models",
            "quote_database_path": "tests/fixtures/test_quotes.json",
        },
        monitoring={
            "enable_metrics": True,
            "enable_structured_logs": False,  # Disable for cleaner test output
            "log_inference_details": False,
        },
    )


@pytest.fixture
def mock_model() -> Any:
    """Mock model for testing without loading real models.

    Returns a mock object that simulates model behavior.
    """

    class MockModel:
        """Mock language model for testing."""

        def __init__(self) -> None:
            self.device = "cpu"
            self.config = type("Config", (), {"model_type": "mock"})()

        def generate(
            self, input_ids: Any, max_new_tokens: int = 50, **kwargs: Any
        ) -> list[list[int]]:
            """Mock generate method."""
            # Return dummy token IDs
            return [[1, 2, 3, 4, 5] * (max_new_tokens // 5)]

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            """Mock forward pass."""
            return type("Output", (), {"logits": [[0.0] * 1000]})()

    return MockModel()


@pytest.fixture
def mock_tokenizer() -> Any:
    """Mock tokenizer for testing."""

    class MockTokenizer:
        """Mock tokenizer for testing."""

        def __init__(self) -> None:
            self.pad_token_id = 0
            self.eos_token_id = 1

        def encode(self, text: str, **kwargs: Any) -> list[int]:
            """Mock encode method."""
            return [1, 2, 3, 4, 5]

        def decode(self, token_ids: list[int], **kwargs: Any) -> str:
            """Mock decode method."""
            return "This is a mock generated response for testing purposes."

        def __call__(self, text: str | list[str], **kwargs: Any) -> Any:
            """Mock tokenization."""
            if isinstance(text, list):
                return type(
                    "BatchEncoding",
                    (),
                    {"input_ids": [[1, 2, 3, 4, 5] for _ in text], "attention_mask": None},
                )()
            return type("BatchEncoding", (), {"input_ids": [1, 2, 3, 4, 5], "attention_mask": None})(
                )

    return MockTokenizer()
