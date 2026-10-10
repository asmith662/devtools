# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, EM101, TRY003, S301 -- trusted own sealed native checkpoint
"""Exclusive claim and canonical atomic text envelopes around trusted pickle state."""

from __future__ import annotations

import base64
import gzip
import os
import pickle
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from experiments.codex_dogfood.case_0009.artifacts import (
    digest,
    json_bytes,
    read_json,
)


def atomic(path: Path, value: object) -> None:
    """Use the native atomic/fsynced filesystem substrate for every state update."""
    write(TextFile(resolve_path(path), json_bytes(value).decode()), overwrite=True)


class Journal:
    """Never re-enter any operation after its durable entered record exists."""

    def __init__(self, root: Path, state: dict[str, Any]) -> None:
        """Retain trusted state and a private measurement overhead counter."""
        self.root, self.state = root, state
        self.overhead_ns = 0

    @classmethod
    def start(cls, root: Path, marker: dict[str, Any]) -> Journal:
        """Claim exclusively, then atomically publish complete start/native state."""
        if any(
            (root / n).exists()
            for n in (
                "execution.claim",
                "execution_started.json",
                "raw_checkpoint.json",
                "integrity.json",
                "summary.json",
                "lexical.json",
                "STAGE_B_REVIEW.md",
                "trace.json",
            )
        ):
            raise FileExistsError("Stage B execution already claimed; no retry")
        root.mkdir(parents=True, exist_ok=True)
        # Explicit experiment boundary: native writer lacks O_EXCL claim semantics.
        with (root / "execution.claim").open("xb") as stream:
            stream.write(json_bytes({"execution": marker["execution"]}))
            stream.flush()
            os.fsync(stream.fileno())
        atomic(root / "execution_started.json", marker)
        journal = cls(
            root,
            {
                "marker": marker,
                "operations": [],
                "values": {},
                "active": [],
                "state": "STARTED",
            },
        )
        journal.save()
        return journal

    @classmethod
    def load(cls, root: Path) -> Journal:
        """Load authenticated own state, never a sterile/adjudicator-provided pickle."""
        envelope = read_json(root / "raw_checkpoint.json")
        raw = base64.b85decode(envelope["native_gzip_b85"])
        if digest(raw) != envelope["native_archive_sha256"]:
            raise ValueError("Raw native checkpoint digest differs")
        state = pickle.loads(gzip.decompress(raw))
        if state["marker"] != read_json(root / "execution_started.json"):
            raise ValueError("Raw checkpoint marker differs")
        return cls(root, state)

    def save(self) -> None:
        """Preserve the complete native object graph and physical serialization hash."""
        started = time.perf_counter_ns()
        raw = gzip.compress(
            pickle.dumps(self.state, protocol=pickle.HIGHEST_PROTOCOL), mtime=0
        )
        atomic(
            self.root / "raw_checkpoint.json",
            {
                "schema": "case-0012-durable-native-v1",
                "execution": self.state["marker"]["execution"],
                "state": self.state["state"],
                "operation_count": len(self.state["operations"]),
                "active": self.state["active"],
                "native_archive_sha256": digest(raw),
                "native_gzip_b85": base64.b85encode(raw).decode(),
            },
        )
        self.overhead_ns += time.perf_counter_ns() - started

    def call(self, identity: str, inputs: object, invoke: Callable[[], Any]) -> Any:
        """Persist entry, return and failed attempt without retrying calls."""
        if any(o["identity"] == identity for o in self.state["operations"]):
            raise ValueError("Operation already entered; no retry")
        operation = {
            "identity": identity,
            "invocations": 1,
            "inputs": inputs,
            "prior_operations": [o["identity"] for o in self.state["operations"]],
            "status": "ENTERED",
            "runtime_ns": None,
        }
        self.state["operations"].append(operation)
        self.state["active"].append(identity)
        self.save()
        started = time.perf_counter_ns()
        overhead_before = self.overhead_ns
        try:
            result = invoke()
        except BaseException as error:
            operation.update(
                status="FAILED_NO_RETURN",
                runtime_ns=time.perf_counter_ns() - started,
                error_type=type(error).__qualname__,
                error=str(error),
            )
            self.state["state"] = "FAILED; NO RETRY"
            self.save()
            raise
        elapsed = time.perf_counter_ns() - started
        overhead = self.overhead_ns - overhead_before
        operation.update(
            status="RETURNED",
            runtime_ns=elapsed - overhead,
            wall_call_ns=elapsed,
            durability_inside_call_ns=overhead,
        )
        self.state["values"][identity] = result
        self.state["active"].remove(identity)
        # Pickle physical return digest is historical; raw envelope authenticates
        # the recoverable graph. Never claim repickle-byte stability on replay.
        started = time.perf_counter_ns()
        operation["serialized_return_sha256"] = digest(
            pickle.dumps(result, protocol=pickle.HIGHEST_PROTOCOL)
        )
        self.overhead_ns += time.perf_counter_ns() - started
        self.save()
        return result

    def ready(self) -> None:
        """Allow only finalization after every entered operation returned durably."""
        if self.state["active"] or any(
            o["status"] != "RETURNED" for o in self.state["operations"]
        ):
            raise ValueError("Unrecoverable entered/failed operation; no native retry")
