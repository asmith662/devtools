# Copyright (c) 2026
# ruff: noqa: ANN401, B023, EM101, TRY003, PLR0915, PLR2004, T201, E501
"""Engineering baseline; never invoke a scientific treatment schedule."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.graph.walk import stationary_distribution
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_content_bm25,
)
from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
    score_repository_text_filename_lexical_bm25,
)
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.resources.filesystem import TextFile, write
from experiments.codex_dogfood.case_0009.artifacts import ROOT, git, json_bytes
from experiments.codex_dogfood.case_0015.stage_b.execute import prepare, prepare_fields
from experiments.codex_dogfood.case_0016.stage_b.execute import observed_ppr
from experiments.performance.retrieval import computation as c
from experiments.performance.retrieval.measurement import (
    Recorder,
    allocation,
    summary,
    viability,
)
from experiments.performance.retrieval.workload import (
    CAPTURE,
    CASE,
    authenticate,
    native_inputs,
    read_json,
    sha,
)
from experiments.task_conditioned_graph.diagnostic import render_map
from experiments.task_conditioned_graph.ranking import rank, require_ranking
from experiments.task_conditioned_graph.view import build_reference_view, require_view

PACKAGE = Path(__file__).resolve().parent


def publish(path: Path, value: object) -> None:
    """Atomically publish engineering output using the canonical filesystem."""
    path.parent.mkdir(parents=True, exist_ok=True)
    write(TextFile(resolve_path(path), json_bytes(value).decode()), overwrite=True)


def implementation_hashes() -> dict[str, str]:
    """Seal imported context implementations and benchmark adapters by physical bytes."""
    paths = {*PACKAGE.glob("*.py")}
    for module in tuple(sys.modules.values()):
        filename = getattr(module, "__file__", None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == ".py" and path.is_relative_to(
                ROOT / "src/devtools/context",
            ):
                paths.add(path)
    paths.update((ROOT / "experiments/task_conditioned_graph").glob("*.py"))
    paths.update(
        {
            ROOT / "experiments/codex_dogfood/case_0016/stage_b/execute.py",
            ROOT / "experiments/codex_dogfood/case_0012/stage_b/durability.py",
        },
    )
    return {
        path.relative_to(ROOT).as_posix(): sha(path.read_bytes())
        for path in sorted(paths)
    }


def setup() -> dict[str, Any]:
    """Prepare trusted retained native state once, with no gold access."""
    hashes = authenticate()
    values = native_inputs()
    frame, state, view = (
        values["frame:prepare"],
        values["lexical:index"],
        values["graph:construct"],
    )
    snapshot = frame.snapshot
    metadata = read_json(CASE / "frame.json")
    if (str(snapshot.id), str(snapshot.repository_id), len(snapshot.resources)) != (
        metadata["snapshot_id"],
        metadata["repository_id"],
        514,
    ):
        raise ValueError("Exact retained frame mismatch")
    if str(state.collection.corpus.id) != metadata["corpus_id"]:
        raise ValueError("Exact corpus mismatch")
    rows = read_json(CASE / "resources.json.gz")
    for document, row in zip(state.collection.documents, rows, strict=True):
        if (
            str(document.id),
            str(document.resource.content_identity),
            document.text,
            str(document.resource.address),
        ) != (
            row["document_identity"],
            row["content_identity"],
            row["content"],
            row["address"],
        ):
            raise ValueError("Exact document/content/address mismatch")
    positions = {node: i for i, node in enumerate(view.nodes)}
    outgoing: list[list[tuple[int, float]]] = [[] for _ in view.nodes]
    for edge in view.edges:
        outgoing[positions[edge.source]].append(
            (positions[edge.target], edge.probability),
        )
    if len(view.nodes) != 514 or len(view.edges) != 561:
        raise ValueError("Frozen graph dimensions mismatch")
    references = tuple(
        reference for edge in view.edges for reference in edge.references
    )
    descriptors = [
        (
            r.identity,
            r.occurrence.resource_address,
            r.target_resource.address,
            repr(r.occurrence.source_range),
        )
        for r in references
    ]
    definitions = {id(r): r.target_declaration.identity for r in references}
    return {
        "input_hashes": hashes,
        "values": values,
        "frame": frame,
        "state": state,
        "view": view,
        "positions": positions,
        "outgoing": outgoing,
        "references": references,
        "descriptors": descriptors,
        "definition_ids": definitions,
        "design": read_json(CASE / "protocol.json"),
        "metadata": metadata,
    }


def check_query(data: Any, q: str, result: Any) -> dict[str, Any]:
    """Check exact A/B/C order and numerical vectors, never effectiveness labels."""
    values = data["values"]
    a, b, fused, scores, iterations, converged, seeds, _, _ = result
    captured = values[f"query:{q}:B"]["ranking"]
    expected_a = read_json(CAPTURE / "arm_a.json.gz")[q]["matches"]
    expected_b = read_json(CAPTURE / "arm_b.json.gz")[q]
    expected_c = read_json(CAPTURE / "arm_c.json.gz")[q]
    if [str(address) for address in c.addresses(a)] != [
        row["address"] for row in expected_a
    ]:
        raise ValueError(q + " canonical A ordering mismatch; stop")
    if [str(address) for address in b] != [row["address"] for row in expected_b]:
        raise ValueError(q + " propagated B ordering mismatch; stop")
    if [str(address) for address, _ in fused] != [row["address"] for row in expected_c]:
        raise ValueError(q + " production C ordering mismatch; stop")
    if seeds != captured.seeds or iterations != captured.iterations or not converged:
        raise ValueError(q + " seed/convergence mismatch")
    error = max(
        abs(actual - state.stationary_mass)
        for actual, state in zip(scores, captured.states, strict=True)
    )
    if error > 1e-12:
        raise ValueError(q + " stationary vector mismatch")
    return {
        "A_order": "EXACT",
        "B_order": "EXACT",
        "C_order": "EXACT",
        "stationary_max_abs_error": error,
        "stationary_tolerance": 1e-12,
        "iterations": iterations,
        "seeds": [str(s) for s in seeds],
        "ranked_counts": {"A": len(a.matches), "B": len(b), "C": len(fused)},
    }


def convergence_observation(outgoing: Any, personalization: Any) -> dict[str, Any]:
    """Observe delta in one untimed call; no profiling during samples."""
    observations = []

    def observe(frame: Any, event: str, _argument: object) -> None:
        if frame.f_code is stationary_distribution.__code__ and event == "return":
            observations.append(
                {
                    "iterations": frame.f_locals["iterations"],
                    "final_l1_delta": frame.f_locals["delta"],
                },
            )

    if sys.getprofile() is not None:
        raise ValueError("Unexpected active profiler")
    sys.setprofile(observe)
    try:
        c.kernel(outgoing, personalization)
    finally:
        sys.setprofile(None)
    return observations[0]


def run(output: Path, *, inputs_only: bool = False) -> dict[str, Any]:  # noqa: C901, PLR0912 -- explicit bounded measurement schedule
    """Execute baseline surfaces; serialization and checks are outside timers."""
    progress: list[dict[str, Any]] = []

    def persist_progress(row: dict[str, Any]) -> None:
        progress.append(row)
        publish(output.parent / "progress.json", progress)

    recorder = Recorder(persist_progress)
    before = time.perf_counter_ns()
    recorder.emit("input_authentication_and_retained_loading", before, phase="START")
    data = setup()
    recorder.emit("input_authentication_and_retained_loading", before, phase="COMPLETE")
    values, frame, state, view = (
        data["values"],
        data["frame"],
        data["state"],
        data["view"],
    )
    snapshot, index = frame.snapshot, state.content
    rows = read_json(CASE / "resources.json.gz")
    design, positions, outgoing = data["design"], data["positions"], data["outgoing"]
    validation = {}
    for obligation in design["requirement_matrix"]:
        q = obligation["query_id"]
        validation[q] = check_query(
            data,
            q,
            c.warm(
                snapshot,
                index,
                view,
                outgoing,
                positions,
                obligation["query"],
                design["seed_policy"]["exact_locators"][q],
            ),
        )
    if inputs_only:
        print(json.dumps(validation, indent=2), flush=True)
        return validation
    result: dict[str, Any] = {
        "schema": "retrieval-performance-baseline-v1",
        "status": "RUNNING",
        "timestamp": Timestamp.now().isoformat(),
        "environment": {
            "os": platform.platform(),
            "python": sys.version,
            "processor": platform.processor(),
            "logical_cpus": os.cpu_count(),
            "architecture": platform.architecture()[0],
            "repository_head": asyncio.run(git("rev-parse", "HEAD")).decode().strip(),
            "gc_enabled": True,
            "tracemalloc_during_latency": False,
        },
        "workload": {
            "case": "0016",
            "execution": "case-0016-stage-b-2",
            "use": "INPUT_DATA_AND_SEMANTIC_OUTPUT_REFERENCE_ONLY",
            "frame": {
                k: data["metadata"][k]
                for k in ("repository_id", "snapshot_id", "corpus_id")
            },
            "resources": 514,
            "python_resources": 415,
            "native_references": 3954,
            "nodes": 514,
            "directed_pairs": 561,
            "dangling_nodes": 305,
        },
        "configuration": {
            "cheap_warmup": 10,
            "cheap_repetitions": 50,
            "nontrivial_warmup": 5,
            "nontrivial_repetitions": 30,
            "offline_repetitions": 3,
            "p95": "nearest rank ceil(0.95*n)-1",
            "standard_deviation": "population",
            "bm25": {"k1": 1.2, "b": 0.75, "filename_weight": 0.25},
            "ppr": {
                "damping": 0.85,
                "tolerance": 1e-10,
                "maximum_iterations": 200,
                "initial": "personalization",
                "dangling": "personalization",
            },
            "rrf": {"k": 60, "weights": [1, 1]},
            "lexical_seed_k": 10,
            "map_bytes": 8192,
        },
        "input_hashes": data["input_hashes"],
        "validation": validation,
        "measurements": recorder.measurements,
        "memory": {},
    }
    recorder.measure(
        "frame_archive_decode",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: read_json(CASE / "resources.json.gz"),
        warmup=0,
        repetitions=3,
    )
    recorder.measure(
        "frame_adaptation",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: prepare(rows, data["metadata"]),
        warmup=0,
        repetitions=3,
        note="Native retained-frame reconstruction includes temporary filesystem observation and frame identity checks; no journal/publication.",
    )
    fields = recorder.measure(
        "lexical_fields",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: prepare_fields(frame),
        warmup=0,
        repetitions=3,
    )

    def index_build() -> Any:
        return build_repository_text_lexical_inverted_index(
            corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
                collection_analysis=fields.content,
            ),
        )

    recorder.measure(
        "lexical_index",
        "OFFLINE_SNAPSHOT_BUILD",
        index_build,
        warmup=0,
        repetitions=3,
        note="Statistics and inverted index only; excludes experiment fingerprint.",
    )
    graph = recorder.measure(
        "graph_computation",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: c.graph_build(snapshot, data["descriptors"]),
        warmup=0,
        repetitions=3,
    )
    expected_edges = tuple(
        (
            edge.source,
            edge.target,
            tuple(r.identity for r in edge.references),
            edge.weight,
            edge.probability,
        )
        for edge in view.edges
    )
    if graph != (view.nodes, expected_edges):
        raise ValueError("Pure graph-build semantic mismatch")
    result["validation"]["graph"] = (
        "EXACT nodes/pairs/occurrence identities/weights/transitions"
    )
    modules = values["ri:module-universe"]
    source_rows = [row for row in rows if row["address"].endswith(".py")]
    native_addresses = {str(r.address): r.address for r in snapshot.resources}
    source_inputs = {
        str(r.address): tuple(
            i for i in modules.interpretations if i.resource.address == r.address
        )
        for r in snapshot.resources
        if str(r.address).endswith(".py")
    }
    derivation_samples = []
    source_samples: dict[str, list[int]] = {row["address"]: [] for row in source_rows}
    total_assessments, total_references = 0, 0
    for repetition in range(3):
        started = time.perf_counter_ns()
        recorder.emit(
            "full_ri_derivation",
            started,
            repetition=repetition + 1,
            total=3,
            phase="START",
        )
        total_assessments, total_references = 0, 0
        for number, row in enumerate(source_rows, 1):
            address = native_addresses[row["address"]]
            before = time.perf_counter_ns()
            derived = derive_python_declaration_references(
                snapshot,
                resource_address=address,
                module_universe=modules,
                source_interpretations=source_inputs[row["address"]],
            )
            elapsed = time.perf_counter_ns() - before
            source_samples[row["address"]].append(elapsed)
            total_assessments += derived.coverage.assessed_count
            total_references += len(derived.references)
            if derived != values["ri:references:" + row["address"]]:
                raise ValueError("RI native output mismatch: " + row["address"])
            if number % 50 == 0 or number == 415:
                recorder.emit(
                    "full_ri_derivation",
                    started,
                    repetition=repetition + 1,
                    sources=number,
                    total_sources=415,
                )
        derivation_samples.append(sum(times[-1] for times in source_samples.values()))
        if (total_assessments, total_references) != (50725, 3954):
            raise ValueError("RI assessment/reference count mismatch")
    recorder.measurements["full_ri_derivation"] = {
        "category": "OFFLINE_SNAPSHOT_BUILD",
        "warmup": 0,
        "samples_ns": derivation_samples,
        "summary": summary(derivation_samples),
        "note": "Sum of individually timed canonical per-resource derivations. Progress, equality checks, loop bookkeeping and publication excluded. No extra full warmup because three full passes are already expensive.",
        "source_samples_ns": source_samples,
        "per_source_summary": summary(
            [sample for samples in source_samples.values() for sample in samples],
        ),
        "assessments_per_second": total_assessments
        * 1e9
        / summary(derivation_samples)["median_ns"],
        "references_per_second": total_references
        * 1e9
        / summary(derivation_samples)["median_ns"],
    }
    representative = sorted(
        source_samples,
        key=lambda address: (summary(source_samples[address])["median_ns"], address),
    )[len(source_samples) // 2]
    address = native_addresses[representative]
    recorder.measure(
        "one_resource_ri",
        "INCREMENTAL_UPDATE",
        lambda: derive_python_declaration_references(
            snapshot,
            resource_address=address,
            module_universe=modules,
            source_interpretations=source_inputs[representative],
        ),
        warmup=5,
        repetitions=30,
        note="Existing per-resource primitive; candidate, not a complete invalidation system. Representative full-pass median source: "
        + representative,
    )
    result["ppr_observations"] = {}
    for obligation in design["requirement_matrix"]:
        q, text = obligation["query_id"], obligation["query"]
        locators = design["seed_policy"]["exact_locators"][q]
        query = recorder.measure(
            q + ".query_analysis",
            "ONLINE_QUERY",
            lambda: analyze_repository_text_lexical_query(text=text),
        )
        content = recorder.measure(
            q + ".content_scoring_and_ranking",
            "ONLINE_QUERY",
            lambda: retrieve_repository_text_documents_by_content_bm25(
                query=query,
                index=index,
                maximum_results=514,
            ),
        )
        filenames = recorder.measure(
            q + ".filename_scoring",
            "ONLINE_QUERY",
            lambda: score_repository_text_filename_lexical_bm25(
                query=query,
                index=state.filename,
                settings=c.SETTINGS,
            ),
        )
        matches = recorder.measure(
            q + ".final_lexical_ranking",
            "ONLINE_QUERY",
            lambda: c.final_lexical_ranking(index, content, filenames),
        )
        a = recorder.measure(
            q + ".bm25",
            "ONLINE_QUERY",
            lambda: c.lexical(index, text),
        )
        if matches != a.matches:
            raise ValueError(q + " split BM25 equivalence mismatch")
        _seeds, personalization = recorder.measure(
            q + ".seed_construction",
            "ONLINE_QUERY",
            lambda: c.seed_vector(snapshot, view.nodes, a, locators),
        )
        scores, iterations, _converged = recorder.measure(
            q + ".ppr",
            "ONLINE_QUERY",
            lambda: c.kernel(outgoing, personalization),
        )
        observed = convergence_observation(outgoing, personalization)
        observed["median_ns_per_iteration"] = (
            recorder.measurements[q + ".ppr"]["summary"]["median_ns"] / iterations
        )
        observed["flag_over_250ms"] = (
            recorder.measurements[q + ".ppr"]["summary"]["median_ns"] > 250_000_000
        )
        result["ppr_observations"][q] = observed
        flows = recorder.measure(
            q + ".pair_flow",
            "ONLINE_QUERY",
            lambda: c.pair_flow(view.edges, positions, scores),
        )
        incoming = recorder.measure(
            q + ".incoming_accumulation",
            "ONLINE_QUERY",
            lambda: c.accumulate(view.nodes, view.edges, flows),
        )
        recorder.measure(
            q + ".B_sort",
            "ONLINE_QUERY",
            lambda: c.ordered_flow(incoming),
        )
        b, _, _ = recorder.measure(
            q + ".B_projection",
            "ONLINE_QUERY",
            lambda: c.projection(view.nodes, view.edges, positions, scores),
        )
        ar = {address: rank for rank, address in enumerate(c.addresses(a), 1)}
        br = {address: rank for rank, address in enumerate(b, 1)}
        recorder.measure(q + ".rrf", "ONLINE_QUERY", lambda: c.rrf(ar, br))
        warm = recorder.measure(
            q + ".warm_graph_query",
            "ONLINE_QUERY",
            lambda: c.warm(snapshot, index, view, outgoing, positions, text, locators),
        )
        validation[q] = check_query(data, q, warm)
        ranking = values[f"query:{q}:B"]["ranking"]
        projected = recorder.measure(
            q + ".definition_projection",
            "CONTEXT_MATERIALIZATION",
            lambda: c.definition_projection(ranking, data["definition_ids"]),
        )
        captured_definitions = values[f"query:{q}:definitions"]
        if [(i, str(a), s) for i, a, s in projected] != [
            (p.definition, p.address, p.incoming_flow) for p in captured_definitions
        ]:
            raise ValueError(q + " definition projection mismatch")
        rendered = recorder.measure(
            q + ".map_rendering",
            "CONTEXT_MATERIALIZATION",
            lambda: render_map(captured_definitions),
        )
        if rendered != values[f"query:{q}:map"]:
            raise ValueError(q + " map output mismatch")
        result["memory"][q + ".ppr"] = allocation(
            lambda: c.kernel(outgoing, personalization),
        )
        result["memory"][q + ".warm_graph_query"] = allocation(
            lambda: c.warm(snapshot, index, view, outgoing, positions, text, locators),
        )
    hit = snapshot.resources[len(snapshot.resources) // 2].address
    miss = RepositoryResourceAddress("performance-benchmark-absent-resource.py")
    recorder.measure(
        "exact_lookup_hit",
        "ONLINE_QUERY",
        lambda: snapshot.resource_at(hit),
    )

    def lookup_miss() -> None:
        try:
            snapshot.resource_at(miss)
        except ValueError:
            return
        raise ValueError("Benchmark miss unexpectedly exists")

    recorder.measure("exact_lookup_miss", "ONLINE_QUERY", lookup_miss)
    recorder.measure(
        "canonical_filename_index_rebuild",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: build_repository_text_filename_lexical_index(
            document_collection=frame.documents,
        ),
        warmup=10,
        repetitions=50,
        note="Query-independent construction currently repeated inside canonical BM25 API; actual online BM25 samples include it.",
    )
    recorder.measure(
        "native_graph_build_with_checks",
        "OFFLINE_SNAPSHOT_BUILD",
        lambda: build_reference_view(snapshot, data["references"]),
        warmup=0,
        repetitions=3,
        note="Current experiment wrapper: endpoint/provenance identities and pair construction; separately compare pure graph computation.",
    )
    recorder.measure(
        "require_view",
        "EXPERIMENT_ONLY",
        lambda: require_view(snapshot, view),
        warmup=0,
        repetitions=3,
    )
    ranking = values["query:Q1:B"]["ranking"]
    recorder.measure(
        "require_ranking",
        "EXPERIMENT_ONLY",
        lambda: require_ranking(ranking),
        warmup=0,
        repetitions=3,
    )
    recorder.measure(
        "B_wrapper_without_profiler",
        "EXPERIMENT_ONLY",
        lambda: rank(
            snapshot,
            view,
            values["query:Q1:A"],
            values["query:Q1:exact"].resources,
        ),
        warmup=0,
        repetitions=3,
        note="Q1 frozen wrapper includes view/lexical validation, state construction and incoming diagnostics; engineering repetition only.",
    )
    recorder.measure(
        "B_wrapper_with_capture_profiler",
        "EXPERIMENT_ONLY",
        lambda: observed_ppr(
            lambda: rank(
                snapshot,
                view,
                values["query:Q1:A"],
                values["query:Q1:exact"].resources,
            ),
        ),
        warmup=0,
        repetitions=3,
        note="Q1 exact observed_ppr callback covers entire rank wrapper, not just kernel. No journal or scientific schedule.",
    )
    result["memory"]["lexical_index"] = allocation(index_build)
    result["memory"]["lexical_fields"] = allocation(lambda: prepare_fields(frame))
    result["memory"]["native_return_decode"] = allocation(native_inputs)
    result["memory"]["graph_computation"] = allocation(
        lambda: c.graph_build(snapshot, data["descriptors"]),
    )
    result["memory"]["limitations"] = (
        "tracemalloc incremental Python allocations; existing frame/graph/index excluded from warm peaks. Native-return decode includes all retained returns, a conservative upper bound for RI alone. No process RSS, allocator arenas, OS cache or external allocations measured. Memory runs are excluded from latency samples."
    )
    result["aggregates"] = {}
    for surface in (
        "bm25",
        "ppr",
        "B_projection",
        "rrf",
        "seed_construction",
        "warm_graph_query",
        "definition_projection",
        "map_rendering",
    ):
        samples = [
            sample
            for i in range(1, 7)
            for sample in recorder.measurements[f"Q{i}.{surface}"]["samples_ns"]
        ]
        result["aggregates"][surface] = {
            "summary": summary(samples),
            "viability": viability(
                summary(samples),
                50_000_000 if surface == "bm25" else 250_000_000,
            ),
            "meaning": "Pooled equal-count six-query samples; per-query results retained.",
        }
    costs = read_json(CAPTURE / "costs.json")
    result["captured_costs"] = costs
    result["captured_publication_costs"] = read_json(CAPTURE / "publication_costs.json")
    operation_costs = {
        row["operation"]: row["runtime_ns"] for row in costs["operations"]
    }
    result["harness_ratios"] = {
        f"Q{i}": {
            "captured_B_ns": operation_costs[f"query:Q{i}:B"],
            "pure_B_ns": recorder.measurements[f"Q{i}.ppr"]["summary"]["median_ns"]
            + recorder.measurements[f"Q{i}.B_projection"]["summary"]["median_ns"],
            "captured_C_ns": operation_costs[f"query:Q{i}:C"],
            "pure_RRF_ns": recorder.measurements[f"Q{i}.rrf"]["summary"]["median_ns"],
        }
        for i in range(1, 7)
    }
    for row in result["harness_ratios"].values():
        row["B_ratio"] = row["captured_B_ns"] / row["pure_B_ns"]
        row["C_ratio"] = row["captured_C_ns"] / row["pure_RRF_ns"]
    result["implementation_sha256"] = implementation_hashes()
    result["status"] = "COMPLETE"
    result["scientific_state"] = {
        "GRAPH-3": "COMPLETE / GRAPH_HARMFUL",
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "confirmation_reserve": "NOT_ACCESSED",
        "gold_join": "NOT_PERFORMED",
        "production_behavior": "UNCHANGED",
    }
    publish(output, result)
    recorder.emit(
        "baseline",
        recorder.started,
        phase="COMPLETE",
        output=str(output.relative_to(ROOT)),
    )
    return result


def main() -> None:
    """Publish a repeatable performance run, or check workload equivalence only."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PACKAGE / "results.json")
    parser.add_argument("--check-inputs", action="store_true")
    args = parser.parse_args()
    run(args.output.resolve(), inputs_only=args.check_inputs)


if __name__ == "__main__":
    main()
