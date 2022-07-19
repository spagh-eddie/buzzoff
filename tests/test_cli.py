"""Test the CLI"""

import subprocess
import sys


def run(*args: str) -> list[str]:
    """Return the words output by running the CLI with arguments ``args``"""
    return (
        subprocess.run(
            [sys.executable, "-m", "buzzoff", *args],
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .splitlines()
    )


def test_simple() -> None:
    """An expected word exists and a word with wrong characters does not"""
    words = run("abcdefg")
    assert "deaf" in words
    assert "hello" not in words


def test_no_three_letter_by_default() -> None:
    """Three letter words or under are not accepted by default"""
    words = run("abcdtuv")
    assert "a" not in words
    assert "at" not in words
    assert "tub" not in words
    assert "tuba" in words


def test_three_letter_if_ask() -> None:
    """Three letter words are accepted if ask for them"""
    words = run("-l", "3", "abcdtuv")
    assert "a" not in words
    assert "at" not in words
    assert "tub" in words
    assert "tuba" in words
