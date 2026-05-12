"""Tests for Trie implementation."""

import sys
from pathlib import Path

import pytest

# Пытаемся найти Trie в разных возможных местах
sys.path.insert(0, str(Path(__file__).parent))  # добавляем папку с тестом в путь

try:
    from py_trie import Trie
except ImportError:
    try:
        from onotation.internal.py_trie import Trie
    except ImportError:
        try:
            from onotation.py_trie import Trie
        except ImportError:
            raise ImportError(
                "Не удалось импортировать Trie. Убедитесь, что файл py_trie.py "
                "находится в одной папке с тестом, или укажите правильный путь "
                "импорта (например, from onotation.internal.trie import Trie)."
            )

EMPTY_STRING = ""
SINGLE_CHAR = "a"
WORD_HELLO = "hello"
WORD_WORLD = "world"
WORD_HELP = "help"
WORD_HE = "he"
WORD_H = "h"
WORD_A = "a"
WORD_B = "b"
WORD_AA = "aa"
WORD_AB = "ab"
NON_STRING_VALUES = [123, None, ["a"]]


class TestTrieBasicOperations:
    """Test basic operations: __init__, __len__, __contains__, add, remove, discard, pop, clear."""

    def test_init_empty(self) -> None:
        """Test empty trie initialization."""
        t = Trie()
        assert len(t) == 0
        assert list(t) == []

    def test_init_with_iterable(self) -> None:
        """Test initialization with an iterable of strings."""
        words = ["hello", "world"]
        t = Trie(words)
        assert len(t) == len(words)
        assert "hello" in t
        assert "world" in t

    def test_add_new_element(self) -> None:
        """Test adding a single element."""
        t = Trie()
        t.add(WORD_HELLO)
        assert len(t) == 1
        assert WORD_HELLO in t

    def test_add_empty_string(self) -> None:
        """Test adding the empty string."""
        t = Trie()
        t.add(EMPTY_STRING)
        assert len(t) == 1
        assert EMPTY_STRING in t

    def test_add_duplicate_element(self) -> None:
        """Test adding an element that already exists."""
        t = Trie([WORD_HELLO])
        t.add(WORD_HELLO)
        assert len(t) == 1

    def test_remove_existing_element(self) -> None:
        """Test removing an existing element."""
        t = Trie([WORD_HELLO])
        t.remove(WORD_HELLO)
        assert len(t) == 0
        assert WORD_HELLO not in t

    def test_remove_empty_string(self) -> None:
        """Test removing the empty string."""
        t = Trie([EMPTY_STRING])
        t.remove(EMPTY_STRING)
        assert len(t) == 0
        assert EMPTY_STRING not in t

    def test_remove_nonexistent_element(self) -> None:
        """Test removing an element not in the trie raises KeyError."""
        t = Trie()
        with pytest.raises(KeyError):
            t.remove(WORD_HELLO)

    def test_discard_existing_element(self) -> None:
        """Test discarding an existing element."""
        t = Trie([WORD_HELLO])
        t.discard(WORD_HELLO)
        assert WORD_HELLO not in t

    def test_discard_nonexistent_element(self) -> None:
        """Test discarding a non-existent element does nothing."""
        t = Trie()
        t.discard(WORD_HELLO)
        assert len(t) == 0

    def test_pop_from_nonempty(self) -> None:
        """Test pop removes and returns an arbitrary element."""
        t = Trie(["a", "b"])
        elem = t.pop()
        assert elem in {"a", "b"}
        assert len(t) == 1
        assert elem not in t

    def test_pop_from_empty(self) -> None:
        """Test pop from empty trie raises KeyError."""
        t = Trie()
        with pytest.raises(KeyError):
            t.pop()

    def test_clear(self) -> None:
        """Test clear removes all elements."""
        t = Trie(["a", "b", "c"])
        t.clear()
        assert len(t) == 0
        assert list(t) == []

    def test_contains_non_string(self) -> None:
        """Test __contains__ with non-string returns False."""
        t = Trie(["a"])
        for value in NON_STRING_VALUES:
            assert value not in t


class TestTrieIterator:
    """Test __iter__ and __reversed__ functionality."""

    def test_iter_empty(self) -> None:
        """Test __iter__ on empty trie."""
        t = Trie()
        assert list(t) == []

    def test_iter_single_element(self) -> None:
        """Test __iter__ with one element."""
        t = Trie([WORD_HELLO])
        assert list(t) == [WORD_HELLO]

    def test_iter_order_ascending(self) -> None:
        """Test __iter__ returns elements in ascending lexicographic order."""
        words = ["a", "aa", "ab", "b", "ba"]
        t = Trie(words)
        assert list(t) == sorted(words)

    def test_iter_with_empty_string(self) -> None:
        """Test __iter__ includes the empty string when present."""
        t = Trie(["", "a", "b"])
        assert list(t) == ["", "a", "b"]

    def test_reversed_empty(self) -> None:
        """Test __reversed__ on empty trie."""
        t = Trie()
        assert list(reversed(t)) == []

    def test_reversed_single_element(self) -> None:
        """Test __reversed__ with one element."""
        t = Trie([WORD_HELLO])
        assert list(reversed(t)) == [WORD_HELLO]

    def test_reversed_order_descending(self) -> None:
        """Test __reversed__ returns elements in descending lexicographic order."""
        words = ["a", "aa", "ab", "b", "ba"]
        t = Trie(words)
        assert list(reversed(t)) == sorted(words, reverse=True)

    def test_reversed_with_empty_string(self) -> None:
        """Test __reversed__ includes the empty string when present."""
        t = Trie(["", "a", "b"])
        assert list(reversed(t)) == ["b", "a", ""]


