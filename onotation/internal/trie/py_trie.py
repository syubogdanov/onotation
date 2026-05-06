from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible, Set as AbstractSet
from typing import Any, Self, TypeVar, overload

Q = TypeVar("Q")

_TERMINAL = None


class Trie(MutableSet[str], Reversible[str]):
    """The trie."""

    __slots__ = ("_root", "_size")

    def __init__(self, iterable: Iterable[str] = (), /) -> None:
        """Initialize the object.

        Parameters
        ----------
        iterable : Iterable[str]
            Iterable.
        """
        self._root: dict[str | None, Any] = {}
        self._size = 0
        for item in iterable:
            self.add(item)

    def __len__(self) -> int:
        """Return the number of elements in the set (cardinality).

        Returns
        -------
        int
            Length.
        """
        return self._size

    def __contains__(self, element: object, /) -> bool:
        """Test ``element`` for membership in the set.

        Parameters
        ----------
        element : object
            Element.

        Returns
        -------
        bool
            :obj:`True` if present, otherwise :obj:`False`.
        """
        if not isinstance(element, str):
            return False
        node: dict[str | None, Any] = self._root
        for char in element:
            if char not in node:
                return False
            node = node[char]
        return node.get(_TERMINAL, False)

    def isdisjoint(self, other: Iterable[object], /) -> bool:
        """Return ``True`` if the set has no elements in common with ``other``.

        Sets are disjoint if and only if their intersection is the empty set.

        Parameters
        ----------
        other : Iterable[object]
            Iterable.

        Returns
        -------
        bool
            :obj:`True` if disjoint, otherwise :obj:`False`.
        """
        return all(element not in self for element in other)

    def __le__(self, other: AbstractSet[object], /) -> bool:
        """Test whether every element in the set is in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        bool
            :obj:`True` if subset, otherwise :obj:`False`.
        """
        return all(element in other for element in self)

    def __lt__(self, other: AbstractSet[object], /) -> bool:
        """Test whether the set is a proper subset of ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        bool
            :obj:`True` if proper subset, otherwise :obj:`False`.
        """
        return self <= other and any(element in self for element in other)

    def __ge__(self, other: AbstractSet[object], /) -> bool:
        """Test whether every element in ``other`` is in the set.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        bool
            :obj:`True` if superset, otherwise :obj:`False`.
        """
        return all(element in self for element in other)

    def __gt__(self, other: AbstractSet[object], /) -> bool:
        """Test whether the set is a proper superset of ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        bool
            :obj:`True` if proper superset, otherwise :obj:`False`.
        """
        return self >= other and any(element in other for element in self)

    @overload
    def __or__(self, other: Trie, /) -> Trie: ...

    @overload
    def __or__(self, other: AbstractSet[Q], /) -> MutableSet[str | Q]: ...

    def __or__(self, other: AbstractSet[Any], /) -> Any:
        """Return a new set with elements from the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[Q]
            Set.

        Returns
        -------
        MutableSet[str | Q]
            Set.
        """
        if isinstance(other, Trie):
            result = Trie()
            for elem in self:
                result.add(elem)
            for elem in other:
                result.add(elem)
            return result
        return set(self) | set(other)

    def __and__(self, other: AbstractSet[object], /) -> Trie:
        """Return a new set with elements common to the set and ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Trie
            Trie.
        """
        result = Trie()
        for element in self:
            if element in other:
                result.add(element)
        return result

    def __sub__(self, other: AbstractSet[object], /) -> Trie:
        """Return a new set with elements in the set that are not in ``other``.

        Parameters
        ----------
        other : AbstractSet[object]
            Set.

        Returns
        -------
        Trie
            Trie.
        """
        result = Trie()
        for element in self:
            if element not in other:
                result.add(element)
        return result

    @overload
    def __xor__(self, other: Trie, /) -> Trie: ...

    @overload
    def __xor__(self, other: AbstractSet[Q], /) -> MutableSet[str | Q]: ...

    def __xor__(self, other: AbstractSet[Any], /) -> Any:
        """Return a new set with elements in either the set or ``other`` but not both.

        Parameters
        ----------
        other : AbstractSet[Q]
            Set.

        Returns
        -------
        MutableSet[str | Q]
            Set.
        """
        if isinstance(other, Trie):
            result = Trie()
            for elem in self:
                if elem not in other:
                    result.add(elem)
            for elem in other:
                if elem not in self:
                    result.add(elem)
            return result
        return set(self) ^ set(other)

    def __ior__(self, other: AbstractSet[str], /) -> Self:  # type: ignore[misc, override]
        """Update the set, adding elements from ``other``.

        Parameters
        ----------
        other : AbstractSet[str]
            Set.

        Returns
        -------
        Self
            self.
        """
        for element in other:
            self.add(element)
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
        removing = [element for element in self if element not in other]
        for element in removing:
            self.discard(element)
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
        for element in other:
            if isinstance(element, str):
                self.discard(element)
        return self

    def __ixor__(self, other: AbstractSet[str], /) -> Self:  # type: ignore[misc, override]
        """Update the set, keeping only elements found in either set, but not in both.

        Parameters
        ----------
        other : AbstractSet[str]
            Set.

        Returns
        -------
        Self
            self.
        """
        for element in other:
            if element in self:
                self.remove(element)
            else:
                self.add(element)
        return self

    def add(self, element: str, /) -> None:
        """Add ``element`` to the set.

        Parameters
        ----------
        element : str
            Element.
        """
        if element == "":
            if _TERMINAL not in self._root:
                self._root[_TERMINAL] = True
                self._size += 1
            return

        node: dict[str | None, Any] = self._root
        for char in element:
            node = node.setdefault(char, {})
        if _TERMINAL not in node:
            node[_TERMINAL] = True
            self._size += 1

    def remove(self, element: str, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : str
            Element.

        Raises
        ------
        KeyError
            If the element is not present.
        """
        node: dict[str | None, Any] = self._root
        nodes: list[tuple[dict[str | None, Any], str]] = []
        for char in element:
            if char not in node:
                raise KeyError(element)
            nodes.append((node, char))
            node = node[char]

        if _TERMINAL not in node:
            raise KeyError(element)

        del node[_TERMINAL]
        self._size -= 1

        while nodes and not node and _TERMINAL not in node:
            parent, char = nodes.pop()
            del parent[char]
            node = parent

    def discard(self, element: str, /) -> None:
        """Remove ``element`` from the set if it is present.

        Parameters
        ----------
        element : str
            Element.
        """
        node: dict[str | None, Any] = self._root
        nodes: list[tuple[dict[str | None, Any], str]] = []
        for char in element:
            if char not in node:
                return
            nodes.append((node, char))
            node = node[char]

        if _TERMINAL not in node:
            return

        del node[_TERMINAL]
        self._size -= 1

        while nodes and not node and _TERMINAL not in node:
            parent, char = nodes.pop()
            del parent[char]
            node = parent

    def pop(self) -> str:
        """Remove and return an arbitrary element from the set.

        Returns
        -------
        str
            Element.

        Raises
        ------
        KeyError
            If the set is empty.
        """
        for element in self:
            self.remove(element)
            return element
        raise KeyError

    def clear(self) -> None:
        """Remove all elements from the set."""
        self._root.clear()
        self._size = 0

    def __eq__(self, other: object) -> bool:
        """Test whether the set equals to ``other``.

        Parameters
        ----------
        other : object
            Object.

        Returns
        -------
        bool
            :obj:`True` if equal, otherwise :obj:`False`.
        """
        if self is other:
            return True
        if not isinstance(other, AbstractSet):
            return False
        return all(elem in other for elem in self) and all(
            elem in self for elem in other
        )

    def __hash__(self) -> int:
        """Return the hash.

        Returns
        -------
        int
            Hash.

        Notes
        -----
        * Not defined.
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        """Return an iterator.

        Returns
        -------
        Iterator[str]
            Iterator.

        Notes
        -----
        * An ascending order is guaranteed.
        """
        stack: list[tuple[dict[str | None, Any], str]] = [(self._root, "")]
        while stack:
            node, prefix = stack.pop()
            if _TERMINAL in node:
                yield prefix

            children = [char for char in node if char is not _TERMINAL]
            stack.extend(
                (node[char], prefix + char) for char in sorted(children, reverse=True)
            )

    def __reversed__(self) -> Iterator[str]:
        """Return a reverse iterator.

        Returns
        -------
        Iterator[str]
            Iterator.

        Notes
        -----
        * A descending order is guaranteed.
        """
        stack: list[tuple[dict[str | None, Any], str]] = [(self._root, "")]
        while stack:
            node, prefix = stack.pop()
            if _TERMINAL in node:
                yield prefix

            children = [char for char in node if char is not _TERMINAL]
            stack.extend(
                (node[char], prefix + char) for char in sorted(children)
            )
