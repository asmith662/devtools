# Copyright (c) 2026
"""Packet refusal and the actual worker audit callback, without global hook mutation."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from typing import TYPE_CHECKING, cast
from uuid import uuid4

import pytest

from devtools.core.paths import resolve_path
from devtools.learning.integrations.local import worker
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.integrations.local.operations import LearningPublication
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.resources.filesystem import FileFormat, read
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


@pytest.mark.parametrize("fault", ["binary", "packet", "plan", "grant"])
def test_bad_packet_refuses_before_any_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """The maintained decoder cannot pass an unsupported packet to fitting."""
    data = _packet()
    if fault == "packet":
        data["extra"] = True
    elif fault in {"plan", "grant"}:
        cast("dict[str, object]", data[fault])["extra"] = True
    packet = tmp_path / "request.json"
    packet.write_text(json.dumps(data), encoding="utf-8")
    if fault == "binary":
        text = read(resolve_path(packet), file_format=FileFormat.TEXT)
        monkeypatch.setattr(worker, "read", lambda *_args, **_kwargs: text)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(worker, "execute_plan", lambda *_: pytest.fail("fit attempted"))
    with pytest.raises((ValueError, TypeError)):
        worker.main()


def test_actual_worker_audit_callback_denies_capabilities_and_foreign_writes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invoke the installed callback directly because CPython suppresses hook tracing.

    This unit control captures registration instead of adding a permanent global
    audit hook to pytest. Real contained execution is qualified separately.
    """
    (tmp_path / "request.json").write_text(json.dumps(_packet()), encoding="utf-8")
    hooks: list[Callable[[str, tuple[object, ...]], None]] = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "addaudithook", hooks.append)
    reference = LearningPublication(
        resolve_path(tmp_path),
        str(uuid4()),
        "0" * 64,
        "unit",
    )
    monkeypatch.setattr(worker, "execute_plan", lambda *_: reference)
    worker.main()
    assert len(hooks) == 1
    guard = hooks[0]
    for event in ("socket.connect", "socket.bind", "subprocess.Popen", "os.system"):
        with pytest.raises(PermissionError, match="no network/child"):
            guard(event, ())
    with pytest.raises(PermissionError, match="outside its owned"):
        guard("open", (str(tmp_path.parent / "foreign"), "w", os.O_CREAT))
    guard("open", (os.fsencode(tmp_path / "owned"), "w", os.O_CREAT))
    guard("open", (str(tmp_path.parent / "readonly"), "r", os.O_RDONLY))
    guard("open", (3, None, os.O_WRONLY))
    guard("unrelated", ())


def _packet() -> dict[str, object]:
    plan = authored_task("regression").plan("mean", "online", "packet-control")
    grant = ExecutionAuthorization(
        plan.identity,
        (plan.method,),
        EvidenceReference("learning_execution_grant-v1", "unit", plan.identity),
    )
    return {"plan": plan.document(), "grant": document(asdict(grant))}
