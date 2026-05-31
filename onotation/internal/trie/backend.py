from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from onotation.internal.trie.py_trie import Trie as PyTrie


if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


c_trie = None

with suppress(ImportError, OSError):
    from onotation.internal.trie.c_trie import Trie as CTrie
    c_trie = CTrie


class Trie:
    """Trie wrapper with automatic backend selection (C if available)."""

    __slots__ = ("_impl",)

    def __init__(self, iterable: Iterable[str] = (), /) -> None:
        """Initialize Trie.

        Parameters
        ----------
        iterable : Iterable[str]
            Optional iterable of strings to insert.
        """
        self._impl = c_trie() if c_trie else PyTrie()

        for x in iterable:
            self.add(x)

    def __len__(self) -> int:
        """Return number of elements in the trie."""
        return len(self._impl)

    def __contains__(self, x: object) -> bool:
        """Check if element exists in trie."""
        return x in self._impl

    def __iter__(self) -> Iterator[str]:
        """Iterate over elements in lexicographic order."""
        return iter(self._impl)

    def __reversed__(self) -> Iterator[str]:
        """Iterate over elements in reverse lexicographic order."""
        return reversed(self._impl)

    def add(self, x: str) -> None:
        """Add element to trie."""
        self._impl.add(x)

    def remove(self, x: str) -> None:
        """Remove element from trie.

        Raises
        ------
        KeyError
            If element not found.
        """
        self._impl.remove(x)

    def discard(self, x: str) -> None:
        """Remove element if present."""
        self._impl.discard(x)

    def clear(self) -> None:
        """Remove all elements from trie."""
        self._impl.clear()
