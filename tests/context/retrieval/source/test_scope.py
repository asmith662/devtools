# Copyright (c) 2026
# ruff: noqa: D103 -- independently authored scoped-source contracts
"""Codex regressions for caller-selected resources, not a new retrieval policy."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.planning import SourceSearchDisclosureOption
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.identity import Repository
from devtools.context.repository.resource import RepositoryResourceAddress as Address
from devtools.context.retrieval.source import (
    build_source_search_index,
    search_repository_source,
)
from devtools.core.paths import resolve_path
from tests.context.retrieval.source.test_search import _index

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context.retrieval.source import SourceSearchIndex, SourceSearchMode


@pytest.fixture
def source_index(tmp_path: Path) -> SourceSearchIndex:
    return _index(
        tmp_path,
        {
            "selected.py": 'def selected():\n    return "needle selected"\n',
            "other.py": 'def needle():\n    return "needle needle needle needle"\n',
            "last.py": (
                'class Last:\n    async def run(self):\n        return "needle last"\n'
            ),
            "empty.py": "",
        },
    )


@pytest.mark.parametrize("mode", ["file", "symbol", "window", "mixed"])
def test_scope_precedes_final_limit_and_preserves_native_evidence(
    source_index: SourceSearchIndex,
    mode: SourceSearchMode,
) -> None:
    selected = (Address("selected.py"),)
    scoped = search_repository_source(
        source_index,
        query="needle",
        mode=mode,
        maximum_results=1,
        resource_addresses=selected,
    )
    broad = search_repository_source(
        source_index,
        query="needle",
        mode=mode,
        maximum_results=100,
    )
    assert scoped.index is source_index
    assert scoped.resource_addresses == selected
    assert len(scoped.hits) == 1
    assert scoped.hits[0].unit.resource.address == selected[0]
    assert all(
        e.unit.resource.address in selected for h in scoped.hits for e in h.evidence
    )
    expected = {
        m.document_statistics.analysis.document.id: m
        for n in broad.native_results
        for m in n.matches
    }
    for native in scoped.native_results:
        for match in native.matches:
            unit = match.document_statistics.analysis.document
            assert unit.resource.address == selected[0]
            assert match == expected[unit.id]
    item = SourceSearchDisclosureOption(
        "Inspect selected",
        scoped.hits[0].unit,
    ).materialize(snapshot=source_index.snapshot)
    assert "needle selected" in item.text
    assert "needle needle needle" not in item.text


@pytest.mark.parametrize("mode", ["file", "symbol", "window", "mixed"])
def test_none_empty_and_no_match_are_distinct(
    source_index: SourceSearchIndex,
    mode: SourceSearchMode,
) -> None:
    default = search_repository_source(source_index, query="needle", mode=mode)
    assert default == search_repository_source(
        source_index,
        query="needle",
        mode=mode,
        resource_addresses=None,
    )
    assert default.resource_addresses is None
    for scope in ((), (Address("empty.py"),)):
        result = search_repository_source(
            source_index,
            query="needle",
            mode=mode,
            resource_addresses=scope,
        )
        assert result.resource_addresses == scope
        assert not result.hits
        assert not any(n.matches for n in result.native_results)


@pytest.mark.parametrize(
    "scope",
    [
        (Address("missing.py"),),
        (Address("selected.py"), Address("selected.py")),
        ("selected.py",),
    ],
)
def test_invalid_scope_refused_even_without_query_matches(
    source_index: SourceSearchIndex,
    scope: tuple[Address, ...],
) -> None:
    with pytest.raises((ValueError, TypeError), match="selection"):
        search_repository_source(
            source_index,
            query="notpresent",
            resource_addresses=scope,
        )


def test_only_admitted_index_files_qualify(
    tmp_path: Path,
    source_index: SourceSearchIndex,
) -> None:
    snapshot = source_index.snapshot
    discovery = discover_repository_resource_addresses(
        repository=Repository(snapshot.repository_id),
        root=resolve_path(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=30,
    )
    corpus = realize_repository_text_corpus(
        definition=define_repository_text_corpus(
            discovery=discovery,
            selected_addresses=(Address("selected.py"),),
        ),
        snapshot=snapshot,
    )
    index = build_source_search_index(snapshot, corpus=corpus)
    assert snapshot.resource_at(Address("last.py"))
    with pytest.raises((ValueError, TypeError), match="selection"):
        search_repository_source(
            index,
            query="needle",
            resource_addresses=(Address("last.py"),),
        )


def test_recorded_order_and_retained_source(
    tmp_path: Path,
    source_index: SourceSearchIndex,
) -> None:
    pair = (Address("last.py"), Address("selected.py"))
    result = search_repository_source(
        source_index,
        query="needle",
        mode="mixed",
        resource_addresses=pair,
    )
    reverse = search_repository_source(
        source_index,
        query="needle",
        mode="mixed",
        resource_addresses=pair[::-1],
    )
    assert result.resource_addresses == pair
    assert result.hits == reverse.hits
    assert {h.unit.resource.address for h in result.hits} == set(pair)
    (tmp_path / "selected.py").write_text("replaced on disk", encoding="utf-8")
    after = search_repository_source(
        source_index,
        query="needle",
        mode="mixed",
        resource_addresses=pair,
    )
    assert after == result


@pytest.mark.parametrize("kwargs", [{"mode": "unknown"}, {"maximum_results": 0}])
def test_existing_invalid_search_requests_stay_invalid(
    source_index: SourceSearchIndex,
    kwargs: dict[str, object],
) -> None:
    with pytest.raises(ValueError, match=r"Unknown source|Maximum source"):
        search_repository_source(
            source_index,
            query="needle",
            resource_addresses=(),
            **kwargs,  # type: ignore[arg-type]
        )


def test_non_tuple_and_non_file_population_are_not_admission(
    source_index: SourceSearchIndex,
) -> None:
    with pytest.raises(TypeError, match="tuple"):
        search_repository_source(
            source_index,
            query="needle",
            resource_addresses=[Address("selected.py")],  # type: ignore[arg-type]
        )
    symbol = next(u for u in source_index.views[1].units if u.kind == "symbol")
    not_file = replace(
        source_index,
        views=(
            replace(source_index.views[0], units=(symbol,)),
            *source_index.views[1:],
        ),
    )
    with pytest.raises(ValueError, match="admitted file"):
        search_repository_source(
            not_file,
            query="needle",
            resource_addresses=(symbol.resource.address,),
        )
