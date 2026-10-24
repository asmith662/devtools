# Copyright (c) 2026
# ruff: noqa: D103, PT011 -- independently qualified exact-range contracts
"""Codex-authored progressive map/source integration regressions."""

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from devtools.context.planning import (
    RepositoryMapDisclosureOption,
    assemble_context_disclosure_model_request,
    choose_repository_map_disclosure,
    choose_repository_map_source_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
    render_context_disclosure,
)
from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
    derive_python_function_declarations,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.resource import ContentIdentity
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.retrieval.graph import (
    PythonGraphProjection,
    build_python_graph_view,
)
from devtools.context.retrieval.repository_map import build_repository_map_view
from devtools.context.retrieval.source import (
    SourceSearchIndex,
    build_source_search_index,
)
from devtools.core.paths import resolve_path
from devtools.models.interaction import ModelRequest, Prompt
from tests.context.retrieval.source.test_search import _index


def _case(
    tmp_path: Path,
    newline: str = "\n",
    *,
    final: bool = True,
) -> tuple[SourceSearchIndex, RepositoryMapDisclosureOption]:
    text = (
        '# pr\u00e9face\n@decorator("not in declaration range")\n'
        "async def caf\u00e9(\n    value: str,\n):\n"
        '    def inner(): return "nested body"\n    return value, inner\n'
        'def repeat(): return "first"\ndef repeat(): return "second"\n'
        "class Cl\u00e4ss:\n    @memo\n    async def m\u00e9thod(self,\n"
        '                        value):\n        return "s\u00e9lected", value\n'
        '    def sibling(self): return "unrelated sibling"\n'
    ).replace("\n", newline)
    if not final:
        text = text.removesuffix(newline)
    index = _index(
        tmp_path,
        {
            "one.py": text,
            "two.py": 'def repeat(): return "other resource"',
            "hidden.py": 'def secret(): return "unselected resource"\n',
        },
    )
    snapshot = index.snapshot
    functions: list[PythonFunctionDeclarationKnowledge] = []
    classes: list[PythonClassDeclarationKnowledge] = []
    methods: list[PythonMethodDeclarationKnowledge] = []
    for resource in snapshot.resources:
        functions.extend(
            derive_python_function_declarations(
                snapshot,
                resource_address=resource.address,
            ).declarations,
        )
        aggregate = derive_python_class_method_declarations(
            snapshot,
            resource_address=resource.address,
        )
        classes.extend(aggregate.classes)
        methods.extend(aggregate.methods)
    view = build_repository_map_view(
        snapshot,
        core=build_python_graph_view(
            snapshot,
            projection=PythonGraphProjection.TYPED_CORE,
            functions=tuple(functions),
            classes=tuple(classes),
            methods=tuple(methods),
        ),
    )
    symbols = tuple(
        symbol
        for symbol in view.symbols
        if symbol.node.resource_address.value != "hidden.py"
    )
    orientation = choose_repository_map_disclosure(
        purpose="Orient and inspect",
        snapshot=snapshot,
        view=view,
        symbols=symbols,
    )
    return index, orientation


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize("final", [False, True])
def test_native_ranges_and_provenance_are_exact(
    tmp_path: Path,
    newline: str,
    *,
    final: bool,
) -> None:
    index, orientation = _case(tmp_path, newline, final=final)
    snapshot = index.snapshot
    identities = []
    for symbol in orientation.symbols:
        option = choose_repository_map_source_disclosure(
            purpose=orientation.purpose,
            snapshot=snapshot,
            map_disclosure=orientation,
            symbol=symbol,
            source_index=index,
        )
        unit = option.unit
        span = symbol.declaration.support.source_range
        node = next(
            node
            for node in ast.walk(ast.parse(unit.resource.content))
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)
            == (
                span.start_line,
                span.start_column_utf8,
                span.end_line,
                span.end_column_utf8,
            )
        )
        assert unit.text == ast.get_source_segment(unit.resource.content, node)
        assert unit.text == unit.resource.content[unit.start : unit.end]
        assert unit.occurrence == symbol.declaration.support
        assert unit.declaration == symbol.declaration
        assert unit.qualified_name == symbol.qualified_name
        assert option.symbol == symbol
        assert unit.resource == snapshot.resource_at(symbol.node.resource_address)
        assert unit.kind == "symbol"
        assert unit.snapshot_id == snapshot.id
        assert unit.repository_id == snapshot.repository_id
        assert not unit.text.startswith("@")
        item = option.materialize(snapshot)
        assert item.native_provenance == (symbol, unit)
        assert item.resource_addresses == (symbol.node.resource_address,)
        assert item.content_identities == (unit.resource.content_identity,)
        assert item.representation != orientation.representation
        assert unit.text in item.text
        assert (
            choose_repository_map_source_disclosure(
                purpose=orientation.purpose,
                snapshot=snapshot,
                map_disclosure=orientation,
                symbol=symbol,
                source_index=index,
            ).identity
            == option.identity
        )
        assert (
            choose_repository_map_source_disclosure(
                purpose="Another question",
                snapshot=snapshot,
                map_disclosure=orientation,
                symbol=symbol,
                source_index=index,
            ).identity
            != option.identity
        )
        identities.append(option.identity)
    assert len(set(identities)) == len(orientation.symbols)


