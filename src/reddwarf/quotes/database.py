"""Quote database models and management."""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Quote:
    """A single Red Dwarf quote."""

    id: int
    text: str
    character: str
    episode: str
    season: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "character": self.character,
            "episode": self.episode,
            "season": self.season,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quote":
        """Create Quote from dictionary."""
        return cls(
            id=data["id"],
            text=data["text"],
            character=data["character"],
            episode=data["episode"],
            season=data["season"],
        )


@dataclass
class QuoteDatabase:
    """Collection of Red Dwarf quotes."""

    quotes: list[Quote]

    @property
    def total_count(self) -> int:
        """Total number of quotes in database."""
        return len(self.quotes)

    @classmethod
    def from_json(cls, path: str | Path) -> "QuoteDatabase":
        """Load quotes from JSON file.

        Args:
            path: Path to quotes JSON file

        Returns:
            QuoteDatabase instance

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is invalid
            KeyError: If required fields are missing
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Quote database not found: {path}")

        with open(file_path) as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Quote database must be a JSON array")

        quotes = [Quote.from_dict(quote_data) for quote_data in data]
        return cls(quotes=quotes)

    def get_by_id(self, quote_id: int) -> Quote | None:
        """Get quote by ID.

        Args:
            quote_id: Quote ID to find

        Returns:
            Quote if found, None otherwise
        """
        for quote in self.quotes:
            if quote.id == quote_id:
                return quote
        return None

    def get_by_character(self, character: str) -> list[Quote]:
        """Get all quotes by character.

        Args:
            character: Character name (case-sensitive)

        Returns:
            List of quotes by that character
        """
        return [q for q in self.quotes if q.character == character]

    def validate(self) -> list[str]:
        """Validate quote database for errors.

        Returns:
            List of error messages (empty if valid)
        """
        errors: list[str] = []

        # Check minimum count
        if self.total_count < 10:
            errors.append(f"Quote database must have at least 10 quotes (found {self.total_count})")

        # Check for duplicate IDs
        ids = [q.id for q in self.quotes]
        if len(ids) != len(set(ids)):
            duplicates = [id_ for id_ in ids if ids.count(id_) > 1]
            errors.append(f"Duplicate quote IDs found: {set(duplicates)}")

        # Check for empty fields
        for i, quote in enumerate(self.quotes):
            if not quote.text.strip():
                errors.append(f"Quote {i} has empty text")
            if not quote.character.strip():
                errors.append(f"Quote {i} has empty character")
            if not quote.episode.strip():
                errors.append(f"Quote {i} has empty episode")
            if not (1 <= quote.season <= 12):
                errors.append(f"Quote {i} has invalid season: {quote.season}")

        # Check text length
        for quote in self.quotes:
            if len(quote.text) > 500:
                errors.append(
                    f"Quote {quote.id} text too long ({len(quote.text)} chars, max 500)"
                )

        return errors


@dataclass
class Session:
    """Tracks quote usage within a user session."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    used_quote_ids: set[int] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)

    def mark_quote_used(self, quote_id: int) -> None:
        """Mark quote as used in this session.

        Args:
            quote_id: ID of quote that was used
        """
        self.used_quote_ids.add(quote_id)
        self.last_activity = datetime.utcnow()

    def reset_if_exhausted(self, total_quotes: int) -> None:
        """Reset used quotes if all quotes have been consumed.

        Args:
            total_quotes: Total number of quotes available
        """
        if len(self.used_quote_ids) >= total_quotes:
            self.used_quote_ids.clear()

    def is_expired(self, timeout_minutes: int = 60) -> bool:
        """Check if session should be cleaned up.

        Args:
            timeout_minutes: Inactivity timeout in minutes

        Returns:
            True if session is expired
        """
        elapsed = (datetime.utcnow() - self.last_activity).total_seconds() / 60
        return elapsed >= timeout_minutes
