# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, T201 -- explicit frozen experiment boundary
"""Freeze the original starting Git frame after immutable manual authoring."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import pickle
import sys
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from experiments.codex_dogfood.acquisition.trace import layer, review
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    put_binary,
    put_json,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0009.freeze import (
    REPOSITORY,
    eligible,
    ensure_absent,
)
from experiments.codex_dogfood.case_0011.protocol import (
    AUTHOR_HASHES,
    CASE,
    START,
    definition,
)

GENERATED = (
    "treatment.json",
    "inputs.pkl.gz",
    "pre_execution.json",
    "stage_a_trace.json",
    "STAGE_A_REVIEW.md",
)
SEALED = (*AUTHOR_HASHES, *GENERATED, "PROTOCOL.md", "CONTRACTS.md", "C5_PROTOCOL.md")


async def freeze() -> dict[str, Any]:
    """Export exact broad eligible bytes; never run a retrieval query."""
    ensure_absent(
        CASE, (*GENERATED, "integrity.json", "execution_started.json", "adjudication")
    )
    if (await git("rev-parse", "HEAD")).decode().strip() != START or (
        await git("branch", "--show-current")
    ).decode().strip() != "main":
        raise ValueError("Expected clean-start main checkpoint differs")
    treatment, task, queries = definition()
    tree = (await git("ls-tree", "-r", "--name-only", START)).decode().splitlines()
    addresses = tuple(sorted(p for p in tree if eligible(p)))
    if any("case_0011" in p for p in tree):
        raise ValueError("Case 0011 existed in starting frame")
    if await git(
        "diff", START, "--name-only", "--", "src", "pyproject.toml", "uv.lock"
    ):
        raise ValueError("Production implementation changed")
    archive = await git("archive", "--format=tar", START, "--", *addresses)
    blobs = {}
    with TemporaryDirectory(prefix="case0011-source-") as temporary:
        root = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            for member in bundle.getmembers():
                if member.isdir():
                    continue
                if not member.isfile() or member.name not in addresses:
                    raise ValueError("Unexpected source archive member")
                stream = bundle.extractfile(member)
                if stream is None:
                    raise ValueError("Missing source archive content")
                data = stream.read()
                blobs[member.name] = digest(data)
                put_text(root / member.name, data.decode("utf-8"))
        if set(blobs) != set(addresses):
            raise ValueError("Source archive coverage differs")
        discovery = discover_repository_resource_addresses(
            repository=REPOSITORY,
            root=resolve_path(root),
            maximum_resource_count=10000,
            maximum_traversal_entry_count=20000,
        )
        snapshot = observe_repository_resources(
            repository=REPOSITORY,
            root=resolve_path(root),
            addresses=tuple(RepositoryResourceAddress(p) for p in addresses),
            maximum_resource_bytes=1 << 20,
        )
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=discovery,
                selected_addresses=tuple(
                    RepositoryResourceAddress(p) for p in addresses
                ),
            ),
            snapshot=snapshot,
        )
        docs = represent_repository_text_corpus(corpus=corpus)
    native = {
        "snapshot": snapshot,
        "corpus": corpus,
        "documents": docs,
        "task": task,
        "queries": queries,
    }
    put_binary(
        CASE / "inputs.pkl.gz",
        gzip.compress(pickle.dumps(native, protocol=pickle.HIGHEST_PROTOCOL), mtime=0),
    )
    put_json(CASE / "treatment.json", treatment)
    put_json(CASE / "stage_a_trace.json", layer(treatment, "STAGE_A"))
    put_text(CASE / "STAGE_A_REVIEW.md", review(treatment))
    sources = [
        *CASE.glob("*.py"),
        *(ROOT / "experiments/codex_dogfood/acquisition").glob("*.py"),
        *(ROOT / "experiments/retrieval_diagnostics").glob("*.py"),
        ROOT / "experiments/codex_dogfood/case_0009/artifacts.py",
        ROOT / "experiments/codex_dogfood/case_0009/freeze.py",
        ROOT / "experiments/codex_dogfood/case_0009/execute.py",
    ]
    implementation = {
        p.relative_to(ROOT).as_posix(): digest(binary(p)) for p in sources
    }
    implementation.update(
        {
            p: digest(binary(ROOT / p))
            for p in addresses
            if p.startswith("src/") and p.endswith(".py")
        }
    )
    put_json(
        CASE / "pre_execution.json",
        {
            "schema": "case-0011-stage-a-v1",
            "source_head": START,
            "freeze_parent": (await git("rev-parse", "HEAD")).decode().strip(),
            "repository_id": str(snapshot.repository_id),
            "snapshot_id": str(snapshot.id),
            "corpus_id": str(corpus.id),
            "resources": len(docs.documents),
            "obligations": len(task.obligations),
            "information_needs": len(treatment["information_needs"]),
            "queries": len(treatment["queries"]),
            "git_blob_sha256": blobs,
            "implementation_sha256": implementation,
            "python": sys.version,
            "task_sha256": treatment["task_sha256"],
            "query_execution": "NONE",
            "gold": "ABSENT",
        },
    )
    put_json(
        CASE / "integrity.json",
        {
            "schema": "case-0011-stage-a-integrity-v1",
            "scope": "exact gzip; UTF-8 LF text",
            "sha256": {n: digest(binary(CASE / n)) for n in SEALED},
        },
    )
    return verify()


def verify() -> dict[str, Any]:
    """Validate author and all frame/code seals without executing retrieval."""
    treatment, _, _ = definition()
    seal = read_json(CASE / "integrity.json")
    if (
        set(seal["sha256"]) != set(SEALED)
        or read_json(CASE / "treatment.json") != treatment
    ):
        raise ValueError("Stage A coverage or treatment differs")
    for name, expected in seal["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Stage A input hash differs: " + name)
    manifest = read_json(CASE / "pre_execution.json")
    for name, expected in manifest["implementation_sha256"].items():
        if digest(binary(ROOT / name)) != expected:
            raise ValueError("Frozen execution implementation differs: " + name)
    if manifest["python"] != sys.version:
        raise ValueError("Frozen runtime differs")
    return manifest


def load_inputs() -> dict[str, Any]:
    """Read only verified trusted native frame; no historical outcome or gold."""
    m = verify()
    native: dict[str, Any] = pickle.loads(  # noqa: S301 -- hash-verified trusted native frame
        gzip.decompress(binary(CASE / "inputs.pkl.gz"))
    )
    if (
        str(native["snapshot"].repository_id) != m["repository_id"]
        or str(native["snapshot"].id) != m["snapshot_id"]
        or str(native["corpus"].id) != m["corpus_id"]
        or len(native["documents"].documents) != m["resources"]
    ):
        raise ValueError("Native frame differs")
    return native


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "verify"))
    args = parser.parse_args()
    result = asyncio.run(freeze()) if args.operation == "freeze" else verify()
    print(
        {
            k: result[k]
            for k in (
                "resources",
                "obligations",
                "information_needs",
                "queries",
                "snapshot_id",
                "corpus_id",
            )
        }
    )