def test_progressive_composition_and_retained_source(tmp_path: Path) -> None:
    index, parent = _case(tmp_path)
    snapshot = index.snapshot
    symbol = next(
        item
        for item in parent.symbols
        if item.qualified_name == "Cl\u00e4ss.m\u00e9thod"
    )
    option = choose_repository_map_source_disclosure(
        purpose=parent.purpose,
        snapshot=snapshot,
        map_disclosure=parent,
        symbol=symbol,
        source_index=index,
    )
    plan = plan_disclosures(
        purpose=parent.purpose,
        snapshot=snapshot,
        disclosures=(parent, option),
    )
    disclosure = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    request = ModelRequest(Prompt("Original objective", "system"))
    assembled = assemble_context_disclosure_model_request(
        task_request=request,
        context=render_context_disclosure(disclosure),
    )
    assert option.unit.text in assembled.prompt.content
    assert "unrelated sibling" not in assembled.prompt.content
    assert "unselected resource" not in assembled.prompt.content
    assert "nested body" not in assembled.prompt.content
    assert request.prompt.content == "Original objective"
    assert assembled.prompt.role == "system"
    assert assembled.prompt.content.index(
        disclosure.items[0].text,
    ) < assembled.prompt.content.index(disclosure.items[1].text)
    reverse = plan_disclosures(
        purpose=parent.purpose,
        snapshot=snapshot,
        disclosures=(option, parent),
    )
    assert reverse.identity != plan.identity
    before = option.materialize(snapshot)
    (tmp_path / symbol.node.resource_address.value).write_bytes(b"later physical state")
    assert option.materialize(snapshot) == before


@pytest.mark.parametrize(
    "invalid",
    ["purpose", "unrepresented", "name", "node", "view", "index", "scope"],
)
def test_factory_rejects_invalid_map_or_scope(tmp_path: Path, invalid: str) -> None:
    index, parent = _case(tmp_path)
    snapshot = index.snapshot
    symbol = parent.symbols[0]
    purpose = parent.purpose
    if invalid == "purpose":
        purpose = " "
    elif invalid == "unrepresented":
        symbol = next(
            item for item in parent.view.symbols if item not in parent.symbols
        )
    elif invalid == "name":
        symbol = replace(symbol, qualified_name="forged")
    elif invalid == "node":
        symbol = replace(symbol, node=replace(symbol.node, identity="invented"))
    elif invalid == "view":
        parent = replace(parent, view=replace(parent.view, symbols=()))
    elif invalid == "index":
        index = replace(
            index,
            snapshot=replace(snapshot, id=RepositorySnapshotId("e" * 64)),
        )
    else:
        hidden = next(
            item
            for item in parent.view.symbols
            if item.node.resource_address.value == "hidden.py"
        )
        discovery = discover_repository_resource_addresses(
            repository=Repository(snapshot.repository_id),
            root=resolve_path(tmp_path),
            maximum_resource_count=30,
            maximum_traversal_entry_count=60,
        )
        corpus = realize_repository_text_corpus(
            definition=define_repository_text_corpus(
                discovery=discovery,
                selected_addresses=(hidden.node.resource_address,),
            ),
            snapshot=snapshot,
        )
        index = build_source_search_index(snapshot, corpus=corpus)
    with pytest.raises(ValueError):
        choose_repository_map_source_disclosure(
            purpose=purpose,
            snapshot=snapshot,
            map_disclosure=parent,
            symbol=symbol,
            source_index=index,
        )


