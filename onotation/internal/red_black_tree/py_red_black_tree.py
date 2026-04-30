from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, Self, TypeVar, overload


T = TypeVar("T")
Q = TypeVar("Q")


class Color(Enum):
    """Node color for RBT."""

    RED = auto()
    BLACK = auto()


@dataclass
class Node(Generic[T]):
    """The RBT node."""

    value: T
    color: Color = Color.RED
    parent: Node[T] | None = None
    left: Node[T] | None = None
    right: Node[T] | None = None

    @property
    def grandparent(self) -> Node[T] | None:
        """Return the grandparent of the node."""
        if self.parent is None:
            return None
        return self.parent.parent

    @property
    def sibling(self) -> Node[T] | None:
        """Return the sibling of the node."""
        if self.parent is None:
            return None
        if self is self.parent.left:
            return self.parent.right
        return self.parent.left

    @property
    def uncle(self) -> Node[T] | None:
        """Return the uncle of the node."""
        if self.parent is None:
            return None
        return self.parent.sibling

    @property
    def leftmost(self) -> Node[T]:
        """Return the leftmost node in the subtree."""
        node = self
        while node.left:
            node = node.left
        return node

    @property
    def rightmost(self) -> Node[T]:
        """Return the rightmost node in the subtree."""
        node = self
        while node.right:
            node = node.right
        return node

    @property
    def successor(self) -> Node[T] | None:
        """Return the in-order successor."""
        if self.right:
            return self.right.leftmost

        current = self
        while current.parent and current.parent.right is current:
            current = current.parent
        return current.parent

    @property
    def predecessor(self) -> Node[T] | None:
        """Return the in-order predecessor."""
        if self.left:
            return self.left.rightmost

        current = self
        while current.parent and current.parent.left is current:
            current = current.parent
        return current.parent


