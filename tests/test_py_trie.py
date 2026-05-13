
"""Tests for Trie implementation."""

from __future__ import annotations

import pytest

from onotation.internal.trie.py_trie import Trie


class TestTrieIterator:
    """Test __iter__ functionality."""

    def test__iter__empty(self) -> None:
        """Test __iter__ on empty trie."""
        trie = Trie()
        assert list(trie) == []

    def test__iter__single_element(self) -> None:
        """Test __iter__ on trie with one element."""
        trie = Trie(["hello"])
        assert list(trie) == ["hello"]

    def test__iter__ascending_order(self) -> None:
        """Test __iter__ returns elements in ascending order."""
        trie = Trie(["cat", "car", "dog", "apple"])
        assert list(trie) == ["apple", "car", "cat", "dog"]

    def test__iter__with_duplicates(self) -> None:
        """Test that duplicates are ignored."""
        trie = Trie(["abc", "abc", "xyz", "xyz"])
        assert list(trie) == ["abc", "xyz"]

    def test__iter__empty_string(self) -> None:
        """Test __iter__ with empty string."""
        trie = Trie(["", "abc"])
        assert list(trie) == ["", "abc"]

    def test__iter__large_dataset(self) -> None:
        """Test __iter__ on larger dataset."""
        words = [f"word{i}" for i in range(100)]
        trie = Trie(words)
        assert list(trie) == sorted(words)


class TestTrieReversed:
    """Test __reversed__ functionality."""

    def test__reversed__empty(self) -> None:
        """Test __reversed__ on empty trie."""
        trie = Trie()
        assert list(reversed(trie)) == []

    def test__reversed__single_element(self) -> None:
        """Test __reversed__ on trie with one element."""
        trie = Trie(["hello"])
        assert list(reversed(trie)) == ["hello"]

    def test__reversed__descending_order(self) -> None:
        """Test __reversed__ returns elements in descending order."""
        trie = Trie(["cat", "car", "dog", "apple"])
        assert list(reversed(trie)) == ["dog", "cat", "car", "apple"]

    def test__reversed__empty_string(self) -> None:
        """Test __reversed__ with empty string."""
        trie = Trie(["", "abc"])
        assert list(reversed(trie)) == ["abc", ""]

    def test__reversed__large_dataset(self) -> None:
        """Test __reversed__ on larger dataset."""
        words = [f"word{i}" for i in range(100)]
        trie = Trie(words)
        assert list(reversed(trie)) == sorted(words, reverse=True)


class TestTrieContains:
    """Test __contains__ functionality."""

    def test__contains__existing_element(self) -> None:
        """Test that existing element is found."""
        trie = Trie(["abc", "def"])
        assert "abc" in trie

    def test__contains__missing_element(self) -> None:
        """Test that missing element is not found."""
        trie = Trie(["abc", "def"])
        assert "xyz" not in trie

    def test__contains__empty_trie(self) -> None:
        """Test __contains__ on empty trie."""
        trie = Trie()
        assert "abc" not in trie

    def test__contains__prefix_only(self) -> None:
        """Test prefix is not considered a full word."""
        trie = Trie(["abcdef"])
        assert "abc" not in trie

    def test__contains__empty_string(self) -> None:
        """Test empty string membership."""
        trie = Trie([""])
        assert "" in trie

    def test__contains__non_string(self) -> None:
        """Test non-string values always return False."""
        trie = Trie(["abc"])
        assert 123 not in trie
        assert None not in trie
        assert [] not in trie


class TestTrieAdd:
    """Test add method."""

    def test__add__new_element(self) -> None:
        """Test adding new element."""
        trie = Trie()
        trie.add("abc")

        assert "abc" in trie
        assert len(trie) == 1

    def test__add__duplicate_element(self) -> None:
        """Test adding duplicate element does nothing."""
        trie = Trie(["abc"])

        trie.add("abc")

        assert len(trie) == 1

    def test__add__empty_string(self) -> None:
        """Test adding empty string."""
        trie = Trie()

        trie.add("")

        assert "" in trie
        assert len(trie) == 1


class TestTrieRemove:
    """Test remove method."""

    def test__remove__existing_element(self) -> None:
        """Test removing existing element."""
        trie = Trie(["abc", "def"])

        trie.remove("abc")

        assert "abc" not in trie
        assert len(trie) == 1

    def test__remove__missing_element(self) -> None:
        """Test removing missing element raises KeyError."""
        trie = Trie(["abc"])

        with pytest.raises(KeyError):
            trie.remove("xyz")

    def test__remove__empty_trie(self) -> None:
        """Test removing from empty trie raises KeyError."""
        trie = Trie()

        with pytest.raises(KeyError):
            trie.remove("abc")

    def test__remove__prefix(self) -> None:
        """Test removing one word does not affect another."""
        trie = Trie(["abc", "abcd"])

        trie.remove("abc")

        assert "abc" not in trie
        assert "abcd" in trie

    def test__remove__empty_string(self) -> None:
        """Test removing empty string."""
        trie = Trie([""])

        trie.remove("")

        assert "" not in trie
        assert len(trie) == 0


