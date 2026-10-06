# Copyright (c) 2026
# ruff: noqa: COM812, EM101, EM102, T201, TRY003 -- bounded case-local JSON/CLI convention
"""Freeze selected committed native input, with no task-relative query execution."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import json
import pickle
import sys
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from devtools.context.repository.document import RepositoryTextDocumentCollection
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )

from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical import (
    analyze_repository_text_document_collection,
    build_repository_text_lexical_inverted_index,
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.case_0009.artifacts import (
    CASE,
    ROOT,
    START,
    binary,
    digest,
    git,
    put_binary,
    put_json,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0009.protocol import TASK, task_inputs, treatment
from experiments.identifier_sparse.analysis import ANALYZER_SEMANTICS

REPOSITORY = Repository(RepositoryId.parse("5cf96d9e-d6a5-44a6-83d3-1e24f6e00009"))
STAGE_A = ("treatment.json", "inputs.pkl.gz", "pre_execution.json")


def eligible(path: str) -> bool:
    """Use broad established dogfood selection, never query/rank/gold inclusion."""
    if path in {
        "README.md",
        "AGENTS.md",
        "pyproject.toml",
        "scripts/validate_development.py",
    }:
        return True
    return (
        path.startswith(("src/", "tests/", "docs/"))
        and Path(path).suffix in {".py", ".md", ".toml", ".yaml", ".yml"}
        and path != "docs/implementation_ledger.md"
        and not path.startswith(
            ("tests/experiments/", "docs/research/", "docs/reports/")
        )
        and not any(
            "confirmation" in part.casefold() or "reserve" in part.casefold()
            for part in path.split("/")
        )
    )


def implementation_files() -> tuple[Path, ...]:
    """Pin concrete consumer and splitter code, not a generic dependency scanner."""
    return tuple(
        sorted(
            (
                *(ROOT / "experiments/identifier_sparse").glob("*.py"),
                *CASE.glob("*.py"),
                ROOT / "experiments/retrieval_identifier.py",
            )
        )
    )


def ensure_absent(root: Path, names: tuple[str, ...]) -> None:
    """Refuse overwrite before doing any stage work."""
    if any((root / name).exists() for name in names):
        raise FileExistsError(
            "Stage already exists; no overwrite or implicit recovery."
        )


async def freeze() -> dict[str, Any]:
    """Observe a selected Git export and freeze the shared native corpus once."""
    ensure_absent(
        CASE, (*STAGE_A, "integrity.json", "execution_started.json", "adjudication")
    )
    if (await git("rev-parse", "HEAD")).decode().strip() != START:
        raise ValueError("Expected starting HEAD differs.")
    if (await git("branch", "--show-current")).decode().strip() != "main":
        raise ValueError("Expected main branch.")
    if await git(
        "diff",
        START,
        "--name-only",
        "--",
        "src",
        "tests/context",
        "pyproject.toml",
        "uv.lock",
    ):
        raise ValueError("Production inputs changed.")
    tree = (await git("ls-tree", "-r", "--name-only", START)).decode().splitlines()
    if any(path.startswith("experiments/codex_dogfood/case_0009/") for path in tree):
        raise ValueError("Prospective case is not new.")
    addresses = tuple(sorted(path for path in tree if eligible(path)))
    selected = tuple(RepositoryResourceAddress(path) for path in addresses)
    archive = await git("archive", "--format=tar", START, "--", *addresses)
    task, queries = task_inputs()
    blob_digests = {}
    with TemporaryDirectory(prefix="r1-case0009-") as temporary:
        exported = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            for member in bundle.getmembers():
                if not member.isfile():
                    continue
                if member.name not in addresses:
                    raise ValueError("Unexpected archive member.")
                stream = bundle.extractfile(member)
                if stream is None:
                    raise ValueError("Missing archive bytes.")
                content = stream.read()
                blob_digests[member.name] = digest(content)
                put_text(exported / member.name, content.decode("utf-8"))
        if set(blob_digests) != set(addresses):
            raise ValueError("Selected archive coverage differs.")
        discovery = discover_repository_resource_addresses(
            repository=REPOSITORY,
            root=resolve_path(exported),
            maximum_resource_count=10000,
            maximum_traversal_entry_count=20000,
        )
        snapshot = observe_repository_resources(
            repository=REPOSITORY,
            root=resolve_path(exported),
            addresses=selected,
            maximum_resource_bytes=1 << 20,
        )
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=discovery, selected_addresses=selected
            ),
            snapshot=snapshot,
        )
        documents = represent_repository_text_corpus(corpus=corpus)
        # No query is analyzed or ranked here. Both treatment indexes build in B.
        request_frame = {
            "snapshot": snapshot,
            "corpus": corpus,
            "documents": documents,
            "task": task,
            "queries": queries,
        }
        native_bytes = gzip.compress(
            pickle.dumps(request_frame, protocol=pickle.HIGHEST_PROTOCOL), mtime=0
        )
        put_json(CASE / "treatment.json", treatment())
        put_binary(CASE / "inputs.pkl.gz", native_bytes)
        manifest = {
            "schema": "case-0009-stage-a-v1",
            "starting_head": START,
            "repository_id": str(snapshot.repository_id),
            "snapshot_id": str(snapshot.id),
            "corpus_id": str(corpus.id),
            "resource_count": len(documents.documents),
            "task_sha256": digest(TASK.encode()),
            "analyzer": ANALYZER_SEMANTICS,
            "representation_records_sha256": {
                name: digest(binary(ROOT / "experiments/identifier_sparse" / name))
                for name in ("analyzer_definition.json", "historical_diagnostic.json")
            },
            "resources": [
                {
                    "address": item.address.value,
                    "content_identity": item.content_identity.value,
                    "git_blob_sha256": blob_digests[item.address.value],
                }
                for item in snapshot.resources
            ],
            "implementation_sha256": {
                **{
                    item.address.value: digest(
                        item.content.replace("\r\n", "\n").encode()
                    )
                    for item in snapshot.resources
                    if item.address.value.startswith("src/")
                    and item.address.value.endswith(".py")
                },
                **{
                    path.relative_to(ROOT).as_posix(): digest(binary(path))
                    for path in implementation_files()
                },
            },
            "runtime": {
                "python": sys.version,
                "pickle_protocol": pickle.HIGHEST_PROTOCOL,
                "pyproject_sha256": digest(
                    await git("show", f"{START}:pyproject.toml")
                ),
                "lock_sha256": digest(await git("show", f"{START}:uv.lock")),
            },
            "stage_b": "ABSENT",
            "labels": "ABSENT",
            "query_execution": "NONE",
        }
        put_json(CASE / "pre_execution.json", manifest)
    put_json(
        CASE / "integrity.json",
        {
            "schema": "case-0009-stage-a-integrity-v1",
            "normalization": "UTF-8 LF; gzip exact",
            "sha256": {name: digest(binary(CASE / name)) for name in STAGE_A},
        },
    )
    return verify()


def verify() -> dict[str, Any]:
    """Verify immutable hashes before any trusted experiment pickle read."""
    integrity = read_json(CASE / "integrity.json")
    if set(integrity["sha256"]) != set(STAGE_A):
        raise ValueError("Stage A artifact coverage differs.")
    for name, expected in integrity["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Frozen Stage A artifact changed.")
    manifest = read_json(CASE / "pre_execution.json")
    if read_json(CASE / "treatment.json") != treatment():
        raise ValueError("Frozen treatment differs from its definition.")
    for name, expected in manifest["implementation_sha256"].items():
        if digest(binary(ROOT / name)) != expected:
            raise ValueError(f"Frozen implementation changed: {name}")
    verify_representation(manifest)
    if (
        manifest["task_sha256"] != digest(TASK.encode())
        or manifest["analyzer"] != ANALYZER_SEMANTICS
    ):
        raise ValueError("Task or analyzer identity differs.")
    return manifest


def verify_representation(manifest: dict[str, Any]) -> None:
    """Check the pre-diagnostic mechanism definition and execution environment."""
    for name, expected in manifest["representation_records_sha256"].items():
        if name not in {"analyzer_definition.json", "historical_diagnostic.json"}:
            raise ValueError("Unexpected representation record.")
        if digest(binary(ROOT / "experiments/identifier_sparse" / name)) != expected:
            raise ValueError("Frozen representation record changed.")
    definition = read_json(
        ROOT / "experiments/identifier_sparse/analyzer_definition.json"
    )
    for name, expected in definition["source_sha256"].items():
        if digest(binary(ROOT / name)) != expected:
            raise ValueError("Pre-diagnostic analyzer definition changed.")
    if manifest["runtime"]["python"] != sys.version:
        raise ValueError("Frozen Python runtime differs.")


def load_inputs() -> dict[str, Any]:
    """Read only our verified, trusted native Stage A archive; never old outcomes."""
    manifest = verify()
    native: dict[str, Any] = pickle.loads(  # noqa: S301 -- hash-verified trusted case archive
        gzip.decompress(binary(CASE / "inputs.pkl.gz"))
    )
    if (
        str(native["snapshot"].id) != manifest["snapshot_id"]
        or str(native["corpus"].id) != manifest["corpus_id"]
        or len(native["documents"].documents) != manifest["resource_count"]
    ):
        raise ValueError("Native identities differ from Stage A.")
    for document in native["documents"].documents:
        if document.resource != native["snapshot"].resource_at(
            document.resource.address
        ):
            raise ValueError("Native document does not belong to snapshot.")
    return native


def canonical_index(
    documents: RepositoryTextDocumentCollection,
) -> RepositoryTextLexicalInvertedIndex:
    """Build the unmodified production index for Arm A or mechanical fixtures."""
    return build_repository_text_lexical_inverted_index(
        corpus_statistics=calculate_repository_text_lexical_corpus_statistics(
            collection_analysis=analyze_repository_text_document_collection(
                document_collection=documents
            ),
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "verify"))
    arguments = parser.parse_args()
    result = asyncio.run(freeze()) if arguments.operation == "freeze" else verify()
    print(
        json.dumps(
            {
                "snapshot_id": result["snapshot_id"],
                "resources": result["resource_count"],
                "status": "VERIFIED STAGE A",
            }
        )
    )
