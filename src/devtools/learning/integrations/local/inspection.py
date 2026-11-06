# Copyright (c) 2026
"""Backend-light, read-only numerical/source and scientific-publication inspection."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, replace
from statistics import mean, pstdev
from uuid import UUID

from devtools.core.paths import resolve_path
from devtools.learning.classification.linear import (
    BinaryLinearTraining,
    FittedBinaryLinearClassifier,
    _hash,
)
from devtools.learning.classification.margin import FittedMarginClassifier
from devtools.learning.evidence.events import Admitted, Outcome, Terminal
from devtools.learning.integrations.local._codec import retained_object as obj
from devtools.learning.integrations.local.classification.codec import (
    document,
)
from devtools.learning.integrations.local.classification.codec import (
    preparation as decode_preparation,
)
from devtools.learning.integrations.local.ledger import (
    inspect_child_execution_ids,
    inspect_execution,
)
from devtools.learning.integrations.local.linear_classification import decode_model
from devtools.learning.integrations.local.margin_classification import decode_margin
from devtools.learning.integrations.local.operations import (
    LearningPublication,
    correspondence,
    knn7_predict,
    quality,
    represented,
)
from devtools.learning.integrations.local.publication import reconcile_publication
from devtools.learning.integrations.local.regression.codec import state as decode_state
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.plans import (
    MAX_PUBLICATION_BYTES,
    BinaryProblem,
    LearningPlan,
    validate_authorization,
)
from devtools.learning.measurement.contracts import Measured, NonValueKind, NoValue
from devtools.learning.regression.contracts import (
    RegressionInput,
    RegressionMethod,
    RegressionPopulation,
    RegressionSpecification,
)
from devtools.learning.regression.limits import REGRESSION_V2
from devtools.learning.regression.state import (
    FittedRegression,
    RegressionPredictions,
    validate_training_state,
)
from devtools.learning.regression.verification import inspect_knn_query
from devtools.learning.representation.features import FeatureTable
from devtools.learning.representation.standardization import (
    FittedFeatureStandardization,
    _fingerprint,
)
from devtools.resources.filesystem import BinaryFile, FileFormat, read


def _independent_features(
    features: FeatureTable,
    preparation: FittedFeatureStandardization | None,
    method: str,
) -> FeatureTable:
    """Recompute raw-source scaling/SQUARE arithmetic without the producing transforms."""
    rows = features.rows
    names = features.feature_names
    if preparation is not None:
        rows = tuple(
            tuple(
                (x - m) / s
                for x, m, s in zip(
                    row,
                    preparation.training_means,
                    preparation.effective_scales,
                    strict=True,
                )
            )
            for row in rows
        )
    if method.startswith("square-"):
        names += tuple(
            f"append_squared_features_v1[{i},{i}]:{name}*{name}"
            for i, name in enumerate(features.feature_names)
        )
        rows = tuple(row + tuple(x * x for x in row) for row in rows)
    kinds = features.feature_value_kinds * (2 if method.startswith("square-") else 1)
    return FeatureTable(names, rows, kinds)


def _independent_f1(
    truth: tuple[int, ...],
    predicted: tuple[int, ...],
    version: int,
) -> float | None:
    """Count original binary outcomes directly, retaining each version's nonvalues."""
    values = []
    for label in (0, 1) if version == 2 else sorted(set(truth) | set(predicted)):
        support = sum(y == label for y in truth)
        guessed = sum(y == label for y in predicted)
        correct = sum(a == b == label for a, b in zip(truth, predicted, strict=True))
        if version == 2:
            if not support + guessed:
                return None
            values.append(2 * correct / (support + guessed))
        else:
            if not support or not guessed:
                return None
            precision, recall = correct / guessed, correct / support
            if not precision + recall:
                return None
            values.append(2 * precision * recall / (precision + recall))
    return sum(values) / len(values)


