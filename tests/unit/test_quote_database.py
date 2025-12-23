"""Unit tests for quote database."""

import json
import pytest
from pathlib import Path

from reddwarf.quotes.database import Quote, QuoteDatabase, Session


def test_quote_creation() -> None:
    """Test creating a Quote object."""
    quote = Quote(
        id=1,
        text="Test quote",
        character="Lister",
        episode="Test Episode",
        season=1
    )

    assert quote.id == 1
    assert quote.text == "Test quote"
    assert quote.character == "Lister"


def test_quote_to_dict() -> None:
    """Test Quote serialization."""
    quote = Quote(id=1, text="Test", character="Lister", episode="Ep", season=1)
    data = quote.to_dict()

    assert data["id"] == 1
    assert data["text"] == "Test"


def test_quote_from_dict() -> None:
    """Test Quote deserialization."""
    data = {
        "id": 1,
        "text": "Test",
        "character": "Lister",
        "episode": "Ep",
        "season": 1
    }
    quote = Quote.from_dict(data)

    assert quote.id == 1
    assert quote.text == "Test"


def test_quote_database_from_json(tmp_path: Path) -> None:
    """Test loading quote database from JSON."""
    quotes_data = [
        {"id": 1, "text": "Quote 1", "character": "Lister", "episode": "Ep1", "season": 1},
        {"id": 2, "text": "Quote 2", "character": "Rimmer", "episode": "Ep2", "season": 2},
    ]

    quotes_file = tmp_path / "quotes.json"
    with open(quotes_file, "w") as f:
        json.dump(quotes_data, f)

    db = QuoteDatabase.from_json(quotes_file)
    assert db.total_count == 2


def test_quote_database_get_by_id(test_quotes: list[Quote]) -> None:
    """Test getting quote by ID."""
    db = QuoteDatabase(quotes=test_quotes)

    quote = db.get_by_id(1)
    assert quote is not None
    assert quote.id == 1

    missing = db.get_by_id(999)
    assert missing is None


def test_quote_database_get_by_character(test_quotes: list[Quote]) -> None:
    """Test filtering quotes by character."""
    db = QuoteDatabase(quotes=test_quotes)

    lister_quotes = db.get_by_character("Lister")
    assert len(lister_quotes) == 1
    assert all(q.character == "Lister" for q in lister_quotes)


def test_quote_database_validate_success(test_quotes: list[Quote]) -> None:
    """Test validation of valid database."""
    db = QuoteDatabase(quotes=test_quotes)
    errors = db.validate()
    assert len(errors) == 0


def test_quote_database_validate_too_few() -> None:
    """Test validation fails with too few quotes."""
    db = QuoteDatabase(quotes=[
        Quote(id=1, text="Only quote", character="Test", episode="Test", season=1)
    ])
    errors = db.validate()
    assert len(errors) > 0
    assert any("at least 10 quotes" in err for err in errors)


def test_quote_database_validate_duplicate_ids() -> None:
    """Test validation fails with duplicate IDs."""
    quotes = [
        Quote(id=1, text="Quote 1", character="Test", episode="Test", season=1),
        Quote(id=1, text="Quote 2", character="Test", episode="Test", season=1),
    ] + [Quote(id=i, text=f"Quote {i}", character="Test", episode="Test", season=1) for i in range(2, 11)]

    db = QuoteDatabase(quotes=quotes)
    errors = db.validate()
    assert any("Duplicate quote IDs" in err for err in errors)


def test_session_creation() -> None:
    """Test creating a Session."""
    session = Session()
    assert len(session.used_quote_ids) == 0
    assert session.session_id is not None


def test_session_mark_quote_used() -> None:
    """Test marking quotes as used."""
    session = Session()
    session.mark_quote_used(1)
    session.mark_quote_used(2)

    assert 1 in session.used_quote_ids
    assert 2 in session.used_quote_ids
    assert len(session.used_quote_ids) == 2


def test_session_reset_if_exhausted() -> None:
    """Test session reset when all quotes exhausted."""
    session = Session()
    session.mark_quote_used(1)
    session.mark_quote_used(2)
    session.mark_quote_used(3)

    session.reset_if_exhausted(total_quotes=3)
    assert len(session.used_quote_ids) == 0


def test_session_not_reset_if_not_exhausted() -> None:
    """Test session doesn't reset prematurely."""
    session = Session()
    session.mark_quote_used(1)

    session.reset_if_exhausted(total_quotes=5)
    assert len(session.used_quote_ids) == 1
