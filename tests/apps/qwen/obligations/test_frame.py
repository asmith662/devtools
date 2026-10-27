# Copyright (c) 2026

"""Reject foreign, unsupported and over-bound host declarations before entry."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen.obligations import ObligationFrame
from devtools.core.paths import resolve_path
from tests.apps.qwen.obligations.test_native import (
    EDIT,
    Scripted,
    frame,
    member,
    obligation,
    read,
    run,
)
from tests.apps.qwen.test_coding_loop import _TINY_SOURCE, _tiny_task

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("field", ["task", "scope", "prepared"])
def test_foreign_frame_refuses_before_model_entry(tmp_path: Path, field: str) -> None:
    """Keep task/scope authorization independent from witness support."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=True))
    selected = frame(task, [obligation("owner", [member()])])
    if field == "task":
        selected = replace(selected, task_definition_sha256="0" * 64)
    elif field == "prepared":
        task = replace(task, context_mode="prepared", path_edits=False)
    else:
        v = selected.to_dict()
        v["obligations"][0]["alternatives"][0]["members"][0]["path"] = "docs/outside.py"
        selected = ObligationFrame.from_dict(v)
    model = Scripted([read(), EDIT])
    with pytest.raises(ValueError, match=r"exact native|authorized existing"):
        run(root, task, model, selected)
    assert not model.requests
    assert not (root / ".local/run").exists()


def malformed(case: str) -> dict[str, Any]:
    """Specify literal invalid declarations independently of validation helpers."""
    value: dict[str, Any] = {
        "schema": "qwen-obligation-frame-v1",
        "task_definition_sha256": "a" * 64,
        "caller": "fixture host",
        "obligations": [obligation("owner", [member()])],
    }
    spec = value["obligations"][0]
    witness = spec["alternatives"][0]["members"][0]
    changes = {
        "boolean-start": (witness, "start", True),
        "reversed-range": (witness, "end", 0),
        "unknown-decision": (witness, "decision", "model-approved"),
        "foreign-version": (witness, "version", "invalid"),
        "unknown-requirement": (spec, "requirement", "model-optional"),
        "empty-query": (spec, "query", " "),
        "empty-caller": (value, "caller", " "),
        "unknown-schema": (value, "schema", "v0"),
    }
    if case in changes:
        target, key, change = changes[case]
        target[key] = change
    elif case == "duplicate-obligation":
        value["obligations"] *= 2
    elif case == "duplicate-member":
        spec["alternatives"][0]["members"] *= 2
    elif case == "duplicate-alternative":
        spec["alternatives"] *= 2
    elif case == "empty-witness-set":
        spec["alternatives"][0]["members"] = []
    elif case == "over-bound":
        value["obligations"] *= 9
    elif case == "conditional-policy":
        spec["applicability_condition"] = "model decides"
    else:
        value["approved_by_model"] = True
    return value


@pytest.mark.parametrize(
    "case",
    [
        "boolean-start",
        "reversed-range",
        "unknown-decision",
        "foreign-version",
        "unknown-requirement",
        "empty-query",
        "empty-caller",
        "unknown-schema",
        "duplicate-obligation",
        "duplicate-member",
        "duplicate-alternative",
        "empty-witness-set",
        "over-bound",
        "conditional-policy",
        "extra-field",
    ],
)
def test_invalid_frame_is_controlled_and_has_no_execution_authority(case: str) -> None:
    """Reject invalid declarations without any model or filesystem side effect."""
    with pytest.raises((ValueError, TypeError)):
        ObligationFrame.from_dict(malformed(case))


@pytest.mark.parametrize(
    "raw",
    ['{"schema":"one","schema":"two"}', '{"priv\\u0061te":1,"private":2}', "{", "[]"],
)
def test_frame_json_uses_bounded_resource_decoding_and_unique_members(
    tmp_path: Path,
    raw: str,
) -> None:
    """Decoded duplicate keys and malformed structures cannot change the frame."""
    path = tmp_path / "host.json"
    path.write_text(raw, encoding="utf-8")
    with pytest.raises((ValueError, TypeError)):
        ObligationFrame.load(path)


def test_frame_load_roundtrip_and_no_implicit_task_schema_change(
    tmp_path: Path,
) -> None:
    """Persist the exact opt-in host specification, leaving task identity intact."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=True))
    selected = frame(task, [obligation("owner", [member()])])
    path = tmp_path / "host.json"
    path.write_text(json.dumps(selected.to_dict()), encoding="utf-8")
    loaded = ObligationFrame.load(path)
    assert loaded == selected
    assert loaded.sha256 == selected.sha256
    assert (
        loaded.to_dict()["obligations"][0]["alternatives"][0]["members"][0]["path"]
        == _TINY_SOURCE
    )
    loaded.validate(task)
