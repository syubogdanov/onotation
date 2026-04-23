import pytest

from onotation.internal.binary_search_tree.py_binary_search_tree import (
    BinarySearchTree,
)


def make_tree(values):
    tree = BinarySearchTree[int]()
    for v in values:
        tree.add(v)
    return tree


def test_empty_tree():
    tree = BinarySearchTree[int]()
    assert len(tree) == 0
    assert list(tree) == []
    assert 1 not in tree


def test_add_and_contains():
    tree = BinarySearchTree[int]()
    tree.add(5)
    tree.add(3)
    tree.add(7)

    assert 5 in tree
    assert 3 in tree
    assert 7 in tree
    assert 10 not in tree


def test_no_duplicates():
    tree = BinarySearchTree[int]()
    tree.add(5)
    tree.add(5)

    assert len(tree) == 1


def test_len():
    tree = make_tree([1, 2, 3, 4])
    assert len(tree) == 4


def test_iter_sorted_order():
    tree = make_tree([5, 3, 7, 1, 4, 6, 8])
    assert list(tree) == [1, 3, 4, 5, 6, 7, 8]


def test_reversed_iter():
    tree = make_tree([5, 3, 7, 1, 4, 6, 8])
    assert list(reversed(tree)) == [8, 7, 6, 5, 4, 3, 1]


def test_iter_empty():
    tree = BinarySearchTree[int]()
    assert list(tree) == []
    assert list(reversed(tree)) == []


def test_remove_leaf():
    tree = make_tree([5, 3, 7])
    tree.remove(3)

    assert list(tree) == [5, 7]
    assert 3 not in tree


def test_remove_node_with_one_child():
    tree = make_tree([5, 3, 7, 6])
    tree.remove(7)

    assert list(tree) == [3, 5, 6]


def test_remove_node_with_two_children():
    tree = make_tree([5, 3, 7, 6, 8])
    tree.remove(7)

    assert list(tree) == [3, 5, 6, 8]


def test_remove_root():
    tree = make_tree([5, 3, 7])
    tree.remove(5)

    assert list(tree) in ([3, 7], [7, 3])
    assert 5 not in tree


def test_remove_not_found():
    tree = make_tree([1, 2, 3])
    with pytest.raises(KeyError):
        tree.remove(10)


def test_discard():
    tree = make_tree([1, 2, 3])
    tree.discard(2)
    assert 2 not in tree

    tree.discard(10)


def test_pop():
    tree = make_tree([5, 3, 7])
    value = tree.pop()

    assert value not in tree
    assert len(tree) == 2


def test_pop_empty():
    tree = BinarySearchTree[int]()
    with pytest.raises(KeyError):
        tree.pop()


def test_clear():
    tree = make_tree([1, 2, 3])
    tree.clear()

    assert len(tree) == 0
    assert list(tree) == []


def test_equality():
    a = make_tree([1, 2, 3])
    b = make_tree([3, 2, 1])
    c = make_tree([1, 2])

    assert a == b
    assert a != c
    assert a != {1, 2}


def test_union():
    a = make_tree([1, 2, 3])
    b = make_tree([3, 4, 5])

    result = a | b
    assert set(result) == {1, 2, 3, 4, 5}


def test_intersection():
    a = make_tree([1, 2, 3])
    b = make_tree([2, 3, 4])

    result = a & b
    assert set(result) == {2, 3}


def test_difference():
    a = make_tree([1, 2, 3])
    b = make_tree([2])

    result = a - b
    assert set(result) == {1, 3}


def test_inplace_and():
    a = make_tree([1, 2, 3])
    b = {2, 3}

    a &= b
    assert set(a) == {2, 3}


def test_inplace_or():
    a = make_tree([1, 2])
    b = {2, 3}

    a |= b
    assert set(a) == {1, 2, 3}


def test_inplace_sub():
    a = make_tree([1, 2, 3])
    b = {2}

    a -= b
    assert set(a) == {1, 3}
