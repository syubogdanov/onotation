# ruff: noqa: D102, PLR2004, SLF001
"""Tests for RedBlackTree implementation."""

import pytest  # type: ignore[import-not-found]

from onotation.internal.red_black_tree.py_red_black_tree import RedBlackTree


class TestRedBlackTreeLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        tree: RedBlackTree[int] = RedBlackTree()
        assert len(tree) == 0

    def test__len__after_add(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        assert len(tree) == 3

    def test__len__after_remove(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        tree.remove(2)
        assert len(tree) == 2


class TestRedBlackTreeContains:
    """Test __contains__ method."""

    def test__contains__existing(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        assert 2 in tree

    def test__contains__missing(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        assert 4 not in tree

    def test__contains__empty(self) -> None:
        tree: RedBlackTree[int] = RedBlackTree()
        assert 1 not in tree


class TestRedBlackTreeAdd:
    """Test add method."""

    def test__add__new(self) -> None:
        tree: RedBlackTree[int] = RedBlackTree()
        tree.add(5)
        assert 5 in tree
        assert len(tree) == 1

    def test__add__duplicate(self) -> None:
        tree = RedBlackTree([5])
        tree.add(5)
        assert len(tree) == 1


class TestRedBlackTreeRemove:
    """Test remove method."""

    def test__remove__existing(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        tree.remove(2)
        assert 2 not in tree
        assert len(tree) == 2

    def test__remove__missing(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        with pytest.raises(KeyError):
            tree.remove(4)

    def test__remove__empty(self) -> None:
        tree: RedBlackTree[int] = RedBlackTree()
        with pytest.raises(KeyError):
            tree.remove(1)


class TestRedBlackTreeDiscard:
    """Test discard method."""

    def test__discard__existing(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        tree.discard(2)
        assert 2 not in tree
        assert len(tree) == 2

    def test__discard__missing(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        tree.discard(99)
        assert len(tree) == 3


class TestRedBlackTreePop:
    """Test pop method."""

    def test__pop(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        result = tree.pop()
        assert result in [1, 2, 3]
        assert len(tree) == 2

    def test__pop__empty(self) -> None:
        tree: RedBlackTree[int] = RedBlackTree()
        with pytest.raises(KeyError):
            tree.pop()


class TestRedBlackTreeClear:
    """Test clear method."""

    def test__clear(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        tree.clear()
        assert len(tree) == 0
        assert list(tree) == []


class TestRedBlackTreeIter:
    """Test __iter__ method."""

    def test__iter__empty(self) -> None:
        tree: RedBlackTree[int] = RedBlackTree()
        assert list(tree) == []

    def test__iter__ascending(self) -> None:
        tree = RedBlackTree([5, 3, 7, 1, 4, 6, 8])
        assert list(tree) == [1, 3, 4, 5, 6, 7, 8]


class TestRedBlackTreeReversed:
    """Test __reversed__ method."""

    def test__reversed__empty(self) -> None:
        tree: RedBlackTree[int] = RedBlackTree()
        assert list(reversed(tree)) == []

    def test__reversed__descending(self) -> None:
        tree = RedBlackTree([1, 2, 3, 4, 5])
        assert list(reversed(tree)) == [5, 4, 3, 2, 1]


class TestRedBlackTreeEq:
    """Test __eq__ method."""

    def test__eq__equal(self) -> None:
        tree1 = RedBlackTree([1, 2, 3])
        tree2 = RedBlackTree([1, 2, 3])
        assert tree1 == tree2

    def test__eq__different(self) -> None:
        tree1 = RedBlackTree([1, 2, 3])
        tree2 = RedBlackTree([1, 2, 4])
        assert tree1 != tree2

    def test__eq__not_tree(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        assert tree != [1, 2, 3]


class TestRedBlackTreeProperties:
    """Test red-black tree properties."""

    def test__root_is_black(self) -> None:
        tree = RedBlackTree([1, 2, 3])
        assert tree._root is not None
        assert not tree._root.red_flg