class RedBlackTree(MutableSet[T], Reversible[T]):
    """The red-black tree."""

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

    def _find_node(self, element: T) -> Node[T] | None:
        """Find node with the given element."""
        node = self._root
        while node and node.value != element:
            node = node.left if node.value < element else node.right # type: ignore[operator]

        return node

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
        return self._find_node(element) is not None # type: ignore[arg-type]

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
        return all(element in other for element in self)

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
        return self <= other and other != self

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
        return self <= other and self != other

    @overload
    def __or__(self, other: RedBlackTree[Q], /) -> RedBlackTree[T | Q]: ...

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
        result = RedBlackTree[T | Q]() if isinstance(other, RedBlackTree) else set[T | Q]()

        for element in self:
            result.add(element)

        for element in other: # type: ignore[assignment]
            result.add(element)

        return result

    def __and__(self, other: AbstractSet[object], /) -> RedBlackTree[T]:
        """Return a new set with elements common to the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        RedBlackTree[T]
            Red-black tree.
        """
        result: RedBlackTree[T] = RedBlackTree()

        for element in result:
            if element in other:
                result.add(element)

        return result

    def __sub__(self, other: AbstractSet[object], /) -> RedBlackTree[T]:
        """Return a new set with elements in the set that are not in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        RedBlackTree[T]
            Red-black tree.
        """
        result: RedBlackTree[T] = RedBlackTree()

        for element in self:
            if element not in other:
                result.add(element)

        return result

    @overload
    def __xor__(self, other: RedBlackTree[Q], /) -> RedBlackTree[T | Q]: ...

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
        result = RedBlackTree[T | Q]() if isinstance(other, RedBlackTree) else set[T | Q]()

        for element in self:
            result.add(element)

        for element in other: # type: ignore[assignment]
            if element in self:
                result.discard(element)
            else:
                result.add(element)

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

    def _rotate_left(self, node: Node[T]) -> None:
        """Left rotate around node."""
        if right_child := node.right:
            node.right = right_child.left
            if right_child.left:
                right_child.left.parent = node

            right_child.parent = node.parent

            if not node.parent:
                self._root = right_child
            elif node is node.parent.left:
                node.parent.left = right_child
            else:
                node.parent.right = right_child

            right_child.left = node
            node.parent = right_child


    def _rotate_right(self, node: Node[T]) -> None:
        """Right rotate around node."""
        if left_child := node.left:
            node.left = left_child.right
            if left_child.right:
                left_child.right.parent = node

            left_child.parent = node.parent

            if not node.parent:
                self._root = left_child
            elif node is node.parent.left:
                node.parent.left = left_child
            else:
                node.parent.right = left_child

            left_child.right = node
            node.parent = left_child


    def _fix_insert(self, node: Node[T]) -> None:
        """Fix red-black properties after insertion."""
        if node is None:
            return

        if not node.parent:
            node.color = Color.BLACK
            return

        if node.parent.color == Color.BLACK:
            return

        parent = node.parent
        grandparent = parent.parent
        uncle = node.uncle

        if uncle and uncle.color == Color.RED:
            self._recolor_insert(parent, uncle, grandparent)
            return

        if grandparent:
            self._rotate_insert(parent, node, grandparent)

    def _recolor_insert(self, parent: Node[T], uncle: Node[T], grandparent: Node[T] | None) -> None:
        """Recolor nodes when uncle is red."""
        parent.color = Color.BLACK
        if grandparent:
            grandparent.color = Color.RED
        uncle.color = Color.BLACK
        if grandparent:
            self._fix_insert(grandparent)

    def _rotate_insert(self, parent: Node[T], node: Node[T], grandparent: Node[T]) -> None:
        """Rotate nodes when uncle is black."""
        if parent is grandparent.left:
            if node is parent.right:
                self._rotate_left(parent)
                node, parent = parent, node
            self._rotate_right(grandparent)
        else:
            if node is parent.left:
                self._rotate_right(parent)
                node, parent = parent, node
            self._rotate_left(grandparent)

        parent.color = Color.BLACK
        grandparent.color = Color.RED

    def add(self, element: T, /) -> None:
        """Add ``element`` to the set.

        Parameters
        ----------
        element : T
            Element.
        """
        if not self._root:
            self._root = Node(element, color=Color.BLACK)
            self._size = 1
            return

        current = self._root
        parent = None

        while current:
            parent = current
            if element < current.value: #  type: ignore[operator]
                current = current.left # type: ignore[assignment]
            elif current < element: # type: ignore[operator]
                current = current.right # type: ignore[assignment]
            else:
                return

        if parent is not None:
            new_node = Node(element, color=Color.RED, parent=parent)

            if element < parent.value: # type: ignore[operator]
                parent.left = new_node
            else:
                parent.right = new_node

            self._size += 1
            self._fix_insert(new_node)

    def _remove_node_with_one_or_zero_child(self, node: Node[T]) -> None:
        """Remove node that has one or less children."""
        if child := (node.left if node.left else node.right):
            child.parent = node.parent
            if not node.parent:
                self._root = child
            elif node.parent.left is node:
                node.parent.left = child
            else:
                node.parent.right = child

    def _remove_node_with_two_children(self, node: Node[T]) -> None:
        """Remove node that has two children."""
        successor = node.successor
        if successor is None:
            return

        node.value = successor.value
        self._remove_node_with_one_or_zero_child(successor)


    def remove(self, element: T, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : T
            Element.
        """
        if not (node := self._find_node(element)):
            raise KeyError(element)

        if not node.left or not node.right:
            self._remove_node_with_one_or_zero_child(node)
        else:
            self._remove_node_with_two_children(node)

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

        value = self._root.leftmost.value
        self.remove(value)
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
        """Return the hash (not defined).

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
        if self._root:
            current: Node[T] | None = self._root.leftmost
            while current:
                yield current.value
                current = current.successor

        return

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
        if self._root:
            current: Node[T] | None = self._root.rightmost
            while current:
                yield current.value
                current = current.predecessor

        return
