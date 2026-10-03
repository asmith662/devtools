# Copyright (c) 2026
# Case-specific packet assertions and inspection CLI.
# ruff: noqa: ANN001, ANN201, D103, INP001, S101, PLR2004
"""Case 0005 static blind archive inspection; never reads checkout resources."""

import gzip
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
MANIFEST_BYTES = (BASE / "blind_manifest.json").read_bytes()
MANIFEST = json.loads(MANIFEST_BYTES)
ARCHIVE_BYTES = (BASE / "blind_resources.json.gz").read_bytes()
ARCHIVE = json.loads(gzip.decompress(ARCHIVE_BYTES))
RESOURCES = ARCHIVE["resources"]
BY_PATH = {r["address"]: r for r in RESOURCES}


def validate_packet():
    assert hashlib.sha256(MANIFEST_BYTES).hexdigest() == (
        "c3d6455d09bcd53beec75c7d325489096f3b4a44c8b2aa6c4266233d93ca1177"
    )
    assert MANIFEST["schema"] == "codex-case-0005-blind-adjudication-v1"
    assert ARCHIVE["schema"] == "codex-case-0005-frozen-resources-v1"
    assert MANIFEST["case"] == "case_0005"
    assert MANIFEST["task_identity"] == (
        "codex-dogfood-case-0005-evidence-witness-association"
    )
    assert len(MANIFEST["anchors"]) == 6
    assert len(MANIFEST["obligations"]) == 9
    validate_task_frame()
    assert len(RESOURCES) == len(BY_PATH) == 515
    assert (
        hashlib.sha256(ARCHIVE_BYTES).hexdigest()
        == (MANIFEST["resource_archive"]["sha256"])
    )
    assert set(ARCHIVE) == {"schema", "resources"}
    expected = {
        "address",
        "content",
        "content_identity",
        "repository_id",
        "resource_identity",
        "snapshot_id",
    }
    for resource in RESOURCES:
        assert set(resource) == expected
        identity = resource["resource_identity"]
        assert set(identity) == expected - {"content", "resource_identity"}
        assert all(identity[k] == resource[k] for k in identity)
        assert resource["repository_id"] == MANIFEST["repository_id"]
        assert resource["snapshot_id"] == MANIFEST["snapshot_id"]
        digest = hashlib.sha256()
        for value in ("decoded-utf8-text-sha256-v1", resource["content"]):
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, byteorder="big"))
            digest.update(encoded)
        assert digest.hexdigest() == resource["content_identity"]
    # Structural fields only: repository text may naturally discuss these concepts.
    forbidden = {
        "lexical_query",
        "lexical_queries",
        "query_identity",
        "query_text",
        "preferred_roles",
        "caller_role_preferences",
        "role_assignments",
        "role_support_records",
        "routing_tier",
        "routed_position",
        "native_rank",
        "bm25_rank",
        "bm25_score",
        "score",
        "retrieved",
        "candidate_count",
        "acquisition_runtime",
        "routing_runtime",
        "retrieval_results",
        "routing_results",
    }

    def check(value) -> None:
        if isinstance(value, dict):
            assert not forbidden.intersection(value)
            for key, child in value.items():
                if key != "content":
                    check(child)
        elif isinstance(value, list):
            for child in value:
                check(child)

    check(MANIFEST)
    check(ARCHIVE)


def validate_task_frame():
    task_digest = hashlib.sha256(MANIFEST["task_text"].encode()).hexdigest()
    assert task_digest == (
        "b2d16844deea7f9f65b29a65064a1f0a9fc167a8cebcd39fc28e04bc68f335ec"
    )
    assert MANIFEST["purpose"].strip()
    for item in MANIFEST["anchors"] + MANIFEST["obligations"]:
        assert item["provenance"]["source_identity"] == task_digest
        assert item["provenance"]["span"] is None
        assert item["provenance"]["explanation"] == (
            "Frozen caller-authored task interpretation."
        )
    assert MANIFEST["repository_id"] == "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
    assert MANIFEST["snapshot_id"] == (
        "0705f0e5ef729d28ed044f36b929a2c9436ad38c821c154bd11430f5fb58989a"
    )
    assert MANIFEST["eligible_frame_identity"] == (
        "12fe8c45e9b90ad9142a2700e6a4c258e222ceb64d719df4e7cb06bc8e2b4d7b"
    )
    assert MANIFEST["eligible_resource_count"] == 515
    assert set(MANIFEST) == {
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
    anchor_ids = {item["identity"] for item in MANIFEST["anchors"]}
    assert anchor_ids == {
        "localization",
        "witnesses",
        "evidence",
        "identity",
        "integration",
        "quality",
    }
    assert {item["identity"] for item in MANIFEST["obligations"]} == {
        "semantic-ownership",
        "witness-algebra",
        "native-evidence",
        "role-routing-integration",
        "snapshot-frame",
        "package-integration",
        "tests",
        "documentation",
        "validation",
    }
    for obligation in MANIFEST["obligations"]:
        assert obligation["requirement_status"] == "mandatory"
        assert set(obligation["anchor_references"]) <= anchor_ids
        assert obligation["predicate"].strip()
        assert set(obligation["satisfaction_criterion"]) == {"name", "statement"}
        assert all(obligation["satisfaction_criterion"].values())
        assert obligation["witness_alternatives"] == []
        expected_condition = (
            "Existing package/API conventions govern integration of the new "
            "association capability."
            if obligation["identity"] == "package-integration"
            else None
        )
        assert obligation["applicability_condition"] == expected_condition


if __name__ == "__main__":
    validate_packet()
    for path in sys.argv[1:]:
        resource = BY_PATH[path]
        sys.stdout.write(f"\n=== {path} ===\n")
        for number, line in enumerate(resource["content"].splitlines(), 1):
            sys.stdout.write(f"{number}: {line}\n")
