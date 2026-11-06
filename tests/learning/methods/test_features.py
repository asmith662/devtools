# Copyright (c) 2026
"""Authored algebraic controls for the admitted SQUARE map and recipe refusal."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.learning.methods.features import (
    SQUARES,
    FeatureOperator,
    FeatureRecipe,
    transform_features,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind

if TYPE_CHECKING:
    from collections.abc import Callable


def _replace[T](original: T, **changes: object) -> T:
    """Exercise deliberately invalid runtime constructors in tests."""
    return cast("Callable[..., T]", replace)(original, **changes)


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"name": ""}, "nonempty"),
        ({"input_semantics": ""}, "nonempty"),
        ({"output_semantics": ""}, "nonempty"),
        ({"version": True}, "positive"),
        ({"version": 0}, "positive"),
        ({"order": True}, "nonnegative"),
        ({"order": -1}, "nonnegative"),
        ({"incompatible_with": []}, "immutable"),
        ({"incompatible_with": ("x", "x")}, "immutable"),
        ({"incompatible_with": ("",)}, "nonempty"),
    ],
)
def test_operator_metadata_is_an_immutable_contract(
    changes: dict[str, object],
    reason: str,
) -> None:
    """Invalid metadata cannot enter the finite recipe, even without execution."""
    with pytest.raises(ValueError, match=reason):
        _replace(SQUARES, **changes)


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"catalog_identity": ""}, "nonempty"),
        ({"construction_rule": "foreign"}, "construction"),
        ({"operators": []}, "immutable"),
        ({"operators": ()}, "nonempty"),
        ({"operators": (object(),)}, "typed"),
        ({"operators": (SQUARES, SQUARES)}, "duplicate"),
        ({"operators": (replace(SQUARES, input_semantics="foreign"),)}, "incompatible"),
        (
            {"operators": (replace(SQUARES, incompatible_with=(SQUARES.identity,)),)},
            "incompatible",
        ),
        ({"operators": (replace(SQUARES, name="z", order=1), SQUARES)}, "noncanonical"),
    ],
)
def test_recipe_refuses_foreign_or_incompatible_semantics(
    changes: dict[str, object],
    reason: str,
) -> None:
    """A recipe identity does not authorize unsupported composition."""
    with pytest.raises((ValueError, TypeError), match=reason):
        _replace(FeatureRecipe("authored", (SQUARES,)), **changes)


def test_square_uses_original_coordinates_and_preserves_row_order() -> None:
    """Independently specified products retain original values and never recurse."""
    table = FeatureTable(
        ("a", "b"),
        ((2.0, -3.0), (-1.0, 0.0)),
        (FeatureValueKind.CONTINUOUS,) * 2,
    )
    recipe = FeatureRecipe("authored", (SQUARES,))
    result = transform_features(table, recipe, maximum_dimension=4)
    assert result.rows == ((2.0, -3.0, 4.0, 9.0), (-1.0, 0.0, 1.0, 0.0))
    assert result.feature_names == (
        "a",
        "b",
        "append_squared_features_v1[0,0]:a*a",
        "append_squared_features_v1[1,1]:b*b",
    )
    assert recipe.identity == "feature-recipe-v1:" + recipe.content_identity
    assert replace(recipe, catalog_identity="other").identity != recipe.identity
    empty = replace(table, rows=())
    assert transform_features(empty, recipe, maximum_dimension=4).rows == ()


@pytest.mark.parametrize("budget", [0, -1, True, 1])
def test_square_refuses_invalid_or_insufficient_budget(budget: int) -> None:
    """No expanded state is produced when its exact dimension exceeds authority."""
    table = FeatureTable(("x",), ((2.0,),), (FeatureValueKind.CONTINUOUS,))
    with pytest.raises(ValueError, match="dimension"):
        transform_features(
            table,
            FeatureRecipe("authored", (SQUARES,)),
            maximum_dimension=budget,
        )


def test_metadata_is_not_executable_implementation_authority() -> None:
    """A well-formed new operator is still unsupported by the installed portfolio."""
    table = FeatureTable(("x",), ((2.0,),), (FeatureValueKind.CONTINUOUS,))
    unknown: FeatureOperator = replace(SQUARES, name="foreign")
    with pytest.raises(ValueError, match="approved executable"):
        transform_features(
            table,
            FeatureRecipe("authored", (unknown,)),
            maximum_dimension=2,
        )


@pytest.mark.parametrize(
    ("table", "reason"),
    [
        (FeatureTable((), ((),), ()), "nonempty"),
        (FeatureTable(("x",), ((1.0,),), (FeatureValueKind.DISCRETE,)), "continuous"),
        (
            FeatureTable(("x",), ((1e308,),), (FeatureValueKind.CONTINUOUS,)),
            "nonfinite",
        ),
        (
            FeatureTable(
                ("x", "append_squared_features_v1[0,0]:x*x"),
                ((1.0, 2.0),),
                (FeatureValueKind.CONTINUOUS,) * 2,
            ),
            "identities",
        ),
    ],
)
def test_square_refuses_inapplicable_or_unrepresentable_input(
    table: FeatureTable,
    reason: str,
) -> None:
    """Keep semantic, overflow and output-identity failures explicit."""
    with pytest.raises(ValueError, match=reason):
        transform_features(
            table,
            FeatureRecipe("authored", (SQUARES,)),
            maximum_dimension=4,
        )
