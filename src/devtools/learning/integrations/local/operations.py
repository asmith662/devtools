# Copyright (c) 2026
"""One granted learning operation using the selected native and scientific owners."""

from __future__ import annotations

import importlib.util
import math
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from devtools.core.paths import ResolvedPath, resolve_path
from devtools.learning.classification.linear import (
    BinaryLinearTraining,
    FittedBinaryLinearClassifier,
    _hash,
)
from devtools.learning.classification.margin import FittedMarginClassifier
from devtools.learning.evaluation.classification import evaluate_classification
from devtools.learning.evaluation.classification_v2 import macro_f1_value
from devtools.learning.evaluation.regression.metrics import evaluate_regression
from devtools.learning.evidence.context import ExecutionContext
from devtools.learning.evidence.events import Admitted, Fact
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.integrations.local.ledger import SQLiteExecutionRecorder
from devtools.learning.integrations.local.linear_classification import model_document
from devtools.learning.integrations.local.margin_classification import margin_document
from devtools.learning.integrations.local.publication import publish_artifacts
from devtools.learning.integrations.sklearn.runtime import observe_runtime
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.errors import LearningUnavailableError
from devtools.learning.investigation.plans import (
    LEDGER_BYTES,
    MAX_PUBLICATION_BYTES,
    BinaryProblem,
    LearningPlan,
    canonical,
    validate_authorization,
)
from devtools.learning.measurement.contracts import Measured, NonValueKind, NoValue
from devtools.learning.methods.features import (
    SQUARES,
    FeatureRecipe,
    transform_features,
)
from devtools.learning.regression.contracts import (
    RegressionMethod,
    RegressionSpecification,
)
from devtools.learning.regression.state import FittedRegression, RegressionPredictions
from devtools.learning.regression.verification import inspect_knn_query
from devtools.learning.representation.features import FeatureTable
from devtools.learning.representation.standardization import (
    FeatureStandardizationSpecification,
    FittedFeatureStandardization,
    fit_feature_standardization,
)
from devtools.resources.filesystem import BinaryFile, write


@dataclass(frozen=True, slots=True)
class LearningPublication:
    """Host-pinned scientific publication; never a model-supplied authority."""

    root: ResolvedPath
    generation_id: str
    manifest_sha256: str
    plan_identity: str


def represented(
    table: FeatureTable,
    preparation: FittedFeatureStandardization | None,
    method: str,
) -> FeatureTable:
    """Apply training-fitted statistics and the explicitly selected SQUARE recipe."""
    result = table if preparation is None else preparation.transform(table).features
    if method.startswith("square-"):
        result = transform_features(
            result,
            FeatureRecipe("learning-square-catalog-v1", (SQUARES,)),
            maximum_dimension=256,
        )
    return result


def knn7_predict(
    training: BinaryLinearTraining,
    features: FeatureTable,
) -> tuple[int, ...]:
    """Replay uniform seven-neighbor voting, ties by original row index then class."""
    if (
        features.feature_names != training.features.feature_names
        or features.feature_value_kinds != training.features.feature_value_kinds
    ):
        msg = "incompatible retained kNN schema"
        raise ValueError(msg)
    result = []
    for row in features.rows:
        selected = sorted(
            range(len(training.targets)),
            key=lambda i: (math.dist(row, training.features.rows[i]), i),
        )[:7]
        result.append(int(sum(training.targets[i] for i in selected) > 3))
    return tuple(result)


def quality(
    plan: LearningPlan,
    predictions: tuple[int, ...] | RegressionPredictions,
) -> tuple[Measured[float] | NoValue, dict[str, object]]:
    """Keep F1 versions and target-unit MAE separate, including typed nonvalues."""
    _training, held = plan.populations()
    if isinstance(held, BinaryProblem):
        if not isinstance(predictions, tuple):
            msg = "binary predictions required"
            raise TypeError(msg)
        evaluated = evaluate_classification(held.targets, predictions)
        value = macro_f1_value(
            evaluated,
            version=1 if plan.metric.endswith(":v1") else 2,
        )
        observation = (
            NoValue(
                NonValueKind.UNDEFINED,
                "undefined_binary_f1",
                "Required binary metric denominator is undefined under the selected version.",
            )
            if value is None
            else Measured(value)
        )
        return observation, document(asdict(evaluated))
    if not isinstance(predictions, RegressionPredictions):
        msg = "quantitative predictions required"
        raise TypeError(msg)
    evaluated_regression = evaluate_regression(held, predictions)
    return evaluated_regression.mae, document(asdict(evaluated_regression))


