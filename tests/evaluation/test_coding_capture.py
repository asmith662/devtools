# Copyright (c) 2026
# ruff: noqa: D103, D105, D107, FBT003, S106 -- literal capture fault controls
"""Known coding results survive exceptions with non-copyable constructors."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding.models import CodingEffect, CodingProgress, CodingResult
from devtools.agents.coding.projection import ProjectionCapacityError, ProjectionPolicy
from experiments.joint_context import capture
from tests.agents.coding.test_projection import configured
from tests.agents.coding.test_repository import LIMITS

if TYPE_CHECKING:
    from pathlib import Path


class PrivateError(Exception):
    """Constructor requires private data; deepcopy and str must never be used."""

    def __init__(self, *, secret: object) -> None:
        self.secret = secret
        super().__init__("private")

    def __str__(self) -> str:  # noqa: PLE0307 -- pytest.fail never returns
        pytest.fail("Arbitrary exception message was exposed")

    def __deepcopy__(self, _memo: object) -> object:
        pytest.fail("Exception was copied")


def test_result_retains_known_and_unknown_effects_without_copying() -> None:
    error = PrivateError(secret=object())
    progress = CodingProgress(LIMITS)
    progress.effects.extend(
        (CodingEffect("tool", ("known",), True), CodingEffect("edit", ("unknown",))),
    )
    progress.usage.append(None)
    result = CodingResult("failed", False, False, progress, error)
    record = capture.result_record(result)
    encoded = json.dumps(record)
    assert "PrivateError" in encoded
    assert "private" not in encoded
    assert '"acknowledged": true' in encoded
    assert '"acknowledged": false' in encoded
    assert '"usage": [null]' in encoded
    assert result.error is error
    assert result.progress.effects[1].acknowledged is False


def test_capacity_result_preserves_structure_and_minimal_fallback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Inventory fits; the complete native request still cannot fit, so capture
    # the intended structured projection error rather than representation refusal.
    host = configured(tmp_path, hard=1500)
    host.projection = ProjectionPolicy(1500, 1400)
    with pytest.raises(ProjectionCapacityError) as caught:
        asyncio.run(host.prepare(host.progress))
    error = caught.value
    result = CodingResult("failed", False, False, host.progress, error)
    path = tmp_path / "result.json"
    assert capture.save_result(path, result)
    value = json.loads(path.read_text())
    assert value["error"]["projection"]["status"] == "insufficient"
    assert (
        value["error"]["projection"]["resulting_bytes"] == error.outcome.resulting_bytes
    )
    assert "request" not in value["error"]["projection"]

    def fail(_result: CodingResult) -> dict[str, object]:
        raise PrivateError(secret="never serialize")

    monkeypatch.setattr(capture, "result_record", fail)
    assert not capture.save_result(tmp_path / "broken.json", result)
    minimal = json.loads((tmp_path / "broken.capture-failed.json").read_text())
    assert minimal["coding_error_class"] == "ProjectionCapacityError"
    assert minimal["capture"] == "failed"
    assert minimal["accepted"] is False
    assert result.error is error
