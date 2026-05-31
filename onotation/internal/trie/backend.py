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
        """Initialize trie."""
        impl_cls = CTrie if CTrie is not None else PyTrie

        self._impl = impl_cls()

        for item in iterable:
            self._impl.add(item)

    def __len__(self) -> int:
        """Return trie size."""
        return len(self._impl)

    def __contains__(self, item: object) -> bool:
        """Check membership."""
        return item in self._impl

    def __iter__(self) -> Iterator[str]:
        """Return iterator."""
        return iter(self._impl)

    def __reversed__(self) -> Iterator[str]:
        """Return reverse iterator."""
        return reversed(self._impl)

    def __eq__(self, other: object) -> bool:
        """Compare tries."""
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
        """Add element."""
        self._impl.add(element)

    def remove(self, element: str) -> None:
        """Remove element."""
        self._impl.remove(element)

    def discard(self, element: str) -> None:
        """Discard element."""
        self._impl.discard(element)

    def pop(self) -> str:
        """Pop element."""
        return self._impl.pop()

    def clear(self) -> None:
        """Clear trie."""
        self._impl.clear()

    def isdisjoint(self, other: object) -> bool:
        """Check disjointness."""
        return self._impl.isdisjoint(other)

    def __le__(self, other: object) -> bool:
        """Subset check."""
        return self._impl <= other

    def __lt__(self, other: object) -> bool:
        """Proper subset check."""
        return self._impl < other

    def __ge__(self, other: object) -> bool:
        """Superset check."""
        return self._impl >= other

    def __gt__(self, other: object) -> bool:
        """Proper superset check."""
        return self._impl > other

    def __or__(self, other: object) -> object:
        """Union."""
        return self._impl | other

    def __and__(self, other: object) -> object:
        """Intersection."""
        return self._impl & other

    def __sub__(self, other: object) -> object:
        """Difference."""
        return self._impl - other

    def __xor__(self, other: object) -> object:
        """Symmetric difference."""
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
        """Return root node."""
        return getattr(self._impl, "_root", None)

    @property
    def _size(self) -> int:
        """Return trie size."""
        return getattr(self._impl, "_size", len(self._impl))