@dataclass(frozen=True, slots=True)
class InspectedLearning:
    """A publication-pinned fitted result under one exact inspected source frame."""

    reference: LearningPublication
    plan: LearningPlan
    preparation: FittedFeatureStandardization | None
    state: (
        FittedRegression | FittedBinaryLinearClassifier | FittedMarginClassifier | None
    )
    binary_training: BinaryLinearTraining | None
    quality: Measured[float] | NoValue

    def predict(
        self,
        inputs: FeatureTable | RegressionInput,
    ) -> tuple[int, ...] | RegressionPredictions:
        """Use retained state for a label-free caller-permitted query; never refit."""
        if isinstance(self.state, FittedRegression):
            if not isinstance(inputs, RegressionInput):
                msg = "source/unit-bound regression inputs required"
                raise TypeError(msg)
            return self.state.predict(inputs)
        if not isinstance(inputs, FeatureTable):
            msg = "binary feature table required"
            raise TypeError(msg)
        features = represented(inputs, self.preparation, self.plan.method)
        if self.binary_training is not None and self.state is None:
            return knn7_predict(self.binary_training, features)
        if isinstance(
            self.state,
            (FittedBinaryLinearClassifier, FittedMarginClassifier),
        ):
            return self.state.classify(features)
        msg = "inspected fitted state required"
        raise TypeError(msg)


