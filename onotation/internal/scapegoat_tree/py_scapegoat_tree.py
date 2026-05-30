from __future__ import annotations

import math

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class Node(Generic[T]):
    """The scapegoat tree node."""

    value: T
    parent: Node[T] | None = None
    left: Node[T] | None = None
    right: Node[T] | None = None

    @property
    def leftmost(self) -> Node[T]:
        """Return the leftmost node in subtree."""
        node: Node[T] = self
        while node.left:
            node = node.left
        return node

    @property
    def rightmost(self) -> Node[T]:
        """Return the rightmost node in subtree."""
        node: Node[T] = self
        while node.right:
            node = node.right
        return node


class ScapegoatTree(MutableSet[T], Reversible[T]):
    """The scapegoat tree."""

    def __init__(self, iterable: Iterable[T] | None = None, alpha: float = 0.66) -> None:
        """Initialize the tree."""
        if not (0.5 <= alpha < 1.0):
            msg = "Alpha must be in the range [0.5, 1.0)"
            raise ValueError(msg)

        self._root: Node[T] | None = None
        self._size: int = 0
        self._max_size: int = 0
        self._alpha: float = alpha

        if iterable is not None:
            self.update(iterable)

    def __len__(self) -> int:
        """Return the number of elements in the tree."""
        return self._size

    def __contains__(self, element: object) -> bool:
        """Check whether element exists in the tree."""
        return self._find_node(element) is not None

    def _find_node(self, element: object) -> Node[T] | None:
        """Find node by value safely handling incompatible types."""
        node = self._root
        while node is not None:
            try:
                if element == node.value:
                    return node
                node = node.left if element < node.value else node.right  # type: ignore[operator]
            except TypeError:
                return None
        return None

    def _subtree_size(self, node: Node[T] | None) -> int:
        """Calculate the size of the subtree recursively."""
        if node is None:
            return 0
        return self._subtree_size(node.left) + self._subtree_size(node.right) + 1

    def _is_alpha_weight_balanced(self, node: Node[T]) -> bool:
        """Check if a node satisfies the alpha-weight-balance property."""
        left_size = self._subtree_size(node.left)
        right_size = self._subtree_size(node.right)
        total_size = left_size + right_size + 1
        limit = self._alpha * total_size
        return left_size <= limit and right_size <= limit

    def _find_scapegoat(self, new_node: Node[T]) -> Node[T] | None:
        """Find the deepest alpha-weight-unbalanced ancestor."""
        scapegoat = new_node.parent
        while scapegoat is not None and self._is_alpha_weight_balanced(scapegoat):
            scapegoat = scapegoat.parent
        return scapegoat

    def _insert_bst(self, element: T) -> tuple[Node[T] | None, int]:
        """Insert element into BST and return the new node along with its depth."""
        node = self._root
        depth = 0

        while node is not None:
            if element == node.value:
                return None, 0
            if element < node.value:  # type: ignore[operator]
                if node.left is None:
                    new_node = Node(element, parent=node)
                    node.left = new_node
                    return new_node, depth + 1
                node = node.left
            else:
                if node.right is None:
                    new_node = Node(element, parent=node)
                    node.right = new_node
                    return new_node, depth + 1
                node = node.right
            depth += 1

        return None, 0

    def add(self, element: T) -> None:
        """Add an element to the tree."""
        if self._root is not None:
            try:
                _ = element < self._root.value  # type: ignore[operator]
            except TypeError as err:
                msg = "Incompatible element type"
                raise TypeError(msg) from err

        if self._root is None:
            self._root = Node(element)
            self._size = 1
            self._max_size = 1
            return

        new_node, depth = self._insert_bst(element)
        if new_node is None:
            return

        self._size += 1
        self._max_size = max(self._max_size, self._size)

        h_limit = math.floor(math.log(self._size, 1 / self._alpha)) if self._size > 0 else 0
        if depth > h_limit:
            scapegoat = self._find_scapegoat(new_node)
            if scapegoat is not None:
                self._rebuild(scapegoat)

    def discard(self, element: T) -> None:
        """Remove an element from the tree if it exists."""
        if self._root is not None:
            try:
                _ = element < self._root.value  # type: ignore[operator]
            except TypeError as err:
                msg = "Incompatible element type"
                raise TypeError(msg) from err

        node = self._find_node(element)
        if node is None:
            return

        if node.left is not None and node.right is not None:
            successor = node.right.leftmost
            node.value = successor.value
            node = successor

        child = node.left if node.left is not None else node.right
        if child is not None:
            child.parent = node.parent

        if node.parent is None:
            self._root = child
        elif node == node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child

        self._size -= 1

        if self._size < self._alpha * self._max_size:
            if self._root is not None:
                self._rebuild(self._root)
            self._max_size = self._size

    def remove(self, element: T) -> None:
        """Remove an element from the tree or raise KeyError."""
        if self._root is not None:
            try:
                _ = element < self._root.value  # type: ignore[operator]
            except TypeError as err:
                msg = "Incompatible element type"
                raise TypeError(msg) from err

        if element not in self:
            raise KeyError(element)
        self.discard(element)

    def _rebuild(self, scapegoat: Node[T]) -> None:
        """Rebuild the subtree under the scapegoat node to be perfectly balanced."""
        parent = scapegoat.parent
        nodes: list[Node[T]] = []

        def inorder(n: Node[T] | None) -> None:
            if n is None:
                return
            inorder(n.left)
            nodes.append(n)
            inorder(n.right)

        inorder(scapegoat)

        def build_balanced(low: int, high: int, p: Node[T] | None) -> Node[T] | None:
            if low > high:
                return None
            mid = (low + high) // 2
            mid_node = nodes[mid]
            mid_node.parent = p
            mid_node.left = build_balanced(low, mid - 1, mid_node)
            mid_node.right = build_balanced(mid + 1, high, mid_node)
            return mid_node

        new_subtree = build_balanced(0, len(nodes) - 1, parent)

        if parent is None:
            self._root = new_subtree
        elif scapegoat == parent.left:
            parent.left = new_subtree
        else:
            parent.right = new_subtree

    def clear(self) -> None:
        """Clear the tree."""
        self._root = None
        self._size = 0
        self._max_size = 0

    def __iter__(self) -> Iterator[T]:
        """Return an inorder iterator over the elements."""
        if self._root is None:
            return

        stack: list[Node[T]] = []
        node: Node[T] | None = self._root

        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                yield node.value
                node = node.right

    def __reversed__(self) -> Iterator[T]:
        """Return a reverse inorder iterator over the elements."""
        if self._root is None:
            return

        stack: list[Node[T]] = []
        node: Node[T] | None = self._root

        while stack or node:
            if node:
                stack.append(node)
                node = node.right
            else:
                node = stack.pop()
                yield node.value
                node = node.left

    def update(self, iterable: Iterable[T]) -> None:
        """Update the tree with elements from an iterable."""
        for element in iterable:
            self.add(element)

    def __repr__(self) -> str:
        """Return the string representation of the tree."""
        elements = ", ".join(repr(x) for x in self)
        return f"{self.__class__.__name__}([{elements}])"
