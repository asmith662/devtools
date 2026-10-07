# Copyright (c) 2026
# ruff: noqa: E501, EM101, TRY003, T201 -- bounded prospective freeze
"""Freeze starting Git bytes and parameter arms before any prospective query."""

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
from experiments.bm25_sensitivity.protocol import BASELINE, START
from experiments.bm25_sensitivity.storage import HERE, get
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
from experiments.codex_dogfood.case_0010.protocol import OBLIGATIONS, TASK, task_inputs

CASE = Path(__file__).resolve().parent
STAGE_A = ("treatment.json", "inputs.pkl.gz", "pre_execution.json")


async def freeze() -> dict[str, Any]:
    """Observe a broad source export without indexing or analyzing any query."""
    ensure_absent(
        CASE,
        (*STAGE_A, "integrity.json", "execution_started.json", "adjudication"),
    )
    if await git(
        "diff",
        START,
        "--name-only",
        "--",
        "src",
        "pyproject.toml",
        "uv.lock",
    ):
        raise ValueError("Production implementation differs from source snapshot.")
    development_commit = (
        (
            await git(
                "log",
                "-1",
                "--format=%H",
                "--",
                "experiments/bm25_sensitivity/development.json.gz",
            )
        )
        .decode()
        .strip()
    )
    await git("merge-base", "--is-ancestor", development_commit, "HEAD")
    development = get(HERE / "development.json.gz")
    if digest(
        await git(
            "show",
            development_commit + ":experiments/bm25_sensitivity/development.json.gz",
        ),
    ) != digest(binary(HERE / "development.json.gz")):
        raise ValueError("Development selection is not committed unchanged.")
    tree = (await git("ls-tree", "-r", "--name-only", START)).decode().splitlines()
    addresses = tuple(sorted(p for p in tree if eligible(p)))
    if any("case_0010" in p for p in tree):
        raise ValueError("Prospective case already existed at source snapshot.")
    archive = await git("archive", "--format=tar", START, "--", *addresses)
    selected = tuple(RepositoryResourceAddress(p) for p in addresses)
    blobs = {}
    with TemporaryDirectory(prefix="case0010-source-") as temporary:
        exported = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            for member in bundle.getmembers():
                if member.isdir():
                    continue
                if not member.isfile() or member.name not in addresses:
                    raise ValueError("Unexpected/nonregular archive member.")
                stream = bundle.extractfile(member)
                if stream is None:
                    raise ValueError("Missing archive content.")
                content = stream.read()
                blobs[member.name] = digest(content)
                put_text(exported / member.name, content.decode("utf-8"))
        if set(blobs) != set(addresses):
            raise ValueError("Selected source coverage differs.")
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
                discovery=discovery,
                selected_addresses=selected,
            ),
            snapshot=snapshot,
        )
        documents = represent_repository_text_corpus(corpus=corpus)
    task, queries = task_inputs()
    parameters = [list(BASELINE), *development["selection"]["unique_challengers"]]
    treatment = {
        "schema": "case-0010-parameter-treatment-v1",
        "task": TASK,
        "selection_rationale": "Documented planning supports whole resources and qualified Python references; explicit bounded text ranges are a realistic missing caller choice. Selected from package contracts after development freeze, without prospective gold or ranks; task is not implemented.",
        "development_commit": development_commit,
        "development_sha256": digest(binary(HERE / "development.json.gz")),
        "selected_roles": development["selection"]["roles"],
        "arms": [
            {
                "arm": chr(65 + i),
                "parameters": p,
                "analyzer": "canonical",
                "architecture": "independent content BM25 + filename_weight * independent filename-stem BM25",
            }
            for i, p in enumerate(parameters)
        ],
        "task_identity": task.identity.value,
        "obligations": [
            {
                "identity": ob.identity.value,
                "predicate": predicate,
                "query_identity": q.identity.value,
                "query": text,
            }
            for ob, q, (_, predicate, text) in zip(
                task.obligations,
                queries,
                OBLIGATIONS,
                strict=True,
            )
        ],
        "full_task_query": TASK,
        "decision_rule": "No required resource/cell/unit loss; global/max-own <=1.05 baseline; >=10% union OR max-own improvement; each own depth <=1.25 baseline; >=half obligations nonworse; median/p95 query scoring <=3x; development worst max-own/union <=1.25. Candidate is later adoption consideration only. BASELINE_ROBUST if all challengers reach-safe and all global/max-own/union ratios within [0.95,1.05] without meaningful improvement; otherwise MIXED / NO SAFE REPLACEMENT. Concrete scorer defect stops.",
        "metrics": [
            "required resource/cell/unit reach",
            "best all-member accepted-alternative global/own completion",
            "maximum own completion",
            "prefix occurrences/union/excess/composition",
            "top5/10/20",
            "R1.5 mechanics",
            "cost",
        ],
        "blind_protocol": "Fresh independent sterile full-frame obligation gold; no treatment, query lanes, arms, parameters, rankings, scores or costs. Explicit compressed/archive and canonical-payload scopes. Stage C is not performed in this increment.",
        "execution": "Every arm/query exactly once using shared canonical indexes; actual score timing excludes diagnostics; no second scoring execution for replay.",
        "tie_order": "descending positive score, stable frozen corpus order",
        "eligibility": "Case 0009 broad policy over starting R1.5 Git snapshot; excludes experiments, research/reports, confirmation/reserve, ledger; no current content substitution",
    }
    put_json(CASE / "treatment.json", treatment)
    put_binary(
        CASE / "inputs.pkl.gz",
        gzip.compress(
            pickle.dumps(
                {
                    "snapshot": snapshot,
                    "corpus": corpus,
                    "documents": documents,
                    "task": task,
                    "queries": queries,
                },
                protocol=pickle.HIGHEST_PROTOCOL,
            ),
            mtime=0,
        ),
    )
    sources = {
        p.relative_to(ROOT).as_posix(): digest(binary(p))
        for p in sorted(
            (
                *CASE.glob("*.py"),
                HERE / "scoring.py",
                *(ROOT / "experiments/retrieval_diagnostics").glob("*.py"),
            ),
        )
    }
    sources.update(
        {
            p: digest(binary(ROOT / p))
            for p in addresses
            if p.startswith("src/") and p.endswith(".py")
        },
    )
    manifest = {
        "schema": "case-0010-stage-a-v1",
        "source_head": START,
        "freeze_parent": (await git("rev-parse", "HEAD")).decode().strip(),
        "repository_id": str(snapshot.repository_id),
        "snapshot_id": str(snapshot.id),
        "corpus_id": str(corpus.id),
        "resources": len(documents.documents),
        "obligations": len(queries),
        "task_sha256": digest(TASK.encode()),
        "git_blob_sha256": blobs,
        "implementation_sha256": sources,
        "python": sys.version,
        "lock_sha256": digest(await git("show", START + ":uv.lock")),
        "query_execution": "NONE",
        "gold": "ABSENT",
        "stage_b": "ABSENT",
    }
    put_json(CASE / "pre_execution.json", manifest)
    put_json(
        CASE / "integrity.json",
        {
            "schema": "case-0010-stage-a-integrity-v1",
            "scope": "Exact gzip bytes and canonical UTF-8 LF text bytes",
            "sha256": {n: digest(binary(CASE / n)) for n in STAGE_A},
        },
    )
    return verify()


