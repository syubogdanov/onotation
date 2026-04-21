from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from contextlib import suppress
from dataclasses import dataclass
from typing import Generic, Self, TypeVar, cast, overload


T = TypeVar("T")
Q = TypeVar("Q")


@dataclass
class Node(Generic[T]):
    """The BST node."""

    value: T
    parent: Node[T] | None = None
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
        element = cast("T", element)

        while node:
            if element < node.value:  # type: ignore[operator]
                node = node.left
            elif node.value < element:  # type: ignore[operator]
                node = node.right
            else:
                return True

        return False

    def _get_rightmost(self, node: Node[T]) -> Node[T]:
        """Return the rightmost node in the subtree."""
        while node.right:
            node = node.right

        return cast("Node[T]", node)

    def _get_leftmost(self, node: Node[T]) -> Node[T]:
        """Return the leftmost node in the subtree."""
        while node.left:
            node = node.left

        return cast("Node[T]", node)

    def _get_predecessor(self, node: Node[T]) -> Node[T] | None:
        """Return the in-order predecessor of the node."""
        if node.left:
            return self._get_rightmost(cast("Node[T]", node.left))

        current = node
        while current.parent and current.parent.left is current:
            current = current.parent

        return current.parent

    def _get_successor(self, node: Node[T]) -> Node[T] | None:
        """Return the in-order successor of the node."""
        if node.right:
            return self._get_leftmost(cast("Node[T]", node.right))

        current = node
        while current.parent and current.parent.right is current:
            current = current.parent

        return current.parent

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
            :obj:`True` if disjoint, otherwise :obj:`False`.parent
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
        if not self._root:
            self._root = Node(element)
            self._size = 1
            return

        node = self._root

        while True:
            if element < node.value:  # type: ignore[operator]
                if not node.left:
                    node.left = Node(element, parent=node)
                    self._size += 1
                    return
                node = node.left
            elif node.value < element:  # type: ignore[operator]
                if not node.right:
                    node.right = Node(element, parent=node)
                    self._size += 1
                    return
                node = node.right
            else:
                return

    def _find_node(self, element: T) -> Node[T] | None:
        """Find node with given element."""
        node = self._root
        while node and node.value != element:
            node = node.left if element < node.value else node.right  # type: ignore[operator]

        return node

    def remove(self, element: T, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : T
            Element.
        """
        node = self._find_node(element)
        if not node:
            raise KeyError(element)

        if not node.left or not node.right:
            child = node.left if node.left else node.right

            if child:
                child.parent = node.parent

            if not node.parent:
                self._root = child
            elif node.parent.left is node:
                node.parent.left = child
            else:
                node.parent.right = child

            self._size -= 1
            return

        exception = "unreachable"
        successor = self._get_successor(node)
        if successor is None:
            raise RuntimeError(exception)

        node.value = successor.value

        child = successor.right

        if child:
            child.parent = successor.parent

        if successor.parent is None:
            self._root = child
        elif successor.parent.left is successor:
            successor.parent.left = child
        else:
            successor.parent.right = child

        self._size -= 1

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
        if not self._root:
            detail = f"pop from an empty {self.__class__.__name__}"
            raise KeyError(detail)

        node = self._root

        while node.left:
            node = node.left

        value = node.value

        if node.right:
            node.right.parent = node.parent

        if not node.parent:
            self._root = node.right
        elif node.parent.left is node:
            node.parent.left = node.right
        else:
            node.parent.left = node.right

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
        if not self._root:
            return

        current: Node[T] | None = self._get_leftmost(self._root)

        while current:
            yield current.value
            current = self._get_successor(current)

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
        if not self._root:
            return

        current: Node[T] | None = self._get_rightmost(self._root)

        while current:
            yield current.value
            current = self._get_predecessor(current)
