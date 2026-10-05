# Copyright (c) 2026
# ruff: noqa: ANN401, C901, COM812, D103, EM101, EM102, E501, PLR2004, T201, TRY003
"""Build or verify the treatment-free Case 0007 blind packet from Stage A."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import hashlib
import json
import pickle
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy

ROOT = Path(__file__).resolve().parents[3]
CASE = Path(__file__).resolve().parent
STAGE_A_COMMIT = "e495c0af2cf57efa3a63016165b41cbba65d26a5"
STAGE_B_COMMIT = "3e22a159e65b59bffab8d83dc5c49519dd8e90b6"
EXPECTED_REPOSITORY = "fe2c8984-a021-4342-9e31-404a6cf07707"
EXPECTED_SNAPSHOT = "404104e498a8d33118b52d5bad41c0ff4a8792d4ae23a2790628b796b91f34fd"
EXPECTED_CORPUS = "a2aaec768f650e9d8928fc1ed1a79eb5650472537b1d3538d740480c6a1b1f87"
EXPECTED_RESOURCES = 521
EXPECTED_ANCHORS = (
    "declarations",
    "bindings",
    "packages",
    "exposure",
    "abstention",
    "provenance",
    "references",
    "api",
    "verification",
)
EXPECTED_OBLIGATIONS = (
    "declaration-identity",
    "binding-reexports",
    "module-membership",
    "explicit-exposure",
    "unsupported-behavior",
    "snapshot-provenance",
    "reference-integration",
    "package-api",
    "tests",
    "documentation",
    "validation",
)
ARCHIVE = "inputs.pkl.gz"
MANIFEST_NAME = "blind_manifest.json"
RESOURCES_NAME = "blind_resources.json.gz"
EXPECTED_TASK = "Implement the first bounded deterministic Python public-export and re-export Repository Intelligence capability for explicit module and package API surfaces. The capability should distinguish source declaration identity, import binding, package membership, and public API exposure; represent direct package-facade re-exports and statically explicit `__all__` declarations where they can be established soundly; preserve native repository/snapshot identity and provenance; retain ambiguity or abstention for dynamic or unsupported export behavior rather than overclaiming; integrate coherently with the existing Python module, declaration, import/member, package, and Reference Repository Intelligence contracts; expose a clean deterministic foundation for future Localization use without introducing a Localization generation operator in this increment; add rigorous tests and authoritative architecture/development documentation; preserve package/API conventions where applicable; and pass protected development validation. Do not implement runtime import execution, dynamic module `__getattr__` resolution, unrestricted star-import closure, inferred popularity or relevance, learned ranking, graph expansion, or automatic witness resolution."
INSTRUCTIONS = (
    "Independently assess the repository evidence against the frozen task and each obligation. "
    "For every obligation, judge applicability and identify information that is REQUIRED, "
    "HELPFUL_ONLY, UNNECESSARY, or unresolved. Record acceptable witness alternatives and "
    "which information must be complementary within each alternative; distinguish competing "
    "alternatives. Assess what could be inferred at task start, inherent discovery prerequisites, "
    "and any task-interpretation gaps. Base judgments on evidence in the supplied snapshot. "
    "Do not infer runtime behavior beyond what the repository establishes."
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _normalized_file(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode(
        "utf-8",
    )


def _git(*arguments: str) -> bytes:
    async def execute() -> bytes:
        executor = CommandExecutor(
            output_policy=CommandOutputPolicy(max_stdout_bytes=32_000_000),
        )
        result = await executor.execute(
            Command("git")
            .args(*arguments)
            .cwd(resolve_path(ROOT))
            .with_timeout(Duration.seconds(30)),
        )
        if result.failed or result.stdout_truncated or result.stderr_truncated:
            raise ValueError(
                "Required bounded Git metadata acquisition did not complete."
            )
        return result.stdout

    return asyncio.run(execute())


def _verify_stage_a() -> tuple[dict[str, Any], dict[str, Any], bytes]:
    head = _git("rev-parse", "HEAD").decode().strip()
    if head != STAGE_B_COMMIT:
        raise ValueError(
            f"Expected captured Stage B commit {STAGE_B_COMMIT}, got {head}."
        )
    committed_integrity = _git(
        "show", f"{STAGE_A_COMMIT}:experiments/codex_dogfood/case_0007/integrity.json"
    )
    current_integrity_bytes = (CASE / "integrity.json").read_bytes()
    if committed_integrity != current_integrity_bytes:
        raise ValueError(
            "Stage A integrity file differs from its committed Stage A version."
        )
    integrity = json.loads(committed_integrity)
    if integrity.get("schema") != "case-0007-stage-a-integrity-v1":
        raise ValueError("Unexpected Stage A integrity schema.")
    for relative, expected in integrity["files"].items():
        if relative not in {
            "README.md",
            "treatment.py",
            "freeze.py",
            "frame.py",
            "test_freeze.py",
            "__init__.py",
            "treatment.json",
            "pre_retrieval.json",
            ARCHIVE,
        }:
            raise ValueError(f"Unexpected Stage A integrity member: {relative}")
        path = CASE / relative
        raw = path.read_bytes()
        if _sha(raw) != expected:
            raise ValueError(f"Stage A integrity mismatch: {relative}")
        committed = _git(
            "show", f"{STAGE_A_COMMIT}:experiments/codex_dogfood/case_0007/{relative}"
        )
        if raw != committed:
            raise ValueError(f"Stage A source differs from frozen commit: {relative}")
    treatment = json.loads((CASE / "treatment.json").read_text(encoding="utf-8"))
    metadata = json.loads((CASE / "pre_retrieval.json").read_text(encoding="utf-8"))
    archive = (CASE / ARCHIVE).read_bytes()
    if _sha(archive) != metadata.get("inputs_archive_sha256"):
        raise ValueError("Stage A native archive digest mismatch.")
    for path, expected in metadata["implementation_sha256"].items():
        if _sha(_normalized_file(ROOT / path)) != expected:
            raise ValueError(f"Frozen implementation identity mismatch: {path}")
    if metadata.get("frame_resource_count") != EXPECTED_RESOURCES:
        raise ValueError("Unexpected frozen frame size.")
    if (
        metadata.get("repository_id") != EXPECTED_REPOSITORY
        or metadata.get("snapshot_id") != EXPECTED_SNAPSHOT
        or metadata.get("corpus_id") != EXPECTED_CORPUS
    ):
        raise ValueError("Frozen repository, snapshot, or corpus identity mismatch.")
    return treatment, metadata, archive


def _provenance(value: Any) -> dict[str, Any]:
    return {
        "source_identity": value.source_identity,
        "span": value.span,
        "explanation": value.explanation,
    }


def _project(
    treatment: dict[str, Any], metadata: dict[str, Any], archive: bytes
) -> tuple[dict[str, Any], bytes]:
    inputs = pickle.loads(gzip.decompress(archive))  # noqa: S301
    request = inputs["lexical_request"]
    task = request.task
    snapshot = request.snapshot
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    if (
        request.full_task_query != EXPECTED_TASK
        or treatment["task"] != EXPECTED_TASK
        or request.purpose != treatment["purpose"]
        or tuple(item.identity.value for item in task.anchors) != EXPECTED_ANCHORS
        or tuple(item.identity.value for item in task.obligations)
        != EXPECTED_OBLIGATIONS
        or len(snapshot.resources) != EXPECTED_RESOURCES
        or snapshot.resources != corpus.resources
        or str(snapshot.repository_id) != EXPECTED_REPOSITORY
        or str(snapshot.id) != EXPECTED_SNAPSHOT
        or str(corpus.id) != EXPECTED_CORPUS
    ):
        raise ValueError(
            "Frozen native task/frame does not match expected Stage A identity."
        )
    anchors = [
        {
            "identity": item.identity.value,
            "text": item.text,
            "provenance": _provenance(item.provenance),
        }
        for item in task.anchors
    ]
    obligations = [
        {
            "identity": item.identity.value,
            "desired_information": item.predicate,
            "anchors": [anchor.value for anchor in item.anchors],
            "provenance": _provenance(item.provenance),
            "requirement": item.requirement.value,
            "applicability": item.applicability_condition,
            "satisfaction_criterion": {
                "name": item.satisfaction.name,
                "statement": item.satisfaction.statement,
            },
            "pre_execution_accepted_witness_alternatives": [],
        }
        for item in task.obligations
    ]
    rows = []
    for resource in snapshot.resources:
        address = resource.address.value
        content = resource.content
        if resource.encoding != "utf-8" or not isinstance(content, str):
            raise ValueError(
                f"Frozen frame resource is not exact UTF-8 text: {address}"
            )
        rows.append(
            {
                "resource_occurrence_identity": (
                    f"{EXPECTED_REPOSITORY}/{EXPECTED_SNAPSHOT}/{address}/"
                    f"{resource.content_identity.value}"
                ),
                "address": address,
                "content_identity": resource.content_identity.value,
                "content": content,
            },
        )
    frozen_identities = [
        {
            "address": row["address"],
            "content_identity": row["content_identity"],
            "byte_size": resource.byte_size,
        }
        for row, resource in zip(rows, snapshot.resources, strict=True)
    ]
    if frozen_identities != metadata["snapshot_resources"]:
        raise ValueError(
            "Frozen resource identities differ from Stage A frame manifest."
        )
    resource_bytes = gzip.compress(_json_bytes(rows), mtime=0)
    manifest = {
        "schema": "case-0007-blind-adjudication-v1",
        "case_identity": "case_0007",
        "task_identity": task.identity.value,
        "task": request.full_task_query,
        "purpose": request.purpose,
        "repository_id": str(snapshot.repository_id),
        "snapshot_id": str(snapshot.id),
        "corpus_id": str(corpus.id),
        "eligible_resource_count": len(rows),
        "shared_anchors": anchors,
        "obligations": obligations,
        "adjudication_instructions": INSTRUCTIONS,
        "resource_archive": {
            "filename": RESOURCES_NAME,
            "sha256": _sha(resource_bytes),
            "format": "gzip-compressed UTF-8 JSON array",
        },
    }
    _validate_manifest(manifest)
    _validate_resources(rows)
    return manifest, resource_bytes


def _validate_manifest(manifest: dict[str, Any]) -> None:
    allowed = {
        "schema",
        "case_identity",
        "task_identity",
        "task",
        "purpose",
        "repository_id",
        "snapshot_id",
        "corpus_id",
        "eligible_resource_count",
        "shared_anchors",
        "obligations",
        "adjudication_instructions",
        "resource_archive",
    }
    if set(manifest) != allowed:
        raise ValueError("Blind manifest fields differ from the explicit allowlist.")
    if manifest["task"] != EXPECTED_TASK or len(manifest["shared_anchors"]) != 9:
        raise ValueError("Blind task or anchor schema mismatch.")
    if (
        len(manifest["obligations"]) != 11
        or manifest["eligible_resource_count"] != EXPECTED_RESOURCES
    ):
        raise ValueError("Blind obligation or frame count mismatch.")
    for anchor in manifest["shared_anchors"]:
        if set(anchor) != {"identity", "text", "provenance"}:
            raise ValueError("Anchor contains a non-allowlisted field.")
        if set(anchor["provenance"]) != {"source_identity", "span", "explanation"}:
            raise ValueError("Anchor provenance contains a non-allowlisted field.")
    for obligation in manifest["obligations"]:
        if (
            set(obligation)
            != {
                "identity",
                "desired_information",
                "anchors",
                "provenance",
                "requirement",
                "applicability",
                "satisfaction_criterion",
                "pre_execution_accepted_witness_alternatives",
            }
            or obligation["pre_execution_accepted_witness_alternatives"]
        ):
            raise ValueError(
                "Obligation contains a non-allowlisted field or witness target."
            )
        if set(obligation["provenance"]) != {
            "source_identity",
            "span",
            "explanation",
        } or set(obligation["satisfaction_criterion"]) != {"name", "statement"}:
            raise ValueError("Nested obligation semantics exceed the allowlist.")
    if set(manifest["resource_archive"]) != {"filename", "sha256", "format"}:
        raise ValueError("Resource archive metadata exceeds the allowlist.")


def _validate_resources(rows: list[dict[str, Any]]) -> None:
    if len(rows) != EXPECTED_RESOURCES:
        raise ValueError("Blind resource count mismatch.")
    allowed = {"resource_occurrence_identity", "address", "content_identity", "content"}
    addresses: set[str] = set()
    for row in rows:
        if set(row) != allowed or row["address"] in addresses:
            raise ValueError("Blind resource fields or address uniqueness mismatch.")
        addresses.add(row["address"])


def _expected() -> tuple[bytes, bytes]:
    treatment, metadata, archive = _verify_stage_a()
    manifest, resources = _project(treatment, metadata, archive)
    return _json_bytes(manifest), resources


def build(output_dir: Path | None = None) -> dict[str, str]:
    """Create packet files exclusively; never overwrite a prior packet."""
    destination = output_dir or CASE / "adjudication"
    manifest_path = destination / MANIFEST_NAME
    resources_path = destination / RESOURCES_NAME
    if destination.exists():
        raise FileExistsError(
            "Blind packet destination already exists; refusing overwrite."
        )
    manifest_bytes, resources_bytes = _expected()
    destination.mkdir(parents=True, exist_ok=False)
    with manifest_path.open("xb") as stream:
        stream.write(manifest_bytes)
    with resources_path.open("xb") as stream:
        stream.write(resources_bytes)
    return verify(destination)


def verify(output_dir: Path | None = None) -> dict[str, str]:
    """Reconstruct expected bytes from Stage A and compare without writing."""
    destination = output_dir or CASE / "adjudication"
    manifest_bytes, resources_bytes = _expected()
    manifest_path = destination / MANIFEST_NAME
    resources_path = destination / RESOURCES_NAME
    actual_manifest = manifest_path.read_bytes()
    actual_resources = resources_path.read_bytes()
    if actual_manifest != manifest_bytes or actual_resources != resources_bytes:
        raise ValueError(
            "Blind packet differs from deterministic Stage A reconstruction."
        )
    parsed = json.loads(actual_manifest)
    _validate_manifest(parsed)
    rows = json.loads(gzip.decompress(actual_resources))
    _validate_resources(rows)
    return {
        MANIFEST_NAME: _sha(actual_manifest),
        RESOURCES_NAME: _sha(actual_resources),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    result = build() if args.mode == "build" else verify()
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
