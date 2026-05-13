"""Tests for Trie implementation."""

from __future__ import annotations

import pytest

from onotation.internal.trie.py_trie import Trie


class TestTrieIterator:
    """Test __iter__ functionality."""

    def test__iter__empty(self) -> None:
        trie = Trie()
        assert list(trie) == []

    def test__iter__single_element(self) -> None:
        trie = Trie(["hello"])
        assert list(trie) == ["hello"]

    def test__iter__ascending_order(self) -> None:
        trie = Trie(["cat", "car", "dog", "apple"])
        assert list(trie) == ["apple", "car", "cat", "dog"]

    def test__iter__with_duplicates(self) -> None:
        trie = Trie(["abc", "abc", "xyz", "xyz"])
        assert list(trie) == ["abc", "xyz"]

    def test__iter__empty_string(self) -> None:
        trie = Trie(["", "abc"])
        assert list(trie) == ["", "abc"]

    def test__iter__large_dataset(self) -> None:
        words = [f"word{i}" for i in range(100)]
        trie = Trie(words)
        assert list(trie) == sorted(words)


class TestTrieReversed:
    """Test __reversed__ functionality."""

    def test__reversed__empty(self) -> None:
        trie = Trie()
        assert list(reversed(trie)) == []

    def test__reversed__single_element(self) -> None:
        trie = Trie(["hello"])
        assert list(reversed(trie)) == ["hello"]

    def test__reversed__descending_order(self) -> None:
        trie = Trie(["cat", "car", "dog", "apple"])
        assert list(reversed(trie)) == ["dog", "cat", "car", "apple"]

    def test__reversed__empty_string(self) -> None:
        trie = Trie(["", "abc"])
        assert list(reversed(trie)) == ["abc", ""]

    def test__reversed__large_dataset(self) -> None:
        words = [f"word{i}" for i in range(100)]
        trie = Trie(words)
        assert list(reversed(trie)) == sorted(words, reverse=True)


class TestTrieContains:
    """Test __contains__ functionality."""

    def test__contains__existing_element(self) -> None:
        trie = Trie(["abc", "def"])
        assert "abc" in trie

    def test__contains__missing_element(self) -> None:
        trie = Trie(["abc", "def"])
        assert "xyz" not in trie

    def test__contains__empty_trie(self) -> None:
        trie = Trie()
        assert "abc" not in trie

    def test__contains__prefix_only(self) -> None:
        trie = Trie(["abcdef"])
        assert "abc" not in trie

    def test__contains__empty_string(self) -> None:
        trie = Trie([""])
        assert "" in trie

    def test__contains__non_string(self) -> None:
        trie = Trie(["abc"])

        assert 123 not in trie
        assert None not in trie
        assert [] not in trie


class TestTrieAdd:
    """Test add method."""

    def test__add__new_element(self) -> None:
        trie = Trie()
        trie.add("abc")

        assert "abc" in trie
        assert len(trie) == 1

    def test__add__duplicate_element(self) -> None:
        trie = Trie(["abc"])
        trie.add("abc")

        assert len(trie) == 1

    def test__add__empty_string(self) -> None:
        trie = Trie()
        trie.add("")

        assert "" in trie
        assert len(trie) == 1


class TestTrieRemove:
    """Test remove method."""

    def test__remove__existing_element(self) -> None:
        trie = Trie(["abc", "def"])

        trie.remove("abc")

        assert "abc" not in trie
        assert len(trie) == 1

    def test__remove__missing_element(self) -> None:
        trie = Trie(["abc"])

        with pytest.raises(KeyError):
            trie.remove("xyz")

    def test__remove__empty_trie(self) -> None:
        trie = Trie()

        with pytest.raises(KeyError):
            trie.remove("abc")

    def test__remove__prefix(self) -> None:
        trie = Trie(["abc", "abcd"])

        trie.remove("abc")

        assert "abc" not in trie
        assert "abcd" in trie

    def test__remove__empty_string(self) -> None:
        trie = Trie([""])

        trie.remove("")

        assert "" not in trie
        assert len(trie) == 0


