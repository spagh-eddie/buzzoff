__all__ = ["__version__", "words", "buzz"]
__version__ = "1.0.0"

from collections.abc import Iterator

with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
    words = f.read().splitlines()


def buzz(letters: str) -> Iterator[str]:
    """Analyze a sequence of letters"""
    letters = set(letters)
    return filter(letters.issuperset, words)
