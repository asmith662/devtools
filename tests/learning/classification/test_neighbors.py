# Copyright (c) 2026
"""Domain refusal of authored invalid adapter outputs; these are not native fits."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.learning.classification.k_nearest_neighbors import (
    FittedKNearestNeighborsClassification,
    KNearestNeighborsClassificationSpecification,
    KNearestNeighborsDistance,
    KNearestNeighborsWeighting,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass
class _Output:
    values: tuple[int, ...] = (0,)

    def predict(self, rows: tuple[tuple[float, ...], ...]) -> tuple[int, ...]:
        """Simulate the untrusted adapter return, retaining real domain validation."""
        del rows
        return self.values


def _fitted() -> FittedKNearestNeighborsClassification:
    return FittedKNearestNeighborsClassification(
        KNearestNeighborsClassificationSpecification(
            7,
            KNearestNeighborsDistance.EUCLIDEAN,
            KNearestNeighborsWeighting.UNIFORM,
        ),
        ("x",),
        (FeatureValueKind.CONTINUOUS,),
        (0, 1),
        _Output(),
    )


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("neighbor_count", 0),
        ("neighbor_count", True),
        ("distance", "euclidean"),
        ("weighting", "uniform"),
    ],
)
def test_neighbor_specification_is_typed(field: str, bad: object) -> None:
    """A name or truth value is not a concrete neighbor method parameter."""
    reconstruct = cast("Callable[..., object]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(_fitted().specification, **{field: bad})


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("specification", None),
        ("feature_names", ()),
        ("feature_names", ("x", "x")),
        ("feature_value_kinds", ()),
        ("feature_value_kinds", ("continuous",)),
        ("categories", (0,)),
        ("categories", (0, 0)),
    ],
)
def test_fitted_neighbor_contract_cannot_erase_its_schema(
    field: str,
    bad: object,
) -> None:
    """Reject invalid class identity, coordinate kinds and original categories."""
    reconstruct = cast("Callable[..., object]", replace)
    with pytest.raises((ValueError, TypeError)):
        reconstruct(_fitted(), **{field: bad})


@pytest.mark.parametrize("output", [(), (2,), (-1,), (True,), (0.0,)])
def test_adapter_output_is_validated_before_category_mapping(
    output: tuple[int, ...],
) -> None:
    """Wrong row counts and unadmitted category indices never escape as predictions."""
    model = replace(_fitted(), _implementation=_Output(output))
    table = FeatureTable(("x",), ((1.0,),), (FeatureValueKind.CONTINUOUS,))
    with pytest.raises(ValueError, match=r"invalid row count|invalid class"):
        model.classify(table)


def test_query_alignment_is_label_free_and_does_not_predict_empty_rows() -> None:
    """Align admitted coordinates, reject missing or changed kinds, and keep empties."""
    model = _fitted()
    table = FeatureTable(
        ("extra", "x"),
        ((9.0, 1.0),),
        (FeatureValueKind.CONTINUOUS,) * 2,
    )
    assert model.classify(table) == (0,)
    assert model.classify(replace(table, rows=())) == ()
    with pytest.raises(ValueError, match="missing"):
        model.classify(
            FeatureTable(("foreign",), ((1.0,),), (FeatureValueKind.CONTINUOUS,)),
        )
    with pytest.raises(ValueError, match="representation-semantic mismatch"):
        model.classify(FeatureTable(("x",), ((1.0,),), (FeatureValueKind.DISCRETE,)))
