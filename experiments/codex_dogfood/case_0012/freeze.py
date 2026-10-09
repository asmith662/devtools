# Copyright (c) 2026
# ruff: noqa: COM812, E501, FBT001, T201, EM101, TRY003 -- literal protocol prose; explicit scientific CLI
"""Authenticate and publish prospective U2 Stage A; no exact or lexical execution."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import io
import json
import sys
import tarfile
import unicodedata
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from devtools.context.python.modules.interpretation import (
    PythonModuleInterpretation,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
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
from experiments.codex_dogfood.case_0009.freeze import eligible
from experiments.codex_dogfood.case_0012 import protocol, reporting
from experiments.exact_hint_routing.routing import ExactFrame

CASE = protocol.CASE
EXPERIMENT = ROOT / "experiments/exact_hint_routing"
GENERATED = (
    "inputs.json.gz",
    "resources.json.gz",
    "frame.json",
    "treatment.json",
    "trace.json",
    "TRACE.md",
    "STAGE_A_REVIEW.md",
    "TASK_REQUIREMENT_MATRIX.md",
    "PROTOCOL.md",
    "trace.schema.json",
    "pre_execution.json",
)
AUTHORED = (
    "AUTHORING.md",
    "task.txt",
    "SELECTION.md",
    "STAGE_C_PROTOCOL.md",
    "README.md",
    ".gitattributes",
)
FORBIDDEN = (
    "execution_started.json",
    "results.json",
    "results.json.gz",
    "costs.json",
    "stage_b_integrity.json",
    "STAGE_B_REVIEW.md",
    "adjudication",
)
REPOSITORY = Repository(RepositoryId.parse("5cf96d9e-d6a5-44a6-83d3-1e24f6e00009"))


def require(condition: bool, message: str) -> None:
    """Reject a broken scientific contract without proceeding."""
    if not condition:
        raise ValueError(message)


def implementation_files() -> tuple[Path, ...]:
    """Seal this experiment, case, tests, policy inventory and canonical helper code."""
    return tuple(
        sorted(
            {
                *(
                    CASE / name
                    for name in (
                        "__init__.py",
                        "protocol.py",
                        "reporting.py",
                        "freeze.py",
                        "blind.py",
                        "test_stage_a.py",
                    )
                ),
                *EXPERIMENT.rglob("*.py"),
                EXPERIMENT / "README.md",
                EXPERIMENT / "CAPABILITIES.md",
                EXPERIMENT / "pytest.ini",
                EXPERIMENT / ".gitattributes",
                CASE / "pytest.ini",
                ROOT / "experiments/codex_dogfood/case_0009/artifacts.py",
                ROOT / "experiments/codex_dogfood/case_0009/freeze.py",
            }
        )
    )


async def committed_blobs() -> dict[str, bytes]:
    """Read only broad eligible committed paths; no confirmation/reserve content."""
    tree = (
        (await git("ls-tree", "-r", "--name-only", protocol.START))
        .decode()
        .splitlines()
    )
    addresses = tuple(sorted(p for p in tree if eligible(p)))
    require(
        all(not p.startswith((".local/", "experiments/")) for p in addresses),
        "Operational/experimental resource contamination",
    )
    archive = await git(
        "-c",
        "core.autocrlf=false",
        "archive",
        "--format=tar",
        protocol.START,
        "--",
        *addresses,
    )
    blobs = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                continue
            require(
                member.isfile() and member.name in addresses,
                "Unexpected committed archive entry",
            )
            stream = bundle.extractfile(member)
            if stream is None:
                raise ValueError("Missing archive member bytes")
            blobs[member.name] = stream.read()
    require(tuple(sorted(blobs)) == addresses, "Committed frame coverage differs")
    return blobs


def prepare_frame(blobs: dict[str, bytes]) -> tuple[ExactFrame, dict[str, Any]]:
    """Freeze exact native universes from broad bytes, without hint-directed lookup."""
    with TemporaryDirectory(prefix="case0012-frame-") as temporary:
        root = Path(temporary)
        for address, raw in sorted(blobs.items()):
            put_text(root / address, raw.decode("utf-8"))
        discovery = discover_repository_resource_addresses(
            repository=REPOSITORY,
            root=resolve_path(root),
            maximum_resource_count=10000,
            maximum_traversal_entry_count=20000,
        )
        addresses = tuple(RepositoryResourceAddress(p) for p in sorted(blobs))
        snapshot = observe_repository_resources(
            repository=REPOSITORY,
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
        declarations = tuple(a for a in addresses if a.value.endswith(".py"))
        interpretations: list[PythonModuleInterpretation] = []
        exclusions: list[dict[str, str]] = []
        for root_value, selected in (
            ("src", tuple(a for a in declarations if a.value.startswith("src/"))),
            (".", tuple(a for a in declarations if not a.value.startswith("src/"))),
        ):
            analysis = interpret_python_module_resources(
                snapshot,
                module_root=PythonModuleRoot(root_value),
                resource_addresses=selected,
            )
            interpretations.extend(analysis.interpretations)
            exclusions.extend(
                {
                    "address": str(e.resource.address),
                    "root": root_value,
                    "reason": e.reason.value,
                }
                for e in analysis.exclusions
            )
        modules = define_python_module_interpretation_universe(
            repository_id=REPOSITORY.id, interpretations=interpretations
        )
        frame = ExactFrame(REPOSITORY.id, snapshot.id, snapshot, modules, declarations)
        frame.validate()
        metadata = {
            "repository_id": str(REPOSITORY.id),
            "snapshot_id": str(snapshot.id),
            "corpus_id": str(corpus.id),
            "frame_identity": frame.identity,
            "source_head": protocol.START,
            "resource_count": len(snapshot.resources),
            "resource_order": "canonical address ascending",
            "eligible_resource_frame": [
                {
                    "address": str(r.address),
                    "content_identity": str(r.content_identity),
                    "utf8_bytes": r.byte_size,
                    "document_identity": str(d.id),
                }
                for r, d in zip(snapshot.resources, documents.documents, strict=True)
            ],
            "module_universe_identity": modules.identity,
            "module_count": len(modules.interpretations),
            "module_universe": [
                {
                    "identity": m.identity,
                    "root": m.module_root.value,
                    "dotted_name": m.dotted_name,
                    "kind": m.kind.value,
                    "address": str(m.resource.address),
                    "content_identity": str(m.resource.content_identity),
                }
                for m in modules.interpretations
            ],
            "module_exclusions": exclusions,
            "declaration_resource_universe": [str(a) for a in declarations],
            "declaration_analysis": "NOT_EXECUTED; explicit full Python resource universe only",
            "resource_universe": "entire eligible committed frame, query-independent",
            "scope": "No task-directed exact lookup, native declaration selection or retrieval; module interpretation is address-only preparation",
        }
    return frame, metadata


def frame_resources(frame: ExactFrame) -> list[dict[str, Any]]:
    """Serialize retained whole-resource contents for later authorized observation."""
    return [
        {
            "address": str(r.address),
            "content_identity": str(r.content_identity),
            "text": r.content,
            "encoding": r.encoding,
            "byte_size": r.byte_size,
        }
        for r in frame.snapshot.resources
    ]


def restore_frame(image: dict[str, Any]) -> ExactFrame:
    """Reconstruct native values from canonical JSON; no parse/lookup outcomes."""
    metadata = image["metadata"]
    repository_id = RepositoryId.parse(metadata["repository_id"])
    snapshot_id = RepositorySnapshotId(metadata["snapshot_id"])
    resources = tuple(
        RepositoryResourceOccurrence(
            RepositoryResourceAddress(r["address"]),
            ContentIdentity(r["content_identity"]),
            r["text"],
            r["encoding"],
            r["byte_size"],
        )
        for r in image["resources"]
    )
    snapshot = RepositorySnapshot(snapshot_id, repository_id, resources)
    modules: list[PythonModuleInterpretation] = []
    for root in dict.fromkeys(m["root"] for m in metadata["module_universe"]):
        addresses = tuple(
            RepositoryResourceAddress(m["address"])
            for m in metadata["module_universe"]
            if m["root"] == root
        )
        modules.extend(
            interpret_python_module_resources(
                snapshot,
                module_root=PythonModuleRoot(root),
                resource_addresses=addresses,
            ).interpretations
        )
    universe = define_python_module_interpretation_universe(
        repository_id=repository_id, interpretations=modules
    )
    frame = ExactFrame(
        repository_id,
        snapshot_id,
        snapshot,
        universe,
        tuple(
            RepositoryResourceAddress(a)
            for a in metadata["declaration_resource_universe"]
        ),
    )
    frame.validate()
    require(
        frame.identity == metadata["frame_identity"], "Restored frame identity differs"
    )
    require(
        [m.identity for m in modules]
        == [m["identity"] for m in metadata["module_universe"]],
        "Restored native module identities differ",
    )
    return frame


def protocol_text(treatment: dict[str, Any]) -> str:
    """Register every prospective question and attribution before outcomes exist."""
    questions = [
        "Caller explicit hint count; rule hint count; accepted/false rule hints; caller-only hints; type disagreement, with task-reference denominators.",
        "Supported/unsupported/ambiguous/unresolved/resolved requests and hints, with shared-hint/lane duplication retained.",
        "After blind gold: REQUIRED/HELPFUL_ONLY/UNNECESSARY exact targets; extraction miss/false/type and native scope classifications.",
        "Every required exact target native lane rank, routed position, saved depth, remaining witness members and shifted bottleneck.",
        "Every obligation and complete alternative depth, prefix occurrences/unique union/duplicates, owning labels, unnecessary burden and UTF-8 bytes.",
        "Does C reproduce B caller route value? Named-target gain versus complete obligation gain; semantic requirements without exact hints remain lexical.",
        "Exact extraction/resolution/presentation costs, shared build cost, query counts, total time; actual evidence-inspection cost NOT MEASURED.",
        "Non-improvements distinguish non-bottleneck/unnecessary targets, wrong association, no hint, fallback discrimination and task-interpretation failure.",
    ]
    lines = [
        "# Case 0012 prospective U2 protocol",
        "",
        "Hypothesis: conservative explicit native hints can route exact-first while unchanged lexical safety retains non-hint evidence. Test depth/burden for hint-supported REQUIRED evidence without inventing relevance. This does not repair U1 missing/incomplete InformationNeeds.",
        "",
        "A = LEXICAL_ONLY; B = CALLER_HINT_EXACT_FIRST; C = RULE_EXTRACTED_EXACT_FIRST. Identical task/obligations/query strings/frame and canonical BM25 settings; only hint inventory and exact-first presentation differ.",
        "",
        "## Primary questions and metrics",
        "",
    ]
    lines += [f"{n}. {q}" for n, q in enumerate(questions, 1)]
    lines += ["", "## Frozen decision rule", ""]
    for key, value in treatment["decision_rule"].items():
        lines += [
            "### " + key,
            "",
            value if isinstance(value, str) else json.dumps(value, indent=2),
            "",
        ]
    lines += [
        "## Attribution records",
        "",
        "For every hint record EXTRACTION_MISS, FALSE_EXTRACTION, TYPE_MISCLASSIFICATION, UNSUPPORTED, AMBIGUOUS, UNRESOLVED or RESOLVED_REQUIRED/HELPFUL/UNNECESSARY after independent gold. For every required unit/resource record earliest failed stage, semantic evidence, mechanical evidence, contributing factors and proposed correction. Native scoped failure is not automatically a router defect. SEARCH_POLICY_FAILURE = NOT_ASSESSED.",
        "",
        "## Freeze and blindness",
        "",
        "Stage A stops before exact resolution and lexical execution. Maintainer review is treatment-aware task-interpretation review, not blind gold. Stage C receives only task/obligations/eligible contents under STAGE_C_PROTOCOL.md; no packet or gold now. No U3, R1.7, BM25F or semantic-resolution experiment is executed.",
        "",
    ]
    return "\n".join(lines).rstrip("\n") + "\n"


def shape(value: Any) -> dict[str, Any]:  # noqa: ANN401 -- case-local JSON schema boundary
    """Freeze the complete nested Stage A projection shape, not a generic codec."""
    if isinstance(value, dict):
        return {
            "type": "object",
            "additionalProperties": False,
            "required": sorted(value),
            "properties": {k: shape(v) for k, v in sorted(value.items())},
        }
    if isinstance(value, list):
        if not value:
            return {"type": "array", "maxItems": 0}
        variants = {json_bytes(shape(v)).decode(): shape(v) for v in value}
        return {
            "type": "array",
            "items": {"anyOf": [variants[k] for k in sorted(variants)]},
        }
    kind = (
        "null"
        if value is None
        else "boolean"
        if isinstance(value, bool)
        else "integer"
        if isinstance(value, int)
        else "number"
        if isinstance(value, float)
        else "string"
    )
    return {"type": kind}


def artifacts(
    frame: ExactFrame, metadata: dict[str, Any], blobs: dict[str, bytes]
) -> dict[str, bytes]:
    """Build deterministic review/trace/input seals with zero outcome slots populated."""
    treatment = protocol.definition()
    trace = {
        "schema": "case-0012-stage-a-trace-v1",
        "stage": "STAGE_A",
        "treatment": treatment,
        "frame": metadata,
        "execution": {"exact_routes": 0, "lexical_queries": 0, "treatments": 0},
        "results": "ABSENT",
        "effectiveness": "UNKNOWN",
    }
    review = reporting.review(treatment, metadata)
    source_hashes = {
        p.relative_to(ROOT).as_posix(): digest(binary(p))
        for p in implementation_files()
    }
    source_hashes.update(
        {
            p: digest(raw)
            for p, raw in blobs.items()
            if p.startswith("src/") and p.endswith(".py")
        }
    )
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "case-0012-stage-a-trace-v1",
        "type": "object",
        "additionalProperties": False,
        "required": list(trace),
        "properties": {
            "schema": {"const": trace["schema"]},
            "stage": {"const": "STAGE_A"},
            "treatment": shape(treatment),
            "frame": shape(metadata),
            "execution": {"const": trace["execution"]},
            "results": {"const": "ABSENT"},
            "effectiveness": {"const": "UNKNOWN"},
        },
    }
    return {
        "inputs.json.gz": gzip.compress(
            json_bytes({"metadata": metadata, "resources": frame_resources(frame)}),
            mtime=0,
        ),
        "resources.json.gz": gzip.compress(
            json_bytes({"resources": frame_resources(frame)}), mtime=0
        ),
        "frame.json": json_bytes(metadata),
        "treatment.json": json_bytes(treatment),
        "trace.json": json_bytes(trace),
        "TRACE.md": review.encode(),
        "STAGE_A_REVIEW.md": review.encode(),
        "TASK_REQUIREMENT_MATRIX.md": reporting.matrix(treatment).encode(),
        "PROTOCOL.md": protocol_text(treatment).encode(),
        "trace.schema.json": json_bytes(schema),
        "pre_execution.json": json_bytes(
            {
                "schema": "case-0012-stage-a-pre-execution-v1",
                "source_head": protocol.START,
                "git_blob_sha256": {p: digest(raw) for p, raw in blobs.items()},
                "implementation_sha256": source_hashes,
                "frame_identity": frame.identity,
                "task_sha256": treatment["task_sha256"],
                "exact_route_executions": 0,
                "lexical_query_executions": 0,
                "stage_b": "NOT_EXECUTED",
                "gold": "ABSENT",
                "effectiveness": "UNKNOWN",
                "python_runtime": sys.version,
                "unicode_version": unicodedata.unidata_version,
            }
        ),
    }


def publish(output: dict[str, bytes], root: Path = CASE) -> None:
    """Refuse partial or complete destination overwrite before any publication."""
    require(
        not any(
            (root / name).exists()
            for name in (*GENERATED, "integrity.json", *FORBIDDEN)
        ),
        "Stage A overwrite/execution refused",
    )
    for name, raw in output.items():
        if name.endswith(".gz"):
            put_binary(root / name, raw)
        else:
            put_text(root / name, raw.decode("utf-8"))
    sealed = {name: digest(raw) for name, raw in output.items()}
    sealed.update({name: digest(binary(CASE / name)) for name in AUTHORED})
    put_text(
        root / "integrity.json",
        json_bytes(
            {
                "schema": "case-0012-stage-a-integrity-v1",
                "sha256": sealed,
                "scope": "Exact gzip; canonical UTF-8 LF; operational handoff/backup excluded",
            }
        ).decode(),
    )


async def verify(root: Path = CASE) -> dict[str, Any]:
    """Authenticate and reconstruct all Stage A artifacts without treatment execution."""
    require(
        not any((root / name).exists() for name in FORBIDDEN),
        "Unexpected Stage B/gold artifact",
    )
    seal = read_json(root / "integrity.json")
    require(
        set(seal["sha256"]) == {*GENERATED, *AUTHORED},
        "Stage A seal coverage differs",
    )
    require(
        all(
            digest(binary(root / name)) == expected
            for name, expected in seal["sha256"].items()
        ),
        "Stage A artifact hash differs",
    )
    blobs = await committed_blobs()
    image = json.loads(gzip.decompress(binary(root / "inputs.json.gz")))
    frame = restore_frame(image)
    frame.validate()
    metadata = read_json(root / "frame.json")
    rebuilt = artifacts(frame, metadata, blobs)
    differences = [name for name, raw in rebuilt.items() if binary(root / name) != raw]
    require(
        not differences,
        "Deterministic Stage A replay differs: " + ", ".join(differences),
    )
    prepared, expected_metadata = prepare_frame(blobs)
    require(
        prepared == frame and expected_metadata == metadata,
        "Native frame differs from committed bytes/universes",
    )
    require(
        artifacts(prepared, expected_metadata, blobs) == rebuilt,
        "Native input/protocol reconstruction differs",
    )
    await git("merge-base", "--is-ancestor", protocol.START, "HEAD")
    return {
        "stage_a": "FROZEN",
        "resources": len(frame.snapshot.resources),
        "hints": len(protocol.CALLER_HINTS),
        "obligations": len(protocol.OBLIGATIONS),
        "exact_route_executions": 0,
        "lexical_query_executions": 0,
        "stage_b": "NOT_EXECUTED",
        "effectiveness": "UNKNOWN",
        "replay": "PASSED",
    }


async def build() -> dict[str, Any]:
    """Freeze once only on the expected main parent; never execute hints/queries."""
    require(
        not any(
            (CASE / name).exists()
            for name in (*GENERATED, "integrity.json", *FORBIDDEN)
        ),
        "Stage A overwrite/execution refused",
    )
    require(
        (await git("rev-parse", "HEAD")).decode().strip() == protocol.START,
        "Unexpected freeze parent",
    )
    require(
        (await git("branch", "--show-current")).decode().strip() == "main",
        "Expected main branch",
    )
    require(
        not await git(
            "diff",
            protocol.START,
            "--name-only",
            "--",
            "src",
            "pyproject.toml",
            "uv.lock",
        ),
        "Production implementation changed",
    )
    # Task-only authoring precedes all broad native frame observation.
    protocol.definition()
    blobs = await committed_blobs()
    frame, metadata = prepare_frame(blobs)
    output = artifacts(frame, metadata, blobs)
    require(output == artifacts(frame, metadata, blobs), "Nondeterministic artifacts")
    publish(output)
    return await verify()


def main() -> None:
    """Provide only build/verify; Stage B requires another authorization/checkpoint."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    args = parser.parse_args()
    print(asyncio.run(build() if args.operation == "build" else verify()))


if __name__ == "__main__":
    main()
