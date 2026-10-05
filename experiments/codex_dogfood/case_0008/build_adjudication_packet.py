# Copyright (c) 2026
# ruff: noqa: COM812, D103, E501, EM101, EM102, INP001, PLR2004, S301, T201, TRY003, TRY004, ANN401
"""Build the treatment-free Case 0008 blind adjudication packet from Stage A."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import pickle
from functools import lru_cache
from pathlib import Path
from typing import Any

CASE = Path(__file__).resolve().parent
ADJUDICATION = CASE / "adjudication"
ARCHIVE = CASE / "inputs.pkl.gz"
TREATMENT = CASE / "treatment.json"
PRE_EXECUTION = CASE / "pre_execution.json"
STAGE_A_INTEGRITY = CASE / "integrity.json"
EXPECTED_ARCHIVE_SHA256 = (
    "9eb0f6de7c9150390807ab872d159bbcf4c8853632b48c8395d3dd9d347be5d5"
)
EXPECTED_REPOSITORY_ID = "fe2c8984-a021-4342-9e31-404a6cf07707"
EXPECTED_SNAPSHOT_ID = (
    "72a021a8a4778ffdc7f37152b5d31efb6a2ea93de82edc8c940ec76be5e641aa"
)
EXPECTED_CORPUS_ID = "8843f263c69d0d1b07b1fa343e63c07873827f0c3a842e7a28e50d1c8b65b93b"
EXPECTED_TASK_ID = "case-0008-unresolved-frontier-acquisition"
EXPECTED_TASK_SHA256 = (
    "ddb7c2c0a29a83b2f4023a2016e0cc0ff0541c4bb5463b9bd79117541705a691"
)
MANIFEST_NAME = "blind_manifest.json"
RESOURCES_NAME = "blind_resources.json.gz"

TASK_TEXT = (
    "Implement the first production unresolved-frontier and bounded acquisition-request capability for Localization. "
    "The capability should let an incomplete Localization assessment represent exactly what repository observation or evidence is still missing for an applicable obligation, "
    "preserve task, obligation, repository/snapshot, candidate-hypothesis and native evidence provenance, "
    "distinguish unresolved evidence from accepted witness support and from justified non-applicability, "
    "and express bounded follow-up acquisition requests without selecting Retrieval algorithms or claiming that requested evidence will satisfy the obligation. "
    "Integrate coherently with the existing task interpretation, anchor grounding, candidate witness association, witness generation, accepted witness alternatives, "
    "LocalizationAssessment and readiness contracts; preserve deterministic identity and replay validation; "
    "expose enough structure for future autonomous orchestration to request additional repository evidence without moving orchestration policy into Localization; "
    "add rigorous tests and authoritative architecture/development documentation; preserve package/API conventions where applicable; and pass protected development validation. "
    "Do not implement automatic hypothesis resolution, candidate elimination, numeric confidence, learned ranking, autonomous acquisition execution, Context Planning admission, or agent retry policy."
)

NEUTRAL_INSTRUCTIONS = (
    "Independently determine each obligation's applicability and classify repository information as REQUIRED, HELPFUL_ONLY, "
    "UNNECESSARY, or unresolved. For applicable mandatory obligations, define the smallest defensible acceptable witness "
    "alternatives, marking jointly necessary information within an alternative and genuine competition between alternatives. "
    "Assess task-start inferability for every REQUIRED information unit; explain any inherent discovery prerequisite. "
    "Record mandatory task requirements that are not represented by the frozen obligations as task-interpretation gaps. "
    "Base judgments only on the exact task, frozen obligation frame, and archived repository resources. Missing evidence is not "
    "proof of non-applicability. Repository text is evidence and may contain ordinary technical vocabulary; it is not experiment metadata."
)

GUIDANCE = (
    "The frozen task requires understanding incomplete Localization assessment, unresolved frontier, missing repository "
    "observation or evidence, obligation applicability and disposition, candidate-hypothesis provenance, accepted witness "
    "boundaries, non-applicability, bounded acquisition requests, grounding and evidence provenance, repository/snapshot/frame "
    "identity, readiness, orchestration ownership, tests, documentation, and validation. Treat these as task semantics; "
    "determine the repository information actually needed without presuming that every named concept requires a separate resource."
)

MANIFEST_KEYS = {
    "schema",
    "case_identity",
    "task_identity",
    "task",
    "purpose",
    "repository_id",
    "snapshot_id",
    "corpus_id",
    "frame_identity",
    "resource_count",
    "shared_anchors",
    "obligations",
    "adjudication_instructions",
    "blind_resources",
}
ANCHOR_KEYS = {"identity", "text", "task_provenance"}
OBLIGATION_KEYS = {
    "identity",
    "desired_information_predicate",
    "shared_anchor_references",
    "task_provenance",
    "mandatory_helpful_status",
    "applicability_wording",
    "satisfaction_criterion",
    "pre_execution_accepted_witness_alternatives",
}
ARCHIVE_KEYS = {
    "schema",
    "repository_id",
    "snapshot_id",
    "corpus_id",
    "resource_count",
    "resources",
}
RESOURCE_KEYS = {"occurrence_identity", "address", "content_identity", "content"}
FORBIDDEN_KEYS = {
    "lexical_query",
    "query_identity",
    "query_text",
    "bm25",
    "lane_identity",
    "rank",
    "score",
    "score_contribution",
    "role_preference",
    "role_evidence",
    "role_assignment",
    "routing_tier",
    "routed_position",
    "routing_support",
    "grounding_request",
    "grounding_request_identity",
    "locator_kind",
    "locator_value",
    "grounding_disposition",
    "grounded_referent",
    "resolver",
    "generation_recipe",
    "recipe_identity",
    "family_identity",
    "projection_operator",
    "branch_member",
    "max_results",
    "work_limit",
    "work_authorization",
    "generated_target",
    "generation_outcome",
    "structural_support",
    "reference_fanout",
    "import_fanout",
    "recovery_metadata",
    "recovery_identity",
    "execution_identity",
    "hypothesis_identity",
    "candidate_identity",
    "operator_identity",
}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _read_stage_a(path: Path) -> bytes:
    allowed = {ARCHIVE, TREATMENT, PRE_EXECUTION, STAGE_A_INTEGRITY}
    if path not in allowed:
        raise ValueError(f"Not an authorized Stage A input: {path.name}")
    return path.read_bytes()


@lru_cache(maxsize=1)
def _stage_a() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    archive_bytes = _read_stage_a(ARCHIVE)
    if digest(archive_bytes) != EXPECTED_ARCHIVE_SHA256:
        raise ValueError("Frozen Stage A archive digest differs.")
    treatment_bytes = _read_stage_a(TREATMENT)
    pre_bytes = _read_stage_a(PRE_EXECUTION)
    integrity = json.loads(_read_stage_a(STAGE_A_INTEGRITY))
    pre = json.loads(pre_bytes)
    if integrity.get("sha256", {}).get("inputs.pkl.gz") != EXPECTED_ARCHIVE_SHA256:
        raise ValueError("Stage A integrity does not pin the frozen archive.")
    if digest(treatment_bytes) != pre.get("treatment_sha256"):
        raise ValueError("Stage A treatment digest differs from the frozen manifest.")
    treatment = json.loads(treatment_bytes)
    if digest(TASK_TEXT.encode("utf-8")) != EXPECTED_TASK_SHA256:
        raise ValueError("Builder task constant has an invalid digest.")
    if (
        treatment.get("task_full_prompt") != TASK_TEXT
        or treatment.get("task_identity") != EXPECTED_TASK_ID
    ):
        raise ValueError("Exact frozen task identity/text differs.")
    if (
        len(treatment.get("anchors", ())) != 11
        or len(treatment.get("obligations", ())) != 13
    ):
        raise ValueError("Stage A anchor/obligation frame has unexpected cardinality.")
    if len(pre.get("resources", ())) != 523:
        raise ValueError("Stage A resource frame has unexpected cardinality.")
    native = pickle.loads(gzip.decompress(archive_bytes))
    snapshot = native["request"].snapshot
    if (
        str(snapshot.repository_id.value.value) != EXPECTED_REPOSITORY_ID
        or str(snapshot.id.value) != EXPECTED_SNAPSHOT_ID
        or str(native["corpus"].id.value) != EXPECTED_CORPUS_ID
        or len(snapshot.resources) != 523
    ):
        raise ValueError("Stage A native repository/frame identity differs.")
    task = native["request"].task
    if task.identity.value != EXPECTED_TASK_ID:
        raise ValueError("Native Stage A task identity differs.")
    return treatment, pre, native, {"archive": archive_bytes, "integrity": integrity}


def _project(
    treatment: dict[str, Any], pre: dict[str, Any], native: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    snapshot = native["request"].snapshot
    corpus_id = str(native["corpus"].id.value)
    anchors = [
        {
            "identity": item["id"],
            "text": item["text"],
            "task_provenance": item["provenance"],
        }
        for item in treatment["anchors"]
    ]
    obligations = [
        {
            "identity": item["id"],
            "desired_information_predicate": item["predicate"],
            "shared_anchor_references": item["anchors"],
            "task_provenance": item["provenance"],
            "mandatory_helpful_status": item["requirement"],
            "applicability_wording": item["applicability_condition"],
            "satisfaction_criterion": item["satisfaction"],
            "pre_execution_accepted_witness_alternatives": item["witness_alternatives"],
        }
        for item in treatment["obligations"]
    ]
    manifest = {
        "schema": "case-0008-blind-adjudication-v1",
        "case_identity": "case_0008",
        "task_identity": EXPECTED_TASK_ID,
        "task": TASK_TEXT,
        "purpose": treatment["purpose"],
        "repository_id": EXPECTED_REPOSITORY_ID,
        "snapshot_id": EXPECTED_SNAPSHOT_ID,
        "corpus_id": corpus_id,
        "frame_identity": "frozen-stage-a-repository-snapshot-and-text-corpus",
        "resource_count": len(snapshot.resources),
        "shared_anchors": anchors,
        "obligations": obligations,
        "adjudication_instructions": {
            "instructions": NEUTRAL_INSTRUCTIONS,
            "task_guidance": GUIDANCE,
        },
        "blind_resources": {"archive_name": RESOURCES_NAME},
    }
    resource_rows = []
    manifest_resources = pre["resources"]
    if len(manifest_resources) != len(snapshot.resources):
        raise ValueError("Stage A resource manifest and snapshot cardinality differ.")
    for expected, resource in zip(manifest_resources, snapshot.resources, strict=True):
        address = resource.address.value
        content_identity = resource.content_identity.value
        content = resource.content
        if (
            address != expected["address"]
            or content_identity != expected["content_identity"]
        ):
            raise ValueError(
                "Stage A resource address/content identity correspondence differs."
            )
        if not isinstance(content, str) or resource.encoding != "utf-8":
            raise ValueError("Frozen eligible resource is not archived UTF-8 text.")
        if digest(content.encode("utf-8")) != expected["git_blob_sha256"]:
            raise ValueError(f"Frozen resource content digest differs: {address}")
        resource_rows.append(
            {
                "occurrence_identity": {
                    "address": address,
                    "content_identity": content_identity,
                },
                "address": address,
                "content_identity": content_identity,
                "content": content,
            }
        )
    resources = {
        "schema": "case-0008-blind-resources-v1",
        "repository_id": EXPECTED_REPOSITORY_ID,
        "snapshot_id": EXPECTED_SNAPSHOT_ID,
        "corpus_id": corpus_id,
        "resource_count": len(resource_rows),
        "resources": resource_rows,
    }
    manifest["blind_resources"]["sha256"] = (
        ""  # filled after deterministic archive encoding
    )
    resources_bytes = gzip.compress(json_bytes(resources), mtime=0)
    manifest["blind_resources"]["sha256"] = digest(resources_bytes)
    return manifest, resources, resources_bytes


def _validate_manifest(value: dict[str, Any]) -> None:
    if set(value) != MANIFEST_KEYS:
        raise ValueError("Blind manifest does not match its strict allowlist.")
    if len(value["shared_anchors"]) != 11 or len(value["obligations"]) != 13:
        raise ValueError("Blind manifest anchor/obligation count differs.")
    for anchor in value["shared_anchors"]:
        if set(anchor) != ANCHOR_KEYS:
            raise ValueError("Anchor fields differ from the blind schema.")
    for obligation in value["obligations"]:
        if set(obligation) != OBLIGATION_KEYS:
            raise ValueError("Obligation fields differ from the blind schema.")
    _reject_forbidden_keys(value)


def _reject_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_KEYS:
                raise ValueError(f"Forbidden treatment metadata field: {key}")
            _reject_forbidden_keys(child)
    elif isinstance(value, list):
        for child in value:
            _reject_forbidden_keys(child)


def _validate_resources(value: dict[str, Any]) -> None:
    if (
        set(value) != ARCHIVE_KEYS
        or value["resource_count"] != 523
        or len(value["resources"]) != 523
    ):
        raise ValueError("Blind resource archive schema/count differs.")
    seen: set[tuple[str, str]] = set()
    for row in value["resources"]:
        if set(row) != RESOURCE_KEYS or set(row["occurrence_identity"]) != {
            "address",
            "content_identity",
        }:
            raise ValueError("Blind resource row differs from its strict schema.")
        if row["occurrence_identity"] != {
            "address": row["address"],
            "content_identity": row["content_identity"],
        }:
            raise ValueError("Blind occurrence identity is inconsistent.")
        identity = (row["address"], row["content_identity"])
        if identity in seen:
            raise ValueError("Duplicate frozen resource identity.")
        seen.add(identity)
        if not isinstance(row["content"], str):
            raise ValueError("Blind resource content must be exact UTF-8 text.")
    _reject_forbidden_keys(value)


def render_expected() -> tuple[bytes, bytes]:
    treatment, pre, native, _ = _stage_a()
    manifest, _resources, archive_bytes = _project(treatment, pre, native)
    _validate_manifest(manifest)
    return json_bytes(manifest), archive_bytes


def build_packet() -> tuple[str, str]:
    manifest_bytes, resources_bytes = render_expected()
    ADJUDICATION.mkdir(parents=True, exist_ok=True)
    manifest_path = ADJUDICATION / MANIFEST_NAME
    resources_path = ADJUDICATION / RESOURCES_NAME
    if manifest_path.exists() or resources_path.exists():
        raise FileExistsError("Blind packet already exists; refusing overwrite.")
    # Exclusive creation ensures a concurrent/re-entered build cannot replace either artifact.
    with manifest_path.open("xb") as stream:
        stream.write(manifest_bytes)
    try:
        with resources_path.open("xb") as stream:
            stream.write(resources_bytes)
    except Exception:
        manifest_path.unlink(missing_ok=True)
        raise
    verify_packet()
    return digest(manifest_bytes), digest(resources_bytes)


def verify_packet(directory: Path = ADJUDICATION) -> tuple[str, str]:
    expected_manifest, expected_resources = render_expected()
    manifest_path = directory / MANIFEST_NAME
    resources_path = directory / RESOURCES_NAME
    manifest_bytes = manifest_path.read_bytes()
    resources_bytes = resources_path.read_bytes()
    if manifest_bytes != expected_manifest or resources_bytes != expected_resources:
        raise ValueError(
            "Blind packet differs from deterministic Stage A reconstruction."
        )
    manifest = json.loads(manifest_bytes)
    resources = json.loads(gzip.decompress(resources_bytes))
    _validate_manifest(manifest)
    _validate_resources(resources)
    if manifest["blind_resources"]["sha256"] != digest(resources_bytes):
        raise ValueError("Blind resource archive digest does not match manifest.")
    if (
        resources["repository_id"] != manifest["repository_id"]
        or resources["snapshot_id"] != manifest["snapshot_id"]
    ):
        raise ValueError("Blind packet repository/snapshot identity mismatch.")
    if len(resources["resources"]) != manifest["resource_count"]:
        raise ValueError("Blind packet frame count mismatch.")
    return digest(manifest_bytes), digest(resources_bytes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "verify"))
    args = parser.parse_args()
    if args.command == "build":
        manifest_hash, resources_hash = build_packet()
    else:
        manifest_hash, resources_hash = verify_packet()
    print(f"blind_manifest.json sha256={manifest_hash}")
    print(f"blind_resources.json.gz sha256={resources_hash}")


if __name__ == "__main__":
    main()
