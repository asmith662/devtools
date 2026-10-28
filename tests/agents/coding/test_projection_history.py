# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independently frozen literal expectations
"""Read-only Case 0003 reconstruction, not a model continuation or experiment rerun."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from devtools.agents.coding.projection import ProjectionPolicy, project_request
from devtools.context import RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.document import (
    RepositoryTextDocument,
    RepositoryTextDocumentId,
    _semantic_digest,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.context.retrieval.source.representation import file_unit
from devtools.models.interaction import ModelToolDefinition, Prompt
from devtools.resources.commands import CommandExecutor
from devtools.tools import ToolRunner
from tests.agents.coding.test_projection import frozen_request

CASE = (
    Path(__file__).resolve().parents[3] / "experiments/local_coding_dogfood/case_0003"
)


def frozen_sources() -> tuple[
    RepositorySnapshot,
    dict[int, tuple[SourceRangeDisclosureOption, ...]],
]:
    """Use original snapshot and canonical source representation, with no live reads."""
    freeze = json.loads((CASE / "freeze.json").read_text(encoding="utf-8"))
    snapshot = RepositorySnapshot(
        RepositorySnapshotId(freeze["snapshot_id"]),
        RepositoryId.parse(freeze["repository_id"]),
        tuple(
            RepositoryResourceOccurrence(
                RepositoryResourceAddress(r["address"]["value"]),
                ContentIdentity(r["content_identity"]["value"]),
                r["content"],
                r["encoding"],
                r["byte_size"],
            )
            for r in freeze["source_snapshot"]["resources"]
        ),
    )
    request = frozen_request()
    calls = {
        c.provider_call_id: c for m in request.prompt.messages for c in m.tool_calls
    }
    sources: dict[int, tuple[SourceRangeDisclosureOption, ...]] = {}
    for index, message in enumerate(request.prompt.messages):
        if message.role != "tool":
            continue
        value = json.loads(message.content)
        if "text" not in value:
            continue
        resource = snapshot.resource_at(RepositoryResourceAddress(value["path"]))
        assert ContentIdentity.from_text(resource.content) == resource.content_identity
        document = RepositoryTextDocument(
            RepositoryTextDocumentId(
                _semantic_digest(
                    RepositoryTextDocument.REPRESENTATION_SEMANTICS,
                    str(snapshot.repository_id),
                    str(resource.address),
                    str(resource.content_identity),
                ),
            ),
            snapshot.repository_id,
            resource,
        )
        arguments = json.loads(calls[message.tool_call_id].arguments_json)
        option = SourceRangeDisclosureOption(
            request.prompt.messages[0].content,
            file_unit(snapshot, document),
            arguments["start"],
            arguments["end"],
            8192,
        )
        assert option.text == value["text"]
        assert list(option.span) == value["span"]
        sources[index] = (option,)
    return snapshot, sources


def test_case0003_exact_reduction_preserves_all_disjoint_source_and_originals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        pytest.fail("Projection attempted a Tool or Command effect")

    monkeypatch.setattr(ToolRunner, "execute", forbidden)
    monkeypatch.setattr(CommandExecutor, "execute", forbidden)
    before = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (CASE / "freeze.json", CASE / "evidence/worker-result.json")
    }
    request = frozen_request()
    original = asdict(request)
    snapshot, sources = frozen_sources()
    result = project_request(
        request,
        policy=ProjectionPolicy(
            28672,
            24576,
            frozenset({"list_repository", "search_source"}),
        ),
        hard_bytes=32768,
        snapshot=snapshot,
        sources=sources,
    )
    assert result.original_bytes == 36640
    # Literal removal: listing exchange 3,821 bytes; two-search exchange 8,749.
    assert result.resulting_bytes == 24070
    assert result.omitted_exchanges == (
        (1, 3, "host-classified-metadata"),
        (3, 6, "host-classified-metadata"),
    )
    assert result.selected_indices == (0, 6, 7, 8, 9, 10, 11)
    assert result.request.prompt.messages == (
        request.prompt.messages[0],
        *request.prompt.messages[6:],
    )
    assert result.status == "reduced"
    assert result.target_reached
    assert result.shortened_indices == ()
    assert result.invalidated_source_identities == ()
    assert result.active_sources == tuple(
        o for values in sources.values() for o in values
    )
    assert [o.span for o in result.active_sources] == [
        (1, 6754),
        (10250, 11200),
        (1, 8193),
    ]
    assert Prompt("", "messages", result.request.prompt.messages)
    assert asdict(request) == original
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in before} == before


def test_complete_experimental_schemas_are_accounted_before_projection() -> None:
    retained = json.loads(
        (CASE / "evidence/worker-result.json").read_text(encoding="utf-8"),
    )
    # The original base-host guard preceded extra schema assembly. Exercise all
    # six retained host-selected definitions as a separately qualified input.
    request = replace(
        frozen_request(),
        tools=tuple(
            ModelToolDefinition(**t)
            for t in retained["requests"][-1]["request"]["tools"]
        ),
    )
    snapshot, sources = frozen_sources()
    result = project_request(
        request,
        policy=ProjectionPolicy(
            28672,
            24576,
            frozenset({"list_repository", "search_source"}),
        ),
        hard_bytes=32768,
        snapshot=snapshot,
        sources=sources,
    )
    assert len(result.request.tools) == 6
    assert result.request.tools == request.tools
    assert result.original_bytes == 37468
    assert result.resulting_bytes == 24898
    assert not result.target_reached
    assert len(result.active_sources) == 3
