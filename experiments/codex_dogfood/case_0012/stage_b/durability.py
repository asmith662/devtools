# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, EM101, TRY003, S301 -- own sealed trusted journal only
"""Immutable native returns own durability; mutable summary is reconstructable."""

from __future__ import annotations

import base64
import gzip
import io
import os
import pickle
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from devtools.resources.filesystem.errors import FilesystemPermissionError
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b.graph import describe


def atomic(path: Path, value: object) -> None:
    """Native atomic/fsynced substrate for derived replaceable summaries."""
    write(TextFile(resolve_path(path), json_bytes(value).decode()), overwrite=True)


def exclusive(path: Path, value: object) -> None:
    """Experiment O_EXCL boundary absent from native replace-based writer.

    Complete write, flush, fsync, close. Partial files block further execution.
    Parent-directory durability after sudden power loss remains OS-dependent.
    """
    with path.open("xb") as stream:
        stream.write(json_bytes(value))
        stream.flush()
        os.fsync(stream.fileno())


def pack(raw: bytes) -> dict[str, str]:
    """Explicit physical compressed-byte digest scope."""
    compressed = gzip.compress(raw, mtime=0)
    return {
        "gzip_b85": base64.b85encode(compressed).decode(),
        "sha256": digest(compressed),
    }


def unpack(value: dict[str, str]) -> bytes:
    """Authenticate bytes before own trusted native deserialization."""
    raw = base64.b85decode(value["gzip_b85"])
    if digest(raw) != value["sha256"]:
        raise ValueError("Journal native archive digest differs")
    return gzip.decompress(raw)


