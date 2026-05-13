from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from contextlib import suppress
from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    """The splay tree node."""

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

    @property
    def successor(self) -> Node[T] | None:
        """Return in-order successor."""
        if self.right:
            return self.right.leftmost

        current: Node[T] = self
        while current.parent and current.parent.right is current:
            current = current.parent

        return current.parent

    @property
    def predecessor(self) -> Node[T] | None:
        """Return in-order predecessor."""
        if self.left:
            return self.left.rightmost

        current: Node[T] = self
        while current.parent and current.parent.left is current:
            current = current.parent

        return current.parent


class SplayTree(MutableSet[T], Reversible[T]):
    """The splay tree."""

    __slots__ = ("_root", "_size")

    def __init__(self, iterable: Iterable[T] = (), /) -> None:
        """Initialize the tree."""
        self._root: Node[T] | None = None
        self._size = 0

        for element in iterable:
            self.add(element)

    def __len__(self) -> int:
        """Return number of elements."""
        return self._size

    def __contains__(self, element: object, /) -> bool:
        """Check whether element exists."""
        return self.find(element) is not None

    def __iter__(self) -> Iterator[T]:
        """Iterate in ascending order."""
        if not self._root:
            return

        current: Node[T] | None = self._root.leftmost

        while current:
            yield current.value
            current = current.successor

    def __reversed__(self) -> Iterator[T]:
        """Iterate in descending order."""
        if not self._root:
            return

        current: Node[T] | None = self._root.rightmost

        while current:
            yield current.value
            current = current.predecessor

    def clear(self) -> None:
        """Remove all elements."""
        self._root = None
        self._size = 0

    def _rotate_left(self, node: Node[T]) -> None:
        """Rotate subtree left around node."""
        right_child = node.right
        if right_child is None:
            return

        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self._root = right_child
        elif node.parent.left is node:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node: Node[T]) -> None:
        """Rotate subtree right around node."""
        left_child = node.left
        if left_child is None:
            return

        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self._root = left_child
        elif node.parent.left is node:
            node.parent.left = left_child
        else:
            node.parent.right = left_child

        left_child.right = node
        node.parent = left_child

    def _splay(self, node: Node[T]) -> None:
        """Move node to the root."""
        while node.parent:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                if parent.left is node:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)

            elif grandparent.left is parent and parent.left is node:
                self._rotate_right(grandparent)
                self._rotate_right(parent)

            elif grandparent.right is parent and parent.right is node:
                self._rotate_left(grandparent)
                self._rotate_left(parent)

            elif grandparent.left is parent and parent.right is node:
                self._rotate_left(parent)
                self._rotate_right(grandparent)

            else:
                self._rotate_right(parent)
                self._rotate_left(grandparent)

    def _find_node(self, element: object) -> Node[T] | None:
        """Find node by value."""
        node = self._root
        last: Node[T] | None = None

        while node:
            last = node
            if element < node.value:      # type: ignore[operator]
                node = node.left
            elif node.value < element:    # type: ignore[operator]
                node = node.right
            else:
                self._splay(node)
                return node

        if last:
            self._splay(last)

        return None

    def find(self, element: object, /) -> T | None:
        """Find element."""
        node = self._find_node(element)
        return node.value if node is not None else None

    def add(self, element: T, /) -> None:
        """Insert element into tree."""
        if self._root is None:
            self._root = Node(element)
            self._size = 1
            return

        current: Node[T] | None = self._root
        parent: Node[T] | None = None

        while current:
            parent = current

            if element < current.value:      # type: ignore[operator]
                current = current.left
            elif current.value < element:    # type: ignore[operator]
                current = current.right
            else:
                self._splay(current)
                return

        if parent is None:
            msg = "parent should not be None"
            raise RuntimeError(msg)

        new_node = Node(element, parent=parent)

        if element < parent.value:           # type: ignore[operator]
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)
        self._size += 1

    def _replace(self, node: Node[T], child: Node[T] | None) -> None:
        """Replace node with child."""
        if node.parent is None:
            self._root = child
        elif node.parent.left is node:
            node.parent.left = child
        else:
            node.parent.right = child

        if child:
            child.parent = node.parent

    def remove(self, element: T, /) -> None:
        """Remove element from tree."""
        node = self._find_node(element)
        if node is None:
            raise KeyError(element)

        self._splay(node)

        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            left_subtree = node.left
            right_subtree = node.right

            left_subtree.parent = None
            right_subtree.parent = None

            maximum = left_subtree.rightmost
            self._root = left_subtree
            self._splay(maximum)

            maximum.right = right_subtree
            right_subtree.parent = maximum
            self._root = maximum

        self._size -= 1

    def discard(self, element: T, /) -> None:
        """Remove element if exists."""
        with suppress(KeyError):
            self.remove(element)

    def minimum(self) -> T:
        """Return minimum element."""
        if self._root is None:
            msg = "tree is empty"
            raise KeyError(msg)

        node = self._root.leftmost
        self._splay(node)
        return node.value

    def maximum(self) -> T:
        """Return maximum element."""
        if self._root is None:
            msg = "tree is empty"
            raise KeyError(msg)

        node = self._root.rightmost
        self._splay(node)
        return node.value

    def split(self, element: T, /) -> tuple[SplayTree[T], SplayTree[T]]:
        """Split tree into <= element and > element."""
        left_tree = SplayTree[T]()
        right_tree = SplayTree[T]()

        if self._root is None:
            return left_tree, right_tree

        self._find_node(element)

        if self._root is None:
            return left_tree, right_tree

        root = self._root

        if root.value <= element:  # type: ignore[operator]
            left_tree._root = root
            right_tree._root = root.right
            if right_tree._root:
                right_tree._root.parent = None
            root.right = None
        else:
            right_tree._root = root
            left_tree._root = root.left
            if left_tree._root:
                left_tree._root.parent = None
            root.left = None

        left_tree._size = len(left_tree)
        right_tree._size = len(right_tree)

        return left_tree, right_tree

    @classmethod
    def join(
        cls,
        left: SplayTree[T],
        right: SplayTree[T],
    ) -> SplayTree[T]:
        """Join two trees (all elements in left <= all elements in right)."""
        if left._root is None:
            return right
        if right._root is None:
            return left

        maximum = left._root.rightmost
        left._splay(maximum)

        maximum.right = right._root
        if right._root:
            right._root.parent = maximum

        left._size += right._size
        return left

    def pop(self) -> T:
        """Remove and return minimum element."""
        if self._root is None:
            msg = f"pop from empty {self.__class__.__name__}"
            raise KeyError(msg)

        node = self._root.leftmost
        value = node.value
        self.remove(value)
        return value

    def __repr__(self) -> str:
        """Return representation."""
        return f"{self.__class__.__name__}({list(self)!r})"
