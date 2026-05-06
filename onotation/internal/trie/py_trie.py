from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSet, Reversible
from collections.abc import Set as AbstractSet
from typing import Self, TypeVar, overload, Any


Q = TypeVar("Q")

_TERMINAL = None


class Trie(MutableSet[str], Reversible[str]):
    __slots__ = ("_root", "_size")

    def __init__(self, iterable: Iterable[str] = (), /) -> None:
        self._root: dict[str | None, Any] = {}
        self._size = 0
        for item in iterable:
            self.add(item)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, element: object, /) -> bool:
        if not isinstance(element, str):
            return False
        node: dict[str | None, Any] = self._root
        for char in element:
            if char not in node:
                return False
            node = node[char]      
        return node.get(_TERMINAL, False)

    def isdisjoint(self, other: Iterable[object], /) -> bool:
        for element in other:
            if element in self:
                return False
        return True

    def __le__(self, other: AbstractSet[object], /) -> bool:
        for element in self:
            if element not in other:
                return False
        return True

    def __lt__(self, other: AbstractSet[object], /) -> bool:
        return self <= other and any(element in self for element in other)

    def __ge__(self, other: AbstractSet[object], /) -> bool:
        for element in other:
            if element not in self:
                return False
        return True

    def __gt__(self, other: AbstractSet[object], /) -> bool:
        return self >= other and any(element in other for element in self)

    @overload
    def __or__(self, other: Trie, /) -> Trie: ...

    @overload
    def __or__(self, other: AbstractSet[Q], /) -> MutableSet[str | Q]: ...

    def __or__(self, other: AbstractSet[Any], /) -> Any:
        if isinstance(other, Trie):
            result = Trie()
            for elem in self:
                result.add(elem)
            for elem in other:
                result.add(elem)
            return result
        return set(self) | set(other)



    def __and__(self, other: AbstractSet[object], /) -> Trie:
        result = Trie()
        for element in self:
            if element in other:
                result.add(element)
        return result

    def __sub__(self, other: AbstractSet[object], /) -> Trie:
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
        for element in other:
            self.add(element)
        return self

    def __iand__(self, other: AbstractSet[object], /) -> Self:
        removing: list[str] = []
        for element in self:
            if element not in other:
                removing.append(element)
        for element in removing:
            self.discard(element)
        return self

    def __isub__(self, other: AbstractSet[object], /) -> Self:
        for element in other:
            if isinstance(element, str):
                self.discard(element)
        return self

    def __ixor__(self, other: AbstractSet[str], /) -> Self:  # type: ignore[misc, override]
        for element in other:
            if element in self:
                self.remove(element)
            else:
                self.add(element)
        return self

    def add(self, element: str, /) -> None:
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
        for element in self:
            self.remove(element)
            return element
        raise KeyError

    def clear(self) -> None:
        """Remove all elements from the set."""
        self._root.clear()
        self._size = 0

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, AbstractSet):
            return False
        return all(elem in other for elem in self) and all(
            elem in self for elem in other
        )
    
    def __hash__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        stack: list[tuple[dict[str | None, Any], str]] = [(self._root, "")]
        while stack:
            node, prefix = stack.pop()
            if _TERMINAL in node:
                yield prefix

            children = [char for char in node if char is not _TERMINAL]
            for char in sorted(children, reverse=True):
                stack.append((node[char], prefix + char))

    def __reversed__(self) -> Iterator[str]:
        stack: list[tuple[dict[str | None, Any], str]] = [(self._root, "")]
        while stack:
            node, prefix = stack.pop()
            if _TERMINAL in node:
                yield prefix

            children = [char for char in node if char is not _TERMINAL]
            for char in sorted(children):
                stack.append((node[char], prefix + char))
