"""Quote selection with no-repeat logic."""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Quote, QuoteDatabase, Session


class QuoteSelector:
    """Selects random quotes with no-repeat logic within sessions."""

    def __init__(self, database: "QuoteDatabase") -> None:
        """Initialize selector with quote database.

        Args:
            database: QuoteDatabase instance
        """
        self._database = database

    def get_random_quote(self, session: "Session") -> "Quote":
        """Get a random quote not used in this session.

        If all quotes have been used, resets the session and starts over.

        Args:
            session: Session instance tracking used quotes

        Returns:
            Random Quote instance

        Raises:
            ValueError: If database is empty
        """
        if self._database.total_count == 0:
            raise ValueError("Quote database is empty")

        # Reset if exhausted
        session.reset_if_exhausted(self._database.total_count)

        # Filter available quotes
        available = [q for q in self._database.quotes if q.id not in session.used_quote_ids]

        # If somehow still empty (shouldn't happen), reset and try again
        if not available:
            session.used_quote_ids.clear()
            available = self._database.quotes

        # Select random quote
        quote = random.choice(available)
        session.mark_quote_used(quote.id)

        return quote

    def get_quote_pair(self, session: "Session") -> tuple["Quote", "Quote"]:
        """Get two different random quotes for opening/closing.

        Args:
            session: Session instance tracking used quotes

        Returns:
            Tuple of (opening_quote, closing_quote)

        Raises:
            ValueError: If database has fewer than 2 quotes
        """
        if self._database.total_count < 2:
            raise ValueError("Quote database must have at least 2 quotes for pair selection")

        opening_quote = self.get_random_quote(session)

        # Get closing quote that's different from opening
        # Temporarily mark opening as unavailable for second selection
        attempts = 0
        max_attempts = 10
        closing_quote = opening_quote

        while closing_quote.id == opening_quote.id and attempts < max_attempts:
            closing_quote = self.get_random_quote(session)
            attempts += 1

        # Fallback: if we somehow got the same quote, just pick any other quote
        if closing_quote.id == opening_quote.id:
            available = [q for q in self._database.quotes if q.id != opening_quote.id]
            if available:
                closing_quote = random.choice(available)
                session.mark_quote_used(closing_quote.id)

        return opening_quote, closing_quote
