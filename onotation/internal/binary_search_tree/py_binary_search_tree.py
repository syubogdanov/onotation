from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from typing import TYPE_CHECKING, Any, Self, TypeAlias, TypeVar, overload

from onotation.internal.typing import SupportsDunderGT, SupportsDunderLT


if TYPE_CHECKING:
    from types import EllipsisType


T = TypeVar("T")
Q = TypeVar("Q")


SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]


class BinarySearchTree(MutableSet[T], Reversible[T]):
    """The binary search tree."""

    def __init__(self, iterable: Iterable[T] = (), /) -> None:
        """Initialize the object.

        Parameters
        ----------
        iterable : Iterable[T]
            Iterable.
        """
        raise NotImplementedError

    def __and__(self, other: AbstractSet[object], /) -> BinarySearchTree[T]:
        """Return a new set with elements common to the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        BinarySearchTree[T]
            Binary search tree.
        """
        raise NotImplementedError

    def __contains__(self, element: object, /) -> bool:
        """Test ``element`` for membership.

        Parameters
        ----------
        element : object
            Element.

        Returns
        -------
        :class:`bool`
            :obj:`True` if present, otherwise :obj:`False`.
        """
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """Test whether the set equals to ``other``.

        Parameters
        ----------
        other : object
            Object.

        Returns
        -------
        :class:`bool`
            :obj:`True` if equal, otherwise :obj:`False`.
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        """Return the hash.

        Returns
        -------
        :class:`int`
            Hash.

        Notes
        -----
        * Not defined.
        """
        raise NotImplementedError

    def __ge__(self, other: AbstractSet[object], /) -> bool:
        """Test whether every element in ``other`` is in the set.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if subset, otherwise :obj:`False`.
        """
        raise NotImplementedError

    def __gt__(self, other: AbstractSet[object], /) -> bool:
        """Test whether the set is a proper superset of ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if proper subset, otherwise :obj:`False`.
        """
        raise NotImplementedError

    def __iand__(self, other: AbstractSet[object], /) -> Self:
        """Update the set, keeping only elements found in it and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Self
            self.
        """
        raise NotImplementedError

    def __ior__(self, other: AbstractSet[T], /) -> Self:  # type: ignore[misc, override]
        """Update the set, adding elements from ``other``.

        Parameters
        ----------
        other : AbstractSet[T]
            Set.

        Returns
        -------
        Self
            self.
        """
        raise NotImplementedError

    def __isub__(self, other: AbstractSet[object], /) -> Self:
        """Update the set, removing elements found in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Self
            self.
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        """Return an iterator.

        Returns
        -------
        Iterator[T]
            Iterator.

        Notes
        -----
        * An ascending order is guaranteed.
        """
        raise NotImplementedError

    def __ixor__(self, other: AbstractSet[T], /) -> Self:  # type: ignore[misc, override]
        """Update the set, keeping only elements found in either set, but not in both.

        Parameters
        ----------
        other : AbstractSet[T]
            Set.

        Returns
        -------
        Self
            self.
        """
        raise NotImplementedError

    def __le__(self, other: AbstractSet[object], /) -> bool:
        """Test whether every element in the set is in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if subset, otherwise :obj:`False`.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Return the number of elements.

        Returns
        -------
        :class:`int`
            Length.
        """
        raise NotImplementedError

    def __lt__(self, other: AbstractSet[object], /) -> bool:
        """Test whether the set is a proper subset of ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if proper subset, otherwise :obj:`False`.
        """
        raise NotImplementedError

    @overload
    def __max__(
        self,
        /,
        *,
        key: Callable[[T], SupportsRichComparison] | EllipsisType = ...,
    ) -> T: ...

    @overload
    def __max__(
        self,
        /,
        *,
        default: Q,
        key: Callable[[T], SupportsRichComparison] | EllipsisType = ...,
    ) -> T | Q: ...

    def __max__(
        self,
        /,
        *,
        default: Q | EllipsisType = ...,
        key: Callable[[T], SupportsRichComparison] | EllipsisType = ...,
    ) -> T | Q:
        """Return the largest item.

        Parameters
        ----------
        key : Callable[[T], SupportsRichComparison], unset
            Comparator.

        default : Q, unset
            Default item.

        Returns
        -------
        T | Q
            Largest or default.
        """
        raise NotImplementedError

    @overload
    def __min__(
        self,
        /,
        *,
        key: Callable[[T], SupportsRichComparison] | EllipsisType = ...,
    ) -> T: ...

    @overload
    def __min__(
        self,
        /,
        *,
        default: Q,
        key: Callable[[T], SupportsRichComparison] | EllipsisType = ...,
    ) -> T | Q: ...

    def __min__(
        self,
        /,
        *,
        default: Q | EllipsisType = ...,
        key: Callable[[T], SupportsRichComparison] | EllipsisType = ...,
    ) -> T | Q:
        """Return the smallest item.

        Parameters
        ----------
        key : Callable[[T], SupportsRichComparison], unset
            Comparator.

        default : Q, unset
            Default item.

        Returns
        -------
        T | Q
            Smallest or default.
        """
        raise NotImplementedError

    @overload
    def __or__(self, other: BinarySearchTree[Q], /) -> BinarySearchTree[T | Q]: ...

    @overload
    def __or__(self, other: AbstractSet[Q], /) -> MutableSet[T | Q]: ...

    def __or__(self, other: AbstractSet[Q], /) -> MutableSet[T | Q]:
        """Return a new set with elements from the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[Q]
            Set.

        Returns
        -------
        MutableSet[T | Q]
            Set.
        """
        raise NotImplementedError

    def __reversed__(self) -> Iterator[T]:
        """Return a reverse iterator.

        Returns
        -------
        Iterator[T]
            Iterator.

        Notes
        -----
        * A descending order is guaranteed.
        """
        raise NotImplementedError

    def __sub__(self, other: AbstractSet[object], /) -> BinarySearchTree[T]:
        """Return a new set with elements in the set that are not in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        BinarySearchTree[T]
            Binary search tree.
        """
        raise NotImplementedError

    @overload
    def __xor__(self, other: BinarySearchTree[Q], /) -> BinarySearchTree[T | Q]: ...

    @overload
    def __xor__(self, other: AbstractSet[Q], /) -> MutableSet[T | Q]: ...

    def __xor__(self, other: AbstractSet[Q], /) -> MutableSet[T | Q]:
        """Return a new set with elements in either the set or ``other`` but not both.

        Parameters
        ----------
        other : AbstractSet[Q]
            Set.

        Returns
        -------
        MutableSet[T | Q]
            Set.
        """
        raise NotImplementedError

    def add(self, element: T, /) -> None:
        """Add ``element`` to the set.

        Parameters
        ----------
        element : T
            Element.
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all elements from the set."""
        raise NotImplementedError

    def discard(self, element: T, /) -> None:
        """Remove ``element`` from the set if it is present.

        Parameters
        ----------
        element : T
            Element.
        """
        raise NotImplementedError

    def isdisjoint(self, other: Iterable[object], /) -> bool:
        """Return ``True`` if the set has no elements in common with ``other``.

        Parameters
        ----------
        other : Iterable[object]
            Iterable.

        Returns
        -------
        :class:`bool`
            :obj:`True` if disjoint, otherwise :obj:`False`.
        """
        raise NotImplementedError

    def pop(self) -> T:
        """Remove and return an arbitrary element from the set.

        Returns
        -------
        T
            Element.
        """
        raise NotImplementedError

    def remove(self, element: T, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : T
            Element.
        """
        raise NotImplementedError
