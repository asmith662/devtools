# Copyright (c) 2026
# ruff: noqa: C901, COM812, PLR2004, S301, S603, S607, T201
"""Build or verify the sanitized Case 0004 blind-adjudication packet."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import pickle
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from devtools.context.localization.lexical import (
        LocalizationLexicalAcquisitionRequest,
    )

ROOT = Path(__file__).resolve().parents[3]
CASE = Path(__file__).resolve().parent
PACKET = CASE / "adjudication"
PROTOCOL = CASE / "pre_retrieval.json"
INPUTS = CASE / "inputs.pkl.gz"
STAGE_A = "719a3d44b45ebc664414ab0267ff23d836cc10a0"
STAGE_B = "9416efc80028ca463375d005e114fb3143fd968d"
STARTING_HEAD = "3cfda0a81ae95f578f42b8fd6b17cc8bcf751bc1"
MANIFEST_NAME = "blind_manifest.json"
RESOURCES_NAME = "blind_resources.json.gz"

MANIFEST_KEYS = {
    "schema",
    "case_identity",
    "task_identity",
    "task_text",
    "purpose",
    "repository_id",
    "snapshot_id",
    "eligible_frame_identity",
    "eligible_resource_count",
    "anchors",
    "obligations",
    "adjudication_instructions",
    "resource_archive",
}
ANCHOR_KEYS = {"identity", "text", "provenance"}
OBLIGATION_KEYS = {
    "identity",
    "predicate",
    "anchors",
    "provenance",
    "requirement",
    "applicability_condition",
    "satisfaction",
    "witness_alternatives",
}
ARCHIVE_KEYS = {
    "schema",
    "repository_id",
    "snapshot_id",
    "eligible_frame_identity",
    "resources",
}
RESOURCE_KEYS = {"identity", "address", "path", "content_identity", "content"}
ADJUDICATION_KEYS = {
    "judge_applicability_from_bounded_repository_evidence",
    "resource_categories",
    "record_acceptable_alternative_witness_sets",
    "distinguish_task_start_inferability_from_named_inherent_discovery",
    "freeze_judgments_before_any_evaluation_join",
    "do_not_treat_missing_evidence_as_non_applicability",
    "scope_claims_to_the_supplied_obligation_frame_and_snapshot",
}
PROVENANCE_KEYS = {"source_identity", "task_phrase", "explanation"}
ANCHOR_PROVENANCE_KEYS = {"source_identity", "explanation"}
SATISFACTION_KEYS = {"name", "statement"}
RESOURCE_ARCHIVE_KEYS = {"path", "sha256", "format"}


def _sha256(content: bytes) -> str:
    """Return lowercase SHA-256 for bytes."""
    return hashlib.sha256(content).hexdigest()


def _git_blob(commit: str, path: str) -> bytes:
    """Read one exact committed source blob."""
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def _canonical_working_text(path: Path) -> bytes:
    """Normalize line endings for comparison with committed text."""
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode()


def _validate_stage_a() -> tuple[dict[str, Any], LocalizationLexicalAcquisitionRequest]:
    """Verify Stage A and load its retained request, never Stage B output."""
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True)
    if head.strip() != STAGE_B:
        msg = "Blind packet construction requires the expected Stage B commit."
        raise ValueError(msg)
    protocol_bytes = _canonical_working_text(PROTOCOL)
    protocol_path = "experiments/codex_dogfood/case_0004/pre_retrieval.json"
    if protocol_bytes != _git_blob(STAGE_A, protocol_path):
        msg = "Stage A protocol differs from its committed content."
        raise ValueError(msg)
    archive_bytes = INPUTS.read_bytes()
    if archive_bytes != _git_blob(
        STAGE_A, "experiments/codex_dogfood/case_0004/inputs.pkl.gz"
    ):
        msg = "Stage A request archive differs from its committed content."
        raise ValueError(msg)
    protocol = json.loads(protocol_bytes)
    if (
        protocol["status"] != "FROZEN BEFORE RETRIEVAL"
        or protocol["starting_head"] != STARTING_HEAD
        or protocol["retrieval_executed"] is not False
        or protocol["confirmation_accessed"] is not False
        or _sha256(archive_bytes) != protocol["inputs_archive_sha256"]
    ):
        msg = "Stage A protocol/archive identity validation failed."
        raise ValueError(msg)
    # The committed digest authenticates this repository-owned pickle input.
    request = pickle.loads(gzip.decompress(archive_bytes))
    _validate_request_fields(protocol, request)
    for path, digest in protocol["implementation_sha256"].items():
        current = (ROOT / path).read_text(encoding="utf-8").encode("utf-8")
        if (
            _sha256(current) != digest
            or _sha256(_git_blob(STARTING_HEAD, path)) != digest
        ):
            msg = f"Frozen implementation digest mismatch: {path}."
            raise ValueError(msg)
    return protocol, request


def _validate_request_fields(
    protocol: dict[str, Any], request: LocalizationLexicalAcquisitionRequest
) -> None:
    """Match authorized task/frame fields to the committed Stage A request."""
    if (
        request.task.identity.value != protocol["task_identity"]
        or request.full_task_query != protocol["task_full_prompt"]
        or _sha256(request.full_task_query.encode()) != protocol["task_sha256"]
        or request.purpose != protocol["purpose"]
        or str(request.snapshot.repository_id) != protocol["repository_id"]
        or str(request.snapshot.id) != protocol["snapshot_id"]
        or len(request.snapshot.resources) != protocol["frame_resource_count"]
    ):
        msg = "Frozen task or repository frame does not match Stage A."
        raise ValueError(msg)
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    if (
        str(corpus.id) != protocol["eligible_corpus_id"]
        or corpus.resources != request.snapshot.resources
        or len(corpus.resources) != protocol["frame_resource_count"]
    ):
        msg = "Frozen corpus membership does not match the retained snapshot."
        raise ValueError(msg)
    expected_resources = [
        {"address": str(item.address), "content_identity": str(item.content_identity)}
        for item in request.snapshot.resources
    ]
    if expected_resources != protocol["snapshot_resources"]:
        msg = "Frozen resource addresses/content identities differ from Stage A."
        raise ValueError(msg)
    if len(request.task.anchors) != len(protocol["anchors"]):
        msg = "Frozen anchor count differs from Stage A."
        raise ValueError(msg)
    for anchor, frozen in zip(request.task.anchors, protocol["anchors"], strict=True):
        if (
            anchor.identity.value != frozen["identity"]
            or anchor.text != frozen["text"]
            or str(anchor.provenance.source_identity)
            != frozen["provenance"]["source_identity"]
            or anchor.provenance.explanation != frozen["provenance"]["explanation"]
        ):
            msg = "Frozen shared anchor differs from Stage A."
            raise ValueError(msg)
    if len(request.task.obligations) != len(protocol["obligations"]):
        msg = "Frozen obligation count differs from Stage A."
        raise ValueError(msg)
    for obligation, frozen in zip(
        request.task.obligations, protocol["obligations"], strict=True
    ):
        if (
            obligation.identity.value != frozen["identity"]
            or obligation.predicate != frozen["predicate"]
            or [anchor.value for anchor in obligation.anchors] != frozen["anchors"]
            or str(obligation.provenance.source_identity)
            != frozen["provenance"]["source_identity"]
            or obligation.provenance.explanation != frozen["provenance"]["explanation"]
            or obligation.requirement.value != frozen["requirement"]
            or obligation.applicability_condition != frozen["applicability_condition"]
            or obligation.satisfaction.name != frozen["satisfaction"]["name"]
            or obligation.satisfaction.statement != frozen["satisfaction"]["statement"]
            or [list(item.members) for item in obligation.witness_alternatives]
            != frozen["witness_alternatives"]
        ):
            msg = "Frozen obligation semantics differ from Stage A."
            raise ValueError(msg)
    if len(request.obligation_queries) != len(protocol["obligation_lanes"]):
        msg = "Frozen request query association differs from Stage A."
        raise ValueError(msg)
    for query, frozen in zip(
        request.obligation_queries, protocol["obligation_lanes"], strict=True
    ):
        if (
            query.identity.value != frozen["identity"]
            or query.obligation.value != frozen["obligation"]
            or query.text != frozen["query_text"]
        ):
            msg = "Frozen request query association differs from Stage A."
            raise ValueError(msg)


def _authorized_manifest(
    protocol: dict[str, Any], archive_digest: str, count: int
) -> dict[str, Any]:
    """Project authorized semantic fields into a restricted blind schema."""
    return {
        "schema": "codex-case-0004-blind-adjudication-v1",
        "case_identity": protocol["case"],
        "task_identity": protocol["task_identity"],
        "task_text": protocol["task_full_prompt"],
        "purpose": protocol["purpose"],
        "repository_id": protocol["repository_id"],
        "snapshot_id": protocol["snapshot_id"],
        "eligible_frame_identity": protocol["eligible_corpus_id"],
        "eligible_resource_count": count,
        "anchors": [
            {
                "identity": item["identity"],
                "text": item["text"],
                "provenance": item["provenance"],
            }
            for item in protocol["anchors"]
        ],
        "obligations": [
            {
                "identity": item["identity"],
                "predicate": item["predicate"],
                "anchors": item["anchors"],
                "provenance": item["provenance"],
                "requirement": item["requirement"],
                "applicability_condition": item["applicability_condition"],
                "satisfaction": item["satisfaction"],
                "witness_alternatives": item["witness_alternatives"],
            }
            for item in protocol["obligations"]
        ],
        "adjudication_instructions": {
            "judge_applicability_from_bounded_repository_evidence": True,
            "resource_categories": [
                "REQUIRED",
                "HELPFUL_ONLY",
                "UNNECESSARY",
                "UNRESOLVED",
            ],
            "record_acceptable_alternative_witness_sets": True,
            "distinguish_task_start_inferability_from_named_inherent_discovery": True,
            "freeze_judgments_before_any_evaluation_join": True,
            "do_not_treat_missing_evidence_as_non_applicability": True,
            "scope_claims_to_the_supplied_obligation_frame_and_snapshot": True,
        },
        "resource_archive": {
            "path": RESOURCES_NAME,
            "sha256": archive_digest,
            "format": "gzip-compressed UTF-8 JSON; deterministic resource order",
        },
    }


def _resource_archive(request: LocalizationLexicalAcquisitionRequest) -> bytes:
    """Serialize only retained snapshot resource identities and exact content."""
    resources = [
        {
            "identity": f"repository-resource-address:{item.address}",
            "address": str(item.address),
            "path": str(item.address),
            "content_identity": str(item.content_identity),
            "content": item.content,
        }
        for item in request.snapshot.resources
    ]
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    payload = {
        "schema": "codex-case-0004-blind-resources-v1",
        "repository_id": str(request.snapshot.repository_id),
        "snapshot_id": str(request.snapshot.id),
        "eligible_frame_identity": str(corpus.id),
        "resources": resources,
    }
    return gzip.compress(
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        mtime=0,
    )


def _validate_packet(
    protocol: dict[str, Any],
    request: LocalizationLexicalAcquisitionRequest,
    manifest: dict[str, Any],
    archive_bytes: bytes,
) -> None:
    """Check allowlisted fields and each resource against retained snapshot."""
    if set(manifest) != MANIFEST_KEYS:
        msg = "Blind manifest fields differ from the allowlisted schema."
        raise ValueError(msg)
    if any(set(item) != ANCHOR_KEYS for item in manifest["anchors"]):
        msg = "Blind anchor fields differ from the allowlist."
        raise ValueError(msg)
    if any(set(item) != OBLIGATION_KEYS for item in manifest["obligations"]):
        msg = "Blind obligation fields differ from the allowlist."
        raise ValueError(msg)
    if set(manifest["adjudication_instructions"]) != ADJUDICATION_KEYS:
        msg = "Blind adjudication instruction fields differ from the allowlist."
        raise ValueError(msg)
    if set(manifest["resource_archive"]) != RESOURCE_ARCHIVE_KEYS:
        msg = "Blind resource archive descriptor differs from the allowlist."
        raise ValueError(msg)
    if any(
        set(item["provenance"]) != ANCHOR_PROVENANCE_KEYS
        for item in manifest["anchors"]
    ):
        msg = "Blind anchor provenance fields differ from the allowlist."
        raise ValueError(msg)
    if any(
        set(item["provenance"]) != PROVENANCE_KEYS
        or set(item["satisfaction"]) != SATISFACTION_KEYS
        for item in manifest["obligations"]
    ):
        msg = "Blind obligation nested fields differ from the allowlist."
        raise ValueError(msg)
    archive = json.loads(gzip.decompress(archive_bytes))
    if set(archive) != ARCHIVE_KEYS or any(
        set(item) != RESOURCE_KEYS for item in archive["resources"]
    ):
        msg = "Blind resource archive fields differ from the allowlist."
        raise ValueError(msg)
    corpus = (
        request.index.corpus_statistics.collection_analysis.document_collection.corpus
    )
    if (
        manifest["eligible_resource_count"] != 498
        or len(archive["resources"]) != 498
        or manifest["repository_id"] != str(request.snapshot.repository_id)
        or manifest["snapshot_id"] != str(request.snapshot.id)
        or archive["repository_id"] != str(request.snapshot.repository_id)
        or archive["snapshot_id"] != str(request.snapshot.id)
        or manifest["eligible_frame_identity"] != str(corpus.id)
        or archive["eligible_frame_identity"] != str(corpus.id)
        or manifest["task_identity"] != request.task.identity.value
    ):
        msg = "Blind packet frame identity or resource count is invalid."
        raise ValueError(msg)
    expected_manifest = _authorized_manifest(
        protocol, _sha256(archive_bytes), len(request.snapshot.resources)
    )
    if manifest != expected_manifest:
        msg = "Blind manifest differs from its authorized Stage A projection."
        raise ValueError(msg)
    for packet, retained in zip(
        archive["resources"], request.snapshot.resources, strict=True
    ):
        if (
            packet["identity"] != f"repository-resource-address:{retained.address}"
            or packet["address"] != str(retained.address)
            or packet["path"] != str(retained.address)
            or packet["content_identity"] != str(retained.content_identity)
            or packet["content"] != retained.content
        ):
            msg = "Blind resource entry differs from retained snapshot content."
            raise ValueError(msg)


def _build_artifacts() -> tuple[bytes, bytes]:
    """Construct deterministic packet bytes from Stage A inputs only."""
    protocol, request = _validate_stage_a()
    archive_bytes = _resource_archive(request)
    manifest = _authorized_manifest(
        protocol, _sha256(archive_bytes), len(request.snapshot.resources)
    )
    _validate_packet(protocol, request, manifest, archive_bytes)
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    return manifest_bytes, archive_bytes


def build() -> None:
    """Create the two blind packet artifacts without overwriting."""
    if PACKET.exists():
        msg = "Case 0004 blind packet already exists; refusing to overwrite."
        raise FileExistsError(msg)
    manifest_bytes, archive_bytes = _build_artifacts()
    PACKET.mkdir()
    (PACKET / MANIFEST_NAME).write_bytes(manifest_bytes)
    (PACKET / RESOURCES_NAME).write_bytes(archive_bytes)
    print(
        json.dumps(
            {
                "packet": "BLIND ADJUDICATION PACKET FROZEN",
                "resource_count": 498,
                "manifest_sha256": _sha256(manifest_bytes),
                "resource_archive_sha256": _sha256(archive_bytes),
            },
            sort_keys=True,
        )
    )


def verify() -> None:
    """Rebuild bytes in memory and compare without writing or reading results."""
    if {item.name for item in PACKET.iterdir()} != {MANIFEST_NAME, RESOURCES_NAME}:
        msg = "Blind adjudication directory contains unexpected artifacts."
        raise ValueError(msg)
    expected_manifest, expected_archive = _build_artifacts()
    if (PACKET / MANIFEST_NAME).read_bytes() != expected_manifest or (
        PACKET / RESOURCES_NAME
    ).read_bytes() != expected_archive:
        msg = "Blind packet differs from deterministic Stage A reconstruction."
        raise ValueError(msg)
    print(
        json.dumps(
            {
                "verification": "PASS",
                "resource_count": 498,
                "manifest_sha256": _sha256(expected_manifest),
                "resource_archive_sha256": _sha256(expected_archive),
            },
            sort_keys=True,
        )
    )


def main() -> None:
    """Build once or verify the existing packet without changing it."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    if parser.parse_args().mode == "build":
        build()
    else:
        verify()


if __name__ == "__main__":
    main()
