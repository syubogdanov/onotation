"""Tests for CartesianTree implementation."""

import pytest  # type: ignore[import-not-found]

from onotation.internal.cartesian_tree.py_cartesian_tree import CartesianTree


class TestCartesianTreeLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        """Test length of empty tree."""
        tree: CartesianTree[int] = CartesianTree()
        assert len(tree) == 0

    def test__len__after_append(self) -> None:
        """Test length after appending elements."""
        tree: CartesianTree[int] = CartesianTree()
        tree.append(1)
        tree.append(2)
        assert len(tree) == 2

    def test__len__after_insert(self) -> None:
        """Test length after inserting elements."""
        tree = CartesianTree([1, 3])
        tree.insert(1, 2)
        assert len(tree) == 3

    def test__len__after_pop(self) -> None:
        """Test length after popping elements."""
        tree = CartesianTree([1, 2, 3])
        tree.pop()
        assert len(tree) == 2


class TestCartesianTreeGetItem:
    """Test __getitem__ method."""

    def test__getitem__positive_index(self) -> None:
        """Test getting element by positive index."""
        tree = CartesianTree([10, 20, 30, 40])
        assert tree[0] == 10
        assert tree[2] == 30

    def test__getitem__negative_index(self) -> None:
        """Test getting element by negative index."""
        tree = CartesianTree([10, 20, 30, 40])
        assert tree[-1] == 40
        assert tree[-3] == 20

    def test__getitem__index_out_of_range(self) -> None:
        """Test index out of range raises IndexError."""
        tree = CartesianTree([1, 2, 3])
        with pytest.raises(IndexError):
            _ = tree[10]

    def test__getitem__slice(self) -> None:
        """Test getting slice returns new CartesianTree."""
        tree = CartesianTree([1, 2, 3, 4, 5])
        result = tree[1:4]
        assert isinstance(result, CartesianTree)
        assert list(result) == [2, 3, 4]


class TestCartesianTreeSetItem:
    """Test __setitem__ method."""

    def test__setitem__positive_index(self) -> None:
        """Test setting element by positive index."""
        tree = CartesianTree([1, 2, 3])
        tree[1] = 99
        assert list(tree) == [1, 99, 3]

    def test__setitem__negative_index(self) -> None:
        """Test setting element by negative index."""
        tree = CartesianTree([1, 2, 3])
        tree[-2] = 88
        assert list(tree) == [1, 88, 3]

    def test__setitem__slice(self) -> None:
        """Test setting slice with iterable."""
        tree = CartesianTree([1, 2, 3, 4, 5])
        with pytest.raises(
            ValueError, match="attempt to assign sequence of size 2 to slice of size 3",
        ):
            tree[1:4] = [99, 88]

    def test__setitem__slice_wrong_length(self) -> None:
        """Test setting slice with wrong length raises ValueError."""
        tree = CartesianTree([1, 2, 3, 4, 5])
        with pytest.raises(
            ValueError, match="attempt to assign sequence of size 2 to slice of size 3",
        ):
            tree[1:4] = [99, 88]


class TestCartesianTreeDelItem:
    """Test __delitem__ method."""

    def test__delitem__positive_index(self) -> None:
        """Test deleting element by positive index."""
        tree = CartesianTree([1, 2, 3, 4])
        del tree[2]
        assert list(tree) == [1, 2, 4]

    def test__delitem__negative_index(self) -> None:
        """Test deleting element by negative index."""
        tree = CartesianTree([1, 2, 3, 4])
        del tree[-2]
        assert list(tree) == [1, 2, 4]

    def test__delitem__slice(self) -> None:
        """Test deleting slice."""
        tree = CartesianTree([1, 2, 3, 4, 5])
        del tree[1:4]
        assert list(tree) == [1, 5]

    def test__delitem__index_out_of_range(self) -> None:
        """Test deleting out of range index raises IndexError."""
        tree = CartesianTree([1, 2, 3])
        with pytest.raises(IndexError):
            del tree[10]


