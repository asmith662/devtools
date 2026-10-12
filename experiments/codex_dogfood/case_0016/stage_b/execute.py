# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, T201, E501, PLC0415, PLR0915, B023, TC003, TRY301
"""Exclusive claim, immutable native returns, no resume or scientific retry."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import platform
import sys
import time
from collections.abc import Callable
from functools import partial
from threading import Event, Thread
from types import FrameType
from typing import Any

from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.graph.walk import stationary_distribution
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.core.time import Timestamp
from devtools.resources.filesystem.errors import FilesystemPermissionError
from experiments.codex_dogfood.case_0009.artifacts import binary, digest, git, read_json
from experiments.codex_dogfood.case_0012.stage_b.durability import (
    Journal as NativeJournal,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import exclusive
from experiments.codex_dogfood.case_0015.stage_b.execute import (
    prepare,
    prepare_fields,
    prepare_index,
)
from experiments.codex_dogfood.case_0016 import freeze, protocol
from experiments.codex_dogfood.case_0016.stage_b.authenticate import (
    CAPTURE,
    EXECUTION,
    SCHEDULE_PATH,
    STAGE_A,
    authenticate,
    source_hashes,
)
from experiments.codex_dogfood.case_0016.stage_b.durability import Journal
from experiments.task_conditioned_graph.diagnostic import definitions, render_map
from experiments.task_conditioned_graph.ranking import fuse, rank, seed_union
from experiments.task_conditioned_graph.seeds import resolve_exact_seeds
from experiments.task_conditioned_graph.view import build_reference_view, require_view


def schedule(rows: list[dict[str, Any]]) -> tuple[str, ...]:
    """Freeze only mechanical composition; never inspect reference connectivity."""
    return (
        "frame:prepare",
        "lexical:fields",
        "lexical:index",
        "ri:module-universe",
        *(
            "ri:references:" + r["address"]
            for r in rows
            if r["address"].endswith(".py")
        ),
        "graph:construct",
        "graph:validate",
        *(
            f"query:Q{i}:{step}"
            for i in range(1, 7)
            for step in ("A", "exact", "seeds", "B", "C", "definitions", "map")
        ),
        "query:reference",
    )


def universe(snapshot: Any) -> Any:
    """Use precisely src/. interpretations, retaining native sources and universe."""
    interpretations: list[Any] = []
    for root, prefix in (("src", "src/"), (".", "")):
        addresses = tuple(
            r.address
            for r in snapshot.resources
            if str(r.address).endswith(".py")
            and (
                str(r.address).startswith(prefix)
                if prefix
                else not str(r.address).startswith("src/")
            )
        )
        result = interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=addresses,
        )
        interpretations.extend(result.interpretations)
    return define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=tuple(interpretations),
    )


def observed_ppr(invoke: Callable[[], Any]) -> dict[str, Any]:
    """Observe actual kernel return locals; no replacement kernel or second walk.

    Python's return profiler reads the final delta from the one frozen native
    invocation. It cannot change arithmetic/inputs/results. Its overhead is part
    of the single captured experimental timing, not a production cost claim.
    """
    if sys.getprofile() is not None:
        raise ValueError("Existing profiler prevents unambiguous kernel observation")
    observations: list[dict[str, Any]] = []

    def observe(frame: FrameType, event: str, _argument: object) -> None:
        if frame.f_code is stationary_distribution.__code__ and event == "return":
            observations.append(
                {
                    "iterations": frame.f_locals["iterations"],
                    "final_delta": frame.f_locals["delta"],
                    "converged": frame.f_locals["converged"],
                },
            )

    sys.setprofile(observe)
    try:
        result = invoke()
    finally:
        sys.setprofile(None)
    expected = 1 if result.seeds else 0
    if len(observations) != expected:
        raise ValueError("Native PPR invocation count differs")
    return {"ranking": result, "kernel_observations": observations}


class Progress:
    """Append-only derived progress, outside scientific success boundaries."""

    def __init__(self, journal: NativeJournal, total: int) -> None:
        """Bind progress only to this journal and frozen operation count."""
        self.journal, self.total = journal, total
        self.started = time.perf_counter_ns()
        self.count = 0
        self.warnings: list[dict[str, Any]] = []
        try:
            (journal.root / "progress").mkdir()
        except OSError as error:
            self.warnings.append({"phase": "CREATE_PROGRESS", "error": str(error)})

    def emit(self, identity: str, sequence: int, phase: str, started: int) -> None:
        """Persist timestamp and operation/total elapsed time before printing."""
        value: dict[str, Any] = {
            "timestamp": Timestamp.now().isoformat(),
            "operation": identity,
            "sequence": sequence,
            "total_operations": self.total,
            "phase": phase,
            "operation_elapsed_ns": time.perf_counter_ns() - started,
            "total_elapsed_ns": time.perf_counter_ns() - self.started,
            "returned_or_entered_journal_chain_sha256": self.journal.chain,
        }
        self.count += 1
        try:
            exclusive(self.journal.root / "progress" / f"{self.count:06}.json", value)
        except (OSError, FilesystemPermissionError) as error:
            self.warnings.append(
                {
                    **value,
                    "error_type": type(error).__qualname__,
                    "error": str(error),
                    "scientific_consequence": "NONE",
                },
            )
        try:
            print(
                f"{value['timestamp']} {sequence}/{self.total} {identity} {phase} operation={value['operation_elapsed_ns'] / 1e9:.3f}s total={value['total_elapsed_ns'] / 1e9:.3f}s",
                flush=True,
            )
        except OSError as error:
            self.warnings.append({"phase": "TERMINAL_PROGRESS", "error": str(error)})

    def call(self, identity: str, inputs: object, invoke: Callable[[], Any]) -> Any:
        """Advance after native RETURNED; progress warnings cannot veto it."""
        sequence = len(self.journal.state["operations"]) + 1
        if self.journal.state["marker"]["operation_schedule"][sequence - 1] != identity:
            raise ValueError("Frozen operation schedule differs")
        started = time.perf_counter_ns()
        self.emit(identity, sequence, "ENTERING", started)
        stop = Event()

        def heartbeat() -> None:
            while not stop.wait(20):
                self.emit(identity, sequence, "ACTIVE", started)

        thread = Thread(target=heartbeat, daemon=True)
        thread.start()
        try:
            return self.journal.call(identity, inputs, invoke)
        finally:
            stop.set()
            thread.join()
            self.emit(identity, sequence, "JOURNAL_BOUNDARY", started)


async def execute() -> None:
    """Make the exclusive durable claim before any prospective native operation."""
    if CAPTURE.exists():
        raise FileExistsError("Authoritative execution already claimed; no retry")
    authentication = await authenticate()
    from experiments.codex_dogfood.case_0016.stage_b.recovery import (
        authenticate_recovery,
    )

    recovery = await authenticate_recovery()
    if (
        (await git("rev-parse", "HEAD")).decode().strip() != recovery["checkpoint"]
        or (await git("rev-parse", "origin/main")).decode().strip()
        != recovery["checkpoint"]
        or (await git("branch", "--show-current")).decode().strip() != "main"
        or (await git("diff", "--name-only")).strip()
        or (await git("diff", "--cached", "--name-only")).strip()
    ):
        raise ValueError("Exact clean synchronized recovery checkpoint required")
    if any(
        (freeze.CASE / name).exists()
        for name in ("adjudication", "gold.json", "stage_d", "stage_c/packet")
    ):
        raise ValueError("Prior result/gold contamination")
    rows = json.loads(gzip.decompress(binary(freeze.CASE / "resources.json.gz")))
    design, metadata = (
        read_json(freeze.CASE / "protocol.json"),
        read_json(freeze.CASE / "frame.json"),
    )
    operations = schedule(rows)
    schedule_path = SCHEDULE_PATH
    if tuple(read_json(schedule_path)["operations"]) != operations:
        raise ValueError("Committed attempt-2 operation schedule differs")
    marker = {
        "case": "0016",
        "execution": EXECUTION,
        "stage_a": STAGE_A,
        "recovery_checkpoint": recovery["checkpoint"],
        "recovery_integrity_sha256": recovery["integrity_sha256"],
        "attempt_1": "FAILED_AUDIT_ONLY / NEVER INPUT TO ATTEMPT 2",
        "attempt_1_failed_audit_sha256": recovery["attempt_1_failed_audit_sha256"],
        "scientific_implementation_sha256": read_json(freeze.CASE / "integrity.json")[
            "implementation"
        ],
        "authentication": authentication,
        "frame": authentication["frame"],
        "protocol_sha256": authentication["protocol_sha256"],
        "implementation_sha256": source_hashes(),
        "runtime": {
            "python": list(sys.version_info[:3]),
            "implementation": sys.implementation.name,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "operation_schedule": operations,
        "schedule_sha256": digest(binary(schedule_path)),
        "initial_counts": protocol.COUNTS,
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
    }
    wall = time.perf_counter_ns()
    journal = Journal.start(CAPTURE, marker)
    progress = Progress(journal, len(operations))
    call = progress.call
    try:
        frame = call(
            "frame:prepare",
            {"archive_sha256": digest(binary(freeze.CASE / "resources.json.gz"))},
            lambda: prepare(rows, metadata),
        )
        fields = call("lexical:fields", {"N": len(rows)}, lambda: prepare_fields(frame))
        state = call(
            "lexical:index",
            {"N": len(rows)},
            lambda: prepare_index(frame, fields),
        )
        modules = call(
            "ri:module-universe",
            {"module_roots": ["src", "."]},
            lambda: universe(frame.snapshot),
        )
        assessments = []
        for row in rows:
            if not row["address"].endswith(".py"):
                continue
            address = RepositoryResourceAddress(row["address"])
            source = tuple(
                i for i in modules.interpretations if i.resource.address == address
            )
            assessments.append(
                call(
                    "ri:references:" + str(address),
                    {
                        "address": str(address),
                        "content_identity": row["content_identity"],
                        "universe": modules.identity,
                    },
                    partial(
                        derive_python_declaration_references,
                        frame.snapshot,
                        resource_address=address,
                        module_universe=modules,
                        source_interpretations=source,
                    ),
                ),
            )
        references = tuple(r for a in assessments for r in a.references)
        view = call(
            "graph:construct",
            {"family": "REFERENCE", "assessed_resources": len(assessments)},
            lambda: build_reference_view(frame.snapshot, references),
        )
        call(
            "graph:validate",
            {"frame": marker["frame"]},
            lambda: require_view(frame.snapshot, view),
        )
        for i, obligation in enumerate(design["requirement_matrix"], 1):
            query = analyze_repository_text_lexical_query(text=obligation["query"])
            binding = {
                "query": f"Q{i}",
                "obligation": obligation["obligation"],
                "text": query.text,
                "maximum_results": len(rows),
            }
            lexical = call(
                f"query:Q{i}:A",
                binding,
                partial(
                    retrieve_repository_text_documents_by_bm25,
                    query=query,
                    index=state.content,
                    maximum_results=len(rows),
                ),
            )
            exact = call(
                f"query:Q{i}:exact",
                binding,
                lambda: resolve_exact_seeds(
                    frame.snapshot,
                    query.text,
                    tuple(
                        RepositoryResourceAddress(s)
                        for s in design["seed_policy"]["exact_locators"][f"Q{i}"]
                    ),
                ),
            )
            call(
                f"query:Q{i}:seeds",
                {"K": 10},
                lambda: seed_union(frame.snapshot, lexical, exact.resources),
            )
            observed = call(
                f"query:Q{i}:B",
                {**binding, "arm": design["arms"]["B"]},
                lambda: observed_ppr(
                    lambda: rank(frame.snapshot, view, lexical, exact.resources),
                ),
            )
            ranking = observed["ranking"]
            call(
                f"query:Q{i}:C",
                {**binding, "arm": design["arms"]["C"]},
                lambda: fuse(ranking),
            )
            projected = call(
                f"query:Q{i}:definitions",
                {"flow": "equal per native occurrence"},
                lambda: definitions(ranking),
            )
            call(
                f"query:Q{i}:map",
                {"budget_utf8_bytes": 8192, "header_characters": 240},
                lambda: render_map(projected),
            )
        reference = analyze_repository_text_lexical_query(text=design["task_text"])
        call(
            "query:reference",
            {"text": reference.text, "maximum_results": len(rows)},
            partial(
                retrieve_repository_text_documents_by_bm25,
                query=reference,
                index=state.content,
                maximum_results=len(rows),
            ),
        )
        if tuple(o["identity"] for o in journal.state["operations"]) != operations:
            raise ValueError("Complete operation schedule differs")
        journal.complete()
    except BaseException as error:
        exclusive(
            CAPTURE / "capture_failure.json",
            {
                "execution": EXECUTION,
                "state": "FAILED; NO RETRY",
                "error_type": type(error).__qualname__,
                "error": str(error),
                "active": journal.state["active"],
                "returned_operations": [
                    o["identity"]
                    for o in journal.state["operations"]
                    if o["status"] == "RETURNED"
                ],
            },
        )
        raise
    exclusive(
        CAPTURE / "capture_costs.json",
        {
            "journal_publication_durability_ns": journal.overhead_ns,
            "capture_wall_ns": time.perf_counter_ns() - wall,
            "progress_records": progress.count,
            "derived_progress_warnings": progress.warnings,
        },
    )
    from experiments.codex_dogfood.case_0016.stage_b.reporting import publish

    publish(CAPTURE)


def main() -> None:
    """Verification reads immutable returns; execution never resumes a claim."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    if parser.parse_args().verify:
        from experiments.codex_dogfood.case_0016.stage_b.reporting import verify

        asyncio.run(authenticate())
        verify(CAPTURE)
        print("Case 0016 Stage B PASS; no scientific operation rerun")
    else:
        asyncio.run(execute())


if __name__ == "__main__":
    main()
