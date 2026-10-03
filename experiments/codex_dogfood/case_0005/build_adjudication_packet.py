# Copyright (c) 2026
# ruff: noqa: ANN001, C901, COM812, EM101, EM102, INP001, PLR0912, PLR2004, T201, TRY003
"""Build and verify a treatment-free Case 0005 Stage C packet."""

from __future__ import annotations

import asyncio
import gzip
import hashlib
import json
import pickle
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.context.localization.identity import TaskTextSpan
from devtools.context.localization.obligation import RequirementStatus
from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import FileFormat, TextFile, read, write

if TYPE_CHECKING:
    from devtools.context.localization.task import LocalizationTaskInterpretation

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[2]
PACKET = CASE / "adjudication"
MANIFEST = PACKET / "blind_manifest.json"
ARCHIVE = PACKET / "blind_resources.json.gz"
CASE_RECORD = CASE / "stage_b5.md"
STAGE_A = "e9764cde6dc6c2f379e4b08561974cd6b59c30d3"
STAGE_B = "c233625dc2d0714ffda2b0b88df8cd73e22ea144"
CASE_RELATIVE = "experiments/codex_dogfood/case_0005"
EXPECTED_INTEGRITY_NAMES = {
    "treatment.json",
    "pre_retrieval.json",
    "inputs.pkl.gz",
    "freeze.py",
    "README.md",
    "test_freeze.py",
}

MANIFEST_KEYS = {
    "schema",
    "case",
    "task_identity",
    "task_text",
    "purpose",
    "repository_id",
    "snapshot_id",
    "eligible_frame_identity",
    "eligible_resource_count",
    "anchors",
    "obligations",
    "adjudication_semantics",
    "resource_archive",
}
ANCHOR_KEYS = {"identity", "text", "provenance"}
OBLIGATION_KEYS = {
    "identity",
    "predicate",
    "anchor_references",
    "provenance",
    "requirement_status",
    "applicability_condition",
    "satisfaction_criterion",
    "witness_alternatives",
}
PROVENANCE_KEYS = {"source_identity", "span", "explanation"}
SPAN_KEYS = {"start", "end"}
CRITERION_KEYS = {"name", "statement"}
ARCHIVE_REFERENCE_KEYS = {"filename", "sha256"}
ADJUDICATION_KEYS = {
    "applicability",
    "information_judgments",
    "witness_algebra",
    "required_scope",
    "inferability",
    "inherent_discovery_record",
    "interpretation_gaps",
    "coverage",
    "independence",
}
RESOURCE_KEYS = {
    "repository_id",
    "snapshot_id",
    "resource_identity",
    "address",
    "content_identity",
    "content",
}
RESOURCE_IDENTITY_KEYS = {
    "repository_id",
    "snapshot_id",
    "address",
    "content_identity",
}


def sha(content: bytes) -> str:
    """Return lowercase SHA-256 of exact artifact bytes."""
    return hashlib.sha256(content).hexdigest()


def canonical_text(data: bytes) -> bytes:
    """Normalize Git/Windows text checkout line endings for source checks."""
    return data.replace(b"\r\n", b"\n")


def read_bytes(path: Path, limit: int = 64 << 20) -> bytes:
    """Read one explicitly named packet/input artifact under a local bound."""
    if path.suffix == ".gz":
        with path.open("rb") as stream:
            data = stream.read(limit + 1)
        if len(data) > limit:
            raise ValueError("Compressed archive exceeds the explicit size bound.")
        return data
    result = read(resolve_path(path), file_format=FileFormat.TEXT, max_bytes=limit)
    if not isinstance(result, TextFile):
        raise TypeError("Expected one bounded textual artifact.")
    return result.content.encode("utf-8")


