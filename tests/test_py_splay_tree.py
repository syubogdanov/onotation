"""Tests for SplayTree implementation."""

from __future__ import annotations

import pytest

from onotation.internal.splay_tree import SplayTree


ZERO = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
TEN = 10
TWENTY = 20
THIRTY = 30
MISSING = 999


class TestSplayTreeInit:
    """Tests for initialization."""

    def test__init__empty(self) -> None:
        """Empty initialization."""
        tree: SplayTree[int] = SplayTree()

        assert len(tree) == ZERO
        assert list(tree) == []

    def test__init__with_values(self) -> None:
        """Initialization with iterable."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        assert ONE in tree
        assert TWO in tree
        assert THREE in tree

    def test__init__duplicates(self) -> None:
        """Duplicates are ignored."""
        tree: SplayTree[int] = SplayTree([ONE, ONE, TWO, TWO])

        assert len(tree) == TWO
        assert list(tree) == [ONE, TWO]


class TestSplayTreeAdd:
    """Tests for add."""

    def test__add_single(self) -> None:
        """Add single element."""
        tree: SplayTree[int] = SplayTree()

        tree.add(TEN)

        assert TEN in tree
        assert len(tree) == ONE

    def test__add_multiple(self) -> None:
        """Add multiple elements."""
        tree: SplayTree[int] = SplayTree()

        tree.add(THREE)
        tree.add(ONE)
        tree.add(TWO)

        assert list(tree) == [ONE, TWO, THREE]

    def test__add_duplicate(self) -> None:
        """Adding duplicate changes nothing."""
        tree: SplayTree[int] = SplayTree([ONE, TWO])

        tree.add(ONE)

        assert len(tree) == TWO
        assert list(tree) == [ONE, TWO]


class TestSplayTreeRemove:
    """Tests for remove."""

    def test__remove_existing(self) -> None:
        """Remove existing element."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        tree.remove(TWO)

        assert TWO not in tree
        assert list(tree) == [ONE, THREE]

    def test__remove_missing(self) -> None:
        """Removing missing element raises KeyError."""
        tree: SplayTree[int] = SplayTree([ONE])

        with pytest.raises(KeyError):
            tree.remove(MISSING)

    def test__remove_empty(self) -> None:
        """Remove from empty tree."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.remove(ONE)


class TestSplayTreeDiscard:
    """Tests for discard."""

    def test__discard_existing(self) -> None:
        """Discard existing element."""
        tree: SplayTree[int] = SplayTree([ONE, TWO])

        tree.discard(ONE)

        assert list(tree) == [TWO]

    def test__discard_missing(self) -> None:
        """Discard missing element is safe."""
        tree: SplayTree[int] = SplayTree([ONE])

        tree.discard(MISSING)

        assert list(tree) == [ONE]


class TestSplayTreePop:
    """Tests for pop."""

    def test__pop(self) -> None:
        """Pop minimum element."""
        tree: SplayTree[int] = SplayTree([TWENTY, TEN, THIRTY])

        value = tree.pop()

        assert value == TEN
        assert list(tree) == [TWENTY, THIRTY]

    def test__pop_empty(self) -> None:
        """Pop from empty tree raises KeyError."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.pop()


class TestSplayTreeClear:
    """Tests for clear."""

    def test__clear(self) -> None:
        """Clear removes all elements."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        tree.clear()

        assert len(tree) == ZERO
        assert list(tree) == []


class TestSplayTreeContains:
    """Tests for __contains__."""

    def test__contains_existing(self) -> None:
        """Existing element."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        assert TWO in tree

    def test__contains_missing(self) -> None:
        """Missing element."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        assert MISSING not in tree


class TestSplayTreeFind:
    """Tests for find."""

    def test__find_existing(self) -> None:
        """Find existing element."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        assert tree.find(TWO) == TWO

    def test__find_missing(self) -> None:
        """Find missing element."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        assert tree.find(MISSING) is None


class TestSplayTreeIter:
    """Tests for iteration."""

    def test__iter_empty(self) -> None:
        """Empty iteration."""
        tree: SplayTree[int] = SplayTree()

        assert list(tree) == []

    def test__iter_sorted(self) -> None:
        """Iteration is sorted."""
        tree: SplayTree[int] = SplayTree([FIVE, ONE, THREE, TWO])

        assert list(tree) == [ONE, TWO, THREE, FIVE]


class TestSplayTreeReversed:
    """Tests for reversed iteration."""

    def test__reversed_empty(self) -> None:
        """Empty reversed iteration."""
        tree: SplayTree[int] = SplayTree()

        assert list(reversed(tree)) == []

    def test__reversed_order(self) -> None:
        """Descending iteration."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE, FOUR])

        assert list(reversed(tree)) == [FOUR, THREE, TWO, ONE]


class TestSplayTreeMinimum:
    """Tests for minimum."""

    def test__minimum(self) -> None:
        """Return minimum element."""
        tree: SplayTree[int] = SplayTree([THREE, ONE, TWO])

        assert tree.minimum() == ONE

    def test__minimum_empty(self) -> None:
        """Minimum on empty tree raises KeyError."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.minimum()


class TestSplayTreeMaximum:
    """Tests for maximum."""

    def test__maximum(self) -> None:
        """Return maximum element."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE])

        assert tree.maximum() == THREE

    def test__maximum_empty(self) -> None:
        """Maximum on empty tree raises KeyError."""
        tree: SplayTree[int] = SplayTree()

        with pytest.raises(KeyError):
            tree.maximum()


class TestSplayTreeSplit:
    """Tests for split."""

    def test__split(self) -> None:
        """Split tree into two trees."""
        tree: SplayTree[int] = SplayTree([ONE, TWO, THREE, FOUR])

        left, right = tree.split(TWO)

        assert list(left) == [ONE, TWO]
        assert list(right) == [THREE, FOUR]

    def test__split_empty(self) -> None:
        """Split empty tree."""
        tree: SplayTree[int] = SplayTree()

        left, right = tree.split(ONE)

        assert list(left) == []
        assert list(right) == []


class TestSplayTreeJoin:
    """Tests for join."""

    def test__join(self) -> None:
        """Join two trees."""
        left: SplayTree[int] = SplayTree([ONE, TWO])
        right: SplayTree[int] = SplayTree([THREE, FOUR])

        result = SplayTree.join(left, right)

        assert list(result) == [ONE, TWO, THREE, FOUR]

    def test__join_left_empty(self) -> None:
        """Join with empty left tree."""
        left: SplayTree[int] = SplayTree()
        right: SplayTree[int] = SplayTree([ONE, TWO])

        result = SplayTree.join(left, right)

        assert list(result) == [ONE, TWO]

    def test__join_right_empty(self) -> None:
        """Join with empty right tree."""
        left: SplayTree[int] = SplayTree([ONE, TWO])
        right: SplayTree[int] = SplayTree()

        result = SplayTree.join(left, right)

        assert list(result) == [ONE, TWO]


class TestSplayTreeRepr:
    """Tests for repr."""

    def test__repr(self) -> None:
        """Representation format."""
        tree: SplayTree[int] = SplayTree([ONE, TWO])

        assert repr(tree) == "SplayTree([1, 2])"
