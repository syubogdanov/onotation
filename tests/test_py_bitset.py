"""Tests for Bitset implementation."""

from __future__ import annotations

import pytest

from onotation.internal.bitset import Bitset


# -----------------------
# Constants (fix PLR2004)
# -----------------------
V1 = 1
V2 = 2
V3 = 3
V4 = 4
V5 = 5
V10 = 10
V20 = 20
V30 = 30
V999 = 999

# length constants (fix PLR2004)
L0 = 0
L1 = 1
L2 = 2
L3 = 3


class TestBitsetInit:
    """Tests for Bitset initialization."""

    def test__init__empty(self) -> None:
        """Empty initialization."""
        bitset = Bitset()
        assert len(bitset) == L0

    def test__init__with_values(self) -> None:
        """Initialization with iterable values."""
        bitset = Bitset([V1, V2, V3])

        assert V1 in bitset
        assert V2 in bitset
        assert V3 in bitset

    def test__init__duplicates(self) -> None:
        """Duplicates are ignored."""
        bitset = Bitset([V1, V1, V2, V2])

        assert len(bitset) == L2
        assert list(bitset) == [V1, V2]


class TestBitsetAdd:
    """Tests for Bitset add."""

    def test__add_single(self) -> None:
        """Add single element."""
        bitset = Bitset()
        bitset.add(V10)

        assert V10 in bitset
        assert len(bitset) == L1

    def test__add_multiple(self) -> None:
        """Add multiple elements."""
        bitset = Bitset()

        bitset.add(V1)
        bitset.add(V2)
        bitset.add(V3)

        assert list(bitset) == [V1, V2, V3]


class TestBitsetRemove:
    """Tests for Bitset remove."""

    def test__remove_existing(self) -> None:
        """Remove existing element."""
        bitset = Bitset([V1, V2, V3])

        bitset.remove(V2)

        assert V2 not in bitset
        assert len(bitset) == L2

    def test__remove_missing(self) -> None:
        """Removing missing element raises KeyError."""
        bitset = Bitset([V1])

        with pytest.raises(KeyError):
            bitset.remove(V999)

    def test__remove_empty(self) -> None:
        """Remove from empty bitset raises KeyError."""
        bitset = Bitset()

        with pytest.raises(KeyError):
            bitset.remove(V1)


class TestBitsetDiscard:
    """Tests for Bitset discard."""

    def test__discard_existing(self) -> None:
        """Discard existing element."""
        bitset = Bitset([V1, V2])

        bitset.discard(V1)

        assert V1 not in bitset
        assert len(bitset) == L1

    def test__discard_missing(self) -> None:
        """Discard missing element is safe."""
        bitset = Bitset([V1])

        bitset.discard(V999)

        assert len(bitset) == L1


class TestBitsetPop:
    """Tests for Bitset pop."""

    def test__pop(self) -> None:
        """Pop returns valid element."""
        bitset = Bitset([V10, V20, V30])

        value = bitset.pop()

        assert value in {V10, V20, V30}
        assert len(bitset) == L2

    def test__pop_empty(self) -> None:
        """Pop from empty raises KeyError."""
        bitset = Bitset()

        with pytest.raises(KeyError):
            bitset.pop()


class TestBitsetClear:
    """Tests for Bitset clear."""

    def test__clear(self) -> None:
        """Clear removes all elements."""
        bitset = Bitset([V1, V2, V3])

        bitset.clear()

        assert len(bitset) == L0
        assert list(bitset) == []


class TestBitsetContains:
    """Tests for Bitset __contains__."""

    def test__contains_existing(self) -> None:
        """Existing element."""
        bitset = Bitset([V1, V2, V3])

        assert V2 in bitset

    def test__contains_missing(self) -> None:
        """Missing element."""
        bitset = Bitset([V1, V2, V3])

        assert V999 not in bitset

    def test__contains_non_int(self) -> None:
        """Non-int values are always False."""
        bitset = Bitset([V1, V2, V3])

        assert "1" not in bitset  # type: ignore[operator]
        assert None not in bitset  # type: ignore[operator]


class TestBitsetIter:
    """Tests for Bitset iteration."""

    def test__iter_empty(self) -> None:
        """Empty iteration."""
        bitset = Bitset()

        assert list(bitset) == []

    def test__iter_sorted(self) -> None:
        """Iteration returns sorted values."""
        bitset = Bitset([V5, V1, V3, V2])

        assert list(bitset) == [V1, V2, V3, V5]

    def test__iter_large(self) -> None:
        """Large dataset iteration."""
        values = list(range(100))
        bitset = Bitset(values)

        assert list(bitset) == values


