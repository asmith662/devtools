# Copyright (c) 2026
# ruff: noqa: D103
"""Adversarial lexical binding and scope cases for bounded References."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from devtools.context.python.classes.declarations import (
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    derive_python_function_declarations,
)
from devtools.context.python.imports.declarations import (
    derive_python_import_declarations,
)
from devtools.context.python.references.declarations.bindings import (
    _module_bindings,
    _scope_bindings,
    _unsupported_scope,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from tests.context.python.references.declarations.test_analysis import _snapshot

if TYPE_CHECKING:
    from pathlib import Path


def test_module_binding_inventory_tracks_nested_and_dynamic_syntax(
    tmp_path: Path,
) -> None:
    source = (
        "from missing import *\n"
        "if flag:\n"
        "    def nested():\n        pass\n"
        "    from other import value as alias\n"
        "    import package.module\n"
        "    from third import *\n"
        "globals()\n"
    )
    snapshot = _snapshot(tmp_path, {"src/use.py": source})
    address = RepositoryResourceAddress("src/use.py")
    bindings, uncertain = _module_bindings(
        ast.parse(source),
        derive_python_import_declarations(snapshot, resource_address=address),
        derive_python_function_declarations(
            snapshot,
            resource_address=address,
        ).declarations,
        derive_python_class_method_declarations(
            snapshot,
            resource_address=address,
        ).classes,
    )
    assert uncertain
    assert {binding.name for binding in bindings} >= {
        "nested",
        "alias",
        "package",
    }
    assert all(binding.kind == "other" for binding in bindings)


def test_scope_binding_inventory_catches_parameters_and_local_bindings() -> None:
    tree = ast.parse(
        "def f(a, *rest, **kwargs):\n"
        "    def nested():\n        pass\n"
        "    class Inner:\n        pass\n"
        "    import package.module\n"
        "    from other import value as alias\n"
        "    try:\n        pass\n    except Exception as error:\n        pass\n"
        "    match a:\n"
        "        case {'key': captured, **tail}:\n            pass\n"
        "    [x for x in rest]\n"
        "    local = 1\n",
    )
    function = tree.body[0]
    assert isinstance(function, ast.FunctionDef)
    names = _scope_bindings(function)
    assert {
        "a",
        "rest",
        "kwargs",
        "nested",
        "Inner",
        "package",
        "alias",
        "error",
        "captured",
        "tail",
        "local",
    } <= names.keys()
    assert "x" not in names


def test_scope_assessment_excludes_argument_and_lambda_syntax() -> None:
    tree = ast.parse("def f(x: External=external):\n    value = lambda: external\n")
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    argument_default = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.lineno == 1
    )
    lambda_name = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name | ast.Attribute)
        and isinstance(node.ctx, ast.Load)
        and node.lineno != argument_default.lineno
    )
    assert _unsupported_scope(argument_default, parents)
    assert _unsupported_scope(lambda_name, parents)
    argument_annotation = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "External"
    )
    assert _unsupported_scope(argument_annotation, parents)


def test_star_import_cannot_establish_local_binding() -> None:
    tree = ast.parse("def f():\n    from other import *\n")
    function = tree.body[0]
    assert isinstance(function, ast.FunctionDef)
    assert not _scope_bindings(function)
