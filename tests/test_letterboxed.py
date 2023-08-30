"""Test the CLI"""

import subprocess
import sys

from buzz.letterboxed import solve, TrieNode


def run(*args: str) -> list[str]:
    """Return the words output by running the CLI with arguments ``args``"""
    return (
        subprocess.run(
            [sys.executable, "-m", "buzz", "letterboxed", *args],
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .splitlines()
    )


def testStringTrie() -> None:
    """Test `StringTrie` behavior"""
    trie = TrieNode.from_words(("hi", "he", "hell", "hello"))
    assert not trie.is_word

    h = trie.children["h"]
    he = h.children["e"]
    hel = he.children["l"]
    hell = hel.children["l"]
    hello = hell.children["o"]

    assert not h.is_word
    assert he.is_word
    assert not hel.is_word
    assert hell.is_word
    assert hello.is_word

    assert hel.word == "hel"
    assert hello.word == "hello"


def test_simple() -> None:
    """An expected pair exists and an unexpected pair does not"""
    solutions = solve("hesopwablurn")
    assert ("hello,", "world!") not in solutions
    assert ("brawls", "sousaphone") in solutions

    out = run("hesopwablurn")
    assert "hello, world!" not in out
    assert "brawls sousaphone" in out


def test_intrarepeated_characters() -> None:
    """Test characters repeated on the same side"""
    assert run("hheelloo") == ["ohelo ohelo"]


def test_interrepeated_characters() -> None:
    """Test characters repeated on different sides"""
    solutions = solve("been")
    assert ("been", "been") not in solutions
    assert ("been", "nee") in solutions
