from __future__ import annotations

import pytest

from onotation.internal.scapegoat_tree import ScapegoatTree


class TestScapegoatTreeInit:
    """Tests for initialization."""

    def test__init__empty(self) -> None:
        """Empty initialization."""
        tree: ScapegoatTree[int] = ScapegoatTree()

        assert len(tree) == 0
        assert list(tree) == []

    def test__init__with_values(self) -> None:
        """Initialization with iterable."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2, 3])

        assert 1 in tree
        assert 2 in tree
        assert 3 in tree

    def test__init__duplicates(self) -> None:
        """Duplicates are ignored."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 1, 2, 2])

        assert len(tree) == 2
        assert list(tree) == [1, 2]

    def test__init__invalid_alpha(self) -> None:
        """Initialization with invalid alpha raises ValueError."""
        with pytest.raises(ValueError, match="Alpha must be in the range"):
            ScapegoatTree(alpha=0.4)

        with pytest.raises(ValueError, match="Alpha must be in the range"):
            ScapegoatTree(alpha=1.0)


class TestScapegoatTreeAdd:
    """Tests for add."""

    def test__add_single(self) -> None:
        """Add single element."""
        tree: ScapegoatTree[int] = ScapegoatTree()

        tree.add(10)

        assert 10 in tree
        assert len(tree) == 1

    def test__add_multiple(self) -> None:
        """Add multiple elements."""
        tree: ScapegoatTree[int] = ScapegoatTree()

        tree.add(3)
        tree.add(1)
        tree.add(2)

        assert list(tree) == [1, 2, 3]

    def test__add_duplicate(self) -> None:
        """Adding duplicate changes nothing."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2])

        tree.add(1)

        assert len(tree) == 2
        assert list(tree) == [1, 2]

    def test__add_incompatible_type(self) -> None:
        """Adding incompatible type raises TypeError."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2])

        with pytest.raises(TypeError):
            tree.add("string")  # type: ignore[arg-type]


class TestScapegoatTreeRemove:
    """Tests for remove."""

    def test__remove_existing(self) -> None:
        """Remove existing element."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2, 3])

        tree.remove(2)

        assert 2 not in tree
        assert list(tree) == [1, 3]

    def test__remove_missing(self) -> None:
        """Removing missing element raises KeyError."""
        tree: ScapegoatTree[int] = ScapegoatTree([1])

        with pytest.raises(KeyError):
            tree.remove(999)

    def test__remove_empty(self) -> None:
        """Remove from empty tree."""
        tree: ScapegoatTree[int] = ScapegoatTree()

        with pytest.raises(KeyError):
            tree.remove(1)

    def test__remove_incompatible_type(self) -> None:
        """Removing incompatible type raises TypeError."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2])

        with pytest.raises(TypeError):
            tree.remove("string")  # type: ignore[arg-type]


class TestScapegoatTreeDiscard:
    """Tests for discard."""

    def test__discard_existing(self) -> None:
        """Discard existing element."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2])

        tree.discard(1)

        assert list(tree) == [2]

    def test__discard_missing(self) -> None:
        """Discard missing element is safe."""
        tree: ScapegoatTree[int] = ScapegoatTree([1])

        tree.discard(999)

        assert list(tree) == [1]

    def test__discard_incompatible_type(self) -> None:
        """Discarding incompatible type raises TypeError."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2])

        with pytest.raises(TypeError):
            tree.discard("string")  # type: ignore[arg-type]


class TestScapegoatTreeClear:
    """Tests for clear."""

    def test__clear(self) -> None:
        """Clear removes all elements."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2, 3])

        tree.clear()

        assert len(tree) == 0
        assert list(tree) == []


class TestScapegoatTreeContains:
    """Tests for __contains__."""

    def test__contains_existing(self) -> None:
        """Existing element."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2, 3])

        assert 2 in tree

    def test__contains_missing(self) -> None:
        """Missing element."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2, 3])

        assert 999 not in tree

    def test__contains_incompatible_type(self) -> None:
        """Incompatible type safely returns False."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2, 3])

        assert "string" not in tree  # type: ignore[comparison-overlap]


class TestScapegoatTreeIter:
    """Tests for iteration."""

    def test__iter_empty(self) -> None:
        """Empty initialization."""
        tree: ScapegoatTree[int] = ScapegoatTree()

        assert list(tree) == []

    def test__iter_sorted(self) -> None:
        """Iteration is sorted."""
        tree: ScapegoatTree[int] = ScapegoatTree([5, 1, 3, 2])

        assert list(tree) == [1, 2, 3, 5]


class TestScapegoatTreeReversed:
    """Tests for reversed iteration."""

    def test__reversed_empty(self) -> None:
        """Empty reversed iteration."""
        tree: ScapegoatTree[int] = ScapegoatTree()

        assert list(reversed(tree)) == []

    def test__reversed_order(self) -> None:
        """Descending iteration."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2, 3, 4])

        assert list(reversed(tree)) == [4, 3, 2, 1]


class TestScapegoatTreeRepr:
    """Tests for repr."""

    def test__repr(self) -> None:
        """Representation format."""
        tree: ScapegoatTree[int] = ScapegoatTree([1, 2])

        assert repr(tree) == "ScapegoatTree([1, 2])"