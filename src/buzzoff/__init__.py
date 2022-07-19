"""buzzoff: word generation"""

__all__ = ["__version__", "words", "buzz"]
__version__ = "1.0.0"

from collections.abc import Iterator

with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
    words = f.read().splitlines()


def buzz(letters: str, minlength: int) -> Iterator[str]:
    """Analyze a sequence of letters"""
    s = set(letters)
    filters = (lambda w: len(w) >= minlength, s.issuperset)
    return filter(lambda w: all(f(w) for f in filters), words)
