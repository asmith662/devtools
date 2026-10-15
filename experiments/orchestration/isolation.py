# Copyright (c) 2026
# ruff: noqa: ANN401, PLC0415 -- case-local sterile transport
"""Create case-isolated inputs and authenticate semantic artifact preservation."""

from __future__ import annotations

import gzip
import json
from typing import TYPE_CHECKING, Any

from experiments.orchestration.storage import (
    bundle,
    materialize,
    no_links,
    require,
    safe,
)
from experiments.structural_discrimination.stage_c.validate_packet import metadata

if TYPE_CHECKING:
    from pathlib import Path

PRIMARY = (
    "stage_c_review.json",
    "stage_c_statistics.json",
    "STAGE_C_REVIEW.md",
    "stage_c_validation.json",
    "stage_c_hashes.json",
    "stage_c_method.md",
    "stage_c_builder.py",
)


def sterile(root: Path, files: dict[str, bytes]) -> None:
    """Copy only packet-authorized exact files; reject treatment metadata."""
    require(
        files and all("/" not in n and n not in {".git", ".local"} for n in files),
        "Sterile file allowlist",
    )
    for name, raw in files.items():
        if name.endswith(".json"):
            metadata(json.loads(raw))
        elif name.endswith(".json.gz"):
            metadata(json.loads(gzip.decompress(raw)))
    materialize(root, files)
    require(
        {p.name for p in root.iterdir()} == set(files),
        "Initial sterile allowlist differs",
    )


def preserve_packet(root: Path, files: dict[str, bytes]) -> None:
    """Reauthenticate original packets after process termination and validation."""
    no_links(root)
    for name, raw in files.items():
        require(safe(root, name).read_bytes() == raw, "Original packet mutation")
    require(not (root / ".git").exists(), "Reviewer Git metadata forbidden")
    for path in root.rglob("*"):
        no_links(path)


def candidate(
    root: Path,
    case: str,
    frame: Any,
    expected_stage: str,
) -> tuple[Any, dict[str, bytes]]:
    """Authenticate transport; scientific validators retain semantic ownership."""
    from experiments.orchestration.storage import load

    value = load(root / "candidate.json")
    require(
        set(value) == {"schema", "case", "frame", "stage", "files"}
        and value["schema"] == "experiment-candidate-v1",
        "Candidate transport schema",
    )
    require(
        value["case"] == case
        and value["frame"] == frame
        and value["stage"] == expected_stage,
        "Candidate identity/frame/stage",
    )
    require(
        value["files"]
        and all(
            not n.startswith((".local/", ".scratch/"))
            and not n.endswith((".pyc", ".pyo"))
            for n in value["files"]
        ),
        "Operational files are not science",
    )
    require(
        expected_stage != "D" or "controller_summary.json" not in value["files"],
        "Controller summary is reserved publication ownership",
    )
    return value, bundle(root, value["files"])


def semantic_receipt(receipt: Any, configuration: Any) -> None:
    """Require blindness/model/single-primary authentication."""
    require(
        receipt["status"] == "PASS"
        and receipt["model"] == configuration["model"]
        and receipt["reasoning"].lower() == configuration["reasoning"].lower(),
        "Semantic designation/validation differs",
    )
    require(
        receipt["second_reviewer"] is False and receipt["reconciliation"] is False,
        "Single primary/no reconciliation required",
    )
    access = receipt["blindness"]
    forbidden = {
        "repository",
        "git_history",
        "parent_siblings",
        "prior_session",
        "web",
        "queries",
        "ranks_scores",
        "annotations",
        "references_treatment",
        "pairs",
        "timings",
        "graph_ppr_rrf",
        "other_cases",
        "child",
        "prior_gold",
        "confirmation_reserve",
    }
    if (
        configuration.get("authorized_surface")
        == "TREATMENT_INDEPENDENT_BROAD_CANDIDATES"
    ):
        forbidden = {
            "repository",
            "git_history",
            "parent_siblings",
            "prior_session",
            "web",
            "queries",
            "ranks_scores",
            "grounding",
            "qualified",
            "treatment_results",
            "timings",
            "other_cases",
            "child",
            "prior_gold",
            "confirmation_reserve",
        }
        require(
            receipt.get("authorized_surface") == configuration["authorized_surface"],
            "Candidate-surface disclosure attestation differs",
        )
    require(
        set(access) == forbidden and all(v is False for v in access.values()),
        "Blindness attestation differs",
    )
    require(
        receipt["host_routing_independently_verified"] is False
        or receipt.get("routing_evidence_sha256"),
        "Unsubstantiated host routing",
    )


def semantic_outputs(files: dict[str, bytes]) -> None:
    """Reject treatment metadata in scientific JSON as an additional blind check."""
    for name, raw in files.items():
        if name.endswith(".json"):
            metadata(json.loads(raw))
