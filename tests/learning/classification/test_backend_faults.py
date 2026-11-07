# Copyright (c) 2026
"""Explicit backend-report fault injection; controls are not native fits."""

from __future__ import annotations

import warnings
from importlib import import_module
from typing import TYPE_CHECKING, Any, cast

import pytest

from devtools.learning.evidence.context import ExecutionContext
from devtools.learning.evidence.events import Admitted, Diagnostic, Outcome
from devtools.learning.integrations.local.ledger import (
    SQLiteExecutionRecorder,
    inspect_execution,
)
from devtools.learning.integrations.sklearn import (
    linear_classification as logistic,
)
from devtools.learning.integrations.sklearn import (
    margin_classification as margin,
)
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


class _ReportedModel:
    """Retain NumPy representation while deliberately reporting an invalid fit."""

    def __init__(self, dimension: int, family: str, fault: str) -> None:
        self.np = import_module("numpy")
        self.family, self.fault = family, fault
        self.coef_ = self.np.zeros((1, dimension))
        self.intercept_ = self.np.zeros(1)
        self.classes_ = self.np.asarray([0, 1])
        self.n_iter_: object = self.np.asarray([1]) if family == "logistic" else 1
        self.calls = 0

    def fit(self, _features: object, _targets: object) -> None:
        """Inject exactly one report; never invoke an optimizer."""
        self.calls += 1
        if self.fault == "classes":
            self.classes_ = self.np.asarray([0, 2])
        if self.fault == "warning":
            warnings.warn("authored backend warning control", UserWarning, stacklevel=2)

    def decision_function(self, rows: object) -> object:
        """Report a finite score inconsistent with the retained state."""
        return self.np.ones(len(cast("Sequence[object]", rows)))

    def predict(self, rows: object) -> object:
        """Report classes inconsistent with the retained all-zero state."""
        return self.np.ones(len(cast("Sequence[object]", rows)), dtype=int)


@pytest.mark.parametrize("family", ["logistic", "margin"])
@pytest.mark.parametrize("fault", ["classes", "parity"])
def test_backend_state_and_arithmetic_disagreement_are_failed_occurrences(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    family: str,
    fault: str,
) -> None:
    """Real scientific recording cannot turn an invalid native report into success."""
    _refuse_report(tmp_path, monkeypatch, family, fault)


def test_margin_warning_is_retained_before_failure_without_retry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Observed warning diagnostics survive the failed scientific occurrence."""
    _refuse_report(tmp_path, monkeypatch, "margin", "warning")


def _refuse_report(
    root: Path,
    patch: pytest.MonkeyPatch,
    family: str,
    fault: str,
) -> None:
    plan = authored_task("classification").plan("knn7", "online", "native-report")
    training, _ = plan.populations()
    typed = cast("Any", training)
    report = _ReportedModel(len(typed.features.feature_names), family, fault)
    module = logistic if family == "logistic" else margin
    patch.setattr(
        module,
        "LogisticRegression" if family == "logistic" else "LinearSVC",
        lambda **_: report,
    )
    configuration = (
        logistic.LogisticClassificationConfiguration()
        if family == "logistic"
        else margin.MarginClassificationConfiguration()
    )
    fit = (
        logistic.fit_binary_logistic
        if family == "logistic"
        else margin.fit_binary_margin
    )
    database = root / "science.sqlite"
    with (
        SQLiteExecutionRecorder(database) as recorder,
        pytest.raises(ValueError, match=r"state|classes|disagreement|warnings"),
        ExecutionContext(recorder, Admitted("backend-report-control")) as run,
    ):
        fit(typed, cast("Any", configuration), execution=run)
    history = inspect_execution(database, run.execution_id)
    assert history is not None
    assert history.outcome is Outcome.FAILED
    assert report.calls == 1
    if fault == "warning":
        assert any(isinstance(event.payload, Diagnostic) for event in history.events)


@pytest.mark.parametrize("family", ["logistic", "margin"])
def test_native_fit_and_fixed_configuration_types_are_required(family: str) -> None:
    """Configuration searches and unmanaged fitting remain outside this contract."""
    configuration = (
        logistic.LogisticClassificationConfiguration
        if family == "logistic"
        else margin.MarginClassificationConfiguration
    )
    with pytest.raises(ValueError, match="configuration"):
        configuration(C=2.0)
    fit = (
        logistic.fit_binary_logistic
        if family == "logistic"
        else margin.fit_binary_margin
    )
    with pytest.raises(TypeError, match="managed fit"):
        fit(cast("Any", None), cast("Any", None), execution=cast("Any", None))
