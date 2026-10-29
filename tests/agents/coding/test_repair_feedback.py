# Copyright (c) 2026
"""A rejected overlapping batch is atomic; later action needs a new proposal."""

# ruff: noqa: D103, PLR2004 -- independent literal native/effect expectations
from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.models.interaction import ModelRequest, ModelResponse
from tests.agents.coding.fixtures import GOOD, SOURCE
from tests.agents.coding.test_repository import (
    EDIT,
    LIMITS,
    READ,
    Script,
    call,
    host_at,
)

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.agents.coding.repository import SourceChange
    from devtools.context import RepositoryResourceAddress


@pytest.mark.parametrize("proposals", [1, 2])
def test_overlap_refusal_and_separate_correction(
    tmp_path: Path,
    proposals: int,
) -> None:
    host = host_at(tmp_path)
    nested = call(
        "replace_source",
        {"path": "module.py", "old_text": "6", "new_text": "8"},
        "nested",
    )
    effects: list[str] = []
    original_effect = host.effect

    async def effect(changes: tuple[SourceChange, ...]) -> None:
        effects.append("application")
        await original_effect(changes)

    class CheckingScript(Script):
        async def send(self, request: object) -> ModelResponse:
            assert isinstance(request, ModelRequest)
            if self.entries == 2:
                assert effects == []
                assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE
                feedback = request.prompt.messages[-2:]
                assert [m.tool_call_id for m in feedback] == ["edit", "nested"]
                assert all(
                    json.loads(m.content)
                    == {"status": "REFUSED", "reason": "Edit anchors overlap."}
                    for m in feedback
                )
            return await super().send(request)

    host.effect = effect
    archived: dict[RepositoryResourceAddress, str | None] = {}
    host.archive = archived.update
    model = CheckingScript(
        [(READ,), (EDIT, nested), (replace(EDIT, provider_call_id="new-correction"),)],
    )
    result = asyncio.run(
        run_coding_agent(model, limits=replace(LIMITS, proposals=proposals), host=host),
    )
    assert result.custody.restored
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE
    assert host.responses[1].tool_calls == (EDIT, nested)
    if proposals == 1:
        assert result.disposition == "proposal_limit"
        assert not result.accepted
        assert effects == []
        assert model.entries == 2
    else:
        assert result.accepted
        assert model.entries == 3
        assert effects == ["application"]
        assert tuple(archived.values()) == (GOOD,)
        assert result.progress.proposals == 2
