"""Tests for BinarySearchTree implementation."""

import pytest

from onotation.internal.binary_search_tree.py_binary_search_tree import (
    BinarySearchTree,
)


class TestBinarySearchTreeIterator:
    """Test __iter__ functionality."""

    def test__iter__empty(self) -> None:
        """Test __iter__ on empty tree."""
        bst: BinarySearchTree[int] = BinarySearchTree()
        assert list(bst) == []

    def test__iter__single_element(self) -> None:
        """Test __iter__ on tree with one element."""
        bst = BinarySearchTree([5])
        assert list(bst) == [5]

    def test__iter__ascending_order(self) -> None:
        """Test __iter__ returns elements in ascending order."""
        bst = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        assert list(bst) == [1, 3, 4, 5, 6, 7, 8]

    def test__iter__with_duplicates(self) -> None:
        """Test that duplicates are ignored (set behavior)."""
        bst = BinarySearchTree([5, 5, 3, 3, 7, 7])
        assert list(bst) == [3, 5, 7]

    def test__iter__large_dataset(self) -> None:
        """Test __iter__ on larger dataset."""
        bst = BinarySearchTree(range(100))
        assert list(bst) == list(range(100))


class TestBinarySearchTreeReversed:
    """Test __reversed__ functionality."""

    def test__reversed__empty(self) -> None:
        """Test __reversed__ on empty tree."""
        bst: BinarySearchTree[int] = BinarySearchTree()
        assert list(reversed(bst)) == []

    def test__reversed__single_element(self) -> None:
        """Test __reversed__ on tree with one element."""
        bst = BinarySearchTree([5])
        assert list(reversed(bst)) == [5]

    def test__reversed__descending_order(self) -> None:
        """Test __reversed__ returns elements in descending order."""
        bst = BinarySearchTree([5, 3, 7, 1, 4, 6, 8])
        assert list(reversed(bst)) == [8, 7, 6, 5, 4, 3, 1]

    def test__reversed__large_dataset(self) -> None:
        """Test __reversed__ on larger dataset."""
        bst = BinarySearchTree(range(100))
        assert list(reversed(bst)) == list(range(99, -1, -1))


class TestBinarySearchTreeContains:
    """Test __contains__ functionality."""

    def test__contains__existing_element(self) -> None:
        """Test that existing element is found."""
        bst = BinarySearchTree([1, 2, 3])
        assert 2 in bst

    def test__contains__missing_element(self) -> None:
        """Test that missing element is not found."""
        bst = BinarySearchTree([1, 2, 3])
        assert 4 not in bst

    def test__contains__empty_tree(self) -> None:
        """Test __contains__ on empty tree."""
        bst: BinarySearchTree[int] = BinarySearchTree()
        assert 10 not in bst


class TestBinarySearchTreeAdd:
    """Test add method."""

    def test__add__new_element(self) -> None:
        """Test adding new element to tree."""
        bst: BinarySearchTree[int] = BinarySearchTree()
        bst.add(5)
        assert 5 in bst
        assert len(bst) == 1

    def test__add__duplicate_element(self) -> None:
        """Test adding duplicate element does nothing."""
        bst = BinarySearchTree([5])
        bst.add(5)
        assert len(bst) == 1


class TestBinarySearchTreeRemove:
    """Test remove method."""

    def test__remove__existing_element(self) -> None:
        """Test removing existing element."""
        bst = BinarySearchTree([1, 2, 3])
        bst.remove(2)
        assert 2 not in bst
        assert len(bst) == 2

    def test__remove__missing_element(self) -> None:
        """Test removing missing element raises KeyError."""
        bst = BinarySearchTree([1, 2, 3])
        with pytest.raises(KeyError):
            bst.remove(4)

    def test__remove__from_empty_tree(self) -> None:
        """Test removing from empty tree raises KeyError."""
        bst: BinarySearchTree[int] = BinarySearchTree()
        with pytest.raises(KeyError):
            bst.remove(1)


class TestBinarySearchTreePop:
    """Test pop method."""

    def test__pop(self) -> None:
        """Test removing arbitrary element from tree."""
        bst = BinarySearchTree([1, 2, 3])
        result = bst.pop()
        assert result in [1, 2, 3]
        assert len(bst) == 2

    def test__pop__empty(self) -> None:
        """Test pop from empty tree raises KeyError."""
        bst: BinarySearchTree[int] = BinarySearchTree()
        with pytest.raises(KeyError) as exc_info:
            bst.pop()
        assert "pop from an empty BinarySearchTree" in str(exc_info.value)


class TestBinarySearchTreeEq:
    """Test __eq__ method."""

    def test__eq__equal_trees(self) -> None:
        """Test two equal trees are equal."""
        bst1 = BinarySearchTree([1, 2, 3])
        bst2 = BinarySearchTree([1, 2, 3])
        assert bst1 == bst2

    def test__eq__different_trees(self) -> None:
        """Test different trees are not equal."""
        bst1 = BinarySearchTree([1, 2, 3])
        bst2 = BinarySearchTree([1, 2, 4])
        assert bst1 != bst2

    def test__eq__not_tree(self) -> None:
        """Test comparing with non-tree returns False."""
        bst = BinarySearchTree([1, 2, 3])
        assert bst != [1, 2, 3]
        assert bst != "not a tree"

    def test__eq__empty_trees(self) -> None:
        """Test two empty trees are equal."""
        bst1: BinarySearchTree[int] = BinarySearchTree()
        bst2: BinarySearchTree[int] = BinarySearchTree()
        assert bst1 == bst2


class TestBinarySearchTreeLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        """Test length of empty tree."""
        bst: BinarySearchTree[int] = BinarySearchTree()
        assert len(bst) == 0

    def test__len__after_add(self) -> None:
        """Test length after adding elements."""
        bst = BinarySearchTree([1, 2, 3])
        assert len(bst) == 3

    def test__len__after_remove(self) -> None:
        """Test length after removing elements."""
        bst = BinarySearchTree([1, 2, 3])
        bst.remove(2)
        assert len(bst) == 3
