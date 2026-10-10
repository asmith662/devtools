# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, E501, EM101, TRY003, T201 -- bounded scientific CLI
"""Run frozen treatment once; all later finalization reads the durable native graph."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import platform
import sys
import unicodedata
from functools import partial
from pathlib import Path
from typing import Any

from devtools.context.localization.grounding.resolve import ground_task_anchor
from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    TaskProvenance,
    TaskTextSpan,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import RepositoryResourceDiscovery
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
    put_binary,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0012 import freeze, protocol
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal
from experiments.exact_hint_routing import behavior, routing
from experiments.exact_hint_routing.extraction import extract
from experiments.exact_hint_routing.models import (
    ExactHintIdentity,
    ExactHintObservation,
    ExactHintResolution,
    ExactHintRouteRequest,
    ExactHintRoutingView,
    HintAssociation,
    HintCategory,
    ResolutionDisposition,
)
from experiments.exact_hint_routing.presentation import present
from experiments.exact_hint_routing.serialization import project

STAGE_A = "4ff6d3950e6c0be834f136a649c1a127f91fdba3"
CAPTURE = Path(__file__).resolve().parent


def provenance(value: dict[str, Any]) -> TaskProvenance:
    """Restore exact frozen task provenance without normalizing author wording."""
    span = value.get("span")
    return TaskProvenance(
        value["source_identity"],
        None if span is None else TaskTextSpan(span["start"], span["end"]),
        value.get("explanation"),
    )


def inventories(treatment: dict[str, Any]) -> dict[str, Any]:
    """Rehydrate frozen callers and mechanical observations without repository lookup."""
    output = {}
    for arm, key in (
        ("B", "caller_reviewed_hint_reference"),
        ("C", "rule_extracted_hints"),
    ):
        hints = tuple(
            ExactHintObservation(
                protocol.TASK_ID,
                h["text"],
                TaskTextSpan(h["span"]["start"], h["span"]["end"]),
                h["rule"],
                h["syntactic_form"],
                HintCategory(h["category"]),
                provenance(h["provenance"]),
            )
            for h in treatment[key]
        )
        associations = tuple(
            HintAssociation(
                ExactHintIdentity(protocol.TASK_ID, a["hint"]["value"]),
                LocalizationObligationIdentity(protocol.TASK_ID, a["lane"]["value"]),
                a["reason"],
                provenance(a["provenance"]),
            )
            for a in treatment["hint_associations"]
        )
        output[arm] = tuple(
            routing.admit(h, a)
            for h in hints
            for a in associations
            if h.identity == a.hint
        )
        if [{**project(r), "identity": r.identity} for r in output[arm]] != treatment[
            "exact_route_requests"
        ][arm]:
            raise ValueError("Rehydrated frozen route differs")
    return output


def index_for(frame: routing.ExactFrame, metadata: dict[str, Any]) -> Any:
    """Rehydrate selected native corpus memberships; never discover new resources."""
    discovery = RepositoryResourceDiscovery(
        frame.repository_id,
        resolve_path(ROOT),
        10000,
        20000,
        len(frame.snapshot.resources),
        tuple(r.address for r in frame.snapshot.resources),
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery, selected_addresses=discovery.addresses
        ),
        snapshot=frame.snapshot,
    )
    documents = represent_repository_text_corpus(corpus=corpus)
    if str(corpus.id) != metadata["corpus_id"] or [
        str(d.id) for d in documents.documents
    ] != [r["document_identity"] for r in metadata["eligible_resource_frame"]]:
        raise ValueError("Native corpus/document identities differ")
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=documents
            )
        )
    )


async def execute() -> dict[str, Any]:  # noqa: C901 -- explicit one-time schedule
    """Authenticate before exclusive claim; no implicit resume or production retry."""
    await freeze.verify()
    if (await git("rev-parse", "HEAD")).decode().strip() != STAGE_A:
        raise ValueError("Unexpected Stage B parent")
    if (CAPTURE / "execution.claim").exists():
        raise FileExistsError("Execution already claimed; finalize/verify only")
    treatment = read_json(freeze.CASE / "treatment.json")
    metadata = read_json(freeze.CASE / "frame.json")
    frame = freeze.restore_frame(
        json.loads(gzip.decompress(binary(freeze.CASE / "inputs.json.gz")))
    )
    routes = inventories(treatment)
    for b, c in zip(routes["B"], routes["C"], strict=True):
        if behavior.route_input(frame, b) != behavior.route_input(frame, c):
            raise ValueError("Frozen semantic route inputs differ")
    sources = {
        p.relative_to(ROOT).as_posix(): digest(binary(p))
        for p in (*CAPTURE.glob("*.py"), freeze.CASE / "packet.py")
    }
    marker = {
        "case": "case-0012",
        "stage_a_commit": STAGE_A,
        "stage_a_integrity_sha256": digest(binary(freeze.CASE / "integrity.json")),
        "stage_a_trace_sha256": digest(binary(freeze.CASE / "trace.json")),
        "treatment_sha256": digest(binary(freeze.CASE / "treatment.json")),
        "frame": {
            k: metadata[k]
            for k in ("repository_id", "snapshot_id", "corpus_id", "frame_identity")
        },
        "implementation_sha256": {
            **read_json(freeze.CASE / "pre_execution.json")["implementation_sha256"],
            **sources,
        },
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "unicode": unicodedata.unidata_version,
        },
        "execution": "case-0012-stage-b-1",
        "starting_invocation_counts": {
            "exact_routes": 0,
            "lexical_queries": 0,
            "arms": 0,
        },
    }
    journal = Journal.start(CAPTURE, marker)
    journal.state["values"].update(frame=frame, metadata=metadata, treatment=treatment)
    journal.save()
    index = journal.call(
        "index-build", {"frame": frame.identity}, lambda: index_for(frame, metadata)
    )
    lexical = {}
    for key, text in [
        ("global", treatment["task_text"]),
        *[(o["key"], o["query"]) for o in treatment["obligations"]],
    ]:
        lexical[key] = journal.call(
            "lexical:" + key,
            {"query": text, "maximum_results": 531},
            partial(
                retrieve_repository_text_documents_by_bm25,
                query=analyze_repository_text_lexical_query(text=text),
                index=index,
                maximum_results=531,
            ),
        )
    journal.call("arm:A", {"lanes": list(lexical)}, lambda: lexical)
    original_ground = ground_task_anchor
    active_route = [""]
    grounding_counts: dict[str, int] = {}

    def observed_ground(**kwargs: Any) -> Any:
        key = active_route[0]
        grounding_counts[key] = grounding_counts.get(key, 0) + 1
        return journal.call(
            f"ground:{key}:{grounding_counts[key]}",
            project(kwargs["request"]),
            lambda: original_ground(**kwargs),
        )

    setattr(routing, "ground_task_anchor", observed_ground)  # noqa: B010 -- instrumented imported native boundary
    try:
        for arm in ("B", "C"):

            def capture_arm(arm: str = arm) -> dict[str, Any]:
                # Retain and time arm-specific task-only inventory processing.
                restored = journal.call(
                    "inventory:" + arm,
                    {"task": treatment["task_identity"]},
                    lambda: (
                        routes[arm]
                        if arm == "B"
                        else tuple(
                            d.observation
                            for d in extract(protocol.TASK_ID, treatment["task_text"])
                            if d.observation is not None
                        )
                    ),
                )
                if arm == "C" and tuple(r.hint for r in routes[arm]) != restored:
                    raise ValueError("Mechanical extraction changed")
                resolutions = []
                for n, request in enumerate(routes[arm], 1):
                    active_route[0] = f"{arm}:H{n:02}"

                    def resolve_request(
                        request: ExactHintRouteRequest = request,
                    ) -> ExactHintResolution:
                        return (
                            routing.resolve(frame, request)
                            if request.locator is not None
                            else ExactHintResolution(
                                request,
                                ResolutionDisposition.UNSUPPORTED,
                                (),
                                (),
                                request.reason,
                                frame.repository_id,
                                frame.snapshot_id,
                                frame.identity,
                            )
                        )

                    result = journal.call(
                        "route:" + active_route[0],
                        project(request),
                        resolve_request,
                    )
                    resolutions.append(result)
                views = {}
                for obligation in treatment["obligations"]:
                    key = obligation["key"]

                    def present_lane(key: str = key) -> ExactHintRoutingView:
                        return present(
                            frame=frame,
                            lane=LocalizationObligationIdentity(protocol.TASK_ID, key),
                            lexical=lexical[key],
                            global_safety=lexical["global"],
                            resolutions=tuple(
                                r
                                for r in resolutions
                                if r.request.association.lane.value == key
                            ),
                            provenance=TaskProvenance(
                                protocol.TASK_ID.value,
                                explanation=f"Arm {arm} frozen construction",
                            ),
                        )

                    views[key] = journal.call(
                        f"present:{arm}:{key}",
                        {"obligation": obligation["identity"]},
                        present_lane,
                    )
                return {"resolutions": tuple(resolutions), "views": views}

            journal.call(
                "arm:" + arm, {"routes": [r.identity for r in routes[arm]]}, capture_arm
            )
    finally:
        setattr(routing, "ground_task_anchor", original_ground)  # noqa: B010
    journal.state["state"] = "NATIVE_CAPTURE_COMPLETE"
    journal.save()
    return finalize()


def finalize() -> dict[str, Any]:
    """Finalize only from raw native state; no resolver/retrieval/presentation call."""
    from experiments.codex_dogfood.case_0012.stage_b import reporting  # noqa: PLC0415

    journal = Journal.load(CAPTURE)
    journal.ready()
    output = reporting.artifacts(journal.state)
    # An interrupted finalization may publish only matching deterministic bytes.
    for name, raw in output.items():
        destination = CAPTURE / name
        if destination.exists():
            if binary(destination) != raw:
                raise ValueError("Existing final capture differs; overwrite refused")
        elif name.endswith(".gz"):
            put_binary(destination, raw)
        else:
            put_text(destination, raw.decode())
    seal = {
        "schema": "case-0012-stage-b-integrity-v1",
        "sha256": {n: digest(raw) for n, raw in output.items()},
        "raw_checkpoint_sha256": digest(binary(CAPTURE / "raw_checkpoint.json")),
        "marker_sha256": digest(binary(CAPTURE / "execution_started.json")),
        "claim_sha256": digest(binary(CAPTURE / "execution.claim")),
    }
    if (CAPTURE / "integrity.json").exists():
        if read_json(CAPTURE / "integrity.json") != seal:
            raise ValueError("Final integrity differs")
    else:
        put_text(CAPTURE / "integrity.json", json_bytes(seal).decode())
    return verify()


def verify() -> dict[str, Any]:
    """Reconstruct capture and verify raw/final integrity without native execution."""
    from experiments.codex_dogfood.case_0012.stage_b import reporting  # noqa: PLC0415

    seal = read_json(CAPTURE / "integrity.json")
    for name, field in (
        ("raw_checkpoint.json", "raw_checkpoint_sha256"),
        ("execution_started.json", "marker_sha256"),
        ("execution.claim", "claim_sha256"),
    ):
        if digest(binary(CAPTURE / name)) != seal[field]:
            raise ValueError("Durable capture hash differs")
    journal = Journal.load(CAPTURE)
    journal.ready()
    if journal.state["state"] != "NATIVE_CAPTURE_COMPLETE":
        raise ValueError("Native capture incomplete")
    if journal.state["marker"]["stage_a_integrity_sha256"] != digest(
        binary(freeze.CASE / "integrity.json")
    ):
        raise ValueError("Stage A binding differs")
    for path, expected in journal.state["marker"]["implementation_sha256"].items():
        if digest(binary(ROOT / path)) != expected:
            raise ValueError("Execution implementation differs")
    output = reporting.artifacts(journal.state)
    if set(output) != set(seal["sha256"]):
        raise ValueError("Stage B seal coverage differs")
    for name, raw in output.items():
        if binary(CAPTURE / name) != raw or digest(raw) != seal["sha256"][name]:
            raise ValueError("Stage B deterministic replay differs")
    return read_json(CAPTURE / "summary.json")


def main() -> None:
    """Separate production execution from recovery-only finalization and replay."""
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("execute", "finalize", "verify"))
    operation = parser.parse_args().operation
    print(
        json.dumps(
            asyncio.run(execute())
            if operation == "execute"
            else finalize()
            if operation == "finalize"
            else verify(),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
