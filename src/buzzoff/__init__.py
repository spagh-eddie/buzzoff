__all__ = ["__version__", "words", "buzz"]
__version__ = "1.0.0"

from collections.abc import Iterator

with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
    words = f.read().splitlines()


def buzz(letters: str, minlength: int) -> Iterator[str]:
    """Analyze a sequence of letters"""
    letters = set(letters)
    filters = (lambda w: len(w) >= minlength, letters.issuperset)
    return filter(lambda w: all(f(w) for f in filters), words)