class Journal:
    """At most one invocation per operation per authorized execution attempt."""

    def __init__(self, root: Path, state: dict[str, Any]) -> None:
        """Keep incremental native memo local; loaded journals cannot invoke."""
        self.root, self.state = root, state
        self.overhead_ns = 0
        self.chain = digest(binary(root / "execution_started.json"))
        self.events = 0
        self.buffer = io.BytesIO()
        self.pickler: pickle.Pickler | None = pickle.Pickler(
            self.buffer, protocol=pickle.HIGHEST_PROTOCOL
        )

    @classmethod
    def start(cls, root: Path, marker: dict[str, Any]) -> Journal:
        """Exclusive claim refuses every existing attempt/capture path."""
        if root.exists() and any(root.iterdir()):
            raise FileExistsError("Stage B execution already claimed; no retry")
        root.mkdir(parents=True, exist_ok=True)
        exclusive(root / "execution.claim", {"execution": marker["execution"]})
        exclusive(root / "execution_started.json", marker)
        (root / "operations").mkdir()
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

    def context(self, values: dict[str, Any]) -> None:
        """Persist pre-operation native inputs once in the shared memo stream."""
        if self.state["operations"] or (self.root / "native_context.json").exists():
            raise ValueError("Native context already initialized")
        self.state["values"].update(values)
        exclusive(
            self.root / "native_context.json",
            {
                "native": pack(self.segment(values)),
                "canonical": pack(json_bytes(describe(values))),
                "marker_sha256": self.chain,
            },
        )
        self.chain = digest(binary(self.root / "native_context.json"))
        self.save()

    def segment(self, value: object) -> bytes:
        """Preserve original native shared identities across immutable segments."""
        if self.pickler is None:
            raise ValueError("Loaded journal cannot invoke native operations")
        self.buffer.seek(0)
        self.buffer.truncate()
        self.pickler.dump(value)
        return self.buffer.getvalue()

    def event(self, sequence: int, status: str, payload: dict[str, Any]) -> None:
        """Append a unique chained event; completion order handles nested calls."""
        self.events += 1
        value = {
            **payload,
            "execution": self.state["marker"]["execution"],
            "sequence": sequence,
            "event": self.events,
            "state": status,
            "prior_chain_sha256": self.chain,
            "frame": self.state["marker"].get("frame"),
            "runtime_identity": self.state["marker"].get("runtime"),
        }
        path = self.root / "operations" / f"{sequence:06}.{status.lower()}.json"
        exclusive(path, value)
        self.chain = digest(binary(path))

    def save(self) -> None:
        """Publish convenience metadata; it never owns a native returned value."""
        started = time.perf_counter_ns()
        atomic(
            self.root / "raw_checkpoint.json",
            {
                "schema": "case-0012-derived-journal-summary-v2",
                "execution": self.state["marker"]["execution"],
                "state": self.state["state"],
                "operations": self.state["operations"],
                "active": self.state["active"],
                "journal_events": self.events,
                "journal_chain_sha256": self.chain,
            },
        )
        self.overhead_ns += time.perf_counter_ns() - started

    @classmethod
    def load(cls, root: Path) -> Journal:  # noqa: C901, PLR0912, PLR0915 -- full journal integrity boundary
        """Reconstruct exclusively from immutable context and operation records."""
        marker = read_json(root / "execution_started.json")
        if read_json(root / "execution.claim") != {"execution": marker["execution"]}:
            raise ValueError("Execution claim differs")
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
        journal.pickler = None
        context_path = root / "native_context.json"
        records = sorted(
            ((read_json(p), p) for p in (root / "operations").glob("*.json")),
            key=lambda pair: pair[0]["event"],
        )
        stream = io.BytesIO()
        if context_path.exists():
            context = read_json(context_path)
            if context["marker_sha256"] != journal.chain:
                raise ValueError("Native context marker differs")
            stream.write(unpack(context["native"]))
            journal.chain = digest(binary(context_path))
        for value, _path in records:
            if value["state"] == "RETURNED":
                stream.write(unpack(value["native"]))
        stream.seek(0)
        loader = pickle.Unpickler(stream)
        if context_path.exists():
            values = loader.load()
            if json_bytes(describe(values)) != unpack(context["canonical"]):
                raise ValueError("Native context canonicalization differs")
            journal.state["values"].update(values)
        operations = journal.state["operations"]
        for value, path in records:
            journal.events += 1
            sequence, status = value["sequence"], value["state"]
            if (
                value["event"] != journal.events
                or value["prior_chain_sha256"] != journal.chain
                or value["execution"] != marker["execution"]
                or value["frame"] != marker.get("frame")
                or value["runtime_identity"] != marker.get("runtime")
                or path.name != f"{sequence:06}.{status.lower()}.json"
            ):
                raise ValueError("Journal chain/frame/sequence differs")
            if status == "ENTERED":
                operation = value["operation"]
                if (
                    sequence != len(operations) + 1
                    or operation["identity"] in {o["identity"] for o in operations}
                    or operation["invocations"] != 1
                    or operation["prior_operations"]
                    != [o["identity"] for o in operations]
                    or value["input_sha256"] != digest(json_bytes(operation["inputs"]))
                ):
                    raise ValueError("Operation sequence/inputs differ")
                operations.append(operation)
                journal.state["active"].append(operation["identity"])
            else:
                operation = operations[sequence - 1]
                entered = root / "operations" / f"{sequence:06}.entered.json"
                if (
                    operation["status"] != "ENTERED"
                    or value["entered_sha256"] != digest(binary(entered))
                    or value["input_sha256"] != digest(json_bytes(operation["inputs"]))
                ):
                    raise ValueError("Return/entry binding differs")
                operation.update(value["operation"])
                if status == "RETURNED":
                    identity, result = loader.load()
                    if identity != operation["identity"] or json_bytes(
                        describe(result)
                    ) != unpack(value["canonical"]):
                        raise ValueError("Canonical native return differs")
                    journal.state["values"][identity] = result
                    journal.state["active"].remove(identity)
                elif status != "FAILED_NO_RETURN":
                    raise ValueError("Unknown operation state")
            journal.chain = digest(binary(path))
        if any(o["status"] == "FAILED_NO_RETURN" for o in operations):
            journal.state["state"] = "FAILED; NO RETRY"
        completed = root / "execution_completed.json"
        if completed.exists():
            journal.ready()
            if read_json(completed) != {
                "execution": marker["execution"],
                "journal_chain_sha256": journal.chain,
                "operations": [o["identity"] for o in operations],
            }:
                raise ValueError("Execution completion seal differs")
            journal.state["state"] = "NATIVE_CAPTURE_COMPLETE"
        return journal

    def complete(self) -> None:
        """Close a complete schedule immutably, distinct from a returned prefix."""
        self.ready()
        exclusive(
            self.root / "execution_completed.json",
            {
                "execution": self.state["marker"]["execution"],
                "journal_chain_sha256": self.chain,
                "operations": [o["identity"] for o in self.state["operations"]],
            },
        )
        self.state["state"] = "NATIVE_CAPTURE_COMPLETE"
        self.save()

    def call(self, identity: str, inputs: object, invoke: Callable[[], Any]) -> Any:
        """Persist immutable return before summary publication and next operation."""
        if any(o["identity"] == identity for o in self.state["operations"]):
            raise ValueError("Operation already entered; no retry")
        if self.pickler is None:
            raise ValueError("Loaded journal cannot invoke native operations")
        if not (self.root / "native_context.json").exists():
            self.context({})
        sequence = len(self.state["operations"]) + 1
        operation = {
            "identity": identity,
            "invocations": 1,
            "inputs": inputs,
            "prior_operations": [o["identity"] for o in self.state["operations"]],
            "status": "ENTERED",
            "runtime_ns": None,
        }
        input_hash = digest(json_bytes(inputs))
        entry_started = time.perf_counter_ns()
        self.event(
            sequence, "ENTERED", {"operation": operation, "input_sha256": input_hash}
        )
        self.overhead_ns += time.perf_counter_ns() - entry_started
        self.state["operations"].append(operation)
        self.state["active"].append(identity)
        entered_hash = digest(
            binary(self.root / "operations" / f"{sequence:06}.entered.json")
        )
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
            self.event(
                sequence,
                "FAILED_NO_RETURN",
                {
                    "operation": operation,
                    "input_sha256": input_hash,
                    "entered_sha256": entered_hash,
                },
            )
            self.state["state"] = "FAILED; NO RETRY"
            raise
        elapsed = time.perf_counter_ns() - started
        overhead = self.overhead_ns - overhead_before
        operation.update(
            status="RETURNED",
            runtime_ns=elapsed - overhead,
            wall_call_ns=elapsed,
            durability_inside_call_ns=overhead,
        )
        persist_started = time.perf_counter_ns()
        canonical = json_bytes(describe(result))
        operation["serialized_return_sha256"] = digest(canonical)
        self.event(
            sequence,
            "RETURNED",
            {
                "operation": operation,
                "input_sha256": input_hash,
                "entered_sha256": entered_hash,
                "canonical": pack(canonical),
                "native": pack(self.segment((identity, result))),
            },
        )
        self.overhead_ns += time.perf_counter_ns() - persist_started
        self.state["values"][identity] = result
        self.state["active"].remove(identity)
        try:
            self.save()
        except (OSError, FilesystemPermissionError) as error:
            exclusive(
                self.root / f"summary_failure_{sequence:06}.json",
                {
                    "execution": self.state["marker"]["execution"],
                    "operation": identity,
                    "returned_chain_sha256": self.chain,
                    "error_type": type(error).__qualname__,
                    "error": str(error),
                    "native_return": "DURABLE; NO RERUN; SUMMARY DERIVED",
                },
            )
        return result

    def ready(self) -> None:
        """Reject missing returns and failures without inferring native values."""
        if self.state["active"] or any(
            o["status"] != "RETURNED" for o in self.state["operations"]
        ):
            raise ValueError("Unrecoverable entered/failed operation; no native retry")
