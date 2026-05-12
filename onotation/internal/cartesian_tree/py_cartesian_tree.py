from __future__ import annotations

import random

from collections.abc import Callable, Iterable, Iterator, MutableSequence, Reversible
from typing import Any, TypeVar, overload


T = TypeVar("T")


class CartesianTree(MutableSequence[T], Reversible[T]):
    """Cartesian tree with implicit key (Treap).

    Data structure that acts like a list (supports O(log(n)) split/merge operations)
    while maintaining heap order by random priorities.
    """

    __slots__ = ("_random", "_root", "_size")

    def __init__(
        self,
        iterable: Iterable[T] = (),
        /,
        *,
        random: Callable[[], Any] = random.random,
    ) -> None:
        """Initialize the object.

        Parameters
        ----------
        iterable : Iterable[T]
            Iterable.
        random : Callable[[], Any], optional
            Random function that returns priorities.
            Default is ``random.random`` from standard library.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Return the number of elements in set (cardinality).

        Returns
        -------
        :class:`int`
            Length.
        """
        raise NotImplementedError

    @overload
    def __getitem__(self, index: int, /) -> T: ...

    @overload
    def __getitem__(self, index: slice, /) -> CartesianTree[T]: ...

    def __getitem__(self, index: int | slice, /) -> T | CartesianTree[T]:
        """Return self[key].

        Accpets both integer indices and slices.
        Slice returns a new CartesianTree.
        """
        raise NotImplementedError

    @overload
    def __setitem__(self, index: int, value: T, /) -> None: ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[T], /) -> None: ...

    def __setitem__(self, index: int | slice, value: T | Iterable[T], /) -> None:
        """Set self[key] to value.

        Supports both integer indices and slices.
        """
        raise NotImplementedError

    @overload
    def __delitem__(self, index: int, /) -> None: ...

    @overload
    def __delitem__(self, index: slice, /) -> None: ...

    def __delitem__(self, index: int | slice, /) -> None:
        """Delete self[key]."""
        raise NotImplementedError

    def insert(self, index: int, value: T, /) -> None:
        """Insert ``value`` before ``index``.

        Parameters
        ----------
        index : int
            Position before which to insert.
        value : T
            Element to insert.
        """
        raise NotImplementedError

    def append(self, value: T, /) -> None:
        """Append ``value`` to the end of the tree.

        Equivalent to ``self.insert(len(self), value)``.
        """
        raise NotImplementedError

    def extend(self, iterable: Iterable[T], /) -> None:
        """Extend the tree by appending elements from the iterable."""
        raise NotImplementedError

    def pop(self, index: int = -1, /) -> T:
        """Remove and return item at ``index`` (default last).

        Raises IndexError if the tree is empty or index is out of range.
        """
        raise NotImplementedError

    def remove(self, value: T, /) -> None:
        """Remove first occurrence of ``value``.

        Raises ValueError if the value is not present.
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all items from the Cartesian tree."""
        raise NotImplementedError

    def reverse(self) -> None:
        """Reverse the Cartesian tree in place.

        Note: this operation is expensive in a treap (O(n) or needs special handling).
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the tree in order.

        Guaranteed in-order (left-to-right) traversal.
        """
        raise NotImplementedError

    def __reversed__(self) -> Iterator[T]:
        """Return a reverse iterator over the tree.

        Guaranteed right-to-left traversal.
        """
        raise NotImplementedError

    def index(self, value: T, start: int = 0, stop: int = -1, /) -> int:
        """Return first index of ``value``.

        Raises ValueError if the value is not present.
        """
        raise NotImplementedError

    def count(self, value: T, /) -> int:
        """Return number of occurrences of ``value``."""
        raise NotImplementedError

    def __eq__(self, other: object, /) -> bool:
        """Return self == other.

        Two CartesianTree instances are equal if they contain the same
        elements in the same order.
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        """Hash is not defined for mutable sequences.

        Raises TypeError if called.
        """
        raise NotImplementedError
