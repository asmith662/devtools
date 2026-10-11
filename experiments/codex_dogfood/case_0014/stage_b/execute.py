# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812, E501, T201, PLC0415 -- bounded CLI with deferred cyclic publication import
"""Execute one claim; reconstruct publication only from durable native returns."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import sys
import time
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any

from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import (
    RepositoryTextDocumentCollection,
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
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
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
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, exclusive
from experiments.codex_dogfood.case_0014 import freeze, protocol
from experiments.codex_dogfood.case_0014.stage_b.authenticate import (
    STAGE_A,
    authenticate,
)
from experiments.query_term_weighting.classification import Arm, QueryPolicy
from experiments.query_term_weighting.scoring import score
from experiments.query_term_weighting.serialization import trace

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )

PACKAGE = Path(__file__).resolve().parent
EXECUTION = "case-0014-stage-b-1"
CAPTURE = PACKAGE / "attempts" / EXECUTION
SCHEDULE = (
    "frame:prepare",
    "index-build",
    *("query:Q" + str(i) for i in range(1, 7)),
    "query:reference",
    *(f"construct:{a}:Q{i}" for a in ("A", "B", "C") for i in range(1, 7)),
)


def source_hashes() -> dict[str, str]:
    """Pin all new capture/reporting/test code and reused durability substrates."""
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


def prepare(
    resources: list[dict[str, Any]], metadata: dict[str, Any]
) -> RepositoryTextDocumentCollection:
    """Use canonical native observation/representation on frozen retained text."""
    with TemporaryDirectory(prefix="case0014-native-frame-") as temporary:
        root = Path(temporary)
        for r in resources:
            put_text(root / r["address"], r["content"])
        discovery = discover_repository_resource_addresses(
            repository=freeze.REPOSITORY,
            root=resolve_path(root),
            maximum_resource_count=10000,
            maximum_traversal_entry_count=20000,
        )
        addresses = tuple(RepositoryResourceAddress(r["address"]) for r in resources)
        snapshot = observe_repository_resources(
            repository=freeze.REPOSITORY,
            root=resolve_path(root),
            addresses=addresses,
            maximum_resource_bytes=1 << 20,
        )
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=discovery, selected_addresses=addresses
            ),
            snapshot=snapshot,
        )
        documents = represent_repository_text_corpus(corpus=corpus)
        if (
            str(snapshot.id) != metadata["snapshot_id"]
            or str(corpus.id) != metadata["corpus_id"]
        ):
            raise ValueError("Native frame reconstruction mismatch")
        for document, row in zip(documents.documents, resources, strict=True):
            if (
                str(document.id) != row["document_identity"]
                or str(document.resource.content_identity) != row["content_identity"]
                or document.resource.content != row["content"]
            ):
                raise ValueError("Native resource/document/content mismatch")
        return documents


def build_index(
    documents: RepositoryTextDocumentCollection,
) -> RepositoryTextLexicalInvertedIndex:
    """Build one canonical content index; native queries own filename indexes."""
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=documents
            )
        )
    )


def construct(
    native: RepositoryTextLexicalBm25RetrievalResult, policy: QueryPolicy, arm: Arm
) -> dict[str, Any]:
    """Time frozen multiplier/application/sort/trace as one captured operation."""
    return trace(score(native, policy, arm))


async def execute() -> None:
    """Authenticate and claim before every prospective operation; never resume."""
    if CAPTURE.exists():
        raise FileExistsError("Attempt already exists; native retry refused")
    authentication = await authenticate()
    for reference in ("HEAD", "origin/main"):
        if (await git("rev-parse", reference)).decode().strip() != STAGE_A:
            raise ValueError("Unexpected capture parent")
    if (
        (await git("branch", "--show-current")).decode().strip() != "main"
        or (await git("diff", "--name-only")).strip()
        or (await git("diff", "--cached", "--name-only")).strip()
    ):
        raise ValueError("Clean tracked main/index required before execution")
    if any(
        (freeze.CASE / p).exists() for p in ("adjudication", "gold.json", "stage_d")
    ):
        raise ValueError("Gold/effectiveness contamination")
    resources = json.loads(gzip.decompress(binary(freeze.CASE / "resources.json.gz")))
    metadata = read_json(freeze.CASE / "frame.json")
    classified_started = time.perf_counter_ns()
    policies = protocol.policies(protocol.authored()["task_text"])
    classification_restore_ns = time.perf_counter_ns() - classified_started
    marker = {
        "case": "0014",
        "execution": EXECUTION,
        "stage_a": STAGE_A,
        "authentication": authentication,
        "frame": authentication["frame"],
        "protocol_sha256": authentication["protocol_sha256"],
        "implementation_sha256": source_hashes(),
        "runtime": {
            "python": list(sys.version_info[:3]),
            "implementation": sys.implementation.name,
        },
        "operation_schedule": SCHEDULE,
        "initial_counts": protocol.COUNTS,
        "classification_restoration_verification_ns": classification_restore_ns,
        "gold": "ABSENT",
        "effectiveness": "UNKNOWN",
        "outcome": "NOT_SELECTED",
    }
    wall_started = time.perf_counter_ns()
    journal = Journal.start(CAPTURE, marker)
    try:
        documents = journal.call(
            "frame:prepare",
            {
                "resource_archive_sha256": digest(
                    binary(freeze.CASE / "resources.json.gz")
                )
            },
            lambda: prepare(resources, metadata),
        )
        index = journal.call(
            "index-build",
            {"corpus_id": metadata["corpus_id"], "documents": len(documents.documents)},
            lambda: build_index(documents),
        )
        print("Durable frame/index RETURNED", flush=True)
        native = {}
        for p in policies:
            key = p.identity.value
            native[key] = journal.call(
                "query:" + key,
                {
                    "identity": key,
                    "obligation": p.obligation.value,
                    "text": p.native_query.text,
                    "maximum_results": 515,
                },
                partial(
                    retrieve_repository_text_documents_by_bm25,
                    query=p.native_query,
                    index=index,
                    maximum_results=515,
                ),
            )
            print("Durable native " + key + " RETURNED", flush=True)
        reference_query = analyze_repository_text_lexical_query(
            text=protocol.authored()["global_reference_lane"]["text"]
        )
        journal.call(
            "query:reference",
            {"text": reference_query.text, "maximum_results": 515, "weighted": False},
            lambda: retrieve_repository_text_documents_by_bm25(
                query=reference_query, index=index, maximum_results=515
            ),
        )
        for arm in Arm:
            for p in policies:
                key = p.identity.value
                journal.call(
                    f"construct:{arm.name}:{key}",
                    {
                        "arm": arm.name,
                        "query": key,
                        "native_operation": "query:" + key,
                        "frozen_policy_sha256": digest(
                            json_bytes(
                                read_json(freeze.CASE / "protocol.json")["queries"][
                                    int(key[1:]) - 1
                                ]
                            )
                        ),
                    },
                    partial(construct, native[key], p, arm),
                )
            print("Durable Arm " + arm.name + " construction RETURNED", flush=True)
        journal.complete()
    except BaseException as error:
        exclusive(
            CAPTURE / "capture_failure.json",
            {
                "execution": EXECUTION,
                "error_type": type(error).__qualname__,
                "error": str(error),
                "active_operations": journal.state["active"],
                "boundary": "STOP; immutable ENTERED/RETURNED records authoritative; NO RETRY",
            },
        )
        raise
    exclusive(
        CAPTURE / "publication_cost.json",
        {
            "capture_wall_ns": time.perf_counter_ns() - wall_started,
            "journal_publication_durability_ns": journal.overhead_ns,
            "classification_restoration_verification_ns": classification_restore_ns,
            "accounting": "Non-mechanism publication/durability and descriptive wall only; no double counting",
        },
    )
    finalize()


def finalize() -> None:
    """Deterministically publish only from complete immutable captured values."""
    from experiments.codex_dogfood.case_0014.stage_b.reporting import outputs

    if (CAPTURE / "integrity.json").exists():
        raise FileExistsError("Stage B publication overwrite refused")
    journal = Journal.load(CAPTURE)
    journal.ready()
    if journal.state["state"] != "NATIVE_CAPTURE_COMPLETE":
        raise ValueError("Incomplete capture cannot be published")
    started = time.perf_counter_ns()
    values = outputs(journal)
    for name, raw in values.items():
        if (CAPTURE / name).exists():
            if binary(CAPTURE / name) != raw:
                raise ValueError("Partial derived publication tamper: " + name)
            continue
        if name.endswith(".gz"):
            put_binary(CAPTURE / name, raw)
        else:
            put_text(CAPTURE / name, raw.decode())
    exclusive(
        CAPTURE / "finalization_cost.json",
        {
            "derivation_publication_ns": time.perf_counter_ns() - started,
            "accounting": "Separate; no treatment timing rerun",
        },
    )
    files = {
        p.relative_to(CAPTURE).as_posix(): digest(binary(p))
        for p in sorted(CAPTURE.rglob("*"))
        if p.is_file()
    }
    put_text(
        CAPTURE / "integrity.json",
        json_bytes(
            {
                "execution": EXECUTION,
                "stage_a": STAGE_A,
                "sha256": files,
                "implementation_sha256": source_hashes(),
                "gold": "ABSENT",
                "effectiveness": "UNKNOWN",
                "outcome": "NOT_SELECTED",
            }
        ).decode(),
    )


def verify() -> dict[str, Any]:
    """Replay pure transformations; never rebuild an index or invoke a query."""
    from experiments.codex_dogfood.case_0014.stage_b.reporting import outputs

    seal = read_json(CAPTURE / "integrity.json")
    actual = {
        p.relative_to(CAPTURE).as_posix()
        for p in CAPTURE.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    if (
        actual != set(seal["sha256"])
        or any(digest(binary(CAPTURE / p)) != h for p, h in seal["sha256"].items())
        or seal["implementation_sha256"] != source_hashes()
    ):
        raise ValueError("Stage B integrity/implementation tamper")
    journal = Journal.load(CAPTURE)
    for name, raw in outputs(journal).items():
        if binary(CAPTURE / name) != raw:
            raise ValueError("Deterministic mechanical replay mismatch: " + name)
    return read_json(CAPTURE / "validation.json")


def main() -> None:
    """Explicit execute, pure finalize, or pure verification CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("execute", "finalize", "verify"))
    mode = parser.parse_args().mode
    if mode == "execute":
        asyncio.run(execute())
    elif mode == "finalize":
        finalize()
    else:
        print(json.dumps(verify(), indent=2))


if __name__ == "__main__":
    main()