@pytest.mark.parametrize("change", ["snapshot", "repository", "missing", "content"])
def test_stale_factory_and_materialization_rejected(
    tmp_path: Path,
    change: str,
) -> None:
    index, parent = _case(tmp_path)
    snapshot = index.snapshot
    symbol = parent.symbols[0]
    option = choose_repository_map_source_disclosure(
        purpose=parent.purpose,
        snapshot=snapshot,
        map_disclosure=parent,
        symbol=symbol,
        source_index=index,
    )
    if change == "snapshot":
        altered = replace(snapshot, id=RepositorySnapshotId("f" * 64))
    elif change == "repository":
        altered = replace(
            snapshot,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000027"),
        )
    elif change == "missing":
        altered = replace(
            snapshot,
            resources=tuple(
                item
                for item in snapshot.resources
                if item.address != symbol.node.resource_address
            ),
        )
    else:
        altered = replace(
            snapshot,
            resources=tuple(
                replace(item, content_identity=ContentIdentity("a" * 64))
                if item.address == symbol.node.resource_address
                else item
                for item in snapshot.resources
            ),
        )
    with pytest.raises(ValueError):
        choose_repository_map_source_disclosure(
            purpose=parent.purpose,
            snapshot=altered,
            map_disclosure=parent,
            symbol=symbol,
            source_index=index,
        )
    with pytest.raises(ValueError):
        option.materialize(altered)


@pytest.mark.parametrize(
    "corruption",
    ["resource", "repository", "snapshot", "kind", "start", "end"],
)
def test_forged_admitted_file_frame_refused(tmp_path: Path, corruption: str) -> None:
    index, parent = _case(tmp_path)
    snapshot = index.snapshot
    symbol = parent.symbols[0]
    files = next(view for view in index.views if view.kind == "file")
    file = next(
        unit
        for unit in files.units
        if unit.resource.address == symbol.node.resource_address
    )
    if corruption == "resource":
        altered = replace(
            file,
            resource=replace(file.resource, content_identity=ContentIdentity("b" * 64)),
        )
    elif corruption == "repository":
        altered = replace(
            file,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000027"),
        )
    elif corruption == "snapshot":
        altered = replace(file, snapshot_id=RepositorySnapshotId("b" * 64))
    elif corruption == "kind":
        altered = replace(file, kind="symbol")
    elif corruption == "start":
        altered = replace(file, start=1)
    else:
        altered = replace(file, end=file.end - 1)
    altered_files = replace(
        files,
        units=tuple(altered if unit == file else unit for unit in files.units),
    )
    changed_index = replace(
        index,
        views=tuple(altered_files if view == files else view for view in index.views),
    )
    with pytest.raises(ValueError):
        choose_repository_map_source_disclosure(
            purpose=parent.purpose,
            snapshot=snapshot,
            map_disclosure=parent,
            symbol=symbol,
            source_index=changed_index,
        )


def test_materialization_rejects_changed_cached_source_slice(tmp_path: Path) -> None:
    index, parent = _case(tmp_path)
    snapshot = index.snapshot
    symbol = parent.symbols[0]
    option = choose_repository_map_source_disclosure(
        purpose=parent.purpose,
        snapshot=snapshot,
        map_disclosure=parent,
        symbol=symbol,
        source_index=index,
    )
    altered = replace(option, unit=replace(option.unit, start=option.unit.start + 1))
    with pytest.raises(ValueError):
        altered.materialize(snapshot)
