from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .py_trie import Trie as PyTrie

CTrie: Any

try:
    from .c_trie import Trie as CTrie
except (ImportError, OSError):
    CTrie = None


class Trie:
    """Backend wrapper for Trie.

    Uses the C extension implementation when available,
    otherwise falls back to the pure Python version.
    """

    __slots__ = ("_impl",)

    def __init__(self, iterable: Iterable[str] = (), /) -> None:
        impl_cls = CTrie if CTrie is not None else PyTrie

        self._impl = impl_cls()

        for item in iterable:
            self._impl.add(item)

    def __len__(self) -> int:
        return len(self._impl)

    def __contains__(self, item: object) -> bool:
        return item in self._impl

    def __iter__(self):
        return iter(self._impl)

    def __reversed__(self):
        return reversed(self._impl)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Trie):
            return self._impl == other._impl
        return self._impl == other

    def __str__(self) -> str:
        return str(self._impl)

    def __repr__(self) -> str:
        return repr(self._impl)

    def add(self, element: str) -> None:
        self._impl.add(element)

    def remove(self, element: str) -> None:
        self._impl.remove(element)

    def discard(self, element: str) -> None:
        self._impl.discard(element)

    def pop(self) -> str:
        return self._impl.pop()

    def clear(self) -> None:
        self._impl.clear()

    def isdisjoint(self, other):
        return self._impl.isdisjoint(other)

    def __le__(self, other):
        return self._impl <= other

    def __lt__(self, other):
        return self._impl < other

    def __ge__(self, other):
        return self._impl >= other

    def __gt__(self, other):
        return self._impl > other

    def __or__(self, other):
        return self._impl | other

    def __and__(self, other):
        return self._impl & other

    def __sub__(self, other):
        return self._impl - other

    def __xor__(self, other):
        return self._impl ^ other

    def __ior__(self, other):
        self._impl |= other
        return self

    def __iand__(self, other):
        self._impl &= other
        return self

    def __isub__(self, other):
        self._impl -= other
        return self

    def __ixor__(self, other):
        self._impl ^= other
        return self

    @property
    def _root(self):
        return getattr(self._impl, "_root", None)

    @property
    def _size(self):
        return getattr(self._impl, "_size", len(self._impl))