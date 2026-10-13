# Copyright (c) 2026
# ruff: noqa: COM812 -- audited historical proof boundary
"""Read-only Case 0016 compatibility proof, anchored in its accepted Git seal.

This adapter is specific to the audited producer control flow, not a heuristic
acceptance of old manifests. Unknown seals fail without falling back to replay.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    json_bytes,
)
from experiments.codex_dogfood.case_0016 import freeze
from experiments.codex_dogfood.case_0016.stage_b import authenticate as a
from experiments.codex_dogfood.case_0016.stage_d.authentication import SEAL

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class AuthenticatedCompletion:
    """Invocation-local immutable evidence identity; no native object cache."""

    bindings: bytes
    envelopes: int
    native_archives_decoded: int = 0
    deep_correspondence_executions: int = 0
    timings: tuple[tuple[str, int], ...] = ()


def require(condition: bool, message: str) -> None:  # noqa: FBT001 -- local assertion
    """Fail explicitly instead of accidentally launching deep replay."""
    if not condition:
        raise ValueError(message + "; explicit deep/proof migration required")


def authenticate(root: Path) -> AuthenticatedCompletion:  # noqa: PLR0915 -- complete compatibility boundary
    """Authenticate the exact publication that followed successful deep proof.

    Accepted seal b94b... binds reporting.publish/derived/reconstruct and the
    inherited Journal.load implementation. Those exact bodies prove native
    correspondence and captured algebra before integrity.json can be published.
    The authoritative Git blob is additionally checked by Stage D checkpoints.
    """
    started = time.perf_counter_ns()
    raw = (root / "integrity.json").read_bytes()
    require(digest(raw) == SEAL, "Unknown or modified authoritative capture seal")
    seal = json.loads(raw)
    paths = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.name != "integrity.json"
    }
    require(paths == set(seal["sha256"]), "Capture file set differs")
    seal_time = time.perf_counter_ns() - started
    canonical_time = 0
    archive_time = 0
    for name, expected in seal["sha256"].items():
        start = time.perf_counter_ns()
        require(
            digest((root / name).read_bytes()) == expected, "Capture bytes: " + name
        )
        elapsed = time.perf_counter_ns() - start
        if "/" not in name and name not in {
            "native_context.json",
            "execution.claim",
            "execution_started.json",
            "execution_completed.json",
        }:
            canonical_time += elapsed
        else:
            archive_time += elapsed
    bindings_start = time.perf_counter_ns()
    sources = a.source_hashes()
    require(
        seal["implementation_sha256"] == sources,
        "Proof producer implementation differs",
    )
    require(seal["execution"] == a.EXECUTION, "Foreign execution seal")

    def load(name: str) -> dict[str, Any]:
        return cast("dict[str, Any]", json.loads((root / name).read_bytes()))

    marker = load("execution_started.json")
    schedule_raw = binary(a.SCHEDULE_PATH)
    schedule = json.loads(schedule_raw)
    stage_a = json.loads(binary(freeze.CASE / "integrity.json"))
    frame = json.loads(binary(freeze.CASE / "frame.json"))
    expected_frame = {
        k: frame[k] for k in ("repository_id", "snapshot_id", "corpus_id")
    }
    require(
        marker["case"] == "0016"
        and marker["execution"] == a.EXECUTION
        and marker["stage_a"] == a.STAGE_A
        and marker["frame"] == expected_frame
        and marker["implementation_sha256"] == sources
        and marker["scientific_implementation_sha256"] == stage_a["implementation"]
        and marker["protocol_sha256"] == digest(binary(freeze.CASE / "protocol.json"))
        and marker["schedule_sha256"] == seal["schedule_sha256"] == digest(schedule_raw)
        and marker["operation_schedule"] == schedule["operations"]
        and schedule["execution"] == a.EXECUTION
        and schedule["protocol_sha256"] == marker["protocol_sha256"],
        "Capture identity/frame/protocol/source/schedule differs",
    )
    for name, sha in marker["scientific_implementation_sha256"].items():
        require(
            digest(binary(ROOT / name)) == sha, "Scientific implementation: " + name
        )
    require(
        load("execution.claim") == {"execution": a.EXECUTION}, "Execution claim differs"
    )
    context = load("native_context.json")
    require(
        context["marker_sha256"]
        == digest((root / "execution_started.json").read_bytes()),
        "Context marker differs",
    )
    chain = digest((root / "native_context.json").read_bytes())
    operations = []
    identities: list[str] = []
    for ordinal, identity in enumerate(schedule["operations"], 1):
        entered_sha = ""
        original = None
        for offset, status in enumerate(("ENTERED", "RETURNED")):
            name = f"operations/{ordinal:06}.{status.lower()}.json"
            event_raw = (root / name).read_bytes()
            event = json.loads(event_raw)
            require(
                event["event"] == 2 * ordinal - 1 + offset
                and event["sequence"] == ordinal
                and event["state"] == status
                and event["prior_chain_sha256"] == chain
                and event["execution"] == a.EXECUTION
                and event["frame"] == marker["frame"]
                and event["runtime_identity"] == marker["runtime"],
                "Journal chain/order/frame/runtime differs",
            )
            op = event["operation"]
            require(
                op["identity"] == identity
                and op["invocations"] == 1
                and op["status"] == status
                and op["prior_operations"] == identities
                and event["input_sha256"] == digest(json_bytes(op["inputs"])),
                "Journal operation/input/schedule differs",
            )
            if status == "ENTERED":
                original = op
                entered_sha = digest(event_raw)
            else:
                require(
                    event["entered_sha256"] == entered_sha
                    and original is not None
                    and op["inputs"] == original["inputs"],
                    "Return envelope entry binding differs",
                )
                operations.append(op)
            chain = digest(event_raw)
        identities.append(identity)
    completed = load("execution_completed.json")
    require(
        completed
        == {
            "execution": a.EXECUTION,
            "journal_chain_sha256": chain,
            "operations": identities,
        },
        "Completion seal differs",
    )
    trace = load("trace.json")
    validation = load("validation.json")
    require(
        trace["operations"] == operations
        and trace["operation_schedule"] == identities
        and trace["authentication"] == marker["authentication"]
        and trace["validation"] == validation,
        "Published deep-proof evidence differs",
    )
    require(
        all(
            v == "PASS"
            for k, v in validation.items()
            if k not in {"gold", "effectiveness", "outcome", "no_scientific_replay"}
        ),
        "Capture-time validation did not pass",
    )
    require(
        all(seal["sha256"].get(n) == sha for n, sha in trace["artifacts"].items()),
        "Canonical artifact publication binding differs",
    )
    bindings = {
        "schema": "case-0016-audited-publication-proof-v1",
        "case": "0016",
        "execution": a.EXECUTION,
        "frame": expected_frame,
        "integrity_sha256": SEAL,
        "journal_chain_sha256": chain,
        "completion_sha256": seal["sha256"]["execution_completed.json"],
        "validation_sha256": seal["sha256"]["validation.json"],
        "protocol_sha256": marker["protocol_sha256"],
        "schedule_sha256": seal["schedule_sha256"],
        "implementation_sha256": sources,
        "scientific_implementation_sha256": marker["scientific_implementation_sha256"],
        "artifact_sha256": seal["sha256"],
        "capture_time_deep_proof": "AUTHENTICATED_BY_AUDITED_PUBLICATION",
        "authority": "4925f8896edc49b6162d191a6d348f78dd958a48",
    }
    return AuthenticatedCompletion(
        json_bytes(bindings),
        len(identities) + 1,
        timings=(
            ("capture_seal_identity", seal_time),
            ("canonical_artifact_hash_authentication", canonical_time),
            ("journal_archive_byte_authentication", archive_time),
            (
                "completion_chain_source_authentication",
                time.perf_counter_ns() - bindings_start,
            ),
        ),
    )
