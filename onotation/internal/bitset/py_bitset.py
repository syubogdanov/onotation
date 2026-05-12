
from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from contextlib import suppress
from typing import Self, cast

BITS_PER_BLOCK = 64


class Bitset(MutableSet[int], Reversible[int]):
    """The bitset."""

    __slots__ = ("_blocks",)

    def __init__(self, iterable: Iterable[int] = (), /) -> None:
        """Initialize the object.

        Parameters
        ----------
        iterable : Iterable[int]
            Iterable.
        """
        self._blocks: list[int] = []
        for element in iterable:
            self.add(element)

    def _reserve(self, blocks: int) -> None:
        """Ensure internal blocks list has at least *blocks* elements."""
        if blocks > len(self._blocks):
            self._blocks.extend([0] * (blocks - len(self._blocks)))

    def _trim(self) -> Self:
        """Remove trailing zero blocks."""
        while self._blocks and self._blocks[-1] == 0:
            self._blocks.pop()
        return self

    def __len__(self) -> int:
        """Return the number of elements in set (cardinality).

        Returns
        -------
        :class:`int`
            Length.
        """
        return sum(block.bit_count() for block in self._blocks)

    def __contains__(self, element: object, /) -> bool:
        """Test ``element`` for membership in the set.

        Parameters
        ----------
        element : object
            Element.

        Returns
        -------
        :class:`bool`
            :obj:`True` if present, otherwise :obj:`False`.
        """
        if not isinstance(element, int):
            return False
        index = element // BITS_PER_BLOCK
        if index >= len(self._blocks):
            return False
        bit = element % BITS_PER_BLOCK
        return bool(self._blocks[index] & (1 << bit))

    def isdisjoint(self, other: Iterable[object], /) -> bool:
        """Return ``True`` if the set has no elements in common with ``other``.

        Sets are disjoint if and only if their intersection is the empty set.

        Parameters
        ----------
        other : Iterable[object]
            Iterable.

        Returns
        -------
        :class:`bool`
            :obj:`True` if disjoint, otherwise :obj:`False`.
        """
        if isinstance(other, Bitset):
            return all(
                lhs & rhs == 0
                for lhs, rhs in zip(self._blocks, other._blocks)
            )
        return all(element not in self for element in other)

    def __le__(self, other: AbstractSet[object], /) -> bool:
        """Test whether every element in the set is in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if subset, otherwise :obj:`False`.
        """
        if isinstance(other, Bitset):
            for index, block in enumerate(self._blocks):
                other_block = (
                    other._blocks[index] if index < len(other._blocks) else 0
                )
                if block & ~other_block:
                    return False
            return True
        return all(el in other for el in self)

    def __lt__(self, other: AbstractSet[object], /) -> bool:
        """Test whether the set is a proper subset of ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if proper subset, otherwise :obj:`False`.
        """
        return self != other and self <= other

    def __ge__(self, other: AbstractSet[object], /) -> bool:
        """Test whether every element in ``other`` is in the set.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if superset, otherwise :obj:`False`.
        """
        return other <= self

    def __gt__(self, other: AbstractSet[object], /) -> bool:
        """Test whether the set is a proper superset of ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        :class:`bool`
            :obj:`True` if proper superset, otherwise :obj:`False`.
        """
        return other < self

    def __or__(self, other: AbstractSet[object], /) -> MutableSet[int]:
        """Return a new set with elements from the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        MutableSet[int]
            Set.
        """
        if isinstance(other, Bitset):
            len_self = len(self._blocks)
            len_other = len(other._blocks)
            n = max(len_self, len_other)

            new_blocks = [0] * n
            for i in range(n):
                a = self._blocks[i] if i < len_self else 0
                b = other._blocks[i] if i < len_other else 0
                new_blocks[i] = a | b

            result = Bitset()
            result._blocks = new_blocks
            return result._trim()

        new_set: set[int] = set(self)
        new_set.update(cast("Iterable[int]", other))
        return new_set

    def __and__(self, other: AbstractSet[object], /) -> Bitset:
        """Return a new set with elements common to the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Bitset
            Bitset.
        """
        if isinstance(other, Bitset):
            min_len = min(len(self._blocks), len(other._blocks))
            new_blocks = [
                self._blocks[i] & other._blocks[i]
                for i in range(min_len)
            ]
            result = Bitset()
            result._blocks = new_blocks
            return result._trim()

        result = Bitset()
        for el in self:
            if el in other:
                result.add(el)
        return result

    def __sub__(self, other: AbstractSet[object], /) -> Bitset:
        """Return a new set with elements in the set that are not in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Bitset
            Bitset.
        """
        if isinstance(other, Bitset):
            new_blocks = [0] * len(self._blocks)
            for i, block in enumerate(self._blocks):
                other_block = (
                    other._blocks[i] if i < len(other._blocks) else 0
                )
                new_blocks[i] = block & ~other_block
            result = Bitset()
            result._blocks = new_blocks
            return result._trim()

        result = Bitset()
        for el in self:
            if el not in other:
                result.add(el)
        return result

    def __xor__(self, other: AbstractSet[object], /) -> MutableSet[int]:
        """Return a new set with elements in either the set or ``other`` but not both.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        MutableSet[int]
            Set.
        """
        if isinstance(other, Bitset):
            len_self = len(self._blocks)
            len_other = len(other._blocks)
            n = max(len_self, len_other)

            new_blocks = [0] * n
            for i in range(n):
                a = self._blocks[i] if i < len_self else 0
                b = other._blocks[i] if i < len_other else 0
                new_blocks[i] = a ^ b

            result = Bitset()
            result._blocks = new_blocks
            return result._trim()

        new_set: set[int] = set(self)
        new_set.symmetric_difference_update(cast("Iterable[int]", other))
        return new_set

    def __ior__(self, other: AbstractSet[int], /) -> Self:  # type: ignore[misc, override]
        """Update the set, adding elements from ``other``.

        Parameters
        ----------
        other : AbstractSet[int]
            Set.

        Returns
        -------
        Self
            self.
        """
        if isinstance(other, Bitset):
            if other._blocks:
                self._reserve(len(other._blocks))
                for i, block in enumerate(other._blocks):
                    self._blocks[i] |= block
                self._trim()
            return self

        for el in other:
            self.add(el)
        return self

    def __iand__(self, other: AbstractSet[object], /) -> Self:
        """Update the set, keeping only elements found in it and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Self
            self.
        """
        if isinstance(other, Bitset):
            min_len = min(len(self._blocks), len(other._blocks))
            self._blocks = [
                self._blocks[i] & other._blocks[i]
                for i in range(min_len)
            ]
            self._trim()
            return self

        to_remove = [el for el in self if el not in other]
        for el in to_remove:
            self.discard(el)
        return self

    def __isub__(self, other: AbstractSet[object], /) -> Self:
        """Update the set, removing elements found in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Self
            self.
        """
        if isinstance(other, Bitset):
            min_len = min(len(self._blocks), len(other._blocks))
            for i in range(min_len):
                self._blocks[i] &= ~other._blocks[i]
            self._trim()
            return self

        for el in other:
            if isinstance(el, int):
                self.discard(el)
        return self

    def __ixor__(self, other: AbstractSet[int], /) -> Self:  # type: ignore[misc, override]
        """Update the set, keeping only elements found in either set, but not in both.

        Parameters
        ----------
        other : AbstractSet[int]
            Set.

        Returns
        -------
        Self
            self.
        """
        if isinstance(other, Bitset):
            if other._blocks:
                self._reserve(len(other._blocks))
                for i, block in enumerate(other._blocks):
                    self._blocks[i] ^= block
                self._trim()
            return self

        for el in other:
            if el in self:
                self.remove(el)
            else:
                self.add(el)
        return self

    def add(self, element: int, /) -> None:
        """Add ``element`` to the set.

        Parameters
        ----------
        element : int
            Element.
        """
        index = element // BITS_PER_BLOCK
        self._reserve(index + 1)
        bit = element % BITS_PER_BLOCK
        self._blocks[index] |= (1 << bit)

    def remove(self, element: int, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : int
            Element.
        """
        index = element // BITS_PER_BLOCK
        if index >= len(self._blocks):
            raise KeyError(element)
        bit = element % BITS_PER_BLOCK
        if not (self._blocks[index] & (1 << bit)):
            raise KeyError(element)
        self._blocks[index] &= ~(1 << bit)
        self._trim()

    def discard(self, element: int, /) -> None:
        """Remove ``element`` from the set if it is present.

        Parameters
        ----------
        element : int
            Element.
        """
        with suppress(KeyError):
            self.remove(element)

    def pop(self) -> int:
        """Remove and return an arbitrary element from the set.

        Returns
        -------
        int
            Element.
        """
        if not self._blocks:
            msg = "pop from an empty set"
            raise KeyError(msg)
        for index, block in enumerate(self._blocks):
            if block:
                bit_pos = 0
                while not (block & (1 << bit_pos)):
                    bit_pos += 1
                value = index * BITS_PER_BLOCK + bit_pos
                self.remove(value)
                return value
        msg = "unreachable"
        raise RuntimeError(msg)

    def clear(self) -> None:
        """Remove all elements from the set."""
        self._blocks.clear()

    def __eq__(self, other: object) -> bool:
        """Test whether the set equals to ``other``.

        Parameters
        ----------
        other : object
            Object.

        Returns
        -------
        :class:`bool`
            :obj:`True` if equal, otherwise :obj:`False`.
        """
        if isinstance(other, Bitset):
            return self._blocks == other._blocks
        if isinstance(other, AbstractSet):
            return len(self) == len(other) and self.__le__(other)
        return NotImplemented

    def __hash__(self) -> int:
        """Return the hash.

        Returns
        -------
        :class:`int`
            Hash.

        Notes
        -----
        * Not defined.
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[int]:
        """Return an iterator.

        Returns
        -------
        Iterator[int]
            Iterator.

        Notes
        -----
        * An ascending order is guaranteed.
        """
        for index, block in enumerate(self._blocks):
            base = index * BITS_PER_BLOCK
            bit_pos = 0
            while bit_pos < BITS_PER_BLOCK:
                if block & (1 << bit_pos):
                    yield base + bit_pos
                bit_pos += 1

    def __reversed__(self) -> Iterator[int]:
        """Return a reverse iterator.

        Returns
        -------
        Iterator[int]
            Iterator.

        Notes
        -----
        * A descending order is guaranteed.
        """
        for index in range(len(self._blocks) - 1, -1, -1):
            block = self._blocks[index]
            base = index * BITS_PER_BLOCK
            bit_pos = BITS_PER_BLOCK - 1
            while bit_pos >= 0:
                if block & (1 << bit_pos):
                    yield base + bit_pos
                bit_pos -= 1
