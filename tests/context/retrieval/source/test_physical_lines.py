# Copyright (c) 2026
# ruff: noqa: COM812, PLR2004 -- independently specified physical source boundaries
"""Physical-line regression fixtures use real retained source and native parsing."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

import pytest

from devtools.context.planning import (
    SourceSearchDisclosureOption,
    materialize_disclosure_plan,
    plan_disclosures,
)
from tests.context.retrieval.source.test_search import _index

if TYPE_CHECKING:
    from pathlib import Path


SEPARATORS = ("\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029")


@pytest.mark.parametrize("separator", [" ", *SEPARATORS])
@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"])
def test_valid_string_separators_do_not_shift_native_source(
    tmp_path: Path, separator: str, newline: str
) -> None:
    """The original 27-case reproduction has literal, AST-independent expectations."""
    expected = f"def target():{newline}    return 1"
    prefix = f'value = "a{separator}b"{newline}'
    content = prefix + expected
    index = _index(tmp_path, {"source.py": content})
    unit = next(u for u in index.views[1].units if u.qualified_name == "target")
    assert unit.text == expected
    assert unit.start == len(prefix)
    assert unit.end == len(content)
    assert (unit.start_line, unit.end_line) == (2, 3)
    assert unit.resource.content == content
    assert unit.declaration is not None
    assert unit.occurrence is not None
    assert unit.occurrence.source_range == unit.declaration.support.source_range
    assert unit.text == ast.get_source_segment(content, ast.parse(content).body[1])
    disclosure = materialize_disclosure_plan(
        plan=plan_disclosures(
            purpose="Inspect target",
            snapshot=index.snapshot,
            disclosures=(SourceSearchDisclosureOption("Inspect target", unit),),
        ),
        snapshot=index.snapshot,
    )
    assert expected in disclosure.items[0].text
    assert disclosure.items[0].native_provenance is unit


@pytest.mark.parametrize("separator", SEPARATORS)
@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"])
@pytest.mark.parametrize("final_newline", [False, True])
def test_non_python_windows_follow_physical_lines_without_normalization(
    tmp_path: Path, separator: str, newline: str, *, final_newline: bool
) -> None:
    """Unicode separators stay inside independently authored physical lines."""
    physical = [f"line{i} é{separator}尾" + newline for i in range(7)]
    if not final_newline:
        physical[-1] = physical[-1].removesuffix(newline)
    content = "".join(physical)
    index = _index(tmp_path, {"notes.txt": content})
    first, second = index.views[2].units
    assert first.text == "".join(physical[:5])
    assert second.text == "".join(physical[3:])
    assert (first.start_line, first.end_line) == (1, 5)
    assert (second.start_line, second.end_line) == (4, 7)
    assert second.start == len("".join(physical[:3]))
    assert second.end == len(content)
    assert first.resource.content == second.resource.content == content


@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"])
@pytest.mark.parametrize("final_newline", [False, True])
def test_decorated_nested_async_unicode_ranges_remain_exact(
    tmp_path: Path, newline: str, *, final_newline: bool
) -> None:
    """Decorators, indentation and native UTF-8 endpoints survive physical slicing."""
    content = (
        'value = "pré\u2028fix"\n'
        "@decorate\nclass Café:\n"
        "    @(decorate)\n    async def méthode(self):\n"
        '        def nested(): return "尾"\n'
        "        return nested\n"
        'def sibling(): return "unselected"'
    ).replace("\n", newline)
    if final_newline:
        content += newline
    index = _index(tmp_path, {"source.py": content, "empty.py": ""})
    symbols = {u.qualified_name: u for u in index.views[1].units if u.kind == "symbol"}
    method = symbols["Café.méthode"]
    expected = newline.join(
        (
            "@(decorate)",
            "    async def méthode(self):",
            '        def nested(): return "尾"',
            "        return nested",
        )
    )
    assert method.text == expected
    assert (method.start_line, method.end_line) == (4, 7)
    assert method.declaration is not None
    assert method.declaration.support.source_range.start_line == 5
    nested = symbols["Café.méthode.nested"]
    assert nested.text == 'def nested(): return "尾"'
    assert nested.occurrence is not None
    assert nested.occurrence.source_range.end_column_utf8 == len(
        '        def nested(): return "尾"'.encode()
    )
    assert nested.declaration is None
    assert nested.parent_symbol_id == method.id
    assert index.expand(method, to="class") == symbols["Café"]
    assert index.expand(nested, to="file").text == content
    empty = next(
        u for u in index.views[0].units if u.resource.address.value == "empty.py"
    )
    assert empty.text == ""
    assert empty.start_line == empty.end_line == 1
