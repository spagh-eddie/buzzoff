"""buzzoff: word generation"""

__all__ = ["__version__", "version_tuple", "buzz"]

import pickle
from collections import defaultdict
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TypeAlias

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError as e:
    raise ModuleNotFoundError("no version found; please install") from e


Store: TypeAlias = dict[frozenset[str], list[str]]
CACHE = Path("~/.buzzoff/preprocessed.txt").expanduser()
CACHE_HASH = Path("~/.buzzoff/hash.txt").expanduser()


def buzz(
    letters: Iterable[str],
    minlength: int,
    mandatory: None | str,
    words: None | tuple[str, ...] = None,
) -> Iterator[str]:
    """
    Analyze a sequence of letters.

    :param letters: the available letters from which to make words
    :param minlength: minimum word length allowed
    :param mandatory: if given, these letters must be included
    :param words: an optional tuple of valid words.
        Defaults to the system's word dictionary.
    """
    if words is not None and (h := read_cache_hash()) and h == hash(words):
        store = read_preprocessed()
    elif words is not None:
        store = preprocess(words)
    else:
        try:
            store = read_preprocessed()
        except FileNotFoundError:
            store = preprocess(default_words())
    s = set(letters)
    filters = [lambda w: len(w) >= minlength, s.issuperset]
    if mandatory:
        filters.insert(0, lambda w: all(c in w for c in mandatory))  # type: ignore[union-attr]
    for word_letters, possibilities in store.items():
        if not word_letters.issubset(s):
            continue
        yield from filter(lambda w: all(f(w) for f in filters), possibilities)


def default_words() -> tuple[str, ...]:
    """Default words if not provided"""
    with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
        return tuple(f.read().splitlines())


def preprocess(words: tuple[str, ...]) -> Store:
    """Preprocess words"""
    store = defaultdict(list)
    for word in words:
        store[frozenset(word)].append(word)
    cache_preprocessed(hash(words), store)
    return store


def cache_preprocessed(h: int, store: Store) -> None:
    """Cache the preprocessed words for speed"""
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE, "xb") as f:
        pickle.dump(store, f)
    CACHE_HASH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_HASH, "w", encoding="utf-8") as f:
        f.write(str(h))


def read_cache_hash() -> int:
    """Read the cache's hash"""
    with open(CACHE_HASH, "r", encoding="utf-8") as f:
        return int(f.read())


def read_preprocessed() -> Store:
    """Read the cache's preprocessed words"""
    with open(CACHE, "rb") as f:
        return pickle.load(f)