def correspondence(
    plan: LearningPlan,
    state: FittedRegression
    | FittedBinaryLinearClassifier
    | FittedMarginClassifier
    | None,
    preparation: FittedFeatureStandardization | None,
) -> dict[str, object]:
    """Retain the exact native-parity scope, including ambiguous v2 query nonclaims."""
    _training, held = plan.populations()
    if plan.method == "knn-v2":
        if not isinstance(state, FittedRegression) or isinstance(held, BinaryProblem):
            msg = "deterministic regression state required"
            raise TypeError(msg)
        rows = represented(held.inputs.features, preparation, plan.method).rows
        flags = [inspect_knn_query(state, row)[3] for row in rows]
        return {
            "contract": "native-regression-parity-v1",
            "qualified_row_ids": [
                r for r, ok in zip(held.inputs.row_ids, flags, strict=True) if ok
            ],
            "unqualified_row_ids": [
                r for r, ok in zip(held.inputs.row_ids, flags, strict=True) if not ok
            ],
            "unqualified_meaning": "Original native boundary choice is not v2 truth; full-corpus deterministic retained arithmetic is independently checked.",
        }
    return {
        "contract": "no-native-fit"
        if plan.method == "mean"
        else "native-and-retained-query-predictions"
        if plan.method in {"ridge", "knn7"}
        else "native-training-linear-state-and-independent-retained-query-arithmetic",
    }


class _Recorder(SQLiteExecutionRecorder):
    """Bound one publication and the existing ledger, without another store."""

    def __init__(self, database: Path) -> None:
        super().__init__(database, maximum_database_bytes=LEDGER_BYTES)
        self._reserved = False

    def reserve_publication(self, payload_bytes: int | None) -> None:
        """Reserve one known finite member before its staging files are created."""
        if (
            self._reserved
            or type(payload_bytes) is not int
            or not 0 <= payload_bytes <= MAX_PUBLICATION_BYTES
        ):
            msg = "scientific publication bound exceeded"
            raise ValueError(msg)
        self._reserved = True