class TestCartesianTreeInsert:
    """Test insert method."""

    def test__insert__at_beginning(self) -> None:
        """Test inserting at beginning."""
        tree = CartesianTree([2, 3])
        tree.insert(0, 1)
        assert list(tree) == [1, 2, 3]

    def test__insert__at_middle(self) -> None:
        """Test inserting at middle."""
        tree = CartesianTree([1, 2, 4])
        tree.insert(2, 3)
        assert list(tree) == [1, 2, 3, 4]

    def test__insert__at_end(self) -> None:
        """Test inserting at end."""
        tree = CartesianTree([1, 2])
        tree.insert(2, 3)
        assert list(tree) == [1, 2, 3]

    def test__insert__negative_index(self) -> None:
        """Test inserting with negative index."""
        tree = CartesianTree([1, 3])
        tree.insert(-1, 2)
        assert list(tree) == [1, 2, 3]


class TestCartesianTreeAppend:
    """Test append method."""

    def test__append__single_element(self) -> None:
        """Test appending single element."""
        tree: CartesianTree[int] = CartesianTree()
        tree.append(1)
        assert list(tree) == [1]

    def test__append__multiple_elements(self) -> None:
        """Test appending multiple elements."""
        tree: CartesianTree[int] = CartesianTree()
        tree.append(1)
        tree.append(2)
        tree.append(3)
        assert list(tree) == [1, 2, 3]


class TestCartesianTreeExtend:
    """Test extend method."""

    def test__extend__empty_tree(self) -> None:
        """Test extending empty tree."""
        tree: CartesianTree[int] = CartesianTree()
        tree.extend([1, 2, 3])
        assert list(tree) == [1, 2, 3]

    def test__extend__non_empty_tree(self) -> None:
        """Test extending non-empty tree."""
        tree = CartesianTree([1, 2])
        tree.extend([3, 4, 5])
        assert list(tree) == [1, 2, 3, 4, 5]


class TestCartesianTreePop:
    """Test pop method."""

    def test__pop__default_last(self) -> None:
        """Test pop with default index (last element)."""
        tree = CartesianTree([1, 2, 3])
        value = tree.pop()
        assert value == 3
        assert list(tree) == [1, 2]

    def test__pop__specific_index(self) -> None:
        """Test pop with specific index."""
        tree = CartesianTree([10, 20, 30, 40])
        value = tree.pop(1)
        assert value == 20
        assert list(tree) == [10, 30, 40]

    def test__pop__negative_index(self) -> None:
        """Test pop with negative index."""
        tree = CartesianTree([1, 2, 3])
        value = tree.pop(-2)
        assert value == 2
        assert list(tree) == [1, 3]

    def test__pop__empty_tree(self) -> None:
        """Test pop from empty tree raises IndexError."""
        tree: CartesianTree[int] = CartesianTree()
        with pytest.raises(IndexError):
            tree.pop()


class TestCartesianTreeRemove:
    """Test remove method."""

    def test__remove__existing_element(self) -> None:
        """Test removing existing element (first occurrence)."""
        tree = CartesianTree([1, 2, 3, 2])
        tree.remove(2)
        assert list(tree) == [1, 3, 2]

    def test__remove__missing_element(self) -> None:
        """Test removing missing element raises ValueError."""
        tree = CartesianTree([1, 2, 3])
        with pytest.raises(
            ValueError, match="attemp to remove an element which is not on in the CartesianTree",
        ):
            tree.remove(99)


class TestCartesianTreeClear:
    """Test clear method."""

    def test__clear__non_empty_tree(self) -> None:
        """Test clearing non-empty tree."""
        tree = CartesianTree([1, 2, 3])
        tree.clear()
        assert len(tree) == 0
        assert list(tree) == []

    def test__clear__empty_tree(self) -> None:
        """Test clearing empty tree (should not raise error)."""
        tree: CartesianTree[int] = CartesianTree()
        tree.clear()
        assert len(tree) == 0


