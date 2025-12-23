"""Unit tests for quote selector."""

import pytest

from reddwarf.quotes.database import Quote, QuoteDatabase, Session
from reddwarf.quotes.selector import QuoteSelector


def test_quote_selector_no_repeat(test_quotes: list[Quote]) -> None:
    """Test that quote selector doesn't repeat quotes within session."""
    db = QuoteDatabase(quotes=test_quotes)
    selector = QuoteSelector(db)
    session = Session()

    # Select all quotes
    selected_ids = []
    for _ in range(len(test_quotes)):
        quote = selector.get_random_quote(session)
        selected_ids.append(quote.id)

    # All should be unique
    assert len(selected_ids) == len(set(selected_ids))
    assert len(session.used_quote_ids) == len(test_quotes)


def test_quote_selector_reset_after_exhaustion(test_quotes: list[Quote]) -> None:
    """Test that selector resets after all quotes used."""
    db = QuoteDatabase(quotes=test_quotes)
    selector = QuoteSelector(db)
    session = Session()

    # Exhaust all quotes
    for _ in range(len(test_quotes)):
        selector.get_random_quote(session)

    # Next quote should reset session
    next_quote = selector.get_random_quote(session)
    assert len(session.used_quote_ids) == 1
    assert next_quote.id in session.used_quote_ids


def test_quote_pair_selection(test_quotes: list[Quote]) -> None:
    """Test getting two different quotes for opening/closing."""
    db = QuoteDatabase(quotes=test_quotes)
    selector = QuoteSelector(db)
    session = Session()

    opening, closing = selector.get_quote_pair(session)

    # Should be different quotes
    assert opening.id != closing.id

    # Both should be marked as used
    assert opening.id in session.used_quote_ids
    assert closing.id in session.used_quote_ids


def test_quote_selector_empty_database() -> None:
    """Test selector with empty database."""
    db = QuoteDatabase(quotes=[])
    selector = QuoteSelector(db)
    session = Session()

    with pytest.raises(ValueError, match="Quote database is empty"):
        selector.get_random_quote(session)


def test_quote_pair_insufficient_quotes() -> None:
    """Test quote pair selection with only one quote."""
    db = QuoteDatabase(quotes=[Quote(id=1, text="Only quote", character="Test", episode="Test", season=1)])
    selector = QuoteSelector(db)
    session = Session()

    with pytest.raises(ValueError, match="at least 2 quotes"):
        selector.get_quote_pair(session)
