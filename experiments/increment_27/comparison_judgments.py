# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Origin-blind judgments of the frozen neutral comparison input."""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any, cast

from experiments.increment_25.development import write_artifact
from experiments.increment_27.depth_diagnostic import _digest, _read_json

ROOT = Path(__file__).parent
INPUT_NAME = "comparison_blinded_judgment_input.json"
OUTPUT_NAME = "comparison_frozen_judgments.json"
INPUT_IDENTITY = "90213a1d9dc7370559313a425a593208ba5c71e523a78fd71753beab8d905fe3"
INPUT_SHA256 = "1114ff4d1b45edfac8178744e29640763ff1cc2c8cd5804e80dc67351694a26f"
SEMANTICS = "purpose-relative-three-state-v1"
STATES = {"U": "USEFUL", "N": "NOT_USEFUL", "J": "UNJUDGED"}

# Rows follow the opaque case/resource order of the verified neutral input.
# Every rationale concerns only the resource's usefulness for its frozen task.
DECISIONS: tuple[tuple[str, ...], ...] = (
    (
        "N|Path exports provide no function disclosure or source materialization behavior.",
    ),
    (
        "N|Filesystem model exports do not address model reasoning content.",
        "N|Atomic file writing does not define model reasoning output.",
        "N|Filesystem model documentation does not describe model response content.",
        "N|JSON file models do not define model reasoning content.",
        "N|Filesystem exceptions do not inform the model response contract.",
        "N|File codecs do not address reasoning content in model output.",
        "U|The public ModelResponse and Prompt boundary identifies where reasoning content must fit.",
    ),
    (
        "N|Path exports do not select resources by Python function name.",
        "U|The Context API exposes existing Python declaration and retrieval contracts relevant to selection.",
    ),
    ("N|Path exports do not derive Python declarations from an explicit resource.",),
    ("N|Path exports do not aggregate declaration analyses across resources.",),
    (
        "U|Duration, Stopwatch, and Timestamp exports provide timing values for usage measurement.",
        "U|Benchmark result values show concrete token and duration measurements.",
        "U|The time API exposes elapsed-time values relevant to usage measurements.",
        "U|Duration defines the elapsed-time representation needed for latency measurements.",
        "U|Benchmark tests show validation of token and duration measurement fields.",
        "J|Optional supervisor token counts may inform usage semantics, but the task gives no worker-measurement scope.",
    ),
    (
        "J|Function declaration dependencies identify module resources, but their role in root interpretation is unclear.",
        "N|Function Context rendering tests do not define module interpretation.",
        "N|General path exports do not define repository-relative Python modules.",
        "J|The broad Context exports show related APIs but not enough module-root behavior to establish material help.",
        "N|Model invocation exports do not concern Python module interpretation.",
        "U|Repository observation defines the identified snapshot resources that module interpretation would consume.",
        "J|Python syntax analysis is adjacent to module interpretation, but the exposed API gives no root semantics.",
        "U|Canonical resource addresses and occurrences are necessary inputs to explicit-root module mapping.",
        "U|Repository identity supplies the logical repository scope for module interpretations.",
        "N|Codex integration documentation does not define Python module roots.",
        "N|Tool documentation does not address Python module interpretation.",
    ),
    (
        "N|Benchmark values do not observe repository snapshots.",
        "N|Time exports do not implement bounded resource observation.",
        "N|Conversation SQLite storage does not observe repository resource snapshots.",
        "N|Model artifact acquisition does not observe repository text resources.",
        "N|llama.cpp serving lifecycle does not address repository snapshot observation.",
        "U|Resolved path exports provide the bounded filesystem-root value needed for observation.",
        "N|vLLM serving lifecycle does not observe repository resources.",
        "N|Filesystem roadmap notes provide no concrete snapshot observation contract.",
    ),
    (
        "J|Model invocation contracts may be used by an acceptance fixture, but the task does not specify that path.",
        "J|A live Codex acceptance example may help fixture design, but it does not show selection stress.",
        "J|Runtime coordination could participate in an acceptance fixture, but the task gives no execution design.",
        "J|ToolRunner could drive selection stress, but the task does not identify its Tool boundary.",
        "J|A live Conversation acceptance example is adjacent, without a stated selection criterion.",
        "N|General path exports do not define a selection-stress acceptance fixture.",
        "J|Conversation values could support a fixture, but their role is unspecified.",
        "N|Model-serving lifecycle documentation does not define repository selection stress.",
        "N|Provider transport exceptions do not define selection behavior.",
        "J|Worker telemetry tests are adjacent to acceptance reporting, but selection-stress measures are unspecified.",
        "N|Model benchmark documentation measures serving behavior rather than repository selection.",
        "U|The bounded repository read and directory-list Tool provides concrete operations for a selection fixture.",
        "J|Filesystem exports might support fixture reads, but the needed resource operations are unspecified.",
    ),
    (
        "U|The Context API exposes the Python function source materialization operation directly.",
        "N|Path exports do not materialize declaration source from snapshot content.",
    ),
    (
        "U|Resource address, occurrence, and content identity define observation outputs.",
        "U|The public Context API exposes repository observation values and operations.",
        "U|Resolved paths provide the bounded root used to read observed resources.",
        "N|Model invocation exports do not observe repository text.",
        "N|Model request assembly tests concern downstream use of Context, not text observation.",
        "N|Function rendering tests concern downstream presentation, not resource observation.",
        "N|Function-name candidate tests do not define bounded text observation.",
        "U|Filesystem read and text-file exports supply the bounded read substrate for observation.",
    ),
    (
        "J|Filesystem models may support discovery, but the exposed exports focus on file contents rather than enumeration.",
        "U|Resolved path primitives provide the root and containment behavior needed by discovery.",
        "N|Function-name candidate tests select within known resources, not discover repository files.",
        "N|Function declaration derivation does not enumerate repository resources.",
        "U|The Context API exposes repository resource discovery as a public responsibility.",
        "N|Generic identity exports do not define filesystem discovery behavior.",
    ),
    (
        "N|Command output values concern subprocess capture rather than model interaction output limits.",
        "J|Runtime response-validation tests may constrain an output bound, but no limit semantics are shown.",
        "N|Qwen acceptance reporting tests do not define a model interaction output bound.",
    ),
    (
        "N|Generic identity exports do not describe repository Context discovery.",
        "U|Repository read and directory-list operations provide concrete discovery behavior to investigate.",
        "N|Model invocation exports do not discover repository context.",
        "N|Conversation message values do not discover repository resources.",
        "N|Time exports do not describe repository context discovery.",
        "N|Conversation exports do not enumerate or select repository resources.",
        "N|Model artifact acquisition does not investigate repository Context discovery.",
        "U|Filesystem Tool tests document directory listing and bounded repository reads relevant to discovery.",
    ),
    (
        "J|The provider package identifies the interaction adapter, but its exports alone do not show thinking controls.",
        "N|Token usage values do not define a thinking-control request.",
        "N|Execution lifecycle exports do not specify model thinking controls.",
        "J|Prompt input could carry a control, but the exposed value has only content and role.",
        "N|Conversation exports do not define model thinking settings.",
        "N|Termination reasons describe response endings, not thinking controls.",
        "N|Generic conversion tests do not concern model thinking.",
        "N|Evidence exports do not configure model interaction thinking.",
    ),
    (
        "J|Filesystem exports might support fixture resources, but the selection measure is unspecified.",
        "N|A Qwen test-package marker contains no fixture behavior.",
        "J|Runtime coordination may participate in measurement, but the fixture execution path is unspecified.",
        "U|Repository-file Tool tests show bounded reads and listing behavior usable in selection stress.",
        "J|Evidence delivery could record a measure, but this task does not identify that protocol.",
        "U|The repository-file Tool implements concrete read and list operations for selection stress.",
        "J|ToolRunner exports could support a fixture, but the requested measurement flow is unspecified.",
        "N|General path exports do not define selection measurements.",
        "N|Model artifact-reference tests do not measure repository selection.",
        "J|Conversation values may be used in an acceptance run, but their role is unspecified.",
        "J|Model invocation values may be used in an acceptance run, but the selection measure is unspecified.",
        "U|Repeated-read experiment tests provide a concrete acceptance pattern for repository reads.",
    ),
    (
        "U|Model interaction contracts identify the request and response boundary used by an acceptance run.",
        "N|General path exports do not test Python function Context acceptance.",
        "U|The Context API exposes the function analysis, disclosure, materialization, and assembly operations under test.",
        "J|Conversation values may matter to an acceptance run, but the task does not specify persistence behavior.",
    ),
    (
        "U|The Tool protocol directly defines the execution boundary under consideration.",
        "U|CommandTool is a concrete adapter demonstrating that boundary.",
        "U|Filesystem Tool tests exercise validation and execution behavior at the boundary.",
        "U|The public Tool API exposes the protocol, runner, and input-error contract.",
        "U|ModelInteraction exports identify the model-facing boundary that native Tool requests would meet.",
        "J|Runtime coordination is adjacent, but the requested Tool boundary does not specify Runtime changes.",
        "N|Conversation exports do not define Tool request or execution semantics.",
        "N|Interaction-attempt lifecycle facts do not define the model-native Tool boundary.",
        "U|Command execution primitives are the concrete resource substrate used by a Tool adapter.",
        "N|Evidence exports do not define Tool request authority or execution.",
        "J|ResolvedPath could type Tool inputs, but the model-native boundary is not path-specific.",
        "U|ToolRunner tests directly show validation, execution, failure, and cancellation contracts.",
    ),
    (
        "N|Evidence exports do not derive Python function declarations.",
        "N|Model invocation exports do not parse Python function declarations.",
        "N|Time exports do not analyze Python source declarations.",
        "N|Provider exports do not derive Python function declarations.",
        "N|Command execution documentation does not define Python declaration analysis.",
        "N|Model-serving exports do not analyze Python source declarations.",
        "N|Command package documentation does not address Python declaration derivation.",
        "N|Codex CLI documentation does not define direct Python declaration analysis.",
    ),
    (
        "N|Path resolution documentation does not define repository text documents.",
        "J|Text-file models may inform representation, but the task gives no document content contract.",
        "J|Discovery yields resource addresses that documents might preserve, but the representation boundary is unspecified.",
        "J|Filesystem file models might inform text storage, but document semantics are not shown.",
        "N|General path exports do not represent observed text documents.",
    ),
    (
        "U|Time primitives supply timestamps for terminal lifecycle evidence.",
        "U|The Runtime public API identifies the coordinator whose terminal evidence is at issue.",
        "U|Runtime documentation describes interaction coordination and evidence delivery boundaries.",
        "U|Attempt lifecycle tests specify terminal transitions and timestamps relevant to evidence.",
        "N|The package root contains no Runtime or Evidence contract.",
        "N|Generic identity exports do not define terminal Evidence production or delivery.",
    ),
    (
        "J|Runtime Tool integration tests exercise interactions, but the request boundary itself is not specified there.",
        "U|Execution documentation describes how Runtime passes a request to one selected ModelInteraction.",
        "U|ModelResponse defines the output counterpart to a ModelInteraction request.",
        "U|The public ModelInteraction API exposes Prompt and protocol contracts at the request boundary.",
        "J|Conversation values may be a request source, but the task does not specify their projection.",
        "J|Provider exports identify adapters, but do not show their request translation contract.",
    ),
    (
        "N|General path exports do not assemble Python function Context into model requests.",
        "U|The Context API exposes the function Context assembly operation directly.",
    ),
)


