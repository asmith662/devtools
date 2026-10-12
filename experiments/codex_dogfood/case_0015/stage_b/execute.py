# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, T201, PLC0415 -- bounded scientific CLI
"""Claim once, capture every native return before the next operation, never resume."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import platform
import sys
import time
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import (
    represent_repository_text_corpus,
)
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
)
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from experiments.bm25f.fields import FieldState, validate_frame
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, exclusive
from experiments.codex_dogfood.case_0015 import freeze, protocol
from experiments.codex_dogfood.case_0015.stage_b.authenticate import (
    STAGE_A,
    authenticate,
)
from experiments.codex_dogfood.case_0015.stage_b.fingerprint import (
    SCHEMA,
    fingerprint,
    score,
)
from experiments.codex_dogfood.case_0015.stage_b.legacy import authenticate_failed
from experiments.codex_dogfood.case_0015.stage_b.records import (
    PreparedFields,
    PreparedFrame,
)

PACKAGE = Path(__file__).resolve().parent
EXECUTION = "case-0015-stage-b-2"
CAPTURE = PACKAGE / "attempts" / EXECUTION
SCHEDULE = (
    "frame:prepare",
    "fields:prepare",
    "index:native-prepare",
    "statistics:union-prepare",
    *(f"query:Q{i}:{arm}" for i in range(1, 7) for arm in ("A", "B")),
    "query:reference",
)


def source_hashes() -> dict[str, str]:
    """Seal only capture implementations and explicit reused durability dependencies."""
    paths = {
        *PACKAGE.glob("*.py"),
        PACKAGE / "README.md",
        PACKAGE / ".gitattributes",
        *(
            ROOT / "experiments/codex_dogfood/case_0012/stage_b" / n
            for n in ("durability.py", "graph.py", "canonical.py")
        ),
    }
    return {p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sorted(paths)}


def prepare(resources: list[dict[str, Any]], metadata: dict[str, Any]) -> PreparedFrame:
    """Observe only exact retained resources through native substrates once."""
    with TemporaryDirectory(prefix="case0015-native-frame-") as temporary:
        root = Path(temporary)
        for r in resources:
            put_text(root / r["address"], r["content"])
        discovery = discover_repository_resource_addresses(
            repository=freeze.REPOSITORY,
            root=resolve_path(root),
            maximum_resource_count=10000,
            maximum_traversal_entry_count=20000,
        )
        snapshot = observe_repository_resources(
            repository=freeze.REPOSITORY,
            root=resolve_path(root),
            addresses=tuple(RepositoryResourceAddress(r["address"]) for r in resources),
            maximum_resource_bytes=1 << 20,
        )
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=discovery,
                selected_addresses=tuple(r.address for r in snapshot.resources),
            ),
            snapshot=snapshot,
        )
        documents = represent_repository_text_corpus(corpus=corpus)
        if (
            str(snapshot.id) != metadata["snapshot_id"]
            or str(corpus.id) != metadata["corpus_id"]
        ):
            raise ValueError("Native frame reconstruction mismatch")
        for d, r in zip(documents.documents, resources, strict=True):
            if (
                str(d.id) != r["document_identity"]
                or str(d.resource.content_identity) != r["content_identity"]
                or d.text != r["content"]
                or str(d.resource.address) != r["address"]
            ):
                raise ValueError("Native exact resource/document/content mismatch")
        validate_frame(documents, snapshot)
        return PreparedFrame(documents, snapshot)


def prepare_fields(frame: PreparedFrame) -> PreparedFields:
    """Use the frozen canonical analysis/filename primitives with unchanged inputs."""
    return PreparedFields(
        analyze_repository_text_document_collection(
            document_collection=frame.documents
        ),
        build_repository_text_filename_lexical_index(
            document_collection=frame.documents
        ),
    )


def prepare_index(frame: PreparedFrame, fields: PreparedFields) -> FieldState:
    """Preserve native scientific state; replace only the capture metadata seal."""
    content = build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=fields.content
        )
    )
    state = FieldState(frame.documents, frame.snapshot, content, fields.filename, "")
    return FieldState(
        frame.documents, frame.snapshot, content, fields.filename, fingerprint(state)
    )


def union_statistics(state: FieldState) -> dict[str, Any]:
    """Capture all term/document memberships, without querying or scoring."""
    memberships: dict[str, dict[str, list[str]]] = {}
    for field, statistics in (
        ("CONTENT", state.content.corpus_statistics.document_statistics),
        ("FILENAME", state.filename.document_statistics),
    ):
        for d in statistics:
            for t in d.term_frequencies:
                memberships.setdefault(
                    t.normalized_term, {"CONTENT": [], "FILENAME": []}
                )[field].append(str(d.analysis.document.id))
    positions = {str(d.id): i for i, d in enumerate(state.collection.documents)}
    return {
        "N": len(positions),
        "terms": {
            t: {
                **fields,
                "union": sorted(
                    set(fields["CONTENT"]) | set(fields["FILENAME"]),
                    key=positions.__getitem__,
                ),
                "df_union": len(set(fields["CONTENT"]) | set(fields["FILENAME"])),
            }
            for t, fields in sorted(memberships.items())
        },
    }


async def execute() -> None:  # noqa: PLR0915 -- explicit once-only operation schedule
    """Authenticate unchanged Stage A and zero state before exclusively claiming."""
    if CAPTURE.exists():
        raise FileExistsError("Attempt already exists; native retry refused")
    attempts = PACKAGE / "attempts"
    if {p.name for p in attempts.iterdir()} != {"case-0015-stage-b-1"}:
        raise ValueError("Only immutable failed attempt 1 may precede attempt 2")
    authenticate_failed(attempts / "case-0015-stage-b-1")
    authentication = await authenticate()
    recovery = (await git("rev-parse", "HEAD")).decode().strip()
    if (
        recovery == STAGE_A
        or (await git("rev-parse", "origin/main")).decode().strip() != recovery
    ):
        raise ValueError("Committed synchronized recovery checkpoint required")
    recovery_seal = read_json(freeze.CASE / "recovery" / "integrity.json")
    for name, expected in recovery_seal["implementation"].items():
        if (
            digest(binary(ROOT / name)) != expected
            or digest(await git("show", recovery + ":" + name)) != expected
        ):
            raise ValueError("Recovery implementation mismatch")
    if (
        (await git("branch", "--show-current")).decode().strip() != "main"
        or (await git("diff", "--name-only")).strip()
        or (await git("diff", "--cached", "--name-only")).strip()
    ):
        raise ValueError("Clean tracked main/index required before execution")
    if any(
        (freeze.CASE / p).exists()
        for p in ("adjudication", "gold.json", "stage_d", "stage_c/packet")
    ):
        raise ValueError("Gold/effectiveness or prior packet contamination")
    design = read_json(freeze.CASE / "protocol.json")
    resources = json.loads(gzip.decompress(binary(freeze.CASE / "resources.json.gz")))
    metadata = read_json(freeze.CASE / "frame.json")
    queries = [
        analyze_repository_text_lexical_query(text=q["text"]) for q in design["queries"]
    ]
    marker = {
        "case": "0015",
        "execution": EXECUTION,
        "stage_a": STAGE_A,
        "recovery_checkpoint": recovery,
        "amendment": "METADATA_CAPTURE_ONLY; scientific semantics unchanged",
        "fingerprint_schema": SCHEMA,
        "record_schemas": [PreparedFrame.SCHEMA, PreparedFields.SCHEMA],
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
        "operation_schedule": SCHEDULE,
        "initial_counts": protocol.COUNTS,
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
    }
    wall_started = time.perf_counter_ns()
    j = Journal.start(CAPTURE, marker)
    mechanical_ns = 0
    try:
        frame = j.call(
            "frame:prepare",
            {"archive_sha256": digest(binary(freeze.CASE / "resources.json.gz"))},
            lambda: prepare(resources, metadata),
        )
        fields = j.call(
            "fields:prepare",
            {"corpus_id": metadata["corpus_id"], "fields": ["CONTENT", "FILENAME"]},
            lambda: prepare_fields(frame),
        )
        state = j.call(
            "index:native-prepare",
            {"corpus_id": metadata["corpus_id"], "documents": 515},
            lambda: prepare_index(frame, fields),
        )
        union = j.call(
            "statistics:union-prepare",
            {"N": 515, "rule": "document once across fields"},
            lambda: union_statistics(state),
        )
        from experiments.codex_dogfood.case_0015.stage_b.validation import (
            validate_fields,
            validate_pair,
        )

        validation_started = time.perf_counter_ns()
        surface = validate_fields(state, union)
        mechanical_ns += time.perf_counter_ns() - validation_started
        print("Durable frame/fields/native index/union statistics RETURNED", flush=True)
        for i, query in enumerate(queries, 1):
            binding = {
                "query": design["queries"][i - 1]["identity"],
                "obligation": design["queries"][i - 1]["obligation"],
                "text": query.text,
                "maximum_results": 515,
            }
            native = j.call(
                f"query:Q{i}:A",
                {**binding, "arm": "CANONICAL_ADDITIVE_BM25"},
                partial(
                    retrieve_repository_text_documents_by_bm25,
                    query=query,
                    index=state.content,
                    maximum_results=515,
                ),
            )
            print(f"Durable Q{i} Arm A RETURNED", flush=True)
            treatment = j.call(
                f"query:Q{i}:B",
                {**binding, "arm": "TRUE_BM25F", "parameters": design["parameters"]},
                partial(score, state, query, snapshot_id=state.snapshot.id),
            )
            validation_started = time.perf_counter_ns()
            validate_pair(
                state, native, treatment, surface, union, design["queries"][i - 1]
            )
            mechanical_ns += time.perf_counter_ns() - validation_started
            print(f"Durable Q{i} Arm B RETURNED", flush=True)
        reference = analyze_repository_text_lexical_query(
            text=design["global_reference_lane"]["text"]
        )
        j.call(
            "query:reference",
            {"text": reference.text, "maximum_results": 515, "canonical": True},
            lambda: retrieve_repository_text_documents_by_bm25(
                query=reference, index=state.content, maximum_results=515
            ),
        )
        j.complete()
    except BaseException as error:
        exclusive(
            CAPTURE / "capture_failure.json",
            {
                "execution": EXECUTION,
                "state": "FAILED; NO RETRY",
                "error_type": type(error).__qualname__,
                "error": str(error),
                "active": j.state["active"],
                "returned_operations": [
                    o["identity"]
                    for o in j.state["operations"]
                    if o["status"] == "RETURNED"
                ],
            },
        )
        raise
    exclusive(
        CAPTURE / "capture_costs.json",
        {
            "journal_publication_durability_ns": j.overhead_ns,
            "capture_wall_ns": time.perf_counter_ns() - wall_started,
            "mechanical_between_operation_validation_ns": mechanical_ns,
        },
    )
    print(
        "Complete immutable native capture; publication uses durable returns only",
        flush=True,
    )
    from experiments.codex_dogfood.case_0015.stage_b.reporting import publish

    publish(CAPTURE)


def main() -> None:
    """Execute one new attempt or exclusively publish/verify durable captured data."""
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--verify", action="store_true")
    modes.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if args.verify or args.publish:
        from experiments.codex_dogfood.case_0015.stage_b.reporting import (
            publish,
            verify,
        )

        asyncio.run(authenticate())
        (verify if args.verify else publish)(CAPTURE)
        print("Stage B mechanical PASS; no native operation invoked")
    else:
        asyncio.run(execute())


if __name__ == "__main__":
    main()