class TestTrieSetOperations:
    """Test set operations: union, intersection, difference, symmetric difference, subset, etc."""

    def test_isdisjoint_true(self) -> None:
        """Test isdisjoint returns True for disjoint sets."""
        t1 = Trie(["a", "b"])
        t2 = Trie(["c", "d"])
        assert t1.isdisjoint(t2)

    def test_isdisjoint_false(self) -> None:
        """Test isdisjoint returns False when sets share an element."""
        t1 = Trie(["a", "b"])
        t2 = Trie(["b", "c"])
        assert not t1.isdisjoint(t2)

    def test_subset_proper(self) -> None:
        """Test __le__ and __lt__."""
        t1 = Trie(["a", "b"])
        t2 = Trie(["a", "b", "c"])
        assert t1 <= t2
        assert t1 < t2
        assert not t2 < t1

    def test_superset_proper(self) -> None:
        """Test __ge__ and __gt__."""
        t1 = Trie(["a", "b", "c"])
        t2 = Trie(["a", "b"])
        assert t1 >= t2
        assert t1 > t2
        assert not t2 > t1

    def test_eq(self) -> None:
        """Test __eq__."""
        t1 = Trie(["a", "b"])
        t2 = Trie(["a", "b"])
        t3 = Trie(["a"])
        assert t1 == t2
        assert t1 != t3
        assert t1 != {"a", "b"}

    def test_union(self) -> None:
        """Test __or__."""
        t1 = Trie(["a", "b"])
        t2 = Trie(["b", "c"])
        result = t1 | t2
        assert isinstance(result, Trie)
        assert set(result) == {"a", "b", "c"}

    def test_union_with_non_trie(self) -> None:
        """Test union with a plain set returns a MutableSet."""
        t1 = Trie(["a", "b"])
        result = t1 | {"b", "c", "d"}
        assert isinstance(result, set)
        assert result == {"a", "b", "c", "d"}

    def test_intersection(self) -> None:
        """Test __and__."""
        t1 = Trie(["a", "b", "c"])
        t2 = Trie(["b", "c", "d"])
        result = t1 & t2
        assert isinstance(result, Trie)
        assert set(result) == {"b", "c"}

    def test_difference(self) -> None:
        """Test __sub__."""
        t1 = Trie(["a", "b", "c"])
        t2 = Trie(["b", "c", "d"])
        result = t1 - t2
        assert isinstance(result, Trie)
        assert set(result) == {"a"}

    def test_symmetric_difference(self) -> None:
        """Test __xor__."""
        t1 = Trie(["a", "b", "c"])
        t2 = Trie(["b", "c", "d"])
        result = t1 ^ t2
        assert isinstance(result, Trie)
        assert set(result) == {"a", "d"}

    def test_symmetric_difference_with_non_trie(self) -> None:
        """Test xor with a plain set returns a Python set."""
        t1 = Trie(["a", "b"])
        result = t1 ^ {"b", "c"}
        assert isinstance(result, set)
        assert result == {"a", "c"}

    def test_inplace_union(self) -> None:
        """Test __ior__."""
        t1 = Trie(["a", "b"])
        t2 = Trie(["b", "c"])
        t1 |= t2
        assert set(t1) == {"a", "b", "c"}

    def test_inplace_intersection(self) -> None:
        """Test __iand__."""
        t1 = Trie(["a", "b", "c"])
        t1 &= {"b", "c", "d"}
        assert set(t1) == {"b", "c"}

    def test_inplace_difference(self) -> None:
        """Test __isub__."""
        t1 = Trie(["a", "b", "c"])
        t1 -= {"b", "d"}
        assert set(t1) == {"a", "c"}

    def test_inplace_symmetric_difference(self) -> None:
        """Test __ixor__."""
        t1 = Trie(["a", "b"])
        t1 ^= {"b", "c"}
        assert set(t1) == {"a", "c"}


class TestTrieEdgeCases:
    """Test edge cases like empty string and deletion that removes intermediate nodes."""

    def test_empty_string_membership(self) -> None:
        """Test containing empty string."""
        t = Trie([EMPTY_STRING])
        assert EMPTY_STRING in t
        t.add("a")
        assert EMPTY_STRING in t
        t.remove(EMPTY_STRING)
        assert EMPTY_STRING not in t

    def test_remove_node_with_shared_prefix(self) -> None:
        """Test removing a word does not delete nodes that are part of other words."""
        t = Trie(["he", "hello"])
        t.remove("he")
        assert "he" not in t
        assert "hello" in t

    def test_remove_last_word_cleans_up_nodes(self) -> None:
        """Test that removing the only word cleans up intermediate nodes."""
        t = Trie(["hello"])
        t.remove("hello")
        assert t._root == {}  # noqa: SLF001
        assert len(t) == 0

    def test_pop_removes_and_cleans_up(self) -> None:
        """Test pop correctly cleans up nodes after removal."""
        t = Trie(["hello", "world"])
        t.pop()
        assert len(t) == 1
        remaining = "world" if "hello" not in t else "hello"
        assert remaining in t

    def test_hash_not_implemented(self) -> None:
        """Test __hash__ raises NotImplementedError."""
        t = Trie()
        with pytest.raises(NotImplementedError):
            hash(t)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
