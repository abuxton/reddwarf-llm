#!/usr/bin/env python3
"""Extract Red Dwarf quotes from subtitle files.

This script parses .srt subtitle files from the reddwarfsubs repository
and extracts memorable quotes with character attribution.

Usage:
    python scripts/extract_quotes.py --subs-dir /path/to/reddwarfsubs --output src/reddwarf/quotes/quotes.json
"""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Quote:
    """Extracted quote with metadata."""

    text: str
    character: str
    episode: str
    season: int


def parse_srt_file(filepath: Path) -> list[tuple[str, str]]:
    """Parse SRT file and extract dialogue lines.

    Args:
        filepath: Path to .srt file

    Returns:
        List of (dialogue_text, raw_context) tuples
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # SRT format: number, timestamp, text, blank line
    # Extract text blocks
    blocks = re.split(r"\n\n+", content)
    dialogues = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        # Skip number and timestamp, get text
        text_lines = lines[2:]
        text = " ".join(text_lines).strip()

        # Remove timing codes like (00:01:03)
        text = re.sub(r"\(\d{2}:\d{2}:\d{2}\)", "", text)
        # Remove sound effects like (DRAMATIC MUSIC)
        text = re.sub(r"\([A-Z\s,\-\"\']+\)", "", text)
        # Clean up
        text = re.sub(r"\s+", " ", text).strip()

        if text and not text.startswith("#"):  # Skip songs
            dialogues.append((text, block))

    return dialogues


def extract_character_from_line(line: str) -> tuple[str | None, str]:
    """Extract character name and clean dialogue.

    Args:
        line: Dialogue line potentially with character name

    Returns:
        (character_name, clean_dialogue) tuple
    """
    # Pattern: "CHARACTER: dialogue" or "CHARACTER, dialogue" or "- CHARACTER: dialogue"
    patterns = [
        r"^-?\s*([A-Z][A-Z\s]+):\s*(.+)$",  # "LISTER: text"
        r"^-?\s*([A-Z][A-Z\s]+),\s+(.+)$",  # "LISTER, text"
    ]

    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            character = match.group(1).strip().title()
            dialogue = match.group(2).strip()
            return character, dialogue

    return None, line


def is_memorable_quote(text: str) -> bool:
    """Check if quote is memorable/significant enough to include.

    Args:
        text: Quote text

    Returns:
        True if quote should be included
    """
    # Too short
    if len(text) < 10:
        return False

    # Too long
    if len(text) > 200:
        return False

    # Contains key Red Dwarf phrases
    key_phrases = [
        "smeg",
        "dead dave",
        "kipper",
        "curry",
        "vindaloo",
        "hologram",
        "android",
        "starbug",
        "gazpacho",
        "jupiter mining",
        "everyone's dead",
        "everybody's dead",
        "mining ship",
        "red dwarf",
        "iq",
        "silicon heaven",
        "better than life",
    ]

    text_lower = text.lower()
    if any(phrase in text_lower for phrase in key_phrases):
        return True

    # Contains exclamation or question (more memorable)
    if "!" in text or "?" in text:
        return True

    # Longer quotes are generally more substantial
    if len(text) > 50:
        return True

    return False


def extract_quotes_from_directory(subs_dir: Path) -> list[Quote]:
    """Extract quotes from all subtitle files in directory.

    Args:
        subs_dir: Root directory containing season subdirectories

    Returns:
        List of extracted Quote objects
    """
    quotes: list[Quote] = []
    quote_id = 1

    # Find all season directories
    season_dirs = sorted([d for d in subs_dir.iterdir() if d.is_dir()])

    for season_dir in season_dirs:
        # Extract season number from directory name (e.g., "01 - Series I" -> 1)
        season_match = re.match(r"(\d+)\s*-", season_dir.name)
        if not season_match:
            continue

        season_num = int(season_match.group(1))

        # Find all .srt files
        srt_files = sorted(season_dir.glob("*.srt"))

        for srt_file in srt_files:
            # Extract episode name from filename
            episode_name = srt_file.stem
            # Remove episode number prefix (e.g., "01-01 The End" -> "The End")
            episode_name = re.sub(r"^\d+-\d+\s+", "", episode_name)

            dialogues = parse_srt_file(srt_file)

            for text, _ in dialogues:
                character, clean_text = extract_character_from_line(text)

                if not character:
                    # Try to infer from common patterns
                    if "lister" in text.lower()[:20]:
                        character = "Lister"
                    elif "rimmer" in text.lower()[:20]:
                        character = "Rimmer"
                    elif "holly" in text.lower()[:20]:
                        character = "Holly"
                    elif "cat" in text.lower()[:20]:
                        character = "Cat"
                    elif "kryten" in text.lower()[:20]:
                        character = "Kryten"
                    else:
                        character = "Unknown"

                if is_memorable_quote(clean_text):
                    quotes.append(
                        Quote(
                            text=clean_text,
                            character=character,
                            episode=episode_name,
                            season=season_num,
                        )
                    )

    return quotes


def manual_curated_quotes() -> list[dict[str, Any]]:
    """Return manually curated iconic Red Dwarf quotes.

    These are guaranteed classics that should always be included.
    """
    return [
        {
            "id": 1,
            "text": "Everybody's dead, Dave.",
            "character": "Holly",
            "episode": "The End",
            "season": 1,
        },
        {
            "id": 2,
            "text": "I'm going to eat you little fishie!",
            "character": "Cat",
            "episode": "Confidence and Paranoia",
            "season": 1,
        },
        {
            "id": 3,
            "text": "Smoke me a kipper, I'll be back for breakfast!",
            "character": "Ace Rimmer",
            "episode": "Dimension Jump",
            "season": 4,
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
            "text": "Smegging hell!",
            "character": "Lister",
            "episode": "Various",
            "season": 1,
        },
        {
            "id": 6,
            "text": "I'm not a god! I'm not a god!",
            "character": "Lister",
            "episode": "Waiting for God",
            "season": 1,
        },
        {
            "id": 7,
            "text": "So what is it? It's a small, off-duty Czechoslovakian traffic warden!",
            "character": "Rimmer",
            "episode": "Queeg",
            "season": 2,
        },
        {
            "id": 8,
            "text": "Gazpacho soup! I wanted it hot!",
            "character": "Rimmer",
            "episode": "Timeslides",
            "season": 3,
        },
        {
            "id": 9,
            "text": "I'm a fish!",
            "character": "Lister",
            "episode": "Backwards",
            "season": 3,
        },
        {
            "id": 10,
            "text": "Silicon heaven? Where would all the calculators go?",
            "character": "Lister",
            "episode": "The Last Day",
            "season": 3,
        },
    ]


def main() -> None:
    """Main execution."""
    parser = argparse.ArgumentParser(description="Extract Red Dwarf quotes from subtitles")
    parser.add_argument(
        "--subs-dir",
        type=Path,
        default="/Users/abuxton/src/github/forks/reddwarfsubs",
        help="Path to reddwarfsubs directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default="src/reddwarf/quotes/quotes.json",
        help="Output JSON file path",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of quotes to extract (in addition to curated)",
    )

    args = parser.parse_args()

    if not args.subs_dir.exists():
        print(f"❌ Subtitles directory not found: {args.subs_dir}")
        return

    print(f"🚀 Extracting quotes from {args.subs_dir}")
    print(f"   Output: {args.output}")

    # Start with curated quotes
    curated = manual_curated_quotes()
    print(f"✅ Loaded {len(curated)} manually curated quotes")

    # Extract additional quotes
    print("🔍 Parsing subtitle files...")
    extracted = extract_quotes_from_directory(args.subs_dir)
    print(f"✅ Extracted {len(extracted)} potential quotes")

    # Combine and deduplicate by text
    all_quotes = curated.copy()
    seen_texts = {q["text"].lower() for q in curated}
    next_id = len(curated) + 1

    for quote in extracted:
        if quote.text.lower() not in seen_texts and len(all_quotes) < args.limit + len(curated):
            all_quotes.append(
                {
                    "id": next_id,
                    "text": quote.text,
                    "character": quote.character,
                    "episode": quote.episode,
                    "season": quote.season,
                }
            )
            seen_texts.add(quote.text.lower())
            next_id += 1

    print(f"📝 Total quotes: {len(all_quotes)}")

    # Write to output file
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(all_quotes, f, indent=2, ensure_ascii=False)

    print(f"✅ Quotes saved to {args.output}")
    print(f"🎉 Smeg! That's done!")


if __name__ == "__main__":
    main()
