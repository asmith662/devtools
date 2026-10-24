# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, PT011 -- independent public-contract regressions
"""Codex-authored regressions for caller-selected repository-map Context."""

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from devtools.context.planning import (
    assemble_context_disclosure_model_request,
    choose_repository_map_disclosure,
    choose_whole_resource_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
    render_context_disclosure,
)
from devtools.context.python.classes.declarations import (
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    derive_python_function_declarations,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
)
from devtools.context.repository.snapshot import RepositorySnapshotId
from devtools.context.retrieval.graph import (
    PythonGraphProjection,
    build_python_graph_view,
)
from devtools.context.retrieval.repository_map import (
    RepositoryMapSymbol,
    build_repository_map_view,
)
from devtools.models.interaction import ModelRequest, Prompt
from tests.context.planning.test_plan import _snapshot
from tests.context.retrieval.graph.test_typed import _inputs, _view


def test_selection_metadata_provenance_and_model_assembly(tmp_path: Path) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    view = build_repository_map_view(snapshot, core=_view(*inputs[:6]))
    names = {symbol.qualified_name: symbol for symbol in view.symbols}
    symbols = tuple(names[name] for name in ("Child.call", "Base", "helper"))
    option = choose_repository_map_disclosure(
        purpose="Find implementation owners",
        snapshot=snapshot,
        view=view,
        symbols=symbols,
    )
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    disclosure = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    item = disclosure.items[0]
    assert item.native_provenance == symbols
    assert item.resource_addresses == tuple(
        dict.fromkeys(symbol.node.resource_address for symbol in symbols),
    )
    assert item.content_identities == tuple(
        snapshot.resource_at(address).content_identity
        for address in item.resource_addresses
    )
    assert str(snapshot.id) in item.text
    for symbol in symbols:
        assert symbol.qualified_name in item.text
        assert symbol.node.kind.value in item.text
        assert symbol.node.resource_address.value in item.text
        assert symbol.declaration.subject.identity in item.text
        span = symbol.declaration.support.source_range
        for coordinate in (
            span.start_line,
            span.start_column_utf8,
            span.end_line,
            span.end_column_utf8,
        ):
            assert str(coordinate) in item.text
    assert (
        item.text.index("Child.call")
        < item.text.index("Base")
        < item.text.index("helper")
    )
    assert "caller" not in item.text
    assert "Base.run" not in item.text
    assert "def helper(" not in item.text
    assert "class Base:" not in item.text
    assert all(str(value) in item.text for value in item.content_identities)
    request = ModelRequest(Prompt("Keep the task unchanged.", "system"))
    assembled = assemble_context_disclosure_model_request(
        task_request=request,
        context=render_context_disclosure(disclosure),
    )
    assert request.prompt.content == "Keep the task unchanged."
    assert assembled.prompt.role == "system"
    assert item.text in assembled.prompt.content
    assert assembled.settings == request.settings
    coarse = choose_whole_resource_disclosure(
        purpose=option.purpose,
        snapshot=snapshot,
        resource_address=item.resource_addresses[0],
    )
    mixed = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option, coarse),
    )
    assert len(materialize_disclosure_plan(plan=mixed, snapshot=snapshot).items) == 2
    # Disclosure is over retained state, independent of later physical files.
    (tmp_path / item.resource_addresses[0].value).unlink()
    assert option.materialize(snapshot) == item
    with pytest.raises((FrozenInstanceError, AttributeError)):
        option.purpose = "mutated"  # type: ignore[misc]


@pytest.mark.parametrize("change", ["purpose", "order", "selection"])
def test_identity_binds_explicit_choice(tmp_path: Path, change: str) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    view = build_repository_map_view(snapshot, core=_view(*inputs[:6]))
    symbols = view.symbols[:2]
    option = choose_repository_map_disclosure(
        purpose="Orient",
        snapshot=snapshot,
        view=view,
        symbols=symbols,
    )
    again = choose_repository_map_disclosure(
        purpose="Orient",
        snapshot=snapshot,
        view=view,
        symbols=symbols,
    )
    assert again == option
    assert again.identity == option.identity
    altered = choose_repository_map_disclosure(
        purpose="Other" if change == "purpose" else "Orient",
        snapshot=snapshot,
        view=view,
        symbols=tuple(reversed(symbols))
        if change == "order"
        else symbols[:1]
        if change == "selection"
        else symbols,
    )
    assert altered.identity != option.identity


