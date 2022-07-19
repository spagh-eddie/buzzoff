"""buzzoff: word generation"""

__all__ = ["__version__", "words", "buzz"]
__version__ = "1.0.0"

from collections.abc import Iterable, Iterator

with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
    words = f.read().splitlines()


def buzz(
    letters: Iterable[str], minlength: int, mandatory: None | str
) -> Iterator[str]:
    """
    Analyze a sequence of letters.

    :param letters: the available letters from which to make words
    :param minlength: minimum word length allowed
    :param mandatory: if given, these letters must be included
    """
    s = set(letters)
    filters = [lambda w: len(w) >= minlength, s.issuperset]
    if mandatory:
        filters.insert(0, lambda w: all(c in w for c in mandatory))  # type: ignore[union-attr]
    return filter(lambda w: all(f(w) for f in filters), words)
