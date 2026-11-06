# Copyright (c) 2026
"""Authored deterministic numerical controls, run only in a contained worker."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, replace
from pathlib import Path
from statistics import mean, pstdev

from devtools.learning.classification.linear import BinaryLinearTraining
from devtools.learning.evaluation.classification import evaluate_classification
from devtools.learning.evaluation.classification_v2 import macro_f1_value
from devtools.learning.evaluation.regression.metrics import evaluate_regression
from devtools.learning.evidence.context import ExecutionContext
from devtools.learning.evidence.events import Admitted, Fact
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.integrations.local.ledger import SQLiteExecutionRecorder
from devtools.learning.integrations.local.linear_classification import (
    decode_model,
    model_document,
)
from devtools.learning.integrations.local.publication import (
    publish_artifacts,
    reconcile_publication,
)
from devtools.learning.integrations.local.regression.codec import state as decode_state
from devtools.learning.integrations.sklearn.linear_classification import (
    LogisticClassificationConfiguration,
    fit_binary_logistic,
)
from devtools.learning.integrations.sklearn.regression import fit_regression
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.learning.regression.contracts import (
    ContinuousTarget,
    RegressionInput,
    RegressionMethod,
    RegressionPopulation,
    RegressionRole,
    RegressionSpecification,
)
from devtools.learning.regression.state import validate_training_state
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.learning.representation.standardization import (
    FeatureStandardizationSpecification,
    fit_feature_standardization,
)


def qualify(root: Path) -> dict[str, object]:
    """Fit on authored training rows; inspect retained arithmetic without refits."""
    root.mkdir()
    table = FeatureTable(
        ("x", "constant"),
        tuple((float(i), 2.0) for i in range(8)),
        (FeatureValueKind.CONTINUOUS,) * 2,
    )
    inputs = RegressionInput(
        table,
        (None, None),
        tuple(f"r{i}" for i in range(8)),
        "authored-training",
        "authored-source-v1",
        RegressionRole.TRAINING,
    )
    population = RegressionPopulation(
        inputs,
        ContinuousTarget("quantity-v1", "authored scalar", "authored unit"),
        tuple(float(2 * i + 1) for i in range(8)),
    )
    authority = ExecutionAuthorization(
        population.content_identity,
        ("authored-control",),
        EvidenceReference("host_control_authority", "authored-control", None),
    )
    assert authority.plan_identity == population.content_identity
    database = root / "science.sqlite"
    records: dict[str, object] = {"grant": document(asdict(authority))}
    with SQLiteExecutionRecorder(database) as recorder:
        with ExecutionContext(
            recorder,
            Admitted(
                "learning.authored.control",
                (Fact("plan_identity", authority.plan_identity),),
            ),
        ) as run:
            preparation = fit_feature_standardization(
                FeatureStandardizationSpecification(table.feature_names),
                table,
                population_id=inputs.population_id,
                source_identity=inputs.source_identity,
                recorder=recorder,
                parent=run,
            )
            assert preparation.training_means == (mean(range(8)), 2.0)
            assert preparation.training_standard_deviations == (pstdev(range(8)), 0.0)
            assert preparation.effective_scales[1] == 1.0
            query = replace(
                inputs,
                features=FeatureTable(
                    table.feature_names,
                    ((0.2, 2.0), (6.7, 2.0)),
                    table.feature_value_kinds,
                ),
                row_ids=("q0", "q1"),
                population_id="authored-online",
                role=RegressionRole.DEVELOPMENT,
            )
            observed = RegressionPopulation(query, population.target, (1.4, 14.4))
            for method in (
                RegressionMethod.MEAN,
                RegressionMethod.RIDGE,
                RegressionMethod.KNN,
            ):
                fitted = fit_regression(
                    RegressionSpecification(method),
                    population,
                    None if method is RegressionMethod.MEAN else preparation,
                    recorder=recorder,
                    parent=run,
                )
                predicted = fitted.predict(query)
                retained = decode_state(document(asdict(fitted.state)))
                validate_training_state(retained, population)
                assert retained.predict(query) == predicted
                transformed = preparation.transform(query.features).features.rows
                if method is RegressionMethod.RIDGE:
                    independent = tuple(
                        math.fsum(
                            (
                                retained.intercept,
                                *(
                                    w * x
                                    for w, x in zip(
                                        retained.coefficients,
                                        row,
                                        strict=True,
                                    )
                                ),
                            ),
                        )
                        for row in transformed
                    )
                    assert independent == predicted.values
                if method is RegressionMethod.MEAN:
                    assert predicted.values == (8.0, 8.0)
                evaluation = evaluate_regression(observed, predicted)
                records[method.value] = {
                    "state": document(asdict(retained)),
                    "prediction": document(asdict(predicted)),
                    "evaluation": document(asdict(evaluation)),
                }
            prepared = preparation.transform(table).features
            training = BinaryLinearTraining(
                prepared,
                (0, 0, 0, 0, 1, 1, 1, 1),
                inputs.row_ids,
                inputs.population_id,
                "binary-target-v1",
                (authority.authority,),
            )
            classifier = fit_binary_logistic(
                training,
                LogisticClassificationConfiguration(),
                execution=run,
            )
            encoded = json.dumps(model_document(classifier)).encode()
            restored = decode_model(encoded)
            prediction = restored.classify(prepared)
            assert prediction == classifier.classify(prepared)
            counts = evaluate_classification(training.targets, prediction)
            records["classification"] = {
                "state": model_document(restored),
                "predictions": prediction,
                "f1": macro_f1_value(counts, version=2),
            }
            records["preparation"] = document(asdict(preparation))
            run.completed((Fact("control_complete", True),))
        payload = json.dumps(records, sort_keys=True, allow_nan=False).encode()

        def write_artifacts(directory: Path) -> None:
            """Write the sole declared scientific member into private staging."""
            (directory / "result.json").write_bytes(payload)

        publication = publish_artifacts(
            root / "publication",
            run.execution_id,
            ("result.json",),
            write_artifacts,
            recorder=recorder,
            dependencies=(Fact("plan_identity", authority.plan_identity),),
        )
    checked = reconcile_publication(root / "publication", database)
    assert checked is not None
    assert checked.manifest == publication.manifest
    assert checked.artifact_paths[0].read_bytes() == payload
    from threadpoolctl import threadpool_info  # type: ignore[import-untyped]

    threads = threadpool_info()
    assert threads
    assert all(t["num_threads"] == 1 for t in threads)
    return {
        "regression_methods": 3,
        "binary_f1": records["classification"],
        "publication_status": str(checked.status),
        "recording_status": str(checked.recording_status),
        "native_pools": threads,
    }


if __name__ == "__main__":
    sys.stdout.write(json.dumps(qualify(Path(sys.argv[1])), sort_keys=True) + "\n")
