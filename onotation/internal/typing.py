from typing import Protocol, TypeVar, runtime_checkable


T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class SupportsBool(Protocol):
    """An ABC with one abstract method ``__bool__``."""

    def __bool__(self) -> bool:
        """Cast an object to ``bool``."""


@runtime_checkable
class SupportsDunderLT(Protocol[T_contra]):
    """An ABC with one abstract method ``__lt__``."""

    def __lt__(self, other: T_contra, /) -> SupportsBool:
        """Perform less-than comparison."""


@runtime_checkable
class SupportsDunderGT(Protocol[T_contra]):
    """An ABC with one abstract method ``__gt__``."""

    def __gt__(self, other: T_contra, /) -> SupportsBool:
        """Perform greater-than comparison."""
