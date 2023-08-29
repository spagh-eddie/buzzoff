"""Common utilities"""

from pathlib import Path


def default_words() -> list[str]:
    """Default words if not provided"""
    with open(Path(__file__).parent / "words_alpha.txt", "r", encoding="utf-8") as f:
        return f.read().splitlines()
