"""Tests for Trie implementation."""

from __future__ import annotations

from typing import cast

import pytest

from onotation.internal.trie.py_trie import Trie


class TestTrieIterator:
    """Tests for Trie __iter__ behavior."""

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
    """Tests for Trie __reversed__ behavior."""

    def test__reversed__empty(self) -> None:
        trie = Trie()
        assert list(reversed(trie)) == []

    def test__reversed__single_element(self) -> None:
        trie = Trie(["hello"])
        assert list(reversed(trie)) == ["hello"]

    def test__reversed__descending_order(self) -> None:
        trie = Trie(["cat", "car", "dog", "apple"])

        result = list(reversed(trie))

        assert set(result) == {"cat", "car", "dog", "apple"}
        assert result == list(reversed(trie))

    def test__reversed__empty_string(self) -> None:
        trie = Trie(["", "abc"])

        result = list(reversed(trie))

        assert set(result) == {"", "abc"}
        assert result == list(reversed(trie))

    def test__reversed__large_dataset(self) -> None:
        words = [f"word{i}" for i in range(100)]
        trie = Trie(words)

        result = list(reversed(trie))

        assert set(result) == set(words)
        assert result == list(reversed(trie))


class TestTrieContains:
    """Tests for Trie __contains__ behavior."""

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

        assert (cast(object, 123) in trie) is False
        assert (cast(object, None) in trie) is False
        assert (cast(object, []) in trie) is False


class TestTrieAdd:
    """Tests for Trie add behavior."""

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
    """Tests for Trie remove behavior."""

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
    """Tests for Trie discard behavior."""

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
    """Tests for Trie pop behavior."""

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
    """Tests for Trie clear behavior."""

    def test__clear(self) -> None:
        trie = Trie(["abc", "def"])
        trie.clear()

        assert len(trie) == 0
        assert list(trie) == []


class TestTrieEq:
    """Tests for Trie equality."""

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

        assert trie != cast(object, 123)
        assert trie != cast(object, "abc")

    def test__eq__empty_tries(self) -> None:
        trie1 = Trie()
        trie2 = Trie()

        assert trie1 == trie2


class TestTrieLen:
    """Tests for Trie length."""

    def test__len__empty(self) -> None:
        trie = Trie()
        assert len(trie) == 0

    def test__len__after_add(self) -> None:
        trie = Trie(["abc", "def"])
        assert len(trie) == 2

    def test__len__after_remove(self) -> None:
        trie = Trie(["abc", "def"])
        trie.remove("abc")

        assert len(trie) == 1


class TestTrieHash:
    """Tests for Trie hashing behavior."""

    def test__hash__raises(self) -> None:
        trie = Trie(["abc"])

        with pytest.raises(TypeError):
            hash(trie)