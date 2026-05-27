from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from contextlib import suppress
from dataclasses import dataclass
from typing import Generic, Self, TypeVar, overload


T = TypeVar("T")
Q = TypeVar("Q")


@dataclass(slots=True)
class Node(Generic[T]):
    """AVL tree node."""

    value: T
    height: int = 1
    parent: Node[T] | None = None
    right: Node[T] | None = None
    left: Node[T] | None = None

    @property
    def leftmost(self) -> Node[T]:
        """Return the leftmost node in the sbubtree."""
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
        """Return in-order successor of a node."""
        if self.right:
            return self.right.leftmost

        current = self
        while current.parent and current.parent.right is current:
            current = current.parent

        return current.parent

    @property
    def predecessor(self) -> Node[T] | None:
        """Return in-order predecessor of a node."""
        if self.left:
            return self.left.rightmost

        current = self
        while current.parent and current.parent.left is current:
            current = current.parent

        return current.parent


class AVLTree(MutableSet[T], Reversible[T]):
    """The AVL tree."""

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
            node = node.left if element < node.value else node.right  # type: ignore[operator]

        return node

    def _get_height(self, node: Node[T] | None) -> int:
        """Return height of the subtree."""
        return node.height if node else 0

    def _update_height(self, node: Node[T]) -> None:
        """Update subtree height of the given node."""
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _get_balance(self, node: Node[T]) -> int:
        """Return balance factor of the node (left height - right height)."""
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, y: Node[T]) -> Node[T]:
        """Make right turn."""
        x = y.left
        if x is None:
            return y

        y.left = x.right
        if x.right:
            x.right.parent = y

        x.right = y
        x.parent = y.parent
        y.parent = x

        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: Node[T]) -> Node[T]:
        """Make left turn."""
        y = x.right
        if y is None:
            return x

        x.right = y.left
        if y.left:
            y.left.parent = x

        y.left = x
        y.parent = x.parent
        x.parent = y

        self._update_height(x)
        self._update_height(y)
        return y

    def _balance(self, node: Node[T]) -> Node[T]:
        """Balance the node and return new root.

        Performs rotations if balance factor is outside [-1, 1].
        """
        self._update_height(node)
        balance = self._get_balance(node)

        if balance > 1:
            if node.left and self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
                if node.left:
                    node.left.parent = node
            return self._rotate_right(node)

        if balance < -1:
            if node.right and self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
                if node.right:
                    node.right.parent = node
            return self._rotate_left(node)

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
        node = self._find_node(element)  # type: ignore[arg-type]
        return node is not None

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
    def __or__(self, other: AVLTree[Q], /) -> AVLTree[T | Q]: ...

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
        result = AVLTree[T | Q]() if isinstance(other, AVLTree) else set[T | Q]()
        for element in self:
            result.add(element)

        for element in other:  # type: ignore[assignment]
            result.add(element)

        return result

    def __and__(self, other: AbstractSet[object], /) -> AVLTree[T]:
        """Return a new set with elements common to the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        AVLTree[T]
            AVL tree.
        """
        result: AVLTree[T] = AVLTree()
        for element in self:
            if element in other:
                result.add(element)

        return result

    def __sub__(self, other: AbstractSet[object], /) -> AVLTree[T]:
        """Return a new set with elements in the set that are not in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        AVLTree[T]
            AVL tree.
        """
        result: AVLTree[T] = AVLTree()
        for element in self:
            if element not in other:
                result.add(element)

        return result

    @overload
    def __xor__(self, other: AVLTree[Q], /) -> AVLTree[T | Q]: ...

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
        result = AVLTree[T | Q]() if isinstance(other, AVLTree) else set[T | Q]()

        for element in self:
            result.add(element)

        for element in other:  # type: ignore[assignment]
            if element in result:
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
        to_remove = [element for element in self if element not in other]
        to_add = [element for element in other if element not in self]
        for element in to_remove:
            self.discard(element)

        for element in to_add:
            self.add(element)

        return self

    def _add(self, node: Node[T] | None, value: T, parent: Node[T] | None = None) -> Node[T]:
        """Recursive add with balancing."""
        if node is None:
            self._size += 1
            return Node(value, parent=parent)

        if value < node.value:  # type: ignore[operator]
            node.left = self._add(node.left, value, node)
        elif node.value < value:  # type: ignore[operator]
            node.right = self._add(node.right, value, node)
        else:
            return node

        node.parent = parent
        return self._balance(node)

    def _remove_node(self, node: Node[T]) -> Node[T] | None:
        """Remove node and return child to replace it."""
        if node.left is None:
            child = node.right
            if child:
                child.parent = node.parent
            self._size -= 1
            return child
        if node.right is None:
            child = node.left
            if child:
                child.parent = node.parent
            self._size -= 1
            return child
        successor = node.right.leftmost
        node.value = successor.value
        node.right = self._remove(node.right, successor.value)
        if node.right:
            node.right.parent = node
        return node

    def _remove(self, node: Node[T] | None, value: T) -> Node[T] | None:
        """Recursive remove with balancing."""
        if node is None:
            raise KeyError

        if value < node.value:  # type: ignore[operator]
            node.left = self._remove(node.left, value)
            if node.left:
                node.left.parent = node
        elif node.value < value:  # type: ignore[operator]
            node.right = self._remove(node.right, value)
            if node.right:
                node.right.parent = node
        else:
            return self._remove_node(node)

        node.parent = node.parent
        return self._balance(node)

    def add(self, element: T, /) -> None:
        """Add ``element`` to the set.

        Parameters
        ----------
        element : T
            Element.
        """
        self._root = self._add(self._root, element)

    def remove(self, element: T, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : T
            Element.
        """
        self._root = self._remove(self._root, element)

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
            return NotImplemented

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
        if self._root:
            current = self._root.leftmost
            while current:
                yield current.value
                current = current.successor  # type: ignore[assignment]

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
            current = self._root.rightmost
            while current:
                yield current.value
                current = current.predecessor  # type: ignore[assignment]
