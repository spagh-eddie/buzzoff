"""Definitely not designed to assist with NYT puzzles. Pinky promise."""

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError as e:
    raise ModuleNotFoundError("no version found; please install") from e
