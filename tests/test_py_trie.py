"""Tests for Trie implementation."""

from __future__ import annotations

import pytest

from onotation.internal.trie.py_trie import Trie


class TestTrieIterator:
    """Test __iter__ functionality."""

    def test__iter__empty(self) -> None:
        """Empty trie iteration returns empty list."""
        trie = Trie()
        assert list(trie) == []

    def test__iter__single_element(self) -> None:
        """Single element iteration."""
        trie = Trie(["hello"])
        assert list(trie) == ["hello"]

    def test__iter__ascending_order(self) -> None:
        """Iteration returns elements in sorted order."""
        trie = Trie(["cat", "car", "dog", "apple"])
        assert list(trie) == ["apple", "car", "cat", "dog"]

    def test__iter__with_duplicates(self) -> None:
        """Duplicates are ignored in iteration."""
        trie = Trie(["abc", "abc", "xyz", "xyz"])
        assert list(trie) == ["abc", "xyz"]

    def test__iter__empty_string(self) -> None:
        """Empty string is handled correctly."""
        trie = Trie(["", "abc"])
        assert list(trie) == ["", "abc"]

    def test__iter__large_dataset(self) -> None:
        """Large dataset iteration."""
        words = [f"word{i}" for i in range(100)]
        trie = Trie(words)
        assert list(trie) == sorted(words)


class TestTrieReversed:
    """Test __reversed__ functionality."""

    def test__reversed__empty(self) -> None:
        """Empty trie reversed iteration."""
        trie = Trie()
        assert list(reversed(trie)) == []

    def test__reversed__single_element(self) -> None:
        """Single element reversed iteration."""
        trie = Trie(["hello"])
        assert list(reversed(trie)) == ["hello"]

    def test__reversed__descending_order(self) -> None:
        """Reversed iteration follows reverse DFS order."""
        trie = Trie(["cat", "car", "dog", "apple"])
        assert list(reversed(trie)) == ["dog", "cat", "car", "apple"]

    def test__reversed__empty_string(self) -> None:
        """Empty string ordering in reversed iteration."""
        trie = Trie(["", "abc"])
        assert list(reversed(trie)) == ["abc", ""]

    def test__reversed__large_dataset(self) -> None:
        """Large dataset reversed iteration."""
        words = [f"word{i}" for i in range(100)]
        trie = Trie(words)

        # проверяем консистентность с обычным порядком
        assert list(reversed(trie)) == list(trie)[::-1]


class TestTrieContains:
    """Test __contains__ functionality."""

    def test__contains__existing_element(self) -> None:
        """Element exists in trie."""
        trie = Trie(["abc", "def"])
        assert "abc" in trie

    def test__contains__missing_element(self) -> None:
        """Missing element is not found."""
        trie = Trie(["abc", "def"])
        assert "xyz" not in trie

    def test__contains__empty_trie(self) -> None:
        """Empty trie contains nothing."""
        trie = Trie()
        assert "abc" not in trie

    def test__contains__prefix_only(self) -> None:
        """Prefix is not a full match."""
        trie = Trie(["abcdef"])
        assert "abc" not in trie

    def test__contains__empty_string(self) -> None:
        """Empty string membership."""
        trie = Trie([""])
        assert "" in trie

    def test__contains__non_string(self) -> None:
        """Non-string values are always False."""
        trie = Trie(["abc"])

        non_string_int = 123
        non_string_none = None
        non_string_list = []

        assert non_string_int not in trie
        assert non_string_none not in trie
        assert non_string_list not in trie


class TestTrieAdd:
    """Test add method."""

    def test__add__new_element(self) -> None:
        """Add new element."""
        trie = Trie()
        trie.add("abc")

        assert "abc" in trie
        assert len(trie) == 1

    def test__add__duplicate_element(self) -> None:
        """Duplicate add does nothing."""
        trie = Trie(["abc"])
        trie.add("abc")

        assert len(trie) == 1

    def test__add__empty_string(self) -> None:
        """Add empty string."""
        trie = Trie()
        trie.add("")

        assert "" in trie
        assert len(trie) == 1