class TestCartesianTreeReverse:
    """Test reverse method."""

    def test__reverse__non_empty_tree(self) -> None:
        """Test reversing non-empty tree."""
        tree = CartesianTree([1, 2, 3, 4, 5])
        tree.reverse()
        assert list(tree) == [5, 4, 3, 2, 1]

    def test__reverse__empty_tree(self) -> None:
        """Test reversing empty tree."""
        tree: CartesianTree[int] = CartesianTree()
        tree.reverse()
        assert list(tree) == []


class TestCartesianTreeIndex:
    """Test index method."""

    def test__index__existing_element(self) -> None:
        """Test finding index of existing element."""
        tree = CartesianTree([10, 20, 30, 20])
        assert tree.index(20) == 1

    def test__index__with_start(self) -> None:
        """Test finding index with start parameter."""
        tree = CartesianTree([10, 20, 30, 20])
        assert tree.index(20, 2) == 3

    def test__index__missing_element(self) -> None:
        """Test finding missing element raises ValueError."""
        tree = CartesianTree([1, 2, 3])
        with pytest.raises(ValueError, match="attemp to find missing element"):
            tree.index(99)


class TestCartesianTreeCount:
    """Test count method."""

    def test__count__existing_element(self) -> None:
        """Test counting occurrences of existing element."""
        tree = CartesianTree([1, 2, 2, 3, 2])
        assert tree.count(2) == 3

    def test__count__missing_element(self) -> None:
        """Test counting missing element returns 0."""
        tree = CartesianTree([1, 2, 3])
        assert tree.count(99) == 0


class TestCartesianTreeContains:
    """Test __contains__ method (in operator)."""

    def test__contains__existing_element(self) -> None:
        """Test that existing element is found."""
        tree = CartesianTree([1, 2, 3])
        assert 2 in tree

    def test__contains__missing_element(self) -> None:
        """Test that missing element is not found."""
        tree = CartesianTree([1, 2, 3])
        assert 99 not in tree


class TestCartesianTreeIter:
    """Test __iter__ method."""

    def test__iter__empty_tree(self) -> None:
        """Test iteration over empty tree."""
        tree: CartesianTree[int] = CartesianTree()
        assert list(tree) == []

    def test__iter__ascending_order(self) -> None:
        """Test iteration returns elements in ascending order."""
        tree = CartesianTree([5, 3, 7, 1, 4, 6, 8])
        assert list(tree) == [5, 3, 7, 1, 4, 6, 8]


class TestCartesianTreeReversed:
    """Test __reversed__ method."""

    def test__reversed__empty_tree(self) -> None:
        """Test reverse iteration over empty tree."""
        tree: CartesianTree[int] = CartesianTree()
        assert list(reversed(tree)) == []

    def test__reversed__descending_order(self) -> None:
        """Test reverse iteration returns elements in descending order."""
        tree = CartesianTree([1, 2, 3, 4, 5])
        assert list(reversed(tree)) == [5, 4, 3, 2, 1]


class TestCartesianTreeEq:
    """Test __eq__ method."""

    def test__eq__equal_trees(self) -> None:
        """Test two equal trees are equal."""
        tree1 = CartesianTree([1, 2, 3])
        tree2 = CartesianTree([1, 2, 3])
        assert tree1 == tree2

    def test__eq__different_trees(self) -> None:
        """Test different trees are not equal."""
        tree1 = CartesianTree([1, 2, 3])
        tree2 = CartesianTree([1, 2, 4])
        assert tree1 != tree2

    def test__eq__different_lengths(self) -> None:
        """Test trees with different lengths are not equal."""
        tree1 = CartesianTree([1, 2, 3])
        tree2 = CartesianTree([1, 2])
        assert tree1 != tree2

    def test__eq__not_tree(self) -> None:
        """Test comparing with non-tree returns False."""
        tree = CartesianTree([1, 2, 3])
        assert tree != [1, 2, 3]
        assert tree != "not a tree"


class TestCartesianTreeHash:
    """Test __hash__ method."""

    def test__hash__raises_type_error(self) -> None:
        """Test that hash raises TypeError (unhashable)."""
        tree = CartesianTree([1, 2, 3])
        with pytest.raises(TypeError):
            hash(tree)