class TestBitsetReversed:
    """Tests for Bitset reversed iteration."""

    def test__reversed_empty(self) -> None:
        """Empty reversed iteration."""
        bitset = Bitset()

        assert list(reversed(bitset)) == []

    def test__reversed_order(self) -> None:
        """Reversed iteration order."""
        bitset = Bitset([V1, V2, V3, V4])

        assert list(reversed(bitset)) == [V4, V3, V2, V1]


class TestBitsetLen:
    """Tests for Bitset length."""

    def test__len_empty(self) -> None:
        """Empty bitset length."""
        bitset = Bitset()

        assert len(bitset) == L0

    def test__len_values(self) -> None:
        """Length after inserts."""
        bitset = Bitset([V1, V2, V3])

        assert len(bitset) == L3


class TestBitsetSubset:
    """Tests for subset/superset relations."""

    def test__le_true(self) -> None:
        """Subset relation."""
        a = Bitset([V1, V2])
        b = Bitset([V1, V2, V3])

        assert a <= b

    def test__lt_true(self) -> None:
        """Proper subset."""
        a = Bitset([V1, V2])
        b = Bitset([V1, V2, V3])

        assert a < b

    def test__ge_true(self) -> None:
        """Superset relation."""
        a = Bitset([V1, V2, V3])
        b = Bitset([V1, V2])

        assert a >= b

    def test__gt_true(self) -> None:
        """Proper superset."""
        a = Bitset([V1, V2, V3])
        b = Bitset([V1, V2])

        assert a > b


class TestBitsetUnion:
    """Tests for union operator."""

    def test__union_bitset(self) -> None:
        """Union with Bitset."""
        a = Bitset([V1, V2])
        b = Bitset([V2, V3])

        result = a | b

        assert set(result) == {V1, V2, V3}

    def test__union_set(self) -> None:
        """Union with Python set."""
        a = Bitset([V1, V2])

        result = a | {V3, V4}

        assert set(result) == {V1, V2, V3, V4}


class TestBitsetIntersection:
    """Tests for intersection operator."""

    def test__and_bitset(self) -> None:
        """Intersection with Bitset."""
        a = Bitset([V1, V2, V3])
        b = Bitset([V2, V3, V4])

        result = a & b

        assert set(result) == {V2, V3}

    def test__and_set(self) -> None:
        """Intersection with set."""
        a = Bitset([V1, V2, V3])

        result = a & {V2, V3, V5}

        assert set(result) == {V2, V3}


class TestBitsetDifference:
    """Tests for difference operator."""

    def test__sub_bitset(self) -> None:
        """Difference with Bitset."""
        a = Bitset([V1, V2, V3])
        b = Bitset([V2, V3])

        result = a - b

        assert set(result) == {V1}

    def test__sub_set(self) -> None:
        """Difference with set."""
        a = Bitset([V1, V2, V3])

        result = a - {V2, V3}

        assert set(result) == {V1}


class TestBitsetXor:
    """Tests for symmetric difference."""

    def test__xor_bitset(self) -> None:
        """XOR with Bitset."""
        a = Bitset([V1, V2])
        b = Bitset([V2, V3])

        result = a ^ b

        assert set(result) == {V1, V3}

    def test__xor_set(self) -> None:
        """XOR with set."""
        a = Bitset([V1, V2])

        result = a ^ {V2, V3}

        assert set(result) == {V1, V3}


class TestBitsetEq:
    """Tests for equality."""

    def test__eq_bitset(self) -> None:
        """Equal Bitsets."""
        a = Bitset([V1, V2])
        b = Bitset([V1, V2])

        assert a == b

    def test__eq_set(self) -> None:
        """Equality with Python set."""
        a = Bitset([V1, V2])

        assert a == {V1, V2}

    def test__eq_not_equal(self) -> None:
        """Not equal."""
        a = Bitset([V1])
        b = Bitset([V2])

        assert a != b


class TestBitsetHash:
    """Tests for hashing."""

    def test__hash_raises(self) -> None:
        """Bitset is not hashable."""
        bitset = Bitset([V1])

        with pytest.raises(NotImplementedError):
            hash(bitset)
