# Copyright (c) 2026
"""Trusted packaged entry for one host-granted operation, never model code."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from devtools.core.paths import resolve_path
from devtools.learning.integrations.local._codec import array, decode_references
from devtools.learning.integrations.local._codec import nonempty_text as text
from devtools.learning.integrations.local._codec import retained_object as obj
from devtools.learning.integrations.local.operations import execute_plan
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.plans import LearningPlan, canonical
from devtools.resources.filesystem import BinaryFile, FileFormat, read

MAX_PACKET_BYTES = 16 << 20


def main() -> None:
    """Read only the caller-owned packet and emit a bounded publication reference."""
    source = read(
        resolve_path(Path.cwd() / "request.json"),
        file_format=FileFormat.BINARY,
        max_bytes=MAX_PACKET_BYTES,
    )
    if not isinstance(source, BinaryFile):
        msg = "binary learning packet required"
        raise TypeError(msg)
    packet = obj(json.loads(source.content))
    if set(packet) != {"plan", "grant"}:
        msg = "unsupported learning packet"
        raise ValueError(msg)
    p = obj(packet["plan"])
    if set(p) != set(LearningPlan.__dataclass_fields__):
        msg = "unsupported plan schema"
        raise ValueError(msg)
    plan = LearningPlan(**{name: text(value) for name, value in p.items()})
    g = obj(packet["grant"])
    if set(g) != {"plan_identity", "candidate_ids", "authority"}:
        msg = "unsupported grant schema"
        raise ValueError(msg)
    grant = ExecutionAuthorization(
        text(g["plan_identity"]),
        tuple(text(v) for v in array(g["candidate_ids"])),
        decode_references([g["authority"]])[0],
    )
    owned = Path.cwd()

    def guard(event: str, arguments: tuple[object, ...]) -> None:
        if event in {"socket.connect", "socket.bind", "subprocess.Popen", "os.system"}:
            msg = "learning worker has no network/child-process capability"
            raise PermissionError(
                msg,
            )
        if event == "open" and isinstance(arguments[0], (str, bytes)):
            name = os.fsdecode(arguments[0])
            flags = arguments[2]
            if isinstance(flags, int) and flags & (
                os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
            ):
                if not resolve_path(
                    Path(name),
                    base_directory=owned,
                ).value.is_relative_to(owned):
                    msg = "learning worker write is outside its owned operation root"
                    raise PermissionError(
                        msg,
                    )

    sys.addaudithook(guard)
    result = execute_plan(plan, grant, owned / "science")
    sys.stdout.write(
        canonical(
            {
                "generation_id": result.generation_id,
                "manifest_sha256": result.manifest_sha256,
                "plan_identity": result.plan_identity,
            },
        )
        + "\n",
    )


if __name__ == "__main__":
    main()
