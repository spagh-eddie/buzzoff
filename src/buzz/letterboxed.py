"""letterboxed: word boxes"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable

from .common import default_words


@dataclasses.dataclass
class TrieNode:
    r"""
    A node on a trie.

    The following is a representation of the words "hi", "he", "hell",
    and "hello", where nodes marked with an asterisk ``*`` mark the ends
    of a word::

          h
         / \
        e*  i*
        |
        l
        |
        l*
        |
        o*
    """

    value: str
    parent: None | TrieNode
    is_word: bool
    children: dict[str, TrieNode]

    @property
    def word(self) -> str:
        """The word up to this node"""
        curr: None | TrieNode = self
        seen = []
        while curr and curr.value:
            seen.append(curr.value)
            curr = curr.parent
        return "".join(reversed(seen))

    @classmethod
    def from_words(cls, words: Iterable[str]) -> TrieNode:
        """Make a trie from the input words"""
        root = TrieNode("", None, False, {})
        for word in words:
            curr = root
            for c in word:
                curr = curr.children.setdefault(c, TrieNode(c, curr, False, {}))
            curr.is_word = True
        return root

    def __contains__(self, word: str) -> bool:
        """Does the trie contain the word?"""
        curr = self
        for c in word:
            try:
                curr = self.children[c]
            except KeyError:
                return False
        return curr.is_word


class LetterBox:
    """
    The NYT's LetterBoxed game.

    Games are represented by boxes of letters::

         HES
        O   A
        P   B
        W   L
         URN

    What you need to do is connect those letters together to create words.
    Consecutive letters cannot be on the same side of the box.
    After the first word, each subsequent word needs to start with the last letter of the previous word.

    The goal is to use up all the letters (repeats allowed) in the fewest words possible!

    The answer to the above problem is::

        BRAWLS-SOUSAPHONE
    """

    def __init__(self, letters: str) -> None:
        n = len(letters)
        if not n or n % 4 != 0:
            raise ValueError("characters not a multiple of 4")
        self.letters = letters
        self.groups: tuple[str, str, str, str] = tuple(  # type: ignore
            letters[i : i + n] for i in range(0, n, n // 4)
        )
        self.graph = {
            i: {j for j in range(n) if j * 4 // n != i * 4 // n} for i in range(n)
        }


def helper(
    node: TrieNode,
    box: LetterBox,
    i: int,
    path: list[int],
    words: list[tuple[str, list[int]]],
):
    """
    Run depth-first search on the trie.
    """
    if node.is_word:
        words.append((node.word, path.copy()))

    for j in box.graph[i]:
        c = box.letters[j]
        if child := node.children.get(c):
            helper(child, box, j, path + [j], words)


def solve(letters: str) -> set[tuple[str, str]]:
    """
    Solve the game.

    - make a trie of all English words within `letters` character set with repeats
    - explore the LetterBox graph depth-first, searching for words in the trie
    - words that can be joined back-to-front sharing one letter are a solution
    """
    box = LetterBox(letters)
    # only need the words made of our letters
    charset = set(box.letters)
    trie = TrieNode.from_words(w for w in default_words() if set(w) <= charset)
    # words and their visited indices
    words = list[tuple[str, list[int]]]()

    # do depth-first search on the LetterBox
    for i, c in enumerate(box.letters):
        path = [i]
        helper(trie.children[c], box, i, path, words)

    all_indices = set(range(len(letters)))
    solutions = set()
    for w1, path1 in words:
        # join words back-to-front sharing one letter
        for w2, path2 in ((w, p) for w, p in words if w.startswith(w1[-1])):
            # if have visited all the vertices, it is a solution
            if (set(path1) | set(path2)) == all_indices:
                solutions.add((w1, w2))
    return solutions
