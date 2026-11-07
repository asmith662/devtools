# Copyright (c) 2026
"""Finite reference-profile choices from authored observations, without fitting."""

from __future__ import annotations

from dataclasses import asdict, replace

import pytest

from devtools.agents.learning.policy import (
    PROFILE,
    best_index,
    decision,
    support_profile,
)
from devtools.learning.investigation.plans import canonical
from devtools.learning.investigation.proposals import LearningFeedback, LearningProposal
from devtools.learning.representation.features import FeatureTable, FeatureValueKind


def _observations(
    family: str,
    values: tuple[float | None, ...],
) -> list[LearningFeedback]:
    metric = (
        "classification.macro_f1:v1"
        if family == "classification"
        else "regression.mae:v1"
    )
    return [
        LearningFeedback(
            "EVALUATE",
            "method-" + str(i),
            metric,
            value,
            "authored-evidence-" + str(i),
        )
        for i, value in enumerate(values)
    ]


@pytest.mark.parametrize(
    ("family", "values", "index"),
    [
        ("classification", (), None),
        ("classification", (None,), None),
        ("classification", (0.6, 0.6), 0),
        ("classification", (0.6, 0.7), 1),
        ("regression", (3.0, 3.0), 0),
        ("regression", (3.0, 2.0), 1),
    ],
)
def test_reference_comparison_retains_ties_and_missing_values(
    family: str,
    values: tuple[float | None, ...],
    index: int | None,
) -> None:
    """Compare admitted values and retain the original incumbent on ties."""
    assert best_index(family, _observations(family, values)) == index


@pytest.mark.parametrize(
    ("values", "changed", "expected"),
    [
        ((), False, ("EVALUATE", "knn7")),
        ((0.6,), False, ("EVALUATE", "square-logistic")),
        ((0.6,), True, ("ABSTAIN", None)),
        ((0.6, 0.6), False, ("STOP", None)),
        ((0.6, 0.7), False, ("EVALUATE", "square-margin")),
        ((0.6, 0.7, 0.8), False, ("STOP", None)),
        ((None,), False, ("ABSTAIN", None)),
    ],
)
def test_profile_decision_uses_new_evidence(
    values: tuple[float | None, ...],
    *,
    changed: bool,
    expected: tuple[str, str | None],
) -> None:
    """Distinguish continuation, stopping and abstention from new evidence."""
    support: dict[str, object] = {
        "changed_constant_coordinates": ["constant"] if changed else [],
    }
    methods = ("knn7", "square-logistic", "square-margin")
    assert (
        decision(
            "classification",
            methods,
            _observations("classification", values),
            support,
            profile=PROFILE,
        )
        == expected
    )
    assert decision("classification", methods, [], None, profile=PROFILE) == (
        "CHECK_SUPPORT",
        None,
    )
    with pytest.raises(ValueError, match="explicitly select"):
        decision("classification", methods, [], None, profile="automatic")


def test_geometry_is_not_accepted_predictive_effectiveness() -> None:
    """Keep support changes factual while effectiveness remains explicitly unknown."""
    training = FeatureTable(
        ("x", "constant"),
        ((0.0, 2.0), (1.0, 2.0)),
        (FeatureValueKind.CONTINUOUS,) * 2,
    )
    later = replace(training, rows=((2.0, 3.0),))
    assert support_profile(training, later) == {
        "changed_constant_coordinates": ["constant"],
        "outside_training_box": ["x", "constant"],
        "effectiveness": "UNKNOWN",
    }
    with pytest.raises(ValueError, match="exact input support schema"):
        support_profile(training, replace(later, feature_names=("foreign", "constant")))


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("rationale", None),
        ("rationale", "x" * 1025),
        ("evidence", ["duplicate", "duplicate"]),
        ("evidence", [str(i) for i in range(6)]),
    ],
)
def test_proposal_text_does_not_expand_admitted_evidence(
    field: str,
    bad: object,
) -> None:
    """A rationale remains untrusted bounded text, with closed evidence membership."""
    proposal = LearningProposal(
        "authored-task",
        "source-handle",
        "classification",
        "classification.macro_f1:v1",
        "schema",
        "unit",
        "online",
        "state",
        (),
        "CHECK_SUPPORT",
        None,
        "authored rationale",
    )
    data = asdict(proposal)
    data[field] = bad
    with pytest.raises(ValueError, match=r"bounded textual|bounded unique"):
        LearningProposal.materialize(canonical(data))