class TestTrieDiscard:
    """Test discard method."""

    def test__discard__existing_element(self) -> None:
        trie = Trie(["abc"])

        trie.discard("abc")

        assert "abc" not in trie
        assert len(trie) == 0

    def test__discard__missing_element(self) -> None:
        trie = Trie(["abc"])

        trie.discard("xyz")

        assert len(trie) == 1


class TestTriePop:
    """Test pop method."""

    def test__pop(self) -> None:
        trie = Trie(["abc", "def"])

        result = trie.pop()

        assert result in {"abc", "def"}
        assert len(trie) == 1

    def test__pop__empty(self) -> None:
        trie = Trie()

        with pytest.raises(KeyError):
            trie.pop()


class TestTrieClear:
    """Test clear method."""

    def test__clear(self) -> None:
        trie = Trie(["abc", "def"])

        trie.clear()

        assert len(trie) == 0
        assert list(trie) == []


class TestTrieEq:
    """Test __eq__ method."""

    def test__eq__equal_tries(self) -> None:
        trie1 = Trie(["abc", "def"])
        trie2 = Trie(["abc", "def"])

        assert trie1 == trie2

    def test__eq__different_tries(self) -> None:
        trie1 = Trie(["abc"])
        trie2 = Trie(["xyz"])

        assert trie1 != trie2

    def test__eq__different_order(self) -> None:
        trie1 = Trie(["abc", "def"])
        trie2 = Trie(["def", "abc"])

        assert trie1 == trie2

    def test__eq__not_trie(self) -> None:
        trie = Trie(["abc"])

        assert trie != 123
        assert trie != "abc"

    def test__eq__empty_tries(self) -> None:
        trie1 = Trie()
        trie2 = Trie()

        assert trie1 == trie2


class TestTrieLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        trie = Trie()
        assert len(trie) == 0

    def test__len__after_add(self) -> None:
        trie = Trie(["abc", "def"])

        expected_len = 2
        assert len(trie) == expected_len

    def test__len__after_remove(self) -> None:
        trie = Trie(["abc", "def"])

        trie.remove("abc")

        assert len(trie) == 1


class TestTrieSetOperations:
    """Test set operations."""

    def test__or__(self) -> None:
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b", "c"])

        result = trie1 | trie2

        assert result == Trie(["a", "b", "c"])

    def test__and__(self) -> None:
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b", "c"])

        result = trie1 & trie2

        assert result == Trie(["b"])

    def test__sub__(self) -> None:
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b"])

        result = trie1 - trie2

        assert result == Trie(["a"])

    def test__xor__(self) -> None:
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["b", "c"])

        result = trie1 ^ trie2

        assert result == Trie(["a", "c"])


class TestTrieInplaceOperations:
    """Test inplace set operations."""

    def test__ior__(self) -> None:
        trie = Trie(["a"])

        trie |= {"b"}

        assert trie == Trie(["a", "b"])

    def test__iand__(self) -> None:
        trie = Trie(["a", "b"])

        trie &= {"b"}

        assert trie == Trie(["b"])

    def test__isub__(self) -> None:
        trie = Trie(["a", "b"])

        trie -= {"a"}

        assert trie == Trie(["b"])

    def test__ixor__(self) -> None:
        trie = Trie(["a", "b"])

        trie ^= {"b", "c"}

        assert trie == Trie(["a", "c"])


class TestTrieComparisons:
    """Test comparison operators."""

    def test__le__(self) -> None:
        trie1 = Trie(["a"])
        trie2 = Trie(["a", "b"])

        assert trie1 <= trie2

    def test__lt__(self) -> None:
        trie1 = Trie(["a"])
        trie2 = Trie(["a", "b"])

        assert trie1 < trie2

    def test__ge__(self) -> None:
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["a"])

        assert trie1 >= trie2

    def test__gt__(self) -> None:
        trie1 = Trie(["a", "b"])
        trie2 = Trie(["a"])

        assert trie1 > trie2

    def test__isdisjoint__(self) -> None:
        trie1 = Trie(["a", "b"])

        assert trie1.isdisjoint({"c", "d"})
        assert not trie1.isdisjoint({"b", "c"})


class TestTrieHash:
    """Test __hash__ method."""

    def test__hash__raises(self) -> None:
        trie = Trie(["abc"])

        with pytest.raises(NotImplementedError):
            hash(trie)