class TestTrieDiscard:
    """Test discard method."""

    def test__discard__existing_element(self) -> None:
        """Test discarding existing element."""
        trie = Trie(["abc"])

        trie.discard("abc")

        assert "abc" not in trie
        assert len(trie) == 0

    def test__discard__missing_element(self) -> None:
        """Test discarding missing element does nothing."""
        trie = Trie(["abc"])

        trie.discard("xyz")

        assert len(trie) == 1


class TestTriePop:
    """Test pop method."""

    def test__pop(self) -> None:
        """Test pop removes arbitrary element."""
        trie = Trie(["abc", "def"])

        result = trie.pop()

        assert result in {"abc", "def"}
        assert len(trie) == 1

    def test__pop__empty(self) -> None:
        """Test pop from empty trie raises KeyError."""
        trie = Trie()

        with pytest.raises(KeyError):
            trie.pop()


class TestTrieClear:
    """Test clear method."""

    def test__clear(self) -> None:
        """Test clear removes all elements."""
        trie = Trie(["abc", "def"])

        trie.clear()

        assert len(trie) == 0
        assert list(trie) == []


class TestTrieEq:
    """Test __eq__ method."""

    def test__eq__equal_tries(self) -> None:
        """Test equal tries are equal."""
        trie1 = Trie(["abc", "def"])
        trie2 = Trie(["abc", "def"])

        assert trie1 == trie2

    def test__eq__different_tries(self) -> None:
        """Test different tries are not equal."""
        trie1 = Trie(["abc"])
        trie2 = Trie(["xyz"])

        assert trie1 != trie2

    def test__eq__different_order(self) -> None:
        """Test insertion order does not matter."""
        trie1 = Trie(["abc", "def"])
        trie2 = Trie(["def", "abc"])

        assert trie1 == trie2

    def test__eq__not_trie(self) -> None:
        """Test comparison with non-set object."""
        trie = Trie(["abc"])

        assert trie != 123
        assert trie != "abc"

    def test__eq__empty_tries(self) -> None:
        """Test empty tries are equal."""
        trie1 = Trie()
        trie2 = Trie()

        assert trie1 == trie2


class TestTrieLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        """Test length of empty trie."""
        trie = Trie()

        assert len(trie) == 0

    def test__len__after_add(self) -> None:
        """Test length after adding elements."""
        trie = Trie(["abc", "def"])

        assert len(trie) == 2

    def test__len__after_remove(self) -> None:
        """Test length after removing elements."""
        trie = Trie(["abc", "def"])

        trie.remove("abc")

        assert len(trie) == 1


class TestTrieSetOperations:
    """Test set operations."""

    def test__or__(self) -> None:
        """Test union operation."""
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b", "c"])

        result = trie1 | trie2

        assert result == Trie(["a", "b", "c"])

    def test__and__(self) -> None:
        """Test intersection operation."""
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b", "c"])

        result = trie1 & trie2

        assert result == Trie(["b"])

    def test__sub__(self) -> None:
        """Test difference operation."""
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b"])

        result = trie1 - trie2

        assert result == Trie(["a"])

    def test__xor__(self) -> None:
        """Test symmetric difference operation."""
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b", "c"])

        result = trie1 ^ trie2

        assert result == Trie(["a", "c"])


class TestTrieInplaceOperations:
    """Test inplace set operations."""

    def test__ior__(self) -> None:
        """Test inplace union."""
        trie = Trie(["a"])

        trie |= {"b"}

        assert trie == Trie(["a", "b"])

    def test__iand__(self) -> None:
        """Test inplace intersection."""
        trie = Trie(["a", "b"])

        trie &= {"b"}

        assert trie == Trie(["b"])

    def test__isub__(self) -> None:
        """Test inplace difference."""
        trie = Trie(["a", "b"])

        trie -= {"a"}

        assert trie == Trie(["b"])

    def test__ixor__(self) -> None:
        """Test inplace symmetric difference."""
        trie = Trie(["a", "b"])

        trie ^= {"b", "c"}

        assert trie == Trie(["a", "c"])


class TestTrieComparisons:
    """Test comparison operators."""

    def test__le__(self) -> None:
        """Test subset operation."""
        trie1 = Trie(["a"])
        trie2 = Trie(["a", "b"])

        assert trie1 <= trie2

    def test__lt__(self) -> None:
        """Test proper subset operation."""
        trie1 = Trie(["a"])
        trie2 = Trie(["a", "b"])

        assert trie1 < trie2

    def test__ge__(self) -> None:
        """Test superset operation."""
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["a"])

        assert trie1 >= trie2

    def test__gt__(self) -> None:
        """Test proper superset operation."""
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["a"])

        assert trie1 > trie2

    def test__isdisjoint__(self) -> None:
        """Test disjoint sets."""
        trie1 = Trie(["a", "b"])

        assert trie1.isdisjoint({"c", "d"})
        assert not trie1.isdisjoint({"b", "c"})


class TestTrieHash:
    """Test __hash__ method."""

    def test__hash__raises(self) -> None:
        """Test __hash__ raises NotImplementedError."""
        trie = Trie(["abc"])

        with pytest.raises(NotImplementedError):
            hash(trie)
