# Copyright (c) 2026
"""Explicit B-0096 engineering comparison profile; no universal strategy default."""

from __future__ import annotations

from devtools.learning.investigation.proposals import LearningFeedback
from devtools.learning.representation.features import FeatureTable

PROFILE = "b0096-engineering-v1"


def support_profile(training: FeatureTable, later: FeatureTable) -> dict[str, object]:
    """Describe exact input geometry without claiming predictive effectiveness."""
    if (
        training.feature_names != later.feature_names
        or training.feature_value_kinds != later.feature_value_kinds
    ):
        msg = "exact input support schema required"
        raise ValueError(msg)
    changed = []
    outside = []
    for j, name in enumerate(training.feature_names):
        low = min(row[j] for row in training.rows)
        high = max(row[j] for row in training.rows)
        if any(not low <= row[j] <= high for row in later.rows):
            outside.append(name)
            if low == high:
                changed.append(name)
    return {
        "changed_constant_coordinates": changed,
        "outside_training_box": outside,
        "effectiveness": "UNKNOWN",
    }


def best_index(family: str, observations: list[LearningFeedback]) -> int | None:
    """Compare only values sharing the admitted family/metric, ties to the incumbent."""
    values = [(i, o.value) for i, o in enumerate(observations) if o.value is not None]
    if not values:
        return None
    return (
        max(values, key=lambda p: (p[1], -p[0]))
        if family == "classification"
        else min(values, key=lambda p: (p[1], p[0]))
    )[0]


def decision(
    family: str,
    methods: tuple[str, ...],
    observations: list[LearningFeedback],
    support: dict[str, object] | None,
    *,
    profile: str,
) -> tuple[str, str | None]:
    """Use newly acknowledged evidence before requesting another original fit."""
    if profile != PROFILE:
        msg = "caller must explicitly select the qualified engineering profile"
        raise ValueError(
            msg,
        )
    if any(o.value is None for o in observations):
        return "ABSTAIN", None
    if support is None:
        return "CHECK_SUPPORT", None
    if len(observations) == len(methods):
        return "STOP", None
    if len(observations) >= 2 and best_index(family, observations) == best_index(
        family,
        observations[:-1],
    ):
        return "STOP", None
    if observations and support["changed_constant_coordinates"]:
        return "ABSTAIN", None
    return "EVALUATE", methods[len(observations)]
