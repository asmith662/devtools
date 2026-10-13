# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003 -- exact sealed capture boundary
"""Authenticate immutable envelopes and completion proof; no normal native replay."""

from __future__ import annotations

import gzip
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    git,
    json_bytes,
)
from experiments.codex_dogfood.verification.proof import (
    CompletionBindings,
    authenticate_proof,
)
from experiments.structural_discrimination.stage_b.capture import (
    STAGE_A,
    capture_root,
    source_hashes,
)
from experiments.structural_discrimination.stage_b.reporting import canonical_validate


def journal_envelopes(root: Path) -> tuple[Any, str]:
    """Every claim/event/input/order/frame/chain binding, without unpacking archives."""
    marker = json.loads((root / "execution_started.json").read_bytes())
    if json.loads((root / "execution.claim").read_bytes()) != {
        "execution": marker["execution"],
    }:
        raise ValueError("Execution claim differs")
    chain = digest((root / "execution_started.json").read_bytes())
    context = json.loads((root / "native_context.json").read_bytes())
    if context["marker_sha256"] != chain:
        raise ValueError("Context marker differs")
    chain = digest((root / "native_context.json").read_bytes())
    operations: list[str] = []
    active = None
    records = [
        (json.loads(p.read_bytes()), p) for p in (root / "operations").glob("*.json")
    ]
    records.sort(key=lambda pair: pair[0]["event"])
    for event, (value, path) in enumerate(records, 1):
        sequence, state = value["sequence"], value["state"]
        if (
            value["event"] != event
            or value["prior_chain_sha256"] != chain
            or value["execution"] != marker["execution"]
            or value["frame"] != marker["frame"]
            or value["runtime_identity"] != marker["runtime"]
            or path.name != f"{sequence:06}.{state.lower()}.json"
        ):
            raise ValueError("Journal event chain/frame/order differs")
        operation = value["operation"]
        if state == "ENTERED":
            if (
                active is not None
                or sequence != len(operations) + 1
                or operation["identity"] != marker["operations"][sequence - 1]
                or operation["invocations"] != 1
                or operation["prior_operations"] != operations
                or value["input_sha256"] != digest(json_bytes(operation["inputs"]))
            ):
                raise ValueError("Journal entered schedule/input differs")
            active = value
        elif state == "RETURNED":
            if (
                active is None
                or sequence != len(operations) + 1
                or value["entered_sha256"]
                != digest(
                    (root / "operations" / f"{sequence:06}.entered.json").read_bytes(),
                )
                or value["input_sha256"] != active["input_sha256"]
                or any(
                    operation[k] != active["operation"][k]
                    for k in ("identity", "invocations", "inputs", "prior_operations")
                )
                or operation["status"] != "RETURNED"
                or set(value["native"]) != {"gzip_b85", "sha256"}
                or set(value["canonical"]) != {"gzip_b85", "sha256"}
            ):
                raise ValueError("Journal return/native envelope differs")
            operations.append(operation["identity"])
            active = None
        else:
            raise ValueError("Incomplete/failed scientific capture")
        chain = digest(path.read_bytes())
    complete = json.loads((root / "execution_completed.json").read_bytes())
    if (
        active is not None
        or operations != marker["operations"]
        or complete
        != {
            "execution": marker["execution"],
            "journal_chain_sha256": chain,
            "operations": operations,
        }
    ):
        raise ValueError("Execution completion/schedule differs")
    return marker, chain