def execute_plan(
    plan: LearningPlan,
    grant: ExecutionAuthorization,
    root: Path,
) -> LearningPublication:
    """Execute once after exact authority; unknown failures retain their original root."""
    validate_authorization(plan, grant)
    if any(
        importlib.util.find_spec(name) is None
        for name in ("numpy", "scipy", "sklearn", "threadpoolctl")
    ):
        msg = "Optional learning numerical dependencies are unavailable."
        raise LearningUnavailableError(
            msg,
        )
    runtime = observe_runtime()
    root.mkdir()  # A reused/uncertain operation root is never overwritten or retried.
    training, held = plan.populations()
    source_features = (
        training.features
        if isinstance(training, BinaryLinearTraining)
        else training.inputs.features
    )
    population_id = (
        training.population_id
        if isinstance(training, BinaryLinearTraining)
        else training.inputs.population_id
    )
    source_identity = (
        held.source_identity
        if isinstance(held, BinaryProblem)
        else held.inputs.source_identity
    )
    database = root / "science.sqlite"
    with _Recorder(database) as recorder:
        with ExecutionContext(
            recorder,
            Admitted(
                "learning.fit",
                (
                    Fact("plan_identity", plan.identity),
                    Fact("grant_json", canonical(document(asdict(grant)))),
                    Fact("invocation_identity", plan.invocation_identity),
                    Fact("phase", plan.phase),
                    Fact("runtime_identity", _hash(runtime)),
                ),
            ),
        ) as run:
            preparation = (
                None
                if plan.method == "mean"
                else fit_feature_standardization(
                    FeatureStandardizationSpecification(source_features.feature_names),
                    source_features,
                    population_id=population_id,
                    source_identity=source_identity,
                    recorder=recorder,
                    parent=run,
                )
            )
            state_document: dict[str, object]
            binary_training = None
            native_regression = None
            native_knn = None
            state: (
                FittedRegression
                | FittedBinaryLinearClassifier
                | FittedMarginClassifier
                | None
            ) = None
            if isinstance(training, BinaryLinearTraining):
                if not isinstance(held, BinaryProblem):
                    msg = "binary held population required"
                    raise TypeError(msg)
                binary_training = replace(
                    training,
                    features=represented(training.features, preparation, plan.method),
                )
                with ExecutionContext(
                    recorder,
                    Admitted("learning.binary_fit", (Fact("method", plan.method),)),
                    parent=run,
                ) as fitting_run:
                    if plan.method == "knn7":
                        from devtools.learning.classification.k_nearest_neighbors import (
                            KNearestNeighborsClassificationSpecification,
                            KNearestNeighborsDistance,
                            KNearestNeighborsWeighting,
                        )
                        from devtools.learning.integrations.sklearn.k_nearest_neighbors import (
                            construct_k_nearest_neighbors_classification,
                        )

                        native_knn = construct_k_nearest_neighbors_classification(
                            KNearestNeighborsClassificationSpecification(
                                7,
                                KNearestNeighborsDistance.EUCLIDEAN,
                                KNearestNeighborsWeighting.UNIFORM,
                            ),
                            binary_training.features,
                            binary_training.targets,
                        )
                        state_document = {
                            "schema": "retained-knn7-v1",
                            "training": document(asdict(binary_training)),
                        }
                    elif plan.method == "square-logistic":
                        from devtools.learning.integrations.sklearn.linear_classification import (
                            LogisticClassificationConfiguration,
                            fit_binary_logistic,
                        )

                        state = fit_binary_logistic(
                            binary_training,
                            LogisticClassificationConfiguration(),
                            execution=fitting_run,
                        )
                        state_document = model_document(state)
                    else:
                        from devtools.learning.integrations.sklearn.margin_classification import (
                            MarginClassificationConfiguration,
                            fit_binary_margin,
                        )

                        state = fit_binary_margin(
                            binary_training,
                            MarginClassificationConfiguration(),
                            execution=fitting_run,
                        )
                        state_document = margin_document(state)
                    fitting_run.completed(
                        (Fact("state_identity", _hash(state_document)),)
                    )
                fitting_id = fitting_run.execution_id
            else:
                from devtools.learning.integrations.sklearn.regression import (
                    fit_regression,
                )

                methods = {
                    "mean": RegressionMethod.MEAN,
                    "ridge": RegressionMethod.RIDGE,
                    "knn-v2": RegressionMethod.KNN,
                }
                specification = RegressionSpecification(
                    methods[plan.method],
                    "regression-specification-v2"
                    if plan.method == "knn-v2"
                    else "regression-specification-v1",
                )
                native_regression = fit_regression(
                    specification,
                    training,
                    preparation,
                    recorder=recorder,
                    parent=run,
                )
                state = native_regression.state
                state_document = document(asdict(state))
                fitting_id = state.execution_id
            with ExecutionContext(
                recorder,
                Admitted(
                    "learning.predict",
                    (Fact("state_identity", _hash(state_document)),),
                ),
                parent=run,
            ) as prediction_run:
                if isinstance(held, BinaryProblem):
                    query = represented(held.features, preparation, plan.method)
                    if native_knn is not None and binary_training is not None:
                        predictions: tuple[int, ...] | RegressionPredictions = (
                            knn7_predict(binary_training, query)
                        )
                        if predictions != native_knn.classify(query):
                            msg = (
                                "native/independent binary kNN prediction disagreement"
                            )
                            raise ValueError(
                                msg,
                            )
                    elif isinstance(
                        state,
                        (FittedBinaryLinearClassifier, FittedMarginClassifier),
                    ):
                        predictions = state.classify(query)
                    else:
                        msg = "retained binary state required"
                        raise TypeError(msg)
                elif native_regression is not None:
                    predictions = native_regression.predict(held.inputs)
                else:
                    msg = "native regression fit required"
                    raise TypeError(msg)
                prediction_run.completed(
                    (
                        Fact(
                            "prediction_identity",
                            _hash(
                                document(asdict(predictions))
                                if isinstance(predictions, RegressionPredictions)
                                else predictions,
                            ),
                        ),
                    ),
                )
            with ExecutionContext(
                recorder,
                Admitted("learning.measure", (Fact("metric", plan.metric),)),
                parent=run,
            ) as measurement_run:
                observation, measurements = quality(plan, predictions)
                measurement_run.completed(
                    (Fact("measurement_identity", _hash(measurements)),),
                )
            result = {
                "schema": "learning-operation-v2",
                "fitting_execution_id": str(fitting_id),
                "plan": plan.document(),
                "grant": document(asdict(grant)),
                "runtime": runtime,
                "native_correspondence": correspondence(plan, state, preparation),
                "preparation": None
                if preparation is None
                else document(asdict(preparation)),
                "state": state_document,
                "predictions": document(asdict(predictions))
                if isinstance(predictions, RegressionPredictions)
                else list(predictions),
                "quality": document(asdict(observation)),
                "measurement": measurements,
                "producing_execution_id": str(run.execution_id),
            }
            raw = canonical(result).encode()
            if len(raw) > MAX_PUBLICATION_BYTES:
                msg = "retained scientific state exceeds publication limit"
                raise ValueError(msg)

            def write_member(directory: Path) -> None:
                write(
                    BinaryFile(resolve_path(directory / "result.json"), raw),
                    overwrite=False,
                )

            publication = publish_artifacts(
                root / "publication",
                run.execution_id,
                ("result.json",),
                write_member,
                dependencies=(Fact("plan_identity", plan.identity),),
                recorder=recorder,
                parent=run,
                payload_bytes=len(raw),
            )
            run.completed(
                (
                    Fact("state_identity", _hash(state_document)),
                    Fact("plan_identity", plan.identity),
                ),
            )
    if publication.manifest is None or publication.manifest_sha256 is None:
        msg = "scientific publication did not retain a manifest"
        raise ValueError(msg)
    return LearningPublication(
        resolve_path(root),
        publication.manifest.generation_id,
        publication.manifest_sha256,
        plan.identity,
    )
