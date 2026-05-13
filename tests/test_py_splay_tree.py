"""Tests for SplayTree implementation."""

from __future__ import annotations

import pytest

from onotation.internal.splay_tree import SplayTree


class TestSplayTreeInit:
    """Tests for initialization."""

    def test__init__empty(self) -> None:
        """Empty initialization."""
        tree: SplayTree[int] = SplayTree()

        assert len(tree) == 0
        assert list(tree) == []

    def test__init__with_values(self) -> None:
        """Initialization with iterable."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        assert 1 in tree
        assert 2 in tree
        assert 3 in tree

    def test__init__duplicates(self) -> None:
        """Duplicates are ignored."""
        tree: SplayTree[int] = SplayTree([1, 1, 2, 2])

        assert len(tree) == 2
        assert list(tree) == [1, 2]


class TestSplayTreeAdd:
    """Tests for add."""

    def test__add_single(self) -> None:
        """Add single element."""
        tree: SplayTree[int] = SplayTree()

        tree.add(10)

        assert 10 in tree
        assert len(tree) == 1

    def test__add_multiple(self) -> None:
        """Add multiple elements."""
        tree: SplayTree[int] = SplayTree()

        tree.add(3)
        tree.add(1)
        tree.add(2)

        assert list(tree) == [1, 2, 3]

    def test__add_duplicate(self) -> None:
        """Adding duplicate changes nothing."""
        tree: SplayTree[int] = SplayTree([1, 2])

        tree.add(1)

        assert len(tree) == 2
        assert list(tree) == [1, 2]


class TestSplayTreeRemove:
    """Tests for remove."""

    def test__remove_existing(self) -> None:
        """Remove existing element."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        tree.remove(2)

        assert 2 not in tree
        assert list(tree) == [1, 3]

    def test__remove_missing(self) -> None:
        """Removing missing element raises KeyError."""
        tree: SplayTree[int] = SplayTree([1])

        with pytest.raises(KeyError):
            tree.remove(999)

    def test__remove_empty(self) -> None:
        """Remove from empty tree."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.remove(1)


class TestSplayTreeDiscard:
    """Tests for discard."""

    def test__discard_existing(self) -> None:
        """Discard existing element."""
        tree: SplayTree[int] = SplayTree([1, 2])

        tree.discard(1)

        assert list(tree) == [2]

    def test__discard_missing(self) -> None:
        """Discard missing element is safe."""
        tree: SplayTree[int] = SplayTree([1])

        tree.discard(999)

        assert list(tree) == [1]


class TestSplayTreePop:
    """Tests for pop."""

    def test__pop(self) -> None:
        """Pop minimum element."""
        tree: SplayTree[int] = SplayTree([20, 10, 30])

        value = tree.pop()

        assert value == 10
        assert list(tree) == [20, 30]

    def test__pop_empty(self) -> None:
        """Pop from empty tree raises KeyError."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.pop()


class TestSplayTreeClear:
    """Tests for clear."""

    def test__clear(self) -> None:
        """Clear removes all elements."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        tree.clear()

        assert len(tree) == 0
        assert list(tree) == []


class TestSplayTreeContains:
    """Tests for __contains__."""

    def test__contains_existing(self) -> None:
        """Existing element."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        assert 2 in tree

    def test__contains_missing(self) -> None:
        """Missing element."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        assert 999 not in tree


class TestSplayTreeFind:
    """Tests for find."""

    def test__find_existing(self) -> None:
        """Find existing element."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        assert tree.find(2) == 2

    def test__find_missing(self) -> None:
        """Find missing element."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        assert tree.find(999) is None


class TestSplayTreeIter:
    """Tests for iteration."""

    def test__iter_empty(self) -> None:
        """Empty iteration."""
        tree: SplayTree[int] = SplayTree()

        assert list(tree) == []

    def test__iter_sorted(self) -> None:
        """Iteration is sorted."""
        tree: SplayTree[int] = SplayTree([5, 1, 3, 2])

        assert list(tree) == [1, 2, 3, 5]


class TestSplayTreeReversed:
    """Tests for reversed iteration."""

    def test__reversed_empty(self) -> None:
        """Empty reversed iteration."""
        tree: SplayTree[int] = SplayTree()

        assert list(reversed(tree)) == []

    def test__reversed_order(self) -> None:
        """Descending iteration."""
        tree: SplayTree[int] = SplayTree([1, 2, 3, 4])

        assert list(reversed(tree)) == [4, 3, 2, 1]


class TestSplayTreeMinimum:
    """Tests for minimum."""

    def test__minimum(self) -> None:
        """Return minimum element."""
        tree: SplayTree[int] = SplayTree([3, 1, 2])

        assert tree.minimum() == 1

    def test__minimum_empty(self) -> None:
        """Minimum on empty tree raises KeyError."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.minimum()


class TestSplayTreeMaximum:
    """Tests for maximum."""

    def test__maximum(self) -> None:
        """Return maximum element."""
        tree: SplayTree[int] = SplayTree([1, 2, 3])

        assert tree.maximum() == 3

    def test__maximum_empty(self) -> None:
        """Maximum on empty tree raises KeyError."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.maximum()


class TestSplayTreeSplit:
    """Tests for split."""

    def test__split(self) -> None:
        """Split tree into two trees."""
        tree: SplayTree[int] = SplayTree([1, 2, 3, 4])

        left, right = tree.split(2)

        assert list(left) == [1, 2]
        assert list(right) == [3, 4]

    def test__split_empty(self) -> None:
        """Split empty tree."""
        tree: SplayTree[int] = SplayTree()

        left, right = tree.split(1)

        assert list(left) == []
        assert list(right) == []


class TestSplayTreeJoin:
    """Tests for join."""

    def test__join(self) -> None:
        """Join two trees."""
        left: SplayTree[int] = SplayTree([1, 2])
        right: SplayTree[int] = SplayTree([3, 4])

        result = SplayTree.join(left, right)

        assert list(result) == [1, 2, 3, 4]

    def test__join_left_empty(self) -> None:
        """Join with empty left tree."""
        left: SplayTree[int] = SplayTree()
        right: SplayTree[int] = SplayTree([1, 2])

        result = SplayTree.join(left, right)

        assert list(result) == [1, 2]

    def test__join_right_empty(self) -> None:
        """Join with empty right tree."""
        left: SplayTree[int] = SplayTree([1, 2])
        right: SplayTree[int] = SplayTree()

        result = SplayTree.join(left, right)

        assert list(result) == [1, 2]


class TestSplayTreeRepr:
    """Tests for repr."""

    def test__repr(self) -> None:
        """Representation format."""
        tree: SplayTree[int] = SplayTree([1, 2])

        assert repr(tree) == "SplayTree([1, 2])"
