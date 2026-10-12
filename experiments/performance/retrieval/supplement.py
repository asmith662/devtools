# Copyright (c) 2026
# ruff: noqa: E501
"""Additional ownership/memory checks after the primary latency run is complete."""

from __future__ import annotations

import time
from functools import partial
from pathlib import Path
from typing import Any

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.composition import require_lexical_result_snapshot
from experiments.codex_dogfood.case_0016.stage_b.execute import universe
from experiments.performance.retrieval.benchmark import PACKAGE, publish, setup
from experiments.performance.retrieval.measurement import Recorder
from experiments.performance.retrieval.memory import retained_size
from experiments.performance.retrieval.workload import sha
from experiments.task_conditioned_graph.diagnostic import definitions


def run(output: Path = PACKAGE / "supplement.json") -> dict[str, Any]:
    """Retain supplement independently; never rewrite original timing samples."""
    progress: list[dict[str, Any]] = []

    def emit(row: dict[str, Any]) -> None:
        progress.append(row)
        publish(output.parent / "supplement_progress.json", progress)

    recorder = Recorder(emit)
    started = time.perf_counter_ns()
    recorder.emit("supplement_input_preparation", started, phase="START")
    data = setup()
    recorder.emit("supplement_input_preparation", started, phase="COMPLETE")
    snapshot = data["frame"].snapshot
    recorder.measure(
        "module_interpretation_universe",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: universe(snapshot),
        warmup=0,
        repetitions=3,
        note="Existing src/. module-root interpretations, before RI derivation.",
    )
    for q in ("Q1", "Q6"):
        locator = data["design"]["seed_policy"]["exact_locators"][q][0]
        address = RepositoryResourceAddress(locator)
        recorder.measure(
            q + ".frozen_exact_lookup_hit",
            "ONLINE_QUERY",
            partial(snapshot.resource_at, address),
        )
    recorder.measure(
        "native_reference_key_preparation",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: [
            (
                r.identity,
                r.occurrence.resource_address,
                r.target_resource.address,
                repr(r.occurrence.source_range),
            )
            for r in data["references"]
        ],
        warmup=0,
        repetitions=3,
        note="Query-independent native identity/provenance keys; excluded from warm computation.",
    )
    recorder.measure(
        "native_lexical_authentication_Q1",
        "EXPERIMENT_ONLY",
        lambda: require_lexical_result_snapshot(snapshot, data["values"]["query:Q1:A"]),
        warmup=0,
        repetitions=3,
    )
    ranking = data["values"]["query:Q1:B"]["ranking"]
    recorder.measure(
        "diagnostic_definition_wrapper_Q1",
        "CONTEXT_MATERIALIZATION",
        lambda: definitions(ranking),
        warmup=0,
        repetitions=3,
        note="Existing full diagnostic wrapper includes require_ranking, repeated native identity work and source extraction; compare cached pure projection in baseline. Not part of warm retrieval.",
    )
    analyses = tuple(
        data["values"]["ri:references:" + str(r.address)]
        for r in snapshot.resources
        if str(r.address).endswith(".py")
    )
    result = {
        "schema": "retrieval-performance-supplement-v1",
        "status": "COMPLETE",
        "measurements": recorder.measurements,
        "retained_python_object_graph": {
            "lexical_index_statistics": retained_size(data["state"].content),
            "native_reference_analyses": retained_size(analyses),
            "positive_native_references": retained_size(data["references"]),
            "native_resource_graph": retained_size(data["view"]),
            "normalized_graph_rows": retained_size(data["outgoing"]),
            "limitation": "Shared objects counted once per surface; overlapping surfaces cannot be summed. sys.getsizeof container/dataclass traversal excludes interpreter/global state and unvisited non-dataclass native internals; not RSS.",
        },
        "implementation_sha256": {
            path.relative_to(PACKAGE).as_posix(): sha(path.read_bytes())
            for path in (Path(__file__), PACKAGE / "memory.py")
        },
    }
    publish(output, result)
    return result


if __name__ == "__main__":
    run()
