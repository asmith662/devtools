# mypy: disable-error-code="import-untyped"
# Copyright (c) 2026

"""One concrete squared-hinge LinearSVC fit; no optimizer/configuration search."""

from __future__ import annotations

import json
import math
import platform
import warnings
from dataclasses import asdict, dataclass

import numpy as np
import scipy
import sklearn
from sklearn.svm import LinearSVC
from threadpoolctl import threadpool_info, threadpool_limits

from devtools.learning.classification.linear import BinaryLinearTraining
from devtools.learning.classification.margin import FittedMarginClassifier
from devtools.learning.evidence.context import ExecutionContext
from devtools.learning.evidence.events import Diagnostic, FailureCategory, Severity


@dataclass(frozen=True, slots=True)
class MarginClassificationConfiguration:
    """Fixed approved native configuration, distinct from a procedure's identity."""

    penalty: str = "l2"

    loss: str = "squared_hinge"

    dual: bool = False

    C: float = 1.0

    fit_intercept: bool = True

    intercept_scaling: float = 1.0

    tol: float = 1e-06

    max_iter: int = 2000

    random_state: int = 42

    numerical_threads: int = 1

    def __post_init__(self) -> None:

        expected = ("l2", "squared_hinge", False, 1.0, True, 1.0, 1e-06, 2000, 42, 1)

        if any(
            (
                type(a) is not type(b) or a != b
                for a, b in zip(asdict(self).values(), expected, strict=True)
            ),
        ):
            msg = "only the approved squared-hinge configuration is supported"
            raise ValueError(
                msg,
            )

    @property
    def observations(self) -> tuple[tuple[str, str], ...]:

        return tuple(((key, str(value)) for key, value in asdict(self).items()))


def fit_binary_margin(
    training: BinaryLinearTraining,
    configuration: MarginClassificationConfiguration,
    *,
    execution: ExecutionContext,
) -> FittedMarginClassifier:
    """Fit 0.5*(||w||²+(b/s)²)+C*sum(max(0,1-y*score)²), y=-1/+1.

    LIBLINEAR regularizes its intercept synthetic-feature coefficient b/s.

    This differs from the existing logistic learner's unpenalized intercept.

    Warnings/iteration limits are recorded and refused, never configuration-tuned.

    Retained/native agreement uses binary64 rtol=atol=1e-12 on actual fitting rows.

    """
    if (
        not isinstance(training, BinaryLinearTraining)
        or not isinstance(configuration, MarginClassificationConfiguration)
        or (not isinstance(execution, ExecutionContext))
    ):
        msg = "validated binary training/configuration and managed fit required"
        raise TypeError(
            msg,
        )

    execution.stage(
        "numerical_input",
        "Actual represented binary fitting rows",
        FailureCategory.INPUT,
    )

    x = np.asarray(training.features.rows, dtype=np.float64)

    y = np.asarray(training.targets, dtype=np.int64)

    native = LinearSVC(
        penalty=configuration.penalty,
        loss=configuration.loss,
        dual=configuration.dual,
        C=configuration.C,
        fit_intercept=configuration.fit_intercept,
        intercept_scaling=configuration.intercept_scaling,
        tol=configuration.tol,
        max_iter=configuration.max_iter,
        random_state=configuration.random_state,
        class_weight=None,
        multi_class="ovr",
        verbose=0,
    )

    execution.stage(
        "margin_numerical_fit",
        "One L2 squared-hinge optimization",
        FailureCategory.NUMERICAL,
    )

    with (
        warnings.catch_warnings(record=True) as observed,
        threadpool_limits(limits=configuration.numerical_threads),
    ):
        warnings.simplefilter("always")

        native.fit(x, y)

        pools = str(
            tuple(

                    (p.get("internal_api"), p.get("num_threads"))
                    for p in threadpool_info()

            ),
        )

    warning_records = [(w.category.__name__, str(w.message)) for w in observed]

    for category, message in warning_records:
        execution.diagnostic(
            Diagnostic(
                FailureCategory.NUMERICAL,
                Severity.WARNING,
                category
                + ": "
                + message
                + "; native_n_iter="
                + str(native.n_iter_)
                + "; classes="
                + json.dumps(native.classes_.tolist())
                + "; dtype="
                + str(native.coef_.dtype),
                stage="margin_numerical_fit",
            ),
        )

    if warning_records:
        msg = "margin fitting emitted backend warnings; retained diagnostics; no retry"
        raise ValueError(
            msg,
        )

    execution.stage(
        "retained_state_validation",
        "Validate original margin/schema/decisions",
        FailureCategory.INVALID_RESULT,
    )

    if (
        tuple(native.classes_.tolist()) != (0, 1)
        or native.coef_.shape != (1, len(training.features.feature_names))
        or native.coef_.dtype != np.dtype("float64")
        or (not 0 < int(native.n_iter_) < configuration.max_iter)
    ):
        msg = "invalid margin classes/schema/dtype or incomplete convergence"
        raise ValueError(
            msg,
        )

    weights = tuple(float(v) for v in native.coef_[0])

    intercept = float(native.intercept_[0])

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
        msg = "native/retained margin or category disagreement"
        raise ValueError(msg)

    return FittedMarginClassifier(
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
            ("native_classes", json.dumps(native.classes_.tolist())),
            ("native_n_iter", str(int(native.n_iter_))),
            ("warnings", json.dumps(warning_records)),
            (
                "convergence",
                "no warning; native iterations below fixed limit; solver criterion not independently reproduced",
            ),
            (
                "intercept_regularization",
                "LIBLINEAR penalized synthetic feature; b/intercept_scaling",
            ),
            (
                "native_training_max_abs_error",
                str(float(max(abs(np.asarray(pure) - scores)))),
            ),
            ("agreement_tolerance", "rtol=1e-12;atol=1e-12;actual-fitting-rows"),
            ("threadpools", pools),
        ),
        training.references,
    )