def verify() -> dict[str, Any]:
    """Require frozen hashes before trusted native input deserialization."""
    seal = read_json(CASE / "integrity.json")
    if set(seal["sha256"]) != set(STAGE_A):
        raise ValueError("Stage A coverage differs.")
    for name, expected in seal["sha256"].items():
        if digest(binary(CASE / name)) != expected:
            raise ValueError("Frozen Stage A changed.")
    manifest = read_json(CASE / "pre_execution.json")
    for name, expected in manifest["implementation_sha256"].items():
        if digest(binary(ROOT / name)) != expected:
            raise ValueError("Frozen execution/diagnostics implementation changed.")
    if (
        manifest["task_sha256"] != digest(TASK.encode())
        or manifest["python"] != sys.version
    ):
        raise ValueError("Frozen task/runtime differs.")
    return manifest


def load_inputs() -> dict[str, Any]:
    """Deserialize only our hash-verified trusted frame, without any gold."""
    manifest = verify()
    native: dict[str, Any] = pickle.loads(  # noqa: S301 -- hash-verified trusted case frame
        gzip.decompress(binary(CASE / "inputs.pkl.gz")),
    )
    if (
        str(native["snapshot"].id) != manifest["snapshot_id"]
        or str(native["corpus"].id) != manifest["corpus_id"]
        or len(native["documents"].documents) != manifest["resources"]
    ):
        raise ValueError("Native frame differs.")
    return native


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("freeze", "verify"))
    args = parser.parse_args()
    print(asyncio.run(freeze()) if args.operation == "freeze" else verify())
