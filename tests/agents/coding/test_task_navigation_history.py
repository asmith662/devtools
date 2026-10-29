# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- immutable-input independent coordinates and sizes
"""Reconstruct navigation candidates without inference, acquisition or effects."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import cast

from devtools.agents.coding.navigation import (
    TASK_FIND,
    NavigationPolicy,
    task_entry,
    unit_read_request,
)
from devtools.agents.coding.projection import request_bytes
from devtools.agents.model_tools import normalize_tool_descriptor
from devtools.context import RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
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
from devtools.tools.source import select_source_read

CASE = Path(__file__).resolve().parents[3] / "experiments/local_maintenance_navigation"


def frozen_comparison() -> dict[str, object]:
    frozen = json.loads((CASE / "freeze.json").read_text(encoding="utf-8"))
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
    # Rehydrate only the retained explicit address observation, not live source.
    discovery = RepositoryResourceDiscovery(
        snapshot.repository_id,
        resolve_path(CASE.parents[1]),
        32,
        256,
        len(addresses),
        addresses,
        addresses,
    )
    definition = RepositoryTextCorpusDefinition(discovery, addresses)
    index = build_source_search_index(
        snapshot,
        corpus=realize_repository_text_corpus(
            definition=definition,
            snapshot=snapshot,
        ),
    )
    view = task_entry(index, frozen["objective"], NavigationPolicy())
    candidate = next(
        u
        for u in cast("list[dict[str, str]]", view["units"])
        if u["path"] == "src/devtools/agents/coding/repository.py"
        and u["name"] == "RepositoryCodingHost"
    )
    read = unit_read_request(
        index,
        {"unit_id": candidate["unit_id"], "snapshot_id": view["snapshot_id"]},
        purpose=frozen["objective"],
        maximum_bytes=8192,
    )
    option = select_source_read(read)
    assert isinstance(option, SourceRangeDisclosureOption)
    # The selectable exact prefix includes the known request-assembly method.
    assert "def build_request(" in option.text
    assert option.start <= 11495
    assert option.span[1] >= 12239
    assert "resources" not in view
    raw_request = json.loads((CASE / "evidence/request-1.json").read_text())["request"]
    request = ModelRequest(
        Prompt("", "messages", (PromptMessage("user", frozen["objective"]),)),
        settings=ModelSettings(**raw_request["settings"]),
        tools=tuple(ModelToolDefinition(**t) for t in raw_request["tools"]),
        provider_settings=LlamaCppRequestSettings(
            **{
                k: v
                for k, v in raw_request["provider_settings"].items()
                if k != "provider"
            },
        ),
    )
    assert request_bytes(request) == 5224
    request = replace(
        request,
        tools=tuple(
            normalize_tool_descriptor(TASK_FIND) if t.name == "find_source" else t
            for t in request.tools
        ),
        prompt=Prompt(
            "",
            "messages",
            (
                *request.prompt.messages,
                PromptMessage("user", json.dumps(view, ensure_ascii=False)),
            ),
        ),
    )
    assert request_bytes(request) < 32768
    return {
        "freeze_sha256": hashlib.sha256(
            (CASE / "freeze.json").read_bytes(),
        ).hexdigest(),
        "initial": view,
        "baseline_request_bytes": 5224,
        "new_request_bytes": request_bytes(request),
        "source_selectable_span": option.span,
        "exact_source_bytes": len(option.text.encode()),
        "metadata_pages_before_source": 0,
        "source_disclosure_actions": 1,
        "qualification": (
            "Effect-free reconstruction. Selectable source is not evidence the "
            "acting model will choose it. No original effect or request replayed."
        ),
    }


def test_frozen_entry_exposes_host_source_before_global_paging() -> None:
    result = frozen_comparison()
    assert result["metadata_pages_before_source"] == 0