def json_bytes(value: object) -> bytes:
    """Serialize deterministic human-readable allowlisted JSON."""
    return (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode("utf-8")


async def git(*arguments: str) -> bytes:
    """Read exact committed evidence through the managed command boundary."""
    result = await CommandExecutor(
        output_policy=CommandOutputPolicy(max_stdout_bytes=32 << 20),
    ).execute(Command("git").args(*arguments).cwd(resolve_path(ROOT)))
    if result.failed or result.stdout_truncated:
        raise ValueError("Stage A committed input could not be verified completely.")
    return result.stdout


def _provenance(value) -> dict:
    """Project native caller provenance without importing other task fields."""
    span = None
    if value.span is not None:
        if not isinstance(value.span, TaskTextSpan):
            raise TypeError("Frozen task provenance has an unsupported span.")
        span = {"start": value.span.start, "end": value.span.end}
    if value.explanation is not None and not value.explanation.strip():
        raise ValueError("Frozen task provenance has an empty explanation.")
    return {
        "source_identity": value.source_identity,
        "span": span,
        "explanation": value.explanation,
    }


def _task_projection(task: LocalizationTaskInterpretation) -> tuple[list, list]:
    """Return only the explicitly allowed anchor and obligation contracts."""
    anchors = [
        {
            "identity": item.identity.value,
            "text": item.text,
            "provenance": _provenance(item.provenance)
            if item.provenance is not None
            else None,
        }
        for item in task.anchors
    ]
    obligations = []
    for item in task.obligations:
        if not isinstance(item.requirement, RequirementStatus):
            raise TypeError("Frozen obligation status is unsupported.")
        obligations.append(
            {
                "identity": item.identity.value,
                "predicate": item.predicate,
                "anchor_references": [anchor.value for anchor in item.anchors],
                "provenance": _provenance(item.provenance),
                "requirement_status": item.requirement.value,
                "applicability_condition": item.applicability_condition,
                "satisfaction_criterion": {
                    "name": item.satisfaction.name,
                    "statement": item.satisfaction.statement,
                },
                "witness_alternatives": [
                    list(alternative.members)
                    for alternative in item.witness_alternatives
                ],
            },
        )
    return anchors, obligations


def _resources(snapshot, protocol: dict) -> list[dict]:
    """Project all and only snapshot resource identity, address and text."""
    native = snapshot.resources
    frozen = protocol["eligible_resources"]
    if len(native) != 515 or len(frozen) != 515:
        raise ValueError("Frozen eligible resource count is not 515.")
    projected = []
    seen = set()
    for item, expected in zip(native, frozen, strict=True):
        address = item.address.value
        identity = item.content_identity.value
        if (
            address != expected["address"]
            or identity != expected["content_identity"]
            or sha(item.content.encode("utf-8")) != expected["git_blob_sha256"]
            or address in seen
        ):
            raise ValueError(
                "Snapshot address/content differs from frozen Stage A frame."
            )
        seen.add(address)
        projected.append(
            {
                "repository_id": str(snapshot.repository_id),
                "snapshot_id": str(snapshot.id),
                "resource_identity": {
                    "repository_id": str(snapshot.repository_id),
                    "snapshot_id": str(snapshot.id),
                    "address": address,
                    "content_identity": identity,
                },
                "address": address,
                "content_identity": identity,
                "content": item.content,
            },
        )
    if len(seen) != 515:
        raise ValueError("Eligible resource identities are incomplete.")
    return projected


def _assert_task_correspondence(protocol: dict, request) -> None:
    """Refuse malformed or drifted frozen task fields; never repair them."""
    task = request.task
    if (
        protocol["case"] != "case_0005"
        or protocol["status"] != "FROZEN BEFORE RETRIEVAL AND ROUTING"
        or protocol["starting_head"] != "1bd2c7a5676ba78edd46879f2c06625c13c12d17"
        or request.full_task_query != protocol["task_full_prompt"]
        or request.purpose != protocol["purpose"]
        or task.identity.value != protocol["task_identity"]
        or str(request.snapshot.repository_id) != protocol["repository_id"]
        or str(request.snapshot.id) != protocol["snapshot_id"]
        or len(task.anchors) != 6
        or len(task.obligations) != 9
        or len(request.snapshot.resources) != 515
    ):
        raise ValueError("Stage A task/snapshot identity differs from its manifest.")
    manifest_anchors = protocol["anchors"]
    if len(manifest_anchors) != len(task.anchors):
        raise ValueError("Frozen anchor coverage differs.")
    for native, frozen in zip(task.anchors, manifest_anchors, strict=True):
        if native.identity.value != frozen["identity"] or native.text != frozen["text"]:
            raise ValueError("Frozen anchor identity/text differs.")
    manifest_obligations = protocol["obligations"]
    if len(manifest_obligations) != len(task.obligations):
        raise ValueError("Frozen obligation coverage differs.")
    for native, frozen in zip(task.obligations, manifest_obligations, strict=True):
        if (
            native.identity.value != frozen["identity"]
            or native.predicate != frozen["predicate"]
            or [item.value for item in native.anchors] != frozen["anchors"]
            or native.requirement.value != frozen["requirement"]
            or native.applicability_condition != frozen["applicability_condition"]
            or native.satisfaction.name != frozen["satisfaction"]["name"]
            or native.satisfaction.statement != frozen["satisfaction"]["statement"]
            or len(native.witness_alternatives) != len(frozen["witness_alternatives"])
        ):
            raise ValueError("Frozen obligation semantic fields differ.")
    if any(item.witness_alternatives for item in task.obligations):
        raise ValueError("Stage A unexpectedly froze witness targets.")


def _manifest(
    protocol: dict, request, archive_sha: str, anchors: list, obligations: list
) -> dict:
    """Construct a strict allowlist; never copy a treatment manifest."""
    return {
        "schema": "codex-case-0005-blind-adjudication-v1",
        "case": "case_0005",
        "task_identity": request.task.identity.value,
        "task_text": request.full_task_query,
        "purpose": request.purpose,
        "repository_id": str(request.snapshot.repository_id),
        "snapshot_id": str(request.snapshot.id),
        "eligible_frame_identity": protocol["eligible_corpus_id"],
        "eligible_resource_count": 515,
        "anchors": anchors,
        "obligations": obligations,
        "adjudication_semantics": {
            "applicability": [
                "APPLICABLE",
                "SUPPORTED_NOT_APPLICABLE",
                "UNRESOLVED_APPLICABILITY",
            ],
            "information_judgments": [
                "REQUIRED",
                "HELPFUL_ONLY",
                "UNNECESSARY",
                "UNRESOLVED",
            ],
            "witness_algebra": (
                "All members of one complete witness alternative are conjunctive; "
                "any one complete acceptable alternative can satisfy its obligation."
            ),
            "required_scope": (
                "Mark information REQUIRED only when correctness could not "
                "reasonably be achieved without it. Keep finer defensible units "
                "distinct from whole-resource identity."
            ),
            "inferability": ["INFERABLE_AT_START", "INHERENT_DISCOVERY"],
            "inherent_discovery_record": [
                "exact later observation",
                "prerequisite",
                "why it could not reasonably be inferred at task start",
            ],
            "interpretation_gaps": (
                "Record obvious omitted mandatory task requirements separately; "
                "do not change the frozen obligation frame."
            ),
            "coverage": (
                "Account deterministically for every eligible resource identity; "
                "use UNRESOLVED where packet evidence is insufficient."
            ),
            "independence": (
                "Judge repository information needs from the frozen task, "
                "obligations and snapshot contents. Do not use files merely "
                "because they were later opened or modified."
            ),
        },
        "resource_archive": {
            "filename": ARCHIVE.name,
            "sha256": archive_sha,
        },
    }


def validate_schema(manifest: dict, resources: list[dict]) -> None:
    """Reject any field outside the explicit task-only packet allowlist."""
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("Blind manifest keys differ from its allowlist.")
    if set(manifest["resource_archive"]) != ARCHIVE_REFERENCE_KEYS:
        raise ValueError("Blind archive reference keys differ from its allowlist.")
    if set(manifest["adjudication_semantics"]) != ADJUDICATION_KEYS:
        raise ValueError(
            "Blind adjudication-instruction keys differ from its allowlist."
        )
    if not all(set(item) == ANCHOR_KEYS for item in manifest["anchors"]):
        raise ValueError("Blind anchor keys differ from its allowlist.")
    for item in manifest["anchors"]:
        if (
            item["provenance"] is not None
            and set(item["provenance"]) != PROVENANCE_KEYS
        ):
            raise ValueError("Blind anchor provenance keys differ from its allowlist.")
        if (
            item["provenance"]
            and item["provenance"]["span"] is not None
            and set(item["provenance"]["span"]) != SPAN_KEYS
        ):
            raise ValueError("Blind provenance span keys differ from its allowlist.")
    if not all(set(item) == OBLIGATION_KEYS for item in manifest["obligations"]):
        raise ValueError("Blind obligation keys differ from its allowlist.")
    for item in manifest["obligations"]:
        if set(item["provenance"]) != PROVENANCE_KEYS:
            raise ValueError(
                "Blind obligation provenance keys differ from its allowlist."
            )
        if (
            item["provenance"]["span"] is not None
            and set(item["provenance"]["span"]) != SPAN_KEYS
        ):
            raise ValueError("Blind provenance span keys differ from its allowlist.")
        if set(item["satisfaction_criterion"]) != CRITERION_KEYS:
            raise ValueError(
                "Blind satisfaction criterion keys differ from its allowlist."
            )
    if len(resources) != 515 or not all(
        set(item) == RESOURCE_KEYS for item in resources
    ):
        raise ValueError("Blind resource record schema or count differs.")
    if any(
        set(item["resource_identity"]) != RESOURCE_IDENTITY_KEYS for item in resources
    ):
        raise ValueError("Blind resource identity keys differ from its allowlist.")


def _payloads(protocol: dict, native: dict) -> tuple[dict, bytes]:
    """Reconstruct deterministic packet bytes from only the retained snapshot."""
    if set(native) != {"request", "role_evidence", "preferences"}:
        raise ValueError("Native Stage A archive shape differs.")
    request = native["request"]
    _assert_task_correspondence(protocol, request)
    anchors, obligations = _task_projection(request.task)
    resources = _resources(request.snapshot, protocol)
    if len(anchors) != 6 or len(obligations) != 9:
        raise ValueError("Frozen task frame is incomplete.")
    archive_data = json.dumps(
        {"schema": "codex-case-0005-frozen-resources-v1", "resources": resources},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    archive_bytes = gzip.compress(archive_data, mtime=0)
    manifest = _manifest(protocol, request, sha(archive_bytes), anchors, obligations)
    validate_schema(manifest, resources)
    return manifest, archive_bytes


async def _verify_stage_a() -> tuple[dict, dict]:
    """Verify only the Stage A allowlisted artifacts and native source archive."""
    await git("merge-base", "--is-ancestor", STAGE_B, "HEAD")
    integrity = json.loads(read_bytes(CASE / "integrity.json"))
    if set(integrity) != EXPECTED_INTEGRITY_NAMES:
        raise ValueError("Stage A integrity inventory differs.")
    for filename, digest in integrity.items():
        current = read_bytes(CASE / filename)
        committed = await git("show", f"{STAGE_A}:{CASE_RELATIVE}/{filename}")
        if filename.endswith((".json", ".py", ".md")):
            current = canonical_text(current)
            committed = canonical_text(committed)
        if current != committed or sha(current) != digest:
            raise ValueError(f"Stage A artifact integrity failed: {filename}")
    protocol_bytes = canonical_text(read_bytes(CASE / "pre_retrieval.json"))
    protocol = json.loads(protocol_bytes)
    native_bytes = read_bytes(CASE / "inputs.pkl.gz")
    if sha(native_bytes) != protocol["inputs_sha256"]:
        raise ValueError("Stage A native input archive digest differs.")
    native = pickle.loads(gzip.decompress(native_bytes))  # noqa: S301
    if (
        protocol["case"] != "case_0005"
        or protocol["starting_head"] != "1bd2c7a5676ba78edd46879f2c06625c13c12d17"
        or str(native["request"].snapshot.repository_id) != protocol["repository_id"]
        or str(native["request"].snapshot.id) != protocol["snapshot_id"]
        or str(
            native[
                "request"
            ].index.corpus_statistics.collection_analysis.document_collection.corpus.id
        )
        != protocol["eligible_corpus_id"]
        or protocol["frame_resource_count"] != 515
    ):
        raise ValueError("Stage A repository/snapshot/frame binding differs.")
    return protocol, native


def verify() -> dict:
    """Verify a saved packet by deterministic reconstruction; no task judgments."""
    protocol, native = asyncio.run(_verify_stage_a())
    manifest, archive_expected = _payloads(protocol, native)
    manifest_bytes = canonical_text(read_bytes(MANIFEST))
    archive_bytes = read_bytes(ARCHIVE)
    parsed_manifest = json.loads(manifest_bytes)
    if (
        parsed_manifest != manifest
        or manifest_bytes != json_bytes(manifest)
        or archive_bytes != archive_expected
        or sha(archive_bytes) != manifest["resource_archive"]["sha256"]
    ):
        raise ValueError("Blind packet does not match deterministic reconstruction.")
    loaded = json.loads(gzip.decompress(archive_bytes))
    if (
        set(loaded) != {"schema", "resources"}
        or loaded["schema"] != "codex-case-0005-frozen-resources-v1"
    ):
        raise ValueError("Blind resource archive top-level schema differs.")
    validate_schema(manifest, loaded["resources"])
    _verify_resource_correspondence(native["request"].snapshot, loaded["resources"])
    return {
        "case": "case_0005",
        "resources": 515,
        "anchors": 6,
        "obligations": 9,
        "manifest_sha256": sha(manifest_bytes),
        "resource_archive_sha256": sha(archive_bytes),
        "deterministic_reconstruction": True,
        "retrieval_or_routing_executed": False,
    }


def _verify_resource_correspondence(snapshot, resources: list[dict]) -> None:
    """Check every packet record against its ordered Stage A occurrence."""
    if len(snapshot.resources) != len(resources) or len(resources) != 515:
        raise ValueError("Blind resource identity coverage differs.")
    seen = set()
    for source, packet in zip(snapshot.resources, resources, strict=True):
        address = source.address.value
        content_identity = source.content_identity.value
        expected_identity = {
            "repository_id": str(snapshot.repository_id),
            "snapshot_id": str(snapshot.id),
            "address": address,
            "content_identity": content_identity,
        }
        if (
            packet["resource_identity"] != expected_identity
            or packet["repository_id"] != str(snapshot.repository_id)
            or packet["snapshot_id"] != str(snapshot.id)
            or packet["address"] != address
            or packet["content_identity"] != content_identity
            or packet["content"] != source.content
            or address in seen
        ):
            raise ValueError("Blind resource record differs from retained snapshot.")
        seen.add(address)
    if len(seen) != 515:
        raise ValueError("Blind packet has duplicate or missing resource identities.")


def build() -> None:
    """Create the packet once with exclusive artifact creation."""
    if PACKET.exists() or MANIFEST.exists() or ARCHIVE.exists():
        raise FileExistsError("Blind packet exists; refusing to overwrite it.")
    protocol, native = asyncio.run(_verify_stage_a())
    manifest, archive_bytes = _payloads(protocol, native)
    manifest_bytes = json_bytes(manifest)
    resources = json.loads(gzip.decompress(archive_bytes))["resources"]
    _verify_resource_correspondence(native["request"].snapshot, resources)
    PACKET.mkdir()
    # Gzip is an explicit experimental binary boundary; there is no production
    # binary filesystem codec. Exclusive creation keeps packet files immutable.
    with ARCHIVE.open("xb") as stream:
        stream.write(archive_bytes)
    write(
        TextFile(resolve_path(MANIFEST), manifest_bytes.decode("utf-8")),
        overwrite=False,
    )
    result = verify()
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    if sys.argv[1:] == ["--build"]:
        build()
    elif sys.argv[1:] == ["--verify"]:
        print(json.dumps(verify(), ensure_ascii=True, sort_keys=True))
    else:
        raise SystemExit("Use --build once or --verify read-only.")
