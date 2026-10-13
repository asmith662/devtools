# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812 -- experiment proof codec boundary
"""Content-addressed completion proofs for future experiment captures.

The caller supplies an authoritative proof digest; a proof never authenticates
itself. Historical captures use separately audited, pinned compatibility paths.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.codex_dogfood.case_0012.stage_b.durability import exclusive

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

CHECKS = (
    "journal",
    "native",
    "canonical",
    "correspondence",
    "aliases_order_types",
    "frame_runtime",
    "scientific_construction",
)
SCHEMA = "experiment-completion-proof-v1"
SHA256_LENGTH = 64


@dataclass(frozen=True)
class CompletionBindings:
    """Exact input digest document, retained as immutable canonical bytes.

    This is experiment composition, not a framework identity or persistence API.
    Actual input authentication remains the capture/consumer owner's duty.
    """

    raw: bytes

    @classmethod
    def create(cls, value: dict[str, Any]) -> CompletionBindings:
        """Require explicit case/execution/frame and all scientific digest scopes."""
        required = {
            "case",
            "execution",
            "frame",
            "protocol_sha256",
            "schedule_sha256",
            "journal_chain_sha256",
            "native_sha256",
            "canonical_sha256",
            "implementation_sha256",
            "verifier_sha256",
            "completion_sha256",
        }
        if set(value) != required or set(value["frame"]) != {
            "repository_id",
            "snapshot_id",
            "corpus_id",
        }:
            raise ValueError("Incomplete completion-proof bindings")
        for key in ("case", "execution"):
            if not isinstance(value[key], str) or not value[key]:
                raise ValueError("Missing completion-proof identity")
        for key, item in value.items():
            if key.endswith("sha256"):
                hashes = item.values() if isinstance(item, dict) else (item,)
                if isinstance(item, dict) and not item:
                    raise ValueError("Empty digest scope")
                for sha in hashes:
                    if (
                        not isinstance(sha, str)
                        or len(sha) != SHA256_LENGTH
                        or any(c not in "0123456789abcdef" for c in sha)
                    ):
                        raise ValueError("Invalid completion-proof digest")
        return cls(json_bytes(value))


def checked_result(raw: bytes) -> None:
    """Require the exact deep-proof result, rather than a summary PASS flag."""
    result = json.loads(raw)
    if result != {"status": "PASS", "checks": dict.fromkeys(CHECKS, "PASS")}:
        raise ValueError("Deep proof did not establish every required check")


def publish_proof(
    path: Path, bindings: CompletionBindings, prove: Callable[[], bytes]
) -> str:
    """Execute deep proof once, then exclusively publish its content binding.

    The capture owner must hash authoritative inputs before invoking this and
    anchor the returned digest in its authoritative completion publication/commit.
    The existing completion seal is an input: no self-referential hash cycle.
    """
    if path.exists():
        raise FileExistsError("Completion proof overwrite refused")
    if CompletionBindings.create(json.loads(bindings.raw)).raw != bindings.raw:
        raise ValueError("Noncanonical completion bindings")
    result = prove()
    checked_result(result)
    value = {
        "schema": SCHEMA,
        "inputs": json.loads(bindings.raw),
        "inputs_sha256": digest(bindings.raw),
        "deep_result_b64": base64.b64encode(result).decode("ascii"),
        "deep_result_sha256": digest(result),
    }
    exclusive(path, value)
    return digest(path.read_bytes())


def authenticate_proof(
    raw: bytes, authoritative_sha256: str, bindings: CompletionBindings
) -> bytes:
    """Authenticate exact proof/input/verifier/result bindings without deep replay."""
    if digest(raw) != authoritative_sha256:
        raise ValueError(
            "Completion proof differs; explicit deep/proof migration required"
        )
    if CompletionBindings.create(json.loads(bindings.raw)).raw != bindings.raw:
        raise ValueError("Noncanonical completion bindings")
    value = json.loads(raw)
    if set(value) != {
        "schema",
        "inputs",
        "inputs_sha256",
        "deep_result_b64",
        "deep_result_sha256",
    } or (
        value["schema"] != SCHEMA
        or json_bytes(value["inputs"]) != bindings.raw
        or value["inputs_sha256"] != digest(bindings.raw)
    ):
        raise ValueError("Completion proof input/implementation binding differs")
    result = base64.b64decode(value["deep_result_b64"], validate=True)
    if digest(result) != value["deep_result_sha256"]:
        raise ValueError("Completion proof result bytes differ")
    checked_result(result)
    return result
