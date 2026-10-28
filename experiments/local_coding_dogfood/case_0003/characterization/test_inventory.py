# Copyright (c) 2026
# ruff: noqa: D103 -- independently specified first-request metadata contract
"""A neutral host exposes scoped metadata without acquiring source or authority."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.agents.coding.models import CodingLimits, CodingProgress
from devtools.agents.coding.repository import (
    CodingObjective,
    EditLimits,
    RepositoryCodingHost,
)
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command
from devtools.resources.filesystem import TextFile, write
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.errors import ToolInputError
from devtools.tools.source import SourceScope

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.models.interaction import ModelToolCall


def make_host(root: Path, *, prompt_bytes: int = 32768) -> RepositoryCodingHost:
    files = {
        "package/source.py": "# private-source-marker\nvalue = 'é'\n",
        "README.md": "read-only-secret\n",
    }
    for name, content in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        write(TextFile(resolve_path(root / name), content))
    write(TextFile(resolve_path(root / "outside.py"), "outside-private-marker"))
    repo = Repository.new()
    addresses = tuple(RepositoryResourceAddress(n) for n in files)
    scope = SourceScope.observe(
        root=resolve_path(root),
        repository=repo,
        addresses=addresses,
    )
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=repo,
            root=scope.root,
            requested_addresses=addresses,
            maximum_resource_count=4,
            maximum_traversal_entry_count=32,
        ),
        selected_addresses=addresses,
    )
    objective = CodingObjective(
        "Inspect the authorized project before proposing work.",
        scope,
        addresses[:1],
        FixedCheckPlan(
            scope.root,
            (
                FixedCheck(
                    "never-entered",
                    Command(sys.executable)
                    .args("-I", "-c", "pass")
                    .cwd(scope.root)
                    .with_timeout(Duration.seconds(5)),
                ),
            ),
            scope,
        ),
        EditLimits(4096, 32768, 8192, 2),
        8192,
        prompt_bytes,
    )

    async def authorize(_call: ModelToolCall, _value: object) -> None:
        return

    async def effect(_changes: object) -> None:
        pytest.fail("Metadata preparation must not execute an edit")

    return RepositoryCodingHost(
        objective,
        corpus=corpus,
        authorize=authorize,
        apply_changes=effect,
        archive=lambda _: None,
        restore=lambda _path, _text: None,
    )


def progress() -> CodingProgress:
    return CodingProgress(
        CodingLimits(2, 1, 4, Duration.seconds(5), Duration.seconds(20)),
    )


def inventory(request: Any) -> dict[str, Any]:  # noqa: ANN401 -- inspect public wire values
    entries = []
    for message in request.prompt.messages:
        try:
            value = json.loads(message.content)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and "resources" in value:
            entries.append(value)
    assert len(entries) == 1, "Exactly one scoped metadata inventory is required"
    return entries[0]


def test_first_request_scoped_inventory(tmp_path: Path) -> None:
    host = make_host(tmp_path)
    request = asyncio.run(host.prepare(progress()))
    data = inventory(request)
    assert data["repository_id"] == str(host.scope.snapshot.repository_id)
    assert data["snapshot_id"] == str(host.scope.snapshot.id)
    assert data["source_acquired"] is False
    rows = {row["address"]: row for row in data["resources"]}
    assert set(rows) == {"package/source.py", "README.md"}
    assert rows["package/source.py"]["editable"] is True
    assert rows["README.md"]["editable"] is False
    for resource in host.scope.snapshot.resources:
        row = rows[resource.address.value]
        assert row["content_identity"] == str(resource.content_identity)
        assert row["byte_size"] == len(resource.content.encode("utf-8"))
    content = "\n".join(m.content for m in request.prompt.messages)
    assert host.objective.text in content
    assert not any(
        s in content
        for s in (
            "private-source-marker",
            "read-only-secret",
            "outside.py",
            "outside-private-marker",
            str(tmp_path),
        )
    )
    assert not host.disclosures
    assert not host.custody.capture()[host.objective.editable[0]].startswith("changed")


def test_inventory_not_duplicated_on_prepare(tmp_path: Path) -> None:
    host = make_host(tmp_path)
    first = asyncio.run(host.prepare(progress()))
    second = asyncio.run(host.prepare(progress()))
    assert inventory(first) == inventory(second)
    assert [m.content for m in first.prompt.messages] == [
        m.content for m in second.prompt.messages
    ]
    assert not host.disclosures


def test_inventory_charged_to_prompt_budget(tmp_path: Path) -> None:
    host = make_host(tmp_path)
    request = asyncio.run(host.prepare(progress()))
    # A bound that fits the old objective-only request must not silently omit metadata.
    from dataclasses import asdict  # noqa: PLC0415 -- literal byte boundary

    from devtools.models.interaction import Prompt  # noqa: PLC0415

    objective_only = replace(
        request,
        prompt=Prompt("", "messages", (request.prompt.messages[0],)),
    )
    maximum = len(json.dumps(asdict(objective_only), ensure_ascii=False).encode()) + 1
    bounded = make_host(tmp_path / "bounded", prompt_bytes=maximum)
    with pytest.raises(ValueError, match="budget"):
        asyncio.run(bounded.prepare(progress()))
    assert not bounded.requests
    assert not bounded.disclosures


def test_inventory_does_not_bypass_currentness(tmp_path: Path) -> None:
    host = make_host(tmp_path)
    write(
        TextFile(resolve_path(tmp_path / "package/source.py"), "changed externally\n"),
    )
    with pytest.raises(ToolInputError, match="no longer current"):
        asyncio.run(host.prepare(progress()))
    assert not host.requests