def bindings(root: Path, hashes: Any, implementation: Any) -> CompletionBindings:
    """Bind acyclic exact completion/input/verifier scopes."""
    marker, chain = journal_envelopes(root)
    native = {
        p: h
        for p, h in hashes.items()
        if p.startswith("operations/")
        or p in {"native_context.json", "execution_started.json", "execution.claim"}
    }
    canonical = {
        p: h
        for p, h in hashes.items()
        if p not in native and p != "execution_completed.json"
    }
    verifier = {
        p: h
        for p, h in implementation.items()
        if "/verification/" in p or "/stage_b/" in p
    }
    return CompletionBindings.create(
        {
            "case": marker["case"],
            "execution": marker["execution"],
            "frame": marker["frame"],
            "protocol_sha256": marker["protocol_sha256"],
            "schedule_sha256": marker["schedule_sha256"],
            "journal_chain_sha256": chain,
            "native_sha256": native,
            "canonical_sha256": canonical,
            "implementation_sha256": implementation,
            "verifier_sha256": verifier,
            "completion_sha256": hashes["execution_completed.json"],
        },
    )


def sealed(root: Path, authoritative_seal: bytes) -> dict[str, Any]:
    """Fresh physical/source authentication; authority is supplied externally."""
    if (root / "integrity.json").read_bytes() != authoritative_seal:
        raise ValueError("Authoritative capture integrity differs")
    seal = json.loads(authoritative_seal)
    hashes = seal["sha256"]
    members = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if members != set(hashes) | {"integrity.json"}:
        raise ValueError("Capture file completeness differs")
    for path, sha in hashes.items():
        if digest((root / path).read_bytes()) != sha:
            raise ValueError("Capture artifact bytes differ: " + path)
    if seal["implementation"] != source_hashes():
        raise ValueError("Capture implementation binding differs")
    marker, _chain = journal_envelopes(root)
    if (
        marker["stage_a_checkpoint"] != STAGE_A
        or marker["implementation"] != seal["implementation"]
        or digest((root / "operation_schedule.json").read_bytes())
        != marker["schedule_sha256"]
    ):
        raise ValueError("Capture Stage A/schedule/source binding differs")
    original_hashes = {p: h for p, h in hashes.items() if p != "completion_proof.json"}
    authenticate_proof(
        (root / "completion_proof.json").read_bytes(),
        hashes["completion_proof.json"],
        bindings(root, original_hashes, seal["implementation"]),
    )
    trace = json.loads(gzip.decompress((root / "trace.json.gz").read_bytes()))
    canonical_validate(trace)
    if (
        trace["summary"] != json.loads((root / "summary.json").read_bytes())
        or trace["queries"]
        != json.loads(gzip.decompress((root / "arm_a.json.gz").read_bytes()))
        or trace["positive_references"]
        != json.loads(gzip.decompress((root / "references.json.gz").read_bytes()))
    ):
        raise ValueError("Canonical scientific artifact correspondence differs")
    if (
        marker["design"]["parent_frame"] != trace["summary"]["frame"]
        or marker["design"]["task_text"] != trace["summary"]["task"]
    ):
        raise ValueError("Canonical task/frame binding differs")
    return {
        "status": "PASS",
        "proof": "CAPTURE_TIME_DEEP_PROOF_AUTHENTICATED",
        "native_archives_decoded": 0,
        "deep_correspondence_executions": 0,
        "summary": trace["summary"],
        "integrity_sha256": digest(authoritative_seal),
        "completion_proof_sha256": hashes["completion_proof.json"],
    }


async def verify(case: str, checkpoint: str) -> dict[str, Any]:
    """Require an externally accepted publication checkpoint for normal verification."""
    root = capture_root(case)
    address = root.relative_to(ROOT).as_posix() + "/integrity.json"
    committed = await git("show", checkpoint + ":" + address)
    result = sealed(root, committed)
    marker = json.loads((root / "execution_started.json").read_bytes())
    design = json.loads(binary(root.parents[2] / "protocol.json"))
    if (
        marker["case"] != case
        or marker["execution"] != f"case-{case}-stage-b-1"
        or marker["design"] != design
        or marker["frame"]
        != {
            k: design["parent_frame"][k]
            for k in ("repository_id", "snapshot_id", "corpus_id")
        }
    ):
        raise ValueError("Stale/foreign capture identity")
    return result