def build_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Bind each human judgment to one exact neutral target and no origin data."""
    path = root / INPUT_NAME
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INPUT_SHA256:
        raise ValueError("Neutral input byte identity differs.")
    blind = _read_json(path)
    blind_payload = cast("dict[str, Any]", blind["payload"])
    if (
        blind.get("content_identity") != INPUT_IDENTITY
        or _digest(blind_payload) != INPUT_IDENTITY
    ):
        raise ValueError("Neutral input content identity differs.")
    cases = blind_payload["cases"]
    if len(cases) != len(DECISIONS):
        raise ValueError("Neutral case count differs from adjudication rows.")
    records: list[dict[str, Any]] = []
    for case, choices in zip(cases, DECISIONS, strict=True):
        resources = case["resources"]
        if len(resources) != len(choices):
            raise ValueError("Neutral target count differs from adjudication rows.")
        for resource, choice in zip(resources, choices, strict=True):
            code, rationale = choice.split("|", 1)
            if code not in STATES or not rationale.strip():
                raise ValueError("Invalid three-state judgment or empty rationale.")
            records.append(
                {
                    "neutral_case_id": case["neutral_case_id"],
                    "information_need": case["information_need"],
                    "parent_snapshot_sha": case["parent_snapshot_sha"],
                    "neutral_resource_id": resource["neutral_resource_id"],
                    "address": resource["address"],
                    "usefulness_semantics": SEMANTICS,
                    "judgment": STATES[code],
                    "rationale": rationale,
                }
            )
    keys = {(row["neutral_case_id"], row["neutral_resource_id"]) for row in records}
    if len(records) != len(keys) or len(records) != 140:
        raise ValueError("Judgment population has missing or duplicate targets.")
    counts = Counter(row["judgment"] for row in records)
    payload: dict[str, Any] = {
        "schema": "devtools-i27-neutral-comparison-frozen-judgments-v1",
        "blinded_input_content_identity": INPUT_IDENTITY,
        "blinded_input_sha256": INPUT_SHA256,
        "usefulness_semantics": SEMANTICS,
        "three_states": ["USEFUL", "NOT_USEFUL", "UNJUDGED"],
        "target_count": len(records),
        "state_counts": {
            state: counts[state] for state in ("USEFUL", "NOT_USEFUL", "UNJUDGED")
        },
        "records": records,
    }
    return {
        "schema": payload["schema"],
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_judgments(root: Path = ROOT) -> dict[str, Any]:
    """Persist the complete blinded decision set before any origin join."""
    artifact = build_judgments(root)
    path = root / OUTPUT_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing frozen judgments differ.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    freeze_judgments()
