# Copyright (c) 2026
"""Explicit unavailable learning capability without implying a numerical failure."""

from devtools.learning.measurement.contracts import NonValueKind, NoValue


class LearningUnavailableError(RuntimeError):
    """Carry the typed missing-dependency nonvalue before any fitting occurs."""

    def __init__(self, detail: str) -> None:
        """Retain unavailable meaning separately from failed or unsupported fitting."""
        super().__init__(detail)
        self.observation = NoValue(
            NonValueKind.UNAVAILABLE,
            "numerical_dependencies_unavailable",
            detail,
        )
