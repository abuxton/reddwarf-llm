"""Test prompts and scenarios for Red Dwarf themed testing."""

from typing import TypedDict


class TestScenario(TypedDict):
    """Test scenario structure."""

    prompt: str
    expected_theme: str
    min_length: int


# Lister scenarios - curry, beer, and slacking off
LISTER_SCENARIOS: list[TestScenario] = [
    {
        "prompt": "What's for dinner?",
        "expected_theme": "curry",
        "min_length": 20,
    },
    {
        "prompt": "What's the best meal?",
        "expected_theme": "food",
        "min_length": 20,
    },
    {
        "prompt": "Tell me about Earth cuisine",
        "expected_theme": "food",
        "min_length": 30,
    },
]

# Rimmer scenarios - bureaucracy, incompetence, and neuroses
RIMMER_SCENARIOS: list[TestScenario] = [
    {
        "prompt": "List my achievements",
        "expected_theme": "achievement",
        "min_length": 20,
    },
    {
        "prompt": "How do I follow proper procedure?",
        "expected_theme": "procedure",
        "min_length": 30,
    },
    {
        "prompt": "What's the risk assessment?",
        "expected_theme": "risk",
        "min_length": 25,
    },
]

# Cat scenarios - vanity, grooming, and looking good
CAT_SCENARIOS: list[TestScenario] = [
    {
        "prompt": "How do I look?",
        "expected_theme": "appearance",
        "min_length": 15,
    },
    {
        "prompt": "What's the best outfit?",
        "expected_theme": "fashion",
        "min_length": 20,
    },
]

# Holly scenarios - computer problems and declining IQ
HOLLY_SCENARIOS: list[TestScenario] = [
    {
        "prompt": "What is the route to Earth?",
        "expected_theme": "navigation",
        "min_length": 30,
    },
    {
        "prompt": "Explain quantum mechanics",
        "expected_theme": "science",
        "min_length": 40,
    },
]

# General Red Dwarf scenarios
GENERAL_SCENARIOS: list[TestScenario] = [
    {
        "prompt": "Calculate the route back to Earth from deep space",
        "expected_theme": "space",
        "min_length": 40,
    },
    {
        "prompt": "What happened to the Red Dwarf crew?",
        "expected_theme": "crew",
        "min_length": 30,
    },
]

# All scenarios combined
ALL_SCENARIOS = (
    LISTER_SCENARIOS
    + RIMMER_SCENARIOS
    + CAT_SCENARIOS
    + HOLLY_SCENARIOS
    + GENERAL_SCENARIOS
)
