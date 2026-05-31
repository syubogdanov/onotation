from __future__ import annotations

from typing import TYPE_CHECKING, Self

from .py_trie import Trie as PyTrie


if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

try:
    from .c_trie import Trie as CTrie
except (ImportError, OSError):
    CTrie = None


class Trie:
    """Backend wrapper for Trie."""

    __slots__ = ("_impl",)

    __hash__ = None

    def __init__(self, iterable: Iterable[str] = (), /) -> None:
        """Initialize trie from iterable of strings."""
        impl_cls = CTrie if CTrie is not None else PyTrie
        self._impl = impl_cls()

        for item in iterable:
            self._impl.add(item)

    def __len__(self) -> int:
        """Return number of elements in trie."""
        return len(self._impl)

    def __contains__(self, item: object) -> bool:
        """Check if item is in trie."""
        return item in self._impl

    def __iter__(self) -> Iterator[str]:
        """Iterate over trie elements."""
        return iter(self._impl)

    def __reversed__(self) -> Iterator[str]:
        """Iterate over trie elements in reverse order."""
        return reversed(self._impl)

    def __eq__(self, other: object) -> bool:
        """Compare trie equality."""
        if isinstance(other, Trie):
            return self._impl == other._impl
        return self._impl == other

    def __str__(self) -> str:
        """Return string representation."""
        return str(self._impl)

    def __repr__(self) -> str:
        """Return debug representation."""
        return repr(self._impl)

    def add(self, element: str) -> None:
        """Add element to trie."""
        self._impl.add(element)

    def remove(self, element: str) -> None:
        """Remove element from trie (raises if missing)."""
        self._impl.remove(element)

    def discard(self, element: str) -> None:
        """Remove element if present."""
        self._impl.discard(element)

    def pop(self) -> str:
        """Remove and return arbitrary element."""
        return self._impl.pop()

    def clear(self) -> None:
        """Remove all elements."""
        self._impl.clear()

    def isdisjoint(self, other: object) -> bool:
        """Return True if no elements intersect."""
        return self._impl.isdisjoint(other)

    def __le__(self, other: object) -> bool:
        """Check subset relation."""
        return self._impl <= other

    def __lt__(self, other: object) -> bool:
        """Check proper subset relation."""
        return self._impl < other

    def __ge__(self, other: object) -> bool:
        """Check superset relation."""
        return self._impl >= other

    def __gt__(self, other: object) -> bool:
        """Check proper superset relation."""
        return self._impl > other

    def __or__(self, other: object) -> object:
        """Return union."""
        return self._impl | other

    def __and__(self, other: object) -> object:
        """Return intersection."""
        return self._impl & other

    def __sub__(self, other: object) -> object:
        """Return difference."""
        return self._impl - other

    def __xor__(self, other: object) -> object:
        """Return symmetric difference."""
        return self._impl ^ other

    def __ior__(self, other: object) -> Self:
        """In-place union."""
        self._impl |= other
        return self

    def __iand__(self, other: object) -> Self:
        """In-place intersection."""
        self._impl &= other
        return self

    def __isub__(self, other: object) -> Self:
        """In-place difference."""
        self._impl -= other
        return self

    def __ixor__(self, other: object) -> Self:
        """In-place symmetric difference."""
        self._impl ^= other
        return self

    @property
    def _root(self) -> object:
        """Internal root access (debug)."""
        return getattr(self._impl, "_root", None)

    @property
    def _size(self) -> int:
        """Return size of trie."""
        return getattr(self._impl, "_size", len(self._impl))
