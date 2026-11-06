# Copyright (c) 2026
"""Real scripted native ModelInteraction/Tool, numerical inspection and parent use."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace

from devtools.agents.learning.process import AdmittedLearningTask
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.investigation.plans import canonical
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.learning.regression.contracts import (
    ContinuousTarget,
    RegressionInput,
    RegressionPopulation,
    RegressionRole,
)
from devtools.learning.representation.features import FeatureTable, FeatureValueKind
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
)


def authored_task(
    family: str,
    *,
    nonvalue: bool = False,
    unsupported: bool = False,
) -> AdmittedLearningTask:
    """Use independently authored rows, never a real-source outcome table."""
    features = FeatureTable(
        ("x", "constant"),
        tuple((float(i), 2.0) for i in range(8)),
        (FeatureValueKind.CONTINUOUS,) * 2,
    )
    source = "authored-source-" + family

    def binary(phase: str) -> dict[str, object]:
        return {
            "identity": "authored-" + phase,
            "source_identity": source,
            "training": {
                "features": document(asdict(features)),
                "targets": [0, 0, 0, 0, 1, 1, 1, 1],
                "row_ids": [f"r{i}" for i in range(8)],
                "population_id": "authored-training",
                "target_identity": "binary-meaning-v1",
                "references": [
                    {"relation": "original_source", "identity": source, "sha256": None},
                ],
            },
            "evaluation_features": {
                "feature_names": ["x", "constant"],
                "feature_value_kinds": ["continuous", "continuous"],
                "rows": [
                    [0.2, 3.0 if unsupported else 2.0],
                    [0.3 if nonvalue else 6.7, 2.0],
                ],
            },
            "evaluation_targets": [0, 0 if nonvalue else 1],
            "evaluation_row_ids": [phase + "0", phase + "1"],
            "evaluation_population_id": "private-final-marker"
            if phase == "final"
            else "online-population",
        }

    def regression(phase: str) -> dict[str, object]:
        target = ContinuousTarget(
            "scalar-quantity",
            "authored quantity",
            "authored unit",
        )
        training = RegressionPopulation(
            RegressionInput(
                features,
                (None, None),
                tuple(f"r{i}" for i in range(8)),
                "training",
                source,
                RegressionRole.TRAINING,
                "regression-input-v2",
            ),
            target,
            tuple(float(i * 2 + 1) for i in range(8)),
            version="regression-population-v2",
        )
        query = FeatureTable(
            features.feature_names,
            ((0.2, 2.0), (6.7, 2.0)),
            features.feature_value_kinds,
        )
        held = RegressionPopulation(
            RegressionInput(
                query,
                (None, None),
                (phase + "0", phase + "1"),
                "private-final-marker" if phase == "final" else "online",
                source,
                RegressionRole.CONFIRMATION
                if phase == "final"
                else RegressionRole.DEVELOPMENT,
                "regression-input-v2",
            ),
            target,
            (1.4, 14.4),
            version="regression-population-v2",
        )
        return {
            "training": document(asdict(training)),
            "evaluation": document(asdict(held)),
        }

    problem = binary if family == "classification" else regression
    return AdmittedLearningTask(
        "authored-" + family,
        family,
        "classification.macro_f1:v2"
        if family == "classification"
        else "regression.mae:v1",
        ("knn7", "square-logistic", "square-margin")
        if family == "classification"
        else ("mean", "ridge", "knn-v2"),
        canonical(problem("online")),
        canonical(problem("final")),
        canonical(
            {
                "source_identity": source,
                "provenance": "authored engineering control; no generalization claim",
            },
        ),
        EvidenceReference("parent_source_admission", source),
    )


def authored_tie_task() -> AdmittedLearningTask:
    """Place a query at a five-neighbor boundary with different tied targets."""
    task = authored_task("regression")

    def problem(serialized: str, phase: str) -> str:
        raw = json.loads(serialized)
        held = raw["evaluation"]
        held["inputs"]["features"]["rows"] = [[3.5, 2.0]]
        held["inputs"]["row_ids"] = [phase + "-tie"]
        held["values"] = [7.0]
        return canonical(raw)

    return replace(
        task,
        methods=("knn-v2",),
        online_problem_json=problem(task.online_problem_json, "online"),
        final_problem_json=problem(task.final_problem_json, "final"),
    )


@dataclass
class ScriptedInvestigator:
    """Read actual acknowledged feedback before emitting the next native request."""

    mutation: dict[str, object] = field(default_factory=dict)
    source: InteractionSource = field(
        default_factory=lambda: InteractionSource("scripted-learning")
    )
    requests: list[ModelRequest] = field(default_factory=list)

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Use a finite deterministic proposer without any grant/evaluator access."""
        self.requests.append(request)
        serialized = canonical([m.content for m in request.prompt.messages])
        assert "private-final-marker" not in serialized
        assert "learning_execution_grant-v1" not in serialized
        frame = json.loads(request.prompt.messages[-1].content)
        seen = frame["observations"]
        action = "EVALUATE"
        method = None
        if any(o["value"] is None for o in seen):
            action = "ABSTAIN"
        elif frame["support"] is None:
            action = "CHECK_SUPPORT"
        elif len(seen) == len(frame["methods"]) or (
            len(seen) >= 2
            and (
                (seen[-1]["value"] <= max(o["value"] for o in seen[:-1]))
                if frame["family"] == "classification"
                else (seen[-1]["value"] >= min(o["value"] for o in seen[:-1]))
            )
        ):
            action = "STOP"
        elif seen and frame["support"]["changed_constant_coordinates"]:
            action = "ABSTAIN"
        else:
            method = frame["methods"][len(seen)]
        payload = {
            name: frame[name]
            for name in (
                "task_identity",
                "source_handle",
                "family",
                "metric",
                "schema_identity",
                "unit_identity",
                "role",
                "state_identity",
                "evidence",
            )
        }
        payload.update(
            action=action,
            method=method,
            rationale="Use the original acknowledged online observations under the selected finite profile.",
        )
        payload.update(self.mutation)
        return ModelResponse(
            "One bounded learning proposal.",
            self.source,
            tool_calls=(
                ModelToolCall(
                    "learning_investigate",
                    canonical(payload),
                    f"call-{len(self.requests)}",
                ),
            ),
        )
