# Copyright (c) 2026
"""Independent real-observation regressions for selected function source binding."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    PythonFunctionExactNameQuery,
    PythonFunctionSourceMaterializationError,
    Repository,
    RepositoryId,
    RepositoryResourceAddress,
    analyze_python_function_declaration_resources,
    assemble_python_function_context_model_request,
    disclose_python_function_exact_name_retrieval,
    discover_repository_resource_addresses,
    materialize_python_function_disclosure_source,
    observe_repository_resources,
    render_materialized_python_function_context,
    retrieve_python_functions_by_exact_name,
)
from devtools.core.paths import resolve_path
from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.context import (
        PythonFunctionExactNameContextDisclosure,
        RepositorySnapshot,
    )


def _frame(
    tmp_path: Path,
) -> tuple[RepositorySnapshot, PythonFunctionExactNameContextDisclosure]:
    """Discover and parse three real retained files with compatible geometry."""
    files = {
        "a.py": 'def wanted(): return "A"',
        "b.py": 'def decoy_(): return "B"',
        "c.py": 'async def wanted(): return "C"',
    }
    for name, text in files.items():
        (tmp_path / name).write_bytes(text.encode())
    repository = Repository(RepositoryId.parse("00000000-0000-4000-8000-000000000041"))
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=resolve_path(tmp_path),
        maximum_resource_count=10,
        maximum_traversal_entry_count=20,
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=resolve_path(tmp_path),
        addresses=discovery.addresses,
        maximum_resource_bytes=4096,
    )
    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=tuple(
            RepositoryResourceAddress(n) for n in ("c.py", "a.py", "b.py")
        ),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("wanted"),
    )
    return snapshot, disclose_python_function_exact_name_retrieval(retrieval)


def test_valid_geometry_redirect_refuses_unchanged_selection(tmp_path: Path) -> None:
    """A valid range in another resource cannot retain the original selection."""
    snapshot, disclosure = _frame(tmp_path)
    item = disclosure.items[1]
    assert item.selected_match.knowledge.support.resource_address.value == "a.py"
    assert len(snapshot.resource_at(RepositoryResourceAddress("a.py")).content) == len(
        snapshot.resource_at(RepositoryResourceAddress("b.py")).content,
    )
    redirected = replace(
        item,
        source_occurrence=replace(
            item.source_occurrence,
            resource_address=RepositoryResourceAddress("b.py"),
        ),
    )
    altered = replace(disclosure, items=(disclosure.items[0], redirected))
    assert altered.identity == disclosure.identity
    with pytest.raises(PythonFunctionSourceMaterializationError, match="projection"):
        materialize_python_function_disclosure_source(
            disclosure=altered,
            snapshot=snapshot,
        )


@pytest.mark.parametrize("change_identity", [False, True])
def test_changed_content_under_same_snapshot_refuses(
    tmp_path: Path,
    *,
    change_identity: bool,
) -> None:
    """Both an unchanged claimed hash and a new hash must honor dependency evidence."""
    snapshot, disclosure = _frame(tmp_path)
    resource = snapshot.resource_at(RepositoryResourceAddress("a.py"))
    other = snapshot.resource_at(RepositoryResourceAddress("b.py"))
    replacement = replace(resource, content=other.content)
    if change_identity:
        replacement = replace(replacement, content_identity=other.content_identity)
    stale = replace(
        snapshot,
        resources=tuple(
            replacement if r == resource else r for r in snapshot.resources
        ),
    )
    assert stale.id == snapshot.id
    with pytest.raises(
        PythonFunctionSourceMaterializationError,
        match=r"content|dependency",
    ):
        materialize_python_function_disclosure_source(
            disclosure=disclosure,
            snapshot=stale,
        )


@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "duplicate",
        "reorder",
        "selected",
        "match",
        "name",
        "kind",
        "proposition",
        "query",
        "knowledge_name",
        "subject",
        "dependency",
        "native_redirect",
        "range",
        "repository",
    ],
)
def test_inconsistent_native_and_projected_selection_refuses(  # noqa: C901, PLR0912 -- explicit independent corruption cases
    tmp_path: Path,
    mutation: str,
) -> None:
    """Refuse named selection/projection/native corruption, not arbitrary errors."""
    snapshot, disclosure = _frame(tmp_path)
    item = disclosure.items[1]
    knowledge = item.selected_match.knowledge
    if mutation == "missing":
        disclosure = replace(disclosure, items=())
    elif mutation == "duplicate":
        disclosure = replace(disclosure, items=(item, item))
    elif mutation == "reorder":
        disclosure = replace(disclosure, items=tuple(reversed(disclosure.items)))
    elif mutation == "selected":
        disclosure = replace(disclosure, selected_matches=())
    elif mutation == "repository":
        snapshot = replace(
            snapshot,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000042"),
        )
    else:
        if mutation == "match":
            item = replace(item, selected_match=disclosure.selected_matches[0])
        elif mutation == "name":
            item = replace(item, declared_name="decoy_")
        elif mutation == "kind":
            item = replace(item, declaration_kind=disclosure.items[0].declaration_kind)
        elif mutation == "proposition":
            item = replace(item, proposition="invented")
        elif mutation == "range":
            item = replace(
                item,
                source_occurrence=replace(
                    item.source_occurrence,
                    source_range=replace(
                        item.source_occurrence.source_range,
                        start_column_utf8=1,
                    ),
                ),
            )
        else:
            if mutation == "query":
                match = replace(
                    item.selected_match,
                    query=PythonFunctionExactNameQuery("foreign"),
                )
            else:
                if mutation == "knowledge_name":
                    knowledge = replace(knowledge, declared_name="decoy_")
                elif mutation == "subject":
                    knowledge = replace(
                        knowledge,
                        subject=replace(
                            knowledge.subject,
                            snapshot_id=replace(snapshot.id, value="f" * 64),
                        ),
                    )
                elif mutation == "dependency":
                    knowledge = replace(
                        knowledge,
                        subject=replace(
                            knowledge.subject,
                            resource_dependency_identity="foreign",
                        ),
                    )
                else:
                    knowledge = replace(
                        knowledge,
                        support=replace(
                            knowledge.support,
                            resource_address=RepositoryResourceAddress("b.py"),
                        ),
                    )
                match = replace(item.selected_match, knowledge=knowledge)
            retrieval = replace(
                disclosure.retrieval,
                matches=(disclosure.retrieval.matches[0], match),
            )
            disclosure = disclose_python_function_exact_name_retrieval(retrieval)
            item = disclosure.items[1]
        disclosure = replace(disclosure, items=(disclosure.items[0], item))
    with pytest.raises(PythonFunctionSourceMaterializationError):
        materialize_python_function_disclosure_source(
            disclosure=disclosure,
            snapshot=snapshot,
        )


def test_real_selection_identity_and_order_reach_request(tmp_path: Path) -> None:
    """Retained ordered source and identity survive physical changes and assembly."""
    snapshot, disclosure = _frame(tmp_path)
    identity = disclosure.identity
    (tmp_path / "a.py").write_bytes(b"later filesystem state")
    result = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    assert result.disclosure.identity == identity
    assert [i.source_text for i in result.items] == [
        'async def wanted(): return "C"',
        'def wanted(): return "A"',
    ]
    for actual, selected in zip(result.items, disclosure.selected_matches, strict=True):
        assert actual.disclosure_item.selected_match == selected
        assert actual.disclosure_item.source_occurrence == selected.knowledge.support
        assert actual.source_snapshot_id == snapshot.id
        assert (
            actual.source_content_identity
            == snapshot.resource_at(
                selected.knowledge.support.resource_address,
            ).content_identity
        )
    request = assemble_python_function_context_model_request(
        task_request=ModelRequest(Prompt("Inspect wanted", "user")),
        context=render_materialized_python_function_context(result),
    )
    assert "def decoy_()" not in request.prompt.content
    assert request.prompt.content.index(
        "async def wanted()",
    ) < request.prompt.content.index('def wanted(): return "A"')
