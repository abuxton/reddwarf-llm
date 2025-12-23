#!/usr/bin/env python3
"""Validate Red Dwarf quotes database for consistency and quality.

Usage:
    python scripts/validate-quotes.py [--path src/reddwarf/quotes/quotes.json]
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def validate_quotes(filepath: Path) -> tuple[bool, list[str]]:
    """Validate quote database.

    Args:
        filepath: Path to quotes JSON file

    Returns:
        (is_valid, errors) tuple
    """
    errors = []

    # Load file
    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        return False, [f"File not found: {filepath}"]
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    if not isinstance(data, list):
        return False, ["Root element must be an array"]

    # Check minimum count
    if len(data) < 10:
        errors.append(f"Too few quotes: {len(data)} (minimum 10)")

    # Validate each quote
    required_fields = ["id", "text", "character", "episode", "season"]
    ids = []
    texts = []

    for i, quote in enumerate(data):
        # Check required fields
        for field in required_fields:
            if field not in quote:
                errors.append(f"Quote {i}: missing field '{field}'")
                continue

        # Validate ID
        if not isinstance(quote["id"], int):
            errors.append(f"Quote {i}: id must be integer")
        else:
            ids.append(quote["id"])

        # Validate text
        text = quote["text"]
        if not isinstance(text, str):
            errors.append(f"Quote {i}: text must be string")
        elif not text.strip():
            errors.append(f"Quote {i}: text cannot be empty")
        elif len(text) > 500:
            errors.append(f"Quote {i}: text too long ({len(text)} chars, max 500)")
        else:
            texts.append(text.lower())

        # Validate character
        if not isinstance(quote["character"], str):
            errors.append(f"Quote {i}: character must be string")
        elif not quote["character"].strip():
            errors.append(f"Quote {i}: character cannot be empty")

        # Validate episode
        if not isinstance(quote["episode"], str):
            errors.append(f"Quote {i}: episode must be string")
        elif not quote["episode"].strip():
            errors.append(f"Quote {i}: episode cannot be empty")

        # Validate season
        season = quote["season"]
        if not isinstance(season, int):
            errors.append(f"Quote {i}: season must be integer")
        elif not (1 <= season <= 13):
            errors.append(f"Quote {i}: invalid season {season} (must be 1-13)")

    # Check for duplicate IDs
    id_counts = Counter(ids)
    duplicates = [id_ for id_, count in id_counts.items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate IDs found: {duplicates}")

    # Check for duplicate texts (case-insensitive)
    text_counts = Counter(texts)
    duplicate_texts = [text for text, count in text_counts.items() if count > 1]
    if duplicate_texts:
        errors.append(f"Duplicate quotes found: {len(duplicate_texts)} duplicates")
        for dup in duplicate_texts[:5]:  # Show first 5
            errors.append(f"  - '{dup[:50]}...'")

    # Check character consistency
    characters = Counter(q["character"] for q in data)
    print("\n📊 Character distribution:")
    for char, count in characters.most_common(10):
        print(f"  {char}: {count} quotes")

    return len(errors) == 0, errors


def main() -> None:
    """Main execution."""
    parser = argparse.ArgumentParser(description="Validate Red Dwarf quotes database")
    parser.add_argument(
        "--path",
        type=Path,
        default="src/reddwarf/quotes/quotes.json",
        help="Path to quotes JSON file",
    )

    args = parser.parse_args()

    print(f"🔍 Validating quotes database: {args.path}")

    is_valid, errors = validate_quotes(args.path)

    if is_valid:
        print("✅ Quote database is valid!")
        sys.exit(0)
    else:
        print(f"\n❌ Found {len(errors)} validation errors:\n")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
