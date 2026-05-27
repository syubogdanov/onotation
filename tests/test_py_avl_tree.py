import pytest

from onotation.internal.avl_tree.py_avl_tree import AVLTree


class TestAVLTreeLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        """Test empty tree."""
        tree: AVLTree[int] = AVLTree()
        assert len(tree) == 0

    def test__len__after_add(self) -> None:
        """Test length after adding elements."""
        tree = AVLTree([1, 2, 3])
        assert len(tree) == 3

    def test__len__after_remove(self) -> None:
        """Test length after removing elements."""
        tree = AVLTree([1, 2, 3])
        tree.remove(2)
        assert len(tree) == 2


class TestAVLTreeContains:
    """Test __contains__ method."""

    def test__contains(self) -> None:
        """Test element membership."""
        tree = AVLTree([1, 2, 3])
        assert 2 in tree
        assert 4 not in tree

    def test__contains__empty(self) -> None:
        """Test contains on empty tree."""
        tree: AVLTree[int] = AVLTree()
        assert 1 not in tree


class TestAVLTreeAdd:
    """Test add method."""

    def test__add(self) -> None:
        """Test adding elements."""
        tree: AVLTree[int] = AVLTree()
        tree.add(5)
        assert 5 in tree
        assert len(tree) == 1

    def test__add__duplicate(self) -> None:
        """Test adding duplicate element."""
        tree = AVLTree([5])
        tree.add(5)
        assert len(tree) == 1


class TestAVLTreeRemove:
    """Test remove method."""

    def test__remove(self) -> None:
        """Test removing existing element."""
        tree = AVLTree([1, 2, 3])
        tree.remove(2)
        assert 2 not in tree
        assert len(tree) == 2

    def test__remove__missing(self) -> None:
        """Test removing missing element raises KeyError."""
        tree = AVLTree([1, 2, 3])
        with pytest.raises(KeyError):
            tree.remove(4)

    def test__remove__empty(self) -> None:
        """Test removing from empty tree."""
        tree: AVLTree[int] = AVLTree()
        with pytest.raises(KeyError):
            tree.remove(1)


class TestAVLTreeDiscard:
    """Test discard method."""

    def test__discard(self) -> None:
        """Test discarding existing element."""
        tree = AVLTree([1, 2, 3])
        tree.discard(2)
        assert 2 not in tree
        assert len(tree) == 2

    def test__discard__missing(self) -> None:
        """Test discarding missing element does nothing."""
        tree = AVLTree([1, 2, 3])
        tree.discard(99)
        assert len(tree) == 3


class TestAVLTreePop:
    """Test pop method."""

    def test__pop(self) -> None:
        """Test popping arbitrary element."""
        tree = AVLTree([1, 2, 3])
        result = tree.pop()
        assert result in [1, 2, 3]
        assert len(tree) == 2

    def test__pop__empty(self) -> None:
        """Test popping from empty tree raises KeyError."""
        tree: AVLTree[int] = AVLTree()
        with pytest.raises(KeyError):
            tree.pop()


class TestAVLTreeClear:
    """Test clear method."""

    def test__clear(self) -> None:
        """Test clearing tree."""
        tree = AVLTree([1, 2, 3])
        tree.clear()
        assert len(tree) == 0
        assert list(tree) == []


class TestAVLTreeIter:
    """Test __iter__ method."""

    def test__iter__empty(self) -> None:
        """Test iteration over empty tree."""
        tree: AVLTree[int] = AVLTree()
        assert list(tree) == []

    def test__iter(self) -> None:
        """Test iteration order."""
        tree = AVLTree([5, 3, 7, 1, 4, 6, 8])
        assert list(tree) == [1, 3, 4, 5, 6, 7, 8]


class TestAVLTreeReversed:
    """Test __reversed__ method."""

    def test__reversed__empty(self) -> None:
        """Test reverse iteration over empty tree."""
        tree: AVLTree[int] = AVLTree()
        assert list(reversed(tree)) == []

    def test__reversed(self) -> None:
        """Test reverse iteration order."""
        tree = AVLTree([1, 2, 3, 4, 5])
        assert list(reversed(tree)) == [5, 4, 3, 2, 1]


class TestAVLTreeEq:
    """Test __eq__ method."""

    def test__eq(self) -> None:
        """Test equality of trees."""
        tree1 = AVLTree([1, 2, 3])
        tree2 = AVLTree([1, 2, 3])
        assert tree1 == tree2

    def test__eq__different(self) -> None:
        """Test inequality of different trees."""
        tree1 = AVLTree([1, 2, 3])
        tree2 = AVLTree([1, 2, 4])
        assert tree1 != tree2

    def test__eq__not_tree(self) -> None:
        """Test comparison with non-tree returns NotImplemented."""
        tree = AVLTree([1, 2, 3])
        assert tree != [1, 2, 3]


class TestAVLTreeBalance:
    """Test AVL tree balance property."""

    def test__balance_after_add(self) -> None:
        """Test tree remains balanced after adding elements."""
        tree = AVLTree([5, 3, 7, 1, 4, 6, 8, 0, 2, 9])
        assert list(tree) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert len(tree) == 10

    def test__balance_after_remove(self) -> None:
        """Test tree remains balanced after removing elements."""
        tree = AVLTree([5, 3, 7, 1, 4, 6, 8])
        tree.remove(7)
        assert list(tree) == [1, 3, 4, 5, 6, 8]
        tree.remove(3)
        assert list(tree) == [1, 4, 5, 6, 8]
