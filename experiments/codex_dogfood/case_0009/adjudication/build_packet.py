# Copyright (c) 2026
# ruff: noqa: COM812, D103, EM101, EM102, PLR2004, T201, TRY003 -- isolated case recovery CLI
"""Deterministically render and verify the frozen Case 0009 blind packet."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    CASE,
    binary,
    json_bytes,
)
from experiments.codex_dogfood.case_0009.freeze import load_inputs
from experiments.codex_dogfood.case_0009.packet import (
    FORBIDDEN_KEYS,
    neutral_packet,
    validate_packet,
)

PACKET = CASE / "adjudication"
FILES = ("manifest.json", "resources.json.gz", "README.md")
README = """# Case 0009 independent blind adjudication

Read `manifest.json`, `resources.json.gz`, this instruction, and
`integrity.json` solely to verify packet integrity. Do not read parent
treatment, results, costs, protocol, implementation, or earlier case outcomes.
Use the obligation-relative methodology in the manifest. Freeze
complete identity-qualified judgments, applicability, required information
units, acceptable alternatives, and inferability before any treatment join.
This packet contains the entire eligible frame; no ranking or treatment
membership. No judgments have been made. A separate independent stage is
required.

Integrity fields distinguish `resources_payload_sha256` (canonical
uncompressed JSON bytes) from `resources_archive_sha256` (exact gzip bytes).
The archive uses deterministic gzip with `mtime=0`; `integrity.json` also seals
the manifest, archive, and this instruction.
"""

RECOVERY_FORBIDDEN_KEYS = frozenset(
    {
        "arm",
        "arm_a",
        "arm_b",
        "arm_identity",
        "canonical_rank",
        "identifier_aware_rank",
        "score_contributions",
        "score_contribution",
        "positive_result_membership",
        "positive_match",
        "identifier_analyzer_terms",
        "identifier_terms",
        "analyzer_terms",
        "rank_delta",
        "treatment_gain",
        "treatment_loss",
        "treatment_gains",
        "treatment_losses",
        "gains",
        "losses",
        "candidate_membership",
        "execution_cost",
        "treatment_cost",
        "effectiveness",
        "outcome",
    }
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def forbidden(value: object) -> bool:
    if isinstance(value, dict):
        return bool(
            (FORBIDDEN_KEYS | RECOVERY_FORBIDDEN_KEYS).intersection(value)
        ) or any(forbidden(item) for item in value.values())
    if isinstance(value, list):
        return any(forbidden(item) for item in value)
    return False


def render(native: dict[str, Any]) -> dict[str, bytes]:
    """Render manifest, canonical resource payload, and archive from Stage A."""
    old_manifest, resources = neutral_packet(native)
    payload = json_bytes(resources)
    archive = gzip.compress(payload, mtime=0)
    obligations = old_manifest["obligations"]
    manifest = {
        "schema": "case-0009-blind-task-v2",
        "case_identity": "case-0009",
        "task": old_manifest["task"],
        "task_identity": old_manifest["task_identity"],
        "repository_id": old_manifest["repository_id"],
        "snapshot_id": old_manifest["snapshot_id"],
        "corpus_id": old_manifest["corpus_id"],
        "obligations": obligations,
        "resource_count": old_manifest["resource_count"],
        "obligation_count": len(obligations),
        "expected_cell_count": old_manifest["resource_count"] * len(obligations),
        "resources_payload_sha256": sha256(payload),
        "resources_archive_sha256": sha256(archive),
        "packet_builder": "build_packet.py:v1; json_bytes; gzip.compress(mtime=0)",
        "instructions": old_manifest["instructions"],
    }
    manifest_bytes = json_bytes(manifest)
    integrity_bytes = json_bytes(
        {
            "schema": "case-0009-blind-integrity-v2",
            "sha256": {
                "README.md": sha256(README.encode("utf-8")),
                "manifest.json": sha256(manifest_bytes),
                "resources.json.gz": sha256(archive),
            },
        }
    )
    result = {
        "manifest.json": manifest_bytes,
        "resources.json.gz": archive,
        "README.md": README.encode("utf-8"),
        "integrity.json": integrity_bytes,
    }
    validate_render(manifest, resources, payload, archive)
    return result


def validate_render(
    manifest: dict[str, Any],
    resources: dict[str, Any],
    payload: bytes,
    archive: bytes,
) -> None:
    """Validate digests, exact packet shape, coverage, and treatment-key absence."""
    legacy_manifest = {
        key: value
        for key, value in manifest.items()
        if key
        not in {
            "case_identity",
            "obligation_count",
            "expected_cell_count",
            "resources_payload_sha256",
            "resources_archive_sha256",
            "packet_builder",
        }
    }
    legacy_manifest["schema"] = "case-0009-blind-task-v1"
    legacy_manifest["resources_sha256"] = manifest["resources_payload_sha256"]
    validate_packet(legacy_manifest, resources)
    if manifest["case_identity"] != "case-0009":
        raise ValueError("Blind case identity differs.")
    if manifest["obligation_count"] != len(manifest["obligations"]):
        raise ValueError("Blind obligation count differs.")
    if (
        manifest["expected_cell_count"]
        != manifest["resource_count"] * manifest["obligation_count"]
    ):
        raise ValueError("Blind cell count differs.")
    if manifest["resources_payload_sha256"] != sha256(payload):
        raise ValueError("Canonical payload digest differs.")
    if manifest["resources_archive_sha256"] != sha256(archive):
        raise ValueError("Archive byte digest differs.")
    if gzip.decompress(archive) != payload:
        raise ValueError("Archive does not contain the canonical payload.")
    if forbidden(manifest) or forbidden(resources):
        raise ValueError("Treatment metadata leaked into blind packet.")


def validate_stage_a(native: dict[str, Any], rendered: dict[str, bytes]) -> None:
    """Require exact frozen Stage A identities, contents, task, and obligations."""
    manifest = json.loads(rendered["manifest.json"])
    resources = json.loads(gzip.decompress(rendered["resources.json.gz"]))
    snapshot = native["snapshot"]
    expected = {
        item.address.value: (item.content_identity.value, item.content)
        for item in snapshot.resources
    }
    actual = {
        item["address"]: (item["content_identity"], item["content"])
        for item in resources["resources"]
    }
    if len(expected) != len(snapshot.resources):
        raise ValueError("Duplicate Stage A resource identities.")
    if len(actual) != len(resources["resources"]):
        raise ValueError("Duplicate packet resource identities.")
    if set(actual) != set(expected):
        raise ValueError("Stage A resource frame differs from packet.")
    if actual != expected:
        raise ValueError("Stage A resource content differs from packet.")
    if len(actual) != 531 or len(manifest["obligations"]) != 9:
        raise ValueError("Expected Case 0009 frame dimensions differ.")
    if manifest["expected_cell_count"] != 4779:
        raise ValueError("Expected Case 0009 cell count differs.")
    frozen_manifest, _ = neutral_packet(native)
    task = native["task"]
    if (
        manifest["task_identity"] != task.identity.value
        or manifest["task"] != frozen_manifest["task"]
    ):
        raise ValueError("Task identity or text differs from Stage A.")
    if manifest["obligations"] != frozen_manifest["obligations"]:
        raise ValueError("Frozen obligations differ from Stage A.")
    if (
        manifest["repository_id"] != str(snapshot.repository_id)
        or manifest["snapshot_id"] != str(snapshot.id)
        or manifest["corpus_id"] != str(native["corpus"].id)
    ):
        raise ValueError("Repository, snapshot, or corpus identity differs.")


def write_packet(rendered: dict[str, bytes], *, replace_existing: bool = False) -> None:
    """Publish packet only when absent unless recovery explicitly opts in."""
    targets = [PACKET / name for name in (*FILES, "integrity.json")]
    if not replace_existing and any(path.exists() for path in targets):
        raise FileExistsError(
            "Packet exists; refusing overwrite without explicit recovery flag."
        )
    PACKET.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        (PACKET / name).write_bytes(rendered[name])
    (PACKET / "integrity.json").write_bytes(rendered["integrity.json"])


def verify_committed() -> None:
    """Read-only replay against committed packet and hash-pinned Stage A inputs."""
    native = load_inputs()
    rendered = render(native)
    validate_stage_a(native, rendered)
    for name, expected in rendered.items():
        if binary(PACKET / name) != expected:
            raise ValueError(f"Committed packet replay differs: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("build", "verify"))
    parser.add_argument("--replace-existing", action="store_true")
    args = parser.parse_args()
    native = load_inputs()
    rendered = render(native)
    validate_stage_a(native, rendered)
    if args.operation == "build":
        write_packet(rendered, replace_existing=args.replace_existing)
    else:
        for name, expected in rendered.items():
            if binary(PACKET / name) != expected:
                raise ValueError(f"Committed packet replay differs: {name}")
    print("Verified Case 0009 blind packet; no judgments.")


if __name__ == "__main__":
    main()
