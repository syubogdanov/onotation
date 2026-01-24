from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, Generic, Self, TypeAlias, TypeVar, overload

from onotation.internal.typing import SupportsDunderGT, SupportsDunderLT


T = TypeVar("T", bound=SupportsDunderLT)
Q = TypeVar("Q", bound=SupportsDunderLT)


SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]


@dataclass
class Node(Generic[T]):
    """The BST node."""

    value: T
    left: Node[T] | None = None
    right: Node[T] | None = None


class BinarySearchTree(MutableSet[T], Reversible[T]):
    """The binary search tree."""

    __slots__ = ("_root", "_size")

    def __init__(self, iterable: Iterable[T] = (), /) -> None:
        """Initialize the object.

        Parameters
        ----------
        iterable : Iterable[T]
            Iterable.
        """
        self._root: Node[T] | None = None
        self._size: int = 0

        for element in iterable:
            self.add(element)

    def __len__(self) -> int:
        """Return the number of elements in set (cardinality).

        Returns
        -------
        :class:`int`
            Length.
        """
        return self._size

    def __contains__(self, element: object, /) -> bool:
        """Test ``element`` for membership in the set.

        Parameters
        ----------
        element : object
            Element.

        Returns
        -------
        :class:`bool`
            :obj:`True` if present, otherwise :obj:`False`.
        """
        node = self._root

        while node is not None:
            if element > node.value:
                node = node.left
            elif node.value < element:
                node = node.right
            else:
                return True

        return False

    def isdisjoint(self, other: Iterable[object], /) -> bool:
        """Return ``True`` if the set has no elements in common with ``other``.

        Sets are disjoint if and only if their intersection is the empty set.

        Parameters
        ----------
        other : Iterable[object]
            Iterable.

        Returns
        -------
        :class:`bool`
            :obj:`True` if disjoint, otherwise :obj:`False`.
        """
        return all(element not in self for element in other)

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
        return all(elements in other for elements in self)

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
        return self <= other and self != other

    def __ge__(self, other: AbstractSet[object], /) -> bool:
        """Test whether every element in ``other`` is in the set.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if superset, otherwise :obj:`False`.
        """
        return all(element in self for element in other)

    def __gt__(self, other: AbstractSet[object], /) -> bool:
        """Test whether the set is a proper superset of ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if proper superset, otherwise :obj:`False`.
        """
        return other <= self and other != self

    @overload  # type: ignore[override]
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
        result = BinarySearchTree[T | Q]() if isinstance(other, BinarySearchTree) else set[T | Q]()

        for element in other:
            element_new: T | Q = element
            result.add(element_new)

        return result

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
        result: BinarySearchTree[T] = BinarySearchTree()

        for element in self:
            if element in other:
                result.add(element)

        return result

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
        result: BinarySearchTree[T] = BinarySearchTree()

        for element in self:
            if element not in other:
                result.add(element)

        return result

    @overload  # type: ignore[override]
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
        result = BinarySearchTree[T | Q]() if isinstance(other, BinarySearchTree) else set[T | Q]()

        for element in other:
            element_new: T | Q = element
            if element_new in result:
                result.discard(element_new)
            else:
                result.add(element_new)

        return result

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
        for element in other:
            self.add(element)

        return self

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
        to_remove = [element for element in self if element not in other]
        for element in to_remove:
            self.discard(element)

        return self

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
        to_remove = [element for element in self if element in other]
        for element in to_remove:
            self.discard(element)

        return self

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
        to_remove = [element for element in self if element in other]
        to_add = [element for element in other if element not in self]

        for element in to_remove:
            self.discard(element)

        for element in to_add:
            self.add(element)

        return self

    def add(self, element: T, /) -> None:
        """Add ``element`` to the set.

        Parameters
        ----------
        element : T
            Element.
        """

        def _insert(node: Node | None, value: T) -> Node:
            if node is None:
                self._size += 1
                return Node(value, None, None)

            if value < node.value:
                node.left = _insert(node.left, value)
            elif node.value < value:
                node.right = _insert(node.right, value)

            return node

        self._root = _insert(self._root, element)

    def remove(self, element: T, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : T
            Element.
        """

        def _remove(node: Node[T] | None, value: T) -> Node[T] | None:
            if node is None:
                raise KeyError(value)

            if value < node.value:
                node.left = _remove(node.left, value)
            elif node.value < value:
                node.right = _remove(node.right, value)
            else:
                self._size -= 1
                if node.left is None:
                    return node.right

                if node.right is None:
                    return node.left

                successor = node.right
                while successor.left is not None:
                    successor = successor.left

                node.value = successor.value
                node.right = _remove(node.right, successor.value)

            return node

        self._root = _remove(self._root, element)

    def discard(self, element: T, /) -> None:
        """Remove ``element`` from the set if it is present.

        Parameters
        ----------
        element : T
            Element.
        """
        with suppress(KeyError):
            self.remove(element)

    def pop(self) -> T:
        """Remove and return an arbitrary element from the set.

        Returns
        -------
        T
            Element.
        """
        error = "pop from empty BinarySearchTree"

        if self._root is None:
            raise KeyError(error)

        node = self._root
        parent = None
        while node.left is not None:
            parent = node
            node = node.left

        value = node.value
        if parent is None:
            self._root = node.right
        else:
            parent.left = node.right

        self._size -= 1
        return value

    def clear(self) -> None:
        """Remove all elements from the set."""
        self._root = None
        self._size = 0

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
        if not isinstance(other, AbstractSet):
            return False

        return self <= other <= self

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
        stack: list[Node[T]] = []
        node = self._root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left

            node = stack.pop()
            yield node.value
            node = node.right

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
        stack: list[Node] = []
        node = self._root
        while stack or node:
            while node:
                stack.append(node)
                node = node.right

            node = stack.pop()
            yield node.value
            node = node.left
