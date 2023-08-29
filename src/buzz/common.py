"""Common utilities"""


def default_words() -> list[str]:
    """Default words if not provided"""
    with open("/usr/share/dict/words", "r", encoding="utf-8") as f:
        return tuple(f.read().splitlines())
