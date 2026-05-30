from __future__ import annotations

from collections.abc import Container, Iterable
from typing import Generic, TypeVar


BITS_PER_BLOCK = 64
T = TypeVar("T")


class BloomFilter(Container[T], Generic[T]):
    """The Bloom filter."""

    __slots__ = ("_blocks", "_k", "_m", "_n")

    def __init__(self, m: int, k: int, iterable: Iterable[T] = (), /) -> None:
        """Initialize the object.

        Parameters
        ----------
        m : int
            The number of bits in the filter.
        k : int
            The number of hash functions.
        iterable : Iterable[T], optional
            Initial elements to add to the filter.
        """
        if m <= 0:
            message = "Filter size (m) must be greater than 0"
            raise ValueError(message)
        if k <= 0:
            message = "Number of hash functions (k) must be greater than 0"
            raise ValueError(message)

        self._m: int = m
        self._k: int = k
        self._n: int = 0

        num_blocks = (m + BITS_PER_BLOCK - 1) // BITS_PER_BLOCK
        self._blocks: list[int] = [0] * num_blocks

        for element in iterable:
            self.add(element)

    @property
    def m(self) -> int:
        """Return the total number of bits (capacity)."""
        return self._m

    @property
    def k(self) -> int:
        """Return the number of hash functions."""
        return self._k

    def __len__(self) -> int:
        """Return the number of unique elements added to the filter.

        Returns
        -------
        int
            The number of added elements.
        """
        return self._n

    def _hash_indices(self, element: T) -> list[int]:
        """Generate k deterministic bit indices for the given element."""
        h1 = hash(element)
        h2 = hash((h1, element))

        indices: list[int] = []
        for i in range(self._k):
            idx = (h1 + i * h2) % self._m
            indices.append(idx)
        return indices

    def __contains__(self, element: object, /) -> bool:
        """Test ``element`` for potential membership in the filter.

        Parameters
        ----------
        element : object
            Element.

        Returns
        -------
        bool
            True if the element might be in the filter, False if it is definitely not.
        """
        try:
            indices = self._hash_indices(element)  # type: ignore[arg-type]
        except TypeError:
            return False

        for idx in indices:
            block_idx = idx // BITS_PER_BLOCK
            bit_pos = idx % BITS_PER_BLOCK
            if not (self._blocks[block_idx] & (1 << bit_pos)):
                return False

        return True

    def add(self, element: T, /) -> None:
        """Add ``element`` to the Bloom filter.

        Parameters
        ----------
        element : T
            Element.
        """
        try:
            indices = self._hash_indices(element)
        except TypeError as err:
            message = f"BloomFilter elements must be hashable, got {type(element).__name__}"
            raise TypeError(message) from err

        for idx in indices:
            block_idx = idx // BITS_PER_BLOCK
            bit_pos = idx % BITS_PER_BLOCK
            self._blocks[block_idx] |= (1 << bit_pos)

        self._n += 1

    def clear(self) -> None:
        """Remove all elements from the filter by resetting bits to zero."""
        for i in range(len(self._blocks)):
            self._blocks[i] = 0
        self._n = 0
