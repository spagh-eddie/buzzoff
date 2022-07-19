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
