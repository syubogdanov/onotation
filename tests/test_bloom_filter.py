from __future__ import annotations

import pytest

from onotation.internal.bloom_filter import BloomFilter


class TestBloomFilterInit:
    """Tests for initialization."""

    def test__init__empty(self) -> None:
        """Empty initialization."""
        filter_: BloomFilter[int] = BloomFilter(m=100, k=3)

        assert filter_.m == 100
        assert filter_.k == 3
        assert len(filter_) == 0

    def test__init__with_values(self) -> None:
        """Initialization with iterable."""
        filter_: BloomFilter[int] = BloomFilter(100, 3, [1, 2, 3])

        assert 1 in filter_
        assert 2 in filter_
        assert 3 in filter_
        assert len(filter_) == 3

    def test__init__duplicates(self) -> None:
        """Duplicates increment the internal item counter."""
        filter_: BloomFilter[int] = BloomFilter(100, 3, [1, 1, 2, 2])

        assert len(filter_) == 4

    def test__init__invalid_m(self) -> None:
        """Initialization with invalid m raises ValueError."""
        with pytest.raises(
            ValueError, match="Filter size \\(m\\) must be greater than 0",
        ):
            BloomFilter(m=0, k=3)

        with pytest.raises(
            ValueError, match="Filter size \\(m\\) must be greater than 0",
        ):
            BloomFilter(m=-10, k=3)

    def test__init__invalid_k(self) -> None:
        """Initialization with invalid k raises ValueError."""
        with pytest.raises(
            ValueError,
            match="Number of hash functions \\(k\\) must be greater than 0",
        ):
            BloomFilter(m=100, k=0)

        with pytest.raises(
            ValueError,
            match="Number of hash functions \\(k\\) must be greater than 0",
        ):
            BloomFilter(m=100, k=-1)


class TestBloomFilterAdd:
    """Tests for add."""

    def test__add_single(self) -> None:
        """Add single element."""
        filter_: BloomFilter[int] = BloomFilter(100, 3)

        filter_.add(10)

        assert 10 in filter_
        assert len(filter_) == 1

    def test__add_multiple(self) -> None:
        """Add multiple elements."""
        filter_: BloomFilter[int] = BloomFilter(100, 3)

        filter_.add(3)
        filter_.add(1)
        filter_.add(2)

        assert 1 in filter_
        assert 2 in filter_
        assert 3 in filter_
        assert len(filter_) == 3

    def test__add_duplicate(self) -> None:
        """Adding duplicate increments the internal counter."""
        filter_: BloomFilter[int] = BloomFilter(100, 3, [1, 2])

        filter_.add(1)

        assert len(filter_) == 3
        assert 1 in filter_

    def test__add_incompatible_type(self) -> None:
        """Adding unhashable type raises TypeError."""
        filter_: BloomFilter[list[int]] = BloomFilter(100, 3)

        with pytest.raises(TypeError, match="BloomFilter elements must be hashable"):
            filter_.add([1, 2])  # type: ignore[arg-type]


class TestBloomFilterClear:
    """Tests for clear."""

    def test__clear(self) -> None:
        """Clear resets the filter and counter."""
        filter_: BloomFilter[int] = BloomFilter(100, 3, [1, 2, 3])

        filter_.clear()

        assert len(filter_) == 0
        assert 1 not in filter_
        assert 2 not in filter_
        assert 3 not in filter_


class TestBloomFilterContains:
    """Tests for __contains__."""

    def test__contains_existing(self) -> None:
        """Existing element."""
        filter_: BloomFilter[int] = BloomFilter(100, 3, [1, 2, 3])

        assert 2 in filter_

    def test__contains_missing(self) -> None:
        """Missing element."""
        filter_: BloomFilter[int] = BloomFilter(100, 3, [1, 2, 3])

        assert 999 not in filter_

    def test__contains_incompatible_type(self) -> None:
        """Unhashable or incompatible type safely returns False."""
        filter_: BloomFilter[int] = BloomFilter(100, 3, [1, 2, 3])

        assert [1, 2] not in filter_  # type: ignore[comparison-overlap]
        assert "string" not in filter_  # type: ignore[comparison-overlap]
