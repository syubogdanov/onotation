from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from typing import Self, TypeVar, overload, Any


Q = TypeVar("Q")


class Trie(MutableSet[str], Reversible[str]):
    """The trie."""

    def __init__(self, iterable: Iterable[str] = (), /) -> None:
        """Initialize the object.

        Parameters
        ----------
        iterable : Iterable[T]
            Iterable.
        """
        self._root: dict[str, Any] = {}
        self._count = 0
        for word in iterable:
            self.add(word)

    def __len__(self) -> int:
        """Return the number of elements in set (cardinality).

        Returns
        -------
        :class:`int`
            Length.
        """

        return self._count

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
        if not isinstance(element, str):
            return False
        node = self._root
        for char in element:
            if char not in node:
                return False
            node = node[char]

        return node.get("*", False)

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
        for element in other:
            if element in self:
                return False
        return True

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
        if len(self) > len(other):
            return False
        for element in self:
            if element not in other:
                return False
        return True

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
        return len(self) < len(other) and self <= other

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
        if len(self) < len(other):
            return False
        for element in other:
            if element not in self:
                return False
        return True

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
        return len(self) > len(other) and self >= other

    @overload
    def __or__(self, other: Trie, /) -> Trie: ...

    @overload
    def __or__(self, other: AbstractSet[Q], /) -> MutableSet[str | Q]: ...

    def __or__(self, other: AbstractSet[Q], /) -> MutableSet[str | Q]:
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

    def __xor__(self, other: AbstractSet[Q], /) -> MutableSet[str | Q]:
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
        removing = []
        for element in self:
            if element not in other:
                removing.append(element)
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
        """Update the set, keeping only elements found in either set, 
        but not in both.

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
            if not self._root.get("*", False):
                self._root["*"] = True
                self._count += 1
            return
        node = self._root
        for char in element:
            if char not in node:
                node[char] = {}
            node = node[char]

        if not node.get("*", False):
            node["*"] = True
            self._count += 1

    def remove(self, element: str, /) -> None:
        """Remove ``element`` from the set.

        Parameters
        ----------
        element : str
            Element.
        """
        if element not in self:
            raise KeyError
        nodes = []
        node = self._root

        for char in element:
            nodes.append((node, char))
            node = node[char]
        
        if node.get("*", False):
            del node["*"]
            self._count -= 1
        
        while nodes and not node and "*" not in node:
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
        if element in self:
            self.remove(element)

    def pop(self) -> str:
        """Remove and return an arbitrary element from the set.

        Returns
        -------
        str
            Element.
        """
        if self._count == 0:
            raise KeyError
        for element in self:
            self.remove(element)
            return element
        raise RuntimeError

    def clear(self) -> None:
        """Remove all elements from the set."""
        self._root.clear()
        self._count = 0

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
        if self is other:
            return True
        if not isinstance(other, AbstractSet):
            return False
        if len(self) != len(other):
            return False
        
        for element in self:
            if element not in other:
                return False
        return True
    
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
        raise TypeError

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
        stack = [(self._root, "")]
        while stack:
            node, prefix = stack.pop()
            if node.get("*", False):
                yield prefix
            
            children = [char for char in node if char != "*"]
            for char in sorted(children, reverse=True):
                stack.append((node[char], prefix + char))

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
        return iter(sorted(self, reverse=True))
