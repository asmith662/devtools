# Copyright (c) 2026
# ruff: noqa: ANN001, C901, COM812, E501, EM101, EM102, INP001, PLR0912, PLR2004, T201, TRY003, TRY004
"""Build and verify the treatment-free Case 0006 blind packet."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import pickle
from pathlib import Path

CASE = Path(__file__).resolve().parent
ROOT = CASE.parents[2]
ADJUDICATION = CASE / "adjudication"
MANIFEST_NAME = "blind_manifest.json"
RESOURCES_NAME = "blind_resources.json.gz"
STAGE_A = "e7aed4162672dd859a0a8a33a2b718dda8425495"
SOURCE_HEAD = "492229e0e0d4661cf5287c26d18c6488a80fe8ce"
REPOSITORY_ID = "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
SNAPSHOT_ID = "ba654221b65584aebdd98804369864162ac3f7da1bf8862abee06ce4d2127a55"
CORPUS_ID = "49c69d2db7c6616731d9c24519a48d47a13a2ee991d46aaaf33d1f5d55b212b9"
RESOURCE_COUNT = 531
EXPECTED_INPUTS_SHA256 = (
    "572b8a575e08fc0012871bbddcbe780b026be03bdca670e607a9f09988ccd402"
)
EXPECTED_INTEGRITY_SHA256 = (
    "12eaa8d412d1ba4abcc4ceb62d0efe9900f96d6a7bbb5ae87b407c57af6b7a35"
)

MANIFEST_KEYS = {
    "schema",
    "case_identity",
    "task_identity",
    "development_task",
    "purpose",
    "repository_id",
    "repository_snapshot_id",
    "eligible_frame_identity",
    "eligible_resource_count",
    "shared_anchors",
    "obligations",
    "adjudication_instructions",
    "resource_archive",
    "resource_archive_sha256",
}
ANCHOR_KEYS = {"identity", "text", "task_provenance"}
PROVENANCE_KEYS = {"source_identity", "span", "explanation"}
CRITERION_KEYS = {"name", "statement"}
OBLIGATION_KEYS = {
    "identity",
    "desired_information_predicate",
    "anchor_references",
    "task_provenance",
    "requirement",
    "applicability_condition",
    "satisfaction_criterion",
    "pre_execution_witness_alternatives",
}
RESOURCE_ARCHIVE_KEYS = {
    "schema",
    "case_identity",
    "repository_id",
    "repository_snapshot_id",
    "eligible_frame_identity",
    "resources",
}
RESOURCE_KEYS = {"identity", "address", "content_identity", "content"}
FORBIDDEN_KEYS = {
    "lexical_query",
    "lexical_queries",
    "query_identity",
    "query_text",
    "role_preference",
    "role_assignment",
    "rank",
    "score",
    "routing_tier",
    "routed_position",
    "grounding_request",
    "locator_kind",
    "locator_value",
    "grounding_disposition",
    "grounded_referent",
    "generation_recipe",
    "projection_operator",
    "generated_target",
    "generation_outcome",
    "recovery_metadata",
}
INSTRUCTIONS = [
    "Use only the frozen task and frozen repository resource frame to judge the information target.",
    "Determine applicability for each obligation, including conditional applicability, using affirmative repository evidence.",
    "Classify obligation-relative information as REQUIRED, HELPFUL_ONLY, UNNECESSARY, or unresolved.",
    "For applicable mandatory obligations, identify the smallest defensible acceptable witness alternatives; all members within one alternative are complementary and any complete alternative may suffice.",
    "For REQUIRED information, classify whether its need is INFERABLE_AT_START or INHERENT_DISCOVERY; document the exact prerequisite and later observation for any inherent discovery.",
    "Record any obvious mandatory task-interpretation gap separately without changing the frozen obligation frame.",
    "Do not infer non-applicability from missing evidence. Preserve unresolved judgments where the frozen contents do not support a defensible conclusion.",
]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode("utf-8")


def _read(path: Path) -> bytes:
    if path.suffix == ".gz":
        with path.open("rb") as stream:
            return stream.read(128 << 20)
    return path.read_bytes()


def _verify_stage_a() -> tuple[dict, dict, bytes]:
    integrity_bytes = _read(CASE / "integrity.json")
    if _sha(integrity_bytes) != EXPECTED_INTEGRITY_SHA256:
        raise ValueError("Frozen Stage A integrity manifest differs.")
    integrity = json.loads(integrity_bytes)
    for name, expected in integrity.items():
        data = _read(CASE / name)
        if name.endswith((".py", ".md", ".json")):
            data = data.replace(b"\r\n", b"\n")
        if _sha(data) != expected:
            raise ValueError(f"Frozen Stage A artifact changed: {name}")
    manifest = json.loads(_read(CASE / "pre_retrieval.json"))
    archive = _read(CASE / "inputs.pkl.gz")
    if (
        _sha(archive) != EXPECTED_INPUTS_SHA256
        or manifest["inputs_sha256"] != EXPECTED_INPUTS_SHA256
    ):
        raise ValueError("Frozen Stage A native archive digest differs.")
    if manifest["starting_head"] != SOURCE_HEAD:
        raise ValueError("Frozen Stage A source snapshot identity differs.")
    for relative, expected in manifest["implementation_sha256"].items():
        data = _read(ROOT / relative).replace(b"\r\n", b"\n")
        if _sha(data) != expected:
            raise ValueError(f"Frozen production source changed: {relative}")
    native = pickle.loads(gzip.decompress(archive))  # noqa: S301
    request = native["request"]
    snapshot = request.snapshot
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    if (
        str(snapshot.repository_id) != REPOSITORY_ID
        or str(snapshot.id) != SNAPSHOT_ID
        or str(corpus.id) != CORPUS_ID
        or len(snapshot.resources) != RESOURCE_COUNT
        or manifest["repository_id"] != REPOSITORY_ID
        or manifest["snapshot_id"] != SNAPSHOT_ID
        or manifest["eligible_corpus_id"] != CORPUS_ID
        or manifest["frame_resource_count"] != RESOURCE_COUNT
    ):
        raise ValueError("Frozen task/resource frame identity differs.")
    if (
        manifest["task_identity"] != request.task.identity.value
        or manifest["task_sha256"] != _sha(request.full_task_query.encode("utf-8"))
        or manifest["task_full_prompt"] != request.full_task_query
        or manifest["purpose"] != request.purpose
        or len(request.task.anchors) != len(manifest["anchors"])
        or len(request.task.obligations) != len(manifest["obligations"])
    ):
        raise ValueError("Frozen task semantic bindings differ.")
    return native, manifest, archive


def _provenance(value) -> dict:
    span = value.span
    if span is not None:
        raise ValueError("Unexpected task provenance span cannot be projected safely.")
    return {
        "source_identity": str(value.source_identity),
        "span": None,
        "explanation": value.explanation,
    }


def _project(native: dict) -> tuple[dict, bytes]:
    request = native["request"]
    task = request.task
    if any(item.witness_alternatives for item in task.obligations):
        raise ValueError("Stage A unexpectedly contains pre-execution witness targets.")
    anchors = [
        {
            "identity": item.identity.value,
            "text": item.text,
            "task_provenance": _provenance(item.provenance),
        }
        for item in task.anchors
    ]
    obligations = [
        {
            "identity": item.identity.value,
            "desired_information_predicate": item.predicate,
            "anchor_references": [anchor.value for anchor in item.anchors],
            "task_provenance": _provenance(item.provenance),
            "requirement": item.requirement.value,
            "applicability_condition": item.applicability_condition,
            "satisfaction_criterion": {
                "name": item.satisfaction.name,
                "statement": item.satisfaction.statement,
            },
            "pre_execution_witness_alternatives": [],
        }
        for item in task.obligations
    ]
    resources = []
    for item in request.snapshot.resources:
        address = item.address.value
        content_identity = item.content_identity.value
        resources.append(
            {
                "identity": {
                    "address": address,
                    "content_identity": content_identity,
                },
                "address": address,
                "content_identity": content_identity,
                "content": item.content,
            }
        )
    resource_archive = _canonical(
        {
            "schema": "case-0006-blind-resources-v1",
            "case_identity": "case_0006",
            "repository_id": REPOSITORY_ID,
            "repository_snapshot_id": SNAPSHOT_ID,
            "eligible_frame_identity": CORPUS_ID,
            "resources": resources,
        }
    )
    manifest = {
        "schema": "case-0006-blind-adjudication-v1",
        "case_identity": "case_0006",
        "task_identity": task.identity.value,
        "development_task": request.full_task_query,
        "purpose": request.purpose,
        "repository_id": REPOSITORY_ID,
        "repository_snapshot_id": SNAPSHOT_ID,
        "eligible_frame_identity": CORPUS_ID,
        "eligible_resource_count": RESOURCE_COUNT,
        "shared_anchors": anchors,
        "obligations": obligations,
        "adjudication_instructions": INSTRUCTIONS,
        "resource_archive": RESOURCES_NAME,
        "resource_archive_sha256": _sha(gzip.compress(resource_archive, mtime=0)),
    }
    return manifest, gzip.compress(resource_archive, mtime=0)


def _walk_keys(value) -> set[str]:
    result = set()
    if isinstance(value, dict):
        for key, child in value.items():
            result.add(str(key).casefold())
            result.update(_walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            result.update(_walk_keys(child))
    return result


def _validate(manifest: dict, resources_bytes: bytes) -> None:
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("Blind manifest fields differ from the explicit allowlist.")
    if FORBIDDEN_KEYS.intersection(_walk_keys(manifest)):
        raise ValueError("Blind manifest exposes a forbidden treatment field.")
    if len(manifest["shared_anchors"]) != len(
        {item["identity"] for item in manifest["shared_anchors"]}
    ):
        raise ValueError("Blind anchor identity repeats.")
    if any(set(item) != ANCHOR_KEYS for item in manifest["shared_anchors"]):
        raise ValueError("Blind anchor fields differ from allowlist.")
    anchor_ids = {item["identity"] for item in manifest["shared_anchors"]}
    if any(
        set(item["task_provenance"]) != PROVENANCE_KEYS
        for item in manifest["shared_anchors"]
    ):
        raise ValueError("Anchor task provenance schema differs from allowlist.")
    if len(manifest["obligations"]) != 10 or any(
        set(item) != OBLIGATION_KEYS for item in manifest["obligations"]
    ):
        raise ValueError("Blind obligation frame/schema differs.")
    obligation_ids = {item["identity"] for item in manifest["obligations"]}
    if len(obligation_ids) != 10 or any(
        set(item["task_provenance"]) != PROVENANCE_KEYS
        or set(item["satisfaction_criterion"]) != CRITERION_KEYS
        or not set(item["anchor_references"]).issubset(anchor_ids)
        or item["pre_execution_witness_alternatives"] != []
        for item in manifest["obligations"]
    ):
        raise ValueError("Obligation nested schema or frozen references differ.")
    if manifest["resource_archive_sha256"] != _sha(resources_bytes):
        raise ValueError("Blind resource archive digest differs.")
    archive = json.loads(gzip.decompress(resources_bytes))
    if set(archive) != RESOURCE_ARCHIVE_KEYS:
        raise ValueError("Blind resource archive fields differ from allowlist.")
    if (
        archive["case_identity"] != "case_0006"
        or archive["repository_id"] != REPOSITORY_ID
        or archive["repository_snapshot_id"] != SNAPSHOT_ID
        or archive["eligible_frame_identity"] != CORPUS_ID
    ):
        raise ValueError("Blind resource archive frame identity differs.")
    resources = archive["resources"]
    if len(resources) != RESOURCE_COUNT or any(
        set(item) != RESOURCE_KEYS for item in resources
    ):
        raise ValueError("Blind resource frame/schema differs.")
    if FORBIDDEN_KEYS.intersection(_walk_keys(archive)):
        raise ValueError("Blind resource schema exposes a forbidden treatment field.")
    if len({item["address"] for item in resources}) != RESOURCE_COUNT:
        raise ValueError("Blind resource address repeats.")
    for item in resources:
        if item["identity"] != {
            "address": item["address"],
            "content_identity": item["content_identity"],
        }:
            raise ValueError("Native resource identity projection differs.")
        if not isinstance(item["content"], str):
            raise ValueError("Blind resource content is not UTF-8 text.")


def build() -> dict:
    """Build packet once from Stage A archive; refuse existing packet files."""
    ADJUDICATION.mkdir(parents=True, exist_ok=True)
    existing = [
        name
        for name in (MANIFEST_NAME, RESOURCES_NAME)
        if (ADJUDICATION / name).exists()
    ]
    if existing:
        raise FileExistsError(f"Blind packet already exists: {existing}")
    native, _stage_a_manifest, _archive = _verify_stage_a()
    manifest, resources_bytes = _project(native)
    manifest_bytes = _canonical(manifest)
    _validate(manifest, resources_bytes)
    (ADJUDICATION / RESOURCES_NAME).write_bytes(resources_bytes)
    try:
        with (ADJUDICATION / MANIFEST_NAME).open("xb") as target:
            target.write(manifest_bytes)
    except Exception:
        (ADJUDICATION / RESOURCES_NAME).unlink(missing_ok=True)
        raise
    return {
        "manifest_sha256": _sha(manifest_bytes),
        "resources_sha256": _sha(resources_bytes),
        "resource_count": RESOURCE_COUNT,
        "obligation_count": len(manifest["obligations"]),
        "anchor_count": len(manifest["shared_anchors"]),
    }


def verify() -> dict:
    """Read-only packet schema, digest, and frozen-frame verification."""
    native, _stage_a_manifest, _archive = _verify_stage_a()
    manifest_bytes = _read(ADJUDICATION / MANIFEST_NAME)
    resources_bytes = _read(ADJUDICATION / RESOURCES_NAME)
    manifest = json.loads(manifest_bytes)
    _validate(manifest, resources_bytes)
    expected, expected_gzip = _project(native)
    if manifest_bytes != _canonical(expected) or resources_bytes != expected_gzip:
        raise ValueError(
            "Blind packet does not deterministically reconstruct from Stage A."
        )
    archive = json.loads(gzip.decompress(resources_bytes))
    frozen_resources = native["request"].snapshot.resources
    if len(frozen_resources) != len(archive["resources"]):
        raise ValueError("Blind frame count differs from frozen snapshot.")
    for frozen, projected in zip(frozen_resources, archive["resources"], strict=True):
        if (
            frozen.address.value != projected["address"]
            or frozen.content_identity.value != projected["content_identity"]
            or frozen.content != projected["content"]
        ):
            raise ValueError("Blind resource differs from exact frozen occurrence.")
    return {
        "manifest_sha256": _sha(manifest_bytes),
        "resources_sha256": _sha(resources_bytes),
        "resource_count": len(archive["resources"]),
        "obligation_count": len(manifest["obligations"]),
        "anchor_count": len(manifest["shared_anchors"]),
        "deterministic_reconstruction": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--verify", action="store_true")
    arguments = parser.parse_args()
    if arguments.build == arguments.verify:
        raise SystemExit("Choose exactly one of --build or --verify.")
    print(json.dumps(build() if arguments.build else verify(), sort_keys=True))
