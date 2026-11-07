# Copyright (c) 2026
"""Check numeric/schema refusals and type-preserving target identities."""

from typing import cast

import pytest

from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.targets import (
    CategoryValue,
    category_identity,
    validate_category_values,
)


def test_features_retain_finite_ordered_values() -> None:
    """Feature identity and numeric values remain independent."""
    table = FeatureTable(("x",), ((3.0,),), (FeatureValueKind.CONTINUOUS,))
    assert table.observation_count == 1
    assert table.rows == ((3.0,),)
    assert table.feature_names == ("x",)


@pytest.mark.parametrize(
    ("names", "rows", "kinds", "error"),
    [
        ((" ",), (), (FeatureValueKind.CONTINUOUS,), ValueError),
        (("x", "x"), (), (FeatureValueKind.CONTINUOUS,) * 2, ValueError),
        (("x",), (), (), ValueError),
        (("x",), (), ("continuous",), TypeError),
        (("x",), ((1.0, 2.0),), (FeatureValueKind.CONTINUOUS,), ValueError),
        (("x",), ((True,),), (FeatureValueKind.CONTINUOUS,), TypeError),
        (("x",), ((object(),),), (FeatureValueKind.CONTINUOUS,), TypeError),
        (("x",), ((float("nan"),),), (FeatureValueKind.CONTINUOUS,), ValueError),
    ],
)
def test_bad_features_refuse(
    names: tuple[str, ...],
    rows: tuple[tuple[object, ...], ...],
    kinds: tuple[object, ...],
    error: type[Exception],
) -> None:
    """Refuse malformed schemas and values before any backend exists."""
    with pytest.raises(error):
        FeatureTable(names, rows, kinds)  # type: ignore[arg-type]


def test_categories_preserve_exact_scalar_types() -> None:
    """Python equal numeric scalars remain scientifically distinct categories."""
    values: tuple[CategoryValue, ...] = ("one", 1, 1.0, True)
    assert validate_category_values(values) == values
    assert len({category_identity(v) for v in values}) == len(values)
    assert validate_category_values(()) == ()


@pytest.mark.parametrize("value", [None, (), object(), float("inf")])
def test_invalid_category(value: object) -> None:
    """Unknown category types and nonfinite numbers have no silent encoding."""
    with pytest.raises((ValueError, TypeError)):
        validate_category_values((cast("CategoryValue", value),))
