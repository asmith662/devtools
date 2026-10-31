# Copyright (c) 2026
# ruff: noqa: D103 -- literal independent lifecycle expectations
"""Complete metadata is current host Context, never exact editing evidence."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.navigation import NavigationPolicy, complete_inventory
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionPolicy,
    request_bytes,
)
from devtools.context import RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.models.interaction import InteractionSource, ModelRequest, ModelResponse
from devtools.resources.filesystem import TextFile, write
from devtools.tools.errors import ToolInputError
from tests.agents.coding.test_navigation import navigation_host
from tests.agents.coding.test_repository import LIMITS, call

if TYPE_CHECKING:
    from pathlib import Path


def inventory(request: ModelRequest) -> dict[str, Any]:
    rows = []
    for message in request.prompt.messages:
        try:
            value = json.loads(message.content)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("complete_inventory") is True:
            rows.append(value)
    assert len(rows) == 1
    assert request.prompt.messages[1].content == json.dumps(rows[0], ensure_ascii=False)
    return rows[0]


@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("candidates", [False, True])
def test_complete_scope_order_privacy_and_idempotence(
    tmp_path: Path,
    *,
    empty: bool,
    candidates: bool,
) -> None:
    host = navigation_host(
        tmp_path,
        {} if empty else {"data with spaces.txt": "\u03c0\r\n", "empty.txt": ""},
    )
    write(TextFile(resolve_path(tmp_path / "unauthorized.txt"), "private-outside"))
    host.objective = replace(host.objective, editable=host.objective.editable[:1])
    host.navigation_policy = NavigationPolicy() if candidates else None
    state = CodingProgress(LIMITS)
    first = asyncio.run(host.prepare(state))
    data = inventory(first)
    assert first.prompt.messages[0].content == host.objective.text
    assert data["repository_id"] == str(host.scope.snapshot.repository_id)
    assert data["snapshot_id"] == str(host.scope.snapshot.id)
    assert data["source_acquired"] is False
    assert [r["address"] for r in data["resources"]] == sorted(
        r.address.value for r in host.scope.snapshot.resources
    )
    for resource, row in zip(
        host.scope.snapshot.resources,
        data["resources"],
        strict=True,
    ):
        assert row["content_identity"] == str(resource.content_identity)
        assert row["byte_size"] == len(resource.content.encode())
        assert row["editable"] is (resource.address in host.objective.editable)
    assert "private-outside" not in str(first)
    assert "unauthorized.txt" not in str(first)
    assert str(tmp_path) not in str(first)
    assert not host.disclosures
    assert not host.active_disclosures
    assert asyncio.run(host.prepare(state)) == first
    if candidates:
        assert (
            json.loads(first.prompt.messages[2].content)["complete_inventory"] is False
        )


@pytest.mark.parametrize("maximum", [0, -1, True])
def test_representation_rejects_invalid_bound(tmp_path: Path, maximum: int) -> None:
    host = navigation_host(tmp_path, {"data.txt": ""})
    with pytest.raises(ValueError, match="positive integer"):
        complete_inventory(host.scope, (), maximum)


def test_foreign_editability_and_stale_scope_are_refused(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"data.txt": "original"})
    with pytest.raises(ValueError, match="outside the authorized scope"):
        complete_inventory(
            host.scope,
            (RepositoryResourceAddress("foreign.txt"),),
            32768,
        )
    write(TextFile(resolve_path(tmp_path / "data.txt"), "changed"))
    with pytest.raises(ToolInputError, match="no longer current"):
        asyncio.run(host.prepare(CodingProgress(LIMITS)))
    assert not host.requests


def test_mandatory_inventory_and_complete_request_overflow(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"data.txt": "\u00e9"})
    state = CodingProgress(LIMITS)
    first = asyncio.run(host.prepare(state))
    old = tuple(host.messages)
    hard = request_bytes(first) - 1
    host.objective = replace(host.objective, prompt_bytes=hard)
    host.projection = ProjectionPolicy(hard, hard)
    with pytest.raises(ProjectionCapacityError) as caught:
        asyncio.run(host.prepare(state))
    assert inventory(caught.value.outcome.request) == inventory(first)
    assert tuple(host.messages) == old
    assert len(host.requests) == 1
    host.objective = replace(host.objective, prompt_bytes=1)
    with pytest.raises(ValueError, match="budget"):
        asyncio.run(host.prepare(state))


def test_inventory_does_not_authorize_unread_source(tmp_path: Path) -> None:
    host = navigation_host(tmp_path, {"module.py": "def answer(): return 6"})
    asyncio.run(host.prepare(CodingProgress(LIMITS)))
    edit = ModelResponse(
        "",
        InteractionSource("inventory-negative"),
        tool_calls=(
            call(
                "replace_source",
                {"path": "module.py", "old_text": "return 6", "new_text": "return 7"},
                "unread",
            ),
        ),
    )
    assert asyncio.run(host.propose(edit)) is None
    assert not host.disclosures
    assert not host.source_results
    assert "return 6" in (tmp_path / "module.py").read_text()
