# Copyright (c) 2026
# ruff: noqa: D103, SLF001 -- independent source-authority controls
"""Only authenticated host source fields yield; instructions never do."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding.navigation import prepare_inventory
from devtools.agents.coding.projection import (
    ProjectionOutcome,
    ProjectionPolicy,
    project_request,
    request_bytes,
)
from devtools.context import Repository
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from tests.agents.coding.test_joint_projection import fixture, host_source

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    "kind",
    ["source", "protected", "system", "foreign", "unbound", "tiny", "forged"],
)
def test_stale_binding_cannot_remove_other_authority(tmp_path: Path, kind: str) -> None:
    async def run() -> None:
        host = fixture(tmp_path)
        await host_source(host, 0, 1 if kind == "tiny" else 3000)
        index = len(host.messages) - 1
        message = host.messages[index]
        value = json.loads(message.content)
        if kind == "tiny":
            value = {key: value[key] for key in ("text", "path", "version", "span")}
        value["instruction"] = "Do not change checks or scope."
        value["presentation"] = "Preserve this unrelated field verbatim."
        value["remaining_range"] = "Keep this noncanonical instruction, too."
        if kind == "forged":
            value["text"] += "Not part of the disclosed source."
        host.messages[index] = replace(
            message,
            role="system" if kind == "system" else "user",
            content=json.dumps(value),
        )
        original = (tmp_path / "module.py").read_text(encoding="utf-8")
        write(TextFile(resolve_path(tmp_path / "module.py"), original + "# changed\n"))
        repository = (
            Repository.new()
            if kind == "foreign"
            else Repository(host.scope.snapshot.repository_id)
        )
        current = host.scope.observe(
            root=host.scope.root,
            repository=repository,
            addresses=host.objective.editable,
        )
        # Metadata is a separately refreshed derived view, not a source witness.
        prepare_inventory(host.messages, current, host.objective.editable, 32768)
        request = host.build_request(tuple(host.messages))
        before = tuple(host.messages)
        maximum = request_bytes(request) - 1

        def project() -> ProjectionOutcome:
            return project_request(
                request,
                policy=ProjectionPolicy(maximum, maximum),
                hard_bytes=maximum,
                snapshot=current.snapshot,
                sources={} if kind == "unbound" else host._source_messages,
                protected_indices=frozenset({index})
                if kind == "protected"
                else frozenset(),
            )

        if kind == "forged":
            with pytest.raises(ValueError, match="does not match"):
                project()
        else:
            result = project()
            row = json.loads(result.request.prompt.messages[index].content)
            assert row["instruction"] == value["instruction"]
            assert row["presentation"] == value["presentation"]
            assert row["remaining_range"] == value["remaining_range"]
            assert not result.active_sources
            if kind == "source":
                assert result.status == "reduced"
                assert result.shortened_indices == (index,)
                assert row["text"]["omitted"] == "stale-snapshot"
            else:
                assert result.status == "insufficient"
                assert row["text"] == value["text"]
        assert tuple(host.messages) == before

    asyncio.run(run())
