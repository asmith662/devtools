# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- exact frozen historical measurements
"""Compare original broad reads with existing method-sized Context, without replay."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from devtools.agents.coding.projection import (
    ProjectionPolicy,
    project_request,
    request_bytes,
    source_feedback,
)
from devtools.context import RepositoryResourceAddress
from devtools.context.planning.source import (
    SourceRangeDisclosureOption,
    materialize_source_range,
)
from devtools.context.repository.corpus import (
    RepositoryTextCorpusDefinition,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import RepositoryResourceDiscovery
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.context.retrieval import build_source_search_index
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    ModelRequest,
    ModelSettings,
    ModelToolDefinition,
    Prompt,
    PromptMessage,
)
from devtools.models.interaction.providers.llama_cpp_request_settings import (
    LlamaCppRequestSettings,
)


def test_frozen_method_contract_working_set_fits_without_replaying_operations() -> None:
    root = Path(__file__).resolve().parents[3]
    case = root / "experiments/local_maintenance_task_navigation"
    frozen = json.loads((case / "freeze.json").read_text(encoding="utf-8"))
    raw = frozen["source_snapshot"]
    resources = tuple(
        RepositoryResourceOccurrence(
            RepositoryResourceAddress(r["address"]["value"]),
            ContentIdentity(r["content_identity"]["value"]),
            r["content"],
            r["encoding"],
            r["byte_size"],
        )
        for r in raw["resources"]
    )
    assert all(
        ContentIdentity.from_text(r.content) == r.content_identity for r in resources
    )
    snapshot = RepositorySnapshot(
        RepositorySnapshotId(raw["id"]["value"]),
        RepositoryId.parse(frozen["repository_id"]),
        resources,
    )
    addresses = tuple(r.address for r in resources)
    definition = RepositoryTextCorpusDefinition(
        RepositoryResourceDiscovery(
            snapshot.repository_id,
            resolve_path(root),
            32,
            256,
            len(addresses),
            addresses,
            addresses,
        ),
        addresses,
    )
    index = build_source_search_index(
        snapshot,
        corpus=realize_repository_text_corpus(definition=definition, snapshot=snapshot),
    )
    retained = json.loads((case / "evidence/result.json").read_text(encoding="utf-8"))
    initial = retained["requests"][0]["request"]
    request = ModelRequest(
        Prompt(
            "",
            "messages",
            tuple(
                PromptMessage(**{**m, "tool_calls": ()})
                for m in initial["prompt"]["messages"]
            ),
        ),
        settings=ModelSettings(**initial["settings"]),
        tools=tuple(ModelToolDefinition(**t) for t in initial["tools"]),
        provider_settings=LlamaCppRequestSettings(
            **{
                k: v for k, v in initial["provider_settings"].items() if k != "provider"
            },
        ),
    )
    names = {
        "RepositoryCodingHost.__init__",
        "RepositoryCodingHost.build_request",
        "RepositoryCodingHost.prepare",
        "RepositoryCodingHost.apply",
        "SourceScope",
        "assert_metadata",
        "test_inventory_charged_to_prompt_budget",
    }
    units = [u for u in index.views[1].units if u.qualified_name in names]
    assert len(units) == 7
    assert sum(len(u.text.encode()) for u in units) == 15141
    messages = list(request.prompt.messages)
    bindings = {}
    for unit in units:
        option = SourceRangeDisclosureOption(
            "Public implementation contracts",
            unit,
            unit.start,
            unit.end,
            8192,
        )
        disclosed = materialize_source_range(snapshot, option).items[0]
        assert not option.truncated
        bindings[len(messages)] = (option,)
        messages.append(
            PromptMessage(
                "user",
                json.dumps(source_feedback(option, disclosed.text), ensure_ascii=False),
            ),
        )
    assembled = replace(request, prompt=Prompt("", "messages", tuple(messages)))
    assert request_bytes(assembled) == 29748
    assert retained["projections"][3]["original_bytes"] == 40312
    outcome = project_request(
        assembled,
        policy=ProjectionPolicy(24576, 20000, report_source_state=True),
        hard_bytes=32768,
        snapshot=snapshot,
        sources=bindings,
    )
    assert outcome.resulting_bytes <= 32768
    assert outcome.omitted_exchanges == ()
    assert len(outcome.active_sources) == 7
    assert outcome.request.prompt.messages[:-1] == tuple(messages)
    assert all(not m.tool_calls and m.tool_call_id is None for m in messages)
    assert messages[:2] == list(request.prompt.messages)
    # This is explicit host disclosure, not claimed autonomous discovery or inference.
