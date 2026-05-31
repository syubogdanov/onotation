from __future__ import annotations

from collections.abc import Iterable, Iterator
from contextlib import suppress

from onotation.internal.avl_tree.py_avl_tree import AVLTree as PyAVLTree

c_avl_tree = None

with suppress(ImportError, OSError):
    from onotation.internal.avl_tree.c_avl_tree import AVLTree as CAVLTree

    c_avl_tree = CAVLTree


class AVLTree:
    """AVL Tree with automatic backend selection (C if available)."""

    __slots__ = ("_impl",)

    def __init__(self, iterable: Iterable[int] = (), /) -> None:
        """Initialize tree with optional iterable."""
        if c_avl_tree is not None:
            self._impl = c_avl_tree()
        else:
            self._impl = PyAVLTree()

        for element in iterable:
            self.add(element)

    def __len__(self) -> int:
        """Return number of elements."""
        return len(self._impl)

    def __contains__(self, element: object) -> bool:
        """Test element membership."""
        return element in self._impl

    def __iter__(self) -> Iterator[int]:
        """Return iterator over elements."""
        return iter(self._impl)

    def __reversed__(self) -> Iterator[int]:
        """Return reverse iterator over elements."""
        return reversed(self._impl)

    def __eq__(self, other: object) -> bool:
        """Compare two trees for equality."""
        if not isinstance(other, AVLTree):
            return NotImplemented
        return self._impl == other._impl

    def __hash__(self) -> int:
        """Hash not defined for mutable tree."""
        raise NotImplementedError

    def add(self, element: int) -> None:
        """Add element to tree."""
        self._impl.add(element)

    def remove(self, element: int) -> None:
        """Remove element from tree."""
        self._impl.remove(element)

    def discard(self, element: int) -> None:
        """Remove element if present."""
        self._impl.discard(element)

    def pop(self) -> int:
        """Remove and return arbitrary element."""
        return self._impl.pop()

    def clear(self) -> None:
        """Remove all elements."""
        self._impl.clear()