def inspect_learning(
    reference: LearningPublication,
    plan: LearningPlan,
    grant: ExecutionAuthorization,
) -> InspectedLearning:
    """Check pinned members, source, preparation, state, metrics and acknowledged order."""
    validate_authorization(plan, grant)
    if reference.plan_identity != plan.identity:
        msg = "foreign scientific reference"
        raise ValueError(msg)
    root = reference.root.value
    database = root / "science.sqlite"
    publication = reconcile_publication(root / "publication", database)
    if (
        publication is None
        or publication.manifest is None
        or publication.manifest.generation_id != reference.generation_id
        or publication.manifest_sha256 != reference.manifest_sha256
        or publication.recording_status.value != "acknowledged"
        or publication.manifest.expected_artifact_names != ("result.json",)
    ):
        msg = "scientific publication is missing, changed or unacknowledged"
        raise ValueError(msg)
    member = read(
        resolve_path(publication.artifact_paths[0]),
        file_format=FileFormat.BINARY,
        max_bytes=MAX_PUBLICATION_BYTES,
    )
    if not isinstance(member, BinaryFile):
        msg = "binary scientific member required"
        raise TypeError(msg)
    saved = obj(json.loads(member.content))
    if (
        set(saved)
        != {
            "schema",
            "plan",
            "grant",
            "runtime",
            "native_correspondence",
            "preparation",
            "state",
            "predictions",
            "quality",
            "measurement",
            "producing_execution_id",
            "fitting_execution_id",
        }
        or saved["schema"] != "learning-operation-v2"
        or saved["plan"] != plan.document()
        or saved["grant"] != document(asdict(grant))
    ):
        msg = "scientific schema/plan/grant correspondence differs"
        raise ValueError(msg)
    producing_id = UUID(str(saved["producing_execution_id"]))
    history = inspect_execution(database, producing_id)
    if (
        history is None
        or history.outcome is not Outcome.COMPLETED
        or history.execution_id != publication.manifest.producing_execution_id
    ):
        msg = "completed original producer required"
        raise ValueError(msg)
    admitted = history.events[0].payload
    terminal = history.events[-1].payload
    if not isinstance(admitted, Admitted) or not isinstance(terminal, Terminal):
        msg = "producer grant/terminal acknowledgments absent"
        raise ValueError(msg)
    facts = {fact.name: fact.value for fact in admitted.facts}
    end_facts = {fact.name: fact.value for fact in terminal.facts}
    if (
        facts.get("plan_identity") != plan.identity
        or facts.get("grant_json")
        != json.dumps(
            document(asdict(grant)),
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        or facts.get("runtime_identity") != _hash(saved["runtime"])
        or end_facts.get("state_identity") != _hash(saved["state"])
    ):
        msg = "original acknowledged grant/state correspondence differs"
        raise ValueError(msg)
    children = [
        inspect_execution(database, identity)
        for identity in inspect_child_execution_ids(database, producing_id)
    ]
    predict_history = next(
        (h for h in children if h is not None and h.operation == "learning.predict"),
        None,
    )
    measure_history = next(
        (h for h in children if h is not None and h.operation == "learning.measure"),
        None,
    )
    if (
        predict_history is None
        or measure_history is None
        or predict_history.outcome is not Outcome.COMPLETED
        or measure_history.outcome is not Outcome.COMPLETED
        or predict_history.events[-1].occurred_at
        > measure_history.events[0].occurred_at
    ):
        msg = "prediction must be acknowledged before measurement"
        raise ValueError(msg)
    publisher_id = publication.manifest.publication_execution_id
    publisher = (
        None if publisher_id is None else inspect_execution(database, publisher_id)
    )
    if (
        publisher is None
        or publisher.parent_execution_id != producing_id
        or publisher.outcome is not Outcome.COMPLETED
        or measure_history.events[-1].occurred_at > publisher.events[0].occurred_at
        or publisher.events[-1].occurred_at > history.events[-1].occurred_at
    ):
        msg_0 = (
            "measurement/publication/producer acknowledgments are causally reordered"
        )
        raise ValueError(
            msg_0,
        )
    training, held = plan.populations()
    fitting_id = UUID(str(saved["fitting_execution_id"]))
    original_fit = inspect_execution(database, fitting_id)
    if (
        original_fit is None
        or original_fit.parent_execution_id != producing_id
        or original_fit.outcome is not Outcome.COMPLETED
        or original_fit.events[-1].occurred_at > predict_history.events[0].occurred_at
    ):
        msg = "original fitting must be acknowledged before prediction begins"
        raise ValueError(msg)
    preparation = (
        None
        if saved["preparation"] is None
        else decode_preparation(saved["preparation"])
    )
    features = (
        training.features
        if isinstance(training, BinaryLinearTraining)
        else training.inputs.features
    )
    if plan.method != "mean":
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
        if (
            preparation is None
            or preparation.fitting_input_sha256 != _fingerprint(features)
            or preparation.fitting_population_id != population_id
            or preparation.source_identity != source_identity
        ):
            msg = "original training-only preparation required"
            raise ValueError(msg)
        columns = tuple(zip(*features.rows, strict=True))
        preparing = inspect_execution(database, preparation.construction_execution_id)
        if (
            preparing is None
            or preparing.outcome is not Outcome.COMPLETED
            or preparing.parent_execution_id != producing_id
            or preparation.effective_scales
            != tuple(s if s else 1.0 for s in preparation.training_standard_deviations)
        ):
            msg_0 = "original training preparation acknowledgment/scales differ"
            raise ValueError(
                msg_0,
            )
        if preparing.events[-1].occurred_at > original_fit.events[0].occurred_at:
            msg = "training preparation must be acknowledged before fitting begins"
            raise ValueError(msg)
        if (
            preparation.training_means != tuple(mean(c) for c in columns)
            or preparation.training_standard_deviations
            != tuple(pstdev(c) for c in columns)
            or preparation.fitting_observation_count != len(features.rows)
        ):
            msg = "independent original-population preparation arithmetic differs"
            raise ValueError(
                msg,
            )
    elif preparation is not None:
        msg = "mean must not silently prepare features"
        raise ValueError(msg)
    state: (
        FittedRegression | FittedBinaryLinearClassifier | FittedMarginClassifier | None
    )
    binary_training = None
    if isinstance(training, BinaryLinearTraining):
        binary_training = replace(
            training,
            features=represented(features, preparation, plan.method),
        )
        if plan.method == "knn7":
            if saved["state"] != {
                "schema": "retained-knn7-v1",
                "training": document(asdict(binary_training)),
            }:
                msg = "retained binary neighbor corpus differs from source"
                raise ValueError(msg)
            state = None
        else:
            raw = json.dumps(saved["state"], allow_nan=False).encode()
            state = (
                decode_model(raw)
                if plan.method == "square-logistic"
                else decode_margin(raw)
            )
            if (
                state.training_input_sha256 != binary_training.content_identity
                or state.training_population_id != training.population_id
                or state.target_identity != training.target_identity
                or state.fitting_execution_id != fitting_id
                or state.feature_names != binary_training.features.feature_names
                or state.references != training.references
            ):
                msg = "binary state/source/fitting correspondence differs"
                raise ValueError(msg)
            expected_configuration = (
                (
                    ("solver", "lbfgs"),
                    ("C", "1.0"),
                    ("fit_intercept", "True"),
                    ("max_iter", "800"),
                    ("tol", "1e-07"),
                    ("random_state", "42"),
                    ("numerical_threads", "1"),
                    ("l1_ratio", "0.0"),
                )
                if plan.method == "square-logistic"
                else (
                    ("penalty", "l2"),
                    ("loss", "squared_hinge"),
                    ("dual", "False"),
                    ("C", "1.0"),
                    ("fit_intercept", "True"),
                    ("intercept_scaling", "1.0"),
                    ("tol", "1e-06"),
                    ("max_iter", "2000"),
                    ("random_state", "42"),
                    ("numerical_threads", "1"),
                )
            )
            if state.configuration != expected_configuration:
                msg = "retained native configuration differs from the exact granted method"
                raise ValueError(msg)
    else:
        state = decode_state(
            saved["state"],
            maximum_bytes=min(MAX_PUBLICATION_BYTES, REGRESSION_V2.state_bytes),
        )
        methods = {
            "mean": RegressionMethod.MEAN,
            "ridge": RegressionMethod.RIDGE,
            "knn-v2": RegressionMethod.KNN,
        }
        expected_specification = RegressionSpecification(
            methods[plan.method],
            "regression-specification-v2"
            if plan.method == "knn-v2"
            else "regression-specification-v1",
        )
        if (
            state.specification != expected_specification
            or state.execution_id != fitting_id
        ):
            msg_0 = "retained method does not match the exact granted plan"
            raise ValueError(msg_0)
        validate_training_state(state, training)
        fitting = inspect_execution(database, state.execution_id)
        if (
            fitting is None
            or fitting.outcome is not Outcome.COMPLETED
            or fitting.parent_execution_id != producing_id
            or not isinstance(fitting.events[-1].payload, Terminal)
            or dict((f.name, f.value) for f in fitting.events[-1].payload.facts).get(
                "state_identity",
            )
            != state.content_identity
        ):
            msg = "original regression fit acknowledgment differs"
            raise ValueError(msg)
    expected_children = {
        fitting_id,
        predict_history.execution_id,
        measure_history.execution_id,
        publisher_id,
    }
    if preparation is not None:
        expected_children.add(preparation.construction_execution_id)
    if set(inspect_child_execution_ids(database, producing_id)) != expected_children:
        msg = "scientific child executions differ from the exact single-operation plan"
        raise ValueError(msg)
    if isinstance(training, BinaryLinearTraining):
        fit_terminal = original_fit.events[-1].payload
        if (
            original_fit.operation != "learning.binary_fit"
            or not isinstance(fit_terminal, Terminal)
            or {f.name: f.value for f in fit_terminal.facts}.get("state_identity")
            != _hash(saved["state"])
        ):
            msg = "original binary fit acknowledgment does not bind the retained state"
            raise ValueError(msg)
    provisional = InspectedLearning(
        reference,
        plan,
        preparation,
        state,
        binary_training,
        NoValue(
            NonValueKind.NOT_MEASURED,
            "inspection_in_progress",
            "Source/state inspection precedes metric replay.",
        ),
    )
    predictions = provisional.predict(
        held.features if isinstance(held, BinaryProblem) else held.inputs,
    )
    encoded_predictions = (
        list(predictions)
        if isinstance(predictions, tuple)
        else document(asdict(predictions))
    )
    measured, measurements = quality(plan, predictions)
    if saved["native_correspondence"] != correspondence(plan, state, preparation):
        msg_0 = "native parity scope differs from independently inspected queries"
        raise ValueError(
            msg_0,
        )
    raw_query = (
        held.features if isinstance(held, BinaryProblem) else held.inputs.features
    )
    independent_query = _independent_features(raw_query, preparation, plan.method)
    if (
        isinstance(training, BinaryLinearTraining)
        and isinstance(held, BinaryProblem)
        and isinstance(predictions, tuple)
    ):
        independent_training = _independent_features(
            training.features,
            preparation,
            plan.method,
        )
        if binary_training is None or independent_training != binary_training.features:
            msg_0 = "independent feature construction differs from original source"
            raise ValueError(
                msg_0,
            )
        if state is None:
            labels = []
            for row in independent_query.rows:
                neighbors = sorted(
                    range(len(training.targets)),
                    key=lambda i: (
                        math.hypot(
                            *(
                                a - b
                                for a, b in zip(
                                    row,
                                    independent_training.rows[i],
                                    strict=True,
                                )
                            ),
                        ),
                        i,
                    ),
                )[:7]
                labels.append(int(sum(training.targets[i] for i in neighbors) > 3))
            independent_predictions = tuple(labels)
        elif isinstance(state, (FittedBinaryLinearClassifier, FittedMarginClassifier)):
            independent_predictions = tuple(
                int(
                    math.fsum(
                        (
                            state.intercept,
                            *(
                                w * x
                                for w, x in zip(state.coefficients, row, strict=True)
                            ),
                        ),
                    )
                    > 0,
                )
                for row in independent_query.rows
            )
        else:
            msg_0 = "binary fitted state required"
            raise TypeError(msg_0)
        if independent_predictions != predictions:
            msg_0 = "independent binary prediction arithmetic differs"
            raise ValueError(msg_0)
        independent_value = _independent_f1(
            held.targets,
            predictions,
            1 if plan.metric.endswith(":v1") else 2,
        )
        if (
            (independent_value is None) != isinstance(measured, NoValue)
            or isinstance(measured, Measured)
            and measured.value != independent_value
        ):
            msg_0 = "independent F1 counts differ"
            raise ValueError(msg_0)
    elif isinstance(state, FittedRegression) and isinstance(
        predictions,
        RegressionPredictions,
    ):
        if not isinstance(training, RegressionPopulation) or not isinstance(
            held,
            RegressionPopulation,
        ):
            msg_0 = "quantitative source populations required for inspection"
            raise TypeError(msg_0)
        if state.specification.method is RegressionMethod.MEAN:
            independent_values = (
                math.fsum(training.values) / len(training.values),
            ) * len(raw_query.rows)
        elif state.specification.method is RegressionMethod.RIDGE:
            independent_values = tuple(
                math.fsum(w * x for w, x in zip(state.coefficients, row, strict=True))
                + state.intercept
                for row in independent_query.rows
            )
        else:
            independent_values = tuple(
                inspect_knn_query(state, row)[2] for row in independent_query.rows
            )
        if independent_values != predictions.values:
            msg_0 = "independent quantitative prediction arithmetic differs"
            raise ValueError(msg_0)
        if isinstance(measured, Measured) and measured.value != math.fsum(
            abs(a - b) for a, b in zip(held.values, independent_values, strict=True)
        ) / len(held.values):
            msg_0 = "independent MAE arithmetic differs"
            raise ValueError(msg_0)
    if (
        saved["predictions"] != encoded_predictions
        or saved["quality"] != document(asdict(measured))
        or saved["measurement"] != measurements
    ):
        msg = "independent prediction/metric/source evidence differs"
        raise ValueError(msg)
    return replace(provisional, quality=measured)