@pytest.mark.parametrize(
    "invalid",
    ["blank", "empty", "repeated", "name", "node", "view"],
)
def test_invalid_selections_fail_closed(tmp_path: Path, invalid: str) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    view = build_repository_map_view(snapshot, core=_view(*inputs[:6]))
    symbol = view.symbols[0]
    selected: tuple[RepositoryMapSymbol, ...] = (symbol,)
    if invalid == "empty":
        selected = ()
    elif invalid == "repeated":
        selected = (symbol, symbol)
    elif invalid == "name":
        selected = (replace(symbol, qualified_name="fabricated"),)
    elif invalid == "node":
        selected = (replace(symbol, node=replace(symbol.node, identity="invented")),)
    elif invalid == "view":
        view = replace(view, symbols=())
    with pytest.raises(ValueError):
        choose_repository_map_disclosure(
            purpose=" " if invalid == "blank" else "Orient",
            snapshot=snapshot,
            view=view,
            symbols=selected,
        )


@pytest.mark.parametrize("change", ["snapshot", "repository", "missing", "content"])
def test_reauthenticate_both_selection_and_materialization(
    tmp_path: Path,
    change: str,
) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    view = build_repository_map_view(snapshot, core=_view(*inputs[:6]))
    symbols = view.symbols[:1]
    option = choose_repository_map_disclosure(
        purpose="Orient",
        snapshot=snapshot,
        view=view,
        symbols=symbols,
    )
    address = symbols[0].node.resource_address
    if change == "snapshot":
        altered = replace(snapshot, id=RepositorySnapshotId("a" * 64))
    elif change == "repository":
        altered = replace(
            snapshot,
            repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000026"),
        )
    elif change == "missing":
        altered = replace(
            snapshot,
            resources=tuple(
                item for item in snapshot.resources if item.address != address
            ),
        )
    else:
        altered = replace(
            snapshot,
            resources=tuple(
                replace(item, content_identity=ContentIdentity("a" * 64))
                if item.address == address
                else item
                for item in snapshot.resources
            ),
        )
    with pytest.raises(ValueError):
        choose_repository_map_disclosure(
            purpose="Orient",
            snapshot=altered,
            view=view,
            symbols=symbols,
        )
    with pytest.raises(ValueError):
        option.materialize(altered)


def test_unicode_async_and_repeated_declared_names_have_exact_occurrences(
    tmp_path: Path,
) -> None:
    text = (
        'async def caf\u00e9():\n    return "hidden body"\n\n'
        "def repeat(): pass\ndef repeat(): pass\nclass Cl\u00e4ss:\n"
        '    async def m\u00e9thod(self): return "secret"\n'
    )
    snapshot = _snapshot(tmp_path, {"unicod\u00e9.py": text})
    address = RepositoryResourceAddress("unicod\u00e9.py")
    functions = derive_python_function_declarations(snapshot, resource_address=address)
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=address,
    )
    core = build_python_graph_view(
        snapshot,
        projection=PythonGraphProjection.TYPED_CORE,
        functions=functions.declarations,
        classes=classes.classes,
        methods=classes.methods,
    )
    view = build_repository_map_view(snapshot, core=core)
    assert len(view.symbols) == 5
    selected = choose_repository_map_disclosure(
        purpose="Unicode orientation",
        snapshot=snapshot,
        view=view,
        symbols=view.symbols,
    )
    item = selected.materialize(snapshot)
    assert "caf\u00e9" in item.text
    assert "Cl\u00e4ss.m\u00e9thod" in item.text
    assert "hidden body" not in item.text
    assert "secret" not in item.text
    assert len({symbol.node.identity for symbol in view.symbols}) == 5
    assert all(
        symbol.declaration.subject.identity in item.text for symbol in view.symbols
    )
    assert item.resource_addresses == (address,)


@pytest.mark.parametrize("change", ["purpose", "symbols", "resources"])
def test_materialization_checks_directly_altered_options(
    tmp_path: Path,
    change: str,
) -> None:
    inputs = _inputs(tmp_path)
    snapshot = inputs[0]
    view = build_repository_map_view(snapshot, core=_view(*inputs[:6]))
    option = choose_repository_map_disclosure(
        purpose="Orient",
        snapshot=snapshot,
        view=view,
        symbols=view.symbols[:1],
    )
    altered = (
        replace(option, purpose=" ")
        if change == "purpose"
        else replace(option, symbols=())
        if change == "symbols"
        else replace(option, resources=())
    )
    with pytest.raises(ValueError):
        altered.materialize(snapshot)