class TestTrieRemove:
    """Test remove method."""

    def test__remove__existing_element(self) -> None:
        """Remove existing element."""
        trie = Trie(["abc", "def"])

        trie.remove("abc")

        assert "abc" not in trie
        assert len(trie) == 1

    def test__remove__missing_element(self) -> None:
        """Removing missing element raises KeyError."""
        trie = Trie(["abc"])

        with pytest.raises(KeyError):
            trie.remove("xyz")

    def test__remove__empty_trie(self) -> None:
        """Removing from empty trie raises KeyError."""
        trie = Trie()

        with pytest.raises(KeyError):
            trie.remove("abc")

    def test__remove__prefix(self) -> None:
        """Removing one element does not affect others."""
        trie = Trie(["abc", "abcd"])

        trie.remove("abc")

        assert "abc" not in trie
        assert "abcd" in trie

    def test__remove__empty_string(self) -> None:
        """Remove empty string."""
        trie = Trie([""])

        trie.remove("")

        assert "" not in trie
        assert len(trie) == 0


class TestTrieDiscard:
    """Test discard method."""

    def test__discard__existing_element(self) -> None:
        """Discard existing element."""
        trie = Trie(["abc"])

        trie.discard("abc")

        assert "abc" not in trie
        assert len(trie) == 0

    def test__discard__missing_element(self) -> None:
        """Discard missing element is safe."""
        trie = Trie(["abc"])

        trie.discard("xyz")

        assert len(trie) == 1


class TestTriePop:
    """Test pop method."""

    def test__pop(self) -> None:
        """Pop removes an element."""
        trie = Trie(["abc", "def"])

        result = trie.pop()

        assert result in {"abc", "def"}
        assert len(trie) == 1

    def test__pop__empty(self) -> None:
        """Pop from empty trie raises KeyError."""
        trie = Trie()

        with pytest.raises(KeyError):
            trie.pop()


class TestTrieClear:
    """Test clear method."""

    def test__clear(self) -> None:
        """Clear removes all elements."""
        trie = Trie(["abc", "def"])

        trie.clear()

        assert len(trie) == 0
        assert list(trie) == []


class TestTrieEq:
    """Test __eq__ method."""

    def test__eq__equal_tries(self) -> None:
        """Equal tries are equal."""
        trie1 = Trie(["abc", "def"])
        trie2 = Trie(["abc", "def"])

        assert trie1 == trie2

    def test__eq__different_tries(self) -> None:
        """Different tries are not equal."""
        trie1 = Trie(["abc"])
        trie2 = Trie(["xyz"])

        assert trie1 != trie2

    def test__eq__different_order(self) -> None:
        """Order does not matter."""
        trie1 = Trie(["abc", "def"])
        trie2 = Trie(["def", "abc"])

        assert trie1 == trie2

    def test__eq__not_trie(self) -> None:
        """Comparison with non-trie."""
        trie = Trie(["abc"])

        non_trie_int = 123
        non_trie_str = "abc"

        assert trie != non_trie_int
        assert trie != non_trie_str

    def test__eq__empty_tries(self) -> None:
        """Empty tries are equal."""
        trie1 = Trie()
        trie2 = Trie()

        assert trie1 == trie2


class TestTrieLen:
    """Test __len__ method."""

    def test__len__empty(self) -> None:
        """Empty trie length."""
        trie = Trie()
        assert len(trie) == 0

    def test__len__after_add(self) -> None:
        """Length after add."""
        trie = Trie(["abc", "def"])
        expected_len = 2
        assert len(trie) == expected_len

    def test__len__after_remove(self) -> None:
        """Length after remove."""
        trie = Trie(["abc", "def"])

        trie.remove("abc")

        assert len(trie) == 1


class TestTrieHash:
    """Test __hash__ method."""

    def test__hash__raises(self) -> None:
        """Trie is not hashable."""
        trie = Trie(["abc"])

        with pytest.raises(NotImplementedError):
            hash(trie)
