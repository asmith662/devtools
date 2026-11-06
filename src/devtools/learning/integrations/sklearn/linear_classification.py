# mypy: disable-error-code="import-untyped"
# Copyright (c) 2026

"""One actual binary L2 logistic fit on supplied numerical features.

This is separate from hard-prediction stacking's OOF-specific fitting contract.

Native state exists only during construction; immutable coefficients survive.

"""

from __future__ import annotations

import math
import platform
import warnings
from dataclasses import asdict, dataclass

import numpy as np
import scipy
import sklearn
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_info, threadpool_limits

from devtools.learning.classification.linear import (
    BinaryLinearTraining,
    FittedBinaryLinearClassifier,
)
from devtools.learning.evidence.context import ExecutionContext
from devtools.learning.evidence.events import FailureCategory


@dataclass(frozen=True, slots=True)
class LogisticClassificationConfiguration:
    """Observable fixed first fitting configuration, not a parameter search."""

    solver: str = "lbfgs"

    C: float = 1.0

    fit_intercept: bool = True

    max_iter: int = 800

    tol: float = 1e-07

    random_state: int = 42

    numerical_threads: int = 1

    l1_ratio: float = 0.0

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        expected = ("lbfgs", 1.0, True, 800, 1e-07, 42, 1, 0.0)

        actual = tuple(asdict(self).values())

        if any(
            (
                type(a) is not type(b) or a != b
                for a, b in zip(actual, expected, strict=True)
            ),
        ):
            msg = "only the declared fixed logistic configuration is supported"
            raise ValueError(
                msg,
            )

    @property
    def observations(self) -> tuple[tuple[str, str], ...]:
        """Apply the explicit observations contract within this owner."""
        return tuple(((k, str(v)) for k, v in asdict(self).items()))


def fit_binary_logistic(
    training: BinaryLinearTraining,
    configuration: LogisticClassificationConfiguration,
    *,
    execution: ExecutionContext,
) -> FittedBinaryLinearClassifier:
    """Fit sum(binary log loss)+||w||²/(2*C), unpenalized intercept.

    Installed sklearn specifies L2 by l1_ratio=0. Convergence warnings are errors;

    no configuration adaptation or retries occur. Agreement covers actual supplied

    fitting rows, with binary64 rtol/atol 1e-12 and identical threshold decisions.

    """
    if (
        not isinstance(training, BinaryLinearTraining)
        or not isinstance(configuration, LogisticClassificationConfiguration)
        or (not isinstance(execution, ExecutionContext))
    ):
        msg = "validated training/configuration and managed fitting required"
        raise TypeError(msg)

    execution.stage(
        "numerical_input",
        "Encode supplied binary fitting population",
        FailureCategory.INPUT,
    )

    x = np.asarray(training.features.rows, dtype=np.float64)

    y = np.asarray(training.targets, dtype=np.int64)

    native = LogisticRegression(
        solver=configuration.solver,
        C=configuration.C,
        fit_intercept=configuration.fit_intercept,
        max_iter=configuration.max_iter,
        tol=configuration.tol,
        random_state=configuration.random_state,
        l1_ratio=configuration.l1_ratio,
        class_weight=None,
        warm_start=False,
    )

    execution.stage(
        "logistic_numerical_fit",
        "One fixed L2 logistic optimization",
        FailureCategory.NUMERICAL,
    )

    with (
        warnings.catch_warnings(),
        threadpool_limits(limits=configuration.numerical_threads),
    ):
        warnings.simplefilter("error")

        native.fit(x, y)

        threads = str(
            tuple(
                (p.get("internal_api"), p.get("num_threads")) for p in threadpool_info()
            ),
        )

    execution.stage(
        "retained_state_validation",
        "Validate retained/native binary64 scores",
        FailureCategory.INVALID_RESULT,
    )

    weights = tuple(float(v) for v in native.coef_[0])

    intercept = float(native.intercept_[0])

    if (
        tuple(int(v) for v in native.classes_) != (0, 1)
        or native.coef_.shape != (1, len(training.features.feature_names))
        or (not 0 <= int(native.n_iter_[0]) < configuration.max_iter)
    ):
        msg = "unexpected binary state or incomplete convergence"
        raise ValueError(msg)

    pure = tuple(
        math.fsum(
            (intercept, *(w * float(v) for w, v in zip(weights, row, strict=True))),
        )
        for row in x
    )

    scores = native.decision_function(x)

    if not np.allclose(pure, scores, rtol=1e-12, atol=1e-12) or tuple(
        int(v > 0) for v in pure
    ) != tuple(int(v) for v in native.predict(x)):
        msg = "native/retained logit or category disagreement"
        raise ValueError(msg)

    return FittedBinaryLinearClassifier(
        training.features.feature_names,
        training.target_identity,
        weights,
        intercept,
        training.population_id,
        training.content_identity,
        execution.execution_id,
        configuration.observations,
        (
            ("python", platform.python_version()),
            ("sklearn", sklearn.__version__),
            ("numpy", np.__version__),
            ("scipy", scipy.__version__),
            ("dtype", "binary64"),
            ("native_n_iter", str(int(native.n_iter_[0]))),
            (
                "native_training_max_abs_error",
                str(float(max(abs(np.asarray(pure) - scores)))),
            ),
            ("agreement_tolerance", "rtol=1e-12;atol=1e-12;actual-fitting-rows"),
            ("threadpools", threads),
        ),
        training.references,
    )
