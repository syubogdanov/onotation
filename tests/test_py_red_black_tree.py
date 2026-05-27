import pytest

from onotation.internal.red_black_tree.py_red_black_tree import RedBlackTree


class TestRedBlackTreeLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        """Test empty tree."""
        tree: RedBlackTree[int] = RedBlackTree()
        assert len(tree) == 0

    def test__len__after_add(self) -> None:
        """Test length after adding elements."""
        tree = RedBlackTree([1, 2, 3])
        assert len(tree) == 3

    def test__len__after_remove(self) -> None:
        """Test length after removing elements."""
        tree = RedBlackTree([1, 2, 3])
        tree.remove(2)
        assert len(tree) == 2


class TestRedBlackTreeContains:
    """Test __contains__ method."""

    def test__contains(self) -> None:
        """Test element membership."""
        tree = RedBlackTree([1, 2, 3])
        assert 2 in tree
        assert 4 not in tree

    def test__contains__empty(self) -> None:
        """Test contains on empty tree."""
        tree: RedBlackTree[int] = RedBlackTree()
        assert 1 not in tree


class TestRedBlackTreeAdd:
    """Test add method."""

    def test__add(self) -> None:
        """Test adding elements."""
        tree: RedBlackTree[int] = RedBlackTree()
        tree.add(5)
        assert 5 in tree
        assert len(tree) == 1

    def test__add__duplicate(self) -> None:
        """Test adding duplicate element."""
        tree = RedBlackTree([5])
        tree.add(5)
        assert len(tree) == 1


class TestRedBlackTreeRemove:
    """Test remove method."""

    def test__remove(self) -> None:
        """Test removing existing element."""
        tree = RedBlackTree([1, 2, 3])
        tree.remove(2)
        assert 2 not in tree
        assert len(tree) == 2

    def test__remove__missing(self) -> None:
        """Test removing missing element raises KeyError."""
        tree = RedBlackTree([1, 2, 3])
        with pytest.raises(KeyError):
            tree.remove(4)

    def test__remove__empty(self) -> None:
        """Test removing from empty tree."""
        tree: RedBlackTree[int] = RedBlackTree()
        with pytest.raises(KeyError):
            tree.remove(1)


class TestRedBlackTreeDiscard:
    """Test discard method."""

    def test__discard(self) -> None:
        """Test discarding existing element."""
        tree = RedBlackTree([1, 2, 3])
        tree.discard(2)
        assert 2 not in tree
        assert len(tree) == 2

    def test__discard__missing(self) -> None:
        """Test discarding missing element does nothing."""
        tree = RedBlackTree([1, 2, 3])
        tree.discard(99)
        assert len(tree) == 3


class TestRedBlackTreePop:
    """Test pop method."""

    def test__pop(self) -> None:
        """Test popping arbitrary element."""
        tree = RedBlackTree([1, 2, 3])
        result = tree.pop()
        assert result in [1, 2, 3]
        assert len(tree) == 2

    def test__pop__empty(self) -> None:
        """Test popping from empty tree raises KeyError."""
        tree: RedBlackTree[int] = RedBlackTree()
        with pytest.raises(KeyError):
            tree.pop()


class TestRedBlackTreeClear:
    """Test clear method."""

    def test__clear(self) -> None:
        """Test clearing tree."""
        tree = RedBlackTree([1, 2, 3])
        tree.clear()
        assert len(tree) == 0
        assert list(tree) == []


class TestRedBlackTreeIter:
    """Test __iter__ method."""

    def test__iter__empty(self) -> None:
        """Test iteration over empty tree."""
        tree: RedBlackTree[int] = RedBlackTree()
        assert list(tree) == []

    def test__iter(self) -> None:
        """Test iteration order."""
        tree = RedBlackTree([5, 3, 7, 1, 4, 6, 8])
        assert list(tree) == [1, 3, 4, 5, 6, 7, 8]


class TestRedBlackTreeReversed:
    """Test __reversed__ method."""

    def test__reversed__empty(self) -> None:
        """Test reverse iteration over empty tree."""
        tree: RedBlackTree[int] = RedBlackTree()
        assert list(reversed(tree)) == []

    def test__reversed(self) -> None:
        """Test reverse iteration order."""
        tree = RedBlackTree([1, 2, 3, 4, 5])
        assert list(reversed(tree)) == [5, 4, 3, 2, 1]


class TestRedBlackTreeEq:
    """Test __eq__ method."""

    def test__eq(self) -> None:
        """Test equality of trees."""
        tree1 = RedBlackTree([1, 2, 3])
        tree2 = RedBlackTree([1, 2, 3])
        assert tree1 == tree2

    def test__eq__different(self) -> None:
        """Test inequality of different trees."""
        tree1 = RedBlackTree([1, 2, 3])
        tree2 = RedBlackTree([1, 2, 4])
        assert tree1 != tree2

    def test__eq__not_tree(self) -> None:
        """Test comparison with non-tree returns False."""
        tree = RedBlackTree([1, 2, 3])
        assert tree != [1, 2, 3]
