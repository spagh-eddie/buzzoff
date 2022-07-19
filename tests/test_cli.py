"""Test the CLI"""


def run(*args: str) -> list[str]:
    """Return the words output by running the CLI with arguments ``args``"""
    raise NotImplementedError()


def test_simple() -> None:
    """An expected word exists and a word with wrong characters does not"""
    words = run("abcdefg")
    assert "deaf" in words
    assert "hello" not in words
