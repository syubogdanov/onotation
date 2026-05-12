from __future__ import annotations

import random

from collections.abc import Callable, Iterable, Iterator, MutableSequence, Reversible
from dataclasses import dataclass, field
from typing import Generic, TypeVar, overload


T = TypeVar("T")


@dataclass(slots=True)
class Node(Generic[T]):
    """Node of an implicit Cartesian Tree (Treap)."""

    value: T
    priority: float
    size: int = 1
    left: Node[T] | None = field(default=None)
    right: Node[T] | None = field(default=None)
    parent: Node[T] | None = field(default=None, repr=False)

    def update_size(self) -> None:
        """Recalculate subtree size."""
        self.size = 1 + _get_size(self.left) + _get_size(self.right)


    def _get_size(node: Node[T] | None) -> int:
        """Return size of subtree."""
        return node.size if node is not None else 0


class CartesianTree(MutableSequence[T], Reversible[T], Generic[T]):
    """Implicit Cartesian Tree (Treap) — list with O(log n) split/merge."""

    __slots__ = ("_random", "_root")

    def __init__(
        self,
        iterable: Iterable[T] = (),
        /,
        *,
        random: Callable[[], float] = random.random,
    ) -> None:
        self._root: Node[T] | None = None
        self._random = random
        self.extend(iterable)

    def _build_node(self, value: T) -> Node[T]:
        return Node(value=value, priority=self._random())

    def _update_parent(self, child: Node[T] | None, parent: Node[T] | None) -> None:
        if child is not None:
            child.parent = parent

    def _split(
        self,
        node: Node[T] | None,
        key: int,
    ) -> tuple[Node[T] | None, Node[T] | None]:
        """Split tree into left (≤ key) and right parts."""
        if node is None:
            return None, None

        left_size = _get_size(node.left)

        if key <= left_size:
            left, right = self._split(node.left, key)
            node.left = right
            self._update_parent(right, node)
            node.update_size()
            self._update_parent(left, None)
            return left, node

        left, right = self._split(node.right, key - left_size - 1)
        node.right = left
        self._update_parent(left, node)
        node.update_size()
        self._update_parent(right, None)
        return node, right

    def _merge(
        self,
        left: Node[T] | None,
        right: Node[T] | None,
    ) -> Node[T] | None:
        """Merge two trees maintaining heap order by priority."""
        if left is None or right is None:
            result = left or right
            self._update_parent(result, None)
            return result

        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            self._update_parent(left.right, left)
            left.update_size()
            self._update_parent(left, None)
            return left

        right.left = self._merge(left, right.left)
        self._update_parent(right.left, right)
        right.update_size()
        self._update_parent(right, None)
        return right

    def _get_node_at(self, node: Node[T] | None, index: int) -> Node[T]:
        """Return node at implicit position `index`."""
        while node is not None:
            left_size = _get_size(node.left)
            if index < left_size:
                node = node.left
            elif index > left_size:
                node = node.right
                index -= left_size + 1
            else:
                return node
        raise IndexError

    def __len__(self) -> int:
        """Return number of elements in the tree."""
        return _get_size(self._root)

    @overload
    def __getitem__(self, index: int, /) -> T: ...

    @overload
    def __getitem__(self, index: slice, /) -> CartesianTree[T]: ...

    def __getitem__(self, index: int | slice, /) -> T | CartesianTree[T]:
        """Support both integer indexing and slicing."""
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if step != 1:
                detail = "Only step=1 is supported in slices"
                raise ValueError(detail)

            result: CartesianTree[T] = CartesianTree(random=self._random)
            for i in range(start, stop):
                result.append(self[i])
            return result

        if index < 0:
            index += len(self)

        if not 0 <= index < len(self):
            raise IndexError

        return self._get_node_at(self._root, index).value

    @overload
    def __setitem__(self, index: int, value: T, /) -> None: ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[T], /) -> None: ...

    def __setitem__(self, index: int | slice, value: T | Iterable[T], /) -> None:
        """Set item by index or slice."""
        if isinstance(index, slice):
            if not isinstance(value, Iterable):
                raise TypeError
            items = list(value)
            indices = range(*index.indices(len(self)))
            if len(items) != len(indices):
                detail = "Length mismatch between slice and value"
                raise ValueError(detail)

            for i, v in zip(indices, items, strict=True):
                self[i] = v
            return

        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError

        left, rest = self._split(self._root, index)
        mid, right = self._split(rest, 1)

        if mid is not None:
            mid.value = value  # type: ignore[assignment]

        self._root = self._merge(self._merge(left, mid), right)

    @overload
    def __delitem__(self, index: int, /) -> None: ...

    @overload
    def __delitem__(self, index: slice, /) -> None: ...

    def __delitem__(self, index: int | slice, /) -> None:
        """Delete item by index or slice."""
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if step != 1:
                detail = "Only step=1 is supported in slices"
                raise ValueError(detail)
            for i in range(stop - 1, start - 1, -1):
                del self[i]
            return

        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError

        left, rest = self._split(self._root, index)
        _, right = self._split(rest, 1)
        self._root = self._merge(left, right)

    def insert(self, index: int, value: T, /) -> None:
        """Insert value before index."""
        if index < 0:
            index += len(self) + 1
        if not 0 <= index <= len(self):
            raise IndexError

        node = self._build_node(value)
        left, right = self._split(self._root, index)
        self._root = self._merge(self._merge(left, node), right)

    def append(self, value: T, /) -> None:
        """Append value to the end."""
        self.insert(len(self), value)

    def extend(self, iterable: Iterable[T], /) -> None:
        """Extend tree by appending elements from iterable."""
        for value in iterable:
            self.append(value)

    def pop(self, index: int = -1, /) -> T:
        """Remove and return item at index (default last)."""
        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError

        value = self[index]
        del self[index]
        return value

    def remove(self, value: T, /) -> None:
        """Remove first occurrence of value."""
        for i, v in enumerate(self):
            if v == value:
                del self[i]
                return
        detail = f"{value!r} not in CartesianTree"
        raise ValueError(detail)

    def clear(self) -> None:
        """Remove all items."""
        self._root = None

    def reverse(self) -> None:
        """Reverse the tree in place."""
        values = list(reversed(self))
        self.clear()
        self.extend(values)

    def __iter__(self) -> Iterator[T]:
        """In-order (left-to-right) traversal."""
        node = self._root
        if not node:
            return

        while node.left:
            node = node.left

        while node:
            yield node.value
            if node.right:
                node = node.right
                while node.left:
                    node = node.left
            else:
                while node.parent and node.parent.right is node:
                    node = node.parent
                node = node.parent

    def __reversed__(self) -> Iterator[T]:
        """Reverse (right-to-left) traversal."""
        node = self._root
        if not node:
            return

        while node.right:
            node = node.right

        while node:
            yield node.value
            if node.left:
                node = node.left
                while node.right:
                    node = node.right
            else:
                while node.parent and node.parent.left is node:
                    node = node.parent
                node = node.parent

    def index(self, value: T, start: int = 0, stop: int = -1, /) -> int:
        """Return first index of value."""
        if stop < 0:
            stop = len(self)
        for i in range(max(start, 0), min(stop, len(self))):
            if self[i] == value:
                return i
        detail = f"{value!r} is not in CartesianTree"
        raise ValueError(detail)

    def count(self, value: T, /) -> int:
        """Return number of occurrences of value."""
        return sum(1 for v in self if v == value)

    def __eq__(self, other: object, /) -> bool:
        """Return self == other."""
        if not isinstance(other, CartesianTree):
            return NotImplemented
        return len(self) == len(other) and all(a == b for a, b in zip(self, other, strict=True))

    def __hash__(self) -> int:
        """CartesianTree is mutable and therefore not hashable."""
        detail = "CartesianTree is mutable and not hashable"
        raise TypeError(detail)